# syntax=docker/dockerfile:1

# ---------- Builder stage: build the project wheel ----------
FROM python:3.12-slim AS builder

WORKDIR /build

COPY pyproject.toml README.md ./
COPY app ./app

RUN pip install --no-cache-dir build \
    && python -m build --wheel --outdir /wheels

# ---------- Runtime stage ----------
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
COPY alembic.ini ./alembic.ini
COPY pyproject.toml ./pyproject.toml
COPY migrations ./migrations

RUN pip install --no-cache-dir /wheels/*.whl \
    && pip install --no-cache-dir ruff pytest pytest-asyncio httpx

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]