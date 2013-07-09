# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx
import os
import sys

from wx.combo import BitmapComboBox


class Text(eg.TranslatableStrings):
    Title = "Options"
    Tab1 = "General"
    StartGroup = "On Start"
    HideOnStartup = "Hide on startup"
    HideOnClose = "Minimize to system tray on close"
    UseAutoloadFile = "Autoload file"
    LanguageGroup = "Language"
    confirmRestart = (
        "Language changes only take effect after restarting the application."
        "\n\n"
        "Do you want to restart EventGhost now?"
    )
    StartWithWindows = "Autostart EventGhost on system startup"
    CheckUpdate = "Check for newer version on startup"
    limitMemory1 = "Limit memory consumption while minimized to"
    limitMemory2 = "MB"
    confirmDelete = "Confirm delete of tree items"



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
            config.startWithWindows,
            text.StartWithWindows
        )
        if eg.folderPath.Startup is None:
            startWithWindowsCtrl.Enable(False)

        hideOnCloseCtrl = page1.CheckBox(
            config.hideOnClose,
            text.HideOnClose
        )
        #checkUpdateCtrl = page1.CheckBox(config.checkUpdate, text.CheckUpdate)
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

        confirmDeleteCtrl = page1.CheckBox(
            config.confirmDelete,
            text.confirmDelete
        )

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
            (page1.StaticText(text.limitMemory2), 0, flags|wx.LEFT, 2),
        )

        startGroupSizer = wx.GridSizer(4, 1, 2, 2)
        startGroupSizer.AddMany(
            (
                (startWithWindowsCtrl, 0, flags),
                (hideOnCloseCtrl, 0, flags),
                #(checkUpdateCtrl, 0, flags),
                (memoryLimitSizer, 0, flags),
                (confirmDeleteCtrl, 0, flags),
            )
        )

        langGroupSizer = page1.VStaticBoxSizer(
            text.LanguageGroup,
            (languageChoice, 0, wx.LEFT|wx.RIGHT, 18),
        )

        page1Sizer = eg.VBoxSizer(
            ((15, 7), 1),
            (startGroupSizer, 0, wx.EXPAND|wx.ALL, 5),
            ((15, 7), 1),
            (langGroupSizer, 0, wx.EXPAND|wx.ALL, 5),
        )
        page1.SetSizer(page1Sizer)
        page1.SetAutoLayout(True)

        sizer = eg.VBoxSizer(
            (notebook, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(sizer)
        self.SetMinSize(self.GetSize())
        notebook.ChangeSelection(0)

        oldLanguage = config.language
        while self.Affirmed():
            tmp = startWithWindowsCtrl.GetValue()
            if tmp != eg.config.startWithWindows:
                config.startWithWindows = tmp
                path = os.path.join(
                    eg.folderPath.Startup,
                    eg.APP_NAME + ".lnk"
                )
                if tmp:
                    # create shortcut in autostart dir
                    eg.Shortcut.Create(
                        path=path,
                        target=os.path.abspath(sys.executable),
                        arguments="-h -e OnInitAfterBoot"
                    )
                else:
                    # remove shortcut from autostart dir
                    try:
                        os.remove(path)
                    except:
                        pass

            config.hideOnClose = hideOnCloseCtrl.GetValue()
            #config.checkUpdate = checkUpdateCtrl.GetValue()
            config.limitMemory = bool(memoryLimitCtrl.GetValue())
            config.limitMemorySize = memoryLimitSpinCtrl.GetValue()
            config.confirmDelete = confirmDeleteCtrl.GetValue()

            config.language = languageList[languageChoice.GetSelection()]
            config.Save()
            self.SetResult()
        if config.language != oldLanguage:
            wx.CallAfter(self.ShowLanguageWarning)
        OptionsDialog.instance = None


    def ShowLanguageWarning(self):
        dlg = wx.MessageDialog(
            eg.document.frame,
            Text.confirmRestart,
            "",
            wx.YES_NO|wx.ICON_QUESTION
        )
        res = dlg.ShowModal()
        dlg.Destroy()
        if res == wx.ID_YES:
            eg.app.Restart()

