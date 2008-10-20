
PACKAGES_TO_ADD = [
    "wx",
    "PIL",
    "comtypes",
    "pywin32",
    "pythoncom",
    "isapi",
    "win32com",
    "greenlet",
    "cFunctions",
]

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

import os
import sys
import string
from os.path import join
import warnings

warnings.simplefilter('error', DeprecationWarning)

gPythonDir = os.path.dirname(sys.executable)
gSitePackagePath = join(gPythonDir, "Lib", "site-packages")


class DummyStdOut:
    def write(self, data):
        pass

dummyStdOut = DummyStdOut()
    
def TestImport(moduleName):
    """
    Test if the given module can be imported without error.
    """
    #print "Testing", moduleName
    oldStdOut = sys.stdout
    sys.stdout = dummyStdOut
    try:
        __import__(moduleName)
        return (True, "", "")
    except DeprecationWarning, e:
        return False, "DeprecationWarning", str(e)
    except ImportError, e:
        return False, "ImportError", str(e)
    except SyntaxError, e:
        return False, "SyntaxError", str(e)
    except Exception, e:
        return False, "Exception", str(e)
    finally:
        sys.stdout = oldStdOut
    
    
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
        if prefix:
            package = prefix + package
        for dir in dirs[:]:
            if not os.path.exists(join(root, dir, "__init__.py")):
                dirs.remove(dir)
                continue
            if ShouldBeIgnored(package + "." + dir):
                dirs.remove(dir)
        if ShouldBeIgnored(package):
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
            if ShouldBeIgnored(moduleName):
                continue
            if moduleName.endswith(".__init__"):
                continue
            #print "Testing:", moduleName,
            ok, eType, eMesg = TestImport(moduleName)
            if ok:
                modules.append(moduleName)
            else:
                if not eType == "DeprecationWarning":
                    print "   ", moduleName, eType, eMesg
    return modules


def ReadGlobalModuleIndex():
    """
    Read the global module index file (created by copy&paste from the python
    documentation) and sort out all modules that are not available on Windows.
    """
    modules = []
    badModules = []
    versionStr = "%d.%d" % sys.version_info[:2]
    inFile = open("Python %s Global Module Index.txt" % versionStr, "rt")
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


def Main():
    global MODULES_TO_IGNORE
    
    globalModuleIndex, badModules = ReadGlobalModuleIndex()
    MODULES_TO_IGNORE += badModules
    
    stdLibModules = FindModulesInPath(join(gPythonDir, "DLLs"))
    stdLibModules += FindModulesInPath(join(gPythonDir, "lib"))
    
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
    
    fd = open("imports.py", "wt")
    fd.write(HEADER)
    for module in stdLibModules:
        fd.write("import %s\n" % module)
    for moduleName in PACKAGES_TO_ADD:
        fd.write("\n# modules found for package '%s'\n" % moduleName)
        pthPath = join(gSitePackagePath, moduleName) + ".pth"
        moduleList = []
        if os.path.exists(pthPath):
            for path in ReadPth(pthPath):
                moduleList += FindModulesInPath(path)
        else:
            mod = __import__(moduleName)
            fd.write("import %s\n" % moduleName)
            if hasattr(mod, "__path__"):
                pathes = mod.__path__
            else:
                if mod.__file__.endswith(".pyd"):
                    continue
                pathes = [os.path.dirname(mod.__file__)]
            for path in pathes:
                moduleList += FindModulesInPath(path, moduleName)
        for module in moduleList:
            fd.write("import %s\n" % module)
    
    fd.close()
    
    
if __name__ == "__main__":
    Main()
