# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from win32com.shell import shell, shellcon
import win32api

def get_path (folder_id):
    location = shell.SHGetSpecialFolderLocation(0, folder_id)
    return shell.SHGetPathFromIDList(location)


def get_path2 (folderId):
    location = shell.SHGetFolderPath(0, folderId, None, 0)
    return location

APPDATA = get_path2(shellcon.CSIDL_APPDATA)
try:
    STARTUP = shell.SHGetSpecialFolderPath(0, shellcon.CSIDL_STARTUP)
except:
    STARTUP = ""
PROGRAMFILES = get_path2(shellcon.CSIDL_PROGRAM_FILES)
TEMPDIR = win32api.GetTempPath()

