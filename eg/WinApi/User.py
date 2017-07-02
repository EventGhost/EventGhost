# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright C 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import win32api
import win32net
import platform


def NameSamCompatible():
    """
    Retrieves the domain/username of the current user.
    
    :rtype: str
    """
    return win32api.GetUserNameEx(win32api.NameSamCompatible)


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


def IsDomainLogin():
    """
    Retrieves if the logged in user is logged into a domain.

    :rtype: bool
    """
    return Domain() == platform.node()


def IsLocalAdmin():
    """
    Retrieves if the logged in user is a member of the local administrators 
    group.

    :rtype: bool
    """
    return 'Administrators' in Groups()


def IsDomainAdmin():
    """
    Retrieves if the logged in user is logged into a domain and if they are in 
    the administrators group of that domain. If the RPC service is not running
    this will return False.

    :rtype: bool
    """

    if Domain() == platform.node():
        return False
    else:
        try:
            return 'Administrators' in Groups(server=Domain())
        except win32net.error as err:
            if err[0] == 1722:
                return False
            else:
                raise
