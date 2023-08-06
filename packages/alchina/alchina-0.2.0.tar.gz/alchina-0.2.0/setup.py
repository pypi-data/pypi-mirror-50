# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['alchina']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.24.2,<0.25.0',
 'scikit-learn>=0.20.3,<0.21.0']

setup_kwargs = {
    'name': 'alchina',
    'version': '0.2.0',
    'description': 'Machine Learning framework',
    'long_description': '# Alchina /al.ki.na/\n\n[![Build Status](https://travis-ci.org/matthieugouel/alchina.svg?branch=master)](https://travis-ci.org/matthieugouel/alchina)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/alchina)\n[![Coverage Status](https://coveralls.io/repos/github/matthieugouel/alchina/badge.svg?branch=master)](https://coveralls.io/github/matthieugouel/alchina?branch=master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![license](https://img.shields.io/github/license/matthieugouel/alchina.svg)](https://github.com/matthieugouel/alchina/blob/master/LICENSE)\n\nAlchina is a Machine Learning framework.\n\n## Capabilities\n\n**Regressors**\n\n- Linear regressor\n- Ridge regressor\n\n**Classifiers**\n\n- Linear classifier\n- Ridge classifier\n\n**Clusters**\n\n- K-Means clustering\n\n**Optimizers**\n\n- Gradient descent\n- Stochastic gradient descent\n- Mini-batch gradient descent\n\n**Preprocessors**\n\n- Min-max normalization\n- Standardization\n- PCA\n\n**Metrics**\n\n- R2 score\n- Confusion matrix\n- Accuracy score\n- Precision score\n- Recall score\n- F-Beta score\n- F-1 score\n\n**Model selection**\n\n- Split dataset\n',
    'author': 'matthieu Gouel',
    'author_email': 'matthieu.gouel@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
