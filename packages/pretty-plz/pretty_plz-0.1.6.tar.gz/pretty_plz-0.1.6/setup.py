# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pretty_plz']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['plz = pretty_plz.main:main']}

setup_kwargs = {
    'name': 'pretty-plz',
    'version': '0.1.6',
    'description': 'pretty_plz is a tool that turns utility scripts into runnable commands',
    'long_description': '## pretty_plz, the script command launcher\n\nPut all those useful utility scripts into a central location and\nhave them magically work from anywhere as simple commands.\n\n1. `pip install pretty-plz`\n1. Set `PLZ_SCRIPTS_PATH` to the directory where you store your scripts\n1. Call any of your scripts with or without extension from anywere as\n   `plz [command] [args]`.\n\n`plz` also automatically reads a project-level `.env` file (unless told not\nto do that via the environment).\n\nThe intended usage is to set PLZ_SCRIPTS_PATH in your shell, and optionally\nset PLZ_LOCAL_SCRIPTS_PATH in the project-level `.env` file.\n\n### Environment variables\n\n`PLZ_SCRIPTS_PATH`\n\nThe global home for your utility scripts.\n\n`PLZ_LOCAL_SCRIPTS_PATH`\n\nProject-level home of your utility scripts.\n\n`PLZ_IGNORE_DOTENV`\n\nWhen set, `plz` will ignore the project-level `.env` file.\n',
    'author': 'Tamás Szelei',
    'author_email': 'szelei.t@gmail.com',
    'url': 'https://github.com/sztomi/plz/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
