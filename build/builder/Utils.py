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
import time
import subprocess
import re
import imp
import _winreg
from os.path import join, normpath

import builder
from builder.subprocess2 import Popen

def EncodePath(path):
    return path.encode('mbcs')


def DecodePath(path):
    return path.decode('mbcs')


def StartProcess(*args):
    #SetIndent(1)
    startupInfo = subprocess.STARTUPINFO()
    startupInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
    startupInfo.wShowWindow = subprocess.SW_HIDE
    process = Popen(
        args,
        cwd=EncodePath(join(builder.buildSetup.sourceDir, "build")),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=startupInfo,
    )
    while process.returncode is None:
        process.poll()
        errData = process.recv_err()
        if errData is not None:
            sys.stderr.write(errData)
        inData = process.recv()
        if inData is not None:
            if inData:
                sys.stdout.write(inData)
            else:
                time.sleep(0.1)
        else:
            break
    process.wait()
    #SetIndent(0)
    return process.returncode


def ExecutePy(*args):
    return StartProcess(sys.executable, "-u", "-c", "\n".join(args))


def GetRevision(buildSetup):
    """
    Get the app version and revision.
    """

    regex = re.compile('^refs/tags')
    all_tags = filter(lambda r: regex.match(r),
                      buildSetup.repo.listall_references())

    if all_tags == []:
        parts = ['0', '0','0']
    else:
        all_sorted = all_tags.sort() if len(all_tags)>1 else all_tags
        parts = all_sorted[0].split('/')
        parts = parts[len(parts)-1].split('.')
        parts[0] = parts[0].strip('v')
        if len(parts) == 3:
            parts[2] = int(parts[2]) + 1
        elif len(parts) == 4:
            parts[2] = int(parts[2]) + 1
            parts.pop(3)
        else:
            parts = ['wrong', 'version','format']
    buildSetup.appVersion = '{0}.{1}.{2}'.format(*parts)


def GetHtmlHelpCompilerPath():
    """
    Try to find the install location of the HTML Help command line compiler
    """
    subkey = r"Software\Microsoft\HTML Help Workshop"
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, subkey)
        path = _winreg.QueryValueEx(key, "InstallDir")[0]
    except WindowsError:
        path = join(os.environ["PROGRAMFILES"], "HTML Help Workshop")
    programPath = join(path, "hhc.exe")
    if not os.path.exists(programPath):
        return None
    return programPath


def ListDir(path, skip_dirs=[], fullpath=True):
    '''
    Return a list with all files in given path (including subdirs).
    skip_dirs is a list of directories, which contents should not be listet.

    :param path: root directory (full path)
    :param skip_dirs: list of directory names to skip
    :param fullpath: should the list contain the full path?
    :return: list of filenames with full path
    '''

    if not fullpath:
        cwd = os.getcwd()
        os.chdir(path)
        path = '.'

    contents = os.walk(path)
    files = []
    for item in contents:
        parts = set(item[0].split('\\'))
        if parts.intersection(skip_dirs):
            continue
        if len(item[2]) > 0:
            for name in item[2]:
                if name[-4:] not in ('.pyc',):
                    filename = normpath(join(item[0], name))
                    files.append(filename)
        if len(item[1]) > 0:
            for subdir in item[1]:
                parts = set(subdir.split('\\'))
                if parts.intersection(skip_dirs):
                    continue
                else:
                    subpath = normpath(join(path, subdir))
                    sublist = ListDir(subpath, skip_dirs)
                    files.extend(sublist)
    if not fullpath:
        os.chdir(cwd)
    return files

