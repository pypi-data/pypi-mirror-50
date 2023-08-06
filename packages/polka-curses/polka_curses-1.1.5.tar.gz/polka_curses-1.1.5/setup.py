# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['polka_curses', 'polka_curses.views', 'polka_curses.views.widgets']

package_data = \
{'': ['*']}

install_requires = \
['polka>=2.4,<3.0', 'urwid>=2.0,<3.0']

entry_points = \
{'console_scripts': ['polka = polka_curses.main:main']}

setup_kwargs = {
    'name': 'polka-curses',
    'version': '1.1.5',
    'description': 'The curses interface for the Polka website (https://polka.academy/)',
    'long_description': "![Installation and Usage](https://raw.githubusercontent.com/dmkskn/polka_curses/master/images/install_and_usage.gif)\n\n## Installation\n\nUse `pip` to install the program (Python 3.7 is required):\n\n```bash\npip install polka-curses\n```\n\nDoesn't work in Windows!\n\n## Usage\n\nTo run the program, write `polka`.\n",
    'author': 'Dima Koskin',
    'author_email': 'dmksknn@gmail.com',
    'url': 'https://github.com/dmkskn/polka_curses/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
