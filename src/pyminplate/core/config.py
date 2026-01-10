"""Application configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from defaults or environment."""

    app_name: str = "pyminplate"
    base_dir: Path = Path.cwd()

    @property
    def data_dir(self) -> Path:
        return self.base_dir / "data"
