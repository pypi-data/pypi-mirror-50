# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dj']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'click>=7.0,<8.0',
 'colorama>=0.4.1,<0.5.0',
 'delegator.py>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['dj = dj:__main__.run']}

setup_kwargs = {
    'name': 'dj-command',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Adam Hill',
    'author_email': 'adamghill@yahoo.com',
    'url': 'https://github.com/adamghill/dj',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
