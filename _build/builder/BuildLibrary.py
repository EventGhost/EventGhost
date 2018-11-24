# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from glob import glob
from os.path import basename, exists, join

# Local imports
import Builder
from Utils import EncodePath

DLL_EXCLUDES = [
    "DINPUT8.dll",
    "w9xpopen.exe",
]

RT_MANIFEST = 24

class BuildLibrary(Builder.Task):
    description = "Build lib%d%d" % sys.version_info[0:2]

    def Setup(self):
        self.zipName = "python%s.zip" % self.buildSetup.pyVersionStr
        if self.buildSetup.showGui:
            if exists(join(self.buildSetup.libraryDir, self.zipName)):
                self.activated = False
        else:
            self.activated = bool(self.buildSetup.args.build)

    def DoTask(self):
        """
        Build the library and .exe files with py2exe.
        """
        buildSetup = self.buildSetup
        sys.path.append(EncodePath(buildSetup.pyVersionDir))
        from distutils.core import setup
        InstallPy2exePatch()

        import py2exe
        origIsSystemDLL = py2exe.build_exe.isSystemDLL

        def isSystemDLL(path):
            if basename(path).lower().startswith("api-ms-win-"):
                return 1
            else:
                return origIsSystemDLL(path)
        py2exe.build_exe.isSystemDLL = isSystemDLL

        libraryDir = buildSetup.libraryDir
        if exists(libraryDir):
            for filename in os.listdir(libraryDir):
                path = join(libraryDir, filename)
                if not os.path.isdir(path):
                    os.remove(path)

        wip_version = None
        if buildSetup.appVersion.startswith("WIP-"):
            # this is to avoid a py2exe warning when building a WIP version
            wip_version = buildSetup.appVersion
            buildSetup.appVersion = ".".join(
                buildSetup.appVersion.split("-")[1].split(".")
            )
        #
        # import Includes
        #
        # for item in Includes.build.STD_LIB_MODULES + Includes.build.INCLUDES:
        #     print 'module found - ', item

        import EventGhostBuild
        import EventGhostBuildExtension
        import Includes

        setup(
            script_args=["py2exe"],
            windows=[Target(buildSetup)],
            verbose=buildSetup.args.verbose,
            zipfile=EncodePath(join(buildSetup.libraryName, self.zipName)),
            options=dict(
                build=dict(
                    build_base=join(buildSetup.tmpDir, "build")
                ),
                build_ext=dict(
                    build_base=buildSetup.tmpDir,
                    threaded_build=True,
                    dist_dir=buildSetup.sourceDir,
                ),
                py2exe=dict(
                    compressed=0,
                    packages=['wx'],
                    includes=[
                        'cFunctions',
                        '_dxJoystick',
                        'VistaVolEvents'
                    ] + Includes.build.INCLUDES,
                    excludes=Includes.EXCLUDES,
                    dll_excludes=DLL_EXCLUDES,
                    dist_dir=EncodePath(buildSetup.sourceDir),
                    custom_boot_script=join(
                        buildSetup.dataDir, "Py2ExeBootScript.py"
                    ),
                )
            ),
            cmdclass=dict(
                py2exe=EventGhostBuild.Build,
                build_ext=EventGhostBuildExtension.BuildEXT,
            ),
            ext_modules=[
                EventGhostBuildExtension.RawInputHook,
                EventGhostBuildExtension.MceIr,
                EventGhostBuildExtension.TaskHook,
                EventGhostBuildExtension.cFunctions,
                EventGhostBuildExtension.dxJoystick,
                EventGhostBuildExtension.VistaVolEvents,
                EventGhostBuildExtension.WinUsbWrapper
            ]

        )

        if wip_version:
            buildSetup.appVersion = wip_version

        dllNames = [basename(name) for name in glob(join(libraryDir, "*.dll"))]
        neededDlls = []

        paths = [sys.prefix]
        if hasattr(sys, "real_prefix"):
            paths.append(sys.real_prefix)

        for path in paths:
            for _, _, files in os.walk(path):
                for filename in files:
                    if filename in dllNames:
                        neededDlls.append(filename)
        for dllName in dllNames:
            if dllName not in neededDlls:
                os.remove(join(libraryDir, dllName))

        #RemoveAllManifests(libraryDir)


class Target:
    def __init__(self, buildSetup):
        self.icon_resources = []
        iconPath = join(buildSetup.docsDir, "_static", "arrow.ico")
        if exists(iconPath):
            self.icon_resources.append((0, iconPath))
        iconPath = join(buildSetup.docsDir, "_static", "ghost.ico")
        if exists(iconPath):
            self.icon_resources.append((6, iconPath))

        manifest = file(
            join(buildSetup.pyVersionDir, "Manifest.xml")
        ).read()

        manifest = manifest.format(app_name=buildSetup.name)

        self.other_resources = [(RT_MANIFEST, 1, manifest)]
        self.name = buildSetup.name
        self.description = buildSetup.description
        self.company_name = buildSetup.companyName
        self.copyright = buildSetup.copyright
        self.dest_base = buildSetup.name
        self.version = buildSetup.appVersion
        self.script = join(buildSetup.sourceDir, buildSetup.mainScript)


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
    except ImportError:  # IGNORE:W0704
        # no build path setup, no worries.
        pass

def RemoveAllManifests(scanDir):
    """
    Remove embedded manifest resource for all DLLs and PYDs in the supplied
    directory.

    This seems to be the only way how the setup can run with Python 2.6
    on Vista and above.
    """
    import ctypes
    BeginUpdateResource = ctypes.windll.kernel32.BeginUpdateResourceW
    UpdateResource = ctypes.windll.kernel32.UpdateResourceW
    EndUpdateResource = ctypes.windll.kernel32.EndUpdateResourceW

    for name in os.listdir(scanDir):
        path = os.path.join(scanDir, name)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in (".pyd", ".dll"):
            continue
        handle = BeginUpdateResource(path, 0)
        if not handle:
            raise ctypes.WinError()
        res = UpdateResource(handle, RT_MANIFEST, 2, 1033, None, 0)
        if not res:
            continue
        if not EndUpdateResource(handle, 0):
            raise ctypes.WinError()
