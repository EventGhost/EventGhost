import sys
import shutil
from os.path import join
import builder
from builder.Utils import ExecutePy

    
class UpdateSvn(builder.TaskBase):
    description = "Update from SVN"
    default = True
    option = "svnUpdate"
    
    def DoTask(self):
        builder.installer.UpdateSvn()



class UpdateVersionFile(builder.TaskBase):
    description = "Update version file"
    default = True
    option = None
    
    def DoTask(self):
        builder.installer.UpdateVersionFile()



class UpdateChangeLog(builder.TaskBase):
    description = "updating CHANGELOG.TXT"
    default = True
    option = None
    
    def DoTask(self):
        builder.installer.UpdateChangeLog()



class BuildHtml(builder.TaskBase):
    description = "Build HTML docs"
    default = True
    option = "buildHtmlDocs"
    
    def DoTask(self):
        ExecutePy(
            "import builder.Docs",
            "builder.Docs.Main(buildHtml=True)"
        )
        

class BuildChm(builder.TaskBase):
    description = "Build CHM docs"
    default = True
    option = "buildChmDocs"
    
    def DoTask(self):
        ExecutePy(
            "import builder.Docs",
            "builder.Docs.Main(buildChm=True)"
        )
        

class CreateSourceArchive(builder.TaskBase):
    description = "Build source archive"
    default = True
    option = "buildSourceArchive"
    
    def DoTask(self):
        builder.installer.CreateSourceArchive()
        

class CreateLibrary(builder.TaskBase):
    description = "Build lib%d%d" %sys.version_info[0:2]
    default = True
    option = "buildLib"
    
    def DoTask(self):
        builder.installer.CreateLibrary()
        

class CreateInstaller(builder.TaskBase):
    description = "Build Setup.exe"
    default = True
    option = "buildInstaller"
    
    def DoTask(self):
        builder.installer.CreateInstaller()
        

class Upload(builder.TaskBase):
    description = "Upload through FTP"
    default = True
    option = "upload"
    
    def IsEnabled(self):
        return bool(builder.config.ftpUrl)
    
    
    def DoTask(self):
        import builder.Upload
        installer = builder.installer
        filename = join(installer.outputDir, installer.outputBaseFilename + ".exe")
        builder.Upload.Upload(filename, builder.config.ftpUrl)
        dst = join(builder.WEBSITE_DIR, "downloads", installer.outputBaseFilename + ".exe")
        shutil.copyfile(filename, dst)
        shutil.copystat(filename, dst)
        

class UpdateWebsite(builder.TaskBase):
    description = "Update website"
    default = True
    option = "updateWebsite"
    
    def IsEnabled(self):
        return bool(builder.config.webUploadUrl)
    
    
    def DoTask(self):
        import builder.website
        builder.website.Main()
        

import builder.StaticImports
import builder.Imports
import builder.PyExe

TASKS = [
    UpdateSvn(),
    UpdateVersionFile(),
    UpdateChangeLog(),
    builder.StaticImports.Task(),
    builder.Imports.Task(),
    BuildHtml(),
    BuildChm(),
    CreateSourceArchive(),
    builder.PyExe.Task(),
    CreateLibrary(),
    CreateInstaller(),
    Upload(),
    UpdateWebsite(),
]


def Main():
    """
    Main task of the script.
    """
    for task in TASKS:
        if task.option is not None:
            enabled = getattr(builder.config, task.option)
        else:
            enabled = task.default
        if enabled and task.IsEnabled():
            print "---", task.description
            task.DoTask()
    print "--- All done!"
    

