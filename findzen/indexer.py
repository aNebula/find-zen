from findzen.utils import append_or_create, fetch_if_key

def index_builder(data, data_type):
    all_indexes = {}
    key_prefix = f'{data_type.__name__.lower()}_index_by_'
    for key in data_type.__fields__:
        all_indexes[f'{key_prefix}{key}']= {}

    for entry in data.dict()["__root__"]:
        for key in data_type.__fields__:
            key_string = f'{key_prefix}{key}'
            if key == "id":
                all_indexes[key_string][str(entry[key])] =  entry
                continue
            if key == "tags":
                for tag in entry["tags"]:
                    all_indexes[key_string]=  append_or_create(all_indexes[key_string], str(tag), entry["id"])
                continue
            if key == "domain_names":
                for domain_name in entry["domain_names"]:
                    all_indexes[key_string]=  append_or_create(all_indexes[key_string], str(domain_name), entry["id"])
                continue

            all_indexes[key_string]= append_or_create(all_indexes[key_string], str(entry[key]), entry["id"])
    
    return all_indexes


def populated_org_index_with_users_tickets(user_index, org_index, ticket_index):

    org_index_by_id = org_index["organization_index_by_id"]
    user_index_by_id = user_index["user_index_by_id"]
    ticket_index_by_id = ticket_index["ticket_index_by_id"]

    for org_id in org_index_by_id:
        user_ids = fetch_if_key(user_index["user_index_by_organization_id"],org_id)
        users = []
        for user_id in user_ids:
            users.append(fetch_if_key(user_index_by_id,user_id))
        org_index["organization_index_by_id"][org_id]["users"] = users
        
        ticket_ids = fetch_if_key(ticket_index["ticket_index_by_organization_id"],org_id)
        tickets = []
        for ticket_id in ticket_ids:
            tickets.append(fetch_if_key(ticket_index_by_id, ticket_id))
        org_index["organization_index_by_id"][org_id]["tickets"] = tickets

    return org_index


def populate_user_index_with_org_tickets(user_index, org_index, ticket_index):
    org_index_by_id = org_index["organization_index_by_id"]
    user_index_by_id = user_index["user_index_by_id"]
    ticket_index_by_id = ticket_index["ticket_index_by_id"]

    for user_id in user_index_by_id:
        # a user belongs to one organization
        org_id = user_index_by_id[user_id]["organization_id"]
        if org_id is None:
            user_index["user_index_by_id"][user_id]["organization"] = []
        else:
            user_index["user_index_by_id"][user_id]["organization"] = fetch_if_key(org_index_by_id,org_id)
        
        ticket_ids = fetch_if_key(ticket_index["ticket_index_by_submitter_id"], user_id)
        tickets = []
        for ticket_id in ticket_ids:
            tickets.append(fetch_if_key(ticket_index_by_id,ticket_id))
        user_index["user_index_by_id"][user_id]["tickets"] = tickets

    return user_index


def populate_ticket_index_with_user_org(user_index, org_index, ticket_index):
    org_index_by_id = org_index["organization_index_by_id"]
    user_index_by_id = user_index["user_index_by_id"]
    ticket_index_by_id = ticket_index["ticket_index_by_id"]

    for ticket_id in ticket_index_by_id:
        user_id = ticket_index_by_id[ticket_id]["submitter_id"]
        if user_id is None:
            ticket_index["ticket_index_by_id"][ticket_id]["user"] = []
        else:
            ticket_index["ticket_index_by_id"][ticket_id]["user"] = fetch_if_key(user_index_by_id, user_id)

        org_id = ticket_index_by_id[ticket_id]["organization_id"]
        if org_id is None:
            ticket_index["ticket_index_by_id"][ticket_id]["organization"] = []
        else:
            ticket_index["ticket_index_by_id"][ticket_id]["organization"] = fetch_if_key(org_index_by_id, org_id)

    return ticket_index
