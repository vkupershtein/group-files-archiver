"""
Module for GroupArchiver class with methods to move (or copy) and archive files
belonging to the users of selected group
"""
from datetime import datetime
import fcntl
import grp
import logging
from dataclasses import dataclass, field
from enum import Enum
import os
from pathlib import Path
import pwd
from typing import ClassVar, List
from zipfile import ZIP_DEFLATED, BadZipfile, ZipFile

from tqdm import tqdm

from .config import ARCHIVER_ARCHIVE_FOLDER, ARCHIVER_LOCK_FOLDER

logger = logging.getLogger('group-files-archiver')

class ArchiverException(Exception):
    """Custom archiver exception"""
    def __init__(self, message):
        self.message = message

class MoveMode(Enum):
    """Available move modes"""
    MOVE = 'move'
    COPY = 'copy'

@dataclass
class GroupUser:
    """Linux group member"""
    id: int
    name: str
    group: str

@dataclass
class MemberGroup:
    """Linux group"""
    name: str
    members: List[str]


@dataclass
class GroupArchiver:
    """Class to archive group files"""
    archive_folder: Path = field(default=Path(ARCHIVER_ARCHIVE_FOLDER))
    input_paths: List[Path] = field(default_factory=lambda: [Path('/home')])    
    move_mode: MoveMode = field(default=MoveMode.MOVE)
    lock_folder: ClassVar[Path] = Path(ARCHIVER_LOCK_FOLDER)

    def __post_init__(self):
        if self.archive_folder.is_file():
            raise ArchiverException('Provided archive folder is not a directory')
        
        self.archive_folder.mkdir(parents=True, exist_ok=True)
        self.lock_folder.mkdir(parents=True, exist_ok=True)
                
        self.inputs_paths = [input_path for input_path in self.input_paths 
                             if input_path.exists() and input_path.is_dir()]
        exclude_subpaths(self.input_paths)

        if len(self.input_paths) == 0:
            raise ArchiverException('No valid input paths provided')

    def _user_archive(self, group_user: GroupUser):
        """Archive files of a user"""
        lock_file = self.lock_folder.joinpath(f'archive_user_{group_user.name}.lock')
        with open(lock_file, "w") as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)                
                user_files = find_user_files(group_user.id, self.input_paths)
                if len(user_files) == 0:
                    str_input_paths = ','.join([str(path) for path in self.input_paths])
                    logger.warning(f'No files found for user {group_user.name} and input file paths {str_input_paths}. Skip')
                    return
                archive_name = get_archive_filename(group_user)
                target_archive = self.archive_folder.joinpath(archive_name)
                
                logger.info(f'Archiving files for user {group_user.name}')
                archive_files(user_files, target_archive)                                      
                if check_archive(target_archive, user_files):
                    logger.info(f'All {len(user_files)} files of user {group_user.name} archived')
                    if self.move_mode == MoveMode.MOVE:
                        logger.info(f'Removing files of user {group_user.name} from original location')
                        remove_files(user_files)
                        logger.info(f'Files of user {group_user.name} removed from original location')

            except BlockingIOError:
                raise ArchiverException(f'Another instance is already archiving user {group_user.name} files') 
                  
       
    def archive(self, member_group: str):
        """Archive files of users from member group"""
        lock_file = self.lock_folder.joinpath(f'archive_group_{member_group}.lock')
        with open(lock_file, "w") as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                group = get_group(member_group)
                group_users = get_group_users(group)
                logger.info(f'Archiving files for member group {member_group}')
                for group_user in group_users:
                    self._user_archive(group_user)
            except BlockingIOError:
                raise ArchiverException(f'Another instance is already archiving group {member_group} files')


def get_user_id(user_name: str) -> int:
    """Check if user exists in the user database"""
    try:
        return pwd.getpwnam(user_name).pw_uid
    except KeyError:
        return -1
    
def get_group(group_name: str) -> MemberGroup:
    """Get group object by group name"""
    try:
        group = grp.getgrnam(group_name)
        return MemberGroup(name=group.gr_name, members=group.gr_mem)
    except KeyError as ex:      
        raise ArchiverException(f'Member group {group_name} not found in the group database') from ex    

def get_group_users(group: MemberGroup) -> List[GroupUser]:
    """Get users of the member group"""  
    user_ids = []    
    for user_name in [group.name, *group.members]:
        user_id = get_user_id(user_name)
        if user_id != -1:
            user_ids.append(GroupUser(id=user_id, name=user_name, group=group.name))
    if len(user_ids) == 0:
        raise ArchiverException(f'No members found for the group {group.members} in the user database')
    return user_ids

def find_user_files(user_id: int, folders: List[Path]) -> List[Path]:
    """Find files of the user starting from specified folders"""
    user_files = []
    for folder in folders: 
        for root, _, files in os.walk(str(folder)):
            for file in files:
                path = Path(os.path.join(root, file))
                if path.exists() and path.stat().st_uid == user_id:
                    user_files.append(path)                
    return user_files

def get_archive_filename(group_user: GroupUser) -> str:
    """Get archive filename from group name and time"""    
    now = datetime.now().strftime('%Y%m%d_%H%M%S')    
    return f'{group_user.name}_{group_user.group}_{now}.zip'

def archive_files(filepaths: List[Path], target_archive: Path):
    """Archive filepaths to a target location with certain archive name"""    
    with ZipFile(target_archive, 'w', ZIP_DEFLATED) as zip_archive:
        for filepath in tqdm(filepaths):
            try:
                zip_archive.write(filepath)
            except PermissionError:
                logger.error(f'{filepath} can not be archived. Permission denied')

def exclude_subpaths(paths: List[Path]):
    """Exclude subpaths in-place"""
    i = 0    
    while i < len(paths):
        path = paths[i]
        for compare_path in paths:
            if path != compare_path and compare_path in path.parents:
                paths.pop(i)
                break
        else:
            i += 1

def check_archive(zip_filepath: Path, filepaths: List[Path]) -> bool:
    try:
        zfile = ZipFile(zip_filepath)
    except BadZipfile as ex:
        logger.error(f'{zip_filepath} no a zip file')
        return False
    
    ret = zfile.testzip()
    
    if ret is not None:
        logger.error(f'{zip_filepath} bad zip file, error: {ret}')
        return False

    archived_paths = zfile.infolist()
    
    if len(archived_paths) != len(filepaths):
        logger.error(f'{zip_filepath} not consistent, not all files archived')
        return False     
    return True

def remove_files(filepaths: List[Path]):
    """Remove files and folders if they are empty"""
    parent_folders = get_parent_folders(filepaths)    
    for filepath in filepaths:  # First remove files
        try:
            filepath.unlink()
        except FileNotFoundError:
            logger.warning(f'{filepath} is missing. Can not be removed')
    # Remove parent folders if empty
    for folder in sorted(parent_folders, key=lambda x: -len(str(x))): 
        if len(list(folder.iterdir())) == 0:
            folder.rmdir()

def get_parent_folders(filepaths: List[Path]):
    """Get parent folders"""
    folders = set()    
    for filepath in filepaths:
        folders.update(filepath.parents)
    return list(folders)        
