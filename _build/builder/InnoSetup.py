# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import _winreg
import os
# Local imports
from Utils import EncodePath, StartProcess

# Exceptions
class InnoSetupError(Exception):
    pass

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
        if section not in self.innoSections:
            self.innoSections[section] = []
        self.innoSections[section].append(EncodePath(line))

    def AddFile(self, source, destDir="", destName=None, ignoreversion=True, prefix="{app}"):
        """
        Adds a file to the [Files] section.
        """
        line = 'Source: "%s"; DestDir: "%s\\%s"' % (
            os.path.abspath(source), prefix, destDir
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

        template_dict = {}
        for key, value in self.buildSetup.__dict__.iteritems():
            if isinstance(value, unicode):
                value = EncodePath(value)

            template_dict[key] = value

        template_path = os.path.join(
            self.buildSetup.dataDir,
            "InnoSetup.template"
        )
        script_path = os.path.join(self.buildSetup.tmpDir, "Setup.iss")

        with open(template_path, "rt") as f:
            script_template = f.read()

        with open(script_path, "w") as iss_file:
            iss_file.write('# define ARCH "{0}"\n\n'.format(self.buildSetup.arch))
            iss_file.write(script_template % template_dict)

            for section, lines in self.innoSections.iteritems():
                iss_file.write("[%s]\n" % section)

                for line in lines:
                    iss_file.write("%s\n" % line)

        if not (StartProcess(GetInnoCompilerPath(), script_path) == 0):
            raise InnoSetupError


def GetInnoCompilerPath():
    try:
        key = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            (
                "SOFTWARE\\\Classes\\\InnoSetupScriptFile\\"
                "shell\\Compile\\command"
            )
        )
        install_path = _winreg.QueryValueEx(key, "")[0]
        _winreg.CloseKey(key)
    except WindowsError:
        return None

    install_path = os.path.dirname(install_path[1:].split('"')[0])
    install_path = os.path.join(install_path, "ISCC.exe")
    if not os.path.exists(install_path):
        return None

    return install_path
