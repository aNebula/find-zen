from findzen.commands.ticket_cmd import TicketCmd
from findzen.commands.load_data import LoadDataCmd
import argparse
import pytest


def test_ticket_cmd_found_multiple(sample_data_dir):
    """Test multiple ticket found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    tickets = TicketCmd()._search_ticket('priority', 'high')
    assert len(tickets) == 2
    assert tickets[0]['id'] == 'Tix1'
    assert tickets[1]['url'] == 'tix.com.au/Tix2'
    assert tickets[0]['user']['name'] == 'John Doe'
    assert tickets[1]['user']['name'] == 'John Doe'
    assert tickets[0]['organization']['id'] == 1000
    assert tickets[1]['organization']['id'] == 1000
 

def test_ticket_cmd_found_single(sample_data_dir):
    """Test multiple ticket found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    tickets = TicketCmd()._search_ticket('id', 'Tix1')
    assert len(tickets) == 1
    assert tickets[0]['id'] == 'Tix1'
    assert tickets[0]['type'] == 'Bug'
    assert tickets[0]['user']['name'] == 'John Doe'
    assert tickets[0]['organization']['id'] == 1000


def test_ticket_cmd_not_found(sample_data_dir):
    """Test ticket not found."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)

    tickets = TicketCmd()._search_ticket('id', '1')
    assert len(tickets) == 0


def test_ticket_not_field(sample_data_dir):
    """Test ticket does not have field."""
    ldc = LoadDataCmd()
    args = argparse.Namespace(name='load', path=sample_data_dir)
    ldc._run(args)
    with pytest.raises(BaseException):
        TicketCmdgCmd()._search_ticket('ticket_id', '98')