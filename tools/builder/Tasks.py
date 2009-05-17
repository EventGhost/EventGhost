import sys
import shutil
import time
from os.path import join
import builder



class UpdateSvn(builder.Task):
    description = "Update from SVN"

    def DoTask(self):
        from builder.Utils import UpdateSvn
        UpdateSvn(self.buildSetup.sourceDir)



class UpdateVersionFile(builder.Task):
    """
    Update buildTime and revision for eg/Classes/VersionRevision.py
    """
    description = "Update version file"
    enabled = None

    def DoTask(self):
        from builder.Utils import GetSvnRevision
        import imp

        svnRevision = GetSvnRevision(self.buildSetup.sourceDir)
        outfile = open(join(self.buildSetup.tmpDir, "VersionRevision.py"), "wt")
        outfile.write("revision = %r\n" % svnRevision)
        outfile.write("buildTime = %f\n" % time.time())
        outfile.close()
        versionFilePath = join(self.buildSetup.sourceDir, "eg", "Classes", "Version.py")
        mod = imp.load_source("Version", versionFilePath)
        self.buildSetup.appVersion = mod.Version.base + (".r%s" % svnRevision)
        self.buildSetup.appNumericalVersion = mod.Version.base + ".%s" % svnRevision


class UpdateChangeLog(builder.Task):
    """
    Add a version header to CHANGELOG.TXT if needed.
    """
    description = "updating CHANGELOG.TXT"
    enabled = None

    def DoTask(self):
        path = join(self.buildSetup.sourceDir, "CHANGELOG.TXT")
        timeStr = time.strftime("%m/%d/%Y")
        header = "**%s (%s)**\n\n" % (self.buildSetup.appVersion, timeStr)
        infile = open(path, "r")
        data = infile.read(100) # read some data from the beginning
        if data.strip().startswith("**"):
            # no new lines, so skip the addition of a new header
            return
        data += infile.read() # read the remaining contents
        infile.close()
        outfile = open(path, "w+")
        outfile.write(header + data)
        outfile.close()



class BuildHtml(builder.Task):
    description = "Build HTML docs"

    def DoTask(self):
        import builder.Docs
        builder.Docs.Main(buildHtml=True)



class BuildChm(builder.Task):
    description = "Build CHM docs"

    def DoTask(self):
        import builder.Docs
        builder.Docs.Main(buildChm=True)



class CreateInstaller(builder.Task):
    description = "Build Setup.exe"

    def DoTask(self):
        self.buildSetup.CreateInstaller()



class Upload(builder.Task):
    description = "Upload through FTP"
    options = {"url": ""}

    def IsEnabled(self):
        return bool(self.options["url"])


    def DoTask(self):
        import builder.Upload
        buildSetup = self.builder.buildSetup
        filename = buildSetup.appName + "_" + buildSetup.appVersion + "_Setup.exe"
        src = join(buildSetup.outDir, filename)
        dst = join(buildSetup.websiteDir, "downloads", filename)
        builder.Upload.Upload(src, self.options["url"])
        shutil.copyfile(src, dst)
        shutil.copystat(src, dst)



class SyncWebsite(builder.Task):
    description = "Synchronize website"
    options = {"url": ""}

    def IsEnabled(self):
        return bool(self.options["url"])


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
from builder.CreateSourceArchive import CreateSourceArchive
from builder.CreatePyExe import CreatePyExe
from builder.CreateLibrary import CreateLibrary
from builder.CreateWebsite import CreateWebsite

TASKS = [
    UpdateSvn(),
    UpdateVersionFile(),
    UpdateChangeLog(),
    CreateStaticImports(),
    CreateImports(),
    BuildChm(),
    CreateSourceArchive(),
    CreatePyExe(),
    CreateLibrary(),
    CreateInstaller(),
    Upload(),
    CreateWebsite(),
    BuildHtml(),
    SyncWebsite(),
]


def Main():
    """
    Main task of the script.
    """
    for task in TASKS:
        if task.enabled is not False and task.IsEnabled():
            print "---", task.description
            task.DoTask()
    print "--- All done!"

