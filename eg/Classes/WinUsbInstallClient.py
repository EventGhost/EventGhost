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

import tempfile
import shutil
import sys
import codecs
from os.path import join
from subprocess import call


def InstallDriver(infContent, srcDir):
    tmpDir = tempfile.mkdtemp()
    targetDir = join(tmpDir, "driver")
    shutil.copytree(srcDir, targetDir)
    infPath = join(targetDir, "driver.inf")
    outfile = codecs.open(infPath, "wt", sys.getfilesystemencoding())
    outfile.write(infContent)
    outfile.close()
    res = call('"' + join(targetDir, "dpinst.exe") + '" /f /lm')
    shutil.rmtree(tmpDir)
    return res


