import wx
import sys
from os.path import basename, dirname, abspath, join
import tempfile

sourceFiles = (
    "eg/*.py",
    "eg/*.pyd",
    "eg/*.png",
    "images/*.png",
    "images/*.ico",
    "languages/*.py",
    "plugins/*.py",
    "plugins/*.png",
)
    
class OptionsDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Make EventGhost Installer")
        
        # create controls
        self.makeUpdateRadioBox = wx.RadioBox(
            self, 
            choices = ("Make Update", "Make Full Installer"),
            style = wx.RA_SPECIFY_ROWS
        )
        self.uploadCB = wx.CheckBox(self, -1, "Upload")
        okButton = wx.Button(self, wx.ID_OK)
        cancelButton = wx.Button(self, wx.ID_CANCEL)
        
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

app = wx.PySimpleApp()
dialog = OptionsDialog()
if dialog.ShowModal() == wx.ID_CANCEL:
    sys.exit(0)

make_update = dialog.makeUpdateRadioBox.GetSelection() == 0
upload = dialog.uploadCB.GetValue()

tmpDir = tempfile.mkdtemp()
tmpSourceDir = join(tmpDir, "source")

#make_update = False
#make_update = True
#
#upload = False
#upload = True
#

import os
import re
import fnmatch
import shutil
import time

DLL_DIR = dirname(sys.executable)

def GetVersion():
    data = {}
    execfile("eg/Version.py", data, data)
    data['buildNum'] += 1
    data['compileTime'] = time.time()
    fd = file("eg/version.py", "wt")
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
            os.remove(join(root, name))
        for name in dirs:
            os.rmdir(join(root, name))
    os.rmdir(path)


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

main_dir = abspath(join(dirname(sys.argv[0]), ".."))
os.chdir(main_dir)

bases = ("eg", "plugins", "Languages")
for base in ("eg", "plugins", "Languages"):
    for filename in locate("*.py", base):
        #print filename
        data = open(filename, "rb").read()
        if '\0' in data:
            print "Binary!", filename
            continue
        newdata = re.sub("\r?\n", "\r\n", data)
        if newdata != data:
            f = open(filename, "wb")
            f.write(newdata)
            f.close()

version_dict = GetVersion()
VersionStr = version_dict['version'] + '_build_' + str(version_dict['buildNum'])
version_dict['VersionStr'] = VersionStr
version_dict['DLL_DIR'] = DLL_DIR


for pattern in ("*.py", "*.pyd", "*.png", "*.txt"):
    xcopy("eg", join(tmpDir, "source\\eg"), pattern)
for pattern in ("*.png", "*.ico", "*.gif"):
    xcopy("images", join(tmpDir, "source\\images"), pattern)
for pattern in ("*.py", "*.pyd", "*.png", "*.gif", "*.jpg"):
    xcopy("plugins", join(tmpDir, "source\\plugins"), pattern)
    
# remove DLLs already in the full installer
#if make_update:
#    os.remove("tmp/source/plugins/MceRemote/MceIr.dll")
#    os.remove("tmp/source/plugins/Streamzap/irdata.dll")
#    os.remove("tmp/source/plugins/Tira/Tira2.dll")
#

xcopy("Languages", join(tmpSourceDir, "languages"), "*.py")

for dir in os.listdir(join(tmpSourceDir, "plugins")):
    if dir[:1] == "_":
        removedir(join(tmpSourceDir, "plugins", dir))

copy("EventGhost.pyw", tmpSourceDir)
copy("EventGhost.ico", tmpSourceDir)
copy("LICENSE.TXT", tmpSourceDir)
copy("Example.xml", tmpSourceDir)

archive = zipfile.ZipFile("EventGhost_%s_Source.zip" % VersionStr, "w", zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(tmpSourceDir):
    print root, dirs, files
    destdir = root[len(tmpSourceDir) + 1:]
    for file in files:
        archive.write(join(destdir, file))

xcopy("plugins", join(tmpSourceDir, "plugins"), "*.dll")
    
# remove DLLs already in the full installer
if make_update:
    os.remove(join(tmpSourceDir, "plugins/MceRemote/MceIr.dll"))
    os.remove(join(tmpSourceDir, "plugins/Streamzap/irdata.dll"))
    os.remove(join(tmpSourceDir, "plugins/Tira/Tira2.dll"))

#import compileall
#compileall.compile_dir("tmp\\source\\eg", force=True)

#os.chdir(os.path.join(main_dir, 'tmp\\source\\plugins'))
#list = os.listdir('.')
#for item in list:
#    if os.path.isdir(item) and (item[0] != "_"):
#        file = zipfile.PyZipFile(item + '.egp', 'w', zipfile.ZIP_STORED)
#        file.writepy(item)
#        if os.path.exists(item + "\\icon.png"):
#            file.write(item + "\\icon.png", 'icon.png')
#        file.close()

os.chdir(join(main_dir, tmpSourceDir))

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


from distutils.core import setup
import py2exe

if len(sys.argv) == 1:
    sys.argv.append("py2exe")

# ModuleFinder can't handle runtime changes to __path__, but win32com uses them,
# particularly for people who build from sources.  Hook this in.
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


setup(
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
    data_files = [
        (
            "",
            [
                "Example.xml",
                "LICENSE.TXT"
            ]
        ),
        #("plugins", GetDir("plugins\\", ".egp")),
        #("images", GetDir("images\\")),
    ],
    windows = [
        dict(
            script = "EventGhost.pyw",
            icon_resources = [(1, "EventGhost.ico")],
            other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog=shortpgm))],
            dest_base = shortpgm
        )
    ],
    # use out build_installer class as extended py2exe build command
    #cmdclass = {"py2exe": py2exe.run},
)

os.chdir(tmpDir)

xcopy("source\\eg", "dist\\eg", "*.pyc")

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
OutputDir=..\.
OutputBaseFilename=EventGhost_%(version)s_build_%(buildNum)s_Setup
LicenseFile=dist\license.txt
DisableReadyPage=yes
AppMutex=EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B

[InstallDelete]
Type: filesandordirs; Name: "{app}\eg"

[Files]
Source: "dist\*.*"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\lib\*.*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs
Source: "source\images\*.*"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs
Source: "source\plugins\*.*"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs
Source: "source\eg\*.*"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs
Source: "source\Languages\*.*"; DestDir: "{app}\Languages"; Flags: ignoreversion recursesubdirs
Source: "dist\Example.xml"; DestDir: "{userappdata}\EventGhost"; DestName: "MyConfig.xml"; Flags: onlyifdoesntexist uninsneveruninstall
Source: "..\MFC71.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(DLL_DIR)s\msvcr71.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "%(DLL_DIR)s\msvcp71.dll"; DestDir: "{app}"; Flags: ignoreversion

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
OutputDir=..\.
OutputBaseFilename=EventGhost_%(version)s_build_%(buildNum)s_Update
;DisableFinishedPage=yes
DisableReadyPage=yes
CreateUninstallRegKey=no
UpdateUninstallLogAppName=no
AppMutex=EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B
;WizardImageFile=C:\EventGhost\logo.bmp
;WizardImageStretch=no
;WizardImageBackColor=$FFFFFF

[Run]
Filename: "{app}\EventGhost.exe"; Parameters: "-install"

[Run] 
Filename: "{app}\EventGhost.exe"; Flags: postinstall nowait skipifsilent 

[InstallDelete]
Type: filesandordirs; Name: "{app}\eg"

[Files]
Source: "source\EventGhost.pyw"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\EventGhost.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "source\images\*.png"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs
Source: "source\images\*.ico"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs
Source: "source\plugins\*.*"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs
Source: "source\eg\*.*"; DestDir: "{app}\eg"; Flags: ignoreversion recursesubdirs
Source: "source\Languages\*.*"; DestDir: "{app}\Languages"; Flags: ignoreversion recursesubdirs
Source: "source\Example.xml"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Example.xml"; DestDir: "{userappdata}\EventGhost"; DestName: "MyConfig.xml"; Flags: onlyifdoesntexist uninsneveruninstall
"""

if make_update:
    pathname = "Update.iss"
    ofi = open(pathname, "w")
    ofi.write(inno_update % version_dict)
    ofi.close()
else:
    pathname = "Setup.iss"
    ofi = open(pathname, "w")
    ofi.write(inno_script % version_dict)
    ofi.close()


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
    
    
import win32api
import win32event
from win32con import *
from win32process import *


def ExecuteAndWait(commandLine, workingDir=None):
    if workingDir is None:
        workingDir = dirname(abspath(pathname))
    si = STARTUPINFO()
    si.dwFlags = STARTF_USESHOWWINDOW
    si.wShowWindow = SW_SHOWNORMAL
    hProcess, _, _, _ = CreateProcess(
        None,         # AppName
        commandLine,  # Command line
        None,         # Process Security
        None,         # ThreadSecurity
        0,            # Inherit Handles?
        NORMAL_PRIORITY_CLASS|CREATE_NEW_CONSOLE,
        None,         # New environment
        workingDir,   # Current directory
        si            # startup info.
    )
    win32event.WaitForSingleObject(hProcess, win32event.INFINITE)


pathname = abspath(pathname)
ExecuteAndWait(GetInnoCompilePath(pathname))

if upload:
    home_dir = abspath(dirname(sys.argv[0]))
    os.chdir(home_dir)
    execfile("_upload.py")
