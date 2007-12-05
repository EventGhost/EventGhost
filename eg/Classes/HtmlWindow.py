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

import thread
import webbrowser
import threading

from wx.html import HtmlWindow as OriginalHtmlWindow
from wx.html import HTML_URL_IMAGE, HTML_OPEN

wx.InitAllImageHandlers()


class HtmlWindow(OriginalHtmlWindow):
    basePath = None
    
    def __init__(self, parent, *args, **kwargs):
        OriginalHtmlWindow.__init__(self, parent, *args, **kwargs)
        self.SetForegroundColour(parent.GetForegroundColour())
        self.SetBackgroundColour(parent.GetBackgroundColour())
        # bugfix: don't open links to soon, as the event might come from the
        # opening of this window (mouse up event)
        self.waiting = True
        threading.Timer(0.5, self.OnTimeout).start()


    def SetPage(self, html):
        r1, g1, b1 = self.GetBackgroundColour().Get()
        r2, g2, b2 = self.GetForegroundColour().Get()
        OriginalHtmlWindow.SetPage(
            self,
            '<html><body bgcolor="#%02X%02X%02X" text="#%02X%02X%02X">%s</body></html>' 
                % (r1, g1, b1, r2, g2, b2, html)
        )
        
    
    
    def OnTimeout(self):
        self.waiting = False
        
    
    def __open_url(self, URL, NotSameWinIfPossible=0):
        webbrowser.open(URL, NotSameWinIfPossible)
    
    
    def OnLinkClicked(self, link):
        if not self.waiting:
            thread.start_new_thread(self.__open_url, (link.GetHref(),))
        
        
    def SetBasePath(self, basePath):
        self.basePath = basePath
        
        
    def OnOpeningURL(self, type, url):
        if (
            type == HTML_URL_IMAGE
            and (self.basePath is not None)
            and not url.startswith(self.basePath)
        ):
            return self.basePath + url
        else:
            return HTML_OPEN
        
        