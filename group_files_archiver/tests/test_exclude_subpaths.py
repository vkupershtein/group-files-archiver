"""
Test module for exclude subpaths function
"""

from pathlib import Path
from group_files_archiver.group_archiver import exclude_subpaths


def test_no_subpaths():
    """Test case when no subpaths given"""
    paths = [Path('/home/great'), Path('/var/lib')]
    exclude_subpaths(paths)
    assert paths == [Path('/home/great'), Path('/var/lib')]

def test_one_subpath():
    """Test case when one subpath given"""
    paths = [Path('/home/great'), Path('/home/great/world'), Path('/var/lib')]
    exclude_subpaths(paths)
    assert paths == [Path('/home/great'), Path('/var/lib')]

def test_two_subpaths():
    """Test case when two different subpaths given"""
    paths = [Path('/var/lib/somelib'), Path('/home/great'), Path('/home/great/world'), Path('/var/lib')]
    exclude_subpaths(paths)
    assert paths == [Path('/home/great'), Path('/var/lib')]