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
import wx
import sys
import os
import imp
import time
from functools import partial
from types import ModuleType


def InitPil():
    """Initialize PIL's Image module."""
    import Image
    import PngImagePlugin #IGNORE:W0612
    import JpegImagePlugin #IGNORE:W0612
    import BmpImagePlugin #IGNORE:W0612
    import GifImagePlugin #IGNORE:W0612
    Image._initialized = 2  


def InitPathesAndBuiltins():
    mainDir = os.path.abspath(os.path.join(os.path.dirname(eg.__file__), ".."))
    sys.path.append(mainDir)
    sys.path.append(
        os.path.join(mainDir, "lib%d%d" % sys.version_info[:2], "site-packages")
    )
    
    import cFunctions
    sys.modules["eg.cFunctions"] = cFunctions
    eg.cFunctions = cFunctions
    
    # add 'wx' to the builtin name space of every module
    import __builtin__
    __builtin__.wx = wx
        
    # we create a package 'PluginModule' and set its path to the plugin-dir
    # so we can simply use __import__ to load a plugin file 
    pluginPackage = imp.new_module("PluginModule")
    pluginPackage.__path__ = [eg.PLUGIN_DIR]
    sys.modules["PluginModule"] = pluginPackage

    # replace builtin raw_input() with a small dialog
    def RawInput(prompt=None):
        return eg.CallWait(
            partial(eg.SimpleInputDialog.CreateModal, prompt)
        )
    __builtin__.raw_input = RawInput

    # replace builtin input() with a small dialog
    def Input(prompt=None):
        return eval(RawInput(prompt))
    __builtin__.input = Input
    
    
def Init():    
    import WinApi.COMServer

    
def InitGui():
    #import eg.WinApi.COMServer
    
    eg.scheduler.start()
    eg.messageReceiver.Start()

    eg.document = eg.Document()
    
    if not (eg.config.hideOnStartup or eg.startupArguments.hideOnStartup):
        eg.document.ShowFrame()
        
    eg.actionThread.Start()

    eg.eventThread.startupEvent = eg.startupArguments.startupEvent
    
    config = eg.config

    startupFile = eg.startupArguments.startupFile
    if startupFile is None:
        startupFile = config.autoloadFilePath
    if startupFile and not os.path.exists(startupFile):
        eg.PrintError(eg.text.Error.FileNotFound % startupFile)
        startupFile = None
            
    eg.eventThread.Start()
    wx.CallAfter(
        eg.eventThread.Call, 
        eg.eventThread.StartSession, 
        startupFile
    )
    if config.checkUpdate:
        # avoid more than one check per day
        today = time.gmtime()[:3]
        if config.lastUpdateCheckDate != today:
            config.lastUpdateCheckDate = today
            wx.CallAfter(eg.CheckUpdate.Start)
            
    eg.Print(eg.text.MainFrame.Logger.welcomeText)

        
def DeInit():
    eg.PrintDebugNotice("stopping threads")
    eg.actionThread.CallWait(eg.actionThread.StopSession)
    eg.scheduler.Stop()
    eg.actionThread.Stop()
    eg.eventThread.Stop()
    
    eg.PrintDebugNotice("shutting down")
    eg.config.Save()
    eg.messageReceiver.Close()
    if eg.dummyAsyncoreDispatcher:
        eg.dummyAsyncoreDispatcher.close()

