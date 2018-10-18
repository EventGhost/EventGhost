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

"""
Builds a file that would import all used modules.

This way we trick py2exe to include all standard library files and some more
packages and modules.
"""

import os
import sys
import warnings
import site

SITE_DIRS = site.getsitepackages()

MODULES_TO_IGNORE = [
    '__builtin__',
    '__main__',
    "__phello__.foo",
    "antigravity",
    "unittest",
    "win32com.propsys.propsys",
    "wx.lib.graphics",
    "wx.lib.rpcMixin",
    "wx.lib.wxcairo",
    "wx.build.config",
    'plat-aix4',
    'plat-darwin',
    'plat-freebsd4',
    'plat-freebsd5',
    'plat-freebsd6',
    'plat-freebsd7',
    'plat-freebsd8',
    'plat-generic',
    'plat-linux',
    'plat-netbsd1',
    'plat-next3',
    'plat-sunos5',
    'plat-unixware7',
    'site-packages',
    'collections.__main__',
    '_osx_support',
    'macpath',
    'lzma',
    'this',
    'macurl2path',
    'venv',
    'lib2to3.__main__',
    'os2emxpath',
    'urllib._hashlib',
    'urllib._socket',
    'urllib._ssl',
    'urllib.select',
]
PACKAGES = [
    'six',
    'CommonMark',
    'comtypes',
    'future',
    'PIL',
    'jinja2',
    'wx',
    'Crypto',
    'comtypes',
    'future',
    'Pillow',
    'pkg_resources',
    'docutils',
    'pywin32',
    'alabaster',
    'asn1crypto',
    'babel',
    'bcrypt',
    'certifi',
    'cffi',
    'chardet',
    'colorama',
    'comtypes',
    'cryptography',
    'docutils',
    'enum34',
    'idna',
    'imagesize',
    'ipaddress',
    'markupsafe',
    'paramiko',
    'pyasn1',
    'pycparser',
    'pygments',
    'pynacl',
    'pytz',
    'snowballstemmer',
]

INCLUDES = [
    'winsound',
    'afxres',
    'commctrl',
    'dbi',
    'mmsystem',
    'netbios',
    'ntsecuritycon',
    'pywintypes',
    'rasutil',
    'regcheck',
    'regutil',
    'sspi',
    'win32con',
    'win32cryptcon',
    'win32evtlogutil',
    'win32gui_struct',
    'win32inetcon',
    'win32netcon',
    'win32pdhquery',
    'win32pdhutil',
    'win32rcparser',
    'win32serviceutil',
    'win32timezone',
    'win32verstamp',
    'winerror',
    'winioclcon',
    'winnt',
    'winperf',
    'winxptheme',
    'backupEventLog',
    'ControlService',
    'killProcName',
    'rasutil',
    'regsetup',
    'setup_d',
    'BrandProject',
    'bulkstamp',
    'vssutil',
    '_win32sysloader',
    '_winxptheme',
    'mmapfile',
    'odbc',
    'perfmon',
    'servicemanager',
    'timer',
    'win2kras',
    'win32api',
    'win32clipboard',
    'win32console',
    'win32cred',
    'win32crypt',
    'win32event',
    'win32evtlog',
    'win32file',
    'win32gui',
    'win32help',
    'win32inet',
    'win32job',
    'win32lz',
    'win32net',
    'win32pdh',
    'win32pipe',
    'win32print',
    'win32process',
    'win32profile',
    'win32ras',
    'win32security',
    'win32service',
    'win32trace',
    'win32transaction',
    'win32ts',
    'win32wnet',
    'winxpgui',
    '_win32sysloader',
    '_winxptheme',
    'win32com',
    'win32com.client',
    'win32com.makegw',
    'win32com.server',
    'win32com.servers',
    'win32com.olectl',
    'win32com.storagecon',
    'win32com.universal',
    'win32com.util',
    'win32com.adsi',
    'win32com.authorization',
    'win32com.axcontrol',
    'win32com.axdebug',
    'win32com.axscript',
    'win32com.bits',
    'win32com.directsound',
    'win32com.ifilter',
    'win32com.internet',
    'win32com.mapi',
    'win32com.propsys',
    'win32com.shell',
    'win32comt.taskscheduler',
    'difflib',
]

EXCLUDES = [
    'sphinx',
    'six.moves',
    'moves',
    'eg',
    '_imagingtk',
    '_tkinter',
    'cffi',
    'comtypes.gen',
    'curses',
    'distutils.command.bdist_packager',
    'distutils.mwerkscompiler',
    'FixTk',
    'gopherlib',
    'idlelib',
    'ImageGL',
    'ImageQt',
    'ImageTk',
    'ipaddr',
    'ipaddress',
    'lib2to3',
    'PIL._imagingtk',
    'PIL.ImageTk',
    'pyasn1',
    'pycparser',
    'pywin',
    'simplejson',
    'tcl',
    'test',
    'Tix',
    'Tkconstants',
    'tkinter',
    'Tkinter',
    'turtle',
    'WalImageFile',
    'win32com.axdebug',
    'win32com.axscript',
    'win32com.demos',
    'win32com.gen_py',
    'sqlite3',
    'doctest',
    'unittest',
    'pydoc',
    'pygments',
    'pdb',
    'numpy',
    'dbi',
    'regcheck',
    'win32traceutil',
    'py2exe',
    'os2emxpath',
    'urllib._hashlib',
    'urllib._socket',
    'urllib._ssl',
    'urllib.select',
]

PY_PATH = sys.real_prefix if hasattr(sys, "real_prefix") else sys.prefix
MODULES_TO_IGNORE += EXCLUDES[:]

HEADER = """\
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

#-----------------------------------------------------------------------------
# This file was automatically created by the BuildImports.py script.
# Don't try to edit this file yourself.
#-----------------------------------------------------------------------------
#pylint: disable-msg=W0611,W0622,W0402,E0611,F0401
"""


def test_import(module):
    if module in MODULES_TO_IGNORE or 'test' in module:
        return None
    try:
        mod = __import__(module)
        return mod
    except:
        pass


def find_modules(path, module=""):
    """
    Find modules and packages for a given filesystem path.
    """
    modules = []

    if module in MODULES_TO_IGNORE:
        return []

    if module:
        module += "."

    dirs = []
    try:
        files = os.listdir(path)
    except OSError:
        return modules

    if 'site-packages' in files:
        files.remove('site-packages')

    if '__init__.py' in files:
        files.remove('__init__.py')

        mod = module[:-1]
        if test_import(mod):
            modules += [mod]

    if '__pycache__' in files:
        files.remove('__pycache__')


    def bad_file():
        for item in ('demo', 'test'):
            if item in file.lower():
                return True
        return False

    for file in files:
        if bad_file():
            continue

        if os.path.isdir(os.path.join(path, file)):
            dirs += [os.path.join(path, file)]
            continue

        if file.endswith('.py') or file.endswith('.pyd'):
            if module == 'pywin32.':
                mod = file.replace('.py', '').replace('.pyd', '')
            else:
                mod = module + file.replace('.py', '').replace('.pyd', '')
            if test_import(mod):
                modules += [mod]

    for mod_path in dirs:
        if module == 'pywin32.':
            mod = module[:-1]
        else:
            mod = module + os.path.split(mod_path)[1]

        modules += find_modules(mod_path, mod)

    return modules


def get_requirements(package):

    for site_dir in SITE_DIRS:
        files = os.listdir(site_dir)
        for f in files:
            meta_data = os.path.join(site_dir, f, 'METADATA')

            if (
                'dist-info' not in meta_data or
                package not in meta_data or
                not os.path.exists(meta_data)
            ):
                continue

            with open(meta_data, 'r') as meta_file:
                meta_data = meta_file.read()

            requirements = list(
                line.strip() for line in meta_data.split('\n')
                if line.startswith('Requires-Dist')
            )
            requirements = list(
                req.split(' ')[1].replace(';', '') for req in requirements
            )

            top_level = os.path.join(site_dir, f, 'top_level.txt')

            if os.path.exists(top_level):
                with open(top_level, 'r') as top_file:
                    top_level = top_file.read()

                package = top_level.split('\n')[0].strip()

            return requirements, package

    return [], package


FOUND_PACKAGES = []

import __builtin__

_original_import = __builtin__.__import__


FOUND_MODULES = {}


def _import(name, globals={}, locals={}, fromlist=[], level=0):
    mod = _original_import(name, globals, locals, fromlist, level)

    name = mod.__name__

    while '.' in name:
        if name in MODULES_TO_IGNORE + EXCLUDES:
            return mod
        name = name.rsplit('.', 1)[0]

    if name in MODULES_TO_IGNORE + EXCLUDES:
        return mod

    if mod.__name__ in FOUND_MODULES:
        return mod

    if hasattr(mod, '__file__'):
        mod_path = mod.__file__
    else:
        mod_path = None

    FOUND_MODULES[mod.__name__] = mod_path
    return mod


PACKAGE_IMPORTS = []


def import_package(package):
    try:
        __import__(package)
        PACKAGE_IMPORTS.append(package)

        while FOUND_MODULES:
            module = FOUND_MODULES.keys()[0]
            path = FOUND_MODULES.pop(module)
            if module not in PACKAGE_IMPORTS:
                PACKAGE_IMPORTS.append(module)
                if path is not None:
                    for module in find_modules(os.path.dirname(path), module):
                        if module not in PACKAGE_IMPORTS:
                            PACKAGE_IMPORTS.append(module)
    except:
        pass


def find_package_modules(package):
    if package in FOUND_PACKAGES:
        return []

    requirements, package = get_requirements(package)
    modules = []

    for requirement in requirements:
        if (
            'test' not in requirement.lower() and
            requirement not in FOUND_PACKAGES
        ):
            modules += find_package_modules(requirement)
            FOUND_PACKAGES.append(requirement)

    pths = []
    for site_dir in SITE_DIRS:
        tail = package + ".pth"
        pths += [os.path.join(site_dir, tail)]

    for pth in pths:
        if os.path.exists(pth):
            for path in read_pth_file(pth):
                modules += find_modules(path, package)
            break
    else:
        mod = test_import(package)
        if mod is not None:
            if mod.__file__.endswith(".pyd"):
                return modules
            modules += find_modules(os.path.dirname(mod.__file__), package)

    return modules


def read_pth_file(path):
    with open(path, "rt") as f:
        for line in f.readlines():
            if line.strip().startswith("#"):
                continue
            module = os.path.join(os.path.dirname(path), line.strip())

            if os.path.exists(line.strip()):
                yield line.strip()
            elif os.path.exists(module):
                yield module


# warnings.simplefilter('error', DeprecationWarning)
# OUT_FILE = os.path.join(BUILD_PATH, 'module_imports.py')
class Build(object):

    @property
    def STD_LIB_MODULES(self):
        return (
            find_modules(os.path.join(PY_PATH, "DLLs"), "") +
            find_modules(os.path.join(PY_PATH, "Lib"), "")
        )

    @property
    def INCLUDES(self):

        __builtin__.__import__ = _import

        for package in PACKAGES[:]:
            import_package(package)
            for item in find_package_modules(package):
                import_package(item)

        for item in INCLUDES[:]:
            import_package(item)
            for itm in find_package_modules(item):
                import_package(itm)

        __builtin__.__import__ = _original_import

        return sorted(item for item in set(PACKAGE_IMPORTS + self.STD_LIB_MODULES))

build = Build()
