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


# PackageInstaller:
# this module will change the default behavior for
# pip. It will check to see if the calling class is either a Python Script,
# Python Command, or from the Shell. And if not it will not allow for pip
# to work restricting all installations to be controlled by EG
# **Added by K 8.15.2016**


import os
import wx
import sys
import site
import inspect
import traceback

from cStringIO import StringIO

# Local imports
import eg

USER_BASE = os.path.join(
    os.environ['PROGRAMDATA'],
    'EventGhost',
    'lib%d%d' % sys.version_info[:2]
)

USER_SITE = os.path.join(
    USER_BASE,
    'site-packages'
)

USER_SCRIPTS = os.path.join(
    USER_BASE,
    'Scripts'
)

class Config(eg.PersistentData):

    if eg.startupArguments.isMain:
        site.USER_BASE = USER_BASE
        site.USER_SITE = USER_SITE

        if not os.path.exists(USER_SITE):
            os.makedirs(USER_SITE)
        if not os.path.exists(USER_SCRIPTS):
            os.makedirs(USER_SCRIPTS)

        if USER_SITE not in sys.path:
            sys.path.append(USER_SITE)

        site.addsitedir(USER_SITE)

        site_packages_directory = USER_SITE
        script_directory = USER_SCRIPTS
        site_packages = tuple(os.listdir(USER_SITE))
        scripts = tuple(os.listdir(USER_SCRIPTS))
    else:
        site_packages_directory = None
        script_directory = None
        site_packages = None
        scripts = None


class Text(eg.TranslatableStrings):
    unauthHeader1 = (
        '%s is not allowed to access the package installation functions.\n'
    )
    unauthHeader2 = (
        'You are not allowed to access the package installation functions\n'
    )
    unauthFooter = (
        'Please use either a Python Shell, Python Script or Python Command\n'
        'to run the eg.Utils.Package.(Install/Uninstall/Upgrade) function'
    )
    unauthError1 = unauthHeader1 + unauthFooter
    unauthError2 = unauthHeader2 + unauthFooter

    start = 'Starting %s process for package %s'
    check = 'Checking currently installed packages'
    sucess = (
        'Finished %s for package %s.\n'
        'A restart of EventGhost may be needed for package %s.'
    )
    failed = 'Package %s failed for package %s'
    permissions = (
        'This may cause EventGhost to show not responding.\n'
        'Checking permissions'
    )
    allowedError = 'WindowsError: [Error 5]'

    class upgrade:
        name = 'Upgrade'
        err1 = (
            'Package %s is not currently installed.\n'
            'Would you like to install it? (y/n)\n'
        )
        err2 = 'Package %s is not currently installed.'

    class install:
        name = 'Install'
        err1 = (
            'Package %s is already installed.\n'
            'Would you like to upgrade it? (y/n)\n'
        )
        err2 = 'Package %s is already installed'

    class uninstall:
        name = 'Uninstall'
        err1 = 'Package %s is not currently installed.'
        err2 = err1


class Check(object):

    unauthError = Text.unauthError2

    def AllowedAccess(self):
        allowable = (
            'pip',
            'setuptools',
            'site',
            'builder',
            'script',
            'eg.log',
            'wx._core',
            'pkg_resources',
            'wx.py.interpreter',
            'eg.Classes.PluginManager',
            'eg.Classes.PackageInstaller',
            'eg.CorePluginModule.EventGhost.PythonScript',
            'eg.CorePluginModule.EventGhost.PythonCommand',
            'eg.Classes.PackageInstaller.InstallerOverride'
        )

        for item in allowable:
            yield item

    def Permissions(self, frame=None, name=None):

        def check(funcName):
            for allowedName in self.AllowedAccess():
                if funcName.startswith(allowedName):
                    return True
            return False

        if frame:
            if '__name__' in frame.f_back.f_back.f_globals:
                name = frame.f_back.f_back.f_globals['__name__']
                granted = check(name)
            else:
                granted = False

            if not granted and '__name__' in frame.f_back.f_globals:
                name = frame.f_back.f_globals['__name__']
                granted = check(name)
            else:
                name = ''
            if name == 'code':
                name = frame.f_back.f_back.f_locals['self'].__module__
                granted = check(name)

            return name, granted

        return check(name)

    def ProcessType(self, process, installer):
        if process == 'Install':
            if installer == 'easy_install':
                return [
                    '--install-dir',
                    USER_SITE,
                    '--script-dir',
                    os.path.join(USER_BASE, 'Scripts'),
                    '--zip-ok'
                ]
            elif installer == 'pip':
                return [
                    'install',
                    '--user',
                    '--trusted-host',
                    'pypi.python.org',
                    '--disable-pip-version-check'
                ]
        elif process == 'Uninstall':
            if installer == 'easy_install':
                return ['-m']

            elif installer == 'pip':
                return [
                    'uninstall',
                    '-y',
                    '--disable-pip-version-check'
                ]
        elif process == 'Upgrade':
            if installer == 'easy_install':
                return [
                    '--upgrade',
                    '--install-dir',
                    USER_SITE,
                    '--script-dir',
                    os.path.join(USER_BASE, 'Scripts'),
                    '--zip-ok'
                ]
            elif installer == 'pip':
                return [
                    'install',
                    '--upgrade'
                    '--user',
                    '--trusted-host',
                    'pypi.python.org',
                    '--disable-pip-version-check'
                ]

    def __set__(self, instance, value):
        raise AttributeError(self.unauthError)

    def __delete__(self, instance):
        raise AttributeError(self.unauthError)

    def __setattr__(self, key, value):
        raise AttributeError(self.unauthError)

    def __delattr__(self, item):
        raise AttributeError(self.unauthError)

Check = Check()


class Std:

    def __init__(self):
        self.stderr = StringIO()
        self.stdout = StringIO()
        self._stderr = None
        self._stdout = None

    def start(self):
        if self._stderr is None:
            self._stderr = sys.stderr
            sys.stderr = self.stderr
        if self._stdout is None:
            self._stdout = sys.stdout
            sys.stdout = self.stdout

    def reset(self):
        self.stderr.truncate(0)
        self.stdout.truncate(0)

    def stop(self):
        if sys.stderr == self.stderr:
            sys.stderr = self._stderr
            self._stderr = None
        if sys.stdout == self.stdout:
            sys.stdout = self._stdout
            self._stdout = None

    def stderr_readlines(self):
        res = []
        for line in self.stderr.readlines():
            res.append(line)
        return res

    def stdout_readlines(self):
        res = []
        for line in self.stdout.readlines():
            res.append(line)
        return res


Std = Std()


class InstallerOverride(object):

    text = Text

    def __init__(self, data=None):
        if data is None:
            Std.start()

            import pip
            import setuptools

            mod = InstallerOverride(pip)
            sys.modules['pip'] = mod
            mod = InstallerOverride(setuptools)
            sys.modules['setuptools'] = mod

            for key in sys.modules.keys():
                if key.startswith('pip.') or key.startswith('setuptools.'):
                    try:
                        __import__(key)
                    except ImportError:
                        continue
                    mod = InstallerOverride(sys.modules[key])
                    sys.modules[key] = mod
            Std.stop()
        else:
            self.data = data

    def CheckPermissions(self):
        def check(**kwargs):
            return Check.Permissions(
                **kwargs
            )

        frame = inspect.stack()[1][0]
        granted = False

        if 'used' in frame.f_locals:
            name = frame.f_locals['used']
            granted = check(name=name)
        if not granted and '__name__' in frame.f_globals:
            name = frame.f_globals['__name__']
            granted = check(name=name)
        if not granted:
            name, granted = check(frame=frame)

        if granted:
            return True
        else:
            raise ImportError(self.text.unauthError1 % name)

    def __set__(self, instance, value):
        if self.CheckPermissions():
            self.data.__set__(instance, value)

    def __delete__(self, instance):
        if self.CheckPermissions():
            self.data.__delete__(instance)

    def __delattr__(self, item):
        if self.CheckPermissions():
            delattr(self.data, item)

    def __setattr__(self, key, value):

        if key == 'data' and key not in self.__dict__:
            self.__dict__[key] = value
        elif self.CheckPermissions():
            setattr(self.data, key, value)

    def __getattr__(self, item):
        if self.CheckPermissions():
            return getattr(self.data, item)

if eg.startupArguments.isMain:

    class Package:
        text = Text

        def __init__(self):
            InstallerOverride()
            self.running = False

        def IsRunning(self):
            return self.running

        def __set__(self, instance, value):
            raise AttributeError(self.text.unauthError2)

        def __delete__(self, instance):
            raise AttributeError(self.text.unauthError2)

        def __setattr__(self, key, value):
            if (key == 'running' and
                    self.CheckPermissions(self.text.unauthError2)):
                self.__dict__[key] = value
            else:
                raise AttributeError(self.text.unauthError2)

        def __getattr__(self, key):
            if (key == 'IsRunning' or
                    self.CheckPermissions(self.text.unauthError2)):
                return self.__dict__[key]

        def __call__(self, args):
            if self.CheckPermissions():
                if isinstance(args, basestring):
                    name = args
                    found = tuple(
                        p for p in self.InstalledPackages() if p[0] == name
                    )
                    if eg.debugLevel:
                        if found:
                            eg.PrintNotice(
                                "Package: %s, Version: %s".format(*found[0])
                            )
                        else:
                            eg.PrintNotice(
                                "Package %s is not installed" % name
                            )
                    if found:
                        return found[0]
                    else:
                        return None
                else:
                    name = args[-1:][0]
                    if '--upgrade' in args:
                        self.Upgrade(name)
                    elif 'uninstall' in args:
                        self.Uninstall(name)
                    else:
                        self.Install(name)

        def InstalledPackages(self, printList=False):
            import pip

            installed = pip.get_installed_distributions()

            if printList:
                printInstalled = sorted(
                    ["Package: %s, Version: %s" % (
                        i.key,
                        i.version
                    ) for i in installed]
                )

                for package in printInstalled:
                    print package

            installed = tuple((i.key, i.version) for i in installed)
            return sorted(installed)

        def RunInstaller(self, installer, options, process, fileDict):
            Std.reset()
            Std.start()
            package = options[-1]
            try:
                installer.main(options)
                exception = ''.join(Std.stderr_readlines())
            except:
                exception = traceback.format_exc()

            Std.stop()

            if eg.debugLevel:
                for line in Std.stdout_readlines():
                    print line

            if exception and exception.find(self.text.allowedError) > -1:
                self.running = False
                eg.PrintNotice(self.text.sucess % (process, package, process))
            elif exception:
                Std.start()
                if 'uninstall' in options:
                    from setuptools.command import easy_install
                    installer = easy_install
                elif '--install-dir' in options:
                    import pip
                    installer = pip
                else:
                    installer = None

                if installer is not None:
                    options = self.FormatOptions(
                        process.title(),
                        package,
                        flip=True
                    )
                    eg.PrintDebugNotice(exception)
                    self.RunInstaller(installer, options, process, fileDict)
                else:
                    Std.stop()
                    self.running = False
                    eg.PrintError(self.text.failed % (process, package))
                    raise
            else:
                if 'uninstall' in options:
                    for key in sys.modules.keys():
                        if key.startswith(package):
                            del (sys.modules[key])
                elif '--install-dir' in options:
                    for f in os.listdir(USER_SITE):
                        path = os.path.join(USER_SITE, f)
                        if path.endswith('.egg') and path not in sys.path:
                            sys.path.append(path)
                if process == 'install':
                    class baseCls:
                        pass

                    fileDict['site_packages'] = tuple(
                        f for f in os.listdir(USER_SITE)
                        if f not in fileDict['site_packages']
                    )
                    fileDict['Scripts'] = tuple(
                        f for f in os.listdir(USER_SCRIPTS)
                        if f not in fileDict['Scripts']
                    )

                    from types import ClassType

                    cls = ClassType(package, (baseCls,), fileDict)
                    setattr(Config, package, cls)

                elif process == 'uninstall':
                    self.RemoveFiles(getattr(Config, package))
                    delattr(Config, package)
                self.running = False
                eg.PrintNotice(self.text.sucess % (process, package, process))

        def RemoveFiles(self, package):
            from shutil import rmtree

            def remove_files(path, files):
                for f in files:
                    f = os.path.join(path, f)
                    if os.path.isdir(f):
                        rmtree(f)
                    elif os.path.isfile(f):
                        os.remove(f)

            remove_files(package.site_packages_directory,
                         package.site_packages)
            remove_files(package.Scripts_directory, package.Scripts)

        def FormatOptions(self, process, package, flip=False):
            if process == 'Uninstall':
                if flip:
                    installer = 'easy_install'
                else:
                    installer = 'pip'
            else:
                if flip:
                    installer = 'pip'
                else:
                    installer = 'easy_install'

            options = Check.ProcessType(process, installer)

            if eg.debugLevel:
                options.append('--verbose')
            else:
                options.append('--quiet')

            options.append(package)
            return options

        def Start(self, process, package, fileDict=None):
            self.running = True
            options = self.FormatOptions(process, package)

            eg.PrintNotice(self.text.start % (process.lower(), options[-1]))

            if 'uninstall' in options:
                import pip
                installer = pip
            else:
                from setuptools.command import easy_install
                installer = easy_install

            wx.CallAfter(
                self.RunInstaller,
                installer,
                options,
                process.lower(),
                fileDict
            )

        def ImportPackage(self, package):
            eg.PrintNotice(self.text.check)

            try:
                __import__(package)
            except ImportError:
                return False
            except:
                pass

            return sys.modules[package]

        def CheckPermissions(self, attributeError=None):
            frame = inspect.stack()[1][0]

            if attributeError is None:
                eg.PrintNotice(self.text.permissions)

            name, granted = Check.Permissions(frame=frame)
            if granted:
                return True
            else:
                if attributeError is None:
                    raise ImportError(self.text.unauthError1 % name)
                else:
                    raise AttributeError(attributeError)

        def Install(self, package):
            text = self.text.install
            if self.CheckPermissions():
                if self.ImportPackage(package) is False:
                    fileDict = dict(
                        site_packages_directory=USER_SITE,
                        Scripts_directory=USER_SCRIPTS,
                        site_packages=os.listdir(USER_SITE),
                        Scripts=os.listdir(USER_SCRIPTS)
                    )
                    self.Start(text.name, package, fileDict)
                else:
                    answer = raw_input(text.err1 % package)
                    if answer.lower() == 'y':
                        self.Upgrade(package)
                    else:
                        raise ImportError(text.err2 % package)

        def Uninstall(self, package):
            text = self.text.uninstall

            if self.CheckPermissions():
                mod = self.ImportPackage(package)
                if mod is False:
                    raise ImportError(text.err2 % package)
                else:
                    self.Start(text.name, package)

        def Upgrade(self, package):
            text = self.text.upgrade

            if self.CheckPermissions():
                if self.ImportPackage(package) is False:
                    answer = raw_input(text.err1 % package)
                    if answer.lower() == 'y':
                        self.Install(package)
                    else:
                        raise ImportError(text.err2 % package)
                else:
                    fileList = os.listdir(USER_SITE)
                    self.Start(text.name, package, fileList)
else:
    class Package:

        def __init__(self):
            pass
