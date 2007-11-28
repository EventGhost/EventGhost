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
# $LastChangedDate: 2007-07-25 05:07:21 +0200 (Mi, 25 Jul 2007) $
# $LastChangedRevision: 187 $
# $LastChangedBy: bitmonster $


import eg
from threading import Thread, Lock, Condition, currentThread
from time import clock
import ctypes
from WinAPI.cTypes import (
    pointer, sizeof, create_string_buffer, Structure, Union, byref, WinError,
    HANDLE, DWORD, LPCSTR, CreateFile, CloseHandle, 
    DCB, OVERLAPPED, COMSTAT, COMMTIMEOUTS, COMMCONFIG, ReadFile, WriteFile,
    GetCommState, SetCommState, ClearCommError, GetDefaultCommConfig,
    EscapeCommFunction, MsgWaitForMultipleObjects, WaitForSingleObject, 
    GetOverlappedResult, CreateEvent, SetEvent, ResetEvent, GetLastError,
    ERROR_IO_PENDING, WAIT_TIMEOUT, WAIT_OBJECT_0, QS_ALLINPUT, INFINITE,
    SETDTR, CLRDTR, SETRTS, CLRRTS, GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING,
    FILE_ATTRIBUTE_NORMAL, FILE_FLAG_OVERLAPPED, DTR_CONTROL_DISABLE, NOPARITY,
    ONESTOPBIT
)

INDENT = "    "
def dumps(obj, name=None, indent=""):
    res = []
    append = res.append
    if name is None:
        name = obj.__class__.__name__
    #append(indent + obj.__class__.__bases__[0].__name__ + " ")
    append(name + "(\n")
    
    for field in obj._fields_:
        if len(field) > 2:
            name, cType, length = field
            append(indent + INDENT + name + " = " + repr(getattr(obj, name)) + ",\n")
        else:
            name, cType = field
            if issubclass(cType, (Union, Structure)):
                append(indent + INDENT + name + " = ")
                append(dumps(getattr(obj, name), indent=indent + INDENT))
                append(",\n")
            else:
                append(indent + INDENT + name + " = " + repr(getattr(obj, name)) + ",\n")
    append(indent + ")")
    return "".join(res)



gSerialPortList = None

def EnumSerialPorts(dummy=None):
    """
    Return a list of all available serial ports of the system. (COM1 = 0)
    """
    global gSerialPortList
    if gSerialPortList is None:
        gSerialPortList = []
        commconfig = COMMCONFIG()
        commconfig.dwSize = sizeof(COMMCONFIG)
        lpCC = pointer(commconfig)
        dwSize = DWORD(0)
        lpdwSize = byref(dwSize)
        for i in range(0, 255):
            name = 'COM%d' % (i+1)
            res = GetDefaultCommConfig(LPCSTR(name), lpCC, lpdwSize)
            if res == 1 or (res == 0 and GetLastError() == 122):
                gSerialPortList.append(i)
    return gSerialPortList



class SerialException(Exception):
    """Base class for serial port related exceptions."""
    pass



class SerialThread(Thread):
    
    # These functions a bound to the class, so instances or subclasses 
    # can replace them. This is needed for code that uses the FTDI.DLL 
    # driver for example.
    ReadFile = ReadFile
    WriteFile = WriteFile
    ClearCommError = ClearCommError
    CreateFile = CreateFile
    CloseHandle = CloseHandle

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
        self.callbackThread = Thread(target=self.CallbackThreadProc, name="SerialReceiveThreadProc")
        
    
    def __enter__(self):
        self.SuspendReadEvents()
        return self
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ResumeReadEvents()
        return False
    
    
    def Open(self, port=0, baudrate=9600):
        #the "//./COMx" format is required for devices >= 9
        #not all versions of windows seem to support this propperly
        #so that the first few ports are used with the DOS device name
        if port < 9:
            deviceStr = 'COM%d' % (port+1) #numbers are transformed to a string
        else:
            deviceStr = '\\\\.\\COM%d' % (port+1)
        try:
            self.hFile = CreateFile(
                deviceStr,
                GENERIC_READ | GENERIC_WRITE,
                0, # exclusive access
                None, # no security
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
        dcb.ByteSize = 8
        dcb.Parity = NOPARITY
        dcb.StopBits = ONESTOPBIT
        dcb.BaudRate = baudrate
        SetCommState(self.hFile, byref(dcb))
    
        
    def Close(self):
        """Close port"""
        self.keepAlive = False
        SetEvent(self.stopEvent)
        if currentThread() != self:
            self.join(1.0)
        if self.hFile:
            #Restore original timeout values:
            #SetCommTimeouts(self.hFile, self._orgTimeouts)
            #Close COM-Port:
            if not self.CloseHandle(self.hFile):
                print (ctypes.FormatError(ctypes.GetLastError())).decode('mbcs')
            self.hFile = None

    
    def Start(self):
        self.callbackThread.start()
        self.start()

        
    def Stop(self):
        self.keepAlive = False
        SetEvent(self.stopEvent)
        if currentThread() != self:
            self.join(1.0)
        
        
    def SetReadEventCallback(self, callback):
        self.readEventCallback = callback
        
        
    def SuspendReadEvents(self):
        self.readEventLock.acquire()
    
    
    def ResumeReadEvents(self):
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
                r = self.ReadFile(
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
                r = GetOverlappedResult(hFile, byref(osReader), byref(dwRead), 0)
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
        readCounter = 0
        while self.keepAlive:
            #print "cycle"
            self.readCondition.acquire()
            while len(self.buffer):
                if self.readEventLock.acquire(0):
                    if self.readEventCallback:
                        try:
                            self.readEventCallback(self)
                        except:
                            eg.PrintTraceback()
                    self.readEventLock.release()
                else:
                    break
            self.readCondition.wait()
            self.readCondition.release()
            
        
    def HandleReceive(self, data):
        # read all data currently available
        data += self.ReadAllAvailable()
        # append the data to the buffer and notify waiting threads
        self.readCondition.acquire()
        self.buffer += data
        self.readCondition.notifyAll()
        self.readCondition.release()
            
            
    def Read(self, numBytes=1, timeout=0.0):    
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
        
        
    def ReadAllAvailable(self):
        """ 
        Get all bytes currently in the drivers receive buffer.
        Only used internally. 
        """
        errors = DWORD()
        self.ClearCommError(self.hFile, byref(errors), byref(self.comstat))
        n = self.comstat.cbInQue
        if n == 0:
            return ''
        ResetEvent(self.osReader.hEvent)
        lpBuffer = create_string_buffer(n)
        numberOfBytesRead = DWORD()
        if self.ReadFile(self.hFile, lpBuffer, n, byref(numberOfBytesRead), byref(self.osReader)):
            return lpBuffer.raw[:numberOfBytesRead.value]
        WaitForSingleObject(self.osReader.hEvent, INFINITE)
        return lpBuffer.raw[:numberOfBytesRead.value]
         
    
    def Write(self, data):
        """Writes data to the port."""
        dwWritten = DWORD(0)
        r = self.WriteFile(self.hFile, data, len(data), byref(dwWritten), byref(self.osWriter))
        if r != 0:
            return
        if GetLastError() != ERROR_IO_PENDING:
            raise WinError()
        if not GetOverlappedResult(self.hFile, byref(self.osWriter), byref(dwWritten), 1):
            raise WinError()
        if dwWritten.value != len(data):
            raise SerialException("Write timeout")
        
        
    def SetDtr(self, flag=True):
        """Sets DTR state."""
        EscapeCommFunction(self.hFile, SETDTR if flag else CLRDTR)
            

    def SetRts(self, flag=True):
        """Sets RTS state."""
        EscapeCommFunction(self.hFile, SETRTS if flag else CLRRTS)
            

    