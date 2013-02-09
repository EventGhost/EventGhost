# -*- coding: utf-8 -*-

version = "0.1.1"

# plugins/NMS/__init__.py
#
# Copyright (C) 2013  Pako <lubos.ruckl@quick.cz>
#
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.1.1 by Pako 2013-02-09 09:50 GMT+1
#     - bugfix - delete a apikeys from list ...
#       subclass not exists in self.text class
# 0.1.0 by Pako 2013-02-07 18:13 GMT+1
#     - bugfix - sometimes (when you start EventGhost) the Notify
#       subclass not exists in self.text class
# 0.0.5 by Pako 2013-02-07 12:00 GMT+1
#     - added try/except block in "UpdateIcon" function
# 0.0.4 by Pako 2013-02-06 19:09 GMT+1
#     - added function "change icons by smartphone type"
#     - plugin renamed to "NMS"
# 0.0.3 by Pako 2013-02-03 16:58 GMT+1
#     - created a separate dialog for setting optional parameters
# 0.0.2 by krambriw 2013-02-02
#     - review and minor edits of text strings
# 0.0.1 by Pako 2013-02-02 11:14 GMT+1
#     - bugfix ("Notify" action - when selected API keys are of same type)
# 0.0.0 by Pako 2013-02-01 18:16 GMT+1
#     - initial version
#===============================================================================
ICON = (
    "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"
)

eg.RegisterPlugin(
    name = "NMS",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{9C4E008B-3B2A-45C9-BEBD-92B58131A2DC}",
    createMacrosOnAdd = False,
    icon = ICON,
    description = ur'''<rst>
**Notify My Smartphone**

Sends push notifications to your Android device and/or iPhone/iPad.

NMA_ is a platform that allows you to deliver push notifications
from virtually any application to your Android device.

Prowl_ is a platform that allows you to deliver push notifications
from virtually any application to your iPhone/iPad.

An account is required to use NMA_ on your Android device.
After registration, you can create any number
of API keys on the 'My Account' page.

An account is required to use Prowl_ on your iPhone/iPad.
After registration, you can create a API key on the 'Settings' page.

**Note:** *The Batch mode is only useful if you have selected more (than one) 
API keys of the same type (NMA or Prowl). Batch mode is applied separately for 
NMA and separately for Prowl.*

-----

This plugin is based on a libraries pynma_ and pyrowl_ by Damien Degois.

.. _NMA:    https://www.notifymyandroid.com
.. _Prowl:  https://www.prowlapp.com
.. _pynma:  https://github.com/babs/pyrowl
.. _pyrowl: https://github.com/babs/pyrowl/tree/master
    ''',
    #url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5207",
)
#===============================================================================

from Image import ANTIALIAS, open as openImage
from pynma import PyNMA
from pyrowl import Pyrowl
from cStringIO import StringIO
from base64 import b64decode, b64encode
from eg.Icons import DISABLED_PIL, PilToBitmap

SPACE = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAIUlEQVR42mNkoBAwjhow"
    "asCoAagGMLFyMf37/e3f0PMCAPkCBBGrN8S0AAAAAElFTkSuQmCC"
)

DROID = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACgklEQVR42mNkwAJOXlgc"
    "Zm4QuwpZ7MrdZVk6ylHT0NUyYjPg8OX+3mv398m9+fpUjomRkUFCQOmtloLzEXONjDa8"
    "Bvz+e4t98e5a+8evrmz5+vMd67///8DizIzMDDycol9N1dxDPMy6duA04NHXtfxz11Rd"
    "Z2Pn+s7w/zf/h09vhRkY/jOICMo9+Pf/jzg7C8/3nMAZUmxMWj9RDHj/+RajIK/a/41H"
    "iwKPXF2+joGBCSj6D838/wyM/1kZIpwr7Y1UMg+hGLDpeH7is9f3PDXkrHe8/Xiz+d9/"
    "5n/////7C9IEUQKh2dh4xAU45czvPj+ZoCiru8tJr24H2ICG+Vqrvv55E6oha7P4+uMj"
    "sYz/gcJADKJgbvgPMoPpP4MQq0rqh193ZosKya0sDTkdAZavnaO+6vv/d6Fq0laLbz89"
    "EQvW+R9kBsjZjGD7gQywadx/ZVK/Mz+ZLcAjuboq8kIYkgHvgQZYLr4FNACklgGmEdkT"
    "QBdw4TNAXcZ66c0nx6LBtv5HD0KEAd+YnswW5EUyoGO56eIPX17GmGh6rjtxfUMQyAX/"
    "gYYwwqyGUUAJcS6t5FffbsxVkTLcle6zzR1swNUni3VevLqtev/lZd6bT44uZPjHiCWN"
    "MgF99Y/BTifaiYmB0UGAW2KZjV7pTRRlW45UKj39cHHz609PlD58ecUhIaz45P///5yv"
    "3t8XFuGX+s7LKXbZUic00FAx5RnevNC1xmTjq7eP/aQFjPy4ONl1b7883qogarA0J2Bn"
    "DFGZqXOl8TqgKwKFOJXdBXhFDO+/OtkhL6q7OCdgTxxRBszfEZ737svLMllRfUcmpj8S"
    "T17f3CwuKJMT6bhgCbpaAD1wHSBoET6EAAAAAElFTkSuQmCC"
)

FRUIT = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACZklEQVR42mNkIAJMOt6U"
    "9fX7W6NKp4kp6HKMhDTX7E1dfP3juRhpFulNk/w2+ZNkwOorM/zWXV+ykfU/M4OdvFtY"
    "inn1aoIGnPtwUPnl+/v8enL6Hxdum+P3nOF+gwSzWpG1gcv5P/9//XCRDrqG1YCjdzaK"
    "7ri3ZdXdz9cd/v3+xSDEJ8Qg8F9iEycHB8ObL08sX/14LfofqFyYTfKcs7pncZBW2gG4"
    "Af9+XOSbc6D52PUv97QZmBgZmP4xM/xl/AuUZASr+PufgYGZAaid8T/DPyAtzG3WX+s+"
    "swhuwId7Xe1/b02pAClC8dR/NP/+Y2X4K6DyRMCwSYWJ0+In3IDX+6M2Mr0+6AexB1Mj"
    "3LeM/xgYFKOzRUw7pqGEwbNFYWf/399txPiPEeGC/5hB/JcZ6CmrrGwZ52ZUA261+i5m"
    "u3sp5h/TbyTnQ3UzIpzDxMDKwKzsNFe2cn4KigGnosKzOK/cmQoKNojzGeH++A8Oyv9g"
    "LiPTf4Zf7JyfOIxNLHVnTLgGN+BGU7/onbUHHrP8YmWH2PsPbB9YOyNQO1j/f2AI/WH4"
    "xcTE8Jud4yenvZ6Re3/lNbgv+/U7pzJ9+5mFYitSeIIMAkYwAygiWfhYnyTNzlfhNOT8"
    "CTdgf/1mmU133z1+/puDgfXvT2AQsDAAXQxMD5DQZAS74h8DB8NfBjt13rD41qDVGEk5"
    "Y9W50KOPf636+IeRgeX/HwYRXqBhLCwMLz5+Z/gNtJ0J6Ak7Fda5VX462RosTD8xDACB"
    "rhMP/S4+eusnxMV+INtDczVIYfeRqw5773xyN5DkudPhrjsXWT0AjVPqEcAA8qsAAAAA"
    "SUVORK5CYII="
)
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
    apiList = 'List of API keys:'
    sLabel = 'Short description:'
    lLabel = 'Long description (optional):'
    apiLabel = 'API key:'
    develLabel = 'NMA - developer API key:'
    providLabel = 'Prowl - provider API key:'
    delete = 'Delete'
    insert = 'Add new'
    dialog = "Advanced settings"
    ok = "OK"
    cancel = "Cancel"
    errMess1 = 'NMA: Unknown API key "%s"'
#===============================================================================

class OptParamsDialog(wx.Frame):

    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL,
            name="Optional parameters"
        )
        self.panel = parent
        self.plugin = plugin
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.devel = self.panel.devel
        self.provid = self.panel.provid


    def ShowOptParamsDialog(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)


        text = self.plugin.text
        panel = wx.Panel(self)
        develLabel = wx.StaticText(panel, -1, text.develLabel)
        w = develLabel.GetTextExtent(6 * '00000000')[0]
        develCtrl = wx.TextCtrl(panel, -1, self.devel, size=(w + w/20, -1))
        providLabel = wx.StaticText(panel, -1, text.providLabel)
        providCtrl = wx.TextCtrl(panel, -1, self.provid, size=(w + w/20, -1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        optionSizer = wx.BoxSizer(wx.VERTICAL)
        flexSizer = wx.FlexGridSizer(2, 2, 4, 4)
        flexSizer.AddGrowableCol(1)
        optionSizer.Add(flexSizer,1,wx.ALL|wx.EXPAND,8)
        sizer.Add(optionSizer,1,wx.EXPAND)
        flexSizer.Add(develLabel,0,wx.TOP,2)
        flexSizer.Add(develCtrl,0,wx.EXPAND)
        flexSizer.Add(providLabel,0,wx.TOP,2)
        flexSizer.Add(providCtrl,0,wx.EXPAND)
        line = wx.StaticLine(
            panel,
            -1,
            size = (20,-1),
            style = wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,6))
        sizer.Fit(self)

        def onChangeApi(evt):
            str1 = develCtrl.GetValue()
            flg1 = len(str1) in (0, 48)
            if flg1:
                self.devel = str1
            str2 = providCtrl.GetValue()
            flg2 = len(str2) in (0, 40)
            if flg2:
                self.provid = str2
            btn1.Enable(flg1 and flg2)
            evt.Skip()
        develCtrl.Bind(wx.EVT_TEXT, onChangeApi)
        providCtrl.Bind(wx.EVT_TEXT, onChangeApi)

        def onClose(evt):
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)
   

        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)
        

        def onOK(evt):
            self.panel.devel = self.devel
            self.panel.provid = self.provid
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)
        
        sizer.Layout()
        self.Raise()
        self.Show()
#===============================================================================

class ApiListCtrl(wx.ListCtrl):

    def __init__(self, parent, id, plugin, size):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
            wx.LC_NO_HEADER | wx.LC_SINGLE_SEL, size = size)
        self.plugin = plugin
        self.sel = -1
        il = wx.ImageList(16, 16)
        stream_sp = StringIO(b64decode(SPACE))
        idx0 = il.Add(wx.BitmapFromImage(wx.ImageFromStream(stream_sp)))
        stream_dr = StringIO(b64decode(DROID))
        idx1 = il.Add(wx.BitmapFromImage(wx.ImageFromStream(stream_dr)))
        stream_fr = StringIO(b64decode(FRUIT))
        idx2 = il.Add(wx.BitmapFromImage(wx.ImageFromStream(stream_fr)))
        self.il = il
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')
        self.InsertColumn(1, '')
        SYS_VSCROLL_X  = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
        self.SetColumnWidth(0, 20)
        self.SetColumnWidth(1, size[0] - 25 - SYS_VSCROLL_X)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.Set()


    def SelRow(self, row):
        if row != self.sel:
            if self.sel in range(self.GetItemCount()):
                item = self.GetItem(self.sel)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.sel = row
            self.SetItemState(row,wx.LIST_STATE_SELECTED,wx.LIST_STATE_SELECTED)
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)


    def SetSelection(self, row):
        self.SelRow(row)


    def GetSelection(self):
        return self.sel


    def OnSelect(self, event):
        self.SelRow(event.GetIndex())
        event.Skip()


    def Set(self):
        lst = self.plugin.apikeys
        self.sel = -1
        self.DeleteAllItems()
        for i, itm in enumerate(lst):
            ix = (40, 40, 48).count(len(itm[1]))
            self.InsertImageStringItem(i, " ", ix)
            self.SetStringItem(i, 1, itm[0])
#===============================================================================

class NMS(eg.PluginClass):
    apikeys = []
    text = Text
    bmp = (0, None)

    def __init__(self):
        self.AddAction(Notify)

    def __start__(self, apikeys = [], devel = "", provid = ""):
        self.apikeys = apikeys
        self.devel = devel
        self.provid = provid
        # It may be necessary to change some icon ... :
        if hasattr(self.text, "Notify"):
            notifActions = self.GetActions(self.text.Notify.name)         
            for act in notifActions:
                if act.parent in eg.document.expandedNodes:
                    nList, pList = self.GetApiKeyLsts(act.args[0], self.apikeys)
                    ix = -1 + int(nList > []) + 2 * int(pList > [])
                    wx.CallAfter(self.UpdateIcon, act, ix)


    def Configure(self, apikeys = [], devel = "", provid = ""):

        def boxEnable(enable):
            shortCtrl.Enable(enable)
            sLabel.Enable(enable)
            longCtrl.Enable(enable)
            lLabel.Enable(enable)
            apiCtrl.Enable(enable)
            apiLabel.Enable(enable)

        def setValue(item):
            shortCtrl.ChangeValue(item[0])
            apiCtrl.ChangeValue(item[1])
            longCtrl.ChangeValue(item[2])

        text = self.text
        self.apikeys = apikeys[:]
        self.oldSel = 0
        self.flag = True
        panel = eg.ConfigPanel(self)
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        panel.devel = devel
        panel.provid = provid
        leftSizer = wx.FlexGridSizer(4, 2, 2, 8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        apiListLbl=wx.StaticText(panel, -1, text.apiList)
        listBoxCtrl = ApiListCtrl(
            panel,
            -1,
            self,
            wx.Size(160, 106),
        )
        sLabel = wx.StaticText(panel, -1, text.sLabel)
        shortCtrl = wx.TextCtrl(panel,-1,'')
        apiLabel = wx.StaticText(panel, -1, text.apiLabel)
        apiCtrl = wx.TextCtrl(panel,-1,'')
        lLabel = wx.StaticText(panel, -1, text.lLabel)
        longCtrl = wx.TextCtrl(panel,-1,'',style=wx.TE_MULTILINE)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(lLabel,0,wx.TOP,5)
        rightSizer.Add(longCtrl,1,wx.TOP|wx.EXPAND,1)
        leftSizer.Add(apiListLbl,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl)
        leftSizer.Add(topMiddleSizer)
        leftSizer.Add(sLabel,0,wx.TOP,3)
        leftSizer.Add((1,1))
        leftSizer.Add(shortCtrl,0,wx.EXPAND)

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
        w1 = panel.GetTextExtent(text.delete)[0]
        w2 = panel.GetTextExtent(text.insert)[0]
        if w1 > w2:
            btnDEL = wx.Button(panel,-1,text.delete)
            btnApp = wx.Button(panel,-1,text.insert,size=btnDEL.GetSize())
        else:
            btnApp = wx.Button(panel,-1,text.insert)
            btnDEL = wx.Button(panel,-1,text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer)
        mainSizer.Add(rightSizer,1,wx.LEFT|wx.EXPAND,10)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)
        panel.sizer.Add(apiLabel,0,wx.TOP,4)
        panel.sizer.Add(apiCtrl,0,wx.TOP|wx.EXPAND,2)
        dialogButton = wx.Button(panel,-1,self.text.dialog + " ...")
        panel.sizer.Add(dialogButton,0,wx.TOP,15)
        
        def OnDialogBtn(evt):
            dlg = OptParamsDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowOptParamsDialog,
                self.text.dialog,
            )
            evt.Skip()
        dialogButton.Bind(wx.EVT_BUTTON, OnDialogBtn)        

        if len(self.apikeys) > 0:
            listBoxCtrl.Set()
            listBoxCtrl.SetSelection(0)
            setValue(self.apikeys[0])
            self.oldSel = 0
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
            sel = evt.GetIndex()
            sLabel = shortCtrl.GetValue()
            if sLabel.strip() <> "":
                if [n[0] for n in self.apikeys].count(sLabel) == 1:
                    self.oldSel = sel
                    item = self.apikeys[sel]
                    setValue(item)
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
            self.flag = True
        listBoxCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, onClick)

        def onButtonUp(evt):
            newSel,self.apikeys=Move(self.apikeys,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set()
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)

        def onButtonDown(evt):
            newSel,self.apikeys=Move(self.apikeys,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set()
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        def OnButtonAppend(evt):
            self.flag = False
            if len(self.apikeys) == 1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel = sel
            item = ['', '', '']
            self.apikeys.insert(sel, item)
            listBoxCtrl.Set()
            listBoxCtrl.SetSelection(sel)
            setValue(item)
            shortCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
            self.flag = True
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

        def onButtonDelete(evt):
            self.flag = False
            lngth = len(self.apikeys)
            if lngth == 2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.apikeys=[]
                listBoxCtrl.Set([])
                item = ['', '', '']
                setValue(item)
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
            tmp = self.apikeys.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set()
            listBoxCtrl.SetSelection(sel)
            item = self.apikeys[sel]
            setValue(item)
            evt.Skip()
            self.flag = True
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)


        def OnTxtChange(evt):
            id = evt.GetId()
            if self.apikeys <> [] and self.flag:
                flag = True
                sel = self.oldSel
                sDescr = shortCtrl.GetValue()
                apikey = apiCtrl.GetValue()
                lDescr = longCtrl.GetValue()
                self.apikeys[sel][0] = sDescr
                self.apikeys[sel][1] = apikey
                self.apikeys[sel][2] = lDescr
                listBoxCtrl.Set()
                listBoxCtrl.SetSelection(sel)
                if sDescr.strip() <> "":
                    if [n[0] for n in self.apikeys].count(sDescr) > 1:
                        flag = False
                else:
                    flag = False
                if len(apikey) == 48 or len(apikey) == 40:
                    if [n[1] for n in self.apikeys].count(apikey) > 1:
                        flag = False
                else:
                    flag = False
                panel.dialog.buttonRow.applyButton.Enable(flag)
                panel.dialog.buttonRow.okButton.Enable(flag)
                btnApp.Enable(flag)
            evt.Skip()
            wx.FindWindowById(id).SetFocus()
        shortCtrl.Bind(wx.EVT_TEXT, OnTxtChange)
        apiCtrl.Bind(wx.EVT_TEXT, OnTxtChange)
        longCtrl.Bind(wx.EVT_TEXT, OnTxtChange)

        while panel.Affirmed():
            panel.SetResult(
            self.apikeys,
            panel.devel,
            panel.provid
        )


    def StringIcon(self, data):
        stream = StringIO(b64decode(data))
        pil = openImage(stream).convert("RGBA")
        stream.close()
        return pil 



    def setItemImage(self, id, ix, tc):

        def equal(b1, b2):
            if not b1 or not b2:
                return
            if b1.ConvertToImage().GetData() == b2.ConvertToImage().GetData():
                return True

        il = tc.GetImageList()
        cnt = il.GetImageCount()
        idx0 = self.bmp[0]
        if idx0 < cnt-1 and equal(il.GetBitmap(idx0), self.bmp[1]):
            pass
        else:
            im0 = self.StringIcon(DROID)
            idx0 = il.Add(PilToBitmap(im0))
            im1 = im0.copy()
            im1.paste(DISABLED_PIL, None, DISABLED_PIL)
            idx1 = il.Add(PilToBitmap(im1))
            im2 = self.StringIcon(FRUIT)
            idx2 = il.Add(PilToBitmap(im2))
            im3 = im2.copy()
            im3.paste(DISABLED_PIL, None, DISABLED_PIL)
            idx3 = il.Add(PilToBitmap(im3))
            box = (8, 0, 16, 16)
            region = im0.crop(box)
            im2.paste(region, box)                      
            idx4 = il.Add(PilToBitmap(im2))
            im2.paste(DISABLED_PIL, None, DISABLED_PIL)
            idx5 = il.Add(PilToBitmap(im2))
            self.bmp = (idx0, il.GetBitmap(idx0))
        tc.SetItemImage(id, ix+idx0)


    def UpdateIcon(self, xmlNode, ix):
        tc = eg.document.frame.treeCtrl
        def Traverse(item):
            if tc.GetPyData(item) == xmlNode:
                return item
            elif tc.ItemHasChildren(item):
                child, cookie = tc.GetFirstChild(item)
                while child.IsOk():
                    res = Traverse(child)
                    if res:
                        return res
                    child, cookie = tc.GetNextChild(child, cookie)
        try:
            ti = Traverse(tc.GetRootItem())
            if ti:
                self.setItemImage(ti, int(not xmlNode.isEnabled) + 2 * ix, tc)
        except:
            pass


    def GetActions(self, actName):
        def Traverse(item):
            if item.__class__ == eg.document.ActionItem:
                if item.executable.name == actName and\
                item.executable.plugin.name == self.name and item.args:
                    actions.append(item)
            elif item and item.childs:
                    for child in item.childs:
                        Traverse(child)
        actions = []
        Traverse(eg.document.__dict__['root'])
        return actions


    def changeIcon(self, action, ix):

        def Traverse(item):
            if item.__class__ == eg.document.ActionItem:
                if item.executable == action:
                    return item
            elif item and item.childs:
                for child in item.childs:
                    result = Traverse(child)
                    if result:
                        break
                return result

        root = eg.document.__dict__['root']
        act = Traverse(root)
        if act:
            wx.CallAfter(self.UpdateIcon, act, ix)


    def GetApiKeyLsts(self, apikeys, apis):
        nmaList = []
        prowlList = []
        for api in apikeys:
            keys = [i[0] for i in apis]
            if api in keys:
                ix = keys.index(api)
                api = [i[1] for i in apis][ix]
                if len(api) == 48:
                    nmaList.append(api)
                elif len(api) == 40:
                    prowlList.append(api)
            else:
                eg.PrintError(text.errMess1 % api)
        return (nmaList, prowlList)
#===============================================================================

class Notify(eg.ActionBase):

    class text:
        errMess2 = 'NMA: There is no valid API key available.'
        errMess3 = 'NMA: Sending notification failed.'
        errMess4 = 'Cause: %s (error %s)'
        empty    = '>>EMPTY<<'
        apiLabel = "Use these API keys:"
        appLabel = "Application:"
        eventLabel = "Event:"
        descrLabel = "Description (payload):"
        urlLabel = "Url:"
        priorityLabel = "Priority:"
        batch_mode = "Batch mode:"
        resType = 'EventGhost result:'
        resTypes = (
            'Full',
            'Short'
        )
        subst = 'Use a short description instead of the API key'
        prnt = 'The result to print to EventGhost log'
        rslt = "Result: %s"
        priorities = (
            "Very Low",
            "Moderate",
            "Normal",
            "High",
            "Emergency"
        )
        batchTip = """Warning: using batch_mode will return error only if all
 the API keys are bad (and success if at least one API is OK)"""


    def GetLabel(
        self,
        apikeys,
        app,
        event,
        description,
        url,
        priority,
        batch_mode,
        resType,
        subst,
        prnt
        ):
#WARNING:self.plugin.apikeys may be an empty list at the time of the first call
# therefore, we use self.plugin.info.treeItem ... GetArguments()[0]
        trItem = self.plugin.info.treeItem
        apis = list(trItem.GetArguments())[0]       
        event = event if event else self.text.empty
        nmaList, prowlList = self.plugin.GetApiKeyLsts(apikeys, apis)
        ix = -1 + int(nmaList > []) + 2 * int(prowlList > [])
        wx.CallAfter(self.plugin.changeIcon, self, ix)
        return "%s: %s" % (self.name, event)   


    def __call__(
        self,
        apikeys = [],
        app = u"EventGhost",
        event = u"{eg.event.string}",
        description = u"{eg.event.payload}",
        url = "",
        priority = 0,
        batch_mode = False,
        resType = 1,
        subst = True,
        prnt = False
        ):
        text = self.text
        app = eg.ParseString(app) if app else "EventGhost"
        event = eg.ParseString(event) if event else text.empty
        description = eg.ParseString(description) if description else text.empty
        url = eg.ParseString(url)
        if url:
            if url.lower()[:7] != r"http://" and url.lower()[:8] != r"https://":
                url = r"http://" + url
        nmaResult = {}
        prowlResult = {}
        nmaRes = {}
        prowlRes = {}
        apis = self.plugin.apikeys
        nmaList, prowlList = self.plugin.GetApiKeyLsts(apikeys, apis)
        if nmaList:
            try:
                devel = self.plugin.devel if self.plugin.devel else None
                mess = PyNMA(nmaList, devel)
                nmaRes = mess.push(
                    app,
                    event,
                    description,
                    url,
                    None,
                    priority,
                    batch_mode
                )
            except Exception, e:
                i = e.args[0]
                s = e.args[1].decode(eg.systemEncoding)
                eg.PrintError(text.errMess3 + "\n" + text.errMess4 % (s,str(i)))
        if prowlList:
            try:
                provid = self.plugin.provid if self.plugin.provid else None
                mess = Pyrowl(prowlList, provid)
                prowlRes = mess.push(
                    app,
                    event,
                    description,
                    url,
                    priority,
                    batch_mode
                )
            except Exception, e:
                i = e.args[0]
                s = e.args[1].decode(eg.systemEncoding)
                eg.PrintError(text.errMess3 + "\n" + text.errMess4 % (s,str(i)))
        if prowlList or nmaList:
            if batch_mode:
                if nmaRes:
                    key = list(nmaRes.iterkeys())[0]
                    aps = []
                    for r in key.split(','):
                        ix = [itm[1] for itm in apis].index(r)
                        aps.append([i[0] for i in apis][ix])
                    ap = ",".join(aps) if subst else key
                    r = nmaRes[key][u'code'] if resType else nmaRes[key]
                    nmaResult = {ap: r}
                if prowlRes:
                    key = list(prowlRes.iterkeys())[0]
                    aps = []
                    for r in key.split(','):
                        ix = [itm[1] for itm in apis].index(r)
                        aps.append([i[0] for i in apis][ix])
                    ap = ",".join(aps) if subst else key
                    r = prowlRes[key][u'code'] if resType else prowlRes[key]
                    prowlResult = {ap: r}
                rslt = dict(nmaResult.items() + prowlResult.items())
                if prnt:
                    eg.Print(text.rslt % str(rslt))
                return rslt
            else: # batch_mode == False
                res = dict(nmaRes.items() + prowlRes.items())
                if res is not None:
                    result = {}
                    for r in res.iterkeys():
                        if subst:
                            ix = [itm[1] for itm in apis].index(r)
                            ap = [i[0] for i in apis][ix]
                        else:
                            ap = r
                        result[ap] = res[r][u'code'] if resType else res[r]
                    if prnt:
                        eg.Print(text.rslt % str(result))
                    return result
        else:
            eg.PrintError(text.errMess2)


    def Configure(
        self,
        apikeys = [],
        application = u"EventGhost",
        event = u"{eg.event.string}",
        description = u"{eg.event.payload}",
        url = "",
        priority = 0,
        batch_mode = False,
        resType = 1,
        subst = True,
        prnt = False
        ):
        self.apis = apikeys
        text = self.text
        panel = eg.ConfigPanel(self)
        im = self.plugin.StringIcon(ICON)
        im = im.resize((16, 16), ANTIALIAS)
        nmaIcon = wx.EmptyIcon()
        nmaIcon.CopyFromBitmap(PilToBitmap(im))               
        
        apiLabel = wx.StaticText(panel, -1, text.apiLabel)
        choices = [n[0] for n in self.plugin.apikeys]
        apiCtrl = wx.CheckListBox(
            panel,
            -1,
            choices = choices,
            size = ((-1,80)),
        )
        for i in range(len(choices)):
            while 1:
                for x in apikeys:
                    if x == choices[i]:
                        apiCtrl.Check(i,True)
                        break
                break
        appLabel = wx.StaticText(panel, -1, text.appLabel)
        appCtrl = wx.TextCtrl(panel, -1, application)
        eventLabel = wx.StaticText(panel, -1, text.eventLabel)
        self.eventCtrl = wx.TextCtrl(panel, -1, event)
        descrLabel = wx.StaticText(panel, -1, text.descrLabel)
        descrCtrl = wx.TextCtrl(panel, -1, description, style = wx.TE_MULTILINE)
        urlLabel = wx.StaticText(panel, -1, text.urlLabel)
        urlCtrl = wx.TextCtrl(panel, -1, url)
        priorityLabel = wx.StaticText(panel, -1, text.priorityLabel)
        priorityCtrl = wx.Slider(
            panel,
            -1,
            0,-2,2,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS | wx.SL_TOP
        )
        priorityCtrl.SetValue(priority)
        priorityCtrl2 = wx.Choice(panel, -1, choices=text.priorities)
        priorityCtrl2.SetSelection(priority+2)
        batchModeLabel = wx.StaticText(panel, -1, text.batch_mode)
        batchModeLabel.SetToolTipString(text.batchTip)
        batchModeCtrl = wx.CheckBox(panel, -1, "")
        batchModeCtrl.SetValue(batch_mode)
        batchModeCtrl.SetToolTipString(text.batchTip)
        resLabel = wx.StaticText(panel, -1, text.resType)
        rb1 = panel.RadioButton(not resType, text.resTypes[0],style=wx.RB_GROUP)
        rb2 = panel.RadioButton(resType, text.resTypes[1])
        substCtrl = wx.CheckBox(panel, -1, text.subst)
        substCtrl.SetValue(subst)
        prntCtrl = wx.CheckBox(panel, -1, text.prnt)
        prntCtrl.SetValue(prnt)

        def validation():
            flag = True
            if not self.apis:
                flag = False
            if not self.eventCtrl.GetValue():
                flag = False
            panel.dialog.buttonRow.applyButton.Enable(flag)
            panel.dialog.buttonRow.okButton.Enable(flag)

        def sliderUpdate(evt):
            val = evt.GetInt()
            priorityCtrl2.SetSelection(val + 2)
            evt.Skip()
        priorityCtrl.Bind(wx.EVT_SLIDER, sliderUpdate)

        def choiceUpdate(evt):
            sel = evt.GetSelection()
            priorityCtrl.SetValue(sel - 2)
            evt.Skip()
        priorityCtrl2.Bind(wx.EVT_CHOICE, choiceUpdate)

        def onCheckListBox(evt = None):
            self.apis = []
            sel = apiCtrl.GetSelection()
            choices = apiCtrl.GetStrings()
            for indx in range(len(choices)):
                if apiCtrl.IsChecked(indx):
                    self.apis.append(choices[indx])
            validation()
            apiCtrl.SetSelection(sel)
            nList, pList = self.plugin.GetApiKeyLsts(
                self.apis,
                self.plugin.apikeys
            )
            if self.plugin.bmp[0]:
                ix = int(nList > []) + 2 * int(pList > [])
                if ix:
                    il = eg.document.frame.treeCtrl.GetImageList()
                    bmp = il.GetBitmap(self.plugin.bmp[0] + 2 * (ix - 1))
                    icon = wx.EmptyIcon()
                    icon.CopyFromBitmap(bmp)
                else:
                    icon = nmaIcon
                panel.GetParent().GetParent().SetIcon(icon)
            if evt:
                evt.Skip()
        apiCtrl.Bind(wx.EVT_CHECKLISTBOX, onCheckListBox)
        onCheckListBox()

        def onEventUpdate(evt):
            validation()
        self.eventCtrl.Bind(wx.EVT_TEXT, onEventUpdate)

        prioritySizer = wx.BoxSizer(wx.HORIZONTAL)
        prioritySizer.Add(priorityCtrl,1,wx.EXPAND|wx.RIGHT,10)
        prioritySizer.Add(priorityCtrl2,0,wx.TOP,7)
        resSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, ""),
            wx.HORIZONTAL
        )

        ressizer = wx.FlexGridSizer(2, 3, 8, 8)
        ressizer.AddGrowableCol(1)
        resSizer.Add(ressizer,1,wx.EXPAND)
        ressizer.Add(rb1)
        ressizer.Add((32,1),1,wx.EXPAND)
        ressizer.Add(substCtrl)
        ressizer.Add(rb2)
        ressizer.Add((32,1),1,wx.EXPAND)
        ressizer.Add(prntCtrl)
        sizer = wx.FlexGridSizer(8, 2, 8, 8)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(3)
        panel.sizer.Add(sizer,1,wx.EXPAND)
        sizer.Add(apiLabel,0,wx.TOP,10)
        sizer.Add(apiCtrl,1,wx.EXPAND|wx.TOP,10)
        sizer.Add(appLabel,0,wx.TOP,10)
        sizer.Add(appCtrl,1,wx.EXPAND|wx.TOP,10)
        sizer.Add(eventLabel,0)
        sizer.Add(self.eventCtrl,1,wx.EXPAND)
        sizer.Add(descrLabel,0)
        sizer.Add(descrCtrl,1,wx.EXPAND)
        sizer.Add(urlLabel,0)
        sizer.Add(urlCtrl,1,wx.EXPAND)
        sizer.Add(priorityLabel,0,wx.TOP,10)
        sizer.Add(prioritySizer,0,wx.EXPAND|wx.BOTTOM,6)
        sizer.Add(batchModeLabel,0,wx.TOP,0)
        sizer.Add(batchModeCtrl,0,wx.BOTTOM,0)
        sizer.Add(resLabel,0,wx.TOP,12)
        sizer.Add(resSizer,1,wx.EXPAND|wx.TOP,4)
        validation()

        while panel.Affirmed():
            panel.SetResult(
                self.apis,
                appCtrl.GetValue(),
                self.eventCtrl.GetValue(),
                descrCtrl.GetValue(),
                urlCtrl.GetValue(),
                priorityCtrl.GetValue(),
                batchModeCtrl.GetValue(),
                rb2.GetValue(),
                substCtrl.GetValue(),
                prntCtrl.GetValue(),
            )
#===============================================================================


