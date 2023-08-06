# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['barrier']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1,<2.0',
 'flask-oidc>=1.4,<2.0',
 'gunicorn>=19.9,<20.0',
 'poetry-version>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['barrier-config = barrier.configure:main',
                     'barrier-dev = barrier.app:app.run',
                     'barrier-wsgi = barrier.wsgi:main']}

setup_kwargs = {
    'name': 'barrier',
    'version': '0.1.1',
    'description': 'Serve static files safely behind OpenIDConnect-compatible authentication (i.e. Okta)',
    'long_description': None,
    'author': 'Matthew de Verteuil',
    'author_email': 'mdeverteuil@gadventures.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
