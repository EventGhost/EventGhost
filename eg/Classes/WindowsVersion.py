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

from .. import Cli

import platform
from collections import OrderedDict


WINDOWS_VERSIONS = OrderedDict()
WINDOWS_VERSIONS["XP"] = [[5, 1], [5, 2]]
WINDOWS_VERSIONS["XP32"] = [5, 1]
WINDOWS_VERSIONS["XP64"] = [5, 2]
WINDOWS_VERSIONS["VISTA"] = [6, 0]
WINDOWS_VERSIONS["7"] = [6, 1]
WINDOWS_VERSIONS["8"] = [[6, 2], [6, 3]]
WINDOWS_VERSIONS["80"] = [6, 2]
WINDOWS_VERSIONS["81"] = [6, 3]
WINDOWS_VERSIONS["10"] = [10, 0]


def _compare(opp, other):
    if isinstance(other, int):
        other = str(other)
    else:
        other = other.upper()

    if other not in WINDOWS_VERSIONS.keys():
        raise WindowsVersionError(other)

    ver = platform.version().split('.')
    this = [int(ver[0]), int(ver[1])]

    versions = WINDOWS_VERSIONS[other]
    if other not in ("8", "XP"):
        versions = [versions]

    if opp == '>':
        return any(this > version for version in versions)
    elif opp == '<':
        return any(this < version for version in versions)
    elif opp == '<=':
        return any(this <= version for version in versions)
    elif opp == '>=':
        return any(this >= version for version in versions)
    elif opp == '==':
        return any(this == version for version in versions)
    elif opp == '!=':
        return any(this != version for version in versions)


class WindowsVersionError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return (
            "'{0}' is not in the list of supported values:\n"
            "\t{1}\n".format(self.msg, ", ".join(WINDOWS_VERSIONS.keys()))
        )


class WindowsVersion:
    """
    A convenience module for checking the windows version.

    In addition to the *IsXY()* methods, you can use comparison like this:

    ``eg.WindowsVersion OPERATOR "KEY"``

    ``OPERATOR`` is one of ``<``, ``<=``, ``==``, ``!=``, ``>=``, ``>``

    +-----------+--------------------------------------+
    | ``KEY``   | Windows version(s)                   |
    +===========+======================================+
    | ``XP``    | *all of XP32 and XP64*               |
    +-----------+--------------------------------------+
    | ``XP32``  | Windows XP,                          |
    |           | Windows XP 64-Bit Edition,           |
    |           | Windows Tablet PC,                   |
    |           | Windows Media Center Edition 2002,   |
    |           | Windows Media Center Edition 2004,   |
    |           | Windows Media Center Edition 2005    |
    +-----------+--------------------------------------+
    | ``XP64``  | Windows XP Professional x64 Edition, |
    |           | Windows Server 2003,                 |
    |           | Windows Server 2003 R2               |
    +-----------+--------------------------------------+
    | ``Vista`` | Windows Vista,                       |
    |           | Windows Server 2008                  |
    +-----------+--------------------------------------+
    | ``7``     | Windows 7,                           |
    |           | Windows Server 2008 R2               |
    +-----------+--------------------------------------+
    | ``8``     | *all of 80 and 81*                   |
    +-----------+--------------------------------------+
    | ``80``    | Windows 8,                           |
    |           | Windows Server 2012,                 |
    |           | Windows RT                           |
    +-----------+--------------------------------------+
    | ``81``    | Windows 8.1,                         |
    |           | Windows 2012 R2,                     |
    |           | Windows RT 8.1                       |
    +-----------+--------------------------------------+
    | ``10``    | Windows 10,                          |
    |           | Windows Server 2016                  |
    +-----------+--------------------------------------+

    |

    .. The above line gives some extra space after the table in the helpfile.
       References:
           https://msdn.microsoft.com/en-us/library/windows/desktop/ms724832(v=vs.85).aspx
           https://en.wikipedia.org/wiki/List_of_Microsoft_Windows_versions
           http://www.gaijin.at/lstwinver.php
    """

    def __eq__(self, other):
        # type: (str) -> bool
        """
        Checks if the installed Windows version is equal
        to *other* windows version.

        :type other: str
        :rtype: bool
        """
        return _compare('==', other)

    def __ne__(self, other):
        # type: (str) -> bool
        """
        Checks if the installed Windows version is not equal
        to *other* windows version.

        :type other: str
        :rtype: bool
        """
        return _compare('!=', other)

    def __gt__(self, other):
        # type: (str) -> bool
        """
        Checks if the installed Windows version is newer
        than *other* windows version.

        :type other: str
        :rtype: bool
        """
        return _compare('>', other)

    def __ge__(self, other):
        # type: (str) -> bool
        """
        Checks if the installed Windows version is newer or equal
        than *other* windows version.

        :type other: str
        :rtype: bool
        """
        return _compare('>=', other)

    def __lt__(self, other):
        # type: (str) -> bool
        """
        Checks if the installed Windows version is older
        than *other* windows version.

        :type other: str
        :rtype: bool
        """
        return _compare('<', other)

    def __le__(self, other):
        # type: (str) -> bool
        """
        Checks if the installed Windows version is older or equal
        than *other* windows version.

        :type other: str
        :rtype: bool
        """
        return _compare('<=', other)

    def __str__(self):
        # type: () -> str
        """
        Gives a string with the word 'Windows' followed by the (full)
        version number for the installed Windows.

        :rtype: str
        """
        return "{0} {1}".format(
            platform.system(),
            platform.version()
        )

    @staticmethod
    def GetVersion():
        # type: () -> list
        """
        Return the major and minor version number of the installed Windows.

        :rtype: list
        :return: [major, minor]

        """
        return platform.version().split('.')[:2]

    @staticmethod
    def IsXP():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows XP x86
        * Windows XP x64
        * Windows Server 2003
        * Windows 2003 R2
        * Windows Tablet PC
        * Windows Media Center Edition 2002
        * Windows Media Center Edition 2004
        * Windows Media Center Edition 2005

        :rtype: bool
        """
        return _compare('==', "XP")

    @staticmethod
    def IsXP32():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows XP x86
        * Windows Tablet PC
        * Windows Media Center Edition 2002
        * Windows Media Center Edition 2004
        * Windows Media Center Edition 2005

        :rtype: bool
        """
        return _compare('==', "XP32")

    @staticmethod
    def IsXP64():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows XP x64
        * Windows Server 2003
        * Windows 2003 R2

        :rtype: bool
        """
        return _compare('==', "XP64")

    @staticmethod
    def IsVista():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows Vista
        * Windows Server 2008

        :rtype: bool
        """
        return _compare('==', "Vista")

    @staticmethod
    def Is7():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows 7
        * Windows Server 2008 R2

        :rtype: bool
        """
        return _compare('==', "7")

    @staticmethod
    def Is8():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows 8
        * Windows 8.1
        * Windows Server 2012
        * Windows 2012 R2
        * Windows RT
        * Windows RT 8.1

        :rtype: bool
        """
        return _compare('==', "8")

    @staticmethod
    def Is80():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows 8
        * Windows Server 2012
        * Windows RT

        :rtype: bool
        """
        return _compare('==', "80")

    @staticmethod
    def Is81():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows 8.1
        * Windows 2012 R2
        * Windows RT 8.1

        :rtype: bool
        """
        return _compare('==', "81")

    @staticmethod
    def Is10():
        # type: () -> bool
        """
        Checks if installed Windows version is one of:

        * Windows 10
        * Windows Server 2016

        :rtype: bool
        """
        return _compare('==', "10")

if Cli.args.isMain:
    WindowsVersion = WindowsVersion()
