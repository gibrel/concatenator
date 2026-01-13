from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


def normalize_extensions(extensions: Iterable[str]) -> set[str]:
    """Normalize a list of file extensions.

    Args:
        extensions: An iterable of file extensions.

    Returns:
        A set of normalized file extensions.
    """
    normalized: set[str] = set()
    for ext in extensions:
        ext = ext.strip()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = f".{ext}"
        normalized.add(ext.lower())
    return normalized


def normalize_ignore_directories(ignore_directories: Iterable[str]) -> set[str]:
    """Normalize a list of directory paths to ignore.

    Args:
        ignore_directories: An iterable of directory paths as strings.

    Returns:
        A set of normalized directory paths.
    """
    normalized: set[str] = set()
    for directory_path in ignore_directories:
        directory_path = directory_path.strip()
        if directory_path:
            normalized.add(directory_path)
            normalized.add(str(Path(directory_path)))
    return normalized


def should_ignore_dir(
    directory_path: Path, dirnames: list[str], ignore_directories: set[str], root_path: Path
) -> list[str]:
    """Check if a directory should be ignored.

    Args:
        directory_path: The directory path to check.
        dirnames: A list of directory names in the current directory.
        ignore_directories: A set of directory paths to ignore.
        root_path: The root path for relative comparisons.
    Returns:
        A filtered list of directory names excluding those to be ignored.
    """
    to_remove: list[str] = []
    for dirname in dirnames:
        full = directory_path / dirname
        relative = str(full.relative_to(root_path))
        if (
            dirname in ignore_directories
            or relative in ignore_directories
            or str(Path(relative)) in ignore_directories
        ):
            to_remove.append(dirname)
    return to_remove


def should_include_file(
    file_path: Path, include_extensions: set[str], ignore_extensions: set[str]
) -> bool:
    """Check if a file should be included based on its extension.

    Args:
        file_path: The file path to check.
        include_extensions: A set of file extensions to include.
        ignore_extensions: A set of file extensions to ignore.
    Returns:
        True if the file should be included, False otherwise.
    """
    ext = file_path.suffix.lower()
    if include_extensions and ext not in include_extensions:
        return False
    if ext in ignore_extensions:
        return False
    return True
