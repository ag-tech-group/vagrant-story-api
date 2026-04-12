"""Sentry SDK initialization for the FastAPI service.

Init must run BEFORE FastAPI() is constructed so FastApiIntegration and
StarletteIntegration can auto-instrument middleware. See app/main.py.
"""

import sentry_sdk

from app.config import settings


def init_sentry() -> None:
    if not settings.sentry_dsn:
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        # Kept false until a public privacy policy ships. Matches the
        # frontend's cookie-free posture so distributed traces aren't
        # leaking PII on one side while hiding it on the other.
        send_default_pii=False,
        traces_sample_rate=settings.sentry_traces_sample_rate,
        # Continuous profiling tied to active spans. Effective profile
        # rate = traces_sample_rate * 1.0, so dev 1.0 / prod 0.1.
        profile_session_sample_rate=1.0,
        profile_lifecycle="trace",
        enable_logs=True,
    )
