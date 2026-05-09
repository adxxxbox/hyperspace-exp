# Hyperspace

This is the narrative explanation of Hyperspace. It tells you what the system is, why it is shaped the way it is, and how its main parts relate to each other.

It is **not** the rulebook. All rules — naming, routing, permissions, where things go, how to add an operator, deferred modules — live in [`_agentic/conventions.CORE.md`](_agentic/conventions.CORE.md). When narrative and rules disagree, the rules win, and this document is wrong and must be updated.

## What Hyperspace is

Hyperspace is a personal operating environment built out of notes, tasks, calendars, logs, and agent instructions.

The User is the centre of the system. The User's life, work, projects, ideas, responsibilities, notes, and decisions are what Hyperspace exists to support.

Operators are agentic workers that help manage parts of the system. They are not the centre. They do not own the User's work. They maintain selected workflows on the User's behalf.

Hyperspace should feel like an organised virtual office, but it should not become bureaucratic. Structure exists only where it helps.

## Goals

Hyperspace should make it easy to:

- Capture ideas, tasks, notes, and commitments quickly.
- Keep active work visible without forcing a rigid folder taxonomy.
- Let operators manage tasks, calendar items, and similar workflows without mixing their instructions into the User's notes.
- Add or remove an operator with a single edit, not a ripple of edits.
- Preserve retired material in one archive.
- Keep communication simple: a person should be able to say where something belongs without reading a long manual.

## Main zones

```text
migration/
  AGENTS.md                        ← single registry of active operators + routing entry
  Hyperspace Agreement.md          ← this document (narrative)
  Workspace/                       ← User-facing active material
  _agentic/                        ← internal operator and rule layer
```

`Workspace/` is the User-facing work area.

`_agentic/` is the internal agentic layer.

`AGENTS.md` is the single source of truth for which operators are active. Adding or removing an operator is a one-line edit there.

The Workspace / `_agentic` distinction is the most important boundary in Hyperspace.

## Workspace

`Workspace/` contains the active material the User directly uses: notes, maps, inbox items, captures, and freeform working folders.

Workspace is intentionally flexible. It may contain folders, but no fixed project/area/resource backbone is imposed. Folders are created by convenience.

The Workspace backbone:

```text
Workspace/
  Home.md           ← main entry point into active work
  Inbox.md          ← fast capture of notes and free-form thoughts; not for tasks
  Task Capture.md   ← write-only capture queue for tasks, drained by task-manager
  Map.md            ← User-facing map of content
  Managed/          ← active content maintained by operators
    Tasks.md
    Calendar.md
```

`Task Capture.md` is the User-facing capture queue. The User writes tasks there in any quick form. The `task-manager` operator drains entries into `Managed/Tasks.md` and clears them. The User reads the active task list directly in `Managed/Tasks.md`, which means managed files must be human-readable, not opaque internal artefacts.

There is no calendar capture file. Calendar items normally arrive via import (Epic, email invites, etc.) into `Managed/Calendar.md`. Rare freeform calendar mentions can be written into `Inbox.md` and routed by the `signal-router`.

## Managed

`Workspace/Managed/` exists because some active content belongs in Workspace but is maintained by operators.

Tasks and calendar items are examples. They are User-facing and about real life and work, but an operator may maintain them. The folder itself encodes the operator-ownership boundary; no extra filename suffix is needed.

Signal routing is behaviour, not a separate User-facing content category. The `signal-router` scans Workspace for signals and routes findings into managed tasks or managed calendar items. Its process history belongs in its own operator log.

## \_agentic

`_agentic/` is the technical internal layer. It contains the mechanics of Hyperspace: shared rules, operator instructions, operator logs, and archive.

`_agentic/` should feel different from Workspace. Workspace names are friendly and human-facing. `_agentic` names are technical, lowercase kebab-case, with uppercase typed suffixes.

The `_agentic` layout:

```text
_agentic/
  conventions.CORE.md              ← single governance file (the rulebook)
  operators/
    task-manager/
      task-manager.OPERATOR.md
      task-manager.LOG.md
    calendar-manager/
      calendar-manager.OPERATOR.md
      calendar-manager.LOG.md
    signal-router/
      signal-router.OPERATOR.md
      signal-router.LOG.md
  archive/
```

There is no `core-rules/` folder, no `tools/` folder, and no tool registry yet. These are listed as deferred modules in the rulebook, with explicit graduation triggers. They will appear when concrete pressure forces them, not before.

## Operators

Operators are the agentic workers in Hyperspace.

They are called operators, not employees or personas. The User is the person Hyperspace serves; operators are workers inside the system.

Each operator gets one folder under `_agentic/operators/` containing two files: an `*.OPERATOR.md` defining behaviour and permissions, and an `*.LOG.md` recording the operator's workflow history.

The operator log is not the same as the active content the operator manages. The task manager's process history belongs in `task-manager.LOG.md`, while the active task content belongs in `Workspace/Managed/Tasks.md`.

## Current operators

The active list is `AGENTS.md`. Today the placeholders are:

- `task-manager` — drains `Task Capture.md` into `Managed/Tasks.md`; maintains the active task list.
- `calendar-manager` — maintains `Managed/Calendar.md` from imports.
- `signal-router` — scans `Inbox.md` and other Workspace notes for signals that should become tasks or calendar items.

None are implemented yet.

## Archive

There is one archive: `_agentic/archive/`. It is the single place for inactive, retired, superseded, or preserved material from anywhere in Hyperspace.

The archive is inside `_agentic` because it is part of the system's storage and maintenance layer, not part of active Workspace. Active User material belongs in Workspace or `Workspace/Managed/`, not archive.

## Boundaries

The main boundary:

```text
Workspace  = active User-facing material
_agentic   = internal operator and system material
```

The second boundary:

```text
Workspace/Managed     = active User-owned material maintained by operators
_agentic/operators    = operator behaviour and history
```

When a managed file has a User-facing capture counterpart, the boundary is explicit:

```text
Workspace/Task Capture.md      = User-facing capture queue (write-only, drained by operator)
Workspace/Managed/Tasks.md     = operator-maintained source of truth (User-readable)
Workspace/Managed/Calendar.md  = operator-maintained source of truth (User-readable)
```

## Design principles

Keep Workspace human and free.

Keep `_agentic` technical and minimal.

Prefer one real module over many imaginary departments.

Add a module only when concrete pressure forces it, not because a category sounds useful.

Use typed filenames where boundaries matter.

Keep archive unified unless a real need forces a split.

Keep communication simple enough that a future reader can answer: "Who owns this, and where does it go?"

## Open questions

The exact format inside `Managed/Tasks.md` and `Managed/Calendar.md` is not decided yet. Because the User reads these files directly, the chosen format must be human-readable, not opaque structured data.

The drain contract for `Task Capture.md` is not yet written. It needs to specify trigger condition, preservation behaviour on parse failure, and a marker the operator leaves so an empty file is unambiguous (just-drained vs never-used). Until this is written, the `task-manager` operator cannot be implemented. On drain, the original line should be moved to the operator log rather than deleted, so nothing is ever truly lost.

The operator runtime is not yet decided. "Operator" is currently a conceptual role; the backbone does not commit to whether operators are slash commands, skills, MCP servers, scheduled jobs, or manual prompts. The first operator implementation will lock this in by accident unless the choice is made deliberately first.

The final migration from the old vault structure has not happened yet.
