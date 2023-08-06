# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['hackinfo']
setup_kwargs = {
    'name': 'hackinfo',
    'version': '1.0.0',
    'description': 'Hackerinfo infromations Web Application Security  hejab Zaeri',
    'long_description': None,
    'author': 'Hejab Zaeri',
    'author_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
