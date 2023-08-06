# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['chitanda',
 'chitanda.listeners',
 'chitanda.modules',
 'chitanda.modules.irc_channels',
 'chitanda.modules.lastfm',
 'chitanda.modules.quotes',
 'chitanda.modules.tell']

package_data = \
{'': ['*'],
 'chitanda.modules.irc_channels': ['migrations/*'],
 'chitanda.modules.lastfm': ['migrations/*'],
 'chitanda.modules.quotes': ['migrations/*'],
 'chitanda.modules.tell': ['migrations/*']}

install_requires = \
['aiohttp>=3.5,<4.0',
 'appdirs>=1.4,<2.0',
 'click>=7.0,<8.0',
 'discord.py>=1.2,<2.0',
 'gevent>=1.4,<2.0',
 'huey>=1.10,<2.0',
 'pydle>=0.9.1,<0.10.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['chitanda = chitanda.__main__:run']}

setup_kwargs = {
    'name': 'chitanda',
    'version': '0.0.4',
    'description': 'An extensible Discord & IRC bot.',
    'long_description': '# chitanda\n\n[![Build Status](https://travis-ci.org/dazuling/chitanda.svg?branch=master)](https://travis-ci.org/dazuling/chitanda)\n[![Coverage Status](https://coveralls.io/repos/github/dazuling/chitanda/badge.svg?branch=master)](https://coveralls.io/github/dazuling/chitanda?branch=master)\n[![Pypi](https://img.shields.io/pypi/v/chitanda.svg)](https://pypi.python.org/pypi/chitanda)\n[![Pyversions](https://img.shields.io/pypi/pyversions/chitanda.svg)](https://pypi.python.org/pypi/chitanda)\n[![Documentation Status](https://readthedocs.org/projects/chitanda/badge/?version=latest)](https://chitanda.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nAn extensible IRC & Discord bot. Requires Python 3.7.\n\nRead the documentation at https://chitanda.readthedocs.io.\n\n## Quickstart\n\nIt is recommended that chitanda be installed with `pipx`; however, if that is\nnot possible, `pip install --user` will also work.\n\n```bash\n$ pipx install chitanda\n$ chitanda migrate  # Upgrade database to latest version.\n$ chitanda config  # See wiki for configuration instructions.\n$ chitanda run\n```\n\n## License\n\n```\nCopyright (C) 2019 dazuling <azuline@riseup.net>\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see <https://www.gnu.org/licenses/>.\n```\n',
    'author': 'dazuling',
    'author_email': 'azuline@riseup.net',
    'url': 'https://github.com/dazuling/chitanda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
