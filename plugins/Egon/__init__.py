version="0.1.1"
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


eg.RegisterPlugin(
    name = "Egon",
    author = "Pako on the basis of work by Bitmonster",
    version = version,
    kind = "remote",
    guid = "{677B5282-BA96-40F8-AEF7-46191007C9B1}",
    description = 'Hardware plugin for the <a href="http://ruckl.wz.cz/egon/egon.html">'
        'Egon</a> USB or RS232 IR receiver.\n\n<p>'
        '<BR><B><U>Features:</U></B>'
        '<BR>Tiny, simple, minimum of parts, single-sided PCB'
        '<BR>Firmware upgradeable using builtin bootloader'
        '<BR>Configurable using terminal emulator program'
        '<BR>Current version "understands" 17 IR protocols (e.g. RC5 etc.)'
        '<BR>Analysis mode for unknown protocols'
        '<BR><BR><I>Construction is free for non-commercial use</I>',
    #url = "http://www.eventghost.org/forum/viewtopic.php",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAACXBIWXMAAAsSAAALEgHS3X78AAAB"
        "LklEQVR42pWSz0oDQQzGv1cSn6CISBEVEQ8eRKHK+odKS9Wi0tp1q6X06E0QFFQQD62gBwWxpayu"
        "1veRPX0mM1gXpDhCSGZn8ttvMgkwFcMjSsQesUVkqZ8LxBwxQ0wQY8QIMUqME0OfkIzJW1ZeWely"
        "95nFRxbumWtx44brl1w5p3fKpRMuHnM4bxjUGPQ0+08TRnXQ4NGHEyA6SFmgR4l9s8fJHbspd9N6"
        "FHj/yej/7zfsndkaGgzcgLULYlpinQeRE5C9JmYN4L8MBJI15JrEvAH2QyeFwh2RMX34B7Aq8ZDl"
        "7sBnTa63H4i8AXbaTo0rd8ywCbD55AaERFEAn6krZUSn1NHryYEf6tMFEauRdqkqjXpjummmGJlY"
        "GNFRC4yvffu68dYkZ1lGI/4CWXPG2yR1czoAAAAASUVORK5CYII="
    ),
)
   
class Text:
    port = "Serial port:"
    virt_port = "Virtual serial port:"
    error = "Can't open serial port"
    radioboxHW = "Version of hardware"
    usb_ver = "USB (6MHz, 57600 Bd)"
    serial_ver ="Serial (4 MHz, 38400 Bd)"
    eventPrefix = "Event prefix:"

import threading
import win32event
import win32file
from time import sleep

class Egon(eg.RawReceiverPlugin):
    canMultiLoad = True
    text = Text

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.serial = None
        self.buffer = ""
    
    @eg.LogIt
    def __start__(self, port, hw, prefix):           
        try:
            self.serial = eg.SerialPort(
                port, 
                baudrate=57600 if hw==0 else 38400, 
                bytesize=8,
                stopbits=1,
                parity='N'
            )
        except:
            eg.PrintTraceback()
            self.serial = None
            raise eg.Exception(self.text.error)
        self.serial.timeout = 1.0
        self.serial.setRTS(1)
        self.serial.setDTR(1)
        self.serial.setRTS(0)
        self.serial.setDTR(0)
        sleep(0.5)
        self.serial.flushInput()
        self.serial.setRTS(1)
        self.serial.setDTR(1)
        self.info.eventPrefix = prefix
        self.terminator = "\x0D\x0A"
        self.stopEvent = win32event.CreateEvent(None, 1, 0, None)
        self.receiveThread = threading.Thread(target=self.ReceiveThread)
        self.receiveThread.start()
    
    def __stop__(self):
        if self.serial is not None:
            if self.receiveThread:
                win32event.SetEvent(self.stopEvent)
                self.receiveThread.join(1.0)
            self.serial.close()
            self.serial = None

           
    def HandleChar(self, ch):
        if True:
            self.buffer += ch
            pos = self.buffer.find(self.terminator)
            if pos != -1:
                eventstring = self.buffer[:pos].strip()
                if eventstring:
                    self.TriggerEvent(eventstring)
                self.buffer = "" #ATTENTION - HERE CHANGE !!!
#            self. buffer = self.buffer[pos+len(self.terminator):]
            
            
    def ReceiveThread(self):
        from win32event import (
            ResetEvent, 
            MsgWaitForMultipleObjects, 
            QS_ALLINPUT, 
            WAIT_OBJECT_0, 
            WAIT_TIMEOUT,
        )
        from win32file import ReadFile, AllocateReadBuffer, GetOverlappedResult
        from win32api import GetLastError

        continueLoop = True
        overlapped = self.serial._overlappedRead
        hComPort = self.serial.hComPort
        hEvent = overlapped.hEvent
        stopEvent = self.stopEvent
        n = 1
        waitingOnRead = False
        buf = AllocateReadBuffer(n)
        while continueLoop:
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
                (hEvent, stopEvent),
                0, 
                1000, 
                QS_ALLINPUT
            )
            if rc == WAIT_OBJECT_0:
                n = GetOverlappedResult(hComPort, overlapped, 1)
                if n:
                    self.HandleChar(str(buf))
                #else:
                #    print "WAIT_OBJECT_0", n, str(buf[:n])
                waitingOnRead = False
            elif rc == WAIT_OBJECT_0+1:
                continueLoop = False
            elif rc == WAIT_TIMEOUT:
                pass
            else:
                self.PrintError("unknown message")        
               
            
    def Configure(self, port=0, hw=0, prefix="Egon"):
        text=self.text
        panel = eg.ConfigPanel(self)
        radioBoxHW = wx.RadioBox(
            panel, 
            -1, 
            text.radioboxHW,
            (0,0),
            (201,70),
            choices=[text.usb_ver, text.serial_ver],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxHW.SetSelection(hw)
        dynSizer = wx.FlexGridSizer(2,2,20,0)
        dynSizer.SetMinSize((201,0))
        dynSizer.AddGrowableCol(0, proportion=2)
        dynSizer.AddGrowableCol(1, proportion=1)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(radioBoxHW,0,wx.TOP,0)
        mainSizer.Add(dynSizer,0,wx.TOP,25)
        panel.AddLine(mainSizer)

        def onHW_Change(event=None):
            dynSizer.Clear(True)
            if radioBoxHW.GetSelection()==0:
                portLbl=wx.StaticText(panel, -1, text.virt_port)
            else:
                portLbl=wx.StaticText(panel, -1, text.port)
            portCtrl = panel.SerialPortChoice(port)
            prefixLbl=wx.StaticText(panel, -1, text.eventPrefix)
            prefixCtrl = panel.TextCtrl(prefix)
            dynSizer.Add(portLbl,0,wx.TOP,5)
            dynSizer.Add(portCtrl,0,wx.EXPAND)
            dynSizer.Add(prefixLbl,0,wx.TOP,5)
            dynSizer.Add(prefixCtrl,0,wx.EXPAND)
            dynSizer.Layout()

            if event != None:
                event.Skip()
            
        radioBoxHW.Bind(wx.EVT_RADIOBOX, onHW_Change)
        onHW_Change()
        
        while panel.Affirmed():
            panel.SetResult(
                dynSizer.GetChildren()[1].GetWindow().GetValue(), 
                radioBoxHW.GetSelection(),
                dynSizer.GetChildren()[3].GetWindow().GetValue()
            )
                    
