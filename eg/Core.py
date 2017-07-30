# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import asyncore
import locale
import os
import socket
import sys
import threading
import time
import wx
from os.path import exists, join

# Local imports
import eg
import Init
import NamedPipe


eg.useTreeItemGUID = False

Init.InitPathsAndBuiltins()

eg.CORE_PLUGIN_GUIDS = (
    "{9D499A2C-72B6-40B0-8C8C-995831B10BB4}",  # "EventGhost"
    "{A21F443B-221D-44E4-8596-E1ED7100E0A4}",  # "System"
    "{E974D074-B0A3-4D0C-BBD1-992475DDD69D}",  # "Window"
    "{6B1751BF-F94E-4260-AB7E-64C0693FD959}",  # "Mouse"
)


eg.namedPipe = NamedPipe.Server()

if eg.Cli.args.isMain:
    eg.namedPipe.start()

eg.ID_TEST = wx.NewId()
eg.mainDir = eg.Cli.mainDir

eg.revision = 2000  # Deprecated
eg.startupArguments = eg.Cli.args
eg.debugLevel = eg.startupArguments.debugLevel
eg.systemEncoding = locale.getdefaultlocale()[1]
eg.document = None
eg.mainFrame = None
eg.result = None
eg.plugins = eg.Bunch()
eg.globals = eg.Bunch()
eg.globals.eg = eg
eg.event = None
eg.eventTable = {}
eg.eventString = ""
eg.notificationHandlers = {}
eg.programCounter = None
eg.programReturnStack = []
eg.indent = 0
eg.pluginList = []
eg.mainThread = threading.currentThread()
eg.stopExecutionFlag = False
eg.lastFoundWindows = []
eg.currentItem = None
eg.actionGroup = eg.Bunch()
eg.actionGroup.items = []
eg.GUID = eg.GUID()

def _CommandEvent():
    """Generate new (CmdEvent, Binder) tuple
        e.g. MooCmdEvent, EVT_MOO = EgCommandEvent()
    """
    evttype = wx.NewEventType()

    class _Event(wx.PyCommandEvent):
        def __init__(self, id, **kw):
            wx.PyCommandEvent.__init__(self, evttype, id)
            self.__dict__.update(kw)
            if not hasattr(self, "value"):
                self.value = None

        def GetValue(self):
            return self.value

        def SetValue(self, value):
            self.value = value

    return _Event, wx.PyEventBinder(evttype, 1)

eg.CommandEvent = _CommandEvent
eg.ValueChangedEvent, eg.EVT_VALUE_CHANGED = eg.CommandEvent()

eg.pyCrustFrame = None
eg.dummyAsyncoreDispatcher = None

from eg.WinApi.Dynamic import GetCurrentProcessId  # NOQA
eg.processId = GetCurrentProcessId()
Init.InitPil()

class Exception(Exception):
    def __unicode__(self):
        try:
            return "\n".join([unicode(arg) for arg in self.args])
        except UnicodeDecodeError:
            return "\n".join([str(arg).decode('mbcs') for arg in self.args])


class StopException(Exception):
    pass


class HiddenAction:
    pass


def Bind(notification, listener):
    if notification not in eg.notificationHandlers:
        notificationHandler = eg.NotificationHandler()
        eg.notificationHandlers[notification] = notificationHandler
    else:
        notificationHandler = eg.notificationHandlers[notification]
    notificationHandler.listeners.append(listener)

def CallWait(func, *args, **kwargs):
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

def DummyFunc(*dummyArgs, **dummyKwargs):
    """
    Just a do-nothing-function, that accepts arbitrary arguments.
    """
    pass

def Exit():
    """
    Sometimes you want to quickly exit a PythonScript, because you don't
    want to build deeply nested if-structures for example. eg.Exit() will
    exit your PythonScript immediately.
    (Note: This is actually a sys.exit() but will not exit EventGhost,
    because the SystemExit exception is catched for a PythonScript.)
    """
    sys.exit()

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

def MessageBox(message, caption=eg.APP_NAME, style=wx.OK, parent=None):
    if parent is None:
        style |= wx.STAY_ON_TOP
    dialog = eg.MessageDialog(parent, message, caption, style)
    result = dialog.ShowModal()
    dialog.Destroy()
    return result

def Notify(notification, value=None):
    if notification in eg.notificationHandlers:
        for listener in eg.notificationHandlers[notification].listeners:
            listener(value)

# pylint: disable-msg=W0613
def RegisterPlugin(
    name = None,
    description = None,
    kind = "other",
    author = "[unknown author]",
    version = "[unknown version]",
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
    :param description: a short description of the plugin.
    :param kind: gives a hint about the category the plugin belongs to. It
        should be a string with a value out of ``"remote"`` (for remote
        receiver plugins), ``"program"`` (for program control plugins),
        ``"external"`` (for plugins that control external hardware) or
        ``"other"`` (if none of the other categories match).
    :param author: can be set to the name or a list of names of the
        developer(s) of the plugin.
    :param version: can be set to a version string.
    :param icon: can be a base64 encoded image for the plugin. If
        ``icon == None``, an "icon.png" will be used if it exists
        in the plugin folder.
    :param canMultiLoad: set this to ``True``, if a configuration can have
       more than one instance of this plugin.
    :param createMacrosOnAdd: if set to ``True``, when adding the plugin,
        EventGhost will ask the user, if he/she wants to add a folder with all
        actions of this plugin to his/her configuration.
    :param url: displays a clickable link in the plugin info dialog.
    :param help: a longer description and/or additional information for the
        plugin. Will be added to
        'description'.
    :param guid: will help EG to identify your plugin, so there are no name
        clashes with other plugins that accidentally might have the same
        name and will later ease the update of plugins.
    :param \*\*kwargs: just to consume unknown parameters, to make the call
       backward compatible.
    """
    pass
# pylint: enable-msg=W0613

def RestartAsyncore():
    """
    Informs the asyncore loop of a new socket to handle.
    """
    oldDispatcher = eg.dummyAsyncoreDispatcher
    dispatcher = asyncore.dispatcher()
    dispatcher.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    eg.dummyAsyncoreDispatcher = dispatcher
    if oldDispatcher:
        oldDispatcher.close()
    if oldDispatcher is None:
        # create a global asyncore loop thread
        threading.Thread(target=asyncore.loop, name="AsyncoreThread").start()

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

def StopMacro(ignoreReturn=False):
    """
    Instructs EventGhost to stop executing the current macro after the
    current action (thus the PythonScript or PythonCommand) has finished.
    """
    eg.programCounter = None
    if ignoreReturn:
        del eg.programReturnStack[:]

def Unbind(notification, listener):
    eg.notificationHandlers[notification].listeners.remove(listener)

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

# now assign all the functions above to `eg`
eg.Bind = Bind
eg.CallWait = CallWait
eg.DummyFunc = DummyFunc
eg.Exception = Exception
eg.Exit = Exit
eg.HasActiveHandler = HasActiveHandler
eg.HiddenAction = HiddenAction
eg.MessageBox = MessageBox
eg.Notify = Notify
eg.RegisterPlugin = RegisterPlugin
eg.RestartAsyncore = RestartAsyncore
eg.RunProgram = RunProgram
eg.StopException = StopException
eg.StopMacro = StopMacro
eg.Unbind = Unbind
eg.Wait = Wait

eg.messageReceiver = eg.MainMessageReceiver()
eg.app = eg.App()

# we can't import the Icons module earlier, because wx.App must exist
import Icons  # NOQA
eg.Icons = Icons

eg.log = eg.Log()
eg.Print = eg.log.Print
eg.PrintError = eg.log.PrintError
eg.PrintNotice = eg.log.PrintNotice
eg.PrintTraceback = eg.log.PrintTraceback
eg.PrintDebugNotice = eg.log.PrintDebugNotice
eg.PrintStack = eg.log.PrintStack

eg.config = eg.Config()
eg.debugLevel = int(eg.config.logDebug) or eg.debugLevel

def TracebackHook(tType, tValue, traceback):
    eg.log.PrintTraceback(excInfo=(tType, tValue, traceback))
sys.excepthook = TracebackHook

eg.colour = eg.Colour()
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

from eg.WinApi.SendKeys import SendKeysParser  # NOQA
eg.SendKeys = SendKeysParser()

setattr(eg, "PluginClass", eg.PluginBase)
setattr(eg, "ActionClass", eg.ActionBase)

eg.taskBarIcon = eg.TaskBarIcon(
    eg.startupArguments.isMain and
    eg.config.showTrayIcon and
    not eg.startupArguments.translate and
    not eg.startupArguments.install and
    not eg.startupArguments.pluginFile
)
eg.SetProcessingState = eg.taskBarIcon.SetProcessingState
eg.wit = None

eg.Init = Init
eg.Init.Init()
