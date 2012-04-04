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

"""
This script creates the EventGhost setup installer.
"""
import sys


class StdErr(object):
    def __init__(self, stream, encoding):
        self.stream = stream
        self.encoding = encoding
        self.filesystemencoding = 'mbcs'

    def write(self, text):
        try:
            text = text.decode(self.filesystemencoding)
        except:
            pass
        self.stream.write(text.encode(self.encoding))
sys.stderr = StdErr(sys.stderr, sys.stderr.encoding)

import os
from os.path import dirname, join, exists
from glob import glob

# local imports
import builder


class MyBuilder(builder.Builder):
    name = "EventGhost"
    description = "EventGhost Automation Tool"
    companyName = "EventGhost Project"
    copyright = u"Copyright © 2005-2009 EventGhost Project"
    mainScript = "EventGhost.pyw"

    includeModules = [
        "wx",
        "PIL",
        "comtypes",
        "pywin32",
        "pythoncom",
        "isapi",
        "win32com",
        "docutils",
        "Crypto",
        "jinja2",
    ]
    excludeModules = [
        "lib2to3",
        "idlelib",
        "gopherlib",
        "Tix",
        "test",
        "Tkinter",
        "_tkinter",
        "Tkconstants",
        "FixTk",
        "tcl",
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

        "ImageTk", # py2exe seems to hang if not removed
        "ImageGL",
        "ImageQt",
        "WalImageFile", # odd syntax error in file
        # and no TCL through PIL
        "_imagingtk",
        "PIL._imagingtk",
        "PIL.ImageTk",
        "FixTk",

        "win32com.gen_py",
        "win32com.demos",
        "win32com.axdebug",
        "win32com.axscript",
        "pywin",
        "comtypes.gen",
        "eg",
    ]


    def GetSetupFiles(self):
        """
        Return all files needed by the installer.

        The code scans for all SVN versioned files in the working copy and adds
        them to the list, except if a "noinstall" property is set for the file
        or a parent directory of the file.

        Plugins with a "noinclude" file are also skipped.
        """
        import pysvn

        files = []
        client = pysvn.Client()
        workingDir = self.sourceDir
        svnRoot = builder.getSvnRoot(workingDir)
        #props = client.propget("noinstall", workingDir, recurse=True)
        props = client.propget("noinstall", svnRoot, recurse=True)
        # propget returns the pathes with forward slash as deliminator, but we
        # need backslashes. It also seems to be encoded in UTF-8.
        props = dict(
            (k.replace("/", "\\").decode("utf8"), v)
                for k, v in props.iteritems()
        )
        numPathParts = len(workingDir.split("\\"))
        #for status in client.status(workingDir, ignore=True):
        status = client.status(svnRoot, ignore=True)
        workingDirStatus = [i for i in status if workingDir in i.path]
        for status in workingDirStatus:
            # we only want versioned files
            if not status.is_versioned:
                continue
            if not os.path.exists(status.path):
                continue
            pathParts = status.path.split("\\")
            # don't include plugins that have a 'noinclude' file
            if len(pathParts) > numPathParts + 1:
                if pathParts[numPathParts].lower() == "plugins":
                    pluginDir = "\\".join(pathParts[:numPathParts + 2])
                    if exists(join(pluginDir, "noinclude")):
                        continue

            # make sure no parent directory has a noinstall property
            for i in range(numPathParts, len(pathParts)+1):
                path2 = "\\".join(pathParts[:i])
                if path2 in props:
                    break
            else:
                if not os.path.isdir(status.path):
                    relativePath = status.path[len(workingDir) + 1:]
                    files.append(relativePath)
        return files


    def CreateInstaller(self):
        """
        Create and compile the Inno Setup installer script.
        """
        from builder.InnoSetup import InnoInstaller
        inno = InnoInstaller(self)
        plugins = {}
        for filename in self.GetSetupFiles():
            if filename.startswith("plugins\\"):
                pluginFolder = filename.split("\\")[1]
                plugins[pluginFolder] = True
            if (
                filename.startswith("lib")
                and not filename.startswith("lib%s\\" % self.pyVersionStr)
            ):
                continue
            if filename.lower() == r"plugins\task\hook.dll":
                inno.AddFile(
                    join(self.sourceDir, filename),
                    dirname(filename),
                    ignoreversion=False
                )
                continue
            inno.AddFile(join(self.sourceDir, filename), dirname(filename))
        for filename in glob(join(self.libraryDir, '*.*')):
            inno.AddFile(filename, self.libraryName)
        inno.AddFile(
            join(self.sourceDir, self.name + ".exe"),
            destName="EventGhost.exe"
        )
        inno.AddFile(
            join(self.sourceDir, "py%s.exe" % self.pyVersionStr),
            destName="py.exe"
        )
        inno.AddFile(
            join(self.sourceDir, "pyw%s.exe" % self.pyVersionStr),
            destName="pyw.exe"
        )
        inno.AddFile(
            join(self.tmpDir, "VersionRevision.py"),
            destDir="eg\\Classes"
        )
        # create entries in the [InstallDelete] section of the Inno script to
        # remove all known plugin directories before installing the new
        # plugins.
        for plugin in plugins.keys():
            inno.Add(
                "InstallDelete",
                'Type: filesandordirs; Name: "{app}\\plugins\\%s"' % plugin
            )
        inno.Add(
            "InstallDelete",
            'Type: files; Name: "{app}\\lib%s\\*.*"' % self.pyVersionStr
        )
        inno.ExecuteInnoSetup()


MyBuilder().RunGui()

