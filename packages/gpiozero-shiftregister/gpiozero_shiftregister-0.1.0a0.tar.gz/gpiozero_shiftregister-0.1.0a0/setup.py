# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gpiozero_shiftregister']

package_data = \
{'': ['*']}

install_requires = \
['RPi.GPIO>=0.7.0,<0.8.0', 'gpiozero>=1.5,<2.0']

setup_kwargs = {
    'name': 'gpiozero-shiftregister',
    'version': '0.1.0a0',
    'description': 'Control shift register on rasperypi using gpiozero library',
    'long_description': None,
    'author': 'Yisrael Dov Lebow',
    'author_email': 'lebow@lebowtech.com',
    'url': 'https://yisraeldov.gitlab.io/gpiozero-shiftregister',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
