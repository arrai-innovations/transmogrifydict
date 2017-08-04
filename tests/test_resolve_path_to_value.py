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
        )
    ))
