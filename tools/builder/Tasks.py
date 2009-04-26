import sys
import shutil
import time
from os.path import join
import builder
from builder.Utils import ExecutePy

class TaskBase(object):
    value = None
    enabled = True
    
    @classmethod
    def GetId(cls):
        return cls.__module__ + "." + cls.__name__
    
    def IsEnabled(self):
        return True
    
    def DoTask(self):
        raise NotImplementedError
    
    
    
class UpdateSvn(TaskBase):
    description = "Update from SVN"
    
    def DoTask(self):
        from builder.Utils import UpdateSvn
        UpdateSvn(builder.SOURCE_DIR)



class UpdateVersionFile(TaskBase):
    """
    Update buildTime and revision for eg/Classes/VersionRevision.py
    """
    description = "Update version file"
    enabled = None
    
    def DoTask(self):
        from builder.Utils import GetSvnRevision
        import imp
        
        svnRevision = GetSvnRevision(builder.SOURCE_DIR)
        outfile = open(join(builder.TMP_DIR, "VersionRevision.py"), "wt")
        outfile.write("revision = %r\n" % svnRevision)
        outfile.write("buildTime = %f\n" % time.time())
        outfile.close()
        versionFilePath = join(builder.SOURCE_DIR, "eg/Classes/Version.py")
        mod = imp.load_source("Version", versionFilePath)
        builder.APP_VERSION = mod.Version.base + (".r%s" % svnRevision)



class UpdateChangeLog(TaskBase):
    """
    Add a version header to CHANGELOG.TXT if needed.
    """
    description = "updating CHANGELOG.TXT"
    enabled = None
    
    def DoTask(self):
        path = join(builder.SOURCE_DIR, "CHANGELOG.TXT")
        timeStr = time.strftime("%m/%d/%Y")
        header = "**%s (%s)**\n\n" % (builder.APP_VERSION, timeStr)
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



class BuildHtml(TaskBase):
    description = "Build HTML docs"
    
    def DoTask(self):
        ExecutePy(
            "import builder.Docs",
            "builder.Docs.Main(buildHtml=True)"
        )
        

class BuildChm(TaskBase):
    description = "Build CHM docs"
    
    def DoTask(self):
        ExecutePy(
            "import builder.Docs",
            "builder.Docs.Main(buildChm=True)"
        )
        

class CreateSourceArchive(TaskBase):
    description = "Build source archive"
    
    def DoTask(self):
        from builder.Utils import CreateSourceArchive
        CreateSourceArchive()
        


class CreateLibrary(TaskBase):
    description = "Build lib%d%d" %sys.version_info[0:2]
    
    def DoTask(self):
        import builder.Library
        builder.Library.CreateLibrary()
        
        

class CreateInstaller(TaskBase):
    description = "Build Setup.exe"
    
    def DoTask(self):
        builder.installer.CreateInstaller()
        
        

class Upload(TaskBase):
    description = "Upload through FTP"
    options = {"url": ""}
    
    def IsEnabled(self):
        return bool(self.options["url"])
    
    
    def DoTask(self):
        import builder.Upload
        filename = builder.APP_NAME + "_" + builder.APP_VERSION + "_Setup.exe"
        src = join(builder.OUT_DIR, filename)
        dst = join(builder.WEBSITE_DIR, "downloads", filename)
        builder.Upload.Upload(src, self.options["url"])
        shutil.copyfile(src, dst)
        shutil.copystat(src, dst)
        


class UpdateWebsite(TaskBase):
    description = "Update website"
    options = {"url": ""}
    
    def IsEnabled(self):
        return bool(self.options["url"])
    
    
    def DoTask(self):
        import builder.website
        builder.website.Main(self.options["url"])
        


class CreateStaticImports(TaskBase):
    description = "Create StaticImports.py"
    
    def DoTask(self):
        import builder.StaticImports
        builder.StaticImports.DoTask()
        


class CreateImports(TaskBase):
    description = "Create Imports.py"
    
    def DoTask(self):
        import builder.Imports
        builder.Imports.DoTask()
        


class BuildPyExe(TaskBase):
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
    

