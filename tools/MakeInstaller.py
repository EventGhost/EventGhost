import wx
import sys
from os.path import basename, dirname, abspath, join
import tempfile
import os
import re
import fnmatch
import shutil
import time


tmpDir = tempfile.mkdtemp()
trunkDir = abspath(join(dirname(sys.argv[0]), ".."))
outDir = abspath(join(trunkDir, "../.."))


def GetVersion():
    data = {}
    versionFilePath = join(trunkDir, "eg/Version.py")
    execfile(versionFilePath, data, data)
    data['buildNum'] += 1
    data['compileTime'] = time.time()
    fd = file(versionFilePath, "wt")
    fd.write("version = " + repr(data['version']) + "\n")
    fd.write("buildNum = " + repr(data['buildNum']) + "\n")
    fd.write("compileTime = " + repr(data['compileTime']) + "\n")
    fd.close()        return data
    
    
def locate(pattern, root=os.curdir):
    '''
    Locate all files matching supplied filename pattern in and below
    supplied root directory.
    '''
    for path, dirs, files in os.walk(root):
        for filename in fnmatch.filter(files, pattern):
            yield join(path, filename)

    
def xcopy(srcdir, destdir, pattern):
    if not os.path.exists(destdir):
        os.makedirs(destdir)
    for root, dirs, files in os.walk(srcdir):
        destdir2 = join(destdir, root[len(srcdir) + 1:])
        for dir in dirs:
            if not os.path.exists(join(destdir2, dir)):
                os.makedirs(join(destdir2, dir))
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                shutil.copy2(join(root, file), join(destdir2, file))
                
                
def removedir(path):
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


def GetDir(theDir, extension=None):
    list = os.listdir(theDir)
    x2 = []
    for x in list:
        if extension:
            if os.path.splitext(x)[1] != extension:
                continue
        x2.append(theDir + x)
    return x2

from shutil import copy2 as copy
import zipfile

#os.chdir(main_dir)
#
#bases = ("eg", "plugins", "Languages")
#for base in ("eg", "plugins", "Languages"):
#    for filename in locate("*.py", base):
#        #print filename
#        data = open(filename, "rb").read()
#        if '\0' in data:
#            print "Binary!", filename
#            continue
#        newdata = re.sub("\r?\n", "\r\n", data)
#        if newdata != data:
#            f = open(filename, "wb")
#            f.write(newdata)
#            f.close()
#
#
#
#for pattern in ("*.py", "*.pyd", "*.png", "*.txt"):
#    xcopy("eg", join(tmpDir, "source\\eg"), pattern)
#for pattern in ("*.png", "*.ico", "*.gif"):
#    xcopy("images", join(tmpDir, "source\\images"), pattern)
#for pattern in ("*.py", "*.pyd", "*.png", "*.gif", "*.jpg"):
#    xcopy("plugins", join(tmpDir, "source\\plugins"), pattern)
#    
#
#xcopy("Languages", join(tmpSourceDir, "languages"), "*.py")
#
#for dir in os.listdir(join(tmpSourceDir, "plugins")):
#    if dir[:1] == "_":
#        removedir(join(tmpSourceDir, "plugins", dir))
#
#copy("EventGhost.pyw", tmpSourceDir)
#copy("EventGhost.ico", tmpSourceDir)
#copy("LICENSE.TXT", tmpSourceDir)
#copy("Example.xml", tmpSourceDir)

def MakeSourceArchive(filepath):
    archive = zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(tmpSourceDir):
        destdir = root[len(tmpSourceDir) + 1:]
        for file in files:
            archive.write(join(destdir, file))
    archive.close()


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



py2exeOptions = dict(
    options = dict(
        build = dict(
            build_base = join(tmpDir, "build")
        ),
        py2exe = dict(
            compressed = 0,
            includes = [
                "encodings",
                "encodings.latin_1",
                "encodings.cp1252",
                "encodings.utf_8",
                "encodings.ascii",
                "encodings.idna",
            ],
            excludes = [
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
            ],
            dll_excludes = ["DINPUT8.dll", "w9xpopen.exe", "gdiplus.dll", "msvcr71.dll"],
            dist_dir = join(tmpDir, "dist"),
        )
    ),
    # The lib directory contains everything except the executables and the python dll.
    #zipfile = r"lib\shardlib",
    zipfile = r"lib\python25.zip",
    windows = [
        dict(
            script = join(trunkDir, "EventGhost.pyw"),
            icon_resources = [(1, join(trunkDir, "EventGhost.ico"))],
            other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog=shortpgm))],
            dest_base = shortpgm
        )
    ],
    # use out build_installer class as extended py2exe build command
    #cmdclass = {"py2exe": py2exe.run},
)


inno_script = """
; WARNING: This script has been created by py2exe. Changes to this script
; will be overwritten the next time py2exe is run!

[Tasks]
Name: "desktopicon"; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: Deutsch; MessagesFile: "compiler:Languages\German.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"

[Setup]
ShowLanguageDialog=auto
AppName=EventGhost
AppVerName=EventGhost %(version)s build %(buildNum)s
DefaultDirName={pf}\EventGhost
DefaultGroupName=EventGhost
Compression=lzma/max
SolidCompression=yes
InternalCompressLevel=max
OutputDir=%(OUT_DIR)s
OutputBaseFilename=%(OUT_FILE_BASE)s
LicenseFile=%(TRUNK)s\LICENSE.TXT
DisableReadyPage=yes
AppMutex=EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B

[InstallDelete]
Type: filesandordirs; Name: "{app}\eg"

[Files]
Source: "%(DIST)s\*.*"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(DIST)s\lib\*.*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs

Source: "%(TRUNK)s\images\*.png"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\images\*.ico"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist

Source: "%(TRUNK)s\plugins\*.py"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.pyd"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.dll"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.txt"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.png"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.gif"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.jpg"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist

Source: "%(TRUNK)s\eg\*.py"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs
Source: "%(TRUNK)s\eg\*.pyd"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\eg\*.png"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\eg\*.txt"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist

Source: "%(TRUNK)s\languages\*.py"; DestDir: "{app}\languages"; Flags: ignoreversion recursesubdirs
Source: "%(TRUNK)s\Example.xml"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(TRUNK)s\Example.xml"; DestDir: "{userappdata}\EventGhost"; DestName: "MyConfig.xml"; Flags: onlyifdoesntexist uninsneveruninstall
Source: "%(PYTHON_DIR)s\MFC71.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(PYTHON_DIR)s\msvcr71.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(PYTHON_DIR)s\msvcp71.dll"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "{app}\EventGhost.exe"; Parameters: "-install"

[UninstallRun]
Filename: "{app}\EventGhost.exe"; Parameters: "-uninstall"

[Run] 
Filename: "{app}\EventGhost.exe"; Flags: postinstall nowait skipifsilent 

[Icons]
Name: "{group}\EventGhost"; Filename: "{app}\EventGhost.exe"
Name: "{group}\Uninstall EventGhost"; Filename: "{uninstallexe}"
Name: "{userdesktop}\EventGhost"; Filename: "{app}\EventGhost.exe"; Tasks: desktopicon
"""

inno_update = """
[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: Deutsch; MessagesFile: "compiler:Languages\\German.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"

[Setup]
ShowLanguageDialog=auto
AppId=EventGhost
AppName=EventGhost-Update %(version)s build %(buildNum)s
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
Filename: "{app}\EventGhost.exe"; Parameters: "-install"

[Run] 
Filename: "{app}\EventGhost.exe"; Flags: postinstall nowait skipifsilent 

[InstallDelete]
Type: filesandordirs; Name: "{app}\eg"

[Files]
Source: "%(DIST)s\*.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "%(TRUNK)s\images\*.png"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\images\*.ico"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist

Source: "%(TRUNK)s\plugins\*.py"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.pyd"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
;Source: "%(TRUNK)s\plugins\*.dll"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.txt"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.png"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.gif"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\plugins\*.jpg"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist

Source: "%(TRUNK)s\eg\*.py"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs
Source: "%(TRUNK)s\eg\*.pyd"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\eg\*.png"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist
Source: "%(TRUNK)s\eg\*.txt"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs skipifsourcedoesntexist

Source: "%(TRUNK)s\languages\*.py"; DestDir: "{app}\languages"; Flags: ignoreversion recursesubdirs
Source: "%(TRUNK)s\Example.xml"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(TRUNK)s\Example.xml"; DestDir: "{userappdata}\EventGhost"; DestName: "MyConfig.xml"; Flags: onlyifdoesntexist uninsneveruninstall
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


def GetInnoCompilePath(filename):
    """
    Return command line to compile the Inno Script File 'filename'
    """
    import _winreg
    key = _winreg.OpenKey(
        _winreg.HKEY_CLASSES_ROOT, 
        "InnoSetupScriptFile\\shell\\Compile"
    )
    value = _winreg.QueryValue(key, "command")
    _winreg.CloseKey(key)
    return value.replace("%1", filename)
    
    

def ExecuteAndWait(commandLine, workingDir=None):
    import win32event
    import win32con
    import win32process

    si = win32process.STARTUPINFO()
    si.dwFlags = win32con.STARTF_USESHOWWINDOW
    si.wShowWindow = win32con.SW_SHOWNORMAL
    hProcess, _, _, _ = win32process.CreateProcess(
        None,         # AppName
        commandLine,  # Command line
        None,         # Process Security
        None,         # ThreadSecurity
        0,            # Inherit Handles?
        win32con.NORMAL_PRIORITY_CLASS|win32con.CREATE_NEW_CONSOLE,
        None,         # New environment
        workingDir,   # Current directory
        si            # startup info.
    )
    win32event.WaitForSingleObject(hProcess, win32event.INFINITE)



def MakeInstaller(isUpdate):
    from distutils.core import setup
    import py2exe

    os.chdir(tmpDir)
    
    templateOptions = GetVersion()
    VersionStr = templateOptions['version'] + '_build_' + str(templateOptions['buildNum'])
    templateOptions['VersionStr'] = VersionStr
    templateOptions["PYTHON_DIR"] = dirname(sys.executable)
    templateOptions["OUT_DIR"] = outDir
    templateOptions["TRUNK"] = trunkDir
    templateOptions["DIST"] = join(tmpDir, "dist")

    InstallPy2exePatch()
    setup(**py2exeOptions)
    
    if isUpdate:
        innoScriptPath = abspath("Update.iss")
        template = inno_update
        outFileBase = "EventGhost_%s_Update" % VersionStr
    else:
        innoScriptPath = abspath("Setup.iss")
        template = inno_script
        outFileBase = "EventGhost_%s_Setup" % VersionStr
        
    templateOptions["OUT_FILE_BASE"] = outFileBase
    
    fd = open(innoScriptPath, "w")
    fd.write(template % templateOptions)
    fd.close()
    
    ExecuteAndWait(GetInnoCompilePath(innoScriptPath))
    os.chdir(trunkDir)
    removedir(tmpDir)
    return join(outDir, outFileBase + ".exe")


def UploadFile(filename, url):
    from ftplib import FTP
    from urlparse import urlparse
    urlComponents = urlparse(url)
    
    dialog = wx.ProgressDialog(
        "Upload",
        "Uploading: %s" % filename,
        maximum=100.0,
        style = wx.PD_CAN_ABORT
            | wx.PD_APP_MODAL
            | wx.PD_ELAPSED_TIME
            | wx.PD_ESTIMATED_TIME
            | wx.PD_REMAINING_TIME
            | wx.PD_SMOOTH
    )

    class progress:
        def __init__(self, filepath):
            self.size = os.path.getsize(filepath)
            self.fd = open(filepath, "rb")
            self.pos = 0
            
        def read(self, size):
            self.pos += size
            keepGoing, skip = dialog.Update(min(100.0, self.pos * 100.0 / self.size))
            if not keepGoing:
                return None
            return self.fd.read(size)
        
        def close(self):
            self.fd.close()

    ftp = FTP(
        urlComponents.hostname, 
        urlComponents.username, 
        urlComponents.password
    )
    ftp.cwd(urlComponents.path)
    fd = progress(filename)
    ftp.storbinary("STOR " + basename(filename), fd)
    fd.close()
    dialog.Destroy()
    
    
    
class MainDialog(wx.Dialog):
    
    def __init__(self, url=""):
        
        wx.Dialog.__init__(self, None, title="Make EventGhost Installer")
        
        # create controls
        self.makeUpdateRadioBox = wx.RadioBox(
            self, 
            choices = ("Make Update", "Make Full Installer"),
            style = wx.RA_SPECIFY_ROWS
        )
        self.uploadCB = wx.CheckBox(self, -1, "Upload")
        if url:
            self.uploadCB.SetValue(True)
        else:
            self.uploadCB.Enable(False)
        self.url = url
        okButton = wx.Button(self, wx.ID_OK)
        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        cancelButton = wx.Button(self, wx.ID_CANCEL)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        # add controls to sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.makeUpdateRadioBox, 0, wx.ALL, 10)
        sizer.Add(self.uploadCB, 0, wx.ALL, 10)
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(okButton)
        btnSizer.AddButton(cancelButton)
        btnSizer.Realize()
        sizer.Add(btnSizer)
        
        # layout sizers
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        
        
    def OnOk(self, event):
        self.Show(False)
        isUpdate = self.makeUpdateRadioBox.GetSelection() == 0
        filename = MakeInstaller(isUpdate)
        if self.uploadCB.GetValue():
            UploadFile(filename, self.url)
        app.ExitMainLoop()
        
        
    def OnCancel(self, event):
        app.ExitMainLoop()
        

app = wx.App(0)
app.SetExitOnFrameDelete(False)
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    url = ""
else:
    url = sys.argv[1]
    sys.argv[1] = "py2exe"
mainDialog = MainDialog(url)
mainDialog.Show()
app.MainLoop()

