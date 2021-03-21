"""Module provides handler classes to load/dump data between disk and memory."""

from findzen.models.org import Organization, Organizations
from findzen.models.user import User, Users
from findzen.models.ticket import Ticket, Tickets
from pathlib import Path
import json
import pickle


class JsonHandler():
    """Handler of JSON files."""
    def __init__(self):
        self.file_type = 'json'
    
    @classmethod
    def write(self, file: Path, data: dict) -> None:
        """Write JSON file."""
        with file.open('w') as f:
            json.dump(data, f)
    
    @classmethod
    def read(self, file: Path) -> dict:
        """Read JSON file from given file."""
        with file.open('r') as f:
            return json.load(f)

class PickleHandler():
    """Handler class for Pickle type files."""
    def __init__(self):
        self.file_type = 'pickle'

    @classmethod
    def read(self, file: Path) -> dict:
        """Read pickle file."""
        with file.open('rb') as f:
            return pickle.load(f)

    @classmethod
    def write(self, file:Path, obj: dict) -> None:
        """Write pickle file."""
        with file.open('wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

class DataLoader():
    """Class to load search data from disk to memory."""
    def __init__(self, file_type: str, data_dir: Path):
        """
        Constructor for DataLoader. Takes type of file_type (currently only 'json' is implemented) and
        path to data directory that contains users.json, organizations.json and tickets.json file.
        """
        if file_type=='json':
            self.file_type = 'json'
            self.file_handler = JsonHandler()
        else:
            raise NotImplementedError('File handler for this type is not yet implemented')
        
        self.users_file = data_dir / f'users.{self.file_type}'
        self.orgs_file = data_dir / f'organizations.{self.file_type}'
        self.tickets_file = data_dir / f'tickets.{self.file_type}'

        self._check_required_files_exist()


    def _check_required_files_exist(self) -> None:
        """Check if the required data files are present in the data directory."""
        if self.users_file.exists()== False:
            raise FileNotFoundError(f'Users data not found at {self.users_file}')
        if self.orgs_file.exists() == False:
            raise FileNotFoundError(f'Organizations data not found at {self.orgs_file}')
        if self.tickets_file.exists() == False:
            raise FileNotFoundError(f'Tickets data not found at {self.tickets_file}')

    def load(self) -> (Users, Organizations, Tickets):
        """Load data from disk. Return a tuple of Users, Organizations, Tickets."""
        users = Users.parse_obj(self.file_handler.read(self.users_file))
        orgs = Organizations.parse_obj(self.file_handler.read(self.orgs_file))
        tickets = Tickets.parse_obj(self.file_handler.read(self.tickets_file))
        
        return users, orgs, tickets


class CacheHandler():
    """Handler of cache files. Currently using only pickle type."""
    def __init__(self):
        """Constructure for CacheHandler. Declares caching directory."""
        self.cache_dir = Path('./.findzen_cache')
        self.cache_handler = PickleHandler()

    def _cache_type_to_filename(self, type: str) -> Path:
        """Return file path to cache directory, given a cache type."""
        return (self.cache_dir / f'{type}.pickle')

    def write_cache(self, obj: dict) -> None:
        """Write cache to cache directory."""
        if self.cache_dir.exists() == False:
            self.cache_dir.mkdir()

        for cache_type in obj:
            filename = self._cache_type_to_filename(cache_type)
            self.cache_handler.write(filename, obj[cache_type])

    def read_cache(self, type: str) -> dict:
        """Given cache type, load cache from cache directory to memory."""
        if self.cache_dir.exists() == False:
            raise FileNotFoundError('Cache does not exist. Load data first using `load` command.')
        filename = self._cache_type_to_filename(type)
        if filename.exists() == False:
            raise FileNotFoundError('This particular data and/or field has not been loaded. Load data first using `load` command.')
        
        return self.cache_handler.read(filename)

    


        
