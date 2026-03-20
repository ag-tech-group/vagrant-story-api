# Vagrant Story API

FastAPI service providing game data for Vagrant Story (PS1). Python 3.12, SQLAlchemy 2.0 (async), PostgreSQL, Alembic migrations.

## Commands

```bash
uv sync                                          # Install deps
uv run uvicorn app.main:app --reload --port 8002  # Dev server
uv run alembic upgrade head                       # Run migrations
uv run ruff check .                               # Lint
uv run ruff format .                              # Format
uv run pytest                                     # Tests
PYTHONPATH=. uv run python scripts/seed_database.py  # Seed DB from JSON
```

Pre-commit: ruff check --fix → ruff format → pytest. CI runs lint + test on push/PR.

Docker alternative: `docker compose up` (API on :8002, Postgres on :5433).

## Database

PostgreSQL with async SQLAlchemy (`asyncpg`). Connection string in `.env`:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/vagrant_story
```

## Architecture

### Models (`app/models/`)

SQLAlchemy 2.0 Mapped column style. Common fields across item models:

```python
id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
game_id: Mapped[int] = mapped_column(Integer, default=0)
field_name: Mapped[str] = mapped_column(String(100))
name: Mapped[str] = mapped_column(String(100))
description_fr: Mapped[str] = mapped_column(String(500), default="")
wep_file_id: Mapped[int] = mapped_column(Integer, default=0)
```

**Stat column naming** — Python attrs use `_stat` suffix, DB columns use short names:
```python
str_stat: Mapped[int] = mapped_column("str", Integer, default=0)
int_stat: Mapped[int] = mapped_column("int", Integer, default=0)
agi_stat: Mapped[int] = mapped_column("agi", Integer, default=0)
```

**Affinity columns** (on Armor, Gem, Material): `human`, `beast`, `undead`, `phantom`, `dragon`, `evil`, `fire`, `water`, `wind`, `earth`, `light`, `dark`

**Damage type columns** (on Armor, Grip): `blunt`, `edged`, `piercing`, `physical`

Export all models from `app/models/__init__.py`.

### Schemas (`app/schemas/game_data.py`)

Pydantic v2 with `serialization_alias` to output short JSON keys:

```python
class WeaponRead(BaseModel):
    str_stat: int = Field(serialization_alias="str")
    int_stat: int = Field(serialization_alias="int")
    model_config = {"from_attributes": True, "populate_by_name": True}
```

### Routes (`app/routers/`)

Consistent pattern for all endpoints:

```python
router = APIRouter(prefix="/weapons", tags=["weapons"])

@router.get("", response_model=list[WeaponRead])
async def list_weapons(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(Weapon)
    if q:
        stmt = stmt.where(Weapon.name.ilike(f"%{q}%"))
    stmt = stmt.order_by(Weapon.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()

@router.get("/{weapon_id}", response_model=WeaponRead)
async def get_weapon(weapon_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Weapon).where(Weapon.id == weapon_id))
    weapon = result.scalar_one_or_none()
    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return weapon
```

Register routers in `app/main.py` via `app.include_router()`.

### Data Files (`data/`)

JSON seed files: `weapons.json`, `armors.json`, `gems.json`, `grips.json`, `materials.json`, `consumables.json`, `crafting_recipes.json`, `material_recipes.json`.

Seeded via `scripts/seed_database.py` which maps `id` → `game_id` and skips if data exists.

### Migrations (`alembic/versions/`)

Schema migrations use `op.create_table()` / `op.add_column()`. Data migrations use `op.execute()` with SQL:

```python
def upgrade() -> None:
    op.add_column("gems", sa.Column("gem_type", sa.String(50), server_default="", nullable=False))
    op.execute("UPDATE gems SET gem_type = 'Weapon' WHERE field_name = 'Talos_Feldspear'")
```

**Important**: When adding NOT NULL columns to tables with existing data, always use `server_default`.

## Conventions

- **Table names**: plural lowercase (`weapons`, `armor`, `crafting_recipes`)
- **Route prefixes**: plural lowercase with hyphens (`/crafting-recipes`)
- **Ruff**: line length 100, target Python 3.12
- **No AI attribution** in commits or PRs
- **Always create PRs** — never push directly to main

## Adding a New Data Type

1. **Model**: Create `app/models/[type].py`, export from `app/models/__init__.py`
2. **Schema**: Add `[Type]Read` class to `app/schemas/game_data.py`
3. **Router**: Create `app/routers/[type].py`, register in `app/main.py`
4. **Migration**: `uv run alembic revision --autogenerate -m "add [type] table"`, then add data inserts
5. **Data**: Create `data/[type].json` and update `scripts/seed_database.py`
6. **Test**: Add endpoint tests in `tests/test_api.py`
