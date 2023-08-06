# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['vvtool', 'vvtool.migrations', 'vvtool.migrations.data']

package_data = \
{'': ['*']}

install_requires = \
['alley>=0.0.3,<0.0.4',
 'click>=7.0,<8.0',
 'coverage>=4.5,<5.0',
 'importlib_resources>=1.0,<2.0',
 'mongoengine>=0.18.2,<0.19.0',
 'pylint>=2.3,<3.0',
 'pymongo>=3.8,<4.0']

entry_points = \
{'console_scripts': ['vvtool = vvtool.cli:cli']}

setup_kwargs = {
    'name': 'voteview-dev',
    'version': '0.1.3',
    'description': 'Voteview command-line interface',
    'long_description': '========\nOverview\n========\n\n.. start-badges\n\n.. list-table::\n    :stub-columns: 1\n\n    * - docs\n      - |docs|\n    * - tests\n      - | |travis|\n        |\n    * - package\n      - | |version| |wheel| |supported-versions| |supported-implementations|\n        | |commits-since|\n\n.. |docs| image:: https://readthedocs.org/projects/voteview-dev/badge/?style=flat\n    :target: https://readthedocs.org/projects/voteview-dev\n    :alt: Documentation Status\n\n\n.. |travis| image:: https://img.shields.io/travis/voteview/voteview-dev/master\n    :alt: Travis-CI Build Status\n    :target: https://travis-ci.org/voteview/voteview-dev\n\n.. |version| image:: https://img.shields.io/pypi/v/voteview-dev.svg\n    :alt: PyPI Package latest release\n    :target: https://pypi.org/pypi/voteview-dev\n\n.. |commits-since| image:: https://img.shields.io/github/commits-since/voteview/voteview-dev/v0.1.3.svg\n    :alt: Commits since latest release\n    :target: https://github.com/voteview/voteview-dev/compare/v0.1.3...master\n\n.. |wheel| image:: https://img.shields.io/pypi/wheel/voteview-dev.svg\n    :alt: PyPI Wheel\n    :target: https://pypi.org/pypi/voteview-dev\n\n.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/voteview-dev.svg\n    :alt: Supported versions\n    :target: https://pypi.org/pypi/voteview-dev\n\n.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/voteview-dev.svg\n    :alt: Supported implementations\n    :target: https://pypi.org/pypi/voteview-dev\n\n\n.. end-badges\n\nVoteview command-line interface.\n\n* Free software: GNU General Public License v3 (GPLv3)\n\nInstallation\n============\n\n::\n\n    pip install voteview-dev\n\nDocumentation\n=============\n\n\nhttps://voteview-dev.readthedocs.io/\n\n\nDevelopment\n===========\n\nTo run the all tests run::\n\n    tox\n\nNote, to combine the coverage data from all the tox environments run:\n\n.. list-table::\n    :widths: 10 90\n    :stub-columns: 1\n\n    - - Windows\n      - ::\n\n            set PYTEST_ADDOPTS=--cov-append\n            tox\n\n    - - Other\n      - ::\n\n            PYTEST_ADDOPTS=--cov-append tox\n',
    'author': 'Adam Boche',
    'author_email': 'aboche@ucla.edu',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
