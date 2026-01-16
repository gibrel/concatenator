from __future__ import annotations

from importlib import metadata

from concatenator import metadata as metadata_module


class DummyDistribution:
    def __init__(self) -> None:
        self.version = "1.2.3"
        self.metadata = {"Name": "concatenator", "Description": "desc"}


def test_get_package_metadata_from_distribution(monkeypatch):
    metadata_module._CACHE = None

    def fake_distribution(_: str) -> DummyDistribution:
        return DummyDistribution()

    monkeypatch.setattr(metadata, "distribution", fake_distribution)
    name, version, description = metadata_module.get_package_metadata()

    assert name == "concatenator"
    assert version == "1.2.3"
    assert description == "desc"


def test_get_package_metadata_falls_back_to_pyproject(monkeypatch, tmp_path):
    metadata_module._CACHE = None

    def raise_not_found(_: str) -> DummyDistribution:
        raise metadata.PackageNotFoundError

    monkeypatch.setattr(metadata, "distribution", raise_not_found)
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
name = "concatenator"
version = "9.9.9"
description = "desc"
""".strip()
    )

    data = metadata_module._read_pyproject_toml(str(tmp_path))
    assert data is not None

    monkeypatch.chdir(tmp_path)
    name, version, description = metadata_module.get_package_metadata()

    assert name == "concatenator"
    assert version == "9.9.9"
    assert description == "desc"


def test_read_pyproject_returns_none_when_missing(tmp_path):
    assert metadata_module._read_pyproject_toml(str(tmp_path)) is None
