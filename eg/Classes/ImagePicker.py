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


from base64 import b64decode, b64encode
from cStringIO import StringIO


class ImagePicker(wx.Window):
    
    def __init__(self, parent, label, title="", mesg="", imageString=None):
        self.title = title
        self.mesg = mesg
        wx.Window.__init__(self, parent, -1)
        self.button = wx.Button(self, -1, label)
        self.imageBox = wx.StaticBitmap(self, -1, size=(10, 10), style=wx.SUNKEN_BORDER)
        self.SetValue(imageString)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.button, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer.Add(self.imageBox, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Layout()


    def OnSetFocus(self, event):
        self.button.SetFocus()
        
        
    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()

        
    def OnButton(self, event):
        dialog = wx.FileDialog(
            self.GetParent(), 
            message=self.mesg,
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST,
            wildcard="BMP and GIF files (*.bmp;*.gif)|*.bmp;*.gif|PNG files (*.png)|*.png"

        )
        if dialog.ShowModal() == wx.ID_OK:
            filePath = dialog.GetPath()
            fd = open(filePath, "rb")
            stream = fd.read()
            fd.close()
            self.SetValue(b64encode(stream))
            event.Skip()
            
            
            
    def SetValue(self, imageString):
        self.imageString = imageString
        if imageString:
            stream = StringIO(b64decode(imageString))
            image = wx.ImageFromStream(stream)
            stream.close()
            boxWidth, boxHeight = (10, 10)
            w, h = image.GetSize()
            if w > boxWidth:
                h *= 1.0 * boxWidth / w
                w = boxWidth
            if h > boxHeight:
                w *= 1.0 * boxHeight / h
                h = boxHeight
            image.Rescale(w, h)
            bmp = wx.BitmapFromImage(image)
            self.imageBox.SetBitmap(bmp)
            self.imageBox.SetSize((30, 30))
        
    
    def GetValue(self):
        return self.imageString
