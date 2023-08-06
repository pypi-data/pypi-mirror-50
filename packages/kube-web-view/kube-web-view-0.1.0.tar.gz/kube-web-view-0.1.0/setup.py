# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kube_web']

package_data = \
{'': ['*'],
 'kube_web': ['templates/*', 'templates/assets/*', 'templates/partials/*']}

install_requires = \
['Jinja2>=2.10,<3.0',
 'Pygments>=2.4,<3.0',
 'aioauth-client>=0.17.3,<0.18.0',
 'aiohttp-jinja2>=1.1,<2.0',
 'aiohttp_remotes>=0.1.2,<0.2.0',
 'aiohttp_session[secure]>=2.7,<3.0',
 'pykube-ng>=0.28.0,<0.29.0']

entry_points = \
{'console_scripts': ['kube-web-view = kube_web:main.main']}

setup_kwargs = {
    'name': 'kube-web-view',
    'version': '0.1.0',
    'description': 'Kubernetes Web UI',
    'long_description': None,
    'author': 'Henning Jacobs',
    'author_email': 'henning@zalando.de',
    'url': 'https://kube-web-view.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
