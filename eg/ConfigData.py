# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
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

import wx
import Persistent
import os

configFilePath = ''
config = None

class DefaultConfig:
    buildNum = 0
    language = 'en_EN'
    startWithWindows = False
    hideOnStartup = False
    checkUpdate = False
    logActions = True
    onlyLogAssigned = False
    useAutoloadFile = True
    autoloadFilePath = os.path.join(
        wx.StandardPaths.Get().GetUserDataDir(),
        'MyConfig.xml'
    )
    storedBootTime = 0
    limitMemory = True
    limitMemorySize = 8
    confirmDelete = True
    class plugins:
        pass



locale = wx.Locale()
if locale.GetLanguageName(locale.GetSystemLanguage()) == 'German':
    DefaultConfig.language = 'de_DE'


def LoadConfig():
    global configFilePath, config
    configDir = wx.StandardPaths.Get().GetUserDataDir()
    if not os.path.exists(configDir):
        os.makedirs(configDir)
        import shutil
        shutil.copy("Example.xml", os.path.join(configDir, "MyConfig.xml"))
    configFilePath = os.path.join(configDir, "config.py")
    config = Persistent.PyLoad(configFilePath, DefaultConfig)
    if config.language == "Deutsch":
        config.language = "de_DE"
    return config


def SaveConfig():
    global configFilePath, config
    import eg
    config.buildNum = eg.buildNum
    Persistent.PySave(config, configFilePath)
