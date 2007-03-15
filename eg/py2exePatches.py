# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import sys
if sys.frozen == "windows_exe":
    from win32com.shell import shell, shellcon
    import os
    logFile = os.path.join(
        shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0),
        "EventGhost",
        "Log.txt"
    )
    class Stderr(object):
        softspace = 0
        _file = None
        _error = None
        def write(self, text, alert=sys._MessageBox, fname=logFile):
            if self._file is None and self._error is None:
                try:
                    self._file = open(fname, 'a')
                except Exception, details:
                    self._error = details
                    import atexit
                    atexit.register(alert, 0,
                                    "The logfile '%s' could not be opened:\n %s" % \
                                    (fname, details),
                                    "Errors occurred")
                else:
                    import atexit
                    atexit.register(alert, 0,
                                    "See the logfile '%s' for details" % fname,
                                    "Errors occurred")
            if self._file is not None:
                self._file.write(text)
                self._file.flush()
        def flush(self):
            if self._file is not None:
                self._file.flush()
    sys.stderr = Stderr()
    del sys._MessageBox
    del Stderr

    class Blackhole(object):
        softspace = 0
        def write(self, text):
            pass
        def flush(self):
            pass
    sys.stdout = Blackhole()
    del Blackhole
del sys

# Disable linecache.getline() which is called by
# traceback.extract_stack() when an exception occurs to try and read
# the filenames embedded in the packaged python code.  This is really
# annoying on windows when the d: or e: on our build box refers to
# someone elses removable or network drive so the getline() call
# causes it to ask them to insert a disk in that drive.
import linecache
def fake_getline(filename, lineno,  module_globals=None):
    return ''
linecache.orig_getline = linecache.getline
linecache.getline = fake_getline

del linecache, fake_getline
