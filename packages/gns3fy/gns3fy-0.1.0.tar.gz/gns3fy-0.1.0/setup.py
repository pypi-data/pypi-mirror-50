# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gns3fy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=0.31.0,<0.32.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'gns3fy',
    'version': '0.1.0',
    'description': 'Python wrapper around GNS3 Server API',
    'long_description': None,
    'author': 'David Flores',
    'author_email': 'davidflores7_8@hotmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
