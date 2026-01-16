from __future__ import annotations

from pathlib import Path

from charset_normalizer import from_bytes


def is_binary_file(file_path: Path, sample_size: int = 4096) -> bool:
    """Check if a file is binary. Simple heuristic based on null bytes.

    Args:
        file_path: The path to the file.
        sample_size: The number of bytes to read for sampling.
    Returns:
        True if the file is binary, False otherwise.
    """
    try:
        with file_path.open("rb") as f:
            sample = f.read(sample_size)
        if b"\x00" in sample:
            return True
        if not sample:
            return False
        non_text = sum(b > 0x7F for b in sample)
        return (non_text / len(sample)) > 0.30
    except Exception:
        return False


def detect_file_encoding(
    data: bytes,
    fallback: str = "utf-8",
    confidence_threshold: float = 0.8,
    min_bytes: int = 24,
) -> str:
    """Detect the encoding of a byte sequence.

    Args:
        data: Raw bytes from a file.
        fallback: Encoding to use when detection fails.
        confidence_threshold: Minimum coherence required to accept the detected encoding.
        min_bytes: Minimum byte length before attempting detection.
    Returns:
        The detected encoding or the fallback encoding.
    """
    if not data or len(data) < min_bytes:
        return fallback
    result = from_bytes(data).best()
    if result and result.encoding:
        encoding = result.encoding
        coherence = result.coherence or 0.0
        if b"\x00" not in data and encoding.lower().startswith(("utf_16", "utf_32")):
            return fallback
        if coherence < confidence_threshold:
            if len(data) >= min_bytes * 2 and encoding.lower() in {
                "latin_1",
                "iso8859_1",
                "iso8859-1",
                "cp1252",
            }:
                return encoding
            return fallback
        return encoding
    return fallback


def read_file_content(
    file_path: Path,
    encoding: str = "utf-8",
    errors: str = "replace",
    detect_encoding: bool = False,
) -> str | None:
    """Read the content of a text file.

    Args:
        file_path: The path to the file.
        encoding: The encoding to use for reading the file.
        errors: The error handling scheme.
    Returns:
        The content of the file as a string.
    """
    try:
        try:
            data = file_path.read_bytes()
            try:
                return data.decode("utf-8", errors="strict")
            except UnicodeDecodeError:
                if detect_encoding:
                    detected = detect_file_encoding(data, fallback=encoding)
                    try:
                        return data.decode(detected, errors=errors)
                    except UnicodeDecodeError:
                        if detected != encoding:
                            return data.decode(encoding, errors=errors)
                        raise
                return data.decode(encoding, errors=errors)
        except UnicodeDecodeError:
            return None
    except Exception:
        return None
