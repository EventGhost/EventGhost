# coding=utf8

import wx

from eg.WinApi.Dynamic import BringWindowToTop, SetEvent
from ..utils import run_email_client
from .details_frame import DetailsFrame


class NotifFrame(wx.MiniFrame):
    details_frame = None
    detFramePosition = (-1, -1)
    detFrameSize = (-1, -1)

    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(self, parent, style=wx.STAY_ON_TOP | wx.CAPTION)
        self.plugin = plugin
        self.text = plugin.text
        self.setup = None

        self.number_lbl = wx.StaticText(self, label=u'')
        waiting_lbl = wx.StaticText(self, label=self.text.notifLabel)
        font = self.number_lbl.GetFont()
        font.SetPointSize(20)
        self.number_lbl.SetFont(font)
        self.SetToolTip(wx.ToolTip(self.text.tip0))
        self.number_lbl.SetToolTip(wx.ToolTip(self.text.tip0))
        waiting_lbl.SetToolTip(wx.ToolTip(self.text.tip0))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.number_lbl, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(waiting_lbl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        self.SetSizerAndFit(sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)
        self.number_lbl.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)
        waiting_lbl.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_click)
        self.number_lbl.Bind(wx.EVT_RIGHT_UP, self.on_right_click)
        waiting_lbl.Bind(wx.EVT_RIGHT_UP, self.on_right_click)

    def show_notif_frame(
        self,
        stp,
        event=None
    ):
        self.setup = stp
        self.SetTitle('  ' + stp[0])
        self.SetBackgroundColour(stp[9])
        self.SetForegroundColour(stp[10])
        SetEvent(event)

    def on_close_window(self, evt):
        if self.details_frame:
            self.details_frame.disappear()
        self.Destroy()
        evt.Skip()

    def on_double_click(self, evt):
        if evt.ControlDown():  # with CTRL
            run_email_client()
        else:  # without CTRL
            if self.details_frame:
                BringWindowToTop(self.details_frame.GetHandle())
            else:
                self.details_frame = DetailsFrame(parent=self)
                wx.CallAfter(
                    self.details_frame.show_details_frame,
                    position=self.detFramePosition,
                    size=self.detFrameSize
                )
            wx.CallAfter(self.details_frame.refresh_list)

    def on_right_click(self, evt):
        evt.Skip()
        if self.details_frame:
            self.details_frame.disappear()
        self.Hide()

    def disappear(self, close=False):
        if self.details_frame:
            self.details_frame.disappear()
        if not close:
            self.Hide()
        else:
            self.Close()

    def get_number(self):
        return int(self.number_lbl.GetLabel())

    def set_number(self, label=""):
        lbl = str(label)
        self.number_lbl.SetLabel(lbl)
        if self.details_frame:
            wx.CallAfter(self.details_frame.refresh_list)
        self.Fit()
        self.Refresh()
        self.Update()
