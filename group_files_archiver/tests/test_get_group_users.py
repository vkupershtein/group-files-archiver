"""
Test module for get group users function
"""
import pytest
from group_files_archiver.group_archiver import (ArchiverException, 
                                                 get_group_users, 
                                                 MemberGroup, 
                                                 GroupUser)

def fake_get_user_id(user_name: str) -> int:
    """Fake function to get user id by user name"""
    users = {
        'richard': 1000,
        'manuel': 1001,
        'brad': 1002
    }
    return users.get(user_name, -1)

def test_get_group_users_with_owner_only(monkeypatch):
    """Test case if only owner is present in the group"""
    monkeypatch.setattr('group_files_archiver.group_archiver.get_user_id', fake_get_user_id)
    group = MemberGroup(name='manuel', members=[])
    
    expected = [GroupUser(id=1001, name='manuel', group='manuel')]

    assert get_group_users(group) == expected

def test_get_group_users_with_owner_and_members(monkeypatch):
    """Test case if owner and members are present in the group and they are users"""
    monkeypatch.setattr('group_files_archiver.group_archiver.get_user_id', fake_get_user_id)
    group = MemberGroup(name='manuel', members=['brad'])
    
    expected = [GroupUser(id=1001, name='manuel', group='manuel'),
                GroupUser(id=1002, name='brad', group='manuel')]

    assert get_group_users(group) == expected

def test_get_group_users_with_non_user_owner_and_members(monkeypatch):
    """Test case if owner is not a user and but members are users"""
    monkeypatch.setattr('group_files_archiver.group_archiver.get_user_id', fake_get_user_id)
    group = MemberGroup(name='docker', members=['brad', 'richard'])
    
    expected = [GroupUser(id=1002, name='brad', group='docker'),
                GroupUser(id=1000, name='richard', group='docker')]

    assert get_group_users(group) == expected

def test_get_group_users_with_non_user_owner(monkeypatch):
    """Test case if owner is not a user and no members present"""
    monkeypatch.setattr('group_files_archiver.group_archiver.get_user_id', fake_get_user_id)
    group = MemberGroup(name='docker', members=[])   

    with pytest.raises(ArchiverException):
        get_group_users(group)
