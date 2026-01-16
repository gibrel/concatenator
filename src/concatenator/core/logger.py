"""Logging configuration helpers."""

from __future__ import annotations

import logging

DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger with a standard formatter."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
        logger.addHandler(handler)
    logger.propagate = False
    return logger
