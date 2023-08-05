# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['json_schema_discovery']

package_data = \
{'': ['*']}

install_requires = \
['tabulate>=0.8.3,<0.9.0']

setup_kwargs = {
    'name': 'json-schema-discovery',
    'version': '1.1.0',
    'description': 'Database-agnostic JSON schema discovery',
    'long_description': None,
    'author': 'Stepland',
    'author_email': 'Stepland@hotmail.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
