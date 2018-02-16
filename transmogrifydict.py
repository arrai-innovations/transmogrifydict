import json
import six
import re

# (?<!\\) - don't match leading slashes
# (?:\\\\)* - allow any even number of slashes
# (\.) - capture the actual separator
PERIOD_SPLIT = re.compile(r'(?<!\\)(?:\\\\)*(\.)')
OPEN_SQUARE_BRACKET_SPLIT = re.compile(r'(?<!\\)(?:\\\\)*(\[)')
EQUAL_SPLIT = re.compile(r'(?<!\\)(?:\\\\)*(=)')
TIDLE_SPLIT = re.compile(r'(?<!\\)(?:\\\\)*(~)')

SINGLE_SLASH = re.compile(r'(?<!\\)(\\)')


def _non_quoted_split(regex, string):
    indices = list(regex.finditer(string))
    retval = []
    for x, y in zip([None]+indices, indices+[None]):
        retval.append(string[x.end(1) if x else 0:y.start(1) if y else None])
    return retval


def _un_slash_escape(string):
    return SINGLE_SLASH.sub('', string).replace('\\\\', '\\')


def resolve_path_to_value(source, path):
    r"""
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

    if the substring `Value` `isdigit()`, we look for an `int` version. You can wrap `'8'` into `'"8"'` to find the
     `string` version.

    examples:
    >>> source_dict = {
    ...     'first_key': 'a',
    ...     'second_key' : ['x', 'y', 'z'],
    ...     'third_key' : [
    ...         {'c': 'asdf'},
    ...         {'b': 3},
    ...         {'b': '5'},
    ...         {'h': 'qw"er'}
    ...     ],
    ...     'fourth_key': [
    ...         {
    ...             'd': {'f': 5, 'g': 6},
    ...             'e': {'f': 7, 'g': 8}
    ...         },
    ...         {
    ...             'd': {'f': 9, 'g': 10},
    ...             'e': {'f': 11, 'g': 12}
    ...         }
    ...     ],
    ...     'fifth_key': [
    ...         {'b.c': '9.a'},
    ...         {'b[c': '9[a'},
    ...         {'b]c': '9]a'},
    ...         {'b\c': '9\\a'},
    ...     ],
    ...     'sixth_key': {
    ...         'a': [
    ...             {'b':6},
    ...             {'b':5},
    ...             {'b':4},
    ...         ],
    ...         'c': [
    ...             {'d':100},
    ...             {'d':{'e': 3}},
    ...             {'d':{'e': 2}},
    ...         ],
    ...         'f': []
    ...     },
    ...     'seventh_key': {
    ...         'bad_api': '{"z":1,"y":2,"x":3}',
    ...         'bad_json': '{"z":1!"y":2,"x":3}',
    ...     }
    ... }
    >>> resolve_path_to_value(source_dict, 'zero_key')[0]
    False
    >>> resolve_path_to_value(source_dict, 'first_key')
    (True, 'a')
    >>> resolve_path_to_value(source_dict, 'second_key[1]')
    (True, 'y')
    >>> resolve_path_to_value(source_dict, 'second_key[4]')
    Traceback (most recent call last):
        ...
    IndexError: index 4 out of range on array at 'second_key'.
    >>> resolve_path_to_value(source_dict, 'third_key[b=3]')
    (True, {'b': 3})
    >>> resolve_path_to_value(source_dict, 'third_key[b=4]')[0]
    False
    >>> resolve_path_to_value(source_dict, 'third_key[b="5"]')
    (True, {'b': '5'})
    >>> resolve_path_to_value(source_dict, 'third_key[h=qw"er]')
    (True, {'h': 'qw"er'})
    >>> resolve_path_to_value(source_dict, 'third_key[c=asdf].c')
    (True, 'asdf')
    >>> resolve_path_to_value(source_dict, 'third_key[c=asdf].b')
    (False, {'c': 'asdf'})
    >>> resolve_path_to_value(source_dict, 'fourth_key[d~g=6].e.f')
    (True, 7)
    >>> resolve_path_to_value(source_dict, r'fifth_key[b\.c=9\.a].b\.c')
    (True, '9.a')
    >>> resolve_path_to_value(source_dict, r'fifth_key[b\[c=9\[a].b\[c')
    (True, '9[a')
    >>> resolve_path_to_value(source_dict, r'fifth_key[b\]c=9\]a].b\]c')
    (True, '9]a')
    >>> resolve_path_to_value(source_dict, r'fifth_key[b\\c=9\\a].b\\c')
    (True, '9\\a')
    >>> resolve_path_to_value(source_dict, 'sixth_key.a[].b')
    (True, [6, 5, 4])
    >>> resolve_path_to_value(source_dict, 'sixth_key.c[].d.e')
    (True, [3, 2])
    >>> resolve_path_to_value(source_dict, 'sixth_key.c[].x')
    (False, [])
    >>> resolve_path_to_value(source_dict, 'sixth_key.f')
    (True, [])
    >>> resolve_path_to_value(source_dict, 'sixth_key.f[]')
    (True, [])
    >>> resolve_path_to_value(source_dict, 'sixth_key.f[].g')
    (False, [])
    >>> resolve_path_to_value(source_dict, 'seventh_key.bad_api.x')
    (True, 3)
    >>> results = resolve_path_to_value(source_dict, 'seventh_key.bad_api.a')
    >>> results[0]
    False
    >>> results[1] == {'x': 3, 'y': 2, 'z': 1}
    True
    >>> resolve_path_to_value(source_dict, 'seventh_key.bad_api[bad-squares]')
    Traceback (most recent call last):
        ...
    ValueError: Bad square brackets syntax on 'bad-squares'
    >>> resolve_path_to_value(source_dict, 'seventh_key.bad_api[a=b=c=]')
    Traceback (most recent call last):
        ...
    ValueError: too many unquoted equals signs in square brackets for 'a=b=c='
    >>> resolve_path_to_value(source_dict, 'seventh_key[0]')
    Traceback (most recent call last):
        ...
    ValueError: array expected at 'seventh_key', found dict-like object.
    >>> resolve_path_to_value(source_dict, 'seventh_key[]')
    Traceback (most recent call last):
        ...
    ValueError: array expected at 'seventh_key', found dict-like object.
    >>> resolve_path_to_value(source_dict, 'seventh_key.bad_json.z')
    Traceback (most recent call last):
        ...
    ValueError: string found when looking for dict-like object at 'seventh_key.bad_json'. failed to convert to json.

    :param source: potentially holds the desired value
    :type source: dict
    :param path: points to the desired value
    :type path: six.string_types
    :returns: a boolean indicating found status, the value that was found
    :rtype: tuple
    :raises ValueError: if we don't understand what went inside some square brackets.
    """
    mapped_value = source
    found_value = True
    path_parts_break = False

    path_parts = _non_quoted_split(PERIOD_SPLIT, path)

    for path_parts_index, path_part_raw in enumerate(path_parts):
        # split on non quoted open bracket

        parts = _non_quoted_split(OPEN_SQUARE_BRACKET_SPLIT, path_part_raw)
        key = parts[0]
        array = parts[1:]
        # future: when dropping python 2 support do this instead.
        # key, *array = _non_quoted_split(OPEN_SQUARE_BRACKET_SPLIT, path_part_raw)

        key = _un_slash_escape(key)
        try:
            if isinstance(mapped_value, six.string_types):
                # ugh, maybe it is json?
                try:
                    mapped_value = json.loads(mapped_value)
                except ValueError:
                    raise ValueError(
                        'string found when looking for dict-like object at {!r}. failed to convert to json.'.format(
                            '.'.join(path_parts[:path_parts_index])
                        )
                    )
            if not hasattr(mapped_value, 'keys'):
                found_value = False
                break
            mapped_value = mapped_value[key]
        except KeyError:
            found_value = False
            break
        for array_part_raw in array:
            array_part = array_part_raw.strip(']')
            if array_part.isdigit():
                # [0]
                try:
                    mapped_value = mapped_value[int(array_part)]
                except KeyError:
                    raise ValueError('array expected at {!r}, found dict-like object.'.format(
                        '.'.join(path_parts[:path_parts_index] + [key])
                    ))
                except IndexError:
                    raise IndexError('index {!r} out of range on array at {!r}.'.format(
                        int(array_part),
                        '.'.join(path_parts[:path_parts_index] + [key])
                    ))
            elif '=' in array_part:
                # [Key=Value] or [Key~SubKey=Value]
                # split on non quoted equals signs
                equal_parts = _non_quoted_split(EQUAL_SPLIT, array_part)
                find_key = equal_parts[0]
                find_value = equal_parts[1:]
                # future: when dropping python 2 support do this instead.
                # find_key, *find_value = _non_quoted_split(EQUAL_SPLIT, array_part)
                if len(find_value) >= 2:
                    raise ValueError('too many unquoted equals signs in square brackets for {!r}'.format(array_part))
                find_value = find_value[0]
                if find_value.isdigit():
                    find_value = int(find_value)
                elif find_value.startswith('"') and find_value.endswith('"'):
                    find_value = find_value[1:-1]
                if isinstance(find_value, six.string_types):
                    find_value = _un_slash_escape(find_value)
                for item in [mapped_value] if hasattr(mapped_value, 'keys') else mapped_value:
                    sub_item = item
                    sub_keys = _non_quoted_split(TIDLE_SPLIT, find_key)
                    try:
                        while sub_keys:
                            sub_key = _un_slash_escape(sub_keys.pop(0))
                            sub_item = sub_item[sub_key]
                    except (KeyError, IndexError):
                        pass
                    else:
                        if sub_item == find_value:
                            mapped_value = item
                            break
                else:
                    # raise KeyError('no item with %r == %r' % (find_key, find_value))
                    found_value = False
                    path_parts_break = True  # break the outer loop, we are done here.
                    break
            elif array_part == '':
                # empty []
                if hasattr(mapped_value, 'keys'):
                    raise ValueError('array expected at {!r}, found dict-like object.'.format(
                        '.'.join(path_parts[:path_parts_index] + [key])
                    ))
                if not mapped_value:
                    if path_parts[path_parts_index+1:]:
                        found_value = False
                    path_parts_break = True  # break the outer loop, we are done here.
                    break
                remainder = '.'.join(path_parts[path_parts_index+1:])
                mapped_value = [resolve_path_to_value(x, remainder) for x in mapped_value]
                mapped_value = [value for found, value in mapped_value if found]
                if not mapped_value:
                    found_value = False
                path_parts_break = True  # break the outer loop, we are done here.
                break
            else:
                raise ValueError('Bad square brackets syntax on {!r}'.format(array_part))
        if path_parts_break:
            break
    return found_value, mapped_value


def resolve_mapping_to_dict(mapping, source):
    """
    move values from `source` into a returned dict, using `mapping` for paths and returned keys.
    see resolve_path_to_value for path string formats.

    >>> mapping = {
    ...     'a': 'x[type=other_type].aa',
    ...     'b': 'x[type=some_type].bb',
    ...     'c': 'x[type=other_type].cc',
    ... }
    >>> source = {
    ...     'x': [
    ...         {
    ...             'type': 'some_type',
    ...             'aa': '4',
    ...             'bb': '5',
    ...             'cc': '6'
    ...         },
    ...         {
    ...             'type': 'other_type',
    ...             'aa': '1',
    ...             'bb': '2',
    ...             'cc': '3'
    ...         }
    ...     ]
    ... }
    >>> resolve_mapping_to_dict(mapping, source) == {'a': '1', 'b': '5', 'c': '3'}
    True

    :param mapping: values are paths to find the corresponding value in `source`, keys are were to store said values
    :type mapping: dict
    :param source: potentially holds the desired values
    :type source: dict
    :returns: destination dict, containing any found values
    :rtype: dict
    """
    destination_dict = {}
    for destination_key, path in mapping.items():
        found_value, mapped_value = resolve_path_to_value(source, path)
        if found_value:
            destination_dict[destination_key] = mapped_value
    return destination_dict
