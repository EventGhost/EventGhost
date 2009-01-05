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
import imp
import subprocess
import warnings

from os.path import dirname, join, exists, abspath
from glob import glob

# local imports
from InnoInstaller import InnoInstaller

#disable deprecation warning in py2exe)
warnings.filterwarnings("ignore", ".*", DeprecationWarning, "py2exe.build_exe")

INI_FILE = os.path.splitext(__file__)[0] + ".ini"

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
    (
        "py2exe", 
        "0.6.9", 
        "py2exe", 
        "http://www.py2exe.org/"
    ),
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
        "sphinx", 
        "0.5.1", 
        "Sphinx (Python documentation generator)", 
        "http://sphinx.pocoo.org/"
    ),
]


def CheckComtypes():
    # comtypes 0.6.0 has a bug in client/_code_cache.py
    # path it if needed
    path = join(sys.prefix, "lib/site-packages/comtypes/client/_code_cache.py")
    lines = open(path, "rt").readlines()
    for linenum, line in enumerate(lines):
        if line.strip() == "import ctypes, logging, os, sys, tempfile":
            print "Needs to be patched:", path 
            lines[linenum] = \
                "import ctypes, logging, os, sys, tempfile, types\n"
            outfile = open(path, "wt")
            outfile.writelines(lines)
            outfile.close()
            print "Patching done!"
            break
    
    
def CompareVersion(actualVersion, wantedVersion):
    wantedParts = wantedVersion.split(".")
    actualParts = actualVersion.split(".")
    numParts = min(len(wantedParts), len(actualParts))
    for i in range(numParts):
        wantedPart = wantedParts[i]
        actualPart = actualParts[i]
        if wantedPart > actualPart:
            return -1
        elif wantedPart < actualPart:
            return 1
    return 0
    
    
    
def CheckDependencies():
    missing = []
    if not InnoInstaller.GetCompilerPath():
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


if not CheckDependencies():
    sys.exit(1)
CheckComtypes()


# third-party module imports
import pysvn
import wx


    
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

[Code]

function InitializeSetup: Boolean;
var
  MS, LS: Cardinal;
  ErrorCode: integer;
begin
  if GetVersionNumbers(ExpandConstant('{sys}\\gdiplus.dll'), MS, LS) then
    Result := true
  else
    begin
      Result := false;
      MsgBox('You need to install GDI+ first.'#13#10#13#10 + 'Please visit http://www.eventghost.org/docs/faq.html for instructions.', MBError, MB_OK);
    end
end;

[InstallDelete]
Type: filesandordirs; Name: "{app}\\eg"

[Files]
Source: "%(libraryDir)s\\*.*"; DestDir: "{app}\\%(libraryName)s"; Flags: ignoreversion recursesubdirs
Source: "%(sourceDir)s\\EventGhost.chm"; DestDir: "{app}"

[Dirs]
Name: "{app}\\%(libraryName)s\\site-packages"

[Run]
Filename: "{app}\\EventGhost.exe"; Parameters: "-install"

[UninstallRun]
Filename: "{app}\\EventGhost.exe"; Parameters: "-uninstall"

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\\EventGhost"
Type: dirifempty; Name: "{app}"
Type: files; Name: "{userstartup}\\EventGhost.lnk"

[Run] 
Filename: "{app}\\EventGhost.exe"; Flags: postinstall nowait skipifsilent 

[Icons]
Name: "{group}\\EventGhost"; Filename: "{app}\\EventGhost.exe"
Name: "{group}\\EventGhost Help"; Filename: "{app}\\EventGhost.chm"
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
    "docutils",
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


class MyInstaller(InnoInstaller):
    appShortName = "EventGhost"
    mainScript = "../EventGhost.pyw"
    icon = "EventGhost.ico"
    excludes = EXCLUDED_MODULES
    innoScriptTemplate = INNO_SCRIPT_TEMPLATE
    outputBaseFilename = None
    
    def __init__(self):
        InnoInstaller.__init__(self)


    def UpdateChangeLog(self):    
        """
        Add a version header to CHANGELOG.TXT if needed.
        """
        path = join(self.sourceDir, "CHANGELOG.TXT")
        timeStr = time.strftime("%m/%d/%Y")
        header = "%s (%s)" % (self.appVersion, timeStr)
        header = header + "\n" + ("=" * len(header)) + "\n"
        infile = open(path, "r")
        data = infile.read(100) # read some data from the beginning
        if not data.strip().startswith("-"):
            # no new lines, so skip the addition of a new header
            return
        data += infile.read() # read the remaining contents
        infile.close()
        outfile = open(path, "w+")
        outfile.write(header + data)
        outfile.close()
        
    
    def UpdateVersionFile(self, incrementBuildNum):
        """
        Update buildNum, buildTime and svnRevision in eg/Classes/Version.py
        """
        svnRevision = self.GetSvnRevision()
        versionFilePath = self.sourceDir + "/eg/Classes/Version.py"
        if incrementBuildNum:
            lines = open(versionFilePath, "rt").readlines()
            outfile = open(versionFilePath, "wt")
            # update buildNum and buildTime in eg/Classes/Version.py
            for line in lines:
                if line.strip().startswith("buildNum"):
                    parts = line.split("=")
                    value = int(parts[1].strip())
                    outfile.write(parts[0] + "= " + str(value+1) + "\n")
                elif line.strip().startswith("buildTime"):
                    parts = line.split("=")
                    outfile.write(parts[0] + "= " + str(time.time()) + "\n")
                elif line.strip().startswith("svnRevision"):
                    parts = line.split("=")
                    outfile.write("%s= %d\n" % (parts[0], svnRevision))
                else:
                    outfile.write(line)
            outfile.close()
        mod = imp.load_source("Version", versionFilePath)
        self.appVersion = mod.Version.string
        
    
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
        if self.pyVersion == "26":
            filename = "%(appShortName)s_%(appVersion)s_Py26_Setup" % self
        else:
            filename = "%(appShortName)s_%(appVersion)s_Setup" % self
        self.outputBaseFilename = filename
        plugins = {}
        for filename in self.GetSetupFiles():
            if filename.startswith("plugins\\"):
                pluginFolder = filename.split("\\")[1]
                plugins[pluginFolder] = True
            if (
                filename.startswith("lib") 
                and not filename.startswith("lib%s\\" % self.pyVersion)
            ):
                continue
            self.AddFile(join(self.sourceDir, filename), dirname(filename))
        for filename in glob(join(self.libraryDir, '*.*')):
            self.AddFile(filename, self.libraryName)
        self.AddFile(join(self.pyVersionDir, "py.exe"))
        self.AddFile(join(self.pyVersionDir, "pyw.exe"))

        # create entries in the [InstallDelete] section of the Inno script to
        # remove all known plugin directories before installing the new 
        # plugins.
        for plugin in plugins.keys():
            self.Add(
                "InstallDelete", 
                'Type: filesandordirs; Name: "{app}\\plugins\\%s"' % plugin
            )
        self.Add(
            "InstallDelete", 
            'Type: files; Name: "{app}\\lib%s\\*.*"' % self.pyVersion
        )
        self.ExecuteInnoSetup()
    
    

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
        
        
    def __getattr__(self, name):
        return self._optionsDict[name].value
    
    
    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            self._optionsDict[name].value = value
    
    
    def __iter__(self):
        return self._options.__iter__()
    
    
    def AddOption(self, name, label, value):
        """ Adds an option to the configuration. """
        option = self.Option(name, label, value)
        self._options.append(option)
        self._optionsDict[name] = option
    
    
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
        configFile = open(self._configFilePath, "w")
        config.write(configFile)
        configFile.close()
        


class MainDialog(wx.Dialog):
    
    def __init__(self, options, builder):
        self.options = options
        self.builder = builder
        wx.Dialog.__init__(self, None, title="Build EventGhost Installer")
        
        # create controls
        self.ctrls = {}
        ctrlsSizer = wx.BoxSizer(wx.VERTICAL)
        for option in list(options)[:-1]:
            ctrl = wx.CheckBox(self, -1, option.label)
            ctrl.SetValue(bool(option.value))
            ctrlsSizer.Add(ctrl, 0, wx.ALL, 5)
            self.ctrls[option.name] = ctrl

        self.ctrls["upload"].Enable(options.ftpUrl != "")
        self.ctrls["commitSvn"].Enable(pysvn is not None)

        
        self.okButton = wx.Button(self, wx.ID_OK)
        self.okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        # add controls to sizers
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(self.okButton)
        btnSizer.AddButton(self.cancelButton)
        btnSizer.Realize()
        
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(ctrlsSizer)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer2, 1, wx.ALL|wx.EXPAND, 0)
        mainSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        self.SetSizerAndFit(mainSizer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
    def OnOk(self, dummyEvent):
        """ Handles a click on the Ok button. """
        self.okButton.Enable(False)
        self.cancelButton.Enable(False)
        #self.SetWindowStyleFlag(wx.CAPTION|wx.RESIZE_BORDER)
        for option in list(self.options)[:-1]:
            ctrl = self.ctrls[option.name]
            setattr(self.options, option.name, ctrl.GetValue())
            ctrl.Enable(False)
        self.options.SaveSettings()
        thread = threading.Thread(
            target=Main, 
            args=(self.options, self.builder, self)
        )
        thread.start()
        
        
    def OnCancel(self, event):
        """ Handles a click on the cancel button. """
        event.Skip()
        self.Destroy()
        #app.ExitMainLoop()
        
        
    @staticmethod
    def OnClose(event):
        """ Handles a click on the close box of the frame. """
        wx.GetApp().ExitMainLoop()
        event.Skip()
     
     
def ExecutePy(scriptFilePath, *args):
    """Spawn a new Python interpreter and let it execute a script file."""
    startupInfo = subprocess.STARTUPINFO()
    startupInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
    startupInfo.wShowWindow = subprocess.SW_HIDE 
    cmdArgs = [sys.executable, scriptFilePath]
    cmdArgs.extend(args)
    errorcode = subprocess.call(
        cmdArgs, 
        stdout=sys.stdout.fileno(),
        startupinfo=startupInfo
    )
    if errorcode > 0:
        raise SystemError
    
        
def BuildImportsPy():
    oldCwd = os.getcwdu()
    import BuildImports
    os.chdir(abspath(u"Python%d%d" % sys.version_info[:2]))
    BuildImports.Main(INCLUDED_MODULES, EXCLUDED_MODULES)
    os.chdir(oldCwd)
        
        
def Main(options, builder, mainDialog=None):
    """
    Main task of the script.
    """
    if options.incrementBuildNum:
        print "--- updating Version.py"
    builder.UpdateVersionFile(options.incrementBuildNum)
    print "--- updating CHANGELOG.TXT"
    builder.UpdateChangeLog()
    if options.buildStaticImports:
        print "--- building StaticImports.py"
        ExecutePy("BuildStaticImports.py")
    if options.buildImports:
        print "--- building imports.py"
        BuildImportsPy()
    if options.buildHtmlDocs or options.buildChmDocs:
        print "--- building docs"
        args = ["BuildDocs.py"]
        if options.buildHtmlDocs:
            args.append("html")
        if options.buildChmDocs:
            args.append("chm")
        ExecutePy(*args)
    if options.commitSvn:
        print "--- committing working copy to SVN"
        builder.CommitSvn()
    if options.buildSourceArchive:
        print "--- building source code archive"
        builder.CreateSourceArchive()
    if options.buildPyExe:
        print "--- building py.exe and pyw.exe"
        ExecutePy("BuildPyExe.py")
    if options.buildLib:
        print "--- building library files"
        builder.CreateLibrary()            
    if options.buildInstaller:
        print "--- building setup.exe"
        builder.CreateInstaller()
        filename = join(builder.outputDir, builder.outputBaseFilename + ".exe")
        if options.upload and options.ftpUrl:
            print "--- uploading setup.exe"
            import UploadFile
            wx.CallAfter(
                UploadFile.UploadDialog, 
                mainDialog, 
                filename, 
                options.ftpUrl
            )        
    print "--- All done!"
    wx.CallAfter(mainDialog.Close)
    

OPTIONS = (
    ("includeNoIncludePlugins", "Include 'noinclude' plugins", False),
    ("incrementBuildNum", "Increment build number", False),
    ("buildStaticImports", "Build StaticImports.py", True),
    ("buildImports", "Build imports.py", True),
    ("buildHtmlDocs", "Build HTML docs", True),
    ("buildChmDocs", "Build CHM docs", True),
    ("buildSourceArchive", "Build source archive", True),
    ("buildPyExe", "Build py.exe and pyw.exe", True),
    ("buildLib", "Build lib%d%d" %sys.version_info[0:2], True),
    ("buildInstaller", "Build Setup.exe", True),
    ("commitSvn", "SVN commit", False),
    ("upload", "Upload through FTP", False),
    ("ftpUrl", "", ""),
)


def RunGui():
    builder = MyInstaller()
    options = Config(INI_FILE)
    for option in OPTIONS:
        options.AddOption(*option)
    options.LoadSettings()
    app = wx.App(0)
    app.SetExitOnFrameDelete(True)
    mainDialog = MainDialog(options, builder)
    mainDialog.Show()
    app.MainLoop()
    
RunGui()

