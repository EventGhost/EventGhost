# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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

import wx
import os
# Local imports
import eg
from . import codes_panel
from . import device_panel
from .utils import h_sizer
from . import decoders
import threading

ICON = eg.Icons.PathIcon(os.path.join(os.path.dirname(__file__), 'remote.png'))


class Config(eg.PersistentData):
    size = (-1, -1)
    position = None


class LearnDialog(wx.Dialog):

    def __init__(self, plugin):
        wx.Dialog.__init__(
            self,
            eg.mainFrame,
            -1,
            'MCE Vista+: Learn Code',
            style=wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
        )

        device_ctrl = device_panel.DevicePanel(self, plugin)
        count_label = wx.StaticText(self, -1, 'Correctness Count:')
        count_ctrl = eg.SpinIntCtrl(self, -1, value=3, min=1, max=10)
        count_sizer = h_sizer(count_label, count_ctrl)

        timeout_label = wx.StaticText(self, -1, 'Learn Timeout:')
        timeout_ctrl = eg.SpinIntCtrl(self, -1, value=10, min=1, max=120)
        timeout_sizer = h_sizer(timeout_label, timeout_ctrl)

        eg.EqualizeWidths((count_label, timeout_label))

        code_ctrl = codes_panel.CodePanel(self)

        size = (450, 300)

        self.buttonRow = eg.ButtonRow(
            self,
            (wx.ID_OK, wx.ID_CANCEL),
            True
        )
        test_button = wx.Button(self, -1, eg.text.General.test)
        start_button = wx.Button(self, -1, 'Start')
        self.buttonRow.Add(start_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 6)
        self.buttonRow.Add(test_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 6)
        test_button.Enable(False)
        self.buttonRow.okButton.Enable(False)
        self.code = None
        self.event = threading.Event()

        def on_test_button(_):
            if self.code is not None:
                device = device_ctrl.GetValue()
                device.transmit(self.code.normalized_rlc, self.code.frequency)

        def on_start_button(_):
            def _do():
                start_button.Enable(False)

                device = device_ctrl.GetValue()
                count = count_ctrl.GetValue()
                timeout = timeout_ctrl.GetValue()

                good_codes = []

                while True:
                    if self.event.is_set():
                        return

                    frequency, data = device.learn(timeout, self.event)
                    code = decoders.IrDecoder.decode(data, len(data), frequency)
                    for g_codes in good_codes:
                        for g_code in g_codes:
                            if g_code == code:
                                g_codes += [code]
                                break
                        else:
                            continue

                        break
                    else:
                        good_codes += [[code]]

                    for g_codes in good_codes:
                        if len(g_codes) == count:
                            break
                    else:
                        continue

                    break

                self.code = code

                start_button.Enable(True)
                test_button.Enable(True)

                self.buttonRow.okButton.Enable(True)

            t = threading.Thread(target=_do)
            t.daemon = True
            t.start()

        test_button.Bind(wx.EVT_BUTTON, on_test_button)
        start_button.Bind(wx.EVT_BUTTON, on_start_button)

        self.buttonRow.testButton = test_button

        self.Bind(wx.EVT_MAXIMIZE, self.on_maximize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.headerBox = eg.HeaderBox(
            self,
            'Learn Code',
            'Learn a new IR Code',
            ICON,
            None
        )
        mainSizer.SetMinSize(size)
        mainSizer.AddMany(
            (
                (self.headerBox, 0, wx.EXPAND, 0),
                (wx.StaticLine(self), 0, wx.EXPAND | wx.ALIGN_CENTER, 0),
                (device_ctrl, 0, wx.EXPAND | wx.ALL, 5),
                (h_sizer(count_sizer, timeout_sizer), 0, wx.ALL, 5),
                (code_ctrl, 1, wx.EXPAND | wx.ALL, 5)
            )
        )
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND, 0)

        self.mainSizer = mainSizer
        self.SetSizer(self.mainSizer)

        if Config.position is None:
            self.CentreOnParent()
        else:
            self.SetPosition(Config.position)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_close)
        self.SetSize(Config.size)

    def on_close(self, evt):
        size = self.GetSize()
        pos = self.GetPosition()
        Config.size = (size[0], size[1])
        Config.position = (pos[0], pos[1])
        self.event.set()
        evt.Skip()

    @eg.LogIt
    def on_maximize(self, event):
        if self.buttonRow.sizeGrip:
            self.buttonRow.sizeGrip.Hide()
        self.Bind(wx.EVT_SIZE, self.on_restore)
        event.Skip()

    @eg.LogIt
    def on_restore(self, event):
        if not self.IsMaximized():
            self.Unbind(wx.EVT_SIZE)
            if self.buttonRow.sizeGrip:
                self.buttonRow.sizeGrip.Show()
        event.Skip()

    def GetValue(self):
        return self.code
