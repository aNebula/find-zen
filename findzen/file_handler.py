"""Loads data from files into memory."""

from findzen.models.org import Organization, Organizations
from findzen.models.user import User, Users
from findzen.models.ticket import Ticket, Tickets
from pathlib import Path
import json
import pickle

class JsonHandler():

    def __init__(self):
        self.file_type = 'json'
    
    @classmethod
    def write(self, file: Path, data: dict):
        with file.open('w') as f:
            json.dump(data, f)
    
    @classmethod
    def read(self, file: Path):
        with file.open('r') as f:
            return json.load(f)

class PickleHandler():

    def __init__(self):
        self.file_type = 'pickle'

    @classmethod
    def read(self, file: Path):
        with file.open('rb') as f:
            return pickle.load(f)

    @classmethod
    def write(self, file:Path, obj: dict):
        with file.open('wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

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


class CacheHandler():
    def __init__(self):
        self.cache_dir = Path("./.findzen_cache")
        self.cache_handler = PickleHandler()

    def _cache_type_to_filename(self, type: str) -> Path:
        return (self.cache_dir / f'{type}.pickle')

    def write_cache(self, obj: dict):
        if self.cache_dir.exists() == False:
            self.cache_dir.mkdir()

        for cache_type in obj:
            filename = self._cache_type_to_filename(cache_type)
            self.cache_handler.write(filename, obj[cache_type])

    def read_cache(self, type: str):
        if self.cache_dir.exists() == False:
            raise FileNotFoundError(f'Cache does not exist. Load data first using `load` command.')
        filename = self._cache_type_to_filename(type)
        if filename.exists() == False:
            raise FileNotFoundError(f'This particular data and/or field has not been loaded. Load data first using `load` command')
        
        return self.cache_handler.read(filename)

    


        
