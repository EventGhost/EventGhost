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

import zipfile
from os.path import join, isdir

import builder


class CreateSourceArchive(builder.Task):
    description = "Build source archive"

    def DoTask(self):
        """
        Create a zip archive off all versioned files in the working copy.
        """
        import pysvn

        filename = join(
            self.buildSetup.outDir,
            "%(appName)s_%(appVersion)s_Source.zip" % self.buildSetup.__dict__
        )
        client = pysvn.Client()
        workingDir = self.buildSetup.sourceDir
        zipFile = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
        for status in client.status(workingDir, ignore=True):
            if status.is_versioned:
                path = status.path
                if not isdir(path):
                    arcname = path[len(workingDir) + 1:]
                    zipFile.write(path, arcname)
        zipFile.close()

