# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['python_vtk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-vtk',
    'version': '0.0.0',
    'description': 'Pythonic API for VTK.',
    'long_description': 'python-vtk\n==========\n\nPythonic API for VTK.\n',
    'author': 'Dominik Steinberger',
    'author_email': 'python-vtk@steinberger.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
