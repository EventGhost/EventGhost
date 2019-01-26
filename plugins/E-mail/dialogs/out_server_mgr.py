# coding=utf8


import wx
from wx.lib.intctrl import IntCtrl

import eg
from ..utils import move_item


class OutServerDialog(eg.Dialog):
    def __init__(self, parent, plugin, servers, pass_smtp, cfgs, val):
        self.text = text = plugin.text
        eg.Dialog.__init__(
            self,
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            title=text.outServerTitle,
            name="Servers dialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.pass_smtp = pass_smtp
        self.servers = servers
        self.cfgs = cfgs
        self.selected_in_cfg = val
        self.oldSel = 0

        self.create_widgets()
        self.create_sizers()
        self.btn_ok = self.FindWindowById(wx.ID_OK)
        self.bindings()

        if len(self.servers) > 0:
            self.server_list_ctrl.Set([n[0] for n in self.servers])
            self.server_list_ctrl.SetSelection(0)
            self.set_value(self.servers[0])
            self.oldSel = 0
            self.btn_up.Enable()
            self.btn_down.Enable()
            self.btn_del.Enable()
            self.on_checkbox()
        else:
            self.box_enable(False)
            self.btn_ok.Disable()
            self.btn_add.Enable()
            self.user_ctrl.Disable()
            self.user_lbl.Disable()
            self.passw_ctrl.Disable()
            self.passw_lbl.Disable()

    def get_servers(self):
        return self.servers

    def get_pass_smtp(self):
        return self.pass_smtp

    def get_string_for_selection(self):
        return self.selected_in_cfg

    def box_enable(self, enable):
        self.server_edit_ctrl.Enable(enable)
        self.out_server_lbl.Enable(enable)
        self.out_server_ctrl.Enable(enable)
        self.out_port_lbl.Enable(enable)
        self.out_port_ctrl.Enable(enable)
        self.choice_secure_lbl.Enable(enable)
        self.choice_secure_ctrl.Enable(enable)
        self.use_secure_ctrl.Enable(enable)

    def set_value(self, item):
        self.server_edit_ctrl.ChangeValue(item[0])
        self.out_server_ctrl.SetValue(item[1])
        self.out_port_ctrl.SetValue(item[2])
        self.choice_secure_ctrl.SetSelection(item[3])
        self.use_secure_ctrl.SetValue(item[4])
        self.user_ctrl.SetValue(item[5])
        if item[0] != u'' and item[0] in self.pass_smtp:
            self.passw_ctrl.ChangeValue(str(self.pass_smtp[item[0]]))
        else:
            self.passw_ctrl.ChangeValue(u'')

    def validation(self):
        flag = True
        label = self.server_edit_ctrl.GetValue()
        if label == "":
            flag = False
        else:
            if [j[0] for j in self.servers].count(label) != 1:
                flag = False
        if self.out_server_ctrl.GetValue() == '':
            flag = False
        if self.out_port_ctrl.GetValue() < 0:
            flag = False
        if self.use_secure_ctrl.GetValue():
            if self.user_ctrl.GetValue() == '' or self.passw_ctrl.GetValue() == '':
                flag = False
        self.btn_ok.Enable(flag)
        self.btn_add.Enable(flag)

    # noinspection PyUnusedLocal
    def on_ok(self, evt):
        # self.servers = self.servers
        # self.cfgs = self.cfgs
        # self.pass_smtp = self.pass_smtp
        # self.server_list_ctrl.Clear()
        # self.server_list_ctrl.AppendItems([j[0] for j in self.servers])
        # self.server_list_ctrl.SetStringSelection(self.val)
        self.validation()
        evt.Skip()

    # noinspection PyUnusedLocal
    def on_label_and_password(self, evt):
        if not self.servers:
            return
        srvrs = [item[8] for item in self.cfgs]
        old_lbl = self.server_list_ctrl.GetStringSelection()
        sel = self.oldSel
        label = self.server_edit_ctrl.GetValue().strip()
        val = self.passw_ctrl.GetValue()
        if val != u'':
            self.pass_smtp[label] = val
        self.servers[sel][0] = label
        if self.server_list_ctrl.GetStrings().count(old_lbl) == 1:
            if old_lbl in srvrs:
                if self.selected_in_cfg == old_lbl:
                    self.selected_in_cfg = label
                for item in self.cfgs:
                    if item[8] == old_lbl:
                        item[8] = label
        self.server_list_ctrl.Set([j[0] for j in self.servers])
        self.server_list_ctrl.SetSelection(sel)
        self.validation()

    # noinspection PyUnusedLocal
    def on_server_name(self, evt):
        if not self.servers:
            return
        val = self.out_server_ctrl.GetValue().strip()
        sel = self.oldSel
        self.servers[sel][1] = val
        self.validation()

    # noinspection PyUnusedLocal
    def on_port(self, evt):
        if not self.servers:
            return
        val = self.out_port_ctrl.GetValue()
        sel = self.oldSel
        self.servers[sel][2] = val
        self.validation()

    # noinspection PyUnusedLocal
    def on_ssl(self, evt):
        if not self.servers:
            return
        ports = (25, 587, 587, 465)
        val = self.choice_secure_ctrl.GetSelection()
        port = ports[val]
        self.out_port_ctrl.SetValue(port)
        sel = self.oldSel
        self.servers[sel][2] = port
        self.servers[sel][3] = val
        self.validation()

    def on_checkbox(self, evt=None):
        if evt:
            evt.Skip()
        val = self.use_secure_ctrl.GetValue()
        sel = self.oldSel
        self.servers[sel][4] = val
        self.user_ctrl.Enable(val)
        self.user_lbl.Enable(val)
        self.passw_ctrl.Enable(val)
        self.passw_lbl.Enable(val)
        if not val:
            self.user_ctrl.SetValue('')
            self.passw_ctrl.SetValue('')
        self.validation()

    # noinspection PyUnusedLocal,PyUnusedLocal
    def on_user(self, evt):
        if not self.servers:
            return
        val = self.user_ctrl.GetValue().strip()
        sel = self.oldSel
        self.servers[sel][5] = val
        self.validation()

    # noinspection PyUnusedLocal
    def on_click(self, evt):
        sel = self.server_list_ctrl.GetSelection()
        label = self.server_edit_ctrl.GetValue()
        if label.strip() != u'':
            if [j[0] for j in self.servers].count(label) == 1:
                self.oldSel = sel
                item = self.servers[sel]
                self.set_value(item)
        self.server_list_ctrl.SetSelection(self.oldSel)
        self.server_list_ctrl.SetFocus()
        val = self.servers[sel][4]
        self.user_ctrl.Enable(val)
        self.user_lbl.Enable(val)
        self.passw_ctrl.Enable(val)
        self.passw_lbl.Enable(val)
        self.validation()

    # noinspection PyUnusedLocal
    def on_button_up(self, evt):
        new_sel, self.servers = move_item(self.servers, self.server_list_ctrl.GetSelection(), -1)
        self.server_list_ctrl.Set([j[0] for j in self.servers])
        self.server_list_ctrl.SetSelection(new_sel)
        self.oldSel = new_sel

    # noinspection PyUnusedLocal
    def on_button_down(self, evt):
        new_sel, self.servers = move_item(self.servers, self.server_list_ctrl.GetSelection(), 1)
        self.server_list_ctrl.Set([j[0] for j in self.servers])
        self.server_list_ctrl.SetSelection(new_sel)
        self.oldSel = new_sel

    # noinspection PyUnusedLocal
    def on_button_delete(self, evt):
        srvrs = [item[8] for item in self.cfgs]
        val = self.server_list_ctrl.GetStringSelection()
        if val in srvrs:
            wx.MessageBox(
                self.text.deleteServer % val,
                eg.APP_NAME,
                wx.OK | wx.ICON_EXCLAMATION
            )
            return
        sel = self.server_list_ctrl.GetSelection()
        lngth = len(self.servers)
        if lngth == 2:
            self.btn_up.Enable(False)
            self.btn_down.Enable(False)
        if lngth == 1:
            self.servers = []
            self.server_list_ctrl.Set([])
            item = ['', '', 25, 0, False, '']
            self.set_value(item)
            self.box_enable(False)
            self.btn_ok.Enable(False)
            self.btn_del.Enable(False)
            self.btn_add.Enable(True)
            self.user_ctrl.Enable(False)
            self.user_lbl.Enable(False)
            self.passw_ctrl.Enable(False)
            self.passw_lbl.Enable(False)
            return
        elif sel == lngth - 1:
            sel = 0
        self.oldSel = sel
        self.servers.pop(self.server_list_ctrl.GetSelection())
        self.server_list_ctrl.Set([j[0] for j in self.servers])
        self.server_list_ctrl.SetSelection(sel)
        item = self.servers[sel]
        self.set_value(item)
        self.on_checkbox()

    # noinspection PyUnusedLocal
    def on_button_append(self, evt):
        if len(self.servers) == 1:
            self.btn_up.Enable(True)
            self.btn_down.Enable(True)
        self.box_enable(True)
        sel = self.server_list_ctrl.GetSelection() + 1
        self.oldSel = sel
        item = ['', '', 25, 0, False, '']
        self.servers.insert(sel, item)
        self.server_list_ctrl.Set([j[0] for j in self.servers])
        self.server_list_ctrl.SetSelection(sel)
        self.set_value(item)
        self.server_edit_ctrl.SetFocus()
        self.btn_add.Enable(False)
        self.btn_del.Enable(True)
        self.on_checkbox()

    def bindings(self):
        # self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        self.server_edit_ctrl.Bind(wx.EVT_TEXT, self.on_label_and_password)
        self.passw_ctrl.Bind(wx.EVT_TEXT, self.on_label_and_password)
        self.out_server_ctrl.Bind(wx.EVT_TEXT, self.on_server_name)
        self.out_port_ctrl.Bind(wx.EVT_TEXT, self.on_port)
        self.choice_secure_ctrl.Bind(wx.EVT_CHOICE, self.on_ssl)
        self.use_secure_ctrl.Bind(wx.EVT_CHECKBOX, self.on_checkbox)
        self.user_ctrl.Bind(wx.EVT_TEXT, self.on_user)
        self.server_list_ctrl.Bind(wx.EVT_LISTBOX, self.on_click)
        self.btn_up.Bind(wx.EVT_BUTTON, self.on_button_up)
        self.btn_down.Bind(wx.EVT_BUTTON, self.on_button_down)
        self.btn_del.Bind(wx.EVT_BUTTON, self.on_button_delete)
        self.btn_add.Bind(wx.EVT_BUTTON, self.on_button_append)

    def create_sizers(self):
        server_sizer_l = wx.BoxSizer(wx.VERTICAL)
        server_sizer_l.Add(self.out_server_lbl, 0, wx.EXPAND)
        server_sizer_l.Add(self.out_server_ctrl, 0, wx.EXPAND)

        server_sizer_r = wx.BoxSizer(wx.VERTICAL)
        server_sizer_r.Add(self.out_port_lbl, 0, wx.LEFT, 3)
        server_sizer_r.Add(self.out_port_ctrl, 0)

        server_sizer = wx.BoxSizer(wx.HORIZONTAL)
        server_sizer.Add(server_sizer_l, 1, wx.EXPAND)
        server_sizer.Add(server_sizer_r, 0, wx.LEFT, 5)

        box = wx.StaticBox(self, label=self.text.servParam)
        right_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        right_sizer.Add(self.choice_secure_lbl, 0, wx.TOP, 5)
        right_sizer.Add(self.choice_secure_ctrl, 0, wx.EXPAND | wx.TOP, 3)
        right_sizer.Add(server_sizer, 0, wx.EXPAND | wx.TOP, 10)
        right_sizer.Add(self.use_secure_ctrl, 0, wx.TOP, 16)
        right_sizer.Add(self.user_lbl, 0, wx.TOP, 5)
        right_sizer.Add(self.user_ctrl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)
        right_sizer.Add(self.passw_lbl, 0, wx.TOP, 5)
        right_sizer.Add(self.passw_ctrl, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)
        right_sizer.Add((1, 3))

        left_sizer = wx.GridBagSizer(hgap=5, vgap=10)
        left_sizer.Add(self.server_list_lbl, pos=(0, 0), flag=wx.EXPAND)
        left_sizer.Add(self.server_list_ctrl, pos=(1, 0), span=(4, 1), flag=wx.EXPAND)
        left_sizer.Add(self.server_edit_ctrl, pos=(5, 0), span=(1, 2), flag=wx.EXPAND)
        left_sizer.Add(self.btn_up, pos=(1, 1), flag=wx.ALIGN_BOTTOM)
        left_sizer.Add(self.btn_down, pos=(2, 1))
        left_sizer.Add(self.btn_del, pos=(3, 1))
        left_sizer.Add(self.btn_add, pos=(4, 1))
        left_sizer.AddGrowableCol(0, 1)
        left_sizer.AddGrowableRow(1, 1)
        left_sizer.SetFlexibleDirection(wx.BOTH)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_sizer, 1, wx.EXPAND | wx.LEFT, 10)
        main_sizer.Add(right_sizer, 2, wx.LEFT | wx.RIGHT | wx.TOP, 14)

        sep_btn_sizer = wx.StaticLine(self)
        std_btn_sizer = self.CreateStdDialogButtonSizer(flags=wx.OK | wx.CANCEL | wx.NO_DEFAULT)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 15)
        sizer.Add(sep_btn_sizer, 0, wx.EXPAND)
        sizer.Add(std_btn_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizerAndFit(sizer)

    # noinspection PyAttributeOutsideInit
    def create_widgets(self):
        text = self.text
        self.server_list_lbl = wx.StaticText(self, wx.ID_ANY, text.serversList)
        self.server_list_ctrl = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.server_edit_ctrl = wx.TextCtrl(self)
        self.out_server_lbl = wx.StaticText(self, label=text.outServer)
        self.out_server_ctrl = wx.TextCtrl(self)
        self.out_port_lbl = wx.StaticText(self, label=text.incPort)
        self.out_port_ctrl = IntCtrl(self, value=25)
        self.choice_secure_lbl = wx.StaticText(self, label=text.secureConnectLabel)
        self.choice_secure_ctrl = wx.Choice(self, choices=text.secureConnectChoice2)
        self.use_secure_ctrl = wx.CheckBox(self, label=text.useName)
        self.user_lbl = wx.StaticText(self, label=text.userLogin)
        self.user_ctrl = wx.TextCtrl(self)
        self.passw_lbl = wx.StaticText(self, label=text.userPassword)
        # self.passw_ctrl = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.passw_ctrl = eg.PasswordCtrl(self)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, (16, 16))
        self.btn_up = wx.BitmapButton(self, -1, bmp)
        self.btn_up.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, (16, 16))
        self.btn_down = wx.BitmapButton(self, -1, bmp)
        self.btn_down.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16, 16))
        self.btn_del = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.btn_del.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16))
        self.btn_add = wx.BitmapButton(self, wx.ID_ANY, bmp)
