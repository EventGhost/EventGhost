# -*- coding: utf-8 -*-

version="0.0.3"

# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.3 by Pako 2012-11-16 13:03 UTC+1
#     - added "Password" and "PC identifier" optional parameters
# 0.0.2 by Pako 2011-10-22 08:53 UTC+1
#     - added "Coalesce notes" feature
# 0.0.1 by Pako 2011-10-21 10:27 UTC+1
#     - initial version
#===============================================================================

eg.RegisterPlugin(
    name="Growl",
    guid = "{20EFFE03-5448-4ECB-B95B-E7CAE51FD6CA}",
    version = version,
    author = "Pako",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=3517",
    icon = (
        "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"
    ),
    description = """<rst>
With this plugin you can send a notifications to Growl program ...

This allows you to use a lot of nice OSD to display your information.
"""
)
#===============================================================================

import logging
import sys
from os.path import abspath, dirname
sys.path.append(abspath(dirname(__file__.decode('mbcs'))))
import gntp.notifier
from os import urandom
from base64 import b64encode
from os.path import join
#===============================================================================

class EG_Logger(logging.Logger):

    def __init__(self, name, level=logging.DEBUG):
        logging.Logger.__init__(self, name, level)


    def info(self, msg, *args):
        eg.PrintNotice("Growl: "+ msg % args)


    def error(self, msg, *args):
        eg.PrintError("Growl: "+ msg % args)


    def debug(self, msg, *args):
        #print ("Growl DEBUG:\r\n"+msg % args)
        pass
#NOTE: uncomment print statement for debug prints !

logging.setLoggerClass(EG_Logger)
logger = logging.getLogger(__name__)
gntp.notifier.logger = logger
#===============================================================================

def Move(lst,index,direction):
    tmpList = lst[:]
    max = len(lst)-1
    #Last to first position, other down
    if index == max and direction == 1:
        tmpList[1:] = lst[:-1]
        tmpList[0] = lst[max]
        index2 = 0
    #First to last position, other up
    elif index == 0 and direction == -1:
        tmpList[:-1] = lst[1:]
        tmpList[max] = lst[0]
        index2 = max
    else:
        index2 = index+direction
        tmpList[index] = lst[index2]
        tmpList[index2] = lst[index]
    return index2,tmpList
#===============================================================================

class Text:
    errMess1 = 'Error "%s" during registration to Growl'
    errMess2 = "%s\r\nIt is possible that Growl is not running"
    listLabel = "List of notification types:"
    labelLbl = "Notification type:"
    passwordLbl = "Password:"
    delete = 'Delete'
    insert = 'Add new'
    options = "Optional parameters"
    pcId = "PC identifier:"
#===============================================================================

class Growl(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddAction(Notify)
      
    
    def __start__(self, types = [], password="", pcId = ""):
        self.types = types
        text = self.text
        appName = "EventGhost"
        self.growl = gntp.notifier.GrowlNotifier(
            applicationName = appName if not pcId else appName + "@" + pcId,
            applicationIcon = join(eg.imagesDir, "icon32x32.png"),
            notifications = types,
            defaultNotifications = types,
            password = password
        )
        try:
            resp = self.growl.register()
            if resp != True :
                eg.PrintError(text.errMess1 % str(resp))

        except IOError, e:
            if e.errno == 10061:
                eg.PrintError(text.errMess2 % e[1])


    def Configure(self, types = [], password="", pcId = ""):

        def boxEnable(enable):
            labelCtrl.Enable(enable)
            labelLbl.Enable(enable)

        text = self.text
        panel = eg.ConfigPanel(self)
        self.types = types
        leftSizer = wx.FlexGridSizer(4, 2, 2, 8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        listLabel=wx.StaticText(panel, -1, text.listLabel)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(200, 106),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(panel, -1, text.labelLbl)
        labelCtrl=wx.TextCtrl(panel,-1,'')
        passwordLbl=wx.StaticText(panel, -1, text.passwordLbl)
        passwordCtrl = wx.TextCtrl(panel, -1, password, style=wx.TE_PASSWORD)        
        pcIdLbl=wx.StaticText(panel, -1, text.pcId)
        pcIdCtrl = wx.TextCtrl(panel, -1, pcId)        
        leftSizer.Add(listLabel,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl,0,wx.TOP,2)
        leftSizer.Add(topMiddleSizer,0,wx.TOP,5)
        leftSizer.Add(labelLbl,0,wx.TOP,2)
        leftSizer.Add((1,1))
        leftSizer.Add(labelCtrl,0,wx.EXPAND)
        leftSizer.Add((1,1))
        rightSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.options),
            wx.VERTICAL
        ) 
        rightSizer.Add(passwordLbl,0,wx.TOP,5)
        rightSizer.Add(passwordCtrl,0,wx.EXPAND|wx.TOP,2)
        rightSizer.Add(pcIdLbl,0,wx.TOP,20)
        rightSizer.Add(pcIdCtrl,0,wx.EXPAND|wx.TOP,2)

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
        btnApp=wx.Button(panel,-1,text.insert)
        btnDEL=wx.Button(panel,-1,text.delete)
        eg.EqualizeWidths((btnDEL, btnApp))
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer,0,wx.RIGHT,15)
        mainSizer.Add(rightSizer, 1, wx.EXPAND|wx.TOP, 7)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)
        if len(self.types) > 0:
            listBoxCtrl.Set(self.types)
            listBoxCtrl.SetSelection(0)
            labelCtrl.SetValue(self.types[0])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            boxEnable(False)
            panel.dialog.buttonRow.applyButton.Enable(False)
            panel.dialog.buttonRow.okButton.Enable(False)
        panel.sizer.Layout()


        def onClick(evt):
            self.flag = False
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            if label.strip() != "":
                if self.types.count(label) == 1:
                    self.oldSel=sel
                    labelCtrl.SetValue(self.types[sel])
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
            self.flag = True
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)


        def onButtonUp(evt):
            newSel,self.types=Move(self.types,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set(self.types)
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)


        def onButtonDown(evt):
            newSel,self.types=Move(self.types,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set(self.types)
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)


        def onButtonDelete(evt):
            self.flag = False
            lngth=len(self.types)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.types=[]
                listBoxCtrl.Set([])
                labelCtrl.SetValue("")
                boxEnable(False)
                panel.dialog.buttonRow.applyButton.Enable(False)
                panel.dialog.buttonRow.okButton.Enable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            self.types.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set(self.types)
            listBoxCtrl.SetSelection(sel)
            labelCtrl.SetValue(self.types[sel])
            evt.Skip()
            self.flag = True
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)


        def OnTxtChange(evt):
            if self.types != [] and self.flag:
                flag = False
                sel = self.oldSel
                label = labelCtrl.GetValue()
                self.types[sel]=label
                listBoxCtrl.Set(self.types)
                listBoxCtrl.SetSelection(sel)
                if label != "":
                    flag = self.types.count(label) == 1
                panel.dialog.buttonRow.applyButton.Enable(flag)
                panel.dialog.buttonRow.okButton.Enable(flag)
                btnApp.Enable(flag)
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)


        def OnButtonAppend(evt):
            self.flag = False
            if len(self.types)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            self.types.insert(sel,"")
            listBoxCtrl.Set(self.types)
            listBoxCtrl.SetSelection(sel)
            labelCtrl.SetValue("")
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
            self.flag = True
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

        while panel.Affirmed():
            panel.SetResult(
                listBoxCtrl.GetStrings(),
                passwordCtrl.GetValue(),
                pcIdCtrl.GetValue()
            )
#===============================================================================

class Notify(eg.ActionBase):

    class text:
        errMess3 = 'Note type "%s" is not registered'
        errMess4 = 'Note Title must be non-empty'
        errMess5 = 'Error "%s" during sending notification'
        typeLabel = "Note type:"
        titleLabel = "Title:"
        descrLabel = "Description:"
        iconLabel = "Icon:"
        stickyLabel = "Sticky:"
        stickyChoices = ("Yes", "No")
        priorityLabel = "Priority:"
        toolTipFile = "Press button and browse to select a icon file ..."
        browseFile = "Notification icon selection" 
        coalesce = "Notes coalesce (supported only by some display - e.g. Meter)"


    def __call__(
        self,
        noteType = "",
        title = "",
        description = "",
        icon = "",
        sticky = False,
        priority = 0,
        id = None,
        coalesce = False
        ):

        if noteType in self.plugin.types:
            if title:
                try:
                    resp = self.plugin.growl.notify(
                        noteType,
                        eg.ParseString(title),
                        eg.ParseString(description),
                        eg.ParseString(icon) if icon else None,
                        not sticky,
                        priority,
                        id if coalesce else None
                    ) 
                    if resp != True:
                        eg.PrintError(self.text.errMess5 % str(resp))
                except IOError, e:
                    if e.errno == 10061:
                        eg.PrintError(self.plugin.text.errMess2 % e[1])
            else:
                eg.PrintError(self.text.errMess4)
        else:
            eg.PrintError(self.text.errMess3 % noteType)


    def GetLabel(
        self,
        noteType,
        title,
        description,
        icon,
        sticky,
        priority,
        id,
        coalesce
        ):
        return "%s: %s: %s: %s" % (self.name, noteType, title, description)


    def Configure(
        self,
        noteType = "",
        title = "",
        description = "",
        icon = "",
        sticky = False,
        priority = 0,
        id = None,
        coalesce = False
        ):
        if not id:
            id = b64encode(urandom(8))
        self.p = priority
        text = self.text
        panel = eg.ConfigPanel(self)
        typeLabel = wx.StaticText(panel, -1, text.typeLabel)
        titleLabel = wx.StaticText(panel, -1, text.titleLabel)
        descrLabel = wx.StaticText(panel, -1, text.descrLabel)
        iconLabel = wx.StaticText(panel, -1, text.iconLabel)
        stickyLabel = wx.StaticText(panel, -1, text.stickyLabel)
        priorityLabel = wx.StaticText(panel, -1, text.priorityLabel)
        typeCtrl = wx.Choice(panel, -1, choices = self.plugin.types)
        typeCtrl.SetStringSelection(noteType)
        titleCtrl = wx.TextCtrl(panel, -1, title)
        descrCtrl = wx.TextCtrl(panel, -1, description)
        iconCtrl =  eg.FileBrowseButton(
            panel,
            toolTip = text.toolTipFile,
            dialogTitle = text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.Pictures,
        )
        iconCtrl.SetValue(icon)
        stickyCtrl = wx.RadioBox(
            panel, -1, choices = text.stickyChoices, style = wx.RA_SPECIFY_COLS
        )
        stickyCtrl.SetSelection(sticky)
        priorityCtrl = wx.Slider(
            panel,
            -1,
            0,-2,2,
            style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS | wx.SL_INVERSE | wx.SL_TOP 
        )
        priorityCtrl.SetValue(priority) 

        def sliderUpdate(evt):
            if not panel.dialog.buttonRow.applyButton.IsEnabled():
                panel.dialog.buttonRow.applyButton.Enable(evt.GetInt() != self.p)
            evt.Skip()
        priorityCtrl.Bind(wx.EVT_SLIDER, sliderUpdate)

        coalesceCtrl = wx.CheckBox(panel, -1, text.coalesce)
        coalesceCtrl.SetValue(coalesce)

        sizer = wx.FlexGridSizer(6, 2, 8, 8)
        sizer.AddGrowableCol(1)
        panel.sizer.Add(sizer,1,wx.EXPAND)
        panel.sizer.Add(coalesceCtrl,0,wx.EXPAND|wx.BOTTOM,8)
        sizer.Add(typeLabel,0,wx.TOP,10)
        sizer.Add(typeCtrl,1,wx.EXPAND|wx.TOP,10)
        sizer.Add(titleLabel,0)
        sizer.Add(titleCtrl,1,wx.EXPAND)
        sizer.Add(descrLabel,0)
        sizer.Add(descrCtrl,1,wx.EXPAND)
        sizer.Add(iconLabel,0)
        sizer.Add(iconCtrl,1,wx.EXPAND)
        sizer.Add(stickyLabel,0,wx.TOP,10)
        sizer.Add(stickyCtrl,1,wx.EXPAND)
        sizer.Add(priorityLabel,0,wx.TOP,10)
        sizer.Add(priorityCtrl,0,wx.EXPAND|wx.BOTTOM,6)

        while panel.Affirmed():
            panel.SetResult(
                typeCtrl.GetStringSelection(),
                titleCtrl.GetValue(),
                descrCtrl.GetValue(),
                iconCtrl.GetValue(),
                bool(stickyCtrl.GetSelection()),
                priorityCtrl.GetValue(),
                id,
                coalesceCtrl.GetValue()
            )
#===============================================================================
