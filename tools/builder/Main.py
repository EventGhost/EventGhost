import wx
import shutil
import threading
from os.path import join

import builder
import builder.StaticImports
import builder.Imports
import builder.PyExe
import builder.website
import builder.Upload

from builder.Utils import ExecutePy


def Main(mainDialog=None):
    """
    Main task of the script.
    """
    options = builder.config
    installer = builder.installer
    
    if options.svnUpdate:
        print "--- updating working copy from SVN"
        installer.UpdateSvn()
    installer.UpdateVersionFile()
    print "--- updating CHANGELOG.TXT"
    installer.UpdateChangeLog()
    if options.buildStaticImports:
        print "--- building StaticImports.py"
        builder.StaticImports.Main()
    if options.buildImports:
        print "--- building imports.py"
        builder.Imports.Main(builder.INCLUDED_MODULES, builder.EXCLUDED_MODULES)
    if options.buildHtmlDocs or options.buildChmDocs:
        print "--- building docs"
        args = []
        if options.buildHtmlDocs:
            args.append("buildHtml=True")
        if options.buildChmDocs:
            args.append("buildChm=True")
        args = ", ".join(args)
        ExecutePy(
            "import builder.Docs",
            "builder.Docs.Main(%s)" % args
        )
    if options.commitSvn:
        print "--- committing working copy to SVN"
        installer.CommitSvn()
    if options.buildSourceArchive:
        print "--- building source code archive"
        installer.CreateSourceArchive()
    if options.buildPyExe:
        print "--- building py.exe and pyw.exe"
        builder.PyExe.Main()
    if options.buildLib:
        print "--- building library files"
        installer.CreateLibrary()            
    if options.buildInstaller:
        print "--- building " + installer.outputBaseFilename
        installer.CreateInstaller()
    if options.upload and options.ftpUrl:
        print "--- uploading setup.exe"
        filename = join(installer.outputDir, installer.outputBaseFilename + ".exe")
        stopEvent = threading.Event()
        wx.CallAfter(
            builder.Upload.UploadDialog, 
            mainDialog, 
            filename, 
            options.ftpUrl,
            stopEvent
        )
        stopEvent.wait()
        dst = join(builder.WEBSITE_DIR, "downloads", installer.outputBaseFilename + ".exe")
        shutil.copyfile(filename, dst)
        shutil.copystat(filename, dst)
    if options.updateWebsite:
        print "--- updating website"
        builder.website.Main()
    print "--- All done!"
    wx.CallAfter(mainDialog.Close)
    

