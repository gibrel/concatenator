"""Command-line interface entrypoint."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from concatenator.metadata import get_package_metadata

from .core.config import Settings
from .core.logger import configure_logger
from .services.condenser import condense_directory

app_name, app_version, app_description = get_package_metadata()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=f"{app_name} CLI v{app_version}", description=app_description
    )
    parser.add_argument("--version", action="version", version=f"{app_name} {app_version}")
    parser.add_argument("root_directory", type=Path, help="Root directory to condense files from.")
    parser.add_argument(
        "-o", "--output-file", type=Path, default=Path.cwd() / "output.md", help="Output file path."
    )
    parser.add_argument(
        "--ignore-directories",
        "--ignore-dirs",
        nargs="*",
        default=[],
        help="List of directory paths to ignore.",
    )
    parser.add_argument(
        "--ignore-extensions",
        "--ignore-exts",
        nargs="*",
        default=[],
        help="List of file extensions to ignore.",
    )
    parser.add_argument(
        "--include-extensions",
        "--include-exts",
        nargs="*",
        default=[],
        help="List of file extensions to include.",
    )
    parser.add_argument("--encoding", type=str, default="utf-8", help="File encoding to use.")
    parser.add_argument(
        "--errors",
        default="replace",
        choices=["strict", "ignore", "replace"],
        help="Error handling scheme for encoding/decoding.",
    )
    parser.add_argument(
        "--skip-binary", action="store_true", help="Skip binary files during condensation."
    )
    parser.add_argument(
        "--max-file-size", type=int, default=None, help="Maximum file size (in bytes) to include."
    )
    # parser.add_argument(
    #     "--relative-paths", action="store_true", help="Use relative paths in output."
    # )
    parser.add_argument(
        "--header-text",
        default="### {path}\n\n````{extension_name}",
        help="Header text format for each file.",
    )
    parser.add_argument(
        "--footer-text",
        default="````\n\n// End of {path}\n",
        help="Footer text format for each file.",
    )
    parser.add_argument(
        "--markdownlint-disable-md010",
        "--mdlint-md010",
        action="store_true",
        help="Add markdownlint disable/enable markers around Makefile content.",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress non-essential log output."
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity level."
    )
    return parser


def setup_logger(verbosity: int, settings: Settings, quiet: bool = False) -> None:
    level = logging.ERROR if quiet else max(10, 30 - (verbosity * 10))
    logger = configure_logger(settings.app_name, level=level)
    logger.debug(f"Logger configured at level: {level}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    settings = Settings(
        root_directory=args.root_directory,
        output_file=args.output_file,
        application_name=app_name,
        ignore_directories=args.ignore_directories,
        ignore_extensions=args.ignore_extensions,
        include_extensions=args.include_extensions,
        encoding=args.encoding,
        errors=args.errors,
        skip_binary=args.skip_binary,
        max_file_size=args.max_file_size,
        # relative_paths=args.relative_paths,
        header_text=args.header_text,
        footer_text=args.footer_text,
        makefile_markdownlint=args.markdownlint_disable_md010,
    )
    setup_logger(verbosity=args.verbose, settings=settings, quiet=args.quiet)

    count = condense_directory(settings)
    print(f"Condensed {count} files into {settings.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
