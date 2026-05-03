---
title: "Note type registry (ARCHIVED v1 — retired 2026-04-19, content absorbed into _meta/modes/work.md §Note types)"
created: 2026-04-11
tags: [meta]
---

# Note type registry

Authoritative list of allowed values for the optional `type:` frontmatter key per §M7 of the vault organization guideline.

## Rules (recap from §M7)

- `type` is **optional**. Most notes do not need it.
- When present, `type` is a short, lowercase, hyphenated string.
- A `type` value not listed here must be added here first, in the same commit as its first use.
- `type` describes the **form** of the note (daily entry, meeting minutes, study summary), not its subject matter. Subject matter goes in `tags:`.

Each type entry below defines *what the type is* and *where it lives*. For content structure (sections, headings, writing conventions), see `_meta/authoring-guidelines.md §4`.

## Registered types

### `daily-note`
A dated daily journal entry. One per day, lives at `journal/YYYY-MM-DD.md`. Injected automatically by `.foam/templates/daily-note.md`.

### `meeting-note`
Notes from a single meeting. Lives under the relevant project or area folder.

### `paper-summary`
A structured summary of one academic paper. Lives under `3-resources/` unless tied to an active project.

### `protocol`
A formal study protocol or procedure document. Lives under its project folder.

### `moc`
Map of content. An atlas/index file that links many other notes together. Lives under `4-atlas/`.

### `card`
An atomic permanent note in the Zettelkasten sense — one idea, one file, stated in the author's own words. Lives under `5-cards/`.

### `checklist`
A reusable checklist (surgical prep, manuscript submission, etc.). Lives under `3-resources/` or the relevant area.

### `case-report`
A clinical case report documenting a notable patient encounter for publication or conference presentation. Lives under its project folder in `1-projects/`.

## How to add a new type

1. Confirm the new type describes a recurring **form** of note, not a one-off.
2. Append a new `### <type>` section here with a one-paragraph description and folder guidance.
3. Add a matching subsection to `_meta/authoring-guidelines.md §4` with content structure (sections, headings).
4. Commit both edits in the same commit as the first note using the new type.

---

_This file is part of `_meta/`. Never delete. Never rename._
