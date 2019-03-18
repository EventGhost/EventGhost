# This file is part of EventGhost.
# Copyright (C) 2009 Peter
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
# $LastChangedDate: 2009-11-02 $
# $LastChangedRevision: 1 $
# $LastChangedBy: Peter $


import eg

eg.RegisterPlugin(
    name="USB-RLY08",
    guid='{B3239935-ACD7-4442-806D-11F98BA41AE9}',
    author="Peter",
    version="1.0." + "$LastChangedRevision: 1194 $".split()[1],
    canMultiLoad=True,
    description=("Allows using the USB-RLY08 device. \n"
                 "More Info on: http://www.robot-electronics.co.uk/htm/usb_rly08tech.htm"
                 ),
    icon=("iVBORw0KGgoAAAANSUhEUgAAABQAAAAQCAIAAACZeshMAAAAB3RJTUUH2QsMFyE2nq9c"
          "YQAAAAlwSFlzAAALEQAACxEBf2RfkQAAAARnQU1BAACxjwv8YQUAAANOSURBVHjaHVNN"
          "aFxVFL7n3vt+5r/JpM04GltLQGkrXURREUJ0UagLF3HjRiwIdeFaXUlLqltFNy4VRMWC"
          "XbnQQmsNDSg21ZpqQ+vkZ5pxGDN/7715777777WLszgcDt93zvd9sPz95yxNapV6EfuA"
          "kQIbUL+T7k/7Fa7lSCSAwSJkXYGVPCNeQWKkGQumpqnMMtGNH6KN2DJD4MTs/D/jLh2x"
          "PMQVCipVzBqKQFKkkSLpQOFS2fqpNLrAaahxRZDq7Z3t0d6br58NKZhi+Vai1nq7QMgr"
          "cyfbnV0TwqmnF6VRxCMffvLxYW/m9hSK6oziXFquVS69QfJ4rWyUBEq7DlaYidRfXboY"
          "8sniqRdgkpYwiIygXjQqedYLycSnOYaCscbaXpy89+lHVgqitSnUKnNHmrVCX6pJxtfW"
          "/1i9vmopAUw7w8HJyiFrNAPkzpKArDZmbrbxztm3PayVgdWbP1+73+qLGAdEY3/pxHMv"
          "Lb6otaKed+78+TAgGACMplIrX1mrtcjTaH8n5wwTytkYEzcnZUCx1Swbbmys+4RwZZPx"
          "uFwvWI2RlFRgKFpNCOml6Rc//gRKOOYcUVYt2P5w3I/9+catrb2t7bYllGA8FnnTKWcM"
          "A0tDpZ2OnOdHDh4698ZbgBQC+sPalautTVYtVUohM/KZ408sL50G0H5YXFm50P67zQ5P"
          "YUGpABQajSwaROMrv1xlaQbG3O3ct1rBfsIznj9c2Gxvf3npa4xRxsTm3TtFXHKiCKWo"
          "AZBKCGVSpW60O8Rqd8wwzro2tzyySjFuBgLlaeLY+ZhEIms2HomwmZicAnfYCBnVrNbe"
          "XX7VagF++O133xyVeuH0QjHwL/96rYTMmZdfw1bSoPj+BxdamzsMQsNCyj0IwVhA+3ly"
          "8frltD8Q0eT3P3978thT/a1/pZR5L1vf25AOQutcqju7LWzBuA4ZePazFecPlAtNIZcR"
          "jfRMprI8Pjp7/ACUozgZ6vhG/JcJMBLaYfjUwwibg1U7V6dhGNiZaR0g0DKQPtR1wRAT"
          "j7KJEr1uEkW8USzPN/GBwoN4OVCECARBDcplWN1ruaz970/nM0dGCeneiOnwXufezQ0h"
          "+MLS848ee8zNMX6w7aLpXoSsMvY/BggPtRZ0zhMAAAAASUVORK5CYII=")
)

###########################################################################################################################
# USB Relais Module - USB-RLY08
#
# The COM port should be set up for 19200 baud, 8 data bits, no parity and two stop bits
#
# Command Action
# dec hex 
#  90 5A Get software version - returns 2 bytes, the first being the Module ID which is 8, followed by the software version 
#  91 5B Get relay states - sends a single byte back to the controller, bit high meaning the corresponding relay is powered
#  92 5C Set relay states - the next single byte will set all relays states, All on = 255 (11111111) All off = 0 
# 100 64 All relays on 
# 101 65 Turn relay 1 on 
# 102 66 Turn relay 2 on 
# 103 67 Turn relay 3 on 
# 104 68 Turn relay 4 on 
# 105 69 Turn relay 5 on 
# 106 6A Turn relay 6 on 
# 107 6B Turn relay 7 on 
# 108 6C Turn relay 8 on  
# 110 6E All relays off  
# 111 6F Turn relay 1 off 
# 112 70 Turn relay 2 off 
# 113 71 Turn relay 3 off 
# 114 72 Turn relay 4 off 
# 115 73 Turn relay 5 off 
# 116 74 Turn relay 6 off 
# 117 75 Turn relay 7 off 
# 118 76 Turn relay 8 off 
############################################################# 

import binascii


class USBRelaisModule(eg.RawReceiverPlugin):
    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(GetSoftwareVersion)
        self.AddAction(GetRelayStates)
        self.AddAction(SetRelayStates)
        self.AddAction(TurnRelaisAllOn)
        self.AddAction(TurnRelais1On)
        self.AddAction(TurnRelais2On)
        self.AddAction(TurnRelais3On)
        self.AddAction(TurnRelais4On)
        self.AddAction(TurnRelais5On)
        self.AddAction(TurnRelais6On)
        self.AddAction(TurnRelais7On)
        self.AddAction(TurnRelais8On)
        self.AddAction(TurnRelaisAllOff)
        self.AddAction(TurnRelais1Off)
        self.AddAction(TurnRelais2Off)
        self.AddAction(TurnRelais3Off)
        self.AddAction(TurnRelais4Off)
        self.AddAction(TurnRelais5Off)
        self.AddAction(TurnRelais6Off)
        self.AddAction(TurnRelais7Off)
        self.AddAction(TurnRelais8Off)

    def __start__(
        self,
        port,
    ):
        try:
            self.serial = eg.SerialPort(
                port,
                baudrate='19200',
                bytesize=8,
                stopbits=2,
                parity='N',
                xonxoff=0,
                rtscts=0,
            )
        except:
            self.serial = None
            raise self.Exceptions.SerialOpenFailed
        self.serial.timeout = 1.0
        self.serial.setRTS()

    def __stop__(self):
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    def Configure(
        self,
        port=0,
    ):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)
        panel.SetColumnFlags(1, wx.EXPAND)
        panel.sizer.Add(portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())


class GetSoftwareVersion(eg.ActionClass):
    description = "Get Software Version (as 2 byte Hex format) of USB-RLY08\n"
    name = "Get Software Version"

    def __call__(self):
        self.plugin.serial.write("\x5A")
        self.plugin.serial.timeout = 1.0
        return binascii.b2a_hex(self.plugin.serial.read(2))


class GetRelayStates(eg.ActionClass):
    description = "Get Relay States (as 1 byte Hex format) of USB-RLY08\n"
    name = "Get Relay States"

    def __call__(self):
        self.plugin.serial.write("\x5B")
        return binascii.b2a_hex(self.plugin.serial.read(1))


class SetRelayStates(eg.ActionClass):
    description = "Set Relay States (as 1 byte Hex format) of USB-RLY08\n"
    name = "Set Relay States"

    def __call__(self, datahexbyte):
        self.plugin.serial.write("\x5C")
        self.plugin.serial.write(binascii.a2b_hex(datahexbyte))
        return self.plugin.serial

    def Configure(
        self,
        datahexbyte="00",
    ):
        panel = eg.ConfigPanel()
        dataCtrl = panel.TextCtrl(datahexbyte)
        panel.SetColumnFlags(1, wx.EXPAND)
        panel.sizer.Add(dataCtrl)
        while panel.Affirmed():
            panel.SetResult(dataCtrl.GetValue()[:2])


class TurnRelaisAllOn(eg.ActionClass):
    description = "Turn ALL Relais On of USB-RLY08\n"
    name = "Turn All Relais On"

    def __call__(self):
        self.plugin.serial.write("\x64")
        return self.plugin.serial


class TurnRelais1On(eg.ActionClass):
    description = "Turn Relais 1 On of USB-RLY08\n"
    name = "Turn Relais 1 On"

    def __call__(self):
        self.plugin.serial.write("\x65")
        return self.plugin.serial


class TurnRelais2On(eg.ActionClass):
    description = "Turn Relais 2 On of USB-RLY08\n"
    name = "Turn Relais 2 On"

    def __call__(self):
        self.plugin.serial.write("\x66")
        return self.plugin.serial


class TurnRelais3On(eg.ActionClass):
    description = "Turn Relais 3 On of USB-RLY08\n"
    name = "Turn Relais 3 On"

    def __call__(self):
        self.plugin.serial.write("\x67")
        return self.plugin.serial


class TurnRelais4On(eg.ActionClass):
    description = "Turn Relais 4 On of USB-RLY08\n"
    name = "Turn Relais 4 On"

    def __call__(self):
        self.plugin.serial.write("\x68")
        return self.plugin.serial


class TurnRelais5On(eg.ActionClass):
    description = "Turn Relais 5 On of USB-RLY08\n"
    name = "Turn Relais 5 On"

    def __call__(self):
        self.plugin.serial.write("\x69")
        return self.plugin.serial


class TurnRelais6On(eg.ActionClass):
    description = "Turn Relais 6 On of USB-RLY08\n"
    name = "Turn Relais 6 On"

    def __call__(self):
        self.plugin.serial.write("\x6A")
        return self.plugin.serial


class TurnRelais7On(eg.ActionClass):
    description = "Turn Relais 7 On of USB-RLY08\n"
    name = "Turn Relais 7 On"

    def __call__(self):
        self.plugin.serial.write("\x6B")
        return self.plugin.serial


class TurnRelais8On(eg.ActionClass):
    description = "Turn Relais 8 On of USB-RLY08\n"
    name = "Turn Relais 8 On"

    def __call__(self):
        self.plugin.serial.write("\x6C")
        return self.plugin.serial


class TurnRelaisAllOff(eg.ActionClass):
    description = "Turn ALL Relais Off of USB-RLY08\n"
    name = "Turn All Relais Off"

    def __call__(self):
        self.plugin.serial.write("\x6E")
        return self.plugin.serial


class TurnRelais1Off(eg.ActionClass):
    description = "Turn Relais 1 Off of USB-RLY08\n"
    name = "Turn Relais 1 Off"

    def __call__(self):
        self.plugin.serial.write("\x6F")
        return self.plugin.serial


class TurnRelais2Off(eg.ActionClass):
    description = "Turn Relais 2 Off of USB-RLY08\n"
    name = "Turn Relais 2 Off"

    def __call__(self):
        self.plugin.serial.write("\x70")
        return self.plugin.serial


class TurnRelais3Off(eg.ActionClass):
    description = "Turn Relais 3 Off of USB-RLY08\n"
    name = "Turn Relais 3 Off"

    def __call__(self):
        self.plugin.serial.write("\x71")
        return self.plugin.serial


class TurnRelais4Off(eg.ActionClass):
    description = "Turn Relais 4 Off of USB-RLY08\n"
    name = "Turn Relais 4 Off"

    def __call__(self):
        self.plugin.serial.write("\x72")
        return self.plugin.serial


class TurnRelais5Off(eg.ActionClass):
    description = "Turn Relais 5 Off of USB-RLY08\n"
    name = "Turn Relais 5 Off"

    def __call__(self):
        self.plugin.serial.write("\x73")
        return self.plugin.serial


class TurnRelais6Off(eg.ActionClass):
    description = "Turn Relais 6 Off of USB-RLY08\n"
    name = "Turn Relais 6 Off"

    def __call__(self):
        self.plugin.serial.write("\x74")
        return self.plugin.serial


class TurnRelais7Off(eg.ActionClass):
    description = "Turn Relais 7 Off of USB-RLY08\n"
    name = "Turn Relais 7 Off"

    def __call__(self):
        self.plugin.serial.write("\x75")
        return self.plugin.serial


class TurnRelais8Off(eg.ActionClass):
    description = "Turn Relais 8 Off of USB-RLY08\n"
    name = "Turn Relais 8 Off"

    def __call__(self):
        self.plugin.serial.write("\x76")
        return self.plugin.serial
