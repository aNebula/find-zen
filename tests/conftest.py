import pytest
import json
import pathlib
import os
from findzen.models.user import User
from findzen.models.org import Organization
from findzen.models.ticket import Ticket


@pytest.fixture
def sample_users():
    user1 = User(
        _id=1, url="url.com", external_id="100", 
        name="John Doe", alias="Johnny", created_at="2016-06-23T10:31:39 -10:00",
        active=True, verified=True, shared=False, locale="zh-CN",
        timezone="Armenia", last_login_at="2012-04-12T04:03:28 -10:00",
        email="john@url.com", phone="9575-552-585", signature="Fake",
        organization_id="101", tags=["tag1", "tag2"], suspended=False, role="admin"
        )
    user2 = User(
        _id=2, url="url2.com", external_id="200", 
        name="Jane Doe", created_at="2017-06-23T10:31:39 -10:00",
        active=False, shared=False, last_login_at="2015-04-12T04:03:28 -10:00",
        phone="9675-552-585", signature="StillFake",
        tags=["tag11", "tag22"], suspended=True, role="role"
        )    
    users_list = [user1, user2]
    return users_list

@pytest.fixture
def sample_orgs():
    org1 = Organization(_id=1000, url="org1.au", external_id="1000-org", name="Good Organization",
    domain_names=["org1.au"], created_at="2017-06-23T10:31:39 -10:00", details="LedaCorp",
    shared_tickets=True, tags=["tag100, tag200"])

    org2 = Organization(_id=2000, url="org2.au", external_id="2000-org", name="Bad Organization",
    domain_names=["org2.au"], created_at="2020-06-23T10:31:39 -10:00", details="PidaCorp",
    shared_tickets=False, tags=["tag200, tag400"])

    orgs_list = [org1, org2]
    return orgs_list

@pytest.fixture
def sample_tickets():
    ticket1 = Ticket(_id="Tix1", url="tix.com.au/Tix1", external_id="Tix-Au-1",
    created_at="2017-06-23T10:31:39 -10:00", type="Bug", subject="subject1",
    description="description1", priority="high", status="", submitter_id="1",
    assignee_id="2", organization_id="1000", tags=["FIXME", "TODO"],
    has_incidents=True, due_at="2017-06-23T10:31:39 -12:00", via="NoOne"
    )

    ticket2 = Ticket(_id="Tix2", url="tix.com.au/Tix2", external_id="Tix-Au-2",
    created_at="2017-06-23T10:31:39 -10:00", subject="subject1", priority="high", 
    status="", submitter_id="1", organization_id="1000", tags=["FIXME2", "TODO2"],
    has_incidents=True, via="NoOne"
    )

    tickets_list = [ticket1, ticket2]
    return tickets_list

@pytest.fixture
def sample_data_dir(tmp_path, sample_users, sample_orgs, sample_tickets):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    users_filename = data_dir / "users.json"
    orgs_filename = data_dir / "organizations.json"
    tickets_filename = data_dir / "tickets.json"

    users = [user.dict(by_alias=True) for user in sample_users]
    orgs = [org.dict(by_alias=True) for org in sample_orgs]
    tickets = [ticket.dict(by_alias=True) for ticket in sample_tickets]

    with open(users_filename, 'w') as f:
        json.dump(users, f)
    with open(orgs_filename, 'w') as f:
        json.dump(orgs, f)
    with open(tickets_filename, 'w') as f:
        json.dump(tickets, f)

    return data_dir

@pytest.fixture
def tmp_cwd(tmp_path):
    pytest_cwd = pathlib.Path.cwd()
    os.chdir(tmp_path)

    yield tmp_path

    os.chdir(pytest_cwd)
