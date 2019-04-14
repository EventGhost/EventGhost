# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2019 EventGhost Project <http://www.eventghost.org/>
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

import ntsecuritycon
import pywintypes
import win32api
import win32net
from win32net import NetUserModalsGet
from win32security import LookupAccountSid


# -------------------------------------------------------------------
# `LookupAliasFromRid` and `LookupUserGroupFromRid` from
# https://github.com/mhammond/pywin32/blob/master/win32/Demos/security/localized_names.py

def lookup_alias_from_rid(TargetComputer, Rid):
    # Sid is the same regardless of machine, since the well-known
    # BUILTIN domain is referenced.
    sid = pywintypes.SID()
    sid.Initialize(ntsecuritycon.SECURITY_NT_AUTHORITY, 2)

    for i, r in enumerate((ntsecuritycon.SECURITY_BUILTIN_DOMAIN_RID, Rid)):
        sid.SetSubAuthority(i, r)

    name, domain, typ = LookupAccountSid(TargetComputer, sid)
    return name


def lookup_user_group_from_rid(TargetComputer, Rid):
    # get the account domain Sid on the target machine
    # note: if you were looking up multiple sids based on the same
    # account domain, only need to call this once.
    umi2 = NetUserModalsGet(TargetComputer, 2)
    domain_sid = umi2['domain_id']

    sub_authority_count = domain_sid.GetSubAuthorityCount()

    # create and init new sid with acct domain Sid + acct Rid
    sid = pywintypes.SID()
    sid.Initialize(domain_sid.GetSidIdentifierAuthority(),
                   sub_authority_count + 1)

    # copy existing subauthorities from account domain Sid into
    # new Sid
    for i in range(sub_authority_count):
        sid.SetSubAuthority(i, domain_sid.GetSubAuthority(i))

    # append Rid to new Sid
    sid.SetSubAuthority(sub_authority_count, Rid)

    name, domain, typ = LookupAccountSid(TargetComputer, sid)
    return name


# -------------------------------------------------------------------

ADMIN_GROUP_NAME = lookup_alias_from_rid(None, ntsecuritycon.DOMAIN_ALIAS_RID_ADMINS)


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
    return ADMIN_GROUP_NAME in Groups()


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
            return ADMIN_GROUP_NAME in Groups(server=Domain())
        except win32net.error as err:
            if err[0] == 1722:
                return False
            else:
                raise
