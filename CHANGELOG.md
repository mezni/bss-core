# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adopts [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## Version History

| Version | Feature Domain | Key Objectives |
| --- | --- | --- |
| 0.0.1 | Project foundation | Python project structure, uv, virtual environments, .env, Git |

---

## [0.0.1] - 2026-09-18

### Phase 1 — Project Foundation

**Feature Domain:** Project foundation

**Key Objectives:**

* Python project structure
* `uv` project management
* Virtual environments
* `.env` configuration
* Git version control
* Dependencies

### Added

* `pyproject.toml` with project metadata and core dependencies (langchain, langchain-openrouter, pydantic, python-dotenv)
* `uv.lock` lockfile
* `.env` template for `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` configuration
* `.gitignore` for virtual environments, environment files, and Python caches
* `README.md` project documentation
* `docs/ROADMAP.md` learning roadmap
* Initial Git repository