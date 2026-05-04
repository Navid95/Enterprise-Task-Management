# task_management — Domain Layer

## Task entity

Extends `BaseEntity` (non-frozen). Entity owns its own state — business methods update fields internally, nothing outside the entity sets fields directly.

Business methods:
- `assign(assignee_id: UserId)` — sets `assignee_id`, updates any related timestamps internally
- `complete()` — marks entity ready for COMPLETED transition (called after WorkflowService validates)

## Value objects

All extend `BaseValueObject` (frozen).

| VO | Constraint |
|---|---|
| `TaskId` | UUID, default_factory=uuid4 |
| `TaskTitle` | non-empty string |
| `TaskStatus` | enum: `OPEN / IN_PROGRESS / COMPLETED` |

## Workflow domain service (`services/task_workflow.py`)

`TaskWorkflowService.transition(task, target)` enforces valid state transitions only.

| From | To | Allowed |
|---|---|---|
| `OPEN` | `IN_PROGRESS` | Yes |
| `IN_PROGRESS` | `COMPLETED` | Yes |
| anything else | anything else | No → raises `InvalidTaskTransition` |

Actor-agnostic — knows nothing about who is calling. Authorization is checked in the use case before calling this service.

## Exceptions

- `InvalidTaskTransition(DomainError)` — registered in `_DOMAIN_TO_HTTP` → 422

## Ports (`ports/driven/`)

- `ITaskRepository` — `save(task)`, `get_by_id(task_id) → Task`; extended as new query methods are needed
