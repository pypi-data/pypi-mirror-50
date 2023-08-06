# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['starlette_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['prometheus_client>=0.7,<0.8', 'starlette>=0.12.0']

setup_kwargs = {
    'name': 'starlette-prometheus',
    'version': '0.3.0',
    'description': 'Prometheus integration for Starlette',
    'long_description': '# Starlette Prometheus\n[![Build Status](https://img.shields.io/circleci/project/github/perdy/flama/master.svg)](https://circleci.com/gh/perdy/flama)\n[![codecov](https://codecov.io/gh/perdy/starlette-prometheus/branch/master/graph/badge.svg)](https://codecov.io/gh/perdy/starlette-prometheus)\n[![PyPI version](https://badge.fury.io/py/starlette-prometheus.svg)](https://badge.fury.io/py/starlette-prometheus)\n\n* **Version:** 0.2.0\n* **Status:** Production/Stable\n* **Author:** José Antonio Perdiguero López\n\n## Introduction\n\nPrometheus integration for Starlette.\n\n## Requirements\n\n* Python 3.6+\n* Starlette 0.9+\n\n## Installation\n\n```console\n$ pip install starlette-prometheus\n```\n\n## Usage\n\nA complete example that exposes prometheus metrics endpoint under `/metrics/` path.\n\n```python\nfrom starlette.applications import Starlette\nfrom starlette_prometheus import metrics, PrometheusMiddleware\n\napp = Starlette()\n\napp.add_middleware(PrometheusMiddleware)\napp.add_route("/metrics/", metrics)\n```\n\n## Contributing\n\nThis project is absolutely open to contributions so if you have a nice idea, create an issue to let the community \ndiscuss it.\n',
    'author': 'José Antonio Perdiguero López',
    'author_email': 'perdy@perdy.io',
    'url': 'https://github.com/PeRDy/starlette-prometheus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
