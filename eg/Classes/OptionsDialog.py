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

import os
import wx
from os.path import exists, join
from time import localtime, strftime
from wx.combo import BitmapComboBox

# Local imports
import eg
from eg.WinApi import Locale


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
    Datestamp = "Datestamp format for log:"
    DatestampHelp = (
        "For imformation on format codes read Python's strftime "
        "documentation:\n"
        "http://docs.python.org/2/library/datetime.html#strftime-and-strptime-"
        "behavior\n"
        "\nHere you can find examples:\n"
        "http://strftime.org/\n"
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

        locales = sorted(
            (
                locale for locale in Locale.EnumLocales()
                if locale.iso_language == 'en' or locale.eg_has_language
            ),
            key=lambda lng: lng.language_name
        )
  
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

        datestampCtrl = page1.TextCtrl(config.datestamp)
        datestampCtrl.SetToolTipString(text.DatestampHelp)
        datestampLabel = page1.StaticText(text.Datestamp)
        datestampLabel.SetToolTipString(text.DatestampHelp)
        datestampSzr = wx.BoxSizer(wx.HORIZONTAL)
        datestampSzr.AddMany((
            (datestampLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5),
            (datestampCtrl, 1, wx.EXPAND)
        ))

        def OnDatestampKillFocus(_):
            dt_fmt = datestampCtrl.GetValue()
            try:
                strftime(dt_fmt, localtime())
            except ValueError:
                wx.MessageBox("Invalid format string!", "Error")
                datestampCtrl.SetBackgroundColour("pink")
                datestampCtrl.Refresh()
                wx.CallAfter(datestampCtrl.SetFocus)
            else:
                datestampCtrl.SetBackgroundColour(
                    wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
                )
                datestampCtrl.Refresh()

        datestampCtrl.Bind(wx.EVT_KILL_FOCUS, OnDatestampKillFocus)

        languageChoice = BitmapComboBox(page1, style=wx.CB_READONLY)

        for locale in locales:
            languageChoice.Append(locale.label, locale.flag)

        for locale in locales:
            if locale.iso_code == config.language:
                languageChoice.SetSelection(locale.label)
        else:
            languageChoice.SetStringSelection('English - United States')
            config.language = 'en_US'

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
                (datestampSzr, 0, flags),
            )
        )

        langGroupSizer = page1.VStaticBoxSizer(
            text.LanguageGroup,
            (languageChoice, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, INDENT_WIDTH),
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
            config.datestamp = datestampCtrl.GetValue()

            lang = languageChoice.GetStringSelection()
            for locale in locales:
                if locale.label == lang:
                    config.language = locale.iso_code
                    break

            config.Save()
            self.SetResult()

        eg.Utils.UpdateStartupShortcut(startWithWindowsCtrl.GetValue())

        if config.showTrayIcon:
            eg.taskBarIcon.Show()
        else:
            eg.taskBarIcon.Hide()

        if eg.mainFrame:
            eg.mainFrame.SetWindowStyleFlag()
            eg.mainFrame.logCtrl.SetDTLogging()

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
