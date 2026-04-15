import time
import uuid

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from scalar_fastapi import get_scalar_api_reference
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.logging import setup_logging
from app.observability.sentry import init_sentry
from app.rate_limit import limiter
from app.routers import (
    areas_router,
    armor_router,
    battle_abilities_router,
    blades_router,
    break_arts_router,
    characters_router,
    chests_router,
    consumables_router,
    crafting_router,
    drops_router,
    enemies_router,
    gems_router,
    grimoires_router,
    grips_router,
    keys_router,
    loadout_router,
    materials_router,
    rankings_router,
    rooms_router,
    sigils_router,
    spells_router,
    titles_router,
    user_router,
    workshops_router,
)

init_sentry()
setup_logging()
logger = structlog.get_logger("app.request")

app = FastAPI(
    title="Vagrant Story API",
    description="Public game data API for Vagrant Story — blades, armor, gems, materials, crafting",
    version="0.1.0",
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "sentry-trace", "baggage"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# SlowAPIMiddleware is what actually enforces the Limiter's default_limits
# against every route. Without it, only routes with an explicit
# @limiter.limit(...) decorator would be rate-limited.
app.add_middleware(SlowAPIMiddleware)


MAX_REQUEST_BODY_SIZE = 1_048_576  # 1 MB


@app.middleware("http")
async def limit_request_size(request: Request, call_next) -> Response:
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_REQUEST_BODY_SIZE:
        return Response(content="Request body too large", status_code=413)
    return await call_next(request)


@app.middleware("http")
async def add_cache_headers(request: Request, call_next) -> Response:
    response = await call_next(request)
    if request.url.path.startswith("/user/"):
        response.headers["Cache-Control"] = "no-store"
    elif request.method == "GET" and response.status_code == 200:
        response.headers["Cache-Control"] = "public, max-age=3600"
    return response


@app.middleware("http")
async def request_id_middleware(request: Request, call_next) -> Response:
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "request",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration_ms,
    )
    return response


# Public API lives under /v1. Non-versioned app-level routes (/, /health,
# /docs, /.well-known/security.txt) stay at the root since they're
# infrastructure, not part of the versioned data contract.
ROUTERS = (
    blades_router,
    grips_router,
    armor_router,
    gems_router,
    materials_router,
    consumables_router,
    break_arts_router,
    battle_abilities_router,
    sigils_router,
    spells_router,
    keys_router,
    grimoires_router,
    workshops_router,
    chests_router,
    crafting_router,
    characters_router,
    enemies_router,
    titles_router,
    rankings_router,
    areas_router,
    rooms_router,
    drops_router,
    loadout_router,
    user_router,
)

for router in ROUTERS:
    app.include_router(router, prefix="/v1")


@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/")
@limiter.exempt
async def root():
    return {"status": "ok", "service": "vagrant-story-api"}


@app.get("/health")
@limiter.exempt
async def health_check():
    return {"status": "healthy"}


# Per https://securitytxt.org/ — security researchers and automated scanners
# look for this file to find an abuse contact. Bump Expires before 2027-04-15.
SECURITY_TXT = """\
Contact: mailto:security@criticalbit.gg
Expires: 2027-04-15T00:00:00.000Z
Preferred-Languages: en
"""


@app.get("/.well-known/security.txt", include_in_schema=False)
@limiter.exempt
async def security_txt() -> PlainTextResponse:
    return PlainTextResponse(SECURITY_TXT)
