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

# Start script: stamp alembic if first run, then apply pending migrations
COPY start.sh ./
RUN chmod +x start.sh

CMD ["./start.sh"]
