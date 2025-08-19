"""Configurable environment"""

import os

ARCHIVER_LOG_PATH = os.environ.get('ARCHIVER_LOG_PATH', 'log/group-files-archiver.log')
ARCHIVER_ARCHIVE_FOLDER = os.environ.get('ARCHIVER_ARCHIVE_FOLDER', 'archive')
ARCHIVER_LOCK_FOLDER = os.environ.get('ARCHIVER_LOCK_FOLDER', 'locks')
