import pytest
import pickle
from findzen.file_handler import JsonHandler, PickleHandler, DataLoader, CacheHandler
from findzen.models.user import Users
from findzen.models.org import Organizations
from findzen.models.ticket import Tickets


def test_json_handler(tmp_path):
    """Test JsonHandler class with read, write."""

    expected_data = {
        "a" : 1,
        "b" : "cd"
    }
    filename = tmp_path / 'test.json'
    JsonHandler.write(filename, expected_data)

    actual_data = JsonHandler.read(filename)
    assert actual_data["a"] == expected_data["a"]
    assert actual_data["b"] == expected_data["b"]


def test_pickle_handler(tmp_path):
    """Test PickleHandler class with read, write."""
    expected_data = {
        "a" : 1,
        "b" : "cd"
    }
    filename = tmp_path / 'test.json'
    ph = PickleHandler()
    ph.write(filename, expected_data)

    actual_data = ph.read(filename)

    assert actual_data["a"] == expected_data["a"]
    assert actual_data["b"] == expected_data["b"]


def test_data_loader(sample_data_dir, sample_users, sample_orgs, sample_tickets):
    """Test DataLoader class, by loading User, Organization and Tickets data."""

    dl = DataLoader('json', sample_data_dir)

    users, orgs, tickets = dl.load()

    assert type(users)== Users
    assert users == Users.parse_obj(sample_users)

    assert type(orgs)== Organizations
    assert orgs == Organizations.parse_obj(sample_orgs)

    assert type(tickets)== Tickets
    assert tickets == Tickets.parse_obj(sample_tickets)

def test_data_loader_fail(tmp_path):
    """Test DataLoader will fail if the data files do not exist."""
    with pytest.raises(FileNotFoundError):
        dl = DataLoader('json', tmp_path)



def test_cache_writer(tmp_cwd, sample_users):
    """Test CacheHandlers write method."""
    expected_cache_filename = tmp_cwd / f'.findzen_cache/test_cache.pickle'
    ch = CacheHandler()
    assert not expected_cache_filename.exists()
    assert not ch.cache_dir.exists()
    ch.write_cache({'test_cache': sample_users})
    assert expected_cache_filename.exists()
    assert ch.cache_dir.exists()

    with expected_cache_filename.open('rb') as f:
        actual_cache = pickle.load(f)

    assert Users.parse_obj(sample_users) == Users.parse_obj(actual_cache)


def test_cache_reader(tmp_cwd, sample_users):
    """Test CacheHandlers read method."""
    cache_dir = tmp_cwd / f'.findzen_cache'
    cache_dir.mkdir()
    cache_filename = cache_dir / f'test_cache.pickle'
    with cache_filename.open('wb') as f:
        pickle.dump(sample_users, f, pickle.HIGHEST_PROTOCOL)

    actual_cache = CacheHandler().read_cache('test_cache')

    assert Users.parse_obj(sample_users) == Users.parse_obj(actual_cache)

    






