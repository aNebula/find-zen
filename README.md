# findzen

[python]: https://www.python.org/downloads/
[python-badge]: https://img.shields.io/badge/python-v3.6+-blue.svg
[![Test](https://github.com/aNebula/findzen/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/aNebula/findzen/actions/workflows/test.yml)
[![Python Compatibility][python-badge]][python]


A simple search cli for user, organisation and ticket data.

## Install
To run `findzen`, you need to have `python3.6` or higher(3.7,3.8,3.9) installed.
```
pip install .
```

## Usage

`findzen --help` will show instructions on usage.

### There are 2 steps to use findzen:
1. Load data for search and is mandetory first step- this creates indexes and caches them. Takes path to data directory as input. Data directory must contain `Users.json`, `Organizations.json` and `Tickets.json` files.

    ```
    findzen load ./data_dir
    ```
    Note that you can not search before data have been indexed. Finzen will prompt you to load data first.

    **IF DATA FILES ARE UPDATED, DATA MUST BE RELOADED TO SEARCH THE UPDATED DATA.**

    This is because on load `findzen` indexes and caches data for faster search. Unless new data is reloaded and new indexes are cached, findzen will continue to return search results on the last loaded version of data.

2. Search for desired entity: `User` or `Organisation` or `Ticket`. You can only search for **one entity at a time**, using only **one field** each time. If match is found, the other associated entities are also returned. 

    To search, use `findzen` followed by type of entity to search, either `user` or `organization` or `ticket`, followed by field name to search by `--{field_name}`, followed by value. e.g.
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
Findzen implements tests with `pytest` library. To run all the tests run
```
$ pytest .
```
A GitHub Actions build pipeline is setup to run test on code push.


## Technical Design Decisions
> Search performance was the top priority while building this tool.

### Use indexing and caching to achieve O(1) time complexity search.

    > The requirements was search to be better than O(n). User should be able to search by any field. Source data was provided in 3 arrays.
    
    There are 2 ways to achieve better than linear time search: binary search of sorted array (O(logn)), or indexing by fields (O(1)). 
    
| Binary Search                                                                                                                                                                                                                       | Indexing                                                                                                                                                   |   |   |   |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|---|---|---|
| Arrays of entities needs to be sorted. Sorting an array of n items is O(nlogn).                                                                                                                                                     | Index needs to be created for contact time search using hashmap, which is O(1) |   |   |   |
| To allow faster than linear time look up by each field 1 array needs to be cloned per field, with they field as key, and sorted. For a dataset with m fields,  m arrays need to be cloned and sorted, leading to total O(m nlogn).  | For search by each field, data needs to be indexed by each field. 1 index can map id to data, while others map a field value to id. Indexing by each fields still takes O(nm).                                                                                                                 |   |   |   |
| Look up is O(logn).                                                                                                                                                                                                                 | Look up is **O(1)**.                                                                                                                                       |   |   |   |


2. For both the methods, having to sort an array or craete an index right before the search pushes time complexity over O(n). The way to do better than that, is to **cache** the sorted array or the index before search. From there onwards, searching is either O(n) or O(1).

3. Since index is faster to both build and search, I chose to index my data.

