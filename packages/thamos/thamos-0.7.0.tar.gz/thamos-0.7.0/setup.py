import os
from setuptools import setup, find_packages
from pathlib import Path


def get_install_requires():
    with open('requirements.txt', 'r') as requirements_file:
        res = requirements_file.readlines()
        return [req.split(' ', maxsplit=1)[0] for req in res if req]


def get_version():
    with open(os.path.join('thamos', '__init__.py')) as f:
        content = f.readlines()

    for line in content:
        if line.startswith('__version__ ='):
            # dirty, remove trailing and leading chars
            return line.split(' = ')[1][1:-2]
    raise ValueError("No version identifier found")


setup(
    name='thamos',
    entry_points={
        'console_scripts': ['thamos=thamos.cli:cli']
    },
    version=get_version(),
    package_data={
        'thamos': [
            os.path.join('data', '*.yaml')
        ]
    },
    include_package_data=True,
    description='A CLI tool and library for interacting with Thoth',
    long_description=Path('README.rst').read_text(),
    author='Fridolin Pokorny',
    author_email='fridolin@redhat.com',
    license='GPLv3+',
    packages=find_packages(),
    install_requires=get_install_requires()
)
