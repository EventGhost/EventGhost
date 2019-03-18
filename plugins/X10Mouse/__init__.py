# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
#
# Large portions of this plugin were adapted from the maX10 software
# written by Colin Bonstead (http://max10.sourceforge.net)
#
#
# $LastChangedDate: 2011-06-07 01:05:06 -0500 (Mon, 07 Jun 2011) $
# $LastChangedBy: Catscradler $


import eg

eg.RegisterPlugin(
    name="X10 MouseRemote",
    guid='{BBDA2146-B0CA-4182-917E-47E524A76D2B}',
    author="Catscradler",
    version="1.0",
    kind="remote",
    canMultiLoad=True,
    description=(
        'Hardware plugin for the X10 MouseRemote '
        '<a href="http://kbase.x10.com/wiki/JR20A">'
        'JR20A/MK19A</a>, '
        'connected via the serial port '
        '<a href="http://kbase.x10.com/wiki/JR21A">'
        'JR21A</a> receiver.'
        '\n\n<p>'
        '<img src="mouseremote.png" alt="X10 MouseRemote" />'
    ),
    help=(
        'Before enabling this plugin go to the '
        'Windows Device Manager and disable the '
        'Microsoft Serial Mouse.'
    ),
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
        "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
        "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
        "YII="
    ),
)

import time

keyTable = {
    43: "PC",
    -85: "CD",
    -117: "Web",
    -53: "DVD",
    75: "Phone",

    15: "Power",
    2: "ChPlus",
    3: "ChMinus",
    6: "VolPlus",
    7: "VolMinus",
    5: "Mute",
    13: "Play",
    14: "Stop",
    28: "RW",
    29: "FF",
    78: "Pause",
    64: "Pad0",
    65: "Pad1",
    66: "Pad2",
    67: "Pad3",
    68: "Pad4",
    69: "Pad5",
    70: "Pad6",
    71: "Pad7",
    72: "Pad8",
    73: "Pad9",
    74: "Enter",
    93: "AB",
    92: "Disp",
    -1: "Rec",
    79: "Last",
    -109: "Select",
    109: "Guide",
    107: "Shift",
}


class X10Mouse(eg.RawReceiverPlugin):

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)

    def __start__(self, port, timeout):
        self.timeout = timeout
        self.serialThread = serialThread = eg.SerialThread()
        serialThread.Open(port, 1200, '7N1')
        serialThread.SetRts()
        serialThread.SetDtr()
        serialThread.Start()
        time.sleep(0.05)
        serialThread.Flush()
        serialThread.SetReadEventCallback(self.OnReceive)

    def __stop__(self):
        self.serialThread.Close()

    def OnReceive(self, serialThread):
        self.byteNum = 0
        self.comBytes = [None, None, None]
        data = serialThread.Read(1, self.timeout)
        reply = {'suffix': None, 'payload': None}
        lastEvent = None
        while (len(data) > 0):
            reply['suffix'] = self.Decode(reply, ord(data))
            if (reply['suffix'] is not None) and (reply != lastEvent):
                self.TriggerEnduringEvent(reply['suffix'], reply['payload'])
                lastEvent = reply.copy()
                reply['payload'] = None
            data = serialThread.Read(1, self.timeout)
        self.EndLastEvent()

    def Decode(self, reply, data):
        comBytes = self.comBytes

        # If sync bit not set, reset to first byte
        if (data & 64):
            self.byteNum = 0
        # Store byte and adjust byteNum
        comBytes[self.byteNum] = data
        self.byteNum += 1

        # If all bytes recieved
        if (self.byteNum == 3):
            # Extract x and y values
            x = ((comBytes[0] & 3) << 6) + comBytes[1]
            y = ((comBytes[0] & 12) << 4) + comBytes[2]
            # Adjust for sign
            if (x >= 128):
                x -= 256
            if (y >= 128):
                y -= 256
            # Extract button states
            if not comBytes[1] and not comBytes[2]:
                if comBytes[0] & 32:
                    return 'MouseButtonLeft'
                elif comBytes[0] & 16:
                    return 'MouseButtonRight'
                else:
                    return 'MouseButtonRelease'

            # Reset to first byte
            self.byteNum = 0

            # If special message, translate and dispatch
            if y == 127:
                if x in keyTable:
                    return keyTable[x]
            # If mouse message
            else:
                ax = abs(x)
                ay = abs(y)

                if ((ax == 0 or ax == 1 or ax == 2 or
                     ax == 4 or ax == 8 or ax == 16) and
                    (ay == 0 or ay == 1 or ay == 2 or
                     ay == 4 or ay == 8 or ay == 16)):
                    reply['payload'] = {'y': y, 'x': x}
                    # return "Degrees " + \
                    #    str((90 + math.degrees(math.atan2(y, x))) % 360) + \
                    #    ", Speed " + str(max(ax, ay))
                    return "MouseMove"
        return None

    def Configure(self, port=0, timeout=0.145):
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)
        timeoutCtrl = panel.SpinIntCtrl(int(timeout * 1000), min=1, max=1000)
        panel.AddLine('COM Port:', portCtrl)
        panel.AddLine(
            'Command repeat timeout (adjust upward '
            '\nif getting unwanted double button presses):',
            timeoutCtrl, '(default=145)'
        )
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                timeoutCtrl.GetValue() / 1000.0
            )
