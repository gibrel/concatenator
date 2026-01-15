from __future__ import annotations

import logging
import os
from pathlib import Path

from concatenator.core.config import Settings
from concatenator.core.exceptions import (
    InvalidRootError,
    OutputWriteError,
)

from .filters import should_ignore_dir, should_include_file
from .readers import is_binary_file, read_file_content

logger = logging.getLogger(__name__)


def build_display_path(path: Path, root: Path, use_relative_paths: bool) -> str:
    if not use_relative_paths:
        return str(path)
    relative = path.relative_to(root)
    display_path = Path(root.name) / relative
    return f"/{display_path.as_posix()}"


def condense_directory(settings: Settings) -> int:
    """Condense files in the root directory based on settings.

    Args:
        settings: Application settings.
    Returns:
        The number of files successfully condensed.
    """
    configuration = settings.ensure_paths()

    if not configuration.root_directory.is_dir():
        raise InvalidRootError(f"Invalid root directory: {configuration.root_directory}")

    configuration.output_file.parent.mkdir(parents=True, exist_ok=True)

    files_condensed = 0

    try:
        with configuration.output_file.open(
            "w", encoding=configuration.encoding, errors=configuration.errors
        ) as output_file:
            output_file.write(f"# {Path(configuration.root_directory).name}\n\n")

            for dirpath, dirnames, filenames in os.walk(configuration.root_directory):
                current_dir = Path(dirpath)
                display_dir = build_display_path(
                    current_dir, configuration.root_directory, configuration.use_relative_paths
                )

                output_file.write(f"## {display_dir}\n\n")

                # Should skip ignored directories
                to_remove = should_ignore_dir(
                    current_dir,
                    dirnames,
                    configuration.ignore_directories,
                    configuration.root_directory,
                )
                for dirname in to_remove:
                    dirnames.remove(dirname)

                for filename in filenames:
                    file_path = current_dir / filename

                    # should not include file based on extensions
                    if not should_include_file(
                        file_path, configuration.include_extensions, configuration.ignore_extensions
                    ):
                        continue

                    # should skip file based on size
                    if configuration.max_file_size is not None:
                        try:
                            if file_path.stat().st_size > configuration.max_file_size:
                                logger.info(f"Skipping large file: {file_path}")
                                continue
                        except OSError:
                            logger.warning(f"Could not access file size: {file_path}")
                            continue

                    # should skip file if it is binary
                    if configuration.skip_binary and is_binary_file(file_path):
                        logger.info(f"Skipping binary file: {file_path}")
                        continue

                    content = read_file_content(
                        file_path,
                        encoding=configuration.encoding,
                        errors=configuration.errors,
                    )

                    # should skip file if content could not be read
                    if content is None:
                        logger.warning(f"Could not read file: {file_path}")
                        continue

                    relative_path = (
                        build_display_path(
                            file_path,
                            configuration.root_directory,
                            configuration.use_relative_paths,
                        )
                        if configuration.use_relative_paths
                        else file_path
                    )

                    extension_name = file_path.suffix.lstrip(".") or file_path.name

                    header = configuration.header_text.format(
                        path=relative_path, extension_name=extension_name
                    )
                    footer = configuration.footer_text.format(path=relative_path)

                    if file_path.name == "Makefile":
                        header = header.replace("\n\n", "\n\n<!-- markdownlint-disable MD010 -->\n")
                        footer = footer.replace("\n\n", "\n<!-- markdownlint-enable MD010 -->\n\n")

                    output_file.write(header + "\n")
                    output_file.write(content)
                    if not content.endswith("\n"):
                        output_file.write("\n")
                    output_file.write(footer + "\n")

                    files_condensed += 1

        condensed_text = configuration.output_file.read_text(
            encoding=configuration.encoding, errors=configuration.errors
        ).rstrip("\n")
        if condensed_text:
            condensed_text += "\n"
        configuration.output_file.write_text(
            condensed_text, encoding=configuration.encoding, errors=configuration.errors
        )

        logger.info(f"Included files: {files_condensed}")
        logger.info(f"Output written to: {configuration.output_file}")
        return files_condensed

    except OSError as e:
        raise OutputWriteError(f"Error writing to output file: {configuration.output_file}") from e
