#!/bin/sh
set -e

# If alembic_version table doesn't exist, stamp the last schema migration
# so alembic knows the schema is already in place and only runs data migrations.
uv run python -c "
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings

async def check():
    engine = create_async_engine(settings.database_url)
    async with engine.connect() as conn:
        result = await conn.execute(text(
            \"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'alembic_version')\"
        ))
        exists = result.scalar()
    await engine.dispose()
    return exists

if not asyncio.run(check()):
    print('No alembic_version table found — stamping at last schema migration')
    import subprocess
    subprocess.run(['uv', 'run', 'alembic', 'stamp', 'b0d0c8bef8bc'], check=True)
else:
    print('alembic_version table exists')
"

# Apply any pending migrations
uv run alembic upgrade head

# Start the application
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
