# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import time
import subprocess
import re
import _winreg
from os.path import join

import builder
from builder.subprocess2 import Popen

def EncodePath(path):
    return path.encode(sys.getfilesystemencoding())


def DecodePath(path):
    return path.decode(sys.getfilesystemencoding())


def StartProcess(*args):
    #SetIndent(1)
    startupInfo = subprocess.STARTUPINFO()
    startupInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
    startupInfo.wShowWindow = subprocess.SW_HIDE
    process = Popen(
        args,
        cwd=EncodePath(join(builder.buildSetup.sourceDir, "tools")),
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


def GetSvnRevision(workingCopyPath):
    """
    Returns the SVN revision of a directory as an integer.

    Returns None if anything goes wrong, such as an unexpected
    format of internal SVN files.
    """
    rev = None
    entriesPath = os.path.join(workingCopyPath, ".svn", "entries")
    try:
        entries = open(entriesPath, 'r').read()
    except IOError:
        pass
    else:
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the
        # revision.
        if re.match('(\d+)', entries):
            revMatch = re.search('\d+\s+dir\s+(\d+)', entries)
            if revMatch:
                rev = revMatch.groups()[0]
    if rev:
        return int(rev)
    return None


def UpdateSvn(workingCopy):
    import pysvn

    def SslServerTrustPromptCallback(dummy):
        """
        See pysvn documentation for
        pysvn.Client.callback_ssl_server_trust_prompt
        """
        return True, 0, True
    svn = pysvn.Client()
    svn.callback_ssl_server_trust_prompt = SslServerTrustPromptCallback
    svn.update(workingCopy)


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

