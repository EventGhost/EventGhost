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

from threading import Condition, currentThread, Lock, Thread
from time import clock, sleep

# Local imports
import eg
from eg.WinApi.Dynamic import (
    # ctypes stuff
    byref,
    create_string_buffer,
    FormatError,
    pointer,
    sizeof,

    # constants
    CLRDTR,
    CLRRTS,
    DTR_CONTROL_DISABLE,
    ERROR_IO_PENDING,
    EV_BREAK,
    EV_CTS,
    EV_DSR,
    EV_ERR,
    EV_RING,
    EV_RLSD,
    EV_RXCHAR,
    EV_RXFLAG,
    EV_TXEMPTY,
    EVENPARITY,
    FILE_ATTRIBUTE_NORMAL,
    FILE_FLAG_OVERLAPPED,
    GENERIC_READ,
    GENERIC_WRITE,
    INFINITE,
    INVALID_HANDLE_VALUE,
    MARKPARITY,
    NOPARITY,
    ODDPARITY,
    ONE5STOPBITS,
    ONESTOPBIT,
    OPEN_EXISTING,
    QS_ALLINPUT,
    SETDTR,
    SETRTS,
    SPACEPARITY,
    TWOSTOPBITS,
    WAIT_OBJECT_0,
    WAIT_TIMEOUT,

    # types
    COMMCONFIG,
    COMMTIMEOUTS,
    COMSTAT,
    DCB,
    DWORD,
    HANDLE,
    OVERLAPPED,

    # functions
    ClearCommError,
    CloseHandle,
    CreateEvent,
    CreateFile,
    EscapeCommFunction,
    GetCommState,
    GetCommTimeouts,
    GetDefaultCommConfig,
    GetLastError,
    GetOverlappedResult,
    MsgWaitForMultipleObjects,
    ReadFile,
    ResetEvent,
    SetCommMask,
    SetCommState,
    SetCommTimeouts,
    SetEvent,
    WaitCommEvent,
    WaitForSingleObject,
    WriteFile,
)

# parity string to dcb value dict
PARITY_S2V_DICT = {
    'N': NOPARITY,
    'O': ODDPARITY,
    'E': EVENPARITY,
    'M': MARKPARITY,
    'S': SPACEPARITY,
}
# parity dcb value to string dict
PARITY_V2S_DICT = {
    NOPARITY: 'N',
    ODDPARITY: 'O',
    EVENPARITY: 'E',
    MARKPARITY: 'M',
    SPACEPARITY: 'S',
}
# stop bits string to dcb value dict
STOPBITS_S2V_DICT = {'1': ONESTOPBIT, '1.5': ONE5STOPBITS, '2': TWOSTOPBITS}
# stop bits dcb value to string dict
STOPBITS_V2S_DICT = {ONESTOPBIT: '1', ONE5STOPBITS: '1.5', TWOSTOPBITS: '2'}

class SerialError(eg.Exception):
    """
    Base class for SerialThread related exceptions.
    """
    def __init__(self, msg=None):
        if msg is None:
            errno = GetLastError()
            strerror = FormatError(errno)
        else:
            errno = 0
            strerror = msg
        eg.Exception.__init__(self, errno, strerror)


class SerialThread(Thread):
    """
    Eased handling of serial port communication.
    """
    # These functions are bound to the class, so instances or subclasses
    # can replace them. This is needed for code that uses the FTDI.DLL
    # driver for example.
    _ReadFile = ReadFile
    _WriteFile = WriteFile
    _ClearCommError = ClearCommError
    _CreateFile = CreateFile
    _CloseHandle = CloseHandle
    # Cache list for GetAllPorts
    _serialPortList = None
    SerialError = SerialError

    def __init__(self, hFile=0):
        Thread.__init__(self, target=self.ReceiveThreadProc)
        self.hFile = int(hFile)
        self.osWriter = OVERLAPPED()
        self.osWriter.hEvent = CreateEvent(None, 0, 0, None)
        self.osReader = OVERLAPPED()
        self.osReader.hEvent = CreateEvent(None, 1, 0, None)
        self.dwRead = DWORD()
        self.comstat = COMSTAT()
        self.dcb = DCB()
        self.dcb.DCBlength = sizeof(DCB)
        self.oldCommTimeouts = COMMTIMEOUTS()

        self.readEventCallback = None
        self.readEventLock = Lock()
        self.readEventLock.acquire()
        self.readCondition = Condition()
        self.buffer = ""
        self.keepAlive = True
        self.stopEvent = CreateEvent(None, 1, 0, None)
        self.callbackThread = Thread(
            target=self.CallbackThreadProc,
            name="SerialReceiveThreadProc"
        )

    def __enter__(self):
        self.SuspendReadEvents()
        return self

    def __exit__(self, dummyExcType, dummyExcValue, dummyTraceback):
        self.ResumeReadEvents()
        return False

    @eg.LogItWithReturn
    def CallbackThreadProc(self):
        while self.keepAlive:
            self.readCondition.acquire()
            while len(self.buffer):
                if self.readEventLock.acquire(0):
                    if self.readEventCallback:
                        try:
                            self.readEventCallback(self)
                        except Exception:
                            eg.PrintTraceback()
                    self.readEventLock.release()
                    sleep(0.001)
                else:
                    break
            self.readCondition.wait()
            self.readCondition.release()

    def Close(self):
        """
        Closes  the serial port and stops all event processing.
        """
        self.keepAlive = False
        SetEvent(self.stopEvent)
        if currentThread() != self:
            self.join(1.0)
        if self.hFile:
            #Restore original timeout values:
            SetCommTimeouts(self.hFile, self.oldCommTimeouts)
            #Close COM-Port:
            if not self._CloseHandle(self.hFile):
                self.hFile = None
                raise SerialError()

    def Flush(self):
        self.readCondition.acquire()
        self.buffer = ""
        self.readCondition.release()

    @classmethod
    def GetAllPorts(cls):
        """
        Returns a list with all available serial ports.
        """
        serialPortList = cls._serialPortList
        if serialPortList is not None:
            return serialPortList
        serialPortList = []
        commconfig = COMMCONFIG()
        commconfig.dwSize = sizeof(COMMCONFIG)
        lpCC = pointer(commconfig)
        dwSize = DWORD(0)
        lpdwSize = byref(dwSize)
        for i in range(0, 255):
            name = 'COM%d' % (i + 1)
            res = GetDefaultCommConfig(name, lpCC, lpdwSize)
            if res == 1 or (res == 0 and GetLastError() == 122):
                serialPortList.append(i)
        cls._serialPortList = serialPortList
        return serialPortList

    def GetBaudrate(self):
        """
        Returns the currently used baud rate as an integer.
        """
        return self.dcb.BaudRate

    def GetMode(self):
        """
        Returns the currently used serial port mode setting as string.

        See :meth:`Open` for a complete description of the mode string.
        """
        dcb = self.dcb
        return (
            str(dcb.ByteSize) +
            PARITY_V2S_DICT[dcb.Parity] +
            STOPBITS_V2S_DICT[dcb.StopBits]
        )

    def HandleReceive(self, data):
        # read all data currently available
        data += self._ReadAllAvailable()
        # append the data to the buffer and notify waiting threads
        self.readCondition.acquire()
        self.buffer += data
        self.readCondition.notifyAll()
        self.readCondition.release()

    def Open(self, port=0, baudrate=9600, mode="8N1"):
        """
        Opens the serial port. After the port is opened, you have to call
        :meth:`Start` to start the actual event processing of this class.

        :Arguments:
            port
                The port to open as an integer starting at one (0 = COM1)
            baudrate
                The baudrate to use as an integer. Defaults to 9600.
            mode
                The serial port mode settings to use. This should be a
                string created by the joining of the following parts:

                #. byte size
                    '5', '6', '7' or '8'
                #. parity mode
                    * 'N' for no parity,
                    * 'E' for even parity,
                    * 'O' for odd parity,
                    * 'M' for mark parity,
                    * 'S' for space parity
                #. stop bits
                    * '1' for one stop bit
                    * '1.5' for one and a half stop bit
                    * '2' for two stop bits

                Example values: '8N1' (default), '8E1', '7N1.5'
        """
        #the "//./COMx" format is required for devices >= 9
        #not all versions of windows seem to support this properly
        #so that the first few ports are used with the DOS device name
        if port < 9:
            deviceStr = 'COM%d' % (port + 1)
        else:
            deviceStr = '\\\\.\\COM%d' % (port + 1)
        try:
            self.hFile = self._CreateFile(
                deviceStr,
                GENERIC_READ | GENERIC_WRITE,
                0,  # exclusive access
                None,  # default security attributes
                OPEN_EXISTING,
                FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED,
                0
            )
        except Exception:
            self.hFile = None    # cause __del__ is called anyway
            raise eg.Exceptions.SerialOpenFailed()
        if self.hFile == INVALID_HANDLE_VALUE:
            self.hFile = None
            raise eg.Exceptions.SerialOpenFailed()
        dcb = self.dcb
        GetCommState(self.hFile, byref(dcb))
        dcb.fBinary = True
        dcb.fParity = False
        dcb.fOutxCtsFlow = False
        dcb.fOutxDsrFlow = False
        dcb.fDtrControl = DTR_CONTROL_DISABLE
        dcb.fDsrSensitivity = False
        dcb.fTXContinueOnXoff = True
        dcb.fOutX = False
        dcb.fInX = False
        dcb.fErrorChar = False
        dcb.fNull = False
        dcb.fRtsControl = False
        dcb.fAbortOnError = False
        dcb.BaudRate = baudrate
        dcb.ByteSize = int(mode[0])
        dcb.Parity = PARITY_S2V_DICT[mode[1].upper()]
        dcb.StopBits = STOPBITS_S2V_DICT[mode[2:]]
        SetCommState(self.hFile, byref(dcb))
        GetCommTimeouts(self.hFile, byref(self.oldCommTimeouts))
        commTimeouts = COMMTIMEOUTS(0, 0, 0, 100, 100)
        SetCommTimeouts(self.hFile, byref(commTimeouts))

    def Read(self, numBytes=1, timeout=0.0):
        """
        Reads data from the serial port.
        """
        self.readCondition.acquire()
        startTime = clock()
        endTime = startTime + timeout
        while len(self.buffer) < numBytes:
            waitTime = endTime - clock()
            if waitTime <= 0:
                numBytes = len(self.buffer)
                break
            self.readCondition.wait(waitTime)
        data = self.buffer[:numBytes]
        self.buffer = self.buffer[numBytes:]
        self.readCondition.release()
        return data

    @eg.LogItWithReturn
    def ReceiveThreadProc(self):
        hFile = self.hFile
        osReader = self.osReader
        lpBuf = create_string_buffer(1)
        dwRead = DWORD()
        pHandles = (HANDLE * 2)(osReader.hEvent, self.stopEvent)

        waitingOnRead = False
        while self.keepAlive:
            #print "ReceiveThreadProc"
            # if no read is outstanding, then issue another one
            if not waitingOnRead:
                #print "ResetEvent"
                ResetEvent(osReader.hEvent)
                returnValue = self._ReadFile(
                    hFile,
                    lpBuf,
                    1,  # we want to get notified as soon as a byte is available
                    byref(dwRead),
                    byref(osReader)
                )
                if not returnValue:
                    err = GetLastError()
                    if err != 0 and err != ERROR_IO_PENDING:
                        raise SerialError()
                    waitingOnRead = True
                else:
                    # read completed immediately
                    if dwRead.value:
                        self.HandleReceive(lpBuf.raw)
                        continue

            ret = MsgWaitForMultipleObjects(
                2, pHandles, 0, 100000, QS_ALLINPUT
            )
            if ret == WAIT_OBJECT_0:
                returnValue = GetOverlappedResult(
                    hFile,
                    byref(osReader),
                    byref(dwRead),
                    0
                )
                #print "GetOverlappedResult", returnValue, dwRead.value
                waitingOnRead = False
                if returnValue and dwRead.value:
                    self.HandleReceive(lpBuf.raw)
            elif ret == WAIT_OBJECT_0 + 1:
                #print "WAIT_OBJECT_1"
                # stop event signaled
                self.readCondition.acquire()
                self.readCondition.notifyAll()
                self.readCondition.release()
                break
            elif ret == WAIT_TIMEOUT:
                #print "WAIT_TIMEOUT"
                pass
            else:
                raise SerialError("Unknown message in ReceiveThreadProc")

    def ReportStatusEvent(self, statusEvent):
        print statusEvent

    def ResumeReadEvents(self):
        """
        Resumes the receive event processing that was disabled before by
        :meth:`SuspendReadEvents`
        """
        self.readEventLock.release()
        self.readCondition.acquire()
        self.readCondition.notifyAll()
        self.readCondition.release()

    def SetBaudrate(self, baudrate):
        """
        Sets the baud rate to an integer value.
        """
        self.dcb.BaudRate = baudrate
        SetCommState(self.hFile, byref(self.dcb))

    def SetDtr(self, flag=True):
        """
        Sets DTR state.
        """
        EscapeCommFunction(self.hFile, SETDTR if flag else CLRDTR)

    def SetMode(self, mode):
        """
        Sets the serial port mode setting from a string.

        See :meth:`Open` for a complete description of the mode string.
        """
        dcb = self.dcb
        dcb.ByteSize = int(mode[0])
        dcb.Parity = PARITY_S2V_DICT[mode[1].upper()]
        dcb.StopBits = STOPBITS_S2V_DICT[mode[2:]]
        SetCommState(self.hFile, byref(dcb))

    def SetReadEventCallback(self, callback):
        """
        Sets a callback function for receive event processing. Should be
        called before :meth:`Start`. The callback should have the form::

            def HandleReceive(serialThread):
                ...

        where serialThread will be the instance of this SerialThread class, so
        you can easily call :meth:`Read` and :meth:`Write` on this object.
        """
        self.readEventCallback = callback
        self.readEventLock.release()

    def SetRts(self, flag=True):
        """
        Sets RTS state.
        """
        EscapeCommFunction(self.hFile, SETRTS if flag else CLRRTS)

    def Start(self):
        """
        Starts the event processing of this class.
        """
        self.callbackThread.start()
        self.start()

    def StatusCheckLoop(self):
        hComm = self.hFile
        waitingOnStatusHandle = False
        dwCommEvent = DWORD()
        dwOvRes = DWORD()
        commMask = (
            EV_BREAK | EV_CTS | EV_DSR | EV_ERR | EV_RING |
            EV_RLSD | EV_RXCHAR | EV_RXFLAG | EV_TXEMPTY
        )

        if not SetCommMask(self.hFile, commMask):
            raise SerialError("error setting communications mask")

        osStatus = OVERLAPPED(0)
        osStatus.hEvent = CreateEvent(None, 1, 0, None)
        if not osStatus.hEvent:
            raise SerialError("error creating event")

        while True:
            # Issue a status event check if one hasn't been issued already.
            if not waitingOnStatusHandle:
                if WaitCommEvent(hComm, byref(dwCommEvent), byref(osStatus)):
                    # WaitCommEvent returned immediately.
                    # Deal with status event as appropriate.
                    self.ReportStatusEvent(dwCommEvent.value)
                else:
                    if GetLastError() == ERROR_IO_PENDING:
                        waitingOnStatusHandle = True
                    else:
                        raise SerialError("error in WaitCommEvent")

            # Check on overlapped operation
            if waitingOnStatusHandle:
                # Wait a little while for an event to occur.
                res = WaitForSingleObject(osStatus.hEvent, 1000)
                if res == WAIT_OBJECT_0:
                    if GetOverlappedResult(
                        hComm, byref(osStatus), byref(dwOvRes), 0
                    ):
                        # Status event is stored in the event flag
                        # specified in the original WaitCommEvent call.
                        # Deal with the status event as appropriate.
                        self.ReportStatusEvent(dwCommEvent.value)
                    else:
                        # An error occurred in the overlapped operation;
                        # call GetLastError to find out what it was
                        # and abort if it is fatal.
                        raise SerialError()
                    # Set waitingOnStatusHandle flag to indicate that a new
                    # WaitCommEvent is to be issued.
                    waitingOnStatusHandle = True
                elif res == WAIT_TIMEOUT:
                    print "timeout"
                else:
                    # This indicates a problem with the OVERLAPPED structure's
                    # event handle.
                    CloseHandle(osStatus.hEvent)
                    raise SerialError("error in the WaitForSingleObject")

        CloseHandle(osStatus.hEvent)

    def Stop(self):
        """
        Stops the event processing of this class.
        """
        self.keepAlive = False
        SetEvent(self.stopEvent)
        if currentThread() != self:
            self.join(1.0)

    def SuspendReadEvents(self):
        """
        Temporarily disables the receive event processing of this class. Call
        :meth:`ResumeReadEvents` to resume processing.
        """
        self.readEventLock.acquire()

    def Write(self, data):
        """
        Writes a string to the port.
        """
        dwWritten = DWORD(0)
        returnValue = self._WriteFile(
            self.hFile,
            data,
            len(data),
            byref(dwWritten),
            byref(self.osWriter)
        )
        if returnValue != 0:
            return
        err = GetLastError()
        if err != 0 and err != ERROR_IO_PENDING:
            raise SerialError()
        if not GetOverlappedResult(
            self.hFile,
            byref(self.osWriter),
            byref(dwWritten),
            1
        ):
            raise SerialError()
        if dwWritten.value != len(data):
            raise self.SerialError("Write timeout")

    def _ReadAllAvailable(self):
        """
        Get all bytes currently in the drivers receive buffer.
        Only used internally.
        """
        sleep(0.001)
        errors = DWORD()
        self._ClearCommError(self.hFile, byref(errors), byref(self.comstat))
        numBytes = self.comstat.cbInQue
        if numBytes == 0:
            return ''
        #ResetEvent(self.osReader.hEvent)
        lpBuffer = create_string_buffer(numBytes)
        numberOfBytesRead = DWORD()
        if not self._ReadFile(
            self.hFile,
            lpBuffer,
            numBytes,
            byref(numberOfBytesRead),
            byref(self.osReader)
        ):
            WaitForSingleObject(self.osReader.hEvent, INFINITE)
        return lpBuffer.raw[:numberOfBytesRead.value]
