# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aws_arn_delete']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'aws-arn-delete',
    'version': '0.1.2',
    'description': 'Delete AWS resources based off its ARN',
    'long_description': '[![CircleCI](https://circleci.com/gh/cfarrend/aws-arn-delete.svg?style=svg)](https://circleci.com/gh/cfarrend/aws-arn-delete)\n\n# aws-arn-delete\nAmbitious attempt at deleting AWS resources by using Amazon Resource Name (ARN) format\n\n## Installing\n:)\n\n## Developing\n### Using Batect\nThis project uses https://github.com/charleskorn/batect as a default method of developing. Batect allows you to develop locally on your development machine without the need of installing all dependencies or setting up a virtual environment yourself. Batect is also integrated into the CI process so you can replicate the same steps done on building\n\n#### Requirements\n* Docker 17.06 or newer\n* Java 8 or newer\n* Mac OS X and Linux: `curl`\n* Windows: Windows 10 OS\n\n#### Setting up environment\n##### Mac OS / Linux\n```\n./batect <command>\n```\n\n##### Windows\n```\n.\\batect.cmd <command>\n```\n\n#### Useful Flags + Commands\n```\n$ ./batect --help\n<help prompt>\n\n$ ./batect --list-tasks\nAvailable tasks:\n- development-env\n```\n\n### Not using Batect\nFeel free to set up your development in your own way, however no support will be given setting up the project as it has been developed using `Batect`, it is also integrated into CI. We suggest to consider using it as it can help to contribute to the shared development environment as a whole, minimal setup is needed\n',
    'author': 'Christopher Farrenden',
    'author_email': 'cfarrend@gmail.com',
    'url': 'https://github.com/cfarrend/aws-arn-delete',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
