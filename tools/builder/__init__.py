import sys
from os.path import abspath, dirname, join

SOURCE_DIR = abspath(join(dirname(__file__), "../.."))
WEBSITE_DIR = join(SOURCE_DIR, "website")
DATA_DIR = abspath(join(dirname(__file__), "Data"))
PYVERSION_STR = "%d%d" % sys.version_info[:2]
PYVERSION_DIR = join(DATA_DIR, "Python%s" % PYVERSION_STR)


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
    
    
from builder.Tasks import TASKS

from builder.Config import Config
config = Config(join(DATA_DIR, "Build.ini"))
