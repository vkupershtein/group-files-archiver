"""
Group files archiver entry point
"""
import logging
from pathlib import Path
from argparse import ArgumentParser

from group_files_archiver.group_archiver import ArchiverException, GroupArchiver, MoveMode
from group_files_archiver.config import ARCHIVER_ARCHIVE_FOLDER, ARCHIVER_LOG_PATH

format = '%(asctime)s %(levelname)s: %(message)s'
formatter = logging.Formatter(format)
logging.basicConfig(format=format, level=logging.INFO)
logger = logging.getLogger('group-files-archiver')
file_handler = logging.FileHandler(filename=ARCHIVER_LOG_PATH, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def main():
    """Main program function to archive files that belong to the same group"""
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