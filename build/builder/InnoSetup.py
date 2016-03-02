# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import _winreg
from os.path import abspath, join, exists
from builder.Utils import StartProcess, EncodePath

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

    def __init__(self, buildSetup):
        self.innoSections = {}
        self.buildSetup = buildSetup


    def Add(self, section, line):
        """
        Adds a line to the INI section.
        """
        if not section in self.innoSections:
            self.innoSections[section] = []
        self.innoSections[section].append(EncodePath(line))


    def AddFile(self, source, destDir="", destName=None, ignoreversion=True):
        """
        Adds a file to the [Files] section.
        """
        line = 'Source: "%s"; DestDir: "{app}\\%s"' % (
            abspath(source), destDir
        )
        if destName is not None:
            line += '; DestName: "%s"' % destName
        if ignoreversion:
            line += '; Flags: ignoreversion'
        self.Add("Files", line)


    def ExecuteInnoSetup(self):
        """
        Finishes the setup, writes the Inno Setup script and calls the
        Inno Setup compiler.
        """
        srcDir = self.buildSetup.sourceDir
        if self.buildSetup.pyVersionStr == "25":
            self.AddFile(join(srcDir, "MFC71.dll"))
            self.AddFile(join(srcDir, "msvcr71.dll"))
            self.AddFile(join(srcDir, "msvcp71.dll"))
            self.AddFile(join(srcDir, "python25.dll"))
        elif self.buildSetup.pyVersionStr in ["26", "27"]:
            self.AddFile(join(srcDir, "msvcr90.dll"))
            self.AddFile(join(srcDir, "msvcp90.dll"))
            self.AddFile(join(srcDir, "msvcm90.dll"))
            self.AddFile(join(srcDir,
                        "python{0}.dll".format(self.buildSetup.pyVersionStr)))
            self.AddFile(join(srcDir, "Microsoft.VC90.CRT.manifest"))
        innoScriptTemplate = file(
                join(self.buildSetup.dataDir, "InnoSetup.template"),
                "rt"
        ).read()
        innoScriptPath = join(self.buildSetup.tmpDir, "Setup.iss")
        issFile = open(innoScriptPath, "w")
        templateDict = {}
        for key, value in  self.buildSetup.__dict__.iteritems():
            if isinstance(value, unicode):
                value = EncodePath(value)
            templateDict[key] = value

        issFile.write(innoScriptTemplate % templateDict)
        for section, lines in self.innoSections.iteritems():
            issFile.write("[%s]\n" % section)
            for line in lines:
                issFile.write("%s\n" % line)
        issFile.close()

        StartProcess(GetInnoCompilerPath(), innoScriptPath, "/Q")

