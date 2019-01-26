# coding=utf8

import email
import time

import wx

from .send_mail_dlg import SendMailDlg
from ..utils import parse_address, run_email_client


class MessageFrame(wx.MiniFrame):
    def __init__(self, parent, message):
        wx.MiniFrame.__init__(
            self,
            parent=parent,
            id=wx.ID_ANY,
            title="Message",
            style=wx.CAPTION | wx.RESIZE_BORDER,
            name="Message Frame"
        )
        self.message = message
        self.setup = parent.setup
        self.parent = parent
        self.plugin = parent.plugin
        self.id = self.plugin.temp_data[self.message[3]][2][int(self.message[4][0]) - 1][0]
        text = self.plugin.text

        self.close_button = wx.Button(self, wx.ID_ANY, text.close)  # , size=(w, -1))
        self.reply_button = wx.Button(self, wx.ID_ANY, text.reply)  # , size=(w, -1))
        self.client_button = wx.Button(self, wx.ID_ANY, text.client)  # , size=(w, -1))
        self.delete_button = wx.Button(self, wx.ID_ANY, text.delete)  # , size=(w, -1))
        self.message_ctrl = wx.TextCtrl(
            self, wx.ID_ANY,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_AUTO_URL | wx.TE_RICH2
        )

        self.message_ctrl.Bind(wx.EVT_TEXT_URL, self.on_url_click)
        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        self.close_button.Bind(wx.EVT_BUTTON, self.on_close_button)
        self.client_button.Bind(wx.EVT_BUTTON, self.on_client_button)
        self.reply_button.Bind(wx.EVT_BUTTON, self.on_reply_button)
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_button)

        central_sizer = wx.GridBagSizer(10, 10)
        central_sizer.Add(self.message_ctrl, (0, 0), (1, 7), flag=wx.EXPAND)
        central_sizer.Add(self.delete_button, (1, 0), flag=wx.ALIGN_LEFT | wx.BOTTOM, border=10)
        central_sizer.Add(self.client_button, (1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL)
        central_sizer.Add(self.reply_button, (1, 4), flag=wx.ALIGN_CENTER_HORIZONTAL)
        central_sizer.Add(self.close_button, (1, 6), flag=wx.RIGHT)
        central_sizer.AddGrowableRow(0)
        central_sizer.AddGrowableCol(1)
        central_sizer.AddGrowableCol(3)
        central_sizer.AddGrowableCol(5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(central_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self.SetMinSize((550, 400))
        self.SetSize((550, 400))
        self.SetSizer(main_sizer)

    def show_message_frame(self, position, size):
        self.set_title()
        self.message_ctrl.SetValue(self.message[2])
        self.SetSize(size)
        self.SetPosition(position)
        self.Show()

    @staticmethod
    def on_url_click(evt):
        if evt.MouseEvent.LeftDown():
            url = evt.GetEventObject().GetValue()[evt.GetURLStart(): evt.GetURLEnd()]
            wx.LaunchDefaultBrowser(url)
        else:
            evt.Skip()

    def on_close_window(self, evt):
        self.parent.mess_fram_size = self.GetSize()
        self.parent.mess_fram_position = self.GetPosition()
        self.Destroy()
        evt.Skip()

    def on_close_button(self, evt):
        evt.Skip()
        self.Close(True)

    def on_client_button(self, evt):
        evt.Skip()
        run_email_client()

    def on_reply_button(self, evt):
        evt.Skip()
        address_list = [item[3] for item in self.plugin.configs]
        if self.message[8] in address_list:
            indx = address_list.index(self.message[8])
        else:
            indx = 0
        from_usr = [
            u"%s <%s> - %s" % (item[2], item[3], item[0]) for item in self.plugin.configs
        ][indx]
        sbjct = u"Re: " + self.message[0]
        repl_addr = email.utils.parseaddr(self.message[6])
        from_addr = email.utils.parseaddr(self.message[1])
        if repl_addr[1] != '':
            to = repl_addr[1]
        else:
            to = from_addr[1]
        if repl_addr[0] != '':
            to_name = parse_address(self.message[6])
        elif from_addr[0] != '':
            to_name = parse_address(self.message[1])
        else:
            to_name = ''
        body = self.message[2].split('\n')
        sender = parse_address(self.message[1])
        re_body = [self.plugin.text.wrote % sender, '']
        for line in body:
            re_body.append('> ' + line)
        re_body = u'\n'.join(re_body)

        my_dlg = SendMailDlg(parent=self)
        my_dlg.show_send_mail_dlg(
            subject=sbjct,
            from_adr=from_usr,
            to_adr=to,
            body=re_body,
            to_name=to_name,
            plugin=self.plugin,
            references=self.message[5],
            message_id=self.message[7]
        )

    def on_delete_button(self, evt):
        wx.CallAfter(self.parent.delete_emails, self.message[3], self.message[4], True)
        evt.Skip()
        time.sleep(0.2)
        self.parent.Refresh()
        self.Close(True)

    def get_email_num(self):
        return self.message[4][0]

    def set_title(self):
        title = ('%s-%s | %s: %s' % (
            self.setup[0],
            self.message[4][0],
            parse_address(self.message[1]),
            self.message[0]
        ))
        if len(title) > 68:
            title = title[:65] + '...'
        self.SetTitle(title)

    def unblock(self, unblock):
        if unblock:
            data = self.plugin.temp_data[self.message[3]][2]
            try:
                ix = [item[0] for item in data].index(self.id)
                self.message[4][0] = data[ix][4]
                self.set_title()
            except ValueError:
                self.Close(True)
            colour = self.GetForegroundColour()
        else:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self.message_ctrl.SetForegroundColour(colour)
        self.delete_button.Enable(unblock)
        self.client_button.Enable(unblock)
        self.close_button.Enable(unblock)
        self.Enable(unblock)
        self.Refresh()
