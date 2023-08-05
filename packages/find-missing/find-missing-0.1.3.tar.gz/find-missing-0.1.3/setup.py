# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['main']
install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['main = find_missing:from_list']}

setup_kwargs = {
    'name': 'find-missing',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'MB',
    'author_email': 'mb@m1k.pw',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
