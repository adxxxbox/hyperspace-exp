# Mode: work

**Authority: author.** May read + write notes. May not touch structure (`_meta/`, renames, folder moves). May not run git. May invoke `vault-check` (read-only).

Loaded when editing, extending, summarizing, or researching inside existing notes. Not for moving, renaming, or deleting files.

Trigger phrases: "edit", "rewrite", "expand", "summarize", "extract", "research", "draft", "continue writing", "fill in", "synthesize".

## Voice

Direct prose. Short sentences. No hedging. Active where natural, passive where the agent doesn't matter (clinical outcomes, data).

Abbreviations defined on first use per note. Exact numeric values with units. Generic drug names over brand names. Citations inline with author/year and PMID when available. De-identified patient data always.

Flag uncertainty with an inline `<!-- VERIFY: claim -->` rather than removing the claim.

## Heading structure

- H1 matches the note title (or is the first line for files without frontmatter)
- H2 for major sections
- H3 for subsections, sparing
- Avoid H4+
- Sentence case, not title case
- One blank line between sections; one blank line after an H2

## Lists and formatting

- `-` for unordered lists
- `1.` for ordered lists
- Emphasis sparingly; bold for true emphasis, italics for terms of art
- Tables only when the content is genuinely tabular
- Fenced code blocks for actual code; ``` inline ``` for literals
- HTML comments preserved verbatim — they often mark authoring state (`VERIFY`, `TODO`)

## Status markers (for task lines inside notes)

- ⬜ not started
- 🟡 in progress / requires attention
- 🚨 overdue / must resolve
- ✅ done

Apply at the start of a task line. Example: `⬜ Draft discussion section by Friday.`

## Note types (optional `type:` in frontmatter)

| Type | Shape |
|---|---|
| `daily-note` | One per day at `journal/YYYY-MM-DD.md`. Template injected by Foam. |
| `meeting-note` | Attendees, Agenda, Discussion, Decisions, Action items. |
| `paper-summary` | Citation, Research question, Design, Population, Intervention/Exposure, Outcomes, Key results, Limitations, My notes. |
| `protocol` | Objective, Eligibility, Procedure, Endpoints, Safety considerations. |
| `moc` | Map of content: wikilinks under headings, minimal prose. Lives in `4-atlas/`. |
| `card` | Atomic permanent note, one idea, ≤300 words. Lives in `5-cards/`. |
| `checklist` | Reusable checklist (pre-op setup, submission checklist). |
| `case-report` | Demographics, Presentation, Diagnosis, Management, Intraoperative course, Postoperative course, Why reportable, References. |
| `reminder` | Dated reminder with status marker. Lives inline in `journal/` or `todo.md`. |

These are conventions, not schemas. Deviate if the content calls for it.

## Linking

- Wikilinks: `[[slug]]`, `[[slug|display text]]`, `[[slug#heading]]`, `![[slug]]` embeds
- Resolve case-insensitively; slugs are unique vault-wide (enforced by vault-check)
- When referencing a textbook chapter in `3-resources/`, use a wikilink — do not copy the full path

## Content you must not generate

- Fabricated citations, PMIDs, or patient identifiers
- Drug dosages without a source
- Clinical recommendations you cannot ground in a referenced source

If you don't know, write `<!-- VERIFY: ... -->` instead of guessing.

## Scope boundary

If the task requires moving files, renaming, creating a new top-level folder, changing templates, or editing `_meta/` — stop, exit this mode, and load `admin.md`.
