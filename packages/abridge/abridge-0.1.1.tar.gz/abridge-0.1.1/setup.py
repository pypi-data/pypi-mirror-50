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
 'proglog>=0.1.9,<0.2.0']

entry_points = \
{'console_scripts': ['abridge = abridge.cli:main']}

setup_kwargs = {
    'name': 'abridge',
    'version': '0.1.1',
    'description': 'Splice similar frames from videos',
    'long_description': '# abridge\n\nAutomatically cutout similar frames from videos\n',
    'author': 'Oliver Bell',
    'author_email': 'freshollie@gmail.com',
    'url': 'https://github.com/sdispater/poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
