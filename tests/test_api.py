from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blade import Blade
from app.models.material import Material


class TestHealth:
    async def test_health(self, client: AsyncClient):
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "healthy"}

    async def test_root(self, client: AsyncClient):
        resp = await client.get("/")
        assert resp.status_code == 200
        assert resp.json()["service"] == "vagrant-story-api"


class TestBlades:
    async def test_list_empty(self, client: AsyncClient):
        resp = await client.get("/blades")
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_with_data(self, client: AsyncClient, session: AsyncSession):
        blade = Blade(
            game_id=1,
            field_name="Test_Sword",
            name="Test Sword",
            description_fr="Une epee de test.",
            blade_type="Sword",
            damage_type="Edged",
            risk=1,
            str_stat=10,
            int_stat=0,
            agi_stat=-1,
            range_stat=3,
            damage=5,
        )
        session.add(blade)
        await session.commit()

        resp = await client.get("/blades")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Sword"
        assert data[0]["str"] == 10
        assert data[0]["range"] == 3

    async def test_get_by_id(self, client: AsyncClient, session: AsyncSession):
        blade = Blade(
            game_id=5,
            field_name="Katana",
            name="Katana",
            blade_type="Great Sword",
            damage_type="Edged",
            str_stat=16,
            range_stat=4,
        )
        session.add(blade)
        await session.commit()

        resp = await client.get(f"/blades/{blade.id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Katana"

    async def test_not_found(self, client: AsyncClient):
        resp = await client.get("/blades/999")
        assert resp.status_code == 404

    async def test_search(self, client: AsyncClient, session: AsyncSession):
        session.add(
            Blade(
                game_id=1,
                field_name="A",
                name="Claymore",
                blade_type="Great Sword",
                damage_type="Edged",
            )
        )
        session.add(
            Blade(
                game_id=2,
                field_name="B",
                name="Dagger",
                blade_type="Dagger",
                damage_type="Piercing",
            )
        )
        await session.commit()

        resp = await client.get("/blades?q=clay")
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Claymore"


class TestMaterials:
    async def test_list_with_data(self, client: AsyncClient, session: AsyncSession):
        session.add(Material(name="Iron", tier=4, str_modifier=1, int_modifier=1, agi_modifier=-2))
        await session.commit()

        resp = await client.get("/materials")
        assert resp.status_code == 200
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Iron"
        assert resp.json()[0]["str_modifier"] == 1
