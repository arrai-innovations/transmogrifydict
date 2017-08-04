# transmogrifydict

The "turn a dict from one API into a dict for another" python module.

![That dict is so cool...](/transmogrifydict.png)

## methods

* `resolve_path_to_value(source, path)` - fetch a value out of `source` using `path` as the pointer to the desired value. see docstring for path string formats.
* `resolve_mapping_to_dict(mapping, source)` - move values from `source` into a returned dict, using `mapping` for paths and returned keys.  see `resolve_path_to_value`'s docstring for path string formats.
