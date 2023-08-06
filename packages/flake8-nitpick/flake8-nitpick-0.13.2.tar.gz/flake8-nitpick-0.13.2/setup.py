# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flake8_nitpick', 'flake8_nitpick.files']

package_data = \
{'': ['*']}

install_requires = \
['attrs',
 'dictdiffer',
 'flake8>=3.0.0',
 'jmespath',
 'python-slugify',
 'pyyaml',
 'requests',
 'toml']

entry_points = \
{'flake8.extension': ['NIP = flake8_nitpick.plugin:NitpickChecker']}

setup_kwargs = {
    'name': 'flake8-nitpick',
    'version': '0.13.2',
    'description': 'Flake8 plugin to enforce the same lint configuration (flake8, isort, mypy, pylint) across multiple Python projects',
    'long_description': '# NOTICE: flake-nitpick renamed to nitpick\n\nThis project has been renamed to [nitpick](https://pypi.org/project/nitpick/).\n',
    'author': 'W. Augusto Andreoli',
    'author_email': 'andreoliwa@gmail.com',
    'url': 'https://github.com/andreoliwa/flake8-nitpick',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
