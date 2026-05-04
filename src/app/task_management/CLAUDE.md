# task_management context

## Responsibility

Owns everything related to tasks: creation, assignment, and completion. References users by `UserId` (plain UUID wrapper) only — never imports User or any other domain object from `user_management`.

## Aggregate: Task

| Field | Type | Notes |
|---|---|---|
| `id` | `TaskId` | VO, UUID |
| `title` | `TaskTitle` | VO, required |
| `owner_id` | `UserId` | immutable, set on creation |
| `assignee_id` | `UserId` | nullable, set on assign |
| `status` | `TaskStatus` | enum: `OPEN / IN_PROGRESS / COMPLETED` |
| `created_at` | datetime | immutable |

## Workflow

State transitions are enforced by `TaskWorkflowService` (domain service) — see `domain/CLAUDE.md`. Valid flow: `OPEN → IN_PROGRESS → COMPLETED`.

## Use cases

| Use case | Actor | Transition |
|---|---|---|
| `CreateTask` | Owner | → `OPEN` |
| `AssignTask` | Owner | → `IN_PROGRESS` |
| `CompleteTask` | Assignee | → `COMPLETED` |

## Layer map

```
domain/         → Task entity; VOs; TaskWorkflowService; InvalidTaskTransition; ITaskRepository port
application/    → CreateTask, AssignTask, CompleteTask use cases + TaskApplicationService; commands
infrastructure/ → SQL adapter; ORM model; Alembic migration; UoW task_repo property
adapters/driving/fast_api/ → task_controller; schemas; dependencies
```
