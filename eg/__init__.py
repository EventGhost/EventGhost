# This file is not used by the EventGhost application. It only exists to 
# build the API documentation with epydoc.
"""
The one and all eg object.

:group User Interface: 
    ConfigurationDialog, SpinNumCtrl, SpinIntCtrl, SerialPortChoice,
    DirBrowseButton, FileBrowseButton
:group Utility: 
    Bunch, Exception, ThreadWorker
:group Constants: 
    APP_NAME, APPDATA, PLUGIN_DIR
:group Function Decorators:
    LogIt, LogItWithReturn, AssertNotMainThread, TimeIt
    
:undocumented: AssertNotMainThread, ActionMetaClass, PluginMetaClass, 
    ActionGroup, Controls, Dialogs, EventGhostEvent, EventThread, TreeItems,
    PluginDatabase, PluginTools, _app, _name
"""

import wx as _wx
import locale as _locale
import os as _os

#: Indicates the debug level (0=no debugging)
debugLevel = 0

#: Every action in EventGhost returns a result. For most actions this is 
#: simply Python's None, but some might return a result that is useful for 
#: later evaluation. For example the 'Window/Find Window' action returns a 
#: list of the window-handles it has found (or an empty list if it hasn't 
#: found anything). So you can place a PythonScript directly after the 
# 'Find Window' action and do something with this list.
result = None

#: The applications name.
APP_NAME = "EventGhost"

#: This is the path to the Application Data on Windows. This will look 
#: like this: C:\\Documents and Settings\\[User Name]\\Application Data
APPDATA = ""

#: Path to the directory where the plugins are stored.
PLUGIN_DIR = _os.path.abspath("plugins")

from Utils import Bunch

globals = Bunch()
plugins = Bunch()
event = None

class Exception(Exception):
    """Base class of all custom exceptions inside EventGhost."""
    pass

_app = _wx.App()
import Utils
from Utils import LogIt
from Utils import LogItWithReturn
from Utils import AssertNotMainThread
from Utils import TimeIt

import Icons
from PluginClass import PluginClass
from ActionClass import ActionClass
from ActionClass import ActionWithStringParameter

from Dialogs.ConfigurationDialog import ConfigurationDialog
from Controls.SpinIntCtrl import SpinIntCtrl
from Controls.SpinNumCtrl import SpinNumCtrl
from Controls.SerialPortChoice import SerialPortChoice
from Controls.FileBrowseButton import FileBrowseButton
from Controls.DirBrowseButton import DirBrowseButton

from ThreadWorker import ThreadWorker

from EventThread import EventThread as _EventThread
TriggerEvent = staticmethod(_EventThread.TriggerEvent)

def RegisterPlugin(        
    name = None,
    description = None,
    kind = "other",
    author = "unknown author",
    version = "unknown version",
    icon = None,
    canMultiLoad = False,
):
    pass
from PluginDatabase import PluginFileInfo as _PluginFileInfo
RegisterPlugin.__doc__ = _PluginFileInfo.RegisterPlugin.__doc__

__all__ = [_name for _name in dir() if not _name.startswith('_')]
