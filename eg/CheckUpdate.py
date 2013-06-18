import threading
import httplib
import webbrowser

import wx
import eg

class Text:
    title = "New EventGhost version available..."
    newVersionMesg = \
        "A newer version of EventGhost has been released.\n\n"\
        "\tYour version:\t%s\n"\
        "\tLatest version:\t%s\n\n"\
        "Do you want to visit the download page now?"
    downloadButton = "Visit download page"
    waitMesg = "Please wait while EventGhost retrieves update information."
    ManOkTitle = "No newer version available"    
    ManOkMesg = "This version of EventGhost is the newest."    
    ManErrorTitle = "Error while checking for update"
    ManErrorMesg = \
        "It wasn't possible to get the information from the EventGhost "\
        "website.\n\n"\
        "Please try it again later."

Text = eg.GetTranslation(Text)


class MessageDialog(eg.Dialog):
    def __init__(self, version, url):
        self.url = url
        cur_version = eg.version
        eg.Dialog.__init__(self, None, -1, Text.title)
        bmp = wx.ArtProvider.GetBitmap(
            wx.ART_INFORMATION, 
            wx.ART_MESSAGE_BOX, 
            (32,32)
        )
        st_bmp = wx.StaticBitmap(self, -1, bmp)
        st_txt = wx.StaticText(
            self, 
            -1, 
            Text.newVersionMesg % (cur_version, version)
        )
        dwnld_btn = wx.Button(self, -1, Text.downloadButton)
        dwnld_btn.Bind(wx.EVT_BUTTON, self.OnOk)
        cancel_btn = wx.Button(self, -1, eg.text.General.cancel)
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(st_bmp, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer2.Add((5,5), 0)
        sizer2.Add(
            st_txt, 
            0, 
            wx.TOP|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 
            10
        )
        
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(dwnld_btn)
        sizer3.Add((5,5), 0)
        sizer3.Add(cancel_btn)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer2)
        sizer.Add((5,5), 1)
        sizer.Add(sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add((2,10), 0)      
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.DoModal()
        
 
    def OnCancel(self, event):
        self.Close()
        

    def OnOk(self, event):
        webbrowser.open(self.url, True, True)
        self.Close()
        
        
        
def CenterOnParent(self):
    parent = eg.mainFrame
    x,y = parent.GetPosition()
    width, height = parent.GetSize()
    cx = x + width / 2
    cy = y + height / 2
    width, height = self.GetSize()
    self.SetPosition((cx - width / 2, cy - height / 2))
    
    
def ShowWaitDialog():
    dlg = wx.Dialog(
        None, 
        -1, 
        pos=eg.mainFrame.GetPosition(),
        style=wx.THICK_FRAME|wx.DIALOG_NO_PARENT
    )
    st_txt = wx.StaticText(dlg, -1, Text.waitMesg)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(st_txt, 1, wx.ALL, 20)
    dlg.SetSizer(sizer)
    dlg.SetAutoLayout(True)
    sizer.Fit(dlg)
    CenterOnParent(dlg)
    dlg.Show()
    wx.GetApp().Yield()
    return dlg
    
    
def _checkUpdate(manually = False):
    dlg = None
    try:
        if manually:
            dlg = ShowWaitDialog()
        conn = httplib.HTTPConnection("www.eventghost.org")
        conn.connect()
        conn.sock.settimeout(10.0) 
        conn.request("GET", "/latest_version.txt")
        response = conn.getresponse()
        if dlg:
            dlg.Destroy()
            dlg = None
        if response.status != 200:
            conn.close()
            raise
        data = response.read().splitlines()
        conn.close()
        new_version = data[0]
        new_tuple = new_version.split(".")
        cur_tuple = eg.version.split(".")
        for i in xrange(0, len(cur_tuple)):
            if new_tuple[i] > cur_tuple[i]:
                wx.CallAfter(MessageDialog, new_version, data[1])
                return
        if manually:
            dlg = wx.MessageDialog(
                None, 
                Text.ManOkMesg, 
                Text.ManOkTitle,
                style=wx.OK|wx.ICON_INFORMATION
            )
            dlg.ShowModal()
            dlg.Destroy()
    except:
        if dlg:
            dlg.Destroy()
        if manually:
            dlg = wx.MessageDialog(
                None, 
                Text.ManErrorMesg,
                Text.ManErrorTitle,
                style=wx.OK|wx.ICON_ERROR
            )
            dlg.ShowModal()
            dlg.Destroy()
        
        
        
def CheckUpdate():
    threading.Thread(target=_checkUpdate, name="CheckUpdate").start()


def CheckUpdateManually():
    _checkUpdate(True)