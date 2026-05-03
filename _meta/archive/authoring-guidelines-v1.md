---
title: "Authoring guidelines (ARCHIVED v1 — retired 2026-04-19, content absorbed into _meta/modes/work.md)"
created: 2026-04-13
tags: [meta]
---

# Authoring guidelines

**Purpose.** This file defines how to *write content* inside vault notes — voice, structure, headings, clinical precision, and markdown conventions. It applies to every agent that creates or edits notes in this vault, and serves as a reference for the vault owner.

**Scope boundary.** This file governs *what goes inside a note*. It does not govern naming, placement, frontmatter, or linking — those belong to the vault organization guideline and `config.jsonc`. If a structural rule here appears to conflict with the guideline, the guideline wins.

**Authority.** This is a standalone spec under `_meta/`, per the modular-specs convention. It is referenced from `CLAUDE.md`'s lookup table and from `config.jsonc → agent.read_before_any_work` (when added).

---

## 1. General voice

Write in clear, direct prose. Prefer short sentences. Avoid filler, hedging, and unnecessary qualifiers. The reader is a busy clinician-researcher — respect their time.

**Do:**
- State findings and decisions plainly.
- Use active voice when the actor matters ("Murphy et al. randomized 156 patients"), passive when it doesn't ("Pain scores were assessed at 12 h").
- Define abbreviations on first use within a note, then use the abbreviation thereafter.

**Don't:**
- Pad with "it is important to note that" or "interestingly."
- Use marketing language, superlatives, or vague claims ("groundbreaking," "novel approach").
- Editorialize unless the note type calls for it (e.g., the "my notes" section of a paper-summary).

---

## 2. Heading structure

Every note starts with an H1 (`#`) that matches or closely paraphrases the `title:` frontmatter value. This is the only H1 in the file.

Use H2 (`##`) for major sections and H3 (`###`) for subsections. Do not skip levels (no H1 → H3). Do not go deeper than H4 — if you need H5, the note should probably be split.

Headings are sentence case ("Anesthetic plan"), not title case ("Anesthetic Plan"), unless the heading is a proper noun or established term.

---

## 3. Clinical and scientific accuracy

This is a clinical/research vault. Accuracy is the highest priority.

- **Numbers.** Report exact values with units. "0.3 mg/kg" not "a small dose." Include confidence intervals and p-values when summarizing statistical results.
- **Drug names.** Use generic names (methadone, remimazolam), not brand names, unless the brand name is clinically relevant context.
- **Citations.** When summarizing a paper, always include first author, year, and journal at minimum. PMID is preferred when available. Do not fabricate citations.
- **Uncertainty.** If a fact is uncertain, say so explicitly ("data are limited to case reports" or "no RCTs exist"). Do not present weak evidence with confident language.
- **Patient data.** If real patient data appears in a note (case reports), do not include identifiers beyond what is necessary for the clinical narrative. Follow standard de-identification practices.

---

## 4. Note-type conventions

Each registered note type (see `_meta/note-types.md`) has its own structural expectations. These are not rigid templates — adapt to the content — but agents should follow these patterns unless the vault owner directs otherwise.

### daily-note

Free-form. The daily note is a scratch surface. No required sections. Write whatever is on your mind. Tasks use `- [ ]` syntax per Rule C1.

### meeting-note

Sections: `## Attendees`, `## Agenda`, `## Discussion`, `## Decisions`, `## Action items`. Keep decisions and action items crisp — one bullet each, with owners and dates where applicable.

### paper-summary

Sections: `## Citation`, `## Research question`, `## Design`, `## Population`, `## Intervention / Exposure`, `## Outcomes`, `## Key results`, `## Limitations`, `## My notes`.

The first eight sections are factual extraction — report what the paper says, not your opinion. `## My notes` is where you assess, critique, and connect to other work. Always separate fact from interpretation.

### protocol

Sections depend on the protocol type, but typically: `## Objective`, `## Eligibility`, `## Procedure`, `## Endpoints`, `## Safety considerations`. Write in imperative or declarative style ("Administer 0.3 mg/kg IV after induction").

### moc

A map of content is mostly wikilinks organized under descriptive headings. Keep prose minimal — the MOC's job is navigation, not explanation. Group links by subtopic, not alphabetically.

### card

One idea per card. State the idea in your own words in the first paragraph — no hedging, no "according to." Link to source material with wikilinks. Keep it under ~300 words. If it's longer, it's probably two cards.

### checklist

Numbered steps or checkboxes. Each step is one action. Include dosages, thresholds, and decision criteria inline — a checklist that sends you elsewhere to look up a value has failed its purpose.

### case-report

Sections: `## Patient demographics`, `## Presentation`, `## Diagnosis`, `## Anesthetic plan` (or `## Management`), `## Intraoperative course`, `## Postoperative course`, `## Why this case is reportable`, `## References`. This structure mirrors the existing template in the vault.

---

## 5. Markdown conventions

- **Lists.** Use `-` for unordered lists, `1.` for ordered. Leave a blank line before any list.
- **Emphasis.** Use `**bold**` sparingly — for key terms on first definition or critical warnings. Use `*italic*` for journal names, gene names, or foreign terms. Do not bold entire sentences.
- **Tables.** Use markdown tables for structured comparisons (dose tables, study characteristics). Keep tables narrow enough to read without horizontal scrolling (~4–5 columns max).
- **Code blocks.** Only for actual code, commands, or file paths. Do not use code blocks for clinical terms or drug names.
- **HTML comments.** Use `<!-- -->` for placeholder instructions or notes-to-self that should not render. Agents should preserve existing HTML comments unless explicitly asked to remove them.
- **Line length.** No hard wrapping. One paragraph = one line. Let the editor soft-wrap.
- **Blank lines.** One blank line between sections. Two blank lines are never necessary.

---

## 6. Agent-specific rules

When an agent (Claude or any other LLM) writes or edits note content:

1. **Don't invent facts.** If the source material doesn't contain a value, leave the field blank or write "not reported." Never fill gaps with plausible-sounding data.
2. **Don't homogenize voice.** If the vault owner wrote a note in a personal, informal style, preserve that style when editing. Match the register of the existing content.
3. **Don't add unsolicited structure.** If a note is free-form and the owner didn't ask for sections, don't impose them. Add structure only when creating new notes or when explicitly asked.
4. **Preserve HTML comments.** They are instructions or placeholders left by the owner.
5. **Flag uncertainty.** If you're unsure whether a clinical detail is accurate, mark it with `<!-- VERIFY: ... -->` rather than guessing.
6. **Separate your contributions.** When adding to an existing note, use a clear marker if the addition is substantial — e.g., a heading like `## Agent notes (YYYY-MM-DD)` — so the owner can distinguish agent-written content from their own.
7. **Write to files.** Per the vault owner's standing instruction, outputs go in files — not chat. Summaries, extractions, and drafts are written as notes in the appropriate vault location.

---

## 7. When this file doesn't cover it

If you encounter a content decision this file doesn't address, fall back to these principles in order:

1. Clinical accuracy over stylistic preference.
2. Brevity over completeness (you can always add; removing bloat is harder).
3. Consistency with neighboring notes in the same folder.
4. When in doubt, leave a `<!-- TODO: ... -->` comment and move on.

---

_This file is part of `_meta/`. Never delete. Never rename._
