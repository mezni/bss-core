# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Dunning & Collections Management** incorporated across all foundational pillars:
  - End-to-end delinquency state machine: `FIRST_NOTICE → WARNING → SUSPENDED → TERMINATED | RESOLVED`.
  - Automated due-diligence notices for overdue invoices.
  - Service suspension via **SIM barring** of resources in the Inventory context.
  - Balance settlement flow that resolves cases and restores service.
- Vision, Scope & Assumptions document (see `docs/BRIEF.md`) updated to reflect Dunning & Collections across all pillars.
- Six-schema domain model: `catalog`, `inventory`, `crm`, `usage`, `billing`, `dunning`.
- Declarative `SQLModel` data & API layer.
- Multi-schema Alembic migration support.
- Topological CLI seeder (Faker & Typer) with health-distribution ratios:
  - ~80% `CURRENT`, ~15% `FIRST_NOTICE`/`WARNING`, ~5% `SUSPENDED` (+ barred SIMs).
- Docker Compose development environment (`app`, `db`).
