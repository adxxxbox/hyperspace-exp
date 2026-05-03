#!/usr/bin/env python3
"""
config_loader.py — Parse _meta/config.jsonc with comment support.

JSONC = JSON with Comments. Supports:
    // line comments
    /* block comments */
and correctly preserves string literals that contain // or /*.

Does NOT support trailing commas (standard json.loads after stripping
comments — keep trailing commas out of config.jsonc).

Standard library only (json, re, pathlib). No external dependencies.

USAGE
    from config_loader import load_config
    cfg = load_config()
    protected_dirs = set(cfg["protected"]["directories"])

    # Or, from the command line, pretty-print the parsed config:
    python3 _meta/lib/config_loader.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

CONFIG_REL_PATH = "_meta/core/config.jsonc"


def find_vault_root(start: Path | None = None) -> Path:
    """Walk up from `start` (or this file) until we find a dir with .git and _meta."""
    p = (start or Path(__file__)).resolve()
    for candidate in [p, *p.parents]:
        if (candidate / ".git").is_dir() and (candidate / "_meta").is_dir():
            return candidate
    raise RuntimeError(
        f"Could not locate vault root starting from {p}. "
        "Expected a directory containing both .git/ and _meta/."
    )


# Regex that matches, in order of alternation:
#   1. A double-quoted string literal (preserved)
#   2. A /* block comment */ (removed)
#   3. A // line comment (removed)
# The string alternative comes first so comments inside strings are not
# accidentally stripped.
_JSONC_PATTERN = re.compile(
    r'("(?:[^"\\]|\\.)*")'  # group 1: double-quoted string
    r"|(/\*[\s\S]*?\*/)"  # group 2: block comment
    r"|(//[^\n]*)",  # group 3: line comment
)


def strip_jsonc_comments(text: str) -> str:
    """Remove // and /* */ comments from a JSONC string, preserving strings."""

    def repl(m: re.Match) -> str:
        # If the match is a string literal (group 1), keep it verbatim.
        # Otherwise (a comment), drop it.
        return m.group(1) if m.group(1) is not None else ""

    return _JSONC_PATTERN.sub(repl, text)


def load_config(vault_root: Path | None = None) -> dict[str, Any]:
    """
    Load and parse _meta/config.jsonc.

    Raises FileNotFoundError if the file is missing,
    ValueError if parsing fails after comment stripping.
    """
    root = vault_root or find_vault_root()
    cfg_path = root / CONFIG_REL_PATH
    if not cfg_path.is_file():
        raise FileNotFoundError(f"config not found at {cfg_path}")
    raw = cfg_path.read_text(encoding="utf-8")
    stripped = strip_jsonc_comments(raw)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"config.jsonc failed to parse as JSON after stripping comments: {e}\n"
            f"Check for trailing commas or unterminated strings."
        ) from e


def main() -> int:
    try:
        cfg = load_config()
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
