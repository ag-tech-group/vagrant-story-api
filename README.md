<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/logo-light.png">
  <img alt="AG Technology Group" src=".github/assets/logo-light.png" width="200">
</picture>

# vagrant-story-api

[![CI](https://github.com/ag-tech-group/vagrant-story-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ag-tech-group/vagrant-story-api/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Game data API for [Vagrant Story](https://en.wikipedia.org/wiki/Vagrant_Story). Part of the [criticalbit.gg](https://criticalbit.gg) gaming tools platform. Pairs with [vagrant-story-web](../vagrant-story-web).

Live API docs (Swagger UI): [vagrant-story-api.criticalbit.gg/docs](https://vagrant-story-api.criticalbit.gg/docs)

## API surface

- **All data routes are versioned under `/v1`** — `GET /v1/blades`, `GET /v1/enemies/{id}`, `GET /v1/drops?item=...`, etc. Infrastructure routes (`/`, `/health`, `/docs`, `/.well-known/security.txt`) stay unversioned.
- **Game data is public and read-only** — no auth needed for blades, armor, gems, grips, materials, consumables, enemies, areas, rooms, chests, drops, spells, abilities, rankings, crafting, workshops, and the rest.
- **Per-user routes require a CriticalBit account** — `/v1/user/inventories/*` (inventory CRUD plus PS1 memory-card save import) and `POST /v1/loadout` (equipment optimizer) authenticate via the `criticalbit_access` JWT cookie issued by [criticalbit-auth-api](../../criticalbit/criticalbit-auth-api), verified against its JWKS.
- **Rate limited** — 60 requests/minute per client IP by default (some routes are exempt). Behind Cloud Run this relies on `--proxy-headers` so the client IP comes from `X-Forwarded-For`.
- **`/.well-known/security.txt`** — RFC 9116 contact info for vulnerability reports.

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
