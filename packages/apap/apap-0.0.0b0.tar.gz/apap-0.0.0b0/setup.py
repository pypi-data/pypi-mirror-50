# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['apap']

package_data = \
{'': ['*']}

install_requires = \
['mypy_extensions==0.4.1', 'requests==2.22.0']

setup_kwargs = {
    'name': 'apap',
    'version': '0.0.0b0',
    'description': 'Declarative and handy RESTful client factory',
    'long_description': None,
    'author': 'mtwtkman',
    'author_email': 'yo@mtwtkman.dev',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
