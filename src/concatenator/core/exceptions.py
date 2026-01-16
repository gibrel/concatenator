"""Custom exception types."""


class ConcatenatorError(Exception):
    """Base exception for the application."""


class ConcatenatorInvalidRootError(ConcatenatorError):
    """Raised when the specified root directory is invalid."""


class ConcatenatorFileNotFoundError(ConcatenatorError):
    """Raised when a required file is not found."""


class ConcatenatorUnsupportedFormatError(ConcatenatorError):
    """Raised when an unsupported file format is encountered."""


class ConcatenatorOutputWriteError(ConcatenatorError):
    """Raised when there is an error writing to the output file."""
