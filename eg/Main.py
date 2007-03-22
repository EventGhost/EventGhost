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
import codecs

encoding = locale.getdefaultlocale()[1]
decoder = codecs.getdecoder(encoding)

#
locale.setlocale(locale.LC_ALL, '')
#if hasattr(sys,"setdefaultencoding"):
#    sys.setdefaultencoding(encoding)
#else:
#    # this needs the sitecustomize.py in the Python path
#    sys.setappdefaultencoding(encoding)


# get program directory
if hasattr(sys, "frozen"):
    mainDir = os.path.dirname(sys.executable)
else:
    mainDir = os.path.abspath(os.path.dirname(sys.argv[0]))

# change working directory to program directory
os.chdir(mainDir)

# append our pathes to sys.path
sys.path.append(mainDir + "\\eg")
sys.path.append(mainDir + "\\plugins")

# determine the commadline parameters
class args:
    hideOnStartup = False
    startupEvent = None
    startupFile = None
    allowMultiLoad = False
    debugLevel = 0
    
argv = [val.decode(encoding) for val in sys.argv]


i = 0
while True:
    i += 1
    if len(argv) <= i:
        break
    arg = argv[i].lower()
    if arg == "-n" or arg == "-netsend":
        import NetworkSend
        NetworkSend.Main(argv[i+1:])
        sys.exit(0)
    elif arg == '-debug':
        args.debugLevel = 1
    elif arg == '-debug2':
        args.debugLevel = 2
    elif arg == '-h' or arg == '-hide':
        args.hideOnStartup = True
    elif arg == '-install':
        import compileall
        compileall.compile_dir(mainDir)
        sys.exit(0)
    elif arg == '-uninstall':
        for root, dirs, files in os.walk(mainDir):
            for name in files:
                if name.lower().endswith(".pyc"):
                    os.remove(os.path.join(root, name))
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
        args.startupFile = argv[i]
    elif arg == '-translate':
        import LanguageEditor
        LanguageEditor.Start()
        sys.exit(0)

if not args.allowMultiLoad:
    # check if another instance of the program is running
    from win32process import ExitProcess
    import win32event, win32api
    appMutex = win32event.CreateMutex(
        None, 
        0, 
        "EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B"
    )
    if win32api.GetLastError() != 0:
        # another instance of EventGhost is running
        import win32com.client
        e = win32com.client.Dispatch("{7EB106DC-468D-4345-9CFE-B0021039114B}")
        if args.startupEvent is not None:
            e.TriggerEvent(args.startupEvent[0], args.startupEvent[1])
        else:
            e.BringToFront()
        ExitProcess(0)		
    

import Init
eg = Init.EventGhost()
eg.Init(args)
eg.StartGui()
eg.app.MainLoop()
ExitProcess(0)
