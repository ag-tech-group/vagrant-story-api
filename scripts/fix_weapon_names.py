"""Fix weapon field_names to match canonical game names used in crafting recipes."""

import asyncio

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.weapon import Weapon

NAME_FIXES = {
    "Holy_Wind": "Holy_Win",
    "Balbriggin": "Balbriggan",
    "Cranquein": "Cranequin",
    "Khophish": "Khopesh",
}

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def main():
    async with async_session() as session:
        for old, new in NAME_FIXES.items():
            result = await session.execute(
                update(Weapon).where(Weapon.field_name == old).values(field_name=new)
            )
            print(f"  {old} → {new}: {result.rowcount} row(s) updated")
        await session.commit()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
