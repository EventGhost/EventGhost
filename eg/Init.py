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

import os
import site
import sys
import winreg
import wx
from ctypes import windll
from time import gmtime
from types import ModuleType

# Local imports
import eg

def DeInit():
    eg.PrintDebugNotice("stopping threads")
    eg.actionThread.Func(eg.actionThread.StopSession)()
    eg.scheduler.Stop()
    eg.actionThread.Stop()
    eg.eventThread.Stop()

    eg.PrintDebugNotice("shutting down")
    eg.config.Save()
    eg.messageReceiver.Stop()
    if eg.dummyAsyncoreDispatcher:
        eg.dummyAsyncoreDispatcher.close()

def ImportAll():
    from os.path import join, basename

    def Traverse(root, moduleRoot):
        for name in os.listdir(root):
            path = join(root, name)
            if os.path.isdir(path):
                name = basename(path)
                if name in [".svn", ".git", ".idea"]:
                    continue
                if not os.path.exists(join(path, "__init__.py")):
                    continue
                moduleName = moduleRoot + "." + name
                #print moduleName
                __import__(moduleName)
                Traverse(path, moduleName)
                continue
            base, ext = os.path.splitext(name)
            if ext != ".py":
                continue
            if base == "__init__":
                continue
            moduleName = moduleRoot + "." + base
            if moduleName in (
                "eg.StaticImports",
                "eg.CorePluginModule.EventGhost.OsdSkins.Default",
            ):
                continue
            #print moduleName
            __import__(moduleName)

    Traverse(join(eg.mainDir, "eg"), "eg")
    Traverse(eg.corePluginDir, "eg.CorePluginModule")

def Init():
    import WinApi.pywin32_patches # NOQA

    if eg.startupArguments.isMain or eg.startupArguments.install:
        import WinApi.COMServer  # NOQA

def InitGui():
    #import eg.WinApi.COMServer

    import __builtin__
    __builtin__.raw_input = RawInput
    __builtin__.input = Input

    eg.scheduler.start()
    eg.messageReceiver.Start()

    eg.document = eg.Document()

    if eg.config.showTrayIcon:
        if not (eg.config.hideOnStartup or eg.startupArguments.hideOnStartup):
            eg.document.ShowFrame()
    else:
        eg.document.ShowFrame()
        if eg.config.hideOnStartup or eg.startupArguments.hideOnStartup:
            eg.mainFrame.Iconize(True)

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
        today = gmtime()[:3]
        if config.lastUpdateCheckDate != today:
            config.lastUpdateCheckDate = today
            wx.CallAfter(eg.CheckUpdate.Start)

    # Register restart handler for easy crash recovery.
    if eg.WindowsVersion.IsVista():
        args = " ".join(eg.app.GetArguments())
        windll.kernel32.RegisterApplicationRestart(args, 8)

    eg.Print(eg.text.MainFrame.Logger.welcomeText)

def InitPathsAndBuiltins():
    sys.path.insert(0, eg.mainDir.encode('mbcs'))
    sys.path.insert(1, eg.sitePackagesDir.encode('mbcs'))

    try:
        if "PYTHONPATH" in os.environ:
            for path in os.environ.get("PYTHONPATH").split(os.pathsep):
                site.addsitedir(path)

        key = winreg.HKEY_LOCAL_MACHINE
        version = sys.version_info[:2]
        subkey = r"SOFTWARE\Python\PythonCore\%d.%d\InstallPath" % version
        with winreg.OpenKey(key, subkey) as hand:
            site.addsitedir(
                os.path.join(
                    winreg.QueryValue(hand, None),
                    "Lib",
                    "site-packages",
                )
            )
    except:
        pass

    import cFunctions
    sys.modules["eg.cFunctions"] = cFunctions
    eg.cFunctions = cFunctions

    # add 'wx' to the builtin name space of every module
    import __builtin__
    __builtin__.wx = wx

    # we create a package 'PluginModule' and set its path to the plugin-dir
    # so we can simply use __import__ to load a plugin file
    corePluginPackage = ModuleType("eg.CorePluginModule")
    corePluginPackage.__path__ = [eg.corePluginDir]
    sys.modules["eg.CorePluginModule"] = corePluginPackage
    eg.CorePluginModule = corePluginPackage
    # we create a package 'PluginModule' and set its path to the plugin-dir
    # so we can simply use __import__ to load a plugin file
    if not os.path.exists(eg.localPluginDir):
        os.makedirs(eg.localPluginDir)
    userPluginPackage = ModuleType("eg.UserPluginModule")
    userPluginPackage.__path__ = [eg.localPluginDir]
    sys.modules["eg.UserPluginModule"] = userPluginPackage
    eg.UserPluginModule = userPluginPackage

def InitPil():
    """
    Initialize PIL's Image module.
    """
    import PIL.Image
    import PIL.PngImagePlugin
    import PIL.JpegImagePlugin
    import PIL.BmpImagePlugin
    import PIL.GifImagePlugin
    PIL.Image._initialized = 2

# replace builtin input() with a small dialog
def Input(prompt=None):
    return eval(eg.SimpleInputDialog.RawInput(prompt))

# replace builtin raw_input() with a small dialog
def RawInput(prompt=None):
    return eg.SimpleInputDialog.RawInput(prompt)
