import logging
import sys

from settings import settings


def configure(name: str) -> logging.Logger:
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.WARN)

    info_debug_handler = logging.StreamHandler(sys.stdout)
    info_debug_handler.setLevel(logging.NOTSET)
    info_debug_handler.addFilter(lambda record: record.levelno <= logging.INFO)

    logging.basicConfig(
        format="%(levelname)s:     %(asctime)s - %(name)s %(message)s",
        level=settings.LOG_LEVEL,
        handlers=[info_debug_handler, error_handler],
    )
    return logging.getLogger(name)
