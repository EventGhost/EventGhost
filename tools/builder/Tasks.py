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

import sys
import shutil
import time
from os.path import join
import builder
from builder.Utils import EncodePath


class UpdateSvn(builder.Task):
    description = "Update from SVN"

    def DoTask(self):
        from builder.Utils import UpdateSvn
        UpdateSvn(self.buildSetup.sourceDir)



class UpdateVersionFile(builder.Task):
    """
    Update buildTime and revision for eg/Classes/VersionRevision.py
    """
    description = "Update version file"
    visible = False

    def DoTask(self):
        from builder.Utils import GetSvnRevision
        import imp
        buildSetup = self.buildSetup
        svnRevision = GetSvnRevision(buildSetup.sourceDir)
        outfile = open(
            join(buildSetup.tmpDir, "VersionRevision.py"),
            "wt"
        )
        outfile.write("revision = %r\n" % svnRevision)
        outfile.write("buildTime = %f\n" % time.time())
        outfile.close()
        versionFilePath = join(
            buildSetup.sourceDir, "eg", "Classes", "Version.py"
        )
        mod = imp.load_source("Version", EncodePath(versionFilePath))
        buildSetup.appVersion = mod.Version.base + (".r%s" % svnRevision)
        buildSetup.appNumericalVersion = mod.Version.base + ".%s" % svnRevision


class UpdateChangeLog(builder.Task):
    """
    Add a version header to CHANGELOG.TXT if needed.
    """
    description = "updating CHANGELOG.TXT"
    visible = False

    def DoTask(self):
        path = join(self.buildSetup.sourceDir, "CHANGELOG.TXT")
        timeStr = time.strftime("%m/%d/%Y")
        header = "**%s (%s)**\n\n" % (self.buildSetup.appVersion, timeStr)
        infile = open(path, "r")
        data = infile.read(100) # read some data from the beginning
        if data.strip().startswith("**"):
            # no new lines, so skip the addition of a new header
            return
        data += infile.read() # read the remaining contents
        infile.close()
        outfile = open(path, "w+")
        outfile.write(header + data)
        outfile.close()



class CreateInstaller(builder.Task):
    description = "Build Setup.exe"

    def DoTask(self):
        self.buildSetup.CreateInstaller()



class Upload(builder.Task):
    description = "Upload through FTP"
    options = {"url": ""}

    def Setup(self):
        if not self.options["url"]:
            self.enabled = False
            self.activated = False


    def DoTask(self):
        import builder.Upload
        buildSetup = self.buildSetup
        filename = (
            buildSetup.appName + "_" + buildSetup.appVersion + "_Setup.exe"
        )
        src = join(buildSetup.outDir, filename)
        dst = join(buildSetup.websiteDir, "downloads", filename)
        builder.Upload.Upload(src, self.options["url"])
        shutil.copyfile(src, dst)
        shutil.copystat(src, dst)



class SyncWebsite(builder.Task):
    description = "Synchronize website"
    options = {"url": ""}

    def Setup(self):
        if not self.options["url"]:
            self.enabled = False
            self.activated = False


    def DoTask(self):
        from SftpSync import SftpSync

        syncer = SftpSync(self.options["url"])
        addFiles = [
            (join(self.buildSetup.websiteDir, "index.html"), "index.html"),
        ]
        syncer.Sync(self.buildSetup.websiteDir, addFiles)
        # touch wiki file, to force re-evaluation of the header template
        syncer.sftpClient.utime(syncer.remotePath + "wiki", None)

        # clear forum cache, to force re-building of the templates
        syncer.ClearDirectory(
            syncer.remotePath + "forum/cache",
            excludes=["index.htm", ".htaccess"]
        )
        syncer.Close()



from builder.CreateStaticImports import CreateStaticImports
from builder.CreateImports import CreateImports
from builder.CheckSources import CheckSources
from builder.CreateSourceArchive import CreateSourceArchive
from builder.CreatePyExe import CreatePyExe
from builder.CreateLibrary import CreateLibrary
from builder.CreateWebsite import CreateWebsite
from builder.CreateDocs import CreateHtmlDocs, CreateChmDocs

TASKS = [
    UpdateSvn,
    UpdateVersionFile,
    UpdateChangeLog,
    CreateStaticImports,
    CreateImports,
    CheckSources,
    CreateChmDocs,
    CreateSourceArchive,
    CreatePyExe,
    CreateLibrary,
    CreateInstaller,
    Upload,
    CreateWebsite,
    CreateHtmlDocs,
    SyncWebsite,
]


def Main(buildSetup):
    """
    Main task of the script.
    """
    for task in buildSetup.tasks:
        if task.activated:
            print "---", task.description
            task.DoTask()
    print "--- All done!"

