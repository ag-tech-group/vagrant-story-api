<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset=".github/assets/logo-light.png">
  <img alt="AG Technology Group" src=".github/assets/logo-light.png" width="200">
</picture>

# vagrant-story-api

[![CI](https://github.com/ag-tech-group/vagrant-story-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ag-tech-group/vagrant-story-api/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Public game data API for [Vagrant Story](https://en.wikipedia.org/wiki/Vagrant_Story). Part of the [criticalbit.gg](https://criticalbit.gg) gaming tools platform.

No authentication required. Read-only. All data extracted from the game.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/weapons` | List all weapons (blades) |
| GET | `/weapons/{id}` | Get weapon by ID |
| GET | `/grips` | List all weapon grips |
| GET | `/grips/{id}` | Get grip by ID |
| GET | `/armor` | List all armor and shields |
| GET | `/armor/{id}` | Get armor piece by ID |
| GET | `/gems` | List all gems |
| GET | `/gems/{id}` | Get gem by ID |
| GET | `/materials` | List all crafting materials |
| GET | `/materials/{id}` | Get material by ID |
| GET | `/consumables` | List all consumable items |
| GET | `/consumables/{id}` | Get consumable by ID |
| GET | `/health` | Health check |

### Query parameters

- `offset` / `limit` — pagination (default: offset=0, limit=50)
- `q` — search by name (e.g., `/weapons?q=katana`)
- `blade_type` — filter weapons by type (`/weapons?blade_type=Sword`)
- `type` — filter armor by type (`/armor?type=Shield`, `?type=Helm`, `?type=Body`, etc.)

## Data

Game data extracted from [korobetski/Vagrant-Story-Unity-Parser](https://github.com/korobetski/Vagrant-Story-Unity-Parser) (hardcoded C# databases). Descriptions are in French (from the French game version). English names cross-referenced with Data Crystal wiki.

| Category | Count |
|----------|-------|
| Weapons (blades) | 90 |
| Grips | 31 |
| Armor + Shields | 111 |
| Gems | 46 |
| Materials | 7 |
| Consumables | 29 |

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

### Data extraction

To re-extract game data from source:

```bash
python3 scripts/extract_data.py
```

Requires the [Vagrant-Story-Unity-Parser](https://github.com/korobetski/Vagrant-Story-Unity-Parser) repo cloned to `~/apps/criticalbit/data-extraction/`.

## License

Apache 2.0 — see [LICENSE](LICENSE).
