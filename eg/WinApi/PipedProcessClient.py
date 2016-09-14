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

import codecs
import imp
import sys
from cPickle import dumps, loads
from os.path import basename, dirname, splitext
from traceback import extract_tb, format_exception_only

# Local imports
from Dynamic import (
    byref,
    CloseHandle,
    create_string_buffer,
    CreateFile,
    DWORD,
    ERROR_MORE_DATA,
    FILE_SHARE_READ,
    FILE_SHARE_WRITE,
    GENERIC_READ,
    GENERIC_WRITE,
    GetLastError,
    INVALID_HANDLE_VALUE,
    OPEN_EXISTING,
    PIPE_READMODE_MESSAGE,
    ReadFile,
    SetNamedPipeHandleState,
    WaitNamedPipe,
    WinError,
    WriteFile,
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


def FormatException(excInfo):
    excType, excValue, excTraceback = excInfo
    lines = [u'Child process traceback (most recent call last)\n']
    if excTraceback:
        decode = codecs.getdecoder('mbcs')
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

def ReadPipeMessage(hPipe):
    data = ""
    fSuccess = 0
    chBuf = create_string_buffer(BUFSIZE)
    cbRead = DWORD(0)
    while not fSuccess:  # repeat loop if ERROR_MORE_DATA
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

def Main(pipeName, debugLevel):
    if debugLevel:
        def Debug(msg):
            sys.stdout.write(msg + "\n")
    else:
        def Debug(msg):
            pass
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
        Debug("reading startup message")
        code, (scriptPath, funcName, args, kwargs) = ReadPipeMessage(hPipe)
        Debug(
            "got startup message:\n"
            "  path: %r\n"
            "  funcName: %r\n"
            "  args: %r\n"
            "  kwargs: %r" % (scriptPath, funcName, args, kwargs)
        )
        if code != MESSAGE_ARGS:
            raise Exception("Unexpected message type")
        try:
            moduleName = splitext(basename(scriptPath))[0]
            try:
                moduleInfo = imp.find_module(moduleName, [dirname(scriptPath)])
            except ImportError:
                import zipimport
                for entry in sys.path:
                    if entry.endswith('.zip'):
                        zipImporter = zipimport.zipimporter(entry)
                        try:
                            module = zipImporter.load_module(moduleName)
                        except zipimport.ZipImportError:
                            continue
            else:
                module = imp.load_module(moduleName, *moduleInfo)
            func = getattr(module, funcName)
            result = func(*args, **kwargs)
            Debug("result: %r" % result)
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
    Main(sys.argv[1], int(sys.argv[2]))
