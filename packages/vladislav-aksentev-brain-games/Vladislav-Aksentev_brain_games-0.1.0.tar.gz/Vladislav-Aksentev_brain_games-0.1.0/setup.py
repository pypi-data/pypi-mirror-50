# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['brain_games', 'brain_games.scripts']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['brain-games = brain_games.scripts.brain_games:main']}

setup_kwargs = {
    'name': 'vladislav-aksentev-brain-games',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Vladislav',
    'author_email': 'ieniki@yandex.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
