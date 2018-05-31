from setuptools import setup

setup(
    name='transmogrifydict',
    url='https://github.com/arrai-innovations/transmogrifydict',
    version='1.1.2',
    description='The "turn a dict from one API into a dict for another" python module.',
    author='Arrai Innovations',
    author_email='support@arrai.com',
    py_modules=['transmogrifydict'],
    install_requires=[x for x in open('./requirements.txt').read().split('\n') if x]
)
