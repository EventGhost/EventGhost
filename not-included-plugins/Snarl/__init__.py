# -*- coding: utf-8 -*-

version="0.0.6"

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
# 0.0.6 by Pako 2015-01-23 18:30 UTC+1
#     - signature no longer contains version string
# 0.0.5 by Pako 2014-03-28 18:55 UTC+1
#     - customized events on notification disappearance can carry a payload now
#       and supports also variables
# 0.0.4 by Pako 2014-03-19 11:32 UTC+1
#     - notification user menu now supports also variables
# 0.0.3 by Pako 2014-03-16 11:39 UTC+1
#     - bugfix
#     - notification menu now supports also event payload
# 0.0.2 by Pako 2012-01-05 07:20 UTC+1
#     - for Snarl 2.5.1
# 0.0.1 by Pako 2011-12-12 19:01 UTC+1
#     - initial version
#===============================================================================

eg.RegisterPlugin(
    name="Snarl",
    guid = "{20EFFE03-5448-4ECB-B95B-E7CAE51FD6CB}",
    createMacrosOnAdd = True,
    version = version,
    author = "Pako",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=3587",
    icon = (
        "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"
        "AElFTkSuQmCC"
    ),
    description = """<rst>
With this plugin you can send a notifications to Snarl ...

This allows you to use a lot of nice OSD to display your information.

**WARNING:** For proper functioning requires Snarl_ 2.5.1 or later

.. _Snarl: http://www.getsnarl.info"""
)
#===============================================================================

import pySnarl
import wx.grid as gridlib
from os.path import join
from time import sleep
from functools import partial
from random import randrange
from copy import deepcopy as cpy
from win32gui import FindWindow, GetWindow, GetWindowText
from eg.WinApi.Utils import BringHwndToFront
GW_CHILD    = 5
GW_HWNDNEXT = 2
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

@eg.AsTasklet
def OnCmdAbout(frm):
    eg.AboutDialog.GetResult(frm)
#===============================================================================

def BringDialogToFront(name):
    hwnd = 0
    i=0
    while hwnd == 0 and i < 10000:
        hwnd = FindWindow("#32770", name)
        i += 1
    if hwnd:
        BringHwndToFront(hwnd)
#===============================================================================

def BringSaveChangesDialog():
    ctrl = 0
    for i in range(1000):
        hwnd = FindWindow("#32770", eg.APP_NAME)
        while hwnd:
            if not GetWindowText(hwnd) == eg.APP_NAME:
                hwnd = GetWindow(hwnd, GW_HWNDNEXT)
                continue
            ctrl = GetWindow(hwnd, GW_CHILD)
            while ctrl:
                if GetWindowText(ctrl) == eg.text.MainFrame.SaveChanges.mesg:
                    break
                ctrl = GetWindow(ctrl, GW_HWNDNEXT)
            if ctrl:
                break
            hwnd = GetWindow(hwnd, GW_HWNDNEXT)
        if ctrl:
            break
        i += 1
    if ctrl and i < 1000:
        BringHwndToFront(hwnd)
#===============================================================================

def GetUid(uids):
    uid = None
    while not uid or uid in uids:
        uid = str(randrange(10000000, 99999999))
    return uid
#===============================================================================

class Text:
    errMess0 = 'Snarl is not running !'
    errMess1 = 'Error during registration to Snarl'
    listLabel = "Notification classes:"
    labelLbl = "Class identifier (name):"
    delete = 'Delete'
    insert = 'Add new'
    titleLabel = "Title:"
    textLabel = "Text:"
    iconLabel = "Icon:"
    soundLabel = "Sound:"
    durationLabel = "Duration [s]:"
    durationLabel2 = "(0 = Sticky; -1 = Snarl default)"
    toolTipFile = "Press button and browse to select a icon file ..."
    browseFile = "Notification icon selection" 
    optPars = "Class %s - standard options (default values)"
    optPars2 = "Class %s - EventGhost specific options (default values)"
    uidIndexLabel = "UID index:"
    uidIndexLabel2 = "(See the description !)"
    gridLabel = "Label"
    gridSuffix = "Event suffix"
    gridPld = "Event payload"
    expired = "Expired"
    invoked = "Invoked"
    closed = "Closed"
    clearTxt = "Clear user menu"
    clearSuff = "Clear table"
    suffLabel = "Events on notification disappearance"
    menuLabel = "User menu"
#===============================================================================

class MenuGrid(gridlib.Grid):

    def __init__(self, parent, plugin, choices = []):
        self.plugin = plugin
        lngth = 8
        gridlib.Grid.__init__(self, parent)
        self.SetRowLabelSize(1)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.CreateGrid(lngth, 3)
        for col in range(3):
            self.SetCellValue(0,col,"XXXXXXXXXXXXXXXX")
        self.Fit()
        self.ClearGrid()
        self.SetColLabelValue(0, plugin.text.gridLabel)
        self.SetColLabelValue(1, plugin.text.gridSuffix)
        self.SetColLabelValue(2, plugin.text.gridPld)
        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        for r in range(lngth):
            self.SetRowLabelValue(r,"")
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0,attr)
        self.SetColAttr(1,attr)
        self.SetColAttr(2,attr)
        self.SetValue(choices)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.SetMargins(
            0-wx.SystemSettings_GetMetric(wx.SYS_VSCROLL_X),
            0-wx.SystemSettings_GetMetric(wx.SYS_HSCROLL_Y)
        )
        self.SetMinSize(self.GetSize())
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnRclick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnRclick)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnChange)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, event):
        w = event.GetSize().width
        w0 = int(w/3.0)
        w1 = int(w/3.0)
        w2 = w - w0 - w1 - 1
        self.SetColSize(0, w0)
        self.SetColSize(1, w1)
        self.SetColSize(2, w2)
        self.ForceRefresh()
        wx.CallAfter(self.ForceRefresh)
        event.Skip() 



    def OnChange(self, evt):
        evt = eg.ValueChangedEvent(self.GetId(), value = self.GetValue())
        wx.PostEvent(self, evt)
        evt.Skip()
        

    def OnClear(self, evt):
        self.ClearGrid()
        evt = eg.ValueChangedEvent(self.GetId(), value = self.GetValue())
        wx.PostEvent(self, evt)
        evt.Skip()


    def OnRclick(self, evt):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnClear, id = self.popupID1)
        menu = wx.Menu()
        menu.Append(self.popupID1, self.plugin.text.clearTxt)
        self.PopupMenu(menu)
        menu.Destroy()


    def GetValue(self):
        value = []
        for r in range(self.GetNumberRows()):
            label = self.GetCellValue(r, 0)
            suffix = self.GetCellValue(r, 1)
            pld = self.GetCellValue(r, 2)
            suffix = "%s.&&PAYLOAD&&%s" % (suffix, pld) if pld else suffix
            if label and suffix: 
                value.append((label, suffix))
        return value


    def SetValue(self, choices):
        self.ClearGrid()
        for i in range(len(choices)):
            self.SetCellValue(i, 0, choices[i][0])
            suffix = choices[i][1]
            sffx = suffix.split(".&&PAYLOAD&&")
            if len(sffx) > 1:
                suffix = sffx[0]
                pld = sffx[1]
            else:
                pld = ""
            self.SetCellValue(i, 1, suffix)
            self.SetCellValue(i, 2, pld)
#===============================================================================

class SuffixGrid(gridlib.Grid):

    def __init__(self, parent, plugin, suffixes = []):
        self.plugin = plugin
        gridlib.Grid.__init__(self, parent)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.CreateGrid(3, 2)
        self.SetColLabelValue(0, plugin.text.gridSuffix)
        self.SetColLabelValue(1, plugin.text.gridPld)
        self.SetRowLabelValue(0, plugin.text.expired)
        self.SetRowLabelValue(1, plugin.text.invoked)
        self.SetRowLabelValue(2, plugin.text.closed)
        self.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0,attr)
        self.SetColAttr(1,attr)
        self.SetCellValue(0,0,"XXXXXXXXXXXXXXXX")
        self.SetCellValue(0,1,"XXXXXXXXXXXXXXXX")
        self.Fit()
        self.ClearGrid()
        self.SetValue(suffixes)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.SetMargins(
            0-wx.SystemSettings_GetMetric(wx.SYS_VSCROLL_X),
            0-wx.SystemSettings_GetMetric(wx.SYS_HSCROLL_Y)
        )
        self.SetMinSize(self.GetSize())
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnRclick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnRclick)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnChange)       
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, event):
        lblW = self.GetRowLabelSize()
        w = event.GetSize().width
        w0 = int((w-lblW)/2.0)
        w1 = w - w0 - lblW - 1
        self.SetColSize(0, w0)
        self.SetColSize(1, w1)
        wx.CallAfter(self.ForceRefresh)
        event.Skip() 
    

    def OnChange(self, evt):
        evt = eg.ValueChangedEvent(self.GetId(), value = self.GetValue())
        wx.PostEvent(self, evt)
        evt.Skip()
        

    def OnClear(self, evt):
        self.ClearGrid()
        evt = eg.ValueChangedEvent(self.GetId(), value = self.GetValue())
        wx.PostEvent(self, evt)
        evt.Skip()
        

    def OnRclick(self, evt):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnClear, id=self.popupID1)
        menu = wx.Menu()
        menu.Append(self.popupID1, self.plugin.text.clearSuff)
        self.PopupMenu(menu)
        menu.Destroy()


    def GetValue(self):
        value = []
        for r in range(self.GetNumberRows()):
            value.append((self.GetCellValue(r, 0), self.GetCellValue(r, 1)))
        return value


    def SetValue(self, suffixes):
        self.ClearGrid()
        for i in range(len(suffixes)):
            item = suffixes[i]
            if not isinstance(item, tuple):
                self.SetCellValue(i,0,suffixes[i])
            else:
                self.SetCellValue(i,0,suffixes[i][0])
                self.SetCellValue(i,1,suffixes[i][1])
#===============================================================================

class SnarlWorkerThread(eg.ThreadWorker):
    """
    Handles the COM interface in a thread of its own.
    """

    snarl = None

    def Setup(self, plugin):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin
        
        class SubEventHandler(pySnarl.EventHandler):
            fn = self.plugin.TriggerEvent

            def TriggEvt(self, suff, payload, uid):
                pld = plugin.uids.index(uid) if uid in plugin.uids else int(uid)
                #if payload is not None:
                #    self.fn("Notification.%s" % suff, payload = pld)
                #else:
                #    self.fn("Notification.%s" % suff, payload = (pld, payload))
                self.fn("Notification.%s" % suff, payload = (pld, payload))
           

            def ReplaceAndParse(self, item, uid):
                item = item.replace(
                    "eg.event",
                    "eg.plugins.Snarl.plugin.suffixes['%s'][3]" % uid
                )
                item = item.replace(
                    "eg.result",
                    "eg.plugins.Snarl.plugin.suffixes['%s'][4]" % uid
                )
                try:
                    item = eg.ParseString(item)
                except:
                    pass
                try:
                    item = eval(item)
                except:
                    pass
                return item


            def GetEvent(self, item, uid):
                if not isinstance(item, tuple):
                    return (item, None)
                suff = self.ReplaceAndParse(item[0], uid)
                payload = self.ReplaceAndParse(item[1], uid)
                return (suff, payload)

            def OnSnarlLaunched(self):
                self.fn("Launched")
                self.Register()

            def OnActivated(self):
                self.fn("DaemonActivated")
                wx.CallAfter(eg.document.ShowFrame)

            def OnNotificationExpired(self, uid):
                suff = "Expired"
                payload = None
                if uid in plugin.suffixes:
                    suff, payload = self.GetEvent(plugin.suffixes[uid][0], uid)
                    del plugin.suffixes[uid]
                self.TriggEvt(suff, payload, uid)

            def OnNotificationInvoked(self, uid):
                suff = "Invoked"
                payload = None
                if uid in plugin.suffixes:
                    suff, payload = self.GetEvent(plugin.suffixes[uid][1], uid)
                    del plugin.suffixes[uid]
                self.TriggEvt(suff, payload, uid)

            def OnNotificationClosed(self, uid):
                suff = "Closed"
                payload = None
                if uid in plugin.suffixes:
                    suff, payload = self.GetEvent(plugin.suffixes[uid][2], uid)
                    del plugin.suffixes[uid]
                self.TriggEvt(suff, payload, uid)

            def OnNotificationActionSelected(self, uid, command):
                cmd = command.split('.&&PAYLOAD&&')
                pld = plugin.uids.index(uid) if uid in plugin.uids else int(uid)
                if len(cmd) > 1 and uid in plugin.suffixes:
                    command = cmd[0]
                    pld1 = self.ReplaceAndParse(cmd[1], uid)
                    payload = (pld, pld1)
                else:
                    payload = (pld,)
                self.fn("UserMenu.%s" % command, payload)

            def OnQuit(self):
                wx.CallAfter(eg.app.Exit)
                if eg.document.isDirty:
                    wx.CallAfter(BringSaveChangesDialog)

            def OnShowAbout(self):
                wx.CallAfter(OnCmdAbout, eg.document.frame)
                wx.CallAfter(BringDialogToFront, eg.text.AboutDialog.Title)

            def OnShowConfig(self):
                plugin.ShowConfig()


        self.SubEventHandler = SubEventHandler

        self.snarl = None
        clss = []
        for item in self.plugin.classes:
            cls=list(item)
            cls.insert(0,item[0]) #identifier = name
            cls.insert(2,True)    #enable
            cls.insert(6,"")      #callback
            clss.append(cls[:-2])
        self.snarl = pySnarl.SnarlApp(
            "EventGhost",                        # signature
            "EventGhost",                        # title
            join(eg.imagesDir, "logo.png"),      # icon
            "",                                  # configTool
            "",                                  # hint
            True,                                # IsDaemon
            self.SubEventHandler,                # event handler
            clss)                                # classes

        if self.snarl.isRunning():
            res = None
            i = 0
            while res != "SUCCESS":
                res = self.Register()
                sleep(0.1)
                i += 1
                if i > 100:
                    break
            if i > 100:
                eg.PrintError(self.plugin.text.errMess1)
                eg.PrintError("STATUS_CODE: %s" % res)


    def IsConnected(self):       
        return self.snarl.isConnected()

            
    def IsVisible(self, uid):
        return self.snarl.isVisible(uid)

            
    def Register(self, autAdd = True): 
        return self.snarl.register()


    def Unregister(self):       
        return self.snarl.unregister()


    def TidyUp(self):       
        return self.snarl.tidyUp()

            
    def SnarlVersion(self):
        return self.snarl.version()

            
    def HideNotification(self, uid):       
        return self.snarl.hideNotification(uid)

            
    def Notify(self, *args):
        return self.snarl.notify(*args)


    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        self.snarl.Destroy() 
        del self.snarl
        self.plugin.thread = None         
#===============================================================================        

class Snarl(eg.PluginBase):
    text = Text
    suffixes = {}
    thread = None

    def __init__(self):
        self.AddActionsFromList(ACTIONS)        
      
    
    def __start__(self, classes = None, uids = None):
        eg.Bind("Main.OnClose", self.TidyUp)      
        self.suffixes = {}
        self.classes = classes
        self.uids = uids
        text = self.text
        self.StartThread()
        if not pySnarl.IsRunning():
            eg.PrintError(text.errMess0)


    def __stop__(self):
        eg.Unbind("Main.OnClose",self.TidyUp)
        if self.thread:
            wx.CallAfter(self.thread.Stop)


    def StartThread(self):
        if self.classes and self.uids:
            if not self.thread:
                eg.scheduler.AddTask(0.1, self.CheckWorkerThread) #Starts thread !!!
            else:
                eg.scheduler.AddTask(0.1, self.StartThread) #wait for Stop thread


    def CheckWorkerThread(self):
        if not self.thread:
            if self.classes and self.uids:
                self.thread = SnarlWorkerThread(self)
                self.thread.Start(100.0)
        if not self.thread:
            return False
        return True


    def HideNotification(self, uid):
        if self.CheckWorkerThread():
            return self.thread.CallWait(
                partial(self.thread.HideNotification, uid),1000
            )


    def Register(self):
        if self.CheckWorkerThread():
            return self.thread.CallWait(
                partial(self.thread.Register),1000
            )


    def Unregister(self):
        if self.CheckWorkerThread():
            return self.thread.CallWait(
                partial(self.thread.Unregister),1000
            )

    def TidyUp(self, event = None):
        if self.CheckWorkerThread():
            return self.thread.CallWait(
                partial(self.thread.TidyUp),1000
            )


    def SnarlVersion(self):
        if self.CheckWorkerThread():
            return self.thread.CallWait(
                partial(self.thread.SnarlVersion),1000
            )


    def Notify(self, *note):
        if self.CheckWorkerThread():
            res = self.thread.CallWait(
                partial(self.thread.Notify, *note[:-1]),1000
            )
            if res == 'SUCCESS':
                self.suffixes[note[12]] = note[-1]
            return res


    def IsConnected(self):
        if self.CheckWorkerThread():
            return self.thread.CallWait(
                partial(self.thread.IsConnected),1000
            )


    def IsVisible(self, *note):
        if self.CheckWorkerThread():
            return self.thread.CallWait(
                partial(self.thread.IsVisible, *note),1000
            )


    def ShowConfig(self):
        autostartChilds = eg.document.__dict__['autostartMacro'].__dict__['childs']
        pluginNode = [item for item in autostartChilds if hasattr(item,'pluginName') and item.pluginName == self.name][0]
        wx.CallAfter(eg.document.OnCmdConfigure, pluginNode)
        wx.CallAfter(
            BringDialogToFront,
            eg.text.General.settingsPluginCaption+" - "+self.name
        )


    def Configure(self, classes = [], uids = None):

        uidMax = 31

        def boxEnable(enable):
            labelCtrl.Enable(enable)
            labelLbl.Enable(enable)
            titleCtrl.Enable(enable)
            titleLabel.Enable(enable)
            textCtrl.Enable(enable)
            textLabel.Enable(enable)
            iconCtrl.Enable(enable)
            soundCtrl.Enable(enable)
            durationCtrl.Enable(enable)
            iconLabel.Enable(enable)
            soundLabel.Enable(enable)
            durationLabel.Enable(enable)
            menuCtrl.Enable(enable)
            suffixCtrl.Enable(enable)
            menuLabel.Enable(enable)
            suffixLabel.Enable(enable)

        def setBox(item):
            labelCtrl.SetValue(item[0])
            box.SetLabel(text.optPars % item[0] if item[0] else "")
            box3.SetLabel(text.optPars2 % item[0] if item[0] else "")
            titleCtrl.ChangeValue(item[1])
            textCtrl.ChangeValue(item[2])
            iconCtrl.SetValue(item[3])
            durationCtrl.SetValue(item[4])
            soundCtrl.SetValue(item[5])
            menuCtrl.SetValue(item[6])
            suffixCtrl.SetValue(item[7])

        text = self.text
        panel = eg.ConfigPanel(self)
        dialog = panel.GetParent().GetParent()
        dialog.SetTitle(dialog.GetTitle()+" - "+self.name) #mandatory for "ShowConfig()" !!!
        self.flag = True
        self.oldSel = 0
        self.clsss = cpy(classes) # MANDATORY [otherwise no Stop/Start at panel.Affirmed() !!!]
        leftSizer = wx.FlexGridSizer(4, 2, 2, 8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        listLabel=wx.StaticText(panel, -1, text.listLabel)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(100, 106),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(panel, -1, text.labelLbl)
        labelCtrl=wx.TextCtrl(panel,-1,'')
        leftSizer.Add(listLabel,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl)
        leftSizer.Add(topMiddleSizer)
        leftSizer.Add(labelLbl,0,wx.TOP,3)
        leftSizer.Add((1,1))
        leftSizer.Add(labelCtrl,0,wx.EXPAND)
        leftSizer.Add((1,1))

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
        mainSizer.Add(leftSizer,0)

        titleLabel = wx.StaticText(panel, -1, text.titleLabel)
        titleCtrl = wx.TextCtrl(panel, -1, "")
        textLabel = wx.StaticText(panel, -1, text.textLabel)
        textCtrl = wx.TextCtrl(panel, -1, "")
        iconLabel = wx.StaticText(panel, -1, text.iconLabel)
        iconCtrl =  eg.FileBrowseButton(
            panel,
            toolTip = text.toolTipFile,
            dialogTitle = text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.Pictures,
        )
        soundLabel = wx.StaticText(panel, -1, text.soundLabel)
        soundCtrl =  eg.FileBrowseButton(
            panel,
            toolTip = text.toolTipFile,
            dialogTitle = text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.Pictures,
        )
        durationLabel = wx.StaticText(panel, -1, text.durationLabel)
        durationLabel2 = wx.StaticText(panel, -1, text.durationLabel2)
        durationCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            -1,
            min=-1,
            max=9999,
        )        

        rightSizer = wx.FlexGridSizer(5, 2, 8, 4)
        rightSizer.AddGrowableCol(1)
        box = wx.StaticBox(panel,-1,text.optPars % "")
        staticSizer = wx.StaticBoxSizer(box,wx.VERTICAL)
        staticSizer.Add(rightSizer,0,wx.EXPAND)
        rightSizer.Add(titleLabel,0,wx.TOP,4)
        rightSizer.Add(titleCtrl,0,wx.EXPAND)
        rightSizer.Add(textLabel,0,wx.TOP,4)
        rightSizer.Add(textCtrl,0,wx.EXPAND)
        rightSizer.Add(iconLabel,0,wx.TOP,4)
        rightSizer.Add(iconCtrl,0,wx.EXPAND)
        rightSizer.Add(soundLabel,0,wx.TOP,4)
        rightSizer.Add(soundCtrl,0,wx.EXPAND)
        durationSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSizer.Add(durationLabel,0,wx.TOP,4)
        rightSizer.Add(durationSizer)
        durationSizer.Add(durationCtrl,0,wx.RIGHT,3)
        durationSizer.Add(durationLabel2,0,wx.TOP,4)
        mainSizer.Add(staticSizer,1,wx.LEFT|wx.EXPAND,10)

        menuLabel = wx.StaticText(panel, -1, text.menuLabel)
        suffixLabel = wx.StaticText(panel, -1, text.suffLabel)
        menuCtrl = MenuGrid(panel, self, [])
        suffixCtrl = SuffixGrid(panel, self, ["","",""])
        box3 = wx.StaticBox(panel,-1,text.optPars2 % "")
        eventSizer = wx.StaticBoxSizer(box3, wx.HORIZONTAL)
        suffixSizer = wx.FlexGridSizer(3, 2, 1, 20)
        suffixSizer.AddGrowableCol(0)
        suffixSizer.AddGrowableCol(1)
        eventSizer.Add(suffixSizer,1,wx.EXPAND)
        suffixSizer.Add((1,2))
        suffixSizer.Add((1,2))
        suffixSizer.Add(menuLabel)
        suffixSizer.Add(suffixLabel)
        suffixSizer.Add(menuCtrl,0,wx.EXPAND)
        xSizer = wx.BoxSizer(wx.VERTICAL)
        xSizer.Add(suffixCtrl,0,wx.EXPAND)
        xSizer.Add((-1,-1),1,wx.EXPAND)
        suffixSizer.Add(xSizer,0,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.EXPAND)
        panel.sizer.Add(eventSizer,0,wx.EXPAND|wx.TOP,8)
        if len(self.clsss) > 0:
            listBoxCtrl.Set([n[0] for n in self.clsss])
            listBoxCtrl.SetSelection(0)
            setBox(self.clsss[0])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            boxEnable(False)
            panel.dialog.buttonRow.applyButton.Enable(False)
            panel.dialog.buttonRow.okButton.Enable(False)
        panel.sizer.Layout()


        def onDefaultTitle(evt):
            self.clsss[self.oldSel][1] = evt.GetString()
            evt.Skip()
        titleCtrl.Bind(wx.EVT_TEXT,  onDefaultTitle)


        def onDefaultText(evt):
            self.clsss[self.oldSel][2] = evt.GetString()
            evt.Skip()
        textCtrl.Bind(wx.EVT_TEXT,  onDefaultText)


        def onDefaultIcon(evt):
            if self.oldSel > -1:
                self.clsss[self.oldSel][3] = evt.GetString()
            evt.Skip()
        iconCtrl.Bind(wx.EVT_TEXT,  onDefaultIcon)


        def onDefaultDuration(evt):
            if self.oldSel > -1:
                self.clsss[self.oldSel][4] = evt.GetValue()
            evt.Skip()
        durationCtrl.Bind(eg.EVT_VALUE_CHANGED,  onDefaultDuration)
        

        def onDefaultSound(evt):
            if self.oldSel > -1:
                self.clsss[self.oldSel][5] = evt.GetString()
            evt.Skip()
        soundCtrl.Bind(wx.EVT_TEXT,  onDefaultSound)


        def onMenuChange(evt):
            self.clsss[self.oldSel][6] = evt.GetValue()
            evt.Skip()
        menuCtrl.Bind(eg.EVT_VALUE_CHANGED, onMenuChange)
        

        def onSuffChange(evt):
            self.clsss[self.oldSel][7] = evt.GetValue()
            evt.Skip()
        suffixCtrl.Bind(eg.EVT_VALUE_CHANGED, onSuffChange)


        def onClick(evt):
            self.flag = False
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            if label.strip() != "":
                if [n[0] for n in self.clsss].count(label) == 1:
                    self.oldSel=sel
                    item = self.clsss[sel]
                    setBox(item)
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
            self.flag = True
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)


        def onButtonUp(evt):
            newSel,self.clsss=Move(self.clsss,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([n[0] for n in self.clsss])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)


        def onButtonDown(evt):
            newSel,self.clsss=Move(self.clsss,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([n[0] for n in self.clsss])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)


        def onButtonDelete(evt):
            self.flag = False
            lngth=len(self.clsss)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.oldSel = -1
                self.clsss=[]
                listBoxCtrl.Set([])
                #classe structure = [name, defTitle, defText, defIcon, defDuration, defSound, defMenu, defSuffixes]
                item = ["", "", "", "", -1, "", [],("","","")]
                setBox(item)
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
            tmp = self.clsss.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in self.clsss])
            listBoxCtrl.SetSelection(sel)
            item = self.clsss[sel]
            setBox(item)
            evt.Skip()
            self.flag = True
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)


        def OnTxtChange(evt):
            if self.clsss != [] and self.flag:
                flag = False
                sel = self.oldSel
                label = labelCtrl.GetValue()
                box.SetLabel(text.optPars % label if label else "")
                box3.SetLabel(text.optPars2 % label if label else "")
                self.clsss[sel][0]=label
                listBoxCtrl.Set([n[0] for n in self.clsss])
                listBoxCtrl.SetSelection(sel)
                if label != "":
                    flag = [n[0] for n in self.clsss].count(label) == 1
                panel.dialog.buttonRow.applyButton.Enable(flag)
                panel.dialog.buttonRow.okButton.Enable(flag)
                btnApp.Enable(flag)
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)


        def OnButtonAppend(evt):
            self.flag = False
            if len(self.clsss)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            #classe structure = [name, defTitle, defText, defIcon, defDuration, defSound, defMenu, defSuffixes]
            item = ["", "", "", "", -1, "", [],("","","")]
            self.clsss.insert(sel,item)
            listBoxCtrl.Set([n[0] for n in self.clsss])
            listBoxCtrl.SetSelection(sel)
            setBox(item)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
            self.flag = True
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)


        while panel.Affirmed():
            if not uids or len(uids) != uidMax:
                uids = []
                for i in range(uidMax):
                    uids.append(GetUid(uids))
                uids = tuple(uids)
            panel.SetResult(self.clsss, uids)
#===============================================================================

class Register(eg.ActionBase):

    def __call__(self):
        return self.plugin.Register()
#===============================================================================

class Unregister(eg.ActionBase):

    def __call__(self):
        return self.plugin.Unregister()
#===============================================================================

class IsConnected(eg.ActionBase):

    def __call__(self):
        return self.plugin.IsConnected()
#===============================================================================

class SnarlVersion(eg.ActionBase):

    def __call__(self):
        return self.plugin.SnarlVersion()
#===============================================================================

class Config(eg.ActionBase):

    def __call__(self):
        self.plugin.ShowConfig()
#===============================================================================

class HideNotification(eg.ActionBase):

    class text:
        isvisibleDecsr = u'''<rst>**Gets "IsVisible" property**

This action is of limited use as there exists the possibility that the
notification will be visible when it is called, but will then immediately
disappear (either due to it expiring, the user clicking it, or some other reason).
Consequently, although the request completed successfully, the actual result is invalid.
For this reason, you should avoid relying on value **True** returned by this action.
On returned value **False** you can rely on (in some cases).
'''     
        hideDecsr = u'''<rst>**Hides the notification**
        
If on screen is found the notification with UID, corresponding to the preset index,
it will be hidden (closed).
'''
    def __call__(self, uidIndex = 0):
        if self.value == 'hide':
            return self.plugin.HideNotification(self.plugin.uids[uidIndex])
        if self.value == 'isvisible':
            result = self.plugin.IsVisible(self.plugin.uids[uidIndex])
            if result == "SUCCESS":
                return True
            elif result == "ERROR_NOTIFICATION_NOT_FOUND":
                return False
            else:
                return result


    def Configure(self, uidIndex = 0):
        ixMax = 31
        panel = eg.ConfigPanel(self)
        uidIndexLabel = wx.StaticText(panel, -1, self.plugin.text.uidIndexLabel)
        uidIndexLabel2 = wx.StaticText(panel, -1, self.plugin.text.uidIndexLabel2)
        uidIndexCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            uidIndex,
            min=0,
            max=ixMax,
        )
        uidIndexSizer = wx.BoxSizer(wx.HORIZONTAL)
        uidIndexSizer.Add(uidIndexLabel,0,wx.TOP,3)
        uidIndexSizer.Add(uidIndexCtrl,0,wx.RIGHT,5)
        uidIndexSizer.Add(uidIndexLabel2,0,wx.TOP,3)
        panel.sizer.Add(uidIndexSizer,0,wx.TOP,30)

        while panel.Affirmed():
            panel.SetResult(
                uidIndexCtrl.GetValue(),
            )
#===============================================================================

class Notify(eg.ActionBase):
    u'''<rst>**Sends notification.**

| **UID index**:
| UID index can take values from 0 to 31, or -1 (see note).
| To each UID index is assigned a fixed UID. Notification  with the same index 
  (and therefore the same UID) is always overwritten by the new. It is convenient 
  (for example) for displaying the volume level.
  Using the action *Hide notification* you can "to delete" a notification with the same index.
  Using the action *Get IsVisible* you can determine whether notification with the 
  appropriate index is currently displayed or not.
| **Note:** *If you set the index of -1, a random UID is used and therefore is no reference 
  to this notification.*

| **Merge UID**:
| If on screen is found any notification with the same index, this new notification
  will be merged with it.

| **Replace UID**:
| The name says it all. However, try the behavior when the *Replace UID = UID* !

| **Priority and duration**:
| If you set a Low priority, notification can not also be Sticky!'''

    class text:
        typeLabel = "Note class:"
        titleLabel = "Title:"
        iconLabel = "Icon:"
        soundLabel = "Sound:"
        priorityLabel = "Priority:"
        durationLabel = "Duration [s]:"
        durationLabel2 = "(0 = Sticky; -1 = default)"
        percentLabel = "Percent value:"
        percentLabel2 = "(0 - 100; -1 = feature disabled)"
        logLabel = "Log:"
        sensLabel = "Sensitivity:"
        sensChoices = (
            "Normal",
            "Personal",
            "Private",
            "Confidential",
            "Restricted",
            "Secret",
            "Top Secret",
        )
        descrLabel = "Text:"
        mergeLabel = "Merge UID:"
        mergeLabel2 = "(-1 = no merge UID)"
        replaceLabel = "Replace UID:"
        replaceLabel2 = "(-1 = no replace UID)"
        priorityChoices = ("Low","Normal     ","High")
        labelBox1 = "User menu (optional)"
        labelBox2 = "Events on notification disappearance (optional)"
        menu = (
            "Change control to Spin Int",
            "Change control to Text with {eg.result}",
            "Change control to Text with {eg.event.payload}",
            "Change control to (empty) Text"
        )
        tooltip = "Use the right mouse button\nto get the context menu !"

    def __call__(
        self,
        noteType = "",
        title = "",
        description = "",
        icon = "",
        priority = 0,
        duration = -1,
        percent = -1,
        uidIndex = -1,
        actions = [],
        sound = "",
        suffixes = ("", "", ""),
        merge = -1,
        replace = -1,
        log = True,
        sens = 0,
        ):
        clsIds = [n[0] for n in self.plugin.classes]
        cls = noteType if noteType in clsIds else ""
        ix = clsIds.index(cls) if cls else None
        sffxs = ["Expired","Invoked","Closed", eg.event, eg.result]
        for i in range(3):
            if suffixes[i]:
                sffxs[i] = suffixes[i]
            elif ix is not None and self.plugin.classes[ix][7][i]:
                sffxs[i] = self.plugin.classes[ix][7][i]
        try:
            dur = duration if isinstance(duration,int) else int(eg.ParseString(duration))
        except:
            dur = -1
        try:
            indx = uidIndex if isinstance(uidIndex,int) else int(eg.ParseString(uidIndex))
        except:
            indx = -1
        try:
            mrg = merge if isinstance(merge,int) else int(eg.ParseString(merge))
        except:
            mrg = -1
        try:
            rplc = replace if isinstance(replace,int) else int(eg.ParseString(replace))
        except:
            rplc = -1
        try:
            prcnt = percent if isinstance(percent,int) else int(eg.ParseString(percent))
        except:
            prcnt = -1
        return self.plugin.Notify(
            self.Actions(actions) if actions else self.Actions(self.plugin.classes[ix][6] if ix is not None else []),
            "",
            "",
            cls, 
            "",
            dur,
            eg.ParseString(icon),
            self.plugin.uids[mrg] if mrg > -1 else "",
            priority - 1,
            self.plugin.uids[rplc] if rplc > -1 else "",
            eg.ParseString(description) if description else "", 
            eg.ParseString(title) if title else "", 
            self.plugin.uids[indx] if indx > -1 else GetUid(self.plugin.uids),
            eg.ParseString(sound), 
            prcnt,
            int(log),
            16*sens,
            sffxs,
        )


    def Actions(self, actions):
        def Parse(item):
            itm = item.split(".&&PAYLOAD&&")
            if len(itm) > 1:
                return "%s.&&PAYLOAD&&%s" % (eg.ParseString(itm[0]), itm[1])
            else:
                return eg.ParseString(item)
        res = []
        for a in actions:
            res.append((eg.ParseString(a[0]), Parse(a[1])))
        return res


    def GetLabel(
        self,
        noteType,
        title,
        description,
        icon,
        priority,
        duration,
        percent,
        uidIndex,
        actions,
        sound,
        suffixes,
        merge,
        replace,
        log,
        sens,
        ):
        return "%s: %s: %s: %s" % (self.name, noteType, title, description)


    def Configure(
        self,
        noteType = "",
        title = "",
        description = "",
        icon = "",
        priority = 1,
        duration = -1,
        percent = -1,
        uidIndex = -1,
        actions = [],
        sound = "",
        suffixes = ("","",""),
        merge = -1,
        replace = -1,
        log = True,
        sens = 0,
        ):

        if hasattr(self.plugin, "classes"):
            pluginFlag = True
            choices = [n[0] for n in self.plugin.classes]
            if noteType == "" and len(self.plugin.classes):
                noteType = choices[0]
        else: # plugin is maybe disabled
            eg.PrintError(eg.text.Error.pluginNotActivated % self.plugin.name)
            pluginFlag = False
            choices = []
        ixMax = 31
        self.p = priority
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.indexId = wx.NewId()
        panel.mergeId = wx.NewId()
        panel.durId = wx.NewId()
        panel.percId = wx.NewId()
        panel.replaceId = wx.NewId()
        panel.ids = (
            panel.indexId,
            panel.mergeId,
            panel.durId,
            panel.percId,
            panel.replaceId,
        )
        panel.activeCtrl = None
        sizer = wx.FlexGridSizer(6, 2, 8, 8)
        box1 = wx.StaticBox(panel,-1,text.labelBox1)
        box2 = wx.StaticBox(panel,-1,text.labelBox2)
        rightSizer_1 = wx.StaticBoxSizer(box1, wx.VERTICAL)
        rightSizer_2 = wx.StaticBoxSizer(box2, wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(rightSizer_1,1,wx.EXPAND)
        rightSizer.Add(rightSizer_2,0,wx.TOP|wx.EXPAND,10)
        mainSizer.Add(sizer,0,wx.EXPAND)
        mainSizer.Add(rightSizer,1,wx.LEFT,10)
        panel.sizer.Add(mainSizer, 1, wx.EXPAND)
        sizer.AddGrowableCol(1)
        uidIndexSizer = wx.BoxSizer(wx.HORIZONTAL)
        mergeSizer = wx.BoxSizer(wx.HORIZONTAL)
        durationSizer = wx.BoxSizer(wx.HORIZONTAL)
        percentSizer = wx.BoxSizer(wx.HORIZONTAL)
        replaceSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        typeLabel = wx.StaticText(panel, -1, text.typeLabel)
        titleLabel = wx.StaticText(panel, -1, text.titleLabel)
        descrLabel = wx.StaticText(panel, -1, text.descrLabel)
        iconLabel = wx.StaticText(panel, -1, text.iconLabel)
        soundLabel = wx.StaticText(panel, -1, text.soundLabel)
        priorityLabel = wx.StaticText(panel, -1, text.priorityLabel)
        durationLabel = wx.StaticText(panel, -1, text.durationLabel)
        durationLabel2 = wx.StaticText(panel, -1, text.durationLabel2)
        percentLabel = wx.StaticText(panel, -1, text.percentLabel)
        percentLabel2 = wx.StaticText(panel, -1, text.percentLabel2)
        logLabel = wx.StaticText(panel, -1, text.logLabel)
        sensLabel = wx.StaticText(panel, -1, text.sensLabel)
        uidIndexLabel = wx.StaticText(panel, -1, self.plugin.text.uidIndexLabel)
        sizer.Add(uidIndexLabel,0,wx.TOP,6)
        uidIndexLabel2 = wx.StaticText(panel, -1, self.plugin.text.uidIndexLabel2)
        mergeLabel = wx.StaticText(panel, -1, text.mergeLabel)
        mergeLabel2 = wx.StaticText(panel, -1, text.mergeLabel2)
        replaceLabel = wx.StaticText(panel, -1, text.replaceLabel)
        replaceLabel2 = wx.StaticText(panel, -1, text.replaceLabel2)
        
        params = (
            (uidIndexLabel2, 1, uidIndex, ixMax),
            (mergeLabel2, 3, merge, ixMax),
            (durationLabel2, 19, duration, 9999),
            (percentLabel2, 21, percent, 100),
            (replaceLabel2, 5, replace, ixMax),
        )
        
        typeCtrl = wx.Choice(panel, -1, choices = choices)
        typeCtrl.SetStringSelection(noteType)
        typeCtrl.Enable(pluginFlag)
        uidIndexLabel2.Enable(pluginFlag)
        titleCtrl = wx.TextCtrl(panel, -1, title)
        descrCtrl = wx.TextCtrl(panel, -1, description)
        iconCtrl =  eg.FileBrowseButton(
            panel,
            toolTip = self.plugin.text.toolTipFile,
            dialogTitle = self.plugin.text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.Pictures,
        )
        iconCtrl.SetValue(icon)
        soundCtrl =  eg.FileBrowseButton(
            panel,
            toolTip = self.plugin.text.toolTipFile,
            dialogTitle = self.plugin.text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.Pictures,
        )
        soundCtrl.SetValue(sound)
        priorityCtrl = wx.RadioBox(
            panel, -1, choices = text.priorityChoices, style = wx.RA_SPECIFY_COLS
        )
        priorityCtrl.SetSelection(priority)
        logCtrl = wx.CheckBox(panel, -1, "")
        logCtrl.SetValue(log)
        sensCtrl = wx.Choice(panel, -1, choices = self.text.sensChoices)
        sensCtrl.SetSelection(sens)


        def OnMenu(evt):
            CreateCtrl(panel.popups.index(evt.GetId()), panel.activeCtrl, False)


        def OnRclick(evt):
            ctrl = evt.GetEventObject()
            if "BaseMaskedTextCtrl" in str(ctrl):
                ctrl = ctrl.GetParent()
            panel.activeCtrl = ctrl.GetId()
            if not hasattr(panel, "popupId0"):
                panel.popupId0 = wx.NewId()
                panel.popupId1 = wx.NewId()
                panel.popupId2 = wx.NewId()
                panel.popupId3 = wx.NewId()
                panel.popups=(
                    panel.popupId0,
                    panel.popupId1,
                    panel.popupId2,
                    panel.popupId3
                )
                panel.Bind(wx.EVT_MENU, OnMenu, id=panel.popupId0)
                panel.Bind(wx.EVT_MENU, OnMenu, id=panel.popupId1)
                panel.Bind(wx.EVT_MENU, OnMenu, id=panel.popupId2)
                panel.Bind(wx.EVT_MENU, OnMenu, id=panel.popupId3)
            menu = wx.Menu()
            for i in range(4):
                menu.Append(panel.popups[i], text.menu[i])
            panel.PopupMenu(menu)
            menu.Destroy()

        menuCtrl = MenuGrid(panel, self.plugin, actions)
        suffixCtrl = SuffixGrid(panel, self.plugin, suffixes)
        rightSizer_1.Add(menuCtrl,1,wx.EXPAND)
        rightSizer_2.Add(suffixCtrl,1,wx.EXPAND)
        uidIndexCtrl = wx.TextCtrl(panel, panel.indexId, "")
        mergeCtrl = wx.TextCtrl(panel, panel.mergeId, "")
        replaceCtrl = wx.TextCtrl(panel, panel.replaceId, "")
        durationCtrl = wx.TextCtrl(panel, panel.durId, "")
        percentCtrl = wx.TextCtrl(panel, panel.percId, "")

        uidIndexSizer.Add(uidIndexCtrl,0,wx.RIGHT,5)
        mergeSizer.Add(mergeCtrl,0,wx.RIGHT,5)            
        durationSizer.Add(durationCtrl,0,wx.RIGHT,5)
        percentSizer.Add(percentCtrl,0,wx.RIGHT,5)
        replaceSizer.Add(replaceCtrl,0,wx.RIGHT,5)            
        sizer.Add(uidIndexSizer,0,wx.TOP,3)               #1
        sizer.Add(mergeLabel,0,wx.TOP,6)
        sizer.Add(mergeSizer,0,wx.TOP,3)                  #3
        sizer.Add(replaceLabel,0,wx.TOP,6)
        sizer.Add(replaceSizer,0,wx.TOP,3)                #5
        sizer.Add(typeLabel,0,wx.TOP,3)
        sizer.Add(typeCtrl,1,wx.EXPAND)
        sizer.Add(titleLabel,0,wx.TOP,3)
        sizer.Add(titleCtrl,1,wx.EXPAND)
        sizer.Add(descrLabel,0,wx.TOP,3)
        sizer.Add(descrCtrl,1,wx.EXPAND)
        sizer.Add(iconLabel,0,wx.TOP,3)
        sizer.Add(iconCtrl,1,wx.EXPAND)
        sizer.Add(soundLabel,0,wx.TOP,3)
        sizer.Add(soundCtrl,1,wx.EXPAND)
        sizer.Add(priorityLabel,0,wx.TOP,5)
        sizer.Add(priorityCtrl,0,wx.EXPAND|wx.TOP,-8)
        sizer.Add(durationLabel,0,wx.TOP,-2)
        sizer.Add(durationSizer,0,wx.TOP,-5)              #19
        sizer.Add(percentLabel,0,wx.TOP,-2)
        sizer.Add(percentSizer,0,wx.TOP,-5)               #21
        sizer.Add(logLabel)
        sizer.Add(logCtrl)
        sizer.Add(sensLabel,0,wx.TOP,3)
        sizer.Add(sensCtrl,1,wx.EXPAND)

        def CreateCtrl(ctrlType, id, init = True):
            ctrl = wx.FindWindowById(id)
            ix = panel.ids.index(id)
            lblCtrl = params[ix][0]
            szr = sizer.GetItem(params[ix][1]).GetSizer()
            szr.Detach(ctrl)
            szr.Detach(lblCtrl)
            ctrl.Destroy()
            if ctrlType == 0:
                ctrl = eg.SpinIntCtrl(
                    panel,
                    id,
                    -1,
                    min = -1,
                    max = params[ix][3],
                )
                ctrl.SetMinSize((48, -1))
                ctrl.numCtrl.Bind(wx.EVT_RIGHT_UP, OnRclick)
                ctrl.numCtrl.SetToolTipString(text.tooltip)
                if init:
                    ctrl.SetValue(params[ix][2])
            else:
                ctrl = wx.TextCtrl(panel, id, "")
                ctrl.Bind(wx.EVT_RIGHT_UP, OnRclick)
                ctrl.SetToolTipString(text.tooltip)
                if init:
                    ctrl.SetValue(params[ix][2])
                else:
                    ctrl.SetValue(("","{eg.result}","{eg.event.payload}","")[ctrlType])
            szr.Add(ctrl,0,wx.RIGHT,5)
            szr.Add(lblCtrl,0,wx.TOP,3)
            szr.Layout()
        CreateCtrl(int(not isinstance(uidIndex, int)), panel.ids[0])
        CreateCtrl(int(not isinstance(merge, int)),    panel.ids[1])
        CreateCtrl(int(not isinstance(replace, int)),  panel.ids[4])
        CreateCtrl(int(not isinstance(duration, int)), panel.ids[2])
        CreateCtrl(int(not isinstance(percent, int)),  panel.ids[3])

        while panel.Affirmed():
            panel.SetResult(
                typeCtrl.GetStringSelection(),
                titleCtrl.GetValue(),
                descrCtrl.GetValue(),
                iconCtrl.GetValue(),
                priorityCtrl.GetSelection(),
                wx.FindWindowById(panel.durId).GetValue(),
                wx.FindWindowById(panel.percId).GetValue(),
                wx.FindWindowById(panel.indexId).GetValue(),
                menuCtrl.GetValue(),
                soundCtrl.GetValue(),
                suffixCtrl.GetValue(),
                wx.FindWindowById(panel.mergeId).GetValue(),
                wx.FindWindowById(panel.replaceId).GetValue(),
                logCtrl.GetValue(),
                sensCtrl.GetSelection(),
            )
#===============================================================================

ACTIONS = (
            (Notify,"Notify","Show notification",Notify.__doc__,None),
            (HideNotification,"HideNotification","Hide notification",HideNotification.text.hideDecsr,"hide"),
            (HideNotification,"IsVisible","Get IsVisible",HideNotification.text.isvisibleDecsr,"isvisible"),
            (Register,"Register","Register","Register.",None),    
            (Unregister,"Unregister","Unregister","Unegister.",None),    
            (SnarlVersion,"SnarlVersion","Get Snarl Version","Gets Snarl Version.",None),    
            (IsConnected,"IsConnected","Get IsConnected","Return connect status.",None),    
            (Config,"Config","Show plugin config","Shows plugin config.",None),    
        )
#===============================================================================
