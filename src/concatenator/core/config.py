"""Application configuration."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from concatenator.services.filters import normalize_extensions, normalize_ignore_directories


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from defaults or environment."""

    root_directory: Path = field(default_factory=Path.cwd)
    output_file: Path = field(default_factory=lambda: Path.cwd() / "output.md")
    application_name: str = "concatenator"
    base_directory: Path = field(default_factory=Path.cwd)

    ignore_directories: Iterable[str] = field(default_factory=set)
    ignore_extensions: Iterable[str] = field(default_factory=set)
    include_extensions: Iterable[str] = field(default_factory=set)

    encoding: str = "utf-8"
    errors: str = "replace"  # "strict", "ignore", "replace"
    detect_encoding: bool = False
    skip_binary: bool = False
    dry_run: bool = False
    list_files: bool = False

    max_file_size: int | None = None  # in bytes

    header_text: str = "### {path}\n\n````{extension_name}"
    footer_text: str = "````\n\n// End of {path}\n"
    use_relative_paths: bool = True
    makefile_markdownlint: bool = False

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
            ignore_directories=normalize_ignore_directories(self.ignore_directories),
            ignore_extensions=normalize_extensions(self.ignore_extensions),
            include_extensions=normalize_extensions(self.include_extensions),
            encoding=self.encoding,
            errors=self.errors,
            detect_encoding=self.detect_encoding,
            skip_binary=self.skip_binary,
            dry_run=self.dry_run,
            list_files=self.list_files,
            max_file_size=self.max_file_size,
            header_text=self.header_text,
            footer_text=self.footer_text,
            use_relative_paths=self.use_relative_paths,
            makefile_markdownlint=self.makefile_markdownlint,
        )
