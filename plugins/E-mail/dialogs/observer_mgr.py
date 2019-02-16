# coding=utf8

import time

import wx


class ObservViewerDialog(wx.MiniFrame):
    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self, parent, -1,
            style=wx.CAPTION | wx.RESIZE_BORDER, name="Observations viewer/manager"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.observ_threads = plugin.observ_threads
        self.plugin = plugin

    def show_observ_viewer_dialog(self):
        text = self.plugin.text
        self.SetTitle(text.viewerTitle)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(
            wx.StaticText(self, -1, text.listhead),
            0, wx.TOP | wx.LEFT | wx.RIGHT, 10
        )

        central_sizer = wx.GridBagSizer(10, 10)
        observ_list_ctrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
        for i, colLabel in enumerate(text.colLabels):
            observ_list_ctrl.InsertColumn(
                i,
                colLabel,
                wx.LIST_FORMAT_RIGHT if (i == 1 or i == 2) else wx.LIST_FORMAT_LEFT
            )

        if int(wx.__version__.split('.', 1)[0]) < 4:
            observ_list_ctrl.InsertStringItem(0, text.colLabels[0])
            observ_list_ctrl.SetStringItem(0, 2, time.strftime("%c"))
        else:
            observ_list_ctrl.InsertItem(0, text.colLabels[0])
            observ_list_ctrl.SetItem(0, 2, time.strftime("%c"))
        size = 0
        for i in range(5):
            observ_list_ctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            size += observ_list_ctrl.GetColumnWidth(i)
        observ_list_ctrl.SetMinSize((size, -1))
        central_sizer.Add(observ_list_ctrl, (0, 0), (1, 5), flag=wx.EXPAND)
        # buttons
        abort_button = wx.Button(self, -1, text.buttons[0])
        abort_all_button = wx.Button(self, -1, text.buttons[1])
        refresh_button = wx.Button(self, -1, text.buttons[2])
        close_button = wx.Button(self, -1, text.buttons[3])
        central_sizer.Add(abort_button, (1, 0), flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)
        central_sizer.Add(abort_all_button, (1, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)
        central_sizer.Add(refresh_button, (1, 2), flag=wx.ALIGN_LEFT)
        central_sizer.Add(close_button, (1, 4), flag=wx.ALIGN_RIGHT)
        central_sizer.AddGrowableRow(0)
        central_sizer.AddGrowableCol(3)

        # noinspection PyUnusedLocal
        def fill_list_ctrl(event=None):
            observ_list_ctrl.DeleteAllItems()
            row = 0
            for j, item in enumerate(self.observ_threads):
                ot = self.observ_threads[item]
                if ot.isAlive() and not ot.is_aborted():
                    timestamp = time.strftime("%c", time.localtime(ot.last_check)) if ot.last_check != 0 else ''
                    if int(wx.__version__.split('.', 1)[0]) < 4:
                        observ_list_ctrl.InsertStringItem(row, ot.observ_name)
                        observ_list_ctrl.SetStringItem(row, 1, str(ot.setup[1]))
                        observ_list_ctrl.SetStringItem(row, 2, timestamp)
                        observ_list_ctrl.SetStringItem(row, 3, ot.setup[3])
                        observ_list_ctrl.SetStringItem(row, 4, ot.setup[12])
                    else:
                        observ_list_ctrl.InsertItem(row, ot.observ_name)
                        observ_list_ctrl.SetItem(row, 1, str(ot.setup[1]))
                        observ_list_ctrl.SetItem(row, 2, timestamp)
                        observ_list_ctrl.SetItem(row, 3, ot.setup[3])
                        observ_list_ctrl.SetItem(row, 4, ot.setup[12])
                    row += 1
            list_selection()

        def on_abort_button(event):
            item = observ_list_ctrl.GetFirstSelected()
            while item != -1:
                name = observ_list_ctrl.GetItemText(item)
                ot = self.observ_threads[name]
                if ot.isAlive():
                    ot.abort_observation()
                    time.sleep(0.25)
                item = observ_list_ctrl.GetNextSelected(item)
            fill_list_ctrl()
            event.Skip()

        def on_abort_all_button(event):
            thrds = list(enumerate(self.observ_threads))
            thrds.reverse()
            for j, name in thrds:
                ot = self.observ_threads[name]
                ot.abort_observation()
                time.sleep(0.25)
                fill_list_ctrl()
                self.Update()
            event.Skip()

        def on_close_button(event):
            self.Destroy()
            event.Skip()

        def list_selection(event=None):
            flag = observ_list_ctrl.GetFirstSelected() != -1
            abort_button.Enable(flag)
            if event:
                event.Skip()

        def on_size(event):
            observ_list_ctrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)
            event.Skip()

        fill_list_ctrl()
        self.SetMinSize((size + 52, 178))
        self.SetSize((size + 52, 178))
        abort_button.Bind(wx.EVT_BUTTON, on_abort_button)
        abort_all_button.Bind(wx.EVT_BUTTON, on_abort_all_button)
        refresh_button.Bind(wx.EVT_BUTTON, fill_list_ctrl)
        close_button.Bind(wx.EVT_BUTTON, on_close_button)
        observ_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, list_selection)
        observ_list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, list_selection)
        self.Bind(wx.EVT_SIZE, on_size)
        main_sizer.Add(central_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        main_sizer.Layout()
        self.SetSizerAndFit(main_sizer)
        self.Show()
