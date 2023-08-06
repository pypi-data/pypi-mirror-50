# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['loopback']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'loopback',
    'version': '0.0.2',
    'description': 'Thread manager and decorator for asynchronous background function execution.',
    'long_description': '# loopback\nThread manager and decorator for asynchronous background function execution\n\n## Simple usage in code:\n```\nfrom loopback import manager, loop\nfrom time import sleep\n\n@loop(manager, interval = 1)\ndef threaded_function(arg):\n    print("running ")\n    sleep(arg)\n    return \'OK\'\n\n\nwhile True:\n    print(threaded_function(4))\n    sleep(1)\n```\n\n## Source Code:\n* [https://github.com/vpuhoff/loopback](https://github.com/vpuhoff/loopback)\n\n## Travis CI Deploys:\n* [https://travis-ci.com/vpuhoff/loopback](https://travis-ci.com/vpuhoff/loopback) [![Build Status](https://travis-ci.com/vpuhoff/loopback.svg?branch=master)](https://travis-ci.com/vpuhoff/loopback)\n',
    'author': 'vpuhoff',
    'author_email': 'vpuhoff@live.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
