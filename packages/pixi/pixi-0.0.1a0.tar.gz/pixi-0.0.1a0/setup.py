# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pixi']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0', 'click>=7.0,<8.0', 'pixiv-api>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['pixi = pixi.__main__.commandgroup']}

setup_kwargs = {
    'name': 'pixi',
    'version': '0.0.1a0',
    'description': 'A command line tool to download images from Pixiv.',
    'long_description': '# pixi\n\nA command line tool to download images from Pixiv.\n',
    'author': 'dazzler',
    'author_email': 'dazzler@riseup.net',
    'url': 'https://github.com/dazuling/pixi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
