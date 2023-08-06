# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['j2dx', 'j2dx.win.ViGEm.x64', 'j2dx.win.ViGEm.x86']

package_data = \
{'': ['*'], 'j2dx': ['nix/*', 'win/*', 'win/ViGEm/*']}

install_requires = \
['eventlet>=0.25,<0.26', 'python-socketio>=4.2,<5.0', 'qrcode>=6.1,<7.0']

extras_require = \
{':sys_platform == "linux"': ['evdev>=1.2,<2.0'],
 ':sys_platform == "win32"': ['colorama>=0.4,<0.5']}

entry_points = \
{'console_scripts': ['j2dx = j2dx:main']}

setup_kwargs = {
    'name': 'j2dx',
    'version': '0.1.0',
    'description': 'Use your Android phone as a virtual Xbox 360 controller or DualShock 4 gamepad on your Windows or Linux PC. This is the server that runs on Windows or Linux.',
    'long_description': "# Joy2DroidX\n\n![Joy2DroidX](assets/screenshot.png)\n\nJoy2DroidX allows you to use your Android device as a\nvirtual Xbox 360 controller or DualShock 4 gamepad.\n\nIt consists of a server that runs on Windows and Linux\nand an Android app. While there's nothing preventing the\napp from running on any Android device, it's been only\ntested on Android phones.\n\n\n### Server\n\nThe server (this app) listens for input from connected\nAndroid devices and manages creation/deletion of virtual devices.\nIt uses UInput on Linux and [ViGEm](https://github.com/ViGEm) on Windows.\n\nWhile running the server *does not* require any special\nprivileges, the initial setup (setting UInput permissions on Linux and installing driver on Windows) *requires root/administrator* access.\n\n### Client\n\nYou can find more information about the Android app as well the sources [here](https://github.com/OzymandiasTheGreat/Joy2DroidX).\n\n\n## Installation\n\nJoy2DroidX is distributed as a portable app on Windows and as an AppImage on Linux.\nYou can find latest versions on [releases page](https://github.com/OzymandiasTheGreat/Joy2DroidX-server/releases).\n\nAlternatively, if you have python 3 and pip setup, you can install from [pypi](https://pypi.org/project/j2dx/):\n\n```\npip install j2dx\n```\n\n\n## Usage\n\n### First run\n\nYou need to setup the system before the first run.\nJoy2DroidX provides a convenience command that does this for you, it however requires root/administrator access.\n\nJust run `j2dx --setup` as root or from administrator command prompt.\n\nOn Linux this will create a udev rule for UInput and add current user to `j2dx` group. If you're not using sudo or user detection fails for another reason, you can provide username as an argument to `--setup`.\nFor udev rules and group changes to take effect you'll have to restart your system.\n\nOn Windows this will download [ViGEmBus driver](https://github.com/ViGEm/ViGEmBus) and prompt you to install it.\nOnce the driver is setup you can use Joy2DroidX, no restart necessary.\n\n### Regular usage\n\nRun `j2dx` (on windows you can just double click `j2dx.exe`), scan QRCode from the Android app and that's it.\nEverything should just work. Switching device mode is done from the Android app.\n\nThe server should not need any extra configuration.\nIf you have an unsual network setup or default port is used by another process, there are a couple option you can modify:\n\n- `-p, --port` allows you to use a different port. Default is 8013.\n- `-H, --host` if hostname detection fails you can specify a hostname or your computers IP address.\n- `-d, --debug` you shouldn't need this one. If you do encounter bugs, run `j2dx -d` and open an issue with a link to debug output (use a gist or pastebin for this).\n",
    'author': 'Tomas Ravinskas',
    'author_email': 'tomas.rav@gmail.com',
    'url': 'https://github.com/OzymandiasTheGreat/Joy2DroidX-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
