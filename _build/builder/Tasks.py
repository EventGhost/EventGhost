# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import shutil
import time
from os.path import join

# Local imports
import builder

class CreateInstaller(builder.Task):
    description = "Build Setup.exe"

    def Setup(self):
        if not self.buildSetup.showGui:
            self.activated = bool(self.buildSetup.args.package)

    def DoTask(self):
        self.buildSetup.CreateInstaller()


class SyncWebsite(builder.Task):
    description = "Synchronize website"
    options = {"url": ""}

    def Setup(self):
        if not self.options["url"]:
            self.enabled = False
            self.activated = False
        elif not self.buildSetup.showGui:
            self.activated = bool(self.buildSetup.args.sync)

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


class UpdateVersionFile(builder.Task):
    """
    Write version information to eg/Classes/VersionInfo.py
    """
    description = "Update version file"
    enabled = False

    def DoTask(self):
        buildSetup = self.buildSetup
        buildSetup.buildTime = time.time()
        filename = join(buildSetup.tmpDir, "VersionInfo.py")
        outfile = open(filename, "wt")
        base = buildSetup.appVersion.split("-")[0]
        major, minor, patch, alpha, beta, rc = buildSetup.appVersionInfo
        outfile.write("string = '{0}'\n".format(buildSetup.appVersion))
        outfile.write("base = '{0}'\n".format(base))
        outfile.write("major = {0}\n".format(major))
        outfile.write("minor = {0}\n".format(minor))
        outfile.write("patch = {0}\n".format(patch))
        outfile.write("alpha = {0}\n".format(alpha))
        outfile.write("beta = {0}\n".format(beta))
        outfile.write("rc = {0}\n".format(rc))
        outfile.write("buildTime = {0}\n".format(buildSetup.buildTime))
        outfile.close()


class Upload(builder.Task):
    description = "Release to web"
    options = {"url": ""}

    def Setup(self):
        if not self.options["url"]:
            self.enabled = False
            self.activated = False
        elif not self.buildSetup.showGui:
            self.activated = bool(self.buildSetup.args.release)

    def DoTask(self):
        import builder.Upload
        buildSetup = self.buildSetup
        filename = (
            buildSetup.appName + "_" + buildSetup.appVersion + "_Setup.exe"
        )
        src = join(buildSetup.sourceDir, filename)
        dst = join(buildSetup.websiteDir, "downloads", filename)
        builder.Upload.Upload(src, self.options["url"])
        shutil.copyfile(src, dst)
        shutil.copystat(src, dst)


from builder.CreateStaticImports import CreateStaticImports  # NOQA
from builder.CreateImports import CreateImports  # NOQA
from builder.CheckSources import CheckSources  # NOQA
from builder.CreatePyExe import CreatePyExe  # NOQA
from builder.CreateLibrary import CreateLibrary  # NOQA
from builder.CreateWebsite import CreateWebsite  # NOQA
from builder.CreateDocs import CreateHtmlDocs, CreateChmDocs  # NOQA
from builder.CreateGitHubRelease import CreateGitHubRelease  # NOQA
from builder.UpdateChangeLog import UpdateChangeLog  # NOQA

TASKS = [
    UpdateVersionFile,
    CheckSources,
    CreateStaticImports,
    CreateImports,
    CreatePyExe,
    CreateLibrary,
    UpdateChangeLog,
    CreateChmDocs,
    CreateInstaller,
    CreateGitHubRelease,
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
