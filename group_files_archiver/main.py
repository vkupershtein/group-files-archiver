"""
Group files archiver entry point
"""
import logging
from pathlib import Path
from argparse import ArgumentParser

from group_archiver import ArchiverException, GroupArchiver, MoveMode
from config import (ARCHIVER_ARCHIVE_FOLDER, ARCHIVER_LOG_PATH, ARCHIVER_LOCK_FOLDER)

def ensure_paths():
    """Ensure that paths to archive, log and lock folders exist"""
    Path(ARCHIVER_LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(ARCHIVER_ARCHIVE_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(ARCHIVER_LOCK_FOLDER).mkdir(parents=True, exist_ok=True)    

def activate_logging():
    """Activate logging for the program"""
    format = '%(asctime)s %(levelname)s: %(message)s'
    formatter = logging.Formatter(format)
    logging.basicConfig(format=format, level=logging.INFO)
    logger = logging.getLogger('group-files-archiver')
    file_handler = logging.FileHandler(filename=ARCHIVER_LOG_PATH, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def main():
    """Main program function to archive files that belong to the same group"""
    ensure_paths()
    logger = activate_logging()
    parser = ArgumentParser(
                        prog='Group Files Archiver',
                        description='Program archives files of all users, that belong to the specified group') 
    parser.add_argument('member_group')
    parser.add_argument('-c', '--copy-files', action='store_true')
    parser.add_argument('--archive-location', type=Path, default=Path(ARCHIVER_ARCHIVE_FOLDER))
    parser.add_argument('--input-paths', type=Path, nargs='*', default=[Path('/home')])

    args = parser.parse_args()

    move_mode = MoveMode.COPY if args.copy_files else MoveMode.MOVE
    try:
        GroupArchiver(archive_folder=args.archive_location,
                    input_paths=args.input_paths,
                    move_mode=move_mode).archive(args.member_group)
    except ArchiverException as ex:
        logger.error(ex.message)    

if __name__ == '__main__':
    main()