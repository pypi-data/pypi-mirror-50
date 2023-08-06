# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hp_report_portal']

package_data = \
{'': ['*']}

install_requires = \
['hook-plug>=0.0.1,<0.0.2', 'reportportal-client>=3.2,<4.0']

setup_kwargs = {
    'name': 'hp-report-portal',
    'version': '0.0.3',
    'description': 'behave report portal hook plugin',
    'long_description': None,
    'author': 'dunossauro',
    'author_email': 'mendesxeduardo@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
