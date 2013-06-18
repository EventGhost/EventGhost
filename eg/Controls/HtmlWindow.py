import thread
import webbrowser
import threading

import wx
import wx.html as html

wx.InitAllImageHandlers()


class HtmlWindow(html.HtmlWindow):
    basePath = None
    
    def __init__(self, *args, **kwargs):
        html.HtmlWindow.__init__(self, *args, **kwargs)
        
        # bugfix: don't open links to soon, as the event might come from the
        # opening of this window (mouse up event)
        self.waiting = True
        threading.Timer(0.5, self.OnTimeout).start()


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
            type == html.HTML_URL_IMAGE
            and (self.basePath is not None)
            and not url.startswith(self.basePath)
        ):
            return self.basePath + url
        else:
            return html.HTML_OPEN
        
        