def resolve_path_to_value(source, path):
    """
    fetch a value out of `source` using `path` as the pointer to the desired value.

    a `path` should be in one of or a combination of the following formats:
    - dictionary keys using dot notation
      key.subkey
    - array item using square bracket notation
      key[0]
    - find dict in array using keys
      key[Key=Value]
    - find dict in array using sub keys
      key[Key~SubKey=Value]

    example:
    >>> source_dict = {
    ...     'first_key': 'a',
    ...     'second_key' : [
    ...         'x',
    ...         'y',
    ...         'z',
    ...     ],
    ...     'third_key' : [
    ...         {
    ...             'b': 1,
    ...             'c': 2
    ...         },
    ...         {
    ...             'b': 3,
    ...             'c': 4
    ...         }
    ...     ],
    ...     'fourth_key': [
    ...         {
    ...             'd': {
    ...                 'f': 5,
    ...                 'g': 6
    ...             },
    ...             'e': {
    ...                 'f': 7,
    ...                 'g': 8
    ...             }
    ...         },
    ...         {
    ...             'd': {
    ...                 'f': 9,
    ...                 'g': 10
    ...             },
    ...             'e': {
    ...                 'f': 11,
    ...                 'g': 12
    ...             }
    ...         }
    ...     ]
    ... }
    >>> resolve_path_to_value(source_dict, 'first_key')
    'a'
    >>> resolve_path_to_value(source_dict, 'second_key[1]')
    True, 'y'
    >>> resolve_path_to_value(source_dict, 'third_key[b=3]')
    {'c': 2, 'b': 1}
    >>> resolve_path_to_value(source_dict, 'third_key[b=3].c')
    2
    >>> resolve_path_to_value(source_dict, 'fourth_key[d~g=8].d.f')
    7

    :param source: potentially holds the desired value
    :type source: dict
    :param path: points to the desired value
    :type path: str
    :returns: a boolean indicating found status, the value that was found
    :rtype: tuple
    :raises ValueError: if we don't understand what went inside some square brackets.
    """
    mapped_value = source
    found_value = True
    # noinspection PyUnresolvedReferences
    for path_part in path.split('.'):
        parts = path_part.split('[')
        try:
            mapped_value = mapped_value[parts[0]]
        except KeyError:
            found_value = False
            break
        for array_part_raw in parts[1:]:
            array_part = array_part_raw[:-1]
            if array_part.isdigit():
                # [0]
                if hasattr(mapped_value, 'keys'):
                    break
                mapped_value = mapped_value[int(array_part)]
            elif '=' in array_part:
                # [Key=Value] or [Key~SubKey=Value]
                find_key, find_value = array_part.split('=')
                for item in hasattr(mapped_value, 'keys') and [mapped_value] or mapped_value:
                    sub_item = item
                    for sub_key in find_key.split('~'):
                        sub_item = sub_item[sub_key]
                    if sub_item == find_value:
                        mapped_value = item
                        break
                else:
                    # raise KeyError('no item with %r == %r' % (find_key, find_value))
                    found_value = False
                    break
            else:
                raise ValueError('Expected square brackets to have be either "[number]", or "[key=value]" or '
                                 '"[key~subkey=value]". got: %r' % array_part)
        if not found_value:
            break
    return found_value, mapped_value
