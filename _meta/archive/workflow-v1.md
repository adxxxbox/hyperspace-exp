---
title: "Foam vault workflow (ARCHIVED v1 — retired 2026-04-19, see _meta/modes/ and _meta/features/ for current recipes)"
created: 2026-04-11
tags: [meta]
---

# Foam vault workflow

**This is the operational manual.** The guideline (`_meta/vault-organization-guideline.md`) tells you *what* the rules are. This doc tells you *how to do things* — one recipe per task, short enough to fit on screen.

If any recipe below contradicts the guideline, the guideline wins. Fix the recipe.

## Daily loop (read me first)

1. Capture everything new to `inbox.md`. No thinking.
2. Once a day (usually before you close the laptop), triage `inbox.md`: each line either becomes a note somewhere, a task in an existing note, or gets deleted.
3. Before any commit, run `python3 _meta/scripts/vault_check.py`. Exit 0 or don't commit.
4. End of week, open `_archive/` and move anything finished.

That's it. The rest of this file is one recipe per task you'll run into.

---

## Capturing a thought right now

**Goal:** get it out of your head in under ten seconds.

1. Open `inbox.md` (VSCode command palette → `Foam: Open Daily Note` then switch to `inbox.md`, or just `Cmd+P` → `inbox`).
2. Append a bullet or a checkbox at the bottom. Don't bother with tags or structure.
3. Save. Done.

Do **not** create a new file from inbox capture. Triage decides placement later. Only the triage step writes real notes.

---

## Triaging `inbox.md`

For each line in `inbox.md`, pick one:

- **Throw it out.** Delete the line.
- **It's a task for an existing note.** Cut the line, paste it into the right note under a `## Tasks` heading. Delete from inbox.
- **It's a new idea/reference worth a note.** Follow "Adding a new note" below, then delete from inbox.
- **It's a reminder with a date.** Put it on the right daily journal file (future-dated) or as a `- [ ] … 📅 YYYY-MM-DD` in `todo.md`.

After triage, `inbox.md` should be empty or nearly empty. That's the win condition.

---

## Adding a new note

**Goal:** a new `.md` file, correctly placed, correctly named, compliant from birth.

1. Walk the §4 placement decision tree in your head: is it journal, a project, an area, a resource, an atlas note, or a card? **First-hit wins.** Don't debate.
2. Pick the slug. Letters/digits only, hyphens between words, no spaces, no dots, no underscores. Case is preserved — you can write `DELIRIUM-review-2026` or `delirium-review-2026`, but not both in the same folder.
3. In VSCode: `Cmd+N` → save to the chosen folder with the slug → Foam will inject the template's frontmatter. **Don't type frontmatter by hand.** Templates live in `.foam/templates/`.
4. Write the note.
5. Before committing, run `vault_check.py`. If it's clean, `git add` + `git commit`.

If the decision tree points two ways, go read §4 again, then make a call. Don't invent a new folder.

---

## Writing today's daily journal

**Goal:** open the daily note for today and start writing.

1. VSCode command palette → `Foam: Open Daily Note`.
2. Foam creates `journal/YYYY-MM-DD.md` from `.foam/templates/daily-note.md` with `type: daily-note` and `created: <today>`.
3. Write. Tag with inline `#topic/...` or frontmatter `tags: […]` as needed.
4. Commit whenever — daily notes can accumulate across many commits.

**Never** rename a daily note. Its slug is the date.

---

## Starting a new project

**Goal:** a new folder under `1-projects/` that holds all work for an ongoing effort.

1. Pick a project slug. Same slug grammar as notes. Prefer a short noun phrase: `delirium-review-2026`, `ercp-protocol`, `grant-k23-draft`.
2. `mkdir 1-projects/<slug>/` by hand (or via VSCode). **Never** commit an empty folder; add at least one real note first.
3. Create the project's anchor note inside the folder. Common conventions:
   - `<slug>/README.md` or `<slug>/overview.md` — one-line purpose, milestones, links.
   - Or just `<slug>/<first-real-note>.md` if it's small.
4. Add tasks inline as `- [ ]` with optional `📅 YYYY-MM-DD`.
5. Run `vault_check.py`. A folder with exactly one file will trigger an F5 warning — that's fine during startup; add the second note within a day or two, or accept the warning.

**Do not** create `1-projects/<slug>/docs/`, `1-projects/<slug>/notes/`, or any other sub-sub-folder. Depth is capped at 3 (§F4). If a project grows deep, flatten first, then ask whether it should split.

---

## Renaming a note (or moving it between folders)

**Goal:** change a slug or a folder without breaking any inbound wikilink.

**Never use `git mv` alone.** It bypasses the wikilink sweep. Use the wrapper:

```bash
./_meta/scripts/rename-note.sh <old-path> <new-path>
```

What the wrapper does, in order:
1. Refuses to run if the working tree is dirty. Commit or stash first.
2. Runs `rename_note.py --dry-run` and prints every wikilink that would change.
3. Prompts you to confirm.
4. `git mv` the file.
5. Applies the wikilink sweep to all files in the vault.
6. Stages everything.
7. Commits as a single atomic rename commit.

If you chicken out at the prompt, the tree is still clean. If the sweep errors partway through, the commit never happens and you can `git restore`.

**Forbidden destinations:** anything listed in `config.jsonc → protected.directories` or `protected.files`. The wrapper refuses.

---

## Archiving a finished project

**Goal:** move `1-projects/<slug>/` to `_archive/1-projects/<slug>/` without breaking links.

1. Verify the project is actually done — no open `- [ ]` tasks, no unresolved TODO comments.
2. Use `git mv` to move the whole folder: `git mv 1-projects/<slug> _archive/1-projects/<slug>`.
3. Wikilinks that reference notes inside the folder do **not** need updating, because Foam resolves by slug alone and slugs are globally unique. A `[[kickoff-notes]]` link still resolves after the file moves from `1-projects/alpha/kickoff-notes.md` to `_archive/1-projects/alpha/kickoff-notes.md`.
4. Run `vault_check.py`.
5. Commit as `archive: <slug>`.

Same recipe applies to `2-areas/`, `3-resources/`, and `5-cards/` — each has a mirror subfolder in `_archive/`.

**If the project has broken wikilinks you want to redirect first,** fix them before the move. The archive move is not the place to rewrite links.

---

## When `vault_check.py` complains

**Exit code 1 means you cannot commit yet.** Don't override it.

For each rule code the auditor prints, do this:

| Code | What to do |
|---|---|
| **F2** (unknown top-level folder) | Move the file into one of the eight canonical top-level folders. If you created a stray folder, remove it. |
| **F4** (depth > 3) | Flatten. A note four levels deep is always wrong. Move files up. |
| **F5** (single-file subfolder) — *warning* | Either add more files to the folder, or flatten it by one level. Acceptable to ignore short-term during project bootstrap. |
| **N1** (bad slug grammar) | Rename with the wrapper. Only filesystem-illegal chars (`/ \ : * ? " < > |` or control chars) and leading/trailing space/dot are rejected — everything else is allowed (v1.8). |
| **N2a** (case-collision in folder) | Rename one of them. Two files differing only in case is invalid. |
| **M1** (missing required frontmatter) | Add `title:` and/or `created:` at the top. If the whole block is missing, use the Foam template as a reference — don't hand-type unless you have to. |
| **M2** (forbidden frontmatter key) | Delete `status`/`folder`/`category`/`project`/`date`/`path`/`modified` from the frontmatter. Those are inferred from location. |
| **M4** (bad `created` format) | Rewrite the value as `YYYY-MM-DD`. Do not invent a new date — use the actual creation date (git log if you have to). |
| **P3** (broken Foam link-reference block) | Let Foam regenerate it. Delete the orphan marker, save the file, and let Foam re-create the block next time it runs. Never hand-edit this region. |
| **L3** (slug collision across vault) | Two different folders contain `foo.md`. Rename one with the wrapper. Slugs must be globally unique. |

Once the vault is clean again (`0 error(s)`), commit.

---

## Adding a new frontmatter key (schema growth)

**Goal:** introduce a new key like `aliases` or `authors` without breaking existing files. Schema changes are rare and deliberate.

Follow §7.1 of the guideline, in order:

1. Amend §7 of the guideline. Specify name, type, required/optional, mutable/immutable, rationale.
2. Update **both** Foam templates (`.foam/templates/new-note.md` and `.foam/templates/daily-note.md`) to inject the new key.
3. Decide back-fill:
   - **Optional key, no back-fill needed:** stop. Existing files stay valid.
   - **Required key, or you want uniform coverage:** write a one-shot migration script that walks the vault, injects the key into each existing file, dry-runs first, produces a diff report, commits as `migration: add <key> frontmatter (YYYY-MM-DD)`.
4. Update `vault_check.py` to validate the new key (add it to `frontmatter.required` in `config.jsonc` and/or add a new rule code).
5. Bump `config.jsonc` `_self.version` and `_self.guideline_version`. Add a line to `_meta/changelog.md`. Commit.

**Do not promote an optional key to required before back-filling.** That floods `vault_check` with false failures.

---

## Adding a new `type` value

**Goal:** use a new `type:` frontmatter value like `type: experiment` or `type: case-report`.

1. Open `_meta/note-types.md`.
2. Add a `### <new-type>` section with a one-line definition and at least one example.
3. Commit the registry update **in the same commit** as the first file using the new type.

Foam does **not** auto-discover `type` values, so the registry is the only source of truth. Tags, by contrast, are discovered automatically (Tag Explorer) and have no registry — see §M3.

---

## Amending the guideline itself

**Goal:** change a rule, not just a file.

1. Open `_meta/vault-organization-guideline.md`.
2. Make the edit in the spec. Update the Status line (e.g. `v1.4` → `v1.5`). Prepend a changelog entry at the top.
3. Update `_meta/config.jsonc` to match — `_self.version` and `_self.guideline_version` both bump, and any enumerated list that changed is edited.
4. If the change touches scripts (rename logic, vault_check rules), update them and their tests. Run all test suites until green.
5. Add a line to `_meta/changelog.md` describing the rationale.
6. Run `python3 _meta/scripts/vault_check.py` to confirm the vault still validates under the new rules.
7. Commit everything atomically with a message of the form:
   ```
   meta: guideline vN.N — <one-line summary>
   ```

**Tiebreaker:** if the guideline and config disagree after your edit, the guideline wins. Re-derive the config.

---

## Status markers (visual convention for tasks and items)

Open tasks in this vault use the GitHub-flavored `- [ ]` checkbox syntax, per Rule C1 of the guideline. That covers the **binary** open/closed state. For anything that needs a richer status — triaged inbox items, project items at different urgency levels, section headers in a daily note, a TASKS list in an MOC — use this four-marker palette:

| Marker | Meaning | When to use |
|---|---|---|
| ⬜ | **Not started.** | Default for any new item before you begin working on it. Keeps the rest of the list visually quiet so attention-needing items stand out. Optional — omit it if most items are pending and clutter outweighs clarity. |
| 🟡 | **Requires attention.** | The item is open, in flight, not overdue, but needs a look: blocked on a question, partially done, decision pending, waiting on someone. Visually warns without screaming. |
| 🚨 | **MUST RESOLVE — past due.** | The item has a due date that has passed, or is otherwise a hard blocker you cannot ignore. Reserved for *urgent*, not merely *important*. Using it too often dilutes the signal. |
| ✅ | **Completed.** | Done. Verified. Can be archived or left in place for provenance. |

**Rules of use.**

1. **Place the marker at the start of the task text**, inside the checkbox line, as the first visible character after `- [ ]`. Example:
   ```markdown
   - [ ] 🚨 Submit IRB amendment 📅 2026-04-09
   - [ ] 🟡 Review draft from Dr. Smith
   - [ ] ⬜ Draft abstract for AANA
   - [x] ✅ File 2025 taxes
   ```
2. **`🚨` is reserved for real deadlines.** If nothing will break by leaving the task another week, it is 🟡, not 🚨. Overuse destroys the signal.
3. **Promote, don't stack.** An item moves 🟡 → 🚨 when its due date passes, or ⬜ → 🟡 when you pick it up. Never combine markers on one line.
4. **`✅` is redundant with `- [x]`.** They mean the same thing. Using both is fine for visual emphasis in a long list; using only `- [x]` is also fine. Pick one style per file and stay consistent.
5. **These are visual aids, not machine-parsed state.** `vault_check.py` does not read them. They exist to make your eye catch the right thing when you scan a long note. The authoritative state for "is a task done?" is the `[ ]` / `[x]` box; for "is a task past due?", it is the `📅 YYYY-MM-DD` stamp compared to today.
6. **Scope.** This palette applies to task lines and to ad-hoc status labels in prose (e.g., section headers like `## Pending decisions 🟡`). It does not apply to frontmatter, filenames, commit messages, or any other machine-parsed surface.
7. **Not mandatory.** A file with zero status markers is still a compliant file. Use them when they help; skip them when the list is short enough to see at a glance.

**Traffic-light mental model.** ⬜ → 🟡 → 🚨 → ✅ is a progression: quiet → warning → alarm → done. When you review a note, your eye should jump to 🚨 first, 🟡 second, and ignore ⬜ and ✅ as background.

---

## The "I'm about to do something" checklist (for Claude and for you)

Before **any** write, rename, or commit to the vault, mentally run through this:

1. Did I read `_meta/vault-organization-guideline.md` and `_meta/config.jsonc` recently?
2. Is the target path under a protected directory or a protected root file?
3. If it's a new note: does the filename pass `naming.slug_regex` and sit in a canonical folder?
4. If it's a rename: am I using `rename-note.sh`, not bare `git mv`?
5. Did I run `vault_check.py` and see exit 0?
6. Is the commit message specific enough that a future reader knows what changed and why?

If any answer is no, stop and fix it before proceeding. "When in doubt, halt and ask" is rule number one of the agent safety list, and it applies to humans too.

---

## Things this workflow deliberately does NOT cover

- How to write a note (content, voice, structure). Out of scope — notes are free-form markdown.
- Multi-vault sync, backup, or iOS capture. Those get their own decision records in `_meta/decisions/` when the time comes.
- Deep project management (Gantt, status boards). Use `- [ ]` tasks in files; that's the system. If you outgrow it, write a new decision record.

---

**End of workflow v1.0.**
