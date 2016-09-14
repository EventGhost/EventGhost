# -*- coding: utf-8 -*-
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

from __future__ import with_statement

import eg

eg.RegisterPlugin(
    name = "Barco CRT Projector",
    description = "Controls Barco CRT projectors via RS232.",
    kind = "external",
    author = "Bitmonster",
    version = "1.0.0",
    guid = "{74902850-2F8B-4384-95D0-59E9D96D0BF9}",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wD/AP83WBt9"
        "AAAACXBIWXMAAAsTAAALEwEAmpwYAAABTElEQVR4nJWRO0sDQRSFz53Z7GNWo0VMYgiI"
        "D9BERJSAP8PCyl9g5T8QC/HniI3Y2qnYZyEoeYAYo8YgaFbzmBmLXdYUksepprjfnHPP"
        "Ja01JpEBwD85lV5p5ChfXxPHRwxAv+jp9idfXZS1KlteUI0nnlvSsgtS5Fo042LK7l3f"
        "yqIXOhCIFzZJOM7hgayWrf09isf56oosVaClUdgCZ2w2Lh+fQ0BDq9YHs0xZrvZu7ozt"
        "DVV/o2mXzSVUsyUrNUB1zi5iO4UQANA9v4yySu9hyCYsiDROPzoCNMZqliJgIk0cyQBw"
        "lcvXFQEgoiGHz+TzuwFQTqXvv/yRDt/JVOgwmMh1hSsEAFeI1+a7ktI0Y1ojcjb+0gEA"
        "lFSZZAKMc86FbfWlchw7ZpqNxkvwrwEgm0kPNtv+6QQPIgLQ9n34vm1b2fk0gGFb/qtf"
        "bUt6K1gxHQUAAAAASUVORK5CYII="
    ),
)



ACTIONS = (
    ("Enter", "Enter", None, (0x07, )),
    ("Exit", "Exit", None, (0x08, )),
    ("Up", "Cursor Up", None, (0x21, )),
    ("Down", "Cursor Down", None, (0x22, )),
    ("Left", "Cursor Left", None, (0x24, )),
    ("Right", "Cursor Right", None, (0x23, )),
    ("AdjustToggle", "Adjust Toggle", None, (0x09, )),
    ("AdjustOn", "Adjust On", None, (0x51, 0x09, 0x00, 0x00, 0x01)),
    ("AdjustOff", "Adjust Off", None, (0x51, 0x09, 0x00, 0x00, 0x00)),
    ("TextToggle", "Text Toggle", None, (0x0d, )),
    ("TextOn", "Text On", None, (0x51, 0x06, 0x00, 0x00, 0x01)),
    ("TextOff", "Text Off", None, (0x51, 0x06, 0x00, 0x00, 0x00)),
    ("PauseToggle", "Pause Toggle", None, (0x0f, )),
    ("PauseOff", "Pause Off", None, (0x51, 0x01, 0x00, 0x00, 0x00)),
    ("PauseOn", "Pause On", None, (0x51, 0x01, 0x00, 0x00, 0x01)),
    ("PowerToggle", "Power Toggle", None, (0x0e, )),
    ("PowerOff", "Power Off (Standby)", None, (0x51, 0x0a, 0x00, 0x00, 0x00)),
    ("PowerOn", "Power On", None, (0x51, 0x0a, 0x00, 0x00, 0x01)),
    ("Numpad0", "Numpad 0", None, (0x10, )),
    ("Numpad1", "Numpad 1", None, (0x11, )),
    ("Numpad2", "Numpad 2", None, (0x12, )),
    ("Numpad3", "Numpad 3", None, (0x13, )),
    ("Numpad4", "Numpad 4", None, (0x14, )),
    ("Numpad5", "Numpad 5", None, (0x15, )),
    ("Numpad6", "Numpad 6", None, (0x16, )),
    ("Numpad7", "Numpad 7", None, (0x17, )),
    ("Numpad8", "Numpad 8", None, (0x18, )),
    ("Numpad9", "Numpad 9", None, (0x19, )),
    ("ContrastUp", "Contrast Up", None, (0x28, )),
    ("ContrastDown", "Contrast Down", None, (0x29, )),
    ("BrightnessUp", "Brightness Up", None, (0x2a, )),
    ("BrightnessDown", "Brightness Down", None, (0x2b, )),
    ("SaturationUp", "Colour Saturation Up", None, (0x2c, )),
    ("SaturationDown", "Colour Saturation Down", None, (0x2d, )),
    ("TintUp", "Colour Tint Up", None, (0x22, )),
    ("TintDown", "Colour Tint Down", None, (0x2f, )),
    ("SharpnessUp", "Sharpness Up", None, (0x36, )),
    ("SharpnessDown", "Sharpness Down", None, (0x37, )),
)

import wx
from time import sleep, clock

STX = 0x02
ACK = chr(0x06)
NAK = chr(0x15)
BAUDRATES = [110, 150, 300, 600, 1200, 2400, 4800, 9600]
ALL_BYTE_VALUES = frozenset(range(256))


class ActionBase(eg.ActionBase):

    def __call__(self):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, *self.value)


    def SendCommand(
        self, serial, cmd, dat1=0, dat2=0, dat3=0, dat4=0, block=None
    ):
        data = [self.plugin.address, cmd, dat1, dat2, dat3, dat4]
        checksum = sum(data) % 256
        data.append(checksum)

        if block is not None:
            data2 = [ord(x) for x in block]
            checksum2 = sum(data2) % 256
            data += data2
            data.append(checksum2)

        offset = 0
        if STX in data:
            offset = 1
            while offset in data:
                offset += 1
            offset = (STX - offset) % 256

        data = [STX, offset] + [(x + offset) % 256 for x in data]
        s = "".join([chr(x) for x in data])
        if eg.debugLevel:
            print " ".join(["%02X" % x for x in data])
        serial.Write(s)
        res = serial.Read(1, 0.5)
        if res != ACK:
            raise self.Exceptions.DeviceNotFound("Got no ACK!")


    def GetResponse(self, serial, cmde):
        answer = serial.Read(7, 1.0)
        if len(answer) < 7:
            raise self.Exceptions.DeviceNotFound("Not enough bytes received!")
        if eg.debugLevel:
            print " ".join(["%02X" % ord(x) for x in answer])
        answer = [ord(c) for c in answer]
        adr, cmd, dat1, dat2, dat3, dat4, chks = answer
        if adr != self.plugin.address:
            raise self.Exceptions.DeviceNotFound("Wrong address received!")
        if cmd != cmde:
            raise self.Exceptions.DeviceNotFound("Wrong command received!")
        if chks != sum(answer[:6]) % 256:
            raise self.Exceptions.DeviceNotFound("Wrong checksum received!")
        return dat1, dat2, dat3, dat4



class SendCustom(ActionBase):

    def __call__(self, cmd, dat1, dat2, dat3, dat4):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, cmd, dat1, dat2, dat3, dat4)


    def GetLabel(self, *args):
            return " ".join("%02X" % arg for arg in args)


    def Configure(self, cmd=0, dat1=0, dat2=0, dat3=0, dat4=0):
        panel = eg.ConfigPanel()
        values = cmd, dat1, dat2, dat3, dat4
        ctrls = [
            panel.SpinIntCtrl(values[i], min=0, max=255)
            for i in range(5)
        ]
        hexCtrl = panel.StaticText("")
        def UpdateValue(event):
            res = ["%02X" % ctrl.GetValue() for ctrl in ctrls]
            hexCtrl.SetLabel(" ".join(res))
            event.Skip()
        UpdateValue(wx.CommandEvent())
        for ctrl in ctrls:
            ctrl.Bind(wx.EVT_TEXT, UpdateValue)

        panel.AddLine("CMD:", ctrls[0])
        panel.AddLine(
            "DAT1:", ctrls[1], None,
            "DAT2:", ctrls[2], None,
            "DAT3:", ctrls[3], None,
            "DAT4:", ctrls[4]
        )
        panel.AddLine()
        panel.AddLine("Hex string:", hexCtrl)
        while panel.Affirmed():
            panel.SetResult(*(ctrl.GetValue() for ctrl in ctrls))



class SetText(ActionBase, eg.ActionWithStringParameter):

    def __call__(self, s):
        s = s + (chr(0) * (208 - len(s)))
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x70, 0x01, 0x01, 0x01, 0x0c, s)



class ReadTime(ActionBase):

    def __call__(self):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x60)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x60)
            result = dat1 * 256 + dat2
            print "Hours:", result
            return result



class ReadStatus(ActionBase):

    def __call__(self):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x4b)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x4b)
            print "Fast/Slow:", bool(dat1 & (1 << 7))
            print "Green Convergence:", bool(dat1 & (1 << 6))
            print "Cursor Position:", dat2
            print "PC mode:", bool(dat3 & (1 << 3))
            print "Text mode:", bool(dat3 & (1 << 2))
            print "Pause:", bool(dat3 & (1 << 1))
            print "Standby:", bool(dat3 & (1 << 0))
            extraInfo = bool(dat3 & (1 << 7))
            if extraInfo:
                print "Magnetic focus:", bool(dat3 & (1 << 6))
                print "Convergence is stripped:", bool(dat3 & (1 << 7))
                print "Orbiting installed:", bool(dat4 & (1 << 0))
                print "Soft edge installed:", bool(dat4 & (1 << 1))
                print "Contrast modulation installed:", bool(dat4 & (1 << 2))
                print "NS is mounted on the convergence:", bool(
                    dat4 & (1 << 3)
                )
                print "Controller with ASIC:", bool(dat4 & (1 << 4))
                print "IRIS is installed:", bool(dat4 & (1 << 5))
                print "Dynamic stigmators:", bool(dat4 & (1 << 6))




class ReadVersion(ActionBase):

    def __call__(self):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x4c)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x4c)
            print "Identifier:", chr(dat1)
            print "Version: %d%d.%d%d" % (
                dat2 / 16, dat2 & 0x0f, dat3 / 16, dat3 & 0x0f
            )
            print "Model:", dat4




class ReadSerialNumber(ActionBase):

    def __call__(self):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x4d)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x4d)
            digits = (
                chr(48 + (dat1 & 0x0f)),
                chr(48 + (dat2 / 16)),
                chr(48 + (dat2 & 0x0f)),
                chr(48 + (dat3 / 16)),
                chr(48 + (dat3 & 0x0f)),
                chr(48 + (dat4 / 16)),
                chr(48 + (dat4 & 0x0f))
            )
            s = "".join(digits)
            print "Serial Number:", s
            return



class GetInfo(ActionBase):

    def __call__(self):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x4b)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x4b)
            print "Fast/Slow:", bool(dat1 & (1 << 7))
            print "Green Convergence:", bool(dat1 & (1 << 6))
            print "Cursor Position:", dat2
            print "PC mode:", bool(dat3 & (1 << 3))
            print "Text mode:", bool(dat3 & (1 << 2))
            print "Pause:", bool(dat3 & (1 << 1))
            print "Standby:", bool(dat3 & (1 << 0))
            extraInfo = bool(dat3 & (1 << 7))
            if extraInfo:
                print "Magnetic focus:", bool(dat3 & (1 << 6))
                print "Convergence is stripped:", bool(dat3 & (1 << 7))
                print "Orbiting installed:", bool(dat4 & (1 << 0))
                print "Soft edge installed:", bool(dat4 & (1 << 1))
                print "Contrast modulation installed:", bool(dat4 & (1 << 2))
                print "NS is mounted on the convergence:", bool(
                    dat4 & (1 << 3)
                )
                print "Controller with ASIC:", bool(dat4 & (1 << 4))
                print "IRIS is installed:", bool(dat4 & (1 << 5))
                print "Dynamic stigmators:", bool(dat4 & (1 << 6))
            self.SendCommand(serial, 0x4d)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x4d)
            digits = (
                chr(48 + (dat1 & 0x0f)),
                chr(48 + (dat2 / 16)),
                chr(48 + (dat2 & 0x0f)),
                chr(48 + (dat3 / 16)),
                chr(48 + (dat3 & 0x0f)),
                chr(48 + (dat4 / 16)),
                chr(48 + (dat4 & 0x0f))
            )
            s = "".join(digits)
            print "Serial Number:", s
            self.SendCommand(serial, 0x60)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x60)
            result = dat1 * 256 + dat2
            print "Hours:", result
            self.SendCommand(serial, 0x4c)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x4c)
            print "Identifier:", chr(dat1)
            print "Version: %d%d.%d%d" % (
                dat2 / 16, dat2 & 0x0f, dat3 / 16, dat3 & 0x0f
            )
            print "Model:", dat4
            self.SendCommand(serial, 0x4a)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x4a)
            print "Horizontal period: %dns" % (dat1 * 250)
            print "Vertical frequency: %d Hz" % dat4
            if dat2 & 0x80:
                print "Source block number: %d not closed" % (dat2 & 0x7f)
            else:
                print "Source block number: %d" % (dat2 & 0x7f)
            SOURCES = {
                0: "Video",
                1: "SVHS",
                2: "TTL",
                3: "RGsB",
                4: "RGBS",
                5: "Internal",
                8: "Forced video",
                9: "Forced SVHS",
                0xA: "Forced TTL",
                0xB: "Forced RGsB",
                0xC: "Forced RGBS",
            }
            print "Source: " + SOURCES.get(dat3 / 16, "Unknown")
            INSTALLATIONS = [
                "Rear/ Ceiling",
                "Front / Table",
                "Front/ Ceiling",
                "Rear / Table"
            ]
            print "Installation: " + INSTALLATIONS[dat3 & 0x03]
            print "HDTV:", dat3 & 0x04



class RequestShape(ActionBase):

    def __call__(self, shape=0, x=0, y=0, colours=0x07):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x78, shape, y * 16 + x, colours)


    def Configure(self, shape=0, x=0, y=0, colours=0x07):
        choices = [
            ("Internal convergence pattern", 0x00),
            ("Horizontal line in center of zones", 0x01),
            ("Vertical line in center of zones", 0x02),
            ("Crosshatch in zone XY", 0x05),
            ("Convergence contour around zone XY", 0x06),
            ("Erase shape, switch colour", 0x07),
            ("Vertical bars, switch colour", 0x08),
            ("Horizontal bars, switch colour", 0x09),
        ]
        panel = eg.ConfigPanel()
        shapeCtrl = panel.SpinIntCtrl(shape, max=255)
        xCtrl = panel.SpinIntCtrl(x, max=9)
        yCtrl = panel.SpinIntCtrl(y, max=9)
        redCtrl = panel.CheckBox(colours & 0x01, "Red")
        greenCtrl = panel.CheckBox(colours & 0x02, "Green")
        blueCtrl = panel.CheckBox(colours & 0x04, "Blue")
        panel.AddLine("Shape:", shapeCtrl)
        panel.AddLine("X coordinate:", xCtrl)
        panel.AddLine("Y coordinate:", yCtrl)
        panel.AddLine("Colours:", redCtrl)
        panel.AddLine(None, greenCtrl)
        panel.AddLine(None, blueCtrl)
        while panel.Affirmed():
            colours = int(redCtrl.GetValue()) * 0x01
            colours |= int(greenCtrl.GetValue()) * 0x02
            colours |= int(blueCtrl.GetValue()) * 0x04
            panel.SetResult(
                shapeCtrl.GetValue(),
                xCtrl.GetValue(),
                yCtrl.GetValue(),
                colours,
            )



class LockIr(ActionBase):
    name = "Lock IR"
    description = (
        "Programs the projector to filter out certain infrared commands."
    )

    def __call__(self, flags=0x7f):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x50, flags)


    def Configure(self, flags=0x7f):
        panel = eg.ConfigPanel()
        choices = [
            "Stand by",
            "Pause",
            "Text",
            "Adjust keys (Adj, Enter, Exit, cursors)",
            "Numeric keys",
            "Picture control keys",
            "Sound control keys",
        ]
        panel.AddLine("Allowed IR-commands:")
        ctrls = []
        for i, choice in enumerate(choices):
            ctrl = panel.CheckBox(flags & (1 << i), choice)
            ctrls.append(ctrl)
            panel.AddLine(None, ctrl)
        while panel.Affirmed():
            flags = 0
            for i, ctrl in enumerate(ctrls):
                flags |= (1 << i) * int(ctrl.GetValue())
            panel.SetResult(flags)



class ReadPotentiometer(ActionBase):

    def __call__(self, kind, x=0, y=0):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x7a, kind, y * 16 + x)
            dat1, dat2, dat3, dat4 = self.GetResponse(serial, 0x7a)
            print "Value:", dat1, dat2, dat3, dat4
            return dat3


    def Configure(self, kind=0, x=0, y=0):
        panel = eg.ConfigPanel()
        kindCtrl = panel.SpinIntCtrl(kind, max=255)
        xCtrl = panel.SpinIntCtrl(x, max=9)
        yCtrl = panel.SpinIntCtrl(y, max=9)
        panel.AddLine("Potentiometer:", kindCtrl)
        panel.AddLine("X coordinate:", xCtrl)
        panel.AddLine("Y coordinate:", yCtrl)
        while panel.Affirmed():
            panel.SetResult(
                kindCtrl.GetValue(),
                xCtrl.GetValue(),
                yCtrl.GetValue(),
            )



class WritePotentiometer(ActionBase):

    def __call__(self, kind, x=0, y=0, value=128, flags=3):
        print kind, x, y, value, flags
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, 0x79, kind, y * 16 + x, value, flags)


    def Configure(self, kind=0, x=0, y=0, value=128, flags=3):
        panel = eg.ConfigPanel()
        kindCtrl = panel.SpinIntCtrl(kind, max=255)
        xCtrl = panel.SpinIntCtrl(x, max=9)
        yCtrl = panel.SpinIntCtrl(y, max=9)
        valueCtrl = panel.SpinIntCtrl(value, max=255)
        deltaCb = panel.CheckBox(not (flags & 1), "Value is delta")
        storeCb = panel.CheckBox(not (flags & 2), "Store in EEPROM")
        panel.AddLine("Potentiometer:", kindCtrl)
        panel.AddLine("X coordinate:", xCtrl)
        panel.AddLine("Y coordinate:", yCtrl)
        panel.AddLine("Value/Delta:", valueCtrl)
        panel.AddLine(deltaCb)
        panel.AddLine(storeCb)

        while panel.Affirmed():
            panel.SetResult(
                kindCtrl.GetValue(),
                xCtrl.GetValue(),
                yCtrl.GetValue(),
                valueCtrl.GetValue(),
                int(not deltaCb.GetValue()) + int(not storeCb.GetValue()) * 2
            )


class Barco(eg.PluginBase):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionBase)
        group = self.AddGroup("Unfinished")
        group.AddAction(SetText)
        group.AddAction(RequestShape)
        group.AddAction(LockIr)
        group.AddAction(ReadSerialNumber)
        group.AddAction(ReadVersion)
        group.AddAction(ReadStatus)
        group.AddAction(ReadTime)
        group.AddAction(GetInfo)
        group.AddAction(ReadPotentiometer)
        group.AddAction(WritePotentiometer)
        group.AddAction(SendCustom)


    @eg.LogIt
    def __start__(self, port=0, address=0, baudrate=9600):
        self.port = port
        self.address = address
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, baudrate)
        self.serialThread.SetRts()
        self.serialThread.Start()


    def __stop__(self):
        self.serialThread.Close()


    def OnReceive(self, serial):
        data = serial.Read(512)
        print "Barco: " + " ".join(["%02X" % ord(c) for c in data])


    def Configure(self, port=0, address=0, baudrate=9600):
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)
        choices = [str(baudrate) for baudrate in BAUDRATES]
        baudrateCtrl = panel.Choice(BAUDRATES.index(baudrate), choices=choices)
        addrCtrl = panel.SpinIntCtrl(address, min=0, max=255)
        panel.AddLine("Serial port:", portCtrl)
        panel.AddLine("Baudrate:", baudrateCtrl)
        panel.AddLine("Projector address:", addrCtrl)
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                addrCtrl.GetValue(),
                BAUDRATES[baudrateCtrl.GetValue()],
            )

