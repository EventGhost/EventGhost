version="0.1.1" 

# Plugins/RadioSure/__init__.py
#
# Copyright (C)  2009 Pako  (lubos.ruckl@quick.cz)
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

# Last change: 2010-02-28 07:50 GMT+1
# ==============================================================================

eg.RegisterPlugin(
    name = "RadioSure",
    author = "Pako",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control the <a href="http://www.radiosure.com/">'
        'RadioSure</a>.'
    ),
    createMacrosOnAdd = True,    
    #url = "http://www.eventghost.org/forum/viewtopic.php?XXXXXXXXX",
    
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUA//+Gh4ju7/Ds"
        "7e7q6+zo6evm5+nk5efi4+Xg4ePd3+Db3N7Z2tzW2Nrr7e5+g4bo6erm5+js7e3a3N7Y"
        "2dt3fYDT1dfp6uzn6Orl5uhIS03V1tjS1NbQ0tTn6Onl5ufi5OXS09XP0dPNz9HR09XP"
        "0NPMztDKzM7h4+Tf4OLd3uCVmp1OUlQZGhoYGRlLTlCHjZDMzdDJy87Hycve4OHc3t+d"
        "oqQyNDU3OjtSVlgpKywqLC2IjpHHyMvExsnc3d/Z29xWWlyBh4p2fH9pbnFfZGYsLi9L"
        "T1HExsjCxMYbHB2XnJ5MUFJKTU9yeHtVWVvBw8a/wcTW19kcHR6UmZypra9RVVeGjI9l"
        "am0aGxu/wcO9v8JcYWNeY2W5vL6xtLamqqyboKK9vsG7vcA9QEG6vL+5u76LkJPIycyy"
        "tbddYmRYXV+jqKqDiYy3ubzFx8nDxcfBw8W4ur22uLsAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADQcfgAAAAAAAXQciD0AAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAABAAgAAAAAAAAAAAAAAAAAAAAAAAAAAABGa1gAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAEAAAAAAAAAAAAPAAAAAAEAAAEAAADQckT/C08AAAAAAAAAAAAAAAMAAADf"
        "BnAAAAAAAAAAAAAAAAAAAAQAAQEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACnZAh6AAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAKdJREFUeNpjYGBgRAVoAl9A"
        "ArwQCbDMayYgg5OTk5GBg4PhPzs7OwNIAESDARsbGwNICxtQKQeQLwSkb4EE1JEMPQfS"
        "wgMGjNwgANZix8h4UwOqYgdIxdmznGKcIPAMaBVIReARW6DcNW2QimUgAWlGe7DynTY8"
        "jPOYwNYzs/+//vqB3ANmZrAWVUeg9EsGCcafHIyTQQKGjDZAAUYOJt4/rH0M6N4HAFCJ"
        "GrcTFgV2AAAAAElFTkSuQmCC"
    ),    
)

#===============================================================================

import os
import subprocess
import xml.sax as sax
from xml.sax.handler import ContentHandler
from threading import Timer
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from time import sleep
from win32gui import GetWindowText, MessageBox, GetWindow, GetDlgCtrlID, GetDlgItem, GetClassName
from win32api import GetSystemMetrics
from eg.WinApi.Dynamic import SendMessage
import _winreg

WM_COMMAND    = 273
WM_SYSCOMMAND = 274
TBM_GETPOS    = 1024
TBM_SETPOS    = 1029
SC_RESTORE    = 61728
GW_CHILD      = 5
GW_HWNDNEXT   = 2

#===============================================================================

class Text:
    label1 = "Folder with RadioSure.exe:"
    label2 = "Folder with RadioSure.xml:"
    filemask = "RadioSure.exe|RadioSure.exe|All-Files (*.*)|*.*"
    text1 = "Couldn't find RadioSure window !"
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = 'Folder "%s" is incorrect'
    boxMessage1 = 'Missing file %s !'
    picker = "Colour Picker"
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
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

    def OnButton(self, event):
        colourData = wx.ColourData()
        colourData.SetChooseFull(True)
        colourData.SetColour(self.value)
        for i, colour in enumerate(eg.config.colourPickerCustomColours):
            colourData.SetCustomColour(i, colour)
        dialog = wx.ColourDialog(self.GetParent(), colourData)
        dialog.SetTitle(Text.picker)
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

class Menu(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'RadioSure OS Menu',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )

    def ShowMenu(
        self,
        fore,
        back,
        fontInfo,
        flag,
        plugin,
        event,
        List
    ):
        self.fore    = fore
        self.back    = back
        self.plugin  = plugin
        self.plugin.RefreshVariables()
        self.plugin.List = List
        self.choices = self.plugin.Favorites if List else self.plugin.History
        self.flag    = flag

        stationChoiceCtrl=wx.ListBox(
            self,
            choices = [item[1] for item in self.choices],
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        if fontInfo is None:
            font = stationChoiceCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        stationChoiceCtrl.SetFont(font)
        # menu height calculation:
        h=stationChoiceCtrl.GetCharHeight()
        height0 = len(self.choices)*h+5
        height1 = h*((GetSystemMetrics (1)-50)/h)+5
        height = min(height0,height1)
        # menu width calculation:
        width_lst=[]
        for item in [item[1] for item in self.choices]:
            width_lst.append(stationChoiceCtrl.GetTextExtent(item+' ')[0])
        width = max(width_lst)+8
        if height<height0:
            width += 20 #for vertical scrollbar
        width = min((width,GetSystemMetrics (0)-50))
        self.SetSize((width+6,height+6))
        stationChoiceCtrl.SetDimensions(2,2,width,height,wx.SIZE_AUTO)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        ix = self.plugin.FavIx if List else self.plugin.HistIx
        stationChoiceCtrl.SetSelection(ix)
        self.SetBackgroundColour((0,0,0))
        stationChoiceCtrl.SetBackgroundColour(self.back)
        stationChoiceCtrl.SetForegroundColour(self.fore)
        mainSizer.Add(stationChoiceCtrl, 0, wx.EXPAND)
        
        self.Bind(wx.EVT_CLOSE, self.onClose)
        stationChoiceCtrl.Bind(wx.EVT_LISTBOX_DCLICK, self.ChangeStation)
        
        if self.flag:
            self.timer=MyTimer(t = 5.0, plugin = self.plugin)
        
        self.Centre()
        self.Show(True)
        wx.Yield()
        SetEvent(event)

    def ChangeStation(self, event = None):
        sel=self.GetSizer().GetChildren()[0].GetWindow().\
            GetSelection()
        self.plugin.PlayFromMenu()

    def onClose(self, event):
        self.Destroy()
        self.plugin.menuDlg = None
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

class my_xml_handler(ContentHandler):
    def __init__(
        self,
        plugin
    ):
        self.plugin = plugin

    def startDocument( self):
        self.plugin.Favorites = []
        self.plugin.History = []
        self.plugin.FavIx = -1
        self.plugin.HistIx = -1
        self.plugin.Current = ['','']
        self._recent_text = ''
        self.List = None
        self.tmpList = []

    def startElement( self, name, attrs):
        if name == "Favorites":
            self.List = self.plugin.Favorites
        if name == "History":
            self.List = self.plugin.History

    def endElement( self, name):
        if name == "Favorites" or name == "History":
            self.List = None
        elif self.List is not None:
            if name.startswith('Source'):
                if self._recent_text.strip() <> '':
                    self.tmpList.append(self._recent_text.strip())
            else:
                if self._recent_text.strip() <> '':
                    self.tmpList.append(self._recent_text.strip())
                    self.List.append(self.tmpList)
                    self.tmpList = []
        elif name == 'Station_URL':
            self.plugin.Current[0] = self._recent_text.strip()
        elif name == 'Station_Title':
            self.plugin.Current[1] = self._recent_text.strip()
        self._recent_text = ''
            
    def characters( self, content):
        self._recent_text += content
#===============================================================================
            
def HandleRS():
    FindRS = eg.WindowMatcher(
                u'RadioSure.exe',
                None,
                u'#32770',
                None,
                None,
                None,
                True,
                0.0,
                0
            )
    hwnds = FindRS()
    res = None
        
    for hwnd in hwnds:
        curhw = GetWindow(hwnd,GW_CHILD)
        while curhw > 0:
            if GetDlgCtrlID(curhw) == 1016 and GetClassName(curhw) == 'SysListView32':
                res = hwnd
                break
            curhw = GetWindow(curhw,GW_HWNDNEXT)
        if res:
            break           
    return res
#===============================================================================

def GetCtrlByID(id):
    res = None
    hwnd = HandleRS()
    if hwnd:
        try:
            res = GetDlgItem(hwnd,id)
        except:
            pass
    return res
#===============================================================================

def getPathFromReg():
    try:
        rs_reg = _winreg.OpenKey(
            _winreg.HKEY_CURRENT_USER,
            "Software\\RadioSure"
        )
        res = unicode(_winreg.EnumValue(rs_reg,0)[1])
        _winreg.CloseKey(rs_reg)
    except:
        res = None
    return res
#===============================================================================

class RadioSure(eg.PluginClass):
    text=Text
    menuDlg = None
    RadioSurePath = u''
    xmlPath = u''
    Favorites = []
    History = []
    Current = ['','']
    FavIx = -1
    HistIx = -1
    List = None


    def RefreshVariables(self):
        xmltoparse = self.xmlPath+u'\\RadioSure.xml'
        dh = my_xml_handler(self)
        sax.parse(xmltoparse.encode(eg.systemEncoding), dh)
        if self.Current in self.Favorites:
            self.FavIx = self.Favorites.index(self.Current)
        else:
            self.FavIx = -1
        if self.Current in self.History:
            self.HistIx = self.History.index(self.Current)
        else:
            self.HistIx = -1

        
    def PlayFromMenu(self):
        if self.menuDlg is not None:
            sel=self.menuDlg.GetSizer().GetChildren()[0].GetWindow().\
                GetSelection()                
            self.menuDlg.Close()
        hwnd = HandleRS()
        if hwnd:
            List = self.Favorites if self.List else self.History
            Base = 1326 if self.List else 1374 
            if sel <= len(List)-1:
                SendMessage(hwnd, WM_COMMAND, Base+sel, 0)
        else:
            self.PrintError(self.text.text1)


    def __init__(self):
        text=Text
        self.AddActionsFromList(Actions)

    def __start__(self, path, xmlpath):
        self.RadioSurePath = path
        self.xmlPath = xmlpath
                   
    def Configure(self, path = None, xmlpath = None):
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        rsPathCtrl = MyDirBrowseButton(
            panel, 
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )        
        rsPathCtrl.GetTextCtrl().SetEditable(False)
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        xmlPathCtrl = MyDirBrowseButton(
            panel, 
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )        
        xmlPathCtrl.GetTextCtrl().SetEditable(False)        
    
        if path is None:
            RSpath = getPathFromReg()
            if RSpath:
                self.RadioSurePath = RSpath
                #self.xmlPath = unicode(eg.folderPath.LocalAppData)+u"\\RadioSure"
                rsPathCtrl.SetValue(self.RadioSurePath)
                #xmlPathCtrl.SetValue(self.xmlPath)
            else:
                self.RadioSurePath = unicode(eg.folderPath.ProgramFiles)+"\\RadioSure"
                #self.xmlPath = self.RadioSurePath
                rsPathCtrl.SetValue("")
                #xmlPathCtrl.SetValue("")

        else:
            rsPathCtrl.SetValue(path)
            xmlPathCtrl.SetValue(xmlpath)
            self.RadioSurePath = path
            self.xmlPath = xmlpath
        rsPathCtrl.startDirectory = self.RadioSurePath
        xmlPathCtrl.startDirectory = self.xmlPath
        sizerAdd = panel.sizer.Add
        sizerAdd(label1Text, 0, wx.TOP,15)
        sizerAdd(rsPathCtrl,0,wx.TOP,3)
        sizerAdd(label2Text, 0, wx.TOP,15)
        sizerAdd(xmlPathCtrl,0,wx.TOP,3)

        def Validation():
            flag1 = os.path.exists(rsPathCtrl.GetValue()+"\\RadioSure.exe")
            flag2 = os.path.exists(xmlPathCtrl.GetValue()+"\\RadioSure.xml")
            flag = flag1 and flag2
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)
       
        def OnPathChange(event = None):
            path = rsPathCtrl.GetValue()
            flag = os.path.exists(path+"\\RadioSure.exe")
            if event and not flag:
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % 'RadioSure.exe',
                    self.text.boxTitle % path,
                        0
                    )
            if path != "":
                rsPathCtrl.startDirectory = path
                self.RadioSurePath = path
                RSpath = getPathFromReg()
                if RSpath and path == RSpath:
                    self.xmlPath = unicode(eg.folderPath.LocalAppData)+u"\\RadioSure"
                else:
                    self.xmlPath = self.RadioSurePath
                xmlPathCtrl.SetValue(self.xmlPath)
            Validation()
        rsPathCtrl.Bind(wx.EVT_TEXT,OnPathChange)
        OnPathChange()        
        
        def OnPath2Change(event = None):
            path2 = xmlPathCtrl.GetValue()
            flag = os.path.exists(path2+"\\RadioSure.xml")
            if event and not flag:
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % 'RadioSure.xml',
                    self.text.boxTitle % path2,
                        0
                    )
            if path2 != "":
                xmlPathCtrl.startDirectory = path2            
            Validation()
        xmlPathCtrl.Bind(wx.EVT_TEXT,OnPath2Change)
        OnPath2Change()        
        
        while panel.Affirmed():
            panel.SetResult(
                rsPathCtrl.GetValue(),
                xmlPathCtrl.GetValue(),
            )           
#===============================================================================
#cls types for Actions list:
#===============================================================================

class Run(eg.ActionClass):
    class text:
        play = "Automatically play selected favorite after start"
        default = "Use start settings RadioSure"
        label = "Select favorite:"
        over = "Too large number (%s > %s) !"
        alt_ret = "Default start"
        alr_run = "RadioSure is already running !"
        text2 = "Couldn't find file %s !"




    def __call__(self, play = False, fav = 1):
        hwnd = HandleRS()        
        if hwnd is None:
            rs = self.plugin.RadioSurePath+'\\RadioSure.exe'
            if os.path.isfile(rs):        
                wx.CallAfter(subprocess.Popen,[rs])
                if play:
                    for n in range(50):                
                        sleep(.1)
                        hwnd = HandleRS()
                        if hwnd:
                            flag = True
                            break
                    if flag:
                        SendMessage(hwnd, WM_COMMAND, 1008, 0) #Stop playing
                        sleep(2.5)
                        self.plugin.RefreshVariables()
                        if fav <= len(self.plugin.Favorites):
                            SendMessage(hwnd, WM_COMMAND, 1325+fav, 0)
                            return str(fav)+": "+self.plugin.Favorites[self.plugin.FavIx][1]
                        else:
                            return self.text.over % (str(fav),\
                                str(len(self.plugin.Favorites)))
                    else:
                        self.PrintError(self.plugin.text.text1)
                        return self.plugin.text.text1
                else:
                    return self.text.alt_ret
            else:
                self.PrintError(self.text.text2 % 'RadioSure.exe')
                return self.text.text2 % 'RadioSure.exe'
        else:
            return self.text.alr_run
                   
    def GetLabel(self, play ,fav):
        num = ':'+str(fav) if play else ''
        return self.name+num
            
    def Configure(self, play = False, fav = 1):
        panel=eg.ConfigPanel(self)
        sizerAdd=panel.sizer.Add
        rb1 = panel.RadioButton(play, self.text.play, style=wx.RB_GROUP)
        rb2 = panel.RadioButton(not play, self.text.default)                            
        sizerAdd(rb1,0,wx.TOP,15)		
        sizerAdd(rb2,0,wx.TOP,6)		
        favLbl=wx.StaticText(panel, -1, self.text.label)
        sizerAdd(favLbl,0,wx.TOP,25)
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=30,
        )
        favCtrl.SetValue(fav)
        sizerAdd(favCtrl,0,wx.TOP,5)
        
        def onChangeMode(evt=None):
            enbl=rb1.GetValue()
            favLbl.Enable(enbl)
            favCtrl.Enable(enbl)
            if evt is not None:
                evt.Skip()
        rb1.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        rb2.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        OnAutostart()
                
        while panel.Affirmed():
            panel.SetResult(
                rb1.GetValue(),
                favCtrl.GetValue()
            )
#===============================================================================

class WindowControl(eg.ActionClass):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            SendMessage(hwnd, WM_SYSCOMMAND, self.value, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1         
#===============================================================================

class SendMessageActions(eg.ActionClass):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            SendMessage(hwnd, WM_COMMAND, self.value, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class Play(eg.ActionClass):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            self.plugin.RefreshVariables()
            SendMessage(hwnd, WM_COMMAND, 1374+self.plugin.HistIx, 0)
            return self.plugin.History[self.plugin.HistIx][1]
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class SetVolume(eg.ActionClass):
    class text:
        label=["Set volume (0 - 100%):",
            "Set step (1 - 25%):",
            "Set step (1 - 25%):"]
        
    def __call__(self, step = None):
        if step is None:
            if self.value == 0:
                step = 50
            else:
                step = 5
        hwnd = GetCtrlByID(1006) #1006 = ID for ctrl "msctls_trackbar32" 
        if hwnd:
            vol = SendMessage(hwnd, TBM_GETPOS, 0, 0)
            key = None
            value = None
            if self.value == 0:
                volume = step
            elif self.value == 1:
                volume = vol+step if (vol+step)<100 else 100
            else:
                volume = vol-step if (vol-step)>0 else 0
            if vol>volume:
                key='{Left}'            
                if vol>volume+1:
                    value = volume+1
            elif vol<volume:
                key='{Right}'
                if vol<volume-1:
                    value = volume-1
            if value:
                SendMessage(hwnd, TBM_SETPOS,1,value)
            if key:
                eg.SendKeys(hwnd, key, False)
            return SendMessage(hwnd, TBM_GETPOS, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
            
    def Configure(self, step = None):
        if step is None:
            if self.value == 0:
                step = 50
            else:
                step = 5
        panel=eg.ConfigPanel(self)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.label[self.value]))
        if self.value == 0:
            Min = 0
            Max = 100
        else:
            Min = 1
            Max = 25
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            fractionWidth=0,
            increment=1,
            min=Min,
            max=Max,
        )
        volumeCtrl.SetValue(step)
        panel.sizer.Add(volumeCtrl,0,wx.TOP,10)
        
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())
#===============================================================================

class GetVolume(eg.ActionClass):
    def __call__(self):       
        hwnd = GetCtrlByID(1006)  #1006 = ID for ctrl "msctls_trackbar32"
        if hwnd:
            return SendMessage(hwnd, TBM_GETPOS, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class SelectFav(eg.ActionClass):
    class text:
        label = "Select preset number (1-30):"
        txtLabel = 'Preset number:'
        over = "Too large number (%s > %s) !"
        modeLabel = 'Preset number to get as:'
        modeChoices = [
            'Event payload',
            'Python expression',
            'Number'
        ]
        
    def __call__(self,fav = 1, mode = 0, number = '{eg.event.payload}'):
        hwnd = HandleRS()
        if hwnd:
            if mode == 2:
                indx = fav
            else:
                indx = int(eg.ParseString(number))
            self.plugin.RefreshVariables()
            if indx <= len(self.plugin.Favorites):
                SendMessage(hwnd, WM_COMMAND, 1325+indx, 0)
                return str(indx)+": "+self.plugin.Favorites[indx-1][1]
            else:
                self.PrintError(
                    self.text.over % (str(indx),str(len(self.plugin.Favorites))))
                return self.text.over % (str(indx),str(len(self.plugin.Favorites)))
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1

    def GetLabel(self, fav,mode,number):
        if mode == 2:
            number = str(fav)
        return self.text.txtLabel+number
            
    def Configure(self, fav = 1, mode = 0, number = '{eg.event.payload}'):
        self.number = number
        panel = eg.ConfigPanel(self)
        radioBoxMode = wx.RadioBox(
            panel, 
            -1, 
            self.text.modeLabel,
            choices = self.text.modeChoices,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(mode)
        txtBoxLabel = wx.StaticText(panel, -1, self.text.txtLabel)
        numberCtrl = wx.TextCtrl(panel,-1,self.number)
        spinLabel = wx.StaticText(panel, -1, self.text.label)
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=30,
        )
        favCtrl.SetValue(fav)
        panel.sizer.Add(radioBoxMode, 0, wx.TOP,0)
        panel.sizer.Add(txtBoxLabel,0,wx.TOP,10)
        panel.sizer.Add(numberCtrl,0,wx.TOP,5)
        panel.sizer.Add(spinLabel,0,wx.TOP,10)
        panel.sizer.Add(favCtrl,0,wx.TOP,5)
        
        def onRadioBox(event = None):
            sel = radioBoxMode.GetSelection()
            txtBoxLabel.Enable(False)
            numberCtrl.Enable(False)
            spinLabel.Enable(False)
            favCtrl.Enable(False)
            if sel == 0:
                self.number = '{eg.event.payload}'
            elif sel == 1:
                txtBoxLabel.Enable(True)
                numberCtrl.Enable(True)
            else:
                self.number = favCtrl.GetValue()
                spinLabel.Enable(True)
                favCtrl.Enable(True)
            numberCtrl.ChangeValue(str(self.number))
            if event:
                event.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, onRadioBox)
        onRadioBox()
        
        def onSpin(event):
            numberCtrl.ChangeValue(str(favCtrl.GetValue()))
            event.Skip()
        favCtrl.Bind(wx.EVT_TEXT, onSpin)
        
        while panel.Affirmed():
            panel.SetResult(
                favCtrl.GetValue(),
                radioBoxMode.GetSelection(),
                numberCtrl.GetValue())
#===============================================================================

class NextPrevFav(eg.ActionClass):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            self.plugin.RefreshVariables()
            ix = self.plugin.FavIx
            if self.value == 1 and ix == len(self.plugin.Favorites) - 1 :
                ix = -1
            elif self.value == -1 and ix == 0:
                ix = len(self.plugin.Favorites)
            SendMessage(hwnd, WM_COMMAND, 1326+ix+self.value, 0)
            return (str(ix+self.value+1)+": "+self.plugin.Favorites[ix+self.value][1])
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class GetPlayingTitle(eg.ActionClass):  
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            return GetWindowText(hwnd)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class ShowMenu(eg.ActionClass):
    panel = None
    
    class text:
        menuPreview = 'On screen menu preview:'
        menuFont = 'Menu font:'
        txtColour = 'Text colour'
        background = 'Background colour'        
#===============================================================================
    def __call__(
        self,
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None
    ):
        if not self.plugin.menuDlg:
            self.plugin.menuDlg = Menu()
            self.event = CreateEvent(None, 0, 0, None)
            wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                fore,
                back,
                fontInfo,
                False, #Timer OFF
                self.plugin,
                self.event,
                self.value
            )
            eg.actionThread.WaitOnEvent(self.event)            
#===============================================================================
        
    def GetLabel(
        self,
        fore,
        back,
        fontInfo,
    ):
        return self.name
        
        
    def Configure(
        self,
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None
    ):

        self.plugin.RefreshVariables()
        self.List = self.plugin.Favorites if self.value else self.plugin.History
        choices = [item[1] for item in self.List]
        self.fore = fore
        self.back = back
        self.oldSel=0
        global panel
        panel = eg.ConfigPanel(self)
        mainSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        mainSizer.Add(previewLbl)
        panel.sizer.Add(mainSizer)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(420,120),
            choices = choices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB 
        )
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
        mainSizer.Add(listBoxCtrl,0,wx.TOP,5)
        
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = extFontSelectButton(panel, value = fontInfo)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = extColourSelectButton(panel,fore)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = extColourSelectButton(panel,back)        
        bottomSizer = wx.FlexGridSizer(3,3,hgap=0,vgap=3)
        bottomSizer.Add((140,10))
        bottomSizer.Add((140,10))
        bottomSizer.Add((140,10))
        bottomSizer.Add(fontLbl)
        bottomSizer.Add(foreLbl)
        bottomSizer.Add(backLbl)
        bottomSizer.Add(fontButton)
        bottomSizer.Add(foreColourButton)
        bottomSizer.Add(backColourButton)
        mainSizer.Add(bottomSizer)
        
        def OnFontBtn(evt):
            value = evt.GetValue()
            font = wx.FontFromNativeInfoString(value)
            for n in range(10,20):
                font.SetPointSize(n)
                listBoxCtrl.SetFont(font)
                if listBoxCtrl.GetTextExtent('X')[1]>20:
                    break            
            evt.Skip()
        fontButton.Bind(EVT_BUTTON_AFTER, OnFontBtn)        

        def OnColourBtn(evt):
            id = evt.GetId()
            value = evt.GetValue()
            if id == foreColourButton.GetId():
                listBoxCtrl.SetForegroundColour(value)
            elif id == backColourButton.GetId():
                listBoxCtrl.SetBackgroundColour(value)
            listBoxCtrl.Refresh()
            evt.Skip()
        foreColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)

        def OnClick(evt):
            listBoxCtrl.SetSelection(-1)
            evt.StopPropagation()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, OnClick)
        
        
        # re-assign the test button
        def OnButton(event):
            if not self.plugin.menuDlg:
                self.plugin.menuDlg = Menu()
                self.event = CreateEvent(None, 0, 0, None)
                wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                    foreColourButton.GetValue(),
                    backColourButton.GetValue(),
                    fontButton.GetValue(), 
                    True, #Timer ON
                    self.plugin,
                    self.event,
                    self.value
                )
                eg.actionThread.WaitOnEvent(self.event)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)
 

        while panel.Affirmed():
            panel.SetResult(
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(), 
            )
#===============================================================================

class MoveCursor(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            max=len(self.plugin.Favorites)
            if max > 0:
                sel=self.plugin.menuDlg.GetSizer().GetChildren()[0].\
                    GetWindow().GetSelection()
                if sel == eval(self.value[0]):
                    sel = eval(self.value[1])
                self.plugin.menuDlg.GetSizer().GetChildren()[0].GetWindow().\
                    SetSelection(sel+self.value[2])
#===============================================================================

class OK_Btn(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            self.plugin.PlayFromMenu()
#===============================================================================

class Cancel_Btn(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            self.plugin.menuDlg.Close() 
#===============================================================================

Actions = (
    (Run,"Run","Run RadioSure","Run RadioSure with its default settings.",None),
    (SendMessageActions,"Minimize","Minimize window","Minimize window.",2),
    (WindowControl,"Restore","Restore window","Restore window.",SC_RESTORE),
    (SendMessageActions,"MinimRest","Minimize/Restore","Minimize/Restore window.",1075),
    (SendMessageActions,"Close","Close window (exit RadioSure)","Close window (exit RadioSure).",1),
    (SendMessageActions,"Expand","Collapse/Expand window","Collapse/Expand window.",1076),
    (SendMessageActions,"OnTop","Stay on top On/Off","Stay on top On/Off.",1077),
    (SendMessageActions,"PlayStop","Play/Stop","Play/Stop.",1000),
    (SendMessageActions,"MuteOnOff","Mute On/Off","Mute On/Off.",1027),
    (SendMessageActions,"RecOnOff","Record On/Off","Record On/Off.",1051),
#    (Play,"Play","Play","Play last playing station.",None),
    (SendMessageActions,"Stop","Stop","Stop.",1008),
#    (SendMessageActions,"RecOn","Rec on","Rec on.",0),
#    (SendMessageActions,"RecOff","Rec off","Rec off.",0),
#    (SendMessageActions,"MuteOn","Mute on","Mute on.",0),
#    (SendMessageActions,"MuteOff","Mute off","Mute off.",0),
    (GetVolume,"GetVolume","Get volume","Get volume.", None),
    (SetVolume,"SetVolume","Set volume","Set volume.", 0),
    (SetVolume,"VolumeUp","Volume up","Volume up.", 1),
    (SetVolume,"VolumeDown","Volume down","Volume down.", 2),
    (eg.ActionGroup, 'Equalizer', 'Equalizer', 'Equalizer',(
        (SendMessageActions,"EqualizerOff","Equalizer Off","Equalizer Off.", 2000),
        (SendMessageActions,"EqualizerJazz","Equalizer Jazz","Equalizer Jazz.", 2001),
        (SendMessageActions,"EqualizerPop","Equalizer Pop","Equalizer Pop.", 2002),
        (SendMessageActions,"EqualizerRock","Equalizer Rock","Equalizer Rock.", 2003),
        (SendMessageActions,"EqualizerClassic","Equalizer Classic","Equalizer Classic.", 2004),
    )),
    (eg.ActionGroup, 'Fav_and_Hist', 'Favorites and History', 'Favorites and History',(
        (SendMessageActions,"AddFav","Add to favorites","Add current station to favorites.",1324),
        (SendMessageActions,"RemFav","Remove from favorites","Remove current station from favorites.",1325),
        (SelectFav,"SelectFav","Select favorite (preset number)","Select favorite by preset number (order).", None),
        (NextPrevFav,"NextFav","Next favorite","Next favorite.", 1),
        (NextPrevFav,"PreviousFav","Previous favorite","Previous favorite.", -1),
        (SendMessageActions,"PreviousHist","Back in history","Back in history.",1038),
        (SendMessageActions,"ForwardHist","Forward in history","Forward in history.",1039),
        (GetPlayingTitle,"GetPlayingTitle","Get currently playing station/title","Gets the name of currently playing station/title.", None),
        (eg.ActionGroup, 'Menu', 'Menu', 'Menu',(
            (ShowMenu, 'ShowFavMenu', 'Show favorites menu', 'Show favorites on screen menu.', True),
            (ShowMenu, 'ShowHistMenu', 'Show history menu', 'Show history on screen menu.', False),
            (MoveCursor, 'MoveDown', 'Cursor down', 'Cursor down.', ('max-1', '-1', 1)),
            (MoveCursor, 'MoveUp', 'Cursor up', 'Cursor up.', ('0', 'max', -1)),
            (OK_Btn, 'OK_Btn', 'OK', 'OK button pressed.', None),
            (Cancel_Btn, 'Cancel_Btn', 'Cancel', 'Cancel button pressed.', None),
        )),
    )),
)
