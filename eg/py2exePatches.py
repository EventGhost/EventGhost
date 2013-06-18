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
