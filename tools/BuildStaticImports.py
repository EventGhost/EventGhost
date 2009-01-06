singletons = (
    "document",
    "taskBarIcon",
)

import os
from os.path import join
from glob import glob

def ScanDir(modName):
    parts = modName.split(".")
    scanDir = join(outDir, *parts)
    if len(parts) > 1:
        outfile.write("from %s import %s\n" % (modName, parts[-1]))
    files = glob(join(scanDir, "*.py"))
    for filename in files:
        name = os.path.splitext(os.path.basename(filename))[0]
        if not name.startswith("__"):
            if len(parts) > 1:
                outfile.write("from %s.%s import %s as _tmp\n" % (modName, name, name))
                outfile.write("%s.%s = _tmp\n" % (parts[-1], name))
            else:
                outfile.write("from %s.%s import %s\n" %(modName, name, name))
    
outDir = os.path.abspath(join(os.path.dirname(__file__), "..", "eg"))

outfile = open(join(outDir, "StaticImports.py"), "wt")
outfile.write('''\
"""
This file was automatically created by the tools/BuildStaticImports.py script.
Don't try to edit this file yourself.

This module is not directly used by EventGhost. It only exists to help
pylint and other tools to read the sources properly, as EventGhost is using
a lazy import pattern.
"""
''')
outfile.write("# py" + "lint: disable-msg=W0611,W0614,C0103\n")
outfile.write("from Utils import * #py" + "lint: disable-msg=W0401\n")
ScanDir("Classes")
ScanDir("Classes.MainFrame")
ScanDir("Classes.UndoHandler")
outfile.write("\n")
for name in singletons:
    clsName = name[0].upper() + name[1:]
    outfile.write("%s = %s()\n" % (name, clsName))
    
outfile.write("""
del _tmp

def RegisterPlugin(**dummyKwArgs): 
    pass
""")
outfile.close()