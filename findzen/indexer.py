"""Module providing methods for indexing data."""
from findzen.utils import append_or_create, fetch_if_key
from findzen.models.user import User
from findzen.models.org import Organization
from findzen.models.ticket import Ticket
from typing import Union


def index_builder(data: dict, data_type: Union[User, Organization,
                                               Ticket]) -> dict:
    """
    Given a `data` dictionary and the type of data, build index of the `data` 
    on all the fields for the data type.
    Field values map to array of ids. Except for index by id, which maps id to 
    the whole object with the id.
    Returns a giant dictionary, mapping index name to index dictionary.
    """
    all_indexes = {}
    key_prefix = f'{data_type.__name__.lower()}_index_by_'
    for key in data_type.__fields__:
        all_indexes[f'{key_prefix}{key}'] = {}

    for entry in data.dict()['__root__']:
        for key in data_type.__fields__:
            key_string = f'{key_prefix}{key}'
            if key == 'id':
                all_indexes[key_string][str(entry[key])] = entry
                continue
            if key == 'tags':
                for tag in entry['tags']:
                    all_indexes[key_string] = append_or_create(
                        all_indexes[key_string], str(tag), entry['id'])
                continue
            if key == 'domain_names':
                for domain_name in entry['domain_names']:
                    all_indexes[key_string] = append_or_create(
                        all_indexes[key_string], str(domain_name), entry['id'])
                continue

            all_indexes[key_string] = append_or_create(all_indexes[key_string],
                                                       str(entry[key]),
                                                       entry['id'])

    return all_indexes


def populated_org_index_with_users_tickets(user_index: dict, org_index: dict,
                                           ticket_index: dict) -> dict:
    """
    Given User, Organizations and Tickets index, populate each instance of 
    Organization (in organization_index_by_id) with associated Users and 
    Tickets to facilitate constant time retrieval.
    """

    org_index_by_id = org_index['organization_index_by_id']
    user_index_by_id = user_index['user_index_by_id']
    ticket_index_by_id = ticket_index['ticket_index_by_id']

    for org_id in org_index_by_id:
        user_ids = fetch_if_key(user_index['user_index_by_organization_id'],
                                org_id)
        users = []
        for user_id in user_ids:
            users.append(fetch_if_key(user_index_by_id, user_id))
        org_index['organization_index_by_id'][org_id]['users'] = users

        ticket_ids = fetch_if_key(
            ticket_index['ticket_index_by_organization_id'], org_id)
        tickets = []
        for ticket_id in ticket_ids:
            tickets.append(fetch_if_key(ticket_index_by_id, ticket_id))
        org_index['organization_index_by_id'][org_id]['tickets'] = tickets

    return org_index


def populate_user_index_with_org_tickets(user_index: dict, org_index: dict,
                                         ticket_index: dict) -> dict:
    """
    Given User, Organizations and Tickets index, populate each instance of 
    User(in user_index_by_id) with associated Users and Tickets to 
    facilitate constant time retrieval.
    """
    org_index_by_id = org_index['organization_index_by_id']
    user_index_by_id = user_index['user_index_by_id']
    ticket_index_by_id = ticket_index['ticket_index_by_id']

    for user_id in user_index_by_id:
        # a user belongs to one organization
        org_id = user_index_by_id[user_id]['organization_id']
        if org_id is None:
            user_index['user_index_by_id'][user_id]['organization'] = []
        else:
            user_index['user_index_by_id'][user_id][
                'organization'] = fetch_if_key(org_index_by_id, org_id)

        ticket_ids = fetch_if_key(ticket_index['ticket_index_by_submitter_id'],
                                  user_id)
        tickets = []
        for ticket_id in ticket_ids:
            tickets.append(fetch_if_key(ticket_index_by_id, ticket_id))
        user_index['user_index_by_id'][user_id]['tickets'] = tickets

    return user_index


def populate_ticket_index_with_user_org(user_index: dict, org_index: dict,
                                        ticket_index: dict) -> dict:
    """
    Given User, Organizations and Tickets index, populate each instance of 
    Ticket(in ticket_index_by_id) with associated User and Organization to 
    facilitate constant time retrieval.
    """
    org_index_by_id = org_index['organization_index_by_id']
    user_index_by_id = user_index['user_index_by_id']
    ticket_index_by_id = ticket_index['ticket_index_by_id']

    for ticket_id in ticket_index_by_id:
        user_id = ticket_index_by_id[ticket_id]['submitter_id']
        if user_id is None:
            ticket_index['ticket_index_by_id'][ticket_id]['user'] = []
        else:
            ticket_index['ticket_index_by_id'][ticket_id][
                'user'] = fetch_if_key(user_index_by_id, user_id)

        org_id = ticket_index_by_id[ticket_id]['organization_id']
        if org_id is None:
            ticket_index['ticket_index_by_id'][ticket_id]['organization'] = []
        else:
            ticket_index['ticket_index_by_id'][ticket_id][
                'organization'] = fetch_if_key(org_index_by_id, org_id)

    return ticket_index
