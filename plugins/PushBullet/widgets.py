# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2015  Pako <lubos.ruckl@gmail.com>
#
# This file is part of the PushBullet plugin for EventGhost.
#


from base64 import b64decode, b64encode
from copy import deepcopy
from cStringIO import StringIO
from math import sqrt
from os.path import abspath, dirname, exists, join
from time import strftime

import wx
import wx.adv
import wx.grid as gridlib
from PIL import Image
from wx.lib.buttons import GenButton
from wx.lib.statbmp import GenStaticBitmap

import eg
from eg.WinApi.Dynamic import BringWindowToTop
from eg.WinApi.Utils import GetMonitorDimensions
from .utils import fluffy_circle_mask, get_nm_nr, image_to_pil, resize, SEP, wrap


SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ICON_DIR = join(abspath(dirname(__file__.decode('mbcs'))), "icons")
AVATAR = (
    "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"
)


def align_center(width, offset):
    return (width / 2) + offset


def align_left(_, offset):
    return offset


def align_right(width, offset):
    return width - offset


ALIGNMENT_FUNCS = (
    (align_left, align_left),  # Top Left
    (align_right, align_left),  # Top Right
    (align_left, align_right),  # Bottom Left
    (align_right, align_right),  # Bottom Right
    (align_center, align_center),  # Screen Center
    (align_center, align_right),  # Bottom Center
    (align_center, align_left),  # Top Center
    (align_left, align_center),  # Left Center
    (align_right, align_center),  # Right Center
)


class StaticBitmap(GenStaticBitmap):
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        if self._bitmap:
            dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
            dc.Clear()
            dc.DrawBitmap(self._bitmap, 0, 0, True)


class PushGroupDialog(wx.Frame):
    oldSel = 0

    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION | wx.RESIZE_BORDER,
            name="Push group dialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.plugin = plugin
        self.groups = deepcopy(self.panel.push_groups)

    def show_push_groups_dlg(self):
        text = self.plugin.text
        self.SetTitle(text.pushGroupsTitle)
        sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer = wx.FlexGridSizer(4, 2, 2, 8)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        top_middle_sizer = wx.BoxSizer(wx.VERTICAL)
        preview_lbl = wx.StaticText(self, -1, text.groupsList)
        list_box_ctrl = wx.ListBox(
            self, -1,
            style=wx.LB_SINGLE | wx.LB_NEEDED_SB
        )
        label_lbl = wx.StaticText(self, -1, text.groupLabel)
        label_ctrl = wx.TextCtrl(self, -1, '')
        left_sizer.Add(preview_lbl, 0, wx.TOP, 5)
        left_sizer.Add((1, 1))
        left_sizer.Add(list_box_ctrl, 1, wx.TOP | wx.EXPAND, 1)
        left_sizer.Add(top_middle_sizer, 0, wx.TOP, 1)
        left_sizer.Add(label_lbl, 0, wx.TOP, 3)
        left_sizer.Add((1, 1))
        left_sizer.Add(label_ctrl, 0, wx.EXPAND)
        left_sizer.Add((1, 1))
        left_sizer.AddGrowableCol(0)
        left_sizer.AddGrowableRow(1)

        w1 = self.GetFullTextExtent(text.delete)[0]
        w2 = self.GetFullTextExtent(text.insert)[0]
        w = max(w1, w2) + 24
        btn_app = wx.Button(self, -1, text.insert, size=(w, -1))
        btn_del = wx.Button(self, -1, text.delete, size=(w, -1))
        btn_del.Enable(False)
        top_middle_sizer.Add(btn_app)
        top_middle_sizer.Add(btn_del, 0, wx.TOP, 5)

        tmp = []
        for t in self.plugin.targets:
            tmp.append([t[0], t[1], t[2], False])
        items = [n[0] for n in tmp]
        ts_ctrl = wx.CheckListBox(
            self,
            -1,
            choices=items,
        )
        right_sizer.Add(ts_ctrl, 1, wx.EXPAND)

        def evt_check_list_box(event):
            index = event.GetSelection()
            # label = ts_ctrl.GetString(index)
            tmp_lst = [list(itm) for itm in self.plugin.targets]
            for i, item in enumerate(tmp_lst):
                tmp_lst[i].append(ts_ctrl.IsChecked(i))
            self.groups[self.oldSel][1] = tmp_lst
            ts_ctrl.SetSelection(index)  # so that (un)checking also selects (moves the highlight)
            validation()

        ts_ctrl.Bind(wx.EVT_CHECKLISTBOX, evt_check_list_box)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_sizer, 1, wx.EXPAND)
        main_sizer.Add(right_sizer, 1, wx.EXPAND | wx.LEFT, 10)
        sizer.Add(main_sizer, 1, wx.ALL | wx.EXPAND, 10)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        sizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        sizer.Add((1, 5))
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())

        def set_value(item):
            label_ctrl.ChangeValue(item[0])
            ts = item[1]
            tmp_lst = []
            lst_1 = [i[1] for i in ts]
            for ix, target in enumerate(self.plugin.targets):
                tmp_lst.append(list(target))
                if target[1] in lst_1:
                    iy = lst_1.index(target[1])
                    tmp_lst[ix].append(ts[iy][3])
                else:
                    tmp_lst[ix].append(False)
                ts_ctrl.Check(ix, tmp_lst[ix][3])
            ts_ctrl.Enable(True)

        if len(self.groups) > 0:
            list_box_ctrl.Set([n[0] for n in self.groups])
            list_box_ctrl.SetSelection(0)
            set_value(self.groups[0])
            self.oldSel = 0
            btn_del.Enable(True)
        else:
            label_lbl.Enable(False)
            label_ctrl.Enable(False)
            btn1.Enable(False)
            ts_ctrl.Enable(False)

        sizer.Layout()
        # self.MakeModal(True)
        self.SetFocus()
        self.Center()
        self.Show()

        def on_close(evt):
            # self.MakeModal(False)
            self.GetParent().GetParent().Raise()
            self.Destroy()
            evt.Skip()

        self.Bind(wx.EVT_CLOSE, on_close)

        def on_cancel(evt):
            self.Close()
            evt.Skip()

        btn2.Bind(wx.EVT_BUTTON, on_cancel)

        def on_ok(evt):
            self.panel.push_groups = self.groups
            self.Close()
            evt.Skip()

        btn1.Bind(wx.EVT_BUTTON, on_ok)

        def validation():
            while True:
                flag = True
                label = label_ctrl.GetValue()
                if label == '':
                    flag = False
                if len(self.groups) > 0:
                    strings = list_box_ctrl.GetStrings()
                    for lbl in strings:
                        if lbl == '':
                            flag = False
                            break
                    if strings.count(label) != 1:
                        flag = False
                        break
                # sel = self.oldSel
                break
            btn1.Enable(flag)
            btn_app.Enable(flag)

        def on_txt_change(evt):
            if self.groups:
                sel = self.oldSel
                label = label_ctrl.GetValue()
                self.groups[sel][0] = label
                list_box_ctrl.Set([grp[0] for grp in self.groups])
                list_box_ctrl.SetSelection(sel)
                validation()
            evt.Skip()

        label_ctrl.Bind(wx.EVT_TEXT, on_txt_change)

        # noinspection PyUnusedLocal
        def on_click(evt):
            sel = list_box_ctrl.GetSelection()
            if self.oldSel != sel:
                self.oldSel = sel
                item = self.groups[sel]
                set_value(item)
                list_box_ctrl.SetSelection(self.oldSel)
                list_box_ctrl.SetFocus()
            # evt.Skip()

        list_box_ctrl.Bind(wx.EVT_LISTBOX, on_click)

        def on_button_delete(evt):
            lngth = len(self.groups)
            sel = list_box_ctrl.GetSelection()
            if lngth == 1:
                self.groups = []
                list_box_ctrl.Set([])
                item = ['', []]
                set_value(item)
                label_lbl.Enable(False)
                label_ctrl.Enable(False)
                ts_ctrl.Enable(False)
                btn1.Enable(True)
                btn_del.Enable(False)
                btn_app.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            # tmp = self.groups.pop(list_box_ctrl.GetSelection())
            list_box_ctrl.Set([grp[0] for grp in self.groups])
            list_box_ctrl.SetSelection(sel)
            item = self.groups[sel]
            set_value(item)
            validation()
            evt.Skip()

        btn_del.Bind(wx.EVT_BUTTON, on_button_delete)

        def on_button_append(evt):
            label_lbl.Enable(True)
            label_ctrl.Enable(True)
            ts_ctrl.Enable(False)
            sel = list_box_ctrl.GetSelection() + 1
            self.oldSel = sel
            item = ['', []]
            self.groups.insert(sel, item)
            list_box_ctrl.Set([grp[0] for grp in self.groups])
            list_box_ctrl.SetSelection(sel)
            set_value(item)
            label_ctrl.SetFocus()
            btn_app.Enable(False)
            btn_del.Enable(True)
            evt.Skip()

        btn_app.Bind(wx.EVT_BUTTON, on_button_append)


class PhonebookChoice(wx.ComboBox):
    phbook = []

    def __init__(self, parent, wxid, phbook, plugin, val, pos=wx.DefaultPosition):
        wx.ComboBox.__init__(self, parent, wxid, pos=pos, choices=[])
        self.val = val
        self.plugin = plugin
        self.Set(phbook)

    def get_sel(self):
        return self.GetValue()

    def set_sel(self, val):
        strings = self.GetStrings()
        if val:
            if SEP in val:
                if val in strings:
                    self.SetStringSelection(val)
                else:
                    phone = val.split(SEP)[1].strip()
                    v = [
                        itm for itm in strings if itm.split(SEP)[1].strip() == phone
                    ]
                    if v:
                        self.SetStringSelection(v[0])
                    else:
                        self.SetStringSelection(phone)
            else:
                v = [
                    itm for itm in strings if itm.split(SEP)[1].strip() == val.strip()
                ]
                if v:
                    self.SetStringSelection(v[0])
                else:
                    self.SetStringSelection(val)

    def Set(self, phbook):
        self.Clear()
        self.phbook = phbook
        wx.ComboBox.Set(self, self.phbook)
        if self.val:
            self.set_sel(self.val)


class SmsGroupDialog(wx.Frame):
    oldSel = 0

    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            style=wx.CAPTION | wx.RESIZE_BORDER,
            name="SMS group dialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.plugin = plugin
        self.groups = deepcopy(self.panel.sms_groups)

    def show_sms_groups_dlg(self):
        text = self.plugin.text
        self.SetTitle(text.smsGroupsTitle)
        sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer = wx.FlexGridSizer(4, 2, 2, 8)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        top_middle_sizer = wx.BoxSizer(wx.VERTICAL)
        preview_lbl = wx.StaticText(self, -1, text.groupsList)
        list_box_ctrl = wx.ListBox(
            self, -1,
            style=wx.LB_SINGLE | wx.LB_NEEDED_SB
        )
        label_lbl = wx.StaticText(self, -1, text.groupLabel)
        label_ctrl = wx.TextCtrl(self, -1, '')
        left_sizer.Add(preview_lbl, 0, wx.TOP, 5)
        left_sizer.Add((1, 1))
        left_sizer.Add(list_box_ctrl, 1, wx.TOP | wx.EXPAND, 1)
        left_sizer.Add(top_middle_sizer, 0, wx.TOP, 1)
        left_sizer.Add(label_lbl, 0, wx.TOP, 3)
        left_sizer.Add((1, 1))
        left_sizer.Add(label_ctrl, 0, wx.EXPAND)
        left_sizer.Add((1, 1))

        w1 = self.GetFullTextExtent(text.delete)[0]
        w2 = self.GetFullTextExtent(text.insert)[0]
        w = max(w1, w2) + 24
        btn_app = wx.Button(self, -1, text.insert, size=(w, -1))
        btn_del = wx.Button(self, -1, text.delete, size=(w, -1))
        btn_del.Enable(False)
        top_middle_sizer.Add(btn_app)
        top_middle_sizer.Add(btn_del, 0, wx.TOP, 5)

        left_sizer.AddGrowableCol(0)
        left_sizer.AddGrowableRow(1)

        try:
            choices = list(self.plugin.get_sm_sdevices().iterkeys())
        except KeyError:
            choices = []
        ctrl_dev = wx.Choice(self, -1, choices=choices)
        lbl_dev = wx.StaticText(self, -1, text.device)
        static_box = wx.StaticBox(self, -1, "")
        static_box_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_sizer = wx.FlexGridSizer(2, 2, 10, 10)

        list_ctrl = Table(
            self,
            text.header,
            3,
            ("DevName", "Recipient name", "XXXXXXXXXXXXXXXX")
        )
        lbl_rec = wx.StaticText(self, -1, text.recip)
        ctrl_rec = PhonebookChoice(
            self,
            -1,
            [],
            self.plugin,
            "",
        )
        btn_add = wx.Button(self, -1, text.insert)
        btn_del = wx.Button(self, -1, text.delete)
        btn_del.Enable(False)
        btn_sizer.Add(btn_add)
        btn_sizer.Add(btn_del, 0, wx.TOP, 10)
        top_sizer.Add(list_ctrl, 1, wx.EXPAND)
        top_sizer.Add(btn_sizer, 0, wx.LEFT, 10)
        static_box_sizer.Add(top_sizer, 1, wx.EXPAND)
        bottom_sizer.Add(lbl_dev, 0, wx.ALIGN_CENTER_VERTICAL)
        bottom_sizer.Add(ctrl_dev, 0, wx.EXPAND)
        bottom_sizer.Add(lbl_rec, 0, wx.ALIGN_CENTER_VERTICAL)
        bottom_sizer.Add(ctrl_rec, 0, wx.EXPAND)
        static_box_sizer.Add(bottom_sizer, 0, wx.EXPAND | wx.TOP, 10)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer.Add(static_box_sizer, 1, wx.EXPAND)
        main_sizer.Add(left_sizer, 1, wx.EXPAND)
        main_sizer.Add(right_sizer, 2, wx.EXPAND | wx.LEFT, 10)
        sizer.Add(main_sizer, 1, wx.ALL | wx.EXPAND, 10)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        sizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        sizer.Add((1, 5))

        bottom_sizer.AddGrowableCol(1)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())

        def set_row():
            dev = ctrl_dev.GetStringSelection()
            nm, nr = get_nm_nr(ctrl_rec.get_sel())
            list_ctrl.set_row((dev, nm, nr))
            self.groups[self.oldSel][1] = list_ctrl.get_data()
            validation()

        def on_dev(evt):
            dev = ctrl_dev.GetStringSelection()
            phbook = self.plugin.get_phonebook(dev)
            rcp = ctrl_rec.GetValue()
            ctrl_rec.Set(phbook)
            if rcp:
                ctrl_rec.SetValue(rcp)
            set_row()
            evt.Skip()

        ctrl_dev.Bind(wx.EVT_CHOICE, on_dev)

        def on_rec(evt):
            set_row()
            evt.Skip()

        ctrl_rec.Bind(wx.EVT_COMBOBOX, on_rec)

        def on_select(evt):
            dev, nm, nr = list_ctrl.get_row()
            if dev != ctrl_dev.GetStringSelection():
                if dev in ctrl_dev.GetStrings():
                    ctrl_dev.SetStringSelection(dev)
                    phbook = self.plugin.get_phonebook(dev)
                    ctrl_rec.Set(phbook)
            ctrl_rec.SetValue(nm + SEP + nr if nr != "" and nm != "" else nr)
            evt.Skip()

        list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, on_select)

        def enable_part(enable=None):
            sel_cnt = list_ctrl.GetSelectedItemCount()
            enable = sel_cnt > 0 if enable is None else enable
            if not enable:
                ctrl_rec.SetValue("")
            btn_del.Enable(enable)
            ctrl_rec.Enable(enable)
            ctrl_dev.Enable(enable)
            lbl_rec.Enable(enable)
            lbl_dev.Enable(enable)

        def on_change(evt=None):
            enable_part()
            if evt:
                evt.Skip()

        list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, on_change)
        list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, on_change)
        on_change()

        def on_delete(evt):
            list_ctrl.DeleteItem(list_ctrl.get_selected_index())
            set_row()
            validation()
            evt.Skip()

        btn_del.Bind(wx.EVT_BUTTON, on_delete)

        def on_add(evt):
            list_ctrl.add_row()
            if ctrl_dev.GetStringSelection():
                set_row()
            evt.Skip()

        btn_add.Bind(wx.EVT_BUTTON, on_add)

        def enable_box(enable):
            list_ctrl.Enable(enable)
            btn_add.Enable(enable)
            if enable:
                enable_part()
            else:
                enable_part(False)

        def set_value(item):
            label_ctrl.ChangeValue(item[0])
            list_ctrl.set_data(item[1])
            enable_box(True)

        if len(self.groups) > 0:
            list_box_ctrl.Set([n[0] for n in self.groups])
            list_box_ctrl.SetSelection(0)
            set_value(self.groups[0])
            self.oldSel = 0
            btn_del.Enable(True)
        else:
            label_lbl.Enable(False)
            label_ctrl.Enable(False)
            btn1.Enable(False)
            enable_box(False)

        sizer.Layout()
        # self.MakeModal(True)
        self.SetFocus()
        self.Center()
        self.Show()

        def on_close(evt):
            # self.MakeModal(False)
            self.GetParent().GetParent().Raise()
            self.Destroy()
            evt.Skip()

        self.Bind(wx.EVT_CLOSE, on_close)

        def on_cancel(evt):
            self.Close()
            evt.Skip()

        btn2.Bind(wx.EVT_BUTTON, on_cancel)

        def on_ok(evt):
            self.panel.sms_groups = self.groups
            self.Close()
            evt.Skip()

        btn1.Bind(wx.EVT_BUTTON, on_ok)

        def validation():
            strings = []
            while True:
                flag = True
                label = label_ctrl.GetValue()
                if label == '':
                    flag = False
                if len(self.groups) > 0:
                    strings = list_box_ctrl.GetStrings()
                    for lbl in strings:
                        if lbl == '':
                            flag = False
                            break
                if strings.count(label) != 1:
                    flag = False
                    break
                # sel = self.oldSel
                data = list_ctrl.get_data()
                if len(data) == 0:
                    flag = False
                    break
                else:
                    for rowData in data:
                        if rowData[2] == "":
                            flag = False
                break
            btn1.Enable(flag)
            btn_app.Enable(flag)

        def on_txt_change(evt):
            if self.groups:
                sel = self.oldSel
                label = label_ctrl.GetValue()
                self.groups[sel][0] = label
                list_box_ctrl.Set([grp[0] for grp in self.groups])
                list_box_ctrl.SetSelection(sel)
                validation()
            evt.Skip()

        label_ctrl.Bind(wx.EVT_TEXT, on_txt_change)

        # noinspection PyUnusedLocal
        def on_click(evt):
            sel = list_box_ctrl.GetSelection()
            if self.oldSel != sel:
                self.oldSel = sel
                item = self.groups[sel]
                set_value(item)
                list_box_ctrl.SetSelection(self.oldSel)
                list_box_ctrl.SetFocus()
            # evt.Skip()

        list_box_ctrl.Bind(wx.EVT_LISTBOX, on_click)

        def on_button_delete(evt):
            lngth = len(self.groups)
            sel = list_box_ctrl.GetSelection()
            if lngth == 1:
                self.groups = []
                list_box_ctrl.Set([])
                item = ['', []]
                set_value(item)
                label_lbl.Enable(False)
                label_ctrl.Enable(False)
                enable_box(False)
                btn1.Enable(False)
                btn_del.Enable(False)
                btn_app.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            # tmp = self.groups.pop(list_box_ctrl.GetSelection())
            list_box_ctrl.Set([grp[0] for grp in self.groups])
            list_box_ctrl.SetSelection(sel)
            item = self.groups[sel]
            set_value(item)
            evt.Skip()

        btn_del.Bind(wx.EVT_BUTTON, on_button_delete)

        def on_button_append(evt):
            label_lbl.Enable(True)
            label_ctrl.Enable(True)
            enable_box(False)
            sel = list_box_ctrl.GetSelection() + 1
            self.oldSel = sel
            item = ['', []]
            self.groups.insert(sel, item)
            list_box_ctrl.Set([grp[0] for grp in self.groups])
            list_box_ctrl.SetSelection(sel)
            set_value(item)
            label_ctrl.SetFocus()
            btn_app.Enable(False)
            btn_del.Enable(True)
            evt.Skip()

        btn_app.Bind(wx.EVT_BUTTON, on_button_append)


class CheckListComboBox(wx.ComboCtrl):
    class CheckListBoxComboPopup(wx.ComboPopup):

        def __init__(self, values, help_text):
            wx.ComboPopup.__init__(self)
            self.values = values
            self.helpText = help_text
            self.curitem = None
            self.data = None
            self.lb = None
            self.itemHeight = None

        # noinspection PyUnusedLocal
        def on_dclick(self, evt):
            self.Dismiss()
            self.set_help_text()

        def Init(self):
            self.curitem = None
            self.data = None

        def Create(self, parent):
            self.lb = wx.CheckListBox(parent, -1, (80, 50), wx.DefaultSize)
            self.itemHeight = self.lb.GetFullTextExtent('A')[1]
            self.set_value(self.values)
            self.set_help_text()
            self.lb.Bind(wx.EVT_MOTION, self.on_motion)
            self.lb.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
            self.lb.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)
            return True

        def set_help_text(self, help_text=None):
            self.helpText = help_text if help_text is not None else self.helpText
            combo = self.GetComboCtrl()
            combo.SetText(self.helpText)
            combo.TextCtrl.SetEditable(False)

        def set_value(self, values):
            self.lb.Set(values[0])
            self.data = values[2] if len(values) == 3 else None
            for i in range(len(values[1])):
                self.lb.Check(i, int(values[1][i]))

        def get_value(self):
            strngs = self.lb.GetStrings()
            flags = [self.lb.IsChecked(i) for i in range(len(strngs))]
            return [strngs, flags] if self.data is None else [
                strngs, flags, self.data
            ]

        def GetControl(self):
            return self.lb

        def OnPopup(self):
            if self.curitem:
                self.lb.EnsureVisible(self.curitem)
                self.lb.SetSelection(self.curitem)

        def GetAdjustedSize(self, min_width, pref_height, max_height):
            return wx.Size(
                min_width,
                min(self.itemHeight * (0.5 + len(self.lb.GetStrings())), max_height)
            )

        def on_motion(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.lb.SetSelection(item)
                self.curitem = item
            evt.Skip()

        def on_left_down(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.curitem = item
            evt.Skip()

    def __init__(self, parent, wxid=-1, values=None, **kwargs):
        if values is None:
            values = [[], []]
        if 'helpText' in kwargs:
            help_text = kwargs['helpText']
            del kwargs['helpText']
        else:
            help_text = ""
        wx.ComboCtrl.__init__(self, parent, wxid, **kwargs)
        self.popup = self.CheckListBoxComboPopup(values, help_text)
        self.SetPopupControl(self.popup)
        self.popup.lb.Bind(wx.EVT_CHECKLISTBOX, self.on_check)

    def on_check(self, evt):
        wx.PostEvent(self, evt)
        evt.StopPropagation()

    def GetValue(self):
        return self.popup.get_value()

    def SetValue(self, values):
        self.popup.set_value(values)

    def SetHelpText(self, help_text=None):
        self.popup.set_help_text(help_text)


class FlatButton(GenButton):

    def __init__(
        self,
        parent=None,
        wxid=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        idle_bmp=None,
        active_bmp=None,
        label=None,
        radius=5,
        idle_text_clr="#FFFFFF",
        active_text_clr="#FFFFFF",
        idle_back_clr="#27ae60",
        active_back_clr="#2ecc71",
        font=None,
        bmp_indent=None,
        lbl_indent=None
    ):
        GenButton.__init__(self, parent, wxid, "", pos, size, 0)
        self.font = font
        self.radius = radius
        self.idleTextClr = idle_text_clr
        self.activeTextClr = active_text_clr
        self.idleBackClr = idle_back_clr
        self.activeBackClr = active_back_clr
        self.idleBmp = idle_bmp
        self.activeBmp = active_bmp if active_bmp else idle_bmp
        self.label = label
        self.bmpIndent = bmp_indent
        self.lblIndent = lbl_indent
        self.state = False
        self.mouse = False
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)

    # noinspection PyUnusedLocal
    def on_paint(self, evt):
        if self.state:
            back_clr = self.activeBackClr
            text_clr = self.activeTextClr
            bmp = self.activeBmp
        else:
            back_clr = self.idleBackClr
            text_clr = self.idleTextClr
            bmp = self.idleBmp
        width, height = self.GetSize()
        th = bw = bh = 0
        if bmp:
            if exists(bmp):
                try:
                    wx_bmp = wx.Image(bmp, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                    bw, bh = wx_bmp.GetWidth(), wx_bmp.GetHeight()
                except IOError:
                    wx_bmp = None
            else:
                try:
                    pil = Image.open(StringIO(b64decode(bmp)))
                    has_alpha = (
                        pil.mode in ('RGBA', 'LA')
                        or (pil.mode == 'P' and 'transparency' in pil.info)
                    )
                    image = wx.EmptyImage(*pil.size)
                    rgb_pil = pil.convert('RGB')
                    if has_alpha:
                        image.set_data(rgb_pil.tobytes())
                        image.SetAlphaData(pil.convert("RGBA").tobytes()[3::4])
                    else:
                        new_image = rgb_pil
                        data = new_image.tobytes()
                        image.set_data(data)
                    wx_bmp = image.ConvertToBitmap()
                    bw, bh = wx_bmp.GetWidth(), wx_bmp.GetHeight()
                except IOError:
                    wx_bmp = None
            if self.bmpIndent is None:
                tmpy = (bh + 2 * self.radius - height) / 2
                self.bmpIndent = self.radius - sqrt(self.radius ** 2 - tmpy ** 2) \
                    if (0 < tmpy < self.radius) else 0
                self.bmpIndent = max(5, self.bmpIndent)
                if not self.label:
                    self.bmpIndent = (width - bw) / 2
        else:
            wx_bmp = None

        if self.label:
            if self.font is None:
                self.font = wx.Font(
                    12,
                    wx.FONTFAMILY_SWISS,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                    False,
                    u'Arial'
                )
            self.SetFont(self.font)
            tw, th = self.GetFullTextExtent(self.label)
            if self.lblIndent is None:
                if wx_bmp:
                    self.lblIndent = (width - tw - bw - self.bmpIndent) / 2
                else:
                    self.lblIndent = (width - tw) / 2
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        path = gc.CreatePath()
        path.AddRoundedRectangle(0, 0, width, height, self.radius)
        path.CloseSubpath()
        gc.SetBrush(wx.Brush(back_clr))
        gc.FillPath(path)
        dc.SetTextForeground(text_clr)
        if wx_bmp:
            dc.DrawBitmap(wx_bmp, self.bmpIndent, (height - bh) / 2)
        if self.label:
            dc.SetFont(self.font)
            lbl_pos = self.lblIndent if not wx_bmp \
                else bw + self.bmpIndent + self.lblIndent
            dc.DrawText(self.label, lbl_pos, (height - th) / 2)

    def on_mouse_down(self, evt):
        if self.mouse:
            self.state = False
        self.Refresh()
        evt.Skip()

    def on_mouse_up(self, evt):
        if self.mouse:
            self.state = True
        self.Refresh()
        evt.Skip()

    def on_enter(self, evt):
        self.mouse = True
        self.state = True
        self.Refresh()
        evt.Skip()

    def on_leave(self, evt):
        self.mouse = False
        self.state = False
        self.Refresh()
        evt.Skip()


# noinspection PyPep8Naming,PyMethodMayBeStatic,PyUnusedLocal
class FakeLbl(object):
    def __init__(self):
        super(FakeLbl, self).__init__()

    def GetSize(self):
        return 0, 0

    def GetTextExtent(self, s):
        return 0, 0

    def SetFont(self, font):
        pass

    def GetPosition(self):
        return 0, 0

    def SetPosition(self, pos):
        pass

    def Bind(self, *args, **kwargs):
        pass

    def SetToolTip(self, s):
        pass

    def SetBackgroundColour(self, clr):
        pass


class EnableDialog(wx.Frame):
    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER,
            name="PushBulletEnableDialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.plugin = plugin
        self.disabled = deepcopy(self.plugin.disabled)
        self.enabled = []
        self.SetIcon(self.plugin.info.icon.GetWxIcon())

    def get_items(self):
        pl = self.plugin
        return [pl.get_device(i[1]) for i in self.disabled]

    def show_enab_dialog(self):
        pl = self.plugin
        text = pl.text
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(text.title3)
        panel = wx.Panel(self)
        line = wx.StaticLine(
            panel,
            -1,
            style=wx.LI_HORIZONTAL
        )
        btn4 = wx.Button(panel, wx.ID_DELETE, text.delete)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, wx.ID_OK, text.ok)
        btnsizer.Add(btn1)
        btnsizer.Add((5, -1))
        btn2 = wx.Button(panel, wx.ID_CANCEL, text.cancel)
        btnsizer.Add(btn2)
        lbl1 = wx.StaticText(panel, -1, text.enabLbl)
        list_box_ctrl = wx.ListBox(
            panel, -1,
            style=wx.LB_SINGLE | wx.LB_NEEDED_SB
        )
        list_box_ctrl.Set(self.get_items())
        btn4.Disable()

        def on_click(evt):
            btn4.Enable(True)
            # sel = evt.GetSelection()
            evt.Skip()

        list_box_ctrl.Bind(wx.EVT_LISTBOX, on_click)

        def on_button_delete(evt):
            # lngth = list_box_ctrl.GetCount()
            sel = list_box_ctrl.GetSelection()
            item = self.disabled.pop(sel)
            self.enabled.append(item)
            list_box_ctrl.Set(self.get_items())
            if list_box_ctrl.GetCount():
                if sel >= list_box_ctrl.GetCount():
                    sel = list_box_ctrl.GetCount() - 1
                list_box_ctrl.SetSelection(sel)
            else:
                btn4.Disable()
            evt.Skip()

        btn4.Bind(wx.EVT_BUTTON, on_button_delete)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(lbl1)
        left_sizer.Add(list_box_ctrl, 1, wx.EXPAND)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add((-1, 10))
        right_sizer.Add(btn4, 0, wx.ALL, 5)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(left_sizer, 1, wx.ALL | wx.EXPAND, 5)
        top_sizer.Add(right_sizer, 0, wx.TOP, 2)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.BOTTOM, 5)
        main_sizer.Add(btnsizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        main_sizer.Add((1, 6))
        panel.SetSizer(main_sizer)

        def on_close(evt):
            # self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
            evt.Skip()

        self.Bind(wx.EVT_CLOSE, on_close)

        def on_ok(_):
            wx.CallAfter(self.plugin.enable_mirroring_many, self.enabled)
            self.Close()

        btn1.Bind(wx.EVT_BUTTON, on_ok)

        def on_cancel(_):
            self.Close()

        btn2.Bind(wx.EVT_BUTTON, on_cancel)

        main_sizer.Fit(self)
        main_sizer.Layout()
        self.Raise()
        # self.MakeModal(True)
        self.Show()


class Table(wx.ListCtrl):

    def __init__(self, parent, header, min_rows, dummy_data=None):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL,
        )
        self.cols = len(header)
        for i, colLabel in enumerate(header):
            self.InsertColumn(
                i,
                colLabel,
                format=wx.LIST_FORMAT_LEFT
            )
            if dummy_data:
                if i:
                    self.SetItem(0, i, dummy_data[i])
                else:
                    self.InsertItem(0, dummy_data[i])
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        self.DeleteAllItems()
        self.w0 = self.GetColumnWidth(0)
        self.w1 = self.GetColumnWidth(1)
        self.w2 = self.GetColumnWidth(2)
        self.wk = SYS_VSCROLL_X + self.GetWindowBorderSize()[0] + self.w0 + self.w1 + self.w2
        width = self.wk
        hh = rect[1]  # header height
        hi = rect[3]  # item height
        self.SetMinSize((width, 4 + hh + min_rows * hi))
        self.SetSize((width, 4 + hh + min_rows * hi))
        self.Bind(wx.EVT_SIZE, self.on_size)

    def set_width(self):
        w = (self.GetSize().width - self.wk)
        w0_ = w / 3 + self.w0
        w1_ = w / 3 + self.w1
        w2_ = w - 2 * w / 3 + self.w2
        self.SetColumnWidth(0, w0_)
        self.SetColumnWidth(1, w1_)
        self.SetColumnWidth(2, w2_)

    def on_size(self, event):
        wx.CallAfter(self.set_width)
        event.Skip()

    def get_selected_index(self):
        item_index = -1
        return self.GetNextItem(
            item_index,
            wx.LIST_NEXT_ALL,
            wx.LIST_STATE_SELECTED
        )

    def add_row(self):
        row = self.GetItemCount()
        self.InsertItem(row, "")
        self.SetItemState(row, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.SetFocus()

    def set_row(self, row_data, row=None):
        row = self.get_selected_index() if row is None else row
        if row > -1:
            for col, colData in enumerate(row_data):
                self.SetItem(row, col, colData)

    def get_row(self, row=None):
        row = self.get_selected_index() if row is None else row
        row_data = []
        for col in range(self.cols):
            row_data.append(self.GetItem(row, col).GetText())
        return row_data

    def get_data(self):
        data = []
        for row in range(self.GetItemCount()):
            row_data = self.get_row(row)
            data.append(row_data)
        return data

    def set_data(self, data):
        self.DeleteAllItems()
        for row, rowData in enumerate(data):
            self.InsertItem(row, rowData[0])
            for col, colData in enumerate(rowData[1:]):
                self.SetItem(row, col + 1, colData)


class ListGrid(gridlib.Grid):

    def __init__(self, parent, wxid, items, width):
        gridlib.Grid.__init__(
            self,
            parent,
            wxid,
            size=(width - 5, -1),
            style=wx.BORDER_RAISED
        )
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetDefaultRowSize(19)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.EnableEditing(True)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.EnableGridLines(True)
        self.SetColMinimalAcceptableWidth(8)
        self.CreateGrid(len(items), 1)
        self.SetColSize(0, width - 6 - SYS_VSCROLL_X)
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0, attr)
        self.SetSelectionMode(gridlib.Grid.wxGridSelectRows)
        self.Bind(gridlib.EVT_GRID_CMD_SELECT_CELL, self.on_grid_select_cell, self)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.set_value(items)
        self.oldW = self.GetSize()[0]
        self.Show(True)

    def set_width(self):
        width = self.GetSize()[0]
        if width != self.oldW:
            self.SetColSize(0, width - 6 - SYS_VSCROLL_X)
            self.oldW = width

    def on_size(self, event):
        wx.CallAfter(self.set_width)
        event.Skip()

    def on_grid_select_cell(self, event):
        rows = self.GetNumberRows()
        row = event.get_row()
        self.SelectRow(row)
        if rows - 1 == row:
            self.AppendRows(1)
        if not self.IsVisible(row, 0):
            self.MakeCellVisible(row, 0)
        event.Skip()

    def get_value(self):
        items = []
        for r in range(self.GetNumberRows()):
            item = self.GetCellValue(r, 0)
            if item.strip():
                items.append(item)
        return items

    def set_value(self, items):
        self.ClearGrid()
        for i in range(len(items)):
            self.SetCellValue(i, 0, items[i])


class ReplyDialog(wx.Frame):

    def __init__(
        self,
        parent,
        plugin,
        title,
        body,
        img,
        app,
        push_dict
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER,
            name="PushBulletReplyDialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.plugin = plugin
        self.title = title
        self.body = body
        self.img = img
        self.app = app
        self.pushDict = push_dict
        self.SetIcon(self.plugin.info.icon.GetWxIcon())

    def show_reply_dialog(self):
        pl = self.plugin
        self.SetTitle(pl.text.title4 % self.title)
        panel = wx.Panel(self)
        panel.SetBackgroundColour(self.GetBackgroundColour())
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(10, 10)

        self.SetSizer(main_sizer)
        int_brdr = 10
        main_sizer.Add(sizer, 1, wx.ALL | wx.EXPAND, int_brdr)
        bmp = StaticBitmap(
            self,
            -1,
            self.img,
            size=(self.img.GetWidth(), self.img.GetHeight())
        )
        ttl = wx.StaticText(
            self,
            -1,
            self.title,
        )
        font = wx.Font(
            14,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            False,
            u'Ariel'
        )
        ttl.SetFont(font)
        dsc = wx.StaticText(
            self,
            -1,
            "Via %s" % self.app,
        )
        font = wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_LIGHT,
            False,
            u'Ariel'
        )
        dsc.SetFont(font)
        btn = FlatButton(
            self,
            -1,
            size=(90, 50),
            idle_bmp=join(ICON_DIR, "Reply.png"),
            label=pl.text.reply,
            radius=5,
            bmp_indent=5
        )
        sizer.Add(bmp, (0, 0), (2, 1))
        sizer.Add(ttl, (0, 1))
        sizer.Add(btn, (0, 2), (2, 1), flag=wx.ALIGN_RIGHT)
        sizer.Add(dsc, (1, 1))

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(3)

        bd = wx.TextCtrl(
            self,
            -1,
            self.body,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE | wx.TE_RICH
        )
        bd.SetBackgroundColour(self.GetBackgroundColour())
        bd.SetFont(font)
        sizer.Add(bd, (2, 0), (1, 3), flag=wx.EXPAND)
        msg = wx.TextCtrl(
            self,
            -1,
            style=wx.TE_MULTILINE | wx.TE_RICH
        )
        msg.ChangeValue(pl.text.replyPrompt)

        fnt = msg.GetFont()
        fnt.SetPointSize(10)
        msg.SetFont(fnt)

        def get_multi_line_text_extent(ctrl, txt):
            slices = [ctrl.GetFullTextExtent(item)[0] for item in txt.split("\n")]
            return max(slices)

        msg_w = get_multi_line_text_extent(msg, pl.text.replyPrompt)
        ext_brdr = self.GetSize()[0] - self.GetClientSize()[0]
        brdrs = 10 + ext_brdr + 2 * int_brdr
        msg.SetForegroundColour(wx.GREEN)
        sizer.Add(msg, (3, 0), (1, 3), flag=wx.EXPAND)

        def on_frame_char_hook(evt):
            kc = evt.GetKeyCode()
            if kc in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) and evt.ControlDown():
                pl.send_reply(self.pushDict, msg.GetValue())
                self.Close()
            else:
                evt.Skip()

        self.Bind(wx.EVT_CHAR_HOOK, on_frame_char_hook)

        def on_focus(evt):
            if msg.GetValue() == pl.text.replyPrompt:
                msg.SetForegroundColour(self.GetForegroundColour())
                msg.ChangeValue("")
            evt.Skip()

        msg.Bind(wx.EVT_SET_FOCUS, on_focus)

        # def on_close(evt):
        #     # self.MakeModal(False)
        #     self.Destroy()
        #
        # self.Bind(wx.EVT_CLOSE, on_close)

        def on_reply(evt):
            pl.send_reply(self.pushDict, msg.GetValue())
            self.Close()
            evt.Skip()

        btn.Bind(wx.EVT_BUTTON, on_reply)

        main_sizer.Fit(self)
        main_sizer.Layout()
        self.Raise()
        # self.MakeModal(True)
        w, h = self.GetSize()
        self.SetSize((max(w, msg_w + brdrs), 320))
        self.SetMinSize((min(w, msg_w + brdrs), min(h, 290)))
        self.Show()


class ProxyDialog(wx.Frame):
    def __init__(self, parent, plugin, labels, data):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER,
            name="ProxyDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.data = data
        self.password = None

    def show_proxy_dlg(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        text = self.plugin.text
        panel = wx.Panel(self)

        def wxst(label):
            return wx.StaticText(panel, -1, label)

        labels = self.labels
        data = self.data
        rows = len(labels)
        sizer = wx.GridBagSizer(5, 5)

        for row in range(rows):
            sizer.Add(wxst(labels[row]), (row, 0), flag=wx.ALIGN_CENTER_VERTICAL)
            txt_ctrl = wx.Size(1, 1)
            if row not in (1, 3):
                txt_ctrl = wx.TextCtrl(panel, -1, data[row])
            elif row == 1:
                txt_ctrl = eg.SpinIntCtrl(
                    panel,
                    -1,
                    data[row],
                    min=0,
                    max=65535
                )
            elif row == 3:
                self.password = eg.Password(data[row])
                txt_ctrl = wx.TextCtrl(
                    panel,
                    -1,
                    self.password.Get(),
                    style=wx.TE_PASSWORD
                )
            sizer.Add(txt_ctrl, (row, 1), flag=wx.EXPAND)

        sizer.AddGrowableCol(1)
        info = wxst(text.proxyInfo)
        info.Enable(False)
        sizer.Add(info, (rows, 0), (1, 2), flag=wx.ALIGN_CENTER_VERTICAL)

        line = wx.StaticLine(
            panel,
            -1,
            style=wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        main_sizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        main_sizer.Add((1, 6))
        panel.SetSizer(main_sizer)
        main_sizer.Fit(self)

        def on_close(evt):
            # self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
            evt.Skip()

        self.Bind(wx.EVT_CLOSE, on_close)

        def on_ok(evt):
            data_ok = []
            children = sizer.GetChildren()
            for child in range(1, len(children), 2):
                ctrl = children[child].GetWindow()
                if child != 7:
                    data_ok.append(ctrl.get_value())
                else:
                    self.password.Set(ctrl.get_value())
                    data_ok.append(self.password)
            self.GetParent().proxy = data_ok
            self.Close()
            evt.Skip()

        btn1.Bind(wx.EVT_BUTTON, on_ok)

        def on_cancel(evt):
            self.Close()
            evt.Skip()

        btn2.Bind(wx.EVT_BUTTON, on_cancel)

        main_sizer.Layout()
        w, h = self.GetSize()
        self.SetSize((max(w, 300), h))
        self.SetMinSize((max(w, 300), h))
        self.Raise()
        # self.MakeModal(True)
        self.Centre()
        self.Show()


class MirrorNote(wx.Frame):

    def __init__(self, parent, plugin, dev, title, body, icon, app, wav, push_dict):
        flag = self.flag = 'type' in push_dict and push_dict['type'] == 'sms' and push_dict['recip'] != "MULTI"
        self.plugin = plugin
        self.pushDict = push_dict
        repl = 'conversation_iden' in push_dict
        dev = dev.rstrip()
        title = title.replace("&", "&&").rstrip()
        body = body.replace("&", "&&")
        body = body if body == body[:1000] else "%s ...." % body[:1000]
        body = wrap(body, 80)

        if icon:
            sbuf = StringIO(b64decode(icon))
        else:
            sbuf = StringIO(b64decode(AVATAR))
        wximg = wx.Image(sbuf)
        w = wximg.GetWidth()
        h = wximg.GetHeight()
        k = 96
        if w > k or h > k:
            factor = max(w, h) / float(k)
            x = int(min(w, h) / factor)
            size = (k, x) if w >= h else (x, k)
            wximg = wximg.Scale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
            w = wximg.GetWidth()
            h = wximg.GetHeight()

        if repl and w == h:
            mask = fluffy_circle_mask(wximg.GetWidth())
            wximg.SetAlphaData(mask)
        img = wx.Bitmap(wximg)

        if w < 72 and h < 72:
            w, h = (72, 72)

        wx.Frame.__init__(
            self,
            parent,
            -1,
            '',
            size=(400, h + 8),
            style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER
        )
        bc = plugin.clr
        self.SetBackgroundColour(bc)
        self.delta = (0, 0)
        bmp = StaticBitmap(
            self,
            -1,
            img,
            (3, 3),
            (img.GetWidth(),
             img.GetHeight())
        )
        app = app if (not plugin.hideBtn and not flag) else ""
        lbl = plugin.text.disable % app if app else ""
        label0 = wx.StaticText(self, -1, dev, (w + 10, 2)) if dev else FakeLbl()
        label1 = wx.StaticText(self, -1, title) if title else FakeLbl()
        label2 = wx.StaticText(self, -1, body) if body else FakeLbl()
        label3 = wx.StaticText(self, -1, lbl) if app else FakeLbl()
        label4 = wx.StaticText(self, -1, strftime('     %H:%M:%S'))

        font = label0.GetFont()
        size = font.GetPointSize()
        font.SetPointSize(size * 1.4)
        label2.SetFont(font)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label1.SetFont(font)
        font = label0.GetFont()
        font.SetStyle(wx.FONTSTYLE_ITALIC)
        label3.SetFont(font)

        w0, h0 = label0.GetSize()
        w1, h1 = label1.GetSize()
        w2, h2 = label2.GetSize()
        w3, h3 = label3.GetSize()
        w4, h4 = label4.GetSize()
        _, e0 = label0.GetTextExtent("X")
        _, e1 = label1.GetTextExtent("X")
        _, e2 = label2.GetTextExtent("X")
        label1.SetPosition((w + 10, 19 - e0 + h0))
        label2.SetPosition((w + 10, 38 - e0 - e1 + h0 + h1))
        x0, y0 = label0.GetPosition()
        x1, y1 = label1.GetPosition()
        x2, y2 = label2.GetPosition()

        if app:
            def on_click(event):
                wx.CallAfter(plugin.disable_mirroring, self.pushDict, app)
                if flag:
                    self.plugin.sms_dismiss()
                else:
                    self.plugin.dismiss(self.pushDict)
                self.Close()
                event.Skip()

            h = max(y0 + h0, y1 + h1, y2 + h2)
            png = wx.Bitmap(
                join(eg.Icons.IMAGES_PATH, "disabled.png"),
                wx.BITMAP_TYPE_PNG
            )
            gr = png.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()
            hh = max(h + 8, h + 32 if repl else h + 22)
            b = wx.BitmapButton(
                self,
                -1,
                gr,
                pos=(w + 10, hh - 20),
                size=(16, 16),
                style=wx.BORDER_NONE
            )

            label0.SetBackgroundColour(bc)
            label1.SetBackgroundColour(bc)
            label2.SetBackgroundColour(bc)
            label3.SetBackgroundColour(bc)
            label4.SetBackgroundColour(bc)
            b.SetBackgroundColour(bc)
            b.SetBitmapCurrent(png)
            b.SetBitmapPressed(png)
            b.Bind(wx.EVT_BUTTON, on_click)
            label3.SetPosition((w + 32, hh - 18))
        else:
            hh = None
        if repl:
            def on_btn(event):
                if flag:
                    self.plugin.sms_dismiss()
                else:
                    self.plugin.dismiss(deepcopy(self.pushDict))
                dlg = ReplyDialog(
                    parent,
                    plugin,
                    title if title else "",
                    body if body else "",
                    img,
                    app,
                    self.pushDict
                )
                self.Show(False)
                self.Close()
                dlg.Centre()
                dlg.show_reply_dialog()
                event.Skip()

            idle_img = wx.Image(join(ICON_DIR, "Reply.png"), wx.BITMAP_TYPE_ANY)
            pil = image_to_pil(idle_img)
            if pil:
                pil = resize(pil, 16)
                io_file = StringIO()
                pil.save(io_file, format='PNG')
                io_file.seek(0)
                data = io_file.read()
                idle_bmp = b64encode(data)
            else:
                idle_bmp = None

            btn = FlatButton(
                self,
                -1,
                idle_bmp=idle_bmp,
                label=plugin.text.reply,
                radius=5,
                bmp_indent=3
            )
            btn.Bind(wx.EVT_BUTTON, on_btn)
            wb, hb = btn.GetSize()
            hh = hh if hh is not None else 8 + max(h, y0 + h0 + hb, y1 + h1 + hb, y2 + h2 + hb)
            w = max(w0 + w4, w1, w2, w3 + wb + 37)
            btn.SetPosition((w + 18 + w - wb - 5, hh - hb - 5))
        else:
            w = max(w0 + w4, w1, w2, w3 + 22)
        self.SetSize((w + 18 + w, hh))
        label4.SetPosition((w + 10 + w0 if w == w0 + w4 else w + 10 + w - w4, 2))
        self.Bind(wx.EVT_CLOSE, self.on_close_window)

        for win in (self, label0, label1, label2, label3, label4, bmp):
            win.Bind(wx.EVT_RIGHT_UP, self.on_right_click)
            win.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
            win.Bind(wx.EVT_LEFT_UP, self.on_left_up)
            win.Bind(wx.EVT_MOTION, self.on_mouse_move)
            win.SetToolTip(plugin.text.tooltip)

        self.timer = wx.Timer(self)
        if plugin.hide:
            self.timer.Start(1000 * plugin.hide)
            self.Bind(wx.EVT_TIMER, self.on_close_window)

        width, height = self.GetSize()
        monitor_dimensions = GetMonitorDimensions()
        try:
            display_rect = monitor_dimensions[plugin.dspl]
        except IndexError:
            display_rect = monitor_dimensions[0]
        x_offset, y_offset = plugin.offset
        x_func, y_func = ALIGNMENT_FUNCS[plugin.alignment]
        x = display_rect.x + x_func((display_rect.width - width), x_offset)
        y = display_rect.y + y_func((display_rect.height - height), y_offset)

        self.SetPosition((x, y))
        if wav:
            self.sound = wx.adv.Sound(wav)
            if self.sound.IsOk():
                self.sound.Play(wx.adv.SOUND_ASYNC)
        else:
            self.sound = None
        self.Show(True)
        plugin.notification_ids[self.pushDict['notification_id']] = self
        BringWindowToTop(self.GetHandle())

    def on_close_window(self, event):
        n_id = self.pushDict['notification_id']
        if n_id in self.plugin.notification_ids:
            del self.plugin.notification_ids[n_id]
        if hasattr(self, 'timer'):
            self.timer.Stop()
            del self.timer
        if self.sound:
            self.sound.Stop()
        self.Destroy()
        event.Skip()

    def on_right_click(self, evt):
        if self.flag:
            self.plugin.sms_dismiss()
        else:
            self.plugin.dismiss(self.pushDict)
        self.Show(False)
        self.Close()
        evt.Skip()

    def on_left_down(self, evt):
        x, y = self.ClientToScreen(evt.GetPosition())
        win = evt.GetEventObject()
        if isinstance(win, (
            wx.StaticText,
            StaticBitmap
        )):
            child_x, child_y = win.GetPosition()
            x += child_x
            y += child_y
        self.CaptureMouse()
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ([dx, dy])

    def on_left_up(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        evt.Skip()

    def on_mouse_move(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)
