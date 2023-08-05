# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['d2c']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'd2c',
    'version': '0.0.0',
    'description': 'Convert discrete dislocation data to continuous fields.',
    'long_description': 'D2C\n===\n\nConvert discrete dislocation data to continuous fields.\n',
    'author': 'Dominik Steinberger',
    'author_email': 'd2c@steinberger.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
