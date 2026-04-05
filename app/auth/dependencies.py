"""FastAPI dependencies for JWT authentication."""

import jwt
import structlog
from fastapi import HTTPException, Request

from app.auth.jwks import get_public_key
from app.config import settings

logger = structlog.get_logger("app.auth")

TOKEN_AUDIENCE = ["fastapi-users:auth"]


def _decode_kwargs() -> dict:
    """Build common kwargs for jwt.decode(), including issuer if configured."""
    kwargs: dict = {"algorithms": ["RS256"], "audience": TOKEN_AUDIENCE}
    if settings.auth_token_issuer:
        kwargs["issuer"] = settings.auth_token_issuer
    return kwargs


async def get_current_user(request: Request) -> str:
    """Extract and verify the JWT from the app_access cookie, returning the user_id."""
    token = request.cookies.get("app_access")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    public_key = await get_public_key()
    decode_kwargs = _decode_kwargs()

    try:
        payload = jwt.decode(token, key=public_key, **decode_kwargs)
    except jwt.exceptions.InvalidSignatureError:
        # Key may have rotated — refresh and retry once
        logger.warning("jwt_signature_invalid", detail="Retrying with refreshed JWKS key")
        public_key = await get_public_key(force_refresh=True)
        try:
            payload = jwt.decode(token, key=public_key, **decode_kwargs)
        except jwt.PyJWTError as e:
            logger.warning("jwt_verify_failed_after_refresh", error=str(e))
            raise HTTPException(status_code=401, detail="Invalid token") from e
    except jwt.PyJWTError as e:
        logger.warning("jwt_verify_failed", error=str(e))
        raise HTTPException(status_code=401, detail="Invalid token") from e

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: missing subject")

    return user_id
