# This file is part of EventGhost.
# Copyright (C) 2007 Lars-Peter Voss <bitmonster@eventghost.org>
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

from ctypes import create_unicode_buffer, windll, HRESULT, c_int
from ctypes.wintypes import HWND, HANDLE, DWORD, LPWSTR

GetTempPathW = windll.kernel32.GetTempPathW
GetTempPathW.restype = DWORD
GetTempPathW.argtypes = [DWORD, LPWSTR]

SHGetFolderPathW = windll.shell32.SHGetFolderPathW
SHGetFolderPathW.restype = HRESULT
SHGetFolderPathW.argtypes = [HWND, c_int, HANDLE, DWORD, LPWSTR]

SHGFP_TYPE_CURRENT = 0
MAX_PATH = 260
CSIDL_FLAG_DONT_VERIFY = 16384

CSIDL = {
    'AdminTools': 48,
    'Startup': 29,
    'RoamingAppData': 26,
    'CDBurning': 59,
    'CommonAdminTools': 47,
    'CommonStartup': 30,
    'ProgramData': 35,
    'PublicDesktop': 25,
    'PublicDocuments': 46,
    'Favorites': 31,
    'PublicMusic': 53,
    'CommonOEMLinks': 58,
    'PublicPictures': 54,
    'CommonPrograms': 23,
    'CommonStartMenu': 22,
    'CommonStartup': 24,
    'CommonTemplates': 45,
    'PublicVideos': 55,
    'Cookies': 33,
    'Desktop': 16,
    'Favorites': 6,
    'Fonts': 20,
    'History': 34,
    'InternetCache': 32,
    'LocalAppData': 28,
    'Documents': 12,
    'Music': 13,
    'Pictures': 39,
    'Videos': 14,
    'NetHood': 19,
    'Documents': 5,
    'PrintHood': 27,
    'Profile': 40,
    'ProgramFiles': 38,
    'ProgramFilesCommon': 43,
    'Programs': 2,
    'Recent': 8,
    'ResourceDir': 56,
    'SendTo': 9,
    'StartMenu': 11,
    'Startup': 7,
    'System': 37,
    'Templates': 21,
    'Windows': 36,
}

buffer = create_unicode_buffer(MAX_PATH)
GetTempPathW(MAX_PATH, buffer)
temporaryFiles = buffer.value[:-1]


class FolderPath(object):
    __ALL__ = CSIDL.keys() + ["TemporaryFiles"]
    TemporaryFiles = temporaryFiles
    __repr__ = object.__repr__
    
    def __getattr__(self, name):
        csidl = CSIDL[name]
        rc = SHGetFolderPathW(
            0, 
            csidl|CSIDL_FLAG_DONT_VERIFY, 
            0, 
            SHGFP_TYPE_CURRENT, 
            buffer
        )
        path = buffer.value
        self.__dict__[name] = path
        return path
    
        
        
