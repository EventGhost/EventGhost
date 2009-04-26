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

import sys
import tempfile
import os
import _winreg
import shutil
import atexit
import zipfile
import builder
from builder.Utils import StartProcess, RemoveAllManifests

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
    libraryName = "lib%d%d" % sys.version_info[:2]
    appVersion = "0.0.0"
    bootScript = "Py2ExeBootScript.py"
    
    # must be set be subclass
    mainScript = None


    def __init__(self):
        self.tmpDir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, self.tmpDir)
        self.outputDir = abspath(join(builder.SOURCE_DIR, ".."))
        self.libraryDir = join(builder.SOURCE_DIR, self.libraryName)
        self.innoSections = {}
        # Add our working dir to the import pathes
        sys.path.append(join(builder.SOURCE_DIR, "tools"))
        sys.path.append(builder.PYVERSION_DIR)

        
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
            [builder.SOURCE_DIR], 
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
        svn.update(builder.SOURCE_DIR)
        
    
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
        workingDir = builder.SOURCE_DIR
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
        libraryDir = self.libraryDir
        if exists(libraryDir):
            for filename in os.listdir(libraryDir):
                path = join(libraryDir, filename)
                if not os.path.isdir(path):
                    os.remove(path)
                    
        manifest = file(
            join(builder.PYVERSION_DIR, "manifest.template")
        ).read() % self

        py2exeOptions = dict(
            options = dict(
                build = dict(build_base = join(self.tmpDir, "build")),
                py2exe = dict(
                    compressed = 0,
                    includes = [
                        "encodings",
                        "encodings.*",
                        "imports",
                    ],
                    excludes = builder.EXCLUDED_MODULES,
                    dll_excludes = [
                        "DINPUT8.dll", 
                        "w9xpopen.exe", 
                        #"gdiplus.dll", 
                        #"msvcr71.dll",
                    ],
                    dist_dir = builder.SOURCE_DIR,
                    custom_boot_script = join(builder.DATA_DIR, self.bootScript),
                )
            ),
            # The lib directory contains everything except the executables and
            # the python dll.
            zipfile = join(self.libraryName, "python%s.zip" % builder.PYVERSION_STR),
            windows = [
                dict(
                    script = join(builder.SOURCE_DIR, self.mainScript),
                    icon_resources = [],
                    other_resources = [(RT_MANIFEST, 1, manifest)],
                    dest_base = self.appShortName
                ),
            ],
            verbose = 0,
        )
        iconPath = join(builder.DATA_DIR, "Main.ico")
        if exists(iconPath):
            py2exeOptions["windows"][0]["icon_resources"].append((1, iconPath))
        #import pprint
        #pprint.pprint(self.py2exeOptions)
        setup(script_args=["py2exe"], **py2exeOptions)
        
        dllNames = [
            basename(name) for name in glob(join(libraryDir, "*.dll"))
        ]
        neededDlls = []
        for _, _, files in os.walk(dirname(sys.executable)):
            for filename in files:
                if filename in dllNames:
                    neededDlls.append(filename)
        for filename in dllNames:
            if filename not in neededDlls:
                os.remove(join(libraryDir, filename))
        if builder.PYVERSION_STR == "26":
            RemoveAllManifests(libraryDir)
    
    
    def ExecuteInnoSetup(self):
        """
        Finishes the setup, writes the Inno Setup script and calls the 
        Inno Setup compiler.
        """
        srcDir = builder.SOURCE_DIR
        if builder.PYVERSION_STR == "25":
            self.AddFile(join(srcDir, "MFC71.dll"))
            self.AddFile(join(srcDir, "msvcr71.dll"))
            self.AddFile(join(srcDir, "msvcp71.dll"))
            self.AddFile(join(srcDir, "python25.dll"))
        elif builder.PYVERSION_STR == "26":
            self.AddFile(join(srcDir, "msvcr90.dll"))
            self.AddFile(join(srcDir, "msvcp90.dll"))
            self.AddFile(join(srcDir, "msvcm90.dll"))
            self.AddFile(join(srcDir, "python26.dll"))
            self.AddFile(join(srcDir, "Microsoft.VC90.CRT.manifest"))
        innoScriptTemplate = file(
                join(builder.DATA_DIR, "InnoSetup.template"),
                "rt"
        ).read()
        innoScriptPath = join(self.tmpDir, "Setup.iss")
        issFile = open(innoScriptPath, "w")
        issFile.write(innoScriptTemplate % self)
        #print self.outputBaseFilename
        for section, lines in self.innoSections.iteritems():
            issFile.write("[%s]\n" % section)
            for line in lines:
                issFile.write("%s\n" % line)            
        issFile.close()

        StartProcess(GetInnoCompilerPath(), innoScriptPath, "/Q")

