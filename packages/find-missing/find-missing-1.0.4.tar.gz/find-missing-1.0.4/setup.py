# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['find_missing']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['Find-Missing = find_missing:main',
                     'find-missing = find_missing:main']}

setup_kwargs = {
    'name': 'find-missing',
    'version': '1.0.4',
    'description': '',
    'long_description': None,
    'author': 'MB',
    'author_email': 'mb@m1k.pw',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
