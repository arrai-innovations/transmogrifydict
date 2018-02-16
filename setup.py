from setuptools import setup

setup(
    name='transmogrifydict',
    url='https://github.com/emergence/transmogrifydict',
    version='1.1.1',
    description='The "turn a dict from one API into a dict for another" python module.',
    author='Emergence by Design',
    author_email='support@emergence.com',
    py_modules=['transmogrifydict'],
    install_requires=[x for x in open('./requirements.txt').read().split('\n') if x]
)
