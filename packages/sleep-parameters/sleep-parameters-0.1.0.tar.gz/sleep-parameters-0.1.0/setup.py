# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sleep_parameters']

package_data = \
{'': ['*'], 'sleep_parameters': ['tests/*']}

setup_kwargs = {
    'name': 'sleep-parameters',
    'version': '0.1.0',
    'description': 'Calculates common sleep parameters defined by AASM',
    'long_description': '# sleep-parameters\nCalculates common sleep parameters defined by AASM\n',
    'author': 'Dagmar Krefting',
    'author_email': 'dagmar.krefting@htw-berlin.de',
    'url': 'https://cbmi.htw-berlin.de/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
