import sys
from os.path import abspath, dirname, join

SOURCE_DIR = abspath(join(dirname(__file__), "../.."))
WEBSITE_DIR = join(SOURCE_DIR, "website")
DATA_DIR = abspath(join(dirname(__file__), "Data"))
PYVERSION_DIR = join(DATA_DIR, "Python%d%d" % sys.version_info[:2])

DEFAULT_OPTIONS = (
    ("svnUpdate", "Update from SVN", True),
    ("includeNoIncludePlugins", "Include 'noinclude' plugins", False),
    ("buildStaticImports", "Build StaticImports.py", True),
    ("buildImports", "Build imports.py", True),
    ("buildSourceArchive", "Build source archive", True),
    ("buildHtmlDocs", "Build HTML docs", True),
    ("buildChmDocs", "Build CHM docs", True),
    ("buildPyExe", "Build py.exe and pyw.exe", True),
    ("buildLib", "Build lib%d%d" %sys.version_info[0:2], True),
    ("buildInstaller", "Build Setup.exe", True),
    ("commitSvn", "SVN commit", False),
    ("upload", "Upload through FTP", False),
    ("updateWebsite", "Update website", False),
    ("ftpUrl", "", ""),
    ("webUploadUrl", "", ""),
)

from builder.Config import Config
config = Config(join(DATA_DIR, "Build.ini"))