"""Global rate limiting behaviour.

The Limiter's ``default_limits`` (60/min, enforced by SlowAPIMiddleware)
must apply to every route that isn't decorated or exempt, and the
infrastructure routes must stay exempt. This is the canary for the class
of regression where a framework upgrade silently disables middleware
enforcement (see slowapi issue #281 for fastapi>=0.137).
"""

from httpx import AsyncClient


class TestGlobalRateLimit:
    async def test_default_limit_enforced_on_undecorated_route(self, client: AsyncClient):
        # /v1/armor has no explicit @limiter.limit, so it gets the 60/min
        # default. (Matches `default_limits` in app/rate_limit.py — bump
        # both together if that changes.)
        for _ in range(60):
            assert (await client.get("/v1/armor")).status_code == 200
        assert (await client.get("/v1/armor")).status_code == 429

    async def test_infrastructure_routes_are_exempt(self, client: AsyncClient):
        # / and /health are @limiter.exempt — many rapid hits (well past
        # the 60/min default) never 429.
        for _ in range(70):
            assert (await client.get("/health")).status_code == 200
        assert (await client.get("/")).status_code == 200
