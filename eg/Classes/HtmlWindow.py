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
from wx.html import (
    EVT_HTML_LINK_CLICKED,
    HTML_OPEN,
    HTML_REDIRECT,
    HTML_URL_IMAGE,
    HtmlWindow as wxHtmlWindow,
    HW_DEFAULT_STYLE,
)

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

        self.Bind(EVT_HTML_LINK_CLICKED, self.OnHtmlLinkClicked)

    def OnHtmlLinkClicked(self, event):
        Thread(
            target=webbrowser.open,
            args=(event.GetLinkInfo().GetHref(), 0)
        ).start()

    def OnOpeningURL(self, htmlUrlType, url, redirect=None):
        if (
            htmlUrlType == HTML_URL_IMAGE and
            (self.basePath is not None) and
            not url.startswith(self.basePath)
        ):
            return HTML_REDIRECT, self.basePath + '/' + url
        else:
            return HTML_OPEN, ''

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
