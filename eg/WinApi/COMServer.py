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

import eg
import os
import sys
import atexit
import pythoncom


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

    def TriggerEvent(self, eventString, payload=None):
        eg.TriggerEvent(eventString, payload)


    def BringToFront(self):
        eg.document.ShowFrame()


    def OpenFile(self, filePath):
        eg.document.Open(filePath)


    def InstallPlugin(self, filePath):
        eg.document.ShowFrame()
        eg.PluginInstall.Import(filePath)
    

# Patch win32com to use the gen_py directory in the programs
# application data directory instead of its package directory.
# When the program runs "frozen" it would not be able to modify
# the package directory
genPath = os.path.join(eg.configDir, "gen_py").encode('mbcs')
if not os.path.exists(genPath):
    os.makedirs(genPath)
import win32com
win32com.__gen_path__ = genPath
sys.modules["win32com.gen_py"].__path__ = [genPath]
import win32com.client
win32com.client.gencache.is_readonly = False

# Support for the COM-Server of the program
if hasattr(sys, "frozen"):
    pythoncom.frozen = 1

from win32com.server.register import RegisterClasses
import pywintypes
try:
    RegisterClasses(EventGhostCom, quiet=True)
except pywintypes.error, data:
    if data[0] != 5:
        raise
sys.coinit_flags = 2
from win32com.server import factory
try:
    __factory_infos = factory.RegisterClassFactories([EventGhostCom._reg_clsid_])
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

