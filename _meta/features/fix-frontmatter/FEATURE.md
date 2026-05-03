---
name: fix-frontmatter
version: 1.0
entry: ./fix_frontmatter.py
language: python
stdlib_only: true
triggers: ["fix frontmatter", "auto-correct frontmatter", "backfill frontmatter", "add missing frontmatter"]
inputs:
  - name: apply
    type: flag
    required: false
    description: write changes to disk (default is dry-run — preview only)
  - name: path
    type: path
    required: false
    description: vault-relative subtree to limit the run to (default is whole vault)
  - name: verbose
    type: flag
    required: false
    description: print per-file actions
outputs:
  - name: files_updated
    type: integer
  - name: files_unchanged
    type: integer
  - name: files_skipped
    type: integer
exit_codes:
  0: success (dry-run completed or changes applied)
  2: bad arguments / path missing
idempotent: true
modifies_git: false
requires_clean_worktree: false
---

## When to use

To backfill the two recommended frontmatter keys (`title`, `created`) on notes that are missing them. Rule M6 in `vault-check` flags these; this feature resolves them deterministically in one pass.

Inference rules:
- `title` — H1 (`# ...`) if present, else the filename stem (without `.md`).
- `created` — the file's git add date (`git log --diff-filter=A --follow --format=%as`), else the OS birth time (`st_birthtime` on macOS / BSD), else today.

Idempotent: files that already have both keys are left untouched.

## When NOT to use

- To rewrite or reorder existing frontmatter. This feature only **adds missing keys**; existing keys are preserved verbatim.
- To touch files inside protected directories, `_archive/`, or `_secretary/`. Those are skipped by default (archive has no outline concerns; `_secretary/` uses HTML-comment entry headers, not YAML frontmatter).
- To commit changes. This feature never runs git. Review with `git diff` and commit manually.

## Invocation

```
# Dry-run (default) — no files are written
python3 _meta/features/fix-frontmatter/fix_frontmatter.py

# Apply changes to the whole vault
python3 _meta/features/fix-frontmatter/fix_frontmatter.py --apply

# Limit to a subtree
python3 _meta/features/fix-frontmatter/fix_frontmatter.py --apply --path 3-resources/

# Verbose per-file output
python3 _meta/features/fix-frontmatter/fix_frontmatter.py --apply --verbose
```

## Side effects

- Writes YAML frontmatter blocks to `.md` files missing `title` and/or `created`. When a frontmatter block already exists, the missing key(s) are inserted just before the closing `---`; other keys and ordering are preserved.
- Empty files (0 non-whitespace bytes) are skipped.
- Does not touch git; does not stage or commit.
- Exempt dirs (hard-coded, matches config): every entry in `protected.directories` plus `_archive/` and `_secretary/`.
