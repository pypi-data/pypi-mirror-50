# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['toml_sort']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'tomlkit>=0.5.5']

entry_points = \
{'console_scripts': ['toml-sort = toml_sort.cli:cli']}

setup_kwargs = {
    'name': 'toml-sort',
    'version': '0.1.0',
    'description': 'Toml sorting library',
    'long_description': '# toml-sort\n\nA command line utility to sort your toml files. Requires Python 3.6 or greater.\n\n## Installation\n\n```bash\npip install toml-sort\n```\n\n## Usage\n\nCurrently, this project only reads from a toml file on disk and writes to stdout. I plan to flesh out the interface in the coming days.\n\n```bash\n# Prints sorted results to stdout\ntoml-sort FILENAME\n```\n\n## Local Development\n\n### Dependencies\n\n* [Poetry](https://github.com/sdispater/poetry#installation)\n* [GNU Make](https://www.gnu.org/software/make/)\n\n### Run Tests\n\n```bash\nmake test\n```\n\n## Written by\n\nSamuel Roeca *samuel.roeca@gmail.com*\n',
    'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'url': 'https://github.com/pappasam/toml-sort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
