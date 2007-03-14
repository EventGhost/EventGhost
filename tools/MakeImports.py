import os
import sys
from os.path import join
import warnings

warnings.simplefilter('error', DeprecationWarning)

skipModules = [
    "wx.lib.vtk",
]

def TestImport(moduleName):
    try:
        __import__(moduleName)
        return (True, "", "")
    except DeprecationWarning, e:
        return False, "DeprecationWarning", str(e)
    except ImportError, e:
        return False, "ImportError", str(e)
    except SyntaxError, e:
        return False, "SyntaxError", str(e)
        
    
def ScanPath(path, prefix, skipPath=[]):
    modules = []
    for root, dirs, files in os.walk(path):
        package = root[len(path) + 1:].replace("\\", ".")
        if prefix:
            package = prefix + package
        for dir in dirs[:]:
            if not os.path.exists(join(root, dir, "__init__.py")):
                dirs.remove(dir)
            if dir in skipPath:
                dirs.remove(dir)
        if package in skipPath:
            continue
        if package.rfind(".test") > 0:
            continue
        if package != prefix:
            ok, eType, eMesg = TestImport(package)
            if ok:
                modules.append(package)
            package += "."
        for file in files:
            name, extension = os.path.splitext(file)
            if (
                not (extension == ".py")# and name[0] != "_")
                and extension != ".pyd"
            ):
                continue
            moduleName = package + name
            ok, eType, eMesg = TestImport(moduleName)
            if ok:
                modules.append(moduleName)
    return modules

def ReadGlobalModuleIndex():
    modules = []
    inFile = open("Global Module Index.txt", "rt")
    for line in inFile.readlines():
        parts = line.strip().split(" ", 1)
        if len(parts) > 1:
            if parts[1].find("Windows") < 0:
                continue
        modules.append(parts[0])
    inFile.close()
    return modules
    
import SimpleHTTPServer
ignoreModules = [
    "idlelib", 
    "test",
    "test.test_support",
    "Tix",
    "Tkinter",
    "distutils.command.bdist_packager",
    "distutils.mwerkscompiler",
]

result = ScanPath(os.path.dirname(SimpleHTTPServer.__file__), "", ignoreModules)
for module in sys.builtin_module_names:
    result.append(module)
print
for module in ReadGlobalModuleIndex():
    if module in ignoreModules:
        continue
    if module not in result:
        print module
        result.append(module)

fd = open("imports.py", "wt")
fd.write("""\
#-----------------------------------------------------------------------------
# This file is automatically created by the MakeImports.py script.
# Don't try to edit this file yourself.
#-----------------------------------------------------------------------------

""")
#result.sort()
for module in result:
    fd.write("import %s\n" % module)


import wx
fd.write("\nimport wx\n")
for module in ScanPath(os.path.dirname(wx.__file__), "wx.", ["wx.lib.vtk"]):
    fd.write("import %s\n" % module)
fd.write("\n")

import Image
for module in ScanPath(os.path.dirname(Image.__file__), ""):
    fd.write("import %s\n" % module)
fd.write("""

import win32com
import win32com.server
import win32com.server.factory
import win32com.server.util
import win32com.server.register
import win32com.client
import win32com.shell
import win32com.shell.shellcon
from win32com.shell.shellcon import *
from win32com.shell import shell
from win32com.shell import shellcon
""")

win32 = """\
_winxptheme 
win32com.adsi 
win32com.axcontrol 
win32com.axdebug 
win32com.axscript 
dde 
win32com.directsound 
#exchange 
#exchdapi 
win32com.internet 
isapi 
isapi.install 
isapi.isapicon 
isapi.simple 
isapi.threaded_extension 
win32com.mapi 
odbc 
perfmon 
pythoncom 
pywintypes 
servicemanager 
win32com.shell 
sspi 
win2kras 
win32api 
win32clipboard 
win32com.authorization.authorization 
win32console 
win32crypt 
win32event 
win32evtlog 
win32file 
win32gui 
win32help 
win32inet 
win32job 
win32lz 
win32net 
win32pdh 
win32pipe 
win32print 
win32process 
win32ras 
win32security 
win32service 
win32ts 
win32ui 
win32uiole 
win32wnet 
#wincerapi 
winxpgui 
"""
for line in win32.splitlines():
    line = line.strip()
    if line and line[0] != "#":
        fd.write("import %s\n" % line)
    

fd.close()
