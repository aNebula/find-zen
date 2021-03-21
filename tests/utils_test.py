"""Tests for findzen.utils modules."""
from findzen.utils import search_cache
from unittest import mock
import pytest


def test_search_cache() -> None:
    """Test the search_cache method."""

    one_item = {'1': ['item1'], '200': ['item99']}
    two_items = {'1': ['item1', 'item2'], '200': ['item99']}
    no_item = {'300': ['item1', 'item2'], '200': ['item99']}

    # happy path - 1 item found
    with mock.patch('findzen.file_handler.CacheHandler.read_cache',
                    return_value=one_item):
        item = search_cache('user', 'id', ['1'])
        assert item == one_item['1']

    # happy path - multiple items found from 1 query
    with mock.patch('findzen.file_handler.CacheHandler.read_cache',
                    return_value=two_items):
        item = search_cache('user', 'id', ['1'])
        assert item == two_items['1']

    # happy path - multiple items found from multiple query
    with mock.patch('findzen.file_handler.CacheHandler.read_cache',
                    return_value=two_items):
        item = search_cache('user', 'id', ['1', '200'])
        assert item == two_items['1'] + two_items['200']

    # happy path - item not found
    with mock.patch('findzen.file_handler.CacheHandler.read_cache',
                    return_value=two_items):
        item = search_cache('user', 'id', ['900', '999'])
        assert item == []

    # happy path - query is not an array or is empty
    with mock.patch('findzen.file_handler.CacheHandler.read_cache',
                    return_value=two_items):
        item = search_cache('user', 'id', [])
        assert item == []

    with mock.patch('findzen.file_handler.CacheHandler.read_cache',
                    return_value=two_items):
        item = search_cache('user', 'id', 'fake')
        assert item == []

    # unhappy path - cache does not exist
    with mock.patch('findzen.file_handler.CacheHandler.read_cache',
                    return_value=two_items) as cache_miss:
        cache_miss.side_effect = FileNotFoundError(
            'This particular data and/or field has not been loaded. Load data first using `load` command'
        )
        with pytest.raises(FileNotFoundError):
            item = search_cache('user', 'id', 'fake')
