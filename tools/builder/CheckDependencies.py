import sys
from string import digits
from os.path import join
from builder.InnoSetup import GetInnoCompilerPath

DEPENDENCIES = [
    (
        "wx", 
        "2.8.9.1", 
        "wxPython", 
        "http://www.wxpython.org/"
    ),
    (
        "pysvn", 
        "1.6.2.1067", 
        "pysvn", 
        "http://pysvn.tigris.org/"
    ),
#    (
#        "py2exe", 
#        "0.6.9", 
#        "py2exe", 
#        "http://www.py2exe.org/"
#    ),
    (
        "win32api", 
        "212", 
        "pywin32 (Mark Hammond's Win32All package)", 
        "http://sourceforge.net/projects/pywin32/"
    ),
    (
        "comtypes", 
        "0.6.0", 
        "comtypes package", 
        "http://sourceforge.net/projects/comtypes/"
    ),
    (
        "Image", 
        "1.1.6", 
        "PIL (Python Image Library)", 
        "http://www.pythonware.com/products/pil/"
    ),
    (
        "Crypto", 
        "2.0.1", 
        "PyCrypto (Python Cryptography Toolkit)", 
        "http://www.dlitz.net/software/pycrypto/"
    ),
    (
        "sphinx", 
        "0.5.1", 
        "Sphinx (Python documentation generator)", 
        "http://sphinx.pocoo.org/"
    ),
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
    missing = []
    if not GetInnoCompilerPath():
        missing.append(
            (
                "Inno Setup", 
                "5.2.3", 
                "Inno Setup", 
                "http://www.innosetup.com/isinfo.php"
            )
        )
    for moduleName, wantedVersion, name, url in DEPENDENCIES:
        try:
            module = __import__(moduleName)
        except ImportError:
            missing.append((moduleName, wantedVersion, name, url))
            continue
        if moduleName == "win32api":
            # sadly pywin32 has no version variable
            # But it has a version file in the site-packages directory.
            versionFilePath = join(
                sys.prefix, "lib/site-packages/pywin32.version.txt"
            )
            version = open(versionFilePath, "rt").readline().strip()
        elif hasattr(module, "__version__"):
            version = module.__version__
        elif hasattr(module, "VERSION"):
            version = module.VERSION
        elif hasattr(module, "version"):
            version = module.version
        else:
            version = "(unknown version)"
        if type(version) != type(""):
            version = ".".join(str(x) for x in version)
        if CompareVersion(version, wantedVersion) < 0:
            missing.append((moduleName, wantedVersion, name, url))
    if missing:
        print "The following dependencies are missing:"
        for moduleName, wantedVersion, name, url in missing:
            print "  *", name
            print "       Needed version:", wantedVersion
            print "       Download URL:", url
        print "You need to install them first to run the build process!"
    return len(missing) == 0
