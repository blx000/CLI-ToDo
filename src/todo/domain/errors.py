class DomainError(Exception):
    """Base class for domain-level errors."""


class InvalidTaskTitle(DomainError):
    """Raised when task title is invalid (empty or blank)."""
