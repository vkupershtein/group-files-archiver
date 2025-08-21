"""Configurable environment"""

import os
from typing import TypedDict

class Config(TypedDict):
    ARCHIVER_LOG_PATH: str
    ARCHIVER_ARCHIVE_FOLDER: str
    ARCHIVER_LOCK_FOLDER: str

def create_config() -> Config:
    """Create config"""
    return Config({'ARCHIVER_LOG_PATH': os.environ.get('ARCHIVER_LOG_PATH', 'log/group-files-archiver.log'), 
                  'ARCHIVER_ARCHIVE_FOLDER': os.environ.get('ARCHIVER_ARCHIVE_FOLDER', 'archive'),
                  'ARCHIVER_LOCK_FOLDER': os.environ.get('ARCHIVER_LOCK_FOLDER', 'locks')})


