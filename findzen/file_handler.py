"""Loads data from files into memory."""

from models.org import Organization, Organizations
from models.user import User, Users
from models.ticket import Ticket, Tickets
from pathlib import Path
import json

class JsonHandler():

    def __init__(self):
        self.file_type = 'json'

    @classmethod
    def read(self, file: Path):
        with file.open('r') as f:
            return json.load(f)

    @classmethod #TODO
    def writer(self, file: Path):
        pass


class DataLoader():

    def __init__(self, file_type: str, data_dir: Path):
        if file_type=="json":
            self.file_type = 'json'
            self.file_handler = JsonHandler()
        else:
            raise NotImplementedError("File handler for this type is not yet implemented")
        
        self.users_file = data_dir / f'users.{self.file_type}'
        self.orgs_file = data_dir / f'organizations.{self.file_type}'
        self.tickets_file = data_dir / f'tickets.{self.file_type}'

        self._check_required_files_exist()


    def _check_required_files_exist(self):
        if self.users_file.exists()== False:
            raise FileNotFoundError(f'Users data not found at {self.users_file}')
        if self.orgs_file.exists() == False:
            raise FileNotFoundError(f'Organizations data not found at {self.orgs_file}')
        if self.tickets_file.exists() == False:
            raise FileNotFoundError(f'Tickets data not found at {self.tickets_file}')

    def load(self) -> (Users, Organizations, Tickets):
        users = Users.parse_obj(self.file_handler.read(self.users_file))
        orgs = Organizations.parse_obj(self.file_handler.read(self.orgs_file))
        tickets = Tickets.parse_obj(self.file_handler.read(self.tickets_file))
        
        return users, orgs, tickets


        
