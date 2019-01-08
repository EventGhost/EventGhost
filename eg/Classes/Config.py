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

import os
import sys
from os.path import exists
from cStringIO import StringIO
from types import ClassType, InstanceType

# Local imports
import eg
from . import Translation

eg.debugLevel = 1

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


class Config(Section):
    version = eg.Version.string
    language = None
    autoloadFilePath = False
    checkUpdate = True
    checkPreRelease = False
    colourPickerCustomColours = [(-1, -1, -1, 255) for n in range(16)]
    confirmDelete = True
    datestamp = "%x"
    defaultThreadStartTimeout = 5.00
    hideOnClose = False
    hideOnStartup = False
    lastUpdateCheckDate = None
    lastUpdateCheckVersion = None
    limitMemory = False
    limitMemorySize = 8
    logActions = True
    logDebug = False
    logMacros = True
    onlyLogAssigned = False
    propResize = True
    refreshEnv = False
    showTrayIcon = True
    useFixedFont = False

    class plugins:  #pylint: disable-msg=C0103
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

        if self.language is None:
            self.language = Translation.get_windows_user_language()

        else:

            for country in Translation.countries:
                for language in country.wx_languages:
                    if language.iso_code == self.language:
                        self.language = language
                        break
                else:
                    continue

                break

            else:
                for country in Translation.countries:
                    for language in country.wx_languages:
                        if language.iso_code == 'en_US':
                            self.language = language
                            break
                    else:
                        continue

                    break

    def Save(self):
        self.version = eg.Version.string
        config_data = StringIO()
        language = self.language
        self.language = self.language.iso_code

        RecursivePySave(self, config_data.write)
        with open(self._configFilePath, 'w+') as config_file:
            config_file.write(config_data.getvalue())

        self.language = language


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
