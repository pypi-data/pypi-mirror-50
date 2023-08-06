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
    'version': '0.2.0',
    'description': 'Toml sorting library',
    'long_description': '# toml-sort\n\nA command line utility to sort your toml files. Requires Python 3.6 or greater.\n\n## Installation\n\n```bash\npip install toml-sort\n```\n\n## Usage\n\nRead from stdin, write to stdout:\n\n    cat input.toml | toml-sort -\n\nRead from file on disk, write to file on disk:\n\n    toml-sort -o output.toml input.toml\n\nRead from file on disk, write to stdout\n\n    toml-sort input.toml\n\nRead from stdin, write to file on disk\n\n    cat input.toml | toml-sort -o output.toml -\n\n## Local Development\n\nThis project is super simple.\n\n**Dependencies**\n\nInstall the following tools manually.\n\n* [Poetry](https://github.com/sdispater/poetry#installation)\n* [GNU Make](https://www.gnu.org/software/make/)\n\n*Recommended*\n\n* [pyenv](https://github.com/pyenv/pyenv)\n\n**Set up development environment**\n\n```bash\nmake setup\n```\n\n**Run Tests**\n\n```bash\nmake test\n```\n\n## Written by\n\nSamuel Roeca *samuel.roeca@gmail.com*\n',
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
