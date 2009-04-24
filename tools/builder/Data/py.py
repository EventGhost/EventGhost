import sys
import os
sys.path.append(os.getcwdu())

if len(sys.argv) > 1:
    mainFilePath = os.path.abspath(sys.argv[1].encode('mbcs'))
    sys.argv = sys.argv[1:]
    sys.argv[0] = mainFilePath
    import imp
    imp.load_source("__main__", mainFilePath)
else:
    if getattr(sys, "frozen", None) == "console_exe":
        from code import InteractiveConsole
        InteractiveConsole().interact()
