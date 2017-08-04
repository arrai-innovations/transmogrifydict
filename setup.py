from setuptools import setup
import unittest


def test_suite():
    return unittest.TestLoader().discover('tests', pattern='test_*.py')

setup(
    name='transmogrifydict',
    url='https://github.com/emergence/transmogrifydict',
    version='1.0.0',
    description='The "turn a dict from one API into a dict for another" python module.',
    author='Emergence by Design',
    author_email='support@emergence.com',
    py_modules=['transmogrifydict'],
    test_suite='setup.test_suite',
    install_requires=[x for x in open('./requirements.txt').read().split('\n') if x]
)
