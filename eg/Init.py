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
import asynchat
import thread
import socket
import time
import asyncore
import threading
import traceback
from os.path import exists
import wx
import locale
import atexit


class EventGhost(object):
    
    def __init__(self, args):
        global eg
        eg = self
        sys.modules["eg"] = self
        
        self.startupArguments = args
        self.debugLevel = args.debugLevel
        self.systemEncoding = locale.getdefaultlocale()[1]
        self.CallAfter = wx.CallAfter
        self.APP_NAME = "EventGhost"
        self.PLUGIN_DIR = os.path.abspath("plugins")
        
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
        
        # create a dummy-asynchat to keep asyncore.loop alive    
        dummyAsyncChat = asynchat.async_chat()
        dummyAsyncChat.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        thread.start_new_thread(asyncore.loop, (1,))
        atexit.register(dummyAsyncChat.close)

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
        
        self.document = None
        self.result = None
        self.event = None
        self.eventTable = {}
        self.eventTable2 = {}
        self.plugins = eg.Bunch()
        self.pluginClassInfo = {}
        self.globals = eg.Bunch()
        self.globals.eg = self
        self.mainThread = threading.currentThread()
        self.onlyLogAssigned = False
        self.programCounter = None
        self.programReturnStack = []
        self.stopExecutionFlag = False
        self.lastFoundWindows = []
        self.currentConfigureItem = None
        self.actionList = []
                
        from Version import version, buildNum
        self.version = version
        self.buildNum = buildNum
        self.versionStr = "%s.%s" % (version, buildNum)

        from MessageReceiver import MessageReceiver
        self.messageReceiver = MessageReceiver()
        
        # because some functions are only available if a wxApp instance
        # exists, we simply create it first
        import App
        self.app = App.MyApp(0)

        import Icons
        self.Icons = Icons
        
        import Log
        self.log = Log.Log()
        self.Print = self.log.Print
        if not self.debugLevel:
            self.DebugNote = self.DummyFunc
        else:
            import warnings
            warnings.simplefilter('error', UnicodeWarning)

            self.DebugNote = Utils.DebugNote
    
            self.DebugNote("----------------------------------------")
            self.DebugNote("        EventGhost started")
            self.DebugNote("----------------------------------------")
            self.DebugNote("Version:", self.versionStr)
            

        from ConfigData import LoadConfig, SaveConfig
        self.config = config = LoadConfig()
        self.SaveConfig = SaveConfig
        self.onlyLogAssigned = config.onlyLogAssigned
        
        from LanguageTools import LoadStrings, GetTranslation
        self.GetTranslation = GetTranslation
        self.text = LoadStrings(config.language)

        import WinAPI
        sys.modules["eg.WinAPI"] = WinAPI
        self.WinAPI = WinAPI
        import TreeItems
        import cFunctions
        sys.modules["eg.TreeItems"] = TreeItems
        sys.modules["eg.cFunctions"] = cFunctions
    
        from Text import Text
        Utils.SetClass(self.text, Text)

        self.DoImports1()
        
        import EventGhostEvent
        self.EventGhostEvent = EventGhostEvent.EventGhostEvent

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

        from WinAPI.SerialPort import EnumSerialPorts as GetAllPorts
        self.SerialPort.GetAllPorts = classmethod(GetAllPorts)
        
        from PluginDatabase import PluginDatabase
        self.pluginDatabase = PluginDatabase()
        
        
    def StartGui(self):
        import WinAPI.COMServer
        self.messageReceiver.Start()
        
        from Document import Document
        self.document = Document()
        eg.app.SetupGui()
                        
        self.SetProcessingState = eg.app.taskBarIcon.SetProcessingState

        from ActionThread import ActionThread
        self.actionThread = actionThread = ActionThread()
        
        from EventGhostEvent import Init
        Init()
        actionThread.Start()

        from EventThread import EventThread
        self.eventThread = eventThread = EventThread()
        eventThread.startupEvent = self.startupArguments.startupEvent
        self.TriggerEvent = eventThread.TriggerEvent
        self.TriggerEnduringEvent = eventThread.TriggerEnduringEvent
                    
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
                
        eventThread.Start()
        wx.CallAfter(eventThread.Call, eventThread.StartSession, startupFile)
        if config.checkUpdate:
            # avoid more than one check per day
            today = time.gmtime()[:3]
            if config.lastUpdateCheckDate != today:
                config.lastUpdateCheckDate = today
                import CheckUpdate
                wx.CallAfter(CheckUpdate.Start)
                
        self.Print(self.text.MainFrame.Logger.welcomeText)

            
    def __getattr__(self, name):
        try:
            mod = __import__("Controls.%s" % name, fromlist=[name])
        except ImportError:
            try:
                mod = __import__("Dialogs.%s" % name, fromlist=[name])
            except ImportError:
                raise
        eg.DebugNote("Loaded module %s" % name)
        attr = getattr(mod, name)
        self.__dict__[name] = attr
        return attr
    
    
    def DoImports1(self):
        from sys import exit as Exit
        from ThreadWorker import ThreadWorker
        from Validators import DigitOnlyValidator, AlphaOnlyValidator
        from WinAPI.Pathes import APPDATA, STARTUP, PROGRAMFILES, TEMPDIR
        self.CONFIG_DIR = os.path.join(APPDATA, self.APP_NAME)
        from WinAPI.Shortcut import CreateShortcut
        from WinAPI.serial import Serial as SerialPort

        from PluginClass import PluginClass
        from IrDecoder import IrDecoder
        from RawReceiverPlugin import RawReceiverPlugin
        from ActionClass import ActionClass, ActionWithStringParameter
        from ActionGroup import ActionGroup

        #import TreeItems
        from TreeItems.TreeItem import TreeItem
        from TreeItems.ContainerItem import ContainerItem
        from TreeItems.EventItem import EventItem
        from TreeItems.RootItem import RootItem
        from TreeItems.MacroItem import MacroItem
        from TreeItems.FolderItem import FolderItem
        from TreeItems.ActionItem import ActionItem
        from TreeItems.AutostartItem import AutostartItem
        from TreeItems.PluginItem import PluginItem
        from TreeItems.TreeLink import TreeLink
        from greenlet import greenlet as Greenlet
        self.__dict__.update(locals())
        
        
    def DeInit(self):
        self.DebugNote("stopping threads")
        self.actionThread.CallWait(self.actionThread.StopSession)
        self.actionThread.Stop()
        self.eventThread.Stop()
        
        self.DebugNote("shutting down")
        self.config.onlyLogAssigned = self.onlyLogAssigned
        self.SaveConfig()
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
        
        
    def RegisterPlugin(self, **kwargs):
        pass
    
    
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
            currentItem, currentIndex = programCounter
            currentItem.Execute()
            if self.programCounter == programCounter:
                # program counter has not changed. Ask the parent for the next
                # item.
                if isinstance(currentItem.parent, eg.MacroItem):
                    self.programCounter = \
                        currentItem.parent.GetNextChild(currentIndex)
                else:
                    self.programCounter = None
                
            if self.programCounter is None:
                # we have no next item in this level. So look in the return 
                # stack if any return has to be executed
                if self.programReturnStack:
                    currentItem, currentIndex = self.programReturnStack.pop()
                    self.programCounter = \
                        currentItem.parent.GetNextChild(currentIndex)
                    
                    

    def StopMacro(self, ignoreReturn=False):
        self.programCounter = None
        if ignoreReturn:
            del self.programReturnStack[:]
        
        
    def PrintError(self, *args):
        def convert(s):
            if type(s) == type(u""):
                return s
            else:
                return str(s)
        text = " ".join([convert(arg) for arg in args])
        self.log.PrintError(text)


    def PrintNotice(self, *args):
        text = " ".join([str(arg) for arg in args])
        self.log.PrintNotice(text)


    def PrintTraceback(self, msg=None, skip=0):
        if msg:
            self.PrintError(msg)
        tbType, tbValue, tbTraceback = sys.exc_info() 
        list = ['Traceback (most recent call last) (%d):\n' % self.buildNum]
        if tbTraceback:
            list += traceback.format_tb(tbTraceback)[skip:]
        list += traceback.format_exception_only(tbType, tbValue)
        
        error = "".join(list)
        eg.PrintError(error.rstrip())
        if eg.debugLevel:
            sys.stderr.write(error)
            
            
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
            config = config.setdefault(part, eg.Bunch)
        return config.setdefault(parts[-1], defaultCls)
            
            
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
    

