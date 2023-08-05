# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dockenv']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.2.1,<0.3.0', 'loguru>=0.3.2,<0.4.0', 'pyyaml>=5.1,<6.0']

entry_points = \
{'console_scripts': ['dockenv = dockenv.dockenv:main']}

setup_kwargs = {
    'name': 'dockenv',
    'version': '0.1.3',
    'description': 'Simple cli utility for generate docker-compose.yml files',
    'long_description': None,
    'author': 't33m4h',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
