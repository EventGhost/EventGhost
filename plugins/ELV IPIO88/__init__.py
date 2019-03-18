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



# Version 0.1.6: Configurable retry cycle added
# Verison 0.2.0: variable printname added,  fixed retry issue, multiload added,
#                CreateMacrosOnAdd added
# Version 0.2.1: payload-tag added
# Version 0.2.2: Global variables deleted with the help of KGSchlosser

import eg


eg.RegisterPlugin(
    name="ELV IPIO 88",
    guid='{95B2198A-E539-4BD4-962E-0C90C818B20C}',
    author="Dieter Brillert",
    version="0.2.2",
    kind="external",
    canMultiLoad=True,
    createMacrosOnAdd=True,
    description=(
        "Very basic plugin to read the input states and set the output states "
        "of the ELV-IPIO88 Device. The plugin interacts with the web "
        "interface of the device. Please make sure that password check is "
        "DISABLED. The device has its own capabilities to combine input and "
        "output channels logicaly. Please be aware of that!"
    )

)

import urllib2 as urllib # NOQA
from threading import Event, Thread # NOQA


class IPIO88(eg.PluginBase):
    def __init__(self):
        self.stopThreadEvent = Event()
        self.thread = None
        self.in_status = ["Null"] * 9
        self.out_status = ["Null"] * 9

        self.AddAction(GetAllInputStates)
        self.AddAction(GetInputState)
        self.AddAction(GetAllOutputStates)
        self.AddAction(GetOutputState)
        self.AddAction(SwitchAllOutputStatesOn)
        self.AddAction(SwitchAllOutputStatesOff)
        self.AddAction(SwitchOutputStateOn)
        self.AddAction(SwitchOutputStateOff)
        self.AddAction(DeleteAllinternalIOBindings)

    def __start__(self, ip, refresh, retry, payloadtag):
        while self.stopThreadEvent.isSet():
            pass

        self.payloadtag = payloadtag
        self.ip = ip
        self.retry = retry
        self.refresh = refresh

        self.thread = Thread(target=self.ThreadLoop)
        self.thread.start()

    def __stop__(self):

        if self.thread is not None:
            self.stopThreadEvent.set()
            self.thread.join(3)
            self.threead = None

    def PrintNotice(self, message):
        eg.PrintNotice(self.payloadtag + message)

    def Print(self, message):
        eg.Print(self.payloadtag + message)

    def ThreadLoop(self):

        url = "http://%s/ipio.cgi" % self.ip

        # print url

        suppress = True
        connect = None
        retrycount = 0

        self.Print(": Start reading from IP " + self.ip)

        try:
            refreshtime = abs(float(self.refresh))
            self.Print(": Refresh cycle time: %s s" % refreshtime)

        except ValueError:
            refreshtime = 2
            self.PrintNotice(
                ": Invalid refresh cycle time configured. -> Set to 2 s."
            )

        try:
            retryNr = abs(int(self.retry))
            self.Print(": Retry cycles: %s" % retryNr)


        except ValueError:
            retryNr = 0
            self.Print(
                ": Invalid number of retry cycles configured. -> Set to 0"
            )

        while not self.stopThreadEvent.isSet():

            try:
                page = str(urllib.urlopen(url).read())
            except IOError:
                # print connect
                # print "try+"+str(retrycount)

                if retrycount < retryNr:
                    retrycount += 1
                    self.Print(": Try to connect to device ...")
                else:
                    if connect is not False:
                        self.PrintNotice(": Can't connect to device")
                        self.TriggerEvent("DeviceIO-Error")

                    connect = False

                self.stopThreadEvent.wait(refreshtime)

            else:
                # print connect
                # print "reading"
                if retrycount > 0:
                    self.Print(":... success, reconnected.")
                retrycount = 0

                if not connect:
                    self.TriggerEvent("DeviceConnected")
                connect = True

                for r in range(1, 9):
                    string = 'input name="in%d" checked="checked"' % r
                    check = page.find(string)

                    if check == -1:
                        if self.in_status[r] <> "off":
                            self.in_status[r] = "off"
                            if not suppress:
                                self.TriggerEvent(
                                    "Input%d.Off" % r,
                                    payload="%s/In/%d/0" % (self.payloadtag, r)
                                )
                    else:
                        if self.in_status[r] <> "on":
                            self.in_status[r] = "on"
                            if not suppress:
                                self.TriggerEvent(
                                    "Input%d.On" % r,
                                    payload="%s/In/%d/1" % (self.payloadtag, r)
                                )

                    string = 'input name="out%d" checked="checked"' % r
                    check = page.find(string)

                    if check == -1:
                        if self.out_status[r] <> "off":
                            self.out_status[r] = "off"

                            if not suppress:
                                self.TriggerEvent(
                                    "Output%d.Off" % r,
                                    payload=(
                                        "%s/Out/%d/0" % (self.payloadtag, r)
                                    )
                                )
                    else:
                        if self.out_status[r] <> "on":
                            self.out_status[r] = "on"

                            if not suppress:
                                self.TriggerEvent(
                                    "Output%d.On" % r,
                                    payload=(
                                        "%s/Out/%d/1" % (self.payloadtag, r)
                                    )
                                )

                suppress = False

                self.stopThreadEvent.wait(refreshtime)

        self.Print(": Stopped reading from " + self.ip)
        self.stopThreadEvent.clear()

    def Configure(
        self,
        ip="192.168.100.1",
        refresh="2",
        retry="0",
        payloadtag="IPIO88"
    ):
        helpString = (
            "Please configure the IP adress of the IPIO88 device you want to "
            "control.\n\n"
            "Format is xxx.xxx.xxx.xxx e.g: 192.168.100.1"
        )

        panel = eg.ConfigPanel(self)
        helpLabel = panel.StaticText(helpString)
        ipEdit = panel.TextCtrl(ip)
        refreshEdit = panel.TextCtrl(refresh)
        retryEdit = panel.TextCtrl(retry)
        payloadtagEdit = panel.TextCtrl(payloadtag)

        panel.AddLine(helpLabel)
        panel.AddLine(
            "Device IP adress: ",
            ipEdit
        )
        panel.AddLine(
            "Refresh Cycle Time (seconds): ",
            refreshEdit
        )
        panel.AddLine(
            "Number of retry cycles before disconnect event is fired: ",
            retryEdit
        )
        panel.AddLine(
            "Payload-tag to identify the device in event payload: ",
            payloadtagEdit
        )

        while panel.Affirmed():
            panel.SetResult(
                ipEdit.GetValue(),
                refreshEdit.GetValue(),
                retryEdit.GetValue(),
                payloadtagEdit.GetValue()
            )


class GetAllInputStates(eg.ActionBase):
    name = "Get all Input States"

    def __call__(self):
        for i in range(9):
            self.plugin.in_status[i] = "?"


class GetInputState(eg.ActionBase):
    name = "Get single Input State "

    def __call__(self, InChannel):

        try:
            InChannelRead = int(InChannel)

        except ValueError:
            self.plugin.Print(": Invalid Channel Number!")

        else:

            if 1 <= InChannelRead <= 8:
                self.plugin.Print(
                    ":Reading Input channel %d ..." % InChannelRead
                )

                self.plugin.in_status[InChannelRead] = "?"

            else:
                self.plugin.PrintNotice(": Invalid Channel Number!")

    def Configure(self, InChannel="1"):
        helpString = (
            "Please configure Input Channel you want to read.\n\n"
            "Channel number between 1 and 8 is allowed."
        )

        panel = eg.ConfigPanel(self)
        helpLabel = panel.StaticText(helpString)
        inStringEdit = panel.TextCtrl(InChannel)
        panel.AddLine(helpLabel)
        panel.AddLine("Channel number: ", inStringEdit)

        while panel.Affirmed():
            panel.SetResult(inStringEdit.GetValue())


class GetAllOutputStates(eg.ActionBase):
    name = "Get all Output States"

    def __call__(self):
        for i in range(9):
            self.plugin.out_status[i] = "?"


class GetOutputState(eg.ActionBase):
    name = "Get single Output State "

    def __call__(self, OutChannel):

        OutChannel = str(OutChannel)

        if not OutChannel.isdigit():
            self.plugin.PrintNotice(": Invalid Channel Number!")
            return

        OutChannelRead = int(OutChannel)

        if 1 <= OutChannelRead <= 8:
            self.plugin.Print(
                ": Reading Output channel Nr: %d ..." % OutChannelRead
            )

            self.plugin.out_status[OutChannelRead] = "?"

        else:
            self.plugin.PrintNotice(": Invalid Channel Number!")

    def Configure(self, OutChannel="1"):
        helpString = (
            "Please configure Output channel you want to read.\n\n"
            "Channel number between 1 and 8 is allowed."
        )

        panel = eg.ConfigPanel(self)
        helpLabel = panel.StaticText(helpString)
        inStringEdit = panel.TextCtrl(OutChannel)
        panel.AddLine(helpLabel)
        panel.AddLine("Channel number: ", inStringEdit)

        while panel.Affirmed():
            panel.SetResult(inStringEdit.GetValue())


class SwitchAllOutputStatesOn(eg.ActionBase):
    name = "Switch all Output States ON"

    def __call__(self):
        command = (
            "http://%s/ipio.cgi?"
            "pg=main&"
            "out1=on&"
            "out2=on&"
            "out3=on&"
            "out4=on&"
            "out5=on&"
            "out6=on&"
            "out7=on&"
            "out8=on&"
            "end=main" %
            self.plugin.ip
        )
        urllib.urlopen(command)


class SwitchAllOutputStatesOff(eg.ActionBase):
    name = "Switch all Output States OFF"

    def __call__(self):
        command = (
            "http://%s/ipio.cgi?"
            "pg=main&"
            "out1=off&"
            "out2=off&"
            "out3=off&"
            "out4=off&"
            "out5=off&"
            "out6=off&"
            "out7=off&"
            "out8=off&"
            "end=main" %
            self.plugin.ip
        )

        urllib.urlopen(command)


class SwitchOutputStateOn(eg.ActionBase):
    name = "Switch single Output State ON "

    def __call__(self, OutChannel):

        OutChannel = str(OutChannel)

        if not OutChannel.isdigit():
            self.plugin.Print(": Invalid Channel Number!")
            return

        OutChannelRead = int(OutChannel)

        if 1 <= OutChannelRead <= 8:
            self.plugin.Print(
                ": Switch Output channel %d On ..." % OutChannelRead
            )

            command = "http://%s/ipio.cgi?pg=main" % self.plugin.ip

            for r in range(1, 9):
                if r == OutChannelRead:
                    command += "&out%d=on" % r
                else:
                    command += "&out%d=%s" % (r, self.plugin.out_status[r])

            command += "&end=main"

            urllib.urlopen(command)

        else:
            self.plugin.PrintNotice(": Invalid Channel Number!")

    def Configure(self, OutChannel="1"):
        helpString = (
            "Please configure Output channel you want to switch ON.\n\n"
            "Channel number between 1 and 8 is allowed."
        )

        panel = eg.ConfigPanel(self)
        helpLabel = panel.StaticText(helpString)
        inStringEdit = panel.TextCtrl(OutChannel)
        panel.AddLine(helpLabel)
        panel.AddLine("Channel number: ", inStringEdit)

        while panel.Affirmed():
            panel.SetResult(inStringEdit.GetValue())


class SwitchOutputStateOff(eg.ActionBase):
    name = "Switch single Output State OFF"

    def __call__(self, OutChannel):

        OutChannel = str(OutChannel)
        if not OutChannel.isdigit():
            self.plugin.PrintNotice(": Invalid Channel Number!")
            return

        OutChannelRead = int(OutChannel)

        if 1 <= OutChannelRead <= 8:
            self.plugin.Print(
                ": Switch Output channel %d OFF ..." % OutChannelRead
            )
            command = "http://%s/ipio.cgi?pg=main" % self.plugin.ip

            for r in range(1, 9):
                command += "&out%d=" % r

                if r == OutChannelRead:
                    command += 'off'
                else:
                    command += self.plugin.out_status[r]

            command = command + "&end=main"

            urllib.urlopen(command)

        else:
            self.plugin.PrintNotice(": Invalid Channel Number!")

    def Configure(self, OutChannel="1"):
        helpString = (
            "Please configure Output channel you want to switch OFF.\n\n"
            "Channel number between 1 and 8 is allowed."
        )

        panel = eg.ConfigPanel(self)
        helpLabel = panel.StaticText(helpString)
        inStringEdit = panel.TextCtrl(OutChannel)
        panel.AddLine(helpLabel)
        panel.AddLine("Channel number: ", inStringEdit)

        while panel.Affirmed():
            panel.SetResult(inStringEdit.GetValue())


class DeleteAllinternalIOBindings(eg.ActionBase):
    name = "Delete all internal device I/O bindings"

    def __call__(self):
        command = (
            "http://%s/ioports.cgi?"
            "pg=io&"
            "1A=fallende+Flanke&"
            "1P=0&"
            "2A=positive+Logik&"
            "2P=0&"
            "3A=positive+Logik&"
            "3P=0&"
            "4A=positive+Logik&"
            "4P=0&"
            "5A=positive+Logik&"
            "5P=0&"
            "6A=positive+Logik&"
            "6P=0&"
            "7A=positive+Logik&"
            "7P=0&"
            "8A=positive+Logik&"
            "8P=0&"
            "set=%%DCbernehmen&"
            "end=io" %
            self.plugin.ip
        )

        urllib.urlopen(command)

        self.plugin.Print(": Bindings deleted")

    def Configure(self):
        helpString = (
            "WARNING! Excecution of this action deletes all internal\n"
            "In/Out bindings set in the device internally. \n\n"
            "This CAN NOT BE UNDONE!\n\n"
            "Useful if you want to control the In -> Out behavior with EG "
            "soley."
        )

        panel = eg.ConfigPanel(self)
        helpLabel = panel.StaticText(helpString)

        panel.AddLine(helpLabel)

        while panel.Affirmed():
            panel.SetResult()
