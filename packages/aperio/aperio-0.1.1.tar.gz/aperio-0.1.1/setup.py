# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aperio']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1.7,<2.0',
 'google-auth>=1.6,<2.0',
 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'aperio',
    'version': '0.1.1',
    'description': 'Unlimited Storage',
    'long_description': None,
    'author': 'elliott-maguire',
    'author_email': 'me@elliott-m.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
