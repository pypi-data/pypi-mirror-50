# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['just_start', 'just_start_urwid']

package_data = \
{'': ['*']}

install_requires = \
['pexpect>=4.6,<5.0', 'pydantic>=0.31,<0.32', 'toml>=0.10.0,<0.11.0']

extras_require = \
{'urwid': ['urwid>=2.0,<3.0']}

entry_points = \
{'console_scripts': ['just-start-term = just_start.client_example:main[term]',
                     'just-start-urwid = just_start_urwid:main[urwid]']}

setup_kwargs = {
    'name': 'just-start',
    'version': '0.5.0',
    'description': 'Just Start is a wrapper for Task Warrior with pomodoro support',
    'long_description': 'just-start\n==========\n\n|Build Status| |Coverage Status|\n\nAn app to defeat procrastination!\n\nIntroduction\n------------\n\nJust-Start is a to-do list application and productivity booster. It prevents\nyou from procrastinating (too much).\n\nThe program is a wrapper for TaskWarrior_ with a timer implementing the\n`Pomodoro Technique`_ (time management). It also draws a bit of inspiration from\nOmodoro_.\n\nFeatures:\n\n- Configurable pomodoro phase durations\n- Support for multiple configurations (a.k.a. *locations*) based on the current time and day of the week\n- Desktop notifications\n- Block time-wasting sites while you’re working\n\nInstallation\n------------\n\nSupported platforms:\n\n- Linux\n- macOS\n\nRequirements:\n\n- Python 3.7\n- TaskWarrior_ (latest)\n\nPick a client from the table below and run:\n\n.. code:: bash\n\n    $ pip install just-start[<client_name>]\n\nIf you pick urwid, you should run:\n\n.. code:: bash\n\n    $ pip install just-start[urwid]\n\nClients\n-------\n\n+--------------------+----------+------------------------------------------------------------+\n|Name                |Framework |Notes                                                       |\n+====================+==========+============================================================+\n|urwid (recommended) |Urwid_    |Inspired by Calcurse_. Similar to a graphical               |\n|                    |          |application, but in your terminal                           |\n+--------------------+----------+------------------------------------------------------------+\n|term                |Terminal  |Example client. Useful for seeing how to write a brand new  |\n|                    |(none)    |one but not intended for continuous usage                   |\n+--------------------+----------+------------------------------------------------------------+\n\nUsage\n-----\n\n.. code:: bash\n\n    $ just-start-<client_name>\n\nSo for the urwid client:\n\n.. code:: bash\n\n    $ just-start-urwid\n\nPress h to see a list of available user actions.\n\nDevelopment\n-----------\n\nIf you want to help out please install Poetry_, clone the repo and run:\n\n.. code:: bash\n\n    $ cd just-start/\n    $ poetry install\n\nThis will ensure you have both the development and install dependencies.\n\nIssues are tracked using `GitHub Issues`_\n\nRunning Tests\n-------------\n\nFirst, you’ll need the Development_ dependencies. Then, just issue the\nfollowing:\n\n.. code:: bash\n\n    $ coverage run --source=just_start,just_start_urwid -m pytest; coverage report\n\n.. |Build Status| image:: https://travis-ci.org/AliGhahraei/\n   just-start.svg?branch=master\n   :target: https://travis-ci.org/AliGhahraei/just-start\n.. |Coverage Status| image:: https://codecov.io/gh/AliGhahraei/just-start/branch\n   /master/graph/badge.svg\n   :target: https://codecov.io/gh/AliGhahraei/just-start\n\n.. _Calcurse: http://calcurse.org\n.. _GitHub Issues: https://github.com/AliGhahraei/just-start/issues\n.. _Omodoro: https://github.com/okraits/omodoro\n.. _Poetry: https://poetry.eustace.io/docs/\n.. _Pomodoro Technique: https://cirillocompany.de/pages/pomodoro-technique\n.. _release: https://github.com/AliGhahraei/just-start/releases\n.. _Taskwarrior: https://taskwarrior.org/\n.. _Urwid: http://urwid.org/\n',
    'author': 'Ali Ghahraei',
    'author_email': 'aligf94@gmail.com',
    'url': 'https://github.com/AliGhahraei/just-start/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
