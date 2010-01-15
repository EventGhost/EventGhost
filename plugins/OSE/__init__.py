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
#Last change: 2010-01-15 19:15 GMT+1



eg.RegisterPlugin(
    name = "On screen explorer",
    author = "Pako",
    version = "0.0.1",
    kind = "other",
    guid = "{D3D2DDD1-9BEB-4A26-969B-C82FA8EAB280}",
    description = u"""<rst>
Allows you to create custom On Screen Explorer.
        
Plugin OSE has built-in a function **"Stop processing this event"**,
if the menu is shown on the screen. This facilitates
the use of OSE in your configuration. You can use to control
the menu the same events (the same remote buttons)
as elsewhere in the configuration, without having
to explicitly use the **"Stop processing this event"**,
**"Disable an item"** or **"Exclusive enable a folder / macro"**.
Only it is necessary to place the folder with the OSE as high
as possible in the configuration tree.""",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?..........",
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

from threading import Timer
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import CreateEvent, SetEvent
import _winreg
import os
import win32api
from fnmatch import fnmatch
ERROR_NO_ASSOCIATION = 1155
FOLDER_ID = ">> "
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
    def SetStartDirectory(self):
        self.startDirectory = self.GetValue()
        
#===============================================================================
def MyComputer():
    mc_reg = _winreg.OpenKey(
        _winreg.HKEY_CLASSES_ROOT,
        "CLSID\\{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
    )
    myComputer = unicode(_winreg.EnumValue(mc_reg,0)[1])
    _winreg.CloseKey(mc_reg)
    return myComputer

def CaseInsensitiveSort(list):
    tmp = [(item.upper(), item) for item in list] # Schwartzian transform
    tmp.sort()
    return [item[1] for item in tmp]

def GetFolderItems(folder, patterns):
    patterns = patterns.split(",")
    myComputer = MyComputer()
    if folder != myComputer:
        ds = [FOLDER_ID+f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder,f))]
        ds = CaseInsensitiveSort(ds)
        fs = ["..",]
        for f in [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]:
            for p in patterns:
                if fnmatch(f,p.strip()):
                    if not f in fs:
                        fs.append(f)
                    break
        fs = CaseInsensitiveSort(fs)
        fs.extend(ds)
        return fs
    else: #pseudo-folder "My computer"
        drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        drvs = []
        for dr in drives:
            try:
               name = win32api.GetVolumeInformation(dr)[0]
               drvs.append(FOLDER_ID+"%s (%s)" % (name,dr[:2]))
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
        prefixLabel = 'Event prefix:'
        suffixLabel = 'Default event suffix:'
        folder = "Start folder:"
        browseTitle = "Selected folder:"
        toolTipFolder = "Press button and browse to select folder ..."
        patterns = "Show only the files corresponding to these patterns:"
#-------------------------------------------------------------------------------

    class MenuColourSelectButton(wx.BitmapButton):

        def __init__(
            self,
            id = -1,
            value=(255, 255, 255),
            name="ColourSelectButton",
            pos=wx.DefaultPosition,
            size=(40, wx.Button.GetDefaultSize()[1]),
            style=wx.BU_AUTODRAW,
            validator=wx.DefaultValidator,
        ):
            self.id = id
            self.value = value
            self.name = name
            wx.BitmapButton.__init__(
                self, panel, id, wx.NullBitmap, pos, size, style, validator,name
            )
            self.SetValue(value)
            self.Bind(wx.EVT_BUTTON, self.OnButton)

        def OnButton(self, event):
            colourData = wx.ColourData()
            colourData.SetChooseFull(True)
            colourData.SetColour(self.value)
            for n, colour in enumerate(eg.config.colourPickerCustomColours):
                colourData.SetCustomColour(n, colour)
            colourDlg = wx.ColourDialog(self.GetParent(), colourData)
            colourDlg.SetTitle(self.name)
            if colourDlg.ShowModal() == wx.ID_OK:
                colourData = colourDlg.GetColourData()
                colour=colourData.GetColour().Get()
                self.SetValue(colour)
                if eg.Version.base >= "0.4.0":
                    listBoxCtrl = event.GetEventObject().GetParent().GetSizer().\
                        GetChildren()[0].GetSizer().GetChildren()[0].GetSizer().\
                        GetChildren()[1].GetWindow()
                else:
                    listBoxCtrl = event.GetEventObject().GetParent().GetSizer().\
                        GetChildren()[0].GetSizer().GetChildren()[1].GetWindow()
                btnId = event.GetId()
                if btnId == 1:
                    listBoxCtrl.SetBackgroundColour(colour)
                    listBoxCtrl.Refresh()
                else:
                    listBoxCtrl.SetForegroundColour(colour)
                    listBoxCtrl.Refresh()
                event.Skip()
            eg.config.colourPickerCustomColours = [
                colourData.GetCustomColour(n).Get() for n in range(16)
            ]
            colourDlg.Destroy()

        def GetValue(self):
            return self.value

        def SetValue(self, value):
            self.value = value
            w, h = self.GetSize()
            image = wx.EmptyImage(w-10, h-10)
            image.SetRGBRect((1, 1, w-12, h-12), *value)
            self.SetBitmapLabel(image.ConvertToBitmap())
#-------------------------------------------------------------------------------

    class MenuFontButton(wx.BitmapButton):
        def __init__(
            self,
            fontInfo = None,
            id=-1,
            pos=wx.DefaultPosition,
            size=(40, wx.Button.GetDefaultSize()[1]),
            style=wx.BU_AUTODRAW,
            validator=wx.DefaultValidator,
            name="MenuFontButton",
        ):
            self.window = panel
            self.fontInfo = fontInfo
            wx.BitmapButton.__init__(
                self,
                panel,
                id,
                wx.Bitmap("images/font.png"),
                pos,
                size,
                style,
                validator,
                name
            )
            self.Bind(wx.EVT_BUTTON, self.OnButton)

        def OnButton(self, event):
            data = wx.FontData()
            if self.fontInfo is not None:
                font = wx.FontFromNativeInfoString(self.fontInfo)
                data.SetInitialFont(font)
            else:
                data.SetInitialFont(
                    wx.SystemSettings_GetFont(wx.SYS_ANSI_VAR_FONT )
                )
            dlg = wx.FontDialog(self.window, data)
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetFontData()
                font = data.GetChosenFont()
                if eg.Version.base >= "0.4.0":
                    listBoxCtrl = event.GetEventObject().GetParent().GetSizer().\
                        GetChildren()[0].GetSizer().GetChildren()[0].GetSizer().\
                        GetChildren()[1].GetWindow()
                else:
                    listBoxCtrl = event.GetEventObject().GetParent().GetSizer().\
                        GetChildren()[0].GetSizer().GetChildren()[1].GetWindow()
                for n in range(10,20):
                    font.SetPointSize(n)
                    listBoxCtrl.SetFont(font)
                    if listBoxCtrl.GetTextExtent('X')[1]>20:
                        break
                self.fontInfo = data.GetChosenFont().GetNativeFontInfo().\
                    ToString()
                event.Skip()
            dlg.Destroy()

        def GetValue(self):
            return self.fontInfo

        def SetValue(self, fontInfo):
            self.fontInfo = fontInfo
#-------------------------------------------------------------------------------

    def __call__(
        self,
        fore,
        back,
        fontInfo,
        prefix,
        suffix,
        monitor=0,
        start = "",
        patterns = "*.*"
    ):
        if not self.plugin.menuDlg:
            self.plugin.menuDlg = Menu()
            self.event = CreateEvent(None, 0, 0, None)
            wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                fore,
                back,
                fontInfo,
                False,
                self.plugin,
                self.event,
                prefix,
                suffix,
                monitor,
                start,
                patterns
            )
            eg.actionThread.WaitOnEvent(self.event)
#-------------------------------------------------------------------------------

    def GetLabel(
        self,
        fore,
        back,
        fontInfo,
        prefix,
        suffix,
        monitor,
        start,
        patterns
    ):
        return "%s: %s, [%s]" % (self.name,start,patterns)

    def Configure(
        self,
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None,
        prefix = 'OSE',
        suffix = 'Open',
        monitor = 0,
        start = "",
        patterns = "*.*"
    ):
        self.fore = fore
        self.back = back
        self.oldSel=0
        global panel
        panel = eg.ConfigPanel(self)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(160,120),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
        )
        if not patterns:
            patterns = "*.*"
        if start:
            items = GetFolderItems(start, patterns)
            listBoxCtrl.Set(items)

        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        if fontInfo is None:
            font = listBoxCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            listBoxCtrl.SetFont(font)
            if listBoxCtrl.GetTextExtent('X')[1]>20:
                break
        displayChoice = eg.DisplayChoice(panel, monitor)
        w = displayChoice.GetSize()[0]
        prefixLbl=wx.StaticText(panel, -1, self.text.prefixLabel)
        prefixCtrl = wx.TextCtrl(panel,-1,prefix,size=wx.Size(w,-1))
        suffixLbl=wx.StaticText(panel, -1, self.text.suffixLabel)
        suffixCtrl = wx.TextCtrl(panel,-1,suffix,size=wx.Size(w,-1))
        OSElbl = wx.StaticText(panel, -1, self.text.OSELabel)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = self.MenuFontButton(fontInfo)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = self.MenuColourSelectButton(
            0,
            fore,
            self.text.txtColour
        )
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = self.MenuColourSelectButton(
            1,
            back,
            self.text.background
        )
        folderLabel = wx.StaticText(panel, -1, self.text.folder)
        folderCtrl = MyDirBrowseButton(
            panel, 
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse,
        )
        folderCtrl.GetTextCtrl().SetEditable(False)
        #if not start:
        #    start = eg.folderPath.Documents           
        folderCtrl.SetValue(start)
        folderCtrl.SetStartDirectory()
        patternsLabel = wx.StaticText(panel, -1, self.text.patterns)
        patternsCtrl = wx.TextCtrl(panel,-1,patterns,size=(410,-1))
        #Sizers
        mainSizer = panel.sizer
        topSizer=wx.GridBagSizer(2, 30)
        mainSizer.Add(topSizer)
        topSizer.Add(previewLbl,(0, 0),flag = wx.TOP,border = 0)
        topSizer.Add(listBoxCtrl,(1, 0),(5,1),flag = wx.EXPAND)        
        topSizer.Add(fontLbl,(0, 1),flag = wx.TOP,border = 0)
        topSizer.Add(fontButton,(1, 1),flag = wx.TOP)
        topSizer.Add(foreLbl,(2, 1),flag = wx.TOP,border = 8)
        topSizer.Add(foreColourButton,(3, 1),flag = wx.TOP)
        topSizer.Add(backLbl,(4, 1),flag = wx.TOP,border = 8)
        topSizer.Add(backColourButton,(5, 1),flag = wx.TOP,border = 0)        
        topSizer.Add(prefixLbl,(0, 2),flag = wx.TOP,border = 0)
        topSizer.Add(prefixCtrl,(1, 2))
        topSizer.Add(suffixLbl,(2, 2),flag = wx.TOP,border = 8)
        topSizer.Add(suffixCtrl,(3, 2))
        topSizer.Add(OSElbl,(4, 2),flag = wx.TOP,border = 8)
        topSizer.Add(displayChoice,(5, 2))
        mainSizer.Add(folderLabel,0,wx.TOP,8)
        mainSizer.Add(folderCtrl,0,wx.TOP,2)
        mainSizer.Add(patternsLabel,0,wx.TOP,8)
        mainSizer.Add(patternsCtrl,0,wx.TOP,2)
        panel.sizer.Layout()

        def OnTextChange(evt):
            folder = folderCtrl.GetValue()
            patterns = patternsCtrl.GetValue()
            if not patterns:
                patterns = "*.*"
            if folder:
                folderCtrl.SetStartDirectory()
                try:
                    items = GetFolderItems(folder, patterns)
                    listBoxCtrl.Set(items)
                except:
                    pass
            evt.Skip()
        folderCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        patternsCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        
        # re-assign the test button
        def OnButton(event):
            if not self.plugin.menuDlg:
                self.plugin.menuDlg = Menu()
                self.event = CreateEvent(None, 0, 0, None)
                wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                    foreColourButton.GetValue(),
                    backColourButton.GetValue(),
                    fontButton.GetValue(), 
                    True,
                    self.plugin,
                    self.event,
                    prefixCtrl.GetValue(),
                    suffixCtrl.GetValue(),
                    displayChoice.GetSelection(),
                    folderCtrl.GetValue(),
                    patternsCtrl.GetValue()
                )
                eg.actionThread.WaitOnEvent(self.event)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            panel.SetResult(
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(),
            prefixCtrl.GetValue(),
            suffixCtrl.GetValue(),
            displayChoice.GetSelection(),
            folderCtrl.GetValue(),
            patternsCtrl.GetValue()
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

class Cancel(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.destroyMenu()
            self.plugin.menuDlg = None
            eg.event.skipEvent = True
#===============================================================================

class Execute (eg.ActionClass):
    class text:
        fileBoxLabel = "Action with the file"
        folderBoxLabel = "Action with the folder"
        returnFile = "Return path to the file as eg.result"
        openFile = "Open the file in associated application"
        goIntoFolder = "Go into that folder"
        returnFolder = "Return path to the folder as eg.result"
        triggerEvent = "Trigger event with this suffix:"

    def __call__(self, val = 54, fileSuff = "", folderSuff = ""):
        if self.plugin.menuDlg:
            eg.event.skipEvent = True
            filePath, prefix, suffix = self.plugin.menuDlg.GetInfo()
            filePath = filePath.replace(FOLDER_ID,"")
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
                    except WindowsError,e:
                        if e.winerror == ERROR_NO_ASSOCIATION:
                            eg.PrintError(Text.noAssoc % os.path.splitext(filePath)[1])
                        else:
                            raise
                self.plugin.menuDlg.destroyMenu()
                self.plugin.menuDlg = None
                if val&4: #return
                    return filePath
            elif os.path.isdir(filePath):
                if filePath[-3:] == r"\..":
                    if len(filePath) == 5:
                        filePath = MyComputer()
                    else:                
                        filePath = os.path.split(filePath[:-3])[0]
                if val&8: #trigger event
                    if folderSuff:
                        suffix = folderSuff
                    eg.TriggerEvent(prefix = prefix, suffix = suffix, payload = filePath) 
                if val&16: #go to the folder
                    event = CreateEvent(None, 0, 0, None)
                    wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                        prefix = prefix,
                        suffix = suffix,
                        start = filePath,
                        event = event,
                    )
                    eg.actionThread.WaitOnEvent(event)            
                    #os.startfile(filePath)
                else:
                    self.plugin.menuDlg.destroyMenu()
                    self.plugin.menuDlg = None
                if val&32: #return
                    return filePath

    def GetLabel(self,val, fileSuff, folderSuff):
        return "%s: %i, %s, %s" % (self.name,val, fileSuff, folderSuff)

    def Configure(self, val = 54, fileSuff = "", folderSuff = ""):
        panel = eg.ConfigPanel(self)
        triggFileCheck = wx.CheckBox(panel, -1, self.text.triggerEvent)
        triggFileCheck.SetValue(val&1)
        openFileCheck = wx.CheckBox(panel, -1, self.text.openFile)
        openFileCheck.SetValue(val&2)
        retFileCheck = wx.CheckBox(panel, -1, self.text.returnFile)
        retFileCheck.SetValue(val&4)
        triggFolderCheck = wx.CheckBox(panel, -1, self.text.triggerEvent)
        triggFolderCheck.SetValue(val&8)
        goFolderCheck = wx.CheckBox(panel, -1, self.text.goIntoFolder)
        goFolderCheck.SetValue(val&16)
        retFolderCheck = wx.CheckBox(panel, -1, self.text.returnFolder)
        retFolderCheck.SetValue(val&32)
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
        folderSuffSizer = wx.BoxSizer(wx.HORIZONTAL)
        fileSuffSizer.Add(triggFileCheck,0,wx.RIGHT,5)
        fileSuffSizer.Add(suffixFile,0,wx.TOP,-4)
        fileSizer.Add(fileSuffSizer,0,wx.TOP,4)
        fileSizer.Add(openFileCheck,0,wx.TOP,6)
        fileSizer.Add(retFileCheck,0,wx.TOP,9)
        folderSuffSizer.Add(triggFolderCheck,0,wx.RIGHT,5)
        folderSuffSizer.Add(suffixFolder,0,wx.TOP,-4)
        folderSizer.Add(folderSuffSizer,0,wx.TOP,4)
        folderSizer.Add(goFolderCheck,0,wx.TOP,6)
        folderSizer.Add(retFolderCheck,0,wx.TOP,9)
        mainSizer.Add(fileSizer,0)
        mainSizer.Add(folderSizer,0,wx.TOP,20)
        while panel.Affirmed():
            val  =      triggFileCheck.GetValue()
            val += 2  * openFileCheck.GetValue()
            val += 4  * retFileCheck.GetValue()
            val += 8  * triggFolderCheck.GetValue()
            val += 16 * goFolderCheck.GetValue()
            val += 32 * retFolderCheck.GetValue()
            panel.SetResult(val,
                suffixFile.GetValue(),
                suffixFolder.GetValue()
                )
#===============================================================================

ACTIONS = (
    (ShowMenu, 'ShowMenu', 'Show explorer', 'Show on screen explorer.', None),
    (MoveCursor, 'MoveUp', 'Cursor Up', 'Cursor Up.', -1),
    (MoveCursor, 'MoveDown', 'Cursor Down', 'Cursor Down.', 1),
    (Execute, 'Execute', 'Execute', 'Execute.', None),
    (Cancel, 'Cancel', 'Cancel', 'Cancel button pressed.', None),
)
#===============================================================================

class Text:
    noAssoc = 'Error: No application is associated with the file type "%s" for operation "Open" !'
    
#===============================================================================    

class OSE(eg.PluginClass):
    monDim = None
    menuDlg = None

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    def __start__(self):
        self.monDim = GetMonitorDimensions()
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

    def ShowMenu(
        self,
        fore=None,
        back=None,
        fontInfo=None,
        flag=None,
        plugin=None,
        event=None,
        prefix=None,
        suffix=None,
        monitor=None,
        start=None,
        patterns=None
    ):
        self.fore     = fore or self.fore
        self.back     = back or self.back
        self.fontInfo = fontInfo or self.fontInfo
        self.flag     = flag or self.flag
        self.plugin   = plugin or self.plugin
        self.prefix   = prefix or self.prefix
        self.suffix   = suffix or self.suffix
        self.monitor  = monitor or self.monitor
        self.start    = start or self.start
        self.patterns = patterns or self.patterns
        
        self.choices  = GetFolderItems(self.start,self.patterns)
        sizer = self.GetSizer()
        if sizer:
            eventChoiceCtrl = sizer.GetChildren()[0].GetWindow()
            eventChoiceCtrl.Set(self.choices)
        else:
            eventChoiceCtrl=wx.ListBox(
                self,
                choices = self.choices,
                style = wx.LB_SINGLE|wx.LB_NEEDED_SB
            )          
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(mainSizer)
            mainSizer.Add(eventChoiceCtrl, 0, wx.EXPAND)
            self.Bind(wx.EVT_CLOSE, self.onClose)
            eventChoiceCtrl.Bind(wx.EVT_LISTBOX_DCLICK, self.DoubleCick)
            font = wx.FontFromNativeInfoString(self.fontInfo)
            eventChoiceCtrl.SetFont(font)
            self.SetBackgroundColour((0,0,0))            
            eventChoiceCtrl.SetBackgroundColour(self.back)
            eventChoiceCtrl.SetForegroundColour(self.fore)            
            if self.flag:
                self.timer=MyTimer(t = 5.0, plugin = self.plugin)
        try:
            x,y,ws,hs = self.plugin.monDim[self.monitor]
        except IndexError:
            x,y,ws,hs = self.plugin.monDim[0]
        # menu height calculation:
        h=eventChoiceCtrl.GetCharHeight()
        height0 = len(self.choices)*h+5
        height1 = h*((hs-20)/h)+5
        height = min(height0,height1)+6
        # menu width calculation:
        width_lst=[]
        for item in self.choices:
            width_lst.append(eventChoiceCtrl.GetTextExtent(item+' ')[0])
        width = max(width_lst)+8
        if height-6 < height0:
            width += 20 #for vertical scrollbar
        width = min((width,ws-50))+6
        x_pos = x+(ws-width)/2
        y_pos = y + (hs-height)/2
        self.SetDimensions(x_pos,y_pos,width,height)
        eventChoiceCtrl.SetDimensions(2,2,width-6,height-6,wx.SIZE_AUTO)
        eventChoiceCtrl.SetSelection(0)
        self.Show(True)
        if event:
            wx.Yield()
            SetEvent(event)
        
    def GetInfo(self):
        sel = self.GetSizer().GetChildren()[0].GetWindow().GetSelection()
        return os.path.join(self.start,self.choices[sel]),self.prefix,self.suffix

    def MoveCursor(self,step):
        max=len(self.choices)
        if max > 0:
            choiceCtrl = self.GetSizer().GetChildren()[0].GetWindow()
            sel = choiceCtrl.GetSelection()
            new = sel + step
            if new < 0:
                new += max
            elif new > max-1:
                new -= max
            choiceCtrl.SetSelection(new)                    

    def DoubleCick(self, evt):
        sel = self.GetSizer().GetChildren()[0].GetWindow().GetSelection()
        filePath = os.path.join(self.start,self.choices[sel])
        filePath = filePath.replace(FOLDER_ID,"")
        if filePath[-2] == ":": #root of drive
            filePath = filePath[-3:-1]+"\\"
        if filePath[-3:] == r"\..":
            if len(filePath) == 5:
                filePath = MyComputer()
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
                    eg.PrintError(Text.noAssoc % os.path.splitext(filePath)[1])
                else:
                    raise
        else:
            self.ShowMenu(
                prefix = self.prefix,
                suffix = self.suffix,
                start = filePath,
            )

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
