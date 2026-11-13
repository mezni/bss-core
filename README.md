# bss-core

A modular monolith FastAPI backend application.

## Overview

This project implements a modular monolith architecture with FastAPI, separating concerns into distinct modules:
- **Auth** - User authentication and authorization
- **Customers** - Customer management with ownership tracking

## Features

- FastAPI-based API with modular structure
- JWT-based authentication with HS256 algorithm
- Bcrypt password hashing via Passlib
- Password complexity validation (8+ chars, mixed case, digit, special char)
- Role-based access control (admin, manager, user)
- Customer ownership linking to authenticated users
- Repository pattern for data access
- Environment-based configuration

## Prerequisites

- Python >= 3.12
- Poetry or pip for dependency management

## Installation

```bash
# Install dependencies
pip install -e .

# Or with poetry
poetry install
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- `SECRET_KEY` - JWT signing key (required for production)
- `DATABASE_URL` - Database connection string
- `ENVIRONMENT` - Set to `production` for prod deployments

## Running

```bash
# Development
uvicorn src.main:app --reload

# Or via the entry point
python run_dev.py
```

API will be available at `http://127.0.0.1:8000`

## API Endpoints

### Auth (`/api/v1/auth`)
- `POST /register` - Register new user
- `POST /login` - Login and receive JWT token

### Customers (`/api/v1/customers`)
- `POST /` - Create customer (authenticated)
- `GET /` - List customers (authenticated, filtered by owner)

## Architecture

```
src/
├── core/          # Core configuration (DB, security, settings)
├── modules/
│   ├── auth/      # Authentication module
│   └── customers/ # Customers module
└── main.py        # FastAPI app assembly
```

## Security

- Passwords hashed with Bcrypt
- JWT tokens signed with SECRET_KEY from environment
- Rate limiting recommended for login/register endpoints
- SECRET_KEY must be set via environment variable in production

## Development

Run tests:
```bash
pytest
```