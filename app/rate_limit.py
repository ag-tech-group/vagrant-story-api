from slowapi import Limiter
from slowapi.util import get_remote_address

# Global default applies to every route that doesn't set its own @limiter.limit.
# Keyed on the real client IP — this requires uvicorn to be run with
# --proxy-headers so X-Forwarded-For is trusted behind Cloud Run's frontend.
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
