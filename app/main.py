import time
import uuid

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import settings
from app.logging import setup_logging
from app.routers import (
    armor_router,
    consumables_router,
    crafting_router,
    gems_router,
    grimoires_router,
    grips_router,
    keys_router,
    materials_router,
    sigils_router,
    spells_router,
    user_router,
    weapons_router,
    workshops_router,
)

setup_logging()
logger = structlog.get_logger("app.request")

app = FastAPI(
    title="Vagrant Story API",
    description="Public game data API for Vagrant Story — weapons, armor, gems, materials, crafting",
    version="0.1.0",
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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


app.include_router(weapons_router)
app.include_router(grips_router)
app.include_router(armor_router)
app.include_router(gems_router)
app.include_router(materials_router)
app.include_router(consumables_router)
app.include_router(sigils_router)
app.include_router(spells_router)
app.include_router(keys_router)
app.include_router(grimoires_router)
app.include_router(workshops_router)
app.include_router(crafting_router)
app.include_router(user_router)


@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/")
async def root():
    return {"status": "ok", "service": "vagrant-story-api"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
