---
name: build-book-indexes
version: 1.0
entry: ./build_book_indexes.py
language: python
stdlib_only: true
triggers: ["build book indexes", "rebuild indexes", "regenerate book index", "index textbooks"]
inputs:
  - name: base
    type: path
    required: false
    description: vault-relative folder containing book subfolders (default 3-resources/anesthesia-refs-md)
  - name: parent
    type: string
    required: false
    description: slug of the parent hub each index links back to (default `anesthesia-reference`)
  - name: dry-run
    type: flag
    required: false
outputs:
  - name: indexes_written
    type: integer
  - name: indexes_unchanged
    type: integer
exit_codes:
  0: success (indexes written or already up to date)
  2: bad arguments / base folder missing
idempotent: true
modifies_git: false
requires_clean_worktree: false
---

## When to use

To (re)generate one `_INDEX.md` per textbook subfolder under `3-resources/anesthesia-refs-md/`. Each generated index lists every chapter in that book as a `[[wikilink]]` and links back to the hub `[[anesthesia-reference]]`, so the chain `outlines → anesthesia-reference → <book>_INDEX → <chapter>` reaches every chapter from the master outline (rule O1).

Run after adding, removing, or renaming chapters in any book folder.

## When NOT to use

To index folders outside `3-resources/anesthesia-refs-md/`. The script is scoped to one base folder; pass `--base` to override, but the script assumes a flat one-level layout (`<base>/<book>/<chapter>.md`).

To hand-edit indexes. The script overwrites; any manual changes will be lost on the next run. If you need a curated index, write it as a separate hub note in `4-atlas/`.

## Invocation

```
python3 _meta/features/build-book-indexes/build_book_indexes.py
python3 _meta/features/build-book-indexes/build_book_indexes.py --dry-run
python3 _meta/features/build-book-indexes/build_book_indexes.py --base 3-resources/anesthesia-refs-md --parent anesthesia-reference
```

## Side effects

- Writes one `_INDEX.md` file per book subfolder under the base folder. Filename derived from the book folder name with `_md` suffix stripped: e.g. `Miller Anesthesia 2025_md/Miller Anesthesia 2025_INDEX.md`. Slug is `<book-name>_INDEX`, unique per book, so no L3 collisions.
- Does not touch git, does not stage, does not commit. The user reviews `git diff` and commits when ready.
- Idempotent: if the file content already matches what would be generated, the file is left untouched (no mtime bump).
