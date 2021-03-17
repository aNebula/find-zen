"""Loads data from files into memory."""

from models.org import Organization, Organizations
from models.user import User, Users
from models.ticket import Ticket, Tickets
from pathlib import Path
import json

class JsonHandler():

    def __init__(self, file: Path):
        self.file_type = 'json'

    @classmethod
    def json_loader(self, file: Path):
        with file.open('r') as f:
            return json.load(f)

    @classmethod #TODO
    def json_writer(self, file: Path):
        pass


class DataLoader():

    def __init__(self):

    def load_jsons(self, data_dir: Path) -> Users, Organizations, Tickets:

        users_file = data_dir / 'users.json'
        orgs_file = data_dir / 'organizations.json'
        tickets_file = data_dir / 'tickets.json'

        if users_file.exist() == False:
            raise FileNotFoundError(f'Users data not found at {users_file}')
        if orgs_file.exist() == False:
            raise FileNotFoundError(f'Organizations data not found at {orgs_file}')
        if tickets_file.exist() == False:
            raise FileNotFoundError(f'Tickets data not found at {tickets_file}')

        users = self._load_users_json(users_file)
        orgs = self._load_orgs_json(orgs_file)
        tickets = self._load_tickets_json(tickets_file)
        
        return users, orgs, tickets

    def _load_users_json(file: path) -> Users:
        user_json = JsonHandler.json_loader(file)
        return Users.parse_obj(user_json)

    def _load_orgs_json(file: path) -> Organizations:
        orgs_json = JsonHandler.json_loader(file)
        return Organizations.parse_obj(orgs_json)

    def _load_tickets_json(file: path) -> Tickets:
        tickets_json = JsonHandler.json_loader(file)
        return Tickets.parse_obj(tickets_json)


        
