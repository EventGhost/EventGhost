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
import pygit2
from os.path import join
import builder


class UpdateVersionFile(builder.Task):
    """
    Update buildTime and revision for eg/Classes/VersionRevision.py
    """
    description = "Update version file"
    enabled = False

    def DoTask(self):
        buildSetup = self.buildSetup
        buildSetup.buildTime = time.time()
        filename = join(buildSetup.tmpDir, "VersionRevision.py")
        outfile = open(filename, "wt")
        major, minor, revision = buildSetup.appVersion.split('.')
        outfile.write("major = %r\n" % major)
        outfile.write("minor = %r\n" % minor)
        outfile.write("revision = %r\n" % revision)
        outfile.write("buildTime = %f\n" % buildSetup.buildTime)
        outfile.close()


class UpdateChangeLog(builder.Task):
    """
    Add a version header to CHANGELOG.TXT if needed.
    """
    description = "updating CHANGELOG.TXT"

    def DoTask(self):
        buildSetup = self.buildSetup
        repo = buildSetup.repo
        changelog_path = join(buildSetup.sourceDir, "CHANGELOG.TXT")

        # read from CHANGELOG.TXT the last version number for which an
        # entry exists (newest must be topmost).
        latest_version_in_log_refname = 'refs/tags/v0.0.0'
        try:
            infile = open(changelog_path, "r")
        except IOError:
            pass
        else:
            line = infile.readline().strip()
            while line:
                if line.startswith("**"):
                    latest_version_in_log_refname = 'refs/tags/v' + \
                                                line[2:].split()[0]
                    break
                line = infile.readline().strip()
            infile.close()

        # Get the last release version number (=highest number) and increment it
        app_version = buildSetup.appVersion

        # check if CHANGELOG.TXT is already up to date
        parts = latest_version_in_log_refname.split('/')
        latest_version = parts[len(parts)-1].strip('v')
        if latest_version == app_version:
            return  # we don't need to add anything

        tagnames = []
        refs = repo.listall_references()
        tags = []
        tagsdict = {}
        refsdict = {}
        for r in refs:
            if r.startswith('refs/tags/'):
                tagnames.append(r)
                ref = repo.lookup_reference(r)
                if ref.type == pygit2.GIT_REF_OID:
                    pass
                elif ref.type == pygit2.GIT_REF_SYMBOLIC:
                    pass
                    # what to do with symbolic?
                    # ref = ref.resolve()  ?
                tags.append(ref.target)
                tagsdict.update({ref.target : ref})
                refsdict.update({r: ref})

        # let's find out if we have a tag for the version from changelog.txt
        # if not, use branch reference.
        try:
            last_log_ref = repo.lookup_reference(latest_version_in_log_refname)
        except KeyError:
            try:
                last_log_ref = repo.lookup_reference(
                        latest_version_in_log_refname.replace('tags/v', 'tags/'))
            except KeyError:
                last_log_ref = repo.lookup_reference(buildSetup.branchFullname)
        last_release_version_oid = last_log_ref.target

        # fetch all commit messages since the last version found in changelog.
        bldDate = time.strftime("%Y-%m-%d", time.gmtime(buildSetup.buildTime))
        new_logs = '**{0} ({1})**\n\n'.format(app_version, bldDate)

        for commit in repo.walk(last_log_ref.target, pygit2.GIT_SORT_TIME):
            oid = commit.oid
            if oid == last_release_version_oid and \
                                last_log_ref.name != buildSetup.branchFullname:
                break
            elif oid in tags:
                commitTime = time.strftime("%Y-%m-%d", time.gmtime(
                    commit.commit_time + (commit.commit_time_offset*60)))
                new_logs += '\n\n**{0} ({1})**\n\n'.format(
                                            tagsdict[oid].shorthand.strip('v'),
                                            commitTime
                )
            message = commit.message.split('\n')[0]
            new_logs += '- {0} ({1})\n'.format(message, commit.author.name)

            # chg = []
            # for l in lines:
            #     # remove some unnecessary text
            #     if not l.startswith('git-svn-id:') and l.strip() != '':
            #         chg.append(l)
            # msg = '\n  '.join(chg)
            # if msg:
            #     new_logs += '- ' + msg + '\n'

        # read the existing changelog...
        try:
            infile = open(changelog_path, "r")
        except IOError:
            old_changelog = ''
        else:
            old_changelog = infile.readlines()
            infile.close()

        # ... and put the new changelog on top
        try:
            outfile = open(changelog_path, "w+")
        except IOError:
            import sys
            import wx
            parent = wx.GetApp().GetTopWindow()

            msg = "CHANGELOG.TXT couldn't be written.\n({0})".format(
                                                                sys.exc_value)
            dlg = wx.MessageDialog(parent, msg, caption="Error",
                                   style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        else:
            outfile.write(new_logs + '\n\n')
            if old_changelog:
                outfile.writelines(old_changelog)
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
        src = join(buildSetup.sourceDir, filename)
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
from builder.CreatePyExe import CreatePyExe
from builder.CreateLibrary import CreateLibrary
from builder.CreateWebsite import CreateWebsite
from builder.CreateDocs import CreateHtmlDocs, CreateChmDocs

TASKS = [
    UpdateVersionFile,
    UpdateChangeLog,
    CreateStaticImports,
    CreateImports,
    CheckSources,
    CreateChmDocs,
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

