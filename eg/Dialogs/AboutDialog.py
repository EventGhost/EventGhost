#
# eg/Dialogs/AboutDialog.py
#
# Copyright (C) 2005 Lars-Peter Voss
#
# This file is part of EventGhost.
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

import eg
import wx

import time
import sys
import platform
import thread
import threading

from cStringIO import StringIO
from math import sin

import Image
from eg.Controls.SizeGrip import SizeGrip


class Text:
    Title = "About EventGhost"
    Author = "Author: %s"
    Version = "Version: %s (build %s)"
    CreationDate = "%a, %d %b %Y %H:%M:%S"
    tabAbout = "About"
    tabSpecialThanks = "Special Thanks"
    tabLicense = "License Agreement"
    tabSystemInfo = "System Information"
    

Text = eg.GetTranslation(Text)



SPECIAL_THANKS_DATA = (
    (
        "Plugin Developers:",
        2,
        (
            ("MonsterMagnet", "Foobar2000, MPC, VLC, Speech"),
            ("Bartman", "Timer, HID, Registry"),
            ("Oliver Wagner", "Denon AV, Optoma H79"),
            ("Milbrot", "MyTheatre"),
            ("Matthew Jacob Edwards", "Winamp Extensions"),
            ("jorel1969", "Medio"),
            ("Mark Clarkson", "Yamaha RX-V1000 Serial"),
        ),
    ),
    (
        "Translators:",
        2,
        (
            ("Lubo&scaron; R&uuml;ckl", "Czech"),
        ),
    ),
    (
        'Donators:',
        2,
        (
            ('TomB', 'MCE remote'),
            ('dlandrum', 'PayPal'),
            ('Steve Ingamells', 'PayPal'),
            ('Stoffel', 'remote'),
            (
                'Jon Rhees, <a href="http://www.usbuirt.com/">USB-UIRT</a>', 
                'USB-UIRT'
            ),
            (
                'Jonah Peskin, <a href="http://www.streamzap.com/">' \
                    'Streamzap, Inc.</a>', 
                'Streamzap remote'
            ),
        ),
    ),
    (
        'Others:',
        2,
        (
            (
                'Benjamin Webb', 
                'for the nice <a href="http://www.eventghost.org/wiki/' \
                'Controlling_Your_Living_Room_with_EventGhost">' \
                'wiki article</a>'
            ),
            ('Oliver Wagner', 'for hosting the website'),
            ('Alf & Metallhuhn', 'for creating the EventGhost logo'),
            (
                'Mark James', 
                'for his <a href="http://www.famfamfam.com/">icons</a>'
            ),
        ),
    ),
)
        


class AnimatedWindow(wx.Window):
    
    def __init__(self, parent, id=-1):
        self.x = 0
        self.y = 0
        self.font = wx.Font(
            40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD
        )
        im = Image.open("images/logo.png").convert("RGBA")
        self.im1 = Image.fromstring("L", im.size, im.tostring()[3::4])
        self.im2 = Image.new("L", im.size, 0)
        self.alpha = 0
        self.image = wx.EmptyImage(im.size[0], im.size[1], 32)
        self.image.SetData(im.convert('RGB').tostring())
        self.bmpWidth = im.size[0]
        self.bmpHeight = im.size[1]
        self.time = time.clock()
        self.count = 0
        self.lock = threading.Lock()
        #self.brush = wx.Brush((255,255,255))
        wx.Window.__init__(self, parent, id)
        colour = (247, 247, 249)
        parent.SetBackgroundColour(colour)
        self.brush = wx.Brush(colour)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.OnSize(None)
        
        
    def OnSize(self,event):
        self.width, self.height = self.GetClientSizeTuple()
        self.lock.acquire()
        self.dcBuffer = wx.EmptyBitmap(self.width, self.height)
        self.lock.release()
        self.y3 = (self.height - self.bmpHeight) / 4.0
        self.x3 = (self.width - self.bmpWidth) / 4.0
        textWidth, _, _, _ = self.GetFullTextExtent("EventGhost", self.font) 
        self.textOffset = (self.width - textWidth) / 2
        self.UpdateDrawing()


    def UpdateDrawing(self):
        self.lock.acquire()
        dc = wx.BufferedDC(wx.ClientDC(self), self.dcBuffer)
        self.Draw(dc)
        self.lock.release()


    def DoAnimation(self):
        import ctypes
        kernel32 = ctypes.windll.kernel32
        thread = kernel32.GetCurrentThread()
        kernel32.SetThreadPriority(thread, -15)
        try:
            while 1:
                t = time.clock() / 2.0
                y3 = self.y3
                x3 = self.x3
                self.y = (sin(t) + sin(1.8 * t)) * y3 + y3 * 2.0
                self.x = (sin(t * 0.8) + sin(1.9 * t)) * x3 + x3 * 2.0
                self.alpha = sin(t) / 2.0 + 0.5
                self.UpdateDrawing()
                time.sleep(0.009)
        except:
            pass
                
                
    def Draw(self, dc):
        dc.BeginDrawing()
        dc.SetBackground(self.brush)
        dc.Clear() # make sure you clear the bitmap!
        dc.SetFont(self.font)
        dc.DrawText("EventGhost", self.textOffset, 50)
        im = Image.blend(self.im1, self.im2, self.alpha)
        self.image.SetAlphaData(im.tostring()) 
        bmp = wx.BitmapFromImage(self.image, 24)
        dc.DrawBitmap(bmp, self.x, self.y, True)
        dc.EndDrawing()



class Panel1(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        textCtrl = wx.StaticText(self, -1, "")
        hypelink1 = eg.HyperLinkCtrl(
            self, 
            wx.ID_ANY, 
            "Homepage", 
            URL="http://www.eventghost.org/"
        )
        hypelink2 = eg.HyperLinkCtrl(
            self,
            wx.ID_ANY, 
            "Forum",
            URL="http://www.eventghost.org/forum/"
        )
        hypelink3 = eg.HyperLinkCtrl(
            self,
            wx.ID_ANY, 
            "Wiki",
            URL="http://www.eventghost.org/wiki/"
        )
        
        animatedWindow = AnimatedWindow(self)
        
        linkLineSizer = wx.BoxSizer(wx.HORIZONTAL)
        linkLineSizer.Add((5,5), 1)
        linkLineSizer.Add(hypelink1, 0, wx.EXPAND, 15)
        linkLineSizer.Add((5,5), 1)
        linkLineSizer.Add(hypelink2, 0, wx.EXPAND, 15)
        linkLineSizer.Add((5,5), 1)
        linkLineSizer.Add(hypelink3, 0, wx.EXPAND, 15)
        linkLineSizer.Add((5,5), 1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(textCtrl, 0, wx.ALIGN_CENTER|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        sizer.Add(linkLineSizer, 0, wx.ALIGN_CENTER|wx.EXPAND)
        sizer.Add(animatedWindow, 1, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 10)
        self.SetSizerAndFit(sizer)
        thread.start_new_thread(animatedWindow.DoAnimation, ())



class Panel2(wx.Panel):
    
    def __init__(self, parent):        
        wx.Panel.__init__(self, parent)

        output = StringIO()
        write = output.write
        write('<TABLE COLS=2 WIDTH="100%">')
        for group, cols, persons in SPECIAL_THANKS_DATA:
            write('<TR><TD COLSPAN="2" ALIGN=CENTER><h5><i><u>')
            write(group)
            write('</h5></i></u></TD></TR>')
            if cols == 1:
                for name, descr in persons:
                    write('<TR><TD ALIGN=CENTER WIDTH="50%" COLSPAN="2"><B>')
                    write(name)
                    write('</B></RIGHT></TD></TR>')
            else:
                for name, descr in persons:
                    write('<TR><TD ALIGN=RIGHT WIDTH="50%"><B>')
                    write(name)
                    write('</B></RIGHT></TD><TD WIDTH="50%">')
                    write(descr)
                    write('</RIGHT></TD></TR>')
        write('</TABLE>')
        contents = output.getvalue()
        output.close()
        self.CreateHtmlWindow(contents)
        
        
    def CreateHtmlWindow(self, html):
        htmlWindow = eg.HtmlWindow(
            self, 
            style=wx.SUNKEN_BORDER|eg.HW_NO_SELECTION
        )
        htmlWindow.SetPage(html)
        htmlWindow.SetMinSize((460, 250))
        htmlWindow.SetScrollbars(1, 1, 1000, 1000)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(htmlWindow, 1, wx.EXPAND, 5)
        self.SetSizerAndFit(sizer)
        
    
        
        
class Panel3(Panel2):        
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.CreateHtmlWindow(eg.license)
        


class Panel4(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        compileTime = time.strftime(
            Text.CreationDate, 
            time.gmtime(eg.compileTime)
        )
        sysInfos = (
            ("EventGhost Version", eg.version),
            ("SVN Revision", eg.svnRevision),
            ("Compile Time", compileTime),
            ("Python Version", "%d.%d.%d %s %d" % sys.version_info),
            ("wxPython Version", wx.VERSION_STRING),
            ("PIL Version", Image.VERSION),
            ("Platform", platform.platform()),
        )
        sysInfoTemplate = "".join(
            [
                "<tr><td><b>%s:</b></td><td>%s</td></tr>" % sysInfo 
                for sysInfo in sysInfos
            ]
        )
            
        sysinfoHtml = eg.HtmlWindow(self, -1, style=wx.SUNKEN_BORDER)
        sysinfoHtml.SetPage("<table>%s</table>" % sysInfoTemplate)
        sysinfoHtml.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        sysinfoHtml.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.sysinfoHtml = sysinfoHtml
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sysinfoHtml, 1, wx.EXPAND, 5)
        self.SetSizerAndFit(sizer)

        self.contextMenu = eg.Menu(self, "EditMenu", eg.text.MainFrame.Menu)
        self.contextMenu.AddItem("Copy")
        

    def OnKeyDown(self, event):
        key = event.KeyCode() 
        controlDown = event.ControlDown() 
        if key == ord('C') and controlDown:
            self.OnCmdCopy(event)
        else:
            event.Skip()


    def OnRightClick(self, event):
        self.PopupMenu(self.contextMenu)


    def OnCmdCopy(self, event):
        if wx.TheClipboard.Open():
            text = self.sysinfoHtml.SelectionToText()
            text = text.replace("\n", "\r\n")             
            tdata = wx.TextDataObject(text)
            wx.TheClipboard.SetData(tdata)
            wx.TheClipboard.Close()
            wx.TheClipboard.Flush()
            eg.app.clipboardEvent.Fire()
                    
        
        
class AboutDialog(eg.Dialog):
    
    def __init__(self, parent=None):
        wx.Dialog.__init__(
            self, 
            parent, 
            -1, 
            Text.Title,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        )
        
        notebook = wx.Notebook(self)
        notebook.AddPage(Panel1(notebook), Text.tabAbout)
        notebook.AddPage(Panel2(notebook), Text.tabSpecialThanks)
        notebook.AddPage(Panel3(notebook), Text.tabLicense)
        notebook.AddPage(Panel4(notebook), Text.tabSystemInfo)

        okButton = wx.Button(self, wx.ID_OK, eg.text.General.ok)
        okButton.SetDefault()

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((0, 0), 1, wx.EXPAND)
        btnSizer.Add(
            okButton, 
            0, 
            wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALL, 
            5
        )
        btnSizer.Add((0, 0), 1, wx.EXPAND)
        btnSizer.Add(SizeGrip(self), 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(notebook, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        mainSizer.Add(btnSizer, 0, wx.EXPAND)

        self.SetSizerAndFit(mainSizer)
        self.SetMinSize(self.GetSize())


    
