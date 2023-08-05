# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['microstructure']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'microstructure',
    'version': '0.0.0',
    'description': 'Library for dealing with microstructure.',
    'long_description': 'microstructure\n==============\n\nLibrary for dealing with microstructure.\n',
    'author': 'Dominik Steinberger',
    'author_email': 'microstructure@steinberger.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
