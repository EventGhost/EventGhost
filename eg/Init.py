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
import asyncore
import socket
import locale


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
        self.__path__ = [os.path.abspath("eg")]
        
        # add 'eg' and 'wx' to the builtin name space of every module
        import __builtin__
        __builtin__.__dict__["eg"] = self
        import wx
        __builtin__.__dict__["wx"] = wx
        import wx.lib.newevent
        eg.ControlChangedEvent, eg.EVT_CONTROL_CHANGED = wx.lib.newevent.NewCommandEvent()
        
        eg.startupArguments = args
        eg.debugLevel = args.debugLevel
        eg.systemEncoding = locale.getdefaultlocale()[1]
        eg.CallAfter = wx.CallAfter
        eg.APP_NAME = "EventGhost"
        eg.PLUGIN_DIR = os.path.abspath("plugins")
        eg.APPDATA = eg.folderPath.RoamingAppData
        eg.PROGRAMFILES = eg.folderPath.ProgramFiles
        eg.CONFIG_DIR = os.path.join(eg.folderPath.RoamingAppData, eg.APP_NAME)
        eg.CORE_PLUGINS = (
            "EventGhost",
            "System",
            "Window",
            "Mouse",
        )
        eg.ID_TEST = wx.NewId()
        
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
        
        import WinAPI.cTypes
        sys.modules["ctypes.dynamic"] = WinAPI.cTypes
        
        import Utils
        for name in Utils.__all__:
            setattr(eg, name, getattr(Utils, name))
        
        #self.document = None
        eg.result = None
        eg.event = None
        eg.eventTable = {}
        eg.eventTable2 = {}
        eg.plugins = eg.Bunch()
        eg.pluginClassInfo = {}
        
        eg.globals = Utils.Bunch()
        eg.globals.eg = self
        eg.mainThread = threading.currentThread()
        eg.programCounter = None
        eg.programReturnStack = []
        eg.stopExecutionFlag = False
        eg.lastFoundWindows = []
        eg.currentConfigureItem = None
        eg.pluginList = []
        eg.actionList = []
                
        from Version import version, buildNum
        eg.version = version
        eg.buildNum = buildNum
        eg.versionStr = "%s.%s" % (version, buildNum)

        # because some functions are only available if a wxApp instance
        # exists, we simply create it first
        eg.app
                
        import Icons
        self.Icons = Icons
        
        eg.Print = self.log.Print
        eg.PrintError = self.log.PrintError
        eg.PrintNotice = self.log.PrintNotice
        eg.PrintTraceback = self.log.PrintTraceback
        eg.PrintDebugNotice = self.log.PrintDebugNotice
            
        # redirect all wxPython error messages to our log
        class MyLog(wx.PyLog):
            def DoLog(self2, level, msg, timestamp):
                if (level >= 6):# and not self.debugLevel:
                    return
                sys.stderr.write("Error%d: %s\n" % (level, msg))
        wx.Log.SetActiveTarget(MyLog())

        from LanguageTools import LoadStrings
        eg.text = LoadStrings(eg.config.language)

        from Text import Text
        Utils.SetClass(self.text, Text)

        eg.Exit = sys.exit
        
        from eg.greenlet import greenlet
        eg.Greenlet = greenlet
        eg.mainGreenlet = greenlet.getcurrent()
        
        from eg.PluginTools import OpenPlugin, ClosePlugin
        eg.OpenPlugin = OpenPlugin
        eg.ClosePlugin = ClosePlugin

        # replace builtin input and raw_input with a small dialog
        def raw_input(prompt=None):
            return eg.CallWait(eg.SimpleInputDialog.CreateModal, prompt)
        __builtin__.raw_input = raw_input

        def input(prompt=None):
            return eval(raw_input(prompt))
        __builtin__.input = input
        
        # TODO: make this lazy imports
        from eg.WinAPI.serial import Serial
        eg.SerialPort = Serial
        
        from eg.WinAPI.SendKeys import SendKeys
        eg.SendKeys = SendKeys
        
        
    def StartGui(self):
        global eg
        # create a global asyncore loop thread
        # TODO: Only start if asyncore is requested
        eg.dummyAsyncoreDispatcher = None
        eg.RestartAsyncore()
        threading.Thread(target=asyncore.loop, name="AsyncoreThread").start()

        import eg.WinAPI.COMServer
        
        self.scheduler.start()
        self.messageReceiver.Start()

        self.focusEvent = eg.EventHook()
        
        if not (eg.config.hideOnStartup or eg.startupArguments.hideOnStartup):
            eg.document.ShowFrame()
            
        self.SetProcessingState = eg.taskBarIcon.SetProcessingState

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
            mod = __import__("eg.Singletons." + modName, fromlist=[modName])
            singelton = getattr(mod, modName)()
            self.__dict__[name] = singelton
            return singelton
            
        try:
            mod = __import__("eg.Classes." + name, fromlist=[name])
        except ImportError:
            raise
        #print("Loaded %s" % name)
        attr = getattr(mod, name)
        self.__dict__[name] = attr
        return attr
    
    
    def DeInit(self):
        self.PrintDebugNotice("stopping threads")
        self.actionThread.CallWait(self.actionThread.StopSession)
        self.scheduler.Stop()
        self.actionThread.Stop()
        self.eventThread.Stop()
        self.dummyAsyncoreDispatcher.close()
        
        self.PrintDebugNotice("shutting down")
        self.config.Save()
        self.messageReceiver.Close()
        
        
    def RestartAsyncore(self):
        """ Informs the asyncore loop of a new socket to handle. """
        oldDispatcher = eg.dummyAsyncoreDispatcher
        dispatcher = asyncore.dispatcher()
        dispatcher.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.dummyAsyncoreDispatcher = dispatcher
        if oldDispatcher:
            oldDispatcher.close()
    
    
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
        
        def __unicode__(self):
            res = [unicode(arg) for arg in self.args]
            return "\n".join(res)


    class StopException(Exception):
        pass
    
    
    class HiddenAction:
        pass
    
