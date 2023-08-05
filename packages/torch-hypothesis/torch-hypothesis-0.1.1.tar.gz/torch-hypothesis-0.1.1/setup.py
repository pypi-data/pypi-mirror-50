# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['torch_hypothesis']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=4.24,<5.0', 'torch>=1.1,<2.0', 'torchvision>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'torch-hypothesis',
    'version': '0.1.1',
    'description': 'Generate pytorch data structures for the hypothesis testing library.',
    'long_description': None,
    'author': 'Jan Fryeberg',
    'author_email': 'jan.freyberg@elementai.com',
    'url': 'https://github.com/janfreyberg/torch-hypothesis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
