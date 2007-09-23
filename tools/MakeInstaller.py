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
import locale
from ftplib import FTP
from urlparse import urlparse
from shutil import copy2 as copy
from os.path import basename, dirname, abspath, join, exists
import pysvn

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
    ]
    return GetFiles(files, SourcePattern)


def GetUpdateFiles():
    files = [
        "Example.xml",
        "LICENSE.TXT",
    ]
    return GetFiles(files, SourcePattern)
    

def GetSetupFiles():
    files = [
        "Example.xml",
        "LICENSE.TXT",
    ]
    return GetFiles(files, SourcePattern + ["*.dll"])
    

def UpdateVersionFile(commitSvn):
    data = {}
    versionFilePath = join(trunkDir, "eg", "Version.py")
    execfile(versionFilePath, data, data)
    data['buildNum'] += 1
    data['compileTime'] = time.time()
    fd = file(versionFilePath, "wt")
    fd.write("version = " + repr(data['version']) + "\n")
    fd.write("buildNum = " + repr(data['buildNum']) + "\n")
    fd.write("compileTime = " + repr(data['compileTime']) + "\n")
    fd.write("svnRevision = int('$LastChangedRevision$'.split()[1])")
    fd.close()    
    if commitSvn:
        svn = pysvn.Client()
        svn.checkin([trunkDir], "Created installer for %s.%i" % (data['version'], data['buildNum']))    return data
    
    
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
                    or exists(join(path, dir, "noinclude"))
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
            dist_dir = trunkDir,
            custom_boot_script=join(trunkDir, "eg", "Py2ExeBootScript.py")
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
Source: "%(TRUNK)s\*.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(TRUNK)s\*.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(TRUNK)s\lib\*.*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs
%(INSTALL_FILES)s
Source: "%(TRUNK)s\Example.xml"; DestDir: "{userappdata}\EventGhost"; DestName: "MyConfig.xml"; Flags: onlyifdoesntexist uninsneveruninstall

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
;Source: "%(TRUNK)s\plugins\TechnoTrendIr\TTUSBIR.dll"; DestDir: "{app}\plugins\TechnoTrendIr"; Flags: ignoreversion
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
    
        

def Execute(*args):
    si = subprocess.STARTUPINFO()
    si.dwFlags = subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE 
    subprocess.call(
        args, 
        stdout=sys.stdout.fileno(),
        startupinfo=si
    )


def MakeSourceArchive(outFile):
    archive = zipfile.ZipFile(outFile, "w", zipfile.ZIP_DEFLATED)
    for filename in GetSourceFiles():
        archive.write(join(trunkDir, filename), filename)
    archive.close()


def MakeInstaller(isUpdate, makeLib, makeSourceArchive, commitSvn):
    templateOptions = UpdateVersionFile(commitSvn)
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
        if os.path.isdir(join(trunkDir, "plugins", item)):
            installDeleteDirs.append(
                'Type: filesandordirs; Name: "{app}\plugins\%s"' % item
            )
    installDelete = "\n".join(installDeleteDirs)
    templateOptions["INSTALL_DELETE"] = installDelete
    
    if makeSourceArchive:
        print "Creating source ZIP file"
        MakeSourceArchive(join(outDir, "EventGhost_%s_Source.zip" % VersionStr))
        
    if makeLib:
        RemoveDirectory(join(trunkDir, "lib"))
        from distutils.core import setup
        import py2exe
        InstallPy2exePatch()
        setup(**py2exeOptions)
        pythonDir = dirname(sys.executable)
        copy(join(pythonDir, "MFC71.dll"), trunkDir)
        copy(join(pythonDir, "msvcr71.dll"), trunkDir)
        copy(join(pythonDir, "msvcp71.dll"), trunkDir)
    
    installFiles = []
    if isUpdate:
        for file in GetUpdateFiles():
            installFiles.append(
                'Source: "' + join(trunkDir, file) + '"; DestDir: "{app}\\' + dirname(file) + '"; Flags: ignoreversion'
            )
        innoScriptPath = abspath(join(tmpDir, "Update.iss"))
        template = inno_update
        outFileBase = "EventGhost_%s_Update" % VersionStr
    else:
        for file in GetSetupFiles():
            installFiles.append(
                'Source: "' + join(trunkDir, file) + '"; DestDir: "{app}\\' + dirname(file) + '"; Flags: ignoreversion'
            )
        innoScriptPath = abspath(join(tmpDir, "Setup.iss"))
        template = inno_script
        outFileBase = "EventGhost_%s_Setup" % VersionStr
        
    templateOptions["INSTALL_FILES"] = "\n".join(installFiles)  
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
    aborted = False
    class progress:
        def __init__(self, filepath):
            self.size = os.path.getsize(filepath)
            self.fd = open(filepath, "rb")
            self.pos = 0
            
        def read(self, size):
            print self.pos, int(round(100.0 * self.pos / self.size))
            self.pos += size
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
    if aborted:
        ftp.delete(tempFileName)
    else:
        ftp.rename(tempFileName, basename(filename))
    ftp.quit()
    fd.close()
    print "Upload done!"
    


class MainDialog(wx.Dialog):
    
    def __init__(self, url=""):
        
        wx.Dialog.__init__(self, None, title="Make EventGhost Installer")
        
        # create controls
        self.createSourceCB = wx.CheckBox(self, -1, "Create Source Archive")
        self.createImportsCB = wx.CheckBox(self, -1, "Create Imports")
        self.createLib = wx.CheckBox(self, -1, "Create Lib")
        self.uploadCB = wx.CheckBox(self, -1, "Upload")
        self.uploadCB.SetValue(bool(url))
        self.commitCB = wx.CheckBox(self, -1, "SVN Commit")
        self.commitCB.SetValue(True)
        self.makeUpdateRadioBox = wx.RadioBox(
            self, 
            choices = ("Make Update", "Make Full Installer"),
            style = wx.RA_SPECIFY_ROWS
        )
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
        sizer.Add(self.createSourceCB, 0, wx.ALL, 10)
        sizer.Add(self.createImportsCB, 0, wx.ALL, 10)
        sizer.Add(self.createLib, 0, wx.ALL, 10)
        sizer.Add(self.uploadCB, 0, wx.ALL, 10)
        sizer.Add(self.commitCB, 0, wx.ALL, 10)
        sizer.Add(self.makeUpdateRadioBox, 0, wx.ALL, 10)
        sizer.Add(btnSizer)

        self.SetSizerAndFit(sizer)
        
        
    def OnOk(self, event):
        self.Show(False)
        if self.createImportsCB.GetValue():
            import MakeImports
        isUpdate = self.makeUpdateRadioBox.GetSelection() == 0
        makeLib = self.createLib.GetValue()
        makeSourceArchive = self.createSourceCB.GetValue()
        commitSvn = self.commitCB.GetValue()
        filename = MakeInstaller(isUpdate, makeLib, makeSourceArchive, commitSvn)
        if self.uploadCB.GetValue():
            UploadFile(filename, self.url)
        app.ExitMainLoop()
        
        
    def OnCancel(self, event):
        app.ExitMainLoop()
     
print vars(pysvn.Client().info(trunkDir))
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

