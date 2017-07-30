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

import sys
import wx
from ctypes import windll
from time import gmtime
from types import ModuleType
from os import listdir, makedirs, chdir
from os.path import join, basename, isdir, exists, splitext

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


    def Traverse(root, moduleRoot):
        for name in listdir(root):
            path = join(root, name)
            if isdir(path):
                name = basename(path)
                if name in [".svn", ".git", ".idea"]:
                    continue
                if not exists(join(path, "__init__.py")):
                    continue
                moduleName = moduleRoot + "." + name
                #print moduleName
                __import__(moduleName)
                Traverse(path, moduleName)
                continue
            base, ext = splitext(name)
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
    if startupFile and not exists(startupFile):
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
    if eg.WindowsVersion >= 'Vista':
        args = " ".join(eg.app.GetArguments())
        windll.kernel32.RegisterApplicationRestart(args, 8)

    eg.Print(eg.text.MainFrame.Logger.welcomeText)

def InitPathsAndBuiltins():
    import cFunctions
    import __builtin__

    eg.folderPath = eg.FolderPath()
    eg.mainDir = eg.folderPath.mainDir
    eg.configDir = eg.folderPath.configDir
    eg.corePluginDir = eg.folderPath.corePluginDir
    eg.localPluginDir = eg.folderPath.localPluginDir
    eg.imagesDir = eg.folderPath.imagesDir
    eg.languagesDir = eg.folderPath.languagesDir
    eg.sitePackagesDir = eg.folderPath.sitePackagesDir

    if not exists(eg.configDir):
        try:
            makedirs(eg.configDir)
        except:
            pass

    if not exists(eg.localPluginDir):
        try:
            makedirs(eg.localPluginDir)
        except:
            eg.localPluginDir = eg.corePluginDir

    if eg.Cli.args.isMain:
        if exists(eg.configDir):
            chdir(eg.configDir)
        else:
            chdir(eg.mainDir)

    __builtin__.wx = wx

    corePluginPackage = ModuleType("eg.CorePluginModule")
    corePluginPackage.__path__ = [eg.corePluginDir]
    userPluginPackage = ModuleType("eg.UserPluginModule")
    userPluginPackage.__path__ = [eg.localPluginDir]

    sys.modules["eg.CorePluginModule"] = corePluginPackage
    sys.modules["eg.UserPluginModule"] = userPluginPackage
    sys.modules['eg.cFunctions'] = cFunctions

    eg.pluginDirs = [eg.corePluginDir, eg.localPluginDir]
    eg.cFunctions = cFunctions
    eg.CorePluginModule = corePluginPackage
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
