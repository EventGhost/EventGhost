"""
This script is executed by py2exe for the frozen application directly after
boot_common.py in the py2exe site package has been executed.

The drawback of the default boot_common.py is, that it directs sys.stdout
to a log file (that's fine so far) in the applications program folder (that's
bad for user accounts with limited priviliges).

So we redirect the sys.stdout to a log file in the applications data folder.
"""


class StdErrReplacement(object):
    softspace = 0
    _file = None
    _error = None
    _logFilePath = None
    
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
                import ctypes
                atexit.register(
                    ctypes.windll.user32.MessageBoxA, 
                    0,
                    "See the logfile '%s' for details" % self._logFilePath,
                    "Errors occurred in EventGhost",
                    0
                )
        if self._file is not None:
            self._file.write(text)
            self._file.flush()
            
            
    def flush(self):
        if self._file is not None:
            self._file.flush()
            
            
import sys
sys.stderr = StdErrReplacement()
del StdErrReplacement
del sys

