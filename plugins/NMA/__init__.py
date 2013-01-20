# -*- coding: utf-8 -*-

version = "0.0.0"

# plugins/NMA/__init__.py
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
# 0.0.0 by Pako 2013-01-20 14:00 GMT+1
#     - initial version
#===============================================================================

eg.RegisterPlugin(
    name = "NMA (Notify My Android)",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{4D5F1C9D-0F0F-4CB9-A98B-7112B46E66F0}",
    createMacrosOnAdd = False,
    icon = (
        "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"
        "9r8P3rmPhmsWL+GMfCS8jED8iEqyp/Coq1VVVf7Ucv+aSvIvWNs9WrNRtWTqIBQPP1UA"
        "7ENau3Jzc79Heafey5rUA/ixCKDWW2xubv6A+LB4hJD/aUM61lVUeKzUjKynDPjhuD3s"
        "i11AqGMZPHPmTBj1/5eOHTv2fE9Pz38FYETz1NRUa35+/usxMTF/oQgY15p70fTq1avc"
        "gwcPoukyUlJaWvoy8WN8mZ6icFb1MjMz5ZycnLdIeBFdVpw+9/qaPHv27HSTyfTW5cuX"
        "V1G75j9Va4z0fklJSS4iWhXdC34TFRVVTjEvTfifsROkMU9XMLG6upqni8mi7u7uPXV1"
        "dck3b95EV1cXrFYrRmdNJpTFd3BwMGbNmmWhGK9JTk7+EzUeFyjWFWpAHYGBga5vAkBg"
        "VzH6nVZbW2seHBz07+vrSyErxBA5f0ghG8MswnIGKyx0OCIjIz+nRrM8LCysNSQkxETX"
        "sQECEkD3Qn9yxX26C8hTBvC/Hv93AP8GSP6eTrfM0n4AAAAASUVORK5CYII="
    ),
    description = ur'''<rst>
Sends notifications to your Android device via NMA_.
 
NMA_ is a platform that allows you to delivery push notifications 
from virtually any application to your Android device.

An account is required to use NMA_ on your Android.
After registration, you can create any number 
of API keys on the 'My Account' page.

.. _NMA:  https://www.notifymyandroid.com
    ''',
    #url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=xxxx",
)

from pynma import PyNMA
#===============================================================================

class Text:
    apiList = 'List of API keys:'
    sLabel = 'Short description:'
    lLabel = 'Long description (optional):'
    apiLabel = 'API key:'
    develLabel = 'Developer API key (optional):'
    delete = 'Delete'
    insert = 'Add new'
#===============================================================================

class NMA(eg.PluginClass):
    apikeys = []
    text = Text

    def __init__(self):
        self.AddAction(Notify)


    def __start__(self, apikeys = [], devel = ""):
        self.apikeys = apikeys
        self.devel = devel


    def Configure(self, apikeys = [], devel = ""):

        def boxEnable(enable):
            shortCtrl.Enable(enable)
            sLabel.Enable(enable)
            longCtrl.Enable(enable)
            lLabel.Enable(enable)
            apiCtrl.Enable(enable)
            apiLabel.Enable(enable)

        def setValue(item):
            shortCtrl.SetValue(item[0])
            apiCtrl.SetValue(item[1])
            longCtrl.SetValue(item[2])

        text = self.text
        self.apikeys = apikeys[:]
        self.oldSel = 0
        self.flag = True
        panel = eg.ConfigPanel(self)
        leftSizer = wx.FlexGridSizer(4,2,2,8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        apiListLbl=wx.StaticText(panel, -1, text.apiList)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size = wx.Size(120, 106),
            style = wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        sLabel = wx.StaticText(panel, -1, text.sLabel)
        shortCtrl = wx.TextCtrl(panel,-1,'')
        apiLabel = wx.StaticText(panel, -1, text.apiLabel)
        apiCtrl = wx.TextCtrl(panel,-1,'')
        develLabel = wx.StaticText(panel, -1, text.develLabel)
        develCtrl = wx.TextCtrl(panel, -1, devel)
        lLabel = wx.StaticText(panel, -1, text.lLabel)
        longCtrl = wx.TextCtrl(panel,-1,'',style=wx.TE_MULTILINE)
        box = wx.StaticBox(panel,-1,"")
        rightSizer = wx.StaticBoxSizer(box,wx.VERTICAL)
        rightSizer.Add(lLabel)
        rightSizer.Add(longCtrl,1,wx.TOP|wx.EXPAND,1)
        leftSizer.Add(apiListLbl,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl,0,wx.TOP,2)
        leftSizer.Add(topMiddleSizer,0,wx.TOP,5)
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
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,1,wx.LEFT|wx.EXPAND,10)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)
        panel.sizer.Add(apiLabel,0,wx.TOP,4)
        panel.sizer.Add(apiCtrl,0,wx.TOP|wx.EXPAND,2)
        panel.sizer.Add(develLabel,0,wx.TOP,14)
        panel.sizer.Add(develCtrl,0,wx.TOP|wx.EXPAND,2)
        if len(self.apikeys) > 0:
            listBoxCtrl.Set([n[0] for n in self.apikeys])
            listBoxCtrl.SetSelection(0)
            setValue(self.apikeys[0])
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
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)

        def onButtonUp(evt):
            newSel,self.apikeys=Move(self.apikeys,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([n[0] for n in self.apikeys])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)

        def onButtonDown(evt):
            newSel,self.apikeys=Move(self.apikeys,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([n[0] for n in self.apikeys])
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
            #apikeys structure = [short description, API key, long description]
            item = ['', '', '']
            self.apikeys.insert(sel, item)
            listBoxCtrl.Set([n[0] for n in self.apikeys])
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
            #apikeys structure = [short description, API key, long description]
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
            listBoxCtrl.Set([n[0] for n in self.apikeys])
            listBoxCtrl.SetSelection(sel)
            item = self.apikeys[sel]
            setValue(item)
            evt.Skip()
            self.flag = True
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnTxtChange(evt):
            if self.apikeys <> [] and self.flag:
                flag = True
                sel = self.oldSel
                sDescr = shortCtrl.GetValue()
                apikey = apiCtrl.GetValue()
                lDescr = longCtrl.GetValue()
                self.apikeys[sel][0]=sDescr
                self.apikeys[sel][1]=apikey
                self.apikeys[sel][2]=lDescr
                listBoxCtrl.Set([n[0] for n in self.apikeys])
                listBoxCtrl.SetSelection(sel)
                if sDescr.strip() <> "":
                    if [n[0] for n in self.apikeys].count(sDescr) > 1:
                        flag = False
                else:
                    flag = False
                if len(apikey) == 48:
                    if [n[1] for n in self.apikeys].count(apikey) > 1:
                        flag = False
                else:
                    flag = False
                panel.dialog.buttonRow.applyButton.Enable(flag)
                panel.dialog.buttonRow.okButton.Enable(flag)
                btnApp.Enable(flag)
            evt.Skip()
        shortCtrl.Bind(wx.EVT_TEXT, OnTxtChange)
        apiCtrl.Bind(wx.EVT_TEXT, OnTxtChange)
        longCtrl.Bind(wx.EVT_TEXT, OnTxtChange)

        while panel.Affirmed():
            panel.SetResult(
            self.apikeys,
            develCtrl.GetValue()
        )
#===============================================================================

class Notify(eg.ActionBase):

    class text:
        errMess1 = 'NMA: Unknown API key "%s"'
        errMess2 = 'NMA: There is available no valid API key.'
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
            'Full (original)',
            'Short'
        )
        subst = 'Instead of the API key use short description'
        priorities = (
            "Very Low",
            "Moderate",
            "Normal",
            "High",
            "Emergency"
        )

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
        subst = True
        ):
        text = self.text
        app = eg.ParseString(app) if app else "EventGhost"
        event = eg.ParseString(event) if event else text.empty
        description = eg.ParseString(description) if description else text.empty 
        url = eg.ParseString(url)
        if url:
            if url.lower()[:7] != r"http://" and url.lower()[:8] != r"https://":
                url = r"http://" + url
        apiList = []
        for api in apikeys:
            apis = self.plugin.apikeys
            keys = [i[0] for i in apis]
            if api in keys:
                ix = keys.index(api)
                apiList.append([i[1] for i in apis][ix])
            else:
                eg.PrintError(text.errMess1 % api)
        if apiList:
            try:
                devel = self.plugin.devel if self.plugin.devel else None
                mess = PyNMA(apiList, devel)
                res = mess.push(
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
                res = None
            if res is not None:
                if batch_mode:
                    key = list(res.iterkeys())[0]
                    aps = []
                    for r in key.split(','):
                        ix = [itm[1] for itm in apis].index(r)
                        aps.append([i[0] for i in apis][ix])
                    ap = ",".join(aps) if subst else key
                    r = res[key][u'code'] if resType else res[key]
                    return {ap: r}   
                else:
                    result = {}
                    for r in res.iterkeys():
                        if subst:
                            ix = [itm[1] for itm in apis].index(r)
                            ap = [i[0] for i in apis][ix]
                        else:
                            ap = r
                        result[ap] = res[r][u'code'] if resType else res[r]
                    return result                   
        else:
            eg.PrintError(text.errMess2)


    def GetLabel(
        self,
        apikeys,
        application,
        event,
        description,
        url,
        priority,
        batch_mode,
        resType,
        subst
        ):
        application = application if application else "EventGhost"
        event = event if event else self.text.empty
        return "%s: %s: %s" % (self.name, application, event)


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
        subst = True
        ):     
        self.apis = apikeys
        text = self.text
        panel = eg.ConfigPanel(self)
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
        batchModeCtrl = wx.CheckBox(panel, -1, "")
        batchModeCtrl.SetValue(batch_mode)
        resLabel = wx.StaticText(panel, -1, text.resType)

        rb1 = panel.RadioButton(not resType, text.resTypes[0],style=wx.RB_GROUP)
        rb2 = panel.RadioButton(resType, text.resTypes[1])   
        substCtrl = wx.CheckBox(panel, -1, text.subst)
        substCtrl.SetValue(subst)

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

        def onCheckListBox(evt):
            self.apis = []
            choices = apiCtrl.GetStrings()
            for indx in range(len(choices)):
                if apiCtrl.IsChecked(indx):
                    self.apis.append(choices[indx])
            validation()
            apiCtrl.SetSelection(evt.GetSelection())
            evt.Skip()
        apiCtrl.Bind(wx.EVT_CHECKLISTBOX, onCheckListBox)

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
        resSizer.Add(rb1)
        resSizer.Add(rb2, 0, wx.LEFT, 8)
        resSizer.Add((32,1),1,wx.EXPAND)
        resSizer.Add(substCtrl)
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
                substCtrl.GetValue()
            )
#===============================================================================

    