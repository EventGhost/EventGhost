# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
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


eg.RegisterPlugin(
    name=u'Text Messaging',
    author=u'K',
    version=u'0.5b',
    description=u'Send SMS/MMS Text Messages',
    kind=u'other',
    url=u'',
    help=u'',
    canMultiLoad=True,
    createMacrosOnAdd=True,
    guid=u'{911F652D-18F2-4AC7-A89E-02FAFEEE4D51}',
    hardwareId=u'',
    icon=None
)

import wx # NOQA
import types  # NOQA
import smtplib  # NOQA
import os.path  # NOQA
import mimetypes  # NOQA
import email.utils # NOQA
import email.Message  # NOQA
from email import Encoders  # NOQA
from email.MIMEBase import MIMEBase  # NOQA
from email.MIMEText import MIMEText  # NOQA
from email.MIMEAudio import MIMEAudio  # NOQA
from email.MIMEImage import MIMEImage  # NOQA
from email.MIMEMultipart import MIMEMultipart  # NOQA
from .carriers import CARRIERS # NOQA


MIME_TYPES = dict(
    text=[MIMEText, ''],
    image=[MIMEImage, 'rb'],
    audio=[MIMEAudio, 'rb'],
)


class TextMessaging(eg.PluginBase):
    def __init__(self):
        self.smtp_server = None
        self.smtp_port = None
        self.use_ssl = None
        self.use_tls = None
        self.username = None
        self.password = None
        self.debug = None
        self.AddAction(SendSMS)
        self.AddAction(SendMMS)

    def __start__(
        self,
        smtp_server='smtp.gmail.com',
        smtp_port=465,
        use_ssl=True,
        use_tls=False,
        username='SOME_GMAIL_ACCOUNT@gmail.com',
        password='',
        debug=False
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.use_ssl = use_ssl
        self.use_tls = use_tls
        self.username = username
        self.password = password
        self.debug = debug

    def __stop__(self):
        pass

    def __close__(self):
        pass

    def send(self, to_email, subject, body, attachment_list=None):

        if isinstance(body, (str, unicode)):
            body = MIMEText(body, 'plain')
        else:
            body = MIMEMultipart('alternative')
            for k in body:
                body.attach(MIMEText(body[k], k))

        msg = MIMEMultipart()
        msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        msg.epilogue = ''
        msg.attach(body)

        msg.set_unixfrom('author')
        msg['To'] = email.utils.formataddr(('Recipient', to_email))
        msg['From'] = email.utils.formataddr(('EventGhost', self.username))
        msg['Subject'] = subject

        if attachment_list is not None:

            for path in attachment_list:
                dirname, filename = os.path.split(path)
                ctype, encoding = mimetypes.guess_type(path)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)

                if maintype in MIME_TYPES:
                    mime, read_type = MIME_TYPES[maintype]
                    with open(path, read_type) as f:
                        attachment = mime(f.read(), _subtype=subtype)
                else:
                    attachment = MIMEBase(maintype, subtype)
                    with open(path, 'rb') as f:
                        attachment.set_payload(f.read())
                    Encoders.encode_base64(msg)

                attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=filename
                )
                msg.attach(attachment)

        if self.use_ssl:
            server = smtplib.SMTP_SSL
        else:
            server = smtplib.SMTP

        server = server(self.smtp_server, self.smtp_port)
        try:
            server.set_debuglevel(self.debug)
            server.ehlo()

            if self.use_tls and server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo()

            server.login(self.username, self.password)
            smtpresult = server.sendmail(
                self.username,
                [to_email],
                msg.as_string()
            )

            if smtpresult:
                for recip in smtpresult.keys():
                    eg.PrintNotice(
                        'Could not delivery mail to: %s Server said: %s %s' %
                        (recip, smtpresult[recip][0], smtpresult[recip][1])
                    )
        finally:
            server.quit()

    def Configure(
        self,
        smtp_server='smtp.gmail.com',
        smtp_port=465,
        use_ssl=True,
        use_tls=False,
        username='SOME_GMAIL_ACCOUNT@gmail.com',
        password='',
        debug=False
    ):
        panel = eg.ConfigPanel()

        server_st = panel.StaticText('SMTP Server:')
        server_ctrl = panel.TextCtrl(smtp_server)
        port_st = panel.StaticText('SMTP Port:')
        port_ctrl = panel.SpinIntCtrl(smtp_port, min=0, max=65535)
        ssl_st = panel.StaticText('SSL Encryption:')
        ssl_ctrl = wx.CheckBox(panel)
        tls_st = panel.StaticText('TLS Encryption:')
        tls_ctrl = wx.CheckBox(panel)
        user_st = panel.StaticText('SMTP Username:')
        user_ctrl = panel.TextCtrl(username)
        pass_st = panel.StaticText('SMTP Password:')
        pass_ctrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        debug_st = panel.StaticText('Debug:')
        debug_ctrl = wx.CheckBox(panel)

        ssl_ctrl.SetValue(use_ssl)
        tls_ctrl.SetValue(use_tls)
        debug_ctrl.SetValue(debug)

        def add(st, widget, prop):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.ALL, 5)
            sizer.Add(widget, prop, wx.EXPAND | wx.ALL, 5)
            panel.sizer.Add(sizer, 0, wx.EXPAND)

        add(server_st, server_ctrl, 1)
        add(port_st, port_ctrl, 0)
        add(ssl_st, ssl_ctrl, 0)
        add(tls_st, tls_ctrl, 0)
        add(user_st, user_ctrl, 1)
        add(pass_st, pass_ctrl, 1)
        add(debug_st, debug_ctrl, 0)

        eg.EqualizeWidths(
            (server_st, port_st, ssl_st, tls_st, user_st, pass_st, debug_st)
        )
        eg.EqualizeWidths((server_ctrl, user_ctrl, pass_ctrl))

        while panel.Affirmed():
            panel.SetResult(
                server_ctrl.GetValue(),
                port_ctrl.GetValue(),
                ssl_ctrl.GetValue(),
                tls_ctrl.GetValue(),
                user_ctrl.GetValue(),
                pass_ctrl.GetValue(),
                debug_ctrl.GetValue()
            )


class MailPanel(wx.Panel):

    def __init__(
        self,
        parent,
        country,
        carrier,
        phone_number,
        gateway,
        subject,
        message,
        msgtype
    ):
        wx.Panel.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        country_st = wx.StaticText(self, -1, 'Country:')
        country_ctrl = wx.Choice(self, -1, choices=sorted(CARRIERS.keys()))

        carrier_st = wx.StaticText(self, -1, 'Carrier:')
        carrier_ctrl = wx.Choice(self, -1, choices=[''])

        phone_st = wx.StaticText(self, -1, 'Phone Number:   ')
        phone_ctrl = wx.TextCtrl(self, -1, phone_number)

        at_st = wx.StaticText(self, -1, '@')

        gateway_ctrl = wx.Choice(self, -1, choices=[''])

        subject_st = wx.StaticText(self, -1, 'Subject:')
        subject_ctrl = wx.TextCtrl(self, -1, subject)

        message_st = wx.StaticText(self, -1, 'Message:')
        message_ctrl = wx.TextCtrl(self, -1, message, style=wx.TE_MULTILINE)

        def on_country(evt=None):
            selection = country_ctrl.GetStringSelection()
            carriers = sorted(CARRIERS[selection].keys())
            carrier_ctrl.SetItems(carriers)
            carrier_ctrl.SetSelection(0)
            self.SendSizeEventToParent()
            if evt is not None:
                evt.Skip()

        def on_carrier(evt=None):
            selection1 = country_ctrl.GetStringSelection()
            selection2 = carrier_ctrl.GetStringSelection()
            carrier_info = CARRIERS[selection1][selection2]

            flag_index = list(
                idx for idx, flag in enumerate(carrier_info['flags'])
                if flag == msgtype
            )

            gateways = list(carrier_info['gateway'][i] for i in flag_index)
            gateway_ctrl.SetItems(gateways)
            gateway_ctrl.SetSelection(0)
            self.SendSizeEventToParent()
            if evt is not None:
                evt.Skip()

        country_ctrl.Bind(wx.EVT_CHOICE, on_country)
        carrier_ctrl.Bind(wx.EVT_CHOICE, on_carrier)

        if country:
            country_ctrl.SetStringSelection(country)
        else:
            country_ctrl.SetSelection(0)

        on_country()

        if carrier:
            carrier_ctrl.SetStringSelection(carrier)
        else:
            carrier_ctrl.SetSelection(0)

        on_carrier()

        if gateway:
            gateway_ctrl.SetStringSelection(gateway)
        else:
            gateway_ctrl.SetSelection(0)

        def OnChar(evt):
            bad_codes = (
                wx.WXK_NUMPAD_DECIMAL,
                wx.WXK_DECIMAL,
                wx.WXK_NUMPAD_SUBTRACT,
                wx.WXK_SUBTRACT,
                wx.WXK_NUMPAD_ADD,
                wx.WXK_ADD
            )

            if evt.GetKeyCode() in bad_codes:
                return

            not_allowed = (
                ord('.'),
                ord('='),
                ord('+'),
                ord('-'),
                ord('('),
                ord(')')
            )
            if evt.GetUnicodeKey() in not_allowed:
                return

            evt.Skip()

        phone_ctrl.Bind(wx.EVT_CHAR_HOOK, OnChar)

        def add(st, widget, prop):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.ALL, 5)
            sizer.Add(widget, prop, wx.EXPAND | wx.ALL, 5)
            main_sizer.Add(sizer, 0, wx.EXPAND)

        add(country_st, country_ctrl, 0)
        add(carrier_st, carrier_ctrl, 0)

        szr = wx.BoxSizer(wx.HORIZONTAL)
        szr.Add(phone_st, 0, wx.ALL, 5)
        szr.Add(phone_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        szr.Add(at_st, 0, wx.ALL, 5)
        szr.Add(gateway_ctrl, 0,  wx.ALL, 5)
        main_sizer.Add(szr, 0, wx.EXPAND)

        add(subject_st, subject_ctrl, 0)
        add(message_st, message_ctrl, 1)

        eg.EqualizeWidths(
            (country_st, phone_st, carrier_st, subject_st, message_st)
        )

        self.SetSizer(main_sizer)

        def GetValues():
            return (
                country_ctrl.GetStringSelection(),
                carrier_ctrl.GetStringSelection(),
                phone_ctrl.GetValue(),
                gateway_ctrl.GetStringSelection(),
                subject_ctrl.GetValue(),
                message_ctrl.GetValue(),
            )

        self.GetValues = GetValues


class SendSMS(eg.ActionBase):
    def __call__(
        self,
        country,
        carrier,
        phone_number,
        gateway,
        subject,
        message
    ):
        phone_number = str(phone_number)
        for char in ('.', '-', '+', '(', ')'):
            phone_number = phone_number.replace(char, '')

        if country in CARRIERS:
            carriers = CARRIERS[country]
            if carrier in carriers:
                carrier = carriers[carrier]
                gateway_index = carrier['gateway'].index(gateway)
                recipient = carrier['format'][gateway_index].replace(
                    '~~NUMBER~~',
                    phone_number
                ) + '@' + gateway

                return self.plugin.send(recipient, subject, message)

        eg.PrintNotice('Something\'s not right')

    def Configure(
        self,
        country='',
        carrier='',
        phone_number='',
        gateway='',
        subject='',
        message=''
    ):
        panel = eg.ConfigPanel()
        mail_panel = MailPanel(
            panel,
            country,
            carrier,
            phone_number,
            gateway,
            subject,
            message,
            'SMS'
        )
        panel.sizer.Add(mail_panel, 1, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(*mail_panel.GetValues())


class SendMMS(eg.ActionBase):
    def __call__(
        self,
        country,
        carrier,
        phone_number,
        gateway,
        subject,
        message,
        *attachments
    ):

        phone_number = str(phone_number)
        for char in ('.', '-', '+'):
            phone_number = phone_number.replace(char, '')

        if country in CARRIERS:
            carriers = CARRIERS[country]
            if carrier in carriers:
                carrier = carriers[carrier]
                gateway_index = carrier['gateway'].index(gateway)
                recipient = carrier['format'][gateway_index].replace(
                    '~~NUMBER~~',
                    phone_number
                ) + '@' + gateway

                self.plugin.send(
                    recipient,
                    subject,
                    message,
                    attachments
                )

    def Configure(
        self,
        country='',
        carrier='',
        phone_number='',
        gateway='',
        subject='',
        message='',
        *attachments
    ):
        panel = eg.ConfigPanel()
        mail_panel = MailPanel(
            panel,
            country,
            carrier,
            phone_number,
            gateway,
            subject,
            message,
            'MMS'
        )
        panel.sizer.Add(mail_panel, 1, wx.EXPAND)

        attachment_st = panel.StaticText('File Attachments:')
        attachment_desc = panel.StaticText(
            'Right click to add/remove attachments'
        )
        attachment_ctrl = AttachmentsList(panel, attachments)

        attachment_sizer = wx.BoxSizer(wx.HORIZONTAL)
        attachment_sizer.Add(attachment_st, 0, wx.ALL, 5)
        attachment_sizer.Add(attachment_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(attachment_sizer, 1, wx.EXPAND)
        desc_sizer = wx.BoxSizer(wx.HORIZONTAL)
        desc_sizer.AddStretchSpacer()
        desc_sizer.Add(attachment_desc, 0, wx.ALL, 5)
        panel.sizer.Add(desc_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            country, carrier, phone_number, gateway, subject, message = (
                mail_panel.GetValues()
            )
            panel.SetResult(
                country,
                carrier,
                phone_number,
                gateway,
                subject,
                message,
                *attachment_ctrl.GetValue()
            )


class AttachmentsList(wx.ListBox):
    def __init__(
        self,
        parent,
        attachments,
    ):
        wx.ListBox.__init__(
            self,
            parent,
            choices=list(attachments),
            style=(
                wx.LB_EXTENDED |
                wx.LB_HSCROLL |
                wx.LB_NEEDED_SB
            )
        )

        self.typedText = ''
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.DeleteAttachment)
        self.Bind(wx.EVT_RIGHT_UP, self.EvtRightButton)
        menu = wx.Menu()

        def append_menu(label, func):
            menu_id = wx.NewIdRef()
            menu.Append(menu_id, label)
            self.Bind(wx.EVT_MENU, func, id=menu_id)

        append_menu('Add Attachment(s)', self.AddAttachment)
        menu.AppendSeparator()
        append_menu('Delete Attachment(s)', self.DeleteAttachment)
        append_menu('Delete All Attachments', self.DeleteAllAttachments)

        self.contextMenu = menu

    def AddAttachment(self, evt):
        dlg = wx.FileDialog(
            self,
            message="Choose a file",
            defaultDir=os.path.expanduser('~\\Documents'),
            defaultFile="",
            wildcard="All files (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.InsertItems(dlg.GetPaths(), self.GetCount())
            evt.Skip()
        dlg.Destroy()

    def DeleteAttachment(self, evt):
        selections = sorted(self.GetSelections())
        for selection in sorted(selections, reverse=True):
            self.Delete(selection)
        evt.Skip()

    def DeleteAllAttachments(self, evt):
        self.Clear()
        evt.Skip()

    def EvtRightButton(self, evt):
        self.PopupMenu(self.contextMenu)

    def FindPrefix(self, prefix):
        if prefix:
            prefix = prefix.lower()
            length = len(prefix)
            for x in range(self.GetCount()):
                text = self.GetString(x).lower()
                if text[:length] == prefix:
                    return x
        return -1

    def OnKey(self, evt):
        key = evt.GetKeyCode()

        if 32 <= key <= 127:
            self.typedText = self.typedText + chr(key)
            item = self.FindPrefix(self.typedText)
            if item != -1:
                self.SetSelection(item)

        elif key == wx.WXK_BACK:
            self.typedText = self.typedText[:-1]

            if not self.typedText:
                self.SetSelection(0)
            else:
                item = self.FindPrefix(self.typedText)
                if item != -1:
                    self.SetSelection(item)
        else:
            self.typedText = ''
            evt.Skip()

    def GetValue(self):
        return tuple(self.GetString(i) for i in range(self.GetCount()))

