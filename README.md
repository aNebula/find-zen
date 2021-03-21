# findzen

[python]: https://www.python.org/downloads/
[python-badge]: https://img.shields.io/badge/python-v3.6+-blue.svg
[![Test](https://github.com/aNebula/findzen/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/aNebula/findzen/actions/workflows/test.yml)
[![Python Compatibility][python-badge]][python]


A simple search cli for user, organisation and ticket data.

## Install
------------
To run `findzen`, you need to have `python3.8` installed.
```
pip install .
```


## Usage

`findzen --help` will show instructions on usage.

### There are 2 steps to use findzen:
1. **Load data** for search (mandetory first step)- this creates indexes and caches them. Takes path to data directory as input. Data directory must contain `Users.json`, `Organizations.json` and `Tickets.json` files.

    ```
    findzen load ./data_dir
    ```
    Note that you can not search before data have been indexed. Finzen will prompt you to load data first.

    **IF DATA FILES ARE UPDATED, DATA MUST BE RELOADED TO SEARCH THE UPDATED DATA.**

    This is because on load `findzen` indexes and caches data for faster search. Unless new data is reloaded and new indexes are cached, findzen will continue to return search results on the last loaded version of data.

2. **Search** for desired entity: `user` or `organization` or `ticket`. You can only search for **one entity at a time**, using only **one field** each time. If match is found, the other associated entities are also returned. 

    To search, use `findzen` followed by type of entity to search(`user`| `organization` | `ticket`), followed by field name to search by `--{field_name}`, followed by `{value}`. For example:
    ```
    findzen user --id 1
    findzen organization --tags Fulton
    findzen ticket --status hold
    ```

To search with empty values use quotes `finezen organization --details ''`

To see the full list of available fields to search by, use `findzen <command> -h`. e.g
```
findzen user -h
findzen organization -h
findzen ticket -h
```


## Test
Findzen implements tests with `pytest` library. To run all the tests first install [dev] dependencies and then run pytest:
```
$ pip install ".[dev]"
$ pytest .
```
A GitHub Actions build pipeline is setup to run test on code push.

------------
<br>
<br>

## Design Decisions

> Search performance was the top priority while building this tool.

### Use indexing and caching to achieve O(1) time complexity search.

    The requirements was search to be better than O(n). 
    
    User should be able to search by any field. 
    
    Source data was provided in 3 arrays.

1. There are 2 ways to achieve better than linear time search: binary search of sorted array (O(logn)), or indexing by fields (O(1)). 
    
| Binary Search                                                                                                                                                                                                                       | Indexing                                                                                                                                                   | 
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Arrays of entities needs to be sorted. Sorting an array of n items is O(nlogn).                                                                                                                                                     | Index needs to be created for constant time search using hashmap, which is O(n) |   |   |   |
| To allow faster than linear time look up, by each field, 1 array needs to be cloned per field, with the field as key, and sorted. For a dataset with m fields, m arrays need to be cloned and sorted, leading to total O(m nlogn).  | For search by each field, data needs to be indexed by each field. 1 index can map id to data, while others map a field value to id. Indexing by each fields of size m still takes O(mn).                                                                                                                 |
| Look up is O(logn).                                                                                                                                                                                                                 | Look up is **O(1)**.                                                                                                                                       |

2. For both the methods, having to sort an array or craete an index right before the search pushes time complexity beyond O(n). The way to do better than that, is to **cache** the sorted array or the index before search. The cache is built only once on a dataset. From there onwards, searching is either O(n) or O(1).

3. **Since indexing is faster to both build and search, I chose to index the data.** A primary index mapped id (e.g `user_id_1` ) to the object with the id (e.g. the `user` object). At the same time secondary indexes on each field of the objects were created - these mapped field values to id of the objects with that field value. (e.g for field `role` "admin" -> `user_ids` [1,5,8,34] ).

4. Secondary indexes by fields are stored in separate files. This allows loading only the required index file for better performance.

5. `Pickle` serialization is used over `json`/`text`/`csv` for faster access to cache.

6. Each objects of primary entity (user/organisation/ticket) was then populated with associated secondary entities. For example, a user in cache holds organisation and ticket objects associated with that particular user. This allows fast constant time search, e.g. `user_role` -> `user_id` -> `user` -> `organisation` and `ticket`

7. Python `dictionary` data structure was used for indexes as it is implemented using HashMap. Search and access is O(1).

### Forcing user to load data before 1st search
1. This allows configurability. Instead of expecting data to be in a certain directory, user can now provide path to where data lives.
2. Explicit update of index and cache on user command. This keeps the app simple and transparent to the user. Alternatie option would be to store checksum of the data in the data directory and trigger rebuild of index and cache on detection of data update during search time.

### Using non-interactive shell
Allows automating large number of queries.

### Search only by 1 field and 1 value
Keep the app simple.

### Missing field value != ""
Where fields are optional and value is not present, e.g. a User might or might not have an Organisation, absence of an optional field and value is NOT equal to having empty value of "".

### Search with --tags allows searching with only 1 tag.
Keep the app simple.



## Assumptions

1. Search is only by full match. 'mar' != 'marry'. All the data fits in memory, so the cache should always fit in memory.
2. Search is case sensetive.
3. Only the tickets submitted by a user (`user.id` == `ticket.submitter_id`) are included in the result with the user.
3. A User may belong to only 1 Organization or no Organizations at all, but can not belong to multiple Organizations. A User can have multiple tickets.
4. An organisation can have many users and many tickets.
5. A Ticket must belong to only 1 submitter. A ticket can only belong to 1 Organization or no organizations, but can not belogn to multiple organisations.
