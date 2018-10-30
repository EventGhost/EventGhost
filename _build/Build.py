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

"""
This script creates the EventGhost setup installer.
"""

from os.path import dirname, exists, join

# Local imports
import builder
from builder.Utils import CaseInsensitiveList, ListDir

SKIP_IF_UNCHANGED = CaseInsensitiveList(
    r"plugins\Task\TaskHook.dll",
)

class MyBuilder(builder.Builder):
    name = "EventGhost"
    description = "EventGhost Automation Tool"
    companyName = "EventGhost Project"
    copyright = u"Copyright © 2005-2016 EventGhost Project"
    mainScript = "EventGhost.pyw"

    includeModules = [
        "CommonMark",
        "comtypes",
        "Crypto",
        "docutils",
        "isapi",
        "jinja2",
        "PIL",
        "pkg_resources",
        "pythoncom",
        "pywin32",
        "six",
        "win32com",
        "wx",
    ]

    excludeModules = [
        "eg",
        "_imagingtk",
        "_tkinter",
        "cffi",  # bundled for no reason
        "comtypes.gen",
        #"ctypes.macholib",  # seems to be for Apple
        "curses",
        "distutils.command.bdist_packager",
        "distutils.mwerkscompiler",
        "FixTk",
        "FixTk",
        "gopherlib",
        "idlelib",
        "ImageGL",
        "ImageQt",
        "ImageTk",  # py2exe seems to hang if not removed
        "ipaddr",  # bundled for no reason
        "ipaddress",  # bundled for no reason
        "lib2to3",
        "PIL._imagingtk",
        "PIL.ImageTk",
        "pyasn1",  # bundles a broken version if not removed
        "pycparser",  # bundled for no reason
        "pywin",
        "simplejson",  # bundled for no reason
        "tcl",
        "test",
        "Tix",
        "Tkconstants",
        "tkinter",  # from `future`
        "Tkinter",
        "turtle",  # another Tkinter module
        "WalImageFile",  # odd syntax error in file
        "win32com.axdebug",
        "win32com.axscript",
        "win32com.demos",
        "win32com.gen_py",
        "wx.lib.floatcanvas",  # needs NumPy
        "wx.lib.plot",  # needs NumPy
        "wx.lib.vtk",
        "wx.tools.Editra",
        "wx.tools.XRCed",
        "wx.lib.pdfwin_old",
        "wx.lib.pdfviewer",
        "wx.lib.pubsub"
        "wx.lib.iewin",
        "wx.lib.iewin_old"
    ]

    def BuildInstaller(self):
        """
        Create and compile the Inno Setup installer script.
        """
        from builder.InnoSetup import InnoInstaller
        inno = InnoInstaller(self)

        for filename, prefix in self.GetSetupFiles():
            inno.AddFile(
                join(self.sourceDir, filename),
                dirname(filename),
                ignoreversion=(filename not in SKIP_IF_UNCHANGED),
                prefix=prefix
            )
        if exists(join(self.outputDir, "CHANGELOG.md")):
            inno.AddFile(join(self.outputDir, "CHANGELOG.md"))
        else:
            inno.AddFile(join(self.sourceDir, "CHANGELOG.md"))
        inno.AddFile(
            join(self.sourceDir, "py%s.exe" % self.pyVersionStr),
            destName="py.exe"
        )
        inno.AddFile(
            join(self.sourceDir, "pyw%s.exe" % self.pyVersionStr),
            destName="pyw.exe"
        )
        inno.AddFile(
            join(self.tmpDir, "VersionInfo.py"),
            destDir="eg\\Classes"
        )

        inno.ExecuteInnoSetup()

    def GetSetupFiles(self):
        """
        Return all files needed by the installer.

        The code scans for all files in the working copy and adds
        them to the list, except if a "noinstall" property is set for the file
        or a parent directory of the file.

        Plugins with a "noinclude" file are also skipped.
        """
        files = set(ListDir(self.sourceDir, [], fullpath=False))
        with open(join(self.pyVersionDir, "Root Includes.txt"), "r") as f:
            rootIncludes = CaseInsensitiveList(*f.read().strip().split("\n"))

        noincludes = [".", "_"]
        coreplugins = []
        for f in files.copy():
            if f.endswith("noinclude"):
                noincludes.append(f.replace("noinclude", ""))
            elif f.endswith("core-plugin"):
                coreplugins.append(f.replace("core-plugin", ""))
                files.remove(f)

        installFiles = []
        for f in files:
            if not f.startswith(tuple(noincludes)):
                if f.count("\\") == 0 and f not in rootIncludes:
                    pass
                else:
                    #if f.startswith(tuple(coreplugins)):
                    installFiles.append([f, "{app}"])
                    #else:
                    #    # Install to ProgramData\EventGhost\plugins
                    #    installFiles.append([f,
                    #        "{commonappdata}\\%s" % self.appName])

        return installFiles


MyBuilder().Start()
