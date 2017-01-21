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

import os
import wx
from os.path import exists, join
from wx.combo import BitmapComboBox

# Local imports
import eg

INDENT_WIDTH = 18

class Text(eg.TranslatableStrings):
    Title = "Options"
    Tab1 = "General"
    CheckPreRelease = "Always notify about new pre-releases"
    CheckUpdate = "Check for EventGhost updates at launch"
    confirmDelete = "Confirm deletion of tree items"
    confirmRestart = (
        "Language changes only take effect after restarting the application."
        "\n\n"
        "Do you want to restart EventGhost now?"
    )
    HideOnClose = "Keep running in background when window closed"
    HideOnStartup = "Hide on startup"
    LanguageGroup = "Language"
    limitMemory1 = "Limit memory consumption while minimized to"
    limitMemory2 = "MB"
    propResize = "Resize window proportionally"
    refreshEnv = 'Refresh environment before executing "Run" actions'
    showTrayIcon = "Display EventGhost icon in system tray"
    StartWithWindows = 'Autostart EventGhost for user "%s"' % os.environ["USERNAME"]
    UseAutoloadFile = "Autoload file"
    UseFixedFont = 'Use fixed-size font in the "Log" pane'


class OptionsDialog(eg.TaskletDialog):
    instance = None

    @eg.LogItWithReturn
    def Configure(self, parent=None):
        if OptionsDialog.instance:
            OptionsDialog.instance.Raise()
            return
        OptionsDialog.instance = self

        text = Text
        config = eg.config
        self.useFixedFont = config.useFixedFont

        eg.TaskletDialog.__init__(
            self,
            parent=parent,
            title=text.Title,
        )

        languageNames = eg.Translation.languageNames
        languageList = ["en_EN"]
        for item in os.listdir(eg.languagesDir):
            name, ext = os.path.splitext(item)
            if ext == ".py" and name in languageNames:
                languageList.append(name)
        languageList.sort()
        languageNameList = [languageNames[x] for x in languageList]
        notebook = wx.Notebook(self, -1)
        page1 = eg.Panel(notebook)
        notebook.AddPage(page1, text.Tab1)

        # page 1 controls
        startWithWindowsCtrl = page1.CheckBox(
            exists(join((eg.folderPath.Startup or ""), eg.APP_NAME + ".lnk")),
            text.StartWithWindows
        )
        if eg.folderPath.Startup is None:
            startWithWindowsCtrl.Enable(False)

        checkUpdateCtrl = page1.CheckBox(config.checkUpdate, text.CheckUpdate)
        checkPreReleaseCtrl = page1.CheckBox(config.checkPreRelease, text.CheckPreRelease)
        checkPreReleaseCtrl.Enable(config.checkUpdate)

        def OnCheckUpdateCheckBox(event):
            checkPreReleaseCtrl.Enable(event.IsChecked())
        checkUpdateCtrl.Bind(wx.EVT_CHECKBOX, OnCheckUpdateCheckBox)

        confirmDeleteCtrl = page1.CheckBox(
            config.confirmDelete,
            text.confirmDelete
        )

        showTrayIconCtrl = page1.CheckBox(
            config.showTrayIcon,
            text.showTrayIcon
        )

        hideOnCloseCtrl = page1.CheckBox(
            config.hideOnClose,
            text.HideOnClose
        )

        memoryLimitCtrl = page1.CheckBox(config.limitMemory, text.limitMemory1)
        memoryLimitSpinCtrl = page1.SpinIntCtrl(
            config.limitMemorySize,
            min=4,
            max=999
        )

        def OnMemoryLimitCheckBox(dummyEvent):
            memoryLimitSpinCtrl.Enable(memoryLimitCtrl.IsChecked())
        memoryLimitCtrl.Bind(wx.EVT_CHECKBOX, OnMemoryLimitCheckBox)
        OnMemoryLimitCheckBox(None)

        refreshEnvCtrl = page1.CheckBox(
            config.refreshEnv,
            text.refreshEnv
        )

        propResizeCtrl = page1.CheckBox(
            config.propResize,
            text.propResize
        )

        useFixedFontCtrl = page1.CheckBox(
            config.useFixedFont,
            text.UseFixedFont
        )

        def OnFixedFontBox(evt):
            self.UpdateFont(evt.IsChecked())
        useFixedFontCtrl.Bind(wx.EVT_CHECKBOX, OnFixedFontBox)

        languageChoice = BitmapComboBox(page1, style=wx.CB_READONLY)
        for name, code in zip(languageNameList, languageList):
            filename = os.path.join(eg.imagesDir, "flags", "%s.png" % code)
            if os.path.exists(filename):
                image = wx.Image(filename)
                image.Resize((16, 16), (0, 3))
                bmp = image.ConvertToBitmap()
                languageChoice.Append(name, bmp)
            else:
                languageChoice.Append(name)
        languageChoice.SetSelection(languageList.index(config.language))
        languageChoice.SetMinSize((150, -1))

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))

        # construction of the layout with sizers

        flags = wx.ALIGN_CENTER_VERTICAL
        memoryLimitSizer = eg.HBoxSizer(
            (memoryLimitCtrl, 0, flags),
            (memoryLimitSpinCtrl, 0, flags),
            (page1.StaticText(text.limitMemory2), 0, flags | wx.LEFT, 2),
        )

        startGroupSizer = wx.GridSizer(cols=1, vgap=2, hgap=2)
        startGroupSizer.AddMany(
            (
                (startWithWindowsCtrl, 0, flags),
                (checkUpdateCtrl, 0, flags),
                (checkPreReleaseCtrl, 0, flags | wx.LEFT, INDENT_WIDTH),
                (confirmDeleteCtrl, 0, flags),
                (showTrayIconCtrl, 0, flags),
                (hideOnCloseCtrl, 0, flags),
                (memoryLimitSizer, 0, flags),
                (refreshEnvCtrl, 0, flags),
                (propResizeCtrl, 0, flags),
                (useFixedFontCtrl, 0, flags),
            )
        )

        langGroupSizer = page1.VStaticBoxSizer(
            text.LanguageGroup,
            (languageChoice, 0, wx.LEFT | wx.RIGHT, INDENT_WIDTH),
        )

        page1Sizer = eg.VBoxSizer(
            ((15, 7), 1),
            (startGroupSizer, 0, wx.EXPAND | wx.ALL, 5),
            ((15, 7), 1),
            (langGroupSizer, 0, wx.EXPAND | wx.ALL, 5),
        )
        page1.SetSizer(page1Sizer)
        page1.SetAutoLayout(True)

        sizer = eg.VBoxSizer(
            (notebook, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(sizer)
        self.SetMinSize(self.GetSize())
        notebook.ChangeSelection(0)

        oldLanguage = config.language

        while self.Affirmed():
            config.checkUpdate = checkUpdateCtrl.GetValue()
            config.checkPreRelease = checkPreReleaseCtrl.GetValue()
            config.confirmDelete = confirmDeleteCtrl.GetValue()
            config.showTrayIcon = showTrayIconCtrl.GetValue()
            config.hideOnClose = hideOnCloseCtrl.GetValue()
            config.limitMemory = bool(memoryLimitCtrl.GetValue())
            config.limitMemorySize = memoryLimitSpinCtrl.GetValue()
            config.refreshEnv = refreshEnvCtrl.GetValue()
            config.propResize = propResizeCtrl.GetValue()
            config.useFixedFont = useFixedFontCtrl.GetValue()
            config.language = languageList[languageChoice.GetSelection()]
            config.Save()
            self.SetResult()

        eg.Utils.UpdateStartupShortcut(startWithWindowsCtrl.GetValue())

        if config.showTrayIcon:
            eg.taskBarIcon.Show()
        else:
            eg.taskBarIcon.Hide()

        if eg.mainFrame:
            eg.mainFrame.SetWindowStyleFlag()

        if config.language != oldLanguage:
            wx.CallAfter(self.ShowLanguageWarning)

        OptionsDialog.instance = None

    @eg.LogItWithReturn
    def OnCancel(self, event):
        self.UpdateFont(self.useFixedFont)
        self.DispatchEvent(event, wx.ID_CANCEL)

    @eg.LogItWithReturn
    def OnClose(self, event):
        self.UpdateFont(self.useFixedFont)
        self.DispatchEvent(event, wx.ID_CANCEL)

    def ShowLanguageWarning(self):
        dlg = wx.MessageDialog(
            eg.document.frame,
            Text.confirmRestart,
            "",
            wx.YES_NO | wx.ICON_QUESTION
        )
        res = dlg.ShowModal()
        dlg.Destroy()
        if res == wx.ID_YES:
            eg.app.Restart()

    def UpdateFont(self, val):
        font = eg.document.frame.treeCtrl.GetFont()
        if val:
            font = wx.Font(font.GetPointSize(), wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Courier New")
        wx.CallAfter(eg.document.frame.logCtrl.SetFont, font)
