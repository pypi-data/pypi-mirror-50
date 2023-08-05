# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['instaffo_sklearn']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=0.13,<0.14',
 'numpy>=1.16,<2.0',
 'pandas>=0.24,<0.25',
 'scikit-learn>=0.21,<0.22',
 'scipy>=1.3,<2.0']

setup_kwargs = {
    'name': 'instaffo-scikit-learn',
    'version': '0.1.0rc1',
    'description': 'This project contains custom scikit-learn estimators that we use.',
    'long_description': '# instaffo-scikit-learn\n\ninstaffo-scikit-learn is a Python package that contains transformers and estimators that are compatible with the popular machine learning package [scikit-learn](https://github.com/scikit-learn/scikit-learn).\n\nscikit-learn is the foundation of many machine learning projects here at [Instaffo](https://instaffo.com/) and we are huge fans of the tool. As we sometimes reach the limits of what is possible out of the box, we regularly create custom classes that we have decided to make open source. Please check the [license](LICENSE) for more details.\n\nAre you curious about how we use technology to disrupt the recruiting industry? Visit our [tech blog](https://instaffo.tech/) or take a look at our [job board](https://instaffo-jobs.personio.de/).\n\n## Installation\n\n### Dependencies\n\ninstaffo-scikit-learn requires:\n\n- python (>= 3.6)\n- numpy (>= 1.16)\n- pandas (>= 0.24)\n- scikit-learn (>= 0.21)\n- scipy (>= 1.3)\n\nMore information about the dependencies can be found in the [pyproject.toml](pyproject.toml) file.\n\n### User Installation\n\nThe easiest way to install instaffo-scikit-learn is using `pip`:\n\n```\npip install instaffo-scikit-learn\n```\n\n## Changelog\n\nSee the [changelog](CHANGELOG.md) for a history of notable changes to instaffo-scikit-learn.\n\n## Development\n\nWe welcome new contributors to this project!\n\n### Source Code\n\nYou can check the latest sources with this command:\n\n```\ngit clone git@gitlab.com:InstaffoOpenSource/DataScience/instaffo-scikit-learn.git\n```\n\n### Dependencies\n\nTo work on this project, we recommend having the following tools installed:\n\n- [poetry](https://github.com/sdispater/poetry), for dependency management and packaging\n- [pyenv](https://github.com/pyenv/pyenv), for Python version managment.\n\n### Testing\n\nAfter installation, you can launch the test suite from root:\n\n```\npoetry run tox\n```\n\n### Linting\n\nYou can launch the linting suite from root:\n\n```\npoetry run black --check .\npoetry run pylint $(git ls-files | grep -E "*.py$")\n```\n\n## Help and Support\n\n### Communication\n\n- Jan-Benedikt Jagusch <jan@instaffo.de>\n- Nikolai Gulatz <nikolai@instaffo.de>\n\n## Acknowledgement\n\nThank you to [scikit-learn](https://scikit-learn.org/stable/) for their contribution to open source software!\n',
    'author': 'Instaffo GmbH',
    'author_email': 'info@instaffo.de',
    'url': 'https://instaffo.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
