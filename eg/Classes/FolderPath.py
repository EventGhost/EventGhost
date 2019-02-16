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

from os.path import join, split
from ctypes import c_int, create_unicode_buffer, HRESULT, windll
from ctypes.wintypes import DWORD, HANDLE, HWND, LPWSTR

import eg

GetTempPathW = windll.kernel32.GetTempPathW
GetTempPathW.restype = DWORD
GetTempPathW.argtypes = [DWORD, LPWSTR]

SHGetFolderPathW = windll.shell32.SHGetFolderPathW
SHGetFolderPathW.restype = HRESULT
SHGetFolderPathW.argtypes = [HWND, c_int, HANDLE, DWORD, LPWSTR]

SHGFP_TYPE_CURRENT = 0
MAX_PATH = 260
CSIDL_FLAG_DONT_VERIFY = 16384

# id's from https://installmate.com/support/im9/using/symbols/functions/csidls.htm
CSIDL = {
    'AdminTools': 48,
    'AltStartup': 29,
    'RoamingAppData': 26,
    'RecycleBin': 10,
    'CDBurning': 59,
    'CommonAdminTools': 47,
    'CommonAltStartup': 30,
    'ProgramData': 35,
    'PublicDesktop': 25,
    'PublicDocuments': 46,
    'PublicFavorites': 31,
    'PublicMusic': 53,
    'CommonOEMLinks': 58,
    'PublicPictures': 54,
    'CommonPrograms': 23,
    'CommonStartMenu': 22,
    'CommonStartup': 24,
    'CommonTemplates': 45,
    'PublicVideos': 55,
    'ComputersNearMe': 61,
    'Connections': 49,
    'ControlPanel': 3,
    'Cookies': 33,
    'Desktop': 16,
    'DesktopRoot': 0,
    'MyComputer': 17,
    'Favorites': 6,
    'Fonts': 20,
    'History': 34,
    'Internet': 1,
    'InternetCache': 32,
    'LocalAppData': 28,
    'Documents2': 12,
    'Music': 13,
    'Pictures': 39,
    'Videos': 14,
    'NetHood': 19,
    'Network': 18,
    'Documents': 5,
    'PhotoAlbums': 69,
    'Playlists': 63,
    'Printers': 4,
    'PrintHood': 27,
    'Profile': 40,
    'ProgramFiles': 38,
    'ProgramFilesX86': 42,
    'ProgramFilesCommon': 43,
    'ProgramFilesCommonX86': 44,
    'Programs': 2,
    'Recent': 8,
    'ResourceDir': 56,
    'ResourceDirLocalized': 57,
    'SampleMusic': 64,
    'SamplePlaylists': 65,
    'SamplePictures': 66,
    'SampleVideos': 67,
    'SendTo': 9,
    'StartMenu': 11,
    'Startup': 7,
    'System': 37,
    'SystemX86': 41,
    'Templates': 21,
    'Windows': 36,
}

BUFFER = create_unicode_buffer(MAX_PATH)
GetTempPathW(MAX_PATH, BUFFER)
temporaryFiles = BUFFER.value[:-1]


class FolderPath(object):

    __repr__ = object.__repr__

    def __init__(self):
        for name in CSIDL.keys():
            try:
                _ = self.__getattr__(name)
            except WindowsError:
                CSIDL.pop(name)

        self.__ALL__ = CSIDL.keys() + ["TemporaryFiles"]
        self.TemporaryFiles = temporaryFiles

    @property
    def mainDir(self):
        return eg.Cli.PythonPaths.mainDir

    @property
    def configDir(self):
        config_dir = join(
            self.RoamingAppData,
            eg.APP_NAME
        )

        if eg.Cli.args.configDir and config_dir != eg.Cli.args.configDir:
            config_dir = eg.Cli.args.configDir

        return config_dir

    @property
    def corePluginDir(self):
        return join(
            self.mainDir,
            "plugins"
        )

    @property
    def localPluginDir(self):
        if self.configDir == eg.Cli.args.configDir:
            return self.corePluginDir

        else:

            return join(
                self.ProgramData,
                eg.APP_NAME,
                'plugins'
            )

    @property
    def imagesDir(self):
        return join(
            self.mainDir,
            "images"
        )

    @property
    def languagesDir(self):
        return join(
            self.mainDir,
            "languages"
        )

    @property
    def sitePackagesDir(self):
        return eg.Cli.PythonPaths.sitePackagesDir

    def __getattr__(self, name):
        csidl = CSIDL[name]
        SHGetFolderPathW(
            0,
            csidl | CSIDL_FLAG_DONT_VERIFY,
            0,
            SHGFP_TYPE_CURRENT,
            BUFFER
        )
        path = BUFFER.value
        self.__dict__[name] = path
        return path
