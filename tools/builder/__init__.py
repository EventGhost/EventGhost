import sys
import tempfile
import atexit
import shutil
from os.path import abspath, dirname, join


class Task(object):
    value = None
    visible = True
    enabled = True
    activated = True
    
    def __init__(self, buildSetup):
        self.buildSetup = buildSetup
        
    def Setup(self):
        pass

    @classmethod
    def GetId(cls):
        return cls.__module__ + "." + cls.__name__

    def DoTask(self):
        raise NotImplementedError



class Builder(object):
    
    def __init__(self):
        from CheckDependencies import CheckDependencies
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
        if not CheckDependencies(self):
            sys.exit(1)
        self.tmpDir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, self.tmpDir)
        self.appName = self.name
        
        
    def RunGui(self):
        from builder.Tasks import TASKS
        self.tasks = [task(self) for task in TASKS]
        from builder.Config import Config
        self.config = Config(self, join(self.dataDir, "Build.ini"))
        for task in self.tasks:
            task.Setup()
        import builder.Gui
        builder.Gui.Main(self)

