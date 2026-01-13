"""Custom exception types."""


class ConcatenatorError(Exception):
    """Base exception for the application."""


class InvalidRootError(ConcatenatorError):
    """Raised when the specified root directory is invalid."""


class FileNotFoundError(ConcatenatorError):
    """Raised when a required file is not found."""


class UnsupportedFormatError(ConcatenatorError):
    """Raised when an unsupported file format is encountered."""


class OutputWriteError(ConcatenatorError):
    """Raised when there is an error writing to the output file."""
