# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

ROOT_DLLS = [
    #"MFC71.dll", "msvcr71.dll", "msvcp71.dll"
]


import py2exe
import wx
import sys
import tempfile
import os
import re
import fnmatch
import time
import zipfile
import subprocess
import _winreg
import locale
import ConfigParser
import threading

from shutil import copy2 as copy
from os.path import basename, dirname, abspath, join, exists
from glob import glob
try:
    import pysvn
except ImportError:
    pysvn = None

tmpDir = tempfile.mkdtemp()
toolsDir = abspath(dirname(sys.argv[0]))
trunkDir = abspath(join(toolsDir, ".."))
outDir = abspath(join(trunkDir, ".."))
PYVERSION = str(sys.version_info[0]) + str(sys.version_info[1])

# Add our working dir to the import pathes
sys.path.append(toolsDir)
sys.path.append(abspath(u"Python%s" % PYVERSION))
os.chdir(abspath(u"Python%s" % PYVERSION))



class Option(object):
    
    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value
        

class Config(object):
    
    def __init__(self, configFilePath):
        self._configFilePath = configFilePath
        self._options = []
        self._optionsDict = {}
        
        
    def AddOption(self, name, label, value):
        option = Option(name, label, value)
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
        

#from py2exe.build_exe import isSystemDLL
#origIsSystemDLL = isSystemDLL
#def newIsSystemDLL(pathname):
#    res = origIsSystemDLL(pathname)
#    if res:
#        print "system dll", pathname, res
#    return res
#py2exe.build_exe.isSystemDLL = newIsSystemDLL

SourcePattern = [
    "*.py", 
    "*.pyw", 
    "*.pyd", 
    "*.txt", 
    "*.png", 
    "*.jpg", 
    "*.gif", 
    "*.xml", 
    "*.ico",
    "*.vbs",
]

def GetFiles(files, pattern):
    for directory in ("eg", "plugins", "languages", "images"):
        for path in locate(pattern, join(trunkDir, directory)):
            files.append(path[len(trunkDir)+1:])
    return files


def GetSetupFiles():
    files = [
        "Example.xml",
        "CHANGELOG.TXT",
    ]
    return GetFiles(files, SourcePattern + ["*.dll"])
    

def UpdateVersionFile():
    versionFilePath = join(trunkDir, "eg", "Classes", "Version.py")
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
        else:
            fd.write(line)
    fd.close()
    data = {}
    execfile(versionFilePath, data, data)
    versionCls = data["Version"]
    if Options.commitSvn:
        def ssl_server_trust_prompt(trust_dict):
            return True, 0, True
        svn = pysvn.Client()
        svn.callback_ssl_server_trust_prompt = ssl_server_trust_prompt
        svn.checkin([trunkDir], "Created installer for %s" % versionCls.string)    return versionCls
    
    
def UpdateChangeLog(namespace):    
    path = join(trunkDir, "CHANGELOG.TXT")
    s1 = "Version %s (%s)\n" % (
        namespace.VERSION, 
        time.strftime("%m/%d/%Y"),
    )
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
    

def locate(patterns, root=os.curdir):
    '''
    Locate all files matching supplied filename patterns in and below
    supplied root directory.
    '''
    for path, dirs, files in os.walk(root):
        ignoreDirs = [
            dir for dir in dirs 
                if (
                    dir.startswith("_") 
                    or dir == ".svn"
                    or (not Options.includeNoIncludePlugins and exists(join(path, dir, "noinclude")))
                )
        ]
        for dir in ignoreDirs:
            dirs.remove(dir)
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                yield join(path, filename)

    
def RemoveDirectory(path):
    """
    Remove a directory and all its contents.
    DANGEROUS!
    """
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            try:
                os.remove(join(root, name))
            except:
                pass
        for name in dirs:
            try:
                os.rmdir(join(root, name))
            except:
                pass
    try:
        os.rmdir(path)
    except:
        pass



# The manifest will be inserted as resource into the exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
PY25_MANIFEST_TEMPLATE = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity
        version="5.0.0.0"
        processorArchitecture="x86"
        name="%(prog)s"
        type="win32"
    />
    <description>%(prog)s Program</description>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.Windows.Common-Controls"
                version="6.0.0.0"
                processorArchitecture="X86"
                publicKeyToken="6595b64144ccf1df"
                language="*"
            />
        </dependentAssembly>
    </dependency>
</assembly>
'''

MANIFEST_TEMPLATE = """
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
        <security>
            <requestedPrivileges>
                <requestedExecutionLevel 
                    level="asInvoker" 
                    uiAccess="false"
                />
            </requestedPrivileges>
        </security>
    </trustInfo>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity 
                type="win32" 
                name="Microsoft.VC90.CRT" 
                version="9.0.21022.8" 
                processorArchitecture="x86" 
                publicKeyToken="1fc8b3b9a1e18e3b"
            />
        </dependentAssembly>
    </dependency>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.Windows.Common-Controls"
                version="6.0.0.0"
                processorArchitecture="X86"
                publicKeyToken="6595b64144ccf1df"
                language="*"
            />
        </dependentAssembly>
    </dependency>
</assembly>"""


RT_MANIFEST = 24
shortpgm = "EventGhost"
PY2EXE_EXCLUDES = [
    "pywin",
    "pywin.dialogs",
    "pywin.dialogs.list",
    "_ssl",
    # no TCL
    "Tkconstants", 
    "Tkinter", 
    "tcl",
    # and no TCL through PIL
    "_imagingtk", 
    "PIL._imagingtk", 
    "ImageTk", 
    "PIL.ImageTk", 
    "FixTk",
    "comtypes.gen",
    #"bsddb",
    #"_bsddb",
]


py2exeOptions = dict(
    options = dict(
        build = dict(
            build_base = join(tmpDir, "build")
        ),
        py2exe = dict(
            compressed = 0,
            includes = [
                "encodings",
                "encodings.*",
            ],
            excludes = PY2EXE_EXCLUDES,
            dll_excludes = [
                "DINPUT8.dll", 
                "w9xpopen.exe", 
                #"gdiplus.dll", 
                #"msvcr71.dll",
            ],
            dist_dir = trunkDir,
            custom_boot_script=join(trunkDir, "eg", "Py2ExeBootScript.py")
        )
    ),
    # The lib directory contains everything except the executables and the python dll.
    zipfile = "lib\\python%s.zip" % PYVERSION,
    windows = [
        dict(
            script = join(trunkDir, "EventGhost.pyw"),
            icon_resources = [(1, join(trunkDir, "EventGhost.ico"))],
            other_resources = [
                (RT_MANIFEST, 1, MANIFEST_TEMPLATE % dict(prog=shortpgm))
            ],
            dest_base = shortpgm
        ),
    ],
    # use out build_installer class as extended py2exe build command
    #cmdclass = {"py2exe": py2exe.run},
    verbose = 0,
)

consoleOptions = dict(
    options = dict(
        build = dict(
            build_base = join(tmpDir, "build2")
        ),
        py2exe = dict(
            compressed = 0,
            dist_dir = trunkDir,
            excludes = PY2EXE_EXCLUDES,
            dll_excludes = ["w9xpopen.exe"],
        )
    ),
    zipfile = "lib\\python%s.zip" % PYVERSION,
    windows = [
        dict(
            script = join(toolsDir, "py.py"),
            dest_base = "pyw"
        )
    ],
    console = [
        dict(
            script = join(toolsDir, "py.py"),
            dest_base = "py"
        )
    ],
    verbose = 0,
)


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
AppVerName=EventGhost %(VERSION)s
DefaultDirName={pf}\\EventGhost
DefaultGroupName=EventGhost
Compression=lzma/ultra
SolidCompression=yes
InternalCompressLevel=ultra
OutputDir=%(OUT_DIR)s
OutputBaseFilename=%(OUT_FILE_BASE)s
InfoBeforeFile=%(TOOLS_DIR)s\\LICENSE.RTF
DisableReadyPage=yes
AppMutex=EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B

[InstallDelete]
Type: filesandordirs; Name: "{app}\\eg"
%(INSTALL_DELETE)s

[Files]
Source: "%(TRUNK)s\\*.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(TRUNK)s\\*.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(TRUNK)s\\*.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(TRUNK)s\\lib\\*.*"; DestDir: "{app}\\lib"; Flags: ignoreversion recursesubdirs
%(INSTALL_FILES)s
Source: "%(TRUNK)s\\Example.xml"; DestDir: "{userappdata}\\EventGhost"; DestName: "MyConfig.xml"; Flags: onlyifdoesntexist uninsneveruninstall

[Dirs]
Name: "{app}\\lib\site-packages"

[Run]
Filename: "{app}\\EventGhost.exe"; Parameters: "-install"

[UninstallRun]
Filename: "{app}\\EventGhost.exe"; Parameters: "-uninstall"

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


def InstallPy2exePatch():
    # ModuleFinder can't handle runtime changes to __path__, but win32com 
    # uses them, particularly for people who build from sources.  Hook this in.
    try:
        import modulefinder
        import win32com
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]:#,"win32com.shellcon","win32com.mapi"]:
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError:
        # no build path setup, no worries.
        pass


def CompileInnoScript(innoScriptPath):
    """
    Execute command line to compile the Inno Script File
    """
    key = _winreg.OpenKey(
        _winreg.HKEY_LOCAL_MACHINE, 
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 5_is1"
    )
    installPath, _ = _winreg.QueryValueEx(key, "InstallLocation")
    _winreg.CloseKey(key)
    return Execute(join(installPath, "ISCC.exe"), "/Q", innoScriptPath)
    
        

def Execute(*args):
    si = subprocess.STARTUPINFO()
    si.dwFlags = subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE 
    return subprocess.call(
        args, 
        #stdout=sys.stdout.fileno(),
        startupinfo=si
    )


def MakeSourceArchive(outFile):
    svn = pysvn.Client()
    
    def ssl_server_trust_prompt(trust_dict):
        return True, 0, True
    svn.callback_ssl_server_trust_prompt = ssl_server_trust_prompt
    
    def callback_notify(event_dict):
        print event_dict["path"][len(tmpDir)+1:]
    svn.callback_notify = callback_notify
    
    print "Checking out trunk"
    svn.checkout(trunkDir, tmpDir)
    zipFile = zipfile.ZipFile(outFile, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(tmpDir):
        if '.svn' in dirs:
            dirs.remove('.svn')
        if "noinclude" in files:
            continue
        for file in files:
            filename = os.path.join(root, file)
            arcname = filename[len(tmpDir)+1:]
            zipFile.write(filename, arcname)
            print "compressing", arcname
    zipFile.close()
    svn.cleanup(tmpDir)
    RemoveDirectory(tmpDir)


def MakeInstaller():
    version = UpdateVersionFile()
    print "Updated Version File"
    class namespace:
        PYTHON_DIR = dirname(sys.executable)
        OUT_DIR = outDir
        TRUNK = trunkDir
        TOOLS_DIR = toolsDir
        DIST = join(tmpDir, "dist")
        VERSION = version.string
    UpdateChangeLog(namespace)
    print "Updated ChangeLog"
    
    installDeleteDirs = []
    for item in os.listdir(join(trunkDir, "plugins")):
        if item.startswith("."):
            continue
        if os.path.isdir(join(trunkDir, "plugins", item)):
            installDeleteDirs.append(
                'Type: filesandordirs; Name: "{app}\\plugins\\%s"' % item
            )
    installDelete = "\n".join(installDeleteDirs)
    namespace.INSTALL_DELETE = installDelete
    
    if Options.createSourceArchive:
        MakeSourceArchive(join(outDir, "EventGhost_%s_Source.zip" % namespace.VERSION))
        
    if Options.createLib:
        from distutils.core import setup
        InstallPy2exePatch()
        RemoveDirectory(join(trunkDir, "lib"))
        setup(**consoleOptions)
        setup(**py2exeOptions)
        pythonDir = dirname(sys.executable)
        # remove unneeded DLLs
        dllNames = [
            basename(name) for name in glob(join(trunkDir, "lib", "*.dll"))
        ]
        neededDlls = []
        for path, dirs, files in os.walk(pythonDir):
            for file in files:
                if file in dllNames:
                    neededDlls.append(file)
        for file in dllNames:
            if file not in neededDlls:
                os.remove(join(trunkDir, "lib", file))
                
        # copy needed DLLs
        for dll in ROOT_DLLS:
            if not os.path.exists(join(trunkDir, dll)):
                copy(join(pythonDir, dll), trunkDir)
                    
    if Options.createInstaller:
        installFiles = []
        for file in GetSetupFiles():
            installFiles.append(
                'Source: "%s"; DestDir: "{app}\\%s";' % 
                    (join(trunkDir, file), dirname(file))
            )
        innoScriptPath = abspath(join(tmpDir, "Setup.iss"))
        template = INNO_SCRIPT_TEMPLATE
        namespace.OUT_FILE_BASE = "EventGhost_%s_Setup" % namespace.VERSION
            
        namespace.INSTALL_FILES = "\n".join(installFiles)  
        
        fd = open(innoScriptPath, "w")
        fd.write(template % namespace.__dict__)
        fd.close()
        
        print "Calling Inno Setup Compiler"
        if CompileInnoScript(innoScriptPath) > 0:
            raise SystemError
        print "Building installer done!"
        RemoveDirectory(tmpDir)
        return join(outDir, namespace.OUT_FILE_BASE + ".exe")



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
        
        self.out = wx.TextCtrl(
            self, 
            style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL 
        )
        self.out.SetMinSize((400, 100))
        #sys.stderr = self.out
        sys.stdout = self.out
        self.out.SetBackgroundColour(self.GetBackgroundColour())

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
        sizer2.Add(self.out, 1, wx.EXPAND|wx.ALL, 10)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer2, 1, wx.ALL|wx.EXPAND, 0)
        sizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        self.SetSizerAndFit(sizer)
        
        
    def OnOk(self, event):
        self.okButton.Enable(False)
        self.cancelButton.Enable(False)
        #self.SetWindowStyleFlag(wx.CAPTION|wx.RESIZE_BORDER)
        for option in list(Options)[:-1]:
            ctrl = getattr(self.Ctrls, option.name)
            setattr(Options, option.name, ctrl.GetValue())
            ctrl.Enable(False)
        Options.SaveSettings()
        thread = threading.Thread(target=self.ThreadProc)
        thread.start()
        
        
    def ThreadProc(self):
        if Options.createImports:
            import MakeImports
            MakeImports.Main()
        filename = MakeInstaller()
        if Options.upload and Options.ftpUrl:
            import UploadFile
            wx.CallAfter(UploadFile.UploadDialog, self, filename, Options.ftpUrl)        
    
    
    def OnCancel(self, event):
        event.Skip()
        self.Destroy()
        #app.ExitMainLoop()
     
     
Options = Config(join(toolsDir, "MakeInstaller.ini"))
Options.AddOption("includeNoIncludePlugins", "Include 'noinclude' plugins", False)
Options.AddOption("createSourceArchive", "Create Source Archive", False)
Options.AddOption("createImports", "Create Imports", False)
Options.AddOption("createLib", "Create Lib", False)
Options.AddOption("createInstaller", "Create Installer", True)
Options.AddOption("commitSvn", "SVN Commit", True)
Options.AddOption("upload", "Upload through FTP", True)
Options.AddOption("ftpUrl", "", "")
Options.LoadSettings()

sys.argv.append("py2exe")
app = wx.App(0)
app.SetExitOnFrameDelete(True)
mainDialog = MainDialog()
mainDialog.Show()
app.MainLoop()

