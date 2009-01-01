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
import win32file, win32con
        
        
def DeviceString(portnum):
    """Turn a port number into a device name"""
    #the "//./COMx" format is required for devices >= 9
    #not all versions of windows seem to support this propperly
    #so that the first few ports are used with the DOS device name
    if portnum < 9:
        return 'COM%d' % (portnum+1) #numbers are transformed to a string
    else:
        return '\\\\.\\COM%d' % (portnum+1)



class SerialPort(object):
    
    def __init__(self, port=0, baud=2400):
        self.port = port
        self.baudrate = baud
        self.buffer = win32file.AllocateReadBuffer(512)
        self.data = ""
        self.hFile = None
        self.dcb = None
       
    
    def open(self):
        try:
            self.hFile = win32file.CreateFile(
                DeviceString(self.port),
                win32con.GENERIC_READ|win32con.GENERIC_WRITE,
                0,    # exclusive access
                None, # no security
                win32con.OPEN_EXISTING,
                0,
                None
            )
            win32file.SetupComm(self.hFile, 1024, 1024)
            # clear any pending I/O
            win32file.PurgeComm(
                self.hFile,
                (
                    win32file.PURGE_TXABORT
                    |win32file.PURGE_TXCLEAR
                    |win32file.PURGE_RXABORT 
                    |win32file.PURGE_RXCLEAR
                )
            )
    
            # set the port characteristics
            dcb = win32file.GetCommState(self.hFile)
            self.dcb = dcb
            dcb.BaudRate = self.baudrate
            dcb.fBinary = True
            dcb.fParity = False
            dcb.fOutxCtsFlow = False
            dcb.fOutxDsrFlow = False
            dcb.fDtrControl = win32file.DTR_CONTROL_DISABLE
            #dcb.fDtrControl = win32file.DTR_CONTROL_ENABLE
            dcb.fDsrSensitivity = False
            dcb.fTXContinueOnXoff = True
            dcb.fOutX = False
            dcb.fInX = False
            dcb.fErrorChar = False
            dcb.fNull = False
            dcb.fRtsControl = False
            #dcb.fAbortOnError = True
            dcb.fAbortOnError = False

            dcb.ByteSize = 8
            dcb.Parity = win32file.NOPARITY
            dcb.StopBits = win32file.ONESTOPBIT
            
            win32file.SetCommState(self.hFile, dcb)
            win32file.SetCommTimeouts(self.hFile, (-1, 0, 0, 100, 100))
        except:
            #eg.PrintError("Error opening " + DeviceString(self.port))
            #eg.PrintTraceback()
            if self.hFile:
                win32file.CloseHandle(self.hFile)
            self.hFile = None
            raise
         
        
    def GetBaudrate(self):
        return self.dcb.Baudrate
    
    
    def SetBaudrate(self, baudrate):
        self.dcb.baudrate = baudrate
        win32file.SetCommState(self.hFile, self.dcb)
        
    baudrate = property(GetBaudrate, SetBaudrate)
    
    
    def SetDTR(self, flag=True):
        if flag:
            win32file.EscapeCommFunction(self.hFile, win32file.SETDTR)
        else:
            win32file.EscapeCommFunction(self.hFile, win32file.CLRDTR)
            

    def SetRTS(self, flag=True):
        if flag:
            win32file.EscapeCommFunction(self.hFile, win32file.SETRTS)
        else:
            win32file.EscapeCommFunction(self.hFile, win32file.CLRRTS)
            


    @eg.LogIt
    def read(self, n=None):
        """try to read a certain number of characters"""
        try:
            rc, data = win32file.ReadFile(self.hFile, self.buffer)
        except:
            eg.PrintTraceback()
            eg.PrintError("I/O Error in read")
            self.close()
            self.open()
            return None
        return data


    @eg.LogIt
    def write(self, data):
        """write data out the port"""
        try:
            errCode, numBytes = win32file.WriteFile(self.hFile, data)
            if errCode:
                raise IOError
        except:
            eg.PrintTraceback()
            eg.PrintError("I/O Error:")
            self.close()
            self.open()
        return numBytes
            

    def close(self):
        if self.hFile:
            win32file.CloseHandle(self.hFile)
            self.hFile = None

