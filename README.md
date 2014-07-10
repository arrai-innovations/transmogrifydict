# transmogrifydict

The "turn a dict from one API into a dict for another" python module.

## methods

* `resolve_path_to_value(source, path)` - fetch a value out of `source` using `path` as the pointer to the desired value. see docstring for path string formats.
* `resolve_mapping_to_dict(mapping, source)` - turn the source into the destination using the mapping. see `resolve_path_to_value`'s docstring for path string formats.
