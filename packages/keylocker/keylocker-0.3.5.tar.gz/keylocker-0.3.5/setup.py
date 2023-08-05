# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keylocker']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.4,<3.0', 'fire>=0.1.3,<0.2.0', 'pickleDB>=0.9.2,<0.10.0']

entry_points = \
{'console_scripts': ['keylocker = keylocker:main']}

setup_kwargs = {
    'name': 'keylocker',
    'version': '0.3.5',
    'description': 'Library with the CLI to save the encrypted secrets in the configuration file, but a transparent read and write the new settings in the app.',
    'long_description': '# Keylocker CLI\nLibrary with the CLI to save the encrypted secrets in the configuration file, but a transparent read and write the new settings in the app.\n\n## Simple usage in CLI:\n```\nkeylocker init\nkeylocker list\nkeylocker read <keyname>\nkeylocker remove <keyname>\nkeylocker write <keyname> <value>\n```\n\n## Simple usage in code:\n```\nfrom keylocker import Storage\nsecrets = Storage()\nprint(secrets[\'test\'])\n```\n\n## Simple usage in bash:\n```\nPYPIPASS="$(keylocker read pypi_password)"\nPYPIUSER="$(keylocker read pypi_user)"\npoetry publish --username "${PYPIUSER}" --password "${PYPIPASS}" --build\n```\n\n## Source Code:\n* [https://github.com/vpuhoff/keylocker](https://github.com/vpuhoff/keylocker)\n\n## Travis CI Deploys:\n* [https://travis-ci.com/vpuhoff/keylocker](https://travis-ci.com/vpuhoff/keylocker) [![Build Status](https://travis-ci.com/vpuhoff/keylocker.svg?branch=master)](https://travis-ci.com/vpuhoff/keylocker)\n',
    'author': 'vpuhoff',
    'author_email': 'vpuhoff@live.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
