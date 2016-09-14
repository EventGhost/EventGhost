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
This script is executed by py2exe for the frozen application directly after
boot_common.py in the py2exe site package has been executed.

The drawback of the default boot_common.py is, that it directs sys.stderr
to a log file (that's fine so far) in the applications program folder (that's
bad for user accounts with limited priviliges).

So we redirect the sys.stderr to a log file in the applications data folder.
"""

import linecache
import sys

class StdErrReplacement(object):
    softspace = 0
    _file = None
    _error = None
    _logFilePath = None
    _displayMessage = True
    encoding = "mbcs"

    def write(self, text):
        if self._file is None and self._error is None:
            if self._logFilePath is None:
                import os
                prgName = os.path.splitext(os.path.basename(sys.executable))[0]  # NOQA
                prgAppDataPath = os.path.join(os.environ["APPDATA"], prgName)
                self._logFilePath = os.path.join(prgAppDataPath, "Log.txt")
            try:
                if not os.path.exists(prgAppDataPath):
                    os.mkdir(prgAppDataPath)
                self._file = open(self._logFilePath, 'a')
            except Exception, details:
                self._error = details
                if "-q" not in sys.argv and "-quiet" not in sys.argv:  # NOQA
                    import atexit
                    import ctypes
                    atexit.register(
                        ctypes.windll.user32.MessageBoxA,
                        0,
                        "The logfile '%s' could not be opened:\n %s" % (
                            self._logFilePath,
                            details
                        ),
                        "Error occurred in EventGhost",
                        0
                    )
            else:
                if "-q" not in sys.argv and "-quiet" not in sys.argv:  # NOQA
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


# Replace stderr.
sys.stderr = StdErrReplacement()

# py2exe disables linecache.getline() in boot_common.py.
# py2exe disabls linecache.getline() which is called by
# traceback.extract_stack() when an exception occurs to try and read
# the filenames embedded in the packaged python code.
# We re-enable it here.
linecache.getline = linecache.orig_getline

# Clean up.
del linecache
del sys
del StdErrReplacement
