# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2019 EventGhost Project <http://www.eventghost.net/>
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

import win32net

import ctypes
from ctypes.wintypes import (
    INT,
    BOOLEAN,
    ULONG,
    BOOL
)

secur32 = ctypes.windll.Secur32
shell32 = ctypes.windll.Shell32
netapi32 = ctypes.windll.Netapi32


class ENUM(INT):
    pass


class EXTENDED_NAME_FORMAT(ENUM):
    # An unknown name type.
    NameUnknown = 0x00
    # The fully qualified distinguished name.
    # CN=Jeff Smith,OU=Users,DC=Engineering,DC=Microsoft,DC=Com
    NameFullyQualifiedDN = 0x01
    # A legacy account name (for example, Engineering\JSmith).
    # The domain-only version includes trailing backslashes (\).
    NameSamCompatible = 0x02
    # A "friendly" display name (for example, Jeff Smith).
    # The display name is not necessarily the defining relative
    # distinguished name (RDN).
    NameDisplay = 0x03
    # A GUID string that the
    # IIDFromString function returns
    # (for example, {4fa050f0-f561-11cf-bdd9-00aa003a77b6}).
    NameUniqueId = 0x04
    # The complete canonical name
    # (for example, engineering.microsoft.com/software/someone).
    # The domain-only version includes a trailing forward slash (/).
    NameCanonical = 0x05
    # The user principal name (for example, someone@example.com).
    NameUserPrincipal = 0x06
    # The same as NameCanonical except that the rightmost forward
    # slash (/) is replaced with a new line character (\n), even in
    # a domain-only case
    # (for example, engineering.microsoft.com/software\nJSmith).
    NameCanonicalEx = 0x07
    # The generalized service principal name
    # (for example, www/www.microsoft.com@microsoft.com).
    NameServicePrincipal = 0x08
    # The DNS domain name followed by a backward-slash and the SAM user name.
    NameDnsDomain = 0x09
    # The Users first name
    NameGivenName = 0x0A
    # The users last name
    NameSurname = 0x0B


# BOOLEAN SEC_ENTRY GetUserNameExW(
#   EXTENDED_NAME_FORMAT NameFormat,
#   LPWSTR               lpNameBuffer,
#   PULONG               nSize
# );
_GetUserNameExW = secur32.GetUserNameExW
_GetUserNameExW.restype = BOOLEAN


def GetUserNameExW(NameFormat):
    if not isinstance(NameFormat, EXTENDED_NAME_FORMAT):
        NameFormat = EXTENDED_NAME_FORMAT(NameFormat)

    lpNameBuffer = ctypes.create_unicode_buffer(255)
    nSize = ULONG(254)

    _GetUserNameExW(NameFormat, lpNameBuffer, ctypes.byref(nSize))

    return lpNameBuffer.value


def IsDomainLogin():
    """
    Retrieves if the logged in user is logged into a domain.

    :rtype: bool
    """

    if GetUserNameExW(EXTENDED_NAME_FORMAT.NameCanonical):
        return True

    return False


# BOOL IsUserAnAdmin();

_IsUserAnAdmin = shell32.IsUserAnAdmin
_IsUserAnAdmin.restype = BOOL


def IsLocalAdmin():
    """
    Retrieves if the logged in user is a member of the local administrators
    group.

    :rtype: bool
    """
    return bool(_IsUserAnAdmin())


def IsDomainAdmin():
    """
    Retrieves if the logged in user is logged into a domain and if they are in
    the administrators group of that domain. If the RPC service is not running
    this will return False.

    :rtype: bool
    """

    return IsDomainLogin() and IsLocalAdmin()


def NameSamCompatible():
    """
    Retrieves the domain/username of the current user.

    :rtype: str
    """
    return GetUserNameExW(EXTENDED_NAME_FORMAT.NameSamCompatible)


def Name():
    """
    Retrieves the username of the current user.

    :rtype: str
    """
    return NameSamCompatible().split('\\')[1]


def Domain():
    """
    Retrieves the domain of the current user.

    :rtype: str
    """
    return NameSamCompatible().split('\\')[0]


def Groups(user_name=Name(), server=None):
    """
    Retrieves direct and indirect group name the username is a member of for a
    specific computer/server. If no parameters are passed it will default to
    the current user and the local computer.

    :type user_name: str
    :type server: str
    :rtype: list
    """
    return win32net.NetUserGetLocalGroups(server, user_name)
