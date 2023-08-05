import os
import logging
import logging.handlers
from .config import LogConfig


LOG_PATH = "log"
LOG_NAME = "your-log-name.log"
SAVE_PATH = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                LOG_PATH, 
                LOG_NAME)
CONSOLE_LEVEL = LogConfig.console_level
FILE_LEVEL    = LogConfig.file_level
MAX_BYTES     = LogConfig.max_bytes
BACKUP_COUNT  = LogConfig.backup_count
FORMATTER     = LogConfig.formatter


def init_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(CONSOLE_LEVEL)

    formatter = logging.Formatter(FORMATTER)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file_logger = logging.handlers.RotatingFileHandler(
            SAVE_PATH,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
    file_logger.setFormatter(formatter)
    file_logger.setLevel(FILE_LEVEL)

    logger.addHandler(console)
    logger.addHandler(file_logger)
    return logger

logger = init_logger()
