# task_management — Application Layer

## Call chain (all use cases follow this pattern)

```
HTTP adapter calls application service
  → application service opens UoW (async with uow:)
  → use case: assert actor authorization (raises domain exception if not allowed)
  → use case: WorkflowService.transition(task, target_status)  ← raises InvalidTaskTransition if illegal
  → use case: task.entity_method()                             ← entity updates own fields
  → use case: await uow.task_repo.save(task)
  → application service: await uow.commit()
  → application service: return DTO  (emit event in future)
```

## Use cases

| Use case | Actor | Auth rule | Transition |
|---|---|---|---|
| `CreateTaskUseCase` | Owner | actor is authenticated | → `OPEN` |
| `AssignTaskUseCase` | Owner | `actor.id == task.owner_id` | → `IN_PROGRESS` |
| `CompleteTaskUseCase` | Assignee | `actor.id == task.assignee_id` | → `COMPLETED` |

Authorization is checked in the use case — the `TaskWorkflowService` is actor-agnostic by design.

## Commands

| Command | Fields |
|---|---|
| `CreateTaskCommand` | `title`, `owner_id` |
| `AssignTaskCommand` | `task_id`, `assignee_id`, `actor_id` |
| `CompleteTaskCommand` | `task_id`, `actor_id` |

## Application service

`TaskApplicationService` — wraps all three use cases. Each method opens UoW, delegates to use case, commits.
