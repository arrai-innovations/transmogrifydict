from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='transmogrifydict',
    url='https://github.com/arrai-innovations/transmogrifydict',
    version='1.1.2',
    description='The "turn a dict from one API into a dict for another" python module.',
    long_description=long_description,
    long_description_conent_type='text/markdown',
    author='Arrai Innovations',
    author_email='support@arrai.com',
    py_modules=['transmogrifydict'],
    install_requires=[x for x in open('./requirements.txt').read().split('\n') if x],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
    ]
)
