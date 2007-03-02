import os
import sys
import locale

encoding = locale.getdefaultlocale()[1]

locale.setlocale(locale.LC_ALL, '')
if hasattr(sys,"setdefaultencoding"):
    sys.setdefaultencoding(encoding)
else:
    # this needs the sitecustomize.py in the Python path
    sys.setappdefaultencoding(encoding)


# get program directory
if hasattr(sys, "frozen"):
    main_dir = os.path.dirname(sys.executable)
else:
    main_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

# change working directory to program directory
os.chdir(main_dir)

# append our pathes to sys.path
sys.path.append(main_dir + "\\eg")
sys.path.append(main_dir + "\\Plugins")

# determine the commadline parameters
hideOnStartup = False
startupEvent = None
startupPayload = []
startupFile = None
debugLevel = 0
i = 0

while True:
    i += 1
    if len(sys.argv) <= i:
        break
    arg = sys.argv[i].lower()
    if arg == '-debug':
        debugLevel = 1
    elif arg == '-debug2':
        debugLevel = 2
    elif arg == '-hide':
        hideOnStartup = True
    elif arg == '-install':
        import compileall
        compileall.compile_dir(main_dir)
        sys.exit(0)
    elif arg == '-uninstall':
        for root, dirs, files in os.walk(main_dir):
            for name in files:
                if name.lower().endswith(".pyc"):
                    os.remove(os.path.join(root, name))
        sys.exit(0)
    elif arg == '-e' or arg == '-event':
        i += 1
        if len(sys.argv) <= i:
            print "missing event string"
            break
        startupEvent = sys.argv[i]
        while i+1 < len(sys.argv):
            i += 1
            startupPayload.append(sys.argv[i])
    elif arg == '-f' or arg == '-file':
        i += 1
        if len(sys.argv) <= i:
            print "missing file string"
            break
        startupFile = sys.argv[i]
    elif arg == '-translate':
        import LanguageEditor
        LanguageEditor.Start()
        sys.exit(0)

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
    if startupEvent:
        e.TriggerEvent(startupEvent, startupPayload)
    else:
        e.BringToFront()
    ExitProcess(0)		
    

import Init
eg = Init.EventGhost()
eg.Init(debugLevel)
eg.StartGui((startupEvent, startupPayload), startupFile, hideOnStartup)
eg.app.MainLoop()
ExitProcess(0)
