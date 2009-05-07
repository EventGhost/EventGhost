import sys
import tempfile
import atexit
import shutil
from os.path import abspath, dirname, join

SOURCE_DIR = abspath(join(dirname(__file__), "../.."))
WEBSITE_DIR = join(SOURCE_DIR, "website")
DATA_DIR = abspath(join(dirname(__file__), "Data"))
PYVERSION_STR = "%d%d" % sys.version_info[:2]
PYVERSION_DIR = join(DATA_DIR, "Python%s" % PYVERSION_STR)
LIBRARY_NAME = "lib%s" % PYVERSION_STR
LIBRARY_DIR = join(SOURCE_DIR, LIBRARY_NAME)
OUT_DIR = abspath(join(SOURCE_DIR, ".."))

TMP_DIR = tempfile.mkdtemp()
atexit.register(shutil.rmtree, TMP_DIR)


from builder.Config import Config
config = Config(join(DATA_DIR, "Build.ini"))

