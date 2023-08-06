# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['torchtrainer',
 'torchtrainer.callbacks',
 'torchtrainer.metrics',
 'torchtrainer.modules']

package_data = \
{'': ['*']}

install_requires = \
['codecov>=2.0,<3.0',
 'pycodestyle>=2.5,<3.0',
 'pytest-cov>=2.7,<3.0',
 'torch>=1.2,<2.0',
 'torchvision>=0.4.0,<0.5.0',
 'tqdm>=4.33,<5.0',
 'visdom>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'torchtrainer',
    'version': '0.2',
    'description': 'Focus on building and optimizing pytorch models not on training loops',
    'long_description': '# torchtrainer\n[![Build Status](https://travis-ci.com/VictorKuenstler/torchtrainer.svg?branch=master)](https://travis-ci.com/VictorKuenstler/torchtrainer)\n[![codecov](https://codecov.io/gh/VictorKuenstler/torchtrainer/branch/master/graph/badge.svg)](https://codecov.io/gh/VictorKuenstler/torchtrainer)\n\n\n## TODO\n\n### Callbacks\n- [] LRDecreaseOnPlateau\n- [] LRScheduler\n- [] plotting after training?',
    'author': 'Victor Künstler',
    'author_email': 'victor.kuenstler@outlook.com',
    'url': 'https://github.com/VictorKuenstler/torchtrainer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
