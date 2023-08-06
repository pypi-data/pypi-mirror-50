# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flask_socketio_lit_html']

package_data = \
{'': ['*'],
 'flask_socketio_lit_html': ['static/*',
                             'templates/*',
                             'webcomponent_templates/*']}

setup_kwargs = {
    'name': 'flask-socketio-lit-html',
    'version': '0.1.0rc1',
    'description': 'Simple Webcomponents with flask',
    'long_description': None,
    'author': 'playerla',
    'author_email': 'playerla.94@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
