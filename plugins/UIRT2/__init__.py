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

class PluginInfo(eg.PluginInfo):
    name = "UIRT2"
    author = "Bitmonster"
    version = "1.0.0"
    kind = "remote"
    description = (
        'Hardware plugin for the "Universal InfraRed Transceiver V2".'
    )
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAaElEQVR42mNkoBAwDgMD"
        "/jMw/IeaRLJhIL1gAw4eOMBg7+AANwQsgYWNrrkR2QWkGALTXE+uAQ1APkgziguQQpU8"
        "F5BiAE4XNEIkGYkJRJghcANgmkmJRpAhjA1QA0jVjORlysDAGwAAHWBIBf4cTRAAAAAA"
        "SUVORK5CYII="
    )


import threading
import Queue
import time
import binascii
import string
import wx
from eg.WinAPI.SerialPort import SerialPort, EnumSerialPorts

SAMPLE_TIME = 0.00005
MyDecoder = eg.IrDecoder(SAMPLE_TIME)

    
def calc_checksum(data):
    checksum = 0
    for i in xrange(len(data)):
        checksum += ord(data[i])
        checksum %= 256
    checksum = (0x100 - checksum) % 256
    return chr(checksum)
    

def get_struct_time(code, start):
    tvalue = (ord(code[start+1]) * 256) + ord(code[start+2])
    bBits = ord(code[start+3])
    bHdr1 = ord(code[start+4])
    bHdr0 = ord(code[start+5])
    bOff0 = ord(code[start+6])
    bOff1 = ord(code[start+7])
    bOn0 = ord(code[start+8])
    bOn1 = ord(code[start+9])
    tvalue += bHdr1 + bHdr0
    for i in range(0, bBits):
        bit = (ord(code[start + 10 + (i / 8)]) >> (i % 8)) & 1
        if (i % 2) == 0:
            if bit:
                tvalue += bOn1
            else:
                tvalue += bOn0
        else:
            if bit:
                tvalue += bOff1
            else:
                tvalue += bOff0
    return tvalue


def calc_time(code):
    tvalue = 0
    if code[0] == "\x36":  
        # RAW
        length = ord(code[1])
        tvalue = (ord(code[2]) * 256) + ord(code[3])
        for i in range(4, length + 4):
            tvalue += ord(code[i])
        tvalue = tvalue * (ord(code[-2]) & 0x1F)
        #tvalue -= (ord(code[2]) * 256) + ord(code[3])
    elif (ord(code[0]) & 0x1F) > 0:
        # REMSTRUCT1
        repeat = ord(code[0]) & 0x1F
        tvalue = get_struct_time(code, 0) * repeat
        #tvalue -= (ord(code[1]) * 256) + ord(code[2])

    else:
        # REMSTRUCT2
        tvalue = get_struct_time(code, 0)
        repeat = ord(code[26]) & 0x1F
        tvalue = tvalue + (get_struct_time(code, 26) * repeat)
    return tvalue * SAMPLE_TIME


class MyHexValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return MyHexValidator()

    def TransferToWindow(self):
        return True
        
    def TransferFromWindow(self):
        return True

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        for x in val:
            if x not in string.hexdigits:
                return False
        return True


    def OnChar(self, event):
        key = event.KeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.hexdigits:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling event.Skip eats the event before it
        # gets to the text control
        return


# Thread class that executes processing
class UirtThread(threading.Thread):
    
    def __init__(self, comport, comspeed, plugin):
        self.receiveQueue = Queue.Queue(2048)
        threading.Thread.__init__(self)
        self._want_abort = False
        self.comport = comport
        self.comspeed = comspeed
        self.plugin = plugin
        self.start()
        
        
    def run(self):
        # This is the code executing in the new thread. 
        lasttime = time.clock()
        sp = self.sp = SerialPort(self.comport, self.comspeed)
        try:
            sp.open()
        except:
            self.plugin.PrintError("Can't open COM port.")
            return 
        sp.SetRTS()
        buffer = ""
        try:
            success = False
            for i in range(0, 3):
                time.sleep(0.05)
                sp.read()
                # get version
                sp.write("\x23\xdd")
                time.sleep(0.05)
                response = sp.read()
                if response != "\x01\x04\xFB":
                    continue
                # set raw mode
                sp.write("\x21\xdf")
                time.sleep(0.05)
                response = sp.read()
                if response != "\x21":
                    continue
                success = True
                break
            if not success:
                self.plugin.PrintError("Error connecting to UIRT2")
                return
            while not self._want_abort:
                if not self.receiveQueue.empty():
                    received_event = self.receiveQueue.get()
                    if received_event[0] == 1:
                        n = sp.write(received_event[1])
                        time.sleep(0.05)
                        data = sp.read(-1)
                        if data != " ":
                            self.plugin.PrintError("Error sending IR code to UIRT2")
                        data = ""
                        while data != "\x21" and not self._want_abort:
                            sp.write("\x21\xdf")
                            time.sleep(0.05)
                            data = sp.read(-1)
                        #time.sleep(calc_time(received_event[1]) + 0.05)
                        received_event[2].set()
                data = sp.read(-1)
                if len(data):
                    buffer += data
                    while True:
                        terminator_pos = buffer.find("\xff")
                        if terminator_pos < 0:
                            break
                        data = []
                        for c in buffer[2:terminator_pos]:
                            data.append(ord(c))
                        buffer = buffer[terminator_pos+1:]
                        if len(data) < 2:
                            continue
                        event = MyDecoder.Decode(data, len(data))
                        if event:
                            self.plugin.TriggerEvent(event)
                else:
                    time.sleep(0.01)
        finally:
            sp.write("\x20\xe0")
            sp.close()
            

    def abort(self):
        self._want_abort = 1
        self.join(1.0)



class UIRT2(eg.RawReceiverPlugin):
    canMultiLoad = True
    
    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(self.TransmitIR)


    def __start__(self, comport=0):
        self.thread = UirtThread(comport, 115200, self)


    def __stop__(self):
        self.thread.abort()


    def Configure(self, comport=0):
        dialog = eg.ConfigurationDialog(self)
        portCtrl = eg.SerialPortChoice(dialog, value=comport)
        
        dialog.sizer.Add(
            wx.StaticText(dialog, -1, "COM-Port:"), 
            0, 
            wx.ALIGN_CENTER_VERTICAL
        )
        dialog.sizer.Add(portCtrl)

        if dialog.AffirmedShowModal():
            return (portCtrl.GetValue(),)
    
    
    
    class TransmitIR(eg.ActionClass):
        name = "Transmit IR"
        
        def __call__(self, code, wait_till_finished=True):
            event = threading.Event()
            self.plugin.thread.receiveQueue.put((1, code, event))
            if wait_till_finished:
                event.wait(5.0)
                if not event.isSet():
                    self.PrintError("UIRT2 transmitting timed out")                
            

        def GetLabel(self, *args):
            return self.name
        
        
        def Configure(self, code=None, wait_till_finished=True):
            dialog = eg.ConfigurationDialog(self)
            code1 = ""
            code2 = ""
            repeatCount = 4
            carrier = 0
            if code:
                code += (48 * "\x00") 
                if code[0] == "\x36":
                    length = ord(code[1])
                    code1 = "R" + binascii.hexlify(code[2:length]).upper()
                    repeatCount = ord(code[length]) & 0x1F
                    carrier = ord(code[length]) >> 6
                else:
                    repeatCount = ord(code[0]) & 0x1F
                    if repeatCount > 0:
                        carrier = ord(code[0]) >> 6
                        code1 = binascii.hexlify(code[1:26]).upper()
                    else:
                        repeatCount = ord(code[26]) & 0x1F
                        carrier = ord(code[0]) >> 6
                        code1 = binascii.hexlify(code[1:26]).upper()
                        code2 = binascii.hexlify(code[27:48]).upper()
            if carrier < 0:
                carrier = 0
            elif carrier > 3:
                carrier = 3
            if repeatCount < 1:
                repeatCount = 1
            elif repeatCount > 31:
                repeatCount = 31
            sizer = wx.FlexGridSizer(4,2,5,5)
            sizer.AddGrowableCol(1)
            
            st1 = wx.StaticText(dialog, -1, "Code 1:")
            sizer.Add(st1, 0, wx.ALIGN_CENTER_VERTICAL)
            code1Ctrl = wx.TextCtrl(dialog, -1, code1, size=(325,-1))
            sizer.Add(code1Ctrl)
            
            st2 = wx.StaticText(dialog, -1, "Code 2:")
            sizer.Add(st2, 0, wx.ALIGN_CENTER_VERTICAL)
            code2Ctrl = wx.TextCtrl(
                dialog, 
                -1, 
                code2, 
                size=(275,-1), 
                validator=MyHexValidator()
            )
            sizer.Add(code2Ctrl)
            
            st3 = wx.StaticText(dialog, -1, "Repeat:")
            sizer.Add(st3, 0, wx.ALIGN_CENTER_VERTICAL)
            repeatCtrl = eg.SpinIntCtrl(dialog, -1, repeatCount, 1, 31)
            repeatCtrl.SetInitialSize((50,-1))
            sizer.Add(repeatCtrl, 0)
            
            st3 = wx.StaticText(dialog, -1, "Carrier:")
            sizer.Add(st3, 0, wx.ALIGN_CENTER_VERTICAL)
            choices = ('35.7 kHz', '37.0 kHz', '38.4 kHz', '40.0 kHz')
            carrierCtrl = wx.Choice(dialog, -1, choices=choices)
            carrierCtrl.SetSelection(3 - carrier)
            sizer.Add(carrierCtrl, 0)
                        
            dialog.sizer.Add(sizer, 0, wx.EXPAND)
            
            dialog.sizer.Add((5,5))
            cb = wx.CheckBox(dialog, -1, "Pause till transmission finished")
            cb.SetValue(wait_till_finished)
            dialog.sizer.Add(cb)

            if dialog.AffirmedShowModal():
                code1 = code1Ctrl.GetValue()
                if len(code1) == 0:
                    return None, cb.GetValue()
                code2 = code2Ctrl.GetValue()
                repeatCount = repeatCtrl.GetValue()
                carrier = 3 - carrierCtrl.GetSelection()
                if code1[0] == "R":
                    data = binascii.unhexlify(code1[1:])
                    bCmd = repeatCount | (carrier << 6)
                    code = "\x36" + chr(len(data) + 2) + data + chr(bCmd)
                elif len(code2) == 0:
                    data = binascii.unhexlify(code1)
                    bCmd = repeatCount | (carrier << 6)
                    code = chr(bCmd) + data
                else:
                    bCmd = 0 | (carrier << 6)
                    bCmd2 = repeatCount | (carrier << 6)
                    code = chr(bCmd) + binascii.unhexlify(code1) \
                           + chr(bCmd2) + binascii.unhexlify(code2)
                return code + calc_checksum(code), cb.GetValue()
