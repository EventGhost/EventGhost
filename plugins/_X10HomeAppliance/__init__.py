# Copyright (c) 2002 Michael Dove <pythondeveloper@optushome.com.au>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import eg

class PluginInfo(eg.PluginInfo):
    name = "X10 Home Appliance"
    author = "Bitmonster"
    version = "0.0.1"
    kind = "external"
    description = "Control X10 home appliance modules through a C11a device."

from __future__ import with_statement


#import select
import thread
import time
from math import log
#import tty
#import termios
import Queue
from threading import Condition, Thread, currentThread
import os
#import fcntl            
import string

# Debug output
DEBUG=1
#########################
#         TODO        
#
# - Extended commands
#########################


#########################
#        Constants
#########################
OK = 0x00
READY = 0x55
STATUS = 0x8b
OFF = 0x03
ON = 0x02
RINGENABLE = 0xeb
RINGDISABLE = 0xdb
POLL = 0x5a
PWRFAIL = 0xa5
FUNCHDR = 0x06
ADDRHDR = 0x04
EXTHDR = 0x07
PCREADY = 0xc3

# Function Codes
ALLUNITOFF = 0x00
ALLLIGHTON = 0x01
DIM = 0x04
BRIGHT = 0x05
ALLLIGHTOFF = 0x06
EXTCODE = 0x07
HAILREQ = 0x08
HAILACK = 0x09
DIMPRE1 = 0x0A
DIMPRE2 = 0x0B
EXTXFER = 0x0C
STATUSON = 0x0D
STATUSOFF = 0x0E
STATUSREQ = 0x0F

FUNCTION_CODES = (
    "All Units Off",
    "All Lights On",
    "On",
    "Off",
    "Dim",
    "Bright",
    "All Lights Off",
    "Extended Code",
    "Hail Request",
    "Hail Acknowledge",
    "Pre-set Dim (1)",
    "Pre-set Dim (2)",
    "Extended Data Transfer",
    "Status On",
    "Status Off",
    "Status Request",
)

MAP2CM11 = [13, 5, 3, 11, 15, 7, 1, 9, 14, 6, 4, 12, 16, 8, 2, 10]
CODE2BYTE = (6, 14, 2, 10, 1, 9, 5, 13, 7, 15, 3, 11, 0, 8, 4, 12)
CODE_CHARS = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
    "N", "O", "P"
]
WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


class CM12:
    "CM12 X10 Device"


    def __init__(self, device):
        self.file = serial.Serial(device, 4800)
        self.queue = Queue.Queue(30)
        self.lock = Condition()
        self.readControl = threading.RLock()
        self.x10listener = X10Listener(self.file, self.queue, self.lock, self, self.readControl)
        self.x10listener.start()
        

    def close(self):
        self.x10listener.stop()
        self.x10listener.join()    
        self.file.close()
    

    def on(self, house, devices):
        "Turn on X10 devices with retries and error checking"
        if self.__switch(ON, house, devices):
            return 1


    def off(self, house, devices):
        "Turn off X10 device with retries and error checking"
        if self.__switch(OFF, house, devices):
            return 1


    def extended(self, house, device, extdata, command):
        "Send an extended command"
        data = [0,0,0,0]
        data[0] = EXTHDR
        data[1] = catBytes(houseCode(house), EXTCODE)
        data[2] = extdata
        data[3] = command
        if self.__sendNibble(data):
            print "Error: Unable to send extended command"

    
    def dim(self, house, device, amount):
        "Dim light"

        if amount > 100: 
            amount = 100
        elif amount < 0: 
            amount = 0

        hbyte = self.houseCode(house)

        for dev in device:
            dbyte = self.devCode(device)
            address = self.catBytes(hbyte, dbyte)
            self.__sendNibble([ADDRHDR, address])

        dimamt = catBytes(amount/100 * 22, FUNCHDR)
        data = self.catBytes(hbyte, DIM)
        self.__sendNibble([dimamt, data])
        

    def bright(self, house, device, amount):
        "Brighten light"
        if amount > 100: 
            amount = 100
        elif amount < 0: 
            amount = 0

        hbyte = self.houseCode(house)

        for dev in device:
            dbyte = self.devCode(dev)
            address = self.catBytes(hbyte, dbyte)
            self.__sendNibble([ADDRHDR, address])

        brightamt = catBytes(amount/100 * 22, FUNCHDR)
        data = self.catBytes(hbyte, BRIGHT)
        self.__sendNibble([brightamt, data])

           
    def __xsend(self, data, retries=3):
        "Send data list with timeout and retry, returns recieved response"
        with self.readControl:
            debug("Sending some data: %s" % data)
            for i in range(retries):        # we will send the data 3 times before giving up for a response
                debug("xsend: try: %d of %d" %(i + 1, retries))
                for byte in data:
                    debug("xsend: sending byte: %s" % hex(byte))
                    self.send(byte)

                response = self.__xread()
                debug("xsend RESPONSE: %X" % response)
                if response: 
                    return response
            

    def __xread(self, timeout=10):
        "Recieve data with a timeout period"
        with self.readControl:
            try:
                return self.queue.get(0)
            except Queue.Empty, e:
                debug("xread: waiting on read")
                self.lock.acquire()
                self.lock.wait(timeout)
                self.lock.release()
                try:
                    return self.queue.get(0)
                except Queue.Empty, e:
                    pass


    def __switch(self, action, house, devices):
        "Do a standard x10 function command"
        with self.readControl:
            hbyte = self.houseCode(house)
            for device in devices:
                dbyte = self.devCode(device)
                data = self.catBytes(hbyte, dbyte)
                self.__sendNibble([ADDRHDR, data])
            data = self.catBytes(hbyte, action)
            self.__sendNibble([FUNCHDR, data])

                
    def __sendNibble(self, data):
        "Send Nibble with retries"
        with self.readControl:
            sum = self.xchecksum(data)
            for i in range(3):
                chksum = self.__xsend(data)
                if chksum == None:
                    print "Error: Device not responding"
                    return 1
                elif chksum == sum:
                    break
                print "Error: Invalid Checksum, trying again, should be: %d" % sum
            self.send(OK)
            if self.__xread() != READY:
                print "Error: Device Not Ready"
                return 1


    def xchecksum(self, data):
        "Calculate the checksum of a list"
        sum = 0
        for i in data:
            sum +=i
        return sum & 0xff            


    def send(self, data):
        "Send a single byte"
        if type(data) == type([]):
            bytes = ''
            for i in data:
                bytes += chr(i)
            return self.file.write(bytes)            
        else: 
            return self.file.write(chr(data))


    def houseCode(self, code):
        "House code to byte"
        code = code.upper()
        return CODE2BYTE[ord(code) - ord("A")]

    def devCode(self, code):
        "Device code to byte"
        return CODE2BYTE[code - 1]

    def byte2hcode(self, byte):
        "Byte to house code"
        return chr(byte + ord('A') - 6)

    def byte2devcode(self, byte):
        "Byte to device code"
        return byte + ord('1') - 6

    def catBytes(self, byteone, bytetwo, shift=4):
        "concat to bytes"
        return byteone << shift | bytetwo

    def ready(self):
        "Check if interface is ready"
        if self.queue.get() == READY:
            return 1

    def getPoll(self):
        with self.readControl:
            debug("Sending PCREADY")
            bufsize = self.__xsend([PCREADY])
            if bufsize is None:
                debug("Error: got no response!")
                return
            debug("Sent PCREADY")
            debug("Poll Buffer Size: %d" % bufsize)
            mask = self.__xread()
            debug("getPoll: BitMask: (%s) %s" % (hex(mask), self.b2s(mask)))
            data = []
            for i in (range(bufsize - 1)):
                tmp = self.__xread()
                debug("getPoll: got data %i of %i: %X" % (i+1, bufsize-1, tmp))
                if mask << i:
                    debug(self.GetFunctionCode(tmp))
                else:
                    debug(self.GetUnitCode(tmp))
                
                data.append(tmp)
            debug("Poll buffer contents: %s" %data)


    def uploadMacro(self, eaddress, data):
        "Upload eeprom data"
        timer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        print "Timer length: %d" % len(timer)
        # 19 bytes of timer data
        self.send(0xfb) # Macro upload start byte
        timer[0] = eaddress / 256
        timer[1] = eaddress % 256
        timer.extend(data)

        if self.__sendNibble(timer):
            print "Error: Unable to upload macro"


    def uploadTime(self, house='A'):
        import time
        curtime = time.localtime()
        data = [0,0,0,0,0,0.0,0]
        data[0] = 0x9b                                     # time upload header
        data[1] = curtime[5]                               # seconds
        data[2] = curtime[4] + ((curtime[3] % 2) * 60)     # minutes 0-119
        data[3] = ((curtime[3] + 5) % 12)                  # hours 0-11
        data[4] = curtime[7] % 256                         # current day
        data[5] =  (curtime[7] / 256) << 7                 # current year day
        data[5] = data[5] | (2 ** ((curtime[6] + 1) % 7))  # weekmask (SMTWTFS)
        data[6] = self.houseCode(house) << 4               # House Code rest of bits blank
        self.send(data)


    def getStatus(self):
        "Get the status of device"

        self.send(STATUS)
        status = []
        # Load up all the bytes into a tuple
        for byte in range(14):
            status.append(self.__xread())
            
        #batt = struct.unpack('H', chr(status[0]) + chr(status[1]))
        # or can use
        batt = status[0] << 8 | status[1]
        sec = status[2] & 0xff
        min = (status[3] & 0xff) %60
        hrs = ((status[4] & 0xff) * 2) + ((status[3] & 0xff) / 60)
        day = status[5] + (((status[6] & 0x080) >> 7) * 256)
        dayofweek = status[6] & 0x7f
        hcode = (status[7] & 0xf0) >> 4
        rev = status[7] & 0x0f
        mon = self.x2unitmap(status[8] + (status[9] << 8))
        mstat = self.x2unitmap(status[10] + (status[11] << 8))
        dimstat = self.x2unitmap(status[12] + (status[13] << 8))

        return [batt, sec, min, hrs, day, dayofweek, hcode, rev, mon, mstat, dimstat]
        

    def printStatus(self):
        status = self.getStatus()

        print "Battery Life: %.0d" % ((1.0 / (2 ** 16 / float(status[0])) * 100) + 0.5)
        print "Seconds: %d" % status[1]
        print "Minutes: %d" % status[2]
        print "Hours: %d" % status[3]
        print "Day: %d" % status[4]
        print "Day of Week: %s" % WEEKDAYS[int(log(status[5]) / log(2))]
        print "House Code: %s" % self.byte2hcode(status[6])
        print "Firmware Revision: %d" % status[7]
        print "Last addressed device: %s" % self.b2s(status[8])
        print "Status of monitored devices: %s" % self.b2s(status[9])
        print "Dim Status of monitored devices: %d" % status[10]


    def ringEnable(self):
        if self.__sendNibble([RINGENABLE]):
            print "Error: Unable to enable ring"


    def ringDisable(self):
        if self.__sendNibble([RINGDISABLE]):
            print "Error: Unable to disable ring"


    def checkQueue(self, data):
        "peform the appropriate action"
        if data == POLL: # Poll
            print "Recieved: Poll"
            self.getPoll()
        elif data == PWRFAIL: # Power fail, time request
            print "Recieved: Powerfail Macro Download, uploading time"
            self.uploadTime()
        elif data == 120:
            stop = self.OK
            print "Unknown poll detected"
            print self.queue.get(0)
            print "Try stopping with %d" % stop
            print self.send(stop)
            print "Done trying to stop poll"


    def GetFunctionCode(self, byte):
        high = (byte >> 4) & 0x0F
        housecode = chr(MAP2CM11[high] + ord("A") - 1)
        function = FUNCTION_CODES[byte & 0xF]
        return housecode + " " + function
    
    
    def GetUnitCode(self, byte):
        high = (byte >> 4) & 0x0F
        housecode = chr(MAP2CM11[high] + ord("A") - 1)
        unitcode = str(MAP2CM11[byte & 0xF])
        return housecode + unitcode
    
    
    def x2unitmap(self, map):
        ret_map = 0
        cntr = 0
        while ( cntr < 16 ):
            if ( (map & ( 0x01 << cntr)) != 0):
                ret_map += (0x1 << (MAP2CM11[cntr] -1))

            cntr+=1
        return ret_map            
            
        
    def b2s(self, bin, numBits=8):
        "binary 2 string"
        output = [0,0,0,0,0,0,0,0]
        for i in range(numBits):
            if (bin & (0x01 << i)):
                output[i] = "1"
            else:
                output[i] = "0"
        output.reverse()
        return string.join(output, '')



def debug(message):
    "Print debug messages"
    if DEBUG:
        print "DEBUG: ", message
            
import threading
import win32event

class X10Listener(Thread):
    
    def __init__(self, file, queue, lock, parent, readControl):
        Thread.__init__(self)
        self.serial = file
        self.queue = queue
        self.runThread = 1
        self.lock = lock
        self.parent = parent
        self.readControl = readControl
        self.stopEvent = win32event.CreateEvent(None, 1, 0, None)


    def stop(self):
        "Stop Listening, ends thread"
        win32event.SetEvent(self.stopEvent)
        self.join()


    def run(self):
        from win32event import (
            ResetEvent, 
            MsgWaitForMultipleObjects, 
            QS_ALLINPUT, 
            WAIT_OBJECT_0, 
            WAIT_TIMEOUT,
        )
        from win32file import ReadFile, AllocateReadBuffer, GetOverlappedResult
        from win32api import GetLastError

        overlapped = self.serial._overlappedRead
        hComPort = self.serial.hComPort
        hEvent = overlapped.hEvent
        stopEvent = self.stopEvent
        events = (hEvent, stopEvent)
        n = 1
        waitingOnRead = False
        buf = AllocateReadBuffer(n)
        while True:
            if not waitingOnRead:
                ResetEvent(hEvent)
                hr, _ = ReadFile(hComPort, buf, overlapped)
                if hr == 997:
                    waitingOnRead = True
                elif hr == 0:
                    pass
                    #n = GetOverlappedResult(hComPort, overlapped, 1)
                    #self.HandleChar(str(buf))
                else:
                    self.PrintError("error")
                    raise

            rc = MsgWaitForMultipleObjects(
                events,
                0, 
                1000, 
                QS_ALLINPUT
            )
            if rc == WAIT_OBJECT_0:
                n = GetOverlappedResult(hComPort, overlapped, 1)
                if n:
                    data = buf[0]
                    if self.readControl.acquire(False):
                        threading.Thread(target=self.parent.checkQueue, args=(ord(data),)).start()
                        self.readControl.release()
                    else:
                        with self.lock:
                            debug("X10Listener: received data: 0x%X" %ord(data))
                            self.queue.put(ord(data))
                            self.lock.notify()
                waitingOnRead = False
            elif rc == WAIT_OBJECT_0+1:
                # stop event received
                break
            elif rc == WAIT_TIMEOUT:
                pass
            else:
                self.PrintError("unknown message")
                
                    
#    def run(self):
#        file = self.file
#        from time import sleep
#        while self.__keepRunning():
#            #debug("X10Listener: listener loop")
#            if file.inWaiting():
#                try:
#                    data = file.read(1)
#                except IOError, e:
#                    print "Error: IOError reading from device"
#                    continue
#                if self.readControl.acquire(False):
#                    threading.Thread(target=self.parent.checkQueue, args=(ord(data),)).start()
#                    self.readControl.release()
#                else:
#                    with self.lock:
#                        debug("X10Listener: received data: 0x%X" %ord(data))
#                        self.queue.put(ord(data))        # if len(data) == 0, select will stop working properly
#                        self.lock.notify()
#            else:
#                sleep(0.01)
                
                
            
import eg
import wx
import eg.WinAPI.serial as serial

class X10HomeAppliance(eg.PluginClass):
    
    def __start__(self, comPort):
        self.x10 = CM12(comPort)
        
        
    def __stop__(self):
        self.x10.close()
        
        
    def Configure(self, comPort=1):
        dialog = eg.ConfigurationDialog(self)
        portCtrl = eg.SerialPortChoice(dialog, value=comPort)
        
        flags = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
        mySizer = wx.FlexGridSizer(4, 2, 5, 5)
        mySizer.Add(wx.StaticText(dialog, -1, 'Port:'), 0, flags)
        mySizer.Add(portCtrl, 0, wx.EXPAND)

        dialog.sizer.Add(mySizer)
        
        if dialog.AffirmedShowModal():
            return (
                portCtrl.GetValue(),
            )
        
        
        
class On(eg.ActionClass):
    
    def __call__(self, houseCode="A", devices=[1]):
        self.plugin.x10.on(houseCode, devices)
        
        
    def GetLabel(self, houseCode, devices):
        s = houseCode + str(devices[0])
        for device in devices[1:]:
            s += ", " + houseCode + str(device)
        return self.plugin.name + ": " + self.name + ": " + s
    
    
    def Configure(self, houseCode="A", devices=[1]):
        dialog = eg.ConfigurationDialog(self)
        houseCodeCtrl = wx.Choice(dialog, choices=CODE_CHARS)
        houseCodeCtrl.SetSelection(ord(houseCode.upper()) - ord("A"))
        dialog.sizer.Add(houseCodeCtrl)
        checkBoxes = []
        gridSizer = wx.GridSizer(1, 16)
        for i in range(16):
            cb = wx.CheckBox(dialog, label=str(i + 1))
            if devices.count(i + 1):
                cb.SetValue(True)
            gridSizer.Add(cb)
            checkBoxes.append(cb)
        dialog.sizer.Add(gridSizer)    
        if dialog.AffirmedShowModal():
            return (
                chr(houseCodeCtrl.GetSelection() + ord("A")),
                [i+1 for i, cb in enumerate(checkBoxes) if cb.GetValue()],
            )
        
        
class Off(On):
    class text:
        name = "Off"
        
    def __call__(self, houseCode="A", devices=[1]):
        self.plugin.x10.off(houseCode, devices)
        
    