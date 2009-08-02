# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
# 
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from glob import glob
from os.path import exists, join, basename, dirname

from builder import Task
from builder.Utils import EncodePath


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
            res = UpdateResource(handle, RT_MANIFEST, 2, 1033, None, 0)
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


class Target:
    def __init__(self, buildSetup):
        self.icon_resources = []
        iconPath = join(buildSetup.dataDir, "Main.ico")
        if exists(iconPath):
            self.icon_resources.append((1, iconPath))
        manifest = file(
            join(buildSetup.pyVersionDir, "manifest.template")
        ).read() % buildSetup.__dict__
        self.other_resources = [(RT_MANIFEST, 1, manifest)]
        self.name = buildSetup.name
        self.description = buildSetup.description
        self.company_name = buildSetup.companyName
        self.copyright = buildSetup.copyright
        self.dest_base = buildSetup.name
        self.version = buildSetup.appNumericalVersion
        self.script = join(buildSetup.sourceDir, buildSetup.mainScript)



class CreateLibrary(Task):
    description = "Build lib%d%d" % sys.version_info[0:2]
   
    def Setup(self):
        self.zipName = "python%s.zip" % self.buildSetup.pyVersionStr
        if not exists(join(self.buildSetup.libraryDir, self.zipName)):
            self.activated = True
            self.enabled = False
        

    def DoTask(self):
        """
        Create the library and .exe files with py2exe.
        """
        buildSetup = self.buildSetup
        sys.path.append(EncodePath(buildSetup.pyVersionDir))
        from distutils.core import setup
        InstallPy2exePatch()
        import py2exe # pylint: disable-msg=W0612
                      # looks like py2exe import is unneeded, but it isn't
        libraryDir = buildSetup.libraryDir
        if exists(libraryDir):
            for filename in os.listdir(libraryDir):
                path = join(libraryDir, filename)
                if not os.path.isdir(path):
                    os.remove(path)
    
        setup(
            script_args=["py2exe"], 
            windows=[Target(buildSetup)],
            verbose=0,
            zipfile=EncodePath(join(buildSetup.libraryName, self.zipName)),
            options = dict(
                build=dict(build_base=join(buildSetup.tmpDir, "build")),
                py2exe=dict(
                    compressed=0,
                    includes=["encodings", "encodings.*", "imports"],
                    excludes=buildSetup.excludeModules,
                    dll_excludes = ["DINPUT8.dll", "w9xpopen.exe"],
                    dist_dir = EncodePath(buildSetup.sourceDir),
                    custom_boot_script=EncodePath(join(
                        buildSetup.dataDir, "Py2ExeBootScript.py"
                    )),
                )
            )
        )
    
        dllNames = [basename(name) for name in glob(join(libraryDir, "*.dll"))]
        neededDlls = []
        for _, _, files in os.walk(dirname(sys.executable)):
            for filename in files:
                if filename in dllNames:
                    neededDlls.append(filename)
        for dllName in dllNames:
            if dllName not in neededDlls:
                os.remove(join(libraryDir, dllName))
        if buildSetup.pyVersionStr == "26":
            RemoveAllManifests(libraryDir)
    
