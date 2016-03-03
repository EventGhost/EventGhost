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
import wx
import builder
from os.path import join
from .github import GitHub

if sys.version_info[0:2] > (3,0):
    import http.client
    import urllib.parse
else:
    import httplib as http
    http.client = http
    import urllib as urllib
    urllib.parse = urllib


class CreateGitHubRelease(builder.Task):
    description = "Create a Release on GitHub\n " \
                  "(commit changelog and upload installer)"
    activated = False

    def DoTask(self):
        srcDir = self.buildSetup.sourceDir
        appVer = self.buildSetup.appVersion
        token = self.buildSetup.githubToken
        user = self.buildSetup.githubUser
        repo = self.buildSetup.githubRepo
        branch = self.buildSetup.githubBranch
        ref = 'heads/{0}'.format(branch)
        setupFile = 'EventGhost_{0}_Setup.exe'.format(appVer)
        setupPath = join(srcDir, 'build', 'output', setupFile)
        chglogFile = 'CHANGELOG.TXT'

        print "reading changelog"
        try:
            f = open(join(srcDir, chglogFile), 'r')
        except IOError:
            print "ERROR: couldn't read changelog file ({0}).".format(chglogFile)
            return
        else:
            changelog = f.read()
            f.close()

        print "loading setup file"
        try:
            f = open(join(srcDir, setupPath), 'rb')
        except IOError:
            print "ERROR: '{0}' not found.".format(setupFile)
            return
        else:
            setupFileContent = f.read()
            f.close()

        gh = GitHub(token=token)

        print "getting branch info"
        rc, data = gh.repos[user][repo].releases.latest.get()
        add2release = wx.ID_CANCEL
        if rc != 200:
            print "INFO: couldn't get latest release info."
        else:
            if data['name'][1:] == appVer:
                app = wx.GetApp()
                win = app.GetTopWindow()
                dlg = wx.MessageDialog(win,
                       "A Release with the name 'v{0}' already exists. "
                       "Should the setup file be uploaded to this release?".
                       format(appVer), "Information", style=wx.OK|wx.CANCEL)
                add2release = dlg.ShowModal()
                uploadUrl = str(data['upload_url'][:-13])

        print "getting branch info"
        rc, data = gh.repos[user][repo].branches[branch].get()
        if rc != 200:
            print "ERROR: couldn't get branch info."
            return
        commitSha = data['commit']['sha']

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
            if entry['path'] == chglogFile and entry['type']=='blob':
                blob = entry
                break
        if blob == None:
            print "ERROR: couldn't get blob info."
            return

        print "posting new changelog"
        body = {'content': changelog,
               'encoding': 'utf-8'}
        rc, data = gh.repos[user][repo].git.blobs.post(body=body)
        if rc != 201:
            print "ERROR: couldn't post new changelog contents."
            return

        print "posting tree"
        newblob = {'path': blob['path'],
            'mode': blob['mode'],
            'type': blob['type'],
            'sha' : data['sha']}
        body = {'tree': [newblob],
            'base_tree': treeSha}
        rc, data = gh.repos[user][repo].git.trees.post(body=body)
        if rc != 201:
            print "ERROR: couldn't post new tree."
            return
        newTreeSha = data['sha']

        print "creating commit for updatet changelog"
        body = {'message': "Updatet {0} for new release v{1}.".
            format(chglogFile, appVer),
            'tree': newTreeSha,
            'parents': [commitSha]}
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

        print "extracting changelog for this release"
        relChglog = ''
        chgLines = changelog.splitlines(True)
        try:
            for i in range(1, len(chgLines)):
                if chgLines[i].startswith('**'):
                    break
                else:
                    relChglog += chgLines[i]
        except IndexError:
            pass

        if add2release == wx.ID_CANCEL:
            print "creating release"
            body = {'tag_name': 'v{0}'.format(appVer),
                    'target_commitish': newCommitSha,
                    'name': 'v{0}'.format(appVer),
                    'body': relChglog,
                    #'draft': False,
                    #'prerelease': False
                    }
            rc, data = gh.repos[user][repo].releases.post(body=body)
            if rc != 201:
                print "ERROR: couldn't create a release on GitHub."
                return
            uploadUrl = str(data['upload_url'][:-13])

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

