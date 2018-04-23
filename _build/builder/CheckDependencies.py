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
import platform
import re
import sys
import warnings
from os.path import basename, exists, expandvars, join
from shutil import copy2
from string import digits

import os
import tempfile
from subprocess import Popen, PIPE

# Local imports
from builder import VirtualEnv
from builder.DllVersionInfo import GetFileVersion
from builder.InnoSetup import GetInnoCompilerPath
from builder.Utils import (
    GetEnvironmentVar, GetHtmlHelpCompilerPath, IsAdmin, StartProcess,
    WrapText,
)

temp_dir = tempfile.gettempdir()


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


class VersionLocationError(Exception):
    pass


class ModuleZipFileError(Exception):
    pass


class PyWin32EggError(Exception):
    pass


class DependencyBase(object):
    # name = None
    # version = None
    attr = None
    exact = False
    module = None
    package = None
    url = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def Check(self):
        raise NotImplementedError

    def Download(self):
        raise NotImplementedError


def install(url, file_name, options):
    from pip._vendor import requests

    response = requests.get(url)
    temp_file = os.path.join(temp_dir, file_name)

    with open(temp_file, 'wb') as f:
        f.write(response.content)

    if 'MsiExec' in options:
        proc = Popen(options % temp_file, stdout=PIPE, stderr=PIPE)
    else:
        proc = Popen(temp_file + options, stdout=PIPE, stderr=PIPE)

    stderr, stdout = proc.communicate()

    print stderr
    print stdout

    os.remove(temp_file)


def pip_install(name, mod, pkg, version=None):
    try:
        __import__(mod)
        print 'upgrading %s....' % name
        upgrade = '--upgrade'
    except ImportError:
        print 'installing %s....' % name
        upgrade = ''

    if version:
        if '%s' in pkg:
            pkg %= version
        else:
            pkg += '==' + version

        proc = Popen(
            sys.executable +
            ' -m pip install %s %s' % (upgrade, pkg)
        )
    else:
        proc = Popen(
            sys.executable +
            ' -m pip install %s %s' % (upgrade, pkg)
        )

    proc.communicate()

    for key in sys.modules.keys()[:]:
        if key.startswith(mod):
            try:
                del sys.modules[key]
            except KeyError:
                pass
    import site
    reload(site)


def easy_install(name, mod, pkg, version=None):
    print 'installing %s....' % name

    if version:
        proc = Popen(
            sys.executable +
            ' -m easy_install --always-unzip %s==%s' % (pkg, version)
        )
    else:
        proc = Popen(
            sys.executable +
            ' -m easy_install --always-unzip %s' % pkg
        )


    proc.communicate()
    for key in sys.modules.keys()[:]:
        if key.startswith(mod):
            try:
                del sys.modules[key]
            except KeyError:
                pass

    import pkg_resources
    try:
        pkg_resources.require(mod)
    except pkg_resources.DistributionNotFound:
        import site
        reload(site)


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
                    raise WrongVersion(self.name)
                else:
                    dest = join(self.buildSetup.sourceDir, basename(file))
                    copy2(file, dest)
        else:
            raise MissingDependency(self.name)


class GitDependency(DependencyBase):
    name = "Git"
    version = "2.8.0"
    package = "git"
    url = "https://git-scm.com/download/win"

    def Check(self):
        if not (os.system('"%s" --version >NUL 2>NUL' % GetGitPath()) == 0):
            raise MissingDependency(self.name)

    def Download(self):
        import platform
        url = (
            'https://github.com/git-for-windows/git/releases/'
            'download/v2.16.2.windows.1/Git-2.16.2-{0}-bit.exe'
        ).format('64' if platform.machine().endswith('64') else '32')
        install(
            url,
            'Git-2.16.2-{0}-bit.exe',
            (
                '/SP /VERYSILENT /SUPPRESSMSGBOXES '
                '/NORESTART /RESTARTAPPLICATIONS /NOICONS'
            )
        )


class HtmlHelpWorkshopDependency(DependencyBase):
    name = "HTML Help Workshop"
    version = "1.32"
    package = "html-help-workshop"
    url = (
        "https://download.microsoft.com/download"
        "/0/A/9/0A939EF6-E31C-430F-A3DF-DFAE7960D564/htmlhelp.exe"
    )

    def Check(self):
        if not GetHtmlHelpCompilerPath():
            raise MissingDependency(self.name)

    def Download(self):
        install(
            'http://go.microsoft.com/fwlink/p/?linkid=14188',
            'htmlhelp.exe',
            ' /q'
        )


class InnoSetupDependency(DependencyBase):
    name = "Inno Setup"
    version = "5.5.8"
    package = "innosetup"
    #url = "http://www.innosetup.com/isdl.php"
    url = "http://www.innosetup.com/download.php/is-unicode.exe"

    def Check(self):
        if not GetInnoCompilerPath():
            raise MissingDependency(self.name)

    def Download(self):
        install(
            'http://files.jrsoftware.org/is/5/innosetup-5.5.9-unicode.exe',
            'innosetup-5.5.9-unicode.exe',
            ' /SP /VERYSILENT /SUPPRESSMSGBOXES /NORESTART '
            '/RESTARTAPPLICATIONS /NOICONS'
        )


class VCRedistDependency(DllDependency):
    name = "Microsoft Visual C++ Redistributable"
    package = "vcredist2008"
    url = "https://www.microsoft.com/download/details.aspx?id=29"

    def Download(self):
        install(
            (
                'https://download.microsoft.com/download/1/1/1'
                '/1116b75a-9ec3-481a-a3c8-1777b5381140/vcredist_x86.exe'
            ),
            'vcredist_x86.exe',
            ' /quiet /passive /qn /norestart'
        )


class ModuleDependency(DependencyBase):
    def Check(self):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                module = __import__(self.module)
        except ImportError:
            raise MissingDependency(self.name)
        if self.attr and hasattr(module, self.attr):
            version = getattr(module, self.attr)
        elif hasattr(module, "__version__"):
            version = module.__version__
        elif hasattr(module, "VERSION"):
            version = module.VERSION
        elif hasattr(module, "version"):
            version = module.version
        else:
            for key in sys.modules.keys()[:]:
                if key.startswith('pip'):
                    try:
                        del sys.modules[key]
                    except KeyError:
                        pass

            import pip

            for p in pip.get_installed_distributions():
                if p.project_name in (
                    self.name,
                    self.name.lower(),
                    self.module
                ):
                    version = p.version
                    break
            else:
                raise VersionLocationError(
                    "Can't get version information for "
                    "the package {0} ".format(self.name)
                )

        if 'egg' in module.__file__:
            if os.path.isfile(os.path.dirname(module.__file__)):
                raise ModuleZipFileError(
                    'Please reinstall {0} using the command "easy_install'
                    ' --always-unzip {0}"'.format(self.mod)
                )

        if not isinstance(version, basestring):
            version = ".".join(str(x) for x in version)
        if CompareVersion(version, self.version) < 0:
            raise WrongVersion(self.name)

    def Download(self):
        pip_install(self.name, self.module, self.package, self.version)


class WXPythonDependency(ModuleDependency):
    name = "wxPython"
    module = "wx"
    version = "3.0.2.0"
    package = 'wxPython'
    url = (
        'http://downloads.sourceforge.net/wxpython/'
        'wxPython3.0-win32-3.0.2.0-py27.exe'
    )

    def Download(self):
        install(
            (
                'http://downloads.sourceforge.net/wxpython/'
                'wxPython3.0-win32-3.0.2.0-py27.exe'
            ),
            'wxPython3.0-win32-3.0.2.0-py27.exe',
            ' /VERYSILENT /SUPPRESSMSGBOXES'
        )


class PyWin32Dependency(ModuleDependency):
    name = "pywin32"
    module = "pywin32"
    version = "223"
    package = "pywin32"

    def Check(self):
        site_packages_path = join(sys.prefix, "lib/site-packages/")
        site_packages = os.listdir(site_packages_path)

        if 'pywin32.version.txt' in site_packages:
            versionFilePath = join(
                site_packages_path,
                'pywin32.version.txt'
            )
        else:
            for item in site_packages:
                if item.startswith('pywin32') and item.endswith('egg'):
                    raise PyWin32EggError(
                        'Please reinstall pywin32 using "pip install pywin32"'
                    )
            else:
                raise MissingDependency(self.name)

        try:
            version = open(versionFilePath, "rt").readline().strip()
        except IOError:
            raise MissingDependency(self.name)
        if CompareVersion(version, self.version) < 0:
            raise WrongVersion(self.name)


class StacklessDependency(DependencyBase):
    name = "Stackless Python"
    version = "2.7.9"
    url = "http://www.stackless.com/binaries/python-2.7.9150-stackless.msi"

    def Check(self):
        try:
            import stackless  # NOQA
        except:
            raise MissingDependency(self.name)
        if CompareVersion("%d.%d.%d" % sys.version_info[:3], self.version) < 0:
            raise WrongVersion(self.name)


class SphinxDependency(ModuleDependency):
    name = "Sphinx"
    module = "sphinx"
    package = 'sphinx'
    version = "1.7.2"

    def Download(self):
        pip_install(self.name, self.module, self.package, self.version)

        import jinja2

        jinja_path = os.path.dirname(jinja2.__file__)

        for path, dirs, files in os.walk(jinja_path):
            head, tail = os.path.split(path)
            parent_mod = []
            while tail != 'jinja2':
                parent_mod += [tail]
                head, tail = os.path.split(head)

            parent_mod = '.'.join(
                sorted(parent_mod + ['jinja2'], reverse=True)
            )

            for mod_name in files:
                if mod_name.endswith('.py'):
                    try:
                        __import__(parent_mod + '.' + mod_name[:-3])
                    except SyntaxError:
                        os.remove(os.path.join(path, mod_name))
                    except:
                        pass

        for key in sys.modules.keys()[:]:
            if key.startswith('jinja2'):
                try:
                    del sys.modules[key]
                except KeyError:
                    pass


class PIPDependency(ModuleDependency):
    name = 'PIP'
    module = 'pip'
    package = 'pip'
    version = '9.0.3'

    def Download(self):
        try:
            import pip
            if pip.__version__ != self.version:
                pip_install(self.name, self.module, self.package, self.version)
        except ImportError:
            easy_install(self.name, self.module, self.package, self.version)


DEPENDENCIES = [
    StacklessDependency(),
    PIPDependency(),
    HtmlHelpWorkshopDependency(),
    InnoSetupDependency(),
    VCRedistDependency(),
    ModuleDependency(
        name='Setuptools',
        module='setuptools',
        package='setuptools',
        version='39.0.1'
    ),
    SphinxDependency(),
    PyWin32Dependency(),
    ModuleDependency(
        name="CommonMark",
        module="CommonMark",
        package='CommonMark',
        version="0.7.5",
    ),
    ModuleDependency(
        name="comtypes",
        module="comtypes",
        package='comtypes',
        version="1.1.4",
    ),
    ModuleDependency(
        name="ctypeslib2",
        module="ctypeslib",
        package="ctypeslib2",
        version="2.2.1",
    ),
    ModuleDependency(
        name="future",
        module="future",
        package='future',
        version="0.16.0",
    ),
    #GitDependency(),
    ModuleDependency(
        name="Pillow",
        module="PIL",
        attr="PILLOW_VERSION",
        package='Pillow',
        version="5.1.0",
    ),
    ModuleDependency(
        name="py2exe_py2",
        module="py2exe",
        package='py2exe_py2',
        version="0.6.9",
    ),
    ModuleDependency(
        name="PyCrypto",
        module="Crypto",
        package='pycrypto',
        version="2.6.1",
        url=(
            "https://eventghost.github.io/dist/dependencies/"
            "pycrypto-2.6.1-cp27-none-win32.whl"
        ),
    ),
    WXPythonDependency()
]


def CheckDependencies(buildSetup):
    failedDeps = []

    class DepFailedError(Exception):
        pass

    def check_dep():
        try:
            dep.Check()
        except (
            MissingDependency,
            WrongVersion,
            VersionLocationError,
            ModuleZipFileError,
            PyWin32EggError,
        ):
            import traceback
            raise DepFailedError(traceback.format_exc())

    for dep in DEPENDENCIES:
        dep.buildSetup = buildSetup

        try:
            check_dep()
        except DepFailedError:
            if buildSetup.download_dependencies:
                dep.Download()
                check_dep()
            else:
                raise

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
