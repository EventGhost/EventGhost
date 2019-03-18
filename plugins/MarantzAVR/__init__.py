# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

import eg
from actions import CreateActions

DEBUG = True

eg.RegisterPlugin(
    name="Marantz AVR Serial/TCP/Forwarding",
    author="K",
    original_authors="Sam West, Daniel Eriksson <daniel@clearminds.se>",
    version="0.5b",
    kind="external",
    description=(
        "******************THIS PLUGIN IS UNDER DEVELOPMENT*******************"
        "\n\n\n"
        "Controls Marantz AVR's over an IP or Serial connection. Due to the "
        "nature of the Marantz AVR's you are only able to make one connection "
        "at a time to the AVR. This plugin eliminates that problem by acting "
        "as a forwarding server.\n"
        " It functions like this for both Serial and IP connections. The "
        "forwarding is able to handle an unlimited number of connections "
        "(computer quality would be the limiting factor). The forwarding sends"
        " and recieves all events responses and commands from the AVR and to "
        "the AVR from the client.\n\n"
        "Every Command I could get my hands on for the 2011 and newer Marantz"
        "AVR's is in this plugin. If by chance one is missing please notify "
        "me.\n\n"
        "Currently provides convenience methods for setting absolute volume, "
        "and sending arbitrary text commands.\n\n"
        "See included MarantzVolumeSync.xml for example usage.\n"
        "<p>See <a href=http://us.marantz.com/DocumentMaster/US/Marantz_AV_SR_"
        "NR_PROTOCOL_V01.xls>here</a> for a full list of supported commands. "
        "<p>Supported Marantz models include: AV7005, SR7005, SR6006, SR6005, "
        "SR5006, NR1602 (and probably others with an ethernet connection). "
        "<p>Might also support (untested) Denon models: AVR-3808, AVC-3808, "
        "command list <a href=http://usa.denon.com/US/Downloads/Pages/Instruct"
        "ionManual.aspx?FileName=DocumentMaster/US/AVR-3808CISerialProtocol_Ve"
        "r5.2.0a.pdf>here</a>."
    ),
    guid='{A263A677-9DD9-4933-BB52-00D2C5AAB013}',
    createMacrosOnAdd=True,
    canMultiLoad=True
)

import threading

from telnetclient import TelnetClient
from telnetserver import TelnetServer
from serial import Serial
from events import GetEvent, GetEventList


# Define commands
# (name, title, description (same as title if None), command)


def debug(message):
    if DEBUG:
        from os.path import join
        from time import strftime

        with open(join(eg.configDir, 'MarantzDebugLog.txt'), 'a') as f:
            f.write(strftime("%H:%M:%S  ") + message + '\n')


class SetVolumeAbsolute(eg.ActionBase):
    name = 'Set absolute volume'
    description = 'Sets the absolute volume'

    def __call__(self, volume):
        return self.plugin.setVolumeAbsolute(volume)

    def GetLabel(self, volume):
        return "Set Absolute Volume to %d" % volume

    def Configure(self, volume=25):
        panel = eg.ConfigPanel(self)

        valueCtrl = eg.SmartSpinIntCtrl(panel, -1, 0, min=0)
        panel.AddLine("Set absolute volume to", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class SendCommandText(eg.ActionBase):
    """"
    Sends a raw text command to the receiver.
    See http://us.marantz.com/DocumentMaster/US/Marantz_AV_SR_NR_PROTOCOL_V01.xls
    for details
    """
    name = 'Send Text Command'
    description = 'Send a manual command'

    def __call__(self, cmd):
        print 'Sending command: '+cmd
        return self.plugin.sendCommand(str(cmd))

    def GetLabel(self, cmd):
        return "Send Command '%s'" % cmd

    def Configure(self, volume=25):
        panel = eg.ConfigPanel(self)

        cmdCtrl = wx.TextCtrl(panel, -1, '')
        desc = wx.StaticText(
            panel,
            -1,
            (
                'See http://us.marantz.com/DocumentMaster/US'
                '/Marantz_AV_SR_NR_PROTOCOL_V01.xls for a list of commands'
            )
        )

        panel.AddLine(desc)
        panel.AddLine("Send Command: ", cmdCtrl)
        while panel.Affirmed():
            panel.SetResult(cmdCtrl.GetValue())


class Marantz(eg.PluginBase):

    def __init__(self):
        self.info.eventList = GetEventList()
        self.server = None
        self.client = None
        self.timeout = None
        self.maxDb = 18
        self.disabled = True

        CreateActions(self)

        group = self.AddGroup('Volume')
        group.AddAction(SetVolumeAbsolute)
        self.AddAction(SendCommandText)

    def __start__(
        self,
        host="192.168.66.60",
        port=23,
        timeout=2,
        maxDb=12,
        prefix='MarantzTCPPlugin',
        server=False,
        serialPort=None
    ):

        self.maxDb = maxDb
        self.info.eventPrefix = prefix

        while self.server:
            pass

        while self.client:
            pass

        if serialPort is None:
            self.client = TelnetClient(self, host, port, timeout, debug)
        else:
            self.client = Serial(self, serialPort, timeout)

        self.client.Start()

        if server:
            self.server = TelnetServer(self, timeout, debug)
            self.server.Start()
        else:
            self.server = None

    def __stop__(self):
        if self.server:
            self.server.Stop()

        if self.client:
            self.client.Stop()

    def __close__(self):
        pass

    def roundTo(self, n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int(n / precision + correction) * precision

    def roundToHalf(self, n):
        """
        Rounds n to nearest 0.5
        """
        return self.roundTo(n, 0.5)

    def volumePercentToMV(self, perc):
        """
        Converts a percentage volume (0,100) to a MV code to set the receiver
        to that volume
        """
        if 100.0 < perc < 0.0:
            eg.PrintNotice('Percentage must be between 0.0 and 100.0')
            return None

        maxMV = self.maxDb + 80
        mvNum = self.roundToHalf((perc / 100.0) * maxMV)
        eg.PrintNotice(
            'Setting receiver volume to {0}dB '.format(mvNum - 80)
        )

        if mvNum < 10:
            cmd = 'MV' + ('%2.1f' % mvNum)
            cmd = cmd.replace('MV', 'MV0')
        else:
            cmd = 'MV' + str(mvNum).replace('.5', '5')
        cmd = cmd.replace('.', '')

        if cmd.endswith('0'):
            cmd = cmd[0:4]

        if len(cmd) < 4:
            cmd += '0'

        return cmd

    def ProcessData(self, data):

        if 31 > ord(data[0]):
            data = data[1:]

        if self.server:
            threading.Thread(target=self.server.Send, args=(data,)).start()

        suffix, payload = GetEvent(data.strip())

        debug('<--- %r' % data.strip())
        debug('---- %r  %r' % (suffix, payload))

        if suffix:
            self.TriggerEvent(suffix=suffix, payload=payload)

    def sendCommand(self, cmd):
        debug('---> %r' % cmd)
        if self.client:
            self.client.Send(cmd + '\r')

    def EchoCommand(self, command):
        self.sendCommand(command.strip())

    def setVolumeAbsolute(self, percentage):
        cmd = self.volumePercentToMV(percentage)
        eg.PrintNotice('(' + str(percentage) + '%)command=' + cmd)
        self.sendCommand(cmd)

    def Configure(
        self,
        host="192.168.66.60",
        port=23,
        timeout=2,
        maxDb=18,
        prefix='MarantzTCPPlugin',
        server=False,
        serialPort=None
    ):

        if serialPort is not None:
            sPort = serialPort
        else:
            sPort = 0

        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())

        hostCtrl = wx.TextCtrl(panel, -1, host)
        rportCtrl = eg.SpinIntCtrl(panel, -1, port, max=65535)
        timeoutCtrl = eg.SpinIntCtrl(panel, -1, timeout, min=1, max=10)
        maxDbCtrl = eg.SpinIntCtrl(panel, -1, maxDb, min=-80, max=18)
        serverCtrl = wx.CheckBox(panel, -1)
        prefixCtrl = wx.TextCtrl(panel, -1, prefix)
        useSerialCtrl = wx.CheckBox(panel, -1, '')
        serialCtrl = eg.SerialPortChoice(panel, value=sPort)
        useSerialCtrl.SetValue(serialPort is not None)
        serverCtrl.SetValue(server)

        panel.AddLine("Marantz Receiver IP Address:", hostCtrl)
        panel.AddLine("Marantz Receiver TCP Port:  ", rportCtrl)
        panel.AddLine("Send Timeout (s):           ", timeoutCtrl)
        panel.AddLine("Max Allowed Volume (dB):    ", maxDbCtrl)
        panel.AddLine("Echo Server:                ", serverCtrl)
        panel.AddLine("Event Prefix:               ", prefixCtrl)
        panel.AddLine("Use Serial Connection:      ", useSerialCtrl)
        panel.AddLine("Serial Port:                ", serialCtrl)

        def OnCheck(evt):
            flag = useSerialCtrl.GetValue()
            serialCtrl.Enable(flag)
            hostCtrl.Enable(not flag)
            rportCtrl.Enable(not flag)
            if evt is not None:
                evt.Skip()

        useSerialCtrl.Bind(wx.EVT_CHECKBOX, OnCheck)
        OnCheck(None)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                rportCtrl.GetValue(),
                timeoutCtrl.GetValue(),
                maxDbCtrl.GetValue(),
                prefixCtrl.GetValue(),
                serverCtrl.GetValue(),
                serialCtrl.GetValue() if useSerialCtrl.GetValue() else None
            )
