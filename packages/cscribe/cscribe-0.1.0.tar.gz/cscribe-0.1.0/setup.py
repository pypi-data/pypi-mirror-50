# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cscribe']

package_data = \
{'': ['*']}

install_requires = \
['cmlkit>=2.0.0a14', 'dscribe', 'numpy>=1.15']

setup_kwargs = {
    'name': 'cscribe',
    'version': '0.1.0',
    'description': 'cmlkit plugin for the dscribe package',
    'long_description': '# cscribe 🐫🖋️\n\n*a camel which writes*\n\n`cscribe` is a [`cmlkit`](https://github.com/sirmarcel/cmlkit/tree/develop-2.0) plugin for [`DScribe`](https://github.com/SINGROUP/dscribe), exposing its capabilities to compute various representations to the `cmlkit` ecosystem.\n\nWARNING: This is very early software. Please do not use in production.\n',
    'author': 'Marcel Langer',
    'author_email': 'dev@sirmarcel.com',
    'url': 'https://github.com/sirmarcel/cscribe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
