# src/app — Shared Application Concerns

## Dependency Injection (`container.py`)

`Container` is a plain Python class instantiated once in the FastAPI lifespan and attached to `app.container`. All services are wired manually here — no framework.

- **Singletons**: `password_hasher`, `token_service`, `user_application_service`, `auth_service`
- **Transients**: `get_uow()` returns a new `AsyncSQLUnitOfWork` per call (one per request)
- FastAPI dependencies in `adapters/driving/fast_api/dependencies/` resolve services via `request.app.container`
- When adding a new service: instantiate it in `__init__`, expose it via a `get_*()` method

## Exception Flow

```
domain raises DomainError subclass
  → caught by global handler in interfaces/http/fast_api/handlers.py
  → exc_mapper() looks up type in _DOMAIN_TO_HTTP dict (api_exception.py)
  → returns APIException(status_code, error_type, message)
  → JSONResponse sent to client
```

To add a new domain exception:
1. Define it in `{context}/domain/exceptions.py`
2. Register it in `_DOMAIN_TO_HTTP` in `interfaces/http/fast_api/api_exception.py`

Unmapped exceptions default to 500.

## App Factory (`main.py`)

`create_app(settings)` builds the FastAPI app. The lifespan:
1. Calls `init_engine(settings)` — initialises the shared async SQLAlchemy engine
2. Attaches `Container(settings)` to `app.container`
3. On shutdown: calls `await close_engine()`

Routers are registered with `app.include_router()` — one call per context controller.

## Shared Infrastructure (`infrastructure/persistence/`)

- `BaseModel` — SQLAlchemy declarative base; provides `id` (UUID PK) and timestamp columns
- `get_session_factory()` — returns `async_sessionmaker` bound to the shared engine
- `init_engine` / `close_engine` — singleton engine lifecycle; `init_engine` is idempotent (silently ignores second calls — be aware this could mask config changes in tests)
