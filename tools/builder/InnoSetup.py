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
import _winreg
from os.path import abspath, join, exists

import builder
from builder.Utils import StartProcess

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
        
    
class InnoInstaller(object): 
    """
    Helper class to create Inno Setup installers more easily.
    """

    def __init__(self):
        self.innoSections = {}

        
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
        innoScriptPath = join(builder.TMP_DIR, "Setup.iss")
        issFile = open(innoScriptPath, "w")
        issFile.write(innoScriptTemplate % builder.__dict__)
        for section, lines in self.innoSections.iteritems():
            issFile.write("[%s]\n" % section)
            for line in lines:
                issFile.write("%s\n" % line)            
        issFile.close()

        StartProcess(GetInnoCompilerPath(), innoScriptPath, "/Q")

