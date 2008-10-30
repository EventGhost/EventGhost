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
# $LastChangedDate: 2008-10-21 16:10:10 +0200 (Di, 21 Okt 2008) $
# $LastChangedRevision: 547 $
# $LastChangedBy: bitmonster $

import sys
import tempfile
import os
import subprocess
import _winreg
import shutil
import atexit
import zipfile
from os.path import basename, dirname, abspath, join, exists
from glob import glob

# third-party module imports
import pysvn
import py2exe

RT_MANIFEST = 24


class InnoInstaller(object): 
    sourceDir = ".."
    outputDir = "../.."
    libraryName = "lib%d%d" % sys.version_info[:2]
    appVersion = "0.0.0"
    SETUP_EXE_NAME_TEMPLATE = "%(APP_SHORT_NAME)s_%(appVersion)s_Setup"
    SOURCE_ZIP_NAME_TEMPLATE = "%(APP_SHORT_NAME)s_%(appVersion)s_Source"
    PYVERSION = str(sys.version_info[0]) + str(sys.version_info[1])
    bootScript = "Py2ExeBootScript.py"
    icon = None
    

    def __init__(self):
        self.tmpDir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, self.tmpDir)
        self.toolsDir = abspath(dirname(sys.argv[0]))
        self.sourceDir = abspath(self.sourceDir)
        self.outputDir = abspath(self.outputDir)
        self.libraryDir = abspath(join(self.sourceDir, self.libraryName))
        self.innoSections = {}
        self.pyVersionDir = abspath(u"Python%s" % self.PYVERSION)
        # Add our working dir to the import pathes
        sys.path.append(self.toolsDir)
        sys.path.append(self.pyVersionDir)
        #self.ROOT_FILES_TO_ADD = ["%s.exe" % self.APP_SHORT_NAME]
        if self.PYVERSION == "25":
            manifestTemplate = PY25_MANIFEST_TEMPLATE
        elif self.PYVERSION == "26":
            manifestTemplate = PY26_MANIFEST_TEMPLATE
        else:
            raise SystemError("Unknown Python version.")

        self.py2exeOptions = dict(
            options = dict(
                build = dict(build_base = join(self.tmpDir, "build")),
                py2exe = dict(
                    compressed = 0,
                    includes = [
                        "encodings",
                        "encodings.*",
                    ],
                    excludes = self.excludes,
                    dll_excludes = [
                        "DINPUT8.dll", 
                        "w9xpopen.exe", 
                        #"gdiplus.dll", 
                        #"msvcr71.dll",
                    ],
                    dist_dir = self.sourceDir,
                    custom_boot_script = abspath(self.bootScript),
                )
            ),
            # The lib directory contains everything except the executables and the 
            # python dll.
            zipfile = join(self.libraryName, "python%s.zip" % self.PYVERSION),
            windows = [
                dict(
                    script = abspath(self.mainScript),
                    icon_resources = [],
                    other_resources = [
                        (RT_MANIFEST, 1, manifestTemplate % self)
                    ],
                    dest_base = self.APP_SHORT_NAME
                ),
            ],
            # use out build_installer class as extended py2exe build command
            #cmdclass = {"py2exe": py2exe.run},
            verbose = 3,
        )
        if self.PYVERSION == "26":
            self.py2exeOptions["data_files"] = [
                (self.libraryName, [
                    join(self.pyVersionDir, "Microsoft.VC90.CRT.manifest")
                ])
            ]
        if self.icon:
            self.py2exeOptions["windows"][0]["icon_resources"].append(
                (1, abspath(self.icon))
            )
        #os.chdir(abspath(u"Python%s" % self.PYVERSION))

        
    def Add(self, section, line):
        if not section in self.innoSections:
            self.innoSections[section] = []
        self.innoSections[section].append(line)
        
    
    def AddFile(self, source, destDir=""):
        self.Add(
            "Files", 
            'Source: "%s"; DestDir: "{app}\\%s";' % (abspath(source), destDir)
        )
        
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    
    def GetSvnRevision(self):
        """
        Return the highest SVN revision in the working copy.
        """
        client = pysvn.Client()
        svnRevision = 0
        for status in client.status(self.sourceDir, ignore=True):
            if status.is_versioned:
                if status.entry.revision.number > svnRevision:
                    svnRevision = status.entry.revision.number
        return svnRevision
    
    
    def CommitSvn(self):
        """
        Commit all modified files in the working copy to the SVN server.
        """
        def ssl_server_trust_prompt(trust_dict):
            return True, 0, True
        svn = pysvn.Client()
        svn.callback_ssl_server_trust_prompt = ssl_server_trust_prompt
        svn.checkin([self.sourceDir], "Created installer for %s" % self.appVersion)
    

    def CreateSourceArchive(self):
        """
        Create a zip archive off all versioned files in the working copy.
        """
        outFile = join(self.outputDir, self.SOURCE_ZIP_NAME_TEMPLATE % self)
        client = pysvn.Client()
        workingDir = self.sourceDir
        zipFile = zipfile.ZipFile(outFile + ".zip", "w", zipfile.ZIP_DEFLATED)
        for status in client.status(workingDir, ignore=True):
            if status.is_versioned:
                path = status.path
                if not os.path.isdir(path):
                    arcname = path[len(workingDir) + 1:]
                    zipFile.write(str(path), str(arcname))
        zipFile.close()


    def InstallPy2exePatch(self):
        # ModuleFinder can't handle runtime changes to __path__, but win32com 
        # uses them, particularly for people who build from sources.  Hook 
        # this in.
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


    def CreateLibrary(self):
        """
        Create the library and .exe files with py2exe.
        """
        sys.argv.append("py2exe")
        from distutils.core import setup
        self.InstallPy2exePatch()
        if exists(self.libraryDir):
            shutil.rmtree(self.libraryDir)
        #setup(**consoleOptions)
        setup(**self.py2exeOptions)
        pythonDir = dirname(sys.executable)
        dllNames = [
            basename(name) for name in glob(join(self.libraryDir, "*.dll"))
        ]
        neededDlls = []
        for path, dirs, files in os.walk(pythonDir):
            for file in files:
                if file in dllNames:
                    neededDlls.append(file)
        for file in dllNames:
            if file not in neededDlls:
                os.remove(join(self.libraryDir, file))
                
#        for dll in self.ROOT_FILES_TO_ADD:
#            if not exists(join(self.sourceDir, dll)):
#                shutil.copy2(join(pythonDir, dll), self.sourceDir)
        
    
    def ExecuteInnoSetup(self):
        self.AddFile("../%s.exe" % self.APP_SHORT_NAME)
        if self.PYVERSION == "25":
            self.AddFile("../MFC71.dll")
            self.AddFile("../msvcr71.dll")
            self.AddFile("../msvcp71.dll")
            self.AddFile("../python25.dll")
        elif self.PYVERSION == "26":
            self.AddFile("../msvcr90.dll")
            self.AddFile("../msvcp90.dll")
            self.AddFile("../msvcm90.dll")
            self.AddFile("../python26.dll")
            self.AddFile("../Microsoft.VC90.CRT.manifest")
        innoScriptPath = join(self.tmpDir, "Setup.iss")
        issFile = open(innoScriptPath, "w")
        issFile.write(self.innoScriptTemplate % self)
        for section, lines in self.innoSections.iteritems():
            issFile.write("[%s]\n" % section)
            for line in lines:
                issFile.write("%s\n" % line)            
        issFile.close()

        key = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE, 
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 5_is1"
        )
        installPath, _ = _winreg.QueryValueEx(key, "InstallLocation")
        _winreg.CloseKey(key)
    
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE 
        errorcode = subprocess.call(
            (join(installPath, "ISCC.exe"), innoScriptPath), 
            stdout=sys.stdout.fileno(),
            startupinfo=si
        )
        if errorcode > 0:
            raise SystemError



# The manifest will be inserted as resource into the exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
PY25_MANIFEST_TEMPLATE = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity
        version="5.0.0.0"
        processorArchitecture="x86"
        name="%(APP_SHORT_NAME)s"
        type="win32"
    />
    <description>%(APP_SHORT_NAME)s Program</description>
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

PY26_MANIFEST_TEMPLATE = '''
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
</assembly>
'''

