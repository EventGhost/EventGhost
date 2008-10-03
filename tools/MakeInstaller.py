# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

ROOT_DLLS = ["MFC71.dll", "msvcr71.dll", "msvcp71.dll"]

OptionsList = (
    ("Create Source Archive", "createSourceArchive", False),
    ("Create Imports", "createImports", False),
    ("Create Lib", "createLib", False),
    ("SVN Commit", "commitSvn", True),
    ("Upload", "upload", True),
    ("Include 'noinclude' plugins", "includeNoIncludePlugins", False),
    ("Create Update", "createUpdate", False),
)

import py2exe
from py2exe.build_exe import isSystemDLL
origIsSystemDLL = isSystemDLL
def newIsSystemDLL(pathname):
    res = origIsSystemDLL(pathname)
    if res:
        print "system dll", pathname, res
    return res
py2exe.build_exe.isSystemDLL = newIsSystemDLL

class Options:
    pass

for label, name, default in OptionsList:
    setattr(Options, name, default)

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

from ftplib import FTP
from urlparse import urlparse
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


def GetSourceFiles():
    files = [
        "EventGhost.pyw",
        "EventGhost.ico",
        "Example.xml",
        "LICENSE.TXT",
        "CHANGELOG.TXT",
    ]
    return GetFiles(files, SourcePattern)


def GetUpdateFiles():
    files = [
        "Example.xml",
        "LICENSE.TXT",
        "CHANGELOG.TXT",
    ]
    return GetFiles(files, SourcePattern)
    

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

manifest_template = '''
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
    "bsddb",
    "_bsddb",
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
                "gdiplus.dll", 
                "msvcr71.dll",
            ],
            dist_dir = trunkDir,
            custom_boot_script=join(trunkDir, "eg", "Py2ExeBootScript.py")
        )
    ),
    # The lib directory contains everything except the executables and the python dll.
    zipfile = r"lib\python25.zip",
    windows = [
        dict(
            script = join(trunkDir, "EventGhost.pyw"),
            icon_resources = [(1, join(trunkDir, "EventGhost.ico"))],
            other_resources = [
                (RT_MANIFEST, 1, manifest_template % dict(prog=shortpgm))
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
    zipfile = r"lib\python25.zip",
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

inno_update = """
[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: Deutsch; MessagesFile: "compiler:Languages\\German.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"

[Setup]
ShowLanguageDialog=auto
AppId=EventGhost
AppName=EventGhost
AppVerName=EventGhost-Update %(version)s build %(buildNum)s
DefaultDirName={pf}\EventGhost
DefaultGroupName=EventGhost
Compression=lzma/max
SolidCompression=yes
InternalCompressLevel=max
OutputDir=%(OUT_DIR)s
OutputBaseFilename=%(OUT_FILE_BASE)s
;DisableFinishedPage=yes
DisableReadyPage=yes
CreateUninstallRegKey=no
UpdateUninstallLogAppName=no
AppMutex=EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B

[Run]
Filename: "{app}\\EventGhost.exe"; Parameters: "-install"

[Run] 
Filename: "{app}\\EventGhost.exe"; Flags: postinstall nowait skipifsilent 

[InstallDelete]
Type: filesandordirs; Name: "{app}\\eg"

[Files]
Source: "%(TRUNK)s\\*.exe"; DestDir: "{app}"; Flags: ignoreversion
%(INSTALL_FILES)s
Source: "%(TRUNK)s\\Example.xml"; DestDir: "{userappdata}\\EventGhost"; DestName: "MyConfig.xml"; Flags: onlyifdoesntexist uninsneveruninstall
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
    return Execute(join(installPath, "ISCC.exe"), innoScriptPath)
    
        

def Execute(*args):
    si = subprocess.STARTUPINFO()
    si.dwFlags = subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE 
    return subprocess.call(
        args, 
        stdout=sys.stdout.fileno(),
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
                    
    installFiles = []
    if Options.createUpdate:
        for file in GetUpdateFiles():
            installFiles.append(
                'Source: "' + join(trunkDir, file) + '"; DestDir: "{app}\\' + dirname(file) + '";'
            )
        innoScriptPath = abspath(join(tmpDir, "Update.iss"))
        template = inno_update
        namespace.OUT_FILE_BASE = "EventGhost_%s_Update" % namespace.VERSION
    else:
        for file in GetSetupFiles():
            installFiles.append(
                'Source: "' + join(trunkDir, file) + '"; DestDir: "{app}\\' + dirname(file) + '";'
            )
        innoScriptPath = abspath(join(tmpDir, "Setup.iss"))
        template = INNO_SCRIPT_TEMPLATE
        namespace.OUT_FILE_BASE = "EventGhost_%s_Setup" % namespace.VERSION
        
    namespace.INSTALL_FILES = "\n".join(installFiles)  
    
    fd = open(innoScriptPath, "w")
    fd.write(template % namespace.__dict__)
    fd.close()
    
    print "Calling Inno Setup Compiler"
    CompileInnoScript(innoScriptPath)
    print "Building installer done!"
    RemoveDirectory(tmpDir)
    return join(outDir, namespace.OUT_FILE_BASE + ".exe")



class Speedometer:
    
    def __init__(self):
        self.period = 15
        self.Reset()
        
    def Reset(self):
        now = time.clock()
        self.start = now
        self.lastSecond = now
        self.rate = 0
        self.lastBytes = 0
        
    def Add(self, b):
        now = time.clock()
        if b == 0 and (now - self.lastSecond) < 0.1:
            return
        
        if self.rate == 0:
            self.Reset()
            
        div = self.period * 1.0
        if self.start > now:
            self.start = now
        if now < self.lastSecond:
            self.lastSecond = now
            
        timePassedSinceStart = now - self.start
        timePassed = now - self.lastSecond
        if timePassedSinceStart < div:
            div = timePassedSinceStart
        if div < 1:
            div = 1.0
            
        self.rate *= 1 - timePassed / div
        self.rate += b / div
        
        self.lastSecond = now
        if b > 0:
            self.lastBytes = now
        if self.rate < 0:
            self.rate = 0
        
        
def UploadFile(filename, url):
    aborted = False
    speedo = Speedometer()
    
    class progress:
        def __init__(self, filepath):
            self.size = os.path.getsize(filepath)
            self.fd = open(filepath, "rb")
            self.pos = 0
            self.startTime = time.clock()
            
        def read(self, size):
            if size + self.pos > self.size:
                size = self.size - self.pos
            speedo.Add(size)
            remaining = (self.size - self.pos + size) / speedo.rate
            percent = 100.0 * self.pos / self.size
            print "%d%%" % percent, "%0.2f KiB/s" % (speedo.rate / 1024), "%0.2fs" % remaining
            self.pos += size
            return self.fd.read(size)
        
        def close(self):
            self.fd.close()
            elapsed = (time.clock() - self.startTime)
            print "File uploaded in %0.2f seconds" % elapsed
            print "Average speed: %0.2f KiB/s" % (self.size / (elapsed * 1024))
            
    urlComponents = urlparse(url)
    fd = progress(filename)
    print "Connecting: %s" % urlComponents.hostname
    ftp = FTP(
        urlComponents.hostname, 
        urlComponents.username, 
        urlComponents.password
    )
    print "Changing path to: %s" % urlComponents.path
    ftp.cwd(urlComponents.path)
    print "Getting filelist."
    try:
        fileList = ftp.nlst()
    except:
        fileList = []
    for i in range(0, 999999):
        tempFileName = "tmp%06d" % i
        if tempFileName not in fileList:
            break
    print "Starting upload."
    ftp.storbinary("STOR " + tempFileName, fd, 64 * 1024)
    fd.close()
    if aborted:
        ftp.delete(tempFileName)
    else:
        ftp.rename(tempFileName, basename(filename))
    ftp.quit()
    print "Upload done!"
    
    
    
class MainDialog(wx.Dialog):
    class Ctrls:
        pass
    
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Make EventGhost Installer")
        self.LoadSettings()
        
        # create controls
        ctrls = []
        for label, name, default in OptionsList:
            ctrl = wx.CheckBox(self, -1, label)
            ctrl.SetValue(default)
            ctrls.append(ctrl)
            setattr(self.Ctrls, name, ctrl)
        self.Ctrls.upload.Enable(self.url != "")
        self.Ctrls.commitSvn.Enable(pysvn is not None)
        
        okButton = wx.Button(self, wx.ID_OK)
        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        cancelButton = wx.Button(self, wx.ID_CANCEL)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        # add controls to sizers
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(okButton)
        btnSizer.AddButton(cancelButton)
        btnSizer.Realize()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        for ctrl in ctrls:
            sizer.Add(ctrl, 0, wx.ALL, 10)
        sizer.Add(btnSizer, 0, wx.ALL, 10)
        self.SetSizerAndFit(sizer)
        
        
    def SaveSettings(self):
        config = ConfigParser.ConfigParser()
        # make ConfigParser case-sensitive
        config.optionxform = str
        config.read(join(toolsDir, "MakeInstaller.ini"))
        if not config.has_section("Settings"):
            config.add_section("Settings")
        for label, ident, value in OptionsList:
            value = getattr(Options, ident)
            config.set("Settings", ident, value)
        fd = open(join(toolsDir, "MakeInstaller.ini"), "w")
        config.write(fd)
        fd.close()
        
    
    def LoadSettings(self):
        global OptionsList
        config = ConfigParser.ConfigParser()
        config.read(join(toolsDir, "MakeInstaller.ini"))
        if config.has_option("Settings", "ftpUrl"):
            self.url = config.get("Settings", "ftpUrl")
        else:
            self.url = ""
        newOptionsList = []
        for label, ident, value in OptionsList:
            if config.has_option("Settings", ident):
                value = config.getboolean("Settings", ident)
            newOptionsList.append((label, ident, value))
        OptionsList = newOptionsList
        

    def OnOk(self, event):
        self.Show(False)
        for label, name, default in OptionsList:
            setattr(Options, name, getattr(self.Ctrls, name).GetValue())
        self.SaveSettings()
        if Options.createImports:
            import MakeImports
            MakeImports.Main()
        filename = MakeInstaller()
        if Options.upload:
            UploadFile(filename, self.url)
        print filename
        app.ExitMainLoop()
        
        
    def OnCancel(self, event):
        app.ExitMainLoop()
     
     
sys.argv.append("py2exe")
app = wx.App(0)
app.SetExitOnFrameDelete(False)
mainDialog = MainDialog()
mainDialog.Show()
app.MainLoop()

