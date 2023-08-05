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


install_requirements = [
    'connexion>=2.0.0',
    'py-buzz>=0.3.6',
]
tests_requirements = [
    'pytest',
    'pytest-cov',
]


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
    name='connexion-buzz',
    version=version,
    description='py-buzz bindings specifically for connexion applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.mytradingdata.com/common/connexion-buzz',
    author='Aleksey Dalekin',
    author_email='ald@investex.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='connexion error py-buzz',
    packages=find_packages(exclude=['test*']),
    setup_requires=['pytest-runner'],
    install_requires=install_requirements,
    tests_require=tests_requirements,
    cmdclass={
        'version': VersionCommand,
    },
)
