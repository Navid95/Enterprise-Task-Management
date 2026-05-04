# user_management — Application Layer

## Use case vs application service

- **Use case** (`use_cases/`) — pure business flow: validates invariants, builds domain objects, calls repo. No transaction management, no infrastructure.
- **Application service** (`services/`) — orchestration: opens UoW, calls the use case, calls `await uow.commit()`, will emit domain events in future. Also handles cross-cutting concerns like password hashing before passing to the use case.

## Call chain (established pattern)

```
HTTP adapter calls application service
  → application service opens UoW (async with uow:)
  → application service calls use case, passing uow.repo and domain objects
  → use case: checks invariants, builds entity, calls repo
  → application service: await uow.commit()
  → application service: returns DTO
```

## Components

| Component | File | Notes |
|---|---|---|
| `CreateUserUseCase` | `use_cases/create_user_use_case.py` | checks duplicate email/mobile, constructs User, saves |
| `UserApplicationService` | `services/user_application_service.py` | hashes password, opens UoW, delegates to use case |
| `AuthenticationService` | `services/authentication_service.py` | login: lookup by email, verify password, issue token |
| `CreateUserCommand` | `commands/create_user_command.py` | raw input DTO from HTTP layer |
| `LoginCommand` | `commands/login_command.py` | email + plain password |
| `UserDTO` | `dtos/user_dtos.py` | output DTO; `from_entity(user)` classmethod |
| `TokenDTO` | `dtos/auth_dto.py` | wraps access token string |

## Ports (application-owned)

- `IPasswordHasher` — `hash_password(plain) → HashedPassword`, `verify(plain, hashed) → bool`
- `IAuthTokenService` — `generate_token(user_id) → str`, `verify_token(token) → UUID`
