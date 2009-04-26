import os
import sys
import time
import subprocess
from os.path import join

import builder
from builder.subprocess2 import Popen


def StartProcess(*args):
    #SetIndent(1)
    startupInfo = subprocess.STARTUPINFO()
    startupInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
    startupInfo.wShowWindow = subprocess.SW_HIDE 
    process = Popen(
        args, 
        cwd=join(builder.SOURCE_DIR, "tools"),
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


def GetSvnRevision(workingCopy):
    """
    Return the highest SVN revision in the working copy.
    """
    import pysvn
    client = pysvn.Client()
    svnRevision = 0
    for status in client.status(workingCopy, ignore=True):
        if status.is_versioned:
            if status.entry.revision.number > svnRevision:
                svnRevision = status.entry.revision.number
    return svnRevision


def RemoveAllManifests(scanDir):
    """ 
    Remove embedded manifest resource for all DLLs and PYDs in the supplied
    path. 
    
    These seems to be the only way how the setup can run with Python 2.6
    on Vista.
    """
    import ctypes
    
    BeginUpdateResource = ctypes.windll.kernel32.BeginUpdateResourceA
    UpdateResource = ctypes.windll.kernel32.UpdateResourceA
    EndUpdateResource = ctypes.windll.kernel32.EndUpdateResourceA
    
    for (dirpath, dirnames, filenames) in os.walk(scanDir):
        if '.svn' in dirnames:
            dirnames.remove('.svn')
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in (".pyd", ".dll"):
                continue
            path = os.path.join(dirpath, name)
            handle = BeginUpdateResource(path, 0)
            if handle == 0:
                continue
            res = UpdateResource(handle, 24, 2, 1033, None, 0)
            if res:
                EndUpdateResource(handle, 0)


