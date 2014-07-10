# transmogrifydict

The "turn a dict from one API into a dict for another" python module.

## methods

* `resolve\_path\_to\_value(source, path)` - fetch a value out of `source` using `path` as the pointer to the desired value. see docstring for path string formats.
* `resolve\_mapping\_to\_dict(mapping, source)` - turn the source into the destination using the mapping. see `resolve\_path\_to\_value`'s docstring for path string formats.
