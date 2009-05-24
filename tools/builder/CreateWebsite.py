import os
import time
from os.path import join, abspath

from jinja2 import Environment, FileSystemLoader
from docutils.core import publish_parts

import builder

class Page(object):

    def __init__(self):
        pass


class HomePage(Page):
    name = "Home"
    target = "/"
    outfile = "index.html"
    template = "home.tmpl"


class ForumPage(Page):
    name = "Forum"
    target = "/forum/"
    outfile = "css/header_forum.html"
    template = "header_only.tmpl"


class DocsPage(Page):
    name = "Documentation"
    target = "/docs/"
    outfile = r"..\docs\source\_templates\header_docs.html"
    template = "header_only.tmpl"


class WikiPage(Page):
    name = "Wiki"
    target = "/wiki/"
    outfile = "css/header_wiki.html"
    template = "header_only.tmpl"


class DownloadPage(Page):
    name = "Downloads"
    target = "/downloads/"
    outfile = "downloads/index.html"
    template = "download.tmpl"



class FileData(object):

    def __init__(self, path):
        self.path = path
        self.target = os.path.basename(path)
        parts = self.target.split("_")
        self.name = " ".join(parts[:2])
        fileStat = os.stat(path)
        self.time = time.strftime("%b %d %Y", time.gmtime(fileStat.st_mtime))
        self.size = "%0.1f MB" % (fileStat.st_size / 1024.0 / 1024)



def GetSetupFiles(srcDir):
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



class CreateWebsite(builder.Task):
    description = "Build website"

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
            template = env.get_template(page.template)
            template.stream(CURRENT=page).dump(
                join(buildSetup.websiteDir, page.outfile)
            )
        
    
