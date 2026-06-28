# Sprint 02 — Plan

## Architecture

Strict Clean Architecture with 4 layers:

```
presentation/  ← HTTP handlers, DTOs, routing
application/   ← Use cases (orchestration + validation)
domain/        ← Entities, repository traits, value objects
infrastructure/ ← SQLx repository implementations, DB pool
```

## Data Flow

```
HTTP Request
  → Handler (DTO extraction)
    → Use Case (validation + orchestration)
      → Repository trait (domain contract)
        → SQLx impl (DB query)
          → PostgreSQL (ev schema)
```

## Implementation Order

1. Domain entities + value objects + repository traits
2. Infrastructure (DB pool + SQLx repositories)
3. Application use cases
4. Presentation handlers + routes
5. Wire up main.rs
6. Tests
7. Documentation
