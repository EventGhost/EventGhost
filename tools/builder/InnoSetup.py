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
Routines to upload a file through FTP with a nice dialog.
"""

import sys
import tempfile
import os
import _winreg
import shutil
import atexit
import zipfile
import builder
from builder.Utils import StartProcess

from os.path import basename, dirname, abspath, join, exists
from glob import glob
import logging

class StdHandler(object):
    indent = 0
    
    def __init__(self, oldStream, logger):
        self.oldStream = oldStream
        self.buf = ""
        self.logger = logger
        
    def write(self, data):
        self.buf += data
        lines = self.buf.split("\n")
        for line in self.buf.split("\n")[:-1]:
            line = (self.indent * 4 * " ") + line.rstrip()
            self.logger(line)
            self.oldStream.write(line + "\n")
        self.buf = lines[-1]
        
        
    def flush(self):
        pass
    
        
LOG_FILENAME = 'Build.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)
logging.getLogger().setLevel(20)
sys.stdout = StdHandler(sys.stdout, logging.info)
sys.stderr = StdHandler(sys.stderr, logging.error)

def SetIndent(level):
    StdHandler.indent = level


RT_MANIFEST = 24

def GetInnoCompilerPath():
    try:
        key = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE, 
            (
                "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\"
                "Uninstall\\Inno Setup 5_is1"
            )
        )
        installPath = _winreg.QueryValueEx(key, "InstallLocation")[0]
        _winreg.CloseKey(key)
    except WindowsError:
        return None
    installPath = join(installPath, "ISCC.exe")
    if not exists(installPath):
        return None
    return installPath
        
    
def InstallPy2exePatch():
    """
    Tricks py2exe to include the win32com module.
    
    ModuleFinder can't handle runtime changes to __path__, but win32com 
    uses them, particularly for people who build from sources.
    """
    try:
        import modulefinder
        import win32com
        for path in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", path)
        for extra in ["win32com.shell"]:
            __import__(extra)
            module = sys.modules[extra]
            for path in module.__path__[1:]:
                modulefinder.AddPackagePath(extra, path)
    except ImportError: #IGNORE:W0704
        # no build path setup, no worries.
        pass 


class InnoInstaller(object): 
    """
    Helper class to create Inno Setup installers more easily.
    """
    appShortName = "Application"
    sourceDir = ".."
    outputDir = "../.."
    libraryName = "lib%d%d" % sys.version_info[:2]
    appVersion = "0.0.0"
    pyVersion = "%d%d" % sys.version_info[:2]
    bootScript = "Py2ExeBootScript.py"
    icon = None
    excludes = []
    
    # must be set be subclass
    mainScript = None
    innoScriptTemplate = None


    def __init__(self):
        self.tmpDir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, self.tmpDir)
        self.toolsDir = abspath(dirname(sys.argv[0]))
        self.sourceDir = abspath(self.sourceDir)
        self.outputDir = abspath(self.outputDir)
        self.libraryDir = abspath(join(self.sourceDir, self.libraryName))
        self.innoSections = {}
        self.pyVersionDir = builder.PYVERSION_DIR
        self.dataDir = builder.DATA_DIR
        # Add our working dir to the import pathes
        sys.path.append(self.toolsDir)
        sys.path.append(self.pyVersionDir)
        manifest = file(
            join(self.pyVersionDir, "manifest.template")
        ).read() % self

        self.py2exeOptions = dict(
            options = dict(
                build = dict(build_base = join(self.tmpDir, "build")),
                py2exe = dict(
                    compressed = 0,
                    includes = [
                        "encodings",
                        "encodings.*",
                        "imports",
                    ],
                    excludes = self.excludes,
                    dll_excludes = [
                        "DINPUT8.dll", 
                        "w9xpopen.exe", 
                        #"gdiplus.dll", 
                        #"msvcr71.dll",
                    ],
                    dist_dir = self.sourceDir,
                    custom_boot_script = join(builder.DATA_DIR, self.bootScript),
                )
            ),
            # The lib directory contains everything except the executables and
            # the python dll.
            zipfile = join(self.libraryName, "python%s.zip" % self.pyVersion),
            windows = [
                dict(
                    script = abspath(self.mainScript),
                    icon_resources = [],
                    other_resources = [
                        (RT_MANIFEST, 1, manifest)
                    ],
                    dest_base = self.appShortName
                ),
            ],
            verbose = 0,
        )
        if self.icon:
            self.py2exeOptions["windows"][0]["icon_resources"].append(
                (1, join(builder.DATA_DIR, self.icon))
            )

        
    def Add(self, section, line):
        """ 
        Adds a line to the INI section. 
        """
        if not section in self.innoSections:
            self.innoSections[section] = []
        self.innoSections[section].append(line)
        
    
    def AddFile(self, source, destDir="", destName=None):
        """ 
        Adds a file to the [Files] section. 
        """
        line = 'Source: "%s"; DestDir: "{app}\\%s";' % (abspath(source), destDir)
        if destName is not None:
            line += ' DestName: "%s";' % destName
        self.Add("Files", line)
        
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    
    def GetSvnRevision(self):
        """
        Return the highest SVN revision in the working copy.
        """
        import pysvn
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
        import pysvn
        
        def SslServerTrustPromptCallback(dummy):
            """ 
            See pysvn documentation for 
            pysvn.Client.callback_ssl_server_trust_prompt
            """
            return True, 0, True
        svn = pysvn.Client()
        svn.callback_ssl_server_trust_prompt = SslServerTrustPromptCallback
        svn.checkin(
            [self.sourceDir], 
            "Created installer for %s" % self.appVersion
        )
    

    def UpdateSvn(self):
        import pysvn
        
        def SslServerTrustPromptCallback(dummy):
            """ 
            See pysvn documentation for 
            pysvn.Client.callback_ssl_server_trust_prompt
            """
            return True, 0, True
        svn = pysvn.Client()
        svn.callback_ssl_server_trust_prompt = SslServerTrustPromptCallback
        svn.update(self.sourceDir)
        
    
    def CreateSourceArchive(self, filename=None):
        """
        Create a zip archive off all versioned files in the working copy.
        """
        import pysvn
        if filename is None:
            filename = join(
                self.outputDir, 
                "%(appShortName)s_%(appVersion)s_Source.zip" % self
            )
        client = pysvn.Client()
        workingDir = self.sourceDir
        zipFile = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
        for status in client.status(workingDir, ignore=True):
            if status.is_versioned:
                path = status.path
                if not os.path.isdir(path):
                    arcname = path[len(workingDir) + 1:]
                    zipFile.write(str(path), str(arcname))
        zipFile.close()


    def CreateLibrary(self):
        """
        Create the library and .exe files with py2exe.
        """
        from distutils.core import setup
        InstallPy2exePatch()
        import py2exe # pylint: disable-msg=W0612
                      # looks like py2exe import is unneeded, but it isn't
        if exists(self.libraryDir):
            for filename in os.listdir(self.libraryDir):
                path = join(self.libraryDir, filename)
                if not os.path.isdir(path):
                    os.remove(path)
        setup(script_args=["py2exe"], **self.py2exeOptions)
        pythonDir = dirname(sys.executable)
        dllNames = [
            basename(name) for name in glob(join(self.libraryDir, "*.dll"))
        ]
        neededDlls = []
        for _, _, files in os.walk(pythonDir):
            for filename in files:
                if filename in dllNames:
                    neededDlls.append(filename)
        for filename in dllNames:
            if filename not in neededDlls:
                os.remove(join(self.libraryDir, filename))
        if self.pyVersion == "26":
            self.RemoveAllManifests()
    
    
    def RemoveAllManifests(self):
        """ 
        Remove embedded manifest resource for all DLLs and PYDs. 
        
        These seems to be the only way how the setup can run with Python 2.6
        on Vista.
        """
        import ctypes
        
        BeginUpdateResource = ctypes.windll.kernel32.BeginUpdateResourceA
        UpdateResource = ctypes.windll.kernel32.UpdateResourceA
        EndUpdateResource = ctypes.windll.kernel32.EndUpdateResourceA
        
        for (dirpath, dirnames, filenames) in os.walk(self.libraryDir):
            if '.svn' in dirnames:
                dirnames.remove('.svn')
            for name in filenames:
                ext = os.path.splitext(name)[1].lower()
                if ext not in (".pyd", ".dll"):
                    continue
                path = os.path.join(dirpath, name)
                handle = BeginUpdateResource(path, 0)
                if handle == 0:
                    continue
                res = UpdateResource(handle, 24, 2, 1033, None, 0)
                if res:
                    EndUpdateResource(handle, 0)
    
    
    def ExecuteInnoSetup(self):
        """
        Finishes the setup, writes the Inno Setup script and calls the 
        Inno Setup compiler.
        """
        if self.pyVersion == "25":
            self.AddFile("../MFC71.dll")
            self.AddFile("../msvcr71.dll")
            self.AddFile("../msvcp71.dll")
            self.AddFile("../python25.dll")
        elif self.pyVersion == "26":
            self.AddFile("../msvcr90.dll")
            self.AddFile("../msvcp90.dll")
            self.AddFile("../msvcm90.dll")
            self.AddFile("../python26.dll")
            self.AddFile("../Microsoft.VC90.CRT.manifest")
        innoScriptPath = join(self.tmpDir, "Setup.iss")
        issFile = open(innoScriptPath, "w")
        issFile.write(self.innoScriptTemplate % self)
        #print self.outputBaseFilename
        for section, lines in self.innoSections.iteritems():
            issFile.write("[%s]\n" % section)
            for line in lines:
                issFile.write("%s\n" % line)            
        issFile.close()

        StartProcess(GetInnoCompilerPath(), innoScriptPath, "/Q")

