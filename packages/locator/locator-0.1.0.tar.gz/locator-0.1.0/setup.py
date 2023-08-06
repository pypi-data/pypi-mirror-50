# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['locator']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.4,<5.0']

setup_kwargs = {
    'name': 'locator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'shidenggui',
    'author_email': '903618848@qq.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
