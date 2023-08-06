# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fetchy', 'fetchy.cli', 'fetchy.plugins', 'fetchy.plugins.packages']

package_data = \
{'': ['*'], 'fetchy.cli': ['commands/*']}

install_requires = \
['PyInquirer>=1.0,<2.0',
 'cleo>=0.7.5,<0.8.0',
 'distro>=1.4,<2.0',
 'docker>=4.0,<5.0',
 'pyelftools>=0.25.0,<0.26.0',
 'pyyaml>=5.1,<6.0',
 'tqdm>=4.32,<5.0',
 'unix_ar>=0.2.1,<0.3.0',
 'validators>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['fetchy = fetchy.cli:main']}

setup_kwargs = {
    'name': 'fetchy',
    'version': '0.1.7',
    'description': 'Minuscule docker images made trivial!',
    'long_description': None,
    'author': 'thomas',
    'author_email': 'thomas.kluiters@gmail.com',
    'url': 'https://github.com/ThomasKluiters/fetchy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
