from __future__ import annotations

import os
import tomllib
from collections.abc import Mapping
from importlib import metadata

_CACHE: tuple[str, str, str, str] | None = None


def _read_pyproject_toml(root: str = ".") -> Mapping[str, object] | None:
    """Read and parse the pyproject.toml file.
    Args:
        root: The root directory where pyproject.toml is located.
    Returns:
        A mapping of the pyproject.toml content, or None if not found or error.
    """
    pyproject_path = os.path.join(root, "pyproject.toml")
    try:
        with open(pyproject_path, "rb") as f:
            return tomllib.load(f)
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        return None


def get_package_metadata(distribution_name: str = "concatenator") -> tuple[str, str, str, str]:
    """Get package metadata: name, version, summary and description.
    Args:
        distribution_name: The name of the distribution/package.
    Returns:
        A tuple of (name, version, summary, description).
    """
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    # installed package metadata
    try:
        dist = metadata.distribution(distribution_name)
        name = dist.metadata["Name"] or distribution_name
        version = dist.version or "0.0.0"
        summary = dist.metadata["Summary"] or ""
        description = dist.metadata["Description"] or ""

        _CACHE = (name, version, summary, description)
        return _CACHE

    except metadata.PackageNotFoundError:
        data = _read_pyproject_toml()
        project = data.get("project", {}) if data else {}
        name = distribution_name
        version = "0.0.0"
        summary = ""
        description = ""

        if isinstance(project, dict):
            name = str(project.get("name", name))
            version = str(project.get("version", version))
            summary = (
                str(project.get("summary", summary))
                if project.get("summary") is not None
                else summary
            )
            description = (
                str(project.get("description", description))
                if project.get("description") is not None
                else description
            )

        _CACHE = (name, version, summary, description)
        return _CACHE
