# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['lite']
install_requires = \
['aiohttp>=3.5,<4.0']

setup_kwargs = {
    'name': 'lite',
    'version': '0.1.4',
    'description': 'Analouge Light.js on Python',
    'long_description': None,
    'author': 'mihett05',
    'author_email': 'mihett05@yandex.ru',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
