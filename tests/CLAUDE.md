# tests — Strategy and Infrastructure

## Marker rule

Every test **must** carry `@pytest.mark.unit` or `@pytest.mark.integration`. The `conftest.py` enforces this — unmarked tests fail immediately.

## Backend auto-selection (`conftest.py`)

The `db_backend` fixture reads the `-m` flag at session scope:
- `-m unit` → `"memory"` — all repos and UoW are in-memory fakes, no DB required
- `-m integration` → `"postgres"` — real PostgreSQL, engine initialised once per session

Integration tests are skipped unless explicitly invoked with `-m integration`.

## Fixture pattern

All fixtures are typed against **port interfaces**, not concrete implementations. The same test body runs against both backends.

Key session-scoped fixtures: `engine`, `token_service`, `password_hasher`, `session_factory`
Key function-scoped fixtures: `session`, `seeded_session`, `user_repo`, `seeded_user_repo`, `uow`, `seeded_uow`

`seeded_*` fixtures pre-populate one default user (credentials from `tests/.env`).

## Fakes

| Fake | Location | Implements |
|---|---|---|
| `FakeUserRepoInMemory` | `user_management/adapters/driven/` | `UserRepository` |
| `FakeUnitOfWorkInMemory` | `user_management/infrastructure/persistence/` | `UnitOfWork` |
| `FakePasswordHasher` | `user_management/infrastructure/security/` | `IPasswordHasher` |
| `FakeTokenService` | `user_management/infrastructure/auth/` | `IAuthTokenService` |

When adding task_management fakes: follow the same pattern under `tests/task_management/`.

## Environment

Integration tests require `tests/.env` (see `.env.example`). Unit tests do not read env vars.
