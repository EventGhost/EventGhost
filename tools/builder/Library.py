import os
import sys
from glob import glob
from os.path import exists, join, basename, dirname

import builder

RT_MANIFEST = 24

def RemoveAllManifests(scanDir):
    """ 
    Remove embedded manifest resource for all DLLs and PYDs in the supplied
    path. 
    
    These seems to be the only way how the setup can run with Python 2.6
    on Vista.
    """
    import ctypes
    
    BeginUpdateResource = ctypes.windll.kernel32.BeginUpdateResourceA
    UpdateResource = ctypes.windll.kernel32.UpdateResourceA
    EndUpdateResource = ctypes.windll.kernel32.EndUpdateResourceA
    
    for (dirpath, dirnames, filenames) in os.walk(scanDir):
        if '.svn' in dirnames:
            dirnames.remove('.svn')
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in (".pyd", ".dll"):
                continue
            path = os.path.join(dirpath, name)
            handle = BeginUpdateResource(path, 0)
            if handle == 0:
                continue
            res = UpdateResource(handle, 24, 2, 1033, None, 0)
            if res:
                EndUpdateResource(handle, 0)



def InstallPy2exePatch():
    """
    Tricks py2exe to include the win32com module.
    
    ModuleFinder can't handle runtime changes to __path__, but win32com 
    uses them, particularly for people who build from sources.
    """
    try:
        import modulefinder
        import win32com
        for path in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", path)
        for extra in ["win32com.shell"]:
            __import__(extra)
            module = sys.modules[extra]
            for path in module.__path__[1:]:
                modulefinder.AddPackagePath(extra, path)
    except ImportError: #IGNORE:W0704
        # no build path setup, no worries.
        pass 



def CreateLibrary():
    """
    Create the library and .exe files with py2exe.
    """
    sys.path.append(builder.PYVERSION_DIR)
    from distutils.core import setup
    InstallPy2exePatch()
    import py2exe # pylint: disable-msg=W0612
                  # looks like py2exe import is unneeded, but it isn't
    libraryDir = builder.LIBRARY_DIR
    if exists(libraryDir):
        for filename in os.listdir(libraryDir):
            path = join(libraryDir, filename)
            if not os.path.isdir(path):
                os.remove(path)
                
    manifest = file(
        join(builder.PYVERSION_DIR, "manifest.template")
    ).read() % builder.__dict__
    py2exeOptions = dict(
        options = dict(
            build = dict(build_base = join(builder.TMP_DIR, "build")),
            py2exe = dict(
                compressed = 0,
                includes = [
                    "encodings",
                    "encodings.*",
                    "imports",
                ],
                excludes = builder.EXCLUDED_MODULES,
                dll_excludes = [
                    "DINPUT8.dll", 
                    "w9xpopen.exe", 
                    #"gdiplus.dll", 
                    #"msvcr71.dll",
                ],
                dist_dir = builder.SOURCE_DIR,
                custom_boot_script = join(builder.DATA_DIR, "Py2ExeBootScript.py"),
            )
        ),
        # The lib directory contains everything except the executables and
        # the python dll.
        zipfile = join(builder.LIBRARY_NAME, "python%s.zip" % builder.PYVERSION_STR),
        windows = [
            dict(
                script = join(builder.SOURCE_DIR, builder.MAIN_SCRIPT),
                icon_resources = [],
                other_resources = [(RT_MANIFEST, 1, manifest)],
                dest_base = builder.APP_NAME
            ),
        ],
        verbose = 0,
    )
    iconPath = join(builder.DATA_DIR, "Main.ico")
    if exists(iconPath):
        py2exeOptions["windows"][0]["icon_resources"].append((1, iconPath))
    #import pprint
    #pprint.pprint(py2exeOptions)
    setup(script_args=["py2exe"], **py2exeOptions)
    
    dllNames = [
        basename(name) for name in glob(join(libraryDir, "*.dll"))
    ]
    neededDlls = []
    for _, _, files in os.walk(dirname(sys.executable)):
        for filename in files:
            if filename in dllNames:
                neededDlls.append(filename)
    for filename in dllNames:
        if filename not in neededDlls:
            os.remove(join(libraryDir, filename))
#    if builder.PYVERSION_STR == "26":
#        RemoveAllManifests(libraryDir)


