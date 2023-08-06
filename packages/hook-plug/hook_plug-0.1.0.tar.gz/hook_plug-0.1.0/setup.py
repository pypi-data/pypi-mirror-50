# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hook_plug']

package_data = \
{'': ['*']}

install_requires = \
['pluggy>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'hook-plug',
    'version': '0.1.0',
    'description': 'Hook Plug is an extension for testing frameworks. This provides the possibility of decoupling hook responsibilities and extending it with plugins.',
    'long_description': None,
    'author': 'dunossauro',
    'author_email': 'mendesxeduardo@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
