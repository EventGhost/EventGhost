# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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
"""
.. attribute:: globals

    :class:`eg.Bunch` instance, that holds all global variables used by
    PythonCommand actions. PythonScripts (and all other code) can access
    these globals through :obj:`eg.globals`.


.. attribute:: event

    Instance of the :class:`eg.EventGhostEvent` instance, that is currently
    been processed.

.. autofunction:: eg.DummyFunc
"""

import wx
import sys
import asyncore
import socket
import time
import threading
import locale
from os.path import join
from wx.lib.newevent import NewCommandEvent
import eg
import Init


eg.APP_NAME = "EventGhost"
eg.CORE_PLUGIN_GUIDS = (
    "{9D499A2C-72B6-40B0-8C8C-995831B10BB4}", # "EventGhost"
    "{A21F443B-221D-44E4-8596-E1ED7100E0A4}", # "System"
    "{E974D074-B0A3-4D0C-BBD1-992475DDD69D}", # "Window"
    "{6B1751BF-F94E-4260-AB7E-64C0693FD959}", # "Mouse"
)
eg.ID_TEST = wx.NewId()
eg.mainDir = eg.Cli.mainDir
eg.imagesDir = join(eg.mainDir, "images")
eg.languagesDir = join(eg.mainDir, "languages")
eg.sitePackagesDir = join(
    eg.mainDir, 
    "lib%d%d" % sys.version_info[:2], 
    "site-packages"
)
eg.revision = eg.Version.revision
eg.startupArguments = eg.Cli.args
eg.debugLevel = eg.startupArguments.debugLevel
eg.systemEncoding = locale.getdefaultlocale()[1]
eg.document = None
eg.result = None
eg.plugins = eg.Bunch()
eg.globals = eg.Bunch()
eg.globals.eg = eg
eg.event = None
eg.eventTable = {}
eg.eventString = ""
eg.EventString = "" # eg.EventString is deprecated
eg.notificationHandlers = {}
eg.programCounter = None
eg.programReturnStack = []
eg.indent = 0
eg.pluginList = []
eg.mainThread = threading.currentThread()
eg.stopExecutionFlag = False
eg.lastFoundWindows = []
eg.currentItem = None
eg.currentConfigureItem = None
eg.actionGroup = eg.Bunch()
eg.actionGroup.items = []
eg.folderPath = eg.FolderPath()
eg.ValueChangedEvent, eg.EVT_VALUE_CHANGED = NewCommandEvent()
eg.pyCrustFrame = None
eg.dummyAsyncoreDispatcher = None

if eg.startupArguments.configDir is None:
    eg.configDir = join(eg.folderPath.RoamingAppData, eg.APP_NAME)
else:
    eg.configDir = eg.startupArguments.configDir
eg.userPluginDir = join(eg.configDir, "plugins")
eg.corePluginDir = join(eg.mainDir, "plugins")

Init.InitPathesAndBuiltins()
from eg.WinApi.Dynamic import GetCurrentProcessId
eg.processId = GetCurrentProcessId()
Init.InitPil()

def RestartAsyncore():
    """ Informs the asyncore loop of a new socket to handle. """
    oldDispatcher = eg.dummyAsyncoreDispatcher
    dispatcher = asyncore.dispatcher()
    dispatcher.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    eg.dummyAsyncoreDispatcher = dispatcher
    if oldDispatcher:
        oldDispatcher.close()
    if oldDispatcher is None:
        # create a global asyncore loop thread
        threading.Thread(target=asyncore.loop, name="AsyncoreThread").start()


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


def Bind(notification, listener):
    if notification not in eg.notificationHandlers:
        notificationHandler = eg.NotificationHandler()
        eg.notificationHandlers[notification] = notificationHandler
    else:
        notificationHandler = eg.notificationHandlers[notification]
    notificationHandler.listeners.append(listener)
    return notificationHandler.value


def Unbind(notification, listener):
    eg.notificationHandlers[notification].listeners.remove(listener)


def Notify(notification, value=None):
    if notification not in eg.notificationHandlers:
        eg.notificationHandlers[notification] = eg.NotificationHandler(value)
        return
    notificationHandler = eg.notificationHandlers[notification]
    notificationHandler.value = value
    for listener in notificationHandler.listeners:
        listener(value)


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


def DummyFunc(*dummyArgs, **dummyKwargs):
    """
    Just a do-nothing-function, that accepts arbitrary arguments.
    """
    pass


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
            eg.indent -= 2
            item, idx = eg.programReturnStack.pop()
            eg.programCounter = item.parent.GetNextChild(idx)
    eg.indent = 0


class Exception(Exception):

    def __unicode__(self):
        return "\n".join([unicode(arg) for arg in self.args])



class StopException(Exception):
    pass



class HiddenAction:
    pass


def MessageBox(message, caption=eg.APP_NAME, style=wx.OK, parent=None):
    if parent is None:
        style |= wx.STAY_ON_TOP
    dialog = eg.MessageDialog(parent, message, caption, style)
    result = dialog.ShowModal()
    dialog.Destroy()
    return result


# pylint: disable-msg=W0613
def RegisterPlugin(
    name = None,
    description = None,
    kind = "other",
    author = "unknown author",
    version = "unknown version",
    icon = None,
    canMultiLoad = False,
    createMacrosOnAdd = False,
    url = None,
    help = None,
    guid = None,
    **kwargs
):
    """
    Registers information about a plugin to EventGhost.

    :param name: should be a short descriptive string with the name of the
       plugin.
    :param description: the description of the plugin.
    :param kind: gives a hint about the category the plugin belongs to. It
       should be a string with a value out of "remote" (for remote receiver
       plugins), "program" (for program control plugins), "external" (for
       plugins that control external hardware) or "other" (if none of the
       other categories match).
    :param author: can be set to the name of the developer of the plugin.
    :param version: can be set to a version string.
    :param canMultiLoad: set this to ``True``, if a configuration can have
       more than one instance of this plugin.
    :param \*\*kwargs: just to consume unknown parameters, to make the call
       backward compatible.
    """
    pass
# pylint: enable-msg=W0613

eg.RegisterPlugin = RegisterPlugin

# now assign all the functions above to `eg`
eg.RestartAsyncore = RestartAsyncore
eg.Exit = Exit
eg.Wait = Wait
eg.HasActiveHandler = HasActiveHandler
eg.Bind = Bind
eg.Unbind = Unbind
eg.Notify = Notify
eg.StopMacro = StopMacro
eg.CallWait = CallWait
eg.DummyFunc = DummyFunc
eg.RunProgram = RunProgram
eg.Exception = Exception
eg.StopException = StopException
eg.HiddenAction = HiddenAction
eg.MessageBox = MessageBox

eg.messageReceiver = eg.MessageReceiver()
eg.app = eg.App()

import Icons # we can't import the Icons module earlier, because wx.App
             # must exist before
eg.Icons = Icons

eg.log = eg.Log()
eg.Print = eg.log.Print
eg.PrintError = eg.log.PrintError
eg.PrintNotice = eg.log.PrintNotice
eg.PrintTraceback = eg.log.PrintTraceback
eg.PrintDebugNotice = eg.log.PrintDebugNotice
eg.PrintStack = eg.log.PrintStack

def TracebackHook(tType, tValue, traceback):
    eg.log.PrintTraceback(excInfo=(tType, tValue, traceback))
sys.excepthook = TracebackHook

eg.colour = eg.Colour()
eg.config = eg.Config()
if eg.startupArguments.isMain and not eg.startupArguments.translate:
    eg.text = eg.Text(eg.config.language)
else:
    eg.text = eg.Text('en_EN')
eg.actionThread = eg.ActionThread()
eg.eventThread = eg.EventThread()
eg.pluginManager = eg.PluginManager()
eg.scheduler = eg.Scheduler()

eg.TriggerEvent = eg.eventThread.TriggerEvent
eg.TriggerEnduringEvent = eg.eventThread.TriggerEnduringEvent

from eg.WinApi.SendKeys import SendKeysParser
eg.SendKeys = SendKeysParser()

setattr(eg, "PluginClass", eg.PluginBase)
setattr(eg, "ActionClass", eg.ActionBase)

eg.taskBarIcon = eg.TaskBarIcon(
    eg.startupArguments.isMain
    and not eg.startupArguments.translate
    and not eg.startupArguments.install
    and not eg.startupArguments.pluginFile
)
eg.SetProcessingState = eg.taskBarIcon.SetProcessingState

eg.Init = Init
eg.Init.Init()


