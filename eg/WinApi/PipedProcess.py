import sys
import imp
import ctypes
from os.path import join, dirname, abspath, splitext, basename
from cPickle import dumps, loads
from Dynamic import (
    byref,
    sizeof,
    create_string_buffer,
    DWORD,

    CreateNamedPipe,
    ReadFile,
    WriteFile,
    FlushFileBuffers,
    ConnectNamedPipe,
    DisconnectNamedPipe,
    SetNamedPipeHandleState,
    WaitNamedPipe,
    CloseHandle,
    GetLastError,
    CreateFile,

    GENERIC_READ,
    GENERIC_WRITE,
    OPEN_EXISTING,
    PIPE_ACCESS_DUPLEX,
    PIPE_TYPE_MESSAGE,
    PIPE_READMODE_MESSAGE,
    PIPE_WAIT,
    PIPE_UNLIMITED_INSTANCES,
    ERROR_PIPE_CONNECTED,
    ERROR_PIPE_BUSY,
    ERROR_MORE_DATA,
    NMPWAIT_USE_DEFAULT_WAIT,
    INVALID_HANDLE_VALUE,

    SHELLEXECUTEINFO,
    SEE_MASK_FLAG_DDEWAIT,
    SEE_MASK_FLAG_NO_UI,
    SEE_MASK_NOCLOSEPROCESS,
    SW_SHOWNORMAL,
)

BUFSIZE = 4096
szPipename = "\\\\.\\pipe\\EventGhostPipedProcess"


def RunAsAdministrator(filePath, *args):
    sei = SHELLEXECUTEINFO()
    sei.cbSize = sizeof(SHELLEXECUTEINFO)
    sei.fMask = (
        SEE_MASK_FLAG_DDEWAIT | SEE_MASK_FLAG_NO_UI | SEE_MASK_NOCLOSEPROCESS
    )
    sei.lpVerb = u"runas"
    sei.lpFile = filePath
    sei.lpParameters = " ".join(
        ['"%s"' % arg.replace('"', '""') for arg in args]
    )
    sei.nShow = SW_SHOWNORMAL
    if not ctypes.windll.shell32.ShellExecuteExW(byref(sei)):
        raise FailedFunc("ShellExecuteEx")


class PipeStream(object):
    def __init__(self, hPipe, code):
        self.hPipe = hPipe
        self.code = code

    def write(self, data):
        WritePipe(self.hPipe, self.code, data)


def WritePipe(hPipe, code, data):
    message = dumps((code, data))
    cbWritten = DWORD(0)
    fSuccess = WriteFile(
        hPipe,
        message,
        len(message),
        byref(cbWritten),
        None
    )
#    if (not fSuccess) or (len(message) != cbWritten.value):
#        print "Write File failed"

def ReadPipeData(hPipe):
    data = ""
    fSuccess = 0
    chBuf = create_string_buffer(BUFSIZE)
    cbRead = DWORD(0)
    while not fSuccess: # repeat loop if ERROR_MORE_DATA
        fSuccess = ReadFile(
            hPipe,
            chBuf,
            BUFSIZE,
            byref(cbRead),
            None
        )
        if fSuccess == 1:
            data += chBuf.value
            break
        elif GetLastError() != ERROR_MORE_DATA:
            break
        data += chBuf.value
    return loads(data)




def ExecAsAdministrator(scriptPath, funcName, *args, **kwargs):
    hPipe = CreateNamedPipe(
        szPipename,
        PIPE_ACCESS_DUPLEX,
        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
        PIPE_UNLIMITED_INSTANCES,
        BUFSIZE,
        BUFSIZE,
        NMPWAIT_USE_DEFAULT_WAIT,
        None
    )
    if (hPipe == INVALID_HANDLE_VALUE):
        print "Error in creating Named Pipe"
        return 0

    executable = abspath(join(
        dirname(__file__.decode(sys.getfilesystemencoding())),
        "..",
        "..",
        "EventGhost.exe"
    ))
    RunAsAdministrator(
        executable,
        "-execscript",
        __file__.decode(sys.getfilesystemencoding()),
        "-client",
        szPipename
    )
    fConnected = ConnectNamedPipe(hPipe, None)
    if fConnected == 0 and GetLastError() == ERROR_PIPE_CONNECTED:
        fConnected = 1
    if fConnected != 1:
        print "Could not connect to the Named Pipe"
        CloseHandle(hPipe)
        return
    WritePipe(hPipe, 0, (scriptPath, funcName, args, kwargs))
    chBuf = create_string_buffer(BUFSIZE)
    cbRead = DWORD(0)
    while True:
        fSuccess = ReadFile(hPipe, chBuf, BUFSIZE, byref(cbRead), None)
        if ((fSuccess == 1) or (cbRead.value != 0)):
            code, data = loads(chBuf.value)
            if code == 1:
                sys.stderr.write(data)
            elif code == 2:
                sys.stdout.write(data)
            elif code == 3:
                result = data
                break
            elif code == 4:
                break
            else:
                print code, data
    FlushFileBuffers(hPipe)
    DisconnectNamedPipe(hPipe)
    CloseHandle(hPipe)
    if code == 4:
        raise Exception("Child process raised an exception\n" + data)
    return result


def Client():
    while 1:
        hPipe = CreateFile(
            szPipename,
            GENERIC_READ | GENERIC_WRITE,
            0,
            None,
            OPEN_EXISTING,
            0,
            None
        )
        if hPipe != INVALID_HANDLE_VALUE:
            break
        else:
            print "Invalid Handle Value"
        if GetLastError() != ERROR_PIPE_BUSY:
            print "Could not open pipe"
            return
        elif WaitNamedPipe(szPipename, 20000) == 0:
            print "Could not open pipe\n"
            return


    dwMode = DWORD(PIPE_READMODE_MESSAGE)
    fSuccess = SetNamedPipeHandleState(hPipe, byref(dwMode), None, None)
    if not fSuccess:
        print "SetNamedPipeHandleState failed"
        CloseHandle(hPipe)
        return
    sys.stderr = PipeStream(hPipe, 1)
    sys.stdout = PipeStream(hPipe, 2)
    code, (scriptPath, funcName, args, kwargs) = ReadPipeData(hPipe)
    moduleName = splitext(basename(scriptPath))[0]
    module = imp.load_module(
        moduleName,
        *imp.find_module(moduleName, [dirname(scriptPath)])
    )
    func = getattr(module, funcName)
    try:
        result = func(*args, **kwargs)
    except:
        import traceback
        WritePipe(hPipe, 4, traceback.format_exc())
    else:
        WritePipe(hPipe, 3, result)
    CloseHandle(hPipe)
    return


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "-client":
            Client()
            sys.exit(0)

