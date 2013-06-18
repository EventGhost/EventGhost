import eg
import wx

import time
import sys
import platform
import thread
import threading

from string import Template
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


system_template = """
<table>
    <tr><td><b>EventGhost Version:</b></td><td>$version build $build</td></tr>
    <tr><td><b>Compile Time:</b></td><td>$compileTime</td></tr>
    <tr><td><b>Python Version:</b></td><td>$pyVersion</td></tr>
    <tr><td><b>wxPython Version:</b></td><td>$wxVersion</td></tr>
    <tr><td><b>PIL Version:</b></td><td>$pilVersion</td></tr>
    <tr><td><b>Platform:</b></td><td>$platform</td></tr>
</table>
"""

ST = (
    (
        "Plugin Developers:",
        1,
        (
            ("MonsterMagnet", ""),
            ("Bartman", ""),
            ("Milbrot", ""),
            ("Oliver Wagner", ""),
            ("Matthew Jacob Edwards", ""),
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
            ('Jon Rhees, <a href="http://www.usbuirt.com/">USB-UIRT</a>', 'USB-UIRT'),
            ('Jonah Peskin, <a href="http://www.streamzap.com/">Streamzap, Inc.</a>', 'Streamzap remote'),
        ),
    ),
    (
        'Others:',
        2,
        (
            ('Benjamin Webb', 'for the nice <a href="http://www.eventghost.org/wiki/Controlling_Your_Living_Room_with_EventGhost">wiki article</a>'),
            ('Oliver Wagner', 'for hosting the website'),
            ('Alf & Metallhuhn', 'for creating the EventGhost logo'),
            ('Mark James', 'for his <a href="http://www.famfamfam.com/">icons</a>'),
        ),
    ),
)
        


class AnimatedWindow(wx.Window):
    
    def __init__(self, parent, id = -1):
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
        self.bmp_width = im.size[0]
        self.bmp_height = im.size[1]
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
        self.Width, self.Height = self.GetClientSizeTuple()
        self.lock.acquire()
        self._Buffer = wx.EmptyBitmap(self.Width, self.Height)
        self.lock.release()
        self.y3 = (self.Height - self.bmp_height) / 4.0
        self.x3 = (self.Width - self.bmp_width) / 4.0
        self.UpdateDrawing()


    def UpdateDrawing(self):
        self.lock.acquire()
        dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
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
        dc.DrawText("EventGhost", 50, 50)
        im = Image.blend(self.im1, self.im2, self.alpha)
        self.image.SetAlphaData(im.tostring()) 
        bmp = wx.BitmapFromImage(self.image, 24)
        dc.DrawBitmap(bmp, self.x, self.y, True)
        dc.EndDrawing()



class AboutDialog(eg.Dialog):
    
    def __init__(self, parent=None):
        wx.Dialog.__init__(
            self, 
            parent, 
            -1, 
            Text.Title,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        )
        
        nb = wx.Notebook(self)
        self.notebook = nb
        
        page1 = wx.Panel(nb, style=wx.SUNKEN_BORDER)
        nb.AddPage(page1, Text.tabAbout)
        
        textCtrl = wx.StaticText(page1, -1, "")
        hypelink1 = eg.HyperLinkCtrl(
            page1, 
            wx.ID_ANY, 
            "Homepage", 
            URL="http://www.eventghost.org/"
        )
        hypelink2 = eg.HyperLinkCtrl(
            page1,
            wx.ID_ANY, 
            "Forum",
            URL="http://www.eventghost.org/forum/"
        )
        hypelink3 = eg.HyperLinkCtrl(
            page1,
            wx.ID_ANY, 
            "Wiki",
            URL="http://www.eventghost.org/wiki/"
        )
        
        animatedWindow = AnimatedWindow(page1, -1)
        
        linkLineSizer = wx.BoxSizer(wx.HORIZONTAL)
        linkLineSizer.Add((5,5), 1)
        linkLineSizer.Add(hypelink1, 0, wx.EXPAND, 15)
        linkLineSizer.Add((5,5), 1)
        linkLineSizer.Add(hypelink2, 0, wx.EXPAND, 15)
        linkLineSizer.Add((5,5), 1)
        linkLineSizer.Add(hypelink3, 0, wx.EXPAND, 15)
        linkLineSizer.Add((5,5), 1)
        
        page1Sizer = wx.BoxSizer(wx.VERTICAL)
        page1Sizer.Add(
            textCtrl, 0, wx.ALIGN_CENTER|wx.TOP|wx.LEFT|wx.RIGHT, 5
        )
        page1Sizer.Add(linkLineSizer, 0, wx.ALIGN_CENTER|wx.EXPAND)
        page1Sizer.Add(
            animatedWindow, 1, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 10
        )
        page1.SetSizer(page1Sizer)
        page1.SetAutoLayout(True)

        nb.AddPage(
            self.CreateHtmlPanel(nb, self.CreateSpecialThanksHtml()), 
            Text.tabSpecialThanks
        )
        nb.AddPage(self.CreateHtmlPanel(nb, eg.license), Text.tabLicense)
        
        page4 = wx.Panel(nb)
        nb.AddPage(page4, Text.tabSystemInfo)
        d = dict(
            version = eg.version,
            build = str(eg.buildNum),
            compileTime = time.strftime(
                Text.CreationDate,
                time.gmtime(eg.compileTime)
            ),
            pyVersion = "%d.%d.%d %s %d" % sys.version_info,
            wxVersion = wx.VERSION_STRING,
            pilVersion = Image.VERSION,
            platform = platform.platform(),
        )
            
        sysinfoHtml = eg.HtmlWindow(page4, -1, style=wx.SUNKEN_BORDER)
        sysinfoHtml.SetPage(Template(system_template).substitute(d))
        self.sysinfoHtml = sysinfoHtml
        page4Sizer = wx.BoxSizer(wx.VERTICAL)
        page4Sizer.Add(sysinfoHtml, 1, wx.EXPAND, 5)
        page4.SetSizer(page4Sizer)
        page4.SetAutoLayout(True)
        sysinfoHtml.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        sysinfoHtml.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

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
        mainSizer.Add(nb, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        mainSizer.Add(btnSizer, 0, wx.EXPAND)

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        mainSizer.Fit(self)
        self.SetMinSize(self.GetSize())

        self.contextMenu = eg.Menu(self, "EditMenu", eg.text.MainFrame.Menu)
        self.contextMenu.AddItem("Copy")
        thread.start_new_thread(animatedWindow.DoAnimation, ())


    def CreateSpecialThanksHtml(self):
        output = StringIO()
        write = output.write
        write('<TABLE COLS=2 WIDTH="100%">')
        for group, cols, persons in ST:
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
        return contents
        
        
    def CreateHtmlPanel(self, notebook, html):
        panel = wx.Panel(notebook)
        licenseHtml = eg.HtmlWindow(
            panel, 
            style=wx.SUNKEN_BORDER|eg.HW_NO_SELECTION
        )
        licenseHtml.SetPage(html)
        licenseHtml.SetMinSize((460, 250))
        licenseHtml.SetScrollbars(1, 1, 1000, 1000)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(licenseHtml, 1, wx.EXPAND, 5)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        return panel
        
    
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
            
    