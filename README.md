# transmogrifydict

The "turn a dict from one API into a dict for another" python module.

![That dict is so cool...](/transmogrifydict.png)

Py2: [![Python 2 Build Status](https://semaphoreci.com/api/v1/emergence/transmogrifydict-py2/branches/master/badge.svg)](https://semaphoreci.com/emergence/transmogrifydict-py2)
Py3: [![Python 3 Build Status](https://semaphoreci.com/api/v1/emergence/transmogrifydict-py3/branches/master/badge.svg)](https://semaphoreci.com/emergence/transmogrifydict-py3)

## methods

* `resolve_path_to_value(source, path)` - fetch a value out of `source` using `path` as the pointer to the desired value. see docstring for path string formats.
* `resolve_mapping_to_dict(mapping, source)` - move values from `source` into a returned dict, using `mapping` for paths and returned keys.  see `resolve_path_to_value`'s docstring for path string formats.
