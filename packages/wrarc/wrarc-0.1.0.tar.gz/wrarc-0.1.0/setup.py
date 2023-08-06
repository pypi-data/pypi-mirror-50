# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['wrarc', 'wrarc.cmd']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['warc = main:main']}

setup_kwargs = {
    'name': 'wrarc',
    'version': '0.1.0',
    'description': 'This is a wrapper around phabricator to make the interactions with tasks seamless and fast.',
    'long_description': None,
    'author': 'Wasiur Rahman',
    'author_email': 'wrahman@uber.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
