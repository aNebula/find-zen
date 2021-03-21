# findzen

[python]: https://www.python.org/downloads/
[python-badge]: https://img.shields.io/badge/python-v3.6+-blue.svg
[![Test](https://github.com/aNebula/findzen/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/aNebula/findzen/actions/workflows/test.yml)
[![Python Compatibility][python-badge]][python]


A simple search cli for user, organisation and ticket data.

## Install
```
pip install .
```

## Usage

`findzen --help` will show instructions on usage.

### There are 2 steps to use findzen:
1. Load data for search - this creates indexes and caches them. Takes path to data directory as input. Data directory must contain `Users.json`, `Organizations.json` and `Tickets.json` files.

    ```
    findzen load ./data_dir
    ```
2. Search for desired User or Organisation or Ticket. Only one entity can be searched by only one field each time. If found, the other associated entities are also returned. To search, use `findzen` followed by type of entity to search, either `user` or `organization` or `ticket` followed by field name to search by `--field_name`, followed by value. e.g.
    ```
    findzen user --id 1
    findzen organization --tags Fulton
    findzen ticket --status hold
    ```

To search with empty values use quotes `finezen organization --details ''`

To see the available fields to search by, use `findzen <command> -h`. e.g
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
A build pipeline is setup to run test on code push.


