# Conventions

The single governance file for Hyperspace. All shared rules every operator must obey live here. This file is the authoritative source for rules; `Hyperspace Agreement.md` is narrative only and links here for any rule.

Sections inside this file are allowed to grow. When a section becomes large enough to dominate the file or to change at a different cadence than the rest, that is the signal to split it into its own `*.CORE.md` next to this one. Until then, do not split.

## Growth rule

A new file or folder enters Hyperspace only when there is concrete pressure for it: a real workflow, a real duplication, a real permissions need, or a real navigation pain. "It might be useful later" is not pressure. The empty-placeholder pattern is forbidden.

This rule applies to everything: operators, tools, core-rule splits, archive subfolders, managed files, and Workspace folders.

## Operator activation

When activating an operator for a request:

1. Read the operator's folder: `_agentic/operators/<operator-name>/`.
2. Read its `<operator-name>.OPERATOR.md` for behaviour and permissions.
3. Read its `<operator-name>.LOG.md` only if prior history is relevant to the current task.
4. Read the managed files the operator owns (per `AGENTS.md`).
5. Do not read other operators' files unless the request explicitly crosses operators.

Minimal context loading is the default. Loading more than is needed is a violation.

## Adding an operator

1. Create the folder: `_agentic/operators/<operator-name>/`.
2. Create `<operator-name>.OPERATOR.md` and `<operator-name>.LOG.md` inside it.
3. Add one row to the **Active operators** table in `AGENTS.md`.

That is the entire registration process. No other file is edited.

If the operator maintains active User-facing content, create the relevant file under `Workspace/Managed/` only when real active content exists to maintain.

## Retiring an operator

1. Move the operator's entire folder into `_agentic/archive/`.
2. Remove its row from the **Active operators** table in `AGENTS.md`.
3. If the operator owned managed files in `Workspace/Managed/`, decide whether those files are still needed: if yes, document the new owner in `AGENTS.md`; if no, move them to `_agentic/archive/`.

## Routing

All routing decisions begin at `AGENTS.md`. The active-operators table there is the only source of truth for which operators exist.

If a request does not map to any operator, it is User-direct and no operator is loaded.

If a request spans operators, the first operator handles its part, then hands off via its log.

(Split into `router.CORE.md` when this section exceeds about fifty lines or routing changes start polluting the diff history of this file.)

## Permissions

Defaults:

- Every operator may read its own folder and the files listed under it in the `AGENTS.md` registry.
- Every operator may write only to the files listed under "Writes" for it in `AGENTS.md`, plus its own `*.LOG.md`.
- No operator may modify `AGENTS.md`, `Hyperspace Agreement.md`, this file, or any other operator's folder.
- No operator may delete files. Retired material moves to `_agentic/archive/`.
- The User may write anywhere.

Permissions are honour-system in a single-User setup; structural enforcement is not provided.

(Split into `permissions.CORE.md` when the first sensitive tool exists, or when three or more operators have meaningfully different boundaries.)

## File naming

- `Workspace/` uses human style: first letter capitalised, spaces allowed, additional capitalisation as the name warrants. Example: `Task Capture.md`.
- `_agentic/` uses tech style: lowercase kebab-case base names with uppercase typed suffixes. Example: `task-manager.OPERATOR.md`.
- The `Managed/` folder inside Workspace marks the operator-ownership boundary; files inside it use the human style without an extra suffix.

Typed suffixes currently in use inside `_agentic/`:

| Suffix | Meaning |
| --- | --- |
| `CORE` | Shared governance file |
| `OPERATOR` | Behaviour spec for one operator |
| `LOG` | History log for one operator |
| `ARCHIVE` | Archive overview or archive-related notes |

New suffixes are added only when a new file class genuinely exists. They are not pre-declared.

## Where things go

| Item                                | Location                                                   | Reason                                                  |
| ----------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
| A normal project note               | `Workspace/` or a convenient Workspace subfolder           | User-facing active work                                 |
| A fast captured note or thought     | `Workspace/Inbox.md`                                       | Freeform, not yet routed, and not a task                |
| A quick task to be organised later  | `Workspace/Task Capture.md`                                | Write-only capture queue drained by `task-manager`      |
| The main map of notes               | `Workspace/Map.md`                                         | User-facing navigation                                  |
| The active task list (read view)    | `Workspace/Managed/Tasks.md`                               | Operator-maintained source of truth, kept human-readable |
| Operator-maintained calendar data   | `Workspace/Managed/Calendar.md`                            | Active User content maintained by an operator           |
| Instructions for an operator        | `_agentic/operators/<name>/<name>.OPERATOR.md`             | Defines operator behaviour                              |
| Operator history                    | `_agentic/operators/<name>/<name>.LOG.md`                  | Records what the operator did                           |
| Shared rules and routing            | `_agentic/conventions.CORE.md`                             | Single governance file until pressure forces a split    |
| Active operator list and routing entry | `AGENTS.md`                                             | Single registry; "drop folder + add one line"           |
| Retired material                    | `_agentic/archive/`                                        | Inactive or preserved                                   |

## Archive

There is one archive: `_agentic/archive/`. Anything retired from anywhere in Hyperspace goes here. The archive has no internal structure until real archived material exists in volume.

## Logs

Each operator maintains its own `*.LOG.md` inside its own folder. Logs are append-only narrative: handoffs, decisions, notable changes, drained items.

Log rotation is not yet defined. When a log becomes hard to read, archive the older portion under `_agentic/archive/` and start a fresh log file. (Split into a dedicated rotation rule when this happens for the first time.)

## Deferred modules

These modules are not in the backbone yet. Each will be added when its trigger fires.

| Deferred module                                            | Add it when |
| ---------------------------------------------------------- | ----------- |
| `_agentic/tools/registry.jsonc`                            | Two operators independently define the same tool, OR a tool needs permission rules, OR the User cannot remember what tools exist. |
| `_agentic/tools/<tool-name>.TOOL.md` (per-tool docs)       | A tool's definition outgrows a paragraph inside the registry. |
| `_agentic/router.CORE.md` (split out)                      | Routing logic in this file exceeds about fifty lines, OR routing changes pollute the diff history of this file. |
| `_agentic/permissions.CORE.md` (split out)                 | The first sensitive tool exists, OR three or more operators have meaningfully different read/write boundaries. |
| `_agentic/org-chart.CORE.md` (split out)                   | Five or more operators exist. |
| `_agentic/context-loading.CORE.md` (split out)             | Context-loading rules diverge per operator class and need a shared spec. |
| Drain contract for `Task Capture.md`                       | Right before implementing the `task-manager` operator. Blocks `task-manager` from being implementable, but does not block the backbone. |
| Managed-file schema (for `Tasks.md`, `Calendar.md`)        | Right before the first operator writes to a managed file. |
| Operator-output conventions (log format, handoff style)    | When the first `*.OPERATOR.md` is written; lifted to this file once a pattern is settled. |
| Log rotation rule                                          | The first operator log becomes hard to read. |
| Archive subfolders                                         | Real archived material exists in volume that browsing flat becomes painful. |
