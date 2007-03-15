# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
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
import string
from types import StringTypes

class Text:
    title = "Find"
    searchLabel = "Fi&nd what:"
    wholeWordsOnly = "Match &whole word only"
    caseSensitive = "&Match case"
    searchParameters = "Search action parameters also"
    direction = "Direction"
    findButton = "&Find Next"
    up = "&Up"
    down = "&Down"
    notFoundMesg = '"%s" couldn\'t be found.'

Text = eg.GetTranslation(Text)


class FindDialog(eg.Dialog):
    
    def __init__(self, parent, document):
        eg.Dialog.__init__(
            self, 
            parent, 
            -1,
            title = Text.title,
            style = wx.DEFAULT_DIALOG_STYLE
        )
        self.document = document
        self.choices = [""]
        textCtrl = wx.TextCtrl(self)
        wholeWordsOnlyCb = wx.CheckBox(self, -1, Text.wholeWordsOnly)
        caseSensitiveCb = wx.CheckBox(self, -1, Text.caseSensitive)
        searchParametersCb = wx.CheckBox(self, -1, Text.searchParameters)
        searchParametersCb.SetValue(1)
        directionRb = wx.RadioBox(
            self, 
            label = Text.direction, 
            choices = [Text.up, Text.down], 
            style = wx.RA_SPECIFY_ROWS
        )
        directionRb.SetSelection(1)
        searchButton = wx.Button(self, -1, Text.findButton)
        searchButton.SetDefault()
        searchButton.Enable(False)
        cancelButton = wx.Button(self, wx.ID_CANCEL, eg.text.General.cancel)
        
        upperLeftSizer = wx.BoxSizer(wx.HORIZONTAL)
        upperLeftSizer.Add(
            wx.StaticText(self, -1, Text.searchLabel), 
            0, 
            wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 
            5
        )
        upperLeftSizer.Add(textCtrl, 1, wx.EXPAND)
        
        cbSizer = wx.BoxSizer(wx.VERTICAL)
        cbSizer.Add(wholeWordsOnlyCb)
        cbSizer.Add(caseSensitiveCb, 0, wx.TOP, 5)
        cbSizer.Add(searchParametersCb, 0, wx.TOP, 5)
        
        lowerLeftSizer = wx.BoxSizer(wx.HORIZONTAL)
        lowerLeftSizer.Add(cbSizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        lowerLeftSizer.Add(directionRb)
        
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(upperLeftSizer, 0, wx.EXPAND|wx.ALL, 5)
        leftSizer.Add(lowerLeftSizer, 0, wx.EXPAND|wx.ALL, 5)

        btnSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer.Add(searchButton, 0, wx.EXPAND)
        btnSizer.Add(cancelButton, 0, wx.EXPAND|wx.TOP, 5)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(leftSizer, 1, wx.EXPAND)
        sizer.Add(btnSizer, 0, wx.EXPAND|wx.ALL, 5)
        
        self.SetSizerAndFit(sizer)
        self.SetMinSize(self.GetSize())
        
        searchButton.Bind(wx.EVT_BUTTON, self.OnFindButton)
        def EnableSearchButton(event):
            enable = textCtrl.GetValue() != ""
            searchButton.Enable(enable)
        textCtrl.Bind(wx.EVT_TEXT, EnableSearchButton)
        
        self.textCtrl = textCtrl
        self.wholeWordsOnlyCb = wholeWordsOnlyCb
        self.caseSensitiveCb = caseSensitiveCb
        self.searchParametersCb = searchParametersCb
        self.directionRb = directionRb
        self.searchButton = searchButton


    def Show(self):
        eg.Dialog.Show(self)
        self.Raise()
        self.textCtrl.SetSelection(-1, -1)
        self.textCtrl.SetFocus()


    def OnFindButton(self, event=None):
        tree = self.document.tree
        item = tree.GetPyData(tree.GetSelection())
        startItem = item
        originalSearchValue = self.textCtrl.GetValue()
        if self.caseSensitiveCb.GetValue():
            convertFunc = lambda s: s
            key = originalSearchValue
        else:
            convertFunc = string.lower
            key = originalSearchValue.lower()
        
        if self.directionRb.GetSelection():
            iterFunc = eg.TreeItem.GetNextItem
        else:
            iterFunc = eg.TreeItem.GetPreviousItem
        ActionItem = eg.ActionItem
        PythonScript = eg.plugins.EventGhost.PythonScript
        keyLen = len(key)
        if self.wholeWordsOnlyCb.GetValue():
            matchFunc = lambda text, pos: (
                (
                    pos == 0 
                    or not text[pos - 1].isalnum()
                )
                and (
                    keyLen + pos == len(text) 
                    or not text[pos + keyLen].isalnum()
                )
            )
        else:
            matchFunc = lambda text, res: True
        searchParameters = self.searchParametersCb.GetValue()
        while True:
            item = iterFunc(item)
            if startItem is item:
                dlg = wx.MessageDialog(
                    eg.mainFrame, 
                    Text.notFoundMesg % originalSearchValue,
                    eg.APP_NAME,
                    wx.OK | wx.ICON_INFORMATION
                )
                dlg.ShowModal()
                dlg.Destroy()
                if self.IsShown():
                    self.Show()
                return
            text = convertFunc(item.GetLabel())
            pos = text.find(key)
            if pos != -1 and matchFunc(text, pos):
                item.Select()
                return
            if searchParameters and isinstance(item, ActionItem):
                for arg in item.args:
                    if type(arg) in StringTypes:
                        text = convertFunc(arg)
                        pos = text.find(key)
                        if pos != -1 and matchFunc(text, pos):
                            item.Select()
                            return
