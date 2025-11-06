import logging
import pathlib

def setup_logger() -> logging.Logger:
    LOG_HOME_PATH = pathlib.Path.cwd()
    LOG_PATH = LOG_HOME_PATH / ".log"
    logger = logging.getLogger("bookmark-assistant")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(LOG_PATH)
    formatter = logging.Formatter('%(name)s | %(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger