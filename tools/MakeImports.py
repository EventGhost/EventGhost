# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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

"""
Creates a file that would import all used modules.

This way we trick py2exe to include all standard library files and some more 
packages and modules.
"""


import os
import sys
from os.path import join
import warnings


MODULES_TO_IGNORE = [
    "idlelib", 
    "gopherlib",
    "Tix",
    "test",
    "Tkinter",
    "_tkinter",
    "turtle", # another Tkinter module
    
    "distutils.command.bdist_packager",
    "distutils.mwerkscompiler",
    "curses",
    #"ctypes.macholib", # seems to be for Apple
    
    "wx.lib.vtk",
    "wx.tools.Editra",
    "wx.tools.XRCed",
    "wx.lib.plot", # needs NumPy
    "wx.lib.floatcanvas", # needs NumPy
    
    "ImageTk",
    "ImageGL",
    "ImageQt",
    "WalImageFile", # odd syntax error in file
    
    "win32com.gen_py",
    "win32com.demos",
    "win32com.axdebug",
    "win32com.axscript",
    "pywin",
    "comtypes.gen",
]

HEADER = """\
#-----------------------------------------------------------------------------
# This file is automatically created by the MakeImports.py script.
# Don't try to edit this file yourself.
#-----------------------------------------------------------------------------

"""

warnings.simplefilter('error', DeprecationWarning)

PYTHON_DIR = os.path.dirname(sys.executable)
SITE_PACKAGES_PATH = join(PYTHON_DIR, "Lib", "site-packages")


class DummyStdOut: #IGNORE:W0232 class has no __init__ method
    """ 
    Just a dummy stdout implementation, that suppresses all output. 
    """
    
    def write(self, dummyData): #IGNORE:C0103
        """ A do-nothing write. """
        pass


    
def TestImport(moduleName, includeDeprecated=False):
    """
    Test if the given module can be imported without error.
    """
    #print "Testing", moduleName
    oldStdOut = sys.stdout
    oldStdErr = sys.stderr
    sys.stdout = DummyStdOut()
    try:
        __import__(moduleName)
        return (True, "", "")
    except DeprecationWarning, exc:
        return includeDeprecated, "DeprecationWarning", str(exc)
    except ImportError, exc:
        return False, "ImportError", str(exc)
    except SyntaxError, exc:
        return False, "SyntaxError", str(exc)
    except Exception, exc:
        return False, "Exception", str(exc)
    finally:
        sys.stdout = oldStdOut
        sys.stderr = oldStdErr
    
    
def ShouldBeIgnored(moduleName):
    """
    Return True if the supplied module should be ignored, because it is a
    module or submodule in MODULES_TO_IGNORE.
    """ 
    moduleParts = moduleName.split(".")
    modulePartsLength = len(moduleParts)
    for module in MODULES_TO_IGNORE:
        ignoreParts = module.split(".")
        ignorePartsLength = len(ignoreParts)
        if ignorePartsLength > modulePartsLength:
            continue
        if moduleParts[:ignorePartsLength] == ignoreParts:
            return True
    return False
    
    
def FindModulesInPath(path, prefix=""):
    """
    Find modules and packages for a given filesystem path.
    """
    if prefix:
        prefix += "."
    print "Scanning:", path
    modules = []
    for root, dirs, files in os.walk(path):
        package = root[len(path) + 1:].replace("\\", ".")
        package = prefix + package
        for directory in dirs[:]:
            if (
                not os.path.exists(join(root, directory, "__init__.py"))
                or ShouldBeIgnored(package + "." + directory)
            ):
                dirs.remove(directory)
        if ShouldBeIgnored(package) or package.rfind(".test") > 0:
            continue
        if package != prefix:
            isOk, eType, eMesg = TestImport(package)
            if isOk:
                modules.append(package)
            package += "."
        for filename in files:
            name, extension = os.path.splitext(filename)
            if extension.lower() not in (".py", ".pyd"):
                continue
            moduleName = package + name
            if ShouldBeIgnored(moduleName) or moduleName.endswith(".__init__"):
                continue
            isOk, eType, eMesg = TestImport(moduleName)
            if not isOk:
                if not eType == "DeprecationWarning":
                    print "   ", moduleName, eType, eMesg
                continue
            modules.append(moduleName)
    return modules


def ReadGlobalModuleIndex():
    """
    Read the global module index file (created by copy&paste from the Python
    documentation) and sort out all modules that are not available on Windows.
    """
    modules = []
    badModules = []
    inFile = open("Global Module Index.txt", "rt")
    for line in inFile.readlines():
        parts = line.strip().split(" ", 1)
        if len(parts) > 1:
            if parts[1].startswith("(") and parts[1].find("Windows") < 0:
                badModules.append(parts[0])
                continue
#            if parts[1].find("Deprecated:") >= 0:
#                print line
        modules.append(parts[0])
    inFile.close()
    return modules, badModules
    
    
def ReadPth(path):
    """
    Read a .PTH file and return the pathes inside as a list
    """
    result = []
    pthFile = open(path, "rt")
    for line in pthFile:
        if line.strip().startswith("#"):
            continue
        result.append(join(os.path.dirname(path), line.strip()))
    return result


def GetPydFiles(path):
    """ 
    Returns a list of all .pyd modules in supplied path. 
    """
    files = []
    for filepath in os.listdir(path):
        moduleName, extension = os.path.splitext(os.path.basename(filepath))
        if extension.lower() == ".pyd":
            files.append(moduleName)
    return files


def GetPackageModules(package):
    """
    Returns a list with all modules of the package.
    """
    pthPath = join(SITE_PACKAGES_PATH, package) + ".pth"
    moduleList = []
    if os.path.exists(pthPath):
        for path in ReadPth(pthPath):
            moduleList.extend(FindModulesInPath(path))
    else:
        mod = __import__(package)
        moduleList.append(package)
        if hasattr(mod, "__path__"):
            pathes = mod.__path__
        else:
            if mod.__file__.endswith(".pyd"):
                return moduleList
            pathes = [os.path.dirname(mod.__file__)]
        for path in pathes:
            moduleList.extend(FindModulesInPath(path, package))
    return moduleList
    
    
def Main(packagesToAdd):    
    """
    Starts the actual work.
    """
    globalModuleIndex, badModules = ReadGlobalModuleIndex()
    MODULES_TO_IGNORE.extend(badModules)
    
    stdLibModules = (
        FindModulesInPath(join(PYTHON_DIR, "DLLs"))
        + FindModulesInPath(join(PYTHON_DIR, "lib"))
    )

    print
    print "Modules found in global module index but not in scan:"
    for module in globalModuleIndex:
        if module in stdLibModules:
            continue
        if module in sys.builtin_module_names:
            continue
        if ShouldBeIgnored(module):
            continue
        print "   ", module
        #result.append(module)
    
    #print "Modules found in scan but not in global module index:"
    #for module in stdLibModules:
    #    if module not in globalModuleIndex:
    #        print "   ", module
    
    outfile = open("imports.py", "wt")
    outfile.write(HEADER)
    for module in stdLibModules:
        outfile.write("import %s\n" % module)
    # add every .pyd of the current directory
    #packagesToAdd = packagesToAdd + GetPydFiles(os.getcwdu())
    for package in packagesToAdd:
        outfile.write("\n# modules found for package '%s'\n" % package)
        for module in GetPackageModules(package):
            outfile.write("import %s\n" % module)
    outfile.close()
    
