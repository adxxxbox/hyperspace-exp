# Hyperspace

This document explains the current perspective of the Hyperspace project. It should be understandable without reading the existing vault, the old secretary files, or the current migration scaffold.

This is not yet the final rulebook. It is a continuously evolving design document: what Hyperspace is trying to become, how its main parts relate to each other, and what boundaries should stay clear as the structure evolves.

## What Hyperspace is

Hyperspace is a personal operating environment built out of notes, tasks, calendars, logs, and agent instructions.

The User is the center of the system. The User's life, work, projects, ideas, responsibilities, notes, and decisions are what Hyperspace exists to support.

Operators are agentic workers that help manage parts of the system. They are not the center. They do not own the User's work. They maintain selected workflows on the User's behalf.

Hyperspace should feel like an organized virtual office, but it should not become bureaucratic. Structure exists only where it helps.

## Goals

Hyperspace should make it easy to:

- Capture ideas, tasks, notes, and commitments quickly.
- Keep active work visible without forcing a rigid folder taxonomy.
- Let operators manage tasks, calendar items, and similar workflows without mixing their instructions into the User's notes.
- Keep operator behavior, rules, tools, and logs modular.
- Add future operators without redesigning the whole vault.
- Make boundaries obvious from filenames and folder locations.
- Preserve retired material in one archive.
- Keep communication simple: a person should be able to say where something belongs without reading a long manual.

## Main zones

The future structure currently has two main zones:

```text
Workspace/
_agentic/
```

`Workspace/` is the User-facing work area.

`_agentic/` is the internal agentic layer.

The distinction is the most important boundary in Hyperspace.

## Workspace

`Workspace/` contains the active material the User directly uses: notes, maps, inbox items, active views, and freeform working folders.

Workspace is intentionally flexible. It may contain folders, but no fixed project/area/resource/card/journal backbone is imposed.

Folders inside Workspace should be created by convenience. A folder can exist for a project, topic, period, person, workflow, or anything else that makes sense at the time.

Workspace organization should be supported by:

- links,
- tags,
- context,
- search,
- lightweight maps,
- and folders only where helpful.

Current Workspace backbone:

```text
Workspace/
  Home.md
  Inbox.md
  Tasks.md
  Outlines.md
  Workspace Overview.md
  Delegated/
    Tasks.DELEGATED.md
    Calendar.DELEGATED.md
```

`Home.md` is the main entry point into active work.

`Inbox.md` is for fast capture before routing.

`Tasks.md` is the User-facing task view. It may summarize, link to, or surface task information, but it does not have to be the full task database.

`Outlines.md` is the User-facing map of content. It helps navigate Workspace through links and context.

`Workspace Overview.md` briefly explains the purpose of Workspace.

`Delegated/` contains active content that is still about the User's life and work, but is actively maintained by operators.

## Delegated

`Workspace/Delegated/` exists because some active content belongs in Workspace but is not purely freeform writing.

Tasks and calendar items are examples. They are User-facing and about real life/work, but an operator may maintain them.

Current delegated files:

```text
Workspace/
  Delegated/
    Tasks.DELEGATED.md
    Calendar.DELEGATED.md
```

`Tasks.DELEGATED.md` is the operator-managed task source or working task file.

`Calendar.DELEGATED.md` is the operator-managed calendar source or working calendar file.

There is intentionally no `Lookups.DELEGATED.md`.

Lookup work is behavior, not a separate User-facing content category. The lookup operator scans Workspace for signals and routes findings into delegated tasks or delegated calendar items. Its process history belongs in its own operator log.

## \_agentic

`_agentic/` is the technical internal layer. It contains the mechanics of Hyperspace: shared rules, tool descriptions, operator instructions, operator logs, and archive.

`_agentic/` should feel different from Workspace. Workspace names may be friendly and human-facing. `_agentic` names should be technical, explicit, and consistent.

Current `_agentic` structure:

```text
_agentic/
  core-rules/
    overview.CORE.md
    router.CORE.md
    org-chart.CORE.md
    conventions.CORE.md
    permissions.CORE.md
    context-loading.CORE.md
    registry.TOOL.jsonc
    overview.TOOL.md

  operators/
    overview.OPERATOR.md
    task-manager/
      task-manager.OPERATOR.md
      task-manager.LOG.md
    calendar-manager/
      calendar-manager.OPERATOR.md
      calendar-manager.LOG.md
    note-lookup/
      note-lookup.OPERATOR.md
      note-lookup.LOG.md

  archive/
    overview.ARCHIVE.md
```

## core-rules

`_agentic/core-rules/` contains the shared operating layer.

It holds rules and technical definitions that may be used by multiple operators. It also holds the tool registry or tool-related descriptions.

Current core-rule files:

```text
overview.CORE.md
router.CORE.md
org-chart.CORE.md
conventions.CORE.md
permissions.CORE.md
context-loading.CORE.md
registry.TOOL.jsonc
overview.TOOL.md
```

`router.CORE.md` will describe how requests are routed to the correct operator or workflow.

`org-chart.CORE.md` will describe the operator map and authority boundaries.

`conventions.CORE.md` will describe always-on system conventions.

`permissions.CORE.md` will describe read/write boundaries.

`context-loading.CORE.md` will describe what an operator should read for a given task.

`registry.TOOL.jsonc` will map tool-like capabilities or triggers to implementation details.

## Operators

Operators are the agentic workers in Hyperspace.

They are called operators, not employees or personas. The User is the person Hyperspace serves; operators are workers inside the system.

Operators live here:

```text
_agentic/operators/
```

Each operator gets one folder:

```text
_agentic/operators/<operator-name>/
```

Each operator folder contains:

```text
<operator-name>.OPERATOR.md
<operator-name>.LOG.md
```

The `.OPERATOR.md` file defines what the operator does, what it can read, what it can write, and how it should behave.

The `.LOG.md` file records the operator's workflow history: handoffs, decisions, activity traces, and notable changes.

The operator log is not the same as the active content the operator manages. For example, the task manager's process history belongs in:

```text
_agentic/operators/task-manager/task-manager.LOG.md
```

But the active task content belongs in:

```text
Workspace/Delegated/Tasks.DELEGATED.md
```

## Current operators

Current operator placeholders:

```text
task-manager
calendar-manager
note-lookup
```

`task-manager` manages delegated tasks.

`calendar-manager` manages delegated calendar items.

`note-lookup` scans Workspace for signals that may become tasks or calendar items.

The name `note-lookup` may still be revisited. Its current meaning is: read notes or other allowed sources, identify actionable signals, and route those signals into tasks or calendar items.

## Archive

There is one archive:

```text
_agentic/archive/
```

The archive is the single place for inactive, retired, superseded, or preserved material from anywhere in Hyperspace.

The archive is inside `_agentic` because it is part of the system's storage and maintenance layer, not part of active Workspace.

Archive organization should be added when real archived material exists. The backbone does not prescribe archive subfolders yet.

## File naming

Workspace can use normal human-readable filenames.

Examples:

```text
Home.md
Inbox.md
Tasks.md
Outlines.md
Workspace Overview.md
```

Delegated files use a type extension because they have a special ownership boundary:

```text
Tasks.DELEGATED.md
Calendar.DELEGATED.md
```

Files in `_agentic/` use:

```text
name.TYPE.ext
```

The base name is lowercase kebab-case.

The type extension is uppercase.

The final extension is the real file format.

Examples:

```text
task-manager.OPERATOR.md
task-manager.LOG.md
conventions.CORE.md
registry.TOOL.jsonc
overview.ARCHIVE.md
```

Current type extensions:

| Type        | Meaning                                                             |
| ----------- | ------------------------------------------------------------------- |
| `CORE`      | Shared rules, routing, permissions, context loading, and governance |
| `TOOL`      | Tool registries or tool-related descriptions                        |
| `OPERATOR`  | Instructions for one operator                                       |
| `LOG`       | Workflow history for one operator                                   |
| `ARCHIVE`   | Archive overview or archive-related notes                           |
| `DELEGATED` | Workspace content actively managed by operators                     |

## Where things go

Use this table when deciding where something belongs.

| Item                             | Location                                                   | Reason                                           |
| -------------------------------- | ---------------------------------------------------------- | ------------------------------------------------ |
| A normal project note            | `Workspace/` or a convenient Workspace subfolder           | It is User-facing active work                    |
| A fast captured thought          | `Workspace/Inbox.md`                                       | It has not been routed yet                       |
| The main map of notes            | `Workspace/Outlines.md`                                    | It is User-facing navigation                     |
| A personal task view             | `Workspace/Tasks.md`                                       | It is a readable task surface                    |
| Operator-managed task data       | `Workspace/Delegated/Tasks.DELEGATED.md`                   | It is active User content managed by an operator |
| Operator-managed calendar data   | `Workspace/Delegated/Calendar.DELEGATED.md`                | It is active User content managed by an operator |
| Instructions for task management | `_agentic/operators/task-manager/task-manager.OPERATOR.md` | It defines operator behavior                     |
| Task manager history             | `_agentic/operators/task-manager/task-manager.LOG.md`      | It records what the operator did                 |
| Shared routing rules             | `_agentic/core-rules/router.CORE.md`                       | It affects multiple operators                    |
| Tool registry                    | `_agentic/core-rules/registry.TOOL.jsonc`                  | It is technical operator infrastructure          |
| Retired material                 | `_agentic/archive/`                                        | It is inactive or preserved                      |

## Boundaries

The main boundary is:

```text
Workspace = active User-facing material
_agentic = internal operator/system material
```

The second boundary is:

```text
Workspace/Delegated = active User-facing material managed by operators
_agentic/operators = operator behavior and history
```

Tasks and calendars belong in `Workspace/Delegated/` because they are about the User's real commitments.

Operator instructions and operator logs belong in `_agentic/operators/` because they describe how the operator behaves and what it has done.

## Modularity rule

Do not create a module just because a category sounds useful.

A module should exist only when it has:

- a real function,
- a clear owner,
- a clear input/output boundary,
- and a reason to be separate from existing modules.

This prevents Hyperspace from becoming a maze of imaginary departments.

## Adding a future operator

When a new operator is genuinely needed, add one folder:

```text
_agentic/operators/<new-operator>/
```

Inside it, add:

```text
<new-operator>.OPERATOR.md
<new-operator>.LOG.md
```

If the operator manages active User-facing content, create the relevant delegated file under:

```text
Workspace/Delegated/
```

Only create a delegated file when there is real active content to manage.

## Design principles

Keep Workspace free.

Keep `_agentic` technical.

Prefer one real module over many imaginary departments.

Do not create a folder just because a category exists in theory.

Put active User-facing content in Workspace.

Put operator-managed active content in `Workspace/Delegated/`.

Put operator behavior and history in `_agentic/operators/`.

Put shared rules and tools in `_agentic/core-rules/`.

Use typed filenames where boundaries matter.

Keep archive unified unless a real need forces a split.

Keep communication simple enough that a future reader can answer: "Who owns this, and where does it go?"

## Open questions

The name `note-lookup` may change if a clearer operator name emerges.

The exact format inside delegated task and calendar files is not decided yet.

The exact archive organization is not decided yet.

The final migration from the old vault structure has not happened yet.
