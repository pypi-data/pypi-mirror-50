# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mikm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mikm',
    'version': '0.1.2',
    'description': 'Library for converting miles in kilometers and kilometers in miles.',
    'long_description': '[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/serhii73/mikm/graphs/commit-activity)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![made-with-python](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![GitHub contributors](https://img.shields.io/github/contributors/serhii73/mikm.svg)](https://GitHub.com/serhii73/mikm/graphs/contributors/)\n[![GitHub stars](https://img.shields.io/github/stars/serhii73/mikm.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/serhii73/mikm/stargazers/)\n![GitHub forks](https://img.shields.io/github/forks/serhii73/mikm.svg?style=social)\n[![GitHub issues](https://img.shields.io/github/issues/serhii73/mikm.svg)](https://GitHub.com/serhii73/mikm/issues/)\n[![Build Status](https://travis-ci.org/serhii73/mikm.svg?branch=master)](https://travis-ci.org/serhii73/mikm)\n[![Maintainability](https://api.codeclimate.com/v1/badges/18c3e844245a2585f912/maintainability)](https://codeclimate.com/github/serhii73/mikm/maintainability)\n[![BCH compliance](https://bettercodehub.com/edge/badge/serhii73/mikm?branch=master)](https://bettercodehub.com/)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/serhii73/mikm.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/serhii73/mikm/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/serhii73/mikm.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/serhii73/mikm/context:python)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/007ff2464e874948add4154dc0f97e35)](https://app.codacy.com/app/serhii73/mikm?utm_source=github.com&utm_medium=referral&utm_content=serhii73/mikm&utm_campaign=Badge_Grade_Settings)\n[![Python 3](https://pyup.io/repos/github/serhii73/mikm/python-3-shield.svg)](https://pyup.io/repos/github/serhii73/mikm/)\n[![Updates](https://pyup.io/repos/github/serhii73/mikm/shield.svg)](https://pyup.io/repos/github/serhii73/mikm/)\n\n# Kilometers to Miles and  miles to kilometers conversion\n\n```\nconversion("1 km") return 0.62\n```\nand\n```\nconversion("1 mi") return 1.61\n```\n',
    'author': 'serhii73',
    'author_email': 'aserhii@protonmail.com',
    'url': 'https://github.com/serhii73/mikm',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
