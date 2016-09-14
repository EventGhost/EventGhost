# -*- coding: utf-8 -*-

version="0.3.5"

# Plugins/Billy/__init__.py
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
    name = "Billy Player",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{12CD9AEB-691F-4EBB-B1F5-10A5FF776429}",
    description = (
        'Adds actions to control the <a href="http://www.sheepfriends.com/?page'
        '=billy">Billy</a> audio player. \n\n<p>'
        '<BR><B>ATTENTION !<BR>Properly works only for beta version 1.04b of Bi'
        'lly !</B>'
        '<BR>The plugin will work with older versions of Billy only in limited '
        'mode!</p>'
    ),
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=537",
    icon = (
        "R0lGODlhEAAQAPcAAAQCBMz+tPz+/AAAABkEFSEAAAAAAAAAAGECDR4AAAAAAAAAAAAADQ"
        "AAABUAAAAAAA0AyAAAHgAAEAAAagAAXQIABAAAhQAAAwAAFwMAAAAAAAAAAIgBAeIAABIA"
        "AAAAAOkaGeUAAIEAAHwAAAAAEQAAAAEAAAAAAFYA0QAAOQAAJQAAW5AVhOEAABIAAAAAAH"
        "MViAAAFgAAKAAAW7ANFeIAABIAAAAAABgNTe4AAJAAAHwAAHDIlQUeOZEQJXxqW/9dYP8E"
        "QP+FOP8DAG0X/gUAEZEAHnwAAIUBUOcAQIEAOHwAAAAZ2wAAGhUAJQAAW1gR/AMA8gAAEg"
        "AAAHABEIUA9xkARQAAAIgHhEIAABUAAAAAAAAI/gAAEQAAHgAAAH4JhAAAAAAAAMAAAAAi"
        "AAAcAAABAACSAP8ATf8AAP8Awf8AAP+IBP/jAP8SAP8AAADQ4gA8BAAlAABbAABIcQBB1Q"
        "A4NgAAfgBNAAAAABUAAAAAAMDBYOIAnhIAgAAAfNJI+ObkVIESFnwAAIhGAELQABUmAABb"
        "AEpIB+NBAIE4AHwAAMAFAHYAAFAAAAAAAIj+AEIRUAEeFgAAAGtQAABAAAA4AAAAAPyJAO"
        "FaABIAAAAAAADYAADjAAASAAAAAPiFAPcrABKDAAB8ABgAaO4AnpAAgHwAfHAA/wUA/5EA"
        "/3wA//8AYP8Anv8AgP8AfG0pIAW3AJGSAHx8AEr4IPRUAIAWAHwAAAA0SABk6xWDEgB8AA"
        "D//wD//wD//wD//4gAAEIAABUAAAAAAAC8BAHj5QASEgAAAAA0vgBkOwCDTAB8AFf45PT3"
        "5IASEnwAAOgYd+PuEBKQTwB8AIgAGEK35RWSEgB8ABH/NAD/ZAD/gwD/fAT4qABU5QAWEg"
        "AAAAM03gBk/wCD/wB8fwAAiADl5QASEgAAAADn+ABkVACDFgB8AASINABkZACDgwB8fAMB"
        "+AAAVAAAFgAAAAAxiQAAWgAAAAAAAAAAAAAAAAAAAAAAAAoA6QAAzgAARwAAACH5BAEAAA"
        "IALAAAAAAQABAABwhEAAUIHEiwoMGDBgEoXMhQIUEAASJKnAjg4cSLASoOhIhRokaBHDtm"
        "tChy5MaSJkGi/CggZEeWLjHCXPmwoU2EOHMeDAgAOw=="
    ),
)

import os
from shutil import copyfile
from win32gui import GetWindowText, MessageBox
from threading import Thread
from time import sleep
from win32api import ShellExecute,GetSystemMetrics

FindBilly = eg.WindowMatcher(
    u'Billy.exe',
    u'{*}Billy{*}',
    u'TAppBilly',
    None,
    None,
    1,
    True,
    0.0,
    0
)

#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl non-editable !!!
        return self.textControl     #


class Text:
  #  filemask = "Billy.exe|Billy.exe|All-Files (*.*)|*.*"
    label1 = "Path to Billy.exe:"
    label2 = "Path to Start_Billy_Events.exe and Stop_Billy_Events.exe:"
    text0="Couldn't find file Stop_Billy_Events.exe !"
    text1 = "Couldn't find Billy window !"
    text2 = "Couldn't find file %s !"
    lbl_start_stop = 'Activate/deactivate event sender by actions "Run or restore/Exit"'
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = 'Folder "%s" is incorrect'
    boxMessage1 = 'Missing file %s !'
    boxMessage2 = 'Missing file %s or %s !'
#===============================================================================

class Billy(eg.PluginClass):

    text=Text
    BillyPath = None
    path2 = None
    menuDlg = None
    play = True
    force = False
    fav_path = ""

    def Execute(self, exe, path):
        try:
            ShellExecute(
                0,
                None,
                exe,
                None,
                path,
                1
            )
        except:
            self.PrintError(self.text.text2 % exe)

    def PlayFavFromMenu(self):
        dir = self.BillyPath+'\\Favorites'
        dirpath = self.fav_path
        template = dir+'\\%s'

        files = os.listdir(dirpath)
        tmpList = []
        for item in files:
            if item[-4:].lower() in ('.txt', '.m3u', '.pls'):
                tmpList.append(item)
        tmpList.sort()

        if os.path.isfile(template % '!!!!!!!!') :
            os.remove(template % '!!!!!!!!')

        if self.menuDlg is not None:
            sel=self.menuDlg.GetSizer().GetChildren()[0].GetWindow().\
                GetSelection()

        else:
            pass
        keys = u'{Ctrl+%s}' % chr(sel+49)
        self.menuDlg.Close()  #

        #Status "playnig/paused" OR "stopped" ???
        hwnds = FindBilly()
        if len(hwnds) != 0:
            strBillyTitle = GetWindowText(hwnds[0])
            if strBillyTitle[-8:] == ' - Billy':
                playing = True
            else:
                playing = False

            if self.force:
                eg.SendKeys(hwnds[0], '{0}{0}', True)    #Stop current playing track

            if sel < 9 and dirpath == dir:  # 0 ... 8
                eg.SendKeys(hwnds[0], keys, False)
            else:
                copyfile(dirpath+'\\'+tmpList[sel], template % '!!!!!!!!.txt')
                eg.SendKeys(hwnds[0], u'{Ctrl+1}', True) #Load Favorite 1 = Selected Playlist
                os.remove(template % '!!!!!!!!.txt')     #Delete temporary file !!!!!!!!.txt

            if (self.force and playing) or (self.play and not playing):
                sleep(0.5)
                eg.SendKeys(hwnds[0], u'{Space}', True)  #Play track from new playlist
        else:
            self.PrintError(self.text.text1)

    def __init__(self):
        text=Text
        self.AddActionsFromList(ACTIONS)

    def __start__(self, BillyPath=None, path2 = None):
        self.BillyPath = BillyPath
        self.path2 = path2

    def Configure(self, BillyPath=None, path2 = None):
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
        if BillyPath is None:
            BillyPath = eg.folderPath.ProgramFiles+'\\Billy'
            filepathCtrl.SetValue("")
        else:
            filepathCtrl.SetValue(BillyPath)
        filepathCtrl.startDirectory = BillyPath
        if path2:
            checkBoxCtrl.SetValue(True)
            startDir = path2
        else:
        #    checkBoxCtrl.SetValue(False)
            startDir = BillyPath
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
            flag0 = os.path.exists(path+"\\Billy.exe")
            if path2 != "":
                flag1 = os.path.exists(path2+"\\Start_Billy_Events.exe")
                flag2 = os.path.exists(path2+"\\Stop_Billy_Events.exe")
                flag = flag0 and flag1 and flag2
            else:
                flag = flag0
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)
            if event and not flag0:
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % 'Billy.exe',
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
            flag0 = os.path.exists(path+"\\Billy.exe")
            if checkBoxCtrl.GetValue():
                flag1 = os.path.exists(path2+"\\Start_Billy_Events.exe")
                flag2 = os.path.exists(path2+"\\Stop_Billy_Events.exe")
                flag = flag1 and flag2
                if event and not flag:
                    MessageBox(
                        panel.GetHandle(),
                        self.text.boxMessage2 % (
                            'Start_Billy_Events.exe',
                            'Stop_Billy_Events.exe'
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

class Run(eg.ActionClass):

    def __call__(self, start = True, startPath = ""):
        self.plugin.Execute('Billy.exe',self.plugin.BillyPath)
        if self.plugin.path2:
            self.plugin.Execute('Start_Billy_Events.exe',self.plugin.path2)
#===============================================================================

class Exit(eg.ActionClass):

    def __call__(self, stop = False):
        hwnds = FindBilly()
        if len(hwnds) != 0:
            eg.SendKeys(hwnds[0], self.value, True)
        else:
            self.PrintError(self.plugin.text.text1)
        if self.plugin.path2:
            self.plugin.Execute('Stop_Billy_Events.exe',self.plugin.path2)
#===============================================================================

class HotKeyAction(eg.ActionClass):
    def __call__(self):
        hwnds = FindBilly()
        if len(hwnds) != 0:
            eg.SendKeys(hwnds[0], self.value, True)
        else:
            self.PrintError(self.plugin.text.text1)
#===============================================================================

# new since 0.3.3:
class GetPlayingFile(eg.ActionClass):

    def __call__(self):
        strBillyTitle = ""
        hwnds = FindBilly()
        if ( hwnds is not None ):
            strBillyTitle = GetWindowText(hwnds[0])
            strBillyTitle = strBillyTitle.replace(" - Billy", "")
        return strBillyTitle
#===============================================================================

class ShowMenu(eg.ActionClass):
    panel = None
    testFlag = False

    class text:
        menuPreview = 'On screen menu preview:'
        menuFont = 'Menu font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        play_label = 'If Billy is stoped, after loading of playlist start play'
        force_label = 'If Billy is playing or paused, interrupt and immediately start new playlist'
        radioPath = 'Folder with playlists/favorites'
        standard = 'Standard (..\\Billy\\Favorites)'
        user = 'User defined'
        dir_err = "Couldn't find Favorites folder !"
        pathdir_err = "Couldn't find folder %s !"
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
                    GetChildren()[0].GetSizer().GetChildren()[0].GetSizer().\
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
                    GetChildren()[0].GetSizer().GetChildren()[0].GetSizer().\
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


    def __call__(
        self,
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None,
        play = True,
        force = False,
        folder = False,
        dirpath = ""

    ):

        if self.plugin.menuDlg is not None:
            return
        if dirpath == "":
            dirpath = self.plugin.BillyPath+'\\Favorites'
        if not os.path.exists(dirpath):
            self.PrintError(self.text.pathdir_err % dirpath)
            return

        self.plugin.play = play
        self.plugin.force = force
        self.plugin.fav_path = dirpath
        self.fore = fore
        self.back = back

        files = os.listdir(dirpath)
        choices = []
        for item in files:
            if item[-4:].lower() in ('.txt', '.m3u', '.pls'):

                choices.append(item[:-4])
        choices.sort()
        self.plugin.favList = choices #

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
        if height < height0:
            width += 20 #for vertical scrollbar
        width = min((width,GetSystemMetrics (0)-50))
        self.plugin.menuDlg.SetSize((width+6,height+6))
        favChoiceCtrl.SetDimensions(2,2,width,height,wx.SIZE_AUTO)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        self.plugin.menuDlg.SetSizer(mainSizer)
        favChoiceCtrl.SetSelection(0)
        self.plugin.menuDlg.SetBackgroundColour((0,0,0))
        favChoiceCtrl.SetBackgroundColour(self.back)
        favChoiceCtrl.SetForegroundColour(self.fore)
        mainSizer.Add(favChoiceCtrl, 0, wx.EXPAND)

        def OnClose(evt):
            self.plugin.menuDlg = None
            self.testFlag = False
            evt.Skip()
        self.plugin.menuDlg.Bind(wx.EVT_CLOSE, OnClose)

        def On2Click(evt):
            if self.plugin.menuDlg is not None:
                self.plugin.PlayFavFromMenu()
                evt.StopPropagation()
        favChoiceCtrl.Bind(wx.EVT_LISTBOX_DCLICK, On2Click)

        self.plugin.menuDlg.Centre()
        if self.testFlag:
            pass
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
        play,
        force,
        folder,
        dirpath
    ):
        return self.name+" "+dirpath

    def Configure(
        self,
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None,
        play = True,
        force = False,
        folder = False,
        dirpath = ""
    ):

#        class MyDirBrowseButton(eg.DirBrowseButton):
#            def GetTextCtrl(self):          #  now I can make build-in textCtrl non-editable !!!
#                return self.textControl     #

        dir = self.plugin.BillyPath+'\\Favorites'
        if not os.path.exists(dir):
            self.PrintError(self.text.dir_err)
            return
#        files = os.listdir(dir)
        if not os.path.exists(dirpath):
            dirpath = dir
        files = os.listdir(dirpath)
        choices = []
        for item in files:
            if item[-4:].lower() in ('.txt', '.m3u', '.pls'):
                choices.append(item[:-4])
        choices.sort()
        self.plugin.favList = choices #

        self.fore = fore
        self.back = back
        self.oldSel=0

    #Controls
        global panel
        panel = eg.ConfigPanel(self)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
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
        w1 = panel.GetTextExtent(self.text.menuFont)[0]
        w2 = panel.GetTextExtent(self.text.txtColour+':')[0]
        w3 = panel.GetTextExtent(self.text.background+':')[0]
        w = max(w1,w2,w3)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(400-w,130),
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
        playCtrl = wx.CheckBox(panel, -1, '  '+self.text.play_label)
        playCtrl.SetValue(play)
        forceCtrl = wx.CheckBox(panel, -1, '  '+self.text.force_label)
        forceCtrl.SetValue(force)
        rb1 = panel.RadioButton(not folder, self.text.standard, style=wx.RB_GROUP)
        rb2 = panel.RadioButton(folder, self.text.user)
        dirpathCtrl = MyDirBrowseButton(
            panel,
            -1,
            size=(410,-1),
            toolTip = self.plugin.text.toolTipFolder,
            dialogTitle = self.plugin.text.browseTitle,
            startDirectory=dirpath,
            labelText="",
            buttonText=eg.text.General.browse,
        )
        dirpathCtrl.GetTextCtrl().SetEditable(False)
        dirpathCtrl.SetValue(dirpath)
        box = wx.StaticBox(panel,-1,self.text.radioPath)

    #Sizers
        mainSizer=wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        radioSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer = wx.StaticBoxSizer(box,wx.VERTICAL)

        panel.sizer.Add(mainSizer)
        mainSizer.Add(topSizer)
        topSizer.Add(leftSizer)
        topSizer.Add(rightSizer,0,wx.LEFT,20)
        leftSizer.Add(previewLbl)
        leftSizer.Add(listBoxCtrl,0,wx.TOP,5)
        rightSizer.Add(fontLbl,0,wx.TOP,0)
        rightSizer.Add(fontButton,0,wx.TOP,3)
        rightSizer.Add(foreLbl,0,wx.TOP,10)
        rightSizer.Add(foreColourButton,0,wx.TOP,3)
        rightSizer.Add(backLbl,0,wx.TOP,10)
        rightSizer.Add(backColourButton,0,wx.TOP,3)
        radioSizer.Add(rb1)
        radioSizer.Add(rb2, 0, wx.LEFT|wx.EXPAND,35)
        boxSizer.Add(radioSizer)
        boxSizer.Add(dirpathCtrl,0,wx.TOP,6)
        mainSizer.Add(boxSizer,0,wx.TOP,10)
        mainSizer.Add(playCtrl,0,wx.TOP,10)
        mainSizer.Add(forceCtrl,0,wx.TOP,8)

    #Events handling
        def OnRadioButton(event=None):
            flag = rb2.GetValue()
            dirpathCtrl.Enable(flag)
            if not flag:
                dirpathCtrl.SetValue(dir)
            if event:
                event.Skip()
        rb1.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb2.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        OnRadioButton()

        def OnPathChange(evt = None):
            dirpath = dirpathCtrl.GetValue()
            files = os.listdir(dirpath)
            choices = []
            for item in files:
                if item[-4:].lower() in ('.txt', '.m3u', '.pls'):
                    choices.append(item[:-4])
            choices.sort()
            self.plugin.favList = choices #
            self.plugin.fav_path = dirpath
            listBoxCtrl.Set(choices)
            listBoxCtrl.SetSelection(-1)
            if evt:
                evt.Skip()
        dirpathCtrl.Bind(wx.EVT_TEXT, OnPathChange)
        OnPathChange()

        def OnClick(evt):
            listBoxCtrl.SetSelection(-1)
            evt.StopPropagation()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, OnClick)

        # re-assign the test button
        def OnButton(event):
            self.testFlag = True
            event.Skip()
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

    #On close panel
        while panel.Affirmed():
            panel.SetResult(
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(),
            playCtrl.GetValue(),
            forceCtrl.GetValue(),
            rb2.GetValue(),
            dirpathCtrl.GetValue(),
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

ACTIONS = (
    (Run,"Run","Run or Restore","Run Billy with its default settings or restore window.", None),
    (Exit,"ExitBilly","Exit Billy","Exit Billy.",u'{Esc}'),
    ( eg.ActionGroup, 'Main', 'Main', 'Adds actions to main control Billy',(
        (HotKeyAction,"Play","Play","Play selected file.",u'{Enter}'),
        (HotKeyAction,"Pause","Pause","Pause.",u'{0}'),
        (HotKeyAction,"PausePlay","Pause/Play","Pause/Play.",u'{Space}'),
        (HotKeyAction,"Stop","Stop","Stop.",'{0}{0}'),
        (HotKeyAction,"Next","Next","Next.",u'{Tab}'),
        (HotKeyAction,"Previous","Previous","Previous.",u'{Shift+Tab}'),
        (HotKeyAction,"ToStart","Jump to start","Jump to start of playing file.",u'{Backspace}'),
        #(HotKeyAction,"SeekLeft","Seek Left","Seek in track left.",u'{Left}'),
        #(HotKeyAction,"SeekRight","Seek Right","Seek in track Right.",u'{Right}'),
        #(HotKeyAction,"SeekLeftBig","Seek Left Big","Seek 60s in track left.",u'{Ctrl+Left}'),
        #(HotKeyAction,"SeekRightBig","Seek Right Big","Seek 60s in track Right.",u'{Ctrl+Right}'),
        #(HotKeyAction,"VolumeUp","Volume Up","Volume Up.",u'{Add}'),
        #(HotKeyAction,"VolumeDown","Volume Down","Volume Down.",u'{Subtract}'),
        )),
    ( eg.ActionGroup, 'Playlist', 'Playlist', 'Adds actions to control of playlist Billy',(
        (HotKeyAction,"TogglePlayMode","Toggle play mode","Toggle play mode.",u'{F9}'),
        (HotKeyAction,"ToggleViewMode","Toggle view mode","Toggle layout list all.",u'{F8}'),
        (HotKeyAction,"OpenFolder","Open Folder","Open a dir with music files.",u'{F4}'),
        (HotKeyAction,"AddFolder","Add Folder","Add a dir with music files.",u'{F3}'),
        (HotKeyAction,"AddFile","Add File(s)","Add File(s).",u'{Ctrl+L}'),
        (HotKeyAction,"AddURL","Add Internet radio stream","Add Internet radio stream.",u'{Ctrl+R}'),
        (HotKeyAction,"OpenPlaylist","Open Playlist","Load Billy Playlist.",u'{Ctrl+O}'),
        (HotKeyAction,"SavePlaylist","Save Playlist","Save Playlist.",u'{Ctrl+S}'),
        #(HotKeyAction,"MoveItemsUp","Move Items Up","Move Items Up.",u'{Ctrl+Up}'),
        #(HotKeyAction,"MoveItemsDown","Move Items Down","Move Items Down.",u'{Ctrl+Down}'),
        #(HotKeyAction,"SelectAll","Select All","Select All.",u'{Ctrl+A}'),
        (HotKeyAction,"Remove","Remove file from list","Remove file from list.",u'{Del}'),
        (HotKeyAction,"Delete","Delete file to recycle bin","Delete file to recycle bin.",u'{Shift+Del}'),
        (HotKeyAction,"ClearList","Clear list","Clear list.",u'{Ctrl+N}'),
        (HotKeyAction,"CheckNewFiles","Check for new files","Check for new files.",u'{F5}'),
        #(HotKeyAction,"SelectPlayingItem","Select playing item","Select playing item.",u';'),
        (HotKeyAction,"Queue","Queue","Add selected file to Queue.",u'{Ins}'),
        (HotKeyAction,"CropQueued","Crop selected or queued items","Crop selected or queued items.",u'{Ctrl+Del}'),
        (HotKeyAction,"ClearHistory","Clear shuffle/queue history","Clear shuffle/queue history.",u'{Shift+Ctrl+C}'),
        #(HotKeyAction,"RemoveMissing","Remove missing files from list","Remove missing files from list.",u'{Alt+Del}'),
        (HotKeyAction,"CutEntry","Cut playlist entry","Cut playlist entry.",u'{Ctrl+X}'),
        (HotKeyAction,"CopyEntry","Copy playlist entry","Copy playlist entry.",u'{Ctrl+C}'),
        (HotKeyAction,"PasteEntry","Paste playlist entry","Paste playlist entry.",u'{Ctrl+V}'),
        (HotKeyAction,"EditEntry","Edit playlist entry","Edit playlist entry.",u'{Shift+F2}'),
        )),
    ( eg.ActionGroup, 'Extras', 'Extras', 'Adds extra actions to control Billy',(
        (HotKeyAction,"Properties","Properties","Properties or multiple filename renamer (on multiple selection).",u'{F2}'),
        (HotKeyAction,"Explore","Explore","Open Explorer in file folder.",u'{Ctrl+E}'),
        (HotKeyAction,"Find","Find","Find file in active list.",u'{Ctrl+F}'),
        (HotKeyAction,"Record","Record Internet Radio","Record.",u'{Multiply}'),
        #(HotKeyAction,"Restore","Restore","Maximize, Restore.",u'{F12}'),
        (HotKeyAction,"Minimize","Minimize to Tray","Minimize to tray.",u'{F11}'),
        #(HotKeyAction,"SoftMute","Soft Mute","Soft mute (30% of volume).",u'{Pause}'),
        #(HotKeyAction,"ExploreApplPath","Explore Billy Directory","Explore from Billy Directory.",u'{Alt+Ctrl+E}'),
        (HotKeyAction,"ResetMixer","Reset Windows Mixer","Reset Windows Mixer.",u'{Ctrl+Space}'),
        #(HotKeyAction,"PlayingLength","Playing Length","Calculate total playlist time.",u'{Ctrl+Alt+T}'),
        #(HotKeyAction,"SleepTimer","Sleep Timer","Sleep Timer.",u'{Alt+T}'),
        (HotKeyAction,"Settings","Settings","Settings menu Billy.",u'{F6}'),
        (GetPlayingFile,"GetPlayingFile","Get Currently Playing File","Gets the name of currently playing file.", None),
        )),
    ( eg.ActionGroup, 'Favorites', 'Favorites', 'Adds actions to control Favorites of Billy',(
        (HotKeyAction,"AddPlistToFav","Add playlist to favorites","Add playlist to favorites.",u'{Ctrl+D}'),
        (HotKeyAction,"OrganizeFav","Organize favorites","Organize favorites.",u'{Ctrl+B}'),
        (HotKeyAction,"LoadFav1","Load Favorite 1","Load Favorite playlist 1.",u'{Ctrl+1}'),
        (HotKeyAction,"LoadFav2","Load Favorite 2","Load Favorite playlist 2.",u'{Ctrl+2}'),
        (HotKeyAction,"LoadFav3","Load Favorite 3","Load Favorite playlist 3.",u'{Ctrl+3}'),
        (HotKeyAction,"LoadFav4","Load Favorite 4","Load Favorite playlist 4.",u'{Ctrl+4}'),
        (HotKeyAction,"LoadFav5","Load Favorite 5","Load Favorite playlist 5.",u'{Ctrl+5}'),
        (HotKeyAction,"LoadFav6","Load Favorite 6","Load Favorite playlist 6.",u'{Ctrl+6}'),
        (HotKeyAction,"LoadFav7","Load Favorite 7","Load Favorite playlist 7.",u'{Ctrl+7}'),
        (HotKeyAction,"LoadFav8","Load Favorite 8","Load Favorite playlist 8.",u'{Ctrl+8}'),
        (HotKeyAction,"LoadFav9","Load Favorite 9","Load Favorite playlist 9.",u'{Ctrl+9}'),
        (eg.ActionGroup, 'Menu', 'Menu', 'Menu',(
            (ShowMenu, 'ShowMenu', 'Show menu', 'Show on screen menu.', None),
            (MoveCursor, 'MoveDown', 'Cursor down', 'Cursor down.', ('max-1', '-1', 1)),
            (MoveCursor, 'MoveUp', 'Cursor up', 'Cursor up.', ('0', 'max', -1)),
            (OK_Btn, 'OK_Btn', 'OK', 'OK button pressed.', None),
            (Cancel_Btn, 'Cancel_Btn', 'Cancel', 'Cancel button pressed.', None),
        )),
    )),
)
#===============================================================================
