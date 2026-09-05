# Contributing

Thanks for your interest in contributing to the Telco SI reference BSS/OSS API.

## Code of Conduct

Be respectful and constructive. This is a reference implementation meant for learning and reuse.

## Getting Started

1. Fork the repository.
2. Set up the environment as described in [docs/OPERATIONS.md](docs/OPERATIONS.md).
3. Create a feature branch: `git checkout -b feature/your-feature`.

## Development Workflow

1. **Understand the domain boundaries** — keep changes within the appropriate schema/context (`catalog`, `inventory`, `crm`, `usage`, `billing`, `dunning`). Do not introduce cross-schema foreign keys; rely on global identifiers (`UUID`, `MSISDN`, `ICCID`).
2. **Declarative entities** — define or modify entities as single-class `SQLModel` structures.
3. **Migrations** — after model changes, autogenerate and apply an Alembic revision:

   ```bash
   docker compose exec app alembic revision --autogenerate -m "description"
   docker compose exec app alembic upgrade head
   ```

4. **Seeding** — if you change the data model, update the seeder and its distribution (see [docs/SEEDING.md](docs/SEEDING.md)) so seeded data remains aligned and lifecycle-representative.
5. **Test** — add or update smoke tests covering your changes, including Dunning state transitions.
6. **Document** — update the relevant file under `docs/` (see the README table of contents).

## Commit Conventions

- Use clear, imperative commit messages.
- Scope the subject to the domain, e.g. `billing: mark invoices overdue before dunning`.
- Note any Dunning/collections lifecycle impact in the message body.

## Pull Requests

- Verify the full flow: migrations apply, seeder runs, API starts, smoke tests pass.
- Keep the docs tree in sync with code changes.
- Reference the issue or feature your PR addresses.

## Reporting Issues

Include:
- Reproduction steps.
- Expected vs actual behavior.
- Relevant logs or `docker compose` output.
