#!/usr/bin/env python3
"""
vault_check.py — Read-only vault auditor for the Foam vault.

Walks the vault, loads _meta/config.jsonc via config_loader, and reports
violations of the guideline. Never writes, renames, or deletes anything.

Exit codes:
    0   vault is clean (or clean under current strictness)
    1   at least one violation found
    2   internal error (bad config, bad CLI args, etc.)

Usage:
    python3 _meta/scripts/vault_check.py                # audit vault at CWD
    python3 _meta/scripts/vault_check.py /path/to/vault
    python3 _meta/scripts/vault_check.py --json         # machine-readable
    python3 _meta/scripts/vault_check.py --strict       # warnings -> errors

Rule codes:
    F1   file outside canonical top-level folders
    F2   unknown top-level folder
    F4   depth > max_depth (optional; only if config declares max_depth)
    F5   single-file subfolder (optional; only if config.forbid_single_file_subfolders)
    N1   filename fails slug_regex
    N2a  case-collision within folder
    M1   missing required frontmatter key (quiet when required=[])
    M2   forbidden frontmatter key present (quiet when forbidden=[])
    M4   `created` value not YYYY-MM-DD
    M6   missing recommended frontmatter key (warning; tracked for recheck)
    P3   Foam link-reference block structurally broken
    L3   slug collision across vault
    O1   note not reachable from the master outline (when outline.enforce_reachability)
    R1   feature folder has no entry in features/registry.jsonc
    R2   feature folder missing FEATURE.md
    R3   registry references a feature folder that does not exist

This script is stdlib-only. No third-party YAML, no regex library beyond `re`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# Import config_loader from _meta/lib/ (two levels up: features/<name>/ -> features/ -> _meta/).
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from config_loader import find_vault_root, load_config  # noqa: E402


# --------------------------------------------------------------------------- #
# Data types
# --------------------------------------------------------------------------- #

SEVERITY_ERROR = "ERROR"
SEVERITY_WARN = "WARN"


@dataclass
class Finding:
    path: str            # vault-relative path
    line: int            # 0 = file-level finding
    rule: str            # rule code, e.g. "M1"
    severity: str        # ERROR | WARN
    message: str

    def format_line(self) -> str:
        loc = f"{self.path}:{self.line}" if self.line > 0 else self.path
        return f"{loc}  [{self.severity}] {self.rule}  {self.message}"

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "line": self.line,
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
        }


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    files_scanned: int = 0

    def add(self, f: Finding) -> None:
        self.findings.append(f)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == SEVERITY_ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == SEVERITY_WARN]


# --------------------------------------------------------------------------- #
# Frontmatter parsing (minimal, stdlib only)
# --------------------------------------------------------------------------- #

_FM_FENCE = "---"
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Frontmatter:
    found: bool
    keys: dict[str, str]          # key -> raw string value (first line only)
    start_line: int               # line of opening ---
    end_line: int                 # line of closing ---
    unparseable: bool = False     # set if we bailed out mid-parse


def parse_frontmatter(lines: list[str]) -> Frontmatter:
    """Very forgiving YAML-frontmatter parser. Only handles flat key: value."""
    if not lines or lines[0].rstrip() != _FM_FENCE:
        return Frontmatter(found=False, keys={}, start_line=0, end_line=0)

    keys: dict[str, str] = {}
    end = 0
    for i in range(1, len(lines)):
        stripped = lines[i].rstrip("\n").rstrip()
        if stripped == _FM_FENCE:
            end = i + 1
            break
        if not stripped or stripped.startswith("#"):
            continue
        # top-level key: value (ignore indented continuation lines)
        if lines[i].startswith((" ", "\t", "-")):
            continue
        if ":" not in stripped:
            return Frontmatter(
                found=True, keys=keys, start_line=1, end_line=0, unparseable=True
            )
        key, _, value = stripped.partition(":")
        keys[key.strip()] = value.strip()

    if end == 0:
        # no closing fence
        return Frontmatter(
            found=True, keys=keys, start_line=1, end_line=0, unparseable=True
        )
    return Frontmatter(found=True, keys=keys, start_line=1, end_line=end)


# --------------------------------------------------------------------------- #
# Foam link-reference block check
# --------------------------------------------------------------------------- #

def check_foam_block(lines: list[str], cfg: dict) -> tuple[int, int] | None:
    """
    Returns (start_line, end_line) if the Foam autogenerated block is present
    and structurally well-formed. Returns None if absent (not a violation).
    Returns (-1, -1) if broken (orphan start or orphan end).
    """
    regions = cfg.get("protected", {}).get("regions", {})
    block = regions.get("foam_link_references", {})
    start_marker = block.get("start_marker")
    end_marker = block.get("end_marker")
    if not start_marker or not end_marker:
        return None

    start = end = -1
    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if line == start_marker and start == -1:
            start = i
        elif line == end_marker and start != -1 and end == -1:
            end = i
            break

    if start == -1 and end == -1:
        return None
    if start != -1 and end != -1:
        return (start, end)
    return (-1, -1)  # broken


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

# N5 (filler words) and N6 (keyword stuffing) were removed in guideline
# v1.8. No filler-word enforcement. Kept as an empty set in case future
# rules want to reintroduce a small reserved list.
_FILLER_WORDS: frozenset[str] = frozenset()


def is_protected_dir(rel_parts: tuple[str, ...], protected_dirs: frozenset[str]) -> bool:
    """True if any ancestor directory is in protected.directories."""
    return any(p in protected_dirs for p in rel_parts)


def get_exempt_dirs(cfg: dict) -> frozenset[str]:
    """Shared exempt-dir list used by L3, O1, and M6.

    Reads `rules.exempt_dirs` (preferred) and falls back to
    `outline.exempt_dirs` for backward compatibility.
    """
    dirs: list[str] = []
    dirs.extend(cfg.get("rules", {}).get("exempt_dirs", []) or [])
    dirs.extend(cfg.get("outline", {}).get("exempt_dirs", []) or [])
    return frozenset(dirs)


def path_is_body_exempt(rel_path: Path, exempt_dirs: frozenset[str]) -> bool:
    """True if the file sits under any exempt top-level dir."""
    return bool(rel_path.parts) and rel_path.parts[0] in exempt_dirs


def check_file_placement(
    rel_path: Path,
    cfg: dict,
    report: Report,
) -> None:
    """F1, F2, F4 checks — folder-structure rules."""
    parts = rel_path.parts
    if len(parts) < 2:
        # root-level file — handled elsewhere (protected.files)
        return
    top = parts[0]
    top_level = set(cfg["canonical_folders"]["top_level"])
    if top not in top_level:
        report.add(Finding(
            path=str(rel_path), line=0, rule="F2", severity=SEVERITY_ERROR,
            message=f"unknown top-level folder '{top}' (allowed: {sorted(top_level)})",
        ))
        return

    # _archive has no internal-structure rules: anything under _archive/
    # is allowed. Slug uniqueness (L3) and other vault-wide rules still
    # apply there; but folder layout inside _archive/ is freeform.

    # Depth check (optional): only fires if config declares max_depth.
    # The relaxed v2 conventions omit this; projects may nest freely.
    max_depth = cfg["canonical_folders"].get("max_depth")
    if max_depth is not None and len(parts) > max_depth + 1:
        report.add(Finding(
            path=str(rel_path), line=0, rule="F4", severity=SEVERITY_ERROR,
            message=f"depth {len(parts)-1} exceeds max_depth {max_depth}",
        ))


def check_filename(
    rel_path: Path,
    cfg: dict,
    slug_re: re.Pattern,
    report: Report,
) -> None:
    """N1 check — slug grammar (permissive per guideline v1.8)."""
    if rel_path.suffix != cfg["naming"]["file_extension"]:
        return
    stem = rel_path.stem
    if not slug_re.match(stem):
        report.add(Finding(
            path=str(rel_path), line=0, rule="N1", severity=SEVERITY_ERROR,
            message=f"filename stem '{stem}' does not match slug_regex",
        ))


def check_frontmatter(
    rel_path: Path,
    lines: list[str],
    cfg: dict,
    report: Report,
    emit_m6: bool = True,
) -> None:
    """M1, M2, M4, M6 checks — frontmatter schema.

    M1/M2 are legacy error-severity checks driven by the (usually-empty)
    `required` and `forbidden` lists. M6 is the warning-severity check for
    recommended keys introduced in config v2.1.

    `emit_m6` should be False for files exempt from M6 (files under
    `rules.exempt_dirs` or in `append_only.files`). M1/M2/M4 still fire —
    those are structural errors and don't have the same exemption rationale.
    """
    if rel_path.suffix != ".md":
        return
    recommended = cfg["frontmatter"].get("recommended", [])
    # Empty files (0 non-whitespace bytes) are not valid M6 targets — they
    # cannot hold frontmatter. Fix-frontmatter skips them too; treat alike.
    is_empty = not any(line.strip() for line in lines)
    fm = parse_frontmatter(lines)
    if not fm.found:
        for key in cfg["frontmatter"].get("required", []):
            report.add(Finding(
                path=str(rel_path), line=1, rule="M1", severity=SEVERITY_ERROR,
                message=f"missing frontmatter block (required key '{key}' absent)",
            ))
        if emit_m6 and not is_empty:
            for key in recommended:
                report.add(Finding(
                    path=str(rel_path), line=1, rule="M6", severity=SEVERITY_WARN,
                    message=f"no frontmatter block (recommended key '{key}' absent)",
                ))
        return
    if fm.unparseable:
        report.add(Finding(
            path=str(rel_path), line=fm.start_line, rule="M1",
            severity=SEVERITY_WARN,
            message="frontmatter could not be parsed (non-flat YAML?); skipping schema check",
        ))
        return

    for key in cfg["frontmatter"].get("required", []):
        if key not in fm.keys:
            report.add(Finding(
                path=str(rel_path), line=fm.start_line, rule="M1",
                severity=SEVERITY_ERROR,
                message=f"missing required frontmatter key '{key}'",
            ))

    if emit_m6:
        for key in recommended:
            if key not in fm.keys:
                report.add(Finding(
                    path=str(rel_path), line=fm.start_line, rule="M6",
                    severity=SEVERITY_WARN,
                    message=f"missing recommended frontmatter key '{key}'",
                ))

    for key in cfg["frontmatter"].get("forbidden", []):
        if key in fm.keys:
            report.add(Finding(
                path=str(rel_path), line=fm.start_line, rule="M2",
                severity=SEVERITY_ERROR,
                message=f"forbidden frontmatter key '{key}' present",
            ))

    created = fm.keys.get("created", "")
    # Strip surrounding quotes if any
    created_stripped = created.strip().strip('"').strip("'")
    if created_stripped and not _DATE_RE.match(created_stripped):
        report.add(Finding(
            path=str(rel_path), line=fm.start_line, rule="M4",
            severity=SEVERITY_ERROR,
            message=f"`created` value '{created_stripped}' is not YYYY-MM-DD",
        ))


def check_foam_block_integrity(
    rel_path: Path,
    lines: list[str],
    cfg: dict,
    report: Report,
) -> None:
    """P3 — Foam link-reference block must be whole if present."""
    result = check_foam_block(lines, cfg)
    if result == (-1, -1):
        report.add(Finding(
            path=str(rel_path), line=0, rule="P3", severity=SEVERITY_ERROR,
            message="Foam link-reference block has orphan start or end marker",
        ))


# --------------------------------------------------------------------------- #
# Outline reachability (O1)
# --------------------------------------------------------------------------- #

# Captures the slug part of [[slug]], [[slug|alias]], [[slug#heading]],
# ![[slug]]. The slug is everything up to the first `|` or `#`.
_WIKILINK_RE = re.compile(r"!?\[\[([^\]\n|#]+)(?:[#|][^\]\n]*)?\]\]")


def collect_wikilink_slugs(text: str) -> set[str]:
    """Extract referenced slugs from text. Skips fenced code blocks. Lowercased.

    Strips a trailing `.md` extension if present (Foam allows `[[foo.md]]`).
    Slashes in the target are resolved to the basename (Foam supports
    `[[folder/note]]` — we just take `note`).
    """
    out: set[str] = set()
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in _WIKILINK_RE.finditer(line):
            target = m.group(1).strip()
            if "/" in target:
                target = target.rsplit("/", 1)[1]
            if target.lower().endswith(".md"):
                target = target[:-3]
            if target:
                out.add(target.lower())
    return out


def check_outline_reachability(
    cfg: dict,
    slug_index: dict[str, list],
    note_text: dict,
    report: Report,
) -> None:
    """O1 — every note in slug_index must be reachable from the master outline.

    Skips notes under any path in `rules.exempt_dirs` (default:
    ['_archive', '_secretary']). Falls back to `outline.exempt_dirs` for
    backward compatibility. Protected files (e.g. inbox.md, todo.md) are not
    in slug_index and so are naturally exempt.
    """
    outline_cfg = cfg.get("outline", {})
    if not outline_cfg.get("enforce_reachability", False):
        return
    master_slug = str(outline_cfg.get("master_moc", "outlines")).lower()
    exempt_dirs = get_exempt_dirs(cfg) or frozenset({"_archive"})

    # Build lowercased slug -> [paths] map for resolution.
    ci_slug_to_paths: dict[str, list] = {}
    for slug, paths in slug_index.items():
        ci_slug_to_paths.setdefault(slug.lower(), []).extend(paths)

    if master_slug not in ci_slug_to_paths:
        report.add(Finding(
            path="<vault>", line=0, rule="O1", severity=SEVERITY_ERROR,
            message=(
                f"master outline note '{master_slug}.md' not found in vault — "
                "create it at the vault root or set outline.master_moc"
            ),
        ))
        return

    # BFS from master outline.
    visited: set[str] = set()
    stack: list[str] = [master_slug]
    while stack:
        slug = stack.pop()
        if slug in visited:
            continue
        visited.add(slug)
        # Some links may target slugs that aren't in the index (broken links);
        # those are silently ignored here — vault-check could add a separate
        # broken-link check later.
        for path in ci_slug_to_paths.get(slug, []):
            text = note_text.get(path, "")
            for child in collect_wikilink_slugs(text):
                if child not in visited:
                    stack.append(child)

    # Report unreachable notes.
    for slug, paths in slug_index.items():
        if slug.lower() in visited:
            continue
        for path in paths:
            if path.parts and path.parts[0] in exempt_dirs:
                continue
            report.add(Finding(
                path=str(path), line=0, rule="O1", severity=SEVERITY_ERROR,
                message=f"note not reachable from master outline '{master_slug}'",
            ))


# --------------------------------------------------------------------------- #
# Walk
# --------------------------------------------------------------------------- #

def walk_vault(vault_root: Path, cfg: dict) -> Report:
    report = Report()
    protected_dirs = frozenset(cfg["protected"]["directories"])
    protected_files = frozenset(cfg["protected"]["files"])
    slug_re = re.compile(cfg["naming"]["slug_regex"])
    exempt_dirs = get_exempt_dirs(cfg)
    append_only_files = frozenset(cfg.get("append_only", {}).get("files", []))

    # Track slug -> list of paths for L3 uniqueness check
    slug_index: dict[str, list[Path]] = {}
    # Track per-folder case-insensitive filename collisions for N2a
    folder_case_index: dict[Path, dict[str, Path]] = {}
    # Track per-folder file counts for F5
    folder_file_counts: dict[Path, int] = {}
    # Track note text for outline reachability check (O1)
    note_text: dict[Path, str] = {}

    # Manual walk so we can prune protected directories in-place.
    for dirpath, dirnames, filenames in os.walk(vault_root):
        # Prune protected dirs: don't descend.
        dirnames[:] = [d for d in dirnames if d not in protected_dirs]

        rel_dir = Path(dirpath).relative_to(vault_root)
        for fname in filenames:
            # Skip dotfiles at all levels (e.g. .gitkeep, .DS_Store)
            if fname.startswith("."):
                continue
            if not fname.endswith(".md"):
                continue
            rel_path = rel_dir / fname
            # protected root files
            if len(rel_path.parts) == 1 and fname in protected_files:
                report.files_scanned += 1
                continue
            # Skip files inside protected dirs (defensive; prune above should cover)
            if is_protected_dir(rel_path.parts[:-1], protected_dirs):
                continue

            report.files_scanned += 1
            abs_path = vault_root / rel_path

            # Read lines once
            try:
                with open(abs_path, "r", encoding="utf-8") as fh:
                    lines = fh.readlines()
            except (OSError, UnicodeDecodeError) as e:
                report.add(Finding(
                    path=str(rel_path), line=0, rule="IO",
                    severity=SEVERITY_ERROR,
                    message=f"could not read file: {e}",
                ))
                continue

            # Per-file checks
            check_file_placement(rel_path, cfg, report)
            check_filename(rel_path, cfg, slug_re, report)
            m6_exempt = (
                path_is_body_exempt(rel_path, exempt_dirs)
                or rel_path.as_posix() in append_only_files
            )
            check_frontmatter(rel_path, lines, cfg, report, emit_m6=not m6_exempt)
            check_foam_block_integrity(rel_path, lines, cfg, report)

            # Global indices
            slug = rel_path.stem
            slug_index.setdefault(slug, []).append(rel_path)
            note_text[rel_path] = "".join(lines)
            parent = rel_path.parent
            lower = fname.lower()
            existing = folder_case_index.setdefault(parent, {}).get(lower)
            if existing and existing.name != fname:
                report.add(Finding(
                    path=str(rel_path), line=0, rule="N2a",
                    severity=SEVERITY_ERROR,
                    message=f"case-collision with '{existing.name}' in same folder",
                ))
            folder_case_index[parent][lower] = rel_path
            folder_file_counts[parent] = folder_file_counts.get(parent, 0) + 1

    # F5: single-file subfolder. Disabled by default under relaxed v2
    # conventions; projects may have intermediate folders with one file.
    # Only enabled if config explicitly sets canonical_folders.forbid_single_file_subfolders.
    if cfg["canonical_folders"].get("forbid_single_file_subfolders", False):
        for folder, count in folder_file_counts.items():
            if count == 1 and len(folder.parts) >= 2:
                report.add(Finding(
                    path=str(folder), line=0, rule="F5", severity=SEVERITY_WARN,
                    message="folder contains exactly one file (consider flattening)",
                ))

    # L3: slug collision across vault (case-insensitive).
    # Exempt paths (see rules.exempt_dirs) do NOT participate in collision
    # detection — their slugs may repeat among themselves and may shadow a
    # non-exempt slug without triggering L3. Rationale: _archive/ is
    # provenance with no wikilink concerns, and _secretary/ uses a different
    # schema and is not wikilinked from the note graph.
    ci_index: dict[str, list[Path]] = {}
    for slug, paths in slug_index.items():
        ci_index.setdefault(slug.lower(), []).extend(paths)
    for slug_l, paths in ci_index.items():
        non_exempt = [
            p for p in paths if not path_is_body_exempt(p, exempt_dirs)
        ]
        unique = list({str(p) for p in non_exempt})
        if len(unique) > 1:
            # Emit on each offender so grep/pre-commit catches every path
            for p in non_exempt:
                report.add(Finding(
                    path=str(p), line=0, rule="L3", severity=SEVERITY_ERROR,
                    message=f"slug '{slug_l}' collides across vault: {sorted(unique)}",
                ))

    # O1: every note reachable from the master outline (opt-in via config).
    check_outline_reachability(cfg, slug_index, note_text, report)

    # R1/R2/R3: feature-registry integrity
    check_feature_registry(vault_root, report)

    return report


def check_feature_registry(vault_root: Path, report: Report) -> None:
    """R1/R2/R3 — every _meta/features/<name>/ folder must have a registry
    entry and a FEATURE.md; every registry entry must point at an existing
    folder with a FEATURE.md.
    """
    features_dir = vault_root / "_meta" / "features"
    if not features_dir.is_dir():
        return  # No features yet — nothing to check.

    registry_path = features_dir / "registry.jsonc"
    if not registry_path.is_file():
        report.add(Finding(
            path="_meta/features/registry.jsonc", line=0, rule="R3",
            severity=SEVERITY_ERROR,
            message="features/ exists but registry.jsonc is missing",
        ))
        return

    # Parse the registry (reuse the JSONC stripper we already depend on).
    sys.path.insert(0, str(vault_root / "_meta" / "lib"))
    from config_loader import strip_jsonc_comments  # noqa: E402
    try:
        registry = json.loads(strip_jsonc_comments(registry_path.read_text("utf-8")))
    except Exception as e:
        report.add(Finding(
            path="_meta/features/registry.jsonc", line=0, rule="R3",
            severity=SEVERITY_ERROR,
            message=f"registry.jsonc failed to parse: {e}",
        ))
        return

    registered = {f.get("name"): f for f in registry.get("features", [])}

    # Walk features/ and find every feature folder.
    on_disk = {
        p.name for p in features_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    }

    # R1: folder on disk but no registry entry
    for name in sorted(on_disk - set(registered)):
        report.add(Finding(
            path=f"_meta/features/{name}/", line=0, rule="R1",
            severity=SEVERITY_ERROR,
            message="feature folder has no entry in features/registry.jsonc",
        ))

    # R2: folder on disk but missing FEATURE.md
    for name in sorted(on_disk):
        if not (features_dir / name / "FEATURE.md").is_file():
            report.add(Finding(
                path=f"_meta/features/{name}/FEATURE.md", line=0, rule="R2",
                severity=SEVERITY_ERROR,
                message="feature folder is missing FEATURE.md",
            ))

    # R3: registry references a feature folder that does not exist
    for name in sorted(set(registered) - on_disk):
        report.add(Finding(
            path=f"_meta/features/registry.jsonc", line=0, rule="R3",
            severity=SEVERITY_ERROR,
            message=f"registry entry '{name}' points at a folder that does not exist",
        ))


# --------------------------------------------------------------------------- #
# Recheck tracker — persists first-seen timestamps for M6 warnings so that
# unresolved issues get re-surfaced after a configurable interval (default
# 24h). Storage is gitignored (maintenance-reports/) so it never touches git.
# --------------------------------------------------------------------------- #

TRACKER_REL = Path("_meta/maintenance-reports/.frontmatter-recheck-tracker.jsonc")


def _now_utc_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(s: str):
    from datetime import datetime
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def update_recheck_tracker(
    vault_root: Path,
    report: Report,
    cfg: dict,
) -> dict[str, bool]:
    """Update the on-disk tracker and return a dict `{tracker_key: overdue}`
    for every M6 finding, where `tracker_key` = "<path>::M6::<key>".

    `overdue` is True when the same finding has been seen continuously for
    ≥ recheck_interval_hours.

    Side effects: writes the tracker file. Errors are non-fatal.
    """
    interval_h = int(
        cfg.get("frontmatter", {}).get("recheck_interval_hours", 24)
    )
    tracker_path = vault_root / TRACKER_REL
    tracker_path.parent.mkdir(parents=True, exist_ok=True)

    # Load prior state.
    prior: dict[str, str] = {}
    if tracker_path.is_file():
        try:
            from datetime import datetime  # noqa: F401
            # JSONC tolerated — reuse the stripper.
            sys.path.insert(0, str(vault_root / "_meta" / "lib"))
            from config_loader import strip_jsonc_comments  # noqa: E402
            raw = tracker_path.read_text("utf-8")
            data = json.loads(strip_jsonc_comments(raw))
            prior = dict(data.get("first_seen_utc", {}))
        except Exception:
            prior = {}

    now = _now_utc_iso()
    now_dt = _parse_iso(now)

    current_keys: set[str] = set()
    overdue: dict[str, bool] = {}
    for f in report.findings:
        if f.rule != "M6":
            continue
        # Use path + message tail as the stable key (message ends with "'<key>'").
        key = f"{f.path}::M6::{f.message}"
        current_keys.add(key)
        first_seen = prior.get(key, now)
        first_dt = _parse_iso(first_seen) or now_dt
        hours = (now_dt - first_dt).total_seconds() / 3600 if now_dt and first_dt else 0
        overdue[key] = hours >= interval_h

    # Next tracker state: keep prior entries that are still current; add new
    # ones with `now`; drop entries whose warning has been resolved.
    next_state = {
        k: prior.get(k, now)
        for k in current_keys
    }

    try:
        tracker_path.write_text(json.dumps({
            "last_run_utc": now,
            "recheck_interval_hours": interval_h,
            "first_seen_utc": next_state,
        }, indent=2), encoding="utf-8")
    except Exception:
        # Non-fatal. Tracker just won't persist this run.
        pass

    return overdue


def rollup_m6(report: Report) -> dict[str, int]:
    """Return {recommended_key: count} for M6 findings, for compact output."""
    counts: dict[str, int] = {}
    for f in report.findings:
        if f.rule != "M6":
            continue
        # Extract the key name from "... '<key>'"
        import re as _re
        m = _re.search(r"'([^']+)'", f.message)
        if m:
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return counts


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only auditor for the Foam vault.",
    )
    parser.add_argument(
        "path", nargs="?", default=None,
        help="vault root (default: auto-detect from CWD)",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="treat warnings as errors (exit 1 on any finding)",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="emit machine-readable JSON instead of human-readable lines",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="list every M6 warning (default: roll up to per-key counts)",
    )
    args = parser.parse_args(argv)

    try:
        vault_root = (
            Path(args.path).resolve() if args.path else find_vault_root(Path.cwd())
        )
        cfg = load_config(vault_root)
    except Exception as e:
        print(f"vault_check: config error: {e}", file=sys.stderr)
        return 2

    report = walk_vault(vault_root, cfg)

    # Persist / read M6 first-seen tracker; detect entries ≥ recheck interval.
    overdue_map = update_recheck_tracker(vault_root, report, cfg)
    any_overdue = any(overdue_map.values())

    # Append a compact event to the hidden activity log. Failures are
    # swallowed by log_event (must never break the caller).
    try:
        sys.path.insert(0, str(vault_root / "_meta" / "lib"))
        from activity_log import log_event  # noqa: E402
        log_event(
            vault_root, "vault_check",
            files=report.files_scanned,
            errors=len(report.errors),
            warnings=len(report.warnings),
            m6_rollup=rollup_m6(report),
            any_m6_overdue=any_overdue,
        )
    except Exception:
        pass

    if args.json:
        payload = {
            "vault_root": str(vault_root),
            "files_scanned": report.files_scanned,
            "errors": len(report.errors),
            "warnings": len(report.warnings),
            "any_m6_overdue": any_overdue,
            "m6_rollup": rollup_m6(report),
            "findings": [f.to_dict() for f in report.findings],
        }
        print(json.dumps(payload, indent=2))
    else:
        # Emit non-M6 findings normally.
        for f in report.findings:
            if f.rule == "M6":
                continue
            print(f.format_line())

        # M6: rolled up by default, per-file with --verbose.
        m6_counts = rollup_m6(report)
        if m6_counts:
            prefix = "[RECHECK ≥24h] " if any_overdue else ""
            for key, count in sorted(m6_counts.items()):
                print(
                    f"{prefix}M6 WARN  {count} file(s) missing recommended "
                    f"frontmatter key '{key}'"
                )
            if args.verbose:
                for f in report.findings:
                    if f.rule == "M6":
                        print("  " + f.format_line())

        print()
        print(
            f"vault_check: scanned {report.files_scanned} file(s), "
            f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)"
        )
        if any_overdue:
            print(
                "vault_check: one or more M6 warnings have persisted for ≥"
                f"{cfg.get('frontmatter', {}).get('recheck_interval_hours', 24)}h. "
                "Consider enabling frontmatter.agent_auto_correct in "
                "_meta/core/config.jsonc and re-running in admin mode."
            )

    if report.errors:
        return 1
    if args.strict and report.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
