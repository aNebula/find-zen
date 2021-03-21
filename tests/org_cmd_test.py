from findzen.commands.org_cmd import OrgCmd
from findzen.commands.load_data import LoadDataCmd
import argparse
import pytest


def test_org_cmd_found_multiple(sample_data_dir):
    """Test multiple orgs found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    orgs = OrgCmd()._search_org('tags', 'tag200')
    assert len(orgs) == 2
    assert orgs[0]['name'] == 'Good Organization'
    assert orgs[1]['name'] == 'Bad Organization'
    assert orgs[0]['users'][0]['name'] == 'John Doe'
    assert orgs[1]['users'] == []
    assert orgs[0]['tickets'][0]['id'] == 'Tix1'
    assert orgs[0]['tickets'][1]['id'] == 'Tix2'
    assert orgs[1]['tickets'] == []


def test_org_cmd_found_single(sample_data_dir):
    """Test multiple orgs found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    orgs = OrgCmd()._search_org('id', '1000')
    assert len(orgs) == 1
    assert orgs[0]['id'] == 1000
    assert orgs[0]['name'] == 'Good Organization'
    assert orgs[0]['users'][0]['name'] == 'John Doe'
    assert orgs[0]['tickets'][0]['id'] == 'Tix1'


def test_org_cmd_not_found(sample_data_dir):
    """Test org not found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    orgs = OrgCmd()._search_org('id', '1')
    assert len(orgs) == 0


def test_org_not_field(sample_data_dir):
    """Test org does not have the field."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)
    with pytest.raises(BaseException):
        OrgCmd()._search_org('ticket_id', '98')