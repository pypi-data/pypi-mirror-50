"""Setup module."""
from os import path
from setuptools import setup, find_packages

__version__ = '0.3.1'

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# get the dependencies and installs
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    ALL_REQS = f.read().split('\n')

install_requires = [x.strip() for x in ALL_REQS if 'git+' not in x]

dependency_links = [x.strip().replace('git+', '')
                    for x in ALL_REQS if x.startswith('git+')]

setup(
    name='aioiliad',
    version=__version__,
    description='A python package that can be installed with pip.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/eliseomartelli/aioiliad',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Eliseo Martelli',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='me@eliseomartelli.it'
)
