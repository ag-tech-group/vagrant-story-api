"""JWKS client that fetches and caches public keys from the auth API."""

import structlog
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from jwt.algorithms import RSAAlgorithm

from app.config import settings

logger = structlog.get_logger("app.auth.jwks")

_cached_public_key: RSAPublicKey | None = None


async def _fetch_jwks() -> dict:
    """Fetch the JWKS from the auth API."""
    import httpx

    url = settings.auth_jwks_url
    async with httpx.AsyncClient(timeout=10.0) as client:
        logger.info("jwks_fetch", url=url)
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def _load_public_key() -> RSAPublicKey:
    """Fetch JWKS and parse the first RSA public key."""
    jwks = await _fetch_jwks()
    keys = jwks.get("keys", [])
    if not keys:
        raise ValueError("No keys found in JWKS response")
    # Use the first RSA key
    key_data = keys[0]
    public_key = RSAAlgorithm.from_jwk(key_data)
    if not isinstance(public_key, RSAPublicKey):
        raise ValueError("JWKS key is not an RSA public key")
    logger.info("jwks_loaded", kid=key_data.get("kid"))
    return public_key


async def get_public_key(force_refresh: bool = False) -> RSAPublicKey:
    """Get the cached RSA public key, fetching from JWKS if needed."""
    global _cached_public_key
    if _cached_public_key is None or force_refresh:
        _cached_public_key = await _load_public_key()
    return _cached_public_key
