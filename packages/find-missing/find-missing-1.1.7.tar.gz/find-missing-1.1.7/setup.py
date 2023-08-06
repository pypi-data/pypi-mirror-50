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
    'version': '1.1.7',
    'description': '',
    'long_description': '# FIND-MISSING\n[![PyPI](https://img.shields.io/pypi/v/find-missing)](https://pypi.org/project/find-missing/)\n![](https://img.shields.io/badge/maintained-not_intended-red)\n\nFind files missing in a folder. This tool is intended to be used with [pipx](https://pipxproject.github.io/pipx/) as a normal command line tool.\n\n## Installation with PIPX   \n```shell script\npip install pipx\npipx install find-missing\n```\n\n## Usage with pipx\n```shell script\n$ find-missing "foo, bar, spam.jpg"\n```\n\nA file `foolitzer.jpg` will be a match without the `--exact` flag.\n\n## Installation and usage without pipx (not recommended)\n```shell script\npip install find-missing\npython find-missing.py "foo, bar, spam.jpg"\n```\n\n### Options\n\n#### Exact match only\n```shell script\n$ find-missing "foo, bar" --exact/-e\n```\n\nLooks for exact match, otherwise looks for partial match, so in the above example a file `foo.jpg` will be a match, and a file `foolitzer.jpg` will not.\n\n#### Include directories\n\n```shell script\nfind-missing "foo, bar" --dirs/-d\n```\n\nWill also check against subdirectories of the current directory.\n\n#### Verbose mode\n```shell script\n$ find-missing "foo, bar" --verbose/-v \n\nVerbose mode: True. Exact mode: False. Include directories: False\nLooking for files: foo\nDirectory content:\n...\nREADME.md\npoetry.lock\npyproject.toml\nsetup.py\n\nFound 1 missing files:\nfoo\n```\n\nVerbose mode (silent by default)\n\n### List separator\nThe tool will do it\'s best to find file names separated by anything. So a comma, a space, a semicolon will all work. The dot, underscore and dash will not as they can all be parts of file names.\n',
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
