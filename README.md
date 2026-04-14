<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/logo-light.png">
  <img alt="AG Technology Group" src=".github/assets/logo-light.png" width="200">
</picture>

# vagrant-story-api

[![CI](https://github.com/ag-tech-group/vagrant-story-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ag-tech-group/vagrant-story-api/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Public game data API for [Vagrant Story](https://en.wikipedia.org/wiki/Vagrant_Story). Part of the [criticalbit.gg](https://criticalbit.gg) gaming tools platform.

No authentication required. Read-only.

Live API docs (Swagger UI): [vagrant-story-api.criticalbit.gg/docs](https://vagrant-story-api.criticalbit.gg/docs)

## Development

```bash
# Install dependencies
uv sync

# Set up environment
cp .env.example .env

# Create database and seed
createdb vagrant_story
uv run alembic upgrade head
PYTHONPATH=. uv run python scripts/seed_database.py

# Start dev server
uv run uvicorn app.main:app --reload --port 8002

# Lint and format
uv run ruff check .
uv run ruff format .
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
