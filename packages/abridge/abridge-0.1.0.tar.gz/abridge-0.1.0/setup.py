# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['abridge']

package_data = \
{'': ['*']}

install_requires = \
['enlighten>=1.3,<2.0',
 'moviepy>=1.0,<2.0',
 'numpy>=1.17,<2.0',
 'proglog>=0.1.9,<0.2.0',
 'pytest-sugar>=0.9.2,<0.10.0']

entry_points = \
{'console_scripts': ['abridge = abridge.cli:main']}

setup_kwargs = {
    'name': 'abridge',
    'version': '0.1.0',
    'description': 'Splice similar frames from videos',
    'long_description': None,
    'author': 'Oliver Bell',
    'author_email': 'freshollie@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
