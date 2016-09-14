# -*- coding: utf-8 -*-
#
# plugins/CM11A /__init__.py
#
# Written by Silviu Marghescu
#
# This file is a plugin for EventGhost.
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
#
# Revision history:
# -----------------
# 0.1 - first revision (basic commands and events)
# 0.2 - added the device reset command and the EEPROM event
# 0.3 - added support for multi-part events (unit and function received in separate messages)

help="""\
The plugin provides basic control of a CM11A device, over the serial interface.
No macro-processing functionality is implemented.

X10 events can be generated in two ways: discrete (e.g. CM11A.D2.On, etc.) or
generic (the event information is passed as payload for further processing).
Event generation can be disabled altogether.
"""

eg.RegisterPlugin(
    name = "CM11A",
    author = "Silviu Marghescu",
    version = "0.3.2",
    kind = "external",
    guid = "{7D5FF697-3094-4209-AEF6-E3DA575FB657}",
    description = "Control a CM11A device via the serial interface",
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1235",
    help = help,
    canMultiLoad = True,
    createMacrosOnAdd = False,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
        "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
        "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
        "YII="
    ),
)

import binascii
import string
import time

class Text:
    serialPort = "Serial Port:"
    eventGeneration = "Event Generation:"

    class StatusCommand:
        name = "Status Request Command"
        description = (
            "Retrieve and print the status of the CM11A device."
            "\n\n<p>"
            "No events are generated as a result of the status request."
        )
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    class ResetCommand:
        name = "Device Reset Command"
        description = (
            "Reset the CM11A device, by clearing any timers and/or macros from its internal memory."
        )

    class X10Command:
        name = "X10 Command"
        description = (
            "Submit an X10 command."
            "\n\n<p>"
            "Must define a house or device code and a function to perform."
        )
        houseCode = "House Code:"
        houseCodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
        deviceCode = "Device Code:"
        deviceCodes = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]
        function = "Function:"
        functions = ["All Units Off", "All Lights On", "All Lights Off", "On", "Off", "Dim", "Bright"]
        dimbright = "Dim/Bright %:"
        dimbrights = ["0", "5", "9", "14", "18", "23", "27", "32", "36", "41", "45", "50", "55", "59", "64", "68", "73", "77", "82", "86", "91", "95", "100"]

class CM11A(eg.PluginClass):
    text = Text

    def __init__(self):
        self.AddAction(StatusCommand)
        self.AddAction(ResetCommand)
        self.AddAction(X10Command)
        self.houseCodeMap = {
            "A" : 0x60,
            "B" : 0xE0,
            "C" : 0x20,
            "D" : 0xA0,
            "E" : 0x10,
            "F" : 0x90,
            "G" : 0x50,
            "H" : 0xD0,
            "I" : 0x70,
            "J" : 0xF0,
            "K" : 0x30,
            "L" : 0xB0,
            "M" : 0x00,
            "N" : 0x80,
            "O" : 0x40,
            "P" : 0xC0
        }
        self.deviceCodeMap = {
             "1" : 0x06,
             "2" : 0x0E,
             "3" : 0x02,
             "4" : 0x0A,
             "5" : 0x01,
             "6" : 0x09,
             "7" : 0x05,
             "8" : 0x0D,
             "9" : 0x07,
            "10" : 0x0F,
            "11" : 0x03,
            "12" : 0x0B,
            "13" : 0x00,
            "14" : 0x08,
            "15" : 0x04,
            "16" : 0x0C
        }
        self.functionMap = {
            "AllUnitsOff"  : 0x00,
            "AllLightsOn"  : 0x01,
            "On"           : 0x02,
            "Off"          : 0x03,
            "Dim"          : 0x04,
            "Bright"       : 0x05,
            "AllLightsOff" : 0x06,
            "ExtCode"      : 0x07,
            "HailReq"      : 0x08,
            "HailAck"      : 0x09,
            "Dim1"         : 0x0A,
            "Dim2"         : 0x0B,
            "ExtXfer"      : 0x0C,
            "StatusOn"     : 0x0D,
            "StatusOff"    : 0x0E,
            "StatusReq"    : 0x0F
        }
        self.serialThread = None
        self.LastAddr = None


    def __start__(self, port, eventGeneration):
        self.port = port
        self.eventGeneration = eventGeneration
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 4800, "8N1")
        self.serialThread.SetRts()
        self.serialThread.Start()


    def __stop__(self):
        self.serialThread.Close()


    def Configure(self, port=0, eventGeneration=0):
        text = self.text
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine(text.serialPort, portCtrl)
        eventCtrl = panel.Choice(eventGeneration, ['Discrete', 'Payload', 'Both', 'None'])
        panel.AddLine(text.eventGeneration, eventCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue(), eventCtrl.GetValue())


    def OnReceive(self, serial):
        ###print "OnReceive"
        buffer = ""
        while True:
            b = serial.Read(1, 0.1)
            if b == "\x5A":
                # event; send ACK to receive actual event data
                ###print "x5A received. Sending ACK."
                serial.Write("\xC3")
                return
            elif b == "\xA5":
                # power failure event; set the clock to clear
                ###print "xA5 received. Setting clock."
                self.TriggerEvent("PowerFail")
                serial.Write("\xFB")
                clockmsg = "\x9B"
                now = time.localtime()
                secs = now[5]
                mins = now[4]
                hrs = now[3]>>1
                if (hrs<<1) != now[3]:
                    mins += 60
                yday = now[7]&0xFF
                wday = now[6]+1
                if wday == 7:
                    wday = 0
                if yday != now[7]:
                    wday += 128
                clockmsg += chr(secs)
                clockmsg += chr(mins)
                clockmsg += chr(hrs)
                clockmsg += chr(yday)
                clockmsg += chr(wday)
                clockmsg += "\x00"
                serial.Write(clockmsg)
                serial.Read(1, 5)
                return
            elif b == "\x00":
                # ACK from the device
                self.TriggerEvent("ACK")
                return
            elif b == "\x5B":
                # EEPROM address
                self.TriggerEvent("EEPROM", binascii.b2a_hex(buffer[2:]).upper())
                return
            elif b == "":
                ###print("Buffer: "+binascii.b2a_hex(buffer).upper(), len(buffer))
                if len(buffer) == 1:
                    houseCode = self.Lookup(self.houseCodeMap, ord(buffer[0]) & 0xF0)
                    deviceCode = self.Lookup(self.deviceCodeMap, ord(buffer[0]) & 0x0F)
                    self.LastAddr = houseCode + deviceCode
                    ###print "Unit message: "+self.LastAddr
                    return
                length = ord(buffer[0])-1
                if length>10:
                    print "CM11A Unknown event: "+binascii.b2a_hex(buffer).upper()
                    return
                mask = ord(buffer[1])
                lastAddr = self.LastAddr
                self.LastAddr = None
                i = 0
                while i<length:
                    crtByte = ord(buffer[i+2])
                    funFlag = mask & (1 << i)
                    if funFlag:
                        houseCode = self.Lookup(self.houseCodeMap, crtByte & 0xF0)
                        functionCode = self.Lookup(self.functionMap, crtByte & 0x0F)
                        if functionCode in ("Dim", "Bright"):
                            dimByte = ord(buffer[i+3])
                            i = i + 1
                            dimVal = round(dimByte*100/210)
                            functionCode = functionCode + "." + str(dimVal)
                        if lastAddr:
                            self.GenerateEvent(lastAddr + "." + functionCode)
                            lastAddr = None
                        else:
                            self.GenerateEvent(houseCode + "." + functionCode)
                    else:
                        houseCode = self.Lookup(self.houseCodeMap, crtByte & 0xF0)
                        deviceCode = self.Lookup(self.deviceCodeMap, crtByte & 0x0F)
                        lastAddr = houseCode + deviceCode
                    i = i + 1
                return
            buffer += b

    def Lookup(self, map, value):
        for k in map.keys():
            if map[k] == value:
                return k
        return None

    def GenerateEvent(self, event):
        if self.eventGeneration in (0, 2):
            self.TriggerEvent(event)
        if self.eventGeneration in (1, 2):
            self.TriggerEvent("X10", event)


class ResetCommand(eg.ActionClass):
    def __call__(self):
        text = self.text
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write("\xFB\x00\x00\x00\x03\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF")
        self.plugin.serialThread.Read(1, 5) # read the F5 checksum
        self.plugin.serialThread.Write("\x00")
        self.plugin.serialThread.Read(1, 5) # read the 00 ACK
        self.plugin.serialThread.ResumeReadEvents()

    def GetLabel(self):
        return "Reset Device"


class StatusCommand(eg.ActionClass):
    def __call__(self):
        text = self.text
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write("\x8B")
        buffer = self.plugin.serialThread.Read(14, 5)
        ###print("Status buffer: "+binascii.b2a_hex(buffer).upper(), len(buffer))
        if buffer[0]=="\xFF" and buffer[1]=="\xFF":
            print "CM11A status: battery timer=RESET"
        else:
            print "CM11A status: battery timer=", ord(buffer[0])*256+ord(buffer[1])
        secs = ord(buffer[2])
        mins = ord(buffer[3])
        hrs = 2*ord(buffer[4])
        if mins>=60:
            mins -= 60
            hrs += 1
        print "CM11A status: time=", hrs, ":", mins, ":", secs
        print "CM11A status: day of year=", ord(buffer[5])+2*(ord(buffer[6])&0x80)
        print "CM11A status: day of week=", text.weekdays[ord(buffer[6])&0x7F]
        self.plugin.serialThread.ResumeReadEvents()

    def GetLabel(self):
        return "Status Request"


class X10Command(eg.ActionClass):

    def __call__(self, houseIndex=0, deviceIndex=0, functionIndex=3, dimbrightIndex=0):
        text = self.text
        houseCode = text.houseCodes[houseIndex]
        deviceCode = text.deviceCodes[deviceIndex]
        function = string.replace(text.functions[functionIndex], " ", "")
        self.plugin.serialThread.SuspendReadEvents()
        if deviceCode == "":
            header = 0x06 + (dimbrightIndex << 3)
            cmd = self.plugin.houseCodeMap[houseCode] | self.plugin.functionMap[function]
            self.SendReceive(chr(header)+chr(cmd), chr((header + cmd)&0xFF))
            self.SendReceive(chr(0), chr(0x55))
        else:
            header = 0x04
            cmd = self.plugin.houseCodeMap[houseCode] | self.plugin.deviceCodeMap[deviceCode]
            self.SendReceive(chr(header)+chr(cmd), chr((header + cmd)&0xFF))
            self.SendReceive(chr(0), chr(0x55))
            time.sleep(0.5)
            header = 0x06 + (dimbrightIndex << 3)
            cmd = self.plugin.houseCodeMap[houseCode] | self.plugin.functionMap[function]
            self.SendReceive(chr(header)+chr(cmd), chr((header + cmd)&0xFF))
            self.SendReceive(chr(0), chr(0x55))
        time.sleep(0.5)
        self.plugin.serialThread.ResumeReadEvents()

    def GetLabel(self, houseIndex, deviceIndex, functionIndex, dimbrightIndex):
        text = self.text
        houseCode = text.houseCodes[houseIndex]
        deviceCode = text.deviceCodes[deviceIndex]
        function = text.functions[functionIndex]
        return houseCode+deviceCode+" : "+function

    def SendReceive(self, buffer, result):
        ###print("Sending: "+binascii.b2a_hex(buffer).upper(), len(buffer))
        ###print("Expecting back: "+binascii.b2a_hex(result).upper(), len(result))
        r = None
        tries = 0
        while r != result and tries<10:
            self.plugin.serialThread.Write(buffer)
            r = self.plugin.serialThread.Read(1, 5)
            ###print("Response buffer: "+binascii.b2a_hex(r).upper(), len(r))
            tries = tries + 1

    def Configure(self, houseIndex=0, deviceIndex=0, functionIndex=3, dimbrightIndex=0):
        text = self.text
        panel = eg.ConfigPanel(self)
        houseCodeCtrl = panel.Choice(houseIndex, text.houseCodes)
        deviceCodeCtrl = panel.Choice(deviceIndex, text.deviceCodes)
        functionCtrl = panel.Choice(functionIndex, text.functions)
        dimbrightCtrl = panel.Choice(dimbrightIndex, text.dimbrights)

        def OnStateChoice(event):
            dimbrightCtrl.Enable(functionCtrl.GetValue() in (5,6))
            event.Skip()
        functionCtrl.Bind(wx.EVT_CHOICE, OnStateChoice)
        OnStateChoice(wx.CommandEvent())

        panel.AddLine(self.text.houseCode, houseCodeCtrl)
        panel.AddLine(self.text.deviceCode, deviceCodeCtrl)
        panel.AddLine(self.text.function, functionCtrl)
        panel.AddLine(self.text.dimbright, dimbrightCtrl)

        while panel.Affirmed():
            panel.SetResult(
                houseCodeCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                functionCtrl.GetValue(),
                dimbrightCtrl.GetValue()
            )

