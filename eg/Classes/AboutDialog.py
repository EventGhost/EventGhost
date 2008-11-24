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

import eg
import wx
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
    


def GetPluginAuthors():
    """
    Returns a list of all plugin authors and the names of their plugins.
    
    Every item in the list is a tuple of the author's name and a string
    containing all plugin names of the author.
    """
    pluginAuthors = {}
    for pluginInfo in eg.pluginManager.database.itervalues():
        for part in pluginInfo.author.split("&"):
            author = part.strip()
            if author.lower() != "bitmonster":
                break
        else:
            continue
        pluginName = pluginInfo.name.replace(" ", "&nbsp;")
        if author in pluginAuthors:
            pluginAuthors[author].append(pluginName)
        else:
            pluginAuthors[author] = [pluginName]
    tmp = pluginAuthors.items()
    tmp.sort(key=lambda x: (-len(x[1]), x[0].lower()))
    authorList = []
    for author, pluginNames in tmp:
        pluginNames.sort(key=str.lower)
        authorList.append((author, ",<BR>".join(pluginNames)))
    return authorList
    

SPECIAL_THANKS_DATA = (
    ("Plugin Developers:", 2, GetPluginAuthors()),
    (
        "Translators:",
        2,
        (
            ("Lubo&scaron; R&uuml;ckl", "Czech"),
            ("Fredrik Jacobsson", "Swedish"),
            ("karlr", "Spanish"),            
        ),
    ),
    (
        "PayPal Donators:",
        0,
        (
            "dlandrum",
            "Steve Ingamells",
            "damdy-cash",
            "krambriw",
            "loomy",
            "specter333",        # 20. Jan 2008
            "Argofanatic",       # 24. Mar 2008
            "bskchaos",          #  8. Apr 2008
            "Warren Hatch",      # 26. Apr 2008
            "Daniel Henriksson", #  3. May 2008
            "skyanchor",         # 13. May 2008
            "Vlad Skarzhevskyy", # 13. Jun 2008
            "David Church",      # 17. Aug 2008
            "Tyson Ward",        # 30. Sep 2008
            "Glenn Maples",      # 13. Okt 2008
            "John Leonard",      # 21. Okt 2008
        ),
    ),
    (
        'Other Donators:',
        2,
        (
            ('TomB', 'MCE remote'),
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
        'Other Contributions:',
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
            if cols == 0:
                write('<TR><TD ALIGN=CENTER WIDTH="50%" COLSPAN="2"><B>')
                persons = [name.replace(" ", "&nbsp;") for name in persons]
                write(", ".join(persons))
                write(' and&nbsp;some&nbsp;anonymous&nbsp;people.')
                write('</B></RIGHT></TD></TR>')
            elif cols == 1:
                for name, descr in persons:
                    write('<TR><TD ALIGN=CENTER WIDTH="50%" COLSPAN="2"><B>')
                    write(name)
                    write('</B></RIGHT></TD></TR>')
            else:
                for name, descr in persons:
                    write('<TR><TD ALIGN=RIGHT VALIGN=TOP WIDTH="50%"><B>')
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
        buildTime = time.strftime(
            Text.CreationDate, 
            time.gmtime(eg.Version.buildTime)
        )
        self.sysInfos = (
            ("EventGhost Version", eg.Version.string),
            ("SVN Revision", eg.Version.svnRevision),
            ("Build Time", buildTime),
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
        tag = None
        buffer = ""
        for line in fd:
            if line.startswith("   "):
                buffer += line
                continue    
            if line.strip == "":
                continue        
            if tag:
                res.append(lineTemplate % (tag, buffer))
                tag = None
            if line.startswith("- "):
                tag = line[2:5]
                buffer = line[7:]
            elif line.startswith("Version"):
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
    
