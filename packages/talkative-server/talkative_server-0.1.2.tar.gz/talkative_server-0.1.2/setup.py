# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['talkative_server', 'talkative_server.jim_mes']

package_data = \
{'': ['*'],
 'talkative_server': ['contacts/*',
                      'docs/*',
                      'docs/_build/doctrees/*',
                      'docs/_build/html/*',
                      'docs/_build/html/_modules/*',
                      'docs/_build/html/_modules/jim_mes/*',
                      'docs/_build/html/_modules/sqlalchemy/orm/*',
                      'docs/_build/html/_sources/*',
                      'docs/_build/html/_static/*',
                      'docs/_build/html/_static/css/*',
                      'docs/_build/html/_static/fonts/*',
                      'docs/_build/html/_static/fonts/Lato/*',
                      'docs/_build/html/_static/fonts/RobotoSlab/*',
                      'docs/_build/html/_static/js/*',
                      'message/*',
                      'templates/*',
                      'templates/icons/*']}

install_requires = \
['dynaconf>=2.0,<3.0',
 'passlib>=1.7,<2.0',
 'pycryptodomex>=3.8,<4.0',
 'pyqt5>=5.13,<6.0',
 'pyyaml>=5.1,<6.0',
 'sqlalchemy-utils>=0.34.1,<0.35.0',
 'sqlalchemy>=1.3,<2.0',
 'tabulate>=0.8.3,<0.9.0']

setup_kwargs = {
    'name': 'talkative-server',
    'version': '0.1.2',
    'description': 'It is example project for study',
    'long_description': '# Talkative (messanger)\nProject for learning\n',
    'author': 'MaxST',
    'author_email': 'mstolpasov@gmail.com',
    'url': 'https://github.com/mom1/messager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
