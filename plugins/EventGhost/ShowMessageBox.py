# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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
from os.path import join
from threading import Thread
from win32con import (
    # constants:
    MB_ABORTRETRYIGNORE, MB_ICONERROR, MB_ICONINFORMATION, MB_ICONQUESTION,
    MB_ICONWARNING, MB_NOFOCUS, MB_OKCANCEL, MB_RETRYCANCEL,
    MB_SYSTEMMODAL, MB_TOPMOST, MB_YESNO, MB_YESNOCANCEL,
)
from win32gui import MessageBox
from winsound import PlaySound, SND_ASYNC

# Local imports
import eg
from eg.WinApi.Dynamic import CreateEvent, SetEvent

class ShowMessageBox(eg.ActionBase):
    retCode = None
    RESULTS = (0, "OK", "CANCEL", "ABORT", "RETRY", "IGNORE", "YES", "NO")
    RES_IDS = (
        wx.ID_OK,
        wx.ID_CANCEL,
        wx.ID_ABORT,
        wx.ID_RETRY,
        wx.ID_IGNORE,
        wx.ID_YES,
        wx.ID_NO,
    )
    name = "Show Message Box"
    description = "Shows a message box."
    iconFile = "icons/Dialog"

    class text:
        main = "General settings:"
        buttons = "Buttons:"
        icon = "Icon:"
        options = "Advanced settings:"
        alias = "Alias:"
        payload = "Payload:"
        title = "Title:"
        body = "Message:"
        wait = "Wait for the Message Box to close"
        radioBoxButtons = [
            "OK",
            "OK, Cancel",
            "Retry, Cancel",
            "Abort, Retry, Ignore",
            "Yes, No",
            "Yes, No, Cancel"
        ]
        radioBoxIcon = [
            "No icon",
            "Information",
            "Question",
            "Warning",
            "Error"
        ]
        radioBoxOptions = [
            "Default",
            "Always on top",
            "No focus",
            "System modal"
        ]
        mbType = "Message Box type"
        mbTypes = (
            "System (Windows)",
            "Tweaked (EventGhost)"
        )
        autoClose0 = "Auto-close timer [s]:"
        autoClose1 = "(0 = feature disabled)"
        yes = "Yes"
        no = "No"
        cancel = "Cancel"
        ok = "OK"
        ignore = "Ignore"
        retry = "Retry"
        abort = "Abort"
        autoClose = "Auto close after %i s"
        aot = "Always on top"
        modal = "Modal"
        play = "Play a system sound"

        #MB_TOPMOST=262144, MB_ABORTRETRYIGNORE=2, MB_ICONERROR=16,
        #MB_ICONINFORMATION=64, MB_ICONQUESTION=32, MB_ICONWARNING=48, MB_NOFOCUS=32768, MB_OK=0,
        #MB_OKCANCEL=1, MB_RETRYCANCEL=5, MB_SYSTEMMODAL=4096, MB_YESNO=4, MB_YESNOCANCEL=3

    def __call__(
        self,
        title = "",
        body = "",
        alias = "",
        payload = "",
        blocking = False,
        options = 0,
        mbType = 0,
        autoClose = 0
    ):
        title = eg.ParseString(title)
        body = eg.ParseString(body)
        alias = eg.ParseString(alias)
        payload = eg.ParseString(payload)
        if not isinstance(autoClose, int):
            try:
                autoClose = int(eg.ParseString(autoClose))
            except:
                autoClose = 0
        if mbType:
            event = CreateEvent(None, 0, 0, None) if blocking else None
            wx.CallAfter(self.showTweakedBox, None, title, body, alias, payload, options, autoClose, event)
            if blocking:
                #print "Waiting ..."
                eg.actionThread.WaitOnEvent(event, 999999999999)
                return self.retCode
        else:
            if blocking:
                return self.showMessageBox(title, body, alias, payload, options)
            else:
                Thread(
                    target = self.showMessageBox,
                    args = (title, body, alias, payload, options)
                ).start()
                return None

    def Configure(
        self,
        title = "",
        body = "",
        alias = "",
        payload = "",
        blocking = False,
        options = 0,
        mbType = 0,
        autoClose = 0
    ):
        ids = (wx.NewId(), wx.NewId(), wx.NewId())

        def getOptions(mbt):
            result = buttonsArr[buttonsCtrl.GetSelection()]
            result += iconArr[iconCtrl.GetSelection()]
            if not mbt:
                result += optionsArr[wx.FindWindowById(ids[0]).GetSelection()]
            else:
                tmp = wx.FindWindowById(ids[0]).GetValue()   + \
                    2 * wx.FindWindowById(ids[1]).GetValue() + \
                    4 * wx.FindWindowById(ids[2]).GetValue()
                result += 4096 * tmp
            return result

        buttonsArr = [0, MB_OKCANCEL, MB_RETRYCANCEL, MB_ABORTRETRYIGNORE, MB_YESNO, MB_YESNOCANCEL]
        iconArr = [0, MB_ICONINFORMATION, MB_ICONQUESTION, MB_ICONWARNING, MB_ICONERROR]
        optionsArr = [0, MB_TOPMOST, MB_NOFOCUS, MB_SYSTEMMODAL]
        optionid, iconid, buttonid = self.getFlags(options, mbType)
        panel = eg.ConfigPanel()
        text = self.text
        waitCtrl = wx.CheckBox(panel, -1, text.wait)
        waitCtrl.SetValue(blocking)
        aliasCtrl = panel.TextCtrl(alias)
        st1 = panel.StaticText(text.alias)
        titleCtrl = panel.TextCtrl(title)
        st2 = panel.StaticText(text.title)
        bodyCtrl = panel.TextCtrl(body, style = wx.TE_MULTILINE)
        st3 = panel.StaticText(text.body)
        payloadCtrl = panel.TextCtrl(payload)
        st4 = panel.StaticText(text.payload)
        statSizer = wx.FlexGridSizer(4, 2, 5, 5)
        statSizer.AddGrowableCol(1)
        statSizer.AddGrowableRow(1)
        statSizer.Add(st2, 0, wx.ALIGN_CENTER_VERTICAL)
        statSizer.Add(titleCtrl, 0, wx.EXPAND)
        statSizer.Add(st3, 0, wx.ALIGN_CENTER_VERTICAL)
        statSizer.Add(bodyCtrl, 1, wx.EXPAND)
        statSizer.Add(st1, 0, wx.ALIGN_CENTER_VERTICAL)
        statSizer.Add(aliasCtrl, 0, wx.EXPAND)
        statSizer.Add(st4, 0, wx.ALIGN_CENTER_VERTICAL)
        statSizer.Add(payloadCtrl, 0, wx.EXPAND)
        statBox = wx.StaticBox(panel, -1, self.text.main)
        box0 = wx.StaticBoxSizer(statBox, wx.HORIZONTAL)
        box0.Add(statSizer, 1, wx.EXPAND)
        buttonsCtrl = wx.RadioBox(
            panel,
            label=text.buttons,
            choices=text.radioBoxButtons,
            style=wx.RA_SPECIFY_ROWS
        )
        buttonsCtrl.SetSelection(buttonid)
        iconCtrl = wx.RadioBox(
            panel,
            label=text.icon,
            choices=text.radioBoxIcon,
            style=wx.RA_SPECIFY_ROWS
        )
        iconCtrl.SetSelection(iconid)
        mbTypeCtrl = wx.RadioBox(
            panel,
            label=text.mbType,
            choices=text.mbTypes,
            style=wx.RA_SPECIFY_COLS
        )
        mbTypeCtrl.SetSelection(mbType)

        autoCloseLbl0 = wx.StaticText(panel, -1, text.autoClose0)
        autoCloseLbl1 = wx.StaticText(panel, -1, text.autoClose1)
        autoCloseCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            autoClose,
            min = 0,
            max = 999
        )
        autoCloseSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoCloseSizer.Add(autoCloseLbl0, 0, wx.ALIGN_CENTER_VERTICAL)
        autoCloseSizer.Add(autoCloseCtrl, 0, wx.LEFT | wx.RIGHT, 5)
        autoCloseSizer.Add(autoCloseLbl1, 0, wx.ALIGN_CENTER_VERTICAL)
        optionSizer = wx.BoxSizer(wx.HORIZONTAL)

        def onRadioBox(evt):
            val = evt.GetSelection() != 1
            waitCtrl.Enable(val)
            if not val:
                waitCtrl.SetValue(False)
            evt.Skip()

        def onCheckBox(evt):
            ctrl1 = wx.FindWindowById(ids[1])
            val = evt.IsChecked()
            ctrl1.Enable(not val)
            if val:
                ctrl1.SetValue(True)
            evt.Skip()

        def fillOptSizer(twk, init = False):
            val = optionid if init else (0, 7)[twk]
            autoCloseLbl0.Enable(twk)
            autoCloseLbl1.Enable(twk)
            autoCloseCtrl.Enable(twk)
            waitCtrl.Enable(twk)
            optionSizer.Clear(True)
            if twk:
                stBox = wx.StaticBox(panel, -1, text.options)
                box1 = wx.StaticBoxSizer(stBox, wx.VERTICAL)
                optionSizer.Add(box1, 1, wx.EXPAND)
                ctrl0 = wx.CheckBox(panel, ids[0], text.modal)
                ctrl0.SetValue(val & 1)
                wx.EVT_CHECKBOX(ctrl0, ids[0], onCheckBox)
                ctrl1 = wx.CheckBox(panel, ids[1], text.aot)
                ctrl1.SetValue(val & 2)
                ctrl2 = wx.CheckBox(panel, ids[2], text.play)
                ctrl2.SetValue(val & 4)
                box1.Add(ctrl0, 0, wx.TOP, 5)
                box1.Add(ctrl1, 0, wx.TOP, 5)
                box1.Add(ctrl2, 0, wx.TOP, 5)
                if ctrl0.GetValue():
                    ctrl1.Enable(False)
                    ctrl1.SetValue(True)
                else:
                    ctrl1.Enable(True)
            else:
                autoCloseCtrl.SetValue(0)
                optionCtrl = wx.RadioBox(
                    panel,
                    ids[0],
                    label=text.options,
                    choices=text.radioBoxOptions,
                    style=wx.RA_SPECIFY_ROWS
                )
                wx.EVT_RADIOBOX(optionCtrl, ids[0], onRadioBox)
                optionCtrl.SetSelection(val)
                if val == 1:
                    waitCtrl.Enable(False)
                    waitCtrl.SetValue(False)
                else:
                    waitCtrl.Enable(True)
                optionSizer.Add(optionCtrl, 0, wx.EXPAND)
            panel.sizer.Layout()
        fillOptSizer(mbType, True)

        def onMbType(event):
            wx.CallAfter(fillOptSizer, bool(event.GetSelection()))
            event.Skip()
        mbTypeCtrl.Bind(wx.EVT_RADIOBOX, onMbType)

        mainSizer = wx.FlexGridSizer(2, 2, 5, 5)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(box0, 0, wx.EXPAND)
        mainSizer.Add(optionSizer, 0, wx.EXPAND)
        mainSizer.Add(buttonsCtrl, 0, wx.EXPAND)
        mainSizer.Add(iconCtrl, 0, wx.EXPAND)
        panel.sizer.Add(mbTypeCtrl, 0, wx.EXPAND)
        panel.sizer.Add(mainSizer, 1, wx.EXPAND | wx.TOP, 5)
        panel.sizer.Add(waitCtrl, 0, wx.TOP, 5)
        panel.sizer.Add(autoCloseSizer, 0, wx.TOP, 5)
        while panel.Affirmed():
            mbt = mbTypeCtrl.GetSelection()
            panel.SetResult(
                titleCtrl.GetValue(),
                bodyCtrl.GetValue(),
                aliasCtrl.GetValue(),
                payloadCtrl.GetValue(),
                waitCtrl.GetValue(),
                getOptions(mbt),
                mbt,
                autoCloseCtrl.GetValue(),
            )

    def getFlags(self, options, twk = True):
        if twk:
            optionid = (options - options % 4096) / 4096
        else:
            optionid = 0
            if options & MB_TOPMOST:
                optionid = 1
            elif options & MB_NOFOCUS:
                optionid = 2
            elif options & MB_SYSTEMMODAL:
                optionid = 3
        iconid = 0
        if options & MB_ICONINFORMATION:
            iconid = 1
        elif options & MB_ICONWARNING == MB_ICONWARNING:
            iconid = 3
        elif options & MB_ICONQUESTION:
            iconid = 2
        elif options & MB_ICONERROR:
            iconid = 4
        buttonid = 0
        if options & MB_RETRYCANCEL == MB_RETRYCANCEL:
            buttonid = 2
        elif options & MB_YESNOCANCEL == MB_YESNOCANCEL:
            buttonid = 5
        elif options & MB_YESNO:
            buttonid = 4
        elif options & MB_ABORTRETRYIGNORE:
            buttonid = 3
        elif options & MB_OKCANCEL:
            buttonid = 1
        return (optionid, iconid, buttonid)

    def showMessageBox(self, title, body, alias, payload, options):
        if not alias:
            alias = title
        result = MessageBox(0, body, title, options)

        if result > 0 and result < 8:
            result = self.RESULTS[result]
        else:
            result = str(result)
        if payload:
            eg.TriggerEvent("%s.%s" % (alias, result), payload, "MessageBox")
        else:
            eg.TriggerEvent("%s.%s" % (alias, result), prefix = "MessageBox")
        return result

    def showTweakedBox(self, parent, title, message, alias, payload, flags, time, event):
        optionid, iconid, buttonid = self.getFlags(flags)
        mssgbx = MessageBoxDialog(parent, title, message, alias, payload, flags, time, self, event)
        if optionid & 1:
            mssgbx.ShowModal()
        else:
            mssgbx.Show()


class MessageBoxDialog(wx.Dialog):
    ARTS = (
        None,
        wx.ART_INFORMATION,
        wx.ART_QUESTION,
        wx.ART_WARNING,
        wx.ART_ERROR
    )
    SOUNDS = (
        'SystemExclamation',
        'SystemAsterisk',
        'SystemQuestion',
        'SystemExclamation',
        'SystemHand'
    )
    BUTTONS = (
        (wx.ID_OK,),
        (wx.ID_OK, wx.ID_CANCEL),
        (wx.ID_RETRY, wx.ID_CANCEL),
        (wx.ID_ABORT, wx.ID_RETRY, wx.ID_IGNORE),
        (wx.ID_YES, wx.ID_NO),
        (wx.ID_YES, wx.ID_NO, wx.ID_CANCEL),
    )
    LABELS = {
        wx.ID_OK: "ok",
        wx.ID_CANCEL: "cancel",
        wx.ID_RETRY: "retry",
        wx.ID_ABORT: "abort",
        wx.ID_IGNORE: "ignore",
        wx.ID_YES: "yes",
        wx.ID_NO: "no",
    }

    def __init__(
        self,
        parent,
        title = "",
        message = "",
        alias = "",
        payload = None,
        flags = 0,
        time = 0,
        action = None,
        event = None
    ):
        self.alias = alias
        self.payload = payload
        self.action = action
        self.event = event
        self.title = title if title else eg.APP_NAME
        optionFlags, iconFlag, buttonFlags = action.getFlags(flags)
        dialogStyle = wx.DEFAULT_DIALOG_STYLE & (~wx.CLOSE_BOX)
        if optionFlags & 2:
            dialogStyle |= wx.STAY_ON_TOP
        wx.Dialog.__init__(self, parent, -1, "", wx.DefaultPosition, style=dialogStyle)
        self.SetTitle(title)
        icon = wx.EmptyIcon()
        icon.LoadFile(join(eg.imagesDir, "icon32x32.png"), wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        art = self.ARTS[iconFlag]
        if art is not None:
            bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MESSAGE_BOX, (32, 32))
            icon = wx.StaticBitmap(self, -1, bmp)
        else:
            icon = (32, 32)
        if optionFlags & 4:
            PlaySound(self.SOUNDS[iconFlag], SND_ASYNC)
        message = wx.StaticText(self, -1, message)
        font = message.GetFont()
        font.SetPointSize(10)
        message.SetFont(font)
        message.Wrap(416)
        line = wx.StaticLine(self, -1, size=(1, -1), style = wx.LI_HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add((10, 1))

        if time:
            self.cnt = time
            txt = action.text.autoClose % self.cnt
            info = wx.StaticText(self, -1, txt)
            info.Enable(False)
            bottomSizer.Add(info, 0, wx.TOP, 3)

            def UpdateInfoLabel(evt):
                self.cnt -= 1
                txt = action.text.autoClose % self.cnt
                info.SetLabel(txt)
                if not self.cnt:
                    self.SetReturnCode(wx.ID_CANCEL)
                    self.Close()

            self.Bind(wx.EVT_TIMER, UpdateInfoLabel)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
        else:
            self.timer = None

        bottomSizer.Add((5, 1), 1, wx.EXPAND)
        buttons = self.BUTTONS[buttonFlags]
        for bttn in buttons:
            b = wx.Button(self, bttn, action.text.__dict__[self.LABELS[bttn]])
            b.SetFont(font)
            bottomSizer.Add(b, 0, wx.LEFT, 5)
        bottomSizer.Add((10, 1))
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add((1, 1), 0, wx.LEFT | wx.RIGHT, 5)
        topSizer.Add(icon, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        topSizer.Add(message, 0, wx.TOP | wx.BOTTOM, 10)
        topSizer.Add((1, 1), 0, wx.EXPAND | wx.RIGHT, 35)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        mainSizer.Add(line, 0, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND | wx.BOTTOM, 5)
        self.SetSizer(mainSizer)
        self.Fit()
        self.Bind(wx.EVT_CLOSE, self.onClose)

        def OnButton(evt):
            self.SetReturnCode(evt.GetId())
            self.Close()
            evt.Skip()
        wx.EVT_BUTTON(self, -1, OnButton)

    def onClose(self, evt):
        retCode = self.GetReturnCode()
        if retCode not in self.LABELS:
            return
        if self.timer:
            self.timer.Stop()
            del self.timer
        ix = 1 + self.action.RES_IDS.index(retCode) if retCode in self.action.RES_IDS else 1
        result = self.action.RESULTS[ix]
        self.alias = self.alias if self.alias else self.title
        if self.payload:
            eg.TriggerEvent("%s.%s" % (self.alias, result), self.payload, "MessageBox")
        else:
            eg.TriggerEvent("%s.%s" % (self.alias, result), prefix = "MessageBox")
        if self.event is not None:
            self.action.retCode = result
            SetEvent(self.event)
        self.Destroy()
