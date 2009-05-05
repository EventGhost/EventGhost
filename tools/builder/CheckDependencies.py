import sys
import warnings
from string import digits
from os.path import join

from builder.InnoSetup import GetInnoCompilerPath



class MissingDependency(Exception):
    pass
class WrongVersion(Exception): 
    pass


class DependencyBase(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def Check(self):
        raise NotImplementedError
    

class ModuleDependency(DependencyBase):
    module = None
    version = None
    
    def Check(self):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                module = __import__(self.module)
        except ImportError:
            raise MissingDependency
        if hasattr(module, "__version__"):
            version = module.__version__
        elif hasattr(module, "VERSION"):
            version = module.VERSION
        elif hasattr(module, "version"):
            version = module.version
        else:
            raise Exception("Can't get version information")  
        if type(version) != type(""):
            version = ".".join(str(x) for x in version)
        if CompareVersion(version, self.version) < 0:
            raise WrongVersion
    
    

class PyWin32Dependency(DependencyBase):
    name = "pywin32 (Mark Hammond's Win32All package)"
    version = "212"
    url = "pywin32 (Mark Hammond's Win32All package)"
    
    def Check(self):
        versionFilePath = join(
            sys.prefix, "lib/site-packages/pywin32.version.txt"
        )
        version = open(versionFilePath, "rt").readline().strip()
        if CompareVersion(version, self.version) < 0:
            raise WrongVersion



class StacklessDependency(DependencyBase):
    name = "Stackless Python"
    version = "2.6.1"
    url = "http://www.stackless.com/"
    
    def Check(self):
        try:
            import stackless
        except:
            raise MissingDependency
        if CompareVersion("%d.%d.%d" % sys.version_info[:3], self.version) < 0:
            raise WrongVersion
        
    
class InnoSetupDependency(DependencyBase):
    name = "Inno Setup"
    url = "http://www.innosetup.com/isinfo.php"
    
    def Check(self):
        if not GetInnoCompilerPath():
            raise MissingDependency
        
    
DEPENDENCIES = [
    ModuleDependency(
        name = "wxPython",
        module = "wx",
        version = "2.8.9.1",
        url = "http://www.wxpython.org/",
    ),
    ModuleDependency(
        name = "pysvn",
        module = "pysvn",
        version = "1.6.2.1067",
        url = "http://pysvn.tigris.org/",
    ),
    ModuleDependency(
        name = "py2exe",
        module = "py2exe",
        version = "0.6.9",
        url = "http://www.py2exe.org/",
    ),
    ModuleDependency(
        name = "PIL (Python Image Library)", 
        module = "Image",
        version = "1.1.6",
        url = "http://www.pythonware.com/products/pil/",
    ),
    ModuleDependency(
        name = "comtypes package",
        module = "comtypes",
        version = "0.6.0", 
        url = "http://sourceforge.net/projects/comtypes/"
    ),
    ModuleDependency(
        name = "PyCrypto (Python Cryptography Toolkit)", 
        module = "Crypto",
        version = "2.0.1", 
        url = "http://www.dlitz.net/software/pycrypto/",
    ),
    ModuleDependency(
        name = "Sphinx (Python documentation generator)", 
        module = "sphinx",
        version = "0.5.1",
        url = "http://sphinx.pocoo.org/",
    ),
    PyWin32Dependency(),
    StacklessDependency(),
    InnoSetupDependency(),
]


def CompareVersion(actualVersion, wantedVersion):
    wantedParts = wantedVersion.split(".")
    actualParts = actualVersion.split(".")
    numParts = min(len(wantedParts), len(actualParts))
    for i in range(numParts):
        wantedPart = wantedParts[i]
        actualPart = actualParts[i]
        wantedPart = int(filter(lambda c: c in digits, wantedPart))
        actualPart = int(filter(lambda c: c in digits, actualPart))
        if wantedPart > actualPart:
            return -1
        elif wantedPart < actualPart:
            return 1
    return 0
    
    
def CheckDependencies():
    first = True
    for dependency in DEPENDENCIES:
        try:
            dependency.Check()
        except (WrongVersion, MissingDependency):
            if first:
                print "The following dependencies are missing:"
                first = False
            print "  *", dependency.name
            print "       Needed version:", dependency.version
            print "       Download URL:", dependency.url
    if not first:
        print "You need to install them first to run the build process!"
        
        