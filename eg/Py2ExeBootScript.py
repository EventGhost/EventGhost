# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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

"""
This script is executed by py2exe for the frozen application directly after
boot_common.py in the py2exe site package has been executed.

The drawback of the default boot_common.py is, that it directs sys.stderr
to a log file (that's fine so far) in the applications program folder (that's
bad for user accounts with limited priviliges).

So we redirect the sys.stderr to a log file in the applications data folder.
"""


class StdErrReplacement(object):
    softspace = 0
    _file = None
    _error = None
    _logFilePath = None
    _displayMessage = True
    
    def write(self, text):
        if self._file is None and self._error is None:
            if self._logFilePath is None:
                import os
                prgName = os.path.splitext(os.path.basename(sys.executable))[0]
                self._logFilePath = os.path.join(
                    os.environ["APPDATA"], 
                    prgName,
                    "Log.txt"
                )
            try:
                self._file = open(self._logFilePath, 'a')
            except Exception, details:
                self._error = details
                import atexit
                import ctypes
                atexit.register(
                    ctypes.windll.user32.MessageBoxA, 
                    0,
                    "The logfile '%s' could not be opened:\n %s" % (
                        self._logFilePath, 
                        details
                    ),
                    "Errors occurred in EventGhost",
                    0
                )
            else:
                import atexit
                atexit.register(self.__DisplayMessage)
        if self._file is not None:
            self._file.write(text)
            self._file.flush()
            
            
    def flush(self):
        if self._file is not None:
            self._file.flush()
            
            
    def __DisplayMessage(self):
        if not self._displayMessage:
            return
        import ctypes
        result = ctypes.windll.user32.MessageBoxA(
            0,
            (
                'See the logfile "%s" for details.\n\n'
                "Do you want to open the file now?"
            ) % self._logFilePath,
            "Errors occurred in EventGhost",
            4
        )
        if result == 6:
            import subprocess
            subprocess.Popen('Notepad.exe "%s"' % self._logFilePath)


            
import sys
sys.stderr = StdErrReplacement()
del StdErrReplacement
del sys
