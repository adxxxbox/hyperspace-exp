# Hyperspace

This document explains the current perspective of the Hyperspace project. It should be understandable without reading the existing vault, the old secretary files, or the current migration scaffold.

This is not yet the final rulebook. It is a continuously evolving design document: what Hyperspace is trying to become, how its main parts relate to each other, and what boundaries should stay clear as the structure evolves.

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
- Keep operator behaviour, rules, tools, and logs modular.
- Add or remove an operator with a single edit, not a ripple of edits.
- Preserve retired material in one archive.
- Keep communication simple: a person should be able to say where something belongs without reading a long manual.

## Main zones

```text
migration/
  AGENTS.md                        ← root registry + routing
  Hyperspace Agreement.md          ← this document
  Workspace/                       ← User-facing active material
  _agentic/                        ← internal operator and rule layer
```

`Workspace/` is the User-facing work area.

`_agentic/` is the internal agentic layer.

`AGENTS.md` is the **single** registry for active operators and the only entry point for routing decisions. There is no second routing file.

The Workspace / `_agentic` distinction is the most important boundary in Hyperspace.

## Workspace

`Workspace/` contains the active material the User directly uses: notes, maps, inbox items, captures, and freeform working folders.

Workspace is intentionally flexible. It may contain folders, but no fixed project/area/resource/card/journal backbone is imposed.

Folders inside Workspace are created by convenience. A folder can exist for a project, topic, period, person, workflow, or anything else that makes sense at the time.

Current Workspace backbone:

```text
Workspace/
  Home.md
  Inbox.md
  Task Capture.md
  Map.md
  Managed/
    Tasks.md
    Calendar.md
```

`Home.md` is the main entry point into active work.

`Inbox.md` is for fast capture of notes and free-form thoughts before routing. It is not for tasks.

`Task Capture.md` is the User-facing capture queue for tasks. The User writes tasks here in any quick form. The `task-manager` operator drains entries into `Managed/Tasks.md` and clears them from this file. The User reads the active task list directly in `Managed/Tasks.md`, which means managed files must be human-readable, not opaque internal artefacts.

There is no calendar capture file. Calendar items normally arrive via import (Epic, email invites, etc.) into `Managed/Calendar.md`. Rare freeform calendar mentions can be written into `Inbox.md` and routed by the `signal-router`.

`Map.md` is the User-facing map of content. It helps navigate Workspace through links and context.

`Managed/` contains active content that is still owned by the User but is actively maintained by operators.

## Managed

`Workspace/Managed/` exists because some active content belongs in Workspace but is maintained by operators.

Tasks and calendar items are examples. They are User-facing and about real life and work, but an operator may maintain them.

Files inside `Managed/` use the same human-readable naming style as the rest of Workspace. The folder itself encodes the operator-ownership boundary; no extra suffix is needed.

Signal routing is behaviour, not a separate User-facing content category. The `signal-router` scans Workspace for signals and routes findings into managed tasks or managed calendar items. Its process history belongs in its own operator log.

## \_agentic

`_agentic/` is the technical internal layer. It contains the mechanics of Hyperspace: shared rules, operator instructions, operator logs, and archive.

`_agentic/` should feel different from Workspace. Workspace names are friendly and human-facing. `_agentic` names are technical, lowercase kebab-case, with uppercase typed suffixes.

Current `_agentic` structure:

```text
_agentic/
  conventions.CORE.md              ← single governance file
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

There is intentionally no `core-rules/` folder, no `tools/` folder, and no tool registry yet. Each of these is in the deferred-modules table below with an explicit graduation trigger.

## Operators

Operators are the agentic workers in Hyperspace.

They are called operators, not employees or personas. The User is the person Hyperspace serves; operators are workers inside the system.

Each operator gets one folder under `_agentic/operators/`:

```text
_agentic/operators/<operator-name>/
  <operator-name>.OPERATOR.md
  <operator-name>.LOG.md
```

The `.OPERATOR.md` file defines what the operator does, what it can read, what it can write, and how it should behave.

The `.LOG.md` file records the operator's workflow history: handoffs, decisions, activity traces, and notable changes.

The operator log is not the same as the active content the operator manages. For example, the task manager's process history belongs in `_agentic/operators/task-manager/task-manager.LOG.md`, but the active task content belongs in `Workspace/Managed/Tasks.md`.

## Current operators

The active list is maintained in `AGENTS.md`. Current placeholders:

- `task-manager` — drains `Task Capture.md` into `Managed/Tasks.md`; maintains the active task list.
- `calendar-manager` — maintains `Managed/Calendar.md` from imports.
- `signal-router` — scans `Inbox.md` and other Workspace notes for signals that should become tasks or calendar items.

## Archive

There is one archive: `_agentic/archive/`. It is the single place for inactive, retired, superseded, or preserved material from anywhere in Hyperspace.

It may contain retired User material, but only because that material is inactive or preserved. Active User material belongs in Workspace or `Workspace/Managed/`, not archive.

The archive is inside `_agentic` because it is part of the system's storage and maintenance layer, not part of active Workspace.

Archive sub-organisation is added when real archived material exists in volume. The backbone does not prescribe archive subfolders yet.

## File naming

Workspace files use a human-readable style: first letter capitalised, spaces allowed, additional capitalisation as the name warrants. This matches how any person would name a document.

Examples:

```text
Home.md
Inbox.md
Task Capture.md
Map.md
Tasks.md         (inside Managed/)
Calendar.md      (inside Managed/)
```

Files in `_agentic/` use `name.TYPE.ext`:

- The base name is lowercase kebab-case.
- The type extension is uppercase.
- The final extension is the real file format.

Examples:

```text
conventions.CORE.md
task-manager.OPERATOR.md
task-manager.LOG.md
```

Current type extensions:

| Type        | Meaning                                |
| ----------- | -------------------------------------- |
| `CORE`      | Shared governance file                 |
| `OPERATOR`  | Behaviour spec for one operator        |
| `LOG`       | History log for one operator           |
| `ARCHIVE`   | Archive overview or archive-related notes |

New typed suffixes are added only when a new file class genuinely exists. They are not pre-declared.

## Where things go

| Item                                | Location                                                   | Reason                                                  |
| ----------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
| A normal project note               | `Workspace/` or a convenient Workspace subfolder           | It is User-facing active work                           |
| A fast captured note or thought     | `Workspace/Inbox.md`                                       | It is freeform, not yet routed, and not a task          |
| A quick task to be organised later  | `Workspace/Task Capture.md`                                | It is a write-only capture queue drained by `task-manager` |
| The main map of notes               | `Workspace/Map.md`                                         | It is User-facing navigation                            |
| The active task list (read view)    | `Workspace/Managed/Tasks.md`                               | Operator-maintained source of truth, kept human-readable |
| Operator-maintained calendar data   | `Workspace/Managed/Calendar.md`                            | Active User content maintained by an operator           |
| Instructions for an operator        | `_agentic/operators/<name>/<name>.OPERATOR.md`             | Defines operator behaviour                              |
| Operator history                    | `_agentic/operators/<name>/<name>.LOG.md`                  | Records what the operator did                           |
| Shared rules and routing            | `_agentic/conventions.CORE.md`                             | Single governance file until pressure forces a split    |
| Active operator list and routing entry | `AGENTS.md`                                             | Single registry; "drop folder + add one line"           |
| Retired material                    | `_agentic/archive/`                                        | Inactive or preserved                                   |

## Boundaries

The main boundary is:

```text
Workspace  = active User-facing material
_agentic   = internal operator and system material
```

The second boundary is:

```text
Workspace/Managed     = active User-owned material maintained by operators
_agentic/operators    = operator behaviour and history
```

When a managed file has a User-facing capture counterpart, keep the boundary explicit:

```text
Workspace/Task Capture.md      = User-facing capture queue (write-only, drained by operator)
Workspace/Managed/Tasks.md     = operator-maintained source of truth (User-readable)
Workspace/Managed/Calendar.md  = operator-maintained source of truth (User-readable)
```

There is no calendar capture file. Calendar items enter `Managed/Calendar.md` through imports or via `Inbox.md` plus the `signal-router`.

Operator instructions and operator logs belong in `_agentic/operators/` because they describe how the operator behaves and what it has done.

## Growth rule

A new file or folder enters Hyperspace only when there is concrete pressure for it: a real workflow, a real duplication, a real permissions need, or a real navigation pain. "It might be useful later" is not pressure. The empty-placeholder pattern is forbidden.

This rule applies to everything: operators, tools, core-rule splits, archive subfolders, managed files, and Workspace folders.

## Adding an operator

1. Create the folder: `_agentic/operators/<operator-name>/`.
2. Create `<operator-name>.OPERATOR.md` and `<operator-name>.LOG.md` inside it.
3. Add one row to the **Active operators** table in `AGENTS.md`.

That is the entire registration process. No other file needs to be edited.

If the operator maintains active User-facing content, create the relevant file under `Workspace/Managed/` only when real active content exists to maintain.

## Deferred modules

These modules are not part of the backbone. Each will be added when its trigger fires.

| Deferred module                                            | Add it when |
| ---------------------------------------------------------- | ----------- |
| `_agentic/tools/registry.jsonc`                            | Two operators independently define the same tool, OR a tool needs permission rules, OR the User cannot remember what tools exist. |
| `_agentic/tools/<tool-name>.TOOL.md` (per-tool docs)       | A tool's definition outgrows a paragraph inside the registry. |
| `_agentic/router.CORE.md` (split out)                      | Routing logic in `conventions.CORE.md` exceeds about fifty lines, OR routing changes pollute the conventions diff history. |
| `_agentic/permissions.CORE.md` (split out)                 | The first sensitive tool exists, OR three or more operators have meaningfully different read/write boundaries. |
| `_agentic/org-chart.CORE.md` (split out)                   | Five or more operators exist. |
| `_agentic/context-loading.CORE.md` (split out)             | Context-loading rules diverge per operator class and need a shared spec. |
| Drain contract for `Task Capture.md`                       | Right before implementing the `task-manager` operator. Blocks task-manager from being implementable, but does not block the backbone. |
| Log rotation rule                                          | The first operator log becomes hard to read. |
| Archive subfolders                                         | Real archived material exists in volume that browsing flat becomes painful. |

## Design principles

Keep Workspace human and free.

Keep `_agentic` technical and minimal.

Prefer one real module over many imaginary departments.

Add a module only when concrete pressure forces it, not because a category sounds useful.

Put active User-facing content in Workspace.

Put operator-maintained active content in `Workspace/Managed/`.

Put operator behaviour and history in `_agentic/operators/`.

Put shared rules in `_agentic/conventions.CORE.md` until pressure forces a split.

Use typed filenames where boundaries matter.

Keep archive unified unless a real need forces a split.

Keep communication simple enough that a future reader can answer: "Who owns this, and where does it go?"

## Open questions

The exact format inside `Managed/Tasks.md` and `Managed/Calendar.md` is not decided yet. Because the User reads these files directly, the chosen format must be human-readable, not opaque structured data.

The drain contract for `Task Capture.md` is not yet written. It needs to specify trigger condition (on-demand, on-invocation, or scheduled), preservation behaviour on parse failure, and a marker the operator leaves so an empty file is unambiguous (just-drained vs never-used). Until this is written, the `task-manager` operator cannot be implemented. On drain, the original line should be moved to the operator log rather than deleted, so nothing is ever truly lost.

The final migration from the old vault structure has not happened yet.
