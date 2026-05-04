# user_management — Domain Layer

## Entities (`entities/users.py`)

- `User` — extends Pydantic `BaseModel`. Fields: `id`, `mobile_num`, `email_address`, `hashed_password`.
- `Team` — extends Pydantic `BaseModel`. Fields: `id`, `name`, `manager_id`, `members`. Business methods: `add_member`, `remove_member` (enforce manager identity check internally).

## Value Objects (`value_objects/`)

All VOs are frozen Pydantic models with `ConfigDict(frozen=True, extra="forbid")`.

| VO | File | Key field |
|---|---|---|
| `UserId` | `user_info.py` | `id: UUID` (default_factory=uuid4) |
| `UserEmail` | `user_info.py` | `email: EmailStr` |
| `UserMobileNumber` | `user_info.py` | `mobile: str` (len 10–13) |
| `HashedPassword` | `user_info.py` | `hashed_password: str` |
| `TeamId` | `team.py` | `id: UUID` (default_factory=uuid4) |

## Exceptions (`exceptions.py`)

Hierarchy: `DomainError` (core) → `BaseUserManagementError` → specific exceptions.

| Exception | HTTP | Trigger |
|---|---|---|
| `UserNotFound` | 404 | repo lookup fails |
| `DuplicateUserInformation` | 409 | email or mobile already exists |
| `NotTeamManagerError` | 409 | non-manager attempts team operation |
| `MemberAlreadyInTeamError` | 409 | adding existing member |
| `MemberNotInTeamError` | 409 | removing non-member |

## Ports (`ports/driven/`)

- `UserRepository` (ABC) — `save`, `get_by_id`, `get_by_email`, `get_by_mobile`, `exists_by_email`, `exists_by_mobile`
- `UnitOfWork` (ABC) — async context manager; exposes `user_repo` property; `commit`, `rollback`, `flush`

The domain layer imports nothing from application, infrastructure, or adapters.
