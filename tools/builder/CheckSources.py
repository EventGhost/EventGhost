# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
from os.path import join, splitext
import builder

HEADER = """# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

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
]


class CheckSources(builder.Task):
    description = "Check source files"

    def DoTask(self):
        sourceDir = self.buildSetup.sourceDir
        searchDirs = [
            join(sourceDir, "eg"),
            join(sourceDir, "tools"),
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
                        self.FixTrailingWhitespace(path)
                        self.CheckHeader(path)
                        self.CheckLineLength(path)


    def FixTrailingWhitespace(self, path):
        """
        Removes trailing whitespace from the source file.
        """
        infile = open(path, "rt")
        oldContent = infile.read()
        infile.close()
        lines = [line.rstrip() for line in oldContent.splitlines()]
        while lines[-1].strip() == "":
            del lines[-1]
        lines.append("")
        lines.append("")
        newContent = "\n".join(lines)
        if oldContent != newContent:
            outfile = open(path, "wt")
            outfile.write(newContent)
            outfile.close()


    def CheckHeader(self, path):
        """
        Checks if the source file has the right GPLv2 header.
        """
        fd = open(path, "rt")
        header = fd.read(len(HEADER))
        if header != HEADER:
            print "wrong file header:", path


    def CheckLineLength(self, path):
        """
        Checks if the source file doesn't exceed the line length.
        """
        fd = open(path, "rt")
        for line in fd.readlines():
            if len(line.rstrip()) > 79:
                print "line to long", path, line.rstrip()
                return

