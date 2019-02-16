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
from ctypes import c_int, create_unicode_buffer, HRESULT, windll
from ctypes.wintypes import DWORD, HANDLE, HWND, LPWSTR


version = sys.version_info[:2]
currentDir = os.path.dirname(__file__)
install_directory, folder_name = os.path.split(currentDir)

while not folder_name:
    install_directory, folder_name = os.path.split(install_directory)

mainDir = os.path.abspath(install_directory)
sitePackagesDir = os.path.join(
    mainDir,
    "lib%d%d" % version,
    "site-packages"
)

SHGFP_TYPE_CURRENT = 0
MAX_PATH = 260
CSIDL_FLAG_DONT_VERIFY = 16384

SHGetFolderPathW = windll.shell32.SHGetFolderPathW
SHGetFolderPathW.restype = HRESULT
SHGetFolderPathW.argtypes = [HWND, c_int, HANDLE, DWORD, LPWSTR]
BUFFER = create_unicode_buffer(MAX_PATH)

SHGetFolderPathW(
    0,
    35 | CSIDL_FLAG_DONT_VERIFY,
    0,
    SHGFP_TYPE_CURRENT,
    BUFFER
)

data_dir = os.path.join(BUFFER.value, 'EventGhost')
data_dir_site_packages = os.path.join(
    data_dir,
    'lib',
    'site-packages'
)
try:
    os.makedirs(data_dir_site_packages)
except WindowsError:
    pass

sys.path.insert(0, data_dir_site_packages)
sys.path.insert(1, mainDir)
sys.path.insert(2, sitePackagesDir)

try:
    # noinspection PyUnresolvedReferences
    import certifi
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
except ImportError:
    pass
