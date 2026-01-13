"""Application configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from defaults or environment."""

    root_directory: Path
    output_file: Path
    application_name: str = "concatenator"
    base_directory: Path = Path.cwd()

    ignore_directories: set[str] = field(default_factory=set)
    ignore_extensions: set[str] = field(default_factory=set)
    include_extensions: set[str] = field(default_factory=set)

    encoding: str = "utf-8"
    errors: str = "replace"  # "strict", "ignore", "replace"
    detect_encoding: bool = False
    skip_binary: bool = True

    max_file_size: int | None = None  # in bytes

    header_text: str = "### {path}\n\n````{extension_name}"
    footer_text: str = "````\n\n// End of {path}"
    use_relative_paths: bool = True

    @property
    def data_dir(self) -> Path:
        return self.base_directory / "data"

    @property
    def app_name(self) -> str:
        return self.application_name

    def ensure_paths(self) -> Settings:
        """Ensure that all path attributes are absolute."""
        return Settings(
            root_directory=self.root_directory.resolve(),
            output_file=self.output_file.resolve(),
            application_name=self.application_name,
            base_directory=self.base_directory.resolve(),
            ignore_directories=set(self.ignore_directories),
            ignore_extensions={e.lower() for e in self.ignore_extensions},
            include_extensions={e.lower() for e in self.include_extensions},
            encoding=self.encoding,
            errors=self.errors,
            detect_encoding=self.detect_encoding,
            skip_binary=self.skip_binary,
            max_file_size=self.max_file_size,
            header_text=self.header_text,
            footer_text=self.footer_text,
            use_relative_paths=self.use_relative_paths,
        )
