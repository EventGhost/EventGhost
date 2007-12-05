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

import threading
import httplib
import webbrowser


class Text(eg.TranslatableStrings):
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



class MessageDialog(eg.Dialog):
    
    def __init__(self, version, url):
        self.url = url
        currentVersion = eg.version
        eg.Dialog.__init__(self, None, -1, Text.title)
        bmp = wx.ArtProvider.GetBitmap(
            wx.ART_INFORMATION, 
            wx.ART_MESSAGE_BOX, 
            (32,32)
        )
        staticBitmap = wx.StaticBitmap(self, -1, bmp)
        staticText = wx.StaticText(
            self, 
            -1, 
            Text.newVersionMesg % (currentVersion, version)
        )
        downloadButton = wx.Button(self, -1, Text.downloadButton)
        downloadButton.Bind(wx.EVT_BUTTON, self.OnOk)
        cancelButton = wx.Button(self, -1, eg.text.General.cancel)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(staticBitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer2.Add((5,5), 0)
        sizer2.Add(
            staticText, 
            0, 
            wx.TOP|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 
            10
        )
        
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(downloadButton)
        sizer3.Add((5,5), 0)
        sizer3.Add(cancelButton)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer2)
        sizer.Add((5,5), 1)
        sizer.Add(sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add((2,10), 0)      
        self.SetSizerAndFit(sizer)
        self.DoModal()
        
 
    def OnCancel(self, event):
        self.Close()
        

    def OnOk(self, event):
        webbrowser.open(self.url, True, True)
        self.Close()
        
        
        
def CenterOnParent(self):
    parent = eg.document.frame
    if parent is None:
        return
    x, y = parent.GetPosition()
    parentWidth, parentHeight = parent.GetSize()
    width, height = self.GetSize()
    self.SetPosition(
        ((parentWidth - width) / 2 + x, (parentHeight - height) / 2 + y)
    )
    
    
def ShowWaitDialog():
    dialog = wx.Dialog(None, style=wx.THICK_FRAME|wx.DIALOG_NO_PARENT)
    staticText = wx.StaticText(dialog, -1, Text.waitMesg)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(staticText, 1, wx.ALL, 20)
    dialog.SetSizerAndFit(sizer)
    CenterOnParent(dialog)
    dialog.Show()
    wx.GetApp().Yield()
    return dialog
    
    
def _checkUpdate(manually=False):
    dialog = None
    try:
        if manually:
            dialog = ShowWaitDialog()
        conn = httplib.HTTPConnection("www.eventghost.org")
        conn.connect()
        conn.sock.settimeout(10.0) 
        conn.request("GET", "/latest_version.txt")
        response = conn.getresponse()
        if dialog:
            dialog.Destroy()
            dialog = None
        if response.status != 200:
            conn.close()
            raise
        data = response.read().splitlines()
        conn.close()
        newVersion = data[0]
        newVersionTuple = newVersion.split(".")
        currentVersionTuple = eg.version.split(".")
        for i in xrange(0, len(currentVersionTuple)):
            if newVersionTuple[i] > currentVersionTuple[i]:
                wx.CallAfter(MessageDialog, newVersion, data[1])
                return
        if manually:
            dialog = wx.MessageDialog(
                None, 
                Text.ManOkMesg, 
                Text.ManOkTitle,
                style=wx.OK|wx.ICON_INFORMATION
            )
            dialog.ShowModal()
            dialog.Destroy()
    except:
        if dialog:
            dialog.Destroy()
        if manually:
            dialog = wx.MessageDialog(
                None, 
                Text.ManErrorMesg,
                Text.ManErrorTitle,
                style=wx.OK|wx.ICON_ERROR
            )
            dialog.ShowModal()
            dialog.Destroy()
        
        
        
@eg.LogIt
def Start():
    threading.Thread(target=_checkUpdate, name="CheckUpdate").start()


def CheckUpdateManually():
    _checkUpdate(manually=True)
