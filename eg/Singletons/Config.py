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


import os
import sys
from os.path import exists
from types import ClassType, InstanceType

configFilePath = ''

locale = wx.Locale()


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



def _MakeSectionMetaClass(name, bases, dict):
    obj = Section()
    obj.__dict__ = dict
    return obj

    
def RecursivePySave(obj, fileWriter, indent=""):
    objDict = obj.__dict__
    keys = objDict.keys()
    keys.sort()
    classKeys = []
    for key in keys:
        if key.startswith("__"):
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
    buildNum = 0
    if locale.GetLanguageName(locale.GetSystemLanguage()) == 'German':
        language = 'de_DE'
    else:
        language = 'en_EN'
    startWithWindows = False
    hideOnStartup = False
    checkUpdate = False
    logActions = True
    logMacros = True
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
    lastUpdateCheckDate = None
    defaultThreadStartTimeout = 5.00
    colourPickerCustomColours = [(-1, -1, -1, 255) for n in range(16)]
    class plugins:
        pass


    def __init__(self):
        global configFilePath
        configDir = eg.CONFIG_DIR
        if not os.path.exists(configDir):
            os.makedirs(configDir)
            import shutil
            shutil.copy("Example.xml", os.path.join(configDir, "MyConfig.xml"))
        configFilePath = os.path.join(configDir, "config.py")
        execDict = {"__metaclass__": _MakeSectionMetaClass}
        
        # BUG: of the python function 'execfile'. It doesn't handle unicode
        # filenames right.
        configFilePath = configFilePath.encode(sys.getfilesystemencoding())
        if exists(configFilePath):
            try:
                execfile(configFilePath, execDict, self.__dict__)
            except:
                if eg.debugLevel:
                    raise
        else:
            eg.PrintDebugNotice('File "%s" does not exist.' % configFilePath)
        if self.language == "Deutsch":
            self.language = "de_DE"
    
    
    def Save(self):
        global configFilePath
        self.buildNum = eg.buildNum
        fd = open(configFilePath, 'w+')
        RecursivePySave(self, fd.write)
        fd.close()
