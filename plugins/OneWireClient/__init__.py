# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2013 Walter Kraembring <krambriw>.
#
###############################################################################
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
#
##############################################################################
#
# Acknowledgement: Ideas from ownet package by Peter Kropf 
#
##############################################################################
# Revision history:
#
# 2013-12-18  Improved response to read/write operations (added path and
#             attribute)
#             Improved initial reading of configurations
# 2013-07-20  Further improved handling of polling thread during the
#             configuration of read actions.
# 2013-07-16  Improved handling of polling during the configuration of read
#             actions.
# 2013-07-12  Minor adjustment to the socket read and write functions.
#             Adjusted handling of polling while configuring read actions as
#             well as when running the action to clear the sensor repository.
#             Fixed a bug in clearing the sensors status repository and in
#             managing persistent data (did not update correctly).
# 2013-07-10  Added comms monitoring with OneWire server
#             Made a minor code improvement in reading responses 
# 2013-07-07  Added settings for individual polling interval of attributes
#             Removed global polling interval setting for plugin
# 2013-07-06  Added a time delay between sensor readings
#             Added error control when building up sensor list
# 2013-06-30  OneWire Client plugin
##############################################################################

import eg

eg.RegisterPlugin(
    name="OneWireClient",
    author="krambriw",
    version="1.0.8",
    kind="other",
    canMultiLoad=True,
    url="http://www.eventghost.org/forum",
    description="Connects to a One-Wire owserver on the network",
    guid="{18635A45-B8CA-4BEC-A851-ED203873FF6C}",
    help="""
        <center><img src="OneWire.png" /></center>
    """
)

import socket
import struct
import time
import wx
from threading import Event, Thread


class Text:
    ow_host = "One-Wire owserver ip or network name:"
    ow_port = "One-Wire owserver port:"
    ow_poll = "Check box if selected read attributes shall be polled"
    ow_poll_interval = "Select and set the polling interval (seconds)"
    message_1 = "One-Wire Client started..."
    message_2 = "One-Wire Client stopped..."
    threadStopped = "Polling thread is stopped..."
    threadStarted = "Polling thread is started..."
    comms_lost = "Communication with OneWire server is lost"
    comms_back = "Communication with OneWire server is restored"
    textBoxName = "Enter a descriptive name for the action"
    textBoxPath = "Select the sensor path to be used"
    textBoxAttribute = "Select the sensor attribute to be read"
    textBoxAttributeW = "Select the sensor attribute"
    textBoxValue = "Type the sensor attribute value to be written"
    textBoxPoll = "Check box if attribute shall be included in the polling"
    retry_txt = "Retry nbr: "
    exception_txt = "An error occurred while polling attribute"


class CurrentStateData(eg.PersistentData):
    sensors_status = {}


class OWMsg():
    # owserver api message types
    error = 0
    nop = 1
    read = 2
    write = 3
    dir = 4
    size = 5
    presence = 6


class OneWireClient(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddAction(ReadAttribute)
        self.AddAction(WriteAttribute)
        self.AddAction(ClearSensorsStatus)

    def __start__(
        self,
        ow_server,
        ow_port,
        b_poll
    ):
        self.sensors_status = CurrentStateData.sensors_status
        self.ow_server = ow_server
        self.ow_port = ow_port
        self.b_poll = b_poll
        self.started = True
        self.thread_up = False
        print self.text.message_1

        # Building up my sensor and attribute repository
        self.my_sensors = []
        self.my_sensors_attributes = {}
        devices = self.D_dir('/')

        for i in devices:
            if i == '/bus.0':
                break
            self.my_sensors.append(i)

        for j in self.my_sensors:
            m = []
            n = self.D_dir(j)
            for k in n:
                try:
                    m.append(k.split('/')[2])
                except:
                    eg.PrintError('Failed to add: ' + str(k))
            self.my_sensors_attributes[j] = m

        self.finished = Event()
        self.pollingThread = Thread(
            target=self.PollingThread,
            name="Polling_Thread"
        )
        if not self.finished.isSet():
            self.pollingThread.start()

    def __stop__(self):
        self.finished.set()
        print self.text.message_2
        self.started = False

    def __close__(self):
        pass

    def T_toNumber(self, str):
        stripped = str.strip()
        if stripped.isdigit():
            return int(stripped)
        if stripped.replace('.', '').isdigit():
            return float(stripped)
        return str

    def U_unpack(self, msg):
        if len(msg) is 24:
            val = struct.unpack('iiiiii', msg)
            version = socket.ntohl(val[0])
            try:
                payload_len = socket.ntohl(val[1])
            except OverflowError:
                payload_len = 0
            try:
                ret_value = socket.ntohl(val[2])
            except OverflowError:
                ret_value = 0
            format_flags = socket.ntohl(val[3])
            data_len = socket.ntohl(val[4])
            offset = socket.ntohl(val[5])
            return ret_value, payload_len, data_len

    def P_pack(self, function, payload_len, data_len):
        return struct.pack('iiiiii',
                           socket.htonl(0),
                           socket.htonl(payload_len),
                           socket.htonl(function),
                           socket.htonl(258),
                           socket.htonl(data_len),
                           socket.htonl(0)
                           )

    def D_dir(self, path):
        fields = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ow_server, self.ow_port))
            smsg = self.P_pack(OWMsg.dir, len(path) + 1, 0)
            s.sendall(smsg)
            s.sendall(path + '\x00')
            while 1:
                data = s.recv(24)
                if len(data) is not 24:
                    break
                ret, payload_len, data_len = self.U_unpack(data)
                if payload_len:
                    data = s.recv(payload_len)
                    fields.append(data[:data_len])
                else:
                    break
                time.sleep(0.05)
            s.close()
            del s
            return fields
        except:
            print "Failed to connect"
            del s
            return fields

    def R_read(self, path):
        rtn = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ow_server, self.ow_port))
            smsg = self.P_pack(OWMsg.read, len(path) + 1, 8192)
            s.sendall(smsg)
            s.sendall(path + '\x00')
            while 1:
                data = s.recv(24)
                if len(data) is not 24:
                    break
                ret, payload_len, data_len = self.U_unpack(data)
                if payload_len:
                    data = s.recv(payload_len)
                    rtn = self.T_toNumber(data[:data_len])
                    break
            s.close()
            del s
            return rtn
        except:
            del s
            return rtn

    def W_write(self, path, value):
        ret = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ow_server, self.ow_port))
            value = str(value)
            smsg = self.P_pack(
                OWMsg.write,
                len(path) + 1 + len(value) + 1,
                len(value) + 1
            )
            s.sendall(smsg)
            s.sendall(path + '\x00' + value + '\x00')
            data = s.recv(24)
            ret, payload_len, data_len = self.U_unpack(data)
            s.close()
            del s
            return ret
        except:
            del s
            return ret

    def commsLost(self, myArgument):
        eg.TriggerEvent(repr(myArgument))

    def commsBack(self, myArgument):
        eg.TriggerEvent(repr(myArgument))

    def commsMonitor(self, monitored, decoded, timeout):
        try:
            eg.scheduler.CancelTask(monitored)
        except:
            if decoded <> None:
                self.commsBack(
                    self.text.comms_back
                )
        monitored = eg.scheduler.AddTask(
            timeout,
            self.commsLost,
            self.text.comms_lost
        )
        return monitored

    def PollingThread(self):
        monitored = None
        print self.text.threadStarted
        while not self.finished.isSet():
            self.thread_up = True
            # Code to read defined attributes....
            if self.b_poll:
                for i in self.sensors_status:
                    t = time.time()
                    delta_t = t - self.sensors_status[i][2]
                    if delta_t >= self.sensors_status[i][1]:
                        self.sensors_status[i][2] = t
                        rsp = self.R_read(i)
                        # print 'rsp', rsp
                        if rsp <> None:
                            monitored = self.commsMonitor(
                                monitored,
                                rsp,
                                300.0
                            )
                        if rsp <> self.sensors_status[i][0]:
                            self.sensors_status[i][0] = rsp
                            if rsp <> None:
                                self.TriggerEvent(
                                    i,
                                    payload=rsp
                                )
                    self.finished.wait(0.1)
            self.finished.wait(0.1)
        try:
            eg.scheduler.CancelTask(monitored)
        except:
            pass
        print self.text.threadStopped
        self.thread_up = False

    def Configure(
        self,
        ow_host='192.168.10.123',
        ow_port=4304,
        b_poll=True
    ):
        text = self.text
        panel = eg.ConfigPanel()

        hostCtrl = panel.TextCtrl(ow_host)
        portCtrl = panel.SpinIntCtrl(ow_port)
        pollCtrl = wx.CheckBox(panel, -1, '')
        pollCtrl.SetValue(b_poll)

        panel.AddLine(text.ow_host, hostCtrl)
        panel.AddLine(text.ow_port, portCtrl)
        panel.AddLine(text.ow_poll, pollCtrl)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                pollCtrl.GetValue()
            )


class ReadAttribute(eg.ActionClass):

    def __call__(
        self,
        name,
        path,
        attribute,
        b_poll,
        poll_interval,
        last_poll

    ):
        msg = str(path + '/' + attribute)
        rsp = self.plugin.R_read(msg)
        print name, msg, rsp
        return rsp

    # Get the choice from dropdown and perform some action
    def OnPathChoice(self, event=None):
        attribCtrl = self.attribCtrl
        pathCtrl = self.pathCtrl
        choice = pathCtrl.GetSelection()
        path = pathCtrl.GetStringSelection()
        a_list = self.plugin.my_sensors_attributes[path]
        attribCtrl.Clear()
        attribCtrl.AppendItems(items=a_list)
        if a_list.count(path) == 0:
            sel = 0
        else:
            sel = int(a_list.index(path))
        attribCtrl.SetSelection(sel)
        if event:
            event.Skip()
        return choice

    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        name="Give me a name",
        path="",
        attribute="",
        b_poll=False,
        poll_interval=10.0,
        last_poll=0
    ):
        plugin_stopped = False
        text = Text
        panel = eg.ConfigPanel(self)
        list = self.plugin.my_sensors
        self.path = path

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for sensor path
        pathCtrl = self.pathCtrl = wx.Choice(parent=panel, pos=(10, 10))
        pathCtrl.AppendItems(items=list)
        if list.count(self.path) == 0:
            pathCtrl.Select(n=0)
        else:
            pathCtrl.SetSelection(int(list.index(self.path)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxPath)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(pathCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        pathCtrl.Bind(wx.EVT_CHOICE, self.OnPathChoice)

        # Create a dropdown for sensor attribute
        attribCtrl = self.attribCtrl = wx.Choice(parent=panel, pos=(10, 10))
        if path:
            self.OnPathChoice()  # This is used when opening the dialog
        a_list = attribCtrl.GetStrings()
        if attribute in a_list:
            attribCtrl.SetStringSelection(attribute)
        staticBox = wx.StaticBox(panel, -1, text.textBoxAttribute)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(attribCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        attribCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a checkbox for polling of sensor attribute
        pollCtrl = wx.CheckBox(panel, -1, '')
        pollCtrl.SetValue(b_poll)
        staticBox = wx.StaticBox(panel, -1, text.textBoxPoll)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(pollCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        poll_intervalCtrl = panel.SpinNumCtrl(
            poll_interval,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            fractionWidth=1,
            integerWidth=3,
            min=1.0,
            max=999.0,
            increment=0.5
        )
        poll_intervalCtrl.SetValue(poll_interval)
        staticBox = wx.StaticBox(panel, -1, text.ow_poll_interval)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(poll_intervalCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            if self.plugin.started and pollCtrl.GetValue():
                self.plugin.__stop__()
                plugin_stopped = True
                while self.plugin.thread_up:
                    time.sleep(0.01)

            pC = str(
                pathCtrl.GetStringSelection()
                + '/'
                + attribCtrl.GetStringSelection()
            )

            if pollCtrl.GetValue():
                CurrentStateData.sensors_status[pC] = [
                    'undefined',
                    poll_intervalCtrl.GetValue(),
                    last_poll
                ]

            if not pollCtrl.GetValue():
                try:
                    del CurrentStateData.sensors_status[pC]
                except:
                    pass

            panel.SetResult(
                nameCtrl.GetValue(),
                pathCtrl.GetStringSelection(),
                attribCtrl.GetStringSelection(),
                pollCtrl.GetValue(),
                poll_intervalCtrl.GetValue(),
                last_poll
            )

            if plugin_stopped:
                self.plugin.__start__(
                    self.plugin.ow_server,
                    self.plugin.ow_port,
                    self.plugin.b_poll
                )


class ClearSensorsStatus(eg.ActionClass):

    def __call__(self):
        # Clear the repository for attributes included in the polling
        plugin_stopped = False
        if self.plugin.started:
            self.plugin.__stop__()
            plugin_stopped = True
            while self.plugin.thread_up:
                time.sleep(0.01)
        time.sleep(1.0)
        CurrentStateData.sensors_status = {}
        del self.plugin.sensors_status
        time.sleep(1.0)
        if plugin_stopped:
            self.plugin.__start__(
                self.plugin.ow_server,
                self.plugin.ow_port,
                self.plugin.b_poll
            )


class WriteAttribute(eg.ActionClass):

    def __call__(
        self,
        name,
        path,
        attribute,
        value
    ):
        msg = str(path + '/' + attribute)
        res = self.plugin.W_write(msg, value)
        print name, msg, self.plugin.R_read(msg)

    # Get the choice from dropdown and perform some action
    def OnPathChoice(self, event=None):
        attribCtrl = self.attribCtrl
        pathCtrl = self.pathCtrl
        choice = pathCtrl.GetSelection()
        path = pathCtrl.GetStringSelection()
        a_list = self.plugin.my_sensors_attributes[path]
        attribCtrl.Clear()
        attribCtrl.AppendItems(items=a_list)
        if a_list.count(path) == 0:
            sel = 0
        else:
            sel = int(a_list.index(path))
        attribCtrl.SetSelection(sel)
        if event:
            event.Skip()
        return choice

    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        name="Give me a name",
        path="",
        attribute="",
        value=""
    ):

        text = Text
        panel = eg.ConfigPanel(self)
        list = self.plugin.my_sensors
        self.path = path

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for sensor path
        pathCtrl = self.pathCtrl = wx.Choice(parent=panel, pos=(10, 10))
        pathCtrl.AppendItems(items=list)
        if list.count(self.path) == 0:
            pathCtrl.Select(n=0)
        else:
            pathCtrl.SetSelection(int(list.index(self.path)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxPath)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(pathCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        pathCtrl.Bind(wx.EVT_CHOICE, self.OnPathChoice)

        # Create a dropdown for sensor attribute
        attribCtrl = self.attribCtrl = wx.Choice(parent=panel, pos=(10, 10))
        if path:
            self.OnPathChoice()  # This is used when opening the dialog
        a_list = attribCtrl.GetStrings()
        if attribute in a_list:
            attribCtrl.SetStringSelection(attribute)
        staticBox = wx.StaticBox(panel, -1, text.textBoxAttributeW)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(attribCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        attribCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a textfield for value string 
        valueCtrl = wx.TextCtrl(panel, -1, value)
        staticBox = wx.StaticBox(panel, -1, text.textBoxValue)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(valueCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                pathCtrl.GetStringSelection(),
                attribCtrl.GetStringSelection(),
                valueCtrl.GetValue()
            )
