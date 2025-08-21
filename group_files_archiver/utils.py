"""Utility functions"""

import logging
from pathlib import Path
from .config import Config


def ensure_paths(config: Config):
    """Ensure that paths to archive, log and lock folders exist"""
    Path(config['ARCHIVER_LOG_PATH']).parent.mkdir(parents=True, exist_ok=True)
    Path(config['ARCHIVER_ARCHIVE_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path(config['ARCHIVER_LOCK_FOLDER']).mkdir(parents=True, exist_ok=True)    

def activate_logging(config: Config):
    """Activate logging for the program"""
    format = '%(asctime)s %(levelname)s: %(message)s'
    formatter = logging.Formatter(format)
    logging.basicConfig(format=format, level=logging.INFO)
    logger = logging.getLogger('group-files-archiver')
    file_handler = logging.FileHandler(filename=config['ARCHIVER_LOG_PATH'], encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger