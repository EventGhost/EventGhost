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

import sys
import os
import imp
import time
import threading
from os.path import exists
import wx
import locale

class ResultDescriptor(object):
    def __init__(self):
        self.data = None
        
    def __set__(self, instance, value):
        self.data = value
        #print value
        
    def __get__(self, instance, owner):
        return self.data
    
    
    
class EventGhost(object):
    
    def result_fget(self):
        return self._result
    
    
    def result_fset(self, value):
        self._result = value
        
    result = property(result_fget, result_fset)
    
    
    def __init__(self, args):
        self._result = None
        global eg
        eg = self
        sys.modules["eg"] = self
        
        self.startupArguments = args
        self.debugLevel = args.debugLevel
        self.systemEncoding = locale.getdefaultlocale()[1]
        self.CallAfter = wx.CallAfter
        self.APP_NAME = "EventGhost"
        self.PLUGIN_DIR = os.path.abspath("plugins")
        self.APPDATA = eg.pathes.RoamingAppData
        self.STARTUP = eg.pathes.Startup
        self.PROGRAMFILES = eg.pathes.ProgramFiles
        self.TEMPDIR = eg.pathes.TemporaryFiles
        self.CONFIG_DIR = os.path.join(self.APPDATA, self.APP_NAME)
        
        # we create a package 'pluginImport' and set its path to the plugin-dir
        # se we can simply use __import__ to load a plugin file 
        pluginPackage = imp.new_module("pluginImport")
        pluginPackage.__path__ = [self.PLUGIN_DIR]
        sys.modules["pluginImport"] = pluginPackage
        
        # initialize PIL's Image module
        import Image
        import PngImagePlugin
        import JpegImagePlugin
        import BmpImagePlugin
        import GifImagePlugin
        Image._initialized = 2  
        
        # create a global asyncore loop thread
        import AsyncoreLoop
        self.RestartAsyncore = AsyncoreLoop.RestartAsyncore

        import Utils
        self.Utils = Utils
        self.LogIt = Utils.LogIt
        self.LogItWithReturn = Utils.LogItWithReturn
        self.TimeIt = Utils.TimeIt
        self.AssertNotMainThread = Utils.AssertNotMainThread
        self.AssertNotActionThread = Utils.AssertNotActionThread
        self.Bunch = Utils.Bunch
        self.EventHook = Utils.EventHook
        self.HexString = Utils.HexString
        self.ParseString = Utils.ParseString
        
        #self.document = None
        self.result = None
        self.event = None
        self.eventTable = {}
        self.eventTable2 = {}
        self.plugins = eg.Bunch()
        self.pluginClassInfo = {}
        
        self.globals = Utils.Bunch()
        self.globals.eg = self
        self.mainThread = threading.currentThread()
        self.onlyLogAssigned = False
        self.programCounter = None
        self.programReturnStack = []
        self.stopExecutionFlag = False
        self.lastFoundWindows = []
        self.currentConfigureItem = None
        self.pluginList = []
        self.actionList = []
                
        from Version import version, buildNum
        self.version = version
        self.buildNum = buildNum
        self.versionStr = "%s.%s" % (version, buildNum)

        # because some functions are only available if a wxApp instance
        # exists, we simply create it first
        self.app

        import Icons
        self.Icons = Icons
        
        self.Print = self.log.Print
        self.PrintError = self.log.PrintError
        self.PrintNotice = self.log.PrintNotice
        self.PrintTraceback = self.log.PrintTraceback
        self.PrintDebugNotice = self.log.PrintDebugNotice
            
        # redirect all wxPython error messages to our log
        class MyLog(wx.PyLog):
            def DoLog(self2, level, msg, timestamp):
                if (level < 6):# and not self.debugLevel:
                    return
                sys.stderr.write("Error%d: %s" % (level, msg))
        #wx.Log.SetActiveTarget(MyLog())

        self.onlyLogAssigned = eg.config.onlyLogAssigned
        
        from LanguageTools import LoadStrings, GetTranslation
        self.GetTranslation = GetTranslation
        self.text = LoadStrings(eg.config.language)

        from Text import Text
        Utils.SetClass(self.text, Text)

        import WinAPI
        sys.modules["eg.WinAPI"] = WinAPI
        self.WinAPI = WinAPI
        import cFunctions
        sys.modules["eg.cFunctions"] = cFunctions
            
        self.Exit = sys.exit
        from WinAPI.Shortcut import CreateShortcut
        self.CreateShortcut = CreateShortcut
        from WinAPI.serial import Serial
        self.SerialPort = Serial
        from WinAPI.SerialThread import SerialThread
        self.SerialThread = SerialThread
        
        from greenlet import greenlet
        self.Greenlet = greenlet
        
        import PluginTools
        self.OpenPlugin = PluginTools.OpenPlugin
        self.ClosePlugin = PluginTools.ClosePlugin

        # replace builtin input and raw_input with a small dialog
#        from Dialogs.SimpleInputDialog import (
#            GetSimpleRawInput, 
#            GetSimpleInput
#        )
#        sys.modules['__builtin__'].raw_input = GetSimpleRawInput
#        sys.modules['__builtin__'].input = GetSimpleInput

        from WinAPI.SerialThread import EnumSerialPorts as GetAllPorts
        self.SerialPort.GetAllPorts = classmethod(GetAllPorts)
        
        from WinAPI.SendKeys import SendKeys
        self.SendKeys = SendKeys
        
        
    def StartGui(self):
        import WinAPI.SendKeys
        import WinAPI.COMServer
        
        self.scheduler.start()
        self.messageReceiver.Start()

        self.focusEvent = eg.EventHook()
        
        if not (eg.config.hideOnStartup or eg.startupArguments.hideOnStartup):
            eg.document.ShowFrame()
            
        self.SetProcessingState = eg.taskBarIcon.SetProcessingState

        self.EventGhostEvent.Init()
        self.actionThread.Start()

        eg.eventThread.startupEvent = self.startupArguments.startupEvent
        self.TriggerEvent = eg.eventThread.TriggerEvent
        self.TriggerEnduringEvent = eg.eventThread.TriggerEnduringEvent
                    
        config = self.config

        startupFile = self.startupArguments.startupFile
        if (
            startupFile is None 
            and config.useAutoloadFile 
            and config.autoloadFilePath
        ):
            if not os.path.exists(config.autoloadFilePath):
                eg.PrintError(
                    self.text.Error.FileNotFound % config.autoloadFilePath
                )
            else:
                startupFile = config.autoloadFilePath
                
        eg.eventThread.Start()
        wx.CallAfter(eg.eventThread.Call, eg.eventThread.StartSession, startupFile)
        if config.checkUpdate:
            # avoid more than one check per day
            today = time.gmtime()[:3]
            if config.lastUpdateCheckDate != today:
                config.lastUpdateCheckDate = today
                import CheckUpdate
                wx.CallAfter(CheckUpdate.Start)
                
        self.Print(self.text.MainFrame.Logger.welcomeText)

            
    def __getattr__(self, name):
        if name[0].islower():
            modName = name[0].upper() + name[1:]
            mod = __import__("Singletons." + modName, fromlist=[modName])
            singelton = getattr(mod, modName)()
            self.__dict__[name] = singelton
            return singelton
            
        try:
            mod = __import__("Classes." + name, fromlist=[name])
        except ImportError:
            raise
        attr = getattr(mod, name)
        self.__dict__[name] = attr
        return attr
    
    
    def DeInit(self):
        self.PrintDebugNotice("stopping threads")
        self.actionThread.CallWait(self.actionThread.StopSession)
        self.scheduler.Stop()
        self.actionThread.Stop()
        self.eventThread.Stop()
        
        self.PrintDebugNotice("shutting down")
        self.config.onlyLogAssigned = self.onlyLogAssigned
        self.config.Save()
        self.messageReceiver.Close()
        
        
    def Wait(self, secs, raiseException=True):
        while secs > 0.0:
            if self.stopExecutionFlag:
                if raiseException:
                    raise self.StopException("Execution interrupted by the user.")
                else:
                    return False
            if secs > 0.1:
                time.sleep(0.1)
            else:
                time.sleep(secs)
            secs -= 0.1
        return True
        
        
    def RegisterEvent(self, eventString, eventHandler):
        eventTable = self.eventTable
        if eventString not in eventTable:
            eventTable[eventString] = []
        eventTable[eventString].append(eventHandler)
    
                
    def UnRegisterEvent(self, eventString, eventHandler):
        eventTable = self.eventTable
        if eventString not in eventTable:
            return
        try:
            eventTable[eventString].remove(eventHandler)
        except:
            pass
        if len(eventTable[eventString]) == 0:
            del eventTable[eventString]

    
    def HasActiveHandler(self, eventstring):
        for eventHandler in self.eventTable.get(eventstring, []):
            obj = eventHandler
            while obj:
                if not obj.isEnabled:
                    break
                obj = obj.parent
            else:
                return True
        return False


    def Bind(self, eventString, eventFunc):
        eventTable = self.eventTable2
        if eventString not in eventTable:
            eventTable[eventString] = []
        eventTable[eventString].append(eventFunc)
    
                
    def Unbind(self, eventString, eventFunc):
        eventTable = self.eventTable2
        if eventString not in eventTable:
            return
        try:
            eventTable[eventString].remove(eventFunc)
        except:
            pass
        if len(eventTable[eventString]) == 0:
            del eventTable[eventString]


    def RunProgram(self):
        self.stopExecutionFlag = False
        del self.programReturnStack[:]
        while self.programCounter is not None:
            programCounter = self.programCounter
            item, idx = programCounter
            item.Execute()
            if self.programCounter == programCounter:
                # program counter has not changed. Ask the parent for the next
                # item.
                if isinstance(item.parent, eg.MacroItem):
                    self.programCounter = item.parent.GetNextChild(idx)
                else:
                    self.programCounter = None
                
            if self.programCounter is None:
                # we have no next item in this level. So look in the return 
                # stack if any return has to be executed
                if self.programReturnStack:
                    item, idx = self.programReturnStack.pop()
                    self.programCounter = item.parent.GetNextChild(idx)
                    

    def StopMacro(self, ignoreReturn=False):
        self.programCounter = None
        if ignoreReturn:
            del self.programReturnStack[:]
        
        
    def CallWait(self, func, *args, **kwargs):
        result = [None]
        event = threading.Event()
        def CallWaitWrapper():
            try:
                result[0] = func(*args, **kwargs)
            finally:
                event.set()
        wx.CallAfter(CallWaitWrapper)
        event.wait()
        return result[0]
            
            
    def GetConfig(self, searchPath, defaultCls):
        config = self.config
        parts = searchPath.split(".")
        for part in parts[:-1]:
            config = config.SetDefault(part, eg.Bunch)
        return config.SetDefault(parts[-1], defaultCls)
            
            
    def DummyFunc(*args, **kwargs):
        pass

            
    class Exception(Exception):
        def __init__(self, message):
            self.message = message
            
        def __str__(self):
            return repr(self.message)


    class StopException(Exception):
        pass
    
    
    class HiddenAction:
        pass
    
