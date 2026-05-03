> **ARCHIVED — DO NOT LOAD.** This 52-KB monolith was retired on 2026-04-19
> as part of the modular/mode-aware redesign. Its enforceable content is now
> split across `_meta/core/conventions.md`, `_meta/modes/capture.md`,
> `_meta/modes/work.md`, and `_meta/modes/admin.md`. Preserved here for
> historical reference only. AI agents: do not read past this banner.

---

# Foam Vault Organization Guideline (Strict) — v1.8, retired

**Vault:** `~/hypernote`
**Owner:** Adnan
**Date:** 2026-04-11
**Status:** Specification v1.8 — permissive naming, reproducible, idempotent.

## Changelog

Full change history is in `_meta/changelog.md` (newest first). This guideline's current version is shown in the Status line above.

---

## 0. Purpose & how to read this document

This is a **specification**, not a tutorial. It is written to be:

- **Deterministic.** Two people (or two runs of the same automation) applying this to the same vault must produce the same result up to ordering of unrelated operations.
- **Idempotent.** Running the rules on an already-compliant vault must make zero changes.
- **Unambiguous.** Every decision has exactly one correct answer. If two rules appear to conflict, §11 (Conflict Resolution) decides.

If any rule below cannot be followed because of a pre-existing Foam template file, §2 (Protected Zones) wins.

**Onboarding.** If you are reading this document for the first time — human or LLM agent — read `CLAUDE.md` at the vault root first. It is the short orientation doc that tells you which files to load in what order. This specification is the authoritative *why*; `CLAUDE.md` is the *where to start*.

---

## 1. Scope

**In scope:** every `.md` file and every folder inside `~/hypernote/`, except the protected zones defined in §2.

**Out of scope:** the host macOS file system outside the vault, and anything the guideline classifies as protected per §2. The specific list of protected paths is enumerated in `_meta/config.jsonc`.

### 1.3 Machine-readable config

This specification has a machine-readable companion at `_meta/config.jsonc`. The companion encodes every enumerated list, regex, path, and schema referenced by this document in a JSONC (JSON-with-comments) file that scripts and LLM agents parse at runtime. It is loaded by `_meta/scripts/config_loader.py`, which uses only the Python standard library.

**Source of truth.** This guideline is the specification. `config.jsonc` is its mechanical extract. If the two disagree, the guideline wins and the config is re-derived.

**Editing rules.** To change a protected path, a canonical folder, the slug grammar, the frontmatter schema, or any other enumerated rule:

1. Amend this guideline first (the *why*).
2. Update `_meta/config.jsonc` to match (the *what*).
3. Bump `_self.version` and `_self.guideline_version` in the config.
4. Add a line to `_meta/changelog.md`.
5. Commit all of the above in one atomic commit.

**Agent instructions.** The `agent` section of `config.jsonc` contains explicit rules for LLM agents (Claude, etc.) working in the vault — what to read before any work, what to check before any write or rename, what to verify before adding a note type, and general safety rules. Any agent acting on the vault must load and obey that section.

### 1.4 Document scope and non-duplication rule

The vault's governance documentation is split across five files. Each file has a single, non-overlapping role. **No file may restate rules or enumerate lists that belong to another file.** Instead, it must reference the authoritative source. This prevents the drift and maintenance burden that come from keeping parallel copies in sync.

| File | Role | Owns |
|---|---|---|
| `CLAUDE.md` | **Onboarding pointer.** Orients new readers (human or agent), provides the read order, and a lookup table. | Nothing — it only points to the other four files. |
| `_meta/vault-organization-guideline.md` | **Specification.** Defines every rule, its rationale, decision trees, algorithms, and test cases. The authoritative *why*. | All rules (F*, N*, M*, L*, P*, D*, C*, R*), conflict resolution, amendment protocol. |
| `_meta/config.jsonc` | **Machine-readable extract.** Encodes every enumerated list, regex, path set, and agent checklist from the guideline. The authoritative *what*. | All enumerated lists (protected paths, canonical folders, slug regex, frontmatter schema, agent checklists). |
| `_meta/workflow.md` | **Operational recipes.** One recipe per task, short enough to fit on screen. The authoritative *how*. | Step-by-step procedures, the pre-commit checklist, status marker convention. |
| `_meta/changelog.md` | **Change log.** One line per non-trivial system change. | Historical record of what changed, when, and why. |

**The non-duplication rule.** When writing or amending any of these files:

- Do not copy a list that `config.jsonc` already enumerates. Reference it: "see `config.jsonc → protected.directories`."
- Do not restate a rule that the guideline defines. Reference it: "per Rule F4" or "see §6."
- Do not repeat a recipe that `workflow.md` already contains. Reference it: "see workflow, 'Renaming a note'."
- `CLAUDE.md` is the most constrained: it may describe *what the vault is* and *where to look*, but must not contain rules, lists, or procedures.

If you find duplication during an edit, remove it and replace with a reference in the same commit.

### 1.5 Scaling with skills

This guideline covers the vault's **structural rules** — naming, placement, frontmatter, protection, linking. These change infrequently and apply to every file in the vault.

New **agent capabilities** (e.g., a PubMed literature search, Apple Reminders sync, automated inbox triage, clinical review drafting) do not belong in this guideline. They are scoped to a specific task, may have their own safety constraints, and evolve independently.

The extension mechanism is **Claude skills** — self-contained instruction files under `.claude/skills/`. Each skill has a `SKILL.md` that defines its purpose, triggers, rules, scripts, and safety constraints. Claude discovers and loads skills automatically based on task context.

**When to create a skill vs. amend the guideline:**

- If the new capability changes how *all notes* are named, placed, linked, or validated → amend the guideline and config.
- If the new capability is a *task-specific agent behavior* that operates on vault content but doesn't change the structural rules → create a skill.

Skills may reference guideline rules (e.g., "obey Rule P1 — never write to protected paths") but must not redefine them. The guideline remains the single source of truth for structural rules; skills extend what agents can *do* within those rules.

**Code modularity.** When writing scripts for this vault (whether in `_meta/scripts/` or as part of a skill), prefer modular design: extract reusable logic into importable modules rather than inlining it. The existing `config_loader.py` is the model — it was written once and is imported by every other script. However, do not abstract prematurely: write focused code first, then extract a module when a second use case appears. The test is "would another script need this exact logic?" — if yes, extract; if maybe, wait.

---

## 2. Protected zones — principles and categories

### 2.0 Definition

A path is **protected** when automation (placement, naming, slug, frontmatter-normalization, rename, wikilink-sweep, vault-check) is forbidden from modifying it. Protection applies to three kinds of target: directories (everything under them is protected), specific files (name and content), and named regions inside otherwise-editable files.

Protection is a property of the path, not of the rule that would touch it. If any rule in this document would modify a protected path, the rule does not apply and the protected path wins. This is **Rule P1**.

Protection is enforced mechanically by every script that walks the vault, which loads the authoritative path lists from `_meta/config.jsonc`. The guideline describes the categories and the reasoning; the config holds the instances.

### 2.0.1 Categories of protected paths

The guideline recognizes four categories of protection. Every protected path belongs to exactly one.

**(A) Infrastructure.** Directories required by Git, Foam, VSCode, or the Jekyll publishing pipeline. These ship with the Foam template and are not user content. Automation must not recurse into them. They are enumerated under `protected.directories` in `config.jsonc`.

**(B) User attachments.** Non-markdown artifacts that the user references from notes but that are not themselves notes. Images, PDFs, the Foam icon. Enumerated under `protected.directories` alongside (A) because the containing directories are the protection boundary.

**(C) Shipped root-level files.** Files that the Foam template creates at the vault root and that serve a defined role in the workflow (capture, index, entry point). Their name, location, and content are fixed. They are enumerated under `protected.files` in `config.jsonc`. Their individual roles are described in §5.

**(D) Protected regions inside editable files.** Segments of otherwise-normal markdown files that are managed by Foam or another tool and must be preserved verbatim. Example: the link-reference definition block Foam maintains at the bottom of every note that contains wikilinks. Enumerated under `protected.regions` in `config.jsonc`. See §2.2.

### 2.0.2 Defaults

The guideline ships with the following defaults, which `config.jsonc` instantiates:

- Infrastructure protection applies to every directory beginning with `.` (dotfile convention) plus `attachments/`.
- `_meta/` is protected from note automation: it is managed only by the guideline's amendment process and by the scripts inside `_meta/scripts/`.
- The two shipped root files — capture (`inbox.md`) and template example (`todo.md`) — are fully protected. Their purposes are described in §5.
- The Foam autogenerated link-reference block, delimited by `[//begin]: # "Autogenerated..."` and `[//end]: # "Autogenerated..."`, is a protected region.
- The `.vscode/` workspace-settings bundle is infrastructure; its contents are described in §5.4.

### 2.1 Exception — user-managed configuration

Protection forbids **automation** from touching a path; it does not forbid **the user** (or Claude acting as a one-time configuration assistant with the user's explicit approval) from editing it. Some paths that are otherwise protected from automation exist specifically to be tuned by the user.

**Principle.** A directory may be declared a *user-managed exception* if editing it is a one-time configuration change rather than a recurring workflow operation. The canonical example is `.foam/templates/` — editing a template changes how *future* notes are born, not how *existing* notes are organized.

**Rule.** Every user-managed exception must be enumerated under `protected.exceptions` in `config.jsonc` with a short rationale, and every edit to such a path must be recorded in `_meta/changelog.md` citing the rationale. Recurring automation still treats the path as protected.

### 2.2 Protected regions inside editable files

Some tools maintain managed blocks inside otherwise-normal markdown files. Foam's `foam.edit.linkReferenceDefinitions: withExtensions` setting causes Foam to append a link-reference definition block at the bottom of every note that contains wikilinks — markdown-compatibility metadata that Foam owns.

**Rule P3.** A protected region, as enumerated under `protected.regions` in `config.jsonc`, must be preserved verbatim by any automation that reads or writes file content. Never reorder it, rewrite its entries, strip it, or move it. Only the tool that manages the region (Foam, in this case) is allowed to regenerate it.

### 2.3 Rule P2 — Foam daily-note path

The Foam daily-note template places daily notes into `journal/YYYY-MM-DD.md`. This vault **adopts `journal/` as canonical** rather than fighting the template. Any rule in this document that mentions daily notes refers to this path.

### 2.2 Protected regions inside otherwise-editable files

Foam's `foam.edit.linkReferenceDefinitions: withExtensions` setting causes Foam to maintain a **link-reference definition block** at the very bottom of every file that contains wikilinks. It looks like this:

```markdown
[srma-delirium-protocol]: srma-delirium-protocol.md "SRMA Delirium Protocol"
[aana-abstract]: aana-abstract.md "AANA Abstract"
```

**Rule P3.** This Foam-managed block is a protected region. Any automation that reads or writes file content must preserve the block verbatim — never reorder it, rewrite its entries, strip it, or move it. Only Foam itself (via the VSCode extension) is allowed to regenerate this block.

---

## 3. Canonical folder layout

After the guideline is applied, the vault root contains exactly these directories, in this order, with exactly these names:

```
~/hypernote/
├── [protected files and dirs from §2]
├── journal/          ← daily notes, one file per day
├── 1-projects/       ← active, deadline-driven work
├── 2-areas/          ← ongoing responsibilities, no end state
├── 3-resources/      ← reference material
├── 4-atlas/          ← maps of content, indexes, dashboards
├── 5-cards/          ← atomic permanent notes
├── _archive/         ← closed projects, inactive areas, old cards
└── _meta/            ← vault scripts, changelog, guideline itself
```

**Rule F1 (no other top-level folders).** No user folder may be created at the vault root outside this list. If a real need arises, the list is amended in this document first, then in the vault.

**Rule F2 (fixed names).** The nine folder names above are fixed strings. No variants, no synonyms, no pluralization changes. `1-project/` is wrong. `Projects/` is also wrong — folder names at the top level are always lowercase, even though file names are now case-preserving (see §N2). Only the exact strings above are correct.

**Rule F3 (prefix semantics).**
- A numeric prefix `N-` identifies a PARA tier (1–5, reserved).
- An underscore prefix `_` identifies a meta/infrastructure folder that must float to the top of alphabetical sort.
- Every user-created top-level folder has exactly one of these prefixes. Never both. Never neither.

**Rule F4 (max depth = 3).** From the vault root, no file may live more than 3 levels deep. Allowed depths:

- L0: `~/hypernote/` (root)
- L1: `1-projects/` (category folder)
- L2: `1-projects/srma-delirium/` (single project folder)
- L3: `1-projects/srma-delirium/Protocol.md` (file)

L4 is forbidden. If a project feels like it needs L4, split the project.

**Rule F5 (no single-file subfolders).** A folder containing exactly one file is always wrong. Either the file moves up one level or a second file moves in. Checked at every run.

**Rule F6 (`_archive/` mirrors the active tree).** Inside `_archive/`, the subfolder structure mirrors the active top-level folders: `_archive/1-projects/`, `_archive/2-areas/`, `_archive/3-resources/`, `_archive/5-cards/`. This keeps archive moves mechanical.

---

## 4. Placement decision tree

Every markdown file in the vault belongs in exactly one top-level location. To place a file, walk this tree top to bottom. **Stop at the first "yes."** There is no ambiguity — always follow the first matching rule.

```
Q1. Is the file a protected Foam/Jekyll file?      → leave where it is (§2)
Q2. Is the file a dated daily/journal entry?       → journal/YYYY-MM-DD.md
Q3. Is the file captured without classification?   → inbox.md (append)
Q4. Does the file describe work with a deadline
    AND an end state, currently in progress?       → 1-projects/<slug>/
Q5. Does the file describe an ongoing responsibility
    with no deadline and no end state?             → 2-areas/<slug>/
Q6. Is the file reference material (a paper summary,
    a clinical protocol, a methods cheatsheet)
    not tied to any one project?                   → 3-resources/<slug>/
Q7. Is the file a map, index, or dashboard that
    links many other notes together?               → 4-atlas/
Q8. Is the file a single atomic idea in your own
    words, small enough to state in one sentence?  → 5-cards/
Q9. Is the file historical, superseded, or the
    remains of a finished project or dead area?    → _archive/<mirror>/
Q10. None of the above?                            → inbox.md (append for triage)
```

**Rule P4 (tie-break = first hit).** If a file seems to satisfy two questions, the earlier question always wins. A completed project moves to `_archive/`, not to `3-resources/`.

**Rule P5 (status is tracked by folder, not by frontmatter).** The only source of truth for "is this project active?" is which folder it lives in. Never put `status: active` in the frontmatter; it will drift. Move the folder instead.

**Rule P6 (one home).** A note exists in exactly one folder. Cross-references use `[[wikilinks]]`, never symbolic links, never copies.

---

## 5. Special root files

### 5.1 `inbox.md`

**Purpose:** the single capture surface for everything unclassified.

**Rules:**
- Every new capture lands at the **bottom** of `inbox.md` as a new `##` section dated `YYYY-MM-DD HH:MM`.
- The weekly review (§10) processes every item in `inbox.md` and moves it to the right folder. After the review, `inbox.md` must be empty below its preserved header.
- The preserved header (the Foam template's existing H1 + opening paragraph) is never touched.
- `inbox.md` is **the only file** where unclassified content may live.

**Idempotency:** running triage twice in a row on an empty inbox is a no-op.

### 5.2 `todo.md`

**Purpose:** Foam template example file. The real task system lives inside the markdown files the tasks relate to, as GitHub-flavored checkboxes (`- [ ]`). See §9 for the task rules.

**Rule:** `todo.md` is a fully-protected root-level file. Its content, name, and location are never modified by automation or by the recurring organization workflow. Treat it exactly like `inbox.md`.

### 5.3 `todo.md`

Protected. Never touched. Ships as the Foam template provides it. `todo.md` and `inbox.md` (§5.1) are the only two protected root files.
### 5.4 `.vscode/` workspace settings bundle

The `.vscode/` directory at the vault root is a VSCode workspace-settings bundle shipped by the Foam template. It is protected infrastructure — automation never modifies it — but it is enumerated here because a human reader needs to know what lives inside and why.

Contents:

- **`extensions.json`** — the recommended-extensions list VSCode prompts the user to install when the workspace is opened. Currently recommends `foam.foam-vscode`, `yzhang.markdown-all-in-one`, `esbenp.prettier-vscode`, and `philipbe.theme-gray-matter`.
- **`settings.json`** — workspace-level VSCode settings. Key entries: `files.autoSave: onFocusChange`, `editor.minimap.enabled: false`, `foam.edit.linkReferenceDefinitions: "withExtensions"` (which drives Rule P3), `git.enableSmartCommit: true`, `git.postCommitCommand: "sync"`, and a markdown custom-styles reference to `custom-tag-style.css`.
- **`keybindings.json`** — workspace-level keybinding overrides. Currently binds `cmd+shift+n` to `foam-vscode.create-note`.
- **`custom-tag-style.css`** — a minimal CSS override that styles Foam tag badges in the preview pane with a black background and white text.

This bundle is declared infrastructure, not user content. Edits to it are rare and are made manually by the user (or by Claude acting as a one-time configuration assistant with explicit approval). Each edit is logged in `_meta/changelog.md`. Recurring automation never writes here.

---

## 6. File naming specification

The naming rules were deliberately relaxed in v1.8. This is a personal knowledge vault, not a code project — friction at capture is the single biggest threat to vault health, and strict slug grammar was buying less than it cost. The remaining rules are only those that pay real dividends: filesystem safety, date format for chronological sorting, and disambiguation where it genuinely matters.

**Rule N1 (permissive pattern).** Every user-created markdown file has a name of the form `<stem>.md`, where the stem is any non-empty string that:

- contains no filesystem/cross-platform illegal characters: `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`, or control characters (0x00–0x1f);
- does not start or end with a space or a dot.

That is all. Spaces, underscores, dots, parentheses, ampersands, commas, apostrophes, plus signs, brackets, non-Latin scripts (Arabic, Chinese, etc.) — all allowed. No mandated casing, no mandated word ordering, no forbidden filler words, no keyword-stuffing rule. Name the file the way you'd describe it to yourself.

Examples of valid stems:

- `Protocol`
- `protocol`
- `SRMA Delirium Protocol`
- `ACE inhibitors in CKD`
- `IRB-2026-0143 Amendment (final)`
- `Dexmedetomidine — postop delirium`
- `سجل-2026`
- `2026-04-11` (daily note)

Examples of **invalid** stems:

- `foo/bar.md` (slash — filesystem-illegal)
- `bad:name.md` (colon — cross-platform illegal)
- ` leading-space.md` / `trailing-dot..md` (leading/trailing space or dot)
- `protocol.MD` (uppercase extension — see §N2b)

**Rule N2 (case-preserving).** Case is preserved as the user writes it. The slug computation algorithm (§13.1) never normalizes case.

**Rule N2a (case-collision prohibition — retained for filesystem safety).** Within any single folder, no two files may have names that differ **only** in case. `Protocol.md` and `protocol.md` may not coexist in the same folder. This prevents silent data loss on case-insensitive filesystems (APFS default, NTFS) and silent file duplication on case-sensitive filesystems (Linux ext4, case-sensitive APFS). This is the one case-related restriction that remains, and it is non-negotiable: it exists to protect data, not to enforce style. The vault-check script must detect case-collisions and halt.

**Rule N2b (extension is always lowercase `.md`).** The file extension is exactly `.md`, lowercase. `.MD`, `.Md`, and `.markdown` are forbidden. This is the one place where case is normalized.

**Rule N3 (non-Latin content).** Non-Latin stems (Arabic, Chinese, etc.) are allowed freely under N1. There is no requirement to avoid mixing scripts, and no requirement that a stem be in any particular script.

**Rule N4 (dates in filenames).**
- Daily notes use exactly `YYYY-MM-DD.md` — nothing else. This is the one place where the date format is enforced, because chronological sorting of `journal/` depends on it.
- For other event-dated files, ISO extended (`YYYY-MM-DD`) is strongly recommended for sortability, but not enforced.

**Rule N7 (slug length).** Recommended ≤ 80 characters including `.md`. Hard cap: 200 characters (most filesystems and git clients tolerate far more, but excessively long names hurt readability). If it won't fit, the concept is too broad — split the file.

**Rule N8 (in-folder uniqueness — see also §L3).** Two files may share a slug only if they live in different folders AND the duplication is permitted by §L3 (which in turn normally forbids it vault-wide). Within one folder, slugs are unique by §N2a — and by the stricter §L3, they are unique across the whole vault.

**Rule N9 (preserved identifiers — recommended).** When a file's primary identifier in your memory is an external code (IRB number, grant ID, manuscript ID, ClinicalTrials.gov NCT number), including the code in the stem is recommended for findability: `IRB-2026-0143 Amendment.md`, `NCT04567890 Inclusion Criteria.md`. Recommended, not enforced.

**Rule N10 (rename-with-sweep — Option B).** Automation is permitted to rename files, but every rename operation must be an **atomic commit** containing three things in this exact order:

1. A vault-wide find-and-replace of `[[old-slug]]` → `[[new-slug]]` across all markdown files, including these wikilink forms:
   - Simple: `[[old-slug]]`
   - Display text: `[[old-slug|display text]]` → `[[new-slug|display text]]`
   - Section reference: `[[old-slug#heading]]` → `[[new-slug#heading]]`
   - Section + display: `[[old-slug#heading|display text]]` → `[[new-slug#heading|display text]]`
   - Embedded transclusion: `![[old-slug]]` → `![[new-slug]]`
2. An update of the Foam-managed link-reference block at the bottom of any affected file, if the automation is confident it can regenerate the block correctly (otherwise, leave the block as-is and let Foam regenerate it on next edit).
3. The actual file rename via `git mv`.

**Rule N10a (code-block safety).** The find-and-replace in step 1 **must not** rewrite wikilinks that appear inside fenced code blocks (```` ``` ... ``` ````) or inline code (`` `...` ``) — those are examples or documentation, not real links. The automation must parse markdown well enough to skip code regions. Failing this check is a violation of the reproducibility contract (§12).

**Rule N10b (idempotent rename).** If the proposed new slug equals the current slug, the rename does not occur. The automation must always check before acting.

**Rule N10c (external rename safety net).** If a file is renamed outside VSCode (e.g., via Finder, terminal `mv`, or another editor), the weekly review runs the vault-check script, which detects orphaned inbound wikilinks and reports them for manual fix. Prevention is preferred; detection is the safety net.

---

## 7. Frontmatter specification

Every user-created markdown file has YAML frontmatter at the top. Frontmatter keys are a **closed set** — only these keys are permitted. Unknown keys cause the vault-check script to warn (not halt); they may be removed in an approved run.

```yaml
---
title: "Human-readable title with any capitalization"
created: 2026-04-11
tags: [tag1, tag2]
aliases: [optional, list, of, aliases]
type: note    # optional; used by Foam for special note types like "daily-note"
---
```

**Rule M1 (required keys).** `title` and `created` are required on every user-created markdown file. `tags`, `aliases`, and `type` are optional. The required keys are injected automatically by the Foam templates for new notes, so files born from templates always start compliant.

### 7.1 Schema growth protocol (how to add new frontmatter keys later)

Frontmatter schemas evolve. To add a new key without breaking existing files, follow this four-step sequence **in order**:

1. **Amend §7 of this guideline** to add the new key, specifying:
   - The key name and type (string, ISO date, list, etc.).
   - Required or optional.
   - Mutable or immutable.
   - Allowed values (if constrained).
   - The rationale — why this key exists and what problem it solves.
2. **Update the Foam templates** under `.foam/templates/` to inject the new key into newly created notes. From that moment on, every new note is born compliant. At the time of writing, `.foam/templates/` contains three files: `new-note.md` (the general-purpose new-note template used by `cmd+shift+n`), `daily-note.md` (the daily-note template Foam uses when generating `journal/YYYY-MM-DD.md`), and `your-first-template.md` (a Foam-shipped example template retained as a reference; safe to ignore for schema growth). Schema growth means updating `new-note.md` and `daily-note.md`. `your-first-template.md` is left alone.
3. **Decide on back-fill** for existing files:
   - If the key is *optional* and back-fill is not required: stop here. Existing files remain valid.
   - If the key is *required* or back-fill is desired: write a one-time migration script that walks the vault, injects the key into each existing file, runs dry-run first, produces a report, and commits as `migration: add <key> frontmatter (YYYY-MM-DD)`.
4. **Update the vault-check script** (§13.3) to validate the new key if it is required.

**The ordering matters.** Promoting a key from "optional" to "required" *before* back-filling existing files will trigger a flood of vault-check failures. Always back-fill first, then promote.

**Reserved key-name namespace.** Keys starting with `foam_` are reserved by Foam; do not use them for user data. Keys starting with `_` are reserved for future internal use by this guideline.

### 7.2 Other frontmatter rules

**Rule M2 (no duplicate info).** Do not put `status`, `folder`, `category`, `project`, `date`, or `path` in the frontmatter — these are implied by the file's location in the folder tree (§4/§5).

**Rule M3 (tag namespace and discovery).** Tags use forward-slash nesting for hierarchy: `topic/delirium`, `status/waiting`, `priority/high`, `person/dr-smith`. No spaces. Tags are treated case-sensitively by Foam, so **conventionally use lowercase for tag names** to avoid accidental duplicates — this is the one sub-domain where lowercase is still recommended (filenames may mix case, but tags should not). Tags are **discovered**, not registered: Foam's Tag Explorer panel indexes every `#hashtag` in prose and every entry in a frontmatter `tags:` array across the vault. There is no authoritative registry file. The vault itself is the registry; Foam is the index. Pruning, merging, or renaming a tag is done the same way as any other refactor — edit the affected files and commit.

**Rule M4 (created date is immutable).** Once set, `created` never changes. Even if the file is renamed, moved, or rewritten. Never.

**Rule M5 (no `modified` key).** Git history is the source of truth for modification time.

**Rule M6 (`type` is optional but recommended for special notes).** Daily notes use `type: daily-note`. Meeting notes may use `type: meeting-note`. The `type` value is a short lowercase-hyphenated string. The registry of allowed types lives in `_meta/note-types.md`.

---

## 8. Link and reference rules

**Rule L1 (wikilinks for internal references).** Inside the vault, use `[[note-slug]]` or `[[note-slug|display text]]`. Never use relative paths like `[text](../1-projects/foo.md)` unless the target is outside the vault.

**Rule L2 (slug-based linking, not path-based).** Wikilinks reference the slug (filename without extension), not the full path. Foam resolves slugs globally. This means moving a file between folders does not break its inbound links. Renaming does — see §N10.

**Rule L3 (slug uniqueness across the vault).** Because Foam resolves wikilinks by filename globally, slugs must be unique across the **entire vault**, not just within a folder. If two files would have the same slug, one must be disambiguated by adding scope to its slug (e.g., `Protocol.md` → `SRMA-Protocol.md`). The case-sensitivity of this uniqueness check matches Foam's wikilink resolution, which is case-insensitive — so `Protocol.md` and `protocol.md` are considered colliding for the purpose of §L3, even if they live in different folders, and the vault-check script flags them as errors.

**Rule L4 (no circular MOCs).** An atlas/MOC file may link to project/area/card files; project/area/card files may link to each other. An atlas file does not link to another atlas file (flatten the hierarchy instead).

**Rule L5 (attachments stay in `attachments/`).** Images and binary attachments live in `attachments/` (the Foam-default folder). Markdown files reference them with `![alt](attachments/foo.png)`. Do not create parallel attachment folders inside project folders.

---

## 9. Content and task rules

**Rule C1 (task syntax).** Tasks are GitHub-flavored markdown checkboxes: `- [ ]` for open, `- [x]` for done. They live inside the markdown file they relate to — not in a standalone `tasks.md`.

**Rule C2 (task due date).** An open task with a due date appends the date at the end of the line in ISO extended format, prefixed by `📅`: `- [ ] Submit amendment 📅 2026-04-20`. The emoji is required because it makes the due date greppable and machine-parsable.

**Rule C3 (task ID for Reminders sync).** If a task is synced to Apple Reminders, it carries a stable ID as an HTML comment at end of line: `- [ ] Call lab 📅 2026-04-15 <!-- rid:7f3a -->`. The sync script writes this ID on first sync and never rewrites it.

**Rule C4 (no task outside a note).** Tasks never live at the top level of a markdown file unless the file is explicitly about tracking tasks (e.g., a project's `Tasks.md` or a daily note). Prefer embedding tasks inside the relevant project/meeting/card note.

**Rule C5 (daily notes own the day's capture).** The daily note is the default scratch surface for the day. Random tasks captured during the day live there first, then get swept into project files during the weekly review (§10).

---

## 10. Maintenance rituals (required for the system to stay valid)

**Rule R1 (daily).** Open today's `journal/YYYY-MM-DD.md`. If it does not exist, create it from the Foam daily-note template. Write the day's agenda. Capture tasks and thoughts as the day progresses.

**Rule R2 (weekly review, Sunday).** In exactly this order:

1. Process `inbox.md` top to bottom. For each entry, apply §4 and move it to the right folder. `inbox.md` must end empty.
2. Process the past 7 daily notes. Sweep loose tasks into the appropriate project/area files.
3. Walk `1-projects/`. Close any project that is done by moving its folder to `_archive/1-projects/`. Promote any area-like responsibility to `2-areas/`.
4. Run the vault-check script (§13.3) and fix any violations it reports.
5. `git add -A && git commit -m "weekly review YYYY-MM-DD" && git push`.

**Rule R3 (monthly).** Walk `2-areas/`. Move any dead areas to `_archive/2-areas/`. Audit `4-atlas/` — every MOC still up to date?

**Rule R4 (quarterly).** Full structural audit. Run the vault-check script in strict mode. Review whether the guideline itself needs amendment. Any amendment is made in this document first, then in the vault, then committed with a `guideline: vN.N` tag.

---

## 11. Conflict resolution (tie-breakers, in priority order)

When two rules appear to conflict, the earlier item in this list wins.

1. **§2 (Protected Zones)** — protected paths always win.
2. **§3 / Rule F2 (fixed folder names)** — canonical structure beats local optimization.
3. **§4 (placement decision tree) — first-hit wins.** Q1 beats Q2 beats … beats Q10.
4. **§6 (naming rules)** — a valid name beats a descriptive name.
5. **§7 / Rule M4 (immutable `created` date)** — the original date wins against any "cleaner" value.
6. **§8 / Rule L3 (slug uniqueness across vault)** — a forced disambiguation beats a shorter slug.
7. **Simplicity** — if all of the above are satisfied and two options remain, the option with fewer characters / fewer folders / fewer rules wins.

---

## 12. Reproducibility requirements (the determinism contract)

A tool (human or script) that implements this guideline must satisfy:

**Rule D1 (pure function).** The output of running the guideline on a vault is determined entirely by the current state of the vault plus the rules in this document. No external state, no random behavior, no "I'll make a judgment call."

**Rule D2 (idempotence test).** If the guideline is applied twice in a row with no edits in between, the second run must make zero changes to any file. This is the primary correctness test. Case preservation (§N2) is essential to this: the slug algorithm never normalizes case, so a file named `SRMA-Delirium-Protocol.md` is not silently rewritten to `srma-delirium-protocol.md` on a second run.

**Rule D3 (stability test).** A small local edit (e.g., adding a paragraph to one note) must not cause global reorganization. Changes made by the guideline must be local to the edited file and its frontmatter.

**Rule D4 (dry-run first).** Any automation that implements the guideline defaults to dry-run: it produces a report of intended changes and waits for explicit approval before touching files. Real mode is opt-in per run.

**Rule D5 (counting invariant).** Before and after any run, total file count in the vault must match — except for explicitly approved deletions, which must appear in the dry-run report.

**Rule D6 (reversibility).** Every change is done via `git mv`, never `rm`. All moves are atomic commits. A failed run must leave the vault in a clean state (either fully done or fully not done).

**Rule D7 (error = halt).** If the automation encounters an ambiguous case (e.g., a file satisfies no question in §4 but contains real content), it halts, logs the file, and requires human adjudication. It does not guess.

---

## 13. Implementation recipes

These are concrete algorithms that satisfy the above spec. They are normative — if a tool wants to claim compliance, it implements these.

### 13.1 Slug computation from a file (case-preserving)

Given a markdown file with content and optional frontmatter `title`:

1. If frontmatter `title` exists, start from it. Else, start from the filename (minus extension).
2. Normalize to NFC Unicode.
3. **(Removed in v1.1 — no case normalization.)** Case is preserved as written.
4. Replace any run of whitespace or underscores or characters outside `[A-Za-z0-9-]` with a single hyphen.
5. Strip leading and trailing hyphens.
6. Collapse runs of hyphens to a single hyphen.
7. Apply §6 rules (length cap, no filler words, no keyword stuffing, no case-collision within target folder).
8. Append `.md`.

**Idempotence guarantee:** because step 3 no longer exists, a slug like `SRMA-Delirium-Protocol` is a fixed point of the algorithm — running it a second time produces the same slug.

### 13.2 Placement computation

1. Read file path. If inside a protected zone (§2), stop.
2. If file is in `journal/`, leave.
3. Walk §4 questions Q4 → Q9 against the file's current content.
4. If the current folder matches the answer, no move. Else `git mv` to the new folder.

### 13.3 Vault check script (contract)

The vault-check auditor is implemented as `_meta/scripts/vault_check.py` — a Python 3 script, standard-library only, with no third-party dependencies. It is a **read-only** auditor: it never writes files, never renames, never stages commits. Its job is to walk the vault and report violations of this specification. Fixing violations is a separate, human-initiated action.

**Inputs.** The script takes one positional argument: the vault root (defaults to the current working directory). Flags: `--strict` (promotes warnings to errors), `--json` (machine-readable JSON output instead of human-readable text).

**Outputs.** Report goes to stdout, not to a changelog file. Each finding is prefixed with a rule code. The summary line reports the number of files scanned, errors, and warnings.

**Exit codes.**

- `0` — the vault is clean (no errors; warnings allowed unless `--strict`).
- `1` — one or more errors found (or any warning in `--strict` mode).
- `2` — internal error (I/O failure, malformed config, unreadable file).

**Rule codes checked.** Each finding carries a code from the list below so the user can trace it to the spec.

- **F2** — a top-level folder name is not in the canonical list (§F1/§F2).
- **F4** — a file lives deeper than L3 (§F4).
- **F5** — a folder contains exactly one file (§F5). Reported as a **warning**, not an error, because transient single-file folders during an edit session are normal.
- **N1** — a filename violates the slug grammar `^[A-Za-z0-9]+(-[A-Za-z0-9]+)*$` (§N1).
- **N2a** — two files in the same folder differ only in case (§N2a).
- **N3** — a filename uses an extension other than lowercase `.md` (§N2b). (Rule letter N3 here is the auditor's internal code for extension; the spec's §N2b is the authority.)
- **M1** — a note is missing a required frontmatter key (`title` or `created`) (§M1).
- **M2** — a note contains a forbidden frontmatter key (`status`, `folder`, `category`, `project`, `date`, `path`, `modified`) (§M2).
- **M4** — `created` is not in `YYYY-MM-DD` format or is otherwise malformed (§M4, immutable date hygiene check).
- **P3** — a protected region (Foam link-reference block) is malformed — e.g., the start marker appears without the end marker (§P3). Reported as a warning unless the block is actually corrupted.
- **L3** — two distinct files resolve to the same slug under case-insensitive comparison, i.e., a global slug collision (§L3).
- **IO** — a file could not be read or decoded as UTF-8.

**Protection.** The script prunes `protected.directories` from `config.jsonc` at walk time, so protected infrastructure never appears in findings.

**Known deferred gap.** Orphan-wikilink detection — a wikilink whose target does not resolve to any file in the vault — is **not** currently checked. The rename-with-sweep workflow (§N10 / §13.4) prevents orphan creation on the write path, and the safety net described in §N10c is the vault-check script itself; this check is deferred to a future version. When added, it will be rule code `L1`.

**Tests.** The script is covered by `_meta/scripts/test_vault_check.py` — a stdlib-only test runner (no pytest) that builds ephemeral vault fixtures in `tmpdir` and verifies each rule code fires in the expected conditions. Every amendment to `vault_check.py` must pass the tests before commit.

**Usage.** The weekly review (R2) runs `python3 _meta/scripts/vault_check.py` before the commit step. Exit 0 is required to proceed; any error halts the review and is fixed first.

### 13.4 Rename-with-sweep algorithm (Option B)

Input: `old_slug`, `new_slug`, vault root.

1. Assert `old_slug != new_slug` (idempotent guard, §N10b). If equal, exit 0 no-op.
2. Assert `new_slug` matches the grammar in §N1 and the filler-word ban in §N5.
3. Assert `new_slug` is unique across the vault (§L3) under case-insensitive comparison. If a collision is found, halt.
4. Build the match patterns:
   - `[[<old_slug>]]`
   - `[[<old_slug>|...]]`
   - `[[<old_slug>#...]]`
   - `[[<old_slug>#...|...]]`
   - `![[<old_slug>]]`
5. Walk every `.md` file in the vault (skip protected zones).
6. For each file, parse the markdown well enough to identify fenced code blocks and inline code. Apply the find-and-replace only *outside* code regions.
7. Stage all resulting edits (`git add`).
8. `git mv <old_slug>.md <new_slug>.md` in the correct folder.
9. Commit as a single atomic commit: `rename: <old_slug> → <new_slug>`.
10. Log the rename in `_meta/changelog.md`.

If any step fails, roll back the staging area (`git reset HEAD`) and exit non-zero. Partial renames are forbidden.

---

## 14. Test cases (examples — required to pass)

These are the reference test cases. A correct implementation of the guideline produces the output listed for each input.

| # | Input (current state) | Expected action |
|---|---|---|
| 1 | `SRMA Delirium Protocol.docx` in vault root | Halt — wrong extension, out of scope (not `.md`). |
| 2 | `SRMA-Delirium-Protocol.md` in vault root, describes active project with deadline | Move to `1-projects/srma-delirium/SRMA-Delirium-Protocol.md`. Case preserved. |
| 3 | `1-projects/srma-delirium/SRMA-Delirium-Protocol.md` already | No change (idempotent). |
| 4 | `Protocol.md` with title frontmatter `title: "SRMA Delirium Protocol"` in wrong folder | Rename to `SRMA-Delirium-Protocol.md` (with wikilink sweep per §N10) AND move per §4. |
| 5 | `notes_from_may.md` in `1-projects/srma-delirium/` | Rename to `notes-from-may.md` (underscores → hyphens per §N2; case preserved). |
| 6 | `Notes_From_May.md` in `1-projects/srma-delirium/` | Rename to `Notes-From-May.md` (underscores → hyphens; case preserved). |
| 7 | `final-draft.md` in any folder | Halt — contains filler words `final` AND `draft`; requires human disambiguation per §N5. |
| 8 | `Final-Draft.md` in any folder | Halt — §N5 filler-word check is case-insensitive. |
| 9 | `journal/2026-04-11.md` | No change (protected daily-note path). |
| 10 | Two files: `1-projects/foo/Protocol.md` and `1-projects/bar/protocol.md` | Halt — §L3 violation under case-insensitive comparison. Requires rename of one. |
| 11 | File with no frontmatter | Inject required frontmatter (`title`, `created=today`), then re-evaluate placement. |
| 12 | Empty folder `3-resources/methods/` | Delete the empty folder. |
| 13 | Folder `2-areas/health/bloodwork/` containing only `Results.md` | Move `Results.md` up to `2-areas/health/Bloodwork-Results.md` and delete `bloodwork/` (§F5). |
| 14 | File referencing `[[srma protocol]]` (spaces in link) | Fix link to `[[SRMA-Delirium-Protocol]]` via slug resolution, if the target exists. If not, halt. |
| 15 | `_archive/1-projects/old-thing/` with an MD file | No change — archive files are frozen. |
| 16 | Rename `foo.md` → `Bar.md`, with `[[foo]]` referenced in 5 other files | Sweep all 5 references to `[[Bar]]`, then `git mv`, all in one commit (§13.4). |
| 17 | Rename where one of the 5 references is inside a fenced code block | The reference inside the code block is left untouched; the other 4 are swept. |
| 18 | File contains Foam link-reference block at bottom with old slug | The block is regenerated by Foam on next edit, or if automation is confident, regenerated in place. Not stripped. |

---

## 15. Amendment protocol

Changes to this guideline follow these rules:

1. Propose the change as a pull-request-style markdown diff to this file in `_meta/changes/YYYY-MM-DD-<short-description>.md`.
2. Apply the change to the file only after review.
3. Bump the version in the header (`Specification v1.0` → `v1.1` → `v1.2`).
4. Add an entry to the top changelog section of this file describing what changed and why.
5. If the change invalidates existing files (e.g., a new naming rule), write a one-time migration entry and run it as a normal dry-run-first operation (§D4).

The guideline itself is version-controlled in git. Every amendment is a commit.

---

## 16. Quick reference card

```
FOLDERS:    1-projects/, 2-areas/, 3-resources/, 4-atlas/, 5-cards/,
            _archive/ (mirrors), _meta/, journal/

DEPTH:      max 3 levels (vault → category → folder → file)

SLUG:       ^[A-Za-z0-9]+(-[A-Za-z0-9]+)*$     .md only (lowercase extension)
            Case preserved as user writes it.
            No two files in one folder may differ only in case.
            Slug unique across the whole vault (case-insensitive).

DATES:      YYYY-MM-DD (extended ISO only)

NO FILLER:  new, old, final, draft, copy, temp, latest, v1, v2, untitled
            (case-insensitive check)

FRONTMATTER: title (req), created (req, immutable),
             tags (opt), aliases (opt), type (opt)
             Schema grows via §7.1 four-step protocol.

TAGS:       lowercase (convention), /-nested, discovered by Foam (no registry)

LINKS:      [[Slug]] — slug-unique across whole vault (case-insensitive)

TASKS:      - [ ] text 📅 YYYY-MM-DD <!-- rid:xxxx -->

FIRST-HIT:  placement decision tree stops at first match (§4)

IDEMPOTENT: second run on a compliant vault = zero changes (§D2)

RENAME:     Option B — sweep wikilinks first, then git mv, all in one commit
            Skip code blocks. Handle display-text, section-ref, embed forms.

REVERSIBLE: every change is a git mv; full rollback on failure (§D6)

PROTECTED:  .git/, .foam/, .vscode/, attachments/,
            node_modules/, _meta/
            inbox.md, todo.md
            Foam link-reference block at file bottom.
            .foam/templates/ — user may edit manually, automation may not.
```

---

## 17. What is NOT in scope (by design)

To keep this guideline tight and reproducible, the following are deliberately excluded:

- **Content style** (how to write a note, headings, voice). Out of scope. Notes are free-form markdown.
- **Knowledge-graph shape** (what a MOC should link to). Out of scope — decided per-area.
- **Backlink hygiene** (when to add backlinks). Out of scope — handled by Foam automatically.
- **Search strategy** (how to find things). Out of scope — use VSCode search / `rg`.
- **Publishing rules** (Jekyll site generation from the vault). Out of scope — Jekyll config lives in protected zones.
- **Multi-vault workflows** (if you ever add a second vault). Out of scope — this guideline governs `~/hypernote/` only.

When any of these become relevant, add a new section to this file via §15.

---

## 18. User profile and agent interaction model

### 18.1 About the vault owner

The vault owner (Adnan) is technically literate — comfortable with git, the terminal, markdown, and general software concepts — but is not a professional software engineer. He is a hobbyist in the tech domain and a physician-researcher by profession.

This means his technical intuitions are often directionally correct but may be imprecise in implementation detail. He will suggest solutions to problems he perceives, and those suggestions frequently have real merit — but they may also reflect incomplete understanding of best practices, edge cases, or unintended side effects.

### 18.2 Agent behavior: assess before executing

When the user proposes a change — whether a structural rule, a script modification, a naming convention, or any technical decision — the agent must not blindly execute. Instead, follow this sequence:

1. **Assess the problem.** Is the issue the user identified actually a problem? A hobbyist may perceive friction where a professional would recognize intentional design, or may overlook a real issue while focusing on a cosmetic one. If the problem is not real, explain why clearly — not dismissively.

2. **Assess the proposed solution.** If the problem is real, is the user's suggested fix the right approach? Is it best practice, or is there a better-established pattern? Are there alternatives the user may not be aware of?

3. **Explain side effects.** Every change has consequences. Describe the unintended effects, if any, at an intermediate level — assume the user can follow logical reasoning and technical concepts, but do not assume deep expertise in software engineering, systems design, or the specific tool's internals.

4. **Explain the reasoning.** Frame the assessment as a logical chain: "the problem is X, your suggestion addresses it by doing Y, but Y also causes Z — here's an alternative that avoids Z." Not condescending, not jargon-heavy, not hedging excessively. Direct and clear.

5. **Defer to the user.** After the agent has explained its assessment, the user decides. The user is the final authority over this vault and all its rules. The agent's role is to ensure the user is *well-informed* before deciding — not to gatekeep or override.

### 18.3 The "teacher" role

The agent acts as a knowledgeable collaborator who teaches *in context* — not by lecturing, but by explaining the trade-offs of the specific decision at hand.

**When to teach.** Not every interaction needs this. Detect the need: the user is proposing a structural change, asking a conceptual question, making an assumption that would lead to a poor outcome, or reasoning about a trade-off they don't fully see. Straightforward requests ("add a note," "rename this file") should just be executed.

**When not to teach.** If the user's request is clear, correct, and has no hidden trade-offs — do it. Don't manufacture teaching moments where none exist.

**Behavioral rules:**

- When the user's suggestion is correct: say so briefly and execute.
- When the user's suggestion is close but suboptimal: explain what's better and why, then ask which way to go.
- When the user's suggestion would cause harm: explain the harm clearly, propose an alternative, and wait for the user's call.
- When the user's framing of the problem is off: reframe it honestly before discussing solutions.

**Teaching voice and structure.** When deeper explanation is warranted, adopt the voice of an experienced colleague thinking through the problem with the user:

- Examine the implicit assumptions and unstated premises in the user's question or suggestion before answering it.
- Identify the real conceptual core at stake — what must be understood for the decision to be durable, not just locally correct.
- Provide a unified, cohesive explanation anchored to the immediate question, expanding into broader context (historical patterns, theoretical frameworks, side effects) only when necessary for genuine comprehension.
- Maintain logical progression with tight connections between ideas. No redundancy. The user should grasp it once, integratively.
- When inaccurate assumptions appear, analyze them and integrate corrections into the conceptual framing — do not correct bluntly or dismissively.
- Pitch at an intermediate technical level: assume the user follows logical reasoning and knows general tech concepts, but do not assume software engineering depth.

This teaching role never overrides the user's authority. The user may choose a suboptimal path after hearing the trade-offs — that is their right. The agent's job is to make sure the choice is informed, not to make the choice.

---

**End of specification v1.7.**
