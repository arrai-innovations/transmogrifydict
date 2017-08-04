from unittest import TestCase
import six
if six.PY3:
    from functools import partialmethod
else:
    from functools import partial

    # noinspection PyPep8Naming
    class partialmethod(partial):
        def __get__(self, instance, owner):
            if instance is None:
                return self
            return partial(self.func, instance,
                           *(self.args or ()), **(self.keywords or {}))


class BaseUnitTest(TestCase):
    def run_test(self, method, output, **kwargs):
        actual = method(**kwargs)
        self.assertEqual(output, actual)


class KwargsToOutputDynamicTestsMetaClass(type):
    def __new__(cls, name, bases, dict):
        method = dict.get('run_test', BaseUnitTest.run_test)
        for name, args in dict['tests'].items():
            dict['test_%s' % (name, )] = partialmethod(method, dict['func'], args['output'], **args['kwargs'])
        return type(name, bases, dict)
