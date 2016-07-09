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

from collections import OrderedDict
from agithub.GitHub import GitHub
from os.path import join

# Local imports
import builder
from builder.Utils import NextPage

class BuildChangelog(builder.Task):
    """
    Populate CHANGELOG.TXT with the latest changes from GitHub.
    """
    description = "Build changelog"

    def Setup(self):
        if not self.buildSetup.showGui:
            self.activated = bool(self.buildSetup.args.package)

    def DoTask(self):
        buildSetup = self.buildSetup
        changelog_path = join(buildSetup.sourceDir, "CHANGELOG.TXT")

        token = buildSetup.gitConfig["token"]
        user = buildSetup.gitConfig["user"]
        repo = buildSetup.gitConfig["repo"]
        branch = buildSetup.gitConfig["branch"]

        gh = GitHub(token=token)
        rc, data = gh.repos[user][repo].releases.latest.get()
        if rc != 200:
            # in case of no latest release
            to_commit = self.get_alternative_release(gh, user, repo)
        else:
            to_commit = data['target_commitish']

        # get commits since last release
        page = 1
        included_prs = []
        item = {}
        while page > 0:
            rc, data = gh.repos[user][repo].commits.get(
                sha=branch,
                per_page=100,
                page=page
            )
            if rc != 200:
                print "INFO: couldn't get commits."
                return
            for item in data:
                if item['sha'] == to_commit:
                    break
                try:
                    msg = item['commit']['message'].splitlines()[0]
                    if msg.startswith("Merge pull request #"):
                        included_prs.append(int(msg.split()[3][1:]))
                except IndexError:
                    pass
            if item.get('sha') == to_commit:
                break
            page = NextPage(gh)

        # get all closed pull requests for the repo
        pulls = []
        page = 1
        while page > 0:
            rc, data = gh.repos[user][repo].pulls.get(
                state="closed",
                base = branch,
                direction="asc",
                per_page=100,
                page=page,
            )
            if rc != 200:
                print "INFO: couldn't get pull requests."
                return
            pulls.extend(data)
            page = NextPage(gh)

        # now filter and group the pull requests
        print "--------------------------------------------------------"
        title_notice = "Important changes for plugin developers:"
        title_enhancement = "Features added:"
        title_bug = "Bugs fixed:"
        title_other = "Other changes:"
        prs = OrderedDict()
        prs[title_notice] = []
        prs[title_enhancement] = []
        prs[title_bug] = []
        prs[title_other] = []
        for pr in pulls:
            if not pr["number"] in included_prs:
                continue
            rc, data = gh.repos[user][repo].issues[pr["number"]].get()
            if rc != 200:
                print "couldn't get additional info for pr #{0} {1}" \
                      "\n   --> skipping #{0}".format(pr["number"], pr["title"])
                continue
            labels = [l["name"] for l in data["labels"]]
            if "internal" in labels:
                # This pull request should not be listed in changelog
                print "skipped internal #{0} {1}".format(pr["number"], pr["title"])
                continue
            elif "notice" in labels:
                prs[title_notice].append(pr)
            elif "enhancement" in labels:
                prs[title_enhancement].append(pr)
            elif "bug" in labels:
                prs[title_bug].append(pr)
            else:
                prs[title_other].append(pr)

        # prepare the grouped output
        print "--------------------------------------------------------"
        new_logs = [""]
        for title, items in prs.iteritems():
            if items:
                print "# {0}".format(title)
                new_logs.append("### {0}\n".format(title))
                for pr in items:
                    txt = "  - #{0} {1}".format(pr["number"], pr["title"])
                    print txt
                    new_logs.append(txt + "\n")
                new_logs.append("\n")
                print ""

        # read the existing changelog...
        try:
            infile = open(changelog_path, "r")
        except IOError:
            old_changelog = ''
        else:
            old_changelog = infile.read()
            infile.close()

        # ... and put the new changelog on top
        try:
            outfile = open(changelog_path, "w+")
        except IOError:
            import sys
            import wx
            parent = wx.GetApp().GetTopWindow()

            msg = "CHANGELOG.TXT couldn't be written.\n({0})".format(
                sys.exc_value
            )
            dlg = wx.MessageDialog(parent, msg, caption="Error",
                                   style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        else:
            outfile.writelines(new_logs)
            if old_changelog:
                outfile.write('\n\n')
                outfile.write(old_changelog)
            outfile.close()

    def get_alternative_release(self, gh, user, repo):
        # try to find any release
        rc, data = gh.repos[user][repo].releases.get()
        if rc != 200:
            #print "INFO: couldn't get latest release info."
            return None

        latestRelName = ''
        latestSha = None
        for item in data:
            if item['name'] > latestRelName:
                latestRelName = item['name']
                latestSha = item['target_commitish']
        # no releases yet, try to find a tag.
        if not latestSha:
            rc, data = gh.repos[user][repo].git.refs.tags.get()
            if rc == 200:
                for item in data:
                    if item['ref'][11:] > latestRelName:
                        latestRelName = item['ref'][11:]
                        latestSha = item['object']['sha']
        return latestSha
