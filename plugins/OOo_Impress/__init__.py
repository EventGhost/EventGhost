version="0.1.1" 
# Plugins/OOo_Impress/__init__.py
#
# Copyright (C)  2008 Pako  (lubos.ruckl@quick.cz)
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
#Last change: 2008-10-24 11:11

eg.RegisterPlugin(
    name = "OOo Impress",
    author = "Pako",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control the '
        '<a href="http://www.openoffice.org/product/impress.html">'
        'OOo Impress</a>.'
    ),
    createMacrosOnAdd = True,    
    url = "http://www.eventghost.org/xxxxx",
    icon = (
        "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"
        "TkSuQmCC"
    )
)

import os
from time import sleep
from threading import Timer
from win32com.client.dynamic import Dispatch
from win32api import GetSystemMetrics
from win32gui import SetFocus, SetForegroundWindow, SetActiveWindow
from eg.WinApi import SendMessageTimeout
from eg.WinApi.Dynamic import PostMessage

WM_CLOSE      = 16
WM_SYSCOMMAND = 274
SC_MINIMIZE   = 61472
WM_KEYDOWN    = 0x0100
WM_KEYUP      = 0x0101
VK_RETURN     = 0x0D

findPresentation=eg.WindowMatcher(
    u'SOFFICE.BIN',
    u'{*} - OpenOffice.org Impress{*}',
    u'SALTMPSUBFRAME',
    None,
    None,
    1,
    False,
    0.0,
    0
)
#====================================================================

#cls types for ACTIONS list:       
class StartPresentation(eg.ActionClass):

    class text:
        pathLabel = 'Path to presentation file:'
        filemask = 'Presentations (*.pps, *.ppt, *.odp)|*.pps; *.ppt;\
            *.odp|All files (*.*)|*.*'
        toolTipFile = 'Type filename or click browse to choose file'

        
    def __call__(self,url=None):
        if self.plugin.menuDlg is None:
            if url is not None:
                self.plugin.StartPresentation(url)


    def Configure(self,url=None):
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(
            panel,
            -1,
            self.text.pathLabel,
            style=wx.ALIGN_LEFT
        )
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            size=(370,-1),
            initialValue = url if (url is not None) else '',
            startDirectory=eg.folderPath.Documents,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse,
            toolTip=self.text.toolTipFile,
        )
        filepathCtrl.GetTextCtrl.SetEditable(False)
        panel.AddLabel(self.text.pathLabel)
        panel.sizer.Add((1, 3))
        panel.AddCtrl(filepathCtrl)
        
        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue())
#====================================================================

#Group Menu :
class ShowMenu(eg.ActionClass):
    panel = None
    
    class text:
        filemask = "Presentations (*.pps, *.ppt, *.odp)|*.pps;*.ppt;\
            *.odp|All files (*.*)|*.*"
        toolTipFile = 'Type filename or click browse to choose file'
        label = 'Label:'
        path = 'File:'
        menuPreview = 'On screen menu preview:'
        delete = 'Delete'
        insert = 'Insert new'
        menuFont = 'Menu font:'
        txtColour = 'Text colour'
        background = 'Background colour'        
#====================================================================

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
                self, panel, id, wx.NullBitmap, pos, size, style, validator, name
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
                    GetChildren()[0].GetSizer().GetChildren()[1].GetSizer().\
                    GetChildren()[1].GetWindow()                
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
#====================================================================

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
                listBoxCtrl =  self.window.GetSizer().GetChildren()[0].\
                    GetSizer().GetChildren()[1].GetSizer().GetChildren()[1].\
                    GetWindow()
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

            
    def Move(self,index,direction):
        tmpList=self.choices[:]
        max = len(self.choices)-1
        #Last to first position, other down
        if index == max and direction == 1:
            tmpList[1:] = self.choices[:-1]
            tmpList[0] = self.choices[max]
            index2 = 0
        #First to last position, other up
        elif index == 0 and direction == -1:
            tmpList[:-1] = self.choices[1:]
            tmpList[max] = self.choices[0]
            index2 = max
        else:
            index2 = index+direction
            tmpList[index] = self.choices[index2]
            tmpList[index2] = self.choices[index]
        self.choices=tmpList
        return index2


    def __call__(
        self,
        choices,
        fore,
        back,
        fontInfo,
    ):
        wx.CallAfter(
            self.plugin.ShowMenu,
            choices,
            fore,
            back,
            fontInfo,
        )


    def GetLabel(
        self,
        choices,
        fore,
        back,
        fontInfo,
    ):
        res=self.text.showMenu+' '
        for n in range(0,min(3,len(choices))):
            res=res+choices[n][0]+', '
        res = res[:-2]
        if len(choices) > 3:
            res += ', ...'
        return res


    def Configure(
        self,
        choices=[],
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None
    ):
        self.choices = choices[:]
        self.fore = fore
        self.back = back
        self.oldSel=0
        global panel
        panel = eg.ConfigPanel(self)
        w1 = panel.GetTextExtent(self.text.label)[0]
        w2 = panel.GetTextExtent(self.text.path)[0]
        w = max((w1,w2))
        mainSizer=wx.BoxSizer(wx.VERTICAL)
        topSizer=wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer=wx.FlexGridSizer(2,2,hgap=5,vgap=5)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        topRightSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        previewLblSizer = wx.BoxSizer(wx.HORIZONTAL)
        previewLblSizer.Add((w+5,1))
        previewLblSizer.Add(previewLbl)
        mainSizer.Add(previewLblSizer)
        mainSizer.Add(topSizer,0,wx.TOP,5)
        mainSizer.Add(bottomSizer,0,wx.TOP,16)
        panel.sizer.Add(mainSizer)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(160,120),
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
        topSizer.Add((w+5,1))
        topSizer.Add(listBoxCtrl)
        topSizer.Add((10,1))
        topSizer.Add(topMiddleSizer)
        topSizer.Add((50,1))
        topSizer.Add(topRightSizer)
        labelLbl=wx.StaticText(panel, -1, self.text.label)
        labelCtrl=wx.TextCtrl(panel,-1,'',size=wx.Size(160,-1))
        bottomSizer.Add(labelLbl,0,wx.TOP,3)
        labelCtrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelCtrlSizer.Add(labelCtrl,0,wx.EXPAND)
        bottomSizer.Add(labelCtrlSizer)
        filepathLbl=wx.StaticText(panel, -1, self.text.path)
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            size=(370,-1),
            startDirectory=eg.folderPath.Documents,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse,
            toolTip=self.text.toolTipFile
        )
        bottomSizer.Add(filepathLbl,0,wx.TOP,3)
        bottomSizer.Add(filepathCtrl,0,wx.EXPAND)
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(panel, -1, bmp)
        btnUP.Enable(False)
        topMiddleSizer.Add(btnUP)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(panel, -1, bmp)
        btnDOWN.Enable(False)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        w1 = panel.GetTextExtent(self.text.delete)[0]
        w2 = panel.GetTextExtent(self.text.insert)[0]
        if w1 > w2:
            btnDEL=wx.Button(panel,-1,self.text.delete)
            btnApp=wx.Button(panel,-1,self.text.insert,size=btnDEL.GetSize())
        else:
            btnApp=wx.Button(panel,-1,self.text.insert)
            btnDEL=wx.Button(panel,-1,self.text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = self.MenuFontButton(fontInfo)
        topRightSizer.Add(fontLbl,0,wx.TOP,-15)
        topRightSizer.Add(fontButton,0,wx.TOP,2)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = self.MenuColourSelectButton(
            0,
            fore,
            self.text.txtColour
        )
        topRightSizer.Add(foreLbl,0,wx.TOP,10)
        topRightSizer.Add(foreColourButton,0,wx.TOP,2)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = self.MenuColourSelectButton(
            1,
            back,
            self.text.background
        )
        topRightSizer.Add(backLbl,0,wx.TOP,10)
        topRightSizer.Add(backColourButton,0,wx.TOP,2)

        def OnClick(evt):
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            filepath = filepathCtrl.GetValue()
            if label.strip()<>"":
                if os.path.isfile(filepath):
                    if [n[0] for n in self.choices].count(label)==1:
                        if [n[1] for n in self.choices].count(filepath)==1:
                            self.oldSel=sel
                            item = self.choices[sel]
                            labelCtrl.SetValue(item[0])
                            filepathCtrl.SetValue(item[1])
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, OnClick)


        def OnButtonUp(evt):
            newSel=self.Move(listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([n[0] for n in self.choices])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, OnButtonUp)


        def OnButtonDown(evt):
            newSel=self.Move(listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([n[0] for n in self.choices])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, OnButtonDown)


        def OnButtonDelete(evt):
            lngth=len(self.choices)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.choices=[]
                listBoxCtrl.Set([])
                labelCtrl.SetValue('')
                filepathCtrl.SetValue('')
                labelCtrl.Enable(False)
                labelLbl.Enable(False)
                filepathCtrl.Enable(False)
                filepathLbl.Enable(False)
                panel.EnableButtons(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.choices.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in self.choices])
            listBoxCtrl.SetSelection(sel)
            item = self.choices[sel]
            labelCtrl.SetValue(item[0])
            filepathCtrl.SetValue(item[1])
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, OnButtonDelete)
        
        if len(self.choices) > 0:
            listBoxCtrl.Set([n[0] for n in self.choices])
            listBoxCtrl.SetSelection(0)
            labelCtrl.SetValue(self.choices[0][0])
            filepathCtrl.SetValue(self.choices[0][1])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            labelCtrl.Enable(False)
            labelLbl.Enable(False)
            filepathCtrl.Enable(False)
            filepathLbl.Enable(False)
            panel.EnableButtons(False)
        panel.sizer.Layout()


        def OnTextChange(evt):
            if self.choices<>[]:
                flag = False
                sel = self.oldSel
                label = labelCtrl.GetValue()
                filepath = filepathCtrl.GetValue()
                self.choices[sel]=(label,filepath)
                listBoxCtrl.Set([n[0] for n in self.choices])
                listBoxCtrl.SetSelection(sel)
                if label.strip()<>"":
                    if os.path.isfile(filepath):
                        if [n[0] for n in self.choices].count(label)==1:
                            if [n[1] for n in self.choices].count(filepath)==1:
                                flag = True
                panel.EnableButtons(flag)
                btnApp.Enable(flag)
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        filepathCtrl.Bind(wx.EVT_TEXT, OnTextChange)


        def OnButtonAppend(evt):
            if len(self.choices)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            labelCtrl.Enable(True)
            labelLbl.Enable(True)
            filepathCtrl.Enable(True)
            filepathLbl.Enable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            self.choices.insert(sel,('',''))
            listBoxCtrl.Set([n[0] for n in self.choices])
            listBoxCtrl.SetSelection(sel)
            labelCtrl.SetValue('')
            labelCtrl.SetFocus()
            filepathCtrl.SetValue('')
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

        # re-assign the test button
        def OnButton(event):
            self.plugin.testFlag = True
            event.Skip()
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            panel.SetResult(
            self.choices,
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(), 
        )
#====================================================================

class MoveCursor(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            max=len(self.plugin.choices)
            if max > 0:
                sel=self.plugin.menuDlg.GetSizer().GetChildren()[0].\
                    GetWindow().GetSelection()
                if sel == eval(self.value[0]):
                    sel = eval(self.value[1])
                self.plugin.menuDlg.GetSizer().GetChildren()[0].GetWindow().\
                    SetSelection(sel+self.value[2])
#====================================================================

class OK_Btn(eg.ActionClass):

    def __call__(self):
        self.plugin.timer.cancel()
        self.plugin.StartFromMenu()       
#====================================================================

class Cancel_Btn(eg.ActionClass):

    def __call__(self):
        self.plugin.destroyMenu()
#======================================================================
 
#Group GoTo slide ...:
class DigitAction(eg.ActionClass):

    def __call__(self):
        hwnd = findPresentation()
        if len(hwnd) != 0:
            self.plugin.number+=self.value
            wx.CallAfter(self.plugin.ShowSlideNumber)
#======================================================================
            
class Enter(eg.ActionClass):

    def __call__(self):
        hwnd = findPresentation()
        if len(hwnd) != 0:
            if (self.plugin.numDialog is not None) and (len(self.plugin.number)>0):
                for vk_num in self.plugin.number:
                    hparam = int(vk_num)+96
                    if vk_num=='0':
                        lparam = 82
                    else:
                        lparam = int(vk_num)+78-7*((int(vk_num)+2)/3-1)
                    lparam = 1+lparam*65536
                    PostMessage(hwnd[0], WM_KEYDOWN, hparam, lparam)
                    PostMessage(hwnd[0], WM_KEYUP, hparam, lparam+0xC0000000)
                PostMessage(hwnd[0], WM_KEYDOWN, VK_RETURN, 0x001C0001)
                PostMessage(hwnd[0], WM_KEYUP, VK_RETURN, 0xC01C0001)
                wx.CallAfter(self.plugin.DestroySlideNumber)
#======================================================================

class Backspace(eg.ActionClass):

    def __call__(self):
        if (self.plugin.numDialog is not None) and (len(self.plugin.number)>0):
                self.plugin.number = self.plugin.number[:-1]
                if len(self.plugin.number) == 0:
                    wx.CallAfter(self.plugin.DestroySlideNumber)
                else:
                    wx.CallAfter(self.plugin.ShowSlideNumber)
#======================================================================

class Cancel(eg.ActionClass):

    def __call__(self):
        if self.plugin.numDialog is not None:
            wx.CallAfter(self.plugin.DestroySlideNumber)
#======================================================================

class HotKeyAction(eg.ActionClass):                    

    def __call__(self):
        hwnd = findPresentation()
        if len(hwnd) != 0:
            if self.plugin.numDialog is None and self.plugin.menuDlg is None:
                eg.SendKeys(hwnd[0], self.value, True) #True is important !!!
#======================================================================

ACTIONS = (
    (StartPresentation, 'StartPresentation', 'Start presentation', 'Start presentation.', None),
    (HotKeyAction, 'Exit', 'End presentation', 'End presentation.', u'{Escape}' ),
    (HotKeyAction, 'Black', 'Black screen', 'Show black screen until next key or mouse wheel event.', u'{B}' ),
    (HotKeyAction, 'White', 'White screen', 'Show white screen until next key or mouse wheel event.', u'{W}' ),
    ( eg.ActionGroup, 'Menu', 'Menu', 'Menu for choice of presentation', (
        (ShowMenu, 'ShowMenu', 'Show menu', 'Show menu.', None),
        (MoveCursor, 'MoveDown', 'Cursor Down', 'Cursor Down.', ('max-1', '-1', 1) ),
        (MoveCursor, 'MoveUp', 'Cursor Up', 'Cursor Up.', ('0', 'max', -1) ),
        (OK_Btn, 'OK_Btn', 'OK', 'OK button pressed.', None),
        (Cancel_Btn, 'Cancel_Btn', 'Cancel', 'Cancel button pressed.', None),
    ) ),    
    ( eg.ActionGroup, 'Navigation', 'Navigation', 'Navigation through presentation', (
        ( eg.ActionGroup, 'GoToSlide', 'Go to slide ...', 'Type a number of a slide and press Enter to go to the slide..', (
            (DigitAction, 'Digit0', 'Digit 0', 'Type Digit 0', '0' ),
            (DigitAction, 'Digit1', 'Digit 1', 'Type Digit 1', '1' ),
            (DigitAction, 'Digit2', 'Digit 2', 'Type Digit 2', '2' ),
            (DigitAction, 'Digit3', 'Digit 3', 'Type Digit 3', '3' ),
            (DigitAction, 'Digit4', 'Digit 4', 'Type Digit 4', '4' ),
            (DigitAction, 'Digit5', 'Digit 5', 'Type Digit 5', '5' ),
            (DigitAction, 'Digit6', 'Digit 6', 'Type Digit 6', '6' ),
            (DigitAction, 'Digit7', 'Digit 7', 'Type Digit 7', '7' ),
            (DigitAction, 'Digit8', 'Digit 8', 'Type Digit 8', '8' ),
            (DigitAction, 'Digit9', 'Digit 9', 'Type Digit 9', '9' ),
            (Enter, 'Enter', 'Enter', 'Enter - Goto slide.', None),
            (Backspace, 'Backspace', 'Backspace', 'Backspace (delete last digit).', None),
            (Cancel, 'Cancel', 'Cancel', 'Cancel - Do not goto a slide.', None),
        ) ),
        (HotKeyAction, 'Next', 'Play next effect/slide', 'Play next effect (if any, else go to next slide).', u'{Down}' ),
        (HotKeyAction,
            'Previous', 'Play previous effect/slide',
            'Play previous effect again. If no previous effect exists on this slide, show previous slide.'
            '</p>\n\n<p><b>For bug in OOo Impress this function meanwhile be out of gear properly !</b>'
            '</p><p>See <a href="http://www.openoffice.org/issues/show_bug.cgi?id=48179"> '
            'http://www.openoffice.org/issues/show_bug.cgi?id=48179</a>',
            u'{Up}'
        ),
        (HotKeyAction, 'NextWithout', 'Next slide without effects', 'Go to next slide without playing effects.', u'{Alt+PageDown}' ),
        (HotKeyAction, 'PreviousWithout', 'Previous slide without effects', 'Go to the previous slide without playing effects.', u'{Alt+PageUp}' ),
        (HotKeyAction, 'First', 'First slide', 'Jump to first slide in the slide show.', u'{Home}' ),
        (HotKeyAction, 'Last', 'Last slide', 'Jump to the last slide in the slide show.', u'{End}' ),
    ) ),
)
#====================================================================

class OOo_Impress(eg.PluginClass):
        
    menuDlg = None
    numDialog = None
    number = ''
    choices = []
    testFlag = False
    
    class text:
        err1 ="Couldn't find file with presentation!"
        err2 ="Couldn't find window with presentation!"

    def __init__(self):
        self.AddActionsFromList(ACTIONS)
        self.timer=Timer(0.0,self.destroyMenu)


    def StartPresentation(self,url):
        objServiceManager = Dispatch('com.sun.star.ServiceManager')
        desktop = objServiceManager.CreateInstance('com.sun.star.frame.Desktop')
        try:
            doc = desktop.loadComponentfromURL("file:///"+url, '_blank', 0, [])
            hWnd = doc.CurrentController.Frame.ContainerWindow.getWindowHandle([],1) # 1 = for win32
            SendMessageTimeout(hWnd, WM_SYSCOMMAND, SC_MINIMIZE, 0)
        except:
            self.PrintError(self.text.err1)
            return
        presentation  = doc.getPresentation()
        #presentation.IsAlwaysOnTop = True
        #presentation.StartWithNavigator = False
        #presentation.IsEndless = False
        #presentation.AllowAnimations = True
        #presentation.IsAutomatic = True
        #presentation.IsShowAll = True
        presentation.IsFullScreen = True
        presentation.Pause = 1
        presentation.start()
        hwnd = findPresentation()
        if len(hwnd)>0:
            SetForegroundWindow(hwnd[0])
            SetFocus(hwnd[0])
            SetActiveWindow(hwnd[0])
        else:
            self.PrintError(self.text.err2)
        PostMessage(hWnd,WM_CLOSE,0,0)

        
    def StartFromMenu(self):
        if self.menuDlg is not None:
            sel=self.menuDlg.GetSizer().GetChildren()[0].GetWindow().\
                GetSelection()
            pres = self.choices[sel][1]
            self.destroyMenu()
            self.StartPresentation(pres)

            
    def DestroySlideNumber(self):
        self.number = ''
        self.numDialog.Destroy()
        self.numDialog = None
        

    def ShowSlideNumber(self):
        if self.numDialog is not None:
            statText = self.numDialog.GetSizer().GetChildren()[0].GetWindow()
            statText.SetLabel(self.number)
        else:
            self.numDialog = wx.Frame(
                None, -1, 'SlideNumber', 
                style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER   
            )
            statText=wx.StaticText(
                self.numDialog,
                -1,
                self.number,
                style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
            )
            font = statText.GetFont()
            font.SetPointSize(100)
            font.SetWeight(wx.BOLD)
            statText.SetFont(font)
            self.numDialog.SetBackgroundColour(wx.Colour(0,255,255))
            statText.SetForegroundColour(wx.Colour(0,255,255))
            statText.SetBackgroundColour(wx.Colour(0, 0, 139))
            w,h = statText.GetTextExtent('8888')
            self.numDialog.SetSize((w+16,h+16))
            statText.SetPosition((7,7))
            statText.SetSize((w,h))
            mainSizer =wx.BoxSizer(wx.VERTICAL)
            self.numDialog.SetSizer(mainSizer)
            mainSizer.Add(statText, 0, wx.EXPAND)
            self.numDialog.Centre()
            self.numDialog.Show()        

    def ShowMenu(
        self,
        choices,
        fore,
        back,
        fontInfo,
    ):
        if self.menuDlg is not None:
            return
        self.fore=fore
        self.back=back
        self.choices=choices
        self.menuDlg = wx.Frame(
                None, -1, 'OS_Menu', 
                style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER
            )

        presChoiceCtrl=wx.ListBox(
            self.menuDlg,
            choices = [n[0] for n in self.choices],
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB 
        )

        if fontInfo is None:
            font = presChoiceCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)        
        presChoiceCtrl.SetFont(font)
        # menu height calculation:
        items=len(choices)
        h=presChoiceCtrl.GetCharHeight()
        height0 = len(choices)*h+5
        height1 = h*((GetSystemMetrics (1)-20)/h)+5
        height = min(height0,height1)
        # menu width calculation:
        width_lst=[]
        for item in [n[0] for n in self.choices]:
            width_lst.append(presChoiceCtrl.GetTextExtent(item+' ')[0])
        width = max(width_lst)+8
        if height<height0:
            width += 20 #for vertical scrollbar
        width = min((width,GetSystemMetrics (0)-50))
        self.menuDlg.SetSize((width+6,height+6))
        presChoiceCtrl.SetDimensions(2,2,width,height,wx.SIZE_AUTO)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        self.menuDlg.SetSizer(mainSizer)
#
        presChoiceCtrl.SetSelection(0)
        self.menuDlg.SetBackgroundColour((0,0,0))
        presChoiceCtrl.SetBackgroundColour(self.back)
        presChoiceCtrl.SetForegroundColour(self.fore)
        mainSizer.Add(presChoiceCtrl, 0, wx.EXPAND)
        self.menuDlg.Centre()
        if self.testFlag:
            self.timer = Timer(5.0,self.destroyMenu)
            self.timer.start()
        self.menuDlg.Show()
        
        def On2Click(evt):
            self.timer.cancel()
            self.StartFromMenu()
            evt.StopPropagation()
        presChoiceCtrl.Bind(wx.EVT_LISTBOX_DCLICK, On2Click)
        
    def destroyMenu(self):
        self.timer.cancel()
        if self.menuDlg is not None:
            self.menuDlg.Destroy()
            self.menuDlg = None
            self.choices = []
            self.testFlag = False
#====================================================================

