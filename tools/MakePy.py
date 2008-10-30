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
# $LastChangedDate: 2008-10-09 23:58:28 +0200 (Do, 09 Okt 2008) $
# $LastChangedRevision: 521 $
# $LastChangedBy: bitmonster $

"""
Create py.exe and pyw.exe for EventGhost
"""

from distutils.core import setup
import py2exe
import tempfile
import shutil
import sys
from os.path import join, dirname

PYVERSION = str(sys.version_info[0]) + str(sys.version_info[1])
tmpDir = tempfile.mkdtemp()

sys.argv.append("py2exe")
setup(
    options=dict(
        build=dict(build_base=join(tmpDir, "build")),
        py2exe=dict(compressed=0, dist_dir=join(tmpDir, "dist"))
    ),
    # it is important, that the zipfile argument does match the one from
    # the main installer.
    zipfile="lib%s/python%s.zip" % (PYVERSION, PYVERSION),
    windows=[dict(script="py.py", dest_base="pyw")],
    console=[dict(script="py.py", dest_base="py")],
    verbose=0,
)
outDir = join(dirname(sys.argv[0]), "Python%s" % PYVERSION)
shutil.copy(join(tmpDir, "dist", "py.exe"), outDir)
shutil.copy(join(tmpDir, "dist", "pyw.exe"), outDir)
shutil.rmtree(tmpDir)
