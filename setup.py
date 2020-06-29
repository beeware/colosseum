#!/usr/bin/env python
import io
import re
from setuptools import setup

# Setuptools currently balks at reading the name
# and version from setup.cfg.

with io.open('./src/colosseum/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

setup(name='colosseum', version=version)
