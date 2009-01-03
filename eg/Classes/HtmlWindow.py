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
import webbrowser
from threading import Timer, Thread

from wx.html import HtmlWindow as wxHtmlWindow
from wx.html import HTML_URL_IMAGE, HTML_OPEN

wx.InitAllImageHandlers()


class HtmlWindow(wxHtmlWindow):
    basePath = None
    
    def __init__(self, parent, *args, **kwargs):
        wxHtmlWindow.__init__(self, parent, *args, **kwargs)
        self.SetForegroundColour(parent.GetForegroundColour())
        self.SetBackgroundColour(parent.GetBackgroundColour())
        # bugfix: don't open links to soon, as the event might come from the
        # opening of this window (mouse up event)
        self.waiting = True
        Timer(0.5, self.OnTimeout).start()


    def SetPage(self, html):
        pos = html.find("<rst>")
        if pos != -1:
            html = eg.Utils.DecodeReST(html[pos+5:])
        wxHtmlWindow.SetPage(
            self,
            '<html><body bgcolor="%s" text="%s">%s</body></html>' % (
                self.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX), 
                self.GetForegroundColour().GetAsString(wx.C2S_HTML_SYNTAX), 
                html
            )
        )
        
    
    def OnTimeout(self):
        self.waiting = False
        
    
    def OnLinkClicked(self, link):
        if not self.waiting:
            Thread(target=webbrowser.open, args=(link.GetHref(), 0)).start()
        
        
    def SetBasePath(self, basePath):
        self.basePath = basePath
        
        
    def OnOpeningURL(self, htmlUrlType, url):
        if (
            htmlUrlType == HTML_URL_IMAGE
            and (self.basePath is not None)
            and not url.startswith(self.basePath)
        ):
            return self.basePath + url
        else:
            return HTML_OPEN
        
        