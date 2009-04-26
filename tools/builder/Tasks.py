import sys
import shutil
from os.path import join
import builder
from builder.Utils import ExecutePy

    
class UpdateSvn(builder.TaskBase):
    description = "Update from SVN"
    
    def DoTask(self):
        builder.installer.UpdateSvn()



class UpdateVersionFile(builder.TaskBase):
    """
    Update buildTime and revision for eg/Classes/VersionRevision.py
    """
    description = "Update version file"
    enabled = None
    
    def DoTask(self):
        builder.installer.UpdateVersionFile()



class UpdateChangeLog(builder.TaskBase):
    """
    Add a version header to CHANGELOG.TXT if needed.
    """
    description = "updating CHANGELOG.TXT"
    enabled = None
    
    def DoTask(self):
        builder.installer.UpdateChangeLog()



class BuildHtml(builder.TaskBase):
    description = "Build HTML docs"
    
    def DoTask(self):
        ExecutePy(
            "import builder.Docs",
            "builder.Docs.Main(buildHtml=True)"
        )
        

class BuildChm(builder.TaskBase):
    description = "Build CHM docs"
    
    def DoTask(self):
        ExecutePy(
            "import builder.Docs",
            "builder.Docs.Main(buildChm=True)"
        )
        

class CreateSourceArchive(builder.TaskBase):
    description = "Build source archive"
    
    def DoTask(self):
        builder.installer.CreateSourceArchive()
        


class CreateLibrary(builder.TaskBase):
    description = "Build lib%d%d" %sys.version_info[0:2]
    
    def DoTask(self):
        builder.installer.CreateLibrary()
        
        

class CreateInstaller(builder.TaskBase):
    description = "Build Setup.exe"
    
    def DoTask(self):
        builder.installer.CreateInstaller()
        
        

class Upload(builder.TaskBase):
    description = "Upload through FTP"
    options = {"url": ""}
    
    def IsEnabled(self):
        return bool(self.options["url"])
    
    
    def DoTask(self):
        import builder.Upload
        installer = builder.installer
        filename = join(installer.outputDir, installer.outputBaseFilename + ".exe")
        builder.Upload.Upload(filename, self.options["url"])
        dst = join(builder.WEBSITE_DIR, "downloads", installer.outputBaseFilename + ".exe")
        shutil.copyfile(filename, dst)
        shutil.copystat(filename, dst)
        


class UpdateWebsite(builder.TaskBase):
    description = "Update website"
    options = {"url": ""}
    
    def IsEnabled(self):
        return bool(self.options["url"])
    
    
    def DoTask(self):
        import builder.website
        builder.website.Main(self.options["url"])
        


class CreateStaticImports(builder.TaskBase):
    description = "Create StaticImports.py"
    
    def DoTask(self):
        import builder.StaticImports
        builder.StaticImports.DoTask()
        


class CreateImports(builder.TaskBase):
    description = "Create Imports.py"
    
    def DoTask(self):
        import builder.Imports
        builder.Imports.DoTask()
        


class BuildPyExe(builder.TaskBase):
    description = "Build py.exe and pyw.exe"
    
    def DoTask(self):
        import builder.PyExe
        builder.PyExe.DoTask()
        


TASKS = [
    UpdateSvn(),
    UpdateVersionFile(),
    UpdateChangeLog(),
    CreateStaticImports(),
    CreateImports(),
    BuildHtml(),
    BuildChm(),
    CreateSourceArchive(),
    BuildPyExe(),
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
        if task.enabled is not False and task.IsEnabled():
            print "---", task.description
            task.DoTask()
    print "--- All done!"
    

