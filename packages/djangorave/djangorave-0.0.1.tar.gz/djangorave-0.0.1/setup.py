# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['djangorave', 'djangorave.example.example', 'djangorave.migrations']

package_data = \
{'': ['*'], 'djangorave': ['example/manage.py', 'templates/djangorave/*']}

install_requires = \
['django>=2.2,<3.0', 'djangorestframework>=3.10,<4.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'djangorave',
    'version': '0.0.1',
    'description': 'Django flutterwave rave',
    'long_description': '# Django Rave\n\n## Project Description\n\nThis project provides Django integration with the [Flutterwave](https://flutterwave.com/) API.\n\nThe project is currently being developed and is considered pre-alpha.\n\n# Installation\n\n```bash\npip install djangorave\n```\n\n# Development and Contribution\n\n### Running the example:\n\n```bash\nmake build\nmake dup\n```\n\n### Building for publication (to PyPI)\n\n```bash\npoetry build\n```',
    'author': 'Brendon Delate',
    'author_email': 'brendon.delate@gmail.com',
    'url': 'https://github.com/bdelate/django-rave.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
