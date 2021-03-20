def append_or_create(dict, key, value):
    if key in dict:
        dict[key].append(value)
        return dict
    dict[key] = [value]
    return dict

def index_builder(data, data_type):
    all_indexes = {}
    key_prefix = f'{data_type.__name__.lower()}_index_by_'
    for key in data_type.__fields__:
        all_indexes[f'{key_prefix}{key}']= {}

    for entry in data.dict()["__root__"]:
        for key in data_type.__fields__:
            key_string = f'{key_prefix}{key}'
            if key == "id":
                all_indexes[key_string][str(entry[key])] =  entry
                continue
            if key == "tags":
                for tag in entry["tags"]:
                    all_indexes[key_string]=  append_or_create(all_indexes[key_string], str(tag), entry["id"])
                continue
            if key == "domain_names":
                for domain_name in entry["domain_names"]:
                    all_indexes[key_string]=  append_or_create(all_indexes[key_string], str(domain_name), entry["id"])
                continue

            all_indexes[key_string]= append_or_create(all_indexes[key_string], str(entry[key]), entry["id"])
    
    return all_indexes