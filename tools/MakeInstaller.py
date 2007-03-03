# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import wx
import sys
import tempfile
import os
import re
import fnmatch
import time
import zipfile
import subprocess
import win32process
import win32con
import _winreg
from ftplib import FTP
from urlparse import urlparse
from shutil import copy2 as copy
from os.path import basename, dirname, abspath, join, exists


SUBWCREV_PATH = r"\Programme\TortoiseSVN\bin\SubWCRev.exe"

tmpDir = tempfile.mkdtemp()
toolsDir = abspath(dirname(sys.argv[0]))
trunkDir = abspath(join(toolsDir, ".."))
outDir = abspath(join(trunkDir, "..", ".."))

SourcePattern = (
    "*.py", 
    "*.pyw", 
    "*.pyd", 
    "*.txt", 
    "*.png", 
    "*.jpg", 
    "*.gif", 
    "*.xml", 
    "*.ico",
)

def GetSourceFiles():
    sources = [
        join(trunkDir, "EventGhost.pyw"),
        join(trunkDir, "EventGhost.ico"),
        join(trunkDir, "Example.xml"),
        join(trunkDir, "LICENSE.TXT"),
    ]
    for directory in ("eg", "plugins", "languages", "images"):
        sources += locate(SourcePattern, join(trunkDir, directory))
    return sources


def UpdateVersionFile(svnRevision):
    data = {}
    versionFilePath = join(trunkDir, "eg/Version.py")
    execfile(versionFilePath, data, data)
    data['buildNum'] += 1
    data['compileTime'] = time.time()
    fd = file(versionFilePath, "wt")
    fd.write("version = " + repr(data['version']) + "\n")
    fd.write("buildNum = " + repr(data['buildNum']) + "\n")
    fd.write("compileTime = " + repr(data['compileTime']) + "\n")
    fd.write("svnRevision = " + repr(svnRevision))
    fd.close()        return data
    
    
def locate(patterns, root=os.curdir):
    '''
    Locate all files matching supplied filename patterns in and below
    supplied root directory.
    '''
    for path, dirs, files in os.walk(root):
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


def GetDir(theDir, extension=None):
    list = os.listdir(theDir)
    x2 = []
    for x in list:
        if extension:
            if os.path.splitext(x)[1] != extension:
                continue
        x2.append(theDir + x)
    return x2

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
            dll_excludes = [
                "DINPUT8.dll", 
                "w9xpopen.exe", 
                "gdiplus.dll", 
                "msvcr71.dll"
            ],
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
            other_resources = [
                (RT_MANIFEST, 1, manifest_template % dict(prog=shortpgm))
            ],
            dest_base = shortpgm
        )
    ],
    # use out build_installer class as extended py2exe build command
    #cmdclass = {"py2exe": py2exe.run},
    verbose = 0,
)


inno_script = """
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
LicenseFile=%(TOOLS_DIR)s\LICENSE.RTF
DisableReadyPage=yes
AppMutex=EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B

[InstallDelete]
Type: filesandordirs; Name: "{app}\eg"
%(INSTALL_DELETE)s

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


def CompileInnoScript(innoScriptPath):
    """
    Return command line to compile the Inno Script File
    """
    key = _winreg.OpenKey(
        _winreg.HKEY_LOCAL_MACHINE, 
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 5_is1"
    )
    installPath, _ = _winreg.QueryValueEx(key, "InstallLocation")
    _winreg.CloseKey(key)
    Execute(join(installPath, "ISCC.exe"), innoScriptPath)
    
    
def GetSvnVersion():
    template = (
        "Revision = $WCREV$\n"
        "Modified = $WCMODS?True:False$\n"
        "Date     = '$WCDATE$'\n"
        "RevRange = '$WCRANGE$'\n"
        "Mixed    = $WCMIXED?True:False$\n"
        "URL      = '$WCURL$'\n"
    )
    fd, templatePath = tempfile.mkstemp(text=True)
    fd = os.fdopen(fd, "wt")
    fd.write(template)
    fd.close()
    fd, resultPath = tempfile.mkstemp(text=True)
    os.close(fd)
    Execute(SUBWCREV_PATH, trunkDir, templatePath, resultPath)
    data = {}
    execfile(resultPath, {}, data)
    os.remove(templatePath)
    os.remove(resultPath)
    return data['Revision']
    

def Execute(*args):
    si = subprocess.STARTUPINFO()
    si.dwFlags = subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE 
    subprocess.call(
        args, 
        stdout=sys.stdout.fileno(),
        startupinfo=si
    )


def MakeSourceArchive(sourcePath, filepath):
    archive = zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED)
    headerLength = len(sourcePath)
    for filename in GetSourceFiles():
        arcname = filename[headerLength + 1:]
        archive.write(filename, arcname)
    archive.close()


def MakeInstaller(isUpdate):
    from distutils.core import setup
    import py2exe

    templateOptions = UpdateVersionFile(GetSvnVersion())
    VersionStr = templateOptions['version'] + '_build_' + str(templateOptions['buildNum'])
    templateOptions['VersionStr'] = VersionStr
    templateOptions["PYTHON_DIR"] = dirname(sys.executable)
    templateOptions["OUT_DIR"] = outDir
    templateOptions["TRUNK"] = trunkDir
    templateOptions["TOOLS_DIR"] = toolsDir
    templateOptions["DIST"] = join(tmpDir, "dist")
    
    installDeleteDirs = []
    for item in os.listdir(join(trunkDir, "plugins")):
        if item.startswith("."):
            continue
        path = join(trunkDir, "plugins", item)
        if os.path.isdir(path):
            installDeleteDirs.append('Type: filesandordirs; Name: "{app}\plugins\%s"' % item)
    installDelete = "\n".join(installDeleteDirs)
    templateOptions["INSTALL_DELETE"] = installDelete
    
    print "Creating source ZIP file"
    MakeSourceArchive(
        trunkDir, 
        join(outDir, "EventGhost_%s_Source.zip" % VersionStr)
    )
        
    InstallPy2exePatch()
    setup(**py2exeOptions)
    
    if isUpdate:
        innoScriptPath = abspath(join(tmpDir, "Update.iss"))
        template = inno_update
        outFileBase = "EventGhost_%s_Update" % VersionStr
    else:
        innoScriptPath = abspath(join(tmpDir, "Setup.iss"))
        template = inno_script
        outFileBase = "EventGhost_%s_Setup" % VersionStr
        
    templateOptions["OUT_FILE_BASE"] = outFileBase
    
    fd = open(innoScriptPath, "w")
    fd.write(template % templateOptions)
    fd.close()
    
    print "Calling Inno Setup Compiler"
    CompileInnoScript(innoScriptPath)
    print "Building installer done!"
    RemoveDirectory(tmpDir)
    return join(outDir, outFileBase + ".exe")


def UploadFile(filename, url):
    
    class progress:
        def __init__(self, filepath):
            self.size = os.path.getsize(filepath)
            self.fd = open(filepath, "rb")
            self.pos = 0
            self.dialog = wx.ProgressDialog(
                "Upload",
                "Uploading: %s" % filename,
                maximum=self.size+1,
                style = wx.PD_CAN_ABORT
                    | wx.PD_APP_MODAL
                    | wx.PD_ELAPSED_TIME
                    | wx.PD_ESTIMATED_TIME
                    | wx.PD_REMAINING_TIME
                    | wx.PD_SMOOTH
            )
            
        def read(self, size):
            keepGoing, skip = self.dialog.Update(min(self.size, self.pos))
            self.pos += size
            if not keepGoing:
                return None
            return self.fd.read(size)
        
        def close(self):
            self.fd.close()

    urlComponents = urlparse(url)
    fd = progress(filename)
    ftp = FTP(
        urlComponents.hostname, 
        urlComponents.username, 
        urlComponents.password
    )
    ftp.cwd(urlComponents.path)
    try:
        fileList = ftp.nlst()
    except:
        fileList = []
    for i in range(0, 999999):
        tempFileName = "tmp%06d" % i
        if tempFileName not in fileList:
            break
    ftp.storbinary("STOR " + tempFileName, fd)
    ftp.rename(tempFileName, basename(filename))
    ftp.quit()
    fd.close()
    print "Upload done!"
    fd.dialog.Destroy()
    


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
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(okButton)
        btnSizer.AddButton(cancelButton)
        btnSizer.Realize()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.makeUpdateRadioBox, 0, wx.ALL, 10)
        sizer.Add(self.uploadCB, 0, wx.ALL, 10)
        sizer.Add(btnSizer)

        self.SetSizerAndFit(sizer)
        
        
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

