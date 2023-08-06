# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pytest_mimesis']
install_requires = \
['mimesis>=3.1,<4.0', 'pytest>=4.2']

entry_points = \
{'pytest11': ['mimesis = pytest_mimesis']}

setup_kwargs = {
    'name': 'pytest-mimesis',
    'version': '1.0.1',
    'description': 'Mimesis integration with the pytest test runner',
    'long_description': "## pytest-mimesis\n\n\n[![Build Status](https://travis-ci.org/pytest-dev/pytest-mimesis.svg?branch=master)](https://travis-ci.org/pytest-dev/pytest-mimesis)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n[![Python Version](https://img.shields.io/pypi/pyversions/pytest-mimesis.svg)](https://pypi.org/project/pytest-mimesis/)\n\n**pytest-mimesis** is a pytest plugin that provides pytest fixtures for [Mimesis](https://github.com/lk-geimfari/mimesis) providers. This allows you to quickly and easily use randomized, dummy data as part of your test suite.\n\n\n## Installation\n\n```bash\npip install pytest-mimesis\n```\n\n## Examples\n\nUsing the personal provider as part of a test.\n\n```python\n# your_module/__init__.py\n\ndef validate_email(email):\n    # code that validates an e-mail address\n    return True\n```\n\n`tests/test_email.py`:\n\n```python\nfrom your_module import validate_email\n\ndef test_validate_email(mimesis):\n    assert validate_email(mimesis('email'))\n```\n\nSpecifying locales:\n\n```python\n@pytest.mark.parameterize('mimesis_locale', 'de')  # use German locale\ndef test_create_user(mimesis):\n    assert create_user(name=mimesis('full_name'))\n\n\n@pytest.mark.parameterize('mimesis_locale', ['de', 'en', 'jp'])  # test multiple locales\ndef test_add_phone(user, mimesis):\n    assert user.add_phone_number(name=mimesis('full_name'))\n```\n\n## Fixtures\n\nWe provide two public fixtures: `mimesis_locale` and `mimesis`.\nWhile `mimesis_locale` is just a string (like: `en`, `ru`),\n`mimesis` is an instance of `mimesis.schema.Field`.\n\nWe use caching of `mimesis` instances for different locales for the whole\ntest session, so creating new instances is cheap.\n\n\n## License\n\npytest-mimesis is licensed under the [MIT License](https://github.com/pytest-dev/pytest-mimesis/blob/master/LICENSE).\n",
    'author': 'Nikita Sobolev',
    'author_email': 'mail@sobolevn.me',
    'url': 'https://github.com/pytest-dev/pytest-mimesis',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
