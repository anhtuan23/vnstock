# %%
"""
Stub module to replace vnai functionality without the ads/telemetry.

This module provides no-op implementations of the vnai functions and decorators
that vnstock imports, effectively disabling:
- Welcome messages and promotional content
- Telemetry and usage tracking
- Rate limiting enforcement (for paid features)
"""
import functools


def setup():
    """No-op replacement for vnai.setup()"""
    pass


def optimize_execution(resource_type="default"):
    """
    No-op replacement for vnai.optimize_execution decorator.
    
    Returns a decorator that simply calls the original function
    without any rate limiting, loop detection, or ad display.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    # Handle case where decorator is used without parentheses
    if callable(resource_type):
        func = resource_type
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    return decorator


def agg_execution(resource_type="default"):
    """No-op replacement for vnai.agg_execution decorator."""
    return optimize_execution(resource_type)


def measure_performance(module_type="function"):
    """No-op replacement for vnai.measure_performance decorator."""
    return optimize_execution(module_type)


def accept_license_terms(terms_text=None):
    """No-op replacement for vnai.accept_license_terms()"""
    return True


def accept_vnstock_terms():
    """No-op replacement for vnai.accept_vnstock_terms()"""
    return True


def configure_privacy(level="standard"):
    """No-op replacement for vnai.configure_privacy()"""
    return {"status": "ok", "level": level}


def check_commercial_usage():
    """No-op replacement for vnai.check_commercial_usage()"""
    return False


def authenticate_for_persistence():
    """No-op replacement for vnai.authenticate_for_persistence()"""
    return None


def tc_init():
    """No-op replacement for vnai.tc_init()"""
    return True
