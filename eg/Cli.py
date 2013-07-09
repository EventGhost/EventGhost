# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Parses the command line arguments of the program.
"""

import os
import sys
import locale
from os.path import join, dirname, basename, splitext, abspath

ENCODING = locale.getdefaultlocale()[1]
locale.setlocale(locale.LC_ALL, '')
argvIter = (val.decode(ENCODING) for val in sys.argv)
scriptPath = argvIter.next()

# get program directory
mainDir = abspath(
    join(dirname(__file__.decode(sys.getfilesystemencoding())), "..")
)

# determine the commandline parameters
class args:
    hideOnStartup = False
    startupEvent = None
    startupFile = None
    allowMultiLoad = False
    debugLevel = 0
    translate = False
    configDir = None
    install = False
    isMain = splitext(basename(scriptPath))[0].lower() == "eventghost"
    pluginFile = None
    pluginDir = None


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
        args.isMain = False
    elif arg == '-plugindir':
        args.plugindir = argvIter.next()
    elif arg == '-configdir':
        args.configDir = argvIter.next()
    elif arg == '-translate':
        args.translate = True

if (
    not args.allowMultiLoad
    and not args.translate
    and args.isMain
    and not args.pluginFile
):
    # check if another instance of the program is running
    import ctypes
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
            else:
                e.BringToFront()
        finally:
            ctypes.windll.kernel32.ExitProcess(0)

# change working directory to program directory
if args.debugLevel < 1 and args.isMain:
    os.chdir(mainDir)

