# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['certificates']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['certificates = certificates.__main__:main']}

setup_kwargs = {
    'name': 'certificates',
    'version': '0.0.3',
    'description': 'Generate event certificates easily.',
    'long_description': '# certificates\n\nScript to generate event certificates easily.\n\n## Requirements\n\n* Inkscape (`apt install inkscape`)\n\n## How to install certificates\n\n```bash\npython setup.py install\n```\n\n## Usage\n\n```\nusage: certificates.py [-h] participants template\n\npositional arguments:\n  participants  csv filaname containing participants.\n  template      certificate template in svg format used to build.\n\noptional arguments:\n  -h, --help    show this help message and exit\n```\n\n## Examples\n\n`certificates participants.csv template.svg`\n\n## Authors\n\nCássio Botaro [(@cassiobotaro)](https://github.com/cassiobotaro)\n\nTiago Guimarães [(@tilacog)](https://github.com/tilacog)\n',
    'author': 'cassiobotaro',
    'author_email': 'cassiobotaro@gmail.com',
    'url': 'https://github.com/cassiobotaro/certificates',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
