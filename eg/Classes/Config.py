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
import wx
import traceback
from types import ClassType, InstanceType

# Local imports

import PersistentData
from Version import Version
from .. import Cli
from ..Utils import GetClosestLanguage


_defaults = dict(
    version=Version.string,
    language=GetClosestLanguage(),
    autoloadFilePath=False,
    checkUpdate=True,
    checkPreRelease=False,
    colourPickerCustomColours=[(-1, -1, -1, 255) for n in range(16)],
    confirmDelete=True,
    defaultThreadStartTimeout=5.00,
    hideOnClose=False,
    hideOnStartup=False,
    lastUpdateCheckDate=None,
    lastUpdateCheckVersion=None,
    limitMemory=False,
    limitMemorySize=8,
    logActions=True,
    logDebug=False,
    logMacros=True,
    onlyLogAssigned=False,
    propResize=True,
    refreshEnv=False,
    showTrayIcon=True,
    useFixedFont=False
)


if not os.path.exists(Cli.args.configDir):
    try:
        os.makedirs(Cli.args.configDir)
    except:
        pass


class Config(PersistentData.PersistentDataBase):

    def __init__(self):
        self.__dict__ = _defaults
        self._fileLoadError = False
        self._configFilePath = os.path.join(Cli.args.configDir, "config.py")

        PersistentData.PersistentDataBase.__init__(self, self, '')

        if Cli.args.isMain:
            self.Load()

        self.version = Version.string

    def Load(self):
        if not os.path.exists(self._configFilePath):
            app = wx.App()
            dlg = wx.MessageDialog(
                None,
                message=(
                    'Configuration file does not exist.\n'
                    'Would you like to create a new file?\n%s\n\n'
                    % self._configFilePath
                ),
                caption='Configuration Load Error',
                style=wx.YES_NO | wx.ICON_QUESTION
            )

            answer = dlg.ShowModal()
            app.MainLoop()
            dlg.Destroy()
            app.ExitMainLoop()
            app.Destroy()

            if answer == wx.ID_NO:
                raise IOError('File %s not found.' % self._configFilePath)
            self.Save()

        try:
            namespace = {}
            with open(self._configFilePath, 'r') as f:
                exec(f.read(), namespace, namespace)

            def LoadConfig(cls, dct):
                for key in dct.keys():
                    if key.startswith('_'):
                        continue
                    value = dct[key]
                    if type(value) in (ClassType, InstanceType):
                        newCls = PersistentData.PersistentDataBase(cls, key)
                        LoadConfig(newCls, value.__dict__)
                        value = newCls
                    cls.__dict__[key] = value
            LoadConfig(self, namespace)

        except (IOError, SyntaxError):
            tb = traceback.format_exc()
            app = wx.App()
            dlg = wx.MessageDialog(
                None,
                message=(
                    'Configuration File did not load properly.\n\n'
                    '%s\n\n'
                    'Would you like to create a new file?\n\n'
                    'WARNING: This will overwrite the existing file\n'
                    '         %s\n\n'
                    % (str(tb), self._configFilePath)
                ),
                caption='Configuration Load Error',
                style=wx.YES_NO | wx.ICON_ERROR
            )

            answer = dlg.ShowModal()
            app.MainLoop()
            dlg.Destroy()
            app.ExitMainLoop()
            app.Destroy()

            if answer == wx.ID_YES:
                self.Save()
            else:
                traceback.print_exc()
                self._fileLoadError = True

    def Save(self):
        if self._fileLoadError:
            return

        configFile = open(self._configFilePath, 'w')

        self.SaveData(configFile.write, 0)
        configFile.close()

    def __repr__(self):
        objRepr = object.__repr__(self).split(' ')
        objRepr[0] = '<eg.config'
        return ' '.join(objRepr)
