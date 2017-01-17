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

import atexit
import os
import pythoncom
import pywintypes
import sys
import win32com
import win32com.client
from win32com.server import factory
from win32com.server.register import RegisterClasses

# Local imports
import eg

class EventGhostCom:
    _public_methods_ = [
        'TriggerEvent',
        'BringToFront',
        'OpenFile',
        'InstallPlugin',
    ]
    _reg_progid_ = "EventGhost"
    _reg_clsid_ = "{7EB106DC-468D-4345-9CFE-B0021039114B}"
    _reg_clsctx_ = pythoncom.CLSCTX_LOCAL_SERVER

    def BringToFront(self):
        if eg.mainFrame is not None:
            eg.mainFrame.Iconize(False)
        else:
            eg.document.ShowFrame()

    def InstallPlugin(self, pluginFile):
        import wx
        wx.CallAfter(eg.PluginInstall.Import, pluginFile)

    def OpenFile(self, filePath):
        eg.document.Open(filePath)

    def TriggerEvent(self, eventString, payload=None, prefix=None):
        kwargs = {}
        if payload:
            kwargs['payload'] = payload
        if prefix:
            kwargs['prefix'] = prefix
        eg.TriggerEvent(eventString, **kwargs)


# Patch win32com to use the gen_py directory in the programs
# application data directory instead of its package directory.
# When the program runs "frozen" it would not be able to modify
# the package directory
genPath = os.path.join(eg.configDir, "gen_py").encode('mbcs')
if not os.path.exists(genPath):
    os.makedirs(genPath)
win32com.__gen_path__ = genPath
sys.modules["win32com.gen_py"].__path__ = [genPath]
win32com.client.gencache.is_readonly = False

# Support for the COM-Server of the program
if hasattr(sys, "frozen"):
    pythoncom.frozen = 1

try:
    RegisterClasses(EventGhostCom, quiet=True)
except pywintypes.error, data:
    if data[0] != 5:
        raise
sys.coinit_flags = 2
try:
    __factory_infos = factory.RegisterClassFactories(
        [EventGhostCom._reg_clsid_]
    )
except:
    __factory_infos = []
    eg.PrintError("RegisterClassFactories failed!")
#import win32api
#pythoncom.EnableQuitMessage(win32api.GetCurrentThreadId())
pythoncom.CoResumeClassObjects()

try:
    e = win32com.client.Dispatch("EventGhost")
except:
    sys.stderr.write("Unable to establish COM dispatch!\n")

def DeInit():
    # shutdown COM-Server
    factory.RevokeClassFactories(__factory_infos)
    pythoncom.CoUninitialize()

atexit.register(DeInit)
