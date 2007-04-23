# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import os
import sys

import wx
import wx.combo
import eg

from LanguageTools import languageNames

class Text:
    Title = "Options"
    Tab1 = "General"
    StartGroup = "On Start"
    HideOnStartup = "Hide on startup"
    HideOnClose = "Hide main window if close box is pressed"
    UseAutoloadFile = "Autoload file"
    LanguageGroup = "Language"
    Warning = \
        "Language changes only take effect after restarting the application."
    StartWithWindows = "Launch on Windows startup"
    CheckUpdate = "Check for newer version at startup"
    limitMemory1 = "Limit memory consumption while minimized to"
    limitMemory2 = "MB"
    confirmDelete = "Confirm delete of tree items"
    
Text = eg.GetTranslation(Text)


class OptionsDialog(eg.Dialog):
    
    def __init__(self, parent):
        wx.Dialog.__init__(
            self, 
            parent, 
            -1,
            Text.Title, 
            style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP 
        )
        
        self.languageList = ["en_EN"]
        for item in os.listdir("Languages"):
            name, ext = os.path.splitext(item)
            if ext == ".py" and name in languageNames:
                self.languageList.append(name)
        self.languageList.sort()
        self.languageNameList = [
            languageNames[x].decode("UTF-8") for x in self.languageList
        ]
        notebook = wx.Notebook(self, -1)
        page1 = wx.Panel(notebook, -1)
        notebook.AddPage(page1, Text.Tab1)

        # page 1 controls        
        cbStartWithWindows = wx.CheckBox(page1, -1, Text.StartWithWindows)
        cbStartWithWindows.SetValue(eg.config.startWithWindows)
        self.cbStartWithWindows = cbStartWithWindows        

        cbHideOnClose = wx.CheckBox(page1, -1, Text.HideOnClose)
        cbHideOnClose.SetValue(eg.config.mainFrame.hideOnClose)
        self.cbHideOnClose = cbHideOnClose
        
        cbCheckUpdate = wx.CheckBox(page1, -1, Text.CheckUpdate)
        cbCheckUpdate.SetValue(eg.config.checkUpdate)
        self.cbCheckUpdate = cbCheckUpdate
        
        memoryLimitCheckBox = wx.CheckBox(page1, -1, Text.limitMemory1)
        memoryLimitCheckBox.SetValue(eg.config.limitMemory)
        self.memoryLimitCheckBox = memoryLimitCheckBox
        
        memoryLimitSpinCtrl = eg.SpinIntCtrl(
            page1, 
            value=eg.config.limitMemorySize,
            min=4,
            max=100
        )
        self.memoryLimitSpinCtrl = memoryLimitSpinCtrl
        def OnMemoryLimitCheckBox(event):
            memoryLimitSpinCtrl.Enable(memoryLimitCheckBox.IsChecked())
        memoryLimitCheckBox.Bind(wx.EVT_CHECKBOX, OnMemoryLimitCheckBox)
        OnMemoryLimitCheckBox(None)
        
        confirmDeleteCheckBox = wx.CheckBox(page1, -1, Text.confirmDelete)
        confirmDeleteCheckBox.SetValue(eg.config.confirmDelete)
        self.confirmDeleteCheckBox = confirmDeleteCheckBox

        languageChoice = wx.combo.BitmapComboBox(
            page1,
            -1, 
            style=wx.CB_READONLY
        )
        for name, code in zip(self.languageNameList, self.languageList):
            filename = "images/flags/%s.png" % code
            if os.path.exists(filename):
                image = wx.Image(filename)
                image.Resize((16, 16), (0, 3))
                bmp = image.ConvertToBitmap()
                languageChoice.Append(name, bmp)
            else:
                languageChoice.Append(name)
        languageChoice.SetSelection(self.languageList.index(eg.config.language))
        languageChoice.SetMinSize((150, -1))
        self.languageChoice = languageChoice

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))
        
        # construction of the layout with sizers
        
        memoryLimitSizer = wx.BoxSizer(wx.HORIZONTAL)
        memoryLimitSizer.Add(memoryLimitCheckBox, 0, wx.ALIGN_CENTER_VERTICAL)
        memoryLimitSizer.Add(memoryLimitSpinCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        memoryLimitSizer.Add(
            wx.StaticText(page1, -1, Text.limitMemory2), 
            0, 
            wx.ALIGN_CENTER_VERTICAL|wx.LEFT,
            2
        )
        
        startGroupSizer = wx.GridSizer(4, 1, 2, 2)
        startGroupSizer.AddMany(
            (
                (cbStartWithWindows, 0, wx.ALIGN_CENTER_VERTICAL),
                (cbHideOnClose, 0, wx.ALIGN_CENTER_VERTICAL),
                (cbCheckUpdate, 0, wx.ALIGN_CENTER_VERTICAL),
                (memoryLimitSizer, 0, wx.ALIGN_CENTER_VERTICAL),
                (confirmDeleteCheckBox, 0, wx.ALIGN_CENTER_VERTICAL),
            )
        )
        
        static_box = wx.StaticBox(page1, -1, Text.LanguageGroup)
        langGroupSizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        langGroupSizer.Add(languageChoice, 0, wx.LEFT|wx.RIGHT, 18)
        
        page1Sizer = wx.BoxSizer(wx.VERTICAL)
        page1Sizer.Add((15, 7), 1)
        page1Sizer.Add(startGroupSizer, 0, wx.EXPAND|wx.ALL, 5)
        page1Sizer.Add((15, 7), 1)
        page1Sizer.Add(langGroupSizer, 0, wx.EXPAND|wx.ALL, 5)
        page1.SetSizer(page1Sizer)
        page1.SetAutoLayout(True)
        
        notebookSizer = wx.BoxSizer(wx.VERTICAL)
        notebookSizer.Add(notebook, 1, wx.EXPAND)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebookSizer, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        sizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(sizer)
        self.SetMinSize(self.GetSize())
        notebook.ChangeSelection(0)
        

    def OnUseAutoloadFileCB(self, event):
        self.fbAutoloadFilePath.Enable(self.cbUseAutoloadFile.GetValue())


    def OnOK(self, event):
        tmp = self.cbStartWithWindows.GetValue()
        if tmp <> eg.config.startWithWindows:
            eg.config.startWithWindows = tmp
            path = os.path.join(eg.STARTUP, eg.APP_NAME)
            path += ".lnk"
            if tmp:
                # create shortcut in autostart dir
                eg.CreateShortcut(
                    path=path,
                    target=os.path.abspath(sys.executable),
                    arguments="-hide"
                )
            else:
                # remove shortcut from autostart dir
                try:
                    os.remove(path)
                except:
                    pass
                
        eg.config.mainFrame.hideOnClose = self.cbHideOnClose.GetValue()
        eg.config.checkUpdate = self.cbCheckUpdate.GetValue()
        eg.config.limitMemory = bool(self.memoryLimitCheckBox.GetValue())
        eg.config.limitMemorySize = self.memoryLimitSpinCtrl.GetValue()
        eg.config.limitMemorySize = self.memoryLimitSpinCtrl.GetValue()
        eg.config.confirmDelete = self.confirmDeleteCheckBox.GetValue()
        
        language = self.languageList[self.languageChoice.GetSelection()]
        if eg.config.language != language:
            dlg = wx.MessageDialog(
                self,
                Text.Warning, 
                "", 
                wx.OK|wx.ICON_INFORMATION
            )
            dlg.ShowModal()
            dlg.Destroy()
        eg.config.language = language
        eg.SaveConfig()
        event.Skip()


