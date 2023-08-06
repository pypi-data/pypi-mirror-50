# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyblast', 'pyblast.blast', 'pyblast.blast_bin', 'pyblast.utils']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.73,<2.0',
 'fire>=0.1.3,<0.2.0',
 'networkx>=2.3,<3.0',
 'termcolor>=1.1,<2.0']

entry_points = \
{'console_scripts': ['pyblast = pyblast:cli.main']}

setup_kwargs = {
    'name': 'pyblastbio',
    'version': '0.2.7',
    'description': '',
    'long_description': '\n[![travis build](https://img.shields.io/travis/jvrana/pyblast.svg)](https://travis-ci.org/jvrana/pyblast)\n[![Coverage Status](https://coveralls.io/repos/github/jvrana/pyblast/badge.svg?branch=master)](https://coveralls.io/github/jvrana/pyblast?branch=master)\n[![PyPI version](https://badge.fury.io/py/REPO.svg)](https://badge.fury.io/py/REPO)\n\n![module_icon](images/module_icon.png?raw=true)\n\n#### Build/Coverage Status\nBranch | Build | Coverage\n:---: | :---: | :---:\n**master** | [![travis build](https://img.shields.io/travis/jvrana/pyblast/master.svg)](https://travis-ci.org/jvrana/pyblast/master) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/pyblast/badge.svg?branch=master)](https://coveralls.io/github/jvrana/pyblast?branch=master)\n**development** | [![travis build](https://img.shields.io/travis/jvrana/pyblast/development.svg)](https://travis-ci.org/jvrana/pyblast/development) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/pyblast/badge.svg?branch=development)](https://coveralls.io/github/jvrana/pyblast?branch=development)\n\n**this repo is not longer active**\n\n# pyblast\n\nThis is a wrapper for other applications to run blast searches on SeqRecord objects and JSON objects.\nFeatures include:\n* Blast self installation\n* Alignment to circular queries, using either linear or circular subjects\n\n# Installation\n\nYou can install BLAST to the pyblast directory using the following command:\n\n```\npyblast install\n```\n\nThis will install it to pyblast/blast_bin. If you want BLAST installed somewhere else, move the *ncbi-blast-X.X.X+* folder\nto your desired location and add *path/to/ncbi-blast-X.X.X+/bin* to you $PATH. **PyBlast** will prefer to use the blast stored\nin your executable path. If it cannot find a blast executable there, it looks for it in that paths in the pyblast/blast_bin/_paths.txt.\nfile. _paths.txt is automatically updated when you run install_blast.py so theres no need to manage the paths manually.\n\nAfter installing and verifying the `blastn` command works from the cmd line,\n\n```\npip install pyblastbio\n```\n\n## Usage\n\nThis package is a python wrapper for the BLAST command line, intended to be run along with a microservice (e.g. Flask).\nThis package also includes a basic python-based installation script which is used in unit-testing.\n\n### Input options\n\n```python\n\nfrom pyblast import BioBlast\nfrom Bio.SeqRecord\n',
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': 'https://www.github.com/jvrana/pyblast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
