# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['libru']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'lxml>=4.4,<5.0',
 'pytz>=2019.2,<2020.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['ru = libru.cli:cli']}

setup_kwargs = {
    'name': 'libru',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Caio Pereira Oliveira',
    'author_email': 'caiopoliveira@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
