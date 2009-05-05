import os
import sys
import time
import subprocess
from os.path import join

import builder


def StartProcess(*args):
    from builder.subprocess2 import Popen
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
        

def CommitSvn():
    """
    Commit all modified files in the working copy to the SVN server.
    """
    import pysvn
    
    def SslServerTrustPromptCallback(dummy):
        """ 
        See pysvn documentation for 
        pysvn.Client.callback_ssl_server_trust_prompt
        """
        return True, 0, True
    svn = pysvn.Client()
    svn.callback_ssl_server_trust_prompt = SslServerTrustPromptCallback
    svn.checkin(
        [builder.SOURCE_DIR], 
        "Created installer for %s" % builder.APP_VERSION
    )


def CreateSourceArchive(filename=None):
    """
    Create a zip archive off all versioned files in the working copy.
    """
    import pysvn
    import zipfile
    
    if filename is None:
        filename = join(
            builder.OUT_DIR, 
            "%(APP_NAME)s_%(APP_VERSION)s_Source.zip" % builder.__dict__
        )
    client = pysvn.Client()
    workingDir = builder.SOURCE_DIR
    zipFile = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    for status in client.status(workingDir, ignore=True):
        if status.is_versioned:
            path = status.path
            if not os.path.isdir(path):
                arcname = path[len(workingDir) + 1:]
                zipFile.write(str(path), str(arcname))
    zipFile.close()


