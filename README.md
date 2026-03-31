# Enterprise Task Management

A backend API built with **Hexagonal Architecture** and **Domain-Driven Design (DDD)** principles, using Python, FastAPI, and SQLAlchemy (async). This project is a deliberate study in applying enterprise patterns — the goal is not just to make it work, but to make it architecturally honest.

---

## Why Hexagonal Architecture?

Most tutorials couple the domain logic tightly to the framework or database. The moment you swap SQLAlchemy for something else, or FastAPI for a CLI, everything breaks. Hexagonal Architecture (Ports & Adapters) solves this by enforcing a strict rule: **the domain knows nothing about the outside world**.

- The domain defines *interfaces* (ports) for what it needs (e.g. a user repository)
- The infrastructure provides *implementations* (adapters) of those interfaces
- The HTTP layer is just another adapter — the domain doesn't know or care that FastAPI exists

This means the core business logic can be tested without a database, without HTTP, and without any framework.

---

## Architecture Overview

```
src/app/
├── core/                    # Cross-cutting concerns (settings, base exceptions)
├── infrastructure/          # Shared infrastructure (DB engine, session management)
├── interfaces/              # Shared HTTP concerns (exception handlers, API errors)
├── container.py             # Manual dependency injection container
├── main.py                  # FastAPI app entry point with lifespan
│
├── user_management/         # Bounded Context: User Management
│   ├── domain/
│   │   ├── entities/        # User, Team (aggregate roots)
│   │   ├── value_objects/   # UserEmail, UserId, UserMobileNumber, HashedPassword
│   │   ├── ports/
│   │   │   └── driven/      # UserRepository (ABC), UnitOfWork (ABC)
│   │   └── exceptions.py    # Domain exceptions
│   ├── application/
│   │   ├── use_cases/       # CreateUserUseCase
│   │   ├── services/        # UserApplicationService
│   │   ├── commands/        # CreateUserCommand
│   │   └── dtos/            # UserDTO
│   ├── adapters/
│   │   └── driving/fast_api/ # HTTP controllers, schemas, FastAPI dependencies
│   └── infrastructure/
│       └── persistence/     # AsyncSQLUserRepository, AsyncSQLUnitOfWork, ORM models
│
└── task_management/         # Bounded Context: Task Management
```

### Dependency Rule

```
domain  ←  application  ←  adapters / infrastructure
```

Arrows point inward only. The domain has zero imports from any outer layer.

---

## DDD Concepts in Practice

### Bounded Contexts

The system is split into `user_management` and `task_management` — two independent bounded contexts. Each has its own domain model, application layer, and infrastructure. They share no domain objects; if a concept appears in both, it is represented separately in each context. This prevents the "big ball of mud" where everything depends on everything.

### Aggregate Roots

`User` and `Team` are aggregate roots — the only entry points for modifying their associated data. External code never reaches inside an aggregate to manipulate its internals directly. For example, adding a member to a team goes through `Team.add_member()`, which enforces the rule that only the manager can do so. The aggregate protects its own invariants.

### Value Objects

`UserEmail`, `UserMobileNumber`, `UserId`, and `HashedPassword` are immutable value objects. They carry no identity — two emails with the same address are equal. More importantly, they are self-validating: a `UserEmail` cannot be constructed with an invalid address, so the domain never handles invalid state. There is no need to validate inputs deeper in the stack because corrupt values simply cannot exist.

### Domain Exceptions

Business rule violations surface as typed domain exceptions (`DuplicateUserInformation`, `UserNotFound`, `NotTeamManagerError`, etc.) rather than generic errors or HTTP status codes. This keeps the domain expressive and decoupled — the domain says *what went wrong*, and the adapter layer decides *how to communicate it* to the outside world.

### Repository Pattern

Each aggregate root is accessed through a repository port defined in the domain. The domain declares what it needs (`UserRepository`); the infrastructure delivers it (`AsyncSQLUserRepository`). The domain has no knowledge of SQL, sessions, or any persistence mechanism.

---

## Key Design Decisions

### Value Objects over primitives

`UserEmail`, `UserMobileNumber`, and `UserId` are frozen Pydantic models, not plain strings. This means invalid values can never exist inside the domain — validation happens at construction, not scattered across the codebase.

### Unit of Work pattern

The `UnitOfWork` port groups repository access and transaction management together. Application services open a UoW context, perform operations, and commit — without knowing whether the underlying session is PostgreSQL, SQLite, or an in-memory fake. This made writing tests without a real database trivial.

### Manual DI container

`container.py` wires everything together at startup. A full DI framework would offer more power, but at the cost of indirection and magic — dependencies resolved at runtime, hard to trace without knowing the framework. The manual approach keeps the wiring explicit and readable: you can follow the dependency graph by just reading the code.

### Domain exceptions mapped at the boundary

Domain exceptions (e.g. `DuplicateUserInformation`, `UserNotFound`) are raised inside the domain and caught at the HTTP adapter boundary, where they're translated to appropriate HTTP status codes. The domain never imports anything from FastAPI.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI |
| ASGI server | Uvicorn |
| ORM | SQLAlchemy 2.0 (async) |
| DB drivers | asyncpg (PostgreSQL), aiosqlite (SQLite) |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Validation | Pydantic v2 |
| Testing | pytest, pytest-asyncio |
| Packaging | Poetry |
| Runtime | Python 3.12 |
| Local dev | Docker Compose |

---

## Running the Project

### With Docker Compose (recommended)

```bash
cp .env.example .env        # fill in your values
docker compose -f docker-compose.dev.yml up -d
alembic upgrade head        # run migrations
```

The API will be available at `http://localhost:8000`.

### Locally with Poetry

```bash
poetry install
alembic upgrade head
uvicorn src.app.main:app --reload
```

> Requires a running PostgreSQL instance. Set `DATABASE_URL` in a `.env` file (see `.env.example`).

---

## Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

The app reads `DATABASE_URL` from environment variables, with an optional `.env` file as fallback. Environment variables take precedence.

---

## Running Tests

Tests support three backends, switchable via a CLI flag:

```bash
# In-memory fakes (default, no DB needed)
pytest

# SQLite (lightweight integration tests)
pytest --db sqlite

# PostgreSQL (full integration tests)
pytest --db postgres
```

The in-memory backend uses fake repository and UoW implementations that satisfy the same ports as the real SQLAlchemy adapters. This means application and domain logic is fully tested without ever touching a database.

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/users/` | Create a new user |

Interactive docs available at `http://localhost:8000/docs` when running.
