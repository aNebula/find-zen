from findzen.commands.user_cmd import UserCmd
from findzen.commands.load_data import LoadDataCmd
import argparse
import pytest


def test_user_cmd_found_multiple(sample_data_dir):
    """Test multiple user found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    users = UserCmd()._search_user('url', 'url.com')
    assert len(users) == 2
    assert users[0]['name'] == 'John Doe'
    assert users[1]['name'] == 'Jane Doe'
    assert users[0]['organization']['name'] == 'Good Organization'
    assert users[1]['organization'] == []
    assert users[0]['tickets'][0]['id'] == 'Tix1'
    assert users[0]['tickets'][1]['id'] == 'Tix2'


def test_user_cmd_found_single(sample_data_dir):
    """Test single user found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    user = UserCmd()._search_user('id', '2')
    assert len(user) == 1
    assert user[0]['name'] == 'Jane Doe'
    assert user[0]['organization'] == []
    assert user[0]['tickets'] == []


def test_user_cmd_not_found(sample_data_dir):
    """Test user not found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    user = UserCmd()._search_user('id', '98')
    assert len(user) == 0


def test_user_cmd_not_field(sample_data_dir):
    """Test argument not a field."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)
    with pytest.raises(BaseException):
        UserCmd()._search_user('ticket_id', '98')