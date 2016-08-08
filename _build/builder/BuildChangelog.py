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

import os
from agithub.GitHub import GitHub
from collections import OrderedDict
from os.path import join
from shutil import copy2
from time import localtime, strftime

# Local imports
import builder
from builder.Utils import EscapeMarkdown, NextPage

class BuildChangelog(builder.Task):
    """
    Populate CHANGELOG.TXT with the latest changes from GitHub.
    """
    description = "Build changelog"

    def Setup(self):
        if os.environ.get("USERNAME") == "appveyor":
            self.activated = False
        elif not self.buildSetup.showGui:
            self.activated = bool(self.buildSetup.args.package)

    def DoTask(self):
        buildSetup = self.buildSetup
        changelog_path = join(buildSetup.outputDir, "CHANGELOG.TXT")
        copy2(
            join(buildSetup.sourceDir, "CHANGELOG.TXT"),
            changelog_path
        )

        token = buildSetup.gitConfig["token"]
        user = buildSetup.gitConfig["user"]
        repo = buildSetup.gitConfig["repo"]
        branch = buildSetup.gitConfig["branch"]

        gh = GitHub(token=token)
        rc, data = gh.repos[user][repo].git.refs.tags.get()
        if rc != 200:
            print "INFO: couldn't get tags."
            exit(1)
        to_commits = [i["object"]["sha"] for i in data]

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
                exit(1)
            for item in data:
                if item['sha'] in to_commits:
                    break
                try:
                    msg = item['commit']['message'].splitlines()[0]
                    if msg.startswith("Merge pull request #"):
                        included_prs.append(int(msg.split()[3][1:]))
                except IndexError:
                    pass
            if item['sha'] in to_commits:
                break
            page = NextPage(gh)

        # now filter and group the pull requests
        page = 1
        pulls = []
        while page > 0:
            rc, data = gh.search.issues.get(
                q='type:pr is:merged '
                  '-label:internal '
                  'user:EventGhost '
                  'repo:EventGhost',
                sort="created",
                order="asc",
                per_page=100,
                page=page
            )
            if rc != 200:
                print "INFO: couldn't get additional info."
                exit(1)
            elif data.get("incomplete_results") == True:
                print "INFO: incomplete search result."
                exit(1)
            pulls.extend(data["items"])
            page = NextPage(gh)

        title_notice = "Important changes for plugin developers"
        title_enhancement = "Enhancements"
        title_bug = "Fixed bugs"
        title_other = "Other changes"
        prs = OrderedDict()
        prs[title_notice] = []
        prs[title_enhancement] = []
        prs[title_bug] = []
        prs[title_other] = []

        for pr in pulls:
            if not pr["number"] in included_prs:
                continue
            labels = [l["name"] for l in pr["labels"]]
            if "internal" in labels:
                # This pull request should not be listed in changelog
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
        buildDate = strftime("%Y-%m-%d", localtime(buildSetup.buildTime))
        releaseUrl = "https://github.com/{0}/{1}/releases/tag/v{2}".format(
            user, repo, buildSetup.appVersion
        )

        changes = ["## [{0}]({1}) ({2})\n".format(
            buildSetup.appVersion,
            releaseUrl,
            buildDate,
        )]
        print "## {0} ({1})\n".format(buildSetup.appVersion, buildDate)
        for title, items in prs.iteritems():
            if items:
                changes.append("\n**{0}:**\n\n".format(title))
                print "{0}:".format(title)
                for pr in items:
                    changes.append("* {0} [#{1}]({2}) ([{3}]({4}))\n".format(
                        EscapeMarkdown(pr["title"]),
                        pr["number"],
                        pr["html_url"],
                        pr["user"]["login"],
                        pr["user"]["html_url"],
                    ))
                    print "* {0} #{1} ({2})".format(
                        pr["title"],
                        pr["number"],
                        pr["user"]["login"],
                    )
                print ""

        if len(changes) == 1:
            text = "\nOnly minor changes in this release.\n"
            changes.append(text)
            print text

        # read the existing changelog...
        try:
            infile = open(changelog_path, "r")
        except IOError:
            old_changes = ''
        else:
            old_changes = infile.read()
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
            outfile.writelines(changes)
            if old_changes:
                outfile.write('\n---\n\n')
                outfile.write(old_changes)
            outfile.close()
