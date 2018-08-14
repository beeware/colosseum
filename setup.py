#!/usr/bin/env python
import io
import re

from setuptools import find_packages, setup

with io.open('./colosseum/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='colosseum',
    version=version,
    description='An independent implementation of the CSS layout algorithm.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    # url='http://pybee.org/colosseum',
    url='https://github.com/pybee/colosseum',
    packages=find_packages(exclude=['tests', 'utils']),
    python_requires='>=3.5',
    install_requires=[],
    license='New BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
    test_suite='tests',
    package_urls={
        'Funding': 'https://pybee.org/contributing/membership/',
        'Documentation': 'https://colosseum.readthedocs.io/',
        'Tracker': 'https://github.com/pybee/colosseum/issues',
        'Source': 'https://github.com/pybee/colosseum',
    },
)
