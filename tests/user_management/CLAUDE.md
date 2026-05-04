# tests/user_management

## Test structure mirrors source structure

```
tests/user_management/
├── domain/                   # entity and VO unit tests (Sprint 2 T3)
├── application/
│   ├── use_cases/            # CreateUserUseCase tests
│   └── services/             # AuthenticationService, UserApplicationService tests
├── adapters/
│   ├── driven/               # FakeUserRepoInMemory lives here
│   └── driving/fastapi/      # HTTP controller integration tests
└── infrastructure/
    ├── auth/                 # FakeTokenService + JWTTokenService tests
    ├── persistence/          # FakeUnitOfWorkInMemory + SQL repo integration tests
    └── security/             # FakePasswordHasher + Argon2PasswordHasher tests
```

## Available fakes

| Fake | Notes |
|---|---|
| `FakeUserRepoInMemory` | in-memory dict store; implements full `UserRepository` interface |
| `FakeUnitOfWorkInMemory` | wraps `FakeUserRepoInMemory`; no-op commit/rollback |
| `FakePasswordHasher` | returns `"hashed_{plain}"` deterministically; verify checks prefix |
| `FakeTokenService` | returns `str(user_id)` as token; verify parses UUID back |

## conftest locations

- `tests/user_management/application/conftest.py` — application-layer fixtures
- `tests/user_management/adapters/driving/fastapi/conftest.py` — FastAPI TestClient with overridden container
- `tests/user_management/infrastructure/persistence/conftest.py` — DB-level fixtures
