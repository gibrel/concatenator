from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path

from concatenator.core.config import Settings
from concatenator.core.exceptions import (
    ConcatenatorInvalidRootError,
    ConcatenatorOutputWriteError,
)

from .filters import (
    normalize_extensions,
    normalize_ignore_directories,
    should_ignore_dir,
    should_include_file,
)
from .readers import is_binary_file, read_file_content

logger = logging.getLogger(__name__)


@dataclass
class CondenseSummary:
    included: int = 0
    ignored_by_rule: int = 0
    skipped_binary: int = 0
    skipped_size: int = 0
    unreadable: int = 0

    @property
    def ignored_total(self) -> int:
        return self.ignored_by_rule + self.skipped_binary + self.skipped_size


def build_display_path(path: Path, root: Path, use_relative_paths: bool) -> str:
    if not use_relative_paths:
        return str(path)
    try:
        relative = path.relative_to(root)
    except ValueError:
        try:
            relative = Path(os.path.relpath(path, root))
        except ValueError:
            return str(path)
    display_path = Path(root.name) / relative
    return f"/{display_path.as_posix()}"


def collect_files_to_condense(configuration: Settings) -> tuple[list[Path], CondenseSummary]:
    files_to_condense: list[Path] = []
    summary = CondenseSummary()

    for dirpath, dirnames, filenames in os.walk(configuration.root_directory):
        current_dir = Path(dirpath)

        to_remove = should_ignore_dir(
            current_dir,
            dirnames,
            normalize_ignore_directories(configuration.ignore_directories),
            configuration.root_directory,
        )
        for dirname in to_remove:
            dirnames.remove(dirname)

        for filename in filenames:
            file_path = current_dir / filename

            if not should_include_file(
                file_path,
                normalize_extensions(configuration.include_extensions),
                normalize_extensions(configuration.ignore_extensions),
            ):
                summary.ignored_by_rule += 1
                continue

            if configuration.max_file_size is not None:
                try:
                    if file_path.stat().st_size > configuration.max_file_size:
                        summary.skipped_size += 1
                        continue
                except OSError:
                    summary.unreadable += 1
                    continue

            if configuration.skip_binary and is_binary_file(file_path):
                summary.skipped_binary += 1
                continue

            content = read_file_content(
                file_path,
                encoding=configuration.encoding,
                errors=configuration.errors,
                detect_encoding=configuration.detect_encoding,
            )

            if content is None:
                summary.unreadable += 1
                continue

            files_to_condense.append(file_path)
            summary.included += 1

    return files_to_condense, summary


def condense_directory(settings: Settings) -> int:
    """Condense files in the root directory based on settings.

    Args:
        settings: Application settings.
    Returns:
        The number of files successfully condensed.
    """
    configuration = settings.ensure_paths()

    if not configuration.root_directory.is_dir():
        raise ConcatenatorInvalidRootError(
            f"Invalid root directory: {configuration.root_directory}"
        )

    files_condensed = 0
    start_time = time.perf_counter()

    try:
        files_to_condense, summary = collect_files_to_condense(configuration)
        last_file = files_to_condense[-1] if files_to_condense else None

        if configuration.list_files:
            for file_path in files_to_condense:
                display_path = build_display_path(
                    file_path, configuration.root_directory, configuration.use_relative_paths
                )
                logger.info("Include: %s", display_path)

        if not (configuration.dry_run or configuration.list_files):
            configuration.output_file.parent.mkdir(parents=True, exist_ok=True)
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
                        normalize_ignore_directories(configuration.ignore_directories),
                        configuration.root_directory,
                    )
                    for dirname in to_remove:
                        dirnames.remove(dirname)

                    for filename in filenames:
                        file_path = current_dir / filename

                        # should not include file based on extensions
                        if not should_include_file(
                            file_path,
                            normalize_extensions(configuration.include_extensions),
                            normalize_extensions(configuration.ignore_extensions),
                        ):
                            continue

                        # should skip file based on size
                        if configuration.max_file_size is not None:
                            try:
                                if file_path.stat().st_size > configuration.max_file_size:
                                    logger.info("Skipping large file: %s", file_path)
                                    continue
                            except OSError:
                                logger.warning("Could not access file size: %s", file_path)
                                continue

                        # should skip file if it is binary
                        if configuration.skip_binary and is_binary_file(file_path):
                            logger.info("Skipping binary file: %s", file_path)
                            continue

                        content = read_file_content(
                            file_path,
                            encoding=configuration.encoding,
                            errors=configuration.errors,
                            detect_encoding=configuration.detect_encoding,
                        )

                        # should skip file if content could not be read
                        if content is None:
                            logger.warning("Could not read file: %s", file_path)
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

                        if configuration.makefile_markdownlint and file_path.name == "Makefile":
                            header = header.replace(
                                "\n\n", "\n\n<!-- markdownlint-disable MD010 -->\n"
                            )
                            footer = footer.replace(
                                "\n\n", "\n<!-- markdownlint-enable MD010 -->\n\n"
                            )

                        output_file.write(header + "\n")
                        output_file.write(content)
                        if not content.endswith("\n"):
                            output_file.write("\n")
                        if file_path == last_file:
                            footer_text = footer.rstrip("\n")
                            output_file.write(f"{footer_text}\n\n")
                        else:
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
        else:
            files_condensed = summary.included

        elapsed = time.perf_counter() - start_time
        logger.info("Included files: %s", summary.included)
        logger.info("Ignored by rule: %s", summary.ignored_by_rule)
        logger.info("Skipped (binary): %s", summary.skipped_binary)
        logger.info("Skipped (size): %s", summary.skipped_size)
        logger.info("Ignored total: %s", summary.ignored_total)
        logger.info("Total time: %.2fs", elapsed)
        logger.debug("Unreadable files: %s", summary.unreadable)
        if not (configuration.dry_run or configuration.list_files):
            logger.info("Output written to: %s", configuration.output_file)
        return files_condensed

    except OSError as e:
        raise ConcatenatorOutputWriteError(
            f"Error writing to output file: {configuration.output_file}"
        ) from e
