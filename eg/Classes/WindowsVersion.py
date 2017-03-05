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

import platform


class WindowsVersion(object):
    """
    A convenience module for checking the windows version.

    Functions:
        IsXP()
        IsVista()
        Is7()
        Is8()
        Is80()
        Is81()
        Is10()

    Comparison:
        eg.WindowsVersion [<|<=|==|!=|>=|>] "[XP|Vista|7|8|80|81|10]"
            XP:    Windows XP
                   Windows Server 2003
                   Windows 2003 R2
                   Windows Tablet PC
                   Windows Media Center Edition 2002
                   Windows Media Center Edition 2004
                   Windows Media Center Edition 2005
            Vista: Windows Vista
                   Windows Server 2008
            7:     Windows 7
                   Windows Server 2008 R2
            8:     (80 and 81)
            80:    Windows 8
                   Windows Server 2012
                   Windows RT
            81:    Windows 8.1
                   Windows 2012 R2
                   Windows RT 8.1
            10:    Windows 10
                   Windows Server 2016
    """

    __docsort__ = (
        "IsXP, IsVista, Is7, Is8, Is80, Is81, Is10"
    )

    WIN_10 = [10, 0]
    WIN_81 = [6, 3]
    WIN_80 = [6, 2]
    WIN_7 = [6, 1]
    WIN_VISTA = [6, 0]
    WIN_XP64 = [5, 2]
    WIN_XP32 = [5, 1]

    class WindowsVersionError(Exception):
        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return (
                "'{0}' is not in the list of supported values:\n"
                "XP, Vista, 7, 8, 80, 81, 10\n".format(self.msg)
            )

    def __init__(self):
        ver = platform.version().split('.')
        self.THIS = [int(ver[0]), int(ver[1])]

    def _compare(self, opp, other):
        if opp == '<=':
            return self.THIS <= getattr(self, 'WIN_' + other.upper())
        elif opp == '>=':
            return self.THIS >= getattr(self, 'WIN_' + other.upper())
        elif other.upper() == 'XP':
            versions = [self.WIN_XP32, self.WIN_XP64]
        elif other == '8':
            versions = [self.WIN_80, self.WIN_81]
        else:
            versions = [getattr(self, 'WIN_' + other.upper())]

        if opp == '>':
            for i, version in enumerate(versions):
                versions[i] = self.THIS > version
        elif opp == '<':
            for i, version in enumerate(versions):
                versions[i] = self.THIS < version

        return versions == [True, True] or versions == [True]

    @staticmethod
    def check_os_value(val):
        if val.upper() not in ['XP', 'VISTA', '7', '8', '80', '81', '10']:
            raise WindowsVersion.WindowsVersionError(val)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        if not item.startswith('_') and not item.startswith('Is'):
            WindowsVersion.check_os_value(item)
            if len(item) == 2:
                item = item.upper()
            else:
                item = item.title()
            return getattr(self, 'Is' + item)()
        raise AttributeError(
            'eg.WindowsVersion does not have attribute ' + item
        )

    def __eq__(self, other):
        return getattr(self, other)

    def __ne__(self, other):
        self.check_os_value(other)
        return not getattr(self, other)

    def __gt__(self, other):
        return self._compare('>', other)

    def __ge__(self, other):
        return self._compare('>=', other)

    def __lt__(self, other):
        return self._compare('<', other)

    def __le__(self, other):
        return self._compare('<=', other)

    def __str__(self):
        return "{0} {1}".format(
            platform.system(),
            platform.version()
        )

    def IsXP(self):
        """
        Checks if Windows version is:

        Windows XP x86
        Windows XP x64
        Windows Server 2003
        Windows 2003 R2
        Windows Tablet PC
        Windows Media Center Edition 2002
        Windows Media Center Edition 2004
        Windows Media Center Edition 2005

        :return: Bool
        """
        return (
            self.THIS == self.WIN_XP32 or
            self.THIS == self.WIN_XP64
        )

    def IsVista(self):
        """
        Checks if Windows version is:

        Windows Vista
        Windows Server 2008

        :return: Bool
        """
        return self.THIS == self.WIN_VISTA

    def Is7(self):
        """
        Checks if Windows version is:

        Windows 7
        Windows Server 2008 R2

        :return: Bool
        """
        return self.THIS == self.WIN_7

    def Is8(self):
        """
        Checks if Windows version is:

        Windows 8
        Windows 8.1
        Windows Server 2012
        Windows 2012 R2
        Windows RT
        Windows RT 8.1

        :return: Bool
        """
        return (
            self.THIS == self.WIN_80 or
            self.THIS == self.WIN_81
        )

    def Is80(self):
        """
        Checks if Windows version is:

        Windows 8
        Windows Server 2012
        Windows RT

        :return: Bool
        """
        return self.THIS == self.WIN_80

    def Is81(self):
        """
        Checks if Windows version is:

        Windows 8.1
        Windows 2012 R2
        Windows RT 8.1

        :return: Bool
        """
        return self.THIS == self.WIN_81

    def Is10(self):
        """
        Checks if Windows version is:

        Windows 10
        Windows Server 2016

        :return: Bool
        """
        return self.THIS == self.WIN_10

WindowsVersion = WindowsVersion()
