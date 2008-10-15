#ToDo: OSD
version = "0.1.1"
# This file is part of EventGhost.
# Copyright (C) 2008 Pako <lubos.ruckl@quick.cz>
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
#
# Last change: 15-10-2008 15:35


eg.RegisterPlugin(
    name = "Multitap",
    author = "Pako",
    version = version,
    kind = "other",
    createMacrosOnAdd = False,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUAAAAAAICAgIDA"
        "wMD///8AJXNWVlZiYmJubm56enoAMZY2AJVAAKxXAO5Ic///SEi4/0j/qiWGhoaSkpKe"
        "np6qqqqoub22trbCwsLe//7y8vL///+enp6goKS2traO/6v/q47/1I7AwMD///9ra2tj"
        "a3Ntc3Rzc2tzc3N7c3N7e3N7e3taa4Rre4x7hISEhISMjIyElJyUlJSUnJyclJScnJyE"
        "lKWEnK2EnLWUnKWcnKWcpaWcpa2Upb2Urb2crbWlnJylpZytpZy1pZy1rZy9rZylpaWl"
        "pa2traWlrbWlrb2trbWssbOttbW1raUYPkMYPoIFDb4AAFQS5LgYUQsFDb4AAFQS5LgY"
        "UKcFEOyctcaltcalvc6ttca1vcatxta1xta1zt69zt7GtZzGtaXGta3Gva3GvbXGvb3G"
        "xr3GxsbGxs7Ozs7Gzt7O1tbWzs7W1s7W1tbe1tbe3tbe3t7n597n5+fn7+/v7+/v9//3"
        "7+/39/f///9pQHAAAAEAAAAS4VQS4mwS6mDUOQrWmvj////RRQDRbshpI9AAAA0AAgjR"
        "btgAAABpI9AAAAAAAAEAAAAAAAES4lzRxrAAAADUG/sAAAAAAADRxrACA7YS4hTRxtEA"
        "AAAAAH8AAAES4hgUAAD4RKgAAAgUCAgUAAAWNaAS4fC6q80S5Dj5iPD0OHD////4RKj0"
        "fXD0ijoAADRQLAAAAACdAAC+cjAS4ij0oyMS5HD5iPD0OHD////4RKj0fXD0ijrl4ZcA"
        "AA4AAQTUF90S41zUOQrWm2j////ROzPRWywAAADRxrACA7YAAH8AAAEAAAAAAAAAAAAS"
        "+fAS+fAS4szRX3PRxrACA7YAAH8AAAEAAAAAAAES4uzUIPLRxrACA7YAAH8AAAEAAAAS"
        "+fAS4wj2gksAAADRWCvRU35tA/4AABQBC9EAAAAAAAAYPFoYPEcBEKTUEBjUEBgAAAIY"
        "Ou0YNg8BENrUEBjUEBgAAAIBEKQS46zUER+dksjUR7CdksjUR8ABEKQS46weK/KLAAAE"
        "K0lEQVR42gEgBN/7AL+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/AL8EBAEE"
        "BL8vGBgvBAQvLy+/vxgvBAQBBAQBBAQEBC+/AL8EBAEEBAS/LxgYLy8vL7+/vxgYLwQE"
        "AQQBBAQELy+/AL8BBAQBBAQEvy8YGC8vvwQEvy8YGC8EBAEEBAQvLy+/AL8EAQEBBAQE"
        "BL8vGC+/BAQEBL8vGBgvBAQEBC8vL7+/AL8EAQQEBAQEBL+/L78EBAQEBAS/LxgYLwQE"
        "Ly8vv7+/AL8BAQQEBAQELy+/vwQEBAQEBAQEvy8YGC8vLy+/v7+/AL8EBAQEBAQvLy+/"
        "BAQBAQQEBAQEBL8vGBgvL78EBL+/AL8EBAQEBC8vL78EBAEEBAQEBAQEBAS/LxgvvwQE"
        "BAS/AL8EBAQELy8vvy8EBAEBAQEBBAQEBAS/vy+/BAQEBAS/AL8vBAQvLy+/vxgvBAQE"
        "BAQBBAQEBC8vv78EBAQEBAS/AL8YLy8vL7+/vxgYLwQEAQEYBAQELy8vvwQEBAEEBAS/"
        "AL8YGC8vvwQEvy8YGC8EBAQEBAQvLy+/BAQEBAEEBAS/AL8vGC+/BAQEBL8vGBgvBAQE"
        "BC8vL78vBAQBAQEBAQS/AL+/L78EBAQEBAS/LxgYLwQELy8vv78YLwQEBAEEBAS/AL+/"
        "vwQEAQEYBAQEvy8YGC8vLy+/v78YGC8EBAEEBAS/AL+/BAQBBAQBAQQEBL8vGBgvL78E"
        "BL8vGBgvBAQEBAS/AL8EBAQBBAEEAQQEBAS/LxgvvwQEBAS/LxgYLwQEBAS/AL8EBAQY"
        "AQQEBAQEBAS/vy+/BAQEBAQEvy8YGC8EBC+/AL8vBAQEAQEEBAQEBC8vv78EBAQBBAQE"
        "BL8vGBgvLy+/AL8YLwQEBAQEBAQELy8vvwQEGAEBBAQEBAS/LxgYLy+/AL8YGC8EBAQE"
        "BAQvLy+/BAQEAQQBBAEEBAQEvy8YL7+/AL8vGBgvBAQEBC8vL78vBAQEAQQBBAEEBAQE"
        "v78vvwS/AL+/LxgYLwQELy8vv78YLwQEBAQBARgEBAQvL7+/BBi/AL8Evy8YGC8vLy+/"
        "v78YGC8EBAQBBAQEBC8vL78EGBi/AL8YBL8vGBgvL78EBL8vGBgvBAQEBAQELy8vvwQY"
        "GBi/AL8YGAS/LxgvvwQYGAS/LxgYLwQEBAQvLy+/LwQYGBi/AL8YGBi/vy+/BBgYGBgE"
        "vy8YGC8EBC8vL7+/GC8EGBi/AL8YGC8vv78EGBgYGBgYBL8vGBgvLy8vv7+/GBgvBBi/"
        "AL8YLy8vvwQYGBgYGBgYGAS/LxgYLy+/BAS/LxgYLwS/AL8vLy+/BBgYGBgYGBgYGBgE"
        "vy8YL78EGBgEvy8YGC+/AL+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/0ODx"
        "b7QO4zQAAAAASUVORK5CYII="
    ),
    description = (
        "Adds Multitapper actions."
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1024",
)

from threading import Timer

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
    #lst=tmpList
    return index2,tmpList

#===============================================================================
class Key(eg.ActionClass):

    class text:
        configLabel = 'Configuration:'
        listEventPayload = 'List of event payloads:'
        eventPayload = 'Event payload:'
        listEventSuffix = 'List of event suffixs:'
        eventSuffix = 'Event suffix:'
        delete = 'Delete'
        insert = 'Add new'
        label_1 = "Keys for Caps Lock OFF:"
        label_2 = "Keys for Caps Lock ON:"
        label_3 = "Digit:"
        warning = "Is not allowed to put a character\nSPACE on the first or last position !"


    def __call__(self,config,listKs):
        return self.plugin.Multitapper(config,listKs)

    def GetLabel(self,config,listKs=[]):
        self.listKeys = listKs[:]
        self.cfg=config
        indx = [n[0] for n in self.plugin.configs].index(self.cfg)
        item = self.plugin.configs[indx]
        if item[2]:
            sep = ' '
        else:
            sep = '.'
        return item[1]+sep+self.listKeys[0]
  #      return listKs[0]
#        return 'Test'

    def Configure(self, config='',listKs=[]):
        self.config = config
        self.listKeys = listKs[:]
        text = self.text
     #   self.flag = True
        panel = eg.ConfigPanel(self)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
#        box = wx.StaticBox(panel,-1,'',size=((50,50)))
        box = wx.StaticBox(panel,-1,'')
        rightSizer = wx.StaticBoxSizer(box,wx.VERTICAL)
        rightSizer.SetMinSize((220,190))
        configLbl=wx.StaticText(panel, -1, text.configLabel)
        choiceConfig = wx.Choice(
            panel,
            -1,
            size=(185,-1),
            choices=[n[0] for n in self.plugin.configs]
        )
  #      if self.config!='':
  #          choiceConfig.SetStringSelection(self.config)
        summary = wx.StaticText(panel,
            -1,
            '',
            size=(185, 130),
            style=wx.BORDER_SUNKEN
        )
        oldColour = summary.GetForegroundColour()
        leftSizer.Add(configLbl)
        leftSizer.Add(choiceConfig,0,wx.TOP,5)
        leftSizer.Add(summary,0,wx.TOP,20)


        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0,wx.LEFT|wx.EXPAND,16)
        panel.sizer.Add(mainSizer)
        panel.sizer.Layout()

#=========================================================================================================
        def onConfigChange(evt=None):
            self.oldSel = 0

            txt = self.text
            flg = False
            summary.SetForegroundColour(oldColour)
            if evt:
                cfg = choiceConfig.GetStringSelection()
            else:
                cfg = self.config
                choiceConfig.SetStringSelection(cfg)
            if cfg != '':
                try:
                    indx = [n[0] for n in self.plugin.configs].index(cfg)
                    item = self.plugin.configs[indx]
                    flg = True
                except:
                    self.PrintError(self.plugin.text.assignError % cfg)
                    summary.SetLabel('\n '+self.plugin.text.assignError % cfg)
                    summary.SetForegroundColour((255,0,0))
        #            panel.sizer.Layout()
            if evt:
                self.listKeys = []

            if flg:
                text = self.plugin.text
                modeLst = (text.string,text.numpad,text.singleKey)
                formatLst = (text.genSuffix,text.genPayload)
                label = u'  '+text.labelMode+u'\n      \u2022 '+modeLst[item[4]]+\
                    u'\n\n  '+text.evtString+u'\n      \u2022 '+item[1]+\
                    u'\n      \u2022 '+formatLst[item[2]]+u'\n\n  '+\
                    text.labelTimeout1+u'\n      \u2022 '+str(item[3])
                summary.SetLabel(label)

                if len(rightSizer.GetChildren()):

                    sizer = rightSizer.GetItem(0).GetSizer()
                    sizer.Clear(True)
                    rightSizer.Detach(sizer)
                    sizer.Destroy()

                if item[4]==0: #SMS mode
                    if evt:
                        panel.EnableButtons(False)
                    labelLbl_1=wx.StaticText(panel,-1,txt.label_1)
                    labelLbl_2=wx.StaticText(panel,-1,txt.label_2)
                    labelWarn=wx.StaticText(panel,-1,txt.warning)
                    labelWarn.Enable(False)
                    ctrlKeys_1=wx.TextCtrl(panel,-1,'')
                    ctrlKeys_2=wx.TextCtrl(panel,-1,'')
                    if self.listKeys == []:
                        self.listKeys.append('')
                        self.listKeys.append('')
                    else:
                        ctrlKeys_1.SetValue(self.listKeys[0])
                        if self.listKeys[0] != self.listKeys[1]:
                            ctrlKeys_2.SetValue(self.listKeys[1])
                    dynamicSizer = wx.BoxSizer(wx.VERTICAL)
                    dynamicSizer.Add(labelLbl_1,0,wx.TOP,8)
                    dynamicSizer.Add(ctrlKeys_1,0,wx.TOP,8)
                    dynamicSizer.Add(labelLbl_2,0,wx.TOP,24)
                    dynamicSizer.Add(ctrlKeys_2,0,wx.TOP,8)
                    dynamicSizer.Add(labelWarn,0,wx.TOP,12)

                    def onText1Change(evt):
                        tmp = self.listKeys[0]
                        self.listKeys[0] = ctrlKeys_1.GetValue().strip()
                        if tmp == self.listKeys[1]:
                            self.listKeys[1] = ctrlKeys_1.GetValue().strip()
                        if ctrlKeys_1.GetValue() != '':
                            panel.EnableButtons(True)
                        else:
                            panel.EnableButtons(False)
                        evt.Skip()
                    ctrlKeys_1.Bind(wx.EVT_TEXT,onText1Change)

                    def onText2Change(evt):
                        if ctrlKeys_2.GetValue().strip() == '':
                            self.listKeys[1]=ctrlKeys_1.GetValue().strip()
                        else:
                            self.listKeys[1]=ctrlKeys_2.GetValue().strip()
                        evt.Skip()
                    ctrlKeys_2.Bind(wx.EVT_TEXT,onText2Change)

                elif item[4]==1: #Numpad mode
                    if self.listKeys==[]:
                        self.listKeys.append('0')
                    labelLbl_3=wx.StaticText(panel,-1,txt.label_3)
                    ctrlDigit = eg.SpinIntCtrl(
                        panel,
                        -1,
                        int(self.listKeys[0]),
                        min=0,
                        max=9,
                    )
                    dynamicSizer = wx.BoxSizer(wx.HORIZONTAL)
                    dynamicSizer.Add(labelLbl_3,0,wx.LEFT|wx.TOP,12)
                    dynamicSizer.Add(ctrlDigit,0,wx.LEFT|wx.TOP,8)
                    def onDigitChange(evt):
                        self.listKeys[0]=str(ctrlDigit.GetValue())
                        evt.Skip()
                    ctrlDigit.Bind(wx.EVT_TEXT,onDigitChange)


                elif item[4]==2: #Single Key mode
                    previewLbl=wx.StaticText(
                        panel,
                        -1,
                        txt.listEventPayload if item[2] else txt.listEventSuffix
                    )
                    listBoxCtrl=wx.ListBox(
                        panel,-1,
                        size=wx.Size(110,106),
                        style=wx.LB_SINGLE|wx.LB_NEEDED_SB
                    )
                    buttonSizer=wx.BoxSizer(wx.VERTICAL)
                    labelLbl=wx.StaticText(
                        panel,
                        -1,
                        txt.eventPayload if item[2] else txt.eventSuffix
                    )
                    labelCtrl=wx.TextCtrl(panel,-1,'')
                    if self.listKeys<>[]:
                        labelCtrl.SetValue(self.listKeys[0])
                    dynamicSizer = wx.FlexGridSizer(4,2,2,8)
                    dynamicSizer.Add(previewLbl)
                    dynamicSizer.Add((1,1))
                    dynamicSizer.Add(listBoxCtrl,0,wx.TOP)
                    dynamicSizer.Add(buttonSizer,0,wx.TOP)
                    dynamicSizer.Add(labelLbl,0,wx.TOP,10)
                    dynamicSizer.Add((1,1))
                    dynamicSizer.Add(labelCtrl,0,wx.EXPAND)
                    dynamicSizer.Add((1,1))

                    #Button UP
                    bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
                    btnUP = wx.BitmapButton(panel, -1, bmp)
                    btnUP.Enable(False)
                    buttonSizer.Add(btnUP)
                    #Button DOWN
                    bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
                    btnDOWN = wx.BitmapButton(panel, -1, bmp)
                    btnDOWN.Enable(False)
                    buttonSizer.Add(btnDOWN,0,wx.TOP,3)
                    #Buttons 'Delete' and 'Insert new'
                    w1 = panel.GetTextExtent(text.delete)[0]
                    w2 = panel.GetTextExtent(text.insert)[0]
                    if w1 > w2:
                        btnDEL=wx.Button(panel,-1,text.delete)
                        btnApp=wx.Button(panel,-1,text.insert,size=btnDEL.GetSize())
                    else:
                        btnApp=wx.Button(panel,-1,text.insert)
                        btnDEL=wx.Button(panel,-1,text.delete,size=btnApp.GetSize())
                    btnDEL.Enable(False)
                    buttonSizer.Add(btnDEL,0,wx.TOP,5)
                    buttonSizer.Add(btnApp,0,wx.TOP,5)

                    def OnTextChange(evt=None):
                        if self.listKeys<>[]:
                            flag = False
                            sel = self.oldSel
                            label = labelCtrl.GetValue()
                            self.listKeys[sel] = label
                            listBoxCtrl.Set(self.listKeys)
                            listBoxCtrl.SetSelection(sel)
                            if label.strip()<>"":
                                if self.listKeys.count(label)==1:
                                    flag = True
                            panel.EnableButtons(flag)
                            btnApp.Enable(flag)
                        if evt:
                            evt.Skip()
                    labelCtrl.Bind(wx.EVT_TEXT, OnTextChange)


                    def OnButtonAppend(evt):
                        if len(self.listKeys)==1:
                            btnUP.Enable(True)
                            btnDOWN.Enable(True)
                        labelCtrl.Enable(True)
                        labelLbl.Enable(True)
                        sel = listBoxCtrl.GetSelection() + 1
                        self.oldSel=sel
                        self.listKeys.insert(sel,'')
                        listBoxCtrl.Set(self.listKeys)
                        listBoxCtrl.SetSelection(sel)
                        labelCtrl.SetValue('')
                        labelCtrl.SetFocus()
                        btnApp.Enable(False)
                        btnDEL.Enable(True)
                        evt.Skip()
                    btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

                    def OnClick(evt):
                        sel = listBoxCtrl.GetSelection()
                        label = labelCtrl.GetValue()
                        if label.strip()<>"":
                            if self.listKeys.count(label)==1:
                                self.oldSel=sel
                                item = self.listKeys[sel]
                                labelCtrl.SetValue(item)
                        listBoxCtrl.SetSelection(self.oldSel)
                        listBoxCtrl.SetFocus()
                        evt.Skip()
                    listBoxCtrl.Bind(wx.EVT_LISTBOX, OnClick)


                    def OnButtonUp(evt):
                        newSel,self.listKeys=Move(self.listKeys,listBoxCtrl.GetSelection(),-1)
                        listBoxCtrl.Set(self.listKeys)
                        listBoxCtrl.SetSelection(newSel)
                        self.oldSel = newSel
                        evt.Skip()
                    btnUP.Bind(wx.EVT_BUTTON, OnButtonUp)


                    def OnButtonDown(evt):
                        newSel,self.listKeys=Move(self.listKeys,listBoxCtrl.GetSelection(),1)
                        listBoxCtrl.Set(self.listKeys)
                        listBoxCtrl.SetSelection(newSel)
                        self.oldSel = newSel
                        evt.Skip()
                    btnDOWN.Bind(wx.EVT_BUTTON, OnButtonDown)


                    def OnButtonDelete(evt):
                        lngth=len(self.listKeys)
                        if lngth==2:
                            btnUP.Enable(False)
                            btnDOWN.Enable(False)
                        sel = listBoxCtrl.GetSelection()
                        if lngth == 1:
                            self.listKeys=[]
                            listBoxCtrl.Set([])
                            labelCtrl.SetValue('')
                            labelCtrl.Enable(False)
                            labelLbl.Enable(False)
                            panel.EnableButtons(False)
                            btnDEL.Enable(False)
                            btnApp.Enable(True)
                            evt.Skip()
                            return
                        elif sel == lngth - 1:
                            sel = 0
                        self.oldSel = sel
                        tmp = self.listKeys.pop(listBoxCtrl.GetSelection())
                        listBoxCtrl.Set(self.listKeys)
                        listBoxCtrl.SetSelection(sel)
                        item = self.listKeys[sel]
                        labelCtrl.SetValue(item)
                        evt.Skip()
                    btnDEL.Bind(wx.EVT_BUTTON, OnButtonDelete)
                    if len(self.listKeys) > 0:
                        listBoxCtrl.Set(self.listKeys)
                        listBoxCtrl.SetSelection(0)
                        labelCtrl.SetValue(self.listKeys[0])
                        self.oldSel=0
                        btnUP.Enable(True)
                        btnDOWN.Enable(True)
                        btnDEL.Enable(True)
                    else:
                        labelCtrl.Enable(False)
                        labelLbl.Enable(False)
                        panel.EnableButtons(False)
                rightSizer.Add(dynamicSizer,0,wx.EXPAND)
                panel.sizer.Layout()


#=========================================================================================================
#End of function onConfigChange() :
            if evt:
                evt.Skip()
        choiceConfig.Bind(wx.EVT_CHOICE,onConfigChange)
        onConfigChange()



        while panel.Affirmed():
            panel.SetResult(
                choiceConfig.GetStringSelection(),
                self.listKeys,
            )
            self.listKeys=None

#===============================================================================

class Enter(eg.ActionClass):

    def __call__(self):
        self.plugin.OnEnter()
#===============================================================================

class Cancel(eg.ActionClass):

    def __call__(self):
        self.plugin.mode=3
#===============================================================================

class Shift(eg.ActionClass):

    def __call__(self):
        self.plugin.OnShift()
#===============================================================================

ACTIONS = (
    (Key, 'Key', 'Key', 'Key.', None),
    (Enter, 'Enter', 'Enter', 'Enter.', None),
    (Cancel, 'Cancel', 'Cancel', 'Cancel.', None),
    (Shift, 'Shift', 'Caps Lock', 'Caps Lock.', None),
)
#===============================================================================
class Multitap(eg.PluginClass):
    configs = []

    class text:
        label = 'Configuration name:'
        evtString = 'Event name and format:'
        menuPreview = 'List of configurations:'
        delete = 'Delete'
        insert = 'Add new'
        labelMode = "Mode of Multitapper:"
        string = "SMS like string"
        numpad = "Numpad (numerical string)"
        singleKey = "Single Key"
        labelTimeout1 = "Timeout:"
        labelTimeout2 = "(0 = never timeout)"
        genSuffix = 'Generate as event suffix'
        genPayload = 'Generate as payload'
        param = "Configuration parameters:"
        assignError = 'Configuration "%s" not exists!'
#===============================================================================

    def __init__(self):
        self.lenKeys = 0
        self.evtString = ''
        self.oldKeys = ''
        self.indx = 0
        self.timeout = 0
        self.timer = Timer(0.0, self.OnTimeout)
        self.AddActionsFromList(ACTIONS)
        self.formatEvent = False
        self.evtName = ''
        self.shift = False
        self.mode = 3 #3 .. idle, 0 .. string, 1 .. number, 2 .. "SingleKey"
                      #4 .. if SMS mode starts by Shift
#===============================================================================

    def Multitapper(self,config,keys):
        try:
            indx = [n[0] for n in self.configs].index(config)
            item = self.configs[indx]
        except:
            self.PrintError(self.text.assignError % config)
            return
        self.timer.cancel()
        if self.mode > 2: #3 = idle, 4 = Shift after idle
            self.evtString = ''
            self.oldKeys = ''
            self.timeout = item[3]
            self.formatEvent = item[2]
            self.evtName = item[1]
            self.shift = False if self.mode == 3 else True
            self.mode = item[4]
        if self.mode == 0: # SMS mode
            set = self.shift
            if self.oldKeys == '':
                self.oldKeys = keys[set]
                self.indx = -1
            if keys[set] != self.oldKeys:
                self.evtString+=self.oldKeys[self.indx]
                self.oldKeys = keys[set]
                self.indx=0
            else:
                self.indx+=1
                if self.indx > len(keys[set])-1:
                    self.indx=0
        elif self.mode==1: # Numpad mode
            self.timer.cancel()
            if self.timeout==0:
                self.timeout=timeout
                self.evtName = evtName
            self.evtString += keys[0]
        else:              # mode Single Key
            if self.oldKeys == '':
                self.oldKeys = keys[:]
                self.indx = -1
            if keys != self.oldKeys: #ERROR or "Enter"?  -> meantime Error
                self.mode = 3
                return
            else:
                self.indx+=1
                if self.indx > len(keys)-1:
                    self.indx=0
                self.evtString = keys[self.indx]
        if self.timeout>0:
            self.timer = Timer(self.timeout, self.OnTimeout)
            self.timer.start()
        return self.evtString
#===============================================================================

    def OnShift(self):
        self.timer.cancel()
        if self.mode == 3:
            self.mode = 4
        elif self.mode == 4:
            self.mode = 3
        elif self.mode == 0:
            self.shift = not self.shift
            if self.oldKeys != '':
                self.evtString+=self.oldKeys[self.indx]
            self.oldKeys = ''
#===============================================================================

    def OnTimeout(self):
        if self.mode==0: #String mode
            self.evtString+=self.oldKeys[self.indx]
        else:            # Numpad  and SingleKey mode
            self.GenerateEvent()
        self.oldKeys = ''
#===============================================================================

    def OnEnter(self):
        self.timer.cancel()
        if self.oldKeys != '':
            if self.mode!=2:
                self.evtString+=self.oldKeys[self.indx]
        self.GenerateEvent()
#===============================================================================

    def GenerateEvent(self):
        if self.evtString != '':
            if self.formatEvent:
                self.TriggerEvent(self.evtName, self.evtString)
            else:
                self.TriggerEvent(
                    self.evtName+'.'+self.evtString if self.evtName !='' else self.evtString
                )
        self.mode = 3 #Cleaning
#===============================================================================

    def __start__(
        self,
        configs=[],
    ):
        self.configs=configs
#===============================================================================

    def Configure(
        self,
        configs=[],
    ):
        def boxEnable(enable):
            labelCtrl.Enable(enable)
            labelLbl.Enable(enable)
            ctrlEvtName.Enable(enable)
            eventLbl.Enable(enable)
            choiceMode.Enable(enable)
            lblMode.Enable(enable)
            lblTimeout1.Enable(enable)
            lblTimeout2.Enable(enable)
            ctrlTimeout.Enable(enable)
            rb0.Enable(enable)
            rb1.Enable(enable)

        def setValue(item):
            labelCtrl.SetValue(item[0])
            ctrlEvtName.SetValue(item[1])
            rb0.SetValue(not item[2])
            rb1.SetValue(item[2])
            ctrlTimeout.SetValue(item[3])
            choiceMode.SetSelection(item[4])

        text = self.text
        self.configs = configs[:]
        self.oldSel=0
        self.flag = True
        panel = eg.ConfigPanel(self)
        leftSizer = wx.FlexGridSizer(4,2,2,8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(panel, -1, text.menuPreview)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(120,106),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(panel, -1, text.label)
        labelCtrl=wx.TextCtrl(panel,-1,'')
        eventLbl=wx.StaticText(panel, -1, text.evtString)
        ctrlEvtName = wx.TextCtrl(panel,-1,'')
        choiceMode = wx.Choice(
            panel,
            -1,
            choices=(text.string, text.numpad, text.singleKey)
        )
        lblMode = wx.StaticText(panel, -1, text.labelMode)
        lblTimeout1 = wx.StaticText(panel, -1, text.labelTimeout1)
        lblTimeout2 = wx.StaticText(panel, -1, text.labelTimeout2)
        ctrlTimeout = eg.SpinNumCtrl(
            panel,
            -1,
            0.0,
            integerWidth = 2,
            fractionWidth = 2,
            allowNegative = False,
            min = 0.0,
            increment = 0.1,
        )
        rb0 = panel.RadioButton(False,text.genSuffix, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(True,text.genPayload)

        timeoutSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeoutSizer.Add(lblTimeout1,0,wx.TOP,4)
        timeoutSizer.Add(ctrlTimeout,0,wx.LEFT|wx.RIGHT,8)

        box = wx.StaticBox(panel,-1,text.param)
        rightSizer = wx.StaticBoxSizer(box,wx.VERTICAL)
        rightSizer.Add(lblMode)
        rightSizer.Add(choiceMode,0,wx.TOP|wx.EXPAND,3)
        rightSizer.Add(eventLbl,0,wx.TOP|wx.EXPAND,12)
        rightSizer.Add(ctrlEvtName,0,wx.TOP|wx.EXPAND,3)
        rightSizer.Add(rb0,0,wx.TOP,3)
        rightSizer.Add(rb1,0,wx.TOP,3)
        rightSizer.Add(timeoutSizer,0,wx.TOP|wx.EXPAND,16)
        rightSizer.Add(lblTimeout2,0,wx.TOP,3)
        leftSizer.Add(previewLbl,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl,0,wx.TOP,5)
        leftSizer.Add(topMiddleSizer,0,wx.TOP,5)
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
        w1 = panel.GetTextExtent(text.delete)[0]
        w2 = panel.GetTextExtent(text.insert)[0]
        if w1 > w2:
            btnDEL=wx.Button(panel,-1,text.delete)
            btnApp=wx.Button(panel,-1,text.insert,size=btnDEL.GetSize())
        else:
            btnApp=wx.Button(panel,-1,text.insert)
            btnDEL=wx.Button(panel,-1,text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer)
        mainSizer.Add(rightSizer,0,wx.LEFT|wx.EXPAND,36)
        panel.sizer.Add(mainSizer)
        if len(self.configs) > 0:
            listBoxCtrl.Set([n[0] for n in self.configs])
            listBoxCtrl.SetSelection(0)
            setValue(self.configs[0])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            boxEnable(False)
            panel.dialog.buttonRow.applyButton.Enable(False)
            panel.dialog.buttonRow.okButton.Enable(False)
        panel.sizer.Layout()
#===============================================================================

        def onClick(evt):
            self.flag = False
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            if label.strip()<>"":
                if [n[0] for n in self.configs].count(label)==1:
                    self.oldSel=sel
                    item = self.configs[sel]
                    setValue(item)
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
            self.flag = True
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)


        def onButtonUp(evt):
            newSel,self.configs=Move(self.configs,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([n[0] for n in self.configs])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)


        def onButtonDown(evt):
            newSel,self.configs=Move(self.configs,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([n[0] for n in self.configs])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        def onButtonDelete(evt):
            self.flag = False
            lngth=len(self.configs)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.configs=[]
                listBoxCtrl.Set([])
                item = ['','',True,1.5,0]
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
            tmp = self.configs.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in self.configs])
            listBoxCtrl.SetSelection(sel)
            item = self.configs[sel]
            setValue(item)
            evt.Skip()
            self.flag = True
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)


        def onChoiceMode(event=None):
            if self.configs<>[]:
                mode = choiceMode.GetSelection()
                sel = self.oldSel
                self.configs[sel][4] = mode
            if event:
                event.Skip()
        choiceMode.Bind(wx.EVT_CHOICE,onChoiceMode)
        onChoiceMode()

        def onTimeout(event=None):
            if self.configs<>[]:
                timeout = ctrlTimeout.GetValue()
                sel = self.oldSel
                self.configs[sel][3] = timeout
            if event:
                event.Skip()
        ctrlTimeout.Bind(wx.EVT_TEXT,onTimeout)
        onTimeout()

        def onEvtFormat(event=None):
            if self.configs<>[]:
                format = rb1.GetValue()
                sel = self.oldSel
                self.configs[sel][2] = format
            if event:
                event.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON,onEvtFormat)
        rb1.Bind(wx.EVT_RADIOBUTTON,onEvtFormat)
        onEvtFormat()

        def OnTxtChange(evt):
            if self.configs<>[] and self.flag:
                flag = False
                sel = self.oldSel
                label = labelCtrl.GetValue()
                event = ctrlEvtName.GetValue()
                self.configs[sel][0]=label
                self.configs[sel][1]=event
                listBoxCtrl.Set([n[0] for n in self.configs])
                listBoxCtrl.SetSelection(sel)
                if label.strip()<>"":
                    if event.strip()<>"":
                        if [n[0] for n in self.configs].count(label)==1:
                            flag = True
                panel.dialog.buttonRow.applyButton.Enable(flag)
                panel.dialog.buttonRow.okButton.Enable(flag)
                btnApp.Enable(flag)
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)
        ctrlEvtName.Bind(wx.EVT_TEXT, OnTxtChange)


        def OnButtonAppend(evt):
            self.flag = False
            if len(self.configs)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            item = ['','',True,1.5,0]
            self.configs.insert(sel,item)
            listBoxCtrl.Set([n[0] for n in self.configs])
            listBoxCtrl.SetSelection(sel)
            setValue(item)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
            self.flag = True
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)


        while panel.Affirmed():
            panel.SetResult(
            self.configs,
        )
#===============================================================================


