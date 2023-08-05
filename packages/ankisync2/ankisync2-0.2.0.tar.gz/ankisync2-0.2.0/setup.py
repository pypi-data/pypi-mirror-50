# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ankisync2', 'ankisync2.builder', 'ankisync2.preset']

package_data = \
{'': ['*']}

install_requires = \
['peewee>=3.9,<4.0', 'shortuuid>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'ankisync2',
    'version': '0.2.0',
    'description': 'Doing in Anki what AnkiConnect cannot do',
    'long_description': None,
    'author': 'patarapolw',
    'author_email': 'patarapolw@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
