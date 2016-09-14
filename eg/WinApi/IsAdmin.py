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

# Local imports
from Dynamic import (
    AllocateAndInitializeSid,
    byref,
    cast,
    create_string_buffer,
    DOMAIN_ALIAS_RID_ADMINS,
    DWORD,
    EqualSid,
    ERROR_INSUFFICIENT_BUFFER,
    ERROR_NO_TOKEN,
    FreeSid,
    GetCurrentProcess,
    GetCurrentThread,
    GetLastError,
    GetTokenInformation,
    HANDLE,
    OpenProcessToken,
    OpenThreadToken,
    POINTER,
    PSID,
    SECURITY_BUILTIN_DOMAIN_RID,
    SID_AND_ATTRIBUTES,
    SID_IDENTIFIER_AUTHORITY,
    TOKEN_GROUPS,
    TOKEN_QUERY,
    TokenGroups,
    WinError,
)

SECURITY_NT_AUTHORITY = 5

def IsAdmin():
    """
    Find out if the user (the owner of the current process) is a member of
    the administrators group on the local computer (not on the domain!).
    """
    # First we must open a handle to the access token for this thread.
    hThread = HANDLE()
    if not OpenThreadToken(
        GetCurrentThread(), TOKEN_QUERY, 0, byref(hThread)
    ):
        err = GetLastError()
        if err == ERROR_NO_TOKEN:
            # If the thread does not have an access token, we'll examine the
            # access token associated with the process.
            if not OpenProcessToken(
                GetCurrentProcess(), TOKEN_QUERY, byref(hThread)
            ):
                raise WinError()
        else:
            raise WinError(err)
    # Then we must query the size of the group information associated with
    # the token. Note that we expect a FALSE result from GetTokenInformation
    # because we've given it a NULL buffer. On exit cbTokenGroups will tell
    # the size of the group information.
    cbTokenGroups = DWORD()
    if GetTokenInformation(
        hThread, TokenGroups, None, 0, byref(cbTokenGroups)
    ):
        raise WinError()

    # Here we verify that GetTokenInformation failed for lack of a large
    # enough buffer.
    err = GetLastError()
    if err != ERROR_INSUFFICIENT_BUFFER:
        raise WinError(err)

    # Now we allocate a buffer for the group information.
    ptg = create_string_buffer(cbTokenGroups.value)

    # Now we ask for the group information again.
    # This may fail if an administrator has added this account to an additional
    # group between our first call to GetTokenInformation and this one.
    if not GetTokenInformation(
        hThread, TokenGroups, ptg, cbTokenGroups, byref(cbTokenGroups)
    ):
        raise WinError()

    # Now we must create a System Identifier for the Admin group.
    systemSidAuthority = SID_IDENTIFIER_AUTHORITY()
    systemSidAuthority.Value[5] = SECURITY_NT_AUTHORITY
    psidAdmin = PSID()
    if not AllocateAndInitializeSid(
            byref(systemSidAuthority),
            2,
            SECURITY_BUILTIN_DOMAIN_RID,
            DOMAIN_ALIAS_RID_ADMINS,
            0, 0, 0, 0, 0, 0,
            byref(psidAdmin)
    ):
        raise WinError()

    # Finally we'll iterate through the list of groups for this access
    # token looking for a match against the SID we created above.
    ptg = cast(ptg, POINTER(TOKEN_GROUPS))
    groups = cast(ptg.contents.Groups, POINTER(SID_AND_ATTRIBUTES))
    isAdmin = False
    for i in range(ptg.contents.GroupCount):
        if EqualSid(groups[i].Sid, psidAdmin.value):
            isAdmin = True
            break
    # Before we exit we must explicitly deallocate the SID we created.
    FreeSid(psidAdmin)
    return isAdmin

if __name__ == "__main__":
    print "Current user is administrator:", IsAdmin()
