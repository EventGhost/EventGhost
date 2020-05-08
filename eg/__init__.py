# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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

import stackless
import sys

# the following three import are needed if we are running from source and the
# Python distribution was not installed by the installer. See the following
# link for details:
# http://www.voidspace.org.uk/python/movpy/reference/win32ext.html#id10
import pywintypes  # NOQA
import pythoncom  # NOQA
import win32api  # NOQA

# Local imports
import Cli
from Utils import *  # NOQA
from Classes.WindowsVersion import WindowsVersion


APP_NAME = "EventGhost"


class DynamicModule(object):
    def __init__(self):
        mod = sys.modules[__name__]
        self.__dict__ = mod.__dict__
        self.__orignal_module__ = mod
        sys.modules[__name__] = self

        import __builtin__
        __builtin__.eg = self

    def __getattr__(self, name):
        mod = __import__("eg.Classes." + name, None, None, [name], 0)
        self.__dict__[name] = attr = getattr(mod, name)
        return attr

    def __repr__(self):
        return "<dynamic-module '%s'>" % self.__name__

    def RaiseAssignments(self):
        """
        After this method is called, creation of new attributes will raise
        AttributeError.

        This is meanly used to find unintended assignments while debugging.
        """
        def __setattr__(self, name, value):
            if name not in self.__dict__:
                try:
                    raise AttributeError(
                        "Assignment to new attribute %s" % name
                    )
                except AttributeError:
                    import traceback
                    eg.PrintWarningNotice(traceback.format_exc())

            object.__setattr__(self, name, value)
        self.__class__.__setattr__ = __setattr__

    def Main(self):
        if Cli.args.install:
            return
        if Cli.args.translate:
            eg.LanguageEditor()
        elif Cli.args.pluginFile:
            eg.PluginInstall.Import(Cli.args.pluginFile)
            return
        else:
            eg.Init.InitGui()
        if eg.debugLevel:
            try:
                eg.Init.ImportAll()
            except:
                eg.PrintDebugNotice(sys.exc_info()[1])
        eg.Tasklet(eg.app.MainLoop)().run()
        stackless.run()


eg = DynamicModule()

# This is only here to make pylint happy. It is never really imported
if "pylint" in sys.modules:
    def RaiseAssignments():
        pass

    from Init import ImportAll
    ImportAll()

    from StaticImports import *  # NOQA
    import Core

    useTreeItemGUID = Core.eg.useTreeItemGUID
    CORE_PLUGIN_GUIDS = Core.eg.CORE_PLUGIN_GUIDS

    import LoopbackSocket

    socketSever = LoopbackSocket.Start()
    ID_TEST = Core.eg.ID_TEST
    revision = Core.eg.revision
    startupArguments = Cli.args
    systemEncoding = Core.eg.systemEncoding
    mainFrame = Core.eg.mainFrame
    result = Core.eg.result
    plugins = Core.eg.plugins
    globals = Bunch()
    globals.eg = Core.eg
    event = Core.eg.event
    eventTable = Core.eg.eventTable
    eventString = Core.eg.eventString
    notificationHandlers = Core.eg.notificationHandlers
    programCounter = Core.eg.programCounter
    programReturnStack = Core.eg.programReturnStack
    indent = Core.eg.indent
    pluginList = Core.eg.pluginList
    mainThread = Core.eg.mainThread
    stopExecutionFlag = Core.eg.stopExecutionFlag
    lastFoundWindows = Core.eg.lastFoundWindows
    currentItem = Core.eg.currentItem
    actionGroup = Bunch()
    actionGroup.items = []
    GUID = GUID()
    CommandEvent = Core._CommandEvent
    ValueChangedEvent, EVT_VALUE_CHANGED = (
        Core.eg.ValueChangedEvent, Core.eg.EVT_VALUE_CHANGED
    )
    pyCrustFrame = Core.eg.pyCrustFrame
    dummyAsyncoreDispatcher = Core.eg.dummyAsyncoreDispatcher
    processId = Core.eg.processId
    messageReceiver = MainMessageReceiver()
    app = App()
    log = Log()


    def Print(*args, **kwargs):
        pass

    def PrintDebugNotice(*args):
        pass

    def PrintWarningNotice(*args):
        pass

    def PrintError(*args, **kwargs):
        pass

    def PrintNotice(*args, **kwargs):
        pass

    def PrintStack(skip=0):
        pass

    def PrintTraceback(msg=None, skip=0, source=None, excInfo=None):
        pass


    config = Config()
    debugLevel = config.logDebug
    colour = Colour()
    text = Text('en_US')
    actionThread = ActionThread()
    eventThread = EventThread()
    pluginManager = PluginManager()
    scheduler = Scheduler()


    def TriggerEvent(
        suffix,
        payload=None,
        prefix="Main",
        source=Core.eg
    ):
        pass


    def TriggerEnduringEvent(
        suffix,
        payload=None,
        prefix="Main",
        source=Core.eg
    ):
        pass

    from WinApi.SendKeys import SendKeysParser
    SendKeys = SendKeysParser()

    PluginClass = PluginBase
    ActionClass = ActionBase
    taskBarIcon = TaskBarIcon(False)

    def SetProcessingState(state, event):
        pass

    wit = False
    document = Document()
    folderPath = FolderPath()
    mainDir = ''
    configDir = ''
    corePluginDir = ''
    localPluginDir = ''
    imagesDir = ''
    languagesDir = ''
    sitePackagesDir = ''
    pluginDirs = []
    cFunctions = None
    CorePluginModule = None
    UserPluginModule = None

    from Core import *  # NOQA

import Core  # NOQA

if eg.debugLevel:
    eg.RaiseAssignments()
