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
    HideOnClose = "Send to Systray on Close"
    UseAutoloadFile = "Autoload file"
    LanguageGroup = "Language"
    Warning = \
        "Language changes only take effect after restarting the application."
    StartWithWindows = "Launch on Windows startup"
    CheckUpdate = "Check for newer version at startup"
    limitMemory1 = "Limit memory consumption while minimized to"
    limitMemory2 = "MB"
    confirmDelete = "Confirm delete of tree items"
    


class OptionsDialog(eg.Dialog):
    
    def Process(self, parent=None):
        t = Text
        c = eg.config
        
        eg.Dialog.__init__(
            self, 
            parent, 
            -1,
            t.Title, 
            style=wx.DEFAULT_DIALOG_STYLE
        )
        
        languageNames = eg.Translation.languageNames
        languageList = ["en_EN"]
        for item in os.listdir("languages"):
            name, ext = os.path.splitext(item)
            if ext == ".py" and name in languageNames:
                languageList.append(name)
        languageList.sort()
        languageNameList = [languageNames[x] for x in languageList]
        notebook = wx.Notebook(self, -1)
        page1 = eg.Panel(notebook)
        notebook.AddPage(page1, t.Tab1)
        
        # page 1 controls        
        startWithWindowsCtrl = page1.CheckBox(
            c.startWithWindows, 
            t.StartWithWindows
        )
        if eg.folderPath.Startup is None:
            startWithWindowsCtrl.Enable(False)
            
        hideOnCloseCtrl = page1.CheckBox(c.mainFrame.hideOnClose, t.HideOnClose)
        checkUpdateCtrl = page1.CheckBox(c.checkUpdate, t.CheckUpdate)
        memoryLimitCtrl = page1.CheckBox(c.limitMemory, t.limitMemory1)
        memoryLimitSpinCtrl = page1.SpinIntCtrl(
            c.limitMemorySize,
            min=4,
            max=999
        )
        def OnMemoryLimitCheckBox(event):
            memoryLimitSpinCtrl.Enable(memoryLimitCtrl.IsChecked())
        memoryLimitCtrl.Bind(wx.EVT_CHECKBOX, OnMemoryLimitCheckBox)
        OnMemoryLimitCheckBox(None)
        
        confirmDeleteCtrl = page1.CheckBox(c.confirmDelete, t.confirmDelete)

        languageChoice = BitmapComboBox(page1, style=wx.CB_READONLY)
        for name, code in zip(languageNameList, languageList):
            filename = "images/flags/%s.png" % code
            if os.path.exists(filename):
                image = wx.Image(filename)
                image.Resize((16, 16), (0, 3))
                bmp = image.ConvertToBitmap()
                languageChoice.Append(name, bmp)
            else:
                languageChoice.Append(name)
        languageChoice.SetSelection(languageList.index(c.language))
        languageChoice.SetMinSize((150, -1))

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL, wx.ID_APPLY))
        
        # construction of the layout with sizers
        
        flags = wx.ALIGN_CENTER_VERTICAL
        memoryLimitSizer = eg.HBoxSizer(
            (memoryLimitCtrl, 0, flags),
            (memoryLimitSpinCtrl, 0, flags),
            (page1.StaticText(t.limitMemory2), 0, flags|wx.LEFT, 2),
        )
        
        startGroupSizer = wx.GridSizer(4, 1, 2, 2)
        startGroupSizer.AddMany(
            (
                (startWithWindowsCtrl, 0, flags),
                (hideOnCloseCtrl, 0, flags),
                (checkUpdateCtrl, 0, flags),
                (memoryLimitSizer, 0, flags),
                (confirmDeleteCtrl, 0, flags),
            )
        )
        
        langGroupSizer = page1.VStaticBoxSizer(
            t.LanguageGroup,
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
        
        while self.Affirmed():
            tmp = startWithWindowsCtrl.GetValue()
            if tmp != eg.config.startWithWindows:
                c.startWithWindows = tmp
                path = os.path.join(eg.folderPath.Startup, eg.APP_NAME)
                path += ".lnk"
                if tmp:
                    # create shortcut in autostart dir
                    eg.Shortcut.Create(
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
                    
            c.mainFrame.hideOnClose = hideOnCloseCtrl.GetValue()
            c.checkUpdate = checkUpdateCtrl.GetValue()
            c.limitMemory = bool(memoryLimitCtrl.GetValue())
            c.limitMemorySize = memoryLimitSpinCtrl.GetValue()
            c.confirmDelete = confirmDeleteCtrl.GetValue()
            
            language = languageList[languageChoice.GetSelection()]
            if c.language != language:
                dlg = wx.MessageDialog(
                    self,
                    t.Warning, 
                    "", 
                    wx.OK|wx.ICON_INFORMATION
                )
                dlg.ShowModal()
                dlg.Destroy()
            c.language = language
            c.Save()
            self.SetResult()


