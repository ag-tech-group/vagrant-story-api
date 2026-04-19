"""Tests for the Sentry pool-exhaustion rate limiter in app.observability.sentry."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from asyncpg.exceptions import TooManyConnectionsError

from app.observability import sentry as sentry_mod


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    sentry_mod._pool_err_times.clear()
    yield
    sentry_mod._pool_err_times.clear()


def _event_hint_for(exc: BaseException) -> tuple[dict, dict]:
    """Build the (event, hint) pair Sentry passes to before_send."""
    return {}, {"exc_info": (type(exc), exc, None)}


def test_unrelated_exception_passes_through():
    event, hint = _event_hint_for(ValueError("nope"))
    assert sentry_mod._rate_limit_pool_exhaustion(event, hint) is event
    assert len(sentry_mod._pool_err_times) == 0


def test_missing_exc_info_passes_through():
    event = {}
    assert sentry_mod._rate_limit_pool_exhaustion(event, {}) is event


def test_first_n_pool_events_pass_then_drop():
    for i in range(sentry_mod._POOL_ERR_MAX_PER_WINDOW):
        event, hint = _event_hint_for(TooManyConnectionsError("exhausted"))
        assert sentry_mod._rate_limit_pool_exhaustion(event, hint) is event, (
            f"event {i} should pass"
        )
    event, hint = _event_hint_for(TooManyConnectionsError("exhausted"))
    assert sentry_mod._rate_limit_pool_exhaustion(event, hint) is None


def test_dropped_events_do_not_count_against_quota():
    # Fill the window
    for _ in range(sentry_mod._POOL_ERR_MAX_PER_WINDOW):
        event, hint = _event_hint_for(TooManyConnectionsError("exhausted"))
        sentry_mod._rate_limit_pool_exhaustion(event, hint)
    # Dropped events must not extend the window — otherwise a sustained
    # storm would permanently starve out new events even after the
    # window rolls over.
    for _ in range(10):
        event, hint = _event_hint_for(TooManyConnectionsError("exhausted"))
        sentry_mod._rate_limit_pool_exhaustion(event, hint)
    assert len(sentry_mod._pool_err_times) == sentry_mod._POOL_ERR_MAX_PER_WINDOW


def test_cause_chain_is_walked():
    outer = RuntimeError("wrapped")
    outer.__cause__ = TooManyConnectionsError("inner")
    event, hint = _event_hint_for(outer)
    assert sentry_mod._rate_limit_pool_exhaustion(event, hint) is event
    assert len(sentry_mod._pool_err_times) == 1


def test_exception_group_is_walked():
    group = BaseExceptionGroup("group", [TooManyConnectionsError("inner")])
    event, hint = _event_hint_for(group)
    assert sentry_mod._rate_limit_pool_exhaustion(event, hint) is event
    assert len(sentry_mod._pool_err_times) == 1


def test_window_eviction_allows_new_events_after_expiry():
    with patch.object(sentry_mod.time, "monotonic", return_value=0.0):
        for _ in range(sentry_mod._POOL_ERR_MAX_PER_WINDOW):
            event, hint = _event_hint_for(TooManyConnectionsError("boom"))
            sentry_mod._rate_limit_pool_exhaustion(event, hint)
        event, hint = _event_hint_for(TooManyConnectionsError("boom"))
        assert sentry_mod._rate_limit_pool_exhaustion(event, hint) is None

    with patch.object(
        sentry_mod.time,
        "monotonic",
        return_value=sentry_mod._POOL_ERR_WINDOW_S + 1.0,
    ):
        event, hint = _event_hint_for(TooManyConnectionsError("boom"))
        assert sentry_mod._rate_limit_pool_exhaustion(event, hint) is event
