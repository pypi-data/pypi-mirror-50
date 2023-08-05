# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['find_missing']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

setup_kwargs = {
    'name': 'find-missing',
    'version': '0.1.16',
    'description': '',
    'long_description': None,
    'author': 'MB',
    'author_email': 'mb@m1k.pw',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
