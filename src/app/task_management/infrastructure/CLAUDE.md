# task_management — Infrastructure Layer

## ORM model (`persistence/models.py`)

`TaskModel` extends shared `BaseModel` (UUID PK + timestamps). Maps to/from domain via:
- `TaskModel.from_entity(task) → TaskModel`
- `task_model.to_entity() → Task`

Domain entity never imports SQLAlchemy.

## Repository (`persistence/async_task_repo_sql.py`)

`AsyncSQLTaskRepository` implements `ITaskRepository`. Minimal interface: `save(task)`, `get_by_id(task_id)`. Extended with new methods only when a use case requires them.

## Unit of Work

`ITaskRepository` is wired into `AsyncSQLUnitOfWork` as a `task_repo` property — follows the same pattern as `user_repo`. The `UnitOfWork` port gains a `task_repo` property.

## Migration

Alembic migration for `tasks` table. Run with `alembic upgrade head`.
