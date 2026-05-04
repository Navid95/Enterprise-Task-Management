# user_management — Infrastructure Layer

## ORM isolation rule

SQLAlchemy models live **only** in `persistence/models.py`. Domain entities never import SQLAlchemy. Mapping is done via:
- `UserModel.from_entity(user) → UserModel` — domain → ORM
- `user_model.to_entity() → User` — ORM → domain

`UserModel` extends `BaseModel` (shared) which provides `id` (UUID PK) and timestamp columns.

## Unit of Work (`persistence/sql_alchemy_uow.py`)

`AsyncSQLUnitOfWork` is a **transient** — created per request via `container.get_uow()`, never shared.

- Session and repo are created in `__aenter__`, destroyed in `__aexit__`
- `__aexit__` auto-rolls back on any exception before closing the session
- `uow.commit()` must be called **explicitly** by the application service — not automatic
- `uow.user_repo` raises `RuntimeError` if accessed outside `async with uow:`
- New repo properties are added here as new contexts grow (e.g. `uow.task_repo`)

## Repository (`persistence/async_user_repo_sql.py`)

`AsyncSQLUserRepository` implements `UserRepository` port. Uniqueness constraint violations from the DB are caught here and re-raised as `DuplicateUserInformation`.

## Security

- `Argon2PasswordHasher` (`security/argon2_hasher.py`) — implements `IPasswordHasher` using argon2-cffi
- `JWTTokenService` (`auth/jwt_token_service.py`) — implements `IAuthTokenService`; signs/verifies JWT with `ENCRYPTION_KEY` from settings; expiry controlled by `EXPIRY_DURATION`
