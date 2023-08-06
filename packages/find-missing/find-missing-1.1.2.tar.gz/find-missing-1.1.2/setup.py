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
    'version': '1.1.2',
    'description': '',
    'long_description': '# FIND-MISSING\nFind files missing in a folder. This tool is intended to be used with [pipx](https://pipxproject.github.io/pipx/) as a normal command line tool.\n\n## Installation with PIPX\n```shell script\npip install pipx\npipx install find-missing\n```\n\n## Usage with pipx\n```shell script\nfind-missing "foo, bar, spam.jpg"\n```\n\nA file `foolitzer.jpg` will be a match without the `--exact` flag.\n\n### Options\n\n```shell script\nfind-missing "foo, bar" --exact\n```\n\nLooks for exact match, otherwise looks for partial match, so in the above example a file `foo.jpg` will be a match, and a file `foolitzer.jpg` will not.\n',
    'author': 'MB',
    'author_email': 'mb@m1k.pw',
    'url': 'https://github.com/licht1stein/find-missing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
