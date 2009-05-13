import os
import time
from os.path import join, abspath

from jinja2 import Environment, FileSystemLoader
from docutils.core import publish_parts

import builder
WEBSITE_DIR = builder.WEBSITE_DIR

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



MENU_TABS = (HomePage, DocsPage, WikiPage, ForumPage, DownloadPage)

def GetSetupFiles():
    files = []
    for name in os.listdir(join(WEBSITE_DIR, "downloads")):
        if name.lower().startswith("eventghost_"):
            if name.lower().endswith("_setup.exe"):
                path = join(WEBSITE_DIR, "downloads", name)
                fileData = FileData(path)
                files.append(fileData)
    return list(reversed(sorted(files, key=lambda x: x.name)))

from docutils.core import publish_parts

def rst2html(rst):
    return publish_parts(rst, writer_name="html")["fragment"]


GLOBALS = {
    "files": GetSetupFiles(),
    "MENU_TABS": MENU_TABS,
    'rst2html': rst2html,

}

def Main():
    env = Environment(
        loader=FileSystemLoader(abspath(join(builder.DATA_DIR, 'templates'))),
        trim_blocks=True
    )
    env.globals = {
        "files": GetSetupFiles(),
        "MENU_TABS": MENU_TABS,
        #"pathto": pathto,
    }
    env.filters = {'rst2html': rst2html}

    for page in MENU_TABS:
        template = env.get_template(page.template)
        template.stream(CURRENT=page).dump(join(WEBSITE_DIR, page.outfile))
    

