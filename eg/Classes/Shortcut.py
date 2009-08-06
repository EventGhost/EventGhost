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

import pythoncom
from win32com.shell import shell


class Shortcut:

    @classmethod
    def Create(
        cls,
        path,
        target,
        arguments="",
        startIn="",
        icon=("", 0),
        description=""
    ):
        """Create a Windows shortcut:

        path - As what file should the shortcut be created?
        target - What command should the desktop use?
        arguments - What arguments should be supplied to the command?
        startIn - What folder should the command start in?
        icon - (filename, index) What icon should be used for the shortcut?
        description - What description should the shortcut be given?

        eg
        Shortcut.Create(
            path=os.path.join (desktop (), "PythonI.lnk"),
            target=r"c:\python\python.exe",
            icon=(r"c:\python\python.exe", 0),
            description="Python Interpreter"
        )
        """
        sh = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
        )
        sh.SetPath(target)
        sh.SetDescription(description)
        sh.SetArguments(arguments)
        sh.SetWorkingDirectory(startIn)
        sh.SetIconLocation(icon[0], icon[1])
        persist = sh.QueryInterface(pythoncom.IID_IPersistFile)
        persist.Save(path, 1)


    @classmethod
    def Get(cls, filename):
        sh = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
        )
        persist = sh.QueryInterface(pythoncom.IID_IPersistFile).Load(filename)
        self = cls()
        self.path = filename
        self.target = sh.GetPath(shell.SLGP_SHORTPATH)[0]
        self.description = sh.GetDescription()
        self.arguments = sh.GetArguments()
        self.startIn = sh.GetWorkingDirectory()
        self.icons = sh.GetIconLocation()
        return self

