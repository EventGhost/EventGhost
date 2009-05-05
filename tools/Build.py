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
This script creates the EventGhost setup installer.
"""
import sys
import os
from os.path import dirname, join, exists
from glob import glob

# local imports
import builder
from builder.CheckDependencies import CheckDependencies
if not CheckDependencies():
    sys.exit(1)
from builder.InnoSetup import InnoInstaller


# third-party module imports
import pysvn


INCLUDED_MODULES = [
    "wx",
    "PIL",
    "comtypes",
    "pywin32",
    "pythoncom",
    "isapi",
    "win32com",
    "docutils",
    "Crypto",
]

EXCLUDED_MODULES = [
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

builder.INCLUDED_MODULES = INCLUDED_MODULES
builder.EXCLUDED_MODULES = EXCLUDED_MODULES
builder.APP_NAME = "EventGhost"
builder.MAIN_SCRIPT = "EventGhost.pyw"


class MyInstaller(object):
    appShortName = "EventGhost_Py%d%d" % sys.version_info[:2]
    
    @staticmethod
    def GetSetupFiles():
        """
        Return all files needed by the installer.
        
        The code scans for all SVN versioned files in the working copy and adds
        them to the list, except if a "noinstall" property is set for the file
        or a parent directory of the file.
        
        Plugins with a "noinclude" file are also skipped.
        """
        
        files = []
        client = pysvn.Client()
        workingDir = builder.SOURCE_DIR
        props = client.propget("noinstall", workingDir, recurse=True)
        # propget returns the pathes with forward slash as deliminator, but we 
        # need backslashes
        props = dict((k.replace("/", "\\"), v) for k, v in props.iteritems())
        numPathParts = len(workingDir.split("\\"))
        for status in client.status(workingDir, ignore=True):
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
        inno = InnoInstaller()
        plugins = {}
        for filename in self.GetSetupFiles():
            if filename.startswith("plugins\\"):
                pluginFolder = filename.split("\\")[1]
                plugins[pluginFolder] = True
            if (
                filename.startswith("lib") 
                and not filename.startswith("lib%s\\" % builder.PYVERSION_STR)
            ):
                continue
            inno.AddFile(join(builder.SOURCE_DIR, filename), dirname(filename))
        for filename in glob(join(builder.LIBRARY_DIR, '*.*')):
            inno.AddFile(filename, builder.LIBRARY_NAME)
        inno.AddFile(
            join(builder.SOURCE_DIR, self.appShortName + ".exe"), 
            destName="EventGhost.exe"
        )
        inno.AddFile(
            join(builder.SOURCE_DIR, "py%s.exe" % builder.PYVERSION_STR), 
            destName="py.exe"
        )
        inno.AddFile(
            join(builder.SOURCE_DIR, "pyw%s.exe" % builder.PYVERSION_STR), 
            destName="pyw.exe"
        )
        inno.AddFile(
            join(builder.TMP_DIR, "VersionRevision.py"), 
            destDir="eg/Classes"
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
            'Type: files; Name: "{app}\\lib%s\\*.*"' % builder.PYVERSION_STR
        )
        inno.ExecuteInnoSetup()
    
    
builder.installer = MyInstaller()
import builder.Gui
builder.Gui.Main()

