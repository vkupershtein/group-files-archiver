"""Command line interface"""

from argparse import ArgumentParser
import logging
from pathlib import Path

from .group_archiver import ArchiverException, GroupArchiver, MoveMode
from .config import Config

logger = logging.getLogger('group-files-archiver')


def run(config: Config):
    """Read user input and run program with command line interface"""
    parser = ArgumentParser(
                        prog='Group Files Archiver',
                        description='Program archives files of all users, that belong to the specified group') 
    parser.add_argument('member_group')
    parser.add_argument('-c', '--copy-files', action='store_true')
    parser.add_argument('--archive-location', type=Path, default=Path(config['ARCHIVER_ARCHIVE_FOLDER']))
    parser.add_argument('--input-paths', type=Path, nargs='*', default=[Path('/home')])

    args = parser.parse_args()

    move_mode = MoveMode.COPY if args.copy_files else MoveMode.MOVE
    try:
        GroupArchiver(archive_folder=args.archive_location,
                      lock_folder=Path(config['ARCHIVER_LOCK_FOLDER']),
                      input_paths=args.input_paths,
                      move_mode=move_mode).archive(args.member_group)
    except ArchiverException as ex:
        logger.error(ex.message)    