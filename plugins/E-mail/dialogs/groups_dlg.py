# coding=utf8

from copy import deepcopy

import wx

import eg
from ..utils import move_item, validate_email_addr


class GroupsDialog(eg.Dialog):
    def __init__(self, parent, plugin, grps):
        eg.Dialog.__init__(
            self,
            parent=parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            title=plugin.text.groupsTitle,
            name="Groups dialog"
        )
        self.parent = parent
        self.plugin = plugin
        self.groups = deepcopy(grps)
        self.text = plugin.text
        self.old_grp_sel = -1
        self.old_adr_sel = -1

        self.SetMinSize((500, 400))
        self.create_widgets()
        self.create_sizers()
        self.btn_ok = self.FindWindowById(wx.ID_OK)
        self.init_lists()
        self.bindings()

    # noinspection PyAttributeOutsideInit
    def create_widgets(self):
        text = self.text
        self.listbox_lbl = wx.StaticText(self, wx.ID_ANY, text.groupsList)
        self.grp_list_ctrl = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.grp_edit_ctrl = wx.TextCtrl(self, wx.ID_ANY, u'', style=wx.TE_PROCESS_ENTER)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, (16, 16))
        self.grp_up = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.grp_up.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, (16, 16))
        self.grp_down = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.grp_down.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16, 16))
        self.grp_del = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.grp_del.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16))
        self.grp_add = wx.BitmapButton(self, wx.ID_ANY, bmp)

        self.addresses_lbl = wx.StaticText(self, wx.ID_ANY, text.outAddress)
        self.adr_list_ctrl = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.adr_edit_ctrl = wx.TextCtrl(self, wx.ID_ANY, u'', style=wx.TE_PROCESS_ENTER)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, (16, 16))
        self.adr_up = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.adr_up.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, (16, 16))
        self.adr_down = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.adr_down.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16, 16))
        self.adr_del = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.adr_del.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16))
        self.adr_add = wx.BitmapButton(self, wx.ID_ANY, bmp)

    def create_sizers(self):
        main_sizer = wx.GridBagSizer(hgap=5, vgap=10)
        main_sizer.Add(self.listbox_lbl, pos=(0, 0), flag=wx.EXPAND)
        main_sizer.Add(self.grp_list_ctrl, pos=(1, 0), span=(4, 1), flag=wx.EXPAND)
        main_sizer.Add(self.grp_edit_ctrl, pos=(5, 0), span=(1, 2), flag=wx.EXPAND)
        main_sizer.Add(self.grp_up, pos=(1, 1), flag=wx.ALIGN_BOTTOM)
        main_sizer.Add(self.grp_down, pos=(2, 1))
        main_sizer.Add(self.grp_del, pos=(3, 1))
        main_sizer.Add(self.grp_add, pos=(4, 1))

        main_sizer.Add(self.addresses_lbl, pos=(0, 2), flag=wx.EXPAND)
        main_sizer.Add(self.adr_list_ctrl, pos=(1, 2), span=(4, 1), flag=wx.EXPAND)
        main_sizer.Add(self.adr_edit_ctrl, pos=(5, 2), span=(1, 2), flag=wx.EXPAND)
        main_sizer.Add(self.adr_up, pos=(1, 3), flag=wx.ALIGN_BOTTOM)
        main_sizer.Add(self.adr_down, pos=(2, 3))
        main_sizer.Add(self.adr_del, pos=(3, 3))
        main_sizer.Add(self.adr_add, pos=(4, 3))

        main_sizer.AddGrowableCol(0, 1)
        main_sizer.AddGrowableCol(2, 3)
        main_sizer.AddGrowableRow(1, 1)
        main_sizer.SetFlexibleDirection(wx.BOTH)

        sep_btn_sizer = wx.StaticLine(self)
        std_btn_sizer = self.CreateStdDialogButtonSizer(flags=wx.OK | wx.CANCEL | wx.NO_DEFAULT)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 15)
        sizer.Add(sep_btn_sizer, 0, wx.EXPAND)
        sizer.Add(std_btn_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizerAndFit(sizer)

    def bindings(self):
        self.grp_edit_ctrl.Bind(wx.EVT_TEXT, self.on_grp_change)
        self.grp_list_ctrl.Bind(wx.EVT_LISTBOX, self.on_grp_clicked)
        self.grp_up.Bind(wx.EVT_BUTTON, self.on_grp_up)
        self.grp_down.Bind(wx.EVT_BUTTON, self.on_grp_down)
        self.grp_del.Bind(wx.EVT_BUTTON, self.on_grp_delete)
        self.grp_add.Bind(wx.EVT_BUTTON, self.on_grp_add)
        self.adr_edit_ctrl.Bind(wx.EVT_TEXT, self.on_adr_change)
        self.adr_list_ctrl.Bind(wx.EVT_LISTBOX, self.on_adr_clicked)
        self.adr_up.Bind(wx.EVT_BUTTON, self.on_adr_up)
        self.adr_down.Bind(wx.EVT_BUTTON, self.on_adr_down)
        self.adr_del.Bind(wx.EVT_BUTTON, self.on_adr_delete)
        self.adr_add.Bind(wx.EVT_BUTTON, self.on_adr_add)

    def init_lists(self):
        if len(self.groups) > 0:
            self.grp_list_ctrl.Set([n[0] for n in self.groups])
            self.grp_list_ctrl.SetSelection(0)
            self.set_value(self.groups[0])
            self.grp_up.Enable()
            self.grp_down.Enable()
            self.grp_del.Enable()
        else:
            self.grp_edit_ctrl.Disable()
            self.btn_ok.Disable()
            self.box_disable()

    def get_groups(self):
        return self.groups

    def box_disable(self):
        self.addresses_lbl.Disable()
        self.adr_list_ctrl.Disable()
        self.adr_edit_ctrl.Disable()
        self.adr_up.Disable()
        self.adr_down.Disable()
        self.adr_add.Disable()
        self.adr_del.Disable()

    def set_value(self, item):
        self.grp_edit_ctrl.ChangeValue(item[0])
        self.adr_list_ctrl.Set(item[1])
        if len(item[1]) == 0:
            self.adr_del.Disable()
            self.adr_up.Disable()
            self.adr_down.Disable()
        else:
            self.adr_list_ctrl.SetSelection(0)
            self.adr_edit_ctrl.ChangeValue(item[1][0])
            self.adr_del.Enable()
            flag = len(item[1]) > 1
            self.adr_up.Enable(flag)
            self.adr_down.Enable(flag)

    def validation(self, ):
        flag = True
        flag2 = True
        label = self.grp_edit_ctrl.GetValue()
        groups = self.grp_list_ctrl.GetStrings()
        if label == u'':
            flag = False
        if len(groups) > 0:
            for item in groups:
                if item == u'':
                    flag = False
            if groups.count(label) != 1:
                flag = False
        adr = self.adr_edit_ctrl.GetValue()
        addresses = self.adr_list_ctrl.GetStrings()
        if len(addresses) > 0:
            if adr == u'':
                flag2 = False
            for item in addresses:
                if item == u'':
                    flag2 = False
            if addresses.count(adr) != 1:
                flag2 = False
        if self.adr_edit_ctrl.HasFocus() and not validate_email_addr(adr):
            flag = False
        self.adr_add.Enable(flag)
        self.btn_ok.Enable(flag and flag2)
        self.grp_add.Enable(flag and flag2)

    def on_grp_change(self, evt):
        if self.groups:
            sel = self.old_grp_sel
            label = self.grp_edit_ctrl.GetValue().strip()
            self.groups[sel][0] = label
            self.grp_list_ctrl.Set([j[0] for j in self.groups])
            self.grp_list_ctrl.SetSelection(sel)
            self.validation()
        evt.Skip()

    # noinspection PyUnusedLocal
    def on_grp_clicked(self, evt):
        sel = self.grp_list_ctrl.GetSelection()
        if self.old_grp_sel != sel:
            flag = True
            for address in self.groups[self.old_grp_sel][1]:
                if not validate_email_addr(address):
                    flag = False
                    break
            label = self.grp_edit_ctrl.GetValue()
            if label.strip() != u"":
                if self.grp_list_ctrl.GetStrings().count(label) > 1:
                    flag = False
            if flag:
                self.old_grp_sel = sel
                item = self.groups[sel]
                self.set_value(item)
            self.grp_list_ctrl.SetSelection(self.old_grp_sel)
            self.grp_list_ctrl.SetFocus()

    def on_grp_up(self, evt):
        new_sel, self.groups = move_item(self.groups, self.grp_list_ctrl.GetSelection(), -1)
        self.grp_list_ctrl.Set([j[0] for j in self.groups])
        self.grp_list_ctrl.SetSelection(new_sel)
        self.old_grp_sel = new_sel
        evt.Skip()

    def on_grp_down(self, evt):
        new_sel, self.groups = move_item(self.groups, self.grp_list_ctrl.GetSelection(), 1)
        self.grp_list_ctrl.Set([j[0] for j in self.groups])
        self.grp_list_ctrl.SetSelection(new_sel)
        self.old_grp_sel = new_sel
        evt.Skip()

    def on_grp_delete(self, evt):
        lngth = len(self.groups)
        if lngth == 2:
            self. grp_up.Enable(False)
            self.grp_down.Enable(False)
        sel = self.grp_list_ctrl.GetSelection()
        if lngth == 1:
            self.groups = []
            self.grp_list_ctrl.Set([])
            item = ['', []]
            self.set_value(item)
            self.adr_edit_ctrl.ChangeValue('')
            self.grp_edit_ctrl.Enable(False)
            self.box_disable()
            self.adr_add.Enable(False)
            self.btn_ok.Enable(False)
            self.grp_del.Enable(False)
            self.grp_add.Enable(True)
            evt.Skip()
            return
        elif sel == lngth - 1:
            sel = 0
        self.old_grp_sel = sel
        self.groups.pop(self.grp_list_ctrl.GetSelection())
        self.grp_list_ctrl.Set([j[0] for j in self.groups])
        self.grp_list_ctrl.SetSelection(sel)
        item = self.groups[sel]
        self.set_value(item)
        evt.Skip()

    # noinspection PyUnusedLocal
    def on_grp_add(self, evt):
        if len(self.groups) >= 1:
            self.grp_up.Enable()
            self.grp_down.Enable()
        self.grp_edit_ctrl.Enable()
        self.box_disable()
        sel = self.grp_list_ctrl.GetSelection() + 1
        self.old_grp_sel = sel
        item = [u'', []]
        self.groups.insert(sel, item)
        self.grp_list_ctrl.Set([j[0] for j in self.groups])
        self.grp_list_ctrl.SetSelection(sel)
        self.set_value(item)
        self.grp_edit_ctrl.SetFocus()
        self.grp_add.Disable()
        self.grp_del.Enable()

    # noinspection PyUnusedLocal
    def on_adr_change(self, evt):
        sel = self.grp_list_ctrl.GetSelection()
        adr = self.adr_edit_ctrl.GetValue()
        pos = self.adr_list_ctrl.GetSelection()
        self.adr_list_ctrl.SetString(pos, adr)
        self.groups[sel][1][pos] = adr
        self.validation()

    def on_adr_clicked(self, evt):
        sel = evt.GetSelection()
        if sel == self.old_adr_sel:
            return

        adr = self.adr_edit_ctrl.GetValue()
        if not validate_email_addr(adr):
            wx.Bell()
            self.adr_list_ctrl.SetSelection(self.old_adr_sel)
            return

        self.old_adr_sel = sel
        self.adr_edit_ctrl.SetValue(self.adr_list_ctrl.GetStringSelection())

    def on_adr_up(self, evt):
        sel = self.old_adr_sel
        new_sel, self.groups[sel][1] = move_item(self.groups[sel][1], self.adr_list_ctrl.GetSelection(), -1)
        self.adr_list_ctrl.Set(self.groups[sel][1])
        self.adr_list_ctrl.SetSelection(new_sel)
        self.old_adr_sel = new_sel
        evt.Skip()

    def on_adr_down(self, evt):
        sel = self.old_adr_sel
        new_sel, self.groups[sel][1] = move_item(self.groups[sel][1], self.adr_list_ctrl.GetSelection(), 1)
        self.adr_list_ctrl.Set(self.groups[sel][1])
        self.adr_list_ctrl.SetSelection(new_sel)
        self.old_adr_sel = new_sel
        evt.Skip()

    def on_adr_delete(self, evt):
        sel = self.old_adr_sel
        sel2 = self.adr_list_ctrl.GetSelection()
        lngth = len(self.groups[sel][1])
        if lngth == 2:
            self.adr_up.Enable(False)
            self.adr_down.Enable(False)
        if lngth == 1:
            self.adr_edit_ctrl.ChangeValue('')
            self.groups[sel][1] = []
            self.adr_list_ctrl.Set([])
            self.adr_list_ctrl.SetStringSelection('')
            self.btn_ok.Enable(False)
            self.adr_del.Enable(False)
            self.adr_add.Enable(True)
            evt.Skip()
            return
        elif sel2 == lngth - 1:
            sel2 = 0
        self.old_adr_sel = sel2
        self.groups[sel][1].pop(self.adr_list_ctrl.GetSelection())
        self.adr_list_ctrl.Set(self.groups[sel][1])
        self.adr_list_ctrl.SetSelection(sel2)
        item = self.groups[sel][1][sel2]
        self.adr_edit_ctrl.ChangeValue(item)
        self.validation()
        evt.Skip()

    # noinspection PyUnusedLocal
    def on_adr_add(self, evt):
        sel = self.grp_list_ctrl.GetSelection()
        self.old_adr_sel = self.adr_list_ctrl.Append(u'')
        self.groups[sel][1].append(u'')
        self.adr_list_ctrl.SetSelection(self.old_adr_sel)
        addresses = self.adr_list_ctrl.GetStrings()
        if len(addresses) > 1:
            self.adr_up.Enable(True)
            self.adr_down.Enable(True)
        self.adr_edit_ctrl.Enable(True)
        self.addresses_lbl.Enable(True)
        self.adr_list_ctrl.Enable(True)
        self.adr_edit_ctrl.SetValue(u'')
        self.adr_edit_ctrl.SetFocus()
        self.adr_add.Enable(False)
        self.adr_del.Enable(True)
