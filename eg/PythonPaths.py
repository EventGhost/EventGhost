# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import site
import winreg
from types import ModuleType


version = sys.version_info[:2]
currentDir = os.path.dirname(__file__.decode('mbcs'))
install_directory, folder_name = os.path.split(currentDir)

while not folder_name:
    install_directory, folder_name = os.path.split(install_directory)

mainDir = os.path.abspath(install_directory)
sitePackagesDir = os.path.join(
    mainDir,
    "lib%d%d" % version,
    "site-packages"
)

sys.path.insert(0, mainDir.encode('mbcs'))
sys.path.insert(1, sitePackagesDir.encode('mbcs'))

try:
    if "PYTHONPATH" in os.environ:
        for path in os.environ.get("PYTHONPATH").split(os.pathsep):
            site.addsitedir(path)

    key = winreg.HKEY_LOCAL_MACHINE

    subkey = r"SOFTWARE\Python\PythonCore\%d.%d\InstallPath" % version
    with winreg.OpenKey(key, subkey) as hand:
        site.addsitedir(
            os.path.join(
                winreg.QueryValue(hand, None),
                "Lib",
                "site-packages",
            )
        )
except:
    pass
