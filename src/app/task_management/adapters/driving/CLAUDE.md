# task_management — HTTP Driving Adapter

## Controllers

| Router | Prefix | File |
|---|---|---|
| `task_v1` | `/tasks` | `fast_api/controllers/task_controller.py` |

Register in `src/app/main.py` via `app.include_router(task_v1)`.

## Endpoints

| Method | Path | Use case | Auth | Returns |
|---|---|---|---|---|
| `POST` | `/tasks/` | `CreateTask` | JWT (any user) | 201 + task id |
| `PATCH` | `/tasks/{id}/assign` | `AssignTask` | JWT (owner enforced in use case) | 200 |
| `PATCH` | `/tasks/{id}/complete` | `CompleteTask` | JWT (assignee enforced in use case) | 200 |

## Pattern

Controllers are thin — parse schema → build command → call application service → return result. No business logic here.

`current_user` dependency provides the authenticated `user_id: UUID` passed into commands as `actor_id`.
