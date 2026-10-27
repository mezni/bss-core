# Contributing Guide

Thank you for considering contributing to this project!

## Getting Started

1. **Prerequisites**: Make sure you have [`uv`](https://github.com/astral-sh/uv) installed on your machine.
2. **Setup**:
   ```bash
   # Sync virtual environment and install dependencies
   uv sync
   
   # Copy environment variables
   cp .env.example .env
   ```

## Development Workflow

We use standard `make` commands to handle local development tasks:

- **Run Dev Server**: `make dev`
- **Run Tests**: `make test`
- **Run Evaluations**: `make evals`
- **Linting & Formatting**: `make lint`

## Pull Request Guidelines

1. Fork the repository and create your branch from `main`.
2. Ensure all tests and linting checks pass cleanly (`make lint` and `make test`).
3. Push your branch and open a Pull Request with a clear description of your changes.
