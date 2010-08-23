# plugins/OSE/__init__.py
#
# Copyright (C)  2010 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
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
#Last change: 2010-08-23 18:25 GMT+1

eg.RegisterPlugin(
    name = "On screen explorer",
    author = "Pako",
    version = "0.2.4",
    kind = "other",
    guid = "{D3D2DDD1-9BEB-4A26-969B-C82FA8EAB280}",
    description = u"""<rst>
Allows you to create custom On Screen Explorer.

Plugin OSE has built-in a function **"Stop processing this event"**,
if the menu **is shown** on the screen and **"Stop processing this macro"**,
if the menu **is not shown** on the screen.
This facilitates the use of OSE in your configuration.
You can use to control the menu the same events (the same remote buttons)
as elsewhere in the configuration, without having
to explicitly use the **"Stop processing this event"**,
**"Disable an item"** or **"Exclusive enable a folder / macro"**.
Only it is necessary to place the folder with the OSE as high
as possible in the configuration tree.""",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2194",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAADT7f+34f+s"
        "2v+n1/+r2P/F4//G5v/F5P/Z7v/e7//e7v/V6/+y1/+t0P/S7P/E5P/f7//Q6f/G5P/D"
        "4//J5f/a7f+nz/+z0/+13//Z7P/E4//C4v+/4P+63//C5P/b7v9+sv/d7v/A4f++4P+5"
        "3v+33f+x2v/s+/9inv+h0v+/4f+83/+43v+23P+y3P+u1//o+/9ZmP+l0f/R6f+03P+v"
        "2v/Y8v9onf/A3v+p0P/Y7P+u2f+r1v+33//S6v+Huv92eZ6hx/+Mv//Y8P/q+v/n+//X"
        "8f+JuP93o///rAC/VACrzP9yqP9Ukf9pnv+LmMj2kgD/4IHinwSqQwDWigDQgAD/1Hfg"
        "lgCvWgDGfwDHdgD/11OlSgDGigCrVQDUpy0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAApc2ZwLipQ"
        "AHNvdG9wb2guKig7ZGRzcC4qAClkZHBwLipQAGQoIEducC4qAClnbnByb1BsYmFhbSAq"
        "KCBtYnBwLioqO21tcHAuKgA7bWJncC4uKjsAbXAgSUdiLiouKjs7Ymdnci4qO2FpZ3Mu"
        "KgAqO3diZ3JyLio7YWJncy5hVAAgYWdpLioqO2JhZ3R2LioqO2F0c3Z3LioAKW5jaS4u"
        "Kjs7YWdkdi4uKjs7dHNpdy5JVAAoIEZ0Yi4uKjs7eGFmdC4uKjs7ZmlpdC4AKWZ0Yi4u"
        "Kjs7eGFmdC4uKjs7ZmlpdC4AAxAAACcKtAgAAAAwHV0Mh4gAAAAAAA8AAAEAAAAMDSAM"
        "DSAAAlxcOkRnb3JzbWFFXEV0bmVzb2hscFxuaWdTT1wAADQAAENCblQAAABBmj0AAAAA"
        "AAAAAAAAAAAAAAAAAAFCadMMDsgAAAAAAAEAAAAAAAAMDZQMDZQAAagAAADVqTzgAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAJBJREFUeNpjYMACGJmYWVjZ"
        "EHx2Dk4ubh5ePhifX0BQSFhEVExcAiogKSUkLSMrJ6+gCBVgUZJWVlFVU9fQhApoiWnr"
        "6OrpGxgaQQWMTaTVTNXNJM0toAKWVtayNrZ29g6OMGucnF1c3dw9PL28YSI+vkZ+/gGB"
        "QcEhKO4NDQuPiEQRiYqOiUX1U1x8AgMRAABAWxNIBjJyPwAAAABJRU5ErkJggg=="
    ),
)

import os
import wx.grid
import pythoncom
from threading import Timer
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import CreateEvent, SetEvent
import _winreg
from win32api import LoadLibrary, LoadString, GetLogicalDriveStrings, GetVolumeInformation
from win32com.shell import shell
from win32file import GetFileAttributes
from fnmatch import fnmatch
from winsound import PlaySound, SND_ASYNC

FO_DELETE = 3
FOF_ALLOWUNDO = 64
FOF_NOCONFIRMATION = 16
ERROR_ACCESS_DENIED  = 5
ERROR_NO_ASSOCIATION = 1155
FILE_ATTRIBUTE_READONLY = 1
FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_SYSTEM = 4
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)

#global variables:
folder_ID   = u">> "
shortcut_ID = u"|•"
#===============================================================================

class Text:
    noAssoc  = 'Error: No application is associated with the "%s" file type for operation "Open" !'
    accDeni  = 'The file or folder "%s" can not be deleted. Access denied.'
    myComp   = "My computer"
    folder   = "Folder identifier string (must not be empty):"
    shortcut = "Shortcut identifier string (may be empty):"
#===============================================================================

newEVT_BUTTON_AFTER = wx.NewEventType()
EVT_BUTTON_AFTER = wx.PyEventBinder(newEVT_BUTTON_AFTER, 1)


class EventAfter(wx.PyCommandEvent):

    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.myVal = None


    def SetValue(self, val):
        self.myVal = val


    def GetValue(self):
        return self.myVal
#===============================================================================

class extColourSelectButton(eg.ColourSelectButton):

    def __init__(self,*args,**kwargs):
        eg.ColourSelectButton.__init__(self, *args)
        self.title = kwargs['title']


    def OnButton(self, event):
        colourData = wx.ColourData()
        colourData.SetChooseFull(True)
        colourData.SetColour(self.value)
        for i, colour in enumerate(eg.config.colourPickerCustomColours):
            colourData.SetCustomColour(i, colour)
        dialog = wx.ColourDialog(self.GetParent(), colourData)
        dialog.SetTitle(self.title)
        if dialog.ShowModal() == wx.ID_OK:
            colourData = dialog.GetColourData()
            self.SetValue(colourData.GetColour().Get())
            event.Skip()
        eg.config.colourPickerCustomColours = [
            colourData.GetCustomColour(i).Get() for i in range(16)
        ]
        dialog.Destroy()
        evt = EventAfter(newEVT_BUTTON_AFTER, self.GetId())
        evt.SetValue(self.GetValue())
        self.GetEventHandler().ProcessEvent(evt)
#===============================================================================

class extFontSelectButton(eg.FontSelectButton):

    def OnButton(self, event):
        fontData = wx.FontData()
        if self.value is not None:
            font = wx.FontFromNativeInfoString(self.value)
            fontData.SetInitialFont(font)
        else:
            fontData.SetInitialFont(
                wx.SystemSettings_GetFont(wx.SYS_ANSI_VAR_FONT)
            )
        dialog = wx.FontDialog(self.GetParent(), fontData)
        if dialog.ShowModal() == wx.ID_OK:
            fontData = dialog.GetFontData()
            font = fontData.GetChosenFont()
            self.value = font.GetNativeFontInfo().ToString()
            event.Skip()
        dialog.Destroy()
        evt = EventAfter(newEVT_BUTTON_AFTER, self.GetId())
        evt.SetValue(self.GetValue())
        self.GetEventHandler().ProcessEvent(evt)
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):

    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!


    def SetStartDirectory(self):
        self.startDirectory = self.GetValue()
#===============================================================================

class MenuGrid(wx.grid.Grid):

    def __init__(self, parent, lngth):
        wx.grid.Grid.__init__(self, parent)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetDefaultRowSize(16)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.EnableEditing(False)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.EnableGridLines(False)
        attr = wx.grid.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0,attr)
        self.CreateGrid(lngth, 1)
        self.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.onGridSelectCell, self)


    def SetBackgroundColour(self, colour):
        self.SetDefaultCellBackgroundColour(colour)


    def SetForegroundColour(self, colour):
        self.SetDefaultCellTextColour(colour)


    def SetFont(self, font):
        self.SetDefaultCellFont(font)


    def Set(self, choices):
        oldLen = self.GetNumberRows()
        newLen = len(choices)
        h = self.GetDefaultRowSize()
        if oldLen > newLen:
            self.DeleteRows(0, oldLen-newLen, False)
        elif oldLen < newLen:
            self.AppendRows(newLen-oldLen, False)
        for i in range(len(choices)):
            self.SetCellValue(i,0,choices[i])
            self.SetRowSize(i,h)


    def onGridSelectCell(self, event):
        row = event.GetRow()
        self.SelectRow(row)
        if not self.IsVisible(row,0):
            self.MakeCellVisible(row,0)
        event.Skip()


    def MoveCursor(self, step):
        max = self.GetNumberRows()
        sel = self.GetSelectedRows()[0]
        new = sel + step
        if new < 0:
            new += max
        elif new > max-1:
            new -= max
        self.SetGridCursor(new, 0)
        self.SelectRow(new)
#===============================================================================

def CaseInsensitiveSort(list):
    tmp = [(item[0].upper(), item) for item in list] # Schwartzian transform
    tmp.sort()
    return [item[1] for item in tmp]


def GetFolderItems(folder, patterns, hide):
    shortcut = pythoncom.CoCreateInstance (
      shell.CLSID_ShellLink,
      None,
      pythoncom.CLSCTX_INPROC_SERVER,
      shell.IID_IShellLink
    )
    persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
    patterns = patterns.split(",")
    if folder != MY_COMPUTER:
        ds = []
        for f in [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder,f))]:
            if hide:
                attr = GetFileAttributes(os.path.join(folder,f))
                if attr & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                    continue
            ds.append(("%s%s" % (folder_ID,f),""))
        fs = [("..",""),]
        for f in [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]:
            if os.path.splitext(f)[1].lower() == ".lnk":
                shortcut_path = os.path.join(folder,f)
                persist_file.Load (shortcut_path)
                path = shortcut.GetPath(shell.SLGP_RAWPATH)[0]
                f = os.path.split(shortcut_path)[1][:-4]
                if hide:
                    attr = GetFileAttributes(path)
                    if attr & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                        continue
                if os.path.isdir(path):
                    if not "%s%s" % (folder_ID,f) in ds:
                        ds.append(("%s%s%s " % (shortcut_ID,folder_ID,f),path))
                        continue
                elif os.path.isfile(path):
                    for p in patterns:
                        if fnmatch(os.path.split(path)[1],p.strip()):
                            if not shortcut_ID+f in fs:
                                fs.append((shortcut_ID+f,path))
                            break
            else:
                if hide:
                    attr = GetFileAttributes(os.path.join(folder,f))
                    if attr & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                        continue
                for p in patterns:
                    if fnmatch(f,p.strip()):
                        if not f in fs:
                            fs.append((f,""))
                        break
        ds = CaseInsensitiveSort(ds)
        fs = CaseInsensitiveSort(fs)
        fs.extend(ds)
        return fs
    else: #pseudo-folder "My computer"
        drives = GetLogicalDriveStrings().split('\000')[:-1]
        drvs = []
        for dr in drives:
            try:
               name = GetVolumeInformation(dr)[0]
               drvs.append(("%s%s (%s)" % (folder_ID,name,dr[:2]),""))
            except:
                pass
        return drvs

#===============================================================================
#cls types for ACTIONS list :
#===============================================================================

class ShowMenu(eg.ActionClass):
    panel = None

    class text:
        OSELabel = 'OSE show on:'
        menuPreview = 'On screen explorer preview:'
        menuFont = 'Font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        prefixLabel = 'Event prefix:'
        suffixLabel = 'Default event suffix:'
        folder = "Start folder:"
        browseTitle = "Selected folder:"
        hide = "Do not display system and hidden files and folders"
        toolTipFolder = "Press button and browse to select folder ..."
        patterns = "Show only the files corresponding to these patterns:"
        compBtnToolTip = 'Press this button to set "%s" as start folder'
        patternsToolTip = '''Here you can enter the patterns of required files, separated by commas.
For example, *.mp3, *.ogg, *.flac or e*.ppt, g*.ppt and the like.'''


    def __call__(
        self,
        fore,
        back,
        fontInfo,
        prefix,
        suffix,
        monitor=0,
        start = "",
        patterns = "*.*",
        hide = True,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75)
    ):
        if not self.plugin.menuDlg:
            if not os.path.isdir(start) and start != MY_COMPUTER:
                start = eg.folderPath.Documents
            self.plugin.menuDlg = Menu()
            self.event = CreateEvent(None, 0, 0, None)
            wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                fore,
                back,
                foreSel,
                backSel,
                fontInfo,
                False,
                self.plugin,
                self.event,
                prefix,
                suffix,
                monitor,
                start,
                patterns,
                hide
            )
            eg.actionThread.WaitOnEvent(self.event)


    def GetLabel(
        self,
        fore,
        back,
        fontInfo,
        prefix,
        suffix,
        monitor,
        start,
        patterns,
        hide,
        foreSel,
        backSel
    ):
        return "%s: %s, [%s]" % (self.name,start,patterns)


    def Configure(
        self,
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = None,
        prefix = 'OSE',
        suffix = 'Open',
        monitor = 0,
        start = "",
        patterns = "*.*",
        hide = True,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75)
    ):
        self.fore = fore
        self.back = back
        self.foreSel = foreSel
        self.backSel = backSel
        self.oldSel=0
        global panel
        panel = eg.ConfigPanel(self)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        listBoxCtrl = MenuGrid(panel, 1)
        listBoxCtrl.SetMinSize(wx.Size(160, 439))
        listBoxCtrl.SetMaxSize(wx.Size(160, 439))
        if not patterns:
            patterns = "*.*"
        if not os.path.isdir(start) and start != MY_COMPUTER:
            start = eg.folderPath.Documents
        items = [item[0] for item in GetFolderItems(start, patterns, hide)]
        listBoxCtrl.Set(items)
        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        listBoxCtrl.SetSelectionBackground(self.backSel)
        listBoxCtrl.SetSelectionForeground(self.foreSel)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = extFontSelectButton(panel, value = fontInfo)
        if fontInfo is None:
            font = listBoxCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            fontButton.SetFont(font)
            hght = fontButton.GetTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        listBoxCtrl.SetDefaultRowSize(hght+4, True)
        displayChoice = eg.DisplayChoice(panel, monitor)
        w = displayChoice.GetSize()[0]
        prefixLbl=wx.StaticText(panel, -1, self.text.prefixLabel)
        prefixCtrl = wx.TextCtrl(panel,-1,prefix,size=wx.Size(w,-1))
        suffixLbl=wx.StaticText(panel, -1, self.text.suffixLabel)
        suffixCtrl = wx.TextCtrl(panel,-1,suffix,size=wx.Size(w,-1))
        OSElbl = wx.StaticText(panel, -1, self.text.OSELabel)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = extColourSelectButton(panel, fore, title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = extColourSelectButton(panel,back, title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = extColourSelectButton(panel,foreSel, title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = extColourSelectButton(panel,backSel, title = self.text.backgroundSel)
        folderLabel = wx.StaticText(panel, -1, self.text.folder)
        folderCtrl = MyDirBrowseButton(
            panel, 
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse,
        )
        compBtn = wx.Button(panel, -1, MY_COMPUTER)
        compBtn.SetToolTip(wx.ToolTip(self.text.compBtnToolTip % MY_COMPUTER))
        folderCtrl.GetTextCtrl().SetEditable(False)
        folderCtrl.SetValue(start)
        folderCtrl.SetStartDirectory()
        patternsLabel = wx.StaticText(panel, -1, self.text.patterns)
        patternsCtrl = wx.TextCtrl(panel,-1,patterns)
        patternsCtrl.SetToolTip(wx.ToolTip(self.text.patternsToolTip))
        hideSystem = wx.CheckBox(panel, -1, self.text.hide)
        hideSystem.SetValue(hide)
        #Sizers
        mainSizer = panel.sizer
        topSizer=wx.GridBagSizer(2, 30)
        mainSizer.Add(topSizer)
        topSizer.Add(previewLbl,(0, 0),flag = wx.TOP,border = 0)
        topSizer.Add(listBoxCtrl,(1, 0),(9, 1),flag = wx.EXPAND)
        topSizer.Add(fontLbl,(0, 1),flag = wx.TOP,border = 0)
        topSizer.Add(fontButton,(1, 1),flag = wx.TOP)
        topSizer.Add(foreLbl,(2, 1),flag = wx.TOP,border = 8)
        topSizer.Add(foreColourButton,(3, 1),flag = wx.TOP)
        topSizer.Add(backLbl,(4, 1),flag = wx.TOP,border = 8)
        topSizer.Add(backColourButton,(5, 1),flag = wx.TOP,border = 0)
        topSizer.Add(prefixLbl,(0, 2),flag = wx.TOP,border = 0)
        topSizer.Add(prefixCtrl,(1, 2))
        topSizer.Add(suffixLbl,(2, 2),flag = wx.TOP,border = 8)
        topSizer.Add(suffixCtrl, (3, 2))
        topSizer.Add(OSElbl,(4, 2), flag = wx.TOP,border = 8)
        topSizer.Add(displayChoice,(5, 2))
        topSizer.Add(foreSelLbl,(6, 1), (1, 2), flag = wx.TOP,border = 8)
        topSizer.Add(foreSelColourButton, (7, 1), flag = wx.TOP)
        topSizer.Add(backSelLbl,(8, 1), (1, 2), flag = wx.TOP,border = 8)
        topSizer.Add(backSelColourButton, (9, 1), flag = wx.TOP,border = 0)
        mainSizer.Add(folderLabel,0,wx.TOP,8)
        folderSizer = wx.BoxSizer(wx.HORIZONTAL)
        folderSizer.Add(folderCtrl,1,wx.EXPAND)
        folderSizer.Add(compBtn,0,wx.LEFT,20)
        mainSizer.Add(folderSizer,0,wx.TOP|wx.EXPAND,2)
        mainSizer.Add(patternsLabel,0,wx.TOP,8)
        mainSizer.Add(patternsCtrl,1,wx.TOP|wx.EXPAND,2)
        mainSizer.Add(hideSystem,0,wx.TOP,10)
        panel.sizer.Layout()
        wdth = 160
        if (hght+4)*listBoxCtrl.GetNumberRows() > listBoxCtrl.GetSize()[1]: #after Layout() !!!
            wdth -=  SYS_VSCROLL_X
        listBoxCtrl.SetColSize(0, wdth)


        def OnFontBtn(evt):
            value = evt.GetValue()
            font = wx.FontFromNativeInfoString(value)
            for n in range(10,20):
                font.SetPointSize(n)
                fontButton.SetFont(font)
                hght = fontButton.GetTextExtent('X')[1]
                if hght > 20:
                    break
            listBoxCtrl.SetDefaultCellFont(font)
            listBoxCtrl.SetDefaultRowSize(hght+4, True)
            for i in range(listBoxCtrl.GetNumberRows()):
                listBoxCtrl.SetCellFont(i,0,font)
            listBoxCtrl.SetFocus()
            evt.Skip()
        fontButton.Bind(EVT_BUTTON_AFTER, OnFontBtn)


        def OnColourBtn(evt):
            id = evt.GetId()
            value = evt.GetValue()
            if id == foreColourButton.GetId():
                listBoxCtrl.SetForegroundColour(value)
            elif id == backColourButton.GetId():
                listBoxCtrl.SetBackgroundColour(value)
            elif id == foreSelColourButton.GetId():
                listBoxCtrl.SetSelectionForeground(value)
            elif id == backSelColourButton.GetId():
                listBoxCtrl.SetSelectionBackground(value)
            listBoxCtrl.Refresh()
            listBoxCtrl.SetFocus()
            evt.Skip()
        foreColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        foreSelColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backSelColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)


        def OnCompBtn(evt):
            folderCtrl.SetValue(MY_COMPUTER)
            evt.Skip()
        compBtn.Bind(wx.EVT_BUTTON, OnCompBtn)


        def OnTextChange(evt):
            folder = folderCtrl.GetValue()
            patterns = patternsCtrl.GetValue()
            hide = hideSystem.GetValue()
            if not patterns:
                patterns = "*.*"
            if folder:
                folderCtrl.SetStartDirectory()
                try:
                    items = [item[0] for item in GetFolderItems(folder, patterns, hide)]
                    listBoxCtrl.Set(items)
                except:
                    pass
            evt.Skip()
        folderCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        patternsCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        hideSystem.Bind(wx.EVT_CHECKBOX, OnTextChange)


        # re-assign the test button
        def OnButton(event):
            if not self.plugin.menuDlg:
                self.plugin.menuDlg = Menu()
                self.event = CreateEvent(None, 0, 0, None)
                wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                    foreColourButton.GetValue(),
                    backColourButton.GetValue(),
                    foreSelColourButton.GetValue(),
                    backSelColourButton.GetValue(),
                    fontButton.GetValue(), 
                    True,
                    self.plugin,
                    self.event,
                    prefixCtrl.GetValue(),
                    suffixCtrl.GetValue(),
                    displayChoice.GetSelection(),
                    folderCtrl.GetValue(),
                    patternsCtrl.GetValue(),
                    hideSystem.GetValue()
                )
                eg.actionThread.WaitOnEvent(self.event)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            fontInfo = fontButton.GetValue()
            if not fontInfo:
                font = listBoxCtrl.GetFont()
                font.SetPointSize(36)
                fontInfo = font.GetNativeFontInfoDesc()
            panel.SetResult(
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontInfo,
            prefixCtrl.GetValue(),
            suffixCtrl.GetValue(),
            displayChoice.GetSelection(),
            folderCtrl.GetValue(),
            patternsCtrl.GetValue(),
            hideSystem.GetValue(),
            foreSelColourButton.GetValue(),
            backSelColourButton.GetValue(),
        )
#===============================================================================

class MoveCursor(eg.ActionClass):

    class text:
        step = "Step size:"


    def __call__(self, step = 1):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.MoveCursor(step * self.value)
            eg.event.skipEvent = True


    def Configure(self, step = 1):
        panel = eg.ConfigPanel(self)
        stepCtrl = panel.SpinIntCtrl(step, min=1, max=25)
        panel.AddLine(self.text.step, stepCtrl)
        while panel.Affirmed():
            panel.SetResult(
                stepCtrl.GetValue(),
                )
#===============================================================================

class PageUpDown(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.PageUpDown(self.value)
            eg.event.skipEvent = True
#===============================================================================

class Cancel(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.destroyMenu()
            self.plugin.menuDlg = None
            eg.event.skipEvent = True
#===============================================================================

class Execute (eg.ActionClass):

    class text:
        fileBoxLabel   = "Action with the file"
        folderBoxLabel = "Action with the folder"
        returnFile     = "Return path to the file as eg.result"
        openFile       = "Open the file in associated application"
        deleteFile     = "Delete the file"
        deleteFolder     = "Delete the folder"
        goIntoFolder   = "Go into that folder"
        returnFolder   = "Return path to this folder as eg.result"
        fileSuffix     = "Trigger event with this suffix:"
        folderSuffix   = "Suffix for folder events:"
        triggerEvent   = "Trigger event, carried path to this folder as payload"
        retContents    = "Return the contents of this folder (only files, no folders) as eg.result"
        triggerEvent2  = "Trigger event, carried contents of this folder (only files, no folders) as payload"

    def __call__(self, val = 22, fileSuff = "", folderSuff = ""):
        if self.plugin.menuDlg:
            eg.event.skipEvent = True
            filePath, prefix, suffix = self.plugin.menuDlg.GetInfo()
            filePath = filePath.replace(folder_ID,"")
            if filePath[-2] == ":": #root of drive
                filePath = filePath[-3:-1]+"\\"
            if os.path.isfile(filePath):
                if val&1: #trigger event
                    if fileSuff:
                        suffix = fileSuff
                    eg.TriggerEvent(prefix = prefix, suffix = suffix, payload = filePath)
                if val&2: #open in associated
                    try:
                        os.startfile(filePath)
                    except WindowsError, e:
                        if e.winerror == ERROR_NO_ASSOCIATION:
                            eg.PrintError(self.plugin.text.noAssoc % os.path.splitext(filePath)[1])
                        else:
                            raise
                if val&256: #delete file
                    if GetFileAttributes(filePath) & FILE_ATTRIBUTE_READONLY:
                        eg.PrintError(self.plugin.text.accDeni % filePath)
                    else:
                        try:
                            shell.SHFileOperation((0, FO_DELETE, filePath, None,
                            FOF_ALLOWUNDO|FOF_NOCONFIRMATION))
                        except WindowsError, e:
                            if e.winerror == ERROR_ACCESS_DENIED:
                                eg.PrintError(self.plugin.text.accDeni % filePath)
                            else:
                                raise
                self.plugin.menuDlg.destroyMenu()
                self.plugin.menuDlg = None
                if val&4: #return
                    return filePath
                #else:
                #    eg.programCounter = None
            elif os.path.isdir(filePath):
                if filePath[-3:] == r"\..":
                    if len(filePath) == 5:
                        filePath = MY_COMPUTER
                    else:
                        filePath = os.path.split(filePath[:-3])[0]
                if val&(64+128):
                    items = self.plugin.menuDlg.GetItemsFolder(filePath)
                    fpList = []
                    for sel in range(len(items)):
                        fp = unicode(items[sel][1].decode(eg.systemEncoding))
                        if not fp:
                            fp = items[sel][0]

                            #if fp == '..':
                            #    continue

                            fp = fp.replace(folder_ID,"")
                            fp = os.path.join(filePath, fp)
                            if fp[-2] == ":": #root of drive
                                fp = fp[-3:-1]+"\\"
                        if os.path.isfile(fp):
                            fpList.append(fp)
                if folderSuff:
                    suffix = folderSuff
                if val&8: #trigger event
                    eg.TriggerEvent(prefix = prefix, suffix = suffix, payload = filePath)
                if val&64:
                    eg.TriggerEvent(prefix = prefix, suffix = suffix, payload = fpList)
                if val&512: #delete file
                    if GetFileAttributes(filePath) & FILE_ATTRIBUTE_READONLY:
                        eg.PrintError(self.plugin.text.accDeni % filePath)
                    else:
                        try:
                            shell.SHFileOperation((0, FO_DELETE, filePath, None,
                            FOF_ALLOWUNDO|FOF_NOCONFIRMATION))
                        except WindowsError, e:
                            if e.winerror == ERROR_ACCESS_DENIED:
                                eg.PrintError(self.plugin.text.accDeni % filePath)
                            else:
                                raise
                if val&16: #go to the folder
                    event = CreateEvent(None, 0, 0, None)
                    wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                        prefix = prefix,
                        suffix = suffix,
                        start = filePath,
                        event = event,
                    )
                    eg.actionThread.WaitOnEvent(event)
                else:
                    self.plugin.menuDlg.destroyMenu()
                    self.plugin.menuDlg = None
                res = None
                if val&32: #return
                    res = filePath
                if val&128: #return
                    res = fpList
                if res:
                    return res
        elif val&(4+32+128):
            eg.programCounter = None


    def GetLabel(self,val, fileSuff, folderSuff):
        return "%s: %i, %s, %s" % (self.name,val, fileSuff, folderSuff)


    def Configure(self, val = 22, fileSuff = "", folderSuff = ""):
        panel = eg.ConfigPanel(self)
        triggFileCheck = wx.CheckBox(panel, -1, self.text.fileSuffix)
        triggFileCheck.SetValue(val&1)
        openFileCheck = wx.CheckBox(panel, -1, self.text.openFile)
        openFileCheck.SetValue(val&2)
        deleteFileCheck = wx.CheckBox(panel, -1, self.text.deleteFile)
        deleteFileCheck.SetValue(val&256)
        deleteFolderCheck = wx.CheckBox(panel, -1, self.text.deleteFolder)
        deleteFolderCheck.SetValue(val&512)
        retFileCheck = wx.CheckBox(panel, -1, self.text.returnFile)
        retFileCheck.SetValue(val&4)
        folderSuffLabel = wx.StaticText(panel, -1, self.text.folderSuffix)
        triggFolderCheck = wx.CheckBox(panel, -1, self.text.triggerEvent)
        triggFolderCheck.SetValue(val&8)
        goFolderCheck = wx.CheckBox(panel, -1, self.text.goIntoFolder)
        goFolderCheck.SetValue(val&16)
        retFolderCheck = wx.CheckBox(panel, -1, self.text.returnFolder)
        retFolderCheck.SetValue(val&32)
        triggFolderCheck2 = wx.CheckBox(panel, -1, self.text.triggerEvent2)
        triggFolderCheck2.SetValue(val&64)
        retFolderCheck2 = wx.CheckBox(panel, -1, self.text.retContents)
        retFolderCheck2.SetValue(val&128)
        suffixFile = wx.TextCtrl(panel,-1,fileSuff,size=wx.Size(80,-1))
        suffixFolder = wx.TextCtrl(panel,-1,folderSuff,size=wx.Size(80,-1))
        #Sizers
        mainSizer = panel.sizer
        fileSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.fileBoxLabel),
            wx.VERTICAL
        )
        fileSuffSizer = wx.BoxSizer(wx.HORIZONTAL)
        folderSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.folderBoxLabel),
            wx.VERTICAL
        )
        fileSuffSizer.Add(triggFileCheck,0,wx.RIGHT,5)
        fileSuffSizer.Add(suffixFile,0,wx.TOP,-4)
        folderSuffSizer = wx.BoxSizer(wx.HORIZONTAL)
        folderSuffSizer.Add(folderSuffLabel,0,wx.RIGHT,5)
        folderSuffSizer.Add(suffixFolder,0,wx.TOP,-4)
        fileSizer.Add(fileSuffSizer,0,wx.TOP,4)
        fileSizer.Add(openFileCheck,0,wx.TOP,6)
        fileSizer.Add(deleteFileCheck,0,wx.TOP,6)
        fileSizer.Add(retFileCheck,0,wx.TOP,8)
        folderSizer.Add(folderSuffSizer,0,wx.TOP,4)
        folderSizer.Add(triggFolderCheck,0,wx.TOP,6)
        folderSizer.Add(triggFolderCheck2,0,wx.TOP,8)
        folderSizer.Add(deleteFolderCheck,0,wx.TOP,6)
        folderSizer.Add(retFolderCheck,0,wx.TOP,8)
        folderSizer.Add(retFolderCheck2,0,wx.TOP,8)
        folderSizer.Add(goFolderCheck,0,wx.TOP,8)
        mainSizer.Add(fileSizer,0)
        mainSizer.Add(folderSizer,0,wx.TOP,20)

        def EnableGo2Folder(evt = None):
            val0 = not triggFolderCheck.GetValue()
            val1 = not triggFolderCheck2.GetValue()
            val2 = not retFolderCheck.GetValue()
            val3 = not retFolderCheck2.GetValue()
            val4 = not deleteFolderCheck.GetValue()
            goFolderCheck.Enable(val0 and val1 and val2 and val3 and val4)
            if evt:
                evt.Skip()

        def onGoFolderCheck(evt = None):
            val = goFolderCheck.GetValue()
            retFolderCheck.Enable(not val)
            retFolderCheck2.Enable(not val)
            triggFolderCheck.Enable(not val)
            triggFolderCheck2.Enable(not val)
            deleteFolderCheck.Enable(not val)
            if evt:
                evt.Skip()
        onGoFolderCheck()

        def onTriggFolderCheck(evt = None):
            val = triggFolderCheck.GetValue()
            triggFolderCheck2.Enable(not val)
            EnableGo2Folder()
            if evt:
                evt.Skip()
        onTriggFolderCheck()

        def onTriggFolderCheck2(evt = None):
            val = triggFolderCheck2.GetValue()
            triggFolderCheck.Enable(not val)
            EnableGo2Folder()
            if evt:
                evt.Skip()
        onTriggFolderCheck2()

        def onRetFolderCheck(evt = None):
            val = retFolderCheck.GetValue()
            retFolderCheck2.Enable(not val)
            EnableGo2Folder()
            if evt:
                evt.Skip()
        onRetFolderCheck()

        def onRetFolderCheck2(evt = None):
            val = retFolderCheck2.GetValue()
            retFolderCheck.Enable(not val)
            EnableGo2Folder()
            if evt:
                evt.Skip()
        onRetFolderCheck2()

        def onOpenFileCheck(evt = None):
            val = openFileCheck.GetValue()
            deleteFileCheck.Enable(not val)
            if evt:
                evt.Skip()
        onOpenFileCheck()

        def onDeleteFileCheck(evt = None):
            val = deleteFileCheck.GetValue()
            openFileCheck.Enable(not val)
            if evt:
                evt.Skip()
        onDeleteFileCheck()

        EnableGo2Folder()

        triggFolderCheck.Bind(wx.EVT_CHECKBOX, onTriggFolderCheck)
        triggFolderCheck2.Bind(wx.EVT_CHECKBOX, onTriggFolderCheck2)
        retFolderCheck.Bind(wx.EVT_CHECKBOX, onRetFolderCheck)
        retFolderCheck2.Bind(wx.EVT_CHECKBOX, onRetFolderCheck2)
        goFolderCheck.Bind(wx.EVT_CHECKBOX, onGoFolderCheck)
        openFileCheck.Bind(wx.EVT_CHECKBOX, onOpenFileCheck)
        deleteFileCheck.Bind(wx.EVT_CHECKBOX, onDeleteFileCheck)
        deleteFolderCheck.Bind(wx.EVT_CHECKBOX, EnableGo2Folder)

        while panel.Affirmed():
            val  =      triggFileCheck.GetValue()
            val += 2  * openFileCheck.GetValue()
            val += 4  * retFileCheck.GetValue()
            val += 8  * triggFolderCheck.GetValue()
            val += 16 * goFolderCheck.GetValue()
            val += 32 * retFolderCheck.GetValue()
            val += 64  * triggFolderCheck2.GetValue()
            val += 128 * retFolderCheck2.GetValue()
            val += 256  * deleteFileCheck.GetValue()
            val += 512  * deleteFolderCheck.GetValue()
            panel.SetResult(val,
                suffixFile.GetValue(),
                suffixFolder.GetValue()
                )
#===============================================================================

ACTIONS = (
    (ShowMenu, 'ShowMenu', 'Show explorer', 'Show on screen explorer.', None),
    (MoveCursor, 'MoveUp', 'Cursor Up', 'Cursor Up.', -1),
    (MoveCursor, 'MoveDown', 'Cursor Down', 'Cursor Down.', 1),
    (PageUpDown, 'PageUp', 'Page Up', 'Page Up.', -1),
    (PageUpDown, 'PageDown', 'Page Down', 'Page Down.', 1),
    (Execute, 'Execute', 'Execute', 'Execute.', None),
    (Cancel, 'Cancel', 'Cancel', 'Cancel button pressed.', None),
)
#===============================================================================

class OSE(eg.PluginClass):
    menuDlg = None
    text=Text


    def MyComputer(self):
        mc_reg = None
        try:
            mc_reg = _winreg.OpenKey(
                _winreg.HKEY_CLASSES_ROOT,
                "CLSID\\{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
            )
            value, type = _winreg.QueryValueEx(mc_reg, "LocalizedString")
            dll = os.path.split(value.split(",")[0][1:])[1]
            index = -1*int(value.split(",")[1])
            myComputer = LoadString(LoadLibrary(dll), index)
        except:
            myComputer = self.text.myComp
        if mc_reg:
            _winreg.CloseKey(mc_reg)
        return myComputer


    def __init__(self):
        global MY_COMPUTER
        MY_COMPUTER = self.MyComputer()
        self.AddActionsFromList(ACTIONS)


    def __start__(self, fid = u">> ", sid = u"|•"):
        global shortcut_ID, folder_ID
        shortcut_ID = sid
        folder_ID = fid


    def Configure(self, fid = u">> ", sid = u"|•"):
        self.text = Text
        panel = eg.ConfigPanel(self)
        folderLabel = wx.StaticText(panel, -1, self.text.folder)
        shortcutLabel = wx.StaticText(panel, -1, self.text.shortcut)
        folderCtrl = wx.TextCtrl(panel,-1,fid)
        shortcutCtrl = wx.TextCtrl(panel,-1,sid)
        Sizer = panel.sizer
        Sizer.Add(folderLabel,0,wx.TOP,15)
        Sizer.Add(folderCtrl,0,wx.TOP,2)
        Sizer.Add(shortcutLabel,0,wx.TOP,15)
        Sizer.Add(shortcutCtrl,0,wx.TOP,2)
        while panel.Affirmed():
            panel.SetResult(
                folderCtrl.GetValue() or u">> ",
                shortcutCtrl.GetValue(),
                )
#===============================================================================

class Menu(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'OS_Explorer',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )
        self.flag = False
        self.monitor = 0
        self.prefix = "OSE"
        self.suffix = "Open"
        self.patterns = "*.*"
        self.hide = False


    def ShowMenu(
        self,
        fore=None,
        back=None,
        foreSel=None,
        backSel=None,
        fontInfo=None,
        flag=None,
        plugin=None,
        event=None,
        prefix=None,
        suffix=None,
        monitor=None,
        start=None,
        patterns=None,
        hide = None
    ):
        self.fore     = fore or self.fore
        self.back     = back or self.back
        self.foreSel  = foreSel or self.foreSel
        self.backSel  = backSel or self.backSel
        self.fontInfo = fontInfo or self.fontInfo
        self.flag     = flag or self.flag
        self.plugin   = plugin or self.plugin
        self.prefix   = prefix or self.prefix
        self.suffix   = suffix or self.suffix
        self.monitor  = monitor or self.monitor
        self.patterns = patterns or self.patterns
        self.hide     = hide or self.hide
        try:
            items  = GetFolderItems(start, self.patterns, self.hide)
            self.start = start
        except:
            PlaySound('SystemExclamation', SND_ASYNC)
            items  = GetFolderItems(self.start, self.patterns, self.hide)
        self.choices = [item[0] for item in items]
        self.shortcuts = [item[1] for item in items]
        sizer = self.GetSizer()
        if sizer:
            self.eventChoiceCtrl.Set(self.choices)
        else:
            self.eventChoiceCtrl = MenuGrid(self,len(self.choices))
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(mainSizer)
            mainSizer.Add(self.eventChoiceCtrl, 0, wx.EXPAND)
            self.Bind(wx.EVT_CLOSE, self.onClose)
            self.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.onDoubleClick, self.eventChoiceCtrl)
            self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
            font = wx.FontFromNativeInfoString(fontInfo)
            self.eventChoiceCtrl.SetFont(font)
            self.SetFont(font)
            self.SetBackgroundColour((0, 0, 0))
            self.eventChoiceCtrl.SetBackgroundColour(self.back)
            self.eventChoiceCtrl.SetForegroundColour(self.fore)
            self.eventChoiceCtrl.SetSelectionBackground(self.backSel)
            self.eventChoiceCtrl.SetSelectionForeground(self.foreSel)
            if self.flag:
                self.timer=MyTimer(t = 5.0, plugin = self.plugin)
        self.eventChoiceCtrl.SetGridCursor(0, 0)
        self.eventChoiceCtrl.SelectRow(0)
        monDim = GetMonitorDimensions()
        try:
            x,y,ws,hs = monDim[self.monitor]
        except IndexError:
            x,y,ws,hs = monDim[0]
        # menu height calculation:
        h=self.GetCharHeight()+4
        for i in range(len(self.choices)):
            self.eventChoiceCtrl.SetCellValue(i,0,self.choices[i])
            self.eventChoiceCtrl.SetRowSize(i,h)
        height0 = len(self.choices)*h
        height1 = h*((hs-20)/h)
        height = min(height0, height1)+6
        # menu width calculation:
        width_lst=[]
        for item in self.choices:
            width_lst.append(self.GetTextExtent(item+' ')[0])
        width = max(width_lst)+8
        self.eventChoiceCtrl.SetColSize(0,width)
        if height1 < height0:
            width += SYS_VSCROLL_X
        width = min((width,ws-50))+6
        x_pos = x+(ws-width)/2
        y_pos = y + (hs-height)/2
        self.SetDimensions(x_pos,y_pos,width,height)
        self.eventChoiceCtrl.SetDimensions(2,2,width-6,height-6,wx.SIZE_AUTO)
        self.Show(True)
        self.Raise()
        if event:
            wx.Yield()
            SetEvent(event)


    def GetInfo(self):
        sel = self.GetSizer().GetChildren()[0].GetWindow().GetSelectedRows()[0]
        fp = unicode(self.shortcuts[sel].decode(eg.systemEncoding))
        if not fp:
            fp = os.path.join(self.start,self.choices[sel])
        return fp, self.prefix, self.suffix


    def GetItemsFolder(self, fp):
        return GetFolderItems(fp, self.patterns, self.hide)


    def MoveCursor(self, step):
        max=len(self.choices)
        if max > 0:
            self.eventChoiceCtrl.MoveCursor(step)


    def PageUpDown(self, direction):
        max=len(self.choices)
        if max > 0:
            if direction > 0:
                self.eventChoiceCtrl.MovePageDown()
            else:
                self.eventChoiceCtrl.MovePageUp()


    def DefaultAction(self):
        sel = self.eventChoiceCtrl.GetSelectedRows()[0]
        filePath = unicode(self.shortcuts[sel].decode(eg.systemEncoding))
        if not filePath:
            filePath = os.path.join(self.start,self.choices[sel])
            filePath = filePath.replace(folder_ID,"")
            if filePath[-2] == ":": #root of drive
                filePath = filePath[-3:-1]+"\\"
            if filePath[-3:] == r"\..":
                if len(filePath) == 5:
                    filePath = MY_COMPUTER
                else:
                    filePath = os.path.split(filePath[:-3])[0]
        eg.TriggerEvent(prefix = self.prefix, suffix = self.suffix, payload = filePath)
        if os.path.isfile(filePath):
            self.destroyMenu()
            self.plugin.menuDlg = None
            try:
                os.startfile(filePath)
            except WindowsError, e:
                if e.winerror == ERROR_NO_ASSOCIATION:
                    eg. Error(self.plugin.text.noAssoc % os.path.splitext(filePath)[1])
                else:
                    raise
        else:
            self.ShowMenu(
                prefix = self.prefix,
                suffix = self.suffix,
                start = filePath,
            )


    def onFrameCharHook(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_RETURN or keyCode == wx.WXK_NUMPAD_ENTER:
            self.DefaultAction()
        elif keyCode == wx.WXK_ESCAPE:
            self.Close()
        elif keyCode == wx.WXK_UP or keyCode == wx.WXK_NUMPAD_UP:
            self.eventChoiceCtrl.MoveCursor(-1)
        elif keyCode == wx.WXK_DOWN or keyCode == wx.WXK_NUMPAD_DOWN:
            self.eventChoiceCtrl.MoveCursor(1)
        else:
            event.Skip()


    def onDoubleClick(self, event):
        self.DefaultAction()
        event.Skip()


    def onClose(self, event):
        self.Destroy()


    def destroyMenu(self):
        if self.flag:
            self.timer.Cancel()
        self.Show(False)
        self.Close()
#===============================================================================

class MyTimer():

    def __init__(self, t, plugin):
        self.timer = Timer(t, self.Run)
        self.plugin = plugin
        self.timer.start()


    def Run(self):
        try:
            self.plugin.menuDlg.destroyMenu()
            self.plugin.menuDlg = None
        except:
            pass


    def Cancel(self):
        self.timer.cancel()
#===============================================================================
