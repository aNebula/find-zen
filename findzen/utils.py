"""Utility functions for findzen."""
from findzen.file_handler import CacheHandler
from typing import Any


def search_cache(entity_type: str, field: str, queries: list) -> list:
    """
    Given a entity type(user, organization or ticket), field to query and a list of queries,
    this function loads the appropriate cache and returns a list of items found in the cache.
    """
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

    return flatten_list(results)


def flatten_list(_list: list) -> list:
    """Flatten nested list, if found in the list. NoneType objects are removed."""
    flat_list = []
    for sublist in _list:
        if sublist is not None:
            if type(sublist) == list:
                for item in sublist:
                    flat_list.append(item)
            else:
                flat_list.append(sublist)
    return flat_list


def append_or_create(dictionary: dict, key: str, value: Any) -> dict:
    """Add [value] to the dictionary by key. If key already exists, append the value to the list under the key."""
    if key in dictionary:
        dictionary[key].append(value)
        return dictionary
    dictionary[key] = [value]
    return dictionary

def fetch_if_key(dictionary, key) -> list:
    """Check if key exists in dictionary. If exists return [value], else return empty list."""
    if str(key) in dictionary:
        return dictionary[str(key)]
    else:
        return []

def sanitize_argument(arg: str) -> str:
    """Sanitize cli arguments. Currently it sanitizes boolean arguments to match cache data format."""
    if arg.lower() == "false":
        return "False"
    elif arg.lower() == "true":
        return "True"
    else:
        return arg
