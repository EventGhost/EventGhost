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

import re
import wx.html as html

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
        
        if hasAdditionalHelp:
            self.text += ' <a href="ShowMoreHelp">' + eg.text.General.moreTag + '</a>'
        r, g, b = self.GetBackgroundColour().Get()
        r2, g2, b2 = self.GetForegroundColour().Get()
        self.text = (
            '<html><body bgcolor="#%02X%02X%02X" text="#%02X%02X%02X">%s</body></html>' 
                % (r, g, b, r2, g2, b2, self.text)
        )
        self.descBox = descBox = wx.html.HtmlWindow(self)
        descBox.SetBorders(1)
        descBox.SetFonts("Arial", "Times New Roman", [8, 8, 8, 8, 8, 8, 8])
        descBox.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkClicked)
        
        staticBitmap = wx.StaticBitmap(self)
        staticBitmap.SetIcon(obj.info.icon.GetWxIcon())
        
        topRightSizer = wx.BoxSizer(wx.HORIZONTAL)
        topRightSizer.Add(nameBox, 1, wx.EXPAND|wx.ALIGN_BOTTOM)
        
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add((4, 4))
        rightSizer.Add(topRightSizer, 0, wx.EXPAND|wx.TOP, 2)
        rightSizer.Add(descBox, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 8)
        #rightSizer.Add((8, 8))
        
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
            self.descBox.SetPage(self.text)
            h = self.descBox.GetInternalRepresentation().GetHeight()
            self.descBox.SetMinSize((-1, h + 4))
            self.Layout()


    def OnLinkClicked(self, event):
        if event.GetLinkInfo().GetHref() == "ShowMoreHelp":
            self.parent.configureItem.ShowHelp(self.GetParent())
        else:
            event.Skip()
        
        
    def AcceptsFocus(self):
        return False
    