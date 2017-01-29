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

import os
from os.path import join, splitext

# Local imports
import builder

PLUGINS = [
    "EventGhost",
    "System",
    "Window",
    "Mouse",
    "AtiRemoteWonder2",
    "Barco",
    "Conceptronic",
    "DBox2",
    "DesktopRemote",
    "DirectoryWatcher",
    "Fhz100Pc",
    "Conceptronic",
    "LogitechUltraX",
    "TechniSatUsb",
    "IgorPlugUSB",
    "Joystick",
    "Keyboard",
    "MediaPortal",
    "NetworkReceiver",
    "NetworkSender",
    "PowerDVD",
    "Serial",
    "Streamzap",
    "SysTrayMenu",
    "Task",
    "TechnoTrendIr",
    "TestPatterns",
    "Tira",
    "TVcentral",
    "UIR",
    "UIRT2",
    "USB-UIRT",
    "Webserver",
    "X10",
    "YARD",
    "ZoomPlayer",
]

HEADER = """# -*- coding: utf-8 -*-
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
"""

class CheckSourceCode(builder.Task):
    description = "Check source code"

    def Setup(self):
        if not self.buildSetup.showGui:
            self.activated = bool(self.buildSetup.args.check)

    def DoTask(self):
        sourceDir = self.buildSetup.sourceDir
        searchDirs = [
            join(sourceDir, "eg"),
            join(self.buildSetup.buildDir),
        ]
        for plugin in PLUGINS:
            searchDirs.append(join(sourceDir, "plugins", plugin))
        serialDir = join(sourceDir, "eg", "WinApi", "serial")

        for searchDir in searchDirs:
            for root, dirs, files in os.walk(searchDir):
                for filename in files:
                    if splitext(filename)[1].lower() in (".py", ".pyw"):
                        path = join(root, filename)
                        if path.startswith(serialDir):
                            continue
                        self.CheckHeader(path)
                        self.CheckLineLength(path)
                        # don't fix files that are versioned but haven't changed
                        # TODO: something equivalent in git? repo.status
                        # itemStatus = status[paths.index(path)]
                        # if itemStatus.text_status == pysvn.wc_status_kind.normal:
                        #     continue
                        self.FixTrailingWhitespace(path)

    def CheckHeader(self, path):
        """
        Checks if the source file has the right GPLv2 header.
        """
        sourceFile = open(path, "rt")
        header = sourceFile.read(len(HEADER))
        if header != HEADER:
            print "wrong file header:", path

    def CheckLineLength(self, path):
        """
        Checks if the source file doesn't exceed the line length.
        """
        sourceFile = open(path, "rt")
        for line in sourceFile.readlines():
            if len(line.rstrip()) > 79:
                print "line too long", path, line.rstrip()
                return

    def FixTrailingWhitespace(self, path):
        """
        Removes trailing whitespace from the source file.
        """
        sourceFile = open(path, "rt")
        oldContent = sourceFile.read()
        sourceFile.close()
        lines = [line.rstrip() for line in oldContent.splitlines()]
        while len(lines) and lines[-1].strip() == "":
            del lines[-1]
        lines.append("")
        lines.append("")
        newContent = "\n".join(lines)
        if oldContent != newContent:
            sourceFile = open(path, "wt")
            sourceFile.write(newContent)
            sourceFile.close()
