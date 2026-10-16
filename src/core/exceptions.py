"""HYDRA-GRID - Custom exceptions."""


class HydraError(Exception):
    """Base exception."""
    pass


class PolicyViolation(HydraError):
    """Security policy violated."""
    pass


class IntegrityError(HydraError):
    """Integrity check failed."""
    pass


class RateLimitExceeded(HydraError):
    """Source exceeded rate limit."""
    pass
