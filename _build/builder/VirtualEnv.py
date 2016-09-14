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

import os
import sys
from os.path import exists, expandvars, join

_CODE_DEACTIVATE = 5000
_CODE_RESTART = 6000

ARGV = " ".join(["Build.py"] + sys.argv[1:])
HOME = os.environ.get("WORKON_HOME", expandvars("%USERPROFILE%\Envs"))
if hasattr(sys, "real_prefix"):
    NAME = sys.prefix.split("\\")[-1]
    PATH = sys.prefix
    for path in sys.path[:]:
        if path.startswith(sys.prefix):
            sys.path.remove(path)
            sys.path.append(path)
else:
    NAME = "eg-py%d%d" % sys.version_info[:2]
    PATH = join(HOME, NAME)
PATH_ACTIVATE = join(PATH, "Scripts", "activate.bat")
PATH_EXECUTABLE = join(PATH, "Scripts", "python.exe")

def Activate():
    """
    Activate the virtualenv for our Python version.
    """
    if not Running():
        restarted = False
        while True:
            exitCode = os.system(
                ("%s && " % (PATH_ACTIVATE)) +
                ("SET _REST=1 && " if restarted else "") +
                ("%s %s" % (PATH_EXECUTABLE, ARGV))
            )

            if exitCode == _CODE_DEACTIVATE:
                break
            elif exitCode == _CODE_RESTART:
                restarted = True
                continue
            else:
                sys.exit(exitCode)

def Deactivate():
    """
    Deactivate the running virtualenv.
    """
    if Running():
        sys.exit(_CODE_DEACTIVATE)

def Exists():
    """
    Check if the virtualenv for our Python version exists.
    """
    return exists(PATH_ACTIVATE)

def Restart():
    """
    Restart the running virtualenv.
    """
    if Running():
        sys.exit(_CODE_RESTART)

def Running():
    """
    Check if we're running inside a virtualenv.
    """
    return (sys.executable.lower() == PATH_EXECUTABLE.lower())
