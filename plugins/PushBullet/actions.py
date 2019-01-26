# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2015  Pako <lubos.ruckl@gmail.com>
#
# This file is part of the PushBullet plugin for EventGhost.
#


import codecs
from copy import deepcopy
from encodings import aliases
from os import startfile
from os.path import join, splitext
from threading import Thread

import wx

import eg
from .utils import check, get_nm_nr, grayed, SEP
from .widgets import ICON_DIR, PhonebookChoice, Table

try:
    from ImageGrab import grab, grabclipboard
except ImportError:
    from PIL.ImageGrab import grab, grabclipboard


class Push(eg.ActionBase):
    ids = []
    ix = 0
    kind = None
    right_sizer = None
    ts = None
    value = None

    class Text(eg.TranslatableStrings):
        limit = "Files must be smaller than 25 MB"
        lbls1 = (
            "Title:",
            "Link title:",
            "Message:",
            "Title:"
        )
        lbls2 = (
            "Message:",
            "Link (something like http://eventghost.net/forum):",
            "File:",
            "Message:"
        )
        lbl3 = "Icon (path to image or base64 string):"
        toolTipFile = '''Type filename or click browse to choose file
Files must be smaller than 25 MB'''
        toolTipIcon = '''Type filename or click browse to choose image
or enter base64 string'''
        browseFile = 'Choose a file'
        browseIcon = 'Choose a image file'
        cont = "Push contents:"
        fMask = "All files (*.*)|*.*"
        iMask = (
            "JPG files (*.jpg)|*.jpg"
            "|BMP files (*.bmp)|*.bmp"
            "|PNG files (*.png)|*.png"
            "|All files (*.*)|*.*"
        )
        ever = 'Everything'
        suffix = "Event suffix when completed:"
        toolTipSuff = '''If you fill out this field, then after sending 
of push(-es) it will be triggered an event, carrying  a result (as a payload). 
If the field is left blank, the event will not be triggered.'''
        smartLabel = "Apply, push and close"
        smartTip = "The changes are saved, push is sent and the dialog closes."
        grLabel = "Group:"
        target = "Push target:"
        toolTipSingle = """The target can be a device or a friend or channel.
You can use iden, (nick)name, email or channel tag.
You can also use variables - for example {eg.result} or {eg.event.payload} ."""

    def __call__(self, kind=0, trgts=None, data=None, suff=""):
        if data is None:
            data = ["", ""]
        if trgts is None:
            trgts = []
        if self.value == "Everything":
            trgts = [['Everything', None, 'everything', True]]
        elif self.value == "Reply":
            trgts = self.plugin.get_targets(eg.event.payload[-2])
            trgts = trgts if trgts else [['Everything', None, 'everything', True]]
        elif self.value == "Gr":
            tmp = [itm[0] for itm in self.plugin.pushGroups]
            if trgts in tmp:
                ix = tmp.index(trgts)
                trgts = self.plugin.pushGroups[ix][1]
            else:
                return  # no targets
        elif self.value == "Single":
            if not isinstance(trgts, (str, unicode)):
                return
            trgts = eg.ParseString(trgts)
            trgts = self.plugin.get_single(trgts)
            if not trgts:
                return
            else:
                trgts = list(trgts[0])
                trgts.append(True)
                trgts = [trgts]
        suff = eg.ParseString(suff)
        pdt = len(data) * [None]
        pdt[0] = eg.ParseString(data[0])
        pdt[1] = eg.ParseString(data[1])
        if len(data) > 2:
            pdt[2] = eg.ParseString(data[2])
        push_thread = Thread(
            target=self.plugin.push,
            args=(kind, trgts, pdt, suff)
        )
        push_thread.start()

    def GetLabel(self, kind, trgts, data, suff):
        k = self.plugin.text.kinds[kind]
        if self.value == "Everything":
            ts = self.text.ever
        elif self.value == "Reply":
            return "%s: %s" % (self.name, k)
        elif self.value in ("Gr", "Single"):
            ts = trgts
        else:
            ts = [i[0] for i in trgts if i[3]]
            ts = repr(ts) if len(ts) > 1 else '"%s"' % ts[0]
        return "%s: %s to %s" % (self.name, k.lower(), ts)

    # noinspection PyArgumentList
    def Configure(self, kind=0, trgts=None, data=None, suff=""):
        if data is None:
            data = ["", ""]
        if trgts is None:
            trgts = []
        text = self.text
        self.kind = kind
        panel = eg.ConfigPanel(self)
        self.ts = []
        ts_label = wx.Size(1, 1)
        ts_ctrl = wx.Size(1, 1)
        if self.value == "Gr":
            ts_label = wx.StaticText(panel, -1, self.text.grLabel)
            ts_ctrl = wx.Choice(
                panel,
                -1,
                choices=[itm[0] for itm in self.plugin.pushGroups],
                size=(-1, 200),
            )
            if isinstance(trgts, (str, unicode)):
                ts_ctrl.SetStringSelection(trgts)
        elif self.value == "Single":
            if not isinstance(trgts, (str, unicode)):
                trgts = ""
            ts_label = wx.StaticText(panel, -1, self.text.target)
            ts_ctrl = wx.TextCtrl(panel, -1, trgts, size=(200, -1))
            ts_label.SetToolTip(text.toolTipSingle)
            ts_ctrl.SetToolTip(text.toolTipSingle)

        elif not self.value:
            self.ts = deepcopy(trgts)
            for t in self.ts:
                if tuple(t[:3]) not in self.plugin.targets:
                    self.ts.remove(t)
            tmp = []
            for t in self.plugin.targets:
                tmp2 = [i[:3] for i in self.ts]
                if list(t) in tmp2:
                    tmp.append(list(self.ts[tmp2.index(list(t))]))
                else:
                    tmp.append([t[0], t[1], t[2], False])
            self.ts = tmp
            items = [n[0] for n in self.ts]
            ts_label = wx.StaticText(panel, -1, self.plugin.text.tsLabel)
            ts_ctrl = wx.CheckListBox(
                panel,
                -1,
                choices=items,
                size=(-1, 200),
            )
            for i, item in enumerate(self.ts):
                ts_ctrl.Check(i, item[3])

            def remove_targets():
                for j, u in enumerate(self.ts):
                    if u[2] != 'pc':
                        self.ts[j][3] = False
                        ts_ctrl.Check(j, False)

            def after_check_list_box():
                ts_ctrl.SetSelection(self.ix)
                if ts_ctrl.IsChecked(self.ix):
                    if self.kind == 3 and self.plugin.targets[self.ix][2] != 'pc':
                        ts_ctrl.Check(self.ix, False)
                        self.ts[self.ix][3] = False
                    else:
                        self.ts[self.ix][3] = True
                else:
                    self.ts[self.ix][3] = False

            def on_check_list_box(evt):
                self.ix = evt.GetInt()
                wx.CallAfter(after_check_list_box)
                evt.Skip()

            ts_ctrl.Bind(wx.EVT_CHECKLISTBOX, on_check_list_box)

            def update_size():
                h = left_sizer.GetSize()[1]
                ts_ctrl.SetSize((-1, h - 17))

            def on_size(event):
                wx.CallAfter(update_size)
                event.Skip()

            panel.Bind(wx.EVT_SIZE, on_size)

        # noinspection PyArgumentList
        def on_click(event):
            img = wx.FindWindowById(id=buttons[self.kind])
            img.SetBitmapLabel(grayed(bmps[self.kind]))  # reset to gray
            evt_id = event.GetId()
            self.kind = buttons.index(evt_id)
            img = wx.FindWindowById(id=evt_id)
            img.SetBitmapLabel(bmps[self.kind])  # selected -> color
            set_dyn_ctrls()
            if not self.value and self.kind == 3:
                remove_targets()
            event.Skip()

        buttons = (
            wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(),
            wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef()
        )
        button_sizer = wx.GridBagSizer(0, 0)
        bmps = []
        kinds = self.plugin.text.kinds if self.value \
            else self.plugin.text.kinds[:-1]
        for i, icon in enumerate(kinds):
            btn_id = buttons[i]
            bmp = wx.Bitmap(join(ICON_DIR, icon + ".png"), wx.BITMAP_TYPE_PNG)
            bmps.append(bmp)
            g = grayed(bmp)
            b = wx.BitmapButton(
                panel,
                btn_id,
                g if i != kind else bmp,
                size=(32, 32),
                style=wx.NO_BORDER
            )
            b.SetBitmapCurrent(bmp)
            if i == 2:
                b.SetToolTip(text.limit)
            button_sizer.Add(b, (0, 2 * i))
            if i < 3:
                button_sizer.Add((18, -1), (0, 2 * i + 1))
            button_sizer.Add(wx.StaticText(panel, -1, icon), (1, 2 * i), (1, 2))
            b.Bind(wx.EVT_BUTTON, on_click, id=btn_id)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        if not self.value or self.value in ("Gr", "Single"):
            left_sizer.Add(ts_label)
            left_sizer.Add(ts_ctrl, 0, wx.TOP | wx.EXPAND, 2)
        main_sizer.Add(left_sizer, 0, wx.EXPAND | wx.RIGHT, 10)

        s_sizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, ""),
            wx.VERTICAL
        )
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        s_sizer.Add(self.right_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.right_sizer.Add(button_sizer)

        self.ids = [
            wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(),
            wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef()
        ]

        def detach_control(wxid):
            # noinspection PyArgumentList
            cntrl = wx.FindWindowById(id=wxid)
            if cntrl:
                self.right_sizer.Detach(cntrl)
                cntrl.Destroy()

        def set_dyn_ctrls(dat=None, knd=None):
            right_sizer = self.right_sizer
            knd = self.kind if knd is None else knd
            for ctrl_id in self.ids:
                detach_control(ctrl_id)
            style = wx.TOP | wx.EXPAND
            flag = 0 if knd in (1, 2) else 1
            cntrl1 = wx.TextCtrl(
                panel,
                self.ids[0],
                dat[0] if dat and (knd != 2 or len(dat) == 2) else ""
            )  # for backward compatibility ^^^^^^^^^^^^^^
            lbl1 = wx.StaticText(panel, self.ids[2], self.text.lbls1[knd])
            if knd == 2:
                if dat and len(dat) == 1:  # for backward compatibility
                    dat.insert(0, "")
                cntrl2 = eg.FileBrowseButton(
                    panel,
                    self.ids[1],
                    toolTip=text.toolTipFile,
                    dialogTitle=text.browseFile,
                    buttonText=eg.text.General.browse,
                    startDirectory=eg.folderPath.Documents,
                    initialValue=dat[1] if dat is not None else "",
                    fileMask=text.fMask,
                )
            else:
                cntrl2 = wx.TextCtrl(
                    panel,
                    self.ids[1],
                    dat[1] if dat is not None else "",
                    style=wx.TE_MULTILINE if knd != 1 else 0
                )
            lbl2 = wx.StaticText(panel, self.ids[3], self.text.lbls2[knd])
            right_sizer.Add(lbl1, 0, wx.TOP, 10)
            right_sizer.Add(cntrl1, 0, style, 1)
            right_sizer.Add(lbl2, 0, wx.TOP, 10)
            right_sizer.Add(cntrl2, flag, style, 1)

            if knd in (1, 3):
                if knd == 1:
                    lbl3 = wx.StaticText(panel, self.ids[4], self.text.lbls2[0])
                    cntrl3 = wx.TextCtrl(
                        panel,
                        self.ids[5],
                        dat[2] if dat and len(dat) > 2 else ""
                    )
                else:
                    lbl3 = wx.StaticText(panel, self.ids[4], self.text.lbl3)
                    cntrl3 = eg.FileBrowseButton(
                        panel,
                        self.ids[5],
                        toolTip=text.toolTipIcon,
                        dialogTitle=text.browseIcon,
                        buttonText=eg.text.General.browse,
                        startDirectory=eg.folderPath.Pictures,
                        initialValue=dat[2] if dat and len(dat) > 2 else "",
                        fileMask=text.iMask,
                    )
                right_sizer.Add(lbl3, 0, wx.TOP, 10)
                right_sizer.Add(cntrl3, 0, style, 1)
            right_sizer.Layout()

        suff_lbl = wx.StaticText(panel, -1, text.suffix)
        suff_ctrl = wx.TextCtrl(panel, -1, suff)
        suff_lbl.SetToolTip(text.toolTipSuff)
        suff_ctrl.SetToolTip(text.toolTipSuff)
        suff_sizer = wx.BoxSizer(wx.HORIZONTAL)
        suff_sizer.Add(suff_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        suff_sizer.Add(suff_ctrl, 1, wx.EXPAND)
        r_sizer = wx.BoxSizer(wx.VERTICAL)
        r_sizer.Add(wx.StaticText(panel, -1, text.cont))
        r_sizer.Add(s_sizer, 1, wx.EXPAND | wx.TOP, -5)
        r_sizer.Add(suff_sizer, 0, wx.EXPAND | wx.TOP, 5)
        main_sizer.Add(r_sizer, 1, wx.EXPAND)
        panel.sizer.Add(main_sizer, 1, wx.ALL | wx.EXPAND, 5)

        if not self.plugin.wsC:
            panel.Enable(False)

        smart_button = wx.Button(panel.dialog, -1, text.smartLabel)
        smart_button.SetToolTip(text.smartTip)
        panel.dialog.buttonRow.Add(smart_button)

        def on_smart_button(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)

        smart_button.Bind(wx.EVT_BUTTON, on_smart_button)

        set_dyn_ctrls(data=("", "", ""), knd=1)  # dialog - size adjustment
        panel.GetParent().GetParent().Show()
        wx.CallAfter(set_dyn_ctrls, data)

        while panel.Affirmed():
            data = []
            if self.value == "Gr":
                ts = ts_ctrl.GetStringSelection()
            elif self.value == "Single":
                ts = ts_ctrl.GetValue()
            else:
                ts = self.ts
            data.append(wx.FindWindowById(id=self.ids[0]).GetValue())
            data.append(wx.FindWindowById(id=self.ids[1]).GetValue())
            if self.kind in (1, 3):
                data.append(wx.FindWindowById(self.ids[5]).GetValue())
            panel.SetResult(
                self.kind,
                ts,
                data,
                suff_ctrl.GetValue()
            )


class PushScreenshot(eg.ActionBase):
    ix = 0
    ts = None
    value = None

    class Text(eg.TranslatableStrings):
        type = "Screenshot or clipboard options"
        types = ("Fullscreen", "Region", "Clipboard")
        descr = "Optional message:"
        suffix = "Event suffix when completed:"
        toolTipSuff = '''If you fill out this field, then after sending 
of push(-es) it will be triggered an event, carrying  a result (as a payload). 
If the field is left blank, the event will not be triggered.'''
        smartLabel = "Apply, push and close"
        smartTip = "The changes are saved, push is sent and the dialog closes."
        x_coord = "X-coordinate of the upper left corner:"
        y_coord = "Y-coordinate of the upper left corner:"
        width = "The width of the region:"
        height = "The height of the region:"
        noData = "PushBullet: The image can not be sent, there are no image datas"

    def __call__(
        self,
        trgts=None,
        region=(0, 0, 0, 0),
        descr="",
        suff="",
        src=None
    ):
        if trgts is None:
            trgts = []
        src = int(region != (0, 0, 0, 0)) if src is None else src
        if self.value:
            trgts = [['Everything', None, 'everything', True]]
        if src == 2:
            im = grabclipboard()
            filename = "%s__clipboard.png"
        elif src == 1:
            im = grab(bbox=region)
            filename = "%s__region.png"
        else:
            im = grab()
            filename = "%s__screenshot.png"
        file_path = join(
            eg.folderPath.TemporaryFiles,
            filename % self.plugin.nickname
        )
        if not im:
            eg.PrintError(self.text.noData)
            return
        im.save(file_path)
        descr = eg.ParseString(descr)
        suff = eg.ParseString(suff)
        push_thread = Thread(
            target=self.plugin.push,
            args=(2, trgts, (descr, file_path), suff)
        )
        push_thread.start()

    def GetLabel(self, trgts, region, descr, suff, src):
        src = int(region != (0, 0, 0, 0)) if src is None else src
        type_ = self.text.types[src]
        if self.value:
            return "%s: %s: %s" % (self.name, descr, type_)
        elif trgts:
            ts = [i[0] for i in trgts if i[3]]
            ts = repr(ts) if len(ts) > 1 else '"%s"' % ts[0]
            return "%s: %s: %s to %s" % (self.name, descr, type_, ts)

    def Configure(
        self,
        trgts=None,
        region=(0, 0, 0, 0),
        descr="",
        suff="",
        src=None
    ):
        if trgts is None:
            trgts = []
        text = self.text
        panel = eg.ConfigPanel(self)
        ts_label = wx.Size(1, 1)
        ts_ctrl = wx.Size(1, 1)
        if self.value:
            self.ts = []
        else:
            self.ts = deepcopy(trgts)
            for t in self.ts:
                if tuple(t[:3]) not in self.plugin.targets:
                    self.ts.remove(t)
            tmp = []
            for t in self.plugin.targets:
                tmp2 = [i[:3] for i in self.ts]
                if list(t) in tmp2:
                    tmp.append(list(self.ts[tmp2.index(list(t))]))
                else:
                    tmp.append([t[0], t[1], t[2], False])
            self.ts = tmp
            items = [n[0] for n in self.ts]
            ts_label = wx.StaticText(panel, -1, self.plugin.text.tsLabel)
            ts_ctrl = wx.CheckListBox(
                panel,
                -1,
                choices=items,
                size=(-1, 200),
            )
            for i, item in enumerate(self.ts):
                ts_ctrl.Check(i, item[3])

            def after_check_list_box():
                ts_ctrl.SetSelection(self.ix)
                if ts_ctrl.IsChecked(self.ix):
                    self.ts[self.ix][3] = True
                else:
                    self.ts[self.ix][3] = False

            def on_check_list_box(evt):
                self.ix = evt.GetInt()
                wx.CallAfter(after_check_list_box)
                evt.Skip()

            ts_ctrl.Bind(wx.EVT_CHECKLISTBOX, on_check_list_box)

            def update_size():
                h = left_sizer.GetSize()[1]
                ts_ctrl.SetSize((-1, h - 17))

            def on_size(event):
                wx.CallAfter(update_size)
                event.Skip()

            panel.Bind(wx.EVT_SIZE, on_size)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        if not self.value:
            left_sizer = wx.BoxSizer(wx.VERTICAL)
            left_sizer.Add(ts_label)
            left_sizer.Add(ts_ctrl, 0, wx.TOP | wx.EXPAND, 2)
            main_sizer.Add(left_sizer, 0, wx.EXPAND | wx.RIGHT, 10)

        s_sizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.type),
            wx.VERTICAL
        )
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        s_sizer.Add(right_sizer, 1, wx.EXPAND | wx.ALL, 5)

        src = int(region != (0, 0, 0, 0)) if src is None else src
        rb0 = panel.RadioButton(src == 0, text.types[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(src == 1, text.types[1])
        rb2 = panel.RadioButton(src == 2, text.types[2])
        rb_sizer = wx.BoxSizer(wx.HORIZONTAL)
        rb_sizer.Add(rb0)
        rb_sizer.Add(rb1, 0, wx.LEFT | wx.RIGHT, 25)
        rb_sizer.Add(rb2)
        right_sizer.Add(rb_sizer)
        region_sizer = wx.FlexGridSizer(4, 2, 2, 15)
        xlbl = wx.StaticText(panel, 0, text.x_coord)
        ylbl = wx.StaticText(panel, 0, text.y_coord)
        wlbl = wx.StaticText(panel, 0, text.width)
        hlbl = wx.StaticText(panel, 0, text.height)
        xctrl = eg.SpinIntCtrl(
            panel,
            -1,
            region[0],
            min=0,
            max=10000
        )
        yctrl = eg.SpinIntCtrl(
            panel,
            -1,
            region[1],
            min=0,
            max=10000
        )
        wctrl = eg.SpinIntCtrl(
            panel,
            -1,
            region[2],
            min=0,
            max=10000
        )
        hctrl = eg.SpinIntCtrl(
            panel,
            -1,
            region[3],
            min=0,
            max=10000
        )

        def on_radio_box(evt=None):
            flg = rb1.GetValue()
            xlbl.Enable(flg)
            xctrl.Enable(flg)
            ylbl.Enable(flg)
            yctrl.Enable(flg)
            wlbl.Enable(flg)
            wctrl.Enable(flg)
            hlbl.Enable(flg)
            hctrl.Enable(flg)
            if not flg:
                xctrl.SetValue(0)
                yctrl.SetValue(0)
                wctrl.SetValue(0)
                hctrl.SetValue(0)
            if evt:
                evt.Skip()

        rb0.Bind(wx.EVT_RADIOBUTTON, on_radio_box)
        rb1.Bind(wx.EVT_RADIOBUTTON, on_radio_box)
        rb2.Bind(wx.EVT_RADIOBUTTON, on_radio_box)
        on_radio_box()

        des_lbl = wx.StaticText(panel, -1, text.descr)
        des_ctrl = wx.TextCtrl(panel, -1, descr)
        region_sizer.Add(xlbl, 0, wx.ALIGN_CENTER_VERTICAL)
        region_sizer.Add(xctrl)
        region_sizer.Add(ylbl, 0, wx.ALIGN_CENTER_VERTICAL)
        region_sizer.Add(yctrl)
        region_sizer.Add(wlbl, 0, wx.ALIGN_CENTER_VERTICAL)
        region_sizer.Add(wctrl)
        region_sizer.Add(hlbl, 0, wx.ALIGN_CENTER_VERTICAL)
        region_sizer.Add(hctrl)
        right_sizer.Add(region_sizer, 0, wx.TOP, 13)
        desc_sizer = wx.BoxSizer(wx.HORIZONTAL)
        desc_sizer.Add(des_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        desc_sizer.Add(des_ctrl, 1, wx.EXPAND)
        right_sizer.Add(desc_sizer, 0, wx.EXPAND | wx.TOP, 15)

        suff_lbl = wx.StaticText(panel, -1, text.suffix)
        suff_ctrl = wx.TextCtrl(panel, -1, suff)
        suff_lbl.SetToolTip(text.toolTipSuff)
        suff_ctrl.SetToolTip(text.toolTipSuff)
        suff_sizer = wx.BoxSizer(wx.HORIZONTAL)
        suff_sizer.Add(suff_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        suff_sizer.Add(suff_ctrl, 1, wx.EXPAND)
        r_sizer = wx.BoxSizer(wx.VERTICAL)
        r_sizer.Add(s_sizer, 1, wx.EXPAND | wx.TOP, 0)
        r_sizer.Add(suff_sizer, 0, wx.EXPAND | wx.TOP, 5)
        main_sizer.Add(r_sizer, 1, wx.EXPAND)
        panel.sizer.Add(main_sizer, 1, wx.ALL | wx.EXPAND, 5)

        if not self.plugin.wsC:
            panel.Enable(False)

        smart_button = wx.Button(panel.dialog, -1, text.smartLabel)
        smart_button.SetToolTip(text.smartTip)
        panel.dialog.buttonRow.Add(smart_button)

        def on_smart_button(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)

        smart_button.Bind(wx.EVT_BUTTON, on_smart_button)

        while panel.Affirmed():
            # data = []
            panel.SetResult(
                self.ts,
                (
                    xctrl.GetValue(),
                    yctrl.GetValue(),
                    wctrl.GetValue(),
                    hctrl.GetValue()
                ),
                des_ctrl.GetValue(),
                suff_ctrl.GetValue(),
                rb1.GetValue() + 2 * rb2.GetValue()
            )


class DeletePush(eg.ActionBase):

    class Text(eg.TranslatableStrings):
        lbl = "Push iden:"

    def __call__(self, iden=""):
        iden = eg.ParseString(iden)
        self.plugin.delete_push(iden)

    def Configure(self, iden=""):
        panel = eg.ConfigPanel()
        lbl = wx.StaticText(panel, -1, self.text.lbl)
        push_ctrl = wx.TextCtrl(panel, -1, iden)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(push_ctrl, 1, wx.EXPAND | wx.LEFT, 8)
        panel.sizer.Add(main_sizer, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                push_ctrl.GetValue(),
            )


class SendReply(eg.ActionBase):

    class Text(eg.TranslatableStrings):
        lblPush = "Reply push:"
        lblMsg = "Reply message:"

    def __call__(self, push="{eg.event.payload[3]}", msg=""):
        push = self.plugin.parse_argument(push)
        msg = eg.ParseString(msg)
        self.plugin.send_reply(push, msg)

    def GetLabel(self, push, msg):
        msg = msg.replace("\n", "<LF>")
        return "%s: %s" % (self.name, msg if len(msg) < 13 else msg[:12] + " .....")

    def Configure(self, push="{eg.event.payload[3]}", msg=""):
        panel = eg.ConfigPanel()
        lbl_push = wx.StaticText(panel, -1, self.text.lblPush)
        lbl_msg = wx.StaticText(panel, -1, self.text.lblMsg)
        push_ctrl = wx.TextCtrl(panel, -1, push)
        msg_ctrl = wx.TextCtrl(panel, -1, msg, style=wx.TE_MULTILINE)
        main_sizer = wx.FlexGridSizer(2, 2, 10, 10)

        main_sizer.Add(lbl_msg, 0, wx.TOP, 3)
        main_sizer.Add(msg_ctrl, 1, wx.EXPAND)
        main_sizer.Add(lbl_push, 0, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(push_ctrl, 0, wx.EXPAND)
        main_sizer.AddGrowableRow(0)
        main_sizer.AddGrowableCol(1)

        panel.sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                push_ctrl.GetValue(),
                msg_ctrl.GetValue()
            )


class Dismiss(eg.ActionBase):

    class Text(eg.TranslatableStrings):
        lblPush = "Push dictionary (for mirror) or push iden:"

    def __call__(self, push_dict="{eg.event.payload[-1]}"):
        push_dict = self.plugin.parse_argument(push_dict)
        self.plugin.dismiss(push_dict)

    def GetLabel(self, pushDict):
        return "%s: %s" % (self.name, pushDict)

    def Configure(self, pushDict="{eg.event.payload[-1]}"):
        panel = eg.ConfigPanel()
        lbl_push = wx.StaticText(panel, -1, self.text.lblPush)
        push_ctrl = wx.TextCtrl(panel, -1, pushDict)
        main_sizer = wx.FlexGridSizer(1, 2, 10, 10)

        main_sizer.Add(lbl_push, 0, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(push_ctrl, 0, wx.EXPAND)
        main_sizer.AddGrowableCol(1)
        panel.sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                push_ctrl.GetValue()
            )


class SendSMS(eg.ActionBase):

    class Text(eg.TranslatableStrings):
        device = "Device:"
        recip = "Recipient:"
        message = "Message:"
        smartLabel = "Apply, send and close"
        smartTip = "The changes are saved, SMS is sent and the dialog closes."

    def __call__(self, dev="", recip="", msg=""):
        dev = self.plugin.parse_argument(dev)
        recip = eg.ParseString(recip)
        msg = eg.ParseString(msg)
        self.plugin.send_sms(dev, recip, msg)

    def GetLabel(self, dev, recip, msg):
        msg = msg.replace("\n", "<LF>")
        return "%s: %s: %s: %s" % (
            self.name,
            dev,
            recip,
            msg if len(msg) < 13 else msg[:12] + " ....."
        )

    def Configure(self, dev="", recip="", msg=""):
        panel = eg.ConfigPanel()
        lbl_dev = wx.StaticText(panel, -1, self.text.device)
        lbl_rec = wx.StaticText(panel, -1, self.text.recip)
        lbl_msg = wx.StaticText(panel, -1, self.text.message)
        try:
            choices = list(self.plugin.get_sm_sdevices().iterkeys())
        except ValueError:
            choices = []
        ctrl_dev = wx.Choice(panel, -1, choices=choices)
        if choices:
            ctrl_dev.SetStringSelection(dev)
        phbook = self.plugin.get_phonebook(dev)
        ctrl_rec = PhonebookChoice(panel, -1, phbook, self.plugin, recip)
        ctrl_msg = wx.TextCtrl(panel, -1, msg, style=wx.TE_MULTILINE)
        main_sizer = wx.FlexGridSizer(3, 2, 10, 10)
        main_sizer.Add(lbl_dev, 0, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(ctrl_dev, 0, wx.EXPAND)
        main_sizer.Add(lbl_rec, 0, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(ctrl_rec, 0, wx.EXPAND)
        main_sizer.Add(lbl_msg, 0, wx.TOP, 3)
        main_sizer.Add(ctrl_msg, 1, wx.EXPAND)
        main_sizer.AddGrowableRow(2)
        main_sizer.AddGrowableCol(1)

        panel.sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 10)

        def on_dev(evt=None):
            devc = ctrl_dev.GetStringSelection()
            pbook = self.plugin.get_phonebook(devc)
            ctrl_rec.Set(pbook)
            if evt:
                evt.Skip()

        ctrl_dev.Bind(wx.EVT_CHOICE, on_dev)
        on_dev()

        smart_button = wx.Button(panel.dialog, -1, self.text.smartLabel)
        smart_button.SetToolTip(self.text.smartTip)
        panel.dialog.buttonRow.Add(smart_button)

        def on_smart_button(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)

        smart_button.Bind(wx.EVT_BUTTON, on_smart_button)

        while panel.Affirmed():
            panel.SetResult(
                ctrl_dev.GetStringSelection(),
                ctrl_rec.get_sel(),
                ctrl_msg.GetValue()
            )


class SendSMS2list(eg.ActionBase):
    enc = None

    class Text(eg.TranslatableStrings):
        device = "Device:"
        filepath = "File with list of numbers:"
        message = "Message:"
        smartLabel = "Apply, send and close"
        smartTip = "The changes are saved, SMS is sent and the dialog closes."
        fileMask = (
            "CSV files (*.csv)|*.csv"
            "|TXT files (*.txt)|*.txt"
            "|All files (*.*)|*.*"
        )
        msgMask = (
            "TXT files (*.txt)|*.txt"
            "|All files (*.*)|*.*"
        )
        toolTipFile = 'Type filename or click browse to choose file'
        browseFile = 'Choose a file'
        src = "Message source:"
        srcs = ("File", "Text box")
        encoding = "File encoding:"

    def __call__(self, dev="", filepath="", msg="", src=1, enc=0):
        col = 0
        sep = "\t"
        filepath = eg.ParseString(filepath)
        msg = eg.ParseString(msg)
        if not src:
            f = codecs.open(msg, 'r', enc, 'replace')
            msg = f.read()
            f.close()
        f = open(filepath, 'r')
        data = [item.split(sep) for item in f.readlines()]
        tmp = [item[col].strip() for item in data]
        numbers = []
        for item in tmp:
            num = check(item)
            if num:
                numbers.append(num)
        f.close()
        self.plugin.send_sm_smulti(numbers, msg, dev)

    def GetLabel(self, dev, filepath, msg, src, enc):
        msg = msg.replace("\n", "<LF>")
        return "%s: %s: %s: %s" % (
            self.name,
            dev,
            filepath,
            msg if len(msg) < 13 else msg[:12] + " ....."
        )

    # noinspection PyArgumentList
    def Configure(self, dev="", filepath="", msg="", src=1, enc=""):
        self.enc = enc
        panel = eg.ConfigPanel()
        text = self.text
        ctrls = [wx.NewIdRef(), wx.NewIdRef()]
        lbl_dev = wx.StaticText(panel, -1, text.device)
        lbl_path = wx.StaticText(panel, -1, text.filepath)
        try:
            choices = list(self.plugin.get_sm_sdevices().iterkeys())
        except ValueError:
            choices = []
        ctrl_dev = wx.Choice(panel, -1, choices=choices)
        if choices:
            ctrl_dev.SetStringSelection(dev)

        file_ctrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip=text.toolTipFile,
            dialogTitle=text.browseFile,
            buttonText=eg.text.General.browse,
            startDirectory=eg.folderPath.Documents,
            initialValue=filepath,
            fileMask=text.fileMask
        )
        src_label = wx.StaticText(panel, -1, text.src)
        rb0 = panel.RadioButton(src == 0, self.text.srcs[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(src == 1, self.text.srcs[1])

        src_sizer = wx.BoxSizer(wx.HORIZONTAL)
        src_sizer.Add(rb0)
        src_sizer.Add(rb1, 0, wx.LEFT, 10)
        main_sizer = wx.FlexGridSizer(0, 2, 10, 10)

        main_sizer.Add(lbl_dev, 0, flag=wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(ctrl_dev, 0, flag=wx.EXPAND)
        main_sizer.Add(lbl_path, 0, flag=wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(file_ctrl, 0, flag=wx.EXPAND)
        main_sizer.Add(src_label, 0, flag=wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(src_sizer, 0)
        main_sizer.AddGrowableCol(1)

        def on_source2(flag=False):
            if rb1.GetValue():
                lbl_msg = wx.StaticText(panel, -1, text.message)
                ctrl_msg = wx.TextCtrl(
                    panel,
                    ctrls[0],
                    "",
                    style=wx.TE_MULTILINE
                )
                if flag:
                    ctrl_msg.ChangeValue(msg)
                main_sizer.Add(lbl_msg, 0, wx.TOP, 3)
                main_sizer.Add(ctrl_msg, 1, wx.EXPAND)
                main_sizer.AddGrowableRow(3)
            else:
                lbl_msg = wx.StaticText(panel, -1, text.message)
                ctrl_msg = eg.FileBrowseButton(
                    panel,
                    ctrls[0],
                    toolTip=text.toolTipFile,
                    dialogTitle=text.browseFile,
                    buttonText=eg.text.General.browse,
                    startDirectory=eg.folderPath.Documents,
                    initialValue="",
                    fileMask=text.msgMask
                )
                lbl_enc = wx.StaticText(panel, -1, text.encoding)
                enc_types = []
                for key, value in aliases.aliases.items():
                    if value not in enc_types:
                        enc_types.append(value)

                enc_types = sorted(enc_types)
                enc_ctrl = wx.Choice(panel, ctrls[1], choices=enc_types)
                if self.enc == "" and eg.systemEncoding in enc_types:
                    self.enc = eg.systemEncoding
                if flag:
                    ctrl_msg.SetValue(msg)

                enc_ctrl.SetStringSelection(self.enc)
                main_sizer.Add(lbl_msg, 0, wx.TOP, 3)
                main_sizer.Add(ctrl_msg, 1, wx.EXPAND)
                main_sizer.Add(lbl_enc, 0, wx.TOP, 3)
                main_sizer.Add(enc_ctrl, 1, wx.EXPAND)
            main_sizer.Layout()

        on_source2(True)

        def on_source(evt):
            chldrns = list(main_sizer.GetChildren())
            cnt = len(chldrns)
            if cnt == 8:
                main_sizer.RemoveGrowableRow(3)
            for i in range(cnt - 1, 5, -1):
                win = chldrns[i].GetWindow()
                main_sizer.Detach(i)
                win.Destroy()
            on_source2()
            evt.Skip()

        rb0.Bind(wx.EVT_RADIOBUTTON, on_source)
        rb1.Bind(wx.EVT_RADIOBUTTON, on_source)

        panel.sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 10)

        smart_button = wx.Button(panel.dialog, -1, text.smartLabel)
        smart_button.SetToolTip(text.smartTip)
        panel.dialog.buttonRow.Add(smart_button)

        def on_smart_button(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)

        smart_button.Bind(wx.EVT_BUTTON, on_smart_button)

        while panel.Affirmed():
            src = int(rb1.GetValue())
            ctrl_enc = wx.FindWindowById(ctrls[1])
            panel.SetResult(
                ctrl_dev.GetStringSelection(),
                file_ctrl.GetValue(),
                wx.FindWindowById(ctrls[0]).GetValue(),
                src,
                ctrl_enc.GetStringSelection() if not src else "",
            )


class SendSMSmulti(eg.ActionBase):
    phbook = None

    class Text(eg.TranslatableStrings):
        message = "Message:"
        smartLabel = "Apply, send and close"
        smartTip = "The changes are saved, SMS is sent and the dialog closes."

    def __call__(self, dev="", recips=None, msg=""):
        if recips is None:
            recips = []
        dev = self.plugin.parse_argument(dev)
        msg = eg.ParseString(msg)
        self.plugin.send_sm_smulti(recips, msg, dev)

    def GetLabel(self, dev, recips, msg):
        msg = msg.replace("\n", "<LF>")
        return "%s: %s: %s" % (
            self.name,
            dev,
            msg if len(msg) < 13 else msg[:12] + " ....."
        )

    def Configure(self, dev="", recips2=None, msg=""):
        if recips2 is None:
            recips2 = []
        text = self.text
        ptext = self.plugin.text

        recips = recips2
        if recips2:  # for backward compatibility
            if dev is not None and isinstance(recips2[0], unicode):
                recips = []
                for recip in recips2:
                    tmp = [dev]
                    nm, nr = get_nm_nr(recip)
                    tmp.append(nm)
                    tmp.append(nr)
                    recips.append(tmp)

        panel = eg.ConfigPanel()
        lbl_dev = wx.StaticText(panel, -1, ptext.device)
        lbl_recs = wx.StaticText(panel, -1, ptext.recips)
        lbl_msg = wx.StaticText(panel, -1, text.message)
        try:
            choices = list(self.plugin.get_sm_sdevices().iterkeys())
        except ValueError:
            choices = []
        ctrl_dev = wx.Choice(panel, -1, choices=choices)
        main_sizer = wx.FlexGridSizer(2, 2, 10, 10)

        static_box = wx.StaticBox(panel, -1, "")
        static_box_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_sizer = wx.FlexGridSizer(2, 2, 10, 10)
        bottom_sizer.AddGrowableCol(1)
        list_ctrl = Table(
            panel,
            ptext.header,
            3,
            ("DevName", "Recipient name", "XXXXXXXXXXXXXXXX")
        )
        list_ctrl.set_data(recips)
        lbl_rec = wx.StaticText(panel, -1, ptext.recip)
        ctrl_rec = PhonebookChoice(
            panel,
            -1,
            [],
            self.plugin,
            "",
        )
        btn_add = wx.Button(panel, -1, ptext.insert)
        btn_del = wx.Button(panel, -1, ptext.delete)
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
        ctrl_msg = wx.TextCtrl(panel, -1, msg, style=wx.TE_MULTILINE)

        main_sizer.Add(lbl_recs, 0, wx.TOP, 6)
        main_sizer.Add(static_box_sizer, 1, wx.EXPAND)
        main_sizer.Add(lbl_msg, 0, wx.TOP, 3)
        main_sizer.Add(ctrl_msg, 1, wx.EXPAND)
        main_sizer.AddGrowableRow(0)
        main_sizer.AddGrowableRow(1)
        main_sizer.AddGrowableCol(1)

        panel.sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 10)

        def set_row():
            devc = ctrl_dev.GetStringSelection()
            sr_nm, sr_nr = get_nm_nr(ctrl_rec.get_sel())
            list_ctrl.set_row((devc, sr_nm, sr_nr))

        def on_dev(evt):
            devc = ctrl_dev.GetStringSelection()
            phbook = self.plugin.get_phonebook(devc)
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
            devc, sel_nm, sel_nr = list_ctrl.get_row()
            if devc != ctrl_dev.GetStringSelection():
                if dev in ctrl_dev.GetStrings():
                    ctrl_dev.SetStringSelection(devc)
                    phbook = self.plugin.get_phonebook(devc)
                    ctrl_rec.Set(phbook)
            ctrl_rec.SetValue(sel_nm + SEP + sel_nr if sel_nr != "" and sel_nm != "" else sel_nr)
            evt.Skip()

        list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, on_select)

        def on_change(evt=None):
            sel_cnt = list_ctrl.GetSelectedItemCount()
            enable = sel_cnt > 0
            if not enable:
                ctrl_rec.SetValue("")
            btn_del.Enable(enable)
            ctrl_rec.Enable(enable)
            ctrl_dev.Enable(enable)
            lbl_rec.Enable(enable)
            lbl_dev.Enable(enable)
            if evt:
                evt.Skip()

        list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, on_change)
        list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, on_change)
        on_change()

        def on_delete(evt):
            list_ctrl.DeleteItem(list_ctrl.get_selected_index())
            evt.Skip()

        btn_del.Bind(wx.EVT_BUTTON, on_delete)

        def on_add(evt):
            list_ctrl.add_row()
            if ctrl_dev.GetStringSelection():
                set_row()
            evt.Skip()

        btn_add.Bind(wx.EVT_BUTTON, on_add)

        smart_button = wx.Button(panel.dialog, -1, text.smartLabel)
        smart_button.SetToolTip(text.smartTip)
        panel.dialog.buttonRow.Add(smart_button)

        def on_smart_button(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)

        smart_button.Bind(wx.EVT_BUTTON, on_smart_button)

        while panel.Affirmed():
            panel.SetResult(
                None,
                list_ctrl.get_data(),
                ctrl_msg.GetValue()
            )


class SendSMSgroup(eg.ActionBase):

    class Text(eg.TranslatableStrings):
        group = "Group:"
        message = "Message:"
        smartLabel = "Apply, send and close"
        smartTip = "The changes are saved, SMS is sent and the dialog closes."

    def __call__(self, group="", msg=""):
        group = eg.ParseString(group)
        msg = eg.ParseString(msg)
        tmp = [itm[0] for itm in self.plugin.smsGroups]
        if group in tmp:
            ix = tmp.index(group)
            self.plugin.send_sm_smulti(self.plugin.smsGroups[ix][1], msg, None)

    def GetLabel(self, group, msg):
        msg = msg.replace("\n", "<LF>")
        return "%s: %s: %s" % (
            self.name,
            group,
            msg if len(msg) < 13 else msg[:12] + " ....."
        )

    def Configure(self, group="", msg=""):
        panel = eg.ConfigPanel()
        lbl_grp = wx.StaticText(panel, -1, self.text.group)
        lbl_msg = wx.StaticText(panel, -1, self.text.message)
        ctrl_group = wx.Choice(
            panel,
            -1,
            choices=[itm[0] for itm in self.plugin.smsGroups],
        )
        ctrl_group.SetStringSelection(group)
        ctrl_msg = wx.TextCtrl(panel, -1, msg, style=wx.TE_MULTILINE)
        main_sizer = wx.FlexGridSizer(2, 2, 10, 10)

        main_sizer.Add(lbl_grp, 0, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(ctrl_group, 0, wx.EXPAND)
        main_sizer.Add(lbl_msg, 0, wx.TOP, 3)
        main_sizer.Add(ctrl_msg, 1, wx.EXPAND)
        panel.sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 10)

        smart_button = wx.Button(panel.dialog, -1, self.text.smartLabel)
        smart_button.SetToolTip(self.text.smartTip)
        main_sizer.AddGrowableRow(1)
        main_sizer.AddGrowableCol(1)

        panel.dialog.buttonRow.Add(smart_button)

        def on_smart_button(event):
            panel.dialog.DispatchEvent(event, eg.ID_TEST)
            panel.dialog.DispatchEvent(event, wx.ID_OK)

        smart_button.Bind(wx.EVT_BUTTON, on_smart_button)

        while panel.Affirmed():
            panel.SetResult(
                ctrl_group.GetStringSelection(),
                ctrl_msg.GetValue()
            )


class JumpIf(eg.ActionBase):
    # iconFile = "../EventGhost/icons/NewJumpIf"

    class Text(eg.TranslatableStrings):
        text1 = "If:"
        text2 = "Jump to:"
        mesg1 = "Select the macro..."
        mesg2 = (
            "Please select the macro that should be executed, if the "
            "condition is/is not fulfilled."
        )
        tooltip = "Enter a list of file extensions, separated by a comma " \
                  "(eg txt, pdf, mp3)"

    def __call__(self, link, kind=0, fl="", exts=""):
        fl = eg.ParseString(fl)
        exts = exts.replace(" ", "").split(",")
        dummy, f_ext = splitext(fl)
        flinexts = f_ext.lower()[1:] in [item.lower() for item in exts]
        if flinexts != bool(kind):
            next_item = link.target
            next_index = next_item.parent.GetChildIndex(next_item)
            eg.indent += 1
            eg.programCounter = (next_item, next_index)
        return flinexts != bool(kind)

    def GetLabel(self, link, kind, fl, exts):
        return "%s %s %s%s %s (%s)" % (
            self.text.text2,
            link.target.name,
            self.plugin.text.ifExt,
            ("", self.plugin.text.notLbl)[kind],
            self.plugin.text.inLbl,
            exts,
        )

    def Configure(self, link=None, kind=0, fl="", exts=""):
        text = self.text
        panel = eg.ConfigPanel()
        lbl1 = wx.StaticText(panel, -1, self.plugin.text.file)
        lbl2 = wx.StaticText(panel, -1, self.plugin.text.ext)
        ctrl1 = wx.TextCtrl(panel, -1, fl)
        ctrl1.SetToolTip(text.tooltip)
        ctrl2 = wx.TextCtrl(panel, -1, exts)
        ctrl2.SetToolTip(text.tooltip)
        kind_ctrl = panel.Choice(kind, choices=self.plugin.text.choices)
        link_ctrl = panel.MacroSelectButton(
            eg.text.General.choose,
            text.mesg1,
            text.mesg2,
            link
        )
        labels = (
            panel.StaticText(text.text1),
            panel.StaticText(text.text2),
        )
        eg.EqualizeWidths(labels)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(lbl1)
        main_sizer.Add(ctrl1, 0, wx.EXPAND)
        main_sizer.Add(lbl2, 0, wx.TOP, 12)
        main_sizer.Add(ctrl2, 0, wx.EXPAND)
        sizer = wx.FlexGridSizer(3, 2, 15, 5)

        sizer.Add(labels[0], 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(kind_ctrl)
        sizer.Add(labels[1], 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(link_ctrl, 1, wx.EXPAND)
        sizer.AddGrowableCol(1, 1)

        panel.sizer.Add(main_sizer, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(sizer, 0, wx.TOP | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)

        while panel.Affirmed():
            panel.SetResult(
                link_ctrl.GetValue(),
                kind_ctrl.GetValue(),
                ctrl1.GetValue(),
                ctrl2.GetValue()
            )


class OpenFile(eg.ActionBase):

    class Text(eg.TranslatableStrings):
        open = "Open the file if"
        stop = "and stop the macro"
        tooltip = "Enter a list of file extensions, separated by a comma " \
                  "(eg txt, pdf, mp3)"

    def GetLabel(self, fl, exts, kind, stop):
        return "%s: %s %s%s %s (%s) %s" % (
            self.name,
            fl,
            self.plugin.text.ifExt,
            ("", self.plugin.text.notLbl)[kind],
            self.plugin.text.inLbl,
            exts,
            ("", self.text.stop)[int(stop)]
        )

    def __call__(
        self,
        fl="{eg.event.payload}",
        exts="",
        kind=0,
        stop=True
    ):
        fl = eg.ParseString(fl)
        exts = exts.replace(" ", "").split(",")
        dummy, f_ext = splitext(fl)
        flinexts = f_ext.lower()[1:] in [item.lower() for item in exts]
        if flinexts:
            try:
                startfile(fl)
            except ValueError:
                pass
        if (kind == 1 and flinexts) or (kind == 2 and not flinexts):
            eg.programCounter = None
        return flinexts

    def Configure(
        self,
        fl="{eg.event.payload}",
        exts="",
        kind=0,
        stop=True
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        lbl1 = wx.StaticText(panel, -1, self.plugin.text.file)
        lbl2 = wx.StaticText(panel, -1, self.plugin.text.ext)
        lbl3 = wx.StaticText(panel, -1, text.open)
        ctrl1 = wx.TextCtrl(panel, -1, fl)
        ctrl1.SetToolTip(text.tooltip)
        ctrl2 = wx.TextCtrl(panel, -1, exts)
        ctrl2.SetToolTip(text.tooltip)
        kind_ctrl = panel.Choice(kind, choices=self.plugin.text.choices)
        if_sizer = wx.FlexGridSizer(2, 2, 12, 10)
        if_sizer.Add(lbl3, 0, wx.ALIGN_CENTER_VERTICAL)
        if_sizer.Add(kind_ctrl, 0)
        if_sizer.Add((-1, -1))
        stop_ctrl = panel.CheckBox(stop, text.stop)
        if_sizer.Add(stop_ctrl)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(lbl1)
        main_sizer.Add(ctrl1, 0, wx.EXPAND)
        main_sizer.Add(lbl2, 0, wx.TOP, 12)
        main_sizer.Add(ctrl2, 0, wx.EXPAND)
        main_sizer.Add(if_sizer, 0, wx.TOP, 14)
        panel.sizer.Add(main_sizer, 1, wx.ALL | wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                ctrl1.GetValue(),
                ctrl2.GetValue(),
                kind_ctrl.GetValue(),
                stop_ctrl.GetValue()
            )


class EnableDisablePopups(eg.ActionBase):

    class Text(eg.TranslatableStrings):
        rbLabel = "Persistence of change"
        choices = (
            "Make the change only temporarily",
            "Make the change persistent (and automatically save the document)"
        )
        labels = ("temporarily", "persistent")
        modes = ("On", "Off", "No change", "Toggle")

    def __call__(
        self,
        pic=2,
        mirr=2,
        save=1
    ):
        self.plugin.enable_disable_popups(pic, mirr, save)

    def GetLabel(self, pic, mirr, save):
        return "%s: %i, %i (%s)" % (self.name, pic, mirr, self.text.labels[save])

    def Configure(
        self,
        pic=2,
        mirr=2,
        save=1
    ):
        panel = eg.ConfigPanel(self)
        text = self.text
        pic_ctrl = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.autoOpen,
            choices=text.modes,
            style=wx.RA_SPECIFY_COLS
        )
        pic_ctrl.SetSelection(pic)
        mirr_ctrl = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.enabMirr,
            choices=text.modes,
            style=wx.RA_SPECIFY_COLS
        )
        mirr_ctrl.SetSelection(mirr)

        save_ctrl = wx.RadioBox(
            panel,
            -1,
            text.rbLabel,
            choices=text.choices,
            style=wx.RA_SPECIFY_ROWS
        )
        save_ctrl.SetSelection(save)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(pic_ctrl, 0, wx.EXPAND)
        main_sizer.Add(mirr_ctrl, 0, wx.TOP | wx.EXPAND, 10)
        main_sizer.Add(save_ctrl, 0, wx.TOP | wx.EXPAND, 20)
        panel.sizer.Add(main_sizer, 0, wx.EXPAND | wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                pic_ctrl.GetSelection(),
                mirr_ctrl.GetSelection(),
                save_ctrl.GetSelection()
            )


class GetPopups(eg.ActionBase):

    def __call__(self):
        return bool(self.plugin.autoOpen), bool(self.plugin.enabMirr)
