class SubscriptionError(Exception):
    """Base exception for subscription errors."""

class TrialAlreadyUsed(SubscriptionError):
    """Raised when a client tries to re-use the free trial."""

class PlanNotFound(SubscriptionError):
    """Raised when an unknown plan key is requested."""

class NotFoundError(SubscriptionError):
    """Raised when a requested record cannot be found."""
