import webbrowser
import thread

from wx.lib.hyperlink import HyperLinkCtrl as wxHyperLinkCtrl


class HyperLinkCtrl(wxHyperLinkCtrl):
    
    def GotoURL(self, URL, ReportErrors=True, NotSameWinIfPossible=False):
        thread.start_new_thread(webbrowser.open, (URL, NotSameWinIfPossible))
        self.SetVisited(True)
        self.UpdateLink(True)
        return True


