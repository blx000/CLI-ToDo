class ApplicationError(Exception):
    """Base class for application-level errors."""


class TaskNotFound(ApplicationError):
    """Raised when requested task does not exist."""
