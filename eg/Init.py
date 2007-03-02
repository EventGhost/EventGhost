#
# eg/Init.py
#
# Copyright (C) 2005 Lars-Peter Voss
#
# This file is part of EventGhost.
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
import pythoncom
import asynchat
import thread
import socket
import time
import asyncore
import threading
import traceback
import linecache

import wx


class ResultProperty(object):
    
    def __get__(self, instance, owner):
        return self.value
    
    def __set__(self, instance, value):
        self.value = value
        
    def __delete__(self, instance, value):
        raise "Can't delete this variable"
        
resultProperty = ResultProperty()



class GlobalsDict(dict):
    def keys(self):
        eg.whoami()
        x = dict.keys(self)
        x.append("result")
        return x
    
    def items(self):
        eg.whoami()
        x = dict.items(self)
        x.append(("result", resultProperty.value))
        return x
    
    def __getitem__(self, key):
        if key == "result":
            return resultProperty.value
        return dict.__getitem__(self, key)
    
    def __setitem__(self, key, value):
        if key == "result":
            resultProperty.value = value
            return
        dict.__setitem__(self, key, value)
    
    def iteritems(self):
        eg.whoami()
        dict.iteritems(self)
        yield ("result", resultProperty.value)
    
    def iterkeys(self):
        eg.whoami()
        dict.iterkeys(self)
        yield "result"
    
    def copy(self):
        eg.whoami()
        return dict.copy(self)
    
    def update(self, b):
        eg.whoami()
        return dict.update(self, b)
    
    def has_key(self, key):
        eg.whoami()
        return dict.has_key(self, key)
    
    def len(self):
        eg.whoami()
        return dict.len(self) + 1
    
    
class GlobalsBunch(object):
    
    result = resultProperty
    def __new__(cls):
        inst = object.__new__(cls)
        inst.__dict__ = GlobalsDict()
        return  inst
        
        
    
class EventGhost(object):
    result = resultProperty
    
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
        
        
    def Init(self, debugLevel):
        global eg
        eg = self
        self.APP_NAME = "EventGhost"
        self.debugLevel = debugLevel
        self.__InitPIL()
        self.__InitAsyncore()
        
        sys.modules["eg"] = self
        from Utils import Bunch, EventHook
        self.Bunch = Bunch
        self.EventHook = EventHook
        #self.text = Bunch()
        #self.text = Text
        #self.originalText = Bunch()
        self.mainFrame = None
        self.treeCtrl = None
        self.logCtrl = None
        self.result = None
        self.event = None
        self.eventTable = {}
        self.eventTable2 = {}
        self.EventString = '' # eg.EventString is deprecated
        self.plugins = Bunch()
        self.pluginFileInfo = {}
        self.pluginClassInfo = {}
        self.corePlugins = {}
        self.globals = GlobalsBunch()
        self.globals.eg = self
        self.mainThread = threading.currentThread()
        self.isRunning = True
        self.onlyLogAssigned = False
        self.programCounter = None
        self.programReturnStack = []
        self.stopExecutionFlag = False
        self.lastFoundWindows = []
        
        self.Plugin = self.plugins # eg.Plugin is deprecated
        self.Global = self.globals # eg.Global is deprecated

        self._lastDefinedPluginClass = None
        self._lastDefinedPluginClassInfo = None

        from Version import version, buildNum, compileTime, svnRevision
        self.version = version
        self.buildNum = buildNum
        self.compileTime = compileTime
        self.versionStr = "%s.%s" % (version, buildNum)
        self.svnRevision = svnRevision

        from Utils import logit
        self.logit = logit
        
        from MessageReceiver import MessageReceiver
        self.messageReceiver = MessageReceiver()
        
        # because some functions are only available if a wxApp instance
        # exists, we simply create it first
        from App import MyApp
        self.app = MyApp(0)
        
        if not debugLevel:
            def _DummyFunc(*args, **kwargs):
                pass
            self.notice = _DummyFunc
            self.whoami = _DummyFunc
        else:
            if debugLevel == 2:
                fd = open("Log.txt", "at")
                class writer:
                    def write(self, data):
                        fd.write(data)
                        fd.flush()
                sys.stderr = writer()
                
            from Utils import notice, whoami
            self.notice = notice
            self.whoami = whoami
    
            notice("----------------------------------------")
            notice("        EventGhost started")
            notice("----------------------------------------")
            notice("Version:", self.versionStr)
            

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
        import Controls
        import Dialogs
        import TreeItems
        import cFunctions
        sys.modules["eg.WinAPI"] = WinAPI
        self.WinAPI = WinAPI
        sys.modules["eg.Controls"] = Controls
        sys.modules["eg.Dialogs"] = Dialogs
        sys.modules["eg.TreeItems"] = TreeItems
        sys.modules["eg.cFunctions"] = cFunctions
    
        from Utils import SetClass
        from Text import Text
        SetClass(self.text, Text)

        #from Dialogs.Dialog import Dialog
        #self.Dialog = Dialog

        self.DoImports1()
        
        from EventGhostEvent import EventGhostEvent
        self.EventGhostEvent = EventGhostEvent

        self.DoImports2()

        # replace builtin input and raw_input with a small dialog
        from eg.Dialogs.SimpleInputDialog import (
            GetSimpleRawInput, 
            GetSimpleInput
        )
        sys.modules['__builtin__'].raw_input = GetSimpleRawInput
        sys.modules['__builtin__'].input = GetSimpleInput

        from WinAPI.SerialPort import EnumSerialPorts as GetAllPorts
        self.SerialPort.GetAllPorts = classmethod(GetAllPorts)
        
        eg.notice("Creating SendKeys parser")
        from WinAPI.SendKeys import SendKeysParser
        _sendKeysObj = SendKeysParser()
        self.SendKeys = _sendKeysObj.Parse

        self.actionList = []
        
        
    def StartGui(self, startupEvent, startupFile, hideOnStartup):
        self.__InitComServer()
        self.messageReceiver.start()
        
        eg.app.SetupGui()
        
        from MainFrame import MainFrame
        self.mainFrame = MainFrame()
                
        self.logCtrl = self.mainFrame.logCtrl
        self.treeCtrl = self.mainFrame.treeCtrl
        self.DoPrint = self.logCtrl.DoPrint
        self.SetProcessingState = eg.app.taskBarIcon.SetProcessingState

        from ActionThread import ActionThread
        self.actionThread = actionThread = ActionThread()
        
        from EventGhostEvent import Init
        Init()
        actionThread.start()

        from EventThread import EventThread
        self.eventThread = eventThread = EventThread()
        eventThread.startupEvent = startupEvent
        self.TriggerEvent = eventThread.TriggerEvent
        self.TriggerEnduringEvent = eventThread.TriggerEnduringEvent
        
        self.__class__.__setattr__ = self.__post__setattr__
        
        config = self.config
        self.app.SetTopWindow(self.mainFrame)
        self.mainFrame.Show(not (config.hideOnStartup or hideOnStartup))

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
                
        eventThread.start()
        wx.CallAfter(eventThread.Call, eventThread.StartSession, startupFile)
        if config.checkUpdate:
            from CheckUpdate import CheckUpdate
            wx.CallAfter(CheckUpdate)
            
            
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
            raise "Can't assign to eg-instance"


    def SetAttr(self, name, value):
        object.__setattr__(self, name, value)
        
        
    def DoImport(self, *imports):
        g = globals()
        l = locals()
        for line in imports:
            if type(line) == type(()):
                name, items = line
                module = __import__(name, g, l, items, -1)
                for item in items:
                    self.__dict__[item] = getattr(module, item)
            else:
                module = __import__(line, g, l, [], -1)
                name = line.split(".")[-1]
                self.__dict__[name] = getattr(getattr(module, name), name)
        
        
    def DoImports1(self):
        from sys import exit as Exit
        
        self.DoImport(
            "Dialogs.Dialog",
            ("Utils", ["hexstring", "ParseString"]),
            ("ThreadWorker", ["ThreadWorker"]),
        )
        #from Utils import hexstring, ParseString
        #from ThreadWorker import ThreadWorker

        import wx
        from wx.html import HW_NO_SELECTION
        from Validators import DigitOnlyValidator, AlphaOnlyValidator
        from WinAPI.Pathes import (
            APPDATA, 
            STARTUP, 
            PROGRAMFILES, 
            TEMPDIR, 
        )
        from WinAPI.Shortcut import CreateShortcut
        from WinAPI.Utils import ShrinkMemory, BringHwndToFront
        from WinAPI.serial import Serial as SerialPort

        self.DoImport(
            ("Controls.Menu", ["MenuBar", "Menu"]),
            "Controls.ButtonRow", 
            "Controls.StaticTextBox",
            "Controls.HtmlWindow",
            "Controls.HyperLinkCtrl",
            ("Controls.FileBrowseButton", ["FileBrowseButton", "DirBrowseButton"]),
        )
#        self.DoImport(
#            ("Controls",
#                ("Menu", 
#                    ["MenuBar", "Menu"]),
#                "ButtonRow", 
#                "StaticTextBox",
#                "HtmlWindow",
#                "HyperLinkCtrl",
#                ("FileBrowseButton", 
#                    ["FileBrowseButton", "DirBrowseButton"]),
#            )
#        )
        #from Controls.Menu import MenuBar, Menu
        #from Controls.ButtonRow import ButtonRow
        #from Controls.StaticTextBox import StaticTextBox
        #from Controls.HtmlWindow import HtmlWindow
        #from Controls.HyperLinkCtrl import HyperLinkCtrl
        #from Controls.FileBrowseButton import (
        #    FileBrowseButton, 
        #    DirBrowseButton
        #)
        from Controls.BrowseItemButton import BrowseMacroButton
        from Controls.SpinNumCtrl import SpinNumCtrl
        from Controls.SpinNumCtrl import SpinIntCtrl
        from Controls.FontButton import FontButton
        from Controls.ColourSelectButton import ColourSelectButton
        from Controls.DisplayChoice import DisplayChoice
        from Controls.StatusBar import StatusBar
        from Controls.ToolBar import ToolBar
        from Controls.SerialPortChoice import SerialPortChoice
        from Controls.RadioBox import RadioBox

        from Dialogs.HTMLDialog import HTMLDialog
        from Dialogs.ConfigurationDialog import ConfigurationDialog

        from License import html as license

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

        self.__dict__.update(locals())
        
        
    def DoImports2(self):    
        from PluginTools import (
            OpenPlugin, 
            ClosePlugin, 
            GetPluginInfo,
            PluginInfo,
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
        
        
    def __InitComServer(self):
        # Support for the COM-Server
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

        import win32com.client
        e = win32com.client.Dispatch("EventGhost")        
        
        
    def __DeInitComServer(self):
        # shutdown COM-Server
        from win32com.server import factory
        factory.RevokeClassFactories(self.__factory_infos)
        pythoncom.CoUninitialize()
        
        
    def __InitAsyncore(self):
        # create a dummy-asynchat to keep asyncore.loop alive    
        dummy_asynchat = asynchat.async_chat()
        dummy_asynchat.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        thread.start_new_thread(asyncore.loop, (1,))
        self.__dummy_asynchat = dummy_asynchat


    def __DeInitAsyncore(self):
        self.__dummy_asynchat.close()
        

    def DeInit(self):
        eg.whoami()
        self.__dict__["isRunning"] = False
        
        self.notice("stopping Threads")
        self.actionThread.CallWait(self.actionThread.StopSession)
        self.actionThread.stop()
        self.eventThread.stop()
        
        self.notice("shutting down")
        self.config.onlyLogAssigned = self.onlyLogAssigned
        self.SaveConfig()
        self.__DeInitAsyncore()
        self.messageReceiver.close()
        
        
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
        if not eventTable.has_key(eventString):
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
        if not eventTable.has_key(eventString):
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
        self.logCtrl.DoPrint(text, 1)


    def PrintNotice(self, *args):
        text = " ".join([str(arg) for arg in args])
        self.logCtrl.DoPrint(text, 2)


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
            
            