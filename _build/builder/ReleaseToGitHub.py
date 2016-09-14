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

import base64
import sys
import wx
from agithub.GitHub import GitHub
from os.path import join

# Local imports
import builder
from builder.Utils import NextPage

if sys.version_info[0:2] > (3, 0):
    import http.client
    import urllib.parse
else:
    import httplib as http
    http.client = http
    import urllib as urllib
    urllib.parse = urllib

class ReleaseToGitHub(builder.Task):
    description = "Release to GitHub"

    def Setup(self):
        self.enabled = bool(self.buildSetup.gitConfig["token"])
        if self.buildSetup.showGui:
            self.activated = False
        else:
            self.activated = (
                bool(self.buildSetup.args.release) and self.enabled
            )

    def DoTask(self):
        buildSetup = self.buildSetup
        appVer = buildSetup.appVersion
        gitConfig = buildSetup.gitConfig
        token = gitConfig["token"]
        user = gitConfig["user"]
        repo = gitConfig["repo"]
        branch = gitConfig["branch"]
        ref = 'heads/{0}'.format(branch)
        setupFile = 'EventGhost_{0}_Setup.exe'.format(appVer)
        setupPath = join(buildSetup.outputDir, setupFile)
        chglogFile = "CHANGELOG.md"
        chglogPath = join(buildSetup.outputDir, chglogFile)

        print "reading changelog"
        try:
            f = open(chglogPath, 'r')
        except IOError:
            print "ERROR: couldn't read changelog file ({0}).".format(chglogFile)
            return
        else:
            changelog = f.read()
            f.close()

        print "loading setup file"
        try:
            f = open(setupPath, 'rb')
        except IOError:
            print "ERROR: '{0}' not found.".format(setupFile)
            return
        else:
            setupFileContent = f.read()
            f.close()

        gh = GitHub(token=token)

        print "getting release info"
        releaseExists = False
        page = 1
        while page > 0:
            rc, data = gh.repos[user][repo].releases.get(
                sha=branch,
                per_page=100,
                page=page
            )
            page = NextPage(gh)
            if rc == 200:
                for rel in data:
                    if rel['name'][1:] == appVer:
                        app = wx.GetApp()
                        win = app.GetTopWindow()
                        dlg = wx.MessageDialog(
                            win,
                            caption="Information",
                            message="Found an existing GitHub release matching"
                            " 'v{0}'\nOverwrite it?".format(appVer),
                            style=wx.YES_NO
                        )
                        if dlg.ShowModal() == wx.ID_NO:
                            return
                        releaseId = rel["id"]
                        uploadUrl = str(rel['upload_url'][:-13])
                        releaseExists = True

        print "getting branch info"
        rc, data = gh.repos[user][repo].branches[branch].get()
        if rc != 200:
            print "ERROR: couldn't get branch info."
            return
        commitSha = data['commit']['sha']

        rc, data = gh.repos[user][repo].contents[chglogFile].get(ref=branch)
        if rc == 200:
            remoteChangelog = base64.decodestring(data["content"])
        else:
            remoteChangelog = None
        if changelog != remoteChangelog:
            print "getting commit referenced by branch"
            rc, data = gh.repos[user][repo].git.commits[commitSha].get()
            if rc != 200:
                print "ERROR: couldn't get commit info."
                return
            treeSha = data['tree']['sha']

            print "getting tree"
            rc, data = gh.repos[user][repo].git.trees[treeSha].get()
            if rc != 200:
                print "ERROR: couldn't get tree info."
                return
            blob = None
            print "getting blob for {0}".format(chglogFile)
            for entry in data['tree']:
                if entry['path'] == chglogFile and entry['type'] == 'blob':
                    blob = entry
                    break
            if blob is None:
                print "ERROR: couldn't get blob info."
                return

            print "posting new changelog"
            body = {
                'content': changelog,
                'encoding': 'utf-8'
            }
            rc, data = gh.repos[user][repo].git.blobs.post(body=body)
            if rc != 201:
                print "ERROR: couldn't post new changelog contents."
                return

            print "posting tree"
            newblob = {
                'path': blob['path'],
                'mode': blob['mode'],
                'type': blob['type'],
                'sha': data['sha']
            }
            body = {
                'tree': [newblob],
                'base_tree': treeSha
            }
            rc, data = gh.repos[user][repo].git.trees.post(body=body)
            if rc != 201:
                print "ERROR: couldn't post new tree."
                return
            newTreeSha = data['sha']

            print "creating commit for changelog update"
            body = {
                'message': "Add changelog for v{0}".format(appVer),
                'tree': newTreeSha,
                'parents': [commitSha]
            }
            rc, data = gh.repos[user][repo].git.commits.post(body=body)
            if rc != 201:
                print "ERROR: couldn't create commit for changelog update."
                return
            newCommitSha = data['sha']

            print "updating reference for branch to new commit"
            body = {'sha': newCommitSha}
            rc, data = gh.repos[user][repo].git.refs[ref].patch(body=body)
            if rc != 200:
                print "ERROR: couldn't update reference ({0}) with new commit.".format(ref)
                return

        if not releaseExists:
            print "extracting changelog for this release"
            relChglog = ''
            chgLines = changelog.splitlines(True)
            try:
                for i in range(1, len(chgLines)):
                    if chgLines[i].startswith("## "):
                        break
                    else:
                        relChglog += chgLines[i]
            except IndexError:
                pass
            relChglog = relChglog.strip()

            print "creating release"
            body = {'tag_name': 'v{0}'.format(appVer),
                    'target_commitish': newCommitSha,
                    'name': 'v{0}'.format(appVer),
                    'body': relChglog,
                    #'draft': False,
                    'prerelease': ("-" in self.buildSetup.appVersion)
                    }
            rc, data = gh.repos[user][repo].releases.post(body=body)
            if rc != 201:
                print "ERROR: couldn't create a release on GitHub."
                return
            uploadUrl = str(data['upload_url'][:-13])
        else:
            print 'deleting existing asset'
            rc, data = gh.repos[user][repo].releases[releaseId].assets.get()
            if rc == 200:
                for asset in data:
                    if asset["name"] == setupFile:
                        rc, data = gh.repos[user][repo].releases.\
                            assets[asset["id"]].delete()
                        if rc != 204:
                            print "ERROR: couldn't delete existing asset."
                            return
                        break

        print "uploading setup file"
        url = uploadUrl + '?name={0}'.format(setupFile)
        headers = {'content-type': 'application/octet-stream',
                   'authorization': 'Token {0}'.format(token),
                   'accept': 'application/vnd.github.v3+json',
                   'user-agent': 'agithub/v2.0'}
        conn = http.client.HTTPSConnection('uploads.github.com')
        conn.request('POST', url, setupFileContent, headers)
        response = conn.getresponse()
        status = response.status
        conn.close()
        if status != 201:
            print "ERROR: couldn't upload installer file to GitHub."
            return
