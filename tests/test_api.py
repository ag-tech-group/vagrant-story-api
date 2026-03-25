from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blade import Blade
from app.models.enemy import Enemy, EnemyBodyPart
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


class TestEnemies:
    async def test_list_empty(self, client: AsyncClient):
        resp = await client.get("/enemies")
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_with_data(self, client: AsyncClient, session: AsyncSession):
        enemy = Enemy(
            name="Bat",
            enemy_class="Beast",
            hp=40,
            mp=0,
            str_stat=97,
            int_stat=65,
            agi_stat=90,
        )
        session.add(enemy)
        await session.commit()

        resp = await client.get("/enemies")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Bat"
        assert data[0]["enemy_class"] == "Beast"
        assert data[0]["str"] == 97
        assert data[0]["int"] == 65
        assert data[0]["agi"] == 90

    async def test_get_by_id_with_body_parts(self, client: AsyncClient, session: AsyncSession):
        enemy = Enemy(
            name="Bat",
            enemy_class="Beast",
            hp=40,
            mp=0,
            str_stat=97,
            int_stat=65,
            agi_stat=90,
        )
        session.add(enemy)
        await session.flush()

        bp = EnemyBodyPart(
            enemy_id=enemy.id,
            name="Body",
            physical=-5,
            air=25,
            fire=-10,
            earth=-25,
            water=10,
            light=-5,
            dark=5,
            blunt=0,
            edged=-10,
            piercing=-5,
        )
        session.add(bp)
        await session.commit()

        resp = await client.get(f"/enemies/{enemy.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Bat"
        assert len(data["body_parts"]) == 1
        assert data["body_parts"][0]["name"] == "Body"
        assert data["body_parts"][0]["physical"] == -5
        assert data["body_parts"][0]["air"] == 25

    async def test_not_found(self, client: AsyncClient):
        resp = await client.get("/enemies/999")
        assert resp.status_code == 404

    async def test_search(self, client: AsyncClient, session: AsyncSession):
        session.add(
            Enemy(
                name="Bat", enemy_class="Beast", hp=40, mp=0, str_stat=97, int_stat=65, agi_stat=90
            )
        )
        session.add(
            Enemy(
                name="Dragon",
                enemy_class="Dragon",
                hp=480,
                mp=0,
                str_stat=118,
                int_stat=132,
                agi_stat=95,
            )
        )
        await session.commit()

        resp = await client.get("/enemies?q=bat")
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Bat"


class TestMaterials:
    async def test_list_with_data(self, client: AsyncClient, session: AsyncSession):
        session.add(Material(name="Iron", tier=4, str_modifier=1, int_modifier=1, agi_modifier=-2))
        await session.commit()

        resp = await client.get("/materials")
        assert resp.status_code == 200
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Iron"
        assert resp.json()[0]["str_modifier"] == 1
