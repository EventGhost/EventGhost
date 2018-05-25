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

# changelog
# 18-12-2017: 23:07 -7:00UTC   K
#   Adds multiple pipe connection support.
# 15-05-2017: 14:00 -7:00UTC   K
#   Code rewrite, This is a pure python implementation
#   without the use of pywin32. One of the main things I have done is I have
#   created variables for each and every argument in any windows function call.
#   These variable names are identical to the names given in the Window API.
#   I did this so it is easier to follow the code for any possible error.
#
#   The code has been change in several ways. The first is it is now able to
#   be used by plugins. If they needed to create their own named pipe server.
#   or simple do a single transaction (send, receive).
#
#   The pipe has also been changed so the connection will remain active until
#   the client sends the CLOSE command.
#
#   I also changed the processing of command. The new processing checks to see
#   if the call is being made to eg.document or eg.mainFrame and if so it will
#   run the command in the main thread. when running the command there is a
#   timer that is set so in the event the execution of the command causes the
#   main thread to hang the pipe will return "MainThreadHung" after 5 seconds
#   has passed and the call has not returned. In all other cases a new thread
#   to run the command in is spawned and the same process takes place as with
#   the main thread except the return value in the event of a hang is
#   "UnableToProcessCommand"
#
#   I have added a mechanism in the server that will cause a loop with a wait
#   if there is already a pipe with the same name. if the pipe becomes
#   available the loop will exit and the pipe will be created. This was mainly
#   put into place because of the use of the cli switch -multiload.
#
#   The starting of the pipe was moved to DynamicModule.Main method. This was
#   done so the starting of the pipe would be done after the core was loaded
#   but before the core threads were started.
#
#   In all of the server side exception catching the connection will be
#   severed, and a possible traceback will be printed. Clients will a PipeError
#   (or subclass of) raised. The calling code is responsible for catching the
#   exceptions and handling them in a manner they see fit.
#
#   In the exception classes i have added __getitem__ so the calling code can
#   grab the original Windows API error. This can be used to compare to one of
#   the Error constants listed above.
#
#   from eg import NamedPipe
#
#   try:
#       res = NamedPipe.send_message('SomeNamedPipe', 'some message')
#       print res
#   except NamedPipe.PipeError as err:
#      if err[1] == NamedPipe.ERROR_FILE_NOT_FOUND:
#          print 'Pipe SomeNamedPipe is not available'
#      else:
#         raise
#
#   or you can do the following and for go the exception handling
#
#   from eg import NamedPipe
#
#   if NamedPipe.is_pipe_running('SomeNamedPipe'):
#       res = NamedPipe.send_message('SomeNamedPipe', 'some message')
#       print res
#   else:
#       print 'Pipe SomeNamedPipe is not available'


import sys
import ctypes
import threading
import traceback
import platform
from ctypes.wintypes import (
    HANDLE,
    ULONG,
    LPCSTR,
    LPCWSTR,
    DWORD,
    WORD,
    BOOL,
    BYTE,
    LPCVOID
)

__version__ = '0.1.0b'

# various c types that get used when passing data to the Windows functions
POINTER = ctypes.POINTER
PVOID = ctypes.c_void_p
LPVOID = ctypes.c_void_p
LPDWORD = POINTER(DWORD)
PULONG = POINTER(ULONG)
LPTSTR = LPCSTR
LPCTSTR = LPTSTR
UCHAR = ctypes.c_ubyte
NULL = None

# checking for x86/x64 not really necessary because EG only runs in x86
# here for completeness
if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong

# returned values for WaitForSingleObject
WAIT_OBJECT_0 = 0x00000000
WAIT_ABANDONED = 0x00000080
WAIT_TIMEOUT = 0x00000102
WAIT_FAILED = 0xFFFFFFFF

# can be passed to WaitForSingleObject
INFINITE = 0xFFFFFFFF

# bit identifiers for the pipe type, used in CreateNamedPipe
PIPE_ACCESS_INBOUND = 0x00000001
PIPE_ACCESS_OUTBOUND = 0x00000002
PIPE_ACCESS_DUPLEX = 0x00000003

# Number of pipe instances
PIPE_UNLIMITED_INSTANCES = 0x000000FF

# pipe type used in server creation of the pipe
# we are only using MESSAGE at the moment (here for completeness)
PIPE_TYPE_BYTE = 0x00000000
PIPE_TYPE_MESSAGE = 0x00000004

# pipe type used in client connection to the pipe
# we are only using MESSAGE at the moment (here for completeness)
PIPE_READMODE_BYTE = 0x00000000
PIPE_READMODE_MESSAGE = 0x00000002

# server use. whether to wait when ConnectNamedPipe is called
PIPE_WAIT = 0x00000000
PIPE_NOWAIT = 0x00000001

# server use, how long to wait.
NMPWAIT_USE_DEFAULT_WAIT = 0x00000000
NMPWAIT_NOWAIT = 0x00000001
NMPWAIT_WAIT_FOREVER = 0xFFFFFFFF


# server use, we are only using the NO_BUFFERING and FIRST_INSTANCE
# the rest are here for completeness
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_OVERLAPPED = 0x40000000
FILE_FLAG_DELETE_ON_CLOSE = 0x04000000
FILE_FLAG_OPEN_NO_RECALL = 0x00100000
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_FLAG_OPEN_REQUIRING_OPLOCK = 0x00040000
FILE_FLAG_POSIX_SEMANTICS = 0x0100000
FILE_FLAG_WRITE_THROUGH = 0x80000000
FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000
FILE_FLAG_SESSION_AWARE = 0x00800000
FILE_FLAG_RANDOM_ACCESS = 0x10000000
FILE_FLAG_NO_BUFFERING = 0x20000000
FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000

FILE_ATTRIBUTE_NORMAL = 0x00000080

# used in client OpenFile and
OPEN_EXISTING = 0x00000003
GENERIC_ALL = 0x10000000
GENERIC_EXECUTE = 0x20000000
GENERIC_WRITE = 0x40000000
GENERIC_READ = 0x80000000

# here for completeness
PIPE_CLIENT_END = 0x00000000
PIPE_SERVER_END = 0x00000001

FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002

# return error codes from GetLastError not all of these errors are specific to
# named pipes but they are used.
ERROR_INVALID_HANDLE = 0x00000006
ERROR_PIPE_CONNECTED = 0x00000217
ERROR_PIPE_LISTENING = 0x00000218
ERROR_BROKEN_PIPE = 0x0000006D
ERROR_PIPE_LOCAL = 0x000000E5
ERROR_MORE_DATA = 0x000000EA
ERROR_BAD_PIPE = 0x000000E6
ERROR_PIPE_BUSY = 0x000000E7
ERROR_NO_DATA = 0x000000E8
ERROR_PIPE_NOT_CONNECTED = 0x000000E9
ERROR_INVALID_NAME = 0x0000007B
ERROR_FILE_NOT_FOUND = 0x00000002
ERROR_ALREADY_EXISTS = 0x000000B7
ERROR_ACCESS_DENIED = 0x00000005
ERROR_IO_INCOMPLETE = 0x000003E4
ERROR_IO_PENDING = 0x000003E5
INVALID_HANDLE_VALUE = -1

# identifiers passed to FormatMessage located in PipeError
FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000


# kernel32 API
kernel32 = ctypes.windll.kernel32
# Windows security API
advapi32 = ctypes.windll.advapi32


# c type structure that handles the overlapped io portion of the pipe
# not used currently here for completeness
# -----------------------------------------------------------------------------
# noinspection PyPep8Naming
class _OVERLAPPED_STRUCTURE(ctypes.Structure):
    _fields_ = [
        ('Offset', DWORD),
        ('OffsetHigh', DWORD)
    ]


# noinspection PyPep8Naming
class _OVERLAPPED_UNION(ctypes.Union):
    _anonymous_ = ('_OVERLAPPED_STRUCTURE',)
    _fields_ = [
        ('_OVERLAPPED_STRUCTURE', _OVERLAPPED_STRUCTURE),
        ('Pointer', PVOID)
    ]


# noinspection PyPep8Naming
class _OVERLAPPED(ctypes.Structure):
    _anonymous_ = ('_OVERLAPPED_UNION',)
    _fields_ = [
        ('Internal', ULONG_PTR),
        ('InternalHigh', ULONG_PTR),
        ('_OVERLAPPED_UNION', _OVERLAPPED_UNION),
        ('hEvent', HANDLE)
    ]


OVERLAPPED = _OVERLAPPED
LPOVERLAPPED = ctypes.POINTER(_OVERLAPPED)
# -----------------------------------------------------------------------------


# c type security structures that set the security of the pipe
# the ACL bits are not used currently and are here for completeness
# -----------------------------------------------------------------------------
class _ACL(ctypes.Structure):
    _fields_ = [
        ('AclRevision', BYTE),
        ('Sbz1', BYTE),
        ('AclSize', WORD),
        ('AceCount', WORD),
        ('Sbz2', WORD)
    ]


ACL = _ACL
PACL = ctypes.POINTER(_ACL)


# noinspection PyPep8Naming
class _SECURITY_DESCRIPTOR(ctypes.Structure):
    _fields_ = [
        ('Revision', UCHAR),
        ('Sbz1', UCHAR),
        ('Control', WORD),
        ('Owner', PVOID),
        ('Group', PVOID),
        ('Sacl', PACL),
        ('Dacl', PACL)
    ]


SECURITY_DESCRIPTOR = _SECURITY_DESCRIPTOR
PSECURITY_DESCRIPTOR = ctypes.POINTER(_SECURITY_DESCRIPTOR)


# noinspection PyPep8Naming
class _SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('nLength', DWORD),
        ('lpSecurityDescriptor', PSECURITY_DESCRIPTOR),
        ('bInheritHandle', BOOL)
    ]


SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
PSECURITY_ATTRIBUTES = ctypes.POINTER(_SECURITY_ATTRIBUTES)
LPSECURITY_ATTRIBUTES = ctypes.POINTER(_SECURITY_ATTRIBUTES)

SetSecurityDescriptorDacl = advapi32.SetSecurityDescriptorDacl
# -----------------------------------------------------------------------------

# defining of the kernel32 functions used and they return types.
# I have found there is no real need to set the argument types and this is a
# waste of time and code.
# -----------------------------------------------------------------------------

GetLastError = kernel32.GetLastError
GetLastError.restype = DWORD

GetNamedPipeClientProcessId = kernel32.GetNamedPipeClientProcessId
GetNamedPipeClientProcessId.restype = BOOL

GetNamedPipeClientSessionId = kernel32.GetNamedPipeClientSessionId
GetNamedPipeClientSessionId.restype = BOOL

GetNamedPipeServerProcessId = kernel32.GetNamedPipeServerProcessId
GetNamedPipeServerProcessId.restype = BOOL

GetNamedPipeServerSessionId = kernel32.GetNamedPipeServerSessionId
GetNamedPipeServerSessionId.restype = BOOL

DisconnectNamedPipe = kernel32.DisconnectNamedPipe
DisconnectNamedPipe.restype = BOOL

ResetEvent = kernel32.ResetEvent
ResetEvent.restype = BOOL

FlushFileBuffers = kernel32.FlushFileBuffers
FlushFileBuffers.restype = BOOL

WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.restype = DWORD

WaitNamedPipe = kernel32.WaitNamedPipeW
WaitNamedPipe.restype = BOOL

SetNamedPipeHandleState = kernel32.SetNamedPipeHandleState
SetNamedPipeHandleState.restype = BOOL

FormatMessage = kernel32.FormatMessageW
FormatMessage.restype = DWORD

CloseHandle = kernel32.CloseHandle
CloseHandle.restype = BOOL

CreateEvent = kernel32.CreateEventW
CreateEvent.restype = HANDLE

CreateFile = kernel32.CreateFileA
CreateFile.restype = HANDLE

CreateNamedPipe = kernel32.CreateNamedPipeW
CreateNamedPipe.restype = HANDLE

ConnectNamedPipe = kernel32.ConnectNamedPipe
ConnectNamedPipe.restype = BOOL

WriteFile = kernel32.WriteFile
WriteFile.restype = BOOL

ReadFile = kernel32.ReadFile
ReadFile.restype = BOOL

GetOverlappedResult = kernel32.GetOverlappedResult
GetOverlappedResult.restype = BOOL
# -----------------------------------------------------------------------------


# exception classes
# -----------------------------------------------------------------------------

class PipeError(Exception):

    def __init__(self, msg, pipe_handle=None):
        if isinstance(msg, int):
            err = msg
            msg = format_error(err)
        else:
            err = None

        self._msg = [msg, err, pipe_handle]

    def __getitem__(self, item):
        return self._msg[item]

    def __str__(self):
        return self._msg[0]


class PipeDataError(PipeError):
    pass


class PipeCommandError(PipeError):
    pass


class PipeConnectionError(PipeError):
    pass


# this is used in the exception classes to query windows for a nice human
# readable error message.
def format_error(err):

    dwFlags = DWORD(FORMAT_MESSAGE_FROM_SYSTEM)
    lpSource = NULL
    dwMessageId = DWORD(err)
    dwLanguageId = DWORD(0)
    lpBuffer = ctypes.create_unicode_buffer(4096)
    nSize = DWORD(4096)
    Arguments = NULL

    kernel32.FormatMessageW(
        dwFlags,
        lpSource,
        dwMessageId,
        dwLanguageId,
        lpBuffer,
        nSize,
        Arguments
    )
    err_hex = '0x' + '{0:#0{1}X}'.format(err, 10)[2:]
    return '{0} [{1}]'.format(lpBuffer.value.rstrip(), err_hex)

# -----------------------------------------------------------------------------


# Checks for the instance of a running pipe. I created this new function so
# eg.NamedPipe can be used in plugins if needed.
def is_pipe_running(pipe_name):
    lpName = ctypes.create_unicode_buffer(_create_pipe_name(pipe_name))
    dwOpenMode = DWORD(PIPE_ACCESS_DUPLEX | FILE_FLAG_FIRST_PIPE_INSTANCE)
    dwPipeMode = DWORD(PIPE_TYPE_MESSAGE | PIPE_WAIT | PIPE_READMODE_MESSAGE)
    nMaxInstances = DWORD(PIPE_UNLIMITED_INSTANCES)
    nOutBufferSize = DWORD(4096)
    nInBufferSize = DWORD(4096)
    nDefaultTimeOut = DWORD(60000)
    lpSecurityAttributes = NULL

    hNamedPipe = CreateNamedPipe(
        lpName,
        dwOpenMode,
        dwPipeMode,
        nMaxInstances,
        nOutBufferSize,
        nInBufferSize,
        nDefaultTimeOut,
        lpSecurityAttributes
    )
    err = GetLastError()
    CloseHandle(hNamedPipe)

    if err in (ERROR_ALREADY_EXISTS, ERROR_ACCESS_DENIED):
        return True

    elif not err:
        return False

    else:
        raise PipeConnectionError(err)


# This is specific to checking is the eventghost named pipe is running
def is_eg_running():
    return is_pipe_running('eventghost')


# formats the pipe name properly, Windows 0 requires a different pipe
# formatting
def _create_pipe_name(name):
    if platform.release() == '10':
        return '\\\\.\\pipe\\LOCAL\\' + name
    else:
        return '\\\\.\\pipe\\' + name


# this is a pipe instance class, it handles all of the nitty gritty for server
# pipe connections.
class Pipe(object):
    """
    Thread class for handling additional pipe connections.
    """

    def __init__(self, parent, pipe_name, pipe_id):
        """

        :param parent: Server class
        :type parent: instance
        :param pipe_id: ID assigned to this pipe instance.
        :type pipe_id: int
        :param security_attributes: Windows SACL and DACL data for creating the
            pipe.
        :type security_attributes: win32security.SECURITY_ATTRIBUTES instance
        """
        self._pipe = None
        self._parent = parent
        self._pipe_id = pipe_id
        self._pipe_name = pipe_name
        self.is_waiting = True
        self.closed = False
        self._event = threading.Event()

        import eg

        eg.PrintDebugNotice(
            'Named Pipe: Creating pipe {0}'.format(pipe_id)
        )

        lpName = ctypes.create_unicode_buffer(_create_pipe_name(pipe_name))
        dwOpenMode = DWORD(PIPE_ACCESS_DUPLEX | FILE_FLAG_FIRST_PIPE_INSTANCE)
        dwPipeMode = DWORD(PIPE_TYPE_MESSAGE | PIPE_WAIT | PIPE_READMODE_MESSAGE)
        nMaxInstances = DWORD(PIPE_UNLIMITED_INSTANCES)
        nOutBufferSize = DWORD(4096)
        nInBufferSize = DWORD(4096)
        nDefaultTimeOut = DWORD(60000)

        # This is where the permissions get created for the pipe
        lpSecurityDescriptor = PSECURITY_DESCRIPTOR()
        lpSecurityAttributes = SECURITY_ATTRIBUTES()
        lpSecurityAttributes.lpSecurityDescriptor = lpSecurityDescriptor
        lpSecurityAttributes.nLength = ctypes.sizeof(lpSecurityDescriptor)

        bDaclPresent = BOOL(True)
        pDacl = NULL
        bDaclDefaulted = BOOL(False)

        SetSecurityDescriptorDacl(
            ctypes.byref(lpSecurityDescriptor),
            bDaclPresent,
            pDacl,
            bDaclDefaulted
        )

        if self._parent.running_pipes:
            dwOpenMode = DWORD(PIPE_ACCESS_DUPLEX)

        self.hNamedPipe = CreateNamedPipe(
            lpName,
            dwOpenMode,
            dwPipeMode,
            nMaxInstances,
            nOutBufferSize,
            nInBufferSize,
            nDefaultTimeOut,
            ctypes.byref(lpSecurityAttributes)
        )

        self._thread = threading.Thread(
            name='{0}.Pipe.{1}.Thread'.format(pipe_name, pipe_id),
            target=self.run
        )
        self._thread.daemon = True

    def open(self):
        self._thread.start()

    def run(self):
        lpOverlapped = NULL
        ConnectNamedPipe(self.hNamedPipe, lpOverlapped)

        self.is_waiting = False
        self._parent.check_available_pipes()
        hFile = self.hNamedPipe

        while not self._event.isSet():
            result = 0
            nNumberOfBytesToRead = DWORD(4096)
            response = ''

            while not result:
                lpBuffer = ctypes.create_string_buffer(4096)
                lpNumberOfBytesRead = DWORD()

                result = ReadFile(
                    hFile,
                    lpBuffer,
                    nNumberOfBytesToRead,
                    ctypes.byref(lpNumberOfBytesRead),
                    lpOverlapped
                )

                err = GetLastError()

                if err == ERROR_MORE_DATA:
                    response += lpBuffer.value
                    result = 0

                if err == ERROR_NO_DATA:
                    result = 0
                    continue

                elif result:
                    response += lpBuffer.value

                elif err:
                    result = 1
                    response = 'CLOSE'

            if response:
                eg.PrintDebugNotice(
                    '>> {0} Pipe {1}: Data : {2}'.format(
                        self._pipe_name,
                        self._pipe_id,
                        response
                    )
                )

                if response == 'CLOSE':
                    self.close()

                else:
                    result = process_command(
                        self._pipe_id,
                        response,
                    )

                self.write(str(repr(result)))

    def close(self):
        self._event.set()
        eg.PrintDebugNotice(
            'Disconnecting pipe {0}: {1}'.format(
                self._pipe_name,
                self._pipe_id
            )
        )
        try:
            DisconnectNamedPipe(self.hNamedPipe)
        except:
            pass

        try:
            eg.PrintDebugNotice(
                'Closing pipe {0}: {1}'.format(
                    self._pipe_name,
                    self._pipe_id
                )
            )
            CloseHandle(self.hNamedPipe)
        except:
            pass

        self.closed = True
        self._parent.check_available_pipes()

    def write(self, msg):

        result = 0
        hFile = self.hNamedPipe
        lpOverlapped = NULL

        while not result:
            lpBuffer = ctypes.create_string_buffer(msg)
            nNumberOfBytesToWrite = DWORD(len(msg))
            lpNumberOfBytesWritten = DWORD()

            result = WriteFile(
                hFile,
                lpBuffer,
                nNumberOfBytesToWrite,
                ctypes.byref(lpNumberOfBytesWritten),
                lpOverlapped
            )

            err = GetLastError()

            if err == ERROR_MORE_DATA:
                msg = msg[lpNumberOfBytesWritten.value:]
                result = 0

            elif err == ERROR_PIPE_BUSY:
                result = 0

            elif err:
                result = 1
                self.close()


def process_command(pipe_id, data):
    import eg

    try:
        command, data = data.split(',', 1)
    except ValueError:
        command = data
        data = '()'

    eg.PrintDebugNotice(
        'Pipe {0}: Command: {1}, Parameters: {2}'.format(
            pipe_id,
            command,
            data
        )
    )

    command = command.strip()
    data = data.strip()

    try:
        if '=' in command:
            eg.PrintDebugNotice(
                'Pipe {0}: Command Format Error: {1}'.format(
                    pipe_id,
                    command
                )
            )
            return 'CommandFormatError'

        if not data.startswith('dict') and '=' in data:
            eg.PrintDebugNotice(
                'Pipe {0}: Parameter Format Error: {1}'.format(
                    pipe_id,
                    data
                )
            )
            return 'ParameterFormatError'

        if (
            data[0] not in ('(', '[', '{') and
            not data.startswith('dict')
        ):
            eg.PrintDebugNotice(
                'Pipe {0}: Parameter Format Error: {1}'.format(
                    pipe_id,
                    data
                )
            )
            return 'ParameterFormatError'

        try:
            func = eval(command.split('(', 1)[0])
        except SyntaxError:
            eg.PrintDebugNotice(
                'Pipe {0}: Command Malformed Error: {1}'.format(
                    pipe_id,
                    command
                )
            )
            return 'CommandMalformedError'
        except AttributeError:
            eg.PrintDebugNotice(
                'Pipe {0}: Command Not Found Error: {1}'.format(
                    pipe_id,
                    command
                )
            )
            return 'CommandNotFoundError'
        else:
            if isinstance(func, (str, unicode)):
                eg.PrintDebugNotice(
                    'Pipe {0}: Command Format Error: {1}'.format(
                        pipe_id,
                        command
                    )
                )
                return 'CommandFormatError'
        try:
            data = eval(data)
        except SyntaxError:
            eg.PrintDebugNotice(
                'Pipe {0}: Parameter Malformed Error: {1}'.format(
                    pipe_id,
                    data
                )
            )
            return 'ParameterMalformedError'

        if not isinstance(data, (dict, list, tuple)):
            eg.PrintDebugNotice(
                'Pipe {0}: Parameter Format Error: {1}'.format(
                    pipe_id,
                    str(data)
                )
            )
            return 'ParameterFormatError'

    except:
        traceback.print_exc()
    else:
        event = threading.Event()

        def run():
            if isinstance(data, dict):
                res[0] = func(**data)
            elif isinstance(data, (tuple, list)):
                res[0] = func(*data)

            eg.PrintDebugNotice(
                'Pipe {0}: Return data: {1}'.format(
                    pipe_id,
                    str(res[0])
                )
            )

            event.set()
        if (
            command.startswith('eg.document') or
            command.startswith('eg.mainFrame')
        ):
            res = ['MainThreadHung']
            wx.CallAfter(run)
            event.wait(5)
            return res[0]
        else:
            res = ['UnableToProcessCommand']
            t = threading.Thread(target=run)
            t.daemon = True
            t.start()
            event.wait(5)
            return res[0]


class Server:
    """
    Receiving thread class for the "\\.\pipe\eventghost" named pipe.

    When EventGhost gets run a named pipe gets created by the name of
    "\\.\pipe\eventghost". The pipe is created so that everyone has full
    control. This allows for an instance of EventGhost to be running as
    Administrator and be able to send commands into EventGhost as a user.

    EventGhost command line arguments have been changed to use
    this pipe and has opened up the ability to be able to do things like hide
    the current running instance from the command line. It has also
    significantly increased the speed in which the operations are carried out.

    This has been added in a way that will allow for another application that
    is running on the same computer as EventGhost to be able to make
    EventGhost perform various tasks. The API is as follows.

    all data written to the pipe has be done as a string. this is a message
    only pipe and you are not able to send any byte data through it. It is also
    one way communications. the running instance of EventGhost will never
    write anything to the pipe. the structure of the message is

    function/class/method name, *args or **kwargs

    you are only able to make a call to an existing function/class/method you
    are not able to set a attributes value directly. you will have to create a
    function and then you can have data passed to that function via the named
    pipe and have the function then set the attributes value.

    the args either have to be a list or a tuple empty if there are no
    parameters to be sent.

    kwargs can either be formatted as
    dict(keyword1=None, keyword2=None)
    or
    {'keyword1': None, 'keyword2': None}

    any public class/method/function can be accessed by use of this pipe.

    when a command is received it passes the command to the main thread to be
    evaluated for correctness and to be run. The reason this is done is 2 fold
    It is so that the named pipe can be created once again as fast as possible
    without having to wait for the command to finish executing. But also if a
    command is used that deals with the GUI aspects of EG a lot of the wx
    components need to be ran from the main thread.

    """

    def __init__(self, pipe_name='eventghost'):
        self._pipe_name = pipe_name
        self._thread = None
        self.running_pipes = []
        self._pipe_id = -1
        self._available_event = threading.Event()

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(
                name='{0}.Pipe.Thread'.format(self._pipe_name),
                target=self.run
            )
            self._thread.daemon = True
            self._thread.start()

    def get_pipe_id(self):
        self._pipe_id += 1
        return self._pipe_id

    def check_available_pipes(self):
        self._available_event.set()

    def run(self):
        def create_pipe():
            pipe = Pipe(
                self,
                self._pipe_name,
                self.get_pipe_id()
            )
            self.running_pipes += [pipe]
            pipe.open()

        while is_pipe_running(self._pipe_name):
            self._available_event.wait(0.5)

        while True:
            for pipe in self.running_pipes[:]:
                if pipe.closed:
                    self.running_pipes.remove(pipe)

            if not self.running_pipes:
                create_pipe()
            else:
                for pipe in self.running_pipes:
                    if pipe.is_waiting:
                        break
                else:
                    create_pipe()

            self._available_event.wait()
            self._available_event.clear()


def send_message(msg, pipe_name='eventghost'):
    lpFileName = _create_pipe_name(pipe_name)
    while True:
        hNamedPipe = CreateFile(
            lpFileName,
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            FILE_FLAG_NO_BUFFERING,
            NULL
        )

        err = GetLastError()

        lpNamedPipeName = lpFileName
        nTimeOut = DWORD(2000)

        if hNamedPipe != INVALID_HANDLE_VALUE and err != ERROR_PIPE_BUSY:
            break

        elif not WaitNamedPipe(lpNamedPipeName, nTimeOut):
            CloseHandle(hNamedPipe)
            raise PipeConnectionError(err, hNamedPipe)

    lpMode = DWORD(PIPE_READMODE_MESSAGE)
    lpMaxCollectionCount = NULL
    lpCollectDataTimeout = NULL

    result = SetNamedPipeHandleState(
        hNamedPipe,
        ctypes.byref(lpMode),
        lpMaxCollectionCount,
        lpCollectDataTimeout
    )

    if not result:
        err = GetLastError()
        CloseHandle(hNamedPipe)
        raise PipeConnectionError(err, hNamedPipe)

    result = 0
    hFile = hNamedPipe
    lpOverlapped = NULL

    while not result:
        lpBuffer = ctypes.create_string_buffer(msg)
        nNumberOfBytesToWrite = DWORD(len(msg))
        lpNumberOfBytesWritten = DWORD()

        result = WriteFile(
            hFile,
            lpBuffer,
            nNumberOfBytesToWrite,
            ctypes.byref(lpNumberOfBytesWritten),
            lpOverlapped
        )

        err = GetLastError()

        if err == ERROR_MORE_DATA:
            msg = msg[lpNumberOfBytesWritten.value:]
            result = 0
        elif err in (
            ERROR_INVALID_HANDLE,
            ERROR_BROKEN_PIPE,
            ERROR_BAD_PIPE,
            ERROR_PIPE_NOT_CONNECTED
        ):
            CloseHandle(hFile)
            raise PipeConnectionError(err, hFile)

        elif result:
            break

        elif err:
            CloseHandle(hFile)
            raise PipeError(err, hFile)

    result = 0
    nNumberOfBytesToRead = DWORD(4096)
    lpOverlapped = NULL
    response = ''

    while not result:
        lpBuffer = ctypes.create_string_buffer(4096)
        lpNumberOfBytesRead = DWORD()

        result = ReadFile(
            hFile,
            lpBuffer,
            nNumberOfBytesToRead,
            ctypes.byref(lpNumberOfBytesRead),
            lpOverlapped
        )

        err = GetLastError()

        if err == ERROR_MORE_DATA:
            response += lpBuffer.value
            result = 0

        elif err in (
            ERROR_INVALID_HANDLE,
            ERROR_BROKEN_PIPE,
            ERROR_BAD_PIPE,
            ERROR_PIPE_NOT_CONNECTED
        ):
            CloseHandle(hFile)
            raise PipeConnectionError(err, hFile)

        elif result:
            response += lpBuffer.value

        elif err:
            CloseHandle(hFile)
            raise PipeError(err, hFile)

    try:
        return eval(response)
    except SyntaxError:
        return response
    finally:
        msg = 'CLOSE'
        lpBuffer = ctypes.create_string_buffer(msg)
        nNumberOfBytesToWrite = DWORD(len(msg))
        lpNumberOfBytesWritten = NULL
        lpOverlapped = NULL

        try:
            WriteFile(
                hFile,
                lpBuffer,
                nNumberOfBytesToWrite,
                lpNumberOfBytesWritten,
                lpOverlapped
            )
        except WindowsError:
            pass

        CloseHandle(hFile)
