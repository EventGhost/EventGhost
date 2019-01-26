# coding=utf8

import wx

from ..threads import SendMailThread
from ..utils import validate_email_addr
from .compose_msg import ComposeMsg


# noinspection PyClassHasNoInit
class SendMailText:
    fromLabel = 'From:'
    toLabel = 'To:'
    copyLabel = 'Copy:'
    subjectLabel = 'Subject:'
    outText = "Text:"
    outTexts = "Append:"
    tip = 'Here can be expression as {eg.event.payload} too !'
    tip1 = "Recipient's Name (not obligatory)"
    tip2 = "Recipient's Address (obligatory)"
    tip3 = 'Send your e-mail now !'
    sendNow = 'Send now !'
    replyTitle = 'Reply'


class SendMailDlg(wx.MiniFrame, ComposeMsg):
    def __init__(self, parent):
        wx.MiniFrame.__init__(
            self,
            parent,
            size=(360, 270),
            style=wx.CAPTION | wx.RESIZE_BORDER,
            name='Send Email'
        )
        ComposeMsg.__init__(self)
        self.text = SendMailText
        self.plugin = None
        self.references = None
        self.message_id = None
        self.btn1 = None

    def show_send_mail_dlg(
        self,
        subject=u'',
        from_adr=u'',
        to_adr=u'',
        cc_adr=u'',
        body=u'',
        templates=u'',
        to_name=u'',
        plugin=None,
        references=None,
        message_id=None
    ):
        self.plugin = plugin
        self.references = references
        self.message_id = message_id
        text = self.text
        self.SetTitle(3 * ' ' + text.replyTitle)
        panel = self
        top_sizer = self.send_cfg(
            panel,
            subject,
            from_adr,
            to_adr,
            cc_adr,
            body,
            templates,
            to_name,
            text,
            plugin
        )

        line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self.btn1 = wx.Button(self, wx.ID_OK)
        self.btn1.SetLabel(text.sendNow)
        self.btn1.Disable()
        self.btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(plugin.text.cancel)

        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(self.btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1, 10))
        sizer.Add(top_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 16)
        sizer.Add((1, 5))
        sizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        sizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 12)
        sizer.Add((1, 5))
        self.SetMinSize((550, 400))
        self.SetSize((550, 400))
        self.SetSizer(sizer)

        self.to_ctrl.Bind(wx.EVT_TEXT, self.validation)
        self.body_ctrl.Bind(wx.EVT_TEXT, self.validation)
        self.subject_ctrl.Bind(wx.EVT_TEXT, self.validation)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        btn2.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.btn1.Bind(wx.EVT_BUTTON, self.on_send)
        self.validation()
        self.Show()

    def validation(self, evt=None):
        if evt:
            evt.Skip()
        flag = True
        if not validate_email_addr(self.to_ctrl.GetValue()):
            flag = False
        if self.subject_ctrl.GetValue() == '':
            flag = False
        if self.body_ctrl.GetValue() == '':
            flag = False
        self.btn1.Enable(flag)

    def on_send(self, evt):
        evt.Skip()
        t = SendMailThread(
            self.plugin,
            self.subject_ctrl.GetValue(),
            self.from_ctrl.GetStringSelection(),
            self.to_ctrl.GetValue(),
            self.cc_ctrl.GetStringSelection(),
            self.body_ctrl.GetValue(),
            self.templates_ctrl.GetValue(),
            self.to_name_ctrl.GetValue(),
            self.references,
            self.message_id
        )
        t.start()
        self.Close()

    def on_close(self, evt):
        evt.Skip()
        self.Destroy()

    def on_cancel(self, evt):
        evt.Skip()
        self.Close()
