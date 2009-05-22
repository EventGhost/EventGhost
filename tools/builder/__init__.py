import sys
import tempfile
import atexit
import shutil
from os.path import abspath, dirname, join


class Task(object):
    value = None
    enabled = True
    buildSetup = None
    
    @classmethod
    def GetId(cls):
        return cls.__module__ + "." + cls.__name__

    def IsEnabled(self):
        return True

    def DoTask(self):
        raise NotImplementedError



class Builder(object):
    
    def __init__(self):
        from CheckDependencies import CheckDependencies
        if not CheckDependencies():
            sys.exit(1)
        global buildSetup
        Task.buildSetup = self
        buildSetup = self
        self.sourceDir = abspath(join(dirname(__file__), "../.."))
        self.websiteDir = join(self.sourceDir, "website")
        self.dataDir = abspath(join(dirname(__file__), "Data"))
        self.pyVersionStr = "%d%d" % sys.version_info[:2]
        self.pyVersionDir = join(self.dataDir, "Python%s" % self.pyVersionStr)
        self.libraryName = "lib%s" % self.pyVersionStr
        self.libraryDir = join(self.sourceDir, self.libraryName)
        self.outDir = abspath(join(self.sourceDir, ".."))
        self.tmpDir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, self.tmpDir)
        self.appName = self.name
        from builder.Config import Config
        self.config = Config(join(self.dataDir, "Build.ini"))
        
        
    def RunGui(self):
        import builder.Gui
        builder.Gui.Main(self)

