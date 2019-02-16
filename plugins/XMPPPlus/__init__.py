# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://www.eventghost.net/>
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

# Initial Release
# K    1/29/2018 11:36 -7:00
# -----------------------------------------------
# Adds looping connect to handle slow wifi card connections on system resume
# K    1/31/2018 15:19 -7:00
# -----------------------------------------------
# Adds automatic ping requests (keep alive)
# K    1/31/2018 15:37 -7:00
# -----------------------------------------------
# Changes disconnect to create connection instead of reconnecting. I also set
# sleekxmpp.ClientXMPP.auto_reconnect to False
# K    2/2/2018 23:37 -7:00
# -----------------------------------------------
# Adds pyasn1 to check for certificate validity and expiration
# K    2/3/2018 00:10 -7:00
# -----------------------------------------------
# Modified sleekxmpp\xmlstream\cert.py file to support pyasn1 version 4.2
# Also corrected issue with 2 digit year formatted certificates.
# K    2/3/2018 01:13 -7:00
# -----------------------------------------------
# Adds dropdown listing connected users in the action dialogs
# moves setting nickname to the plugin config dialog
# K    2/4/2018 10:58 -7:00
# -----------------------------------------------
# Adds GetPresence action
# K    2/4/2018 12:58 -7:00
# -----------------------------------------------
# Adds autocomplete for JID and resource in actions
# K    2/4/2018 13:49 -7:00
# -----------------------------------------------
# Fixes startup parameter alignment
# K    2/4/2018 17:19 -7:00
# -----------------------------------------------
# Fixes double listing of client JID in actions
# K    2/4/2018 21:43 -7:00
# -----------------------------------------------
# Changes print statements to TriggerEvent
# K    2/6/2018 22:41 -7:00
# -----------------------------------------------
# Adds actions GetMessageBody, IsMessageFrom, IsPresenceFrom,
# IsMessageType, IsPresenceType
# K    2/7/2018 00:13 -7:00
# -----------------------------------------------
# Adds message receipts xep-0184
# K    2/9/2018 11:24 -7:00
# -----------------------------------------------
# Adds receipt requests
# K    2/9/2018 23:02 -7:00
# -----------------------------------------------
# Formatting, Adds available and offline to get presence return
# K    3/17/2018 10:27 -6:00
# -----------------------------------------------

DEBUGGING = False

import eg # NOQA

eg.RegisterPlugin(
    name="XMPP Plus",
    author="K",
    kind="other",
    version="1.2.2",
    canMultiLoad=True,
    createMacrosOnAdd=True,
    guid='{9CE4EF99-BE87-4016-93C9-E4A9811D55D6}',
    description="Sends and receives data using the XMPP protocol",
)

import wx # NOQA
import threading # NOQA
import os # NOQA
import sys # NOQA
import wx.lib.newevent # NOQA

if DEBUGGING:
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-8s %(message)s'
    )


sys.path += [os.path.split(__file__)[0]]
from sleekxmpp import ClientXMPP # NOQA
from sleekxmpp.xmlstream.handler import Callback # NOQA
from sleekxmpp.xmlstream.matcher import StanzaPath # NOQA


NewChoicesEvent, EVT_NEW_CHOICES_EVENT = wx.lib.newevent.NewCommandEvent()


def create_sizer(st, widget, prop=0):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
    sizer.Add(widget, prop, wx.EXPAND | wx.ALL, 5)
    return sizer


def parse(data):
    try:
        return eg.ParseString(data)
    except:
        return data


ESCAPES = ''.join([chr(char) for char in range(1, 32)])


class Message(object):
    def __init__(self, msg):
        self.__msg = msg
        self.type = msg.get_type()
        self.sender = msg.get_from()
        self.room = msg.get_mucroom()
        self.body = msg['body']
        self.subject = msg['subject']

    def __repr__(self):
        return repr([
            self.sender,
            str(self.body[:50]).translate(None, ESCAPES)
            + (u'...' if len(self.body) > 50 else u'')
        ])

    def __str__(self):
        return self.__repr__()

    def reply(self, msg):
        self.__msg.reply(msg).send()


class MessageReceipt(object):

    def __init__(self, plugin, msg):
        self.__plugin = plugin
        self.__msg = msg

        self.type = msg.get_type()
        self.sender = msg.get_from()
        self.room = msg.get_mucroom()
        self.body = msg['body']
        self.subject = msg['subject']

    def send_receipt(self):
        self.__plugin.ack(self.__msg)


class Presence(object):
    def __init__(self, event):
        self.__event = event
        self.priority=event.get_priority()
        self.type=event.get_type()
        self.sender=event.get_from()
        self.status=event['status']

    def unsubscribe(self):
        self.__event.set_type('unsubscribe')
        self.__event.reply().send()

    def __repr__(self):
        return unicode(
            repr([
                unicode(self.type),
                unicode(
                    str(self.status[:50]).translate(None, ESCAPES)
                    + (u'...' if len(self.status) > 50 else u'')
                ),
            ])
        )

    def __str__(self):
        return self.__repr__()

    def reply(self, msg):
        self.__msg.reply(msg).send()


class XMPPPlus(eg.PluginClass):

    def __init__(self):
        self.AddAction(SendMessage)
        self.AddAction(SendPresence)
        self.AddAction(GetPresence)
        self.AddAction(GetMessageBody)
        self.AddAction(SendMessageReceipt)
        self.AddAction(IsMessageFrom)
        self.AddAction(IsPresenceFrom)
        self.AddAction(IsMessageType)
        self.AddAction(IsPresenceType)
        self._client = None
        self._password = ''
        self._resource = ''
        self._server = ''
        self._port = ''
        self._jid = ''
        self._nick = ''
        self._socket_error = False
        self._reconnect_flag = False
        self._disconnect_event = threading.Event()
        self._disconnect_event.set()
        self._shutting_down_event = threading.Event()

    def __start__(
        self,
        jid="username@gmail.com",
        password="password",
        resource="eg/",
        server="talk.google.com",
        port="5222",
        nick=''
    ):

        if resource.endswith('/'):
            resource = resource[:-1]

        if resource.startswith('/'):
            resource = resource[1:]

        self._password = password
        self._resource = resource
        self._server = server
        self._port = port
        self._jid = jid
        self._nick = nick

        self._socket_error = False
        self._reconnect_flag = False
        self._shutting_down_event.clear()

        t = threading.Thread(target=self._connect)
        t.daemon = True
        t.start()

    def _presence_callback(self, event):
        self.TriggerEvent(
            '{0}.Incoming.Presence'.format(self._jid),
            payload=Presence(event)
        )

    def _message_callback(self, message):
        self.TriggerEvent(
            '{0}.Incoming.Message'.format(self._jid),
            payload=Message(message)
        )

    def _connect(self):
        self._disconnect_event.wait()

        if self._resource:
            resource = self._jid + '/' + self._resource
        else:
            resource = self._jid

        self._client = ClientXMPP(
            resource,
            self._password
        )
        self._client.auto_reconnect = False

        self._client.register_plugin('xep_0199')
        self._client.register_plugin('xep_0184')

        self._client.remove_handler('Message Receipt Request')
        self._client['xep_0184'].auto_ack = False

        self._client.register_handler(
            Callback(
                'Message Receipt Request',
                StanzaPath('message/request_receipt'),
                self._handle_receipt_request
            )
        )

        self._client.add_event_handler(
            "connected",
            self._connect_callback
        )
        self._client.add_event_handler(
            "auth_success",
            self._auth_callback
        )
        self._client.add_event_handler(
            "session_start",
            self._start_callback
        )
        self._client.add_event_handler(
            "session_end",
            self._end_callback
        )
        self._client.add_event_handler(
            "socket_error",
            self._socket_callback
        )
        self._client.add_event_handler(
            "disconnected",
            self._disconnect_callback
        )
        self._client.add_event_handler(
            'message',
            self._message_callback
        )
        self._client.add_event_handler(
            'presence',
            self._presence_callback
        )
        self._client.add_event_handler(
            'receipt_received',
            self._receipt_received_callback
        )
        self._client.add_event_handler(
            'receipt_request',
            self._receipt_request_callback
        )

        import time

        address = (self._server, int(self._port))

        while not self._client.connect(address, reattempt=False):
            if self._socket_error:

                self.shutting_down_event.wait(10)
                if self._shutting_down_event.isSet():
                    return

                t = threading.Thread(
                    target=self._connect
                )
                t.daemon = True
                t.start()
                return

            self.shutting_down_event.wait(2)
            if self._shutting_down_event.isSet():
                return

    def _handle_receipt_request(self, msg):
        self._client.event('receipt_request', msg)

    def _receipt_request_callback(self, msg):
        if msg['type'] in self._client['xep_0184'].ack_types:
            if not msg['receipt']:
                self.TriggerEvent(
                    '{0}.Incoming.ReceiptRequest'.format(self._jid),
                    payload=MessageReceipt(self._client['xep_0184'], msg)
                )

    def _receipt_received_callback(self, message):
        self.TriggerEvent(
            '{0}.Incoming.Receipt'.format(self._jid),
            payload=Message(message)
        )

    def _start_callback(self, _):
        self._reconnect_flag = False
        self.TriggerEvent(
            '{0}.SessionStarted'.format(self._jid)
        )
        self._client.send_presence()
        self._client.get_roster(block=False, callback=self._roster_callback)

    def _end_callback(self, _):
        if not self._reconnect_flag:
            self.TriggerEvent(
                '{0}.SessionEnded'.format(self._jid)
            )

    def _socket_callback(self, _):
        self.TriggerEvent(
            '{0}:{1}.SocketError'.format(self._server, self._port)
        )
        self._socket_error = True

    def _auth_callback(self, _):
        self.TriggerEvent(
            '{0}.AuthenticationSuccessful'.format(self._jid)
        )

    def _roster_callback(self, _):
        self.TriggerEvent(
            '{0}.RosterReceived'.format(self._jid)
        )

    def _connect_callback(self, _):
        if not self._reconnect_flag:
            self.TriggerEvent(
                '{0}:{1}.Connected'.format(self._server, self._port)
            )
        self._client.process(block=False)

    @property
    def client_jid(self):
        return self._client.boundjid

    @property
    def roster_jids(self):
        res = sorted(
            list(
                jid.split('/', 1)[0] for jid in self.roster
            )
        )

        if self._client.boundjid.bare not in res:
            res += [self._client.boundjid.bare]
        return res

    @property
    def roster(self):
        return self._client.client_roster

    def send_presence(
        self,
        jid,
        presence_type,
        priority,
        status
    ):

        presence = self._client.make_presence(
            pfrom=self.client_jid.bare,
            pto=jid,
            pshow=presence_type,
            ppriority=priority,
            pstatus=status,
            pnick=self._nick
        )
        presence.send()

    def send_message(
        self,
        jid,
        msg_type,
        msg,
        subject,
        receipt
    ):
        self._client['xep_0184'].auto_request = receipt

        message = self._client.make_message(
            mto=jid,
            mfrom=self.client_jid.bare,
            msubject=subject,
            mtype=msg_type,
            mnick=self._nick,
            mbody=msg
        )
        message.send()

    def _disconnect_callback(self, _):
        if self._socket_error is False and self._disconnect_event.isSet():
            self._reconnect_flag = True
            t = threading.Thread(target=self._connect)
            t.daemon = True
            t.start()
        else:
            self._disconnect_event.set()

    def __stop__(self):
        self._shutting_down_event.set()
        self._disconnect_event.clear()
        self._client.disconnect()

    def OnComputerResume(self, _):
        self.__start__(
            self._jid,
            self._password,
            self._resource,
            self._server,
            self._port,
            self._nick
        )

    def OnComputerSuspend(self, _):
        self.__stop__()

    def Configure(
        self,
        jid="username@gmail.com",
        password="password",
        resource="eg/",
        server="talk.google.com",
        port="5222",
        nick=''
    ):

        panel = eg.ConfigPanel()

        jid_st = panel.StaticText("JID:")
        jid_ctrl = panel.TextCtrl(jid)

        nick_st = panel.StaticText("Nickname:")
        nick_ctrl = panel.TextCtrl(nick)

        pwd_st = panel.StaticText("Password:")
        pwd_ctrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)

        res_st = panel.StaticText("Resource:")
        res_ctrl = panel.TextCtrl(resource)

        srv_st = panel.StaticText("Server:")
        srv_ctrl = panel.TextCtrl(server)

        prt_st = panel.StaticText("Port:")
        prt_ctrl = panel.TextCtrl(port)

        jid_sizer = create_sizer(jid_st, jid_ctrl)
        nick_sizer = create_sizer(nick_st, nick_ctrl)
        password_sizer = create_sizer(pwd_st, pwd_ctrl)
        resource_sizer = create_sizer(res_st, res_ctrl)
        server_sizer = create_sizer(srv_st, srv_ctrl)
        port_sizer = create_sizer(prt_st, prt_ctrl)

        eg.EqualizeWidths(
            (jid_st, nick_st, pwd_st, res_st, srv_st, prt_st)
        )
        eg.EqualizeWidths(
            (jid_ctrl, nick_ctrl, pwd_ctrl, res_ctrl, srv_ctrl, prt_ctrl)
        )

        panel.sizer.Add(jid_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(nick_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(password_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(resource_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(server_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(port_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        while panel.Affirmed():
            panel.SetResult(
                jid_ctrl.GetValue(),
                pwd_ctrl.GetValue(),
                res_ctrl.GetValue(),
                srv_ctrl.GetValue(),
                prt_ctrl.GetValue(),
                nick_ctrl.GetValue(),
            )


class ComboBoxBase(wx.ComboBox):

    def __init__(self, parent, choices):

        wx.ComboBox.__init__(
            self,
            parent,
            -1,
            '',
            choices=choices,
            style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER
        )

        self.ignore_evt = False
        self.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        self.Bind(wx.EVT_TEXT, self.on_text)
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox)

    def on_combobox(self, evt):
        self.ignore_evt = True
        evt.Skip()

    def on_char(self, evt):
        if evt.GetKeyCode() == 8:
            self.ignore_evt = True
        evt.Skip()

    def on_text(self, evt):
        if self.ignore_evt:
            self.ignore_evt = False
            return

        current_text = evt.GetString()

        for choice in self.GetItems():
            if choice.startswith(current_text):
                self.ignore_evt = True
                self.SetValue(choice)
                self.SetInsertionPoint(len(current_text))
                self.SetTextSelection(len(current_text), len(choice))
                break
        else:
            evt.Skip()

    def GetStringSelection(self):
        wx.CallAfter(self.process_entry)
        return wx.ComboBox.GetStringSelection(self)

    def process_entry(self):
        raise NotImplementedError

    def on_enter(self, evt):
        self.process_entry()
        evt.Skip()

        def do(win):
            wx.PostEvent(win, NewChoicesEvent(-1))

        t = threading.Thread(target=do, args=(self,))
        t.setDaemon(True)
        t.start()


class JIDCtrl(ComboBoxBase):

    def __init__(self, plugin, parent, jid):

        choices = list(j for j in plugin.roster_jids)
        if jid and jid not in choices:
            choices = sorted(choices + [jid])

        ComboBoxBase.__init__(
            self,
            parent,
            choices
        )
        if jid:
            self.SetStringSelection(jid)

    def process_entry(self):
        jid = self.GetValue()
        if '@' not in jid:
            self.SetValue('')
        else:
            jids = self.GetItems()
            if jid not in jids:
                jids = sorted(jids + [jid])
                self.Clear()
                self.SetItems(jids)

            self.SetStringSelection(jid)


class ResourceCtrl(ComboBoxBase):

    def __init__(self, plugin, parent, jid, resource):
        self.plugin = plugin

        jids = list(j for j in plugin.roster_jids)

        if jid and jid in jids:
            resources = plugin.roster.presence(jid)
            choices = sorted(resources.keys())
        else:
            choices = []

        if resource and resource not in choices:
            choices = sorted(choices + [resource])

        ComboBoxBase.__init__(
            self,
            parent,
            choices
        )
        if resource:
            self.SetStringSelection(resource)

        self.Bind(wx.EVT_TEXT_ENTER, self.on_enter)

    def SetItems(self, jid):
        jids = list(j for j in self.plugin.roster_jids)

        if jid and jid in jids:
            resources = self.plugin.roster.presence(jid)
            choices = sorted(resources.keys())
        else:
            choices = []

        self.Clear()
        wx.ComboBox.SetItems(self, choices)
        if choices:
            self.SetSelection(0)

    def process_entry(self):
        resource = self.GetValue()

        resources = self.GetItems()
        if resource not in resources:
            resources = sorted(resources + [resource])
            self.Clear()
            wx.ComboBox.SetItems(self, resources)
            self.SetStringSelection(resource)


class SendMessage(eg.ActionBase):
    name = "Send Message"
    description = "Sends a message"

    def __call__(
        self,
        jid,
        msg_type,
        msg,
        subject=None,
        receipt=False
    ):

        self.plugin.send_message(
            parse(jid),
            msg_type.lower().replace(' ', ''),
            parse(msg),
            parse(subject),
            receipt
        )

    def Configure(
        self,
        jid='',
        msg_type='Normal',
        msg='',
        subject='',
        receipt=False
    ):

        panel = eg.ConfigPanel()

        jid_st = panel.StaticText("To (JID)*:")
        jid_ctrl = JIDCtrl(self.plugin, panel, jid)

        type_st = panel.StaticText("Message Type:")
        type_ctrl = panel.Choice(
            value=0,
            choices=['Normal', 'Chat', 'Headline', 'Error', 'Group Chat']
        )
        type_ctrl.SetStringSelection(msg_type)

        msg_st = panel.StaticText("Message:")
        msg_ctrl = panel.TextCtrl(msg, style=wx.TE_MULTILINE)

        subject_st = panel.StaticText("Subject:")
        subject_ctrl = panel.TextCtrl(subject)

        receipt_st = panel.StaticText("Request Receipt:")
        receipt_ctrl = wx.CheckBox(panel, -1, '')
        receipt_ctrl.SetValue(receipt)
        receipt_ctrl.Enable(msg_type in ('Normal', 'Chat', 'Headline'))

        def on_type(evt):
            m_type = type_ctrl.GetStringSelection()
            receipt_ctrl.Enable(m_type in ('Normal', 'Chat', 'Headline'))
            evt.Skip()

        type_ctrl.Bind(wx.EVT_CHOICE, on_type)

        eg.EqualizeWidths((type_st, subject_st, jid_st, receipt_st))
        eg.EqualizeWidths((jid_ctrl, type_ctrl))
        eg.EqualizeWidths((subject_ctrl, msg_ctrl))

        jid_sizer = create_sizer(jid_st, jid_ctrl)
        jid_sizer.AddStretchSpacer(1)
        type_sizer = create_sizer(type_st, type_ctrl)
        type_sizer.AddStretchSpacer(1)
        receipt_sizer = create_sizer(receipt_st, receipt_ctrl)
        receipt_sizer.AddStretchSpacer(1)
        subject_sizer = create_sizer(subject_st, subject_ctrl, prop=1)

        msg_sizer = wx.BoxSizer(wx.VERTICAL)
        msg_sizer.Add(msg_st, 0, wx.EXPAND | wx.ALL, 5)
        msg_sizer.Add(msg_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(jid_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(type_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(receipt_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(subject_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(msg_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        note_st = panel.StaticText('* Field is editable.')
        panel.sizer.Add(note_st, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        wx.CallAfter(panel.dialog.SetSize, (700, 500))

        while panel.Affirmed():
            panel.SetResult(
                jid_ctrl.GetStringSelection(),
                type_ctrl.GetStringSelection(),
                msg_ctrl.GetValue(),
                subject_ctrl.GetValue(),
                receipt_ctrl.GetValue() and receipt_ctrl.IsEnabled()
            )


class SendPresence(eg.ActionBase):
    name = "Send Presence"
    description = "Send presence"

    def __call__(
        self,
        jid,
        presence_type,
        priority,
        status=None
    ):
        self.plugin.send_presence(
            parse(jid),
            parse(presence_type).lower(),
            parse(priority),
            parse(status)
        )

    def Configure(
        self,
        jid='',
        presence_type='Available',
        priority=1,
        status=''
    ):

        panel = eg.ConfigPanel()

        jid_st = panel.StaticText("To (JID)*:")
        jid_ctrl = JIDCtrl(self.plugin, panel, jid)

        type_st = panel.StaticText("Presence Type:")
        type_ctrl = panel.Choice(
            value=0,
            choices=['Away', 'Available', 'Chat', 'DND', 'Offline', 'XA']
        )
        type_ctrl.SetStringSelection(presence_type)
        priority_st = panel.StaticText('Priority:')
        priority_ctrl = panel.SpinIntCtrl(value=priority, max=127)

        status_st = panel.StaticText("Status Message:")
        status_ctrl = panel.TextCtrl(status, style=wx.TE_MULTILINE)

        eg.EqualizeWidths((type_st, jid_st, priority_st))
        eg.EqualizeWidths((jid_ctrl, type_ctrl, priority_ctrl))

        jid_sizer = create_sizer(jid_st, jid_ctrl)
        jid_sizer.AddStretchSpacer(1)
        type_sizer = create_sizer(type_st, type_ctrl)
        type_sizer.AddStretchSpacer(1)
        priority_sizer = create_sizer(priority_st, priority_ctrl)
        priority_sizer.AddStretchSpacer(1)

        status_sizer = wx.BoxSizer(wx.VERTICAL)
        status_sizer.Add(status_st, 0, wx.EXPAND | wx.ALL, 5)
        status_sizer.Add(status_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(jid_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(type_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(priority_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(status_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        note_st = panel.StaticText('* Field is editable.')
        panel.sizer.Add(note_st, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        wx.CallAfter(panel.dialog.SetSize, (700, 500))

        while panel.Affirmed():
            panel.SetResult(
                jid_ctrl.GetStringSelection(),
                type_ctrl.GetStringSelection(),
                priority_ctrl.GetValue(),
                status_ctrl.GetValue()
            )


class GetMessageBody(eg.ActionBase):
    name = "Get Message"
    description = "Gets the body of an incoming message"

    def __call__(self):
        message = eg.event.payload
        if isinstance(message, Message):
            return message.body


class SendMessageReceipt(eg.ActionBase):
    name = "Send Message Receipt"
    description = "Send receipt if an incoming message requested one."

    def __call__(self):
        message = eg.event.payload
        if isinstance(message, MessageReceipt):
            message.send_receipt()


class GetPresence(eg.ActionBase):
    name = "Get Presence"
    description = "Get presence"

    def __call__(self, jid, resource):
        try:
            presence = self.plugin.roster.presence(parse(jid))
            presence = presence[parse(resource)]['show']

            if presence is None:
                presence = 'offline'
            elif not presence:
                presence = 'available'

            return presence
        except KeyError:
            return 'offline'

    def Configure(self, jid='', resource=''):
        panel = eg.ConfigPanel()

        jid_st = panel.StaticText("JID*:")
        jid_ctrl = JIDCtrl(self.plugin, panel, jid)

        resource_st = panel.StaticText('Resource*:')
        resource_ctrl = ResourceCtrl(self.plugin, panel, jid, resource)

        def on_jid_choice(evt):
            resource_ctrl.SetItems(jid_ctrl.GetStringSelection())
            evt.Skip()

        jid_ctrl.Bind(wx.EVT_COMBOBOX, on_jid_choice)
        jid_ctrl.Bind(EVT_NEW_CHOICES_EVENT, on_jid_choice)

        jid_sizer = create_sizer(jid_st, jid_ctrl)
        resource_sizer = create_sizer(resource_st, resource_ctrl)

        eg.EqualizeWidths((jid_st, resource_st))
        eg.EqualizeWidths((jid_ctrl, resource_ctrl))

        panel.sizer.Add(jid_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(resource_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        note_st = panel.StaticText('* Field is editable.')
        panel.sizer.AddStretchSpacer(1)
        panel.sizer.Add(note_st, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        while panel.Affirmed():
            panel.SetResult(
                jid_ctrl.GetStringSelection(),
                resource_ctrl.GetStringSelection()
            )


class IsFromBase(eg.ActionBase):
    name = ''
    description = ''
    _obj = None

    def __call__(
        self,
        jid,
        stop_macro
    ):

        payload = eg.event.payload
        if isinstance(payload, self._obj):
            res =  str(payload.sender).startswith(parse(jid))
        else:
            res = False

        if stop_macro and not res:
            eg.StopMacro()

        return res

    def Configure(
        self,
        jid='',
        stop_macro=False
    ):

        panel = eg.ConfigPanel()

        jid_st = panel.StaticText("From (JID)*:")
        jid_ctrl = JIDCtrl(self.plugin, panel, jid)

        stop_st = panel.StaticText("Stop macro if not from sender:")
        stop_ctrl = wx.CheckBox(panel, -1, '')

        stop_ctrl.SetValue(stop_macro)
        eg.EqualizeWidths((stop_st, jid_st))

        jid_sizer = create_sizer(jid_st, jid_ctrl)
        stop_sizer = create_sizer(stop_st, stop_ctrl)

        panel.sizer.Add(jid_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(stop_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        note_st = panel.StaticText('* Field is editable.')
        panel.sizer.AddStretchSpacer(1)
        panel.sizer.Add(note_st, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        while panel.Affirmed():
            panel.SetResult(
                jid_ctrl.GetStringSelection(),
                stop_ctrl.GetValue()
            )


class IsMessageFrom(IsFromBase):
    name = "Is Message From"
    description = "Checks the sender of an incoming message."
    _obj = Message


class IsPresenceFrom(IsFromBase):
    name = "Is Presence From"
    description = "Checks the sender of an incoming presence."
    _obj = Presence


class IsTypeBase(eg.ActionBase):
    name = ''
    description = ''
    _choices = []
    _obj = None

    def __call__(
        self,
        check_type,
        stop_macro
    ):
        payload = eg.event.payload
        if isinstance(payload, self._obj):
            res = payload.type == parse(check_type).lower().replace(' ', '')
        else:
            res = False

        if stop_macro and not res:
            eg.StopMacro()

    def Configure(
        self,
        check_type=None,
        stop_macro=False
    ):

        panel = eg.ConfigPanel()

        type_st = panel.StaticText("Type:")
        type_ctrl = panel.Choice(
            value=0,
            choices=self._choices
        )
        if check_type is not None:
            type_ctrl.SetStringSelection(check_type)

        stop_st = panel.StaticText("Stop macro if type does not match:")
        stop_ctrl = wx.CheckBox(panel, -1, '')

        stop_ctrl.SetValue(stop_macro)
        eg.EqualizeWidths((type_st, stop_st))

        type_sizer = create_sizer(type_st, type_ctrl)
        stop_sizer = create_sizer(stop_st, stop_ctrl)

        panel.sizer.Add(type_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        panel.sizer.Add(stop_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        while panel.Affirmed():
            panel.SetResult(
                type_ctrl.GetStringSelection(),
                stop_ctrl.GetValue()
            )


class IsMessageType(IsTypeBase):
    name = "Is Message Type"
    description = "Checks the type of an incoming message."
    _choices = ['Normal', 'Chat', 'Headline', 'Error', 'Group Chat']
    _obj = Message


class IsPresenceType(IsTypeBase):
    name = "Is Presence Type"
    description = "Checks the type of an incoming presence."
    _choices = ['Away', 'Available', 'Chat', 'DND', 'Offline', 'XA']
    _obj = Presence

