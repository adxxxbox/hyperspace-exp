# Mode: admin

**Authority: admin (highest).** May read + write notes, touch structure, edit `_meta/`, invoke any feature. **Still does not run bare git commands** unless the user explicitly asks in the current turn (see `conventions.md §7`). Invoking a registry feature with `modifies_git: true` (e.g. `rename-note`) IS explicit authorization.

Loaded when the user wants to reorganize, rename, archive, add a feature, or amend the rules themselves.

Trigger phrases: "rename", "move", "archive", "delete", "reorganize", "add a script", "add a feature", "change the rules", "amend the guideline", or any request that touches `_meta/core/`, `_meta/modes/`, or `_meta/features/`.

(Routine audits and cleanups — "audit", "run vault check", "clean up reports", "fix frontmatter" — load `_meta/modes/maintenance.md` instead. Admin is for structural/governance work.)

## Rule of engagement

Admin changes affect shared state. Before acting:

1. Is the working tree clean? If not, pause and tell the user.
2. Is the action reversible via `git revert`? If no, surface that risk.
3. Is there a feature in `_meta/features/registry.jsonc` that already does this? If yes, use it.
4. Run `vault-check` after any change. Fix, do not bypass, any new errors.

## Feature dispatch

1. Read `_meta/features/registry.jsonc`.
2. Match the user's intent against `triggers` across all features (case-insensitive substring).
3. Read the matched feature's `FEATURE.md`. Only that one.
4. Invoke per its `Invocation` section. Respect `exit_codes`.
5. If multiple features match: pick the one with highest `priority`; if still tied, ask.
6. If no feature matches but the action is still valid admin work (e.g. editing a mode file), proceed manually.

## Renames

Never use bare `git mv` for renaming a note. Use the `rename-note` feature — it rewrites wikilinks atomically and commits the result.

For moving non-note files (e.g. a script, a template, an admin doc), `git mv` is fine.

## Archiving

Move anything retired under `_archive/` using whatever layout makes sense — there are no internal-structure rules on `_archive/`. You may drop a note at `_archive/<name>.md`, keep a project's original subfolder, group by year, or nest however you like.

```
git mv 1-projects/<slug>/ _archive/<slug>/          # or any destination under _archive/
```

No wikilink sweep is required — links to archived notes still resolve (the slug is unchanged). Archived notes are also exempt from O1 outline-reachability.

## Adding a new feature (script)

1. Create `_meta/features/<name>/`.
2. Write `FEATURE.md` per the schema below.
3. Write the entry script. Python stdlib only, or Bash + git. If external deps are required, declare them in FEATURE.md and set `stdlib_only: false`.
4. Write a test file if the feature is non-trivial.
5. Append one entry to `_meta/features/registry.jsonc`.
6. Run `_meta/features/vault-check/vault_check.py` — it verifies folder/registry parity.
7. Append a line to `_meta/changelog.md`.

### FEATURE.md required schema

YAML frontmatter, then four prose sections (When to use, When NOT to use, Invocation, Side effects). Fields:

```yaml
name: <folder-name>           # must match folder
version: <semver>
entry: ./<filename>           # single entry point, relative to feature folder
language: bash | python | node | ...
stdlib_only: true | false     # if false, list deps in a 'deps:' key
triggers: ["phrase1", "phrase2"]
inputs: [{ name, type, required }, ...]
outputs: [{ name: type }, ...]
exit_codes: { 0: "...", 2: "...", 10: "...", 20: "..." }
idempotent: true | false
modifies_git: true | false
requires_clean_worktree: true | false
```

Keep the whole file ≤80 lines. If it's longer, the feature is too big — split it.

### registry.jsonc entry

```jsonc
{
  "name": "<same as folder>",
  "path": "_meta/features/<name>/",
  "doc": "_meta/features/<name>/FEATURE.md",
  "triggers": ["phrase1", "phrase2"],
  "modes": ["admin"],           // which modes can invoke it
  "priority": 10,
  "enabled": true
}
```

## Amending conventions

1. Edit `_meta/core/conventions.md`.
2. Mirror any machine-readable change into `_meta/core/config.jsonc`.
3. Update `vault-check` if a new check or relaxed rule is involved.
4. Append a changelog line with the reason.
5. Run `vault-check`; confirm no new regressions.

## Amending a mode file

1. Edit the mode file directly.
2. Append a changelog line.

No version bumps required. Mode files are living docs; changelog is the audit trail.

## Running vault-check

```
python3 _meta/features/vault-check/vault_check.py
```

Exit 0 = clean. Exit 1 = errors. Exit 2 = internal failure.

**Run vault-check on entry to admin mode.** The output surfaces any `[RECHECK ≥24h]` frontmatter warnings that have persisted; report them to the user before starting other work.

When vault-check reports an error, fix the root cause. Do not silence the check or bypass it with `--no-verify` or equivalent.

## Frontmatter auto-correct (opt-in)

Config key `frontmatter.agent_auto_correct` (in `_meta/core/config.jsonc`) gates this behavior:

- `false` (default): warn only. Do not write frontmatter.
- `true`: you may add missing recommended keys (`title`, `created`) to notes flagged by M6. Rules:
  1. Infer `title` from H1 if present, else from the filename stem.
  2. Infer `created` from `git log --diff-filter=A --follow --format=%as -- <path>` (file add date). If empty, use today.
  3. Preserve existing frontmatter verbatim — only add missing keys, never reorder or rewrite.
  4. **Do not commit.** After editing, tell the user "N files updated; review with `git diff`, commit if acceptable."
  5. Run `vault-check` again after the pass to confirm M6 count dropped.

## Activity log

A compact JSONL activity log is maintained at

```
_meta/maintenance-reports/.activity.jsonl
```

Dot-prefixed, gitignored — not read by default. Consult it only when it is relevant to the current admin task (e.g. tracing when a feature was last invoked, or confirming a prior rename's commit SHA). Writers: `vault_check`, `rename-note`. One JSON object per line, keys include `ts` and `event`.

## Safety overrides (never violate)

- Never delete user content without explicit confirmation.
- Never skip the dry-run step of a rename.
- Never commit secrets or credentials.
- Never use `--no-verify`, `--no-gpg-sign`, or equivalent bypasses.
- Never force-push to `main`.
- When uncertain, halt and ask.
