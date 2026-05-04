# user_management — HTTP Driving Adapter

## Controllers

| Router | Prefix | File |
|---|---|---|
| `auth_v1` | `/auth` | `controllers/auth_controller.py` |
| `user_v1` | `/users` | `controllers/user_controller.py` |

Both are registered in `src/app/main.py` via `app.include_router()`.

## Request/Response pattern

Controllers are thin — they only:
1. Parse the request body into a Pydantic schema
2. Build a command/query object
3. Call the application service
4. Return the result (FastAPI serialises it)

No business logic lives here.

## Dependencies (`dependencies/`)

| Dependency | Returns | Notes |
|---|---|---|
| `get_uow()` | `UnitOfWork` | `request.app.container.get_uow()` — new instance per request |
| `get_authentication_service()` | `AuthenticationService` | singleton from container |
| `current_user()` | `UUID` | verifies JWT via `HTTPBearer`; returns `user_id` |

`current_user` uses `HTTPBearer` — returns 403 for a missing header (FastAPI default). Should be subclassed as `JWTBearer` to return 401 with `WWW-Authenticate: Bearer` header per RFC 6750.

## Schemas (`schemas/`)

Pydantic models for HTTP request/response. They are not domain objects — they exist only at the adapter boundary. Do not reuse domain VOs as schemas.
