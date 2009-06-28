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

import os
import sys
import locale
from os.path import join, dirname, basename, splitext

ENCODING = locale.getdefaultlocale()[1]
locale.setlocale(locale.LC_ALL, '')


# get program directory
if hasattr(sys, "frozen"):
    MAIN_DIR = dirname(unicode(sys.executable, sys.getfilesystemencoding()))
else:
    MAIN_DIR = os.path.abspath(join(dirname(__file__), ".."))

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
    isMain = splitext(basename(sys.argv[0]))[0].lower() == "eventghost"
    
argv = [val.decode(ENCODING) for val in sys.argv]

i = 0
while True:
    i += 1
    if len(argv) <= i:
        break
    arg = argv[i].lower()
    if arg == "-n" or arg == "-netsend":
        from Classes.NetworkSend import Main
        Main(argv[i+1:])
        sys.exit(0)
    elif arg == '-debug':
        args.debugLevel = 1
    elif arg == '-debug2':
        args.debugLevel = 2
    elif arg == '-h' or arg == '-hide':
        args.hideOnStartup = True
    elif arg == '-install':
        import compileall
        compileall.compile_dir(MAIN_DIR)
        args.install = True
    elif arg == '-uninstall':
        for root, dirs, files in os.walk(MAIN_DIR):
            for name in files:
                if name.lower().endswith(".pyc"):
                    os.remove(join(root, name))
        sys.exit(0)
    elif arg == '-m' or arg == '-multiload':
        args.allowMultiLoad = True
    elif arg == '-e' or arg == '-event':
        i += 1
        if len(argv) <= i:
            print "missing event string"
            break
        eventstring = argv[i]
        if len(argv) <= i + 1:
            payloads = None
        else:
            payloads = []
            while i + 1 < len(argv):
                i += 1
                payloads.append(argv[i])
        args.startupEvent = (eventstring, payloads)
    elif arg == '-f' or arg == '-file':
        i += 1
        if len(argv) <= i:
            print "missing file string"
            break
        args.startupFile = os.path.abspath(argv[i])
    elif arg == '-configdir':
        i += 1
        if len(argv) <= i:
            print "missing directory string"
            break
        args.configDir = argv[i]
    elif arg == '-translate':
        args.translate = True


if not args.allowMultiLoad and not args.translate and args.isMain:
    # check if another instance of the program is running
    import ctypes
    appMutex = ctypes.windll.kernel32.CreateMutexA(
        None,
        0,
        "Global\\EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B"
    )
    if ctypes.GetLastError() != 0:
        # another instance of EventGhost is running
        import win32com.client
        e = win32com.client.Dispatch("{7EB106DC-468D-4345-9CFE-B0021039114B}")
        if args.startupFile is not None:
            e.OpenFile(args.startupFile)
        if args.startupEvent is not None:
            e.TriggerEvent(args.startupEvent[0], args.startupEvent[1])
        else:
            e.BringToFront()
        ctypes.windll.kernel32.ExitProcess(0)

# change working directory to program directory
if args.debugLevel < 1 and args.isMain:
    os.chdir(MAIN_DIR)

