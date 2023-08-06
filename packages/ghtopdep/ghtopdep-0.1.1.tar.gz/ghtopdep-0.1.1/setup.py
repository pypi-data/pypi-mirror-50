# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ghtopdep']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'halo>=0.0.26,<0.0.27',
 'httpx>=0.6.8,<0.7.0',
 'selectolax>=0.1.13,<0.2.0',
 'tabulate>=0.8.3,<0.9.0']

entry_points = \
{'console_scripts': ['ghtopdep = ghtopdep.ghtopdep:cli']}

setup_kwargs = {
    'name': 'ghtopdep',
    'version': '0.1.1',
    'description': 'CLI tool for sorting dependents repo by stars',
    'long_description': '# GHTOPDEP\n[![image](https://img.shields.io/pypi/v/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)\n[![image](https://img.shields.io/pypi/l/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)\n[![image](https://img.shields.io/pypi/pyversions/ghtopdep.svg)](https://pypi.org/project/ghtopdep/)\n\nCLI tool for sorting dependents repo by stars\n\n## Requirements\n* Python 3.5 and up\n\n## Installation\nfrom PyPI\n```\n$ pip install ghtopdep\n```\n\nfrom git repository\n```\n$ pip install git+https://github.com/github-tooling/ghtopdep\n```\n\nfrom source\n```\n$ git clone https://github.com/github-tooling/ghtopdep\n$ cd ghtopdep\n$ python setup.py install\n```\n\n## Usage\n\n```\n$ ghtopdep --help\nUsage: ghtopdep [OPTIONS] URL\n\nOptions:\n  --show INTEGER       Number of showing repositories (default=10).\n  --more-than INTEGER  Number of stars (default=5).\n  --help               Show this message and exit.\n```\n\n\n```\n$ ghtopdep https://github.com/dropbox/dropbox-sdk-js     \n+-------------------------------------------+---------+\n| URL                                       |   Stars |\n+===========================================+=========+\n| https://github.com/LN-Zap/zap-desktop     |     978 |\n+-------------------------------------------+---------+\n| https://github.com/Cleod9/syncmarx-webext |      35 |\n+-------------------------------------------+---------+\n| https://github.com/Playork/StickyNotes    |      32 |\n+-------------------------------------------+---------+\n| https://github.com/WebAssemblyOS/wasmos   |      23 |\n+-------------------------------------------+---------+\n| https://github.com/Cleod9/syncmarx-api    |      19 |\n+-------------------------------------------+---------+\n| https://github.com/Bearer/templates       |      11 |\n+-------------------------------------------+---------+\n| https://github.com/nathsimpson/isobel     |       9 |\n+-------------------------------------------+---------+\n| https://github.com/sorentycho/blackmirror |       8 |\n+-------------------------------------------+---------+\n| https://github.com/easylogic/edy          |       6 |\n+-------------------------------------------+---------+\n| https://github.com/Kikugumo/imas765probot |       5 |\n+-------------------------------------------+---------+\nfound 1203 repos others is private\nfound 289 repos with more than zero star\n```\n\n\n## Development setup\nUsing [Poetry](https://poetry.eustace.io/docs/)   \n```\n$ poetry install\n```\nor [Pipenv](https://docs.pipenv.org/)   \n```\n$ pipenv install --dev -e .\n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Andriy Orehov',
    'author_email': 'andriyorehov@gmail.com',
    'url': 'https://github.com/github-tooling/ghtopdep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
