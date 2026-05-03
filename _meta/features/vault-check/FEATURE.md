---
name: vault-check
version: 2.0
entry: ./vault_check.py
language: python
stdlib_only: true
triggers: ["check", "lint", "audit", "verify", "validate"]
inputs:
  - name: path
    type: path
    required: false
    default: auto-detect vault root from CWD
outputs:
  - name: findings
    type: "text (default) | json (--json)"
  - name: exit_code
    type: integer
exit_codes:
  0: clean (no errors; warnings allowed unless --strict)
  1: at least one error (or any warning if --strict)
  2: internal failure (bad config, bad args, I/O error)
idempotent: true
modifies_git: false
requires_clean_worktree: false
---

## When to use

Before committing any admin change. Before merging any PR that touches notes or `_meta/`.
To diagnose why a wikilink, Foam graph, or daily-note link is broken.

## When NOT to use

To enforce style (prose voice, heading sentence case). That's the author's responsibility, not a linter's.
To check content accuracy — this is a structural auditor, not a fact-checker.

## Invocation

```
python3 _meta/features/vault-check/vault_check.py             # human-readable
python3 _meta/features/vault-check/vault_check.py --strict    # promote warnings to errors
python3 _meta/features/vault-check/vault_check.py --json      # machine-readable
```

Runs in read-only mode. Safe to run any time, including with a dirty worktree.

## Side effects

None. Pure read. Writes nothing. Does not touch git.
