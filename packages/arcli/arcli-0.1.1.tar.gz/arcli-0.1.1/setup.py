# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['arcli',
 'arcli.config',
 'arcli.exceptions',
 'arcli.terminal',
 'arcli.triggers',
 'arcli.worker',
 'arcli.worker.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1.2,<6.0.0',
 'click>=7.0,<8.0',
 'colorama>=0.4.1,<0.5.0',
 'gitpython>=2.1.13,<3.0.0',
 'pydantic[ujson]>=0.31.1,<0.32.0',
 'semantic_version>=2.6.0,<3.0.0']

entry_points = \
{'console_scripts': ['arcli = arcli.terminal.cli:cli']}

setup_kwargs = {
    'name': 'arcli',
    'version': '0.1.1',
    'description': 'A TravisCI inspired builder',
    'long_description': '<h3 align="center">Arcli</h3>\n\n<div align="center">\n\n  [![GitHub Issues](https://img.shields.io/github/issues/guiscaranse/arcli.svg)](https://github.com/guiscaranse/arcli/issues)\n  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/guiscaranse/arcli.svg)](https://github.com/guiscaranse/arcli/pulls)\n  [![License](https://img.shields.io/badge/license-Apache2.0-blue.svg)](/LICENSE)\n\n</div>\n\n---\n\n<p align="center"> Arcli is a lightweight cross-platform builder inspired by TravisCI. It can automate deploying aplications with a single command line, and is highly extensive.\n    <br> \n</p>\n\n## 📝 Table of Contents\n- [About](#about)\n- [Getting Started](#getting_started)\n- [Usage and definitions](#usage)\n- [Built Using](#built_using)\n- [Contributing](../CONTRIBUTING.md)\n\n## \U0001f9d0 About <a name = "about"></a>\nArcli started as a hobby and quickly evolved into something incredibly useful that I implement in my daily life. With Arcli you can write code routines to be executed at the time of a deployment, as well as optional steps that can be triggered by certain conditions.\n\n## 🏁 Getting Started <a name = "getting_started"></a>\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes.\n\n### Installing\nYou can install Arcli using pip \n\n```sh\npip install arcli\n```\n\nor by downloading one of our pre-compiled binaries.\n\n```sh\n# Download\nwget https://github.com/guiscaranse/arcli/releases/latest/download/arcli-linux_arm64.tar.gz\n# Extract\ntar arcli-linux_arm64.tar.gz\n# Make executable\nchmod u+x arcli\n```\n\nStart using it or add it to your `PATH` \n\n```sh\narcli run\n```\n\n## 🎈 Usage and Definitions <a name="usage"></a>\nArcli will try to find and read an Arcli File (`arcli.yml`) where it will parse and run it.\n\n### Arcli File\nAn Arcli file is an instruction file written in YAML. Arcli will interpret it, perform validations, and thus run the codes described.\n\nHere it is a sample Arcli file (more samples on `samples`).\n\n```yaml\narcli: 0.1\nos: linux\ndependencies:\n  - git\nenv:\n  - TEST=sampleenv\nruntime:\n  - \'echo Hello World\'\n  - $step checkgit\n  - \'echo Arcli End\'\nstep @checkgit:\n  trigger:\n    name: GitDiff\n    args: ["arcli/*.py"]\n  script:\n    - \'echo Python Files Modified\'\n```\n\n#### Arcli file definitions\n\n| Key          | Type  | Optional | Description                                                                                                      |\n|--------------|-------|----------|------------------------------------------------------------------------------------------------------------------|\n| arcli        | float | No       | Refers to the version of Arcli that that file was made, it is possible to use Semantic Versioning for this field |\n| os           | str   | Yes      | Which operating system this file was made to run [`linux`, `osx`, `windows`, `any` (default)]                    |\n| dependencies | list  | Yes      | Which executables this file will need to use                                                                     |\n| env          | list  | Yes      | List of environment variables that will be injected at runtime.                                                  |\n| runtime      | list  | No       | List of main commands to be executed by Arcli. You can reference steps using `$step [step name]`                 |\n\n#### Step and Triggers definitions\nSteps are separate blocks of code that can be executed under certain circumstances when triggered by Triggers.\n\nThis is how a step look like:\n\n```yaml\nstep @checkgit:\n  trigger:\n    name: GitDiff\n    args: ["arcli/*.py"]\n  script:\n    - \'echo Python Files Modified\'\n```\n\n| Key     | Type | Optional | Description                                                                                                                                           |\n|---------|------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|\n| step    | str  | No       | It will be used to refer to the step in the runtime, you must name it after the @. Example: `step @mystep`                                            |\n| trigger | obj  | Yes      | Not all steps need to have a trigger, in the absence of a trigger it will always be executed. You can see the triggers available in `arcli/triggers`. |\n| script  | list | Yes      | Code to be executed if the step is valid (trigger is triggered or trigger is missing)                                                                 |\n\nThis is how a trigger looks like:\n\n```yaml\ntrigger:\n  name: GitDiff\n  args: ["arcli/*.py"]\n  options:\n    autopull: true\n```\n\n| Key     | Type | Optional | Description                                                                    |\n|---------|------|----------|--------------------------------------------------------------------------------|\n| name    | str  | No       | It will be used to identify the trigger, it must be the same as the class name |\n| args    | list | Yes      | Arguments that can be passed at the time of executing the trigger              |\n| options | obj  | Yes      | Advanced options that can contain keys and values to be passed to the trigger  |\n\nTriggers documentation can be found in each respective trigger file.\n\n\n## ⛏️ Built Using <a name = "built_using"></a>\n- [Python](https://www.python.org/) - Python\n- [Click](https://click.palletsprojects.com/en/master/) - CLI Framework\n- [Nuitka](http://nuitka.net) - Binaries generator',
    'author': 'Guilherme Scaranse',
    'author_email': None,
    'url': 'https://github.com/guiscaranse/arcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
