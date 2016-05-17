# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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
Parses the command line arguments of the program.
"""

import ctypes
import locale
import os
import pywintypes
import sys
from os.path import abspath, dirname, join

ENCODING = locale.getdefaultlocale()[1]
locale.setlocale(locale.LC_ALL, '')
argvIter = (val.decode(ENCODING) for val in sys.argv)
scriptPath = argvIter.next()

# get program directory
mainDir = abspath(join(dirname(__file__.decode('mbcs')), ".."))

# determine the commandline parameters
import __main__  # NOQA
class args:
    hideOnStartup = False
    startupEvent = None
    startupFile = None
    allowMultiLoad = False
    debugLevel = 0
    translate = False
    configDir = None
    install = False
    isMain = hasattr(__main__, "isMain")  #splitext(basename(scriptPath))[0].lower() == "eventghost"
    pluginFile = None
    pluginDir = None


if args.isMain:
    for arg in argvIter:
        arg = arg.lower()
        if arg.startswith('-debug'):
            args.debugLevel = 1
            if len(arg) > 6:
                args.debugLevel = int(arg[6:])
        elif arg in ("-n", "-netsend"):
            from Classes.NetworkSend import Main
            Main(list(argvIter))
            sys.exit(0)
        elif arg in ('-h', '-hide'):
            args.hideOnStartup = True
        elif arg == '-install':
            import compileall
            compileall.compile_dir(mainDir)
            args.install = True
        elif arg == '-uninstall':
            for root, dirs, files in os.walk(mainDir):
                for name in files:
                    if name.lower().endswith(".pyc"):
                        os.remove(join(root, name))
            sys.exit(0)
        elif arg in ('-m', '-multiload'):
            args.allowMultiLoad = True
        elif arg in ('-e', '-event'):
            eventstring = argvIter.next()
            payloads = list(argvIter)
            if len(payloads) == 0:
                payloads = None
            args.startupEvent = (eventstring, payloads)
        elif arg in ('-f', '-file'):
            args.startupFile = abspath(argvIter.next())
        elif arg in ('-p', '-plugin'):
            args.pluginFile = abspath(argvIter.next())
            #args.isMain = False
        elif arg == '-plugindir':
            args.plugindir = argvIter.next()
        elif arg == '-configdir':
            args.configDir = argvIter.next()
        elif arg == '-translate':
            args.translate = True
        elif arg == "-restart":
            import time
            while True:
                appMutex = ctypes.windll.kernel32.CreateMutexA(
                    None,
                    0,
                    "Global\\EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B"
                )
                err = ctypes.GetLastError()
                if appMutex:
                    ctypes.windll.kernel32.CloseHandle(appMutex)
                if err == 0:
                    break
                time.sleep(0.1)
        else:
            path = abspath(arg)
            ext = os.path.splitext(path)[1].lower()
            if ext == ".egplugin":
                args.pluginFile = path
            elif ext in (".egtree", ".xml"):
                args.startupFile = path

    if (
        not args.allowMultiLoad and
        not args.translate and
        args.isMain  #and
        #not args.pluginFile
    ):
        # check if another instance of the program is running
        appMutex = ctypes.windll.kernel32.CreateMutexA(
            None,
            0,
            "Global\\EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B"
        )
        if ctypes.GetLastError() != 0:
            # another instance of EventGhost is running
            from win32com.client import Dispatch
            try:
                e = Dispatch("{7EB106DC-468D-4345-9CFE-B0021039114B}")
                if args.startupFile is not None:
                    e.OpenFile(args.startupFile)
                if args.startupEvent is not None:
                    e.TriggerEvent(args.startupEvent[0], args.startupEvent[1])
                elif args.pluginFile:
                    e.InstallPlugin(args.pluginFile)
                else:
                    e.BringToFront()
            except pywintypes.com_error as err:
                if err[0] == -2147024156:
                    msg = "Unable to launch unelevated while already running elevated."
                else:
                    msg = "Failed to launch for unknown reasons."
                ctypes.windll.user32.MessageBoxA(0, msg, "EventGhost", 48)
            finally:
                ctypes.windll.kernel32.ExitProcess(0)

    # change working directory to program directory
    if args.debugLevel < 1 and args.isMain:
        os.chdir(mainDir)
