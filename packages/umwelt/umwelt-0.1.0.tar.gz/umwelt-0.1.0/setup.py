# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['umwelt', 'umwelt.decoders']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=0.17,<1']

setup_kwargs = {
    'name': 'umwelt',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thibaut Le Page',
    'author_email': 'thilp@thilp.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
