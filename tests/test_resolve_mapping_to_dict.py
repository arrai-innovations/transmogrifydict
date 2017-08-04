from collections import OrderedDict

from tests.helpers import BaseUnitTest, KwargsToOutputDynamicTestsMetaClass
from transmogrifydict import resolve_mapping_to_dict
from six import with_metaclass


class ResolvePathToValueTestCase(with_metaclass(KwargsToOutputDynamicTestsMetaClass, BaseUnitTest)):
    func = resolve_mapping_to_dict
    tests = OrderedDict((
        (
            'doctest_test_1',
            {
                'kwargs': {
                    'mapping': {
                        'a': 'x[type=other_type].aa',
                        'b': 'x[type=some_type].bb',
                        'c': 'x[type=other_type].cc',
                    },
                    'source': {
                        'x': [
                            {
                                'type': 'some_type',
                                'aa': '4',
                                'bb': '5',
                                'cc': '6'
                            },
                            {
                                'type': 'other_type',
                                'aa': '1',
                                'bb': '2',
                                'cc': '3'
                            }
                        ]
                    }
                },
                'output': {'a': '1', 'c': '3', 'b': '5'}
            }
        ),
    ))
