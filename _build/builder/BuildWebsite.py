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

import errno
import os
import time
from docutils.core import publish_parts
from jinja2 import Environment, FileSystemLoader
from os.path import abspath, join

# Local imports
import builder

class BuildWebsite(builder.Task):
    description = "Build website"

    def Setup(self):
        if self.buildSetup.showGui:
            self.activated = False
        else:
            self.activated = bool(self.buildSetup.args.sync)

    def DoTask(self):
        buildSetup = self.buildSetup
        menuTabs = (HomePage, DocsPage, WikiPage, ForumPage, DownloadPage)
        env = Environment(
            loader=FileSystemLoader(
                abspath(join(buildSetup.dataDir, 'templates'))
            ),
            trim_blocks=True
        )
        env.globals = {
            "files": GetSetupFiles(join(buildSetup.websiteDir, "downloads")),
            "MENU_TABS": menuTabs,
        }
        env.filters = {'rst2html': rst2html}
        for page in menuTabs:
            path = os.path.abspath(join(buildSetup.websiteDir, page.outfile))
            try:
                os.makedirs(os.path.dirname(path))
            except os.error, exc:
                if exc.errno != errno.EEXIST:
                    raise
            env.get_template(page.template).stream(CURRENT=page).dump(path)


class FileData(object):
    def __init__(self, path):
        self.path = path
        self.target = os.path.basename(path)
        parts = self.target.split("_")
        self.name = " ".join(parts[:2])
        fileStat = os.stat(path)
        self.time = time.strftime("%b %d %Y", time.gmtime(fileStat.st_mtime))
        self.size = "%0.1f MB" % (fileStat.st_size / 1024.0 / 1024)


class Page(object):
    def __init__(self):
        pass


class HomePage(Page):
    name = "Home"
    target = "/"
    outfile = "index.html"
    template = "home.tmpl"


class DocsPage(Page):
    name = "Documentation"
    target = "/docs/"
    outfile = "css/header_docs.html"
    template = "header_only.tmpl"


class DownloadPage(Page):
    name = "Downloads"
    target = "/downloads/"
    outfile = "downloads/index.html"
    template = "download.tmpl"


class ForumPage(Page):
    name = "Forum"
    target = "/forum/"
    outfile = "css/header_forum.html"
    template = "header_only.tmpl"


class WikiPage(Page):
    name = "Wiki"
    target = "/mediawiki/"
    outfile = "css/header_wiki.html"
    template = "header_only.tmpl"


def GetSetupFiles(srcDir):
    if not os.path.exists(srcDir):
        return []
    files = []
    for name in os.listdir(srcDir):
        if name.lower().startswith("eventghost_"):
            if name.lower().endswith("_setup.exe"):
                path = join(srcDir, name)
                fileData = FileData(path)
                files.append(fileData)

    def Cmp(x, y):
        x = x.target.split("_")[1].replace("r", "").split(".")
        y = y.target.split("_")[1].replace("r", "").split(".")
        x = [int(s) for s in x]
        y = [int(s) for s in y]
        return cmp(x, y)

    return list(reversed(sorted(files, cmp=Cmp)))

def rst2html(rst):
    return publish_parts(rst, writer_name="html")["fragment"]
