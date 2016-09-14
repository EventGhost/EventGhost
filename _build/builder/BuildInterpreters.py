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
Build py.exe and pyw.exe for EventGhost
"""

import shutil
import sys
import tempfile
import warnings
from distutils.core import setup
from os.path import exists, join

# Local imports
import builder

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import py2exe  # NOQA

PYVERSION = "%d%d" % sys.version_info[:2]
PY_BASE_NAME = "py%s" % PYVERSION
PYW_BASE_NAME = "pyw%s" % PYVERSION

class BuildInterpreters(builder.Task):
    description = "Build interpreters (py.exe, pyw.exe)"

    def Setup(self):
        if self.buildSetup.showGui:
            sourceDir = self.buildSetup.sourceDir
            if (exists(join(sourceDir, PY_BASE_NAME + ".exe")) and
                    exists(join(sourceDir, PYW_BASE_NAME + ".exe"))):
                self.activated = False
        else:
            self.activated = bool(self.buildSetup.args.build)

    def DoTask(self):
        buildSetup = self.buildSetup
        tmpDir = tempfile.mkdtemp()
        manifest = file(
            join(buildSetup.pyVersionDir, "Manifest.xml")
        ).read()
        setup(
            script_args = ["py2exe"],
            options=dict(
                build=dict(build_base=join(tmpDir, "build")),
                py2exe=dict(compressed=0, dist_dir=join(tmpDir, "dist"))
            ),
            # it is important, that the zipfile argument does match the one
            # from the main installer.
            zipfile="lib%s/python%s.zip" % (PYVERSION, PYVERSION),
            windows=[
                dict(
                    script=join(buildSetup.dataDir, "py.py"),
                    dest_base=PYW_BASE_NAME,
                    other_resources = [(24, 1, manifest)],
                )
            ],
            console=[
                dict(
                    script=join(buildSetup.dataDir, "py.py"),
                    dest_base=PY_BASE_NAME,
                    other_resources = [(24, 1, manifest)],
                )
            ],
            verbose=0,
        )
        shutil.copy(
            join(tmpDir, "dist", PY_BASE_NAME + ".exe"),
            buildSetup.sourceDir
        )
        shutil.copy(
            join(tmpDir, "dist", PYW_BASE_NAME + ".exe"),
            buildSetup.sourceDir
        )
        shutil.rmtree(tmpDir)
