from __future__ import annotations

from pathlib import Path


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


def read_file_content(
    file_path: Path, encoding: str = "utf-8", errors: str = "replace"
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
        with file_path.open("r", encoding=encoding, errors=errors) as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with file_path.open("r", encoding="latin-1", errors="ignore") as f:
                return f.read()
        except Exception:
            return None
    except Exception:
        return None
