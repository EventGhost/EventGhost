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
# 21-04-2018: 12:46 -7:00   K
# Complete rewrite. This is now a multi-threaded asynchronous overlapped IO
# pipe written in pure python using only the std lib. I have added commented
# lines detailing how this whole system works.
#
# 18-12-2017: 23:07 -7:00   K
# Adds multiple pipe connection support.

import wx
import ctypes
import threading
import platform
import traceback
from ctypes.wintypes import (
    HANDLE,
    ULONG,
    LPCSTR,
    DWORD,
    WORD,
    LPVOID,
    BOOL,
    BYTE,
)

# various c types that get used when passing data to the Windows functions
PVOID = ctypes.c_void_p
UCHAR = ctypes.c_ubyte
ULONG_PTR = ctypes.POINTER(ULONG)
NULL = None

# returned values for kernel32.WaitForSingleObject
WAIT_OBJECT_0 = 0x00000000
WAIT_ABANDONED = 0x00000080
WAIT_TIMEOUT = 0x00000102
WAIT_FAILED = 0xFFFFFFFF

# can be passed to kernel32.WaitForSingleObject
INFINITE = 0xFFFFFFFF

# bit identifiers for the pipe type, used in kernel32.CreateNamedPipeA
PIPE_ACCESS_INBOUND = 0x00000001
PIPE_ACCESS_OUTBOUND = 0x00000002
PIPE_ACCESS_DUPLEX = 0x00000003

PIPE_UNLIMITED_INSTANCES = 0x000000FF

PIPE_TYPE_BYTE = 0x00000000
PIPE_TYPE_MESSAGE = 0x00000004

PIPE_READMODE_BYTE = 0x00000000
PIPE_READMODE_MESSAGE = 0x00000002

PIPE_WAIT = 0x00000000
PIPE_NOWAIT = 0x00000001

NMPWAIT_USE_DEFAULT_WAIT = 0x00000000
NMPWAIT_NOWAIT = 0x00000001
NMPWAIT_WAIT_FOREVER = 0xFFFFFFFF

FILE_FLAG_OVERLAPPED = 0x40000000
FILE_ATTRIBUTE_NORMAL = 0x00000080

FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000

# bit identifiers passed to kernel32.OpenFile
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

# return codes for a variety of the kernel32 functions
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
ERROR_FILE_NOT_FOUND = 0x00000002
ERROR_ALREADY_EXISTS = 0x000000B6
ERROR_ACCESS_DENIED = 0x00000005
ERROR_IO_PENDING = 0x000003E5
INVALID_HANDLE_VALUE = -1

# bit identifiers passed to kernel32.FormatMessageA located in PipeError
FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000

# Used to identify the current data state. PipeInstance class
CONNECTING_STATE = 0
READING_STATE = 1
WRITING_STATE = 2

# various settings that can be changed
BUFFER_SIZE = 0x00001000
PIPE_TIMEOUT = 20000

# we have to do some windows version checking. Windows 10 the pipe name needs
# to be formatted differently
WINDOWS_10 = platform.release() == '10'

# kernel32 API
kernel32 = ctypes.windll.kernel32
# Windows security API
advapi32 = ctypes.windll.advapi32


# c type structure that handles the overlapped io portion of the pipe
class _OVERLAPPED_STRUCTURE(ctypes.Structure):
    _fields_ = [
        ('Offset', DWORD),
        ('OffsetHigh', DWORD)
    ]


class _OVERLAPPED_UNION(ctypes.Union):
    _anonymous_ = ('_OVERLAPPED_STRUCTURE',)
    _fields_ = [
        ('_OVERLAPPED_STRUCTURE', _OVERLAPPED_STRUCTURE),
        ('Pointer', PVOID)
    ]


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


# c type security structures that set the security of the pipe
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


class _SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('nLength', DWORD),
        ('lpSecurityDescriptor', PSECURITY_DESCRIPTOR),
        ('bInheritHandle', BOOL)
    ]


SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
PSECURITY_ATTRIBUTES = ctypes.POINTER(_SECURITY_ATTRIBUTES)
LPSECURITY_ATTRIBUTES = ctypes.POINTER(_SECURITY_ATTRIBUTES)


# a single Exception class that handles all pipe errors. This queries Windows
# for an error message if an error code was supplied otherwise it will use the
# strng that has been passed to it. You can check the error code by doing the
# following
#
# try:
#     # do pipe code here
# except PipeError as err:
#     print err[1]
#
# the above will print out None if it is an error that does not have a code
# passed otherwise it will print out a decimal version of the windows error
# code

class PipeError(Exception):
    def __init__(self, msg):
        if isinstance(msg, int):
            buf = ctypes.create_string_buffer(4096)

            kernel32.FormatMessageA(
                DWORD(FORMAT_MESSAGE_FROM_SYSTEM),
                NULL,
                DWORD(msg),
                DWORD(0),
                buf,
                DWORD(4096),
                NULL
            )
            err = msg
            err_hex = '0x' + '{0:#0{1}X}'.format(msg, 10)[2:]
            msg = '{0} [{1}]'.format(buf.value.rstrip(), err_hex)
            self._msg = [msg, err]
        else:
            self._msg = [msg, None]

    def __getitem__(self, item):
        return self._msg[item]

    def __str__(self):
        return self._msg[0]


# formats the pipe name properly
def _create_pipe_name(name):
    if WINDOWS_10:
        return '\\\\.\\pipe\\LOCAL\\' + name
    else:
        return '\\\\.\\pipe\\' + name


# used to check the existence of the named pipe. This is a means to know
# whether or not EG is running
def is_eg_running():
    pipe_handle = kernel32.CreateNamedPipeA(
        _create_pipe_name('EventGhost'),
        PIPE_ACCESS_DUPLEX,
        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
        PIPE_UNLIMITED_INSTANCES,
        BUFFER_SIZE,
        BUFFER_SIZE,
        50,
        NULL
    )
    err = kernel32.GetLastError()
    kernel32.CloseHandle(pipe_handle)

    if err:
        return True

    return False


# processes the incoming data. If the data is not formatted correctly or is
# not allowed this will reject it with a PipeError
def _process_command(command):
    import eg

    try:
        command, data = command.split(',', 1)
    except ValueError:
        data = '()'

    command = command.strip()
    data = data.strip()

    eg.PrintDebugNotice(
        'Processing: Command: {0}, Parameters: {1}'.format(command, data)
    )

    try:
        if '=' in command:
            raise PipeError(
                'Pipe: Command not allowed: {0}'.format(command)
            )

        if not data.startswith('dict') and '=' in data:
            raise PipeError(
                'Pipe: Data not allowed: {0}'.format(data)
            )

        if (
            data[0] not in ('(', '[', '{') and
            not data.startswith('dict')
        ):
            raise PipeError(
                'Pipe: Data not allowed: {0}'.format(data)
            )

        try:
            command = eval(command.split('(', 1)[0])
        except SyntaxError:
            raise PipeError(
                'Pipe: Command malformed: {0}'.format(command)
            )
        else:
            if isinstance(command, (str, unicode)):
                raise PipeError(
                    'Pipe: Command does not exist: {0}'.format(command)
                )
        try:
            data = eval(data)
        except SyntaxError:
            raise PipeError(
                'Pipe: Data malformed: {0}'.format(data)
            )

        if not isinstance(data, (dict, list, tuple)):
            raise PipeError(
                'Pipe: Data malformed: {0}'.format(str(data))
            )

    except PipeError:
        traceback.print_exc()

    else:
        res = [None]
        event = threading.Event()

        def run():
            try:
                if isinstance(data, dict):
                    res[0] = command(**data)
                elif isinstance(data, (tuple, list)):
                    res[0] = command(*data)
            except:
                traceback.print_exc()

            eg.PrintDebugNotice(
                'Processing: Return data: {0}'.format(str(res[0]))
            )

            event.set()
        try:
            wx.CallAfter(run)
            event.wait()
        except:
            if isinstance(data, dict):
                res[0] = command(**data)
            elif isinstance(data, (tuple, list)):
                res[0] = command(*data)

        return res[0]
    return None


# the main handler for a pipe connection. if eg.config.maxPipes is set to 10
# there will be 10 instances of this class created. It handles the IO, client
# connection and pipe disconnect for that pipe instance
class PipeInstance(object):

    def __init__(self, pipe_handle):
        # create an instance os the overlapped io structure
        self.overlap = OVERLAPPED()

        # get an event handle from Windows
        self.event = kernel32.CreateEventA(
            NULL, # default security attribute
            True, # manual-reset event
            True, # initial state = signaled
            NULL # unnamed event object
        )

        # if for some reason Windows is not able to give us an event handle
        # stop everything right there
        if self.event == NULL:
            err = kernel32.GetLastError()
            raise PipeError(err)

        # set the event handle into the overlapped io instance
        self.overlap.hEvent = self.event

        # the handle to the named pipe instance
        self.pipe_handle = pipe_handle

        # temporary storage of data read from the client
        self.read_buffer = ctypes.create_string_buffer(BUFFER_SIZE)
        # number of bytes that has been read from the pipe
        self.read_bytes = ULONG(0)

        # temporary storage for data to be sent back to the client
        self.write_buffer = ''
        # number of bytes written to the pipe
        self.write_bytes = ULONG(0)

        # pipe state
        self.state = CONNECTING_STATE

        # flag to tell us that we need to do something with the pipe
        self.pending_io = False

        # if a client is connected to the pipe
        self.has_client = False

        # threading bits
        self.__lock = threading.Lock()
        self.__io_event = threading.Event()
        self.__io_thread = threading.Thread(
            name='Named Pipe {0} IO Worker'.format(str(self.pipe_handle)),
            target=self.__io
        )

        # even tho there is a shutdown procedure for the pipe we still want to
        # end the thread that controls the pipe in the event the main process
        # terminates without running the shutdown procedure
        self.__io_thread.daemon = True
        self.__io_thread.start()

    # since creating a closing pipe instances takes time to do, we only do it
    # once.
    # so to keep performance boosted as the cost of a very small amount of
    # memory use we reuse the pipe when the client disconnects or an error
    # takes place
    def reconnect(self):
        # makes the pipe thread safe. this method can get called from more then
        # a single thread, so we do not want any data corruption. we make sure
        # only a single thread can perform operations on the pipe at any given
        # time
        with self.__lock:
            # this disconnects the client end of the pipe it does not close the
            # pipe
            kernel32.DisconnectNamedPipe(self.pipe_handle)
            # reset data storage containers
            self.read_buffer = ctypes.create_string_buffer(BUFFER_SIZE)
            self.read_bytes = ULONG(0)
            self.write_buffer = ''
            self.write_bytes = ULONG(0)
            self.state = CONNECTING_STATE
            self.pending_io = False
            self.has_client = False

    # if the pipe is open or closed. closed means a client can no longer
    # connect to this pipe instance
    @property
    def is_connected(self):
        return not self.__io_event.isSet()

    # closes the pipe instance
    def disconnect(self):
        eg.PrintDebugNotice(
            'Disconnecting pipe ' + str(self.pipe_handle)
        )
        self.__io_event.set()

        if threading.currentThread() != self.__io_thread:
            self.__io_thread.join(1.0)

    # writes data to the pipe this only gets called if the state is set to
    # WRITING_STATE and only from the io thread for this pipe instance
    def write(self):
        result = kernel32.WriteFile(
            self.pipe_handle,
            LPCSTR(self.write_buffer),
            len(self.write_buffer),
            ctypes.byref(self.write_bytes),
            ctypes.byref(self.overlap)
        )

        err = kernel32.GetLastError()

        if (
            result and
            (
                len(self.write_buffer) ==
                self.write_bytes.value
            )
        ):
            self.pending_io = False
            # data across the pipe operates in a read write fashion. this is
            # the only synchronous portion of the pipe. In the future when we
            # come up with a more complex means of sending data through the
            # pipe this can get changed to being asynchronous. we will need to
            # track the reads and writes through the use of an ID if we want to
            # make it fully async
            self.state = READING_STATE

        # I have made it so that if the  data being sent in the pipe exceeds
        # the pipe buffer size (defaulted to 4096) to keep on writing the data
        # to the pipe when the last chunck of data has been read. We keep the
        # state set to READING_STATE because the io thread will change it to
        # WRITING_STATE before reading any data
        elif not result and err == ERROR_MORE_DATA:
            self.pending_io = True
        else:
            traceback.print_exc()
            self.reconnect()

    # pretty much the same as above except we keep in a loop for reading the
    # data incase the data being received is larger then the buffer
    def read(self):
        while True:
            result = 0

            while not result:  # repeat loop if ERROR_MORE_DATA
                result = kernel32.ReadFile(
                    self.pipe_handle,
                    self.read_buffer,
                    BUFFER_SIZE,
                    ctypes.byref(self.read_bytes),
                    ctypes.byref(self.overlap)
                )
                if result:
                    break

                err = kernel32.GetLastError()
                if err == ERROR_MORE_DATA:
                    continue

                elif err == ERROR_IO_PENDING:
                    break

                else:
                    if err in (
                        ERROR_BROKEN_PIPE,
                        ERROR_BAD_PIPE,
                        ERROR_NO_DATA,
                        ERROR_INVALID_HANDLE,
                        ERROR_PIPE_NOT_CONNECTED
                    ):
                        self.reconnect()
                        return
                    else:
                        try:
                            raise PipeError(err)
                        except PipeError:
                            traceback.print_exc()
                            self.reconnect()
                            return

            if self.read_bytes.value != 0:
                if self.read_buffer.value == 'stop_pipe':
                    self.disconnect()
                    return
                try:
                    message = str(repr(
                        _process_command(
                            self.read_buffer.value
                        )
                    ))
                    self.pending_io = True
                    self.state = WRITING_STATE
                    self.write_buffer = message
                    self.write()

                except PipeError:
                    traceback.print_exc()
                    self.reconnect()
                    return

            else:
                self.reconnect()
                return

    # The method the io thread loops in waiting on an event in the pipe. it
    # only waits for 50 milliseconds then loops back around if no event has
    # taken place. This is so the pipe doesn't get blocked in the event of some
    #  kind of an error on the client side that causes a disconnect. we don't
    # want the pipe to hang because of no client
    def __io(self):
        while not self.__io_event.isSet():
            if not self.has_client:
                self.connect()

            with self.__lock:
                result = kernel32.WaitForSingleObject(
                    self.pipe_handle,
                    50
                )

                if result == WAIT_TIMEOUT:
                    continue

                if result in (WAIT_ABANDONED, WAIT_FAILED):
                    err = kernel32.GetLastError()
                    try:
                        raise PipeError(err)
                    except PipeError:
                        traceback.print_exc()
                        self.reconnect()
                        continue

                eg.PrintDebugNotice(
                    'Named pipe {0} incoming event'.format(
                        str(self.pipe_handle)
                    )
                )

                if self.pending_io:
                    io_bytes = ULONG(0)
                    result = kernel32.GetOverlappedResult(
                        self.pipe_handle,  # handle to pipe
                        ctypes.byref(self.overlap),  # OVERLAPPED structure
                        ctypes.byref(io_bytes),  # bytes transferred
                        False  # do not wait
                    )

                    # we run a test cycle on startup to ensure the event system
                    # is working as intended. When we crated the Windows event
                    # we set the event to be "triggered" on creation. because
                    # the initial state is set to CONNECTING_STATE we check the
                    # returned value of GetOverlappedResult to ensure there are
                    # no errors. and is there is to reset the pipe for a new
                    # connection. and if not then set the pipe state to
                    # READING_STATE so we can then read the data received when
                    # the client sends it
                    if self.state == CONNECTING_STATE:
                        if not result:
                            err = kernel32.GetLastError()
                            try:
                                raise PipeError(err)
                            except PipeError:
                                traceback.print_exc()
                                self.reconnect()
                        else:
                            self.state = READING_STATE

                    elif self.state == READING_STATE:
                        if not result or self.read_bytes.value == 0:
                            self.reconnect()
                        else:
                            self.state = WRITING_STATE

                    elif self.state == WRITING_STATE:
                        if not result or self.write_bytes.value == 0:
                            self.reconnect()
                        else:
                            self.state = READING_STATE

                if self.state == WRITING_STATE:
                    self.write()

                elif self.state == READING_STATE:
                    self.read()

        # this is the spot where the pipe instance gets closed. This happens
        # when the shutdown procedure has been run. We have a secondary
        # shutdown protocol put into place as a backup or if a specific pipe
        # instance needs to be terminated remotely. If "stop_pipe" is sent from
        # the client it will cause the pipe instance to be closed and a new
        # one to be spawned. It is good housekeeping to periodically do this
        # when we make full use of the named pipes. the command is very generic
        # at the moment and is very easily changed

        kernel32.FlushFileBuffers(self.pipe_handle)
        kernel32.DisconnectNamedPipe(self.pipe_handle)
        kernel32.CloseHandle(self.pipe_handle)

    def connect(self):
        eg.PrintDebugNotice('Connecting named pipe')

        kernel32.ConnectNamedPipe(self.pipe_handle, None)
        err = kernel32.GetLastError()

        if err == ERROR_IO_PENDING:
            self.pending_io = True
            self.has_client = True

        elif err == ERROR_PIPE_CONNECTED:
            if kernel32.SetEvent(self.event):
                self.pending_io = True
                self.has_client = True
        elif err:
            kernel32.DisconnectNamedPipe(self.pipe_handle)
            try:
                raise PipeError(err)
            except PipeError:
                traceback.print_exc()

            self.has_client = False
            return
        else:
            self.pending_io = True
            self.has_client = True

        eg.PrintDebugNotice(
            'Named pipe {0} connected'.format(str(self.pipe_handle))
        )


# container object that holds the pipe instances. This container checks for
# closed pipes and removes them. it also checks to see if eg.config.maxPipes
# has changed and if the number is now lower it will close any pipes that are
# not connected to a client. it will do this each time the container is
# accessed until the number of pipe instances matches eg.config.maxPipes
class PipesContainer(object):
    __lock = threading.RLock()
    __pipes = []

    def append(self,  p_object):
        with self.__lock:
            self.__pipes.append(p_object)

    def count(self, value):
        with self.__lock:
            return self.__pipes.count(value)

    def extend(self, iterable):
        with self.__lock:
            self.__pipes.extend(iterable)

    def index(self, value, start=None, stop=None):
        with self.__lock:
            return self.__pipes.index(value, start, stop)

    def insert(self, index,  p_object):
        with self.__lock:
            self.__pipes.insert(index, p_object)

    def pop(self, index=None):
        with self.__lock:
            return self.__pipes.pop(index)

    def remove(self, value):
        with self.__lock:
            self.__pipes.remove(value)

    def reverse(self):
        with self.__lock:
            self.__pipes.reverse()

    def sort(self, cmp=None, key=None,  reverse=False):
        with self.__lock:
            self.__pipes.sort(cmp, key, reverse)

    def __add__(self, y):
        return self.__pipes + y

    def __contains__(self, y):
        with self.__lock:
            return self.__pipes.__contains__(y)

    def __delitem__(self, y):
        with self.__lock:
            self.__pipes.__delitem__(y)

    def __delslice__(self, i,  j):
        with self.__lock:
            self.__pipes.__delslice__(i, j)

    def __eq__(self, y):
        return self.__pipes.__eq__(y)

    def __getitem__(self, y):
        with self.__lock:
            return self.__pipes.__getitem__(y)

    def __getslice__(self, i, j):
        with self.__lock:
            return self.__pipes.__getslice__(i, j)

    def __ge__(self, y):
        return self.__pipes.__ge__(y)

    def __gt__(self, y):
        return self.__pipes.__gt__(y)

    def __iadd__(self, y):
        with self.__lock:
            self.__pipes = self.__pipes.__iadd__(y)
        return self

    def __imul__(self, y):
        with self.__lock:
            self.__pipes = self.__pipes.__imul__(y)
        return self

    def purge(self):
        with self.__lock:
            for pipe_instance in self.__pipes:
                if not pipe_instance.is_connected:
                    self.__pipes.remove(pipe_instance)

            to_many = len(self.__pipes) - eg.config.maxPipes

            if to_many > 0:
                no_clients = list(
                    pipe_instance
                    for pipe_instance in self.__pipes
                    if not pipe_instance.has_client
                )
                while to_many and no_clients:
                    try:
                        send_message('stop_pipe')
                    except PipeError:
                        pass
                    to_many -= 1
                    no_clients.pop(0)
                self.purge()

    def __iter__(self):
        with self.__lock:
            self.purge()
        return self.__pipes.__iter__()

    def __len__(self):
        with self.__lock:
            self.purge()
        return self.__pipes.__len__()

    def __le__(self, y):
        return self.__pipes.__le__(y)

    def __lt__(self, y):
        return self.__pipes.__lt__(y)

    def __mul__(self, n):
        return self.__pipes.__mul__(n)

    def __ne__(self, y):
        return self.__pipes.__ne__(y)

    def __repr__(self):
        return repr(self.__pipes)

    def __reversed__(self):
        return self.__pipes.__reversed__()

    def __rmul__(self, n):
        return self.__pipes.__rmul__(n)

    def __setitem__(self, i, y):
        with self.__lock:
            self.__pipes.__setitem__(i, y)

    def __setslice__(self, i, j, y):
        with self.__lock:
            self.__pipes.__setslice__(i, j, y)


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

    def __init__(self):
        self._thread = None
        self.pipes = PipesContainer()
        self._stopped = False
        self._event = threading.Event()

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(
                name='EventGhost Named Pipe',
                target=self.run
            )
            self._thread.start()

    def stop(self):
        self._event.set()
        self._thread.join(3.0)
        return self._stopped

    @property
    def is_running(self):
        return not self._stopped

    def run(self):
        import eg

        pipe_name = _create_pipe_name('EventGhost')

        # always need to have at least a single pipe instance to identify if
        # EG is running or not.
        if not eg.config.maxPipes:
            eg.config.maxPipes = 1

        while not self._event.isSet():
            while (
                len(self.pipes) < eg.config.maxPipes and
                not self._event.isSet()
            ):
                eg.PrintDebugNotice('Creating security descriptor')
                security_attributes = SECURITY_ATTRIBUTES()
                security_descriptor = PSECURITY_DESCRIPTOR()

                advapi32.SetSecurityDescriptorDacl(
                    ctypes.byref(security_descriptor),
                    BOOL(1),
                    NULL,
                    BOOL(0)
                )

                security_attributes.lpSecurityDescriptor = security_descriptor
                security_attributes.nLength = ctypes.sizeof(
                    security_attributes
                )

                eg.PrintDebugNotice('Creating named pipe')

                if len(self.pipes) == 0:
                    pipe_handle = kernel32.CreateNamedPipeA(
                        pipe_name,
                        (
                            PIPE_ACCESS_DUPLEX |
                            FILE_FLAG_OVERLAPPED |
                            FILE_FLAG_FIRST_PIPE_INSTANCE
                        ),
                        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
                        PIPE_UNLIMITED_INSTANCES,
                        BUFFER_SIZE,
                        BUFFER_SIZE,
                        NMPWAIT_WAIT_FOREVER,
                        ctypes.byref(security_attributes)
                    )
                else:
                    pipe_handle = kernel32.CreateNamedPipeA(
                        pipe_name,
                        PIPE_ACCESS_DUPLEX | FILE_FLAG_OVERLAPPED,
                        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
                        PIPE_UNLIMITED_INSTANCES,
                        BUFFER_SIZE,
                        BUFFER_SIZE,
                        NMPWAIT_WAIT_FOREVER,
                        ctypes.byref(security_attributes)
                    )

                if pipe_handle == INVALID_HANDLE_VALUE:
                    err = kernel32.GetLastError()
                    kernel32.DisconnectNamedPipe(pipe_handle)
                    kernel32.CloseHandle(pipe_handle)
                    if err:
                        raise PipeError(err)
                    else:
                        raise PipeError('Unable to create named pipe')

                pipe_instance = PipeInstance(pipe_handle)
                self.pipes.append(pipe_instance)

            self._event.wait(0.2)

        eg.PrintDebugNotice('Closing named pipe')
        for pipe in self.pipes:
            if not pipe.has_client:
                try:
                    send_message('stop_pipe')
                except PipeError:
                    pass

        while self.pipes:
            pipe_instance = self.pipes.pop(0)
            if not pipe_instance.is_connected:
                continue
            pipe_instance.disconnect()

        eg.PrintDebugNotice('Named pipe is closed')
        self._stopped = True


def send_message(msg):
    pipe_name = _create_pipe_name('EventGhost')
    while True:
        pipe_handle = kernel32.CreateFileA(
            pipe_name,
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            0,
            NULL
        )
        if pipe_handle != INVALID_HANDLE_VALUE:
            break
        if kernel32.GetLastError() != ERROR_PIPE_BUSY:
            pass
        elif kernel32.WaitNamedPipeA(pipe_name, 2000) == 0:
            kernel32.CloseHandle(pipe_handle)
            return False

    pipe_mode = ULONG(PIPE_READMODE_MESSAGE)
    result = kernel32.SetNamedPipeHandleState(
        pipe_handle,
        ctypes.byref(pipe_mode),
        NULL,
        NULL
    )

    if not result:
        err = kernel32.GetLastError()
        kernel32.CloseHandle(pipe_handle)
        if err:
            raise PipeError(err)
        else:
            raise PipeError('send_message SetNamedPipeHandleState failed')

    write_bytes = ULONG(0)
    result = kernel32.WriteFile(
        pipe_handle,
        LPCSTR(msg),
        len(msg),
        ctypes.byref(write_bytes),
        None
    )
    if not result or len(msg) != write_bytes.value:
        err = kernel32.GetLastError()
        kernel32.CloseHandle(pipe_handle)
        if err:
            raise PipeError(err)
        else:
            raise PipeError('send_message WriteFile failed')

    result = 0
    read_buffer = ctypes.create_string_buffer(BUFFER_SIZE)
    read_bytes = ULONG(0)

    while not result:  # repeat loop if ERROR_MORE_DATA
        result = kernel32.ReadFile(
            pipe_handle,
            read_buffer,
            BUFFER_SIZE,
            ctypes.byref(read_bytes),
            NULL
        )
        if result == 1:
            break

        err = kernel32.GetLastError()
        kernel32.CloseHandle(pipe_handle)
        if err != ERROR_MORE_DATA:
            kernel32.CloseHandle(pipe_handle)
            raise PipeError(err)

    data = read_buffer.value
    if data != '':
        try:
            return eval(data)
        except SyntaxError:
            return data
    else:
        return data
