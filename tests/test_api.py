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


class TestLaunchGuardrails:
    async def test_security_txt(self, client: AsyncClient):
        resp = await client.get("/.well-known/security.txt")
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/plain")
        body = resp.text
        assert "Contact: mailto:security@criticalbit.gg" in body
        assert "Expires:" in body

    async def test_unversioned_routes_removed(self, client: AsyncClient):
        # The transitional unversioned mount was removed once the
        # vagrant-story-web frontend finished migrating to /v1.
        # Old paths should now 404; /v1 is the only public data path.
        assert (await client.get("/v1/blades")).status_code == 200
        assert (await client.get("/blades")).status_code == 404


class TestCacheHeaders:
    # Regression coverage for the /v1 migration that inadvertently made
    # authenticated endpoints publicly cacheable for an hour because the
    # middleware's path prefix check matched pre-v1 routes only.
    async def test_public_endpoints_are_cacheable(self, client: AsyncClient):
        resp = await client.get("/v1/blades")
        assert resp.status_code == 200
        assert resp.headers["cache-control"] == "public, max-age=3600"

    async def test_auth_required_endpoints_are_no_store(self, client: AsyncClient):
        # Unauthenticated — the dependency raises 401, but the auth-required
        # flag is set before the raise so the response is still marked no-store.
        resp = await client.get("/v1/user/inventories")
        assert resp.status_code == 401
        assert resp.headers["cache-control"] == "no-store"
        assert "Cookie" in resp.headers["vary"]

    async def test_loadout_endpoint_is_no_store(self, client: AsyncClient):
        resp = await client.post("/v1/loadout", json={})
        assert resp.status_code == 401
        assert resp.headers["cache-control"] == "no-store"
        assert "Cookie" in resp.headers["vary"]


class TestBlades:
    async def test_list_empty(self, client: AsyncClient):
        resp = await client.get("/v1/blades")
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

        resp = await client.get("/v1/blades")
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

        resp = await client.get(f"/v1/blades/{blade.id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Katana"

    async def test_not_found(self, client: AsyncClient):
        resp = await client.get("/v1/blades/999")
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

        resp = await client.get("/v1/blades?q=clay")
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Claymore"


class TestEnemies:
    async def test_list_empty(self, client: AsyncClient):
        resp = await client.get("/v1/enemies")
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

        resp = await client.get("/v1/enemies")
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

        resp = await client.get(f"/v1/enemies/{enemy.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Bat"
        assert len(data["body_parts"]) == 1
        assert data["body_parts"][0]["name"] == "Body"
        assert data["body_parts"][0]["physical"] == -5
        assert data["body_parts"][0]["air"] == 25

    async def test_not_found(self, client: AsyncClient):
        resp = await client.get("/v1/enemies/999")
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

        resp = await client.get("/v1/enemies?q=bat")
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Bat"


class TestMaterials:
    async def test_list_with_data(self, client: AsyncClient, session: AsyncSession):
        session.add(Material(name="Iron", tier=4, str_modifier=1, int_modifier=1, agi_modifier=-2))
        await session.commit()

        resp = await client.get("/v1/materials")
        assert resp.status_code == 200
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Iron"
        assert resp.json()[0]["str_modifier"] == 1
