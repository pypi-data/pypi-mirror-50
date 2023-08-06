# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytest_assert_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytest-assert-utils',
    'version': '0.0.1',
    'description': 'Useful assertion utilities for use with pytest',
    'long_description': '# pytest-assert-utils\n\nHandy assertion utilities for use with pytest\n\n\n# Installation\n\n```bash\npip install pytest-assert-utils\n```\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'url': 'https://github.com/usePF/pytest-assert-utils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
