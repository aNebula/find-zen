from findzen.file_handler import CacheHandler


def search_cache(entity_type, field, queries):
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

    return results


def flatten_list(_list):
    flat_list = []
    for sublist in _list:
        if sublist is not None:
            for item in sublist:
                flat_list.append(item)
    return flat_list


def append_or_create(dict, key, value):
    if key in dict:
        dict[key].append(value)
        return dict
    dict[key] = [value]
    return dict

def fetch_if_key(dictionary, key):
    if str(key) in dictionary:
        return dictionary[str(key)]
    else:
        return []
