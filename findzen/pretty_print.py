def pretty_print_users(users_orgs_tickets):
    for user_details in users_orgs_tickets:
        print("==========================================")
        print("USER")
        print("==========================================")
        for key in user_details["user"]:
            print(f'{key} : {user_details["user"][key]}')
        print('\n')
        print("------------------------")
        print("Organization")
        print("------------------------")
        print(f'name : {user_details["org"]["name"]}')
        print(f'id : {user_details["org"]["id"]}')
        print('\n')
        print("------------------------")
        print("Tickets")
        print("------------------------")
        for ticket in user_details["tickets"]:
            print(f'{ticket["subject"]} [STATUS :{ticket["status"].upper()}]')
        print('\n')

def pretty_print_tickets(tickets_users_orgs):
    for ticket_details in tickets_users_orgs:
        print("==========================================")
        print("TICKET")
        print("==========================================")
        for key in ticket_details["ticket"]:
            print(f'{key} : {ticket_details["ticket"][key]}')
        print('\n')
        print("------------------------")
        print("User")
        print("------------------------")
        print(f'id: {ticket_details["user"]["id"]}')
        print(f'name: {ticket_details["user"]["name"]}')
        print('\n')
        print("------------------------")
        print("Organization")
        print("------------------------")
        print(f'id: {ticket_details["org"]["id"]}')
        print(f'name: {ticket_details["org"]["name"]}')
        print('\n')

def pretty_print_orgs(orgs_users_tickets):
    for org_details in orgs_users_tickets:
        print("==========================================")
        print("ORGANIZATIONS")
        print("==========================================")
        for key in org_details["org"]:
            print(f'{key} : {org_details["org"][key]}')
        print('\n')
        print("------------------------")
        print("Users")
        print("------------------------")
        for user in org_details["users"]:
            print(f'id: {user["id"]}, name: {user["name"]}')
        print('\n')
        print("------------------------")
        print("Tickets")
        print("------------------------")
        for ticket in org_details["tickets"]:
            print(f'{ticket["subject"]} [STATUS: {ticket["status"].upper()}]')
        print('\n')

