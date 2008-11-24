# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import eg
from threading import Thread, Lock, Condition, currentThread
from time import clock
from eg.WinApi.Dynamic import (
    # ctypes stuff
    pointer, 
    sizeof, 
    create_string_buffer, 
    byref, 
    FormatError, 
    WinError,
    
    # constants
    GENERIC_READ, 
    GENERIC_WRITE, 
    OPEN_EXISTING,
    FILE_ATTRIBUTE_NORMAL, 
    FILE_FLAG_OVERLAPPED, 
    WAIT_OBJECT_0,
    WAIT_TIMEOUT,
    INFINITE,
    QS_ALLINPUT, 
    ERROR_IO_PENDING, 
    NOPARITY,
    ODDPARITY,
    EVENPARITY,
    MARKPARITY,
    SPACEPARITY,
    ONESTOPBIT,
    ONE5STOPBITS,
    TWOSTOPBITS,
    SETDTR, 
    CLRDTR, 
    SETRTS, 
    CLRRTS,
    DTR_CONTROL_DISABLE,
    
    # types
    HANDLE, 
    DWORD, 
    OVERLAPPED,
    DCB, 
    COMMCONFIG, 
    COMSTAT, 
    
    # functions
    GetLastError, 
    CreateEvent, 
    SetEvent, 
    ResetEvent, 
    MsgWaitForMultipleObjects, 
    WaitForSingleObject, 
    CreateFile, 
    CloseHandle, 
    ReadFile, 
    WriteFile,
    GetOverlappedResult, 
    GetCommState, 
    SetCommState,
    EscapeCommFunction,
    ClearCommError, 
    GetDefaultCommConfig,
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


class SerialException(Exception):
    """Base class for SerialThread related exceptions."""
    pass



class SerialThread(Thread):
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
    
    @classmethod
    def GetAllPorts(cls):
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
            name = 'COM%d' % (i+1)
            res = GetDefaultCommConfig(name, lpCC, lpdwSize)
            if res == 1 or (res == 0 and GetLastError() == 122):
                serialPortList.append(i)
        cls._serialPortList = serialPortList
        return serialPortList

        
    def __init__(self, hFile=0):
        self.deviceStr = ""
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
        
        self.readCounter = 0
        self.readEventCallback = None
        self.readEventLock = Lock()
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
                0, # exclusive access
                None, # default security attributes 
                OPEN_EXISTING,
                FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED,
                0
            )
        except Exception, msg:
            self.hFile = None    # cause __del__ is called anyway
            raise SerialException("could not open port: %s" % msg)
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
    
        
    def Close(self):
        """Closes  the serial port and stops all event processing."""
        self.keepAlive = False
        SetEvent(self.stopEvent)
        if currentThread() != self:
            self.join(1.0)
        if self.hFile:
            #Restore original timeout values:
            #SetCommTimeouts(self.hFile, self._orgTimeouts)
            #Close COM-Port:
            if not self._CloseHandle(self.hFile):
                print (FormatError(GetLastError())).decode('mbcs')
            self.hFile = None

    
    def Start(self):
        """
        Starts the event processing of this class.
        """
        self.callbackThread.start()
        self.start()

        
    def Stop(self):
        """
        Stops the event processing of this class.
        """
        self.keepAlive = False
        SetEvent(self.stopEvent)
        if currentThread() != self:
            self.join(1.0)
        
        
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
        
        
    def SuspendReadEvents(self):
        """
        Temporarily disables the receive event processing of this class. Call
        :meth:`ResumeReadEvents` to resume processing.
        """
        self.readEventLock.acquire()
    
    
    def ResumeReadEvents(self):
        """
        Resumes the receive event processing that was disabled before by
        :meth:`SuspendReadEvents`
        """
        self.readEventLock.release()
        self.readCondition.acquire()
        self.readCondition.notifyAll()
        self.readCondition.release()
        
    
    def ReceiveThreadProc(self):
        hFile = self.hFile
        osReader = self.osReader
        lpBuf = create_string_buffer(1)
        dwRead = DWORD()
        pHandles = (HANDLE * 2)(osReader.hEvent, self.stopEvent)
        
        waitingOnRead = False
        while self.keepAlive:
            # if no read is outstanding, then issue another one
            if not waitingOnRead:
                ResetEvent(osReader.hEvent)
                r = self._ReadFile(
                    hFile, 
                    lpBuf, 
                    1, # we want to get notified as soon as a byte is available
                    byref(dwRead), 
                    byref(osReader)
                )
                if not r:
                    err = GetLastError()
                    if err != 0 and err != ERROR_IO_PENDING:
                        raise WinError()
                    waitingOnRead = True
                else:
                    # read completed immediately
                    if dwRead.value:
                        self.HandleReceive(lpBuf.raw)
                        continue

            rc = MsgWaitForMultipleObjects(2, pHandles, 0, 10000, QS_ALLINPUT)
            if rc == WAIT_OBJECT_0:
                r = GetOverlappedResult(
                    hFile, 
                    byref(osReader), 
                    byref(dwRead), 
                    0
                )
                waitingOnRead = False
                if r and dwRead.value:
                    self.HandleReceive(lpBuf.raw)
            elif rc == WAIT_OBJECT_0 + 1:
                # stop event signaled
                self.readCondition.acquire()
                self.readCondition.notifyAll()
                self.readCondition.release()
                break
            elif rc == WAIT_TIMEOUT:
                pass
            else:
                raise Exception("unknown message received")
                
    
    def CallbackThreadProc(self):
        while self.keepAlive:
            #print "cycle"
            self.readCondition.acquire()
            while len(self.buffer):
                if self.readEventLock.acquire(0):
                    if self.readEventCallback:
                        try:
                            self.readEventCallback(self)
                        except Exception:
                            eg.PrintTraceback()
                    self.readEventLock.release()
                else:
                    break
            self.readCondition.wait()
            self.readCondition.release()
            
        
    def HandleReceive(self, data):
        # read all data currently available
        data += self._ReadAllAvailable()
        # append the data to the buffer and notify waiting threads
        self.readCondition.acquire()
        self.buffer += data
        self.readCondition.notifyAll()
        self.readCondition.release()
            
            
    def Read(self, numBytes=1, timeout=0.0):
        """
        Reads data from the serial port.
        """
        self.readCondition.acquire()
        startTime = clock()
        endTime = startTime + timeout
        while len(self.buffer) < numBytes:
            waitTime = endTime - clock()
            if waitTime < 0:
                numBytes = len(self.buffer)
                break
            self.readCondition.wait(waitTime)
        data = self.buffer[:numBytes]
        self.readCounter += len(data)
        self.buffer = self.buffer[numBytes:]
        self.readCondition.release()
        return data
        
        
    def _ReadAllAvailable(self):
        """ 
        Get all bytes currently in the drivers receive buffer.
        Only used internally. 
        """
        errors = DWORD()
        self._ClearCommError(self.hFile, byref(errors), byref(self.comstat))
        n = self.comstat.cbInQue
        if n == 0:
            return ''
        ResetEvent(self.osReader.hEvent)
        lpBuffer = create_string_buffer(n)
        numberOfBytesRead = DWORD()
        if not self._ReadFile(
            self.hFile, 
            lpBuffer, 
            n, 
            byref(numberOfBytesRead), 
            byref(self.osReader)
        ):
            WaitForSingleObject(self.osReader.hEvent, INFINITE)
        return lpBuffer.raw[:numberOfBytesRead.value]
         
    
    def Write(self, data):
        """Writes a string to the port."""
        dwWritten = DWORD(0)
        r = self._WriteFile(
            self.hFile, 
            data, 
            len(data), 
            byref(dwWritten), 
            byref(self.osWriter)
        )
        if r != 0:
            return
        err = GetLastError()
        if err != 0 and err != ERROR_IO_PENDING:
            raise WinError()
        if not GetOverlappedResult(
            self.hFile, 
            byref(self.osWriter), 
            byref(dwWritten), 
            1
        ):
            raise WinError()
        if dwWritten.value != len(data):
            raise SerialException("Write timeout")
        
        
    def SetDtr(self, flag=True):
        """Sets DTR state."""
        EscapeCommFunction(self.hFile, SETDTR if flag else CLRDTR)
            

    def SetRts(self, flag=True):
        """Sets RTS state."""
        EscapeCommFunction(self.hFile, SETRTS if flag else CLRRTS)
            
            
    def GetBaudrate(self):
        """Returns the currently used baud rate as an integer."""
        return self.dcb.BaudRate
    
    
    def SetBaudrate(self, baudrate):
        """Sets the baud rate to an integer value."""
        self.dcb.BaudRate = baudrate
        SetCommState(self.hFile, byref(self.dcb))
        
        
    def GetMode(self):
        """
        Returns the currently used serial port mode setting as string.
        
        See :meth:`Open` for a complete description of the mode string.
        """
        dcb = self.dcb
        return (
            str(dcb.ByteSize) 
            + PARITY_V2S_DICT[dcb.Parity] 
            + STOPBITS_V2S_DICT[dcb.StopBits]
        )
        
    
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