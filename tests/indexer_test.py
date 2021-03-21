"""Tests for indexer module."""
from findzen.indexer import index_builder, populated_org_index_with_users_tickets, populate_user_index_with_org_tickets, populate_ticket_index_with_user_org
from findzen.models.user import User, Users
from findzen.models.org import Organization, Organizations
from findzen.models.ticket import Ticket, Tickets
import dictdiffer


def test_index_builder(sample_users: list) -> None:
    expected_user_index = {
        'user_index_by_id': {
            '1': sample_users[0].dict(),
            '2': sample_users[1].dict()
        },
        'user_index_by_url': {
            'url.com': [1, 2]
        },
        'user_index_by_external_id': {
            '100': [1],
            '200': [2]
        },
        'user_index_by_name': {
            'John Doe': [1],
            'Jane Doe': [2]
        },
        'user_index_by_alias': {
            'Johnny': [1],
            'None': [2]
        },
        'user_index_by_created_at': {
            '2016-06-23T10:31:39 -10:00': [1],
            '2017-06-23T10:31:39 -10:00': [2]
        },
        'user_index_by_active': {
            'True': [1],
            'False': [2]
        },
        'user_index_by_verified': {
            'True': [1],
            'None': [2]
        },
        'user_index_by_shared': {
            'False': [1, 2]
        },
        'user_index_by_locale': {
            'zh-CN': [1],
            'None': [2]
        },
        'user_index_by_timezone': {
            'Armenia': [1],
            'None': [2]
        },
        'user_index_by_last_login_at': {
            '2012-04-12T04:03:28 -10:00': [1],
            '2015-04-12T04:03:28 -10:00': [2]
        },
        'user_index_by_email': {
            'john@url.com': [1],
            'None': [2]
        },
        'user_index_by_phone': {
            '9575-552-585': [1],
            '9675-552-585': [2]
        },
        'user_index_by_signature': {
            'Fake': [1],
            'StillFake': [2]
        },
        'user_index_by_organization_id': {
            '1000': [1],
            'None': [2]
        },
        'user_index_by_tags': {
            'tag1': [1, 2],
            'tag2': [1],
            'tag22': [2]
        },
        'user_index_by_suspended': {
            'False': [1],
            'True': [2]
        },
        'user_index_by_role': {
            'admin': [1],
            'role': [2]
        },
    }

    users = Users.parse_obj(sample_users)
    actual_users_index = index_builder(users, User)

    assert len(list(dictdiffer.diff(expected_user_index,
                                    actual_users_index))) == 0


def test_populated_org_index_with_users_tickets(sample_users: list,
                                                sample_orgs: list,
                                                sample_tickets: list) -> None:
    users = Users.parse_obj(sample_users)
    user_index_pre_population = index_builder(users, User)

    orgs = Organizations.parse_obj(sample_orgs)
    orgs_index_pre_population = index_builder(orgs, Organization)

    tickets = Tickets.parse_obj(sample_tickets)
    ticket_index_pre_population = index_builder(tickets, Ticket)

    org_index_populated = populated_org_index_with_users_tickets(
        user_index_pre_population, orgs_index_pre_population,
        ticket_index_pre_population)

    org1000_expected_user = [sample_users[0]]
    org2000_expected_user = []

    org1000_expected_tickets = [sample_tickets[0], sample_tickets[1]]
    org2000_expected_tickets = []

    assert org_index_populated['organization_index_by_id']['1000'][
        'users'] == org1000_expected_user
    assert org_index_populated['organization_index_by_id']['2000'][
        'users'] == []
    assert org_index_populated['organization_index_by_id']['1000'][
        'tickets'].sort(
            key=lambda x: x['id']) == org1000_expected_tickets.sort(
                key=lambda x: x.id)
    assert org_index_populated['organization_index_by_id']['2000'][
        'tickets'] == []


def test_populate_user_index_with_org_tickets(sample_users: list,
                                              sample_orgs: list,
                                              sample_tickets: list) -> None:
    users = Users.parse_obj(sample_users)
    user_index_pre_population = index_builder(users, User)

    orgs = Organizations.parse_obj(sample_orgs)
    orgs_index_pre_population = index_builder(orgs, Organization)

    tickets = Tickets.parse_obj(sample_tickets)
    ticket_index_pre_population = index_builder(tickets, Ticket)

    user_index_populated = populate_user_index_with_org_tickets(
        user_index_pre_population, orgs_index_pre_population,
        ticket_index_pre_population)

    user1_expected_org = sample_orgs[0]
    user2_expected_org = []
    user1_expected_tickets = sample_tickets
    user2_expected_tickets = []

    assert user_index_populated['user_index_by_id']['1'][
        'organization'] == user1_expected_org
    assert user_index_populated['user_index_by_id']['2'][
        'organization'] == user2_expected_org
    assert user_index_populated['user_index_by_id']['1']['tickets'].sort(
        key=lambda x: x['id']) == user1_expected_tickets.sort(
            key=lambda x: x.id)
    assert user_index_populated['user_index_by_id']['2'][
        'tickets'] == user2_expected_tickets


def test_populate_ticket_index_with_user_org(sample_users: list,
                                             sample_orgs: list,
                                             sample_tickets: list) -> None:
    users = Users.parse_obj(sample_users)
    user_index_pre_population = index_builder(users, User)

    orgs = Organizations.parse_obj(sample_orgs)
    orgs_index_pre_population = index_builder(orgs, Organization)

    tickets = Tickets.parse_obj(sample_tickets)
    ticket_index_pre_population = index_builder(tickets, Ticket)

    ticket_index_populated = populate_ticket_index_with_user_org(
        user_index_pre_population, orgs_index_pre_population,
        ticket_index_pre_population)

    ticket1_expected_user = sample_users[0]
    ticket2_expected_user = sample_users[0]
    ticket1_expected_org = sample_orgs[0]
    ticket2_expected_org = sample_orgs[0]

    assert ticket_index_populated['ticket_index_by_id']['Tix1'][
        'user'] == ticket1_expected_user
    assert ticket_index_populated['ticket_index_by_id']['Tix2'][
        'user'] == ticket2_expected_user
    assert ticket_index_populated['ticket_index_by_id']['Tix1'][
        'organization'] == ticket1_expected_org
    assert ticket_index_populated['ticket_index_by_id']['Tix2'][
        'organization'] == ticket2_expected_org
