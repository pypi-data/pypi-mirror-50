# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['firstapp_ku34']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'firstapp-ku34',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Asadur Rahman',
    'author_email': 'asadur.rahman@oscillosoft.com.au',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
