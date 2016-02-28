# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import warnings
import shutil
import glob
from string import digits
from os.path import join

from builder.InnoSetup import GetInnoCompilerPath
from builder.Utils import GetHtmlHelpCompilerPath
from builder.DllVersionInfo import GetFileVersion


class MissingDependency(Exception):
    pass
class WrongVersion(Exception):
    pass


def CompareVersion(actualVersion, wantedVersion):
    wantedParts = wantedVersion.split(".")
    actualParts = actualVersion.split(".")
    numParts = min(len(wantedParts), len(actualParts))
    for i in range(numParts):
        wantedPart = wantedParts[i]
        actualPart = actualParts[i]
        wantedPart = int(filter(lambda c: c in digits, wantedPart))
        actualPart = int(filter(lambda c: c in digits, actualPart))
        if wantedPart > actualPart:
            return -1
        elif wantedPart < actualPart:
            return 1
    return 0



class DependencyBase(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def Check(self):
        raise NotImplementedError



class ModuleDependency(DependencyBase):
    module = None
    version = None

    def Check(self):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                module = __import__(self.module)
        except ImportError:
            raise MissingDependency
        if hasattr(module, "__version__"):
            version = module.__version__
        elif hasattr(module, "VERSION"):
            version = module.VERSION
        elif hasattr(module, "version"):
            version = module.version
        else:
            raise Exception("Can't get version information")
        if type(version) != type(""):
            version = ".".join(str(x) for x in version)
        if CompareVersion(version, self.version) < 0:
            raise WrongVersion



class PyWin32Dependency(DependencyBase):
    name = "pywin32 (Mark Hammond's Win32All package)"
    version = "220"
    url = "pywin32 (Mark Hammond's Win32All package)"

    def Check(self):
        versionFilePath = join(
            sys.prefix, "lib/site-packages/pywin32.version.txt"
        )
        try:
            version = open(versionFilePath, "rt").readline().strip()
        except IOError:
            raise MissingDependency
        if CompareVersion(version, self.version) < 0:
            raise WrongVersion



class StacklessDependency(DependencyBase):
    name = "Stackless Python"
    version = "2.7.9"
    url = "http://www.stackless.com/"

    def Check(self):
        try:
            import stackless
        except:
            raise MissingDependency
        if CompareVersion("%d.%d.%d" % sys.version_info[:3], self.version) < 0:
            raise WrongVersion



class InnoSetupDependency(DependencyBase):
    name = "Inno Setup"
    version = "5.5.8"
    url = "http://www.innosetup.com/isinfo.php"

    def Check(self):
        if not GetInnoCompilerPath():
            raise MissingDependency



class HtmlHelpWorkshopDependency(DependencyBase):
    name = "HTML Help Workshop"
    version = "1.0"
    url = (
        "http://www.microsoft.com/Downloads/details.aspx?"
        "familyid=00535334-C8A6-452F-9AA0-D597D16580CC&displaylang=en"
    )

    def Check(self):
        if not GetHtmlHelpCompilerPath():
            raise MissingDependency



class DllDependency(DependencyBase):
    url = (
        "http://www.microsoft.com/downloads/details.aspx?"
        "displaylang=en&FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf"
    )

    def Check(self):
        path = join(self.buildSetup.sourceDir, self.name)
        wantedVersion = tuple(int(x) for x in self.version.split("."))
        if not os.path.exists(path) or GetFileVersion(path) != wantedVersion:
            self.TryCopy()
            if GetFileVersion(path) != wantedVersion:
                raise WrongVersion


    def TryCopy(self):
        winSxsDir = join(
            os.environ["SystemRoot"],
            "WinSxS",
            "x86_microsoft.vc90.crt_*_%s_*_*" % self.version,
            self.name
        )
        pathes = glob.glob(winSxsDir)
        if len(pathes) < 1:
            raise MissingDependency
        src = pathes[0]
        dst = join(self.buildSetup.sourceDir, self.name)
        shutil.copyfile(src, dst)
        shutil.copystat(src, dst)


DEPENDENCIES = [
    ModuleDependency(
        name = "pygit2",
        module = "pygit2",
        version = "0.23.3",
        url = "http://www.pygit2.org/",
    ),
    ModuleDependency(
        name = "wxPython",
        module = "wx",
        version = "2.8.12.1",
        url = "http://www.wxpython.org/",
    ),
    ModuleDependency(
        name = "py2exe",
        module = "py2exe",
        version = "0.6.9",
        url = "http://www.py2exe.org/",
    ),
    ModuleDependency(
        name = "PIL (Python Image Library)",
        module = "Image",
        version = "1.1.7",
        url = "http://www.pythonware.com/products/pil/",
    ),
    ModuleDependency(
        name = "comtypes package",
        module = "comtypes",
        version = "1.1.2",
        url = "http://sourceforge.net/projects/comtypes/"
    ),
    ModuleDependency(
        name = "ctypeslib package",
        module = "ctypeslib",
        version = "0.5.6",
        url = "http://pypi.python.org/pypi/ctypeslib/"
    ),
    ModuleDependency(
        name = "PyCrypto (Python Cryptography Toolkit)",
        module = "Crypto",
        version = "2.6.1",
        url = "http://www.dlitz.net/software/pycrypto/",
    ),
    ModuleDependency(
        name = "Sphinx (Python documentation generator)",
        module = "sphinx",
        version = "1.3.5",
        url = "http://sphinx.pocoo.org/",
    ),
    PyWin32Dependency(),
    StacklessDependency(),
    InnoSetupDependency(),
    HtmlHelpWorkshopDependency(),
    DllDependency(name="msvcm90.dll", version="9.0.21022.8"),
    DllDependency(name="msvcp90.dll", version="9.0.21022.8"),
    DllDependency(name="msvcr90.dll", version="9.0.21022.8"),
]


def CheckDependencies(buildSetup):
    isOK = True
    for dependency in DEPENDENCIES:
        dependency.buildSetup = buildSetup
        try:
            dependency.Check()
        except (WrongVersion, MissingDependency):
            if isOK:
                print "The following dependencies are missing:"
                isOK = False
            print "  *", dependency.name
            print "       Needed version:", dependency.version
            print "       Download URL:", dependency.url
    if not isOK:
        print "You need to install them first to run the build process!"
    return isOK

