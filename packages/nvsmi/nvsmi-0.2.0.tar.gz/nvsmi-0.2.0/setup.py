# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['nvsmi']
entry_points = \
{'console_scripts': ['nvsmi = nvsmi:main']}

setup_kwargs = {
    'name': 'nvsmi',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Panos Mavrogiorgos',
    'author_email': 'pmav99@gmail.com',
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
