# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import glob
import os
import pip
import platform
import re
import sys
import warnings
from os.path import basename, exists, expandvars, join
from pip._vendor import requests
from shutil import copy2
from string import digits

# Local imports
from builder import VirtualEnv
from builder.DllVersionInfo import GetFileVersion
from builder.InnoSetup import GetInnoCompilerPath
from builder.Utils import (
    GetEnvironmentVar, GetHtmlHelpCompilerPath, IsAdmin, StartProcess,
    WrapText,
)

# Exceptions
class MissingChocolatey(Exception):
    pass
class MissingDependency(Exception):
    pass
class MissingInstallMethod(Exception):
    pass
class MissingPip(Exception):
    pass
class MissingPowerShell(Exception):
    pass
class WrongVersion(Exception):
    pass

class DependencyBase(object):
    #name = None
    #version = None
    attr = None
    exact = False
    module = None
    package = None
    url = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def Check(self):
        raise NotImplementedError


class DllDependency(DependencyBase):
    def Check(self):
        with open(join(self.buildSetup.pyVersionDir, "Manifest.xml")) as f:
            manifest = f.read()
        match = re.search(
            'name="(?P<name>.+\.CRT)"\n'
            '\s*version="(?P<ver>.+)"\n'
            '\s*processorArchitecture="(?P<arch>.+)"',
            manifest
        )
        self.exact = True
        self.version = match.group("ver")
        wantedVersion = tuple(int(x) for x in self.version.split("."))

        files = glob.glob(
            join(
                os.environ["SystemRoot"],
                "WinSxS",
                "{2}_{0}_*_{1}_*_*".format(
                    *match.groups()
                ),
                "*.dll",
            )
        )

        if len(files):
            for file in files:
                if GetFileVersion(file) != wantedVersion:
                    raise WrongVersion
                else:
                    dest = join(self.buildSetup.sourceDir, basename(file))
                    copy2(file, dest)
        else:
            raise MissingDependency


class GitDependency(DependencyBase):
    name = "Git"
    version = "2.8.0"
    package = "git"
    url = "https://git-scm.com/download/win"

    def Check(self):
        if not (os.system('"%s" --version >NUL 2>NUL' % GetGitPath()) == 0):
            raise MissingDependency


class HtmlHelpWorkshopDependency(DependencyBase):
    name = "HTML Help Workshop"
    version = "1.32"
    package = "html-help-workshop"
    #url = "https://www.microsoft.com/download/details.aspx?id=21138"
    url = (
        "https://download.microsoft.com/download"
        "/0/A/9/0A939EF6-E31C-430F-A3DF-DFAE7960D564/htmlhelp.exe"
    )

    def Check(self):
        if not GetHtmlHelpCompilerPath():
            raise MissingDependency


class InnoSetupDependency(DependencyBase):
    name = "Inno Setup"
    version = "5.5.8"
    package = "innosetup"
    #url = "http://www.innosetup.com/isdl.php"
    url = "http://www.innosetup.com/download.php/is-unicode.exe"

    def Check(self):
        if not GetInnoCompilerPath():
            raise MissingDependency


class ModuleDependency(DependencyBase):
    def Check(self):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                module = __import__(self.module)
        except ImportError:
            raise MissingDependency
        if self.attr and hasattr(module, self.attr):
            version = getattr(module, self.attr)
        elif hasattr(module, "__version__"):
            version = module.__version__
        elif hasattr(module, "VERSION"):
            version = module.VERSION
        elif hasattr(module, "version"):
            version = module.version
        else:
            result = [
                p.version
                for p in pip.get_installed_distributions()
                if str(p).startswith(self.name + " ")
            ]
            if result:
                version = result[0]
            else:
                raise Exception("Can't get version information")
        if not isinstance(version, basestring):
            version = ".".join(str(x) for x in version)
        if CompareVersion(version, self.version) < 0:
            raise WrongVersion


class PyWin32Dependency(DependencyBase):
    name = "pywin32"
    version = "220"
    url = "https://eventghost.github.io/dist/dependencies/pywin32-220-cp27-none-win32.whl"

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
    url = "http://www.stackless.com/binaries/python-2.7.9150-stackless.msi"

    def Check(self):
        try:
            import stackless  # NOQA
        except:
            raise MissingDependency
        if CompareVersion("%d.%d.%d" % sys.version_info[:3], self.version) < 0:
            raise WrongVersion


DEPENDENCIES = [
    ModuleDependency(
        name = "CommonMark",
        module = "CommonMark",
        version = "0.7.0",
    ),
    ModuleDependency(
        name = "comtypes",
        module = "comtypes",
        version = "1.1.2",
    ),
    ModuleDependency(
        name = "ctypeslib",
        module = "ctypeslib",
        version = "0.5.6",
        url = "https://eventghost.github.io/dist/dependencies/ctypeslib-0.5.6-cp27-none-any.whl"
    ),
    ModuleDependency(
        name = "future",
        module = "future",
        version = "0.15.2",
    ),
    #GitDependency(),
    HtmlHelpWorkshopDependency(),
    InnoSetupDependency(),
    DllDependency(
        name="Microsoft Visual C++ Redistributable",
        package="vcredist2008",
        #url = "https://www.microsoft.com/download/details.aspx?id=29",
        url = (
            "https://download.microsoft.com/download"
            "/1/1/1/1116b75a-9ec3-481a-a3c8-1777b5381140/vcredist_x86.exe"
        ),
    ),
    ModuleDependency(
        name = "Pillow",
        module = "PIL",
        attr = "PILLOW_VERSION",
        version = "3.1.1",
    ),
    ModuleDependency(
        name = "py2exe_py2",
        module = "py2exe",
        version = "0.6.9",
    ),
    ModuleDependency(
        name = "PyCrypto",
        module = "Crypto",
        version = "2.6.1",
        url = "https://eventghost.github.io/dist/dependencies/pycrypto-2.6.1-cp27-none-win32.whl",
    ),
    PyWin32Dependency(),
    ModuleDependency(
        name = "Sphinx",
        module = "sphinx",
        version = "1.3.5",
    ),
    StacklessDependency(),
    ModuleDependency(
        name = "wxPython",
        module = "wx",
        version = "3.0.2.0",
        url = "https://eventghost.github.io/dist/dependencies/wxPython-3.0.2.0-cp27-none-win32.whl",
    ),
]

def CheckDependencies(buildSetup):
    failedDeps = []

    for dep in DEPENDENCIES:
        dep.buildSetup = buildSetup
        try:
            dep.Check()
        except (WrongVersion, MissingDependency):
            failedDeps.append(dep)

    if failedDeps and buildSetup.args.make_env and not os.environ.get("_REST"):
        if not IsAdmin():
            print WrapText(
                "ERROR: Can't create virtual environment from a command "
                "prompt without administrative privileges."
            )
            return False

        if not VirtualEnv.Running():
            if not VirtualEnv.Exists():
                print "Creating our virtual environment..."
                CreateVirtualEnv()
                print ""
            VirtualEnv.Activate()

        for dep in failedDeps[:]:
            print "Installing %s..." % dep.name
            try:
                if InstallDependency(dep):  #and dep.Check():
                    failedDeps.remove(dep)
                else:
                    print "ERROR: Installation of %s failed!" % dep.name
            except MissingChocolatey:
                print WrapText(
                    "ERROR: To complete installation of this package, I need "
                    "package manager Chocolatey, which wasn't found and "
                    "couldn't be installed automatically. Please install it "
                    "by hand and try again."
                )
            except MissingPip:
                print WrapText(
                    "ERROR: To complete installation of this package, I need "
                    "package manager pip, which wasn't found. Note that "
                    "all versions of Python capable of building EventGhost "
                    "come bundled with pip, so please install a supported "
                    "version of Python and try again."
                )
            except MissingPowerShell:
                print WrapText(
                    "ERROR: To complete installation of this package, I need "
                    "package manager Chocolatey, which can't be installed "
                    "without PowerShell. Please install PowerShell by hand "
                    "and try again."
                )
            print ""
        VirtualEnv.Restart()

    if failedDeps:
        print WrapText(
            "Before we can continue, the following dependencies must "
            "be installed:"
        )
        print ""
        for dep in failedDeps:
            print "  *", dep.name, dep.version
            if dep.url:
                print "    Link:", dep.url
            print ""
        print WrapText(
            "Dependencies without an associated URL can be installed via "
            "`pip install [package-name]`. Dependencies in .whl format "
            "can be installed via `pip install [url]`. All other dependencies "
            "will need to be installed manually or via Chocolatey "
            "<https://chocolatey.org/>."
        )
        if not buildSetup.args.make_env:
            print ""
            print WrapText(
                "Alternately, from a command prompt with administrative "
                "privileges, I can try to create a virtual environment for "
                "you that satisfies all dependencies via `%s %s --make-env`."
                % (basename(sys.executable).split(".")[0], sys.argv[0])
            )
    return not failedDeps

def Choco(*args):
    choco = GetChocolateyPath()
    if not choco:
        try:
            if not (StartProcess(
                "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-Command", "iex ((new-object net.webclient).DownloadString"
                "('https://chocolatey.org/install.ps1'))"
            ) == 0):
                raise MissingChocolatey
        except WindowsError:
            raise MissingPowerShell

    choco = GetChocolateyPath()
    args = list(args) + ["-f", "-y"]
    return (StartProcess(choco, *args) == 0)

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

def CreateVirtualEnv():
    # These files will be replaced by virtualenv. We don't want that.
    backups = [
        join(VirtualEnv.PATH, "Lib", "distutils", "__init__.py"),
        join(VirtualEnv.PATH, "Lib", "site.py"),
    ]

    # Install virtualenv and virtualenvwrapper.
    #Pip("install", "pip", "-q")
    Pip("install", "virtualenvwrapper-win", "-q")

    # Install Stackless Python in virtualenv folder.
    url = [d.url for d in DEPENDENCIES if d.name == "Stackless Python"][0]
    file = DownloadFile(url)
    InstallMSI(file, VirtualEnv.PATH)
    os.unlink(file)

    # Backup stock files.
    for f in backups:
        copy2(f, f + ".bak")

    # Create virtualenv on top of Stackless Python.
    result = (StartProcess(
        sys.executable,
        "-m",
        "virtualenv",
        "--python=%s" % join(VirtualEnv.PATH, "python.exe"),
        VirtualEnv.PATH,
    ) == 0)

    # Restore stock files.
    for f in backups:
        os.unlink(f)
        os.rename(f + ".bak", f)

    # Start in build folder when virtualenv activated manually.
    with open(join(VirtualEnv.PATH, ".project"), "w") as f:
        f.write(os.getcwd())

    return result

def DownloadFile(url, path = "%TEMP%"):
    file = expandvars(join(path, basename(url.split("?")[0])))
    r = requests.get(url, stream=True)
    with open(file, "wb") as f:
        for chunk in r.iter_content(chunk_size=16384):
            if chunk:
                f.write(chunk)
    return file

def GetChocolateyPath():
    path = join(
        GetEnvironmentVar("ChocolateyInstall"),
        "bin",
        "choco.exe",
    )
    return path if exists(path) else ""

def GetGitPath():
    path = ""
    for p in GetEnvironmentVar("PATH").split(os.pathsep):
        if "\\Git\\" in p:
            path = join(p, "git.exe")
    return path if exists(path) else ""

def InstallDependency(dep):
    if dep.name == "Stackless Python":
        return dep.Check()
    elif not dep.url and not dep.package:
        package = dep.name + ("==" + dep.version if dep.exact else "")
        return Pip("install", package)
    elif dep.url and dep.url.endswith(".whl"):
        return Pip("install", dep.url)
    elif dep.package:
        args = []
        if dep.exact:
            args.append("--version=%s" % dep.version)
            if platform.architecture()[0] == "32bit":
                args.append("--x86")
        return Choco("install", dep.package, *args)
    else:
        raise MissingInstallMethod

def InstallMSI(file, path):
    file = file if exists(file) else DownloadFile(file)
    return (StartProcess(
        "msiexec",
        "/a",
        file,
        "/qb",
        "TARGETDIR=%s" % path,
    ) == 0)

def Pip(*args):
    args = list(args)
    if args[0].lower() == "install":
        args += ["-U"]
    elif args[0].lower() == "uninstall":
        args += ["-y"]

    try:
        return (StartProcess(sys.executable, "-m", "pip", *args) == 0)
    except WindowsError:
        raise MissingPip
