from findzen.commands.load_data import LoadDataCmd
import argparse
from findzen.file_handler import CacheHandler
from findzen.models.user import User
from findzen.models.org import Organization
from findzen.models.ticket import Ticket

def test_load_data_run(tmp_cwd, sample_data_dir):

    ldc = LoadDataCmd()
    args = argparse.Namespace(name="load", path=sample_data_dir)

    ldc._run(args)

    # read cache to find out if data written is correct

    ch = CacheHandler()

    for key in User.__fields__:
        index_name = f'user_index_by_{key}'
        # check no error is thrown for reading any of the cache files
        assert ch.read_cache(index_name)
   
    for key in Ticket.__fields__:
        index_name = f'ticket_index_by_{key}'
        # check no error is thrown for reading any of the cache files
        assert ch.read_cache(index_name) 

    for key in Organization.__fields__:
        index_name = f'Organization_index_by_{key}'
        # check no error is thrown for any of the cache files
        assert ch.read_cache(index_name)

    user_by_id = ch.read_cache('user_index_by_id')

    assert user_by_id["1"]["name"] == 'John Doe'
    assert user_by_id["1"]["tickets"][0]["description"] == "description1"

