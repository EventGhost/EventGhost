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

import wx
import eg
import re

from wx.html import HW_SCROLLBAR_NEVER, HW_NO_SELECTION 
import wx.lib.hyperlink as hl

REPLACE_BR_TAG = re.compile('<br[ \/]*>')
REMOVE_HTML_PATTERN = re.compile('<([^!>]([^>]|\n)*)>')


class HeaderBox(wx.PyWindow):
    """
    The top description box of every action/plugin configuration dialog.
    """
    
    def __init__(self, parent, obj):
        description = obj.description.strip()
        text = ""
        for line in description.splitlines():
            if line == "":
                break
            text += line
        
        hasAdditionalHelp = (description != text)
        text = REPLACE_BR_TAG.sub('\n', text)
        text = REMOVE_HTML_PATTERN.sub('', text)
        if text == obj.name:
            self.text = ""
        else:
            self.text = text
        self.obj = obj
        self.parent = parent
        wx.PyWindow.__init__(self, parent, -1)
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        )
        
        nameBox = wx.StaticText(self, -1, obj.name)
        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD )
        nameBox.SetFont(font)
        
        descBox = wx.StaticText(self, -1, style=wx.ST_NO_AUTORESIZE )
        self.descBox = descBox
        
        staticBitmap = wx.StaticBitmap(self)
        staticBitmap.SetIcon(obj.info.GetWxIcon())
        
        topRightSizer = wx.BoxSizer(wx.HORIZONTAL)
        topRightSizer.Add(nameBox, 1, wx.EXPAND|wx.ALIGN_BOTTOM)
        if hasAdditionalHelp:
            helpLink = hl.HyperLinkCtrl(
                self, 
                wx.ID_ANY, 
                eg.text.General.moreHelp, 
                URL=eg.text.General.moreHelp,
                style=wx.TAB_TRAVERSAL 
            )
            helpLink.Bind(hl.EVT_HYPERLINK_LEFT, self.OnLink)
            helpLink.AutoBrowse(False)
            topRightSizer.Add(helpLink, 0, wx.EXPAND|wx.RIGHT, 2)
            
            helpBitmap = wx.StaticBitmap(self)
            helpBitmap.SetBitmap(wx.Bitmap("images/help.png"))
            topRightSizer.Add(helpBitmap, 0, wx.RIGHT, 4)
            helpBitmap.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            helpBitmap.Bind(wx.EVT_LEFT_UP, self.OnLink)
        
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add((4, 4))
        rightSizer.Add(topRightSizer, 0, wx.EXPAND|wx.TOP, 2)
        rightSizer.Add(descBox, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 8)
        rightSizer.Add((8, 8))
        
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add((4, 4))
        mainSizer.Add(staticBitmap, 0, wx.TOP, 5)
        mainSizer.Add((4, 4))
        mainSizer.Add(rightSizer, 1, wx.EXPAND)
        
        # odd sequence to setup the window, but all other ways seem
        # to wrap the text wrong
        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        mainSizer.Fit(self)
        mainSizer.Layout()
        self.Layout()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        
    def OnSize(self, event=None):
        if self.GetAutoLayout():
            self.Layout()
            y = self.descBox.GetSize()[0]
            self.descBox.SetLabel(self.text)
            self.descBox.Wrap(y)
            self.Layout()


    def OnLink(self, event):
        self.parent.configureItem.ShowHelp()
        
        
    def AcceptsFocus(self):
        return False
    
        
        
class ConfigurationDialog(eg.Dialog):
    """
    A configuration dialog for all plug-ins and actions.
    """
    __postInited = False
    
    def __init__(self, obj, resizeable=None, showLine=True):
        self.showLine = showLine
        if resizeable is None:
            resizeable = bool(eg.debugLevel)
        self.resizeable = resizeable
        
        if isinstance(obj, eg.PluginClass):
            title = eg.text.General.pluginLabel % obj.name
            flags = wx.EXPAND|wx.ALL|wx.ALIGN_CENTER
        else:
            title = "%s: %s" % (obj.plugin.info.label, obj.name)
            flags = wx.EXPAND|wx.ALL|wx.ALIGN_CENTER

        self.configureItem = eg.currentConfigureItem
        eg.currentConfigureItem.openConfigDialog = self
        
        dialogStyle = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU
        if resizeable:
            dialogStyle |= wx.RESIZE_BORDER
        eg.Dialog.__init__(self, eg.document.frame, -1, title, style=dialogStyle)
        
#        icon = obj.info.GetWxIcon()
#        self.icon = icon
#        if icon:
#            self.SetIcon(icon)
        
        self.buttonRow = eg.ButtonRow(
            self, 
            (wx.ID_OK, wx.ID_CANCEL)
        )
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        paramSizer = wx.BoxSizer(wx.VERTICAL)
        self.headerBox = HeaderBox(self, obj)
        mainSizer.SetMinSize((450, 300))
        mainSizer.Add(self.headerBox, 0, wx.EXPAND, 0)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALIGN_CENTER, 0)
        mainSizer.Add(paramSizer, 1, flags|wx.ALIGN_CENTER_VERTICAL, 15)
        self.mainSizer = mainSizer
        self.sizer = paramSizer
        
        def ShowHelp(event):
            self.configureItem.ShowHelp()
        wx.EVT_MENU(self, wx.ID_HELP, ShowHelp)
        
        self.SetAcceleratorTable(
            wx.AcceleratorTable(
                [
                    (wx.ACCEL_NORMAL, wx.WXK_F1, wx.ID_HELP),
                ]
            )
        )        
        


    def FinishSetup(self):
        if not self.__postInited:
            self.__postInited = True
            line = wx.StaticLine(self)
            self.sizer.Add((0,0))
            self.mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER)
            self.buttonRow.cancelButton.MoveAfterInTabOrder(line)
            self.buttonRow.okButton.MoveAfterInTabOrder(line)
            
            if not self.showLine:
                line.Hide()
            if self.resizeable:
                flag = wx.EXPAND
                border = 0
            else:
                flag = wx.EXPAND|wx.RIGHT
                border = 10
            self.mainSizer.Add(self.buttonRow.sizer, 0, flag, border)
            self.SetSizerAndFit(self.mainSizer)
            self.SetMinSize(self.GetSize())
            self.Layout()
        self.Centre()
        
    
    def SetCallback(self, callback, *args, **kwargs):
        def OkCallWarpper(event):
            callback(wx.ID_OK, *args, **kwargs)
        self.buttonRow.okButton.Bind(wx.EVT_BUTTON, OkCallWarpper)
        def CancelCallWarpper(event):
            callback(wx.ID_CANCEL, *args, **kwargs)
        self.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, CancelCallWarpper)
    
    
    def AffirmedShowModal(self):
        FinishSetup()
        if self.ShowModal() == wx.ID_OK:
            return True
        return False


    def AffirmedShowModal(self):
        gr1 = eg.Greenlet.getcurrent()
        self.FinishSetup()
        self.Show()
        self.Raise()
        self.SetCallback(gr1.switch)
        result = gr1.parent.switch()
        self.Hide()
        self.Destroy()
        return result == wx.ID_OK

#    def OnHelp(self, event):
#        self.configureItem.ShowHelp()
#

    def AddLabel(self, label):
        labelCtrl = wx.StaticText(self, -1, label)
        self.sizer.Add(labelCtrl, 0, wx.BOTTOM, 2)
        
        
    def AddCtrl(self, ctrl):
        self.sizer.Add(ctrl, 0, wx.BOTTOM, 10)
        
        
    def AddCtrlExpanded(self, ctrl):
        self.sizer.Add(ctrl, 0, wx.BOTTOM|wx.EXPAND, 10)
        
