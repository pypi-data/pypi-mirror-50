# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tinydb_dict']

package_data = \
{'': ['*']}

install_requires = \
['tinydb>=3.13,<4.0']

setup_kwargs = {
    'name': 'tinydb-dict',
    'version': '0.1.2',
    'description': 'Simple dict-like class for TinyDB',
    'long_description': "# tinydb-dict\nSimple dict-like class for TinyDB\n\n## Usage\n```python\nfrom tinydb import TinyDB\nfrom tinydb.storages import MemoryStorage\nfrom tinydb_dict import TinyDBDict\n\n# Pass any TinyDB argument to TinyDBDict\ndb_dict = TinyDBDict('db.json')\ndb_dict = TinyDBDict(storage=MemoryStorage)\n\n# Then use it as a dictionary\ndb_dict['key'] = 1\ndb_dict['key']  # 1\ndb_dict['key'] = 2\ndb_dict['key']  # 2\ndb_dict['unknown_key']  # KeyError: 'unknown_key'\n\n# You can also pass a TinyDB instance\ndb = TinyDB('db.json')\ndb_dict = TinyDBDict(tinydb=db)\n```\n",
    'author': 'Ali Ghahraei',
    'author_email': 'aligf94@gmail.com',
    'url': 'https://github.com/AliGhahraei/tinydb-dict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
