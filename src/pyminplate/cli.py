"""Command-line interface entrypoint."""

from __future__ import annotations

import argparse

from pyminplate.core.config import Settings
from pyminplate.core.logger import configure_logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="pyminplate CLI")
    parser.add_argument("--name", default="pyminplate", help="Name to greet")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    settings = Settings(app_name=args.name)

    logger = configure_logger(settings.app_name)
    logger.info("Hello from %s", settings.app_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
