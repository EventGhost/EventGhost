# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import imp
import ctypes
import codecs
from traceback import extract_tb, format_exception_only
from os.path import join, dirname, abspath, splitext, basename
from cPickle import dumps, loads
from comtypes import GUID
from Dynamic import (
    byref,
    sizeof,
    create_string_buffer,
    cast,
    WinError,
    POINTER,
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
    FormatError,
    CreateEvent,
    WaitForMultipleObjects,

    OVERLAPPED,
    GENERIC_READ,
    GENERIC_WRITE,
    FILE_SHARE_READ,
    FILE_SHARE_WRITE,
    OPEN_EXISTING,
    PIPE_ACCESS_DUPLEX,
    PIPE_TYPE_MESSAGE,
    PIPE_READMODE_MESSAGE,
    PIPE_WAIT,
    PIPE_UNLIMITED_INSTANCES,
    ERROR_PIPE_BUSY,
    ERROR_MORE_DATA,
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

DEBUG = eg.debugLevel
if DEBUG:
    def Msg(msg):
        print msg
else:
    def Msg(dummyMsg):
        pass


class PipeStream(object):

    def __init__(self, hPipe, code):
        self.hPipe = hPipe
        self.code = code

    def write(self, data):
        WritePipeMessage(self.hPipe, self.code, data)



def GetUncPathOf(filePath):
    BUF_SIZE = 1024
    buf = create_string_buffer(BUF_SIZE)
    size = DWORD(BUF_SIZE)
    err = WNetGetUniversalName(
        filePath,
        UNIVERSAL_NAME_INFO_LEVEL,
        buf,
        byref(size)
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
        raise Exception("Write File failed")


def ReadPipeMessage(hPipe):
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
        None #byref(sa)
    )
    if hPipe == INVALID_HANDLE_VALUE:
        raise Exception("Error in creating Named Pipe")
    overlapped = OVERLAPPED()
    overlapped.hEvent = CreateEvent(None, 1, 0, None)
    try:
        Msg("calling ConnectNamedPipe")
        ConnectNamedPipe(hPipe, byref(overlapped))
        executable = abspath(join(
            dirname(__file__.decode(sys.getfilesystemencoding())),
            "..",
            "..",
            "EventGhost.exe"
        ))
        Msg("starting subprocess")
        #print GetUncPathOf(__file__.decode(sys.getfilesystemencoding()))
        hProcess = RunAs(
            executable,
            asAdministrator,
            "-execscript",
            GetUncPathOf(__file__.decode(sys.getfilesystemencoding())),
            pipeName,
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

#        if fConnected == 0 and GetLastError() == ERROR_PIPE_CONNECTED:
#            fConnected = 1
#        if fConnected != 1:
#            raise Exception("Could not connect to the Named Pipe")
#
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


def FormatException(excInfo):
    excType, excValue, excTraceback = excInfo
    lines = [u'Child process traceback (most recent call last)\n']
    if excTraceback:
        decode = codecs.getdecoder(sys.getfilesystemencoding())
        for filename, lineno, funcname, text in extract_tb(excTraceback):
            lines.append(
                u'  File "%s", line %d, in %s\n' % (
                    decode(filename)[0], lineno, funcname
                )
            )
            if text:
                lines.append(u"    %s\n" % text)
    lines += format_exception_only(excType, excValue)
    return u"".join(lines)


def Client(pipeName):
    if not WaitNamedPipe(pipeName, 5000):
        raise WinError()
    hPipe = CreateFile(
        pipeName,
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        None
    )
    if hPipe == INVALID_HANDLE_VALUE:
        raise WinError()
    try:
        # The pipe connected; change to message-read mode.
        dwMode = DWORD(PIPE_READMODE_MESSAGE)
        if not SetNamedPipeHandleState(hPipe, byref(dwMode), None, None):
            raise WinError()

        sys.stderr = PipeStream(hPipe, MESSAGE_STDERR)
        sys.stdout = PipeStream(hPipe, MESSAGE_STDOUT)
        Msg("reading startup message")
        code, (scriptPath, funcName, args, kwargs) = ReadPipeMessage(hPipe)
        Msg(
            "got startup message:\n"
            "  path: %r\n"
            "  funcName: %r\n"
            "  args: %r\n"
            "  kwargs: %r" %
                (scriptPath, funcName, args, kwargs)
        )
        if code != MESSAGE_ARGS:
            raise Exception("Unexpected message type")
        try:
            moduleName = splitext(basename(scriptPath))[0]
            moduleInfo = imp.find_module(moduleName, [dirname(scriptPath)])
            module = imp.load_module(moduleName, *moduleInfo)
            func = getattr(module, funcName)
            result = func(*args, **kwargs)
        except:
            WritePipeMessage(
                hPipe,
                MESSAGE_EXCEPTION,
                FormatException(sys.exc_info())
            )
        else:
            WritePipeMessage(hPipe, MESSAGE_RESULT, result)
    finally:
        CloseHandle(hPipe)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        Client(sys.argv[1])

