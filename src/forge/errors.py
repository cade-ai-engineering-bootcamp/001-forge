"""Framework-independent application errors with safe public contracts."""

from typing import ClassVar


class ApplicationError(Exception):
    """Base exception for expected Forge application failures."""

    code: ClassVar[str] = "application_error"
    public_message: ClassVar[str] = "The application could not complete the operation."

    def __init__(self, *, internal_detail: str | None = None) -> None:
        super().__init__(self.public_message)
        self.internal_detail = internal_detail

    def to_public_dict(self) -> dict[str, str]:
        """Return the stable, safe representation exposed at system boundaries."""
        return {"code": self.code, "message": self.public_message}


class InvalidInputError(ApplicationError):
    """The caller supplied input that cannot be accepted."""

    code = "invalid_input"
    public_message = "The supplied input is invalid."


class ResourceNotFoundError(ApplicationError):
    """A requested application resource does not exist."""

    code = "resource_not_found"
    public_message = "The requested resource was not found."


class ConflictError(ApplicationError):
    """The requested operation conflicts with current application state."""

    code = "conflict"
    public_message = "The operation conflicts with the current state."


class DependencyUnavailableError(ApplicationError):
    """A required external or infrastructure dependency is unavailable."""

    code = "dependency_unavailable"
    public_message = "A required service is temporarily unavailable."
