# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import hashlib
import os
import re
import sys
import time
import wx
import _winreg
from StringIO import StringIO

# Local imports
import eg
from eg.WinApi.Dynamic import (
    MEMORYSTATUSEX, GlobalMemoryStatusEx, byref, sizeof
)

try:
    import stackless  # NOQA
    is_stackless = True
except ImportError:
    is_stackless = False

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


class AboutDialog(eg.TaskletDialog):
    instance = None

    @eg.LogItWithReturn
    def Configure(self, parent):  #IGNORE:W0221
        if AboutDialog.instance:
            AboutDialog.instance.Raise()
            return
        AboutDialog.instance = self
        eg.TaskletDialog.__init__(
            self,
            parent=parent,
            title=Text.Title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
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
            (okButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL, 5),
            ((0, 0), 1, wx.EXPAND),
            (eg.SizeGrip(self), 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT),
        )
        mainSizer = eg.VBoxSizer(
            (notebook, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5),
            (buttonSizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(mainSizer)
        self.SetMinSize(self.GetSize())
        while self.Affirmed():
            self.SetResult()
        AboutDialog.instance = None


class HtmlPanel(wx.Panel):
    def __init__(self, parent, html):
        wx.Panel.__init__(self, parent)
        htmlWindow = eg.HtmlWindow(
            self,
            style=wx.SUNKEN_BORDER | wx.html.HW_NO_SELECTION
        )
        htmlWindow.SetForegroundColour(eg.colour.windowText)
        htmlWindow.SetBackgroundColour(eg.colour.windowBackground)
        htmlWindow.SetPage(html)
        htmlWindow.SetMinSize((490, 270))
        htmlWindow.SetScrollbars(1, 1, 1000, 1000)
        self.SetSizerAndFit(
            eg.VBoxSizer(
                (htmlWindow, 1, wx.EXPAND, 5),
            )
        )
        self.htmlWindow = htmlWindow


class AboutPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        backgroundColour = (255, 255, 255)
        self.SetBackgroundColour(backgroundColour)
        hypelink1 = eg.HyperLinkCtrl(
            self,
            wx.ID_ANY,
            eg.text.MainFrame.Menu.WebHomepage.replace("&", ""),
            URL="http://www.eventghost.org/"
        )
        font = hypelink1.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        hypelink1.SetFont(font)
        hypelink2 = eg.HyperLinkCtrl(
            self,
            wx.ID_ANY,
            eg.text.MainFrame.Menu.WebForum.replace("&", ""),
            URL="http://www.eventghost.org/forum/"
        )
        hypelink2.SetFont(font)
        hypelink3 = eg.HyperLinkCtrl(
            self,
            wx.ID_ANY,
            eg.text.MainFrame.Menu.WebWiki.replace("&", ""),
            URL="http://www.eventghost.org/mediawiki/"
        )
        hypelink3.SetFont(font)

        animatedWindow = eg.AnimatedWindow(self)
        animatedWindow.SetBackgroundColour(backgroundColour)

        sizer = eg.VBoxSizer(
            (eg.HBoxSizer(
                ((5, 5), 1),
                (hypelink1, 0, wx.EXPAND, 15),
                ((5, 5), 1),
                (hypelink2, 0, wx.EXPAND, 15),
                ((5, 5), 1),
                (hypelink3, 0, wx.EXPAND, 15),
                ((5, 5), 1),
            ), 0, wx.ALIGN_CENTER | wx.EXPAND | wx.TOP, 15),
            (animatedWindow, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 10),
        )
        self.SetSizerAndFit(sizer)


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
                write('<TR><TD ALIGN=CENTER WIDTH="100%" COLSPAN="2"><B>')
                write('<TABLE><TR>')
                #persons = [name.replace(" ", "&nbsp;") for name in persons]
                col = 0
                for name in persons:
                    name = name.replace(" ", "&nbsp;")
                    write('<TD WIDTH="33%%"><CENTER>%s</CENTER></TD>' % name)
                    col += 1
                    if col == 3:
                        write("</TR><TR>")
                        col = 0
                #write(", ".join(persons))
                write('</TR><TR><TD COLSPAN=3><CENTER>')
                write('and&nbsp;some&nbsp;anonymous&nbsp;people')
                write('</CENTER></TD></TR></TABLE>')
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
                    write('</B></RIGHT></TD><TD WIDTH="50%"><I>')
                    write(descr)
                    write('</I></RIGHT></TD></TR>')
        write('</TABLE>')
        contents = output.getvalue()
        output.close()
        HtmlPanel.__init__(self, parent, contents)


class LicensePanel(HtmlPanel):
    def __init__(self, parent):
        HtmlPanel.__init__(self, parent, eg.License)


class SystemInfoPanel(HtmlPanel):
    def __init__(self, parent):
        from eg.WinApi.SystemInformation import GetWindowsVersionString
        buildTime = time.strftime(
            Text.CreationDate,
            time.gmtime(eg.Version.buildTime)
        ).decode(eg.systemEncoding)
        totalMemory = GetRam()[0]
        pythonVersion = "%d.%d.%d %s %d" % tuple(sys.version_info)
        if is_stackless:
            pythonVersion = "Stackless Python " + pythonVersion
        self.sysInfos = [
            "Software",
            ("Program Version", eg.Version.string),
            ("Build Time", buildTime),
            ("Python Version", pythonVersion),
            ("wxPython Version", wx.VERSION_STRING),
            "\nSystem",
            ("Operating System", GetWindowsVersionString()),
            ("CPU", GetCpuName()),
            ("RAM", "%s GB" % totalMemory),
            "\nUSB-Devices",
        ]
        devices = eg.WinUsb.ListDevices()
        for hardwareId in sorted(devices.keys()):
            device = devices[hardwareId]
            self.sysInfos.append((device.name, device.hardwareId))
        lines = []
        for line in self.sysInfos:
            if isinstance(line, tuple):
                lines.append('<tr><td>%s:</td><td>%s</td></tr>' % line)
            else:
                lines.append('</table><p><b>%s</b><br><table>' % line)
        lines.append('</table>')
        page = "\n".join(lines)
        HtmlPanel.__init__(self, parent, page)
        self.htmlWindow.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.htmlWindow.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        contextMenu = wx.Menu()
        contextMenu.Append(wx.ID_COPY, eg.text.MainFrame.Menu.Copy)
        self.Bind(wx.EVT_MENU, self.OnCmdCopy, id=wx.ID_COPY)
        self.contextMenu = contextMenu

    @eg.LogIt
    def OnCmdCopy(self, dummyEvent):
        if not wx.TheClipboard.Open():
            return
        lines = []
        for line in self.sysInfos:
            if isinstance(line, tuple):
                lines.append("%s: %s" % line)
            else:
                lines.append("%s" % line)
        text = "\n".join(lines)
        tdata = wx.TextDataObject(text.replace("\n", "\r\n"))
        wx.TheClipboard.SetData(tdata)
        wx.TheClipboard.Close()
        wx.TheClipboard.Flush()

    @eg.LogIt
    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        controlDown = event.ControlDown()
        if key == ord('C') and controlDown:
            self.OnCmdCopy(event)
        else:
            event.Skip()

    def OnRightClick(self, dummyEvent):
        self.PopupMenu(self.contextMenu)


class ChangelogPanel(HtmlPanel):
    @eg.TimeIt
    def __init__(self, parent):
        try:
            infile = open(os.path.join(eg.mainDir, "CHANGELOG.md"))
            text = infile.read()
        except IOError:
            text = ""

        # test if the changelog has changed. If not read the changelog.dat
        # from the config dir, as it is already parsed.
        digest = hashlib.md5(text).hexdigest()
        changelogDatPath = os.path.join(eg.configDir, "changelog.dat")
        if not os.path.exists(changelogDatPath):
            text = self.UpdateChangelog(changelogDatPath, text, digest)
        else:
            changelogDatFile = open(changelogDatPath, "rt")
            oldDigest = changelogDatFile.readline().strip()
            if oldDigest != digest:
                changelogDatFile.close()
                text = self.UpdateChangelog(changelogDatPath, text, digest)
            else:
                text = changelogDatFile.read()
        HtmlPanel.__init__(self, parent, text)

    @eg.LogIt
    def UpdateChangelog(self, changelogDatPath, text, digest):
        """
        Parses the Markdown and stores a copy of the result in the
        eg.configDir to speed up loading.
        """
        text = eg.Utils.DecodeMarkdown(text)
        changelogDatFile = open(changelogDatPath, "wt")
        changelogDatFile.write(digest + "\n")
        changelogDatFile.write(text)
        changelogDatFile.close()
        return text


def GetCpuName():
    name = GetRegistryValue(
        r"HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        "ProcessorNameString"
    )
    if name:
        return name
    else:
        id = GetRegistryValue(
            r"HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\CentralProcessor\0",
            "Identifier")
        vendor = GetRegistryValue(
            r"HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\CentralProcessor\0",
            "VendorIdentifier")
        return "%s, %s" % (id, vendor)

def GetPluginAuthors():
    """
    Returns a list of all plugin authors and the names of their plugins.

    Every item in the list is a tuple of the author's name and a string
    containing all plugin names of the author.
    """
    pluginAuthors = {}
    for pluginInfo in eg.pluginManager.database.itervalues():
        pluginName = pluginInfo.name.replace(" ", "&nbsp;")
        for part in re.split("\s*(?:&|,|\+|/|and)\s*", pluginInfo.author):
            author = part.strip()
            if author in pluginAuthors:
                pluginAuthors[author].append(pluginName)
            else:
                pluginAuthors[author] = [pluginName]
        else:
            continue
    tmp = pluginAuthors.items()
    tmp.sort(key=lambda x: (-len(x[1]), x[0].lower()))
    authorList = []
    for author, pluginNames in tmp:
        pluginNames.sort(key=lambda s: s.lower())
        authorList.append((author, ",<BR>".join(pluginNames)))
    return authorList

def GetRam():
    memoryStatus = MEMORYSTATUSEX()
    memoryStatus.dwLength = sizeof(MEMORYSTATUSEX)
    GlobalMemoryStatusEx(byref(memoryStatus))
    return (
        round(memoryStatus.ullTotalPhys / 1024.0 / 1024 / 1024, 1),
        round(memoryStatus.ullAvailPhys / 1024.0 / 1024 / 1024, 1),
    )

def GetRegistryValue(key, value):
    key, subkey = key.split("\\", 1)
    handle = _winreg.OpenKey(getattr(_winreg, key), subkey)
    try:
        val = _winreg.QueryValueEx(handle, value)[0]
    except WindowsError, err:
        val = None
        if err[0] == 2:
            eg.PrintError("%s: %s" % (err[1].decode(eg.systemEncoding), value))
        else:
            raise
    return val

SPECIAL_THANKS_DATA = (
    ("Plugin Developers:", 2, GetPluginAuthors()),
    (
        "Translators:",
        2,
        (
            ("Pako", "Czech"),
            ("Fredrik Jacobsson", "Swedish"),
            ("karlr", "Spanish"),
            ("peter", "Dutch"),
            ("noc123", "Polish"),
            ("somainit", "Japanese"),
            ("PedroV9", "Portuguese (Brazilian)"),
            ("batto", "Vietnamese"),
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
            "specter333",          # 20. Jan 2008
            "Argofanatic",         # 24. Mar 2008
            "bskchaos",            #  8. Apr 2008
            "Warren Hatch",        # 26. Apr 2008
            "Daniel Henriksson",   #  3. May 2008
            "skyanchor",           # 13. May 2008
            "Vlad Skarzhevskyy",   # 13. Jun 2008
            "David Church",        # 17. Aug 2008
            "Tyson Ward",          # 30. Sep 2008
            "Glenn Maples",        # 13. Oct 2008
            "John Leonard",        # 21. Oct 2008
            "Silviu Marghescu",    # 26. Nov 2008
            "tireich",             # 05. Dec 2008
            "Sergio Herculano",    # 30. Dec 2008
            "Cassidy Caid",        # 13. Jan 2009
            "Beat Horn",           # 20. Jan 2009
            "Davin Roche",         # 11. Feb 2009
            "Nico Nordendorf",     # 16. Feb 2009
            "Mariusz Lon",         # 18. Feb 2009
            "Paul Tonkes",         # 22. Feb 2009
            "Ina Henderson",       # 05. May 2009
            "Kosta Krauth",        # 06. May 2009
            "Leandre da Silva",    # 15. May 2009
            "Franz Pentenrieder",  # 27. May 2009
            "David Grenker",       # 30. May 2009
            "Anthony Field",       # 09. Jun 2009
            "Nikhil Kapur",        # 16. Jun 2009
            "Tom Browning",        # 02. Jul 2009
            "Ludwig Strydom",      # 22. Jul 2009
            "Christoph Heins",     # 26. Aug 2009
            "Jeffrey Sonnabend",   #  2. Sep 2009
            "Stephen Evans",       #  6. Sep 2009
            "Sven Buerger",        #  9. Sep 2009
            "Erik Josefsson",      # 11. Nov 2009
            "Harry Hartenstine",   #  7. Dec 2009
            "Mathew Bentley",      #  8. Jan 2010
            "Jonas Ernst",         # 17. Jan 2010
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
                (
                    'Jonah Peskin, <a href="http://www.streamzap.com/">'
                    'Streamzap, Inc.</a>'
                ),
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
                    'for the nice <a href="http://www.eventghost.org/mediawiki/'
                    'Controlling%20your%20living%20room%20with%20EventGhost">'
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
