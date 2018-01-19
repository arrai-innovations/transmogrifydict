# transmogrifydict

The "map a dict from one API into a dict for another" python module.

![That dict is so cool...](/transmogrifydict.png)

| Python | Branch | Build Status | Coverage Status |
| ------ | ------ | ------------ | --------------- |
| 2 | master | [![Python 2 Build Status](https://semaphoreci.com/api/v1/emergence/transmogrifydict-py2/branches/master/shields_badge.svg)](https://semaphoreci.com/emergence/transmogrifydict-py2/branches/master) | [![Python 2 Coverage](https://docs.emergence.com/transmogrifydict/htmlcov_py2_master/coverage.svg)](https://docs.emergence.com/transmogrifydict/htmlcov_py2_master/) |
| 2 | develop | [![Python 2 Build Status](https://semaphoreci.com/api/v1/emergence/transmogrifydict-py2/branches/develop/shields_badge.svg)](https://semaphoreci.com/emergence/transmogrifydict-py2/branches/develop) | [![Python 2 Coverage](https://docs.emergence.com/transmogrifydict/htmlcov_py2_develop/coverage.svg)](https://docs.emergence.com/transmogrifydict/htmlcov_py2_develop/) |
| 3 | master | [![Python 3 Build Status](https://semaphoreci.com/api/v1/emergence/transmogrifydict-py3/branches/master/shields_badge.svg)](https://semaphoreci.com/emergence/transmogrifydict-py3/branches/master) | [![Python 3 Coverage](https://docs.emergence.com/transmogrifydict/htmlcov_py3_master/coverage.svg)](https://docs.emergence.com/transmogrifydict/htmlcov_py3_master/) |
| 3 | develop | [![Python 3 Build Status](https://semaphoreci.com/api/v1/emergence/transmogrifydict-py3/branches/develop/shields_badge.svg)](https://semaphoreci.com/emergence/transmogrifydict-py3/branches/develop) | [![Python 3 Coverage](https://docs.emergence.com/transmogrifydict/htmlcov_py3_develop/coverage.svg)](https://docs.emergence.com/transmogrifydict/htmlcov_py3_develop/) |

## methods

* `resolve_path_to_value(source, path)` - fetch a value out of `source` using `path` as the pointer to the desired value. see docstring for path string formats.
* `resolve_mapping_to_dict(mapping, source)` - move values from `source` into a returned dict, using `mapping` for paths and returned keys.  see `resolve_path_to_value`'s docstring for path string formats.
