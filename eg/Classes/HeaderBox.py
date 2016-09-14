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

import re
import wx
import wx.html

# Local imports
import eg

REPLACE_BR_TAG = re.compile('<br[ \/]*>')
REMOVE_HTML_PATTERN = re.compile('<([^!>]([^>]|\n)*)>')

class HeaderBox(wx.PyWindow):
    """
    The top description box of every tree item configuration dialog.
    """
    def __init__(self, parent, name="", text="", icon=None, url = None):
        text = REPLACE_BR_TAG.sub('\n', text)
        text = REMOVE_HTML_PATTERN.sub('', text).strip()
        if text == name:
            text = ""
        self.parent = parent
        wx.PyWindow.__init__(self, parent, -1)
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        )

        nameBox = wx.StaticText(self, -1, name)
        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        nameBox.SetFont(font)

        self.text = '<html><body bgcolor="%s" text="%s">%s</body></html>' % (
            self.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
            self.GetForegroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
            text
        )
        if url:
            self.text = eg.Utils.AppUrl(self.text, url)
        descBox = eg.HtmlWindow(self, style=wx.html.HW_NO_SELECTION)
        descBox.SetBorders(1)
        descBox.SetFonts("Arial", "Times New Roman", [8, 8, 8, 8, 8, 8, 8])
        descBox.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkClicked)
        self.descBox = descBox

        staticBitmap = wx.StaticBitmap(self)
        staticBitmap.SetIcon(icon.GetWxIcon())

        mainSizer = eg.HBoxSizer(
            ((4, 4)),
            (staticBitmap, 0, wx.TOP, 5),
            ((4, 4)),
            (eg.VBoxSizer(
                ((4, 4)),
                (eg.HBoxSizer(
                    (nameBox, 1, wx.EXPAND | wx.ALIGN_BOTTOM),
                ), 0, wx.EXPAND | wx.TOP, 2),
                (descBox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 8),
            ), 1, wx.EXPAND),
        )
        # odd sequence to setup the window, but all other ways seem
        # to wrap the text wrong
        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        mainSizer.Fit(self)
        mainSizer.Layout()
        self.Layout()
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def AcceptsFocus(self):
        return False

    def OnLinkClicked(self, event):
        if event.GetLinkInfo().GetHref() == "ShowMoreHelp":
            self.parent.configureItem.ShowHelp(eg.document.frame)
        else:
            event.Skip()

    def OnSize(self, dummyEvent=None):
        if self.GetAutoLayout():
            self.Layout()
            self.descBox.SetPage(self.text)
            height = self.descBox.GetInternalRepresentation().GetHeight()
            self.descBox.SetMinSize((-1, height + 4))
            self.Layout()
