# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hypy', 'hypy.modules']

package_data = \
{'': ['*']}

install_requires = \
['asciitree>=0.3.3,<0.4.0',
 'click>=7.0,<8.0',
 'paramiko>=2.6,<3.0',
 'pywinrm>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'hypy3',
    'version': '0.3.5',
    'description': 'Multiplataform Hyper-V Manager using Python and FreeRDP',
    'long_description': None,
    'author': 'Gabriel Avanzi',
    'author_email': 'gabriel.avanzi@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
