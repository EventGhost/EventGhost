# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import sys
import ctypes
from os.path import join, dirname, abspath
from cPickle import dumps, loads
from comtypes import GUID
import eg
from Dynamic import (
    byref,
    sizeof,
    create_string_buffer,
    cast,
    POINTER,
    DWORD,

    CreateNamedPipe,
    ReadFile,
    WriteFile,
    FlushFileBuffers,
    ConnectNamedPipe,
    DisconnectNamedPipe,
    CloseHandle,
    GetLastError,
    FormatError,
    CreateEvent,
    WaitForMultipleObjects,

    OVERLAPPED,
    PIPE_ACCESS_DUPLEX,
    PIPE_TYPE_MESSAGE,
    PIPE_READMODE_MESSAGE,
    PIPE_WAIT,
    PIPE_UNLIMITED_INSTANCES,
    ERROR_NOT_CONNECTED,
    INVALID_HANDLE_VALUE,
    FILE_FLAG_OVERLAPPED,

    SHELLEXECUTEINFO,
    SEE_MASK_FLAG_DDEWAIT,
    SEE_MASK_FLAG_NO_UI,
    SEE_MASK_NOCLOSEPROCESS,
    SW_SHOWNORMAL,
    HANDLE,
    WAIT_OBJECT_0,
    WAIT_TIMEOUT,
)
from Dynamic.Winnetwk import (
    WNetGetUniversalName,
    UNIVERSAL_NAME_INFO_LEVEL,
    UNIVERSAL_NAME_INFO
)

MESSAGE_ARGS = 0
MESSAGE_STDOUT = 1
MESSAGE_STDERR = 2
MESSAGE_RESULT = 3
MESSAGE_EXCEPTION = 4

BUFSIZE = 4096

if eg.debugLevel:
    def Msg(msg):
        print msg
else:
    def Msg(dummyMsg):
        pass



def GetUncPathOf(filePath):
    buf = create_string_buffer(1024)
    dwBufSize = DWORD(1024)
    err = WNetGetUniversalName(
        filePath,
        UNIVERSAL_NAME_INFO_LEVEL,
        buf,
        byref(dwBufSize)
    )
    if err == 0:
        return cast(buf, POINTER(UNIVERSAL_NAME_INFO)).contents.lpUniversalName
    elif err == ERROR_NOT_CONNECTED:
        pass
    else:
        print "GetUncPathOf Error:", err, FormatError(err)
    return filePath


def RunAs(filePath, asAdministrator, *args):
    sei = SHELLEXECUTEINFO()
    sei.cbSize = sizeof(SHELLEXECUTEINFO)
    sei.fMask = (
        SEE_MASK_FLAG_DDEWAIT | SEE_MASK_FLAG_NO_UI | SEE_MASK_NOCLOSEPROCESS
    )
    if asAdministrator:
        sei.lpVerb = u"runas"
    else:
        sei.lpVerb = u""
    sei.lpFile = GetUncPathOf(filePath)
    sei.lpParameters = " ".join(
        ['"%s"' % arg.replace('"', '""') for arg in args]
    )
    sei.nShow = SW_SHOWNORMAL
    if not ctypes.windll.shell32.ShellExecuteExW(byref(sei)):
        err = GetLastError()
        raise WindowsError(err, "ShellExecuteEx: %s" % FormatError(err))
    return sei.hProcess


def RunAsAdministrator(filePath, *args):
    return RunAs(filePath, True, *args)


def WritePipeMessage(hPipe, code, data):
    message = dumps((code, data))
    cbWritten = DWORD(0)
    fSuccess = WriteFile(
        hPipe,
        message,
        len(message),
        byref(cbWritten),
        None
    )
    if (not fSuccess) or (len(message) != cbWritten.value):
        raise Exception("WritePipeMessage failed")


def ExecAs(scriptPath, asAdministrator, funcName, *args, **kwargs):
    pipeName = "\\\\.\\pipe\\" + str(GUID.create_new())
    Msg("creating named pipe")
    hPipe = CreateNamedPipe(
        pipeName,
        PIPE_ACCESS_DUPLEX | FILE_FLAG_OVERLAPPED,
        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
        PIPE_UNLIMITED_INSTANCES,
        BUFSIZE,
        BUFSIZE,
        0,
        None
    )
    if hPipe == INVALID_HANDLE_VALUE:
        raise Exception("Error in creating Named Pipe")
    overlapped = OVERLAPPED()
    overlapped.hEvent = CreateEvent(None, 1, 0, None)
    try:
        Msg("calling ConnectNamedPipe")
        ConnectNamedPipe(hPipe, byref(overlapped))
        localPath = dirname(__file__.decode('mbcs'))
        Msg("starting subprocess")
        hProcess = RunAs(
            abspath(join(localPath, "..", "..", "EventGhost.exe")),
            asAdministrator,
            "-execfile",
            GetUncPathOf(join(localPath, "PipedProcessClient.py")),
            pipeName,
            str(eg.debugLevel)
        )
        Msg("waiting for subprocess to connect")
        pHandles = (HANDLE * 2)(overlapped.hEvent, hProcess)
        ret = WaitForMultipleObjects(2, pHandles, 0, 25000)
        if ret == WAIT_OBJECT_0:
            # connect event
            Msg("got connect event")
        elif ret == WAIT_OBJECT_0 + 1:
            raise Exception("Unexpected end of subprocess.")
        elif ret == WAIT_TIMEOUT:
            raise Exception("Timeout in waiting for subprocess.")
        else:
            raise Exception("Unknown return value")

        Msg("sending startup message")
        WritePipeMessage(
            hPipe,
            MESSAGE_ARGS,
            (GetUncPathOf(scriptPath), funcName, args, kwargs)
        )
        chBuf = create_string_buffer(BUFSIZE)
        cbRead = DWORD(0)
        while True:
            fSuccess = ReadFile(hPipe, chBuf, BUFSIZE, byref(cbRead), None)
            if ((fSuccess == 1) or (cbRead.value != 0)):
                code, data = loads(chBuf.value)
                if code == MESSAGE_STDERR:
                    sys.stderr.write(data)
                elif code == MESSAGE_STDOUT:
                    sys.stdout.write(data)
                elif code == MESSAGE_RESULT:
                    result = data
                    break
                elif code == MESSAGE_EXCEPTION:
                    break
                else:
                    raise Exception("Unknown message type %r" % code)
        FlushFileBuffers(hPipe)
        DisconnectNamedPipe(hPipe)
    finally:
        CloseHandle(hPipe)
        CloseHandle(overlapped.hEvent)
    if code == MESSAGE_EXCEPTION:
        raise Exception("Child process raised an exception\n" + data)
    return result


def ExecAsAdministrator(scriptPath, funcName, *args, **kwargs):
    """
    Execute some Python code in a process with elevated privileges.

    This call will only return, after the subprocess has terminated. The
    sys.stdout and sys.stderr streams of the subprocess will be directed to
    the calling process through a named pipe. All parameters for the function
    to call and its return value must be picklable.

    :param scriptPath: Path to the Python file to load.
    :param funcName: Name of the function to call inside the Python file
    :param args: Positional parameters for the function
    :param kwargs: Keyword parameters for the function
    :returns: The return value of the function
    """
    return ExecAs(scriptPath, True, funcName, *args, **kwargs)

