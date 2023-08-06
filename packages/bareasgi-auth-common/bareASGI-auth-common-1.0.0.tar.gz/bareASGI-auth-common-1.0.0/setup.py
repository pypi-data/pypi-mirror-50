# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['bareasgi_auth_common']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.7,<2.0', 'bareclient>=3.0,<4.0']

setup_kwargs = {
    'name': 'bareasgi-auth-common',
    'version': '1.0.0',
    'description': '',
    'long_description': '# bareASGI-auth-common\n\nCommon code for authentication with bareASGI.',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
