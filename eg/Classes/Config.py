# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import eg
import wx
import os
import sys
from os.path import exists
from types import ClassType, InstanceType


LOCALE = wx.Locale()


class Section:

    def __init__(self, defaults=None):
        if defaults:
            for key, value in defaults.__dict__.iteritems():
                if type(value) == ClassType:
                    setattr(self, key, Section(value))
                elif not hasattr(self, key):
                    setattr(self, key, value)


    def SetDefault(self, key, default):
        if key not in self.__dict__:
            setattr(self, key, Section(default))
        else:
            section = self.__dict__[key]
            for key2, value in default.__dict__.iteritems():
                if not hasattr(section, key2):
                    setattr(section, key2, value)
        return getattr(self, key)



def MakeSectionMetaClass(dummyName, dummyBases, dct):
    section = Section()
    section.__dict__ = dct
    return section


def RecursivePySave(obj, fileWriter, indent=""):
    objDict = obj.__dict__
    keys = objDict.keys()
    keys.sort()
    classKeys = []
    for key in keys:
        if key.startswith("_"):
            continue
        value = objDict[key]
        if type(value) == ClassType:
            classKeys.append(key)
        elif type(value) == InstanceType:
            classKeys.append(key)
        else:
            line = indent + key + " = " + repr(value) + "\n"
            fileWriter(line)
    for key in classKeys:
        value = objDict[key]
        fileWriter(indent + "class " + key + ":\n")
        RecursivePySave(value, fileWriter, indent + "    ")




class Config(Section):
    revision = 0
    if LOCALE.GetLanguageName(LOCALE.GetSystemLanguage()) == 'German':
        language = 'de_DE'
    else:
        language = 'en_EN'
    autoloadFilePath = False
    checkUpdate = False
    colourPickerCustomColours = [(-1, -1, -1, 255) for n in range(16)]
    confirmDelete = True
    defaultThreadStartTimeout = 5.00
    hideOnClose = False
    hideOnStartup = False
    lastUpdateCheckDate = None
    limitMemory = False
    limitMemorySize = 8
    logActions = True
    logMacros = True
    onlyLogAssigned = False
    propResize = True
    refreshEnv = False
    scrollLog = True
    startWithWindows = True
    useFixedFont = False

    class plugins: #pylint: disable-msg=C0103
        pass


    def __init__(self):
        Section.__init__(self)
        configDir = eg.configDir
        if not os.path.exists(configDir):
            os.makedirs(configDir)
        configFilePath = os.path.join(configDir, "config.py")
        self._configFilePath = configFilePath

        # BUG: of the python function 'ExecFile'. It doesn't handle unicode
        # filenames right.
        configFilePath = configFilePath.encode(sys.getfilesystemencoding())

        if exists(configFilePath):
            try:
                eg.ExecFile(
                    configFilePath,
                    {"__metaclass__": MakeSectionMetaClass},
                    self.__dict__
                )
            except:
                if eg.debugLevel:
                    raise
        else:
            eg.PrintDebugNotice('File "%s" does not exist.' % configFilePath)
            eg.Utils.UpdateStartupShortcut(self.startWithWindows)
        if self.language == "Deutsch":
            self.language = "de_DE"


    def Save(self):
        self.revision = eg.revision
        configFile = open(self._configFilePath, 'w+')
        RecursivePySave(self, configFile.write)
        configFile.close()

