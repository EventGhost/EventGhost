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
import socket
import locale
from functools import partial

class args:
    hideOnStartup = False
    startupEvent = None
    startupFile = None
    allowMultiLoad = False
    debugLevel = 0
    translate = False
    configDir = None
    install = True
    

class Init(object):
    """
    The eg object/module is EventGhost itself.
    """
    
    def result_fget(self, owner):
        return self._result
    
    
    def result_fset(self, owner, value):
        self._result = value
        
    
    
    def __init__(self, args=args):
        global eg
        import eg
        for name in self.__class__.__dict__:
            if not name.startswith("_"):
                setattr(eg, name, self.__class__.__dict__[name])
        eg.__doc__ = self.__doc__
        self._result = None
        eg.__class__.result = property(self.result_fget, self.result_fset)
#        eg = self
#        sys.modules["eg"] = self
#        self.__path__ = [os.path.abspath("eg")]
        sys.path.append(os.path.abspath("lib\\site-packages"))
        if not hasattr(sys, "frozen"):
            sys.path.append(os.path.abspath("tools\\Python%d%d" % sys.version_info[:2]))
        sys.path.append(os.getcwdu())

        import cFunctions
        sys.modules["eg.cFunctions"] = cFunctions
        
        # add 'eg' and 'wx' to the builtin name space of every module
        import __builtin__
#        __builtin__.__dict__["eg"] = self
        import wx
        __builtin__.__dict__["wx"] = wx
        import wx.lib.newevent
        eg.ValueChangedEvent, eg.EVT_VALUE_CHANGED = wx.lib.newevent.NewCommandEvent()
        
        eg.folderPath = eg.FolderPath()
        eg.startupArguments = args
        eg.debugLevel = args.debugLevel
        eg.systemEncoding = locale.getdefaultlocale()[1]
        eg.CallAfter = wx.CallAfter
        eg.APP_NAME = "EventGhost"
        eg.PLUGIN_DIR = os.path.abspath("plugins")
        eg.APPDATA = eg.folderPath.RoamingAppData
        eg.PROGRAMFILES = eg.folderPath.ProgramFiles
        if args.configDir is None:
            eg.CONFIG_DIR = os.path.join(eg.folderPath.RoamingAppData, eg.APP_NAME)
        else:
            eg.CONFIG_DIR = args.configDir
        eg.CORE_PLUGINS = ("EventGhost", "System", "Window", "Mouse")
        eg.ID_TEST = wx.NewId()
        
        # we create a package 'pluginImport' and set its path to the plugin-dir
        # se we can simply use __import__ to load a plugin file 
        pluginPackage = imp.new_module("pluginImport")
        pluginPackage.__path__ = [eg.PLUGIN_DIR]
        sys.modules["pluginImport"] = pluginPackage
        
        eg.InitPil()
        
        import eg.Utils as Utils
        for name in Utils.__all__:
            setattr(eg, name, getattr(Utils, name))
                
        #self.document = None
        eg.result = None
        eg.event = None
        eg.eventTable = {}
        eg.eventTable2 = {}
        eg.plugins = eg.Bunch()
        eg.pluginClassInfo = {}
        
        eg.globals = eg.Bunch()
        eg.globals.eg = eg
        eg.mainThread = threading.currentThread()
        eg.programCounter = None
        eg.programReturnStack = []
        eg.stopExecutionFlag = False
        eg.lastFoundWindows = []
        eg.currentConfigureItem = None
        eg.pluginList = []
        eg.actionGroup = eg.Bunch()
        eg.actionGroup.items = []
        eg.buildNum = eg.Version.buildNum

        eg.messageReceiver = eg.MessageReceiver()
        # because some wx-functions are only available if a wxApp instance
        # exists, we simply create it first
        eg.app = eg.App()
        eg.colour = eg.Colour()
        eg.config = eg.Config()
        
        import eg.Icons
        
        eg.log = eg.Log()
        eg.Print = eg.log.Print
        eg.PrintError = eg.log.PrintError
        eg.PrintNotice = eg.log.PrintNotice
        eg.PrintTraceback = eg.log.PrintTraceback
        eg.PrintDebugNotice = eg.log.PrintDebugNotice
        eg.PrintStack = eg.log.PrintStack
        
        eg.actionThread = eg.ActionThread()
        eg.eventThread = eg.EventThread()
        eg.pluginManager = eg.PluginManager()
        eg.scheduler = eg.Scheduler()
        
        eg.TriggerEvent = eg.eventThread.TriggerEvent
        eg.TriggerEnduringEvent = eg.eventThread.TriggerEnduringEvent

        # redirect all wxPython error messages to our log
        class MyLog(wx.PyLog):
            def DoLog(self, level, msg, timestamp):
                if (level >= 6):# and not self.debugLevel:
                    return
                sys.stderr.write("Error%d: %s\n" % (level, msg))
        wx.Log.SetActiveTarget(MyLog())

        eg.text = eg.Translation.Load(eg.config.language)

        Utils.SetClass(eg.text, eg.Text)

        from greenlet import greenlet
        eg.Greenlet = greenlet
        eg.mainGreenlet = greenlet.getcurrent()
        
        # replace builtin raw_input with a small dialog
        def raw_input(prompt=None):
            return eg.CallWait(
                partial(eg.SimpleInputDialog.CreateModal, prompt)
            )
        __builtin__.raw_input = raw_input

        # replace builtin input with a small dialog
        def input(prompt=None):
            return eval(raw_input(prompt))
        __builtin__.input = input
        
        # TODO: make this lazy imports
        from eg.WinApi.serial import Serial
        eg.SerialPort = Serial
        
        from eg.WinApi.SendKeys import SendKeysParser
        eg.SendKeys = SendKeysParser()
        
        import eg.WinApi.COMServer
        if not args.install:
            if args.translate:
                eg.LanguageEditor()
            else:
                self.StartGui()

        
    def InitComTypes(self):
        #Bit of a dance to force comtypes generated interfaces in to our directory
        import comtypes.client
        genPath = os.path.join(eg.CONFIG_DIR, "cgen_py").encode('mbcs')
        if not os.path.exists(genPath):
            os.makedirs(genPath)
        genInitPath = os.path.join(eg.CONFIG_DIR, "cgen_py", "__init__.py").encode('mbcs')
        if not os.path.exists(genInitPath):
            ofi = open(genInitPath, "w")
            ofi.write("# comtypes.gen package, directory for generated files.\n")
            ofi.close()
        
        comtypes.client.gen_dir = genPath
        import comtypes
        sys.path.insert(0, eg.CONFIG_DIR)
        sys.modules["comtypes.gen"] = comtypes.gen = __import__("cgen_py", globals(),locals(),[])
        del sys.path[0]
        import comtypes.client._generate
        comtypes.client._generate.__verbose__ = False

        
    def StartGui(self):
        import eg
        self.InitComTypes()
        # create a global asyncore loop thread
        # TODO: Only start if asyncore is requested
        eg.dummyAsyncoreDispatcher = None
        eg.RestartAsyncore()
        threading.Thread(target=asyncore.loop, name="AsyncoreThread").start()

        import eg.WinApi.COMServer
        
        eg.scheduler.start()
        eg.messageReceiver.Start()

        eg.focusEvent = eg.EventHook()
        eg.document = eg.Document()
        eg.taskBarIcon = eg.TaskBarIcon()
        
        if not (eg.config.hideOnStartup or eg.startupArguments.hideOnStartup):
            eg.document.ShowFrame()
            
        eg.SetProcessingState = eg.taskBarIcon.SetProcessingState

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

            
    def InitPil():
        """Initialize PIL's Image module."""
        import Image
        import PngImagePlugin
        import JpegImagePlugin
        import BmpImagePlugin
        import GifImagePlugin
        Image._initialized = 2  
        
    
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
        
        
    def RestartAsyncore():
        """ Informs the asyncore loop of a new socket to handle. """
        oldDispatcher = eg.dummyAsyncoreDispatcher
        dispatcher = asyncore.dispatcher()
        dispatcher.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.dummyAsyncoreDispatcher = dispatcher
        if oldDispatcher:
            oldDispatcher.close()
    
    
    def Exit():
        """
        Sometimes you want to quickly exit a PythonScript, because you don't 
        want to build deeply nested if-structures for example. eg.Exit() will 
        exit your PythonScript immediately. 
        (Note: This is actually a sys.exit() but will not exit EventGhost, 
        because the SystemExit exception is catched for a PythonScript.) 
        """
        sys.exit()
        
        
    def Wait(secs, raiseException=True):
        while secs > 0.0:
            if eg.stopExecutionFlag:
                if raiseException:
                    raise eg.StopException("Execution interrupted by the user.")
                else:
                    return False
            if secs > 0.1:
                time.sleep(0.1)
            else:
                time.sleep(secs)
            secs -= 0.1
        return True
        
        
    def HasActiveHandler(eventstring):
        for eventHandler in eg.eventTable.get(eventstring, []):
            obj = eventHandler
            while obj:
                if not obj.isEnabled:
                    break
                obj = obj.parent
            else:
                return True
        return False


    def Bind(eventString, eventFunc):
        eventTable = eg.eventTable2
        if eventString not in eventTable:
            eventTable[eventString] = []
        eventTable[eventString].append(eventFunc)
    
                
    def Unbind(eventString, eventFunc):
        eventTable = eg.eventTable2
        if eventString not in eventTable:
            return
        try:
            eventTable[eventString].remove(eventFunc)
        except:
            pass
        if len(eventTable[eventString]) == 0:
            del eventTable[eventString]


    def RunProgram():
        eg.stopExecutionFlag = False
        del eg.programReturnStack[:]
        while eg.programCounter is not None:
            programCounter = eg.programCounter
            item, idx = programCounter
            item.Execute()
            if eg.programCounter == programCounter:
                # program counter has not changed. Ask the parent for the next
                # item.
                if isinstance(item.parent, eg.MacroItem):
                    eg.programCounter = item.parent.GetNextChild(idx)
                else:
                    eg.programCounter = None
                
            while eg.programCounter is None and eg.programReturnStack:
                # we have no next item in this level. So look in the return 
                # stack if any return has to be executed
                item, idx = eg.programReturnStack.pop()
                eg.programCounter = item.parent.GetNextChild(idx)


    def StopMacro(ignoreReturn=False):
        """
        Instructs EventGhost to stop executing the current macro after the 
        current action (thus the PythonScript or PythonCommand) has finished. 
        """
        eg.programCounter = None
        if ignoreReturn:
            del eg.programReturnStack[:]
        
        
    def CallWait(func):
        result = [None]
        event = threading.Event()
        def CallWaitWrapper():
            try:
                result[0] = func()
            finally:
                event.set()
        wx.CallAfter(CallWaitWrapper)
        event.wait()
        return result[0]
            
            
    def GetConfig(searchPath, defaultCls):
        config = eg.config
        parts = searchPath.split(".")
        for part in parts[:-1]:
            config = config.SetDefault(part, eg.Bunch)
        return config.SetDefault(parts[-1], defaultCls)
            
            
    def DummyFunc(*args, **kwargs):
        pass

            
    class Exception(Exception):
        
        def __unicode__(self):
            return "\n".join([unicode(arg) for arg in self.args])


    class StopException(Exception):
        pass
    
    
    class HiddenAction:
        pass
    
