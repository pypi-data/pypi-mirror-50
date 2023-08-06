# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sbot']

package_data = \
{'': ['*']}

install_requires = \
['j5>=0.7.4,<0.8.0']

setup_kwargs = {
    'name': 'sbot',
    'version': '0.6.0',
    'description': 'SourceBots API',
    'long_description': "# sbot\n\n[![CircleCI](https://circleci.com/gh/sourcebots/sbot.svg?style=svg)](https://circleci.com/gh/sourcebots/sbot)\n[![PyPI version](https://badge.fury.io/py/sbot.svg)](https://badge.fury.io/py/sbot)\n[![Documentation Status](https://readthedocs.org/projects/pip/badge/?version=stable)](http://pip.pypa.io/en/stable/?badge=stable)\n\n`sbot` - SourceBots Robot API - Powered by j5\n\nThis is the API for SourceBots, based on the [j5](https://github.com/j5api/j5)\nlibrary for writing Robotics APIs. It will first be deployed at Smallpeice 2019.\n\nMuch like it's predecessor, [robot-api](https://github.com/sourcebots/robot-api), `sbot` supports\nmultiple backends, although should be more reliable as there is no `UNIX-AF` socket layer.\n\n## Installation\n\nOnce published:\n\nInstall: `pip install sbot`\nInstall with vision support: `pip install sbot j5[zoloto-vision]`\n\n## Usage\n\n```python\n\nfrom sbot import Robot\n\nr = Robot()\n\n```\n\nOr alternatively:\n\n```python\n\nfrom sbot import Robot\n\nr = Robot(wait_start=False)\n\n# Setup in here\n\nr.wait_start()\n\n```\n",
    'author': 'SourceBots',
    'author_email': 'hello@sourcebots.co.uk',
    'url': 'https://sourcebots.co.uk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
