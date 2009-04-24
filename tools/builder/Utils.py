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


