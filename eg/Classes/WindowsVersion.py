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

"""
A convenience module for checking the windows version.
Functions:
    IsXP()
    IsVista()
    Is7()
    Is8()
    Is10()
"""

import sys
import wx

PI = wx.PlatformInformation()

WIN_10 = PI.CheckOSVersion(10, 0)
WIN_8 = False
WIN_7 = False
WIN_VISTA = False
WIN_XP = False

if not WIN_10:
    WIN_8 = PI.CheckOSVersion(6, 2) or PI.CheckOSVersion(6, 3)
if True not in (WIN_10, WIN_8):
    WIN_7 = PI.CheckOSVersion(6, 1)
if True not in (WIN_10, WIN_8, WIN_7):
    WIN_VISTA = PI.CheckOSVersion(6, 0)
if True not in (WIN_10, WIN_8, WIN_7, WIN_VISTA):
    WIN_XP = PI.CheckOSVersion(5, 1) or PI.CheckOSVersion(5, 2)


def IsXP():
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
    return WIN_XP


def IsVista():
    """
    Checks if Windows version is:
    Windows Vista
    Windows Server 2008
    :return: Bool
    """
    return WIN_VISTA


def Is7():
    """
    Checks if Windows version is:
    Windows 7
    Windows Server 2008 R2
    :return: Bool
    """
    return WIN_7


def Is8():
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
    return WIN_8


def Is10():
    """
    Checks if Windows version is:
    Windows 10
    Windows Server 2016
    :return: Bool
    """
    return WIN_10


WindowsVersion = sys.modules[__name__]
