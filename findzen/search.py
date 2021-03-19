from file_handler import CacheHandler


def search(entity_type, field, queries, flatten_list=False):
    cache = CacheHandler()
    cache_type = f'{entity_type}_index_by_{field}'
    search_index = cache.read_cache(cache_type)

    results = []
    for query in queries:
        if str(query) in search_index:
            result = search_index[str(query)]
            results.append(result)

            # if type(result) is list:
            #     results+=result
            # else:
            #     results.append(result)
    if flatten_list==True:
        nested_results = results
        results = [item for sublist in nested_results for item in sublist]
    return results


def search_org_ticket_by_users(users):
    cache = CacheHandler()
    org_index_by_id = cache.read_cache('organization_index_by_id')
    ticket_index_by_submitter_id = cache.read_cache('ticket_index_by_submitter_id')
    ticket_index_by_id = cache.read_cache('ticket_index_by_id')

    results = []

    for user in users:

        result= {"user": user, "org" : None, "tickets" : []}
        user_id= str(user["id"])

        org_id = str(user["organization_id"])
        if org_id in org_index_by_id:
            org = org_index_by_id[org_id]
            result["org"] = org

        if user_id in ticket_index_by_submitter_id:
            ticket_ids = ticket_index_by_submitter_id[user_id]
            for ticket_id in ticket_ids:
                ticket = ticket_index_by_id[ticket_id]
                result["tickets"].append(ticket)

        results.append(result)

    return results

def search_user_org_by_tickets(tickets):
    ticket_ids = [ticket["id"] for ticket in tickets]
    orgs_ids = [ticket["organization_id"] for ticket in tickets]
    user_ids = [ticket["submitter_id"] for ticket in tickets]

    orgs = search('organization', 'id', orgs_ids)
    users = search('user', 'id', user_ids)

    results = []
    for idx,ticket in enumerate(tickets):
        result = {"ticket": ticket, "org": orgs[idx], "user": users[idx]}
        results.append(result)

    return results

def search_user_ticket(orgs):
    org_ids = [org["id"] for org in orgs]

    user_ids = search('user', 'organization_id', org_ids)
    ticket_ids = search('ticket', 'organization_id', org_ids)
    
    cache = CacheHandler()
    user_index_by_id = cache.read_cache('user_index_by_id')
    ticket_index_by_id = cache.read_cache('ticket_index_by_id')

    results = []
    for idx,org in enumerate(orgs):
        users = []
        for user_id in user_ids[idx]:
            if str(user_id) in user_index_by_id:
                users.append(user_index_by_id[str(user_id)])
        tickets = []
        for ticket_id in ticket_ids[idx]:
            if str(ticket_id) in ticket_index_by_id:
                tickets.append(ticket_index_by_id[str(ticket_id)])
        
        result={"org": org, "users": users, "tickets": tickets}
        results.append(result)

    return results
        
