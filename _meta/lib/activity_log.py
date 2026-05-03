#!/usr/bin/env python3
"""
activity_log.py — Append JSONL events to a hidden, gitignored log.

Path: `_meta/maintenance-reports/.activity.jsonl`
  - dot-prefixed (hidden to `ls` by default)
  - inside a gitignored folder (never committed)
  - read only when an admin- or maintenance-authority agent decides it is
    relevant to the current task. No mode file outside those two references
    this log.

Format: one JSON object per line. Schema-less by design — each event type
defines its own fields, minimum required:
    ts     ISO8601 UTC timestamp
    event  short identifier (e.g. "vault_check", "rename-note")

Usage (from Python):
    from activity_log import log_event
    log_event(vault_root, "vault_check", files=624, errors=2, warnings=1238)

Usage (from bash / any CLI):
    python3 _meta/lib/activity_log.py vault_check files=624 errors=2

Failures are swallowed — logging MUST NOT break its callers.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_REL = Path("_meta/maintenance-reports/.activity.jsonl")


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_event(vault_root: Path, event: str, **fields: Any) -> None:
    """Append one JSONL event. Errors are swallowed."""
    try:
        path = vault_root / LOG_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        record: dict[str, Any] = {"ts": _utc_iso(), "event": event}
        record.update(fields)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _coerce(v: str) -> Any:
    """Best-effort int / float / bool / null / string."""
    lv = v.lower()
    if lv in ("true", "false"):
        return lv == "true"
    if lv == "null":
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: activity_log.py <event> [key=value ...]", file=sys.stderr)
        return 2

    event = args[0]
    fields: dict[str, Any] = {}
    for kv in args[1:]:
        if "=" in kv:
            k, v = kv.split("=", 1)
            fields[k] = _coerce(v)

    # Find vault root via config_loader (sibling in _meta/lib/).
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from config_loader import find_vault_root
    log_event(find_vault_root(), event, **fields)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
