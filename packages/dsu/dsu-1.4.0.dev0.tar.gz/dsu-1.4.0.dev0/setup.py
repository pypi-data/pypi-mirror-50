# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dsu', 'dsu.automodel', 'dsu.features']

package_data = \
{'': ['*'], 'dsu.features': ['audio_helpers/*']}

install_requires = \
['ace>=0.3.2,<0.4.0',
 'causality>=0.0.9,<0.0.10',
 'cython>=0.29.13,<0.30.0',
 'gensim>=3.8,<4.0',
 'gym>=0.14.0,<0.15.0',
 'hpsklearn>=0.1.0,<0.2.0',
 'keras>=2.2,<3.0',
 'lifelines>=0.22.3,<0.23.0',
 'nltk>=3.4,<4.0',
 'numpy>=1.17,<2.0',
 'optunity>=1.1,<2.0',
 'ortools>=7.3,<8.0',
 'patsy>=0.5.1,<0.6.0',
 'pymc>=2.3,<3.0',
 'robustats>=0.1.2,<0.2.0',
 'scikit-MDR>=0.4.4,<0.5.0',
 'scikit-build>=0.10.0,<0.11.0',
 'scikit-data>=0.1.3,<0.2.0',
 'scikit-gof>=0.1.3,<0.2.0',
 'scikit-image>=0.15.0,<0.16.0',
 'scikit-learn>=0.21.3,<0.22.0',
 'scikit-surprise>=1.0,<2.0',
 'scipy>=1.3,<2.0',
 'seqlearn>=0.2.0,<0.3.0',
 'spacy>=2.1,<3.0',
 'statsmodels>=0.10.1,<0.11.0',
 'tensorflow>=1.14,<2.0',
 'tpot>=0.10.2,<0.11.0',
 'tsfresh>=0.12.0,<0.13.0',
 'umap>=0.1.1,<0.2.0',
 'xgboost>=0.90.0,<0.91.0']

setup_kwargs = {
    'name': 'dsu',
    'version': '1.4.0.dev0',
    'description': '',
    'long_description': None,
    'author': 'Nandhini Anand',
    'author_email': 'cattykatrina4@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
