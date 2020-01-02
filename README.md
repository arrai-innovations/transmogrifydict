# transmogrifydict

The "map a dict from one API into a dict for another" python module.

![That dict is so cool...](https://docs.arrai-dev.com/transmogrifydict/transmogrifydict.png)

###### master

![Tests](https://docs.arrai-dev.com/transmogrifydict/master.python38.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/master.python38.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_master_python38/)

![Tests](https://docs.arrai-dev.com/transmogrifydict/master.python37.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/master.python37.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_master_python37/)

![Tests](https://docs.arrai-dev.com/transmogrifydict/master.python36.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/master.python36.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_master_python36/)

![Tests](https://docs.arrai-dev.com/transmogrifydict/master.python35.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/master.python35.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_master_python35/)

![Tests](https://docs.arrai-dev.com/transmogrifydict/master.python27.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/master.python27.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_master_python27/)

![Flake8](https://docs.arrai-dev.com/transmogrifydict/master.flake8.svg)

###### develop

![Tests](https://docs.arrai-dev.com/transmogrifydict/develop.python38.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/develop.python38.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_develop_python38/)

![Tests](https://docs.arrai-dev.com/transmogrifydict/develop.python37.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/develop.python37.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_develop_python37/)

![Tests](https://docs.arrai-dev.com/transmogrifydict/develop.python36.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/develop.python36.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_develop_python36/)

![Tests](https://docs.arrai-dev.com/transmogrifydict/develop.python35.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/develop.python35.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_develop_python35/)

![Tests](https://docs.arrai-dev.com/transmogrifydict/develop.python27.svg) [![Coverage](https://docs.arrai-dev.com/transmogrifydict/develop.python27.coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_develop_python27/)

![Flake8](https://docs.arrai-dev.com/transmogrifydict/develop.flake8.svg)


## methods

*   `resolve_mapping_to_dict(mapping, source)` - move values from `source` into a returned dict, using `mapping` for paths and returned keys.

    ```python
    from transmogrifydict import resolve_mapping_to_dict

    mapping = {
        'a': 'd',
        'b': 'e',
        'c': 'f'
    }

    source = {
        'd': 1,
        'e': 2,
        'f': 3
    }

    resolve_mapping_to_dict(mapping, source)
    # {
    #     'a': 1,
    #     'b': 2,
    #     'c': 3,
    # }
    ```

*   `resolve_path_to_value(source, path)` - fetch a value out of `source` using `path` as the pointer to the desired value. see docstring for path string formats.

    ```python
    from transmogrifydict import resolve_path_to_value

    source = {
        'd': 1,
        'e': 2,
        'f': 3
    }

    found, value = resolve_path_to_value(source, 'e')

    print((found, value))
    # (True, 2)
    ```

## `path` or `mapping` value format
```python
from transmogrifydict import resolve_path_to_value

source = {
    'some-key': {
        'another-key': '123'
    }
}

# dot notation can be used to descend into dictionaries.
resolve_path_to_value(source, 'some-key.another-key')
# (True, '123')

source = {
    'some-key': '{"another-key":"123"}'
}

# dot notation can also be used to descend into json strings that are dictionary like
resolve_path_to_value(source, 'some-key.another-key')
# (True, '123')

source = {
    'some-key': {
        'another-key': ['1', '2', '3']
    }
}

# square brackets can be used to get specific indexes from a list
resolve_path_to_value(source, 'some-key.another-key[1]')
# (True, '2')

source = {
    'some-key': {
        'another-key': [
            {
                'filter-key': 'yeah',
                'each-key': 'a',
            },
            {
                'filter-key': 'yeah',
                'each-key': 'b',
            },
            {
                'filter-key': 'nah',
                'each-key': 'c',
            }
        ]
    }
}

# dot notation can be used after square brackets if the list contains dict-like values
resolve_path_to_value(source, 'some-key.another-key[1].each-key')
# (True, ['b']) 

# square brackets can be used to iterate over arrays to descend into the items
resolve_path_to_value(source, 'some-key.another-key[].each-key')
# (True, ['a', 'b', 'c'])

# when iterating over a list, a filter can be applied using [key=value]
resolve_path_to_value(source, 'some-key.another-key[filter-key=yeah].each-key')
# (True, ['a', 'b'])

source = {
    'a-key': [
        {
            'b-key': {
                'c-key': 1,
                'd-key': 2,
            }
        },
        {
            'b-key': {
                'c-key': 1,
                'd-key': 3,
            }
        },
        {
            'b-key': {
                'c-key': 0,
                'd-key': 4,
            }
        }
    ]
}
# tidle notation can be used to filter on sub keys of dict list items.
resolve_path_to_value(source, 'a-key[b-key~c-key=1].b-key.d-key')
# (True, [2, 3, 4])
# 
```
