# Mode: maintenance

**Authority: maintenance** (between author and admin). May read + write notes. May invoke any read-only or author-scoped feature. May auto-correct frontmatter if `frontmatter.agent_auto_correct` is enabled in `_meta/core/config.jsonc`. May NOT rename files, NOT add/remove top-level folders, NOT change rules, NOT modify `_meta/core/` or `_meta/features/`, NOT run bare git (see `conventions.md §7`).

Loaded when the user asks for a periodic check, cleanup, or routine hygiene work on the vault.

Trigger phrases: "audit", "run vault check", "lint", "run maintenance", "clean up reports", "fix frontmatter", "auto-correct frontmatter", "triage inbox", "health check".

## Standard maintenance pass

1. Run `python3 _meta/features/vault-check/vault_check.py`.
2. Surface to the user: error count, warning count, any `[RECHECK ≥24h]` lines, and the rolled-up M6 counts.
3. If `frontmatter.agent_auto_correct` is `true` AND there are M6 warnings, offer to auto-correct them (see admin.md § Frontmatter auto-correct — same rules: infer `title` from H1/filename, `created` from git-add date; never commit). Otherwise just report.
4. Triage `inbox.md`: surface each entry and suggest the canonical folder per `modes/capture.md`. Do not move; let the user approve.
5. Review `_meta/maintenance-reports/`: note any stale snapshot files (>30 days); ask before deleting.

## Activity log

There is a compact JSONL activity log at

```
_meta/maintenance-reports/.activity.jsonl
```

It is dot-prefixed (hidden from default `ls`) and lives in a gitignored folder. **Do not read it by default.** Consult it only when it is plausibly useful for the current task — for example:

- To see when `vault_check` was last run and what it found.
- To trace a rename — `grep rename-note _meta/maintenance-reports/.activity.jsonl | tail`.
- To investigate why M6 warnings keep re-appearing.

Each line is one JSON object with at minimum `ts` (UTC ISO8601) and `event`. Current writers: `vault_check`, `rename-note`.

## Out of scope in maintenance mode

- Renaming notes → switch to admin mode, use the `rename-note` feature.
- Changing rules → switch to admin mode.
- Archiving finished projects → switch to admin mode.
- Anything that touches `_meta/core/`, `_meta/modes/`, or `_meta/features/` → admin mode.

If you (the agent) find yourself wanting to do one of these, stop and tell the user.
