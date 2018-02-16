import doctest

from collections import OrderedDict

from tests.helpers import BaseUnitTest, KwargsToOutputDynamicTestsMetaClass
import transmogrifydict
from six import with_metaclass


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(transmogrifydict))
    return tests


class ResolvePathToValueTestCase(with_metaclass(KwargsToOutputDynamicTestsMetaClass, BaseUnitTest)):
    func = transmogrifydict.resolve_path_to_value
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
    ))
