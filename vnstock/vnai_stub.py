"""
No-op replacement for ``vnai`` runtime hooks.

The upstream package imports ``vnai`` for decorators, setup, API-key helpers,
license acceptance, update notices, and usage checks. This stub keeps those
imports working without running ad, telemetry, or persistence behavior.
"""

from __future__ import annotations

import functools
import sys
import types
from collections.abc import Callable
from typing import Any


def install_as_vnai() -> None:
    """Register this module wherever the package expects to import ``vnai``."""
    sys.modules["vnai"] = sys.modules[__name__]

    scope_module = types.ModuleType("vnai.scope")
    profile_module = types.ModuleType("vnai.scope.profile")
    profile_module.inspector = _Inspector()
    scope_module.profile = profile_module

    sys.modules["vnai.scope"] = scope_module
    sys.modules["vnai.scope.profile"] = profile_module


def setup(*_args: Any, **_kwargs: Any) -> None:
    """Skip vnai setup side effects."""
    return None


def optimize_execution(resource_type: Any = "default") -> Callable[..., Any]:
    """Return the wrapped function unchanged."""
    if callable(resource_type):
        return _wrap_noop(resource_type)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return _wrap_noop(func)

    return decorator


def agg_execution(resource_type: Any = "default") -> Callable[..., Any]:
    """Return the wrapped function unchanged."""
    return optimize_execution(resource_type)


def measure_performance(module_type: Any = "function") -> Callable[..., Any]:
    """Return the wrapped function unchanged."""
    return optimize_execution(module_type)


def accept_license_terms(*_args: Any, **_kwargs: Any) -> bool:
    """Pretend license acceptance is already satisfied."""
    return True


def accept_vnstock_terms(*_args: Any, **_kwargs: Any) -> bool:
    """Pretend vnstock terms are already satisfied."""
    return True


def configure_privacy(level: str = "standard", **_kwargs: Any) -> dict[str, str]:
    """Return a harmless privacy status without persisting anything."""
    return {"status": "ok", "level": level}


def check_commercial_usage(*_args: Any, **_kwargs: Any) -> bool:
    """Disable commercial-usage checks."""
    return False


def authenticate_for_persistence(*_args: Any, **_kwargs: Any) -> None:
    """Skip persistence authentication."""
    return None


def tc_init(*_args: Any, **_kwargs: Any) -> bool:
    """Pretend TC initialization succeeded."""
    return True


def setup_api_key(_api_key: str, *_args: Any, **_kwargs: Any) -> bool:
    """Accept API keys without sending them to vnai."""
    return True


def check_api_key_status(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    """Return a local stub status for callers that display API-key state."""
    return {
        "has_api_key": True,
        "api_key_preview": "LOCAL***STUB",
        "tier": "Local Stub",
        "limits": {"per_minute": None},
    }


def _wrap_noop(func: Callable[..., Any]) -> Callable[..., Any]:
    """Preserve function metadata while skipping decorator side effects."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


class _Inspector:
    """Small stand-in for ``vnai.scope.profile.inspector``."""

    def fingerprint(self) -> str:
        """Return a stable local fingerprint without inspecting the machine."""
        return "local-stub"


__all__ = [
    "accept_license_terms",
    "accept_vnstock_terms",
    "agg_execution",
    "authenticate_for_persistence",
    "check_api_key_status",
    "check_commercial_usage",
    "configure_privacy",
    "install_as_vnai",
    "measure_performance",
    "optimize_execution",
    "setup",
    "setup_api_key",
    "tc_init",
]
