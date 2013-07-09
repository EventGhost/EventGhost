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
from os.path import join
from glob import glob
import builder

SINGLETONS = (
    "document",
)

HEADER = '''\
"""
This file was automatically created by the tools/StaticImports.py script.
Don't try to edit this file yourself.

This module is not directly used by EventGhost. It only exists to help
pylint and other tools to read the sources properly, as EventGhost is using
a lazy import pattern.
"""
'''

FOOTER = """
del _tmp

from Classes.IrDecoder import IrDecoder

def RegisterPlugin(**dummyKwArgs):
    pass
"""

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
                outfile.write("from %s.%s import %s as _tmp\n" % (modName, name, name))
                outfile.write("%s.%s = _tmp\n" % (parts[-1], name))
            else:
                outfile.write("from %s.%s import %s\n" %(modName, name, name))
                outfile.write("eg.%s = %s\n" %(name, name))



class CreateStaticImports(builder.Task):
    description = "Create StaticImports.py"

    def Setup(self):
        self.outFileName = join(
            self.buildSetup.sourceDir, "eg", "StaticImports.py"
        )
        if not os.path.exists(self.outFileName):
            self.activated = True
            self.enabled = False
        

    def DoTask(self):
        outDir = join(self.buildSetup.sourceDir, "eg")
        outfile = open(self.outFileName, "wt")
        outfile.write(HEADER)
        outfile.write("# py" + "lint: disable-msg=W0611,W0614,C0103\n")
        outfile.write("import eg\n")
        outfile.write("from Utils import * #py" + "lint: disable-msg=W0401\n")
        ScanDir(outDir, outfile, "Classes")
        ScanDir(outDir, outfile, "Classes.MainFrame")
        ScanDir(outDir, outfile, "Classes.UndoHandler")
        outfile.write("\n")
        for name in SINGLETONS:
            clsName = name[0].upper() + name[1:]
            outfile.write("%s = %s()\n" % (name, clsName))
        outfile.write(FOOTER)
        outfile.close()
    
