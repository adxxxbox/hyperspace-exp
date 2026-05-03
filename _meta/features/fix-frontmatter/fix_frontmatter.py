#!/usr/bin/env python3
"""
fix_frontmatter.py — Backfill missing `title` and `created` frontmatter keys.

Walks the vault, finds .md files missing either `title` or `created` in their
YAML frontmatter, and adds the missing keys using deterministic inference:

    title   -> first H1 (`# ...`) if present, else filename stem
    created -> git add date (`git log --diff-filter=A --follow --format=%as`),
               else OS birth time (`st_birthtime` on macOS / BSD), else today

Preserves existing frontmatter verbatim — only adds missing keys. Files that
already have both keys are left untouched (idempotent).

Skips:
  - Everything under `protected.directories` from config (.git, .foam, .vscode,
    .claude, attachments, node_modules, _meta).
  - `_archive/` and `_secretary/` (the former has no outline concerns; the
    latter uses HTML-comment entry headers, not YAML frontmatter).
  - Files listed in `append_only.files` from config (inbox.md, todo.md) — they
    are append-only by design; prepending a frontmatter block would violate
    the append-only contract.
  - Empty files (0 non-whitespace bytes).

Default is dry-run. Pass `--apply` to actually write.

Stdlib only. No git operations.

USAGE
    python3 _meta/features/fix-frontmatter/fix_frontmatter.py
    python3 _meta/features/fix-frontmatter/fix_frontmatter.py --apply
    python3 _meta/features/fix-frontmatter/fix_frontmatter.py --apply --path 3-resources/
    python3 _meta/features/fix-frontmatter/fix_frontmatter.py --apply --verbose
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

# Make _meta/lib importable.
_HERE = Path(__file__).resolve().parent
_VAULT_LIB = _HERE.parent.parent / "lib"
sys.path.insert(0, str(_VAULT_LIB))
from config_loader import find_vault_root, load_config  # noqa: E402


# Hard-coded exempt dirs in addition to protected dirs from config.
# _archive/ has no outline/frontmatter concerns; _secretary/ uses HTML-comment
# entry headers, not YAML frontmatter.
EXTRA_EXEMPT_DIRS = {"_archive", "_secretary"}

FRONTMATTER_FENCE = "---"
RECOMMENDED_KEYS = ("title", "created")


@dataclass
class FileResult:
    path: Path
    action: str  # "updated", "unchanged", "skipped"
    reason: str = ""
    added_keys: tuple[str, ...] = ()


def is_exempt(rel_path: Path, exempt_top_level: set[str]) -> bool:
    """True if this path sits under any exempt top-level directory."""
    parts = rel_path.parts
    if not parts:
        return False
    return parts[0] in exempt_top_level


def parse_frontmatter(text: str) -> tuple[dict[str, str], int]:
    """
    Parse YAML frontmatter at the top of `text`.

    Returns (keys_present, body_start_offset_in_lines).

    - keys_present is a shallow dict of top-level scalar keys. Values are kept
      as raw strings (we only care about presence, not value).
    - body_start_offset_in_lines is the line index where content after the
      closing `---` begins (0 if no frontmatter).

    This is NOT a full YAML parser — it only handles top-level `key: value`
    lines between opening and closing `---` fences. Nested structures are
    ignored (their keys are still recorded).
    """
    lines = text.splitlines(keepends=False)
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        return {}, 0

    keys: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == FRONTMATTER_FENCE:
            # Found closing fence.
            return keys, i + 1
        # Only match top-level scalar keys: `key: value` (not indented).
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m:
            keys[m.group(1)] = m.group(2).strip()

    # No closing fence found — malformed frontmatter. Treat as no frontmatter.
    return {}, 0


def find_first_h1(text: str, body_start: int) -> str | None:
    """Find the first `# Heading` line starting at body_start. Return the text."""
    lines = text.splitlines(keepends=False)
    for line in lines[body_start:]:
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def git_add_date(vault_root: Path, rel_path: Path) -> str | None:
    """Return the ISO date (YYYY-MM-DD) when the file was first added to git, or None."""
    try:
        out = subprocess.run(
            [
                "git",
                "-C",
                str(vault_root),
                "log",
                "--diff-filter=A",
                "--follow",
                "--format=%as",
                "--",
                str(rel_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    for line in out.stdout.splitlines():
        line = line.strip()
        if line:
            # %as emits YYYY-MM-DD already.
            return line
    return None


def os_birth_date(abs_path: Path) -> str | None:
    """Return the OS birth time as YYYY-MM-DD, if available (macOS/BSD)."""
    try:
        st = abs_path.stat()
    except OSError:
        return None
    ts = getattr(st, "st_birthtime", None)
    if ts is None or ts <= 0:
        return None
    try:
        return date.fromtimestamp(ts).isoformat()
    except (OSError, OverflowError, ValueError):
        return None


def infer_created(vault_root: Path, rel_path: Path) -> str:
    """Fallback chain: git add date -> OS birth time -> today."""
    v = git_add_date(vault_root, rel_path)
    if v:
        return v
    v = os_birth_date(vault_root / rel_path)
    if v:
        return v
    return date.today().isoformat()


def infer_title(text: str, body_start: int, filename_stem: str) -> str:
    h1 = find_first_h1(text, body_start)
    if h1:
        return h1
    return filename_stem


def yaml_quote_if_needed(value: str) -> str:
    """Quote a value for YAML if it contains characters that could confuse a parser."""
    # Keep it simple: quote if it starts/ends with whitespace, contains a colon
    # followed by a space, or looks like a YAML special value.
    needs_quote = (
        value != value.strip()
        or ": " in value
        or value.startswith(("!", "&", "*", "{", "[", "#", "|", ">", "%", "@", "`"))
        or value.lower() in {"true", "false", "null", "yes", "no", "~"}
    )
    if not needs_quote:
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_new_content(
    text: str, existing_keys: dict[str, str], body_start: int, additions: dict[str, str]
) -> str:
    """
    Return the file text with `additions` inserted into the frontmatter.

    - If the file had frontmatter (body_start > 0), insert the new key lines
      immediately before the closing `---`.
    - If it had no frontmatter, prepend a new frontmatter block.
    """
    # Preserve original line ending style.
    newline = "\n"
    if "\r\n" in text:
        newline = "\r\n"

    new_lines = [
        f"{k}: {yaml_quote_if_needed(v)}" for k, v in additions.items()
    ]

    if body_start > 0:
        # Insert before the closing fence.
        lines = text.split(newline) if newline in text else text.splitlines(keepends=False)
        # Recompute split with proper newline handling — splitlines drops the
        # trailing empty string after a final newline; use split to preserve it.
        lines = text.split(newline)
        # Find the closing fence index (body_start - 1 refers to the line AFTER
        # the fence in the old scheme; recompute here to be safe).
        fence_idx = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == FRONTMATTER_FENCE:
                fence_idx = i
                break
        if fence_idx is None:
            # Should not happen if body_start > 0, but fall through safely.
            fence_idx = 1
        new_lines_full = lines[:fence_idx] + new_lines + lines[fence_idx:]
        return newline.join(new_lines_full)

    # No existing frontmatter — prepend a new block.
    block = [FRONTMATTER_FENCE] + new_lines + [FRONTMATTER_FENCE, ""]
    prefix = newline.join(block)
    if text.startswith(newline):
        return prefix + text
    return prefix + newline + text


def process_file(
    abs_path: Path,
    rel_path: Path,
    vault_root: Path,
    apply: bool,
) -> FileResult:
    try:
        raw_bytes = abs_path.read_bytes()
    except OSError as e:
        return FileResult(rel_path, "skipped", reason=f"read_error:{e}")

    if not raw_bytes.strip():
        return FileResult(rel_path, "skipped", reason="empty_file")

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return FileResult(rel_path, "skipped", reason="not_utf8")

    existing_keys, body_start = parse_frontmatter(text)
    missing = [k for k in RECOMMENDED_KEYS if k not in existing_keys or not existing_keys[k]]
    if not missing:
        return FileResult(rel_path, "unchanged")

    additions: dict[str, str] = {}
    if "title" in missing:
        additions["title"] = infer_title(text, body_start, abs_path.stem)
    if "created" in missing:
        additions["created"] = infer_created(vault_root, rel_path)

    new_text = build_new_content(text, existing_keys, body_start, additions)
    if new_text == text:
        return FileResult(rel_path, "unchanged")

    if apply:
        try:
            abs_path.write_text(new_text, encoding="utf-8")
        except OSError as e:
            return FileResult(rel_path, "skipped", reason=f"write_error:{e}")

    return FileResult(rel_path, "updated", added_keys=tuple(additions.keys()))


def walk_vault(
    vault_root: Path,
    exempt_top_level: set[str],
    exempt_files: set[str],
    subpath: Path | None,
) -> list[Path]:
    """Walk the vault (or subpath) and return a sorted list of .md files, relative to vault_root.

    `exempt_files` is a set of vault-relative POSIX paths that must always be
    skipped (e.g. append-only files like inbox.md and todo.md).
    """
    start = vault_root / subpath if subpath else vault_root
    if not start.exists():
        raise SystemExit(f"error: path does not exist: {start}")

    results: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(start):
        dirpath_p = Path(dirpath)
        # Prune exempt top-level dirs when at the vault root. (If the user
        # specified --path inside an exempt dir, honor the explicit scope —
        # but the top-level prune only applies when walking the whole vault.)
        try:
            rel_dir = dirpath_p.relative_to(vault_root)
        except ValueError:
            rel_dir = Path(".")
        if rel_dir == Path(".") and subpath is None:
            dirnames[:] = [d for d in dirnames if d not in exempt_top_level]

        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            abs_path = dirpath_p / fn
            rel = abs_path.relative_to(vault_root)
            if subpath is None and is_exempt(rel, exempt_top_level):
                continue
            if rel.as_posix() in exempt_files:
                continue
            results.append(rel)
    results.sort()
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Backfill missing `title` and `created` frontmatter keys."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write changes to disk (default: dry-run, preview only)",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="vault-relative subtree to limit the run to (default: whole vault)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print per-file actions",
    )
    args = parser.parse_args(argv)

    try:
        vault_root = find_vault_root()
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    cfg = load_config(vault_root)
    protected_dirs = set(cfg.get("protected", {}).get("directories", []))
    exempt_top_level = protected_dirs | EXTRA_EXEMPT_DIRS
    append_only_files = set(cfg.get("append_only", {}).get("files", []))

    subpath = Path(args.path) if args.path else None
    files = walk_vault(vault_root, exempt_top_level, append_only_files, subpath)

    updated: list[FileResult] = []
    unchanged: list[FileResult] = []
    skipped: list[FileResult] = []

    for rel in files:
        abs_path = vault_root / rel
        result = process_file(abs_path, rel, vault_root, args.apply)
        if result.action == "updated":
            updated.append(result)
        elif result.action == "unchanged":
            unchanged.append(result)
        else:
            skipped.append(result)

        if args.verbose:
            if result.action == "updated":
                keys = ",".join(result.added_keys)
                print(f"  updated  {rel}  (+{keys})")
            elif result.action == "skipped":
                print(f"  skipped  {rel}  ({result.reason})")

    mode_str = "APPLY" if args.apply else "DRY-RUN"
    print(f"\nfix_frontmatter [{mode_str}]: scanned {len(files)} file(s)")
    print(f"  updated:   {len(updated)}")
    print(f"  unchanged: {len(unchanged)}")
    print(f"  skipped:   {len(skipped)}")

    if skipped and not args.verbose:
        # Roll up skip reasons.
        reasons: dict[str, int] = {}
        for r in skipped:
            k = r.reason.split(":", 1)[0]
            reasons[k] = reasons.get(k, 0) + 1
        print("  skipped breakdown:")
        for k, v in sorted(reasons.items(), key=lambda kv: -kv[1]):
            print(f"    {k}: {v}")

    if not args.apply and updated:
        print("\n(dry-run — no files were written. re-run with --apply to persist.)")
    elif args.apply and updated:
        print("\nDone. Review with `git diff`, then commit manually.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
