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
import wx.html
import re
from eg.Utils import GetFirstParagraph

REPLACE_BR_TAG = re.compile('<br[ \/]*>')
REMOVE_HTML_PATTERN = re.compile('<([^!>]([^>]|\n)*)>')


class HeaderBox(wx.PyWindow):
    """
    The top description box of every tree item configuration dialog.
    """

    def __init__(self, parent, item):
        name = item.GetTypeName()
        description = item.GetDescription().strip()
        text = GetFirstParagraph(description)

        text = REPLACE_BR_TAG.sub('\n', text)
        text = REMOVE_HTML_PATTERN.sub('', text).strip()
        hasAdditionalHelp = (description != text)
        if text == name:
            text = ""
        self.parent = parent
        wx.PyWindow.__init__(self, parent, -1)
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        )

        nameBox = wx.StaticText(self, -1, name)
        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD )
        nameBox.SetFont(font)

        if hasAdditionalHelp:
            text += ' <a href="ShowMoreHelp">%s</a>' % eg.text.General.moreTag
        self.text = '<html><body bgcolor="%s" text="%s">%s</body></html>' % (
            self.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
            self.GetForegroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
            text
        )
        descBox = eg.HtmlWindow(self, style=wx.html.HW_NO_SELECTION)
        descBox.SetBorders(1)
        descBox.SetFonts("Arial", "Times New Roman", [8, 8, 8, 8, 8, 8, 8])
        descBox.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkClicked)
        self.descBox = descBox

        staticBitmap = wx.StaticBitmap(self)
        staticBitmap.SetIcon(item.icon.GetWxIcon())

        mainSizer = eg.HBoxSizer(
            ((4, 4)),
            (staticBitmap, 0, wx.TOP, 5),
            ((4, 4)),
            (eg.VBoxSizer(
                ((4, 4)),
                (eg.HBoxSizer(
                    (nameBox, 1, wx.EXPAND|wx.ALIGN_BOTTOM),
                ), 0, wx.EXPAND|wx.TOP, 2),
                (descBox, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 8),
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


    def OnSize(self, dummyEvent=None):
        if self.GetAutoLayout():
            self.Layout()
            self.descBox.SetPage(self.text)
            height = self.descBox.GetInternalRepresentation().GetHeight()
            self.descBox.SetMinSize((-1, height + 4))
            self.Layout()


    def OnLinkClicked(self, event):
        if event.GetLinkInfo().GetHref() == "ShowMoreHelp":
            #self.parent.configureItem.ShowHelp(self.GetParent())
            self.parent.configureItem.ShowHelp(eg.document.frame)
        else:
            event.Skip()


    def AcceptsFocus(self):
        return False

