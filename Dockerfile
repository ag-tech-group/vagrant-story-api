FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY data ./data

# Expose port
EXPOSE 8000

# Sentry release version from CI. Positioned last so COMMIT_SHA changes
# don't invalidate the layer cache for dependency install or code copies.
ARG COMMIT_SHA=unknown
ENV SENTRY_RELEASE=$COMMIT_SHA

CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
