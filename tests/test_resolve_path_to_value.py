from collections import OrderedDict

from tests.helpers import BaseUnitTest, KwargsToOutputDynamicTestsMetaClass
from transmogrifydict import resolve_path_to_value
from six import with_metaclass


class ResolvePathToValueTestCase(with_metaclass(KwargsToOutputDynamicTestsMetaClass, BaseUnitTest)):
    func = resolve_path_to_value
    tests = OrderedDict((
        (
            'simple',
            {
                'kwargs': {
                    'source': {
                        'one': 1,
                        'two': 2,
                        'three': 3
                    },
                    'path': 'two'
                },
                'output': (True, 2)
            }
        ),
        (
            'with_sub_keys',
            {
                'kwargs': {
                    'source': {
                        'one': 1,
                        'two': {
                            'sleeping': 'bereft of life',
                            'pining for the fjords': 'has ceased to be',
                            'stunned': 'an ex-parrot',
                        },
                        'three': 3
                    },
                    'path': 'two.sleeping'
                },
                'output': (True, 'bereft of life')
            }
        ),
        (
            'with_sub_keys_with_spaces',
            {
                'kwargs': {
                    'source': {
                        'one': 1,
                        't w o': {
                            'sleeping': 'bereft of life',
                            'pining for the fjords': 'has ceased to be',
                            'stunned': 'an ex-parrot',
                        },
                        'three': 3
                    },
                    'path': 't w o.pining for the fjords'
                },
                'output': (True, 'has ceased to be')
            }
        ),
        (
            'docstring_test_1',
            {
                'kwargs': {
                    'source': {
                        'first_key': 'a',
                        'second_key': [
                            'x',
                            'y',
                            'z',
                        ],
                        'third_key': [
                            {
                                'b': 1,
                                'c': 2,
                                'h': 'asdf'
                            },
                            {
                                'b': 3,
                                'c': 4,
                                'h': 'qw"er'
                            }
                        ],
                        'fourth_key': [
                            {
                                'd': {
                                    'f': 5,
                                    'g': 6
                                },
                                'e': {
                                    'f': 7,
                                    'g': 8
                                }
                            },
                            {
                                'd': {
                                    'f': 9,
                                    'g': 10
                                },
                                'e': {
                                    'f': 11,
                                    'g': 12
                                }
                            }
                        ]
                    },
                    'path': 'first_key'
                },
                'output': (True, 'a')
            }
        ),
        (
            'docstring_test_2',
            {
                'kwargs': {
                    'source': {
                        'first_key': 'a',
                        'second_key': [
                            'x',
                            'y',
                            'z',
                        ],
                        'third_key': [
                            {
                                'b': 1,
                                'c': 2,
                                'h': 'asdf'
                            },
                            {
                                'b': 3,
                                'c': 4,
                                'h': 'qw"er'
                            }
                        ],
                        'fourth_key': [
                            {
                                'd': {
                                    'f': 5,
                                    'g': 6
                                },
                                'e': {
                                    'f': 7,
                                    'g': 8
                                }
                            },
                            {
                                'd': {
                                    'f': 9,
                                    'g': 10
                                },
                                'e': {
                                    'f': 11,
                                    'g': 12
                                }
                            }
                        ]
                    },
                    'path': 'second_key[1]'
                },
                'output': (True, 'y')
            }
        ),
        (
            'docstring_test_3',
            {
                'kwargs': {
                    'source': {
                        'first_key': 'a',
                        'second_key': [
                            'x',
                            'y',
                            'z',
                        ],
                        'third_key': [
                            {
                                'b': 1,
                                'c': 2,
                                'h': 'asdf'
                            },
                            {
                                'b': 3,
                                'c': 4,
                                'h': 'qw"er'
                            }
                        ],
                        'fourth_key': [
                            {
                                'd': {
                                    'f': 5,
                                    'g': 6
                                },
                                'e': {
                                    'f': 7,
                                    'g': 8
                                }
                            },
                            {
                                'd': {
                                    'f': 9,
                                    'g': 10
                                },
                                'e': {
                                    'f': 11,
                                    'g': 12
                                }
                            }
                        ]
                    },
                    'path': 'third_key[b=3]'
                },
                'output': (True, {'h': 'qw"er', 'c': 4, 'b': 3})
            }
        ),
        (
            'docstring_test_4',
            {
                'kwargs': {
                    'source': {
                        'first_key': 'a',
                        'second_key': [
                            'x',
                            'y',
                            'z',
                        ],
                        'third_key': [
                            {
                                'b': 1,
                                'c': 2,
                                'h': 'asdf'
                            },
                            {
                                'b': 3,
                                'c': 4,
                                'h': 'qw"er'
                            }
                        ],
                        'fourth_key': [
                            {
                                'd': {
                                    'f': 5,
                                    'g': 6
                                },
                                'e': {
                                    'f': 7,
                                    'g': 8
                                }
                            },
                            {
                                'd': {
                                    'f': 9,
                                    'g': 10
                                },
                                'e': {
                                    'f': 11,
                                    'g': 12
                                }
                            }
                        ]
                    },
                    'path': 'third_key[h="qw"er"]'
                },
                'output': (True, {'h': 'qw"er', 'c': 4, 'b': 3})
            }
        ),
        (
            'docstring_test_5',
            {
                'kwargs': {
                    'source': {
                        'first_key': 'a',
                        'second_key': [
                            'x',
                            'y',
                            'z',
                        ],
                        'third_key': [
                            {
                                'b': 1,
                                'c': 2,
                                'h': 'asdf'
                            },
                            {
                                'b': 3,
                                'c': 4,
                                'h': 'qw"er'
                            }
                        ],
                        'fourth_key': [
                            {
                                'd': {
                                    'f': 5,
                                    'g': 6
                                },
                                'e': {
                                    'f': 7,
                                    'g': 8
                                }
                            },
                            {
                                'd': {
                                    'f': 9,
                                    'g': 10
                                },
                                'e': {
                                    'f': 11,
                                    'g': 12
                                }
                            }
                        ]
                    },
                    'path': 'third_key[h=asdf].c'
                },
                'output': (True, 2)
            }
        ),
        (
            'docstring_test_6',
            {
                'kwargs': {
                    'source': {
                        'first_key': 'a',
                        'second_key': [
                            'x',
                            'y',
                            'z',
                        ],
                        'third_key': [
                            {
                                'b': 1,
                                'c': 2,
                                'h': 'asdf'
                            },
                            {
                                'b': 3,
                                'c': 4,
                                'h': 'qw"er'
                            }
                        ],
                        'fourth_key': [
                            {
                                'd': {
                                    'f': 5,
                                    'g': 6
                                },
                                'e': {
                                    'f': 7,
                                    'g': 8
                                }
                            },
                            {
                                'd': {
                                    'f': 9,
                                    'g': 10
                                },
                                'e': {
                                    'f': 11,
                                    'g': 12
                                }
                            }
                        ]
                    },
                    'path': 'fourth_key[d~g=6].e.f'
                },
                'output': (True, 7)
            }
        ),
    ))
