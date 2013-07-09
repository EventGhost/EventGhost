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
import codecs
import imp
from traceback import extract_tb, format_exception_only
from os.path import dirname, splitext, basename
from cPickle import dumps, loads

from Dynamic import (
    byref,
    create_string_buffer,
    WinError,
    DWORD,

    ReadFile,
    WriteFile,
    SetNamedPipeHandleState,
    WaitNamedPipe,
    CloseHandle,
    GetLastError,
    CreateFile,

    GENERIC_READ,
    GENERIC_WRITE,
    FILE_SHARE_READ,
    FILE_SHARE_WRITE,
    OPEN_EXISTING,
    PIPE_READMODE_MESSAGE,
    ERROR_MORE_DATA,
    INVALID_HANDLE_VALUE,
)

BUFSIZE = 4096
MESSAGE_ARGS = 0
MESSAGE_STDOUT = 1
MESSAGE_STDERR = 2
MESSAGE_RESULT = 3
MESSAGE_EXCEPTION = 4



class PipeStream(object):

    def __init__(self, hPipe, code):
        self.hPipe = hPipe
        self.code = code

    def write(self, data):
        WritePipeMessage(self.hPipe, self.code, data)



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


def Main():
    pipeName = sys.argv[1]
    debug = int(sys.argv[2])
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
        if debug:
            print "reading startup message"
        code, (scriptPath, funcName, args, kwargs) = ReadPipeMessage(hPipe)
        if debug:
            print (
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
            if debug:
                print "result: %r" % result
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
    Main()

