# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['dislocation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dislocation',
    'version': '0.0.0',
    'description': 'Library for dealing with dislocations.',
    'long_description': 'dislocation\n===========\n\nLibrary for dealing with dislocations.\n',
    'author': 'Dominik Steinberger',
    'author_email': 'dislocation@steinberger.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
