# transmogrifydict

The "map a dict from one API into a dict for another" python module.

![That dict is so cool...](/transmogrifydict.png)

| Python | Branch | Build Status | Coverage Status |
| ------ | ------ | ------------ | --------------- |
| 2.7 | master | [![Python 2 Build Status](https://semaphoreci.com/api/v1/arrai-innovations/transmogrifydict-py2/branches/master/shields_badge.svg)](https://semaphoreci.com/arrai-innovations/transmogrifydict-py2/branches/master) | [![Python 2 Coverage](https://docs.arrai-dev.com/transmogrifydict/htmlcov_py2_master/coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_py2_master/) |
| 2.7 | develop | [![Python 2 Build Status](https://semaphoreci.com/api/v1/arrai-innovations/transmogrifydict-py2/branches/develop/shields_badge.svg)](https://semaphoreci.com/arrai-innovations/transmogrifydict-py2/branches/develop) | [![Python 2 Coverage](https://docs.arrai-dev.com/transmogrifydict/htmlcov_py2_develop/coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_py2_develop/) |
| 3.5 | master | [![Python 3 Build Status](https://semaphoreci.com/api/v1/arrai-innovations/transmogrifydict-py3/branches/master/shields_badge.svg)](https://semaphoreci.com/arrai-innovations/transmogrifydict-py3/branches/master) | [![Python 3 Coverage](https://docs.arrai-dev.com/transmogrifydict/htmlcov_py3_master/coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_py3_master/) |
| 3.5 | develop | [![Python 3 Build Status](https://semaphoreci.com/api/v1/arrai-innovations/transmogrifydict-py3/branches/develop/shields_badge.svg)](https://semaphoreci.com/arrai-innovations/transmogrifydict-py3/branches/develop) | [![Python 3 Coverage](https://docs.arrai-dev.com/transmogrifydict/htmlcov_py3_develop/coverage.svg)](https://docs.arrai-dev.com/transmogrifydict/htmlcov_py3_develop/) |

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
