"""Sentry SDK initialization for the FastAPI service.

Init must run BEFORE FastAPI() is constructed so FastApiIntegration and
StarletteIntegration can auto-instrument middleware. See app/main.py.
"""

import time
from collections import deque
from threading import Lock

import sentry_sdk
from asyncpg.exceptions import TooManyConnectionsError

from app.config import settings

# Rate-limit pool-exhaustion reports to Sentry. The first N events per
# window surface normally (storm visibility preserved); beyond that,
# events drop from Sentry but remain in structlog app logs. Per-process
# state, so aggregate Sentry volume scales with Cloud Run instance count.
_POOL_ERR_WINDOW_S = 60.0
_POOL_ERR_MAX_PER_WINDOW = 5
_pool_err_times: deque[float] = deque(maxlen=_POOL_ERR_MAX_PER_WINDOW)
_pool_err_lock = Lock()


def _contains_pool_exhaustion(exc: BaseException | None) -> bool:
    if exc is None:
        return False
    if isinstance(exc, TooManyConnectionsError):
        return True
    if isinstance(exc, BaseExceptionGroup):
        return any(_contains_pool_exhaustion(sub) for sub in exc.exceptions)
    cause = exc.__cause__ if exc.__cause__ is not None else exc.__context__
    if cause is not None and cause is not exc:
        return _contains_pool_exhaustion(cause)
    return False


def _rate_limit_pool_exhaustion(event, hint):
    exc_info = hint.get("exc_info")
    if not exc_info or not _contains_pool_exhaustion(exc_info[1]):
        return event
    now = time.monotonic()
    with _pool_err_lock:
        while _pool_err_times and _pool_err_times[0] < now - _POOL_ERR_WINDOW_S:
            _pool_err_times.popleft()
        if len(_pool_err_times) >= _POOL_ERR_MAX_PER_WINDOW:
            return None
        _pool_err_times.append(now)
    return event


def init_sentry() -> None:
    if not settings.sentry_dsn:
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        release=settings.sentry_release or None,
        # Privacy policy at criticalbit.gg/privacy discloses the data
        # collected here (IP, headers, request body). Enabled for
        # debuggability now that users have been given notice.
        send_default_pii=True,
        traces_sample_rate=settings.sentry_traces_sample_rate,
        # Continuous profiling tied to active spans. Effective profile
        # rate = traces_sample_rate * 1.0, so dev 1.0 / prod 0.1.
        profile_session_sample_rate=1.0,
        profile_lifecycle="trace",
        enable_logs=True,
        before_send=_rate_limit_pool_exhaustion,
    )
