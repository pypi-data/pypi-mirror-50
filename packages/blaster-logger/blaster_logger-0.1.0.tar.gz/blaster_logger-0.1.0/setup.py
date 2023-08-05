# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['blaster_logger']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'blaster-logger',
    'version': '0.1.0',
    'description': '',
    'long_description': "## Blaster Logger\nTurn-key logging solution based on [loguru](https://github.com/Delgan/loguru)\n\n### Installation\n\n```bash\npip install blaster_logger\n```\n\n### Usage\n\n#### As logger\n```python\nfrom blaster_logger import log\n\nlog.debug('This is DEBUG level message')\nlog.info('This is INFO level message')\nlog.warning('This is a warning')\nlog.error('This is an error message')\nlog.critical('This is a critical level message')\n\ntry:\n    raise RuntimeError('Error message')\nexcept RuntimeError as e:\n    log.trace(e) # This is a traceback log\n```\n\n#### As decorator\n```python\nfrom blaster_logger import log\n\n@log.this\ndef some_func(x):\n    return x * 2\n```\n\n",
    'author': 'MB',
    'author_email': 'mb@blaster.ai',
    'url': 'https://github.com/Blasterai/blaster-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
