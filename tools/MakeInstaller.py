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
import time
import ConfigParser
import threading
import shutil
import imp

from os.path import dirname, join, exists, abspath
from glob import glob

# third-party module imports
import pysvn
import wx

# local imports
from InnoInstaller import InnoInstaller


INNO_SCRIPT_TEMPLATE = """
[Tasks]
Name: "desktopicon"; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: checkedonce 

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: Deutsch; MessagesFile: "compiler:Languages\\German.isl"
Name: "fr"; MessagesFile: "compiler:Languages\\French.isl"

[Setup]
ShowLanguageDialog=auto
AppName=EventGhost
AppPublisher=EventGhost Project
AppPublisherURL=http://www.eventghost.org/
AppVerName=EventGhost %(appVersion)s
DefaultDirName={pf}\\EventGhost
DefaultGroupName=EventGhost
Compression=lzma/ultra
SolidCompression=yes
InternalCompressLevel=ultra
OutputDir=%(outputDir)s
OutputBaseFilename=%(outputBaseFilename)s
InfoBeforeFile=%(toolsDir)s\\LICENSE.RTF
DisableReadyPage=yes
AppMutex=EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B

[InstallDelete]
Type: filesandordirs; Name: "{app}\\eg"

[Files]
Source: "%(libraryDir)s\\*.*"; DestDir: "{app}\\%(libraryName)s"; Flags: ignoreversion recursesubdirs

[Dirs]
Name: "{app}\\%(libraryName)s\\site-packages"

[Run]
Filename: "{app}\\EventGhost.exe"; Parameters: "-install"

[UninstallRun]
Filename: "{app}\\EventGhost.exe"; Parameters: "-uninstall"

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\\EventGhost"

[Run] 
Filename: "{app}\\EventGhost.exe"; Flags: postinstall nowait skipifsilent 

[Icons]
Name: "{group}\\EventGhost"; Filename: "{app}\\EventGhost.exe"
Name: "{group}\\EventGhost Web Site"; Filename: "http://www.eventghost.org/"
Name: "{group}\\EventGhost Forums"; Filename: "http://www.eventghost.org/forum/"
Name: "{group}\\EventGhost Wiki"; Filename: "http://www.eventghost.org/wiki/"
Name: "{group}\\Uninstall EventGhost"; Filename: "{uninstallexe}"
Name: "{userdesktop}\\EventGhost"; Filename: "{app}\\EventGhost.exe"; Tasks: desktopicon
"""

INCLUDED_MODULES = [
    "wx",
    "PIL",
    "comtypes",
    "pywin32",
    "pythoncom",
    "isapi",
    "win32com",
]

EXCLUDED_MODULES = [
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
]


class MyInstaller(InnoInstaller):
    APP_SHORT_NAME = "EventGhost"
    mainScript = "../EventGhost.pyw"
    icon = "EventGhost.ico"
    excludes = EXCLUDED_MODULES
    innoScriptTemplate = INNO_SCRIPT_TEMPLATE
    
    def __init__(self):
        if self.PYVERSION == "26":
            self.SETUP_EXE_NAME_TEMPLATE = "%(APP_SHORT_NAME)s_%(appVersion)s_Py26_Setup"
        InnoInstaller.__init__(self)


    def UpdateChangeLog(self):    
        """
        Add a version header to CHANGELOG.TXT if needed.
        """
        path = join(self.sourceDir, "CHANGELOG.TXT")
        s1 = "Version %s (%s)\n" % (self.appVersion, time.strftime("%m/%d/%Y"))
        fd = open(path, "r")
        s2 = fd.read(100) # read some data from the beginning
        if s2.strip().startswith("Version "):
            # no new lines, so skip the addition of a new header
            return
        s2 += fd.read() # read the remaining contents
        fd.close()
        fd = open(path, "w+")
        fd.write(s1 + s2)
        fd.close()
        
    
    def UpdateVersionFile(self):
        """
        Update buildNum, buildTime and svnRevision in eg/Classes/Version.py
        """
        svnRevision = self.GetSvnRevision()
        versionFilePath = self.sourceDir + "/eg/Classes/Version.py"
        fd = file(versionFilePath, "rt")
        lines = fd.readlines()
        fd.close()
        fd = file(versionFilePath, "wt")
        # update buildNum and buildTime in eg/Classes/Version.py
        for line in lines:
            if line.strip().startswith("buildNum"):
                parts = line.split("=")
                value = int(parts[1].strip())
                fd.write(parts[0] + "= " + str(value+1) + "\n")
            elif line.strip().startswith("buildTime"):
                parts = line.split("=")
                fd.write(parts[0] + "= " + str(time.time()) + "\n")
            elif line.strip().startswith("svnRevision"):
                parts = line.split("=")
                fd.write("%s= %d\n" % (parts[0], svnRevision))
            else:
                fd.write(line)
        fd.close()
        data = {}
        mod = imp.load_source("Version", versionFilePath)
        self.appVersion = mod.Version.string
        
    
    def CreateImports(self):
        import MakeImports
        oldCwd = os.getcwdu()
        os.chdir(abspath(u"Python%s" % self.PYVERSION))
        MakeImports.Main()
        os.chdir(oldCwd)
        
        
    def GetSetupFiles(self):
        """
        Return all files needed by the installer.
        
        The code scans for all SVN versioned files in the working copy and adds
        them to the list, except if a "noinstall" property is set for the file
        or a parent directory of the file.
        
        Plugins with a "noinclude" file are also skipped.
        """
        
        files = []
        client = pysvn.Client()
        workingDir = self.sourceDir
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
        self.outputBaseFilename = self.SETUP_EXE_NAME_TEMPLATE % self
        for file in self.GetSetupFiles():
            self.AddFile(join(self.sourceDir, file), dirname(file))
        for file in glob(join(self.libraryDir, '*.*')):
            self.AddFile(file, self.libraryName)
        self.AddFile(join(self.pyVersionDir, "py.exe"))
        self.AddFile(join(self.pyVersionDir, "pyw.exe"))
    
        # create entries in the [InstallDelete] section of the Inno script to
        # remove all known plugin directories before installing the new plugins.
        for item in os.listdir(join(self.sourceDir, "plugins")):
            if item.startswith("."):
                continue
            if os.path.isdir(join(self.sourceDir, "plugins", item)):
                self.Add(
                    "InstallDelete", 
                    'Type: filesandordirs; Name: "{app}\\plugins\\%s"' % item
                )
        self.ExecuteInnoSetup()
    
    

def Main(mainDialog=None):
    """
    Main task of the script.
    """
    print "--- updating Version.py"
    NS.UpdateVersionFile()
    print "--- updating CHANGELOG.TXT"
    NS.UpdateChangeLog()
    if Options.createImports:
        print "--- creating imports.py"
        NS.CreateImports()
    if Options.commitSvn:
        print "--- committing working copy to SVN"
        NS.CommitSvn()
    if Options.createSourceArchive:
        print "--- creating source code archive"
        NS.CreateSourceArchive()
    if Options.createLib:
        print "--- creating library files"
        NS.CreateLibrary()            
    if Options.createInstaller:
        print "--- creating setup.exe"
        NS.CreateInstaller()
        filename = join(NS.outputDir, NS.outputBaseFilename + ".exe")
        if Options.upload and Options.ftpUrl:
            print "--- uploading setup.exe"
            import UploadFile
            wx.CallAfter(
                UploadFile.UploadDialog, 
                mainDialog, 
                filename, 
                Options.ftpUrl
            )        
    print "--- All done!"



class Config(object):

    class Option(object):
        """
        Represents a single option of the Config class
        """
        def __init__(self, name, label, value):
            self.name = name
            self.label = label
            self.value = value
            
    
    def __init__(self, configFilePath):
        self._configFilePath = configFilePath
        self._options = []
        self._optionsDict = {}
        
        
    def AddOption(self, name, label, value):
        option = self.Option(name, label, value)
        self._options.append(option)
        self._optionsDict[name] = option
    
    
    def __getattr__(self, name):
        return self._optionsDict[name].value
    
    
    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            self._optionsDict[name].value = value
    
    
    def __iter__(self):
        return self._options.__iter__()
    
    
    def LoadSettings(self):
        """
        Load the ini file and set all options.
        """ 
        configParser = ConfigParser.ConfigParser()
        configParser.read(self._configFilePath)
        for option in self._options:
            if configParser.has_option("Settings", option.name):
                value = configParser.get("Settings", option.name)
                if value == "True":
                    value = True
                elif value == "False":
                    value = False
                option.value = value
            
            
    def SaveSettings(self):
        """
        Save all options to the ini file.
        """
        config = ConfigParser.ConfigParser()
        # make ConfigParser case-sensitive
        config.optionxform = str
        config.read(self._configFilePath)
        if not config.has_section("Settings"):
            config.add_section("Settings")
        for option in self._options:
            config.set("Settings", option.name, option.value)
        fd = open(self._configFilePath, "w")
        config.write(fd)
        fd.close()
        


class MainDialog(wx.Dialog):
    class Ctrls:
        pass
    
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Make EventGhost Installer")
        
        # create controls
        ctrls = []
        for option in list(Options)[:-1]:
            ctrl = wx.CheckBox(self, -1, option.label)
            ctrl.SetValue(bool(option.value))
            ctrls.append(ctrl)
            setattr(self.Ctrls, option.name, ctrl)
        self.Ctrls.upload.Enable(Options.ftpUrl != "")
        self.Ctrls.commitSvn.Enable(pysvn is not None)
        
        #self.out = wx.TextCtrl(
        #    self, 
        #    style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL 
        #)
        #self.out.SetMinSize((400, 100))
        #sys.stderr = self.out
        #sys.stdout = self.out
        #self.out.SetBackgroundColour(self.GetBackgroundColour())

        self.okButton = wx.Button(self, wx.ID_OK)
        self.okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        # add controls to sizers
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(self.okButton)
        btnSizer.AddButton(self.cancelButton)
        btnSizer.Realize()
        
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        for ctrl in ctrls:
            sizer1.Add(ctrl, 0, wx.ALL, 10)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(sizer1)
        #sizer2.Add(self.out, 1, wx.EXPAND|wx.ALL, 10)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer2, 1, wx.ALL|wx.EXPAND, 0)
        sizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        self.SetSizerAndFit(sizer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
    def OnOk(self, event):
        self.okButton.Enable(False)
        self.cancelButton.Enable(False)
        #self.SetWindowStyleFlag(wx.CAPTION|wx.RESIZE_BORDER)
        for option in list(Options)[:-1]:
            ctrl = getattr(self.Ctrls, option.name)
            setattr(Options, option.name, ctrl.GetValue())
            ctrl.Enable(False)
        Options.SaveSettings()
        thread = threading.Thread(target=Main, args=(self, ))
        thread.start()
        
        
    def OnCancel(self, event):
        event.Skip()
        self.Destroy()
        #app.ExitMainLoop()
        
        
    def OnClose(self, event):
        app.ExitMainLoop()
        event.Skip()
     
     
NS = MyInstaller()
Options = Config(join(NS.toolsDir, "MakeInstaller.ini"))
Options.AddOption("includeNoIncludePlugins", "Include 'noinclude' plugins", False)
Options.AddOption("createSourceArchive", "Create Source Archive", False)
Options.AddOption("createImports", "Create Imports", False)
Options.AddOption("createLib", "Create Lib", False)
Options.AddOption("createInstaller", "Create Installer", True)
Options.AddOption("commitSvn", "SVN Commit", False)
Options.AddOption("upload", "Upload through FTP", False)
Options.AddOption("ftpUrl", "", "")
Options.LoadSettings()

app = wx.App(0)
app.SetExitOnFrameDelete(True)
mainDialog = MainDialog()
mainDialog.Show()
app.MainLoop()

