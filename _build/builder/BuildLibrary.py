# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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
import builder
from builder.Utils import EncodePath

DLL_EXCLUDES = [
    "DINPUT8.dll",
    "w9xpopen.exe",
    # TODO: find out where the following comes from. Is it because of Win10?
    "api-ms-win-core-com-l1-1-1.dll",
    "api-ms-win-core-com-midlproxystub-l1-1-0.dll",
    "api-ms-win-core-console-l1-1-0.dll",
    "api-ms-win-core-console-l2-1-0.dll",
    "api-ms-win-core-datetime-l1-1-1.dll",
    "api-ms-win-core-debug-l1-1-1.dll",
    "api-ms-win-core-delayload-l1-1-1.dll",
    "api-ms-win-core-errorhandling-l1-1-1.dll",
    "api-ms-win-core-errorhandling-l1-1-3.dll",
    "api-ms-win-core-file-l1-2-1.dll",
    "api-ms-win-core-file-l2-1-1.dll",
    "api-ms-win-core-file-l2-1-2.dll",
    "api-ms-win-core-handle-l1-1-0.dll",
    "api-ms-win-core-heap-l1-2-0.dll",
    "api-ms-win-core-heap-l2-1-0.dll",
    "api-ms-win-core-heap-obsolete-l1-1-0.dll",
    "api-ms-win-core-io-l1-1-1.dll",
    "api-ms-win-core-kernel32-legacy-l1-1-1.dll",
    "api-ms-win-core-libraryloader-l1-2-0.dll",
    "api-ms-win-core-libraryloader-l1-2-1.dll",
    "api-ms-win-core-localization-l1-2-1.dll",
    "api-ms-win-core-localization-obsolete-l1-3-0.dll",
    "api-ms-win-core-memory-l1-1-2.dll",
    "api-ms-win-core-path-l1-1-0.dll",
    "api-ms-win-core-processenvironment-l1-2-0.dll",
    "api-ms-win-core-processthreads-l1-1-2.dll",
    "api-ms-win-core-profile-l1-1-0.dll",
    "api-ms-win-core-psapi-ansi-l1-1-0.dll",
    "api-ms-win-core-psapi-l1-1-0.dll",
    "api-ms-win-core-realtime-l1-1-0.dll",
    "api-ms-win-core-registry-l1-1-0.dll",
    "api-ms-win-core-registry-l2-2-0.dll",
    "api-ms-win-core-rtlsupport-l1-2-0.dll",
    "api-ms-win-core-shlwapi-legacy-l1-1-0.dll",
    "api-ms-win-core-shlwapi-obsolete-l1-2-0.dll",
    "api-ms-win-core-sidebyside-l1-1-0.dll",
    "api-ms-win-core-string-l1-1-0.dll",
    "api-ms-win-core-string-l2-1-0.dll",
    "api-ms-win-core-string-obsolete-l1-1-0.dll",
    "api-ms-win-core-stringansi-l1-1-0.dll",
    "api-ms-win-core-synch-l1-2-0.dll",
    "api-ms-win-core-synch-l1-2-1.dll",
    "api-ms-win-core-sysinfo-l1-2-1.dll",
    "api-ms-win-core-threadpool-l1-2-0.dll",
    "api-ms-win-core-threadpool-legacy-l1-1-0.dll",
    "api-ms-win-core-timezone-l1-1-0.dll",
    "api-ms-win-core-url-l1-1-0.dll",
    "api-ms-win-core-wow64-l1-1-0.dll",
    "api-ms-win-eventing-classicprovider-l1-1-0.dll",
    "api-ms-win-eventing-controller-l1-1-0.dll",
    "api-ms-win-eventing-legacy-l1-1-0.dll",
    "api-ms-win-eventing-provider-l1-1-0.dll",
    "api-ms-win-eventlog-legacy-l1-1-0.dll",
    "api-ms-win-power-base-l1-1-0.dll",
    "api-ms-win-power-setting-l1-1-0.dll",
    "api-ms-win-security-activedirectoryclient-l1-1-0.dll",
    "api-ms-win-security-activedirectoryclient-l1-1-1.dll",
    "api-ms-win-security-base-l1-2-0.dll",
]

RT_MANIFEST = 24

class BuildLibrary(builder.Task):
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
        # Looks like py2exe import is unneeded, but it isn't.
        import py2exe  # pylint: disable-msg=W0612 # NOQA
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
                    includes=["encodings", "encodings.*", "Imports"],
                    excludes=buildSetup.excludeModules,
                    dll_excludes = DLL_EXCLUDES,
                    dist_dir = EncodePath(buildSetup.sourceDir),
                    custom_boot_script=join(
                        buildSetup.dataDir, "Py2ExeBootScript.py"
                    ),
                )
            )
        )

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
        iconPath = join(buildSetup.dataDir, "Main.ico")
        if exists(iconPath):
            self.icon_resources.append((1, iconPath))
        manifest = file(
            join(buildSetup.pyVersionDir, "Manifest.xml")
        ).read() % buildSetup.__dict__
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
