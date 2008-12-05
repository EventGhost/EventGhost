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
import threading
import asyncore
from functools import partial


def InitPil():
    """Initialize PIL's Image module."""
    import Image
    import PngImagePlugin
    import JpegImagePlugin
    import BmpImagePlugin
    import GifImagePlugin
    Image._initialized = 2  
        
        
def InitComTypes():
    #Bit of a dance to force comtypes generated interfaces in to our directory
    import comtypes.client
    genPath = os.path.join(eg.configDir, "cgen_py").encode('mbcs')
    if not os.path.exists(genPath):
        os.makedirs(genPath)
    genInitPath = os.path.join(
        eg.configDir, 
        "cgen_py", "__init__.py"
    ).encode('mbcs')
    if not os.path.exists(genInitPath):
        ofi = open(genInitPath, "w")
        ofi.write("# comtypes.gen package, directory for generated files.\n")
        ofi.close()
    
    comtypes.client.gen_dir = genPath
    import comtypes
    sys.path.insert(0, eg.configDir)
    comtypes.gen = __import__("cgen_py", globals(), locals(), [])
    sys.modules["comtypes.gen"] = comtypes.gen
    del sys.path[0]
    import comtypes.client._generate
    comtypes.client._generate.__verbose__ = False

        
def InitPathesAndBuiltins():
    
    sys.path.append(
        os.path.abspath("lib%d%d\\site-packages" % sys.version_info[:2])
    )
    sys.path.append(os.getcwdu())
    
    import cFunctions
    sys.modules["eg.cFunctions"] = cFunctions
    
    # add 'wx' to the builtin name space of every module
    import __builtin__
    import wx
    __builtin__.__dict__["wx"] = wx
        
    # we create a package 'pluginImport' and set its path to the plugin-dir
    # so we can simply use __import__ to load a plugin file 
    pluginPackage = imp.new_module("pluginImport")
    pluginPackage.__path__ = [eg.PLUGIN_DIR]
    sys.modules["pluginImport"] = pluginPackage

    # replace builtin raw_input() with a small dialog
    def raw_input(prompt=None):
        return eg.CallWait(
            partial(eg.SimpleInputDialog.CreateModal, prompt)
        )
    __builtin__.raw_input = raw_input

    # replace builtin input() with a small dialog
    def input(prompt=None):
        return eval(raw_input(prompt))
    __builtin__.input = input
    
    
def Init():
    from greenlet import greenlet
    eg.Greenlet = greenlet
    eg.mainGreenlet = greenlet.getcurrent()
    
    from WinApi.SendKeys import SendKeysParser
    eg.SendKeys = SendKeysParser()
    
    import WinApi.COMServer

    
def InitGui():
    InitComTypes()
    # create a global asyncore loop thread
    # TODO: Only start if asyncore is requested
    eg.dummyAsyncoreDispatcher = None
    eg.RestartAsyncore()
    threading.Thread(target=asyncore.loop, name="AsyncoreThread").start()

    #import eg.WinApi.COMServer
    
    eg.scheduler.start()
    eg.messageReceiver.Start()

    eg.document = eg.Document()
    eg.taskBarIcon = eg.TaskBarIcon()
    eg.SetProcessingState = eg.taskBarIcon.SetProcessingState
    
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
    eg.dummyAsyncoreDispatcher.close()
    
    eg.PrintDebugNotice("shutting down")
    eg.config.Save()
    eg.messageReceiver.Close()

