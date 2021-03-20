from findzen.file_handler import CacheHandler


def search(entity_type, field, queries):
    cache = CacheHandler()
    cache_type = f'{entity_type}_index_by_{field}'
    search_index = cache.read_cache(cache_type)

    results = []
    for query in queries:
        if str(query) in search_index:
            result = search_index[str(query)]
            results.append(result)
        else:
            results.append(None)

    return results


def search_org_ticket_by_users(users):
    cache = CacheHandler()
    user_ids = [user["id"] for user in users]
    org_ids = [user["organization_id"] for user in users]
    orgs =search('organization', "id", org_ids)
    ticket_ids = search('ticket', "submitter_id", user_ids)

    ticket_index_by_id = cache.read_cache('ticket_index_by_id')

    results = []
    for idx, user in enumerate(users):
        tickets=[]
        if ticket_ids[idx] is not None:
            for ticket_id in ticket_ids[idx]:
                if ticket_id in ticket_index_by_id:
                    tickets.append(ticket_index_by_id[ticket_id])
        else:
            tickets=None
        result = {"user": user, "org": orgs[idx], "tickets": tickets}
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
        if user_ids[idx] is not None:
            for user_id in user_ids[idx]:
                if str(user_id) in user_index_by_id:
                    users.append(user_index_by_id[str(user_id)])
        else:
            users=None
        tickets = []
        if ticket_ids[idx] is not None:
            for ticket_id in ticket_ids[idx]:
                if str(ticket_id) in ticket_index_by_id:
                    tickets.append(ticket_index_by_id[str(ticket_id)])
        else:
            tickets=None
        
        result={"org": org, "users": users, "tickets": tickets}
        results.append(result)

    return results
        
