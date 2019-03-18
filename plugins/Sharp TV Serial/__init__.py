# -*- coding: utf-8 -*-
#
# plugins/SharpTV/__init__.py
# 
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg

help = """\
Plugin to control Sharp Aqous LCD TV via RS-232."""

eg.RegisterPlugin(
    name="Sharp TV Serial",
    guid='{9379B23D-24C5-42AA-9C87-BBE6452A70D5}',
    author="kalia",
    version="0.1",
    kind="external",
    description="Control Sharp Aquos LCD TV via RS232",
    help=help,
    canMultiLoad=True,
    createMacrosOnAdd=True,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=6016",

)

import thread
import wx

cmdList = (

    ('Power Settings', None, None, None),
    ('', 'Power ON', 'POWR1   ', None),
    ('', 'Power OFF', 'POWR0   ', None),
    ('', 'Power Status', 'POWR?   ', None),

    ('Volume', None, None, None),
    ('', 'Mute Toggle', 'MUTE0   ', None),
    ('', 'Mute ON', 'MUTE1   ', None),
    ('', 'Mute OFF', 'MUTE2   ', None),
    ('', 'Get Volume Level', 'VOLM??  ', None),
    ('', 'Volume 5', 'VOLM05  ', None),
    ('', 'Volume 10', 'VOLM10  ', None),
    ('', 'Volume 15', 'VOLM15  ', None),
    ('', 'Volume 20', 'VOLM20  ', None),
    ('', 'Volume 25', 'VOLM25  ', None),
    ('', 'Volume 30', 'VOLM30  ', None),
    ('', 'Volume 35', 'VOLM35  ', None),
    ('', 'Volume 40', 'VOLM40  ', None),
    ('', 'Volume 45', 'VOLM45  ', None),
    ('', 'Volume 50', 'VOLM50  ', None),
    ('', 'Volume 55', 'VOLM55  ', None),
    ('', 'Volume 60', 'VOLM60  ', None),
    ('Set Volume Level (0-60)', 'Volume', 'VOLM', '0-60'),

    ('Input', None, None, None),
    ('', 'TV', 'ITVD0   ', None),
    ('', 'Input 1', 'IAVD1   ', None),
    ('', 'Input 2', 'IAVD2   ', None),
    ('', 'Input 3', 'IAVD3   ', None),
    ('', 'Input 4', 'IAVD4   ', None),
    ('', 'Input 5', 'IAVD5   ', None),
    ('', 'Input 6', 'IAVD6   ', None),
    ('', 'Input 7', 'IAVD7   ', None),
    ('', 'Input 8', 'IAVD8   ', None),
    ('', 'Input 9', 'IAVD9   ', None),

    ('View Mode', None, None, None),
    ('', 'S.Stretch [AV]', 'WIDE1   ', None),
    ('', 'Side Bar [AV]', 'WIDE2   ', None),
    ('', 'Zoom [AV]', 'WIDE3   ', None),
    ('', 'Stretch [AV]', 'WIDE4   ', None),
    ('', 'Normal [PC]', 'WIDE5   ', None),
    ('', 'Zoom [PC]', 'WIDE6   ', None),
    ('', 'Stretch [PC]', 'WIDE7   ', None),
    ('', 'Dot by Dot [PC][AV]', 'WIDE8   ', None),
    ('', 'Full Screen [AV]', 'WIDE9   ', None),

    ('Sleep Timer', None, None, None),
    ('', 'Off Timer', 'OFTM0   ', None),
    ('', 'Off Timer 30 Min', 'OFTM1   ', None),
    ('', 'Off Timer 60 Min', 'OFTM2   ', None),
    ('', 'Off Timer 90 Min', 'OFTM3   ', None),
    ('', 'Off Timer 120 Min', 'OFTM4   ', None),

    ('Audio', None, None, None),
    ('', 'Surround Toggle', 'ACSU0   ', None),
    ('', 'Surroung On', 'ACSU1   ', None),
    ('', 'Surround Off', 'ACSU2   ', None),
    ('', 'Closed Caption', 'CLCP0   ', None),
    ('', 'Audio Selection', 'ACHA0   ', None),

    ('Channel', None, None, None),
    ('', 'Channel Up', 'CHUP1   ', None),
    ('', 'Channel Down', 'CHDW1   ', None),
    ('Set OTA Channel (10-9999)', 'Set OTA Channel', 'DA2P', '10-9999'),
    ('', 'Closed Caption', 'CLCP0   ', None),
    ('', 'Audio Selection', 'ACHA0   ', None),

    (None, None, None, None),

)


class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        print self.cmd
        self.plugin.serial.write(self.cmd + chr(13))
        return self.plugin.readertext


class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):

        # Fix length of Volume change command
        if self.cmd == "VOLM":
            if len(data) == 1:
                data = "0" + data + "  "
            else:
                data = data + "  "

        # Fix lenght of Over the Air (OTA) channel change command
        if self.cmd == "DA2P":
            if len(data) == 2:
                data = "0" + data + " "
            elif len(data) == 3:
                data = data + " "
            else:
                data = data

        #        print self.cmd+data+chr(13)

        self.plugin.serial.write(str(self.cmd + data + chr(13)))
        return self.plugin.readertext


class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        # Change the length of RAW command
        while len(data) <> 8:
            data += " "

        self.plugin.serial.write(str(data.upper() + chr(13)))
        return self.plugin.readertext


class SharpTV(eg.PluginClass):

    def __init__(self):
        self.serial = None
        self.readerkiller = False
        self.readertext = ""
        group = topGroup = self

        for cmd_text, cmd_name, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_name is not None:
                line = cmd_name.replace(' ', '')
            #                print line
            if cmd_name != "":
                test = str(cmd_name) + " " + str(cmd_text)
            if cmd_name == "":
                test = str(cmd_name)
            if cmd_name is None:
                # New subgroup, or back up
                if cmd_text is None:
                    group = topGroup
                else:
                    group = topGroup.AddGroup(cmd_text)
            elif cmd_rangespec is not None:
                # Command with argument
                actionName, paramDescr = cmd_text.split("(")
                actionName = actionName.strip()
                paramDescr = paramDescr[:-1]
                minValue, maxValue = cmd_rangespec.split("-")

                class Action(ValueAction):
                    name = actionName
                    cmd = cmd_cmd
                    parameterDescription = "Value: (%s)" % paramDescr

                Action.__name__ = cmd_name
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = str(cmd_name)
                    description = test
                    cmd = cmd_cmd

                Action.__name__ = line
                group.AddAction(Action)

        group.AddAction(Raw)

    # Serial port reader
    def reader(self):
        line = ""
        while self.readerkiller is False:
            ch = self.serial.read()
            if ch != '\r':
                #            print ch
                line += str(ch)
            #            print line
            else:
                #            print line
                self.readertext = line
                line = ""
        self.readerkiller = None

    def __start__(self, port):
        try:
            self.serial = eg.SerialPort(port)
        except:
            raise eg.Exception("Can't open serial port.")
        self.serial.baudrate = 9600
        self.serial.timeout = 30.0
        self.serial.setDTR(1)
        self.serial.setRTS(1)
        self.readerkiller = False
        thread.start_new_thread(self.reader, ())
        print "Sharp LCD TV Serial Control Plug-in Started!"

    def __stop__(self):
        self.readerkiller = True
        while self.readerkiller is not None:
            wx.MilliSleep(100)
        if self.serial is not None:
            self.serial.close()
            self.serial = None
            print "Sharp LCD TV Serial Control Plug-in Stopped!"

    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())
