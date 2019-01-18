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
import ctypes
from glob import glob
from os.path import join, exists, expandvars
from ctypes.wintypes import BOOL, DWORD


# Local imports
import builder

HEADER = '''\
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

"""
This file was automatically created by the BuildIDEIntegration.py script.
Don't try to edit this file yourself.

This module is used to assist and IDE in locating the modules that are apart 
of EventGhost. Because EventGhost uses a dynamic import system and there are 
no "hard coded" imports of it's modules, normally an IDE would not be able to 
track these modules. This file never gets used by the program, it is only here 
to provide the "hard coded" imports an IDE needs to see.

Follow the instructions below to create an EventGhost programming environment.
Here is a list of a couple of the features in your IDE that will now work 
properly.

    Code Completion
    Function/Method/Class parameters
    Code Inspection
    Object Definitions

Instructions for PyCharm
    Build EventGhost with the Build IDE Integration selected. 
    File --> Settings --> Project:{YOUR PROJECT NAM} --> Project Structure
    +Add Content Root
    Navigate to one level lower then this file location.
    click on OK
    click on Sources
    click on Apply
    click on OK
"""
'''

FOOTER = """
del _tmp

from Classes.IrDecoder import IrDecoder
"""

# BOOLEAN CreateSymbolicLinkA(
#   LPCSTR lpSymlinkFileName,
#   LPCSTR lpTargetFileName,
#   DWORD  dwFlags
# );

CreateSymbolicLinkW = ctypes.windll.kernel32.CreateSymbolicLinkW
CreateSymbolicLinkW.restype = BOOL


def symlink(source, link_name):
    flags = 1 if os.path.isdir(source) else 0
    lpTargetFileName = ctypes.create_unicode_buffer(source)
    lpSymlinkFileName = ctypes.create_unicode_buffer(link_name)
    dwFlags = DWORD(flags)

    if not CreateSymbolicLinkW(lpSymlinkFileName, lpTargetFileName, dwFlags):
        print (
            'Build IDE Integration: '
            'Unable to create symbolic links user MUST '
            'be in the Administrators group'
        )
        raise ctypes.WinError()


class BuildIDEIntegration(builder.Task):
    description = "Build IDE Integration (StaticImports.py)"

    def Setup(self):
        self.outFileName = join(self.buildSetup.sourceDir,
                                "eg", "StaticImports.py")
        if self.buildSetup.showGui:
            if os.path.exists(self.outFileName):
                self.activated = False
        else:
            self.activated = bool(self.buildSetup.args.build)

    def DoTask(self):
        outDir = join(self.buildSetup.sourceDir, "eg")
        outfile = open(self.outFileName, "w")
        outfile.write(HEADER)
        outfile.write("# py" + "lint: disable-msg=W0611,W0614,C0103\n")
        outfile.write("import eg\n")
        outfile.write("from Utils import * #py" + "lint: disable-msg=W0401\n")
        ScanDir(outDir, outfile, "Classes")
        ScanDir(outDir, outfile, "Classes.MainFrame")
        ScanDir(outDir, outfile, "Classes.UndoHandler")
        outfile.write("\n")
        outfile.write(FOOTER)
        outfile.close()

        src = join(self.buildSetup.sourceDir, 'plugins')
        dst = join(self.buildSetup.sourceDir, 'eg', 'CorePluginModule')

        try:
            symlink(src, dst)
        except WindowsError:
            pass
        else:
            with open(join(src, '__init__.py'), 'w') as f:
                f.write('')

            src = join(expandvars('%PROGRAMDATA%'), 'EventGhost', 'plugins')
            if exists(src):
                dst = join(self.buildSetup.sourceDir, 'eg', 'UserPluginModule')
                symlink(src, dst)

                with open(join(src, '__init__.py'), 'w') as f:
                    f.write('')


def ScanDir(srcDir, outfile, modName):
    parts = modName.split(".")
    scanDir = join(srcDir, *parts)
    if len(parts) > 1:
        outfile.write("from %s import %s\n" % (modName, parts[-1]))
    files = glob(join(scanDir, "*.py"))
    for filename in files:
        name = os.path.splitext(os.path.basename(filename))[0]
        if not name.startswith("__"):
            if len(parts) > 1:
                outfile.write(
                    "from %s.%s import %s as _tmp\n" % (modName, name, name)
                )
                outfile.write("%s.%s = _tmp\n" % (parts[-1], name))
            else:
                outfile.write("from %s.%s import %s\n" % (modName, name, name))
                outfile.write("eg.%s = %s\n" % (name, name))
