# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['openapi2jsonschema']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'colorama>=0.4.1,<0.5.0',
 'jsonref>=0.2.0,<0.3.0',
 'pyyaml>=5.1,<6.0']

entry_points = \
{'console_scripts': ['openapi2jsonschema = openapi2jsonschema.command:default']}

setup_kwargs = {
    'name': 'openapi2jsonschema',
    'version': '0.9.1',
    'description': 'A utility to extract JSON Schema from a valid OpenAPI specification',
    'long_description': '# openapi2jsonschema\n\nA utility to extract [JSON Schema](http://json-schema.org/) from a\nvalid [OpenAPI](https://www.openapis.org/) specification.\n\n\n## Why\n\nOpenAPI contains a list of type `definitions` using a superset of JSON\nSchema. These are used internally by various OpenAPI compatible tools. I\nfound myself however wanting to use those schemas separately, outside\nexisting OpenAPI tooling. Generating separate schemas for types defined\nin OpenAPI allows for all sorts of indepent tooling to be build which\ncan be easily maintained, because the canonical definition is shared.\n\n\n## Installation\n\n`openapi2jsonschema` is implemented in Python. Assuming you have a\nPython intepreter and pip installed you should be able to install with:\n\n```\npip install openapi2jsonschema\n```\n\nThis has not yet been widely tested and is currently in a _works on my\nmachine_ state.\n\n\n## Usage\n\nThe simplest usage is to point the `openapi2jsonschema` tool at a URL\ncontaining a JSON (or YAML) OpenAPI definition like so:\n\n```\nopenapi2jsonschema https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json\n```\n\nThis will generate a set of schemas in a `schemas` directory. The tool\nprovides a number of options to modify the output:\n\n```\n$ openapi2jsonschema --help\nUsage: openapi2jsonschema [OPTIONS] SCHEMA\n\n  Converts a valid OpenAPI specification into a set of JSON Schema files\n\nOptions:\n  -o, --output PATH  Directory to store schema files\n  -p, --prefix TEXT  Prefix for JSON references (only for OpenAPI versions\n                     before 3.0)\n  --stand-alone      Whether or not to de-reference JSON schemas\n  --kubernetes       Enable Kubernetes specific processors\n  --strict           Prohibits properties not in the schema\n                     (additionalProperties: false)\n  --help             Show this message and exit.\n```\n\n\n## Example\n\nMy specific usecase was being able to validate a Kubernetes\nconfiguration file without a Kubernetes client like `kubectl` and\nwithout the server. For that I have a bash script shown below:\n\n```bash\n#!/bin/bash -xe\n\n# This script uses openapi2jsonschema to generate a set of JSON schemas\nfor\n# the specified Kubernetes versions in three different flavours:\n#\n#   X.Y.Z - URL referenced based on the specified GitHub repository\n#   X.Y.Z-standalone - de-referenced schemas, more useful as standalone\ndocuments\n#   X.Y.Z-local - relative references, useful to avoid the network\ndependency\n\nREPO="garethr/kubernetes=json-schema"\n\ndeclare -a arr=(1.6.6\n                1.6.5\n                1.6.4\n                1.6.3\n                1.6.2\n                1.6.1\n                1.6.0\n                1.5.6\n                1.5.4\n                1.5.3\n                1.5.2\n                1.5.1\n                1.5.0\n                )\n\nfor version in "${arr[@]}"\ndo\n    schema=https://raw.githubusercontent.com/kubernetes/kubernetes/v${version}/api/openapi-spec/swagger.json\n    prefix=https://raw.githubusercontent.com/${REPO}/master/v${version}/_definitions.json\n\n    openapi2jsonschema -o "${version}-standalone" --stand-alone "${schema}"\n    openapi2jsonschema -o "${version}-local" "${schema}"\n    openapi2jsonschema -o "${version}"" --prefix "${prefix}" "${schema}"\ndone\n```\n\nThe output from running this script can be seen in the accompanying\n[garethr/kubernetes-json-schema](https://github.com/garethr/kubernetes-json-schema).\n\n\n\n',
    'author': 'Gareth Rushgrove',
    'author_email': 'gareth@morethanseven.net',
    'url': 'https://github.com/garethr/openapi2jsonschema',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
