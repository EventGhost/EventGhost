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

import webbrowser
import wx
from threading import Thread
from wx.html import HtmlWindow as wxHtmlWindow
from wx.html import (
    EVT_HTML_LINK_CLICKED, HTML_OPEN, HTML_URL_IMAGE, HW_DEFAULT_STYLE
)

# Local imports
from eg.Utils import DecodeMarkdown, DecodeReST

class HtmlWindow(wxHtmlWindow):
    basePath = None

    def __init__(
        self,
        parent,
        id=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=HW_DEFAULT_STYLE,
        name="htmlWindow"
    ):
        wxHtmlWindow.__init__(self, parent, id, pos, size, style, name)
        self.SetForegroundColour(parent.GetForegroundColour())
        self.SetBackgroundColour(parent.GetBackgroundColour())

        #if wx.html.HW_NO_SELECTION & style:
        #    self.Bind(wx.EVT_MOTION, self.OnIdle)
        #    self.handCursor = wx.StockCursor(wx.CURSOR_HAND)
        #    self.x1, self.y1 = self.GetScrollPixelsPerUnit()
        #    self.isSet = False
        self.Bind(EVT_HTML_LINK_CLICKED, self.OnHtmlLinkClicked)

    def OnHtmlLinkClicked(self, event):
        Thread(
            target=webbrowser.open,
            args=(event.GetLinkInfo().GetHref(), 0)
        ).start()

#    def OnIdle(self, event):
#        x2, y2 = self.GetViewStart()
#        x3, y3 = event.GetPosition()
#        x = self.x1 * x2 + x3
#        y = self.y1 * y2 + y3
#        cell = self.GetInternalRepresentation().FindCellByPos(x, y)
#        if cell:
#            if cell.GetLink(x, y):
#                if not self.isSet:
#                    self.SetCursor(self.handCursor)
#                    self.isSet = True
#            elif self.isSet:
#                self.SetCursor(wx.STANDARD_CURSOR)
#                self.isSet = False
#        elif self.isSet:
#            self.SetCursor(wx.STANDARD_CURSOR)
#            self.isSet = False

    def OnOpeningURL(self, htmlUrlType, url):
        if (
            htmlUrlType == HTML_URL_IMAGE and
            (self.basePath is not None) and
            not url.startswith(self.basePath)
        ):
            return self.basePath + "/" + url
        else:
            return HTML_OPEN

    def SetBasePath(self, basePath):
        self.basePath = basePath

    def SetPage(self, html):
        if html.startswith("<md>"):
            html = DecodeMarkdown(html[4:])
        elif html.startswith("<rst>"):
            html = DecodeReST(html[5:])
        wxHtmlWindow.SetPage(
            self,
            '<html><body bgcolor="%s" text="%s">%s</body></html>' % (
                self.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
                self.GetForegroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
                html
            )
        )
