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
import pythoncom
import asynchat
import thread
import socket
import time
import asyncore
import threading
import traceback
import linecache
from os.path import exists
import wx
import locale



class EventGhost(object):
    
    class Exception(Exception):
        def __init__(self, message):
            self.message = message
            
        def __str__(self):
            return repr(self.message)


    class StopException(Exception):
        pass
    
    
    class HiddenAction:
        pass
    
    
    def __init__(self):
        sys.modules["eg"] = self        
        
        
    def Init(self, args):
        global eg
        eg = self
        self.systemEncoding = encoding = locale.getdefaultlocale()[1]
        self.CallAfter = wx.CallAfter
        self.APP_NAME = "EventGhost"
        self.PLUGIN_DIR = os.path.abspath("plugins")
        
        # we create a package 'pluginImport' and set its path to the plugin-dir
        # se we can simply use __import__ to load a plugin file 
        pluginPackage = imp.new_module("pluginImport")
        pluginPackage.__path__ = [self.PLUGIN_DIR]
        sys.modules["pluginImport"] = pluginPackage
        
        self.startupArguments = args
        self.debugLevel = args.debugLevel
        self.__InitPIL()
        self.__InitAsyncore()
        
        sys.modules["eg"] = self
        from Utils import Bunch, EventHook
        self.Bunch = Bunch
        self.EventHook = EventHook
        self.document = None
        
        self.result = None
        self.event = None
        self.eventTable = {}
        self.eventTable2 = {}
        self.plugins = Bunch()
        self.pluginClassInfo = {}
        self.globals = Bunch()
        self.globals.eg = self
        self.result = None
        self.mainThread = threading.currentThread()
        self.onlyLogAssigned = False
        self.programCounter = None
        self.programReturnStack = []
        self.stopExecutionFlag = False
        self.lastFoundWindows = []
        self.currentConfigureItem = None
        
        from Version import version, buildNum, compileTime, svnRevision
        self.version = version
        self.buildNum = buildNum
        self.compileTime = compileTime
        self.versionStr = "%s.%s" % (version, buildNum)
        self.svnRevision = svnRevision

        from Utils import (
            LogIt, 
            LogItWithReturn, 
            TimeIt,
            AssertNotMainThread, 
            AssertNotActionThread
        )
        self.LogIt = LogIt
        self.LogItWithReturn = LogItWithReturn
        self.TimeIt = TimeIt
        self.AssertNotMainThread = AssertNotMainThread
        self.AssertNotActionThread = AssertNotActionThread
        
        from MessageReceiver import MessageReceiver
        self.messageReceiver = MessageReceiver()
        
        # because some functions are only available if a wxApp instance
        # exists, we simply create it first
        from App import MyApp
        self.app = MyApp(0)
        if True:#not args.translate:
            import Log
            self.log = Log.Log()
            self.DoPrint = self.log.DoPrint
        if not self.debugLevel:
            def _DummyFunc(*args, **kwargs):
                pass
            self.Notice = _DummyFunc
            self.DebugNote = _DummyFunc
        else:
            import warnings
            warnings.simplefilter('error', UnicodeWarning)

            if self.debugLevel == 2:
                fd = open("Log.txt", "at")
                class writer:
                    def write(self, data):
                        fd.write(data)
                        fd.flush()
                sys.stderr = writer()
                
            from Utils import DebugNote
            self.Notice = DebugNote
            self.DebugNote = DebugNote
    
            DebugNote("----------------------------------------")
            DebugNote("        EventGhost started")
            DebugNote("----------------------------------------")
            DebugNote("Version:", self.versionStr)
            

        import IconTools
        IconTools.Init()
        self.IconTools = IconTools
        self.SetupIcons = IconTools.SetupIcons
        self.imageList = IconTools.gImageList
        self.AddPluginIcon = IconTools.AddPluginIcon
        sys.modules["eg.IconTools"] = IconTools
        
        from ConfigData import LoadConfig, SaveConfig
        self.config = config = LoadConfig()
        self.SaveConfig = SaveConfig
        self.onlyLogAssigned = config.onlyLogAssigned
        
        from LanguageTools import LoadStrings, GetTranslation
        self.GetTranslation = GetTranslation
        self.text = LoadStrings(config.language)

        import WinAPI
        import TreeItems
        import cFunctions
        sys.modules["eg.WinAPI"] = WinAPI
        self.WinAPI = WinAPI
        sys.modules["eg.TreeItems"] = TreeItems
        sys.modules["eg.cFunctions"] = cFunctions
    
        from Utils import SetClass
        from Text import Text
        SetClass(self.text, Text)

        self.DoImports1()
        
        from EventGhostEvent import EventGhostEvent
        self.EventGhostEvent = EventGhostEvent

        self.DoImports2()

        # replace builtin input and raw_input with a small dialog
#        from Dialogs.SimpleInputDialog import (
#            GetSimpleRawInput, 
#            GetSimpleInput
#        )
#        sys.modules['__builtin__'].raw_input = GetSimpleRawInput
#        sys.modules['__builtin__'].input = GetSimpleInput

        from WinAPI.SerialPort import EnumSerialPorts as GetAllPorts
        self.SerialPort.GetAllPorts = classmethod(GetAllPorts)
        
        eg.DebugNote("Creating SendKeys parser")
        from WinAPI.SendKeys import SendKeysParser
        _sendKeysObj = SendKeysParser()
        self.SendKeys = _sendKeysObj.Parse

        self.actionList = []
        
        from PluginDatabase import PluginDatabase
        self.pluginDatabase = PluginDatabase()
        
        
    def StartGui(self):
        self.InitWin32Com()
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
                    
        self.__class__.__setattr__ = self.__post__setattr__
        
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
                from CheckUpdate import CheckUpdate
                wx.CallAfter(CheckUpdate)
                
        self.DoPrint(self.text.MainFrame.Logger.welcomeText)

            
    __setattr_set = frozenset(
        (
            "result",
            "currentItem", 
            "event", 
            "eventString", 
            "EventString",
            "onlyLogAssigned"
        )
    )
    
    def __post__setattr__(self, name, value):
        if name in self.__setattr_set:
            object.__setattr__(self, name, value)
        else:
            raise Exception("Can't assign to eg-instance")


    def SetAttr(self, name, value):
        if not hasattr(self, name):
            raise AttributeError("eg has not attribute '%s'" % name)
        object.__setattr__(self, name, value)
        
        
    def __getattr__(self, name):
        try:
            mod = __import__("Controls.%s" % name, fromlist=[name])
        except ImportError:
            try:
                mod = __import__("Dialogs.%s" % name, fromlist=[name])
            except ImportError:
                raise AttributeError
        eg.DebugNote("Loaded module %s" % name)
        attr = getattr(mod, name)
        self.__dict__[name] = attr
        return attr
    
    
    def DoImports1(self):
        from sys import exit as Exit
        
        from Utils import hexstring, ParseString
        from ThreadWorker import ThreadWorker

        import wx
        from wx import CallAfter
        from wx.html import HW_NO_SELECTION
        from Validators import DigitOnlyValidator, AlphaOnlyValidator
        from WinAPI.Pathes import (
            APPDATA, 
            STARTUP, 
            PROGRAMFILES, 
            TEMPDIR, 
        )
        
        from WinAPI.Shortcut import CreateShortcut
        from WinAPI.Utils import BringHwndToFront
        from WinAPI.serial import Serial as SerialPort

        from PluginClass import PluginClass
        from IrDecoder import IrDecoder
        from IrDecoder2 import IrDecoder2
        from RawReceiverPlugin import RawReceiverPlugin
        from ActionClass import ActionClass, ActionWithStringParameter
        from ActionGroup import ActionGroup

        #from time import sleep as Wait
        import TreeItems
        from TreeItems import (
            TreeItem, 
            ContainerItem, 
            EventItem, 
            RootItem,
            MacroItem, 
            FolderItem, 
            ActionItem,
            AutostartItem, 
            PluginItem, 
        )
        from TreeItems.TreeLink import TreeLink
        from greenlet import greenlet as Greenlet
        self.__dict__.update(locals())
        
        
    def DoImports2(self):    
        from PluginTools import (
            OpenPlugin, 
            ClosePlugin, 
            GetPluginInfo,
            GetPluginInfoList
        )
        self.__dict__.update(locals())
        
        
    def __InitPIL(self):
        # initialize PIL's Image module
        import Image
        import PngImagePlugin
        import JpegImagePlugin
        import BmpImagePlugin
        import GifImagePlugin
        Image._initialized = 2
        
        
    def InitWin32Com(self):
        # Patch win32com to use the gen_py directory in the programs
        # application data directory instead of its package directory.
        # When the program runs "frozen" it would not be able to modify
        # the package directory
        __gen_path__ = os.path.join(self.APPDATA, "EventGhost", "gen_py")
        if not os.path.exists(__gen_path__):
            os.makedirs(__gen_path__)
        import win32com
        win32com.__gen_path__ = __gen_path__
        sys.modules["win32com.gen_py"].__path__ = [__gen_path__]
        import win32com.client
        win32com.client.gencache.is_readonly = False
        
        # Support for the COM-Server of the program
        if hasattr(sys, "frozen"):
            pythoncom.frozen = 1
        from WinAPI.COMServer import EventGhostCom
        from win32com.server.register import RegisterClasses
        import pywintypes
        try:
            RegisterClasses(EventGhostCom, quiet=True)
        except pywintypes.error, data:
            if data[0] != 5:
                raise
        sys.coinit_flags = 2
        from win32com.server import factory
        self.__factory_infos = factory.RegisterClassFactories(["EventGhost"])
        #import win32api
        #pythoncom.EnableQuitMessage(win32api.GetCurrentThreadId())	
        pythoncom.CoResumeClassObjects()

        e = win32com.client.Dispatch("EventGhost")        
        
        
    def DeInitWin32Com(self):
        # shutdown COM-Server
        from win32com.server import factory
        factory.RevokeClassFactories(self.__factory_infos)
        pythoncom.CoUninitialize()
        
        
    def __InitAsyncore(self):
        # create a dummy-asynchat to keep asyncore.loop alive    
        dummyAsyncChat = asynchat.async_chat()
        dummyAsyncChat.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        thread.start_new_thread(asyncore.loop, (1,))
        self.__dummyAsyncChat = dummyAsyncChat


    def __DeInitAsyncore(self):
        self.__dummyAsyncChat.close()
        

    def DeInit(self):
        self.Notice("stopping threads")
        self.actionThread.CallWait(self.actionThread.StopSession)
        self.actionThread.Stop()
        self.eventThread.Stop()
        
        self.Notice("shutting down")
        self.config.onlyLogAssigned = self.onlyLogAssigned
        self.SaveConfig()
        self.__DeInitAsyncore()
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


    def SetProgramCounter(self, counter):
        self.__dict__["programCounter"] = counter
    
    
    def RunProgram(self):
        self.__dict__["stopExecutionFlag"] = False
        del self.programReturnStack[:]
        while self.programCounter is not None:
            programCounter = self.programCounter
            currentItem, currentIndex = programCounter
            currentItem.Execute()
            if self.programCounter == programCounter:
                # program counter has not changed. Ask the parent for the next
                # item.
                if isinstance(currentItem.parent, eg.MacroItem):
                    self.SetProgramCounter(
                        currentItem.parent.GetNextChild(currentIndex)
                    )
                else:
                    self.SetProgramCounter(None)
                
            if self.programCounter is None:
                # we have no next item in this level. So look in the return 
                # stack if any return has to be executed
                if self.programReturnStack:
                    currentItem, currentIndex = self.programReturnStack.pop()
                    self.SetProgramCounter(
                        currentItem.parent.GetNextChild(currentIndex)
                    )
                    

    def StopMacro(self, ignoreReturn=False):
        self.SetProgramCounter(None)
        if ignoreReturn:
            del self.programReturnStack[:]
        
        
    def PrintError(self, *args):
        def convert(s):
            if type(s) == type(u""):
                return s
            else:
                return str(s)
        text = " ".join([convert(arg) for arg in args])
        self.log.DoPrint(text, 1)


    def PrintNotice(self, *args):
        text = " ".join([str(arg) for arg in args])
        self.log.DoPrint(text, 2)


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

            
