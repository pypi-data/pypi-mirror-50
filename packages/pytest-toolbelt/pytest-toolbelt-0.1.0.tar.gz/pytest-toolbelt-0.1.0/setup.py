import codecs
import os
import re

from setuptools import Command, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

version = '0.0.0'
changes = os.path.join(here, 'CHANGES.md')
match = r'^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        res = re.match(match, line)
        if res:
            version = res.group('version')
            break

# Get the long description
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version
with codecs.open(os.path.join(here, 'CHANGES.md'), encoding='utf-8') as f:
    changelog = f.read()


# Get requirements
def get_requirements(env=None):
    requirements_filename = 'requirements.txt'

    if env:
        requirements_filename = f'requirements-{env}.txt'

    with open(requirements_filename) as fp:
        return [x.strip() for x in fp.read().split('\n') if not x.startswith('#')]


install_requirements = get_requirements()
tests_requirements = get_requirements('test')


class VersionCommand(Command):
    description = 'print library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name='pytest-toolbelt',
    version=version,
    description='This is just a collection of utilities for pytest, but don\'t really belong in pytest proper.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/adalekin/pytest-toolbelt',
    author='Aleksey Dalekin',
    author_email='ald@investex.com.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Testing :: Unit',
    ],
    keywords='rest client http pytest assert',
    packages=find_packages(exclude=['test*']),
    setup_requires=['pytest-runner'],
    install_requires=install_requirements,
    tests_require=tests_requirements,
    cmdclass={
        'version': VersionCommand,
    },
    entry_points={
       'pytest11': [
           'toolbelt = pytest_toolbelt.plugin',
       ],
    },
)
