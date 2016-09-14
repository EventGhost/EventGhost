# -*- coding: utf-8 -*-

version="0.1.6"

# plugins/ScreamerRadio/__init__.py
#
# Copyright (C)  2008 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
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

eg.RegisterPlugin(
    name = "Screamer Radio",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{22D52B5E-D1D9-4352-AC53-A620441C67CC}",
    description = (
        'Adds actions to control the <a href="http://www.screamer-radio.com/">'
        'Screamer radio</a>.'
    ),
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=840",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAACuEALHOgfL"
        "WiLTbzX6xmX/337/5m//2Vv/00n+szDXZAf3rFL/2Wn/zSnxoAT/8s7/5JT/xQz/6Kr/"
        "tQL9vlL/+/T/mQH/15r/hQHWTQL/nDT/umz/jBT2dwDugQAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABhZgQHtjQAF2QA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA+vbaVAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAK1JREFUeNpNj1kShCAMBQE3"
        "QIOALAbBuf8tJy5TNe+vO6ksjF3housEZ7/wfhgnqfT8Kr5ME0gJ0qz8ZRgtKOWcv01P"
        "ZWsVjH6TYaaGKJVLYMwIfguZM6GUTM4Y713YdRasM8ZaQh9ADxELKwbSzSHquKBgwrsk"
        "AyXHox4k+BogbTrnXFttJ+2dQ9bWVmztWGgE7f2s2GraERuez6lnRjwq4stkyokXlr9/"
        "BeXBL7jEDHFjtSheAAAAAElFTkSuQmCC"
    ),
)

# Changelog:
# ==============================================================================
# 2008-05-06 Pako
#     * initial version 0.1.0
# 2008-05-07 Pako
#     * only little enhancement
#     * increased version to 0.1.2
# 2008-05-07 Pako
#     * fix SetVolume action
#     * increased version to 0.1.3
# 2008-07-29 Pako
#     * now uses AddActionsFromList
#     * add "On screeen menu" for choice of favorite
#     * increased version to 0.1.4
# 2008-09-01 Pako
#     * add option Start/Stop Event Sender
#     * increased version to 0.1.5
# 2010-07-19 Pako
#     * bugfix (UnicodeEncodeError when non-ascii filepath)
#     * guid attribute added
#     * increased version to 0.1.6
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl non-editable !!!
        return self.textControl     #
#===============================================================================

class Text:
    label1 = "Path to screamer.exe:"
    label2 = "Path to Start_SR_Events.exe and Stop_SR_Events.exe:"
    filemask = "screamer.exe|screamer.exe|All-Files (*.*)|*.*"
    text1 = "Couldn't find Screamer Radio window !"
    text2 = "Couldn't find file %s !"
    lbl_start_stop = 'Activate/deactivate event sender by actions "Run or restore/Exit"'
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = 'Folder "%s" is incorrect'
    boxMessage1 = 'Missing file %s !'
    boxMessage2 = 'Missing file %s or %s !'


import os
import xml.sax as sax
from xml.sax.handler import ContentHandler
from threading import Thread
from time import sleep
from win32gui import GetWindowText, MessageBox
from win32api import ShellExecute,GetSystemMetrics
from eg.WinApi import SendMessageTimeout
from eg.WinApi.Dynamic import PostMessage

BM_CLICK      = 245
WM_COMMAND    = 273
WM_SYSCOMMAND = 274
TBM_GETPOS    = 1024
SC_MINIMIZE   = 61472
SC_CLOSE      = 61536
SC_RESTORE    = 61728


def FindWindowFunction(key,case,match):
    return eg.WindowMatcher(
                u'screamer.exe',
                None,
                u'#32770',
                key,
                case,
                match,
                True,
                0.0,
                0
            )

def Handle():
    FindWindow = FindWindowFunction(None,None,1)
    hwnds = FindWindow()
    if len(hwnds) > 0:
        if GetWindowText(hwnds[0]) == "Screamer Log":
            FindWindow = FindWindowFunction(None,None,2)
            hwnds = FindWindow()
    return hwnds


#my xmlhandler1
class my_xml_handler1(ContentHandler):
    def startDocument( self):
        self.document = {}
        self._recent_text = ''

    def endElement( self, name):
        if name=="LanguageFile":
            self.document[name] = self._recent_text.strip()
        if name=="NotPlaying":
            self.document[name] = self._recent_text.strip()
        for item in Actions:
            if name==item[1]:
                self.document[name] = self._recent_text.strip()
                break
        self._recent_text = ''

    def characters( self, content):
        self._recent_text += content


#my xmlhandler2
class my_xml_handler2(ContentHandler):

    def startDocument(self):
        self.favList = ScreamerRadio.favList = []

    def startElement(self, name, attrs):
        if name == "Station":
            temp = attrs.get("title")
            self.favList.append(temp)

#===============================================================================
class ScreamerRadio(eg.PluginClass):
    text=Text
    ScreamerPath = None
    path2 = None
    menuDlg = None
    fav_num = 0

    def Execute(self, exe, path):
        try:
            res = ShellExecute(
                0,
                None,
                exe,
                None,
                path,
                1
            )
        except:
            res = None
            self.PrintError(self.text.text2 % exe)
        return res

    def PlayFavFromMenu(self):
        if self.menuDlg is not None:
            sel=self.menuDlg.GetSizer().GetChildren()[0].GetWindow().\
                GetSelection()

        self.fav_num=sel
        self.menuDlg.Close()  #
        hwnds = Handle()
        if len(hwnds) > 0:
            if sel <= len(self.favList)-1:
                PostMessage(hwnds[0], WM_COMMAND, 9217+sel, 0)
        else:
            self.PrintError(self.text.text1)



    def __init__(self):
        text=Text
        favList=[]
        self.AddActionsFromList(Actions)

    def __start__(self, ScreamerPath, path2 = None):
        self.ScreamerPath = ScreamerPath
        self.path2 = path2
        xmltoparse = ScreamerPath+'\\screamer.xml'
        self.dh = my_xml_handler1()
        sax.parse(xmltoparse.encode(eg.systemEncoding), self.dh)
        xmltoparse = self.dh.document['LanguageFile']
        sax.parse(xmltoparse.encode(eg.systemEncoding), self.dh)

    def Configure(self, ScreamerPath=None, path2 = None):
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        filepathCtrl = MyDirBrowseButton(
            panel,
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )

        filepathCtrl.GetTextCtrl().SetEditable(False)
        checkBoxCtrl = wx.CheckBox(panel, label="  "+self.text.lbl_start_stop)
        if ScreamerPath is None:
            ScreamerPath = eg.folderPath.ProgramFiles+'\\Screamer'
            filepathCtrl.SetValue("")
        else:
            filepathCtrl.SetValue(ScreamerPath)
        filepathCtrl.startDirectory = ScreamerPath
        if path2:
            checkBoxCtrl.SetValue(True)
            startDir = path2
        else:
        #    checkBoxCtrl.SetValue(False)
            startDir = ScreamerPath
        startStopPathCtrl = MyDirBrowseButton(
            panel,
            size=(410,-1),

            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            startDirectory=startDir,
            buttonText=eg.text.General.browse
        )
        startStopPathCtrl.GetTextCtrl().SetEditable(False)
        startStopPathCtrl.SetValue(startDir)
        sizerAdd = panel.sizer.Add
        sizerAdd(label1Text, 0, wx.TOP,15)
        sizerAdd(filepathCtrl,0,wx.TOP,3)
        sizerAdd(checkBoxCtrl,0,wx.TOP,30)
        sizerAdd(label2Text,0,wx.TOP,15)
        sizerAdd(startStopPathCtrl,0,wx.TOP,3)
        def OnCheckBox(event = None):
            flag = checkBoxCtrl.GetValue()
            if not flag:
                startStopPathCtrl.SetValue("")
                if event:
                    event.Skip()
            else:
                if event:
                    startStopPathCtrl.OnBrowse()
                    if startStopPathCtrl.GetValue() =="":
                        flag = False
            checkBoxCtrl.SetValue(flag)
            label2Text.Enable(flag)
            startStopPathCtrl.Enable(flag)
        checkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        OnCheckBox()

        def OnPathChange(event = None):
            path = filepathCtrl.GetValue()
            path2 = startStopPathCtrl.GetValue()
            flag0 = os.path.exists(path+"\\screamer.exe")
            if path2 != "":
                flag1 = os.path.exists(path2+"\\Start_SR_Events.exe")
                flag2 = os.path.exists(path2+"\\Stop_SR_Events.exe")
                flag = flag0 and flag1 and flag2
            else:
                flag = flag0
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)
            if event and not flag0:
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % 'screamer.exe',
                    self.text.boxTitle % path,
                        0
                    )
            if path != "":
                filepathCtrl.startDirectory = path
        filepathCtrl.Bind(wx.EVT_TEXT,OnPathChange)
        OnPathChange()

        def OnPath2Change(event = None):
            path = filepathCtrl.GetValue()
            path2 = startStopPathCtrl.GetValue()
            flag0 = os.path.exists(path+"\\screamer.exe")
            if checkBoxCtrl.GetValue():
                flag1 = os.path.exists(path2+"\\Start_SR_Events.exe")
                flag2 = os.path.exists(path2+"\\Stop_SR_Events.exe")
                flag = flag1 and flag2
                if event and not flag:
                    MessageBox(
                        panel.GetHandle(),
                        self.text.boxMessage2 % (
                            'Start_SR_Events.exe',
                            'Stop_SR_Events.exe'
                        ),
                        self.text.boxTitle % path2,
                        0
                    )
                startStopPathCtrl.startDirectory = path2
            else:
                flag = True
            flg = flag and flag0
            panel.dialog.buttonRow.okButton.Enable(flg)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flg)
        startStopPathCtrl.Bind(wx.EVT_TEXT,OnPath2Change)
        OnPath2Change()

        while panel.Affirmed():
            if checkBoxCtrl.GetValue():
                startStopPath = startStopPathCtrl.GetValue()
            else:
                startStopPath =None
            panel.SetResult(filepathCtrl.GetValue(),
            startStopPath,
            )
#===============================================================================
#cls types for Actions list:
#===============================================================================
class Run(eg.ActionClass):
    class text:
        play = "Automatic play selected favorite after start"
        label = "Select favorite:"
        over = "Too large number (%s > %s) !"
        alt_ret = "No autostart"

    def __call__(self, play=False, fav = 1):
        flag = self.plugin.Execute('screamer.exe',self.plugin.ScreamerPath)
        if self.plugin.path2:
            self.plugin.Execute('Start_SR_Events.exe',self.plugin.path2)

        if flag:
                if self.plugin.path2:
                    self.plugin.Execute('Start_SR_Events.exe',self.plugin.path2)
                if play:
                    for n in range(50):
                        sleep(.2)
                        hwnds = Handle()
                        if len(hwnds) > 0:
                            flag = False
                            break
                    if not flag:
                        sleep(2)
                        ScreamerPath = self.plugin.ScreamerPath
                        xmltoparse = ScreamerPath+'\\favorites.xml'
                        self.dh2 = my_xml_handler2()
                        sax.parse(xmltoparse.encode(eg.systemEncoding), self.dh2)
                        if fav <= len(self.plugin.favList):
                            self.plugin.fav_num=fav-1
                            PostMessage(hwnds[0], WM_COMMAND, 9216+fav, 0)
                            return str(fav)+": "+self.plugin.favList[self.plugin.fav_num]
                        else:
                            return self.text.over % (str(fav),\
                                str(len(self.plugin.favList)))
                    else:
                        return self.plugin.text.text1
                else:
                    return self.text.alt_ret


    def Configure(self, play=False, fav=1):
        panel=eg.ConfigPanel(self)
        sizerAdd=panel.sizer.Add
        playChkBoxCtrl = wx.CheckBox(panel, label=self.text.play)
        sizerAdd(playChkBoxCtrl,0,wx.TOP,15)
        playChkBoxCtrl.SetValue(play)
        favLbl=wx.StaticText(panel, -1, self.text.label)
        sizerAdd(favLbl,0,wx.TOP,25)
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=999,
        )
        favCtrl.SetValue(fav)
        sizerAdd(favCtrl,0,wx.TOP,5)
        def OnAutostart(evt=None):
            enbl=playChkBoxCtrl.GetValue()
            favLbl.Enable(enbl)
            favCtrl.Enable(enbl)
            if evt is not None:
                evt.Skip()
        playChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnAutostart)
        OnAutostart()

        while panel.Affirmed():
            panel.SetResult(
                playChkBoxCtrl.GetValue(),
                favCtrl.GetValue()
            )

#===============================================================================
class WindowControl(eg.ActionClass):
    def __call__(self):
        hwnds = Handle()
        if len(hwnds) > 0:
            SendMessageTimeout(
                hwnds[0], WM_SYSCOMMAND, self.value, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1


#===============================================================================
class Close(eg.ActionClass):
    def __call__(self):
        hwnds = Handle()
        if len(hwnds) > 0:
            SendMessageTimeout(
                hwnds[0], WM_SYSCOMMAND, self.value, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
        if self.plugin.path2:
            self.plugin.Execute('Stop_SR_Events.exe',self.plugin.path2)


#===============================================================================
class PlayStop(eg.ActionClass):
    def __call__(self):
        key = self.plugin.dh.document['NotPlaying']
        FindWindow = FindWindowFunction(key,u'Static',1)
        hwnds = FindWindow()
        if len(hwnds) > 0: #Not playing
            key = eval("self.plugin.dh.document[self.value[0]]")
            ret = "1"
        else:              #Playing
            key = eval("self.plugin.dh.document[self.value[1]]")
            ret = "0"
        FindWindow = FindWindowFunction(key,u'Button',1)
        hwnds = FindWindow()
        if len(hwnds) != 0:
            SendMessageTimeout(hwnds[0], BM_CLICK, 0, 0)
            return ret
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1


#===============================================================================
class OtherActions(eg.ActionClass):
    def __call__(self):
        key = eval("self.plugin.dh.document[self.value[0]]")
        FindWindow = FindWindowFunction(key,u'Button',1)
        hwnds = FindWindow()
        if self.value[1] != "": #for toggle actions
            ret = "0"
            if len(hwnds) == 0:
                key = eval("self.plugin.dh.document[self.value[1]]")
                FindWindow = FindWindowFunction(key,u'Button',1)
                hwnds = FindWindow()
                ret = "1"
        else:
            ret = " "
        if len(hwnds) != 0:
            SendMessageTimeout(hwnds[0], BM_CLICK, 0, 0)
            return ret
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1

#===============================================================================
class VolumeUpDown(eg.ActionClass):
    def __call__(self):
        FindWindow = FindWindowFunction(u'Slider1',u'msctls_trackbar32',1)
        hwnds = FindWindow()
        if len(hwnds) != 0:
            volume=SendMessageTimeout(hwnds[0], TBM_GETPOS, 0, 0)
            if eval(self.value[0]):
                eg.SendKeys(hwnds[0], self.value[1], False)
                #PostMessage(hwnds[0], TBM_SETPOS, 1, volume-1)
            else:
                volume=self.value[2]
            return 100-5*(volume+self.value[3])
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1

#===============================================================================
class SetVolume(eg.ActionClass):
    class text:
        label="Set volume (0-100%):"

    def __call__(self,volume):
        FindWindow = FindWindowFunction(u'Slider1',u'msctls_trackbar32',1)
        hwnds = FindWindow()
        if len(hwnds) != 0:
            vol=SendMessageTimeout(hwnds[0], TBM_GETPOS, 0, 0)
            step = -20+vol+volume/5
            if step<>0:
                key = u'{Up}' if step>0 else u'{Down}'
                for n in range(abs(step)):
                    eg.SendKeys(hwnds[0], key, False)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1

    def Configure(self, volume=100):
        panel=eg.ConfigPanel(self)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.label))
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            volume,
            fractionWidth=0,
            increment=5,
            min=0,
            max=100,
            style=wx.TE_READONLY,
        )
        volumeCtrl.SetValue(volume)
        panel.sizer.Add(volumeCtrl,0,wx.TOP,10)

        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())


#===============================================================================
class GetVolume(eg.ActionClass):
    def __call__(self):
        FindWindow = FindWindowFunction(u'Slider1',u'msctls_trackbar32',1)
        hwnds = FindWindow()
        if len(hwnds) != 0:
            return 100-5*SendMessageTimeout(hwnds[0], TBM_GETPOS, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1


#===============================================================================
class SelectFav(eg.ActionClass):
    class text:
        label="Select favorite:"
        over = "Too large number (%s > %s) !"
    def __call__(self,fav=1):
        hwnds = Handle()
        if len(hwnds) > 0:
            ScreamerPath = self.plugin.ScreamerPath
            xmltoparse = ScreamerPath+'\\favorites.xml'
            self.dh2 = my_xml_handler2()
            sax.parse(xmltoparse.encode(eg.systemEncoding), self.dh2)
            if fav <= len(self.plugin.favList):
                self.plugin.fav_num=fav-1
                PostMessage(hwnds[0], WM_COMMAND, 9216+fav, 0)
                return str(fav)+": "+self.plugin.favList[self.plugin.fav_num]
            else:
                self.PrintError(
                    self.text.over % (str(fav),str(len(self.plugin.favList))))
                return self.text.over % (str(fav),str(len(self.plugin.favList)))
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1

    def GetLabel(self, fav):
        return self.name+' '+str(fav)

    def Configure(self, fav=1):
        panel=eg.ConfigPanel(self)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.label))
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=999,
        )
        favCtrl.SetValue(fav)
        panel.sizer.Add(favCtrl,0,wx.TOP,10)

        while panel.Affirmed():
            panel.SetResult(favCtrl.GetValue())

#===============================================================================
class NextPrevFav(eg.ActionClass):
    def __call__(self):
        hwnds = Handle()
        if len(hwnds) > 0:
            ScreamerPath = self.plugin.ScreamerPath
            xmltoparse = ScreamerPath+'\\favorites.xml'
            self.dh2 = my_xml_handler2()
            sax.parse(xmltoparse.encode(eg.systemEncoding), self.dh2)
            if eval(self.value[2]):
                self.plugin.fav_num += self.value[0]
            else:
                self.plugin.fav_num = eval(self.value[1])
            PostMessage(hwnds[0], WM_COMMAND, 9217+self.plugin.fav_num, 0)
            num = self.plugin.fav_num
            return (str(num+1)+": "+self.plugin.favList[num])
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1

#===============================================================================
class GetPlayingTitle(eg.ActionClass):
    def __call__(self):
        hwnds = Handle()
        if len(hwnds) > 0:
            return GetWindowText(hwnds[0])
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
                listBoxCtrl = event.GetEventObject().GetParent().GetSizer().\
                    GetChildren()[0].GetSizer(). GetChildren()[1].GetWindow()
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

#===============================================================================
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
                listBoxCtrl = event.GetEventObject().GetParent().GetSizer().\
                    GetChildren()[0].GetSizer(). GetChildren()[1].GetWindow()
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


    def __call__(
        self,
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None

    ):
        self.Show_OSM(fore,back,fontInfo,False)

    def Show_OSM(
        self,
        fore,
        back,
        fontInfo,
        flag
    ):

        if self.plugin.menuDlg is not None:
            return
        self.fore = fore
        self.back = back
        self.flag = flag

        ScreamerPath = self.plugin.ScreamerPath
        xmltoparse = ScreamerPath+'\\favorites.xml'
        self.dh2 = my_xml_handler2()
        sax.parse(xmltoparse.encode(eg.systemEncoding), self.dh2)
        choices = self.plugin.favList

        self.plugin.menuDlg = wx.Frame(
                None, -1, 'OS_Menu',
                style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER
            )
        favChoiceCtrl=wx.ListBox(
            self.plugin.menuDlg,
            choices = choices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )

        if fontInfo is None:
            font = favChoiceCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        favChoiceCtrl.SetFont(font)
        # menu height calculation:
        h=favChoiceCtrl.GetCharHeight()
        height0 = len(choices)*h+5
        height1 = h*((GetSystemMetrics (1)-20)/h)+5
        height = min(height0,height1)
        # menu width calculation:
        width_lst=[]
        for item in choices:
            width_lst.append(favChoiceCtrl.GetTextExtent(item+' ')[0])
        width = max(width_lst)+8
        if height<height0:
            width += 20 #for vertical scrollbar
        width = min((width,GetSystemMetrics (0)-50))
        self.plugin.menuDlg.SetSize((width+6,height+6))
        favChoiceCtrl.SetDimensions(2,2,width,height,wx.SIZE_AUTO)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        self.plugin.menuDlg.SetSizer(mainSizer)
        favChoiceCtrl.SetSelection(self.plugin.fav_num)
        self.plugin.menuDlg.SetBackgroundColour((0,0,0))
        favChoiceCtrl.SetBackgroundColour(self.back)
        favChoiceCtrl.SetForegroundColour(self.fore)
        mainSizer.Add(favChoiceCtrl, 0, wx.EXPAND)


        def OnClose(evt):
            self.plugin.menuDlg = None
            evt.Skip()
        self.plugin.menuDlg.Bind(wx.EVT_CLOSE, OnClose)


        def On2Click(evt):
            if self.plugin.menuDlg is not None:
                self.plugin.PlayFavFromMenu()
                evt.Skip()
        favChoiceCtrl.Bind(wx.EVT_LISTBOX_DCLICK, On2Click)
        self.plugin.menuDlg.Centre()
        if self.flag:
            cm=self.CloseMenu(self.plugin.menuDlg)
            cm.start()
        self.plugin.menuDlg.Show()
#===============================================================================
    class CloseMenu(Thread):

        def __init__(self,dlg):
            Thread.__init__(self)
            self.dlg = dlg

        def run(self):
            sleep(5)
            try:
                self.dlg.Close() #
            except:
                pass

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

        ScreamerPath = self.plugin.ScreamerPath
        xmltoparse = ScreamerPath+'\\favorites.xml'
        self.dh2 = my_xml_handler2()
        sax.parse(xmltoparse.encode(eg.systemEncoding), self.dh2)
        choices = self.plugin.favList
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

        def OnClick(evt):
            listBoxCtrl.SetSelection(-1)
            evt.StopPropagation()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, OnClick)


        # re-assign the test button
        def OnButton(event):
            self.Show_OSM(
                foreColourButton.GetValue(),
                backColourButton.GetValue(),
                fontButton.GetValue(),
                True
            )
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
            max=len(self.plugin.favList)
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
            self.plugin.PlayFavFromMenu()

#===============================================================================
class Cancel_Btn(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            self.plugin.menuDlg.Close()

#===============================================================================
Actions = (
    (Run,"Run","Run Screamer","Run Screamer with its default settings.",None),
    (WindowControl,"Minimize","Minimize window","Minimize window.",SC_MINIMIZE),
    (WindowControl,"Restore","Restore window","Restore window.",SC_RESTORE),
    (Close,"Close","Close window","Close window.",SC_CLOSE),
    (OtherActions,"Play","Play","Play last playing station.",("Play","")),
    (OtherActions,"Stop","Stop","Stop.",("Stop","")),
    (PlayStop,"PlayStop","Play/Stop","Play/Stop.",("Play","Stop")),
    (OtherActions,"Next","Next stream","Next stream.",("Next","")),
    (OtherActions,"Prev","Previous stream","Previous stream.",("Prev","")),
    (OtherActions,"RecOff","Rec on","Rec on.",("RecOff","")),
    (OtherActions,"RecOn","Rec off","Rec off.",("RecOn","")),
    (OtherActions,"RecOnOff","Rec On/Off","Rec On/Off.",("RecOn","RecOff")),
    (OtherActions,"MuteOff","Mute on","Mute on.",("MuteOff","")),
    (OtherActions,"MuteOn","Mute off","Mute off.",("MuteOn","")),
    (OtherActions,"MuteOnOff","Mute On/Off","Mute On/Off.",("MuteOn","MuteOff")),
    (VolumeUpDown,"VolumeUp","Volume up","Volume up.", ('volume > 0',u'{Up}',1,-1)),
    (VolumeUpDown,"VolumeDown","Volume down","Volume down.", ('volume < 20',u'{Down}',19,1)),
    (SetVolume,"SetVolume","Set volume","Set volume.", None),
    (GetVolume,"GetVolume","Get volume","Get volume.", None),
    ( eg.ActionGroup, 'Favorites', 'Favorites', 'Favorites',(
        (SelectFav,"SelectFav","Select favorite","Select favorite by order.", None),
        (NextPrevFav,"NextFav","Next favorite","Next favorite.", (1, '0', 'self.plugin.fav_num < len(self.plugin.favList)-1')),
        (NextPrevFav,"PreviousFav","Previous favorite","Previous favorite.", (-1, 'len(self.plugin.favList)-1', 'self.plugin.fav_num < (len(self.plugin.favList)-1) and self.plugin.fav_num>0')),
        (GetPlayingTitle,"GetPlayingTitle","Get currently playing title","Gets the name of currently playing title.", None),
        ( eg.ActionGroup, 'Menu', 'Menu', 'Menu',(
            (ShowMenu, 'ShowMenu', 'Show menu', 'Show on screen menu.', None),
            (MoveCursor, 'MoveDown', 'Cursor down', 'Cursor down.', ('max-1', '-1', 1)),
            (MoveCursor, 'MoveUp', 'Cursor up', 'Cursor up.', ('0', 'max', -1)),
            (OK_Btn, 'OK_Btn', 'OK', 'OK button pressed.', None),
            (Cancel_Btn, 'Cancel_Btn', 'Cancel', 'Cancel button pressed.', None),
        )),
    )),
)


