import os
import time
from os.path import join, abspath
from mako.template import Template
from mako.lookup import TemplateLookup

import builder
BASE_DIR = builder.WEBSITE_DIR

class Page(object):
    
    def __init__(self):
        pass
    

class HomePage(Page):
    name = "Home"
    target = "/"
    outfile = "index.html"
    template = "home.mako"
    

class ForumPage(Page):
    name = "Forum"
    target = "/forum/"
    outfile = "css/header_forum.html"
    template = "header_only.mako"
    

class DocsPage(Page):
    name = "Documentation"
    target = "/docs/"
    outfile = r"..\docs\source\_templates\header_docs.html"
    template = "header_only.mako"
    

class WikiPage(Page):
    name = "Wiki"
    target = "/wiki/"
    outfile = "css/header_wiki.html"
    template = "header_only.mako"
    

class DownloadPage(Page):
    name = "Downloads"
    target = "/downloads/"
    outfile = "downloads/index.html"
    template = "download.mako"
    
    

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
    for name in os.listdir(join(BASE_DIR, "downloads")):
        if name.lower().startswith("eventghost_"):
            if name.lower().endswith("_setup.exe"):
                path = join(BASE_DIR, "downloads", name)
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

def Main(url):
    
    myLookUp = TemplateLookup(directories=[abspath(join(builder.DATA_DIR, 'templates'))])

    for page in MENU_TABS:
        GLOBALS["CURRENT"] = page
        content = Template(
            filename=join(builder.DATA_DIR, "templates", page.template), 
            lookup=myLookUp
        ).render(**GLOBALS)
#        if os.path.splitext(page.template)[1] == ".rst":
#            print "is rst"
        open(join(BASE_DIR, page.outfile), "wt").write(content)
    
    #import BuildDocs
    #BuildDocs.Main(buildHtml=True)
     
    from SftpSync import SftpSync
    
    syncer = SftpSync(url)
    addFiles = [
        (join(BASE_DIR, "index.html"), "index.html"),
    ]
    syncer.Sync(BASE_DIR, addFiles)
    syncer.sftpClient.utime(syncer.remotePath + "wiki", None)
    syncer.ClearDirectory(
        syncer.remotePath + "forum/cache", 
        excludes=["index.htm", ".htaccess"]
    )
    syncer.Close()