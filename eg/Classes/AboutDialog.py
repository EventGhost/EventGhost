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

import eg.Version

import time
import sys
import platform
from cStringIO import StringIO

import Image



class Text(eg.TranslatableStrings):
    Title = "About EventGhost"
    Author = "Author: %s"
    Version = "Version: %s (build %s)"
    CreationDate = "%a, %d %b %Y %H:%M:%S"
    tabAbout = "About"
    tabSpecialThanks = "Special Thanks"
    tabLicense = "License Agreement"
    tabSystemInfo = "System Information"
    tabChangelog = "Changelog"
    


SPECIAL_THANKS_DATA = (
    (
        "Plugin Developers:",
        2,
        (
            ("Bartman", "Timer, HID, Registry, ffdshow"),
            ("MonsterMagnet", "Foobar2000, MPC, VLC, Speech"),
            ("Oliver Wagner", "Denon AV, Optoma H79, JVC HD-1"),
            ("Lubo&scaron; R&uuml;ckl", "Billy, MediaMonkey, IrfanView"),
            ("Dexter", "Sound Mixer Ex, Marantz Serial"),
            ("Milbrot", "MyTheatre"),
            ("Matthew Jacob Edwards", "Winamp Extensions"),
            ("jorel1969", "Meedio"),
            ("Mark Clarkson", "Yamaha RX-V1000 Serial"),
            ("jinxdone", "LIRC Event Receiver"),
            ("Micke Prag", "TellStick"),
            ("oystein", "Windows Media Player"),
            ("SurFan", "TheaterTek"),
            ("townkat", "DVB Dream"),
            ("Thierry Couquillou", "PlayStation 3 Bluetooth Remote"),
            ("Dean Owens", "X10 CM15A"),
        ),
    ),
    (
        "Translators:",
        2,
        (
            ("Lubo&scaron; R&uuml;ckl", "Czech"),
            ("Fredrik Jacobsson", "Swedish"),
        ),
    ),
    (
        'Donators:',
        2,
        (
            ('TomB', 'MCE remote'),
            ('dlandrum', 'PayPal'),
            ('Steve Ingamells', 'PayPal'),
            ('damdy-cash', 'PayPal'),
            ('krambriw', 'PayPal'),
            ('loomy', 'PayPal'),
            ('specter333', 'PayPal'),
            ('some anonymous people', 'PayPal'),
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
                (
                    'for the nice <a href="http://www.eventghost.org/wiki/' 
                    'Controlling_Your_Living_Room_with_EventGhost">'
                    'wiki article</a>'
                )
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
        

class AboutPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        backgroundColour = (255, 255, 255)
        self.SetBackgroundColour(backgroundColour)
        hypelink1 = eg.HyperLinkCtrl(
            self, 
            wx.ID_ANY, 
            eg.text.MainFrame.Menu.WebHomepage, 
            URL="http://www.eventghost.org/"
        )
        font = hypelink1.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        hypelink1.SetFont(font)
        hypelink2 = eg.HyperLinkCtrl(
            self,
            wx.ID_ANY, 
            eg.text.MainFrame.Menu.WebForum,
            URL="http://www.eventghost.org/forum/"
        )
        hypelink2.SetFont(font)
        hypelink3 = eg.HyperLinkCtrl(
            self,
            wx.ID_ANY, 
            eg.text.MainFrame.Menu.WebWiki,
            URL="http://www.eventghost.org/wiki/"
        )
        hypelink3.SetFont(font)
        
        animatedWindow = eg.AnimatedWindow(self)
        animatedWindow.SetBackgroundColour(backgroundColour)
        
        sizer = eg.VBoxSizer(
            (eg.HBoxSizer(
                ((5,5), 1),
                (hypelink1, 0, wx.EXPAND, 15),
                ((5,5), 1),
                (hypelink2, 0, wx.EXPAND, 15),
                ((5,5), 1),
                (hypelink3, 0, wx.EXPAND, 15),
                ((5,5), 1),
            ), 0, wx.ALIGN_CENTER|wx.EXPAND|wx.TOP, 15),
            (animatedWindow, 1, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 10),
        )
        self.SetSizerAndFit(sizer)



class HtmlPanel(wx.Panel):
    
    def __init__(self, parent, html):
        wx.Panel.__init__(self, parent)
        htmlWindow = eg.HtmlWindow(
            self, 
            style=wx.SUNKEN_BORDER|wx.html.HW_NO_SELECTION
        )
        htmlWindow.SetForegroundColour(eg.colour.windowText)
        htmlWindow.SetBackgroundColour(eg.colour.windowBackground)
        htmlWindow.SetPage(html)
        htmlWindow.SetMinSize((480, 270))
        htmlWindow.SetScrollbars(1, 1, 1000, 1000)
        self.SetSizerAndFit(
            eg.VBoxSizer(
                (htmlWindow, 1, wx.EXPAND, 5),
            )
        )
        self.htmlWindow = htmlWindow
        


class SpecialThanksPanel(HtmlPanel):
    
    def __init__(self, parent):        

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
        HtmlPanel.__init__(self, parent, contents)
        
    
        
        
class LicensePanel(HtmlPanel):        
    
    def __init__(self, parent):
        HtmlPanel.__init__(self, parent, eg.License)
        


class SystemInfoPanel(HtmlPanel):
    
    def __init__(self, parent):
        compileTime = time.strftime(
            Text.CreationDate, 
            time.gmtime(eg.Version.compileTime)
        )
        self.sysInfos = (
            ("EventGhost Version", eg.versionStr),
            ("SVN Revision", eg.Version.svnRevision),
            ("Compile Time", compileTime),
            ("Python Version", "%d.%d.%d %s %d" % sys.version_info),
            ("wxPython Version", wx.VERSION_STRING),
            ("PIL Version", Image.VERSION),
            ("Platform", platform.platform()),
        )
        
        sysInfoTemplate = "".join(
            ["<tr><td><b>%s:</b></td><td>%s</td></tr>" % sysInfo 
                for sysInfo in self.sysInfos]
        )
            
        HtmlPanel.__init__(self, parent, "<table>%s</table>" % sysInfoTemplate)
        self.htmlWindow.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.htmlWindow.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        
        self.contextMenu = eg.Menu(self, "EditMenu", eg.text.MainFrame.Menu)
        self.contextMenu.AddItem("Copy")
        

    @eg.LogIt
    def OnKeyDown(self, event):
        key = event.GetKeyCode() 
        controlDown = event.ControlDown() 
        if key == ord('C') and controlDown:
            self.OnCmdCopy(event)
        else:
            event.Skip()


    def OnRightClick(self, event):
        self.PopupMenu(self.contextMenu)


    @eg.LogIt
    def OnCmdCopy(self, event):
        if wx.TheClipboard.Open():
            text = "\r\n".join(["%s: %s" % x for x in self.sysInfos])
            tdata = wx.TextDataObject(text)
            wx.TheClipboard.SetData(tdata)
            wx.TheClipboard.Close()
            wx.TheClipboard.Flush()
            eg.app.clipboardEvent.Fire()
                    

     
        
class ChangelogPanel(HtmlPanel):
    
    def __init__(self, parent):
        try:
            fd = open("CHANGELOG.TXT")
        except:
            return
        res = ["<TABLE>"]
        headerTemplate = (
            "<TR><TD COLSPAN=2><P><FONT SIZE=+0><B><U>%s"
            "</U></B></FONT></TD</TR>"
        )
        lineTemplate = (
            "<TR>"
            "<TD VALIGN=TOP><b>&nbsp;&nbsp;%s</b></TD>"
            "<TD>%s</TD>"
            "</TR>"
        )
        for line in fd:
            if line.startswith("+"):
                res.append(lineTemplate % ("NEW", line[1:]))
            elif line.startswith("-"):
                res.append(lineTemplate % ("FIX", line[1:]))
            elif line.startswith("*"):
                res.append(lineTemplate % ("UPD", line[1:]))
            elif line.strip() == "":
                pass
            else:
                res.append(headerTemplate % line)
        res.append("</TABLE>")
        fd.close()
        HtmlPanel.__init__(self, parent, "".join(res))



class AboutDialog(eg.Dialog):

    def Process(self, parent):
        eg.Dialog.__init__(
            self, 
            parent, 
            -1, 
            Text.Title,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        )
        notebook = wx.Notebook(self)
        notebook.AddPage(AboutPanel(notebook), Text.tabAbout)
        notebook.AddPage(SpecialThanksPanel(notebook), Text.tabSpecialThanks)
        notebook.AddPage(LicensePanel(notebook), Text.tabLicense)
        notebook.AddPage(SystemInfoPanel(notebook), Text.tabSystemInfo)
        notebook.AddPage(ChangelogPanel(notebook), Text.tabChangelog)
        
        def OnPageChanged(event):
            pageNum = event.GetSelection()
            notebook.ChangeSelection(pageNum)
            notebook.GetPage(pageNum).SetFocus()
        notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, OnPageChanged)
        
        okButton = wx.Button(self, wx.ID_OK, eg.text.General.ok)
        okButton.SetDefault()
        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        
        buttonSizer = eg.HBoxSizer(
            ((0, 0), 1, wx.EXPAND),
            (okButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALL, 5),
            ((0, 0), 1, wx.EXPAND),
            (eg.SizeGrip(self), 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT),
        )
        mainSizer = eg.VBoxSizer(
            (notebook, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5),
            (buttonSizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(mainSizer)
        self.SetMinSize(self.GetSize())
        self.Affirmed()
    
        
        
        