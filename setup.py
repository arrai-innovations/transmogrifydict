from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()
with open('./requirements.txt') as reqs:
    install_requires = [x for x in reqs.read().split('\n') if x]
setup(
    name='transmogrifydict',
    url='https://github.com/arrai-innovations/transmogrifydict',
    version='1.1.3',
    description='The "turn a dict from one API into a dict for another" python module.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Arrai Innovations',
    author_email='support@arrai.com',
    py_modules=['transmogrifydict'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
    ]
)
