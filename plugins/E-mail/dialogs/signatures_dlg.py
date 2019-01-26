# coding=utf8

from copy import deepcopy

import wx

import eg
from ..utils import move_item


class SignaturesDialog(eg.Dialog):
    old_sel = 0

    def __init__(self, parent, plugin, signatures):
        self.text = plugin.text
        eg.Dialog.__init__(
            self,
            parent=parent,
            id=wx.ID_ANY,
            title=self.text.textsTitle,
            name="Texts dialog",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.panel = parent
        self.plugin = plugin
        self.signatures = deepcopy(signatures)

        self.create_widgets()
        self.create_sizers()
        self.btn_ok = self.FindWindowById(wx.ID_OK)
        self.bindings()

        if len(self.signatures) > 0:
            self.list_box_ctrl.Set([n[0] for n in self.signatures])
            self.list_box_ctrl.SetSelection(0)
            self.set_value(self.signatures[0])
            self.old_sel = 0
            self.btn_up.Enable(True)
            self.btn_down.Enable(True)
            self.btn_del.Enable(True)
        else:
            self.box_enable(False)
            self.btn_ok.Enable(False)

    def bindings(self):
        self.label_ctrl.Bind(wx.EVT_TEXT, self.on_txt_change)
        self.signature_ctrl.Bind(wx.EVT_TEXT, self.on_text_name)
        self.list_box_ctrl.Bind(wx.EVT_LISTBOX, self.on_click)
        self.btn_up.Bind(wx.EVT_BUTTON, self.on_button_up)
        self.btn_down.Bind(wx.EVT_BUTTON, self.on_button_down)
        self.btn_del.Bind(wx.EVT_BUTTON, self.on_button_delete)
        self.btn_add.Bind(wx.EVT_BUTTON, self.on_button_append)

    def create_sizers(self):
        main_sizer = wx.GridBagSizer(hgap=5, vgap=10)
        main_sizer.Add(self.listbox_lbl, pos=(0, 0), flag=wx.EXPAND)
        main_sizer.Add(self.list_box_ctrl, pos=(1, 0), span=(4, 1), flag=wx.EXPAND)
        main_sizer.Add(self.label_ctrl, pos=(5, 0), span=(1, 2), flag=wx.EXPAND)
        main_sizer.Add(self.btn_up, pos=(1, 1), flag=wx.ALIGN_BOTTOM)
        main_sizer.Add(self.btn_down, pos=(2, 1))
        main_sizer.Add(self.btn_del, pos=(3, 1))
        main_sizer.Add(self.btn_add, pos=(4, 1))
        main_sizer.Add(self.out_text_lbl, pos=(0, 2))
        main_sizer.Add(self.signature_ctrl, pos=(1, 2), span=(5, 1), flag=wx.EXPAND)

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
        self.SetMinSize((500, 400))
        sizer.Layout()
        self.SetSizerAndFit(sizer)

    # noinspection PyAttributeOutsideInit
    def create_widgets(self):
        text = self.text
        self.listbox_lbl = wx.StaticText(self, wx.ID_ANY, text.textsList)
        self.list_box_ctrl = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.label_ctrl = wx.TextCtrl(self)
        self.out_text_lbl = wx.StaticText(self, wx.ID_ANY, text.outText)
        self.signature_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, (16, 16))
        self.btn_up = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.btn_up.Enable(False)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, (16, 16))
        self.btn_down = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.btn_down.Enable(False)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16, 16))
        self.btn_del = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.btn_del.Enable(False)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16))
        self.btn_add = wx.BitmapButton(self, wx.ID_ANY, bmp)

    def box_enable(self, enable):
        self.label_ctrl.Enable(enable)
        self.signature_ctrl.Enable(enable)
        self.out_text_lbl.Enable(enable)

    def set_value(self, item):
        self.label_ctrl.ChangeValue(item[0])
        self.signature_ctrl.ChangeValue(item[1])

    def validation(self):
        flag = True
        label = self.label_ctrl.GetValue()
        if label == "":
            flag = False
        else:
            if [j[0] for j in self.signatures].count(label) != 1:
                flag = False
        if self.signature_ctrl.GetValue().strip() == '':
            flag = False
        self.btn_ok.Enable(flag)
        self.btn_add.Enable(flag)

    def on_txt_change(self, evt):
        if self.signatures:
            sel = self.old_sel
            label = self.label_ctrl.GetValue().strip()
            self.signatures[sel][0] = label
            self.list_box_ctrl.Set([j[0] for j in self.signatures])
            self.list_box_ctrl.SetSelection(sel)
            self.validation()
        evt.Skip()

    def on_text_name(self, evt):
        if self.signatures:
            val = self.signature_ctrl.GetValue()  # .strip()
            sel = self.old_sel
            self.signatures[sel][1] = val
            self.validation()
        evt.Skip()

    def on_click(self, evt):
        sel = self.list_box_ctrl.GetSelection()
        label = self.label_ctrl.GetValue()
        if label.strip() != u"":
            if [j[0] for j in self.signatures].count(label) == 1:
                self.old_sel = sel
                item = self.signatures[sel]
                self.set_value(item)
        self.list_box_ctrl.SetSelection(self.old_sel)
        self.list_box_ctrl.SetFocus()
        evt.Skip()

    def on_button_up(self, evt):
        new_sel, self.signatures = move_item(self.signatures, self.list_box_ctrl.GetSelection(), -1)
        self.list_box_ctrl.Set([j[0] for j in self.signatures])
        self.list_box_ctrl.SetSelection(new_sel)
        self.old_sel = new_sel
        evt.Skip()

    def on_button_down(self, evt):
        new_sel, self.signatures = move_item(self.signatures, self.list_box_ctrl.GetSelection(), 1)
        self.list_box_ctrl.Set([j[0] for j in self.signatures])
        self.list_box_ctrl.SetSelection(new_sel)
        self.old_sel = new_sel
        evt.Skip()

    def on_button_delete(self, evt):
            lngth = len(self.signatures)
            if lngth == 2:
                self.btn_up.Enable(False)
                self.btn_down.Enable(False)
            sel = self.list_box_ctrl.GetSelection()
            if lngth == 1:
                self.signatures = []
                self.list_box_ctrl.Set([])
                item = ['', '']
                self.set_value(item)
                self.box_enable(False)
                self.btn_ok.Enable(False)
                self.btn_del.Enable(False)
                self.btn_add.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.old_sel = sel
            self.signatures.pop(self.list_box_ctrl.GetSelection())
            self.list_box_ctrl.Set([j[0] for j in self.signatures])
            self.list_box_ctrl.SetSelection(sel)
            item = self.signatures[sel]
            self.set_value(item)
            evt.Skip()

    def on_button_append(self, evt):
            if len(self.signatures) == 1:
                self.btn_up.Enable(True)
                self.btn_down.Enable(True)
            self.box_enable(True)
            sel = self.list_box_ctrl.GetSelection() + 1
            self.old_sel = sel
            item = ['', '']
            self.signatures.insert(sel, item)
            self.list_box_ctrl.Set([j[0] for j in self.signatures])
            self.list_box_ctrl.SetSelection(sel)
            self.set_value(item)
            self.label_ctrl.SetFocus()
            self.btn_add.Enable(False)
            self.btn_del.Enable(True)
            evt.Skip()

    def get_texts(self):
        return self.signatures
