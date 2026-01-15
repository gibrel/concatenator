import logging

from concatenator.core import paths
from concatenator.core.logger import configure_logger


def test_configure_logger_sets_handler_and_level():
    logger = configure_logger("concatenator-test", level=logging.DEBUG)
    assert logger.level == logging.DEBUG
    assert logger.handlers

    same_logger = configure_logger("concatenator-test", level=logging.INFO)
    assert same_logger is logger
    logger.handlers.clear()


def test_paths_point_to_repo():
    assert paths.PROJECT_ROOT.name == "concatenator" or paths.PROJECT_ROOT.name == "Concatenator"
    assert paths.SRC_DIR.name == "src"
