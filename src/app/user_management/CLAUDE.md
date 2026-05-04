# user_management context

## Responsibility

Owns everything related to users and teams: registration, authentication, profile, team membership. Nothing outside this context imports domain objects from here — other contexts reference users by `UserId` (plain UUID wrapper) only.

## Aggregates

- **User** — core aggregate. Fields: `id` (UserId), `mobile_num` (UserMobileNumber), `email_address` (UserEmail), `hashed_password` (HashedPassword)
- **Team** — secondary aggregate. Fields: `id` (TeamId), `name`, `manager_id` (UserId), `members` (set[UserId]). Business methods: `add_member`, `remove_member` (enforce manager check).

## Layer map

```
domain/         → User, Team entities; VOs; domain exceptions; UserRepository + UoW ports
application/    → use cases; application services; commands; DTOs; IPasswordHasher, IAuthTokenService ports
infrastructure/ → AsyncSQLUserRepository; AsyncSQLUnitOfWork; Argon2PasswordHasher; JWTTokenService; ORM models
adapters/driving/fast_api/ → auth_controller, user_controller; schemas; dependencies
```
