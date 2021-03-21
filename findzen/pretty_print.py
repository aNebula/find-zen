"""Module for printing results out to command line with formatting."""

def pretty_print_users(users_orgs_tickets: dict) -> None:
    """Format and print Users and associated Organizations and Tickets"""
    for user_details in users_orgs_tickets:
        print('==========================================')
        print('USER')
        print('==========================================')
        for key in user_details:
            if key == 'organization' or key == 'tickets':
                continue
            print(f'{key} : {user_details[key]}')
        print('\n')
        print('------------------------')
        print('Organization')
        print('------------------------')
        if len(user_details['organization']) < 1:
            print('No Organisation found.')
        else:
            print(f'name : {user_details["organization"]["name"]}')
            print(f'id : {user_details["organization"]["id"]}')
        print('\n')
        print('------------------------')
        print('Tickets')
        print('------------------------')
        if len(user_details['tickets']) < 1:
            print('No Tickets found.')
        else:
            for ticket in user_details['tickets']:
                print(f'{ticket["subject"]} [STATUS :{ticket["status"].upper()}]')
        print('\n')


def pretty_print_tickets(tickets_users_orgs:dict) -> None:
    """Format and print found Tickets with associated User and Organizations."""
    for ticket_details in tickets_users_orgs:
        # for each ticket
        print('==========================================')
        print('TICKET')
        print('==========================================')
        for key in ticket_details:
            if key == 'user' or key == 'organization':
                continue
            print(f'{key} : {ticket_details[key]}')
        print('\n')
        print('------------------------')
        print('User')
        print('------------------------')
        if len(ticket_details['user'])<1:
            print('Submitter/User not found.')
        else:
            print(f'id: {ticket_details["user"]["id"]}')
            print(f'name: {ticket_details["user"]["name"]}')
        print('\n')
        print('------------------------')
        print('Organization')
        print('------------------------')
        if len(ticket_details['organization']) <1 :
            print('Organization not found.')
        else:
            print(f'id: {ticket_details["organization"]["id"]}')
            print(f'name: {ticket_details["organization"]["name"]}')
        print('\n')


def pretty_print_orgs(orgs_users_tickets: dict) -> None:
    """Format and print found Organizations with associated Users and Tickets."""
    for org_details in orgs_users_tickets:
        print('==========================================')
        print('ORGANIZATIONS')
        print('==========================================')
        for key in org_details:
            if key == 'users' or key == 'tickets':
                continue
            print(f'{key} : {org_details[key]}')
        print('\n')
        print('------------------------')
        print('Users')
        print('------------------------')
        if len(org_details['users']) <1:
            print('No Users found.')
        else:
            for user in org_details['users']:
                print(f'id: {user["id"]}, name: {user["name"]}')
        print('\n')
        print('------------------------')
        print('Tickets')
        print('------------------------')
        if len(org_details['tickets']) < 1:
            print('No Tickets found.')
        else:
            for ticket in org_details['tickets']:
                print(f'{ticket["subject"]} [STATUS: {ticket["status"].upper()}]')
        print('\n')

