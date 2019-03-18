# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# This plugin is an HTTP client and Server that sends and receives MiCasaVerde UI5 and UI7 states.
# This plugin is based on the Vera plugins by Rick Naething, well kinda sorta, gave me inspiration at the least.
# This plugin is currently being tested by the members of the EventGhost Forum, m19brandon, blaher, kgschlosser (the artist that is K)
# WinoOutWest, loveleejohn, kkl... I thank these people for being the first to tell me the errors which I am hoping are solved,
# but if not you know where to find me.

import eg
import wx
import time
import ctypes
import win32api
import win32con
import win32gui
import threading
from copy import deepcopy as dc
from eg.WinApi.Utils import GetMonitorDimensions
from TextControls import *
from ChoiceControls import *

class DisplayMenu(eg.ActionBase):

    text = Text
 
    def __call__(
                self,
                fontinfo,
                fontcolor,
                selectedfontcolor, 
                backgroundcolor,
                backgroundtransparency,
                bordercolor,
                bordertransparency,
                bordercornerradius,
                borderwidth,
                menutimeout,
                windowtransparency,
                menufadeIn,
                menufadeOut,
                displaymonitor,
                menuwidth,
                menuheight
                ):
        try:
            self.plugin.UPDATEMENU.EVENT.set()
            self.plugin.UPDATEMENU.start()
        except:
            self.plugin.UPDATEMENU = UPDATEMENU(self.plugin, STATIC)
            self.plugin.UPDATEMENU.start()

        self.plugin.VERAMENU.start(
                                   self,
                                    fontinfo,
                                    fontcolor,
                                    selectedfontcolor, 
                                    backgroundcolor,
                                    backgroundtransparency,
                                    bordercolor,
                                    bordertransparency,
                                    bordercornerradius,
                                    borderwidth,
                                    menutimeout,
                                    windowtransparency,
                                    menufadeIn,
                                    menufadeOut,
                                    displaymonitor,
                                    menuwidth,
                                    menuheight
                                    )

    def Configure(
                self,
                fontinfo='0;-41;0;0;0;700;255;0;0;0;3;2;1;82;Gabriola',
                fontcolor=(34, 24, 218),
                selectedfontcolor=(0,255,0), 
                backgroundcolor=(31, 31, 31),
                backgroundtransparency=195,
                bordercolor=(155, 155, 155),
                bordertransparency=195,
                bordercornerradius=15,
                borderwidth=10,
                menutimeout=20,
                windowtransparency=220,
                menufadeIn=12,
                menufadeOut=12,
                displaymonitor=0,
                menuwidth=0.35,
                menuheight=0.80
                ):

        text = self.text.DisplayMenu
        panel = eg.ConfigPanel()

        settingsizer = wx.BoxSizer(wx.HORIZONTAL)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        rightsizer = wx.BoxSizer(wx.VERTICAL)

        fontCtrl = panel.FontSelectButton(fontinfo, size=(75, 22))
        fontColorCtrl = panel.ColourSelectButton(fontcolor, size=(75, 22))
        selectedCtrl = panel.ColourSelectButton(selectedfontcolor, size=(75, 22))
        backColorCtrl = panel.ColourSelectButton(backgroundcolor, size=(75, 22))
        backTransCtrl = panel.SpinIntCtrl(backgroundtransparency, max=255, size=(75,22))
        borderColorCtrl = panel.ColourSelectButton(bordercolor, size=(75, 22))
        borderTransCtrl = panel.SpinIntCtrl(bordertransparency, max=255, size=(75,22))
        borderCornerCtrl = panel.SpinIntCtrl(bordercornerradius, max=17, size=(75,22))
        borderWidthCtrl= panel.SpinIntCtrl(borderwidth, max=50, size=(75,22))
        timeoutCtrl = panel.SpinIntCtrl(menutimeout, max=100, size=(75,22))
        windowTransCtrl = panel.SpinIntCtrl(windowtransparency, max=255, size=(75,22))
        fadeInCtrl = panel.SpinIntCtrl(menufadeIn, max=100, size=(75,22))
        fadeOutCtrl = panel.SpinIntCtrl(menufadeOut, max=100, size=(75,22))
        monitorCtrl = panel.DisplayChoice(displaymonitor, size=(75,22))
        widthCtrl = Choice(panel, str(int(menuwidth*100.00))+'%', self.text.Dimmer.Choice, size=(75,22))
        heightCtrl = Choice(panel, str(int(menuheight*100.00))+'%', self.text.Dimmer.Choice, size=(75,22))

        def boxbuilder(lbl, data, cdata=None):
            staticbox = wx.StaticBox(panel, -1, lbl)
            staticsizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)
            csizer = wx.GridBagSizer(0,0)

            if lbl != cdata:
                staticsizer.Add(panel.StaticText(cdata), 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10)


            for i, item in enumerate(data):
                csizer.Add(item[0], (i, 0), (1, 8), wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 10)
                csizer.Add(item[1], (i, 9), (1, 3), wx.EXPAND|wx.ALIGN_RIGHT|wx.BOTTOM, 10)

            staticsizer.Add(csizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10)
            return staticsizer

        def gencolumns(stext):
            for txt in stext:
                txt = panel.StaticText(txt, size=(130,20))
                yield txt

        lbls = [
                [text.FontBox],
                [text.BackBox],
                [text.BorderBox],
                [text.DimensionBox, text.DimensionDesc],
                [text.OtherBox]
                ]

        txts = [
                [text.FontText, text.FontColorText, text.SelectFontColorText],
                [text.BackColortext, text.TransparencyText],
                [text.BorderColorText, text.BorderTransText, text.BorderCornerText, text.BorderWidthText],
                [text.WidthText, text.HeightText],
                [text.MonitorText, text.WindowTransText, text.FadeInText, text.FadeOutText, text.menuTimeText]
                ]
        itms = [
                [fontCtrl, fontColorCtrl, selectedCtrl],
                [backColorCtrl, backTransCtrl],
                [borderColorCtrl, borderTransCtrl, borderCornerCtrl, borderWidthCtrl],
                [widthCtrl, heightCtrl],
                [monitorCtrl, windowTransCtrl, fadeInCtrl, fadeOutCtrl, timeoutCtrl]
                ]

        txts = [[item for item in gencolumns(genitem)] for genitem in txts]
        for i, box in enumerate([boxbuilder(widget[0], zip(txts[i], itms[i]), widget[-1:][0]) for i, widget in enumerate(lbls)]):
            if i < 3: leftsizer.Add(box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)
            else: rightsizer.Add(box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)

        settingsizer.Add(leftsizer)
        settingsizer.Add(rightsizer)
        panel.sizer.Add(settingsizer)

        while panel.Affirmed():
            panel.SetResult(
                            fontCtrl.GetValue(),
                            fontColorCtrl.GetValue(),
                            selectedCtrl.GetValue(),
                            backColorCtrl.GetValue(),
                            backTransCtrl.GetValue(),
                            borderColorCtrl.GetValue(),
                            borderTransCtrl.GetValue(),
                            borderCornerCtrl.GetValue(), 
                            borderWidthCtrl.GetValue(),
                            timeoutCtrl.GetValue(),
                            windowTransCtrl.GetValue(),
                            fadeInCtrl.GetValue(),
                            fadeOutCtrl.GetValue(),
                            monitorCtrl.GetValue(),
                            float(widthCtrl.GetStringSelection()[:-1]+'.0')/100.0,
                            float(heightCtrl.GetStringSelection()[:-1]+'.0')/100.0
                            )


class UPDATEMENU(threading.Thread):

    text = Text

    MENUDATA = None
    EVENT = threading.Event()

    def __init__(self, plugin, STATIC):
        self.STATIC = dc(STATIC)
        self.plugin = plugin
        super(UPDATEMENU, self).__init__()

    def run(self):
        self.EVENT.set()
        event = threading.Event()
        event.wait(0.01)
        self.EVENT.clear()

        eg.PrintNotice("Vera Menu Update Started")
        while not self.EVENT.isSet():
            self.MENUDATA = self.BuildMenu()
            self.plugin.VERAMENU.LoadMenu(dc(self.MENUDATA))
            self.EVENT.wait(self.plugin.upspeed*2.0)
        eg.PrintNotice("Vera Menu Update Stopped")

    def BuildMenu(self):
        VDL = self.plugin.VDL
        devices = dc(VDL.devices)
        scenes = dc(VDL.scenes)
        rooms = dc(VDL.rooms)
        menu = [None]*len(rooms)
        
        for i, room in enumerate(rooms):
            if room: menu[i] = dict(selectforeground=True, selected=False, txt=dc(room['name']), event=[])
        menu[0] = dict(selectforeground=True, selected=False, txt='No Room', event=[])
        menu += [dict(selectforeground=True, selected=False, txt='Plugins', event=[])]
        menu += [dict(selectforeground=True, selected=False, txt='Weather', event=[])]

        sorteddevicekeys = [[]]*len(menu)

        for i, device in enumerate(devices):
            if not device: continue
            textnonselect = []
            textselect = []
            textnonselectkeys = []
            textselectkeys = []

            devicenumber = device.pop('id')
            roomnumber = int(device.pop('room'))
            categorynumber = device.pop('category')
            
            try: parentname = dc(VDL.devices[int(device.pop('parent'))]['name'])
            except: parentname = None

            devicename = device.pop('name')
            categorynumber = '25' if devicename.find('Weather') > -1 else categorynumber
            categoryname = VDL.GetCategory(categorynumber)

            if categoryname == 'Plugin':
                roomnumber = len(menu)-2
            if categoryname == 'Weather':
                roomnumber = len(menu)-1
            if parentname and parentname.find('Weather') > -1:
                roomnumber = len(menu)-1

            degree = '\xb0'
            thermalunit = VDL.GetThermalUnit()
            
            for key in device.keys():
                e = VDL.GetEvent(categorynumber, key)
                if e is None: continue

                if isinstance(e[0], list):
                    e += [e[0][int(device[key])]]
                else:
                    DEGREE = ['Temperature', 'Heat', 'Cool', 'Chill', 'Dew']
                    PERCENT = ['Level', 'Humidity']
                    SPEED = ['Gust', 'Speed']

                    if e[0].find('Pressure') > -1:
                        e += [device[key]+'inch Hg'] if thermalunit == 'F' else [device[key]+'mb']
                    for idx in range(5):
                        if e[0].find(DEGREE[idx]) > -1:
                            e += [device[key]+degree+' '+thermalunit]
                        elif idx < 2 and e[0].find(PERCENT[idx]) > -1:
                            e += [device[key]+'%']
                        elif idx < 2 and e[0].find(SPEED[idx]) > -1:
                            e += [device[key]+'mph'] if thermalunit == 'F' else [device[key]+'km/h']
                    if len(e) == 1:
                        e += [str(device[key])]

                selectforeground = False
                lineevent = None
                try: txt = e[0]+': '+e[1]
                except: txt = categoryname+': '+e[1]
                comlookup = categorynumber+key
                comitems = ['5fanmode', '5mode', '5coolsp', '5cool', '5heatsp', '5heat', '2level', '7locked', '3status', '22armed']

                if comlookup in comitems:
                    selectforeground = True
                    lineevent = []
                    parameter = None
                    paramlist = None
                    usedevice = devicenumber
                    comlookup = comitems.index(comlookup)
                    
                    if comlookup == 0:
                        paramlist = dc(self.text.HVAC.FanChoice)
                        parameter = 'hvacFanMode'
                    elif comlookup == 1:
                        paramlist = dc(self.text.HVAC.OppChoice)
                        parameter = 'hvacOppMode'
                    elif comlookup <= 5:
                        paramlist = dc(self.text.HVAC.SetTmpChoiceF)
                        if VDL.GetThermalUnit() == 'C': paramlist = dc(self.text.HVAC.SetTmpChoiceC)
                        if comlookup <= 3: parameter = 'hvacSetTempC'
                        else: parameter = 'hvacSetTempH'
                    elif comlookup == 6:
                        paramlist = dc(self.text.Dimmer.Choice)
                        parameter = 'dimmer'
                    elif comlookup == 7:
                        paramlist = dc(self.text.DoorLock.Choice)
                        parameter = 'doorLock'
                    elif comlookup == 8:
                        paramlist = dc(self.text.Switch.Choice)
                        parameter = 'switch'
                    elif comlookup == 9:
                        paramlist = dc(self.text.Alarm.Choice)
                        parameter = 'alarm'
                        usedevice = None

                    for pnum, param in enumerate(paramlist):
                        newevt = {parameter: param}
                        checksel = param
                        if comlookup > 6:
                            checksel = str(pnum)
                            newevt[parameter] = str(pnum)
                        if param[-1:] in ['%', '\xb0']:
                            checksel = param[:-1]
                            newevt[parameter] = param[:-1]
                        if usedevice: newevt['device'] = usedevice

                        try: checkval = str(int(float(device[key])))
                        except: checkval = device[key]

                        sel = True if checkval == checksel else False

                        lineevent += [dict(selectforeground=selectforeground, selected=sel, txt=param, event=newevt)]

                deviceevent = dict(selectforeground=selectforeground, selected=False, txt=txt, event=lineevent)

                if selectforeground:
                    textselectkeys = sorted(textselectkeys+[deviceevent['txt']])
                    textselect.insert(textselectkeys.index(deviceevent['txt']), deviceevent)
                else:
                    textnonselectkeys = sorted(textnonselectkeys+[deviceevent['txt']])
                    textnonselect.insert(textnonselectkeys.index(deviceevent['txt']), deviceevent)

            textnonselect.insert(0, dict(selectforeground=False, selected=False, txt='Type: '+categoryname, event=None))
            textnonselect.insert(0, dict(selectforeground=False, selected=True, txt='ID: '+devicenumber, event=None))
            if parentname: textnonselect.insert(2, dict(selectforeground=False, selected=False, txt='Parent: '+parentname, event=None))

            roomevent = dict(selectforeground=True, selected=False, txt=devicename, event=textnonselect+textselect)
            sorteddevicekeys[roomnumber] = sorted(sorteddevicekeys[roomnumber]+[roomevent['txt']])
            menu[roomnumber]['event'].insert(sorteddevicekeys[roomnumber].index(roomevent['txt']), roomevent)

        sortedscenes = sorted([[scene['name'], scene['id'], scene['room'], scene['active'], scene['category']] for scene in scenes if scene])

        for scene in sortedscenes:
            scenename, sceneid, sceneroom, sceneactive, scenecategory = scene
            sceneactive = VDL.GetEvent(scenecategory, 'active')[0][int(sceneactive)]
            sceneevent = [
                        dict(selectforeground=False, selected=True, txt='ID: '+sceneid, event=None),
                        dict(selectforeground=False, selected=False, txt='Scene: '+sceneactive, event=None),
                        dict(selectforeground=True, selected=False, txt='Run Scene', event=dict(scene=sceneid))
                        ]
            evt = dict(selectforeground=True, selected=False, txt=scenename, event=sceneevent)
            menu[int(sceneroom)]['event'] += [dc(evt)]

        if not menu[0]['event']: menu[0] = None

        sortedmenu = sorted([[item['txt'], dc(item)] for item in menu if item])
        menu = []

        for item in sortedmenu:
            if not item[1]['event']:
                evt = dict(selectforeground=False, selected=True, txt='No Devices or Scenes', event=None)
                item[1]['event'] = [evt]
            menu += [item[1]]

        menu[0]['selected'] = True

        return dc(menu)

class VERAMENU:

    EVENT = threading.Event()

    def __init__(self, plugin, STATIC):
        self.STATIC = dc(STATIC)
        self.plugin = plugin
        self.menuLocation = None
        self.menuData = None
        self.clearingMenu = False
        self.windowFrame = False
        
    def start(self, parent, *args):
        if self.menuLocation is None:
            self.menuData = None

        self.EVENT.set()
        event = threading.Event()
        event.wait(0.01)
        self.EVENT.clear()

        self.storedSettings = dc(args)
        threading.Thread(target=self.CheckEVENT).start()
        wx.CallAfter(self.DisplayMenu)

    def CheckEVENT(self):
        eg.PrintNotice("Vera Menu Started")
        while not self.EVENT.isSet():
            self.EVENT.wait(1)
        self.plugin.UPDATEMENU.EVENT.set()

        try: self.windowFrame.doublepresstimer.Stop()
        except: pass
        try: self.windowFrame.closeMenuTimer.Stop()
        except: pass

        self.ClearMenu()
        eg.PrintNotice("Vera Menu Stopped")
        
    def DownLevel(self):
        self.menuLocation.pop()
        if not self.menuLocation:
            self.menuLocation = None
            wx.CallAfter(self.windowFrame.onClose)
        else:
            self.ClearMenu()
            wx.CallAfter(self.DisplayMenu)

    def UpLevel(self, item):
        item = dc(item)
        self.ClearMenu()
        setselected = self.GetSelected(item)
        item[setselected]['selected'] = True
        self.menuLocation += [dc(item)]
        wx.CallAfter(self.DisplayMenu)

    def ClearMenu(self):
        if self.windowFrame:
            wx.CallAfter(self.windowFrame.FadeOut)
            while self.clearingMenu: pass

    def MenuHome(self):
        self.ClearMenu()
        self.menulocation = [dc(self.menuData)]
        wx.CallAfter(self.DisplayMenu)

    def MoveMenuCursor(self, steps, redraw=True):
        if self.windowFrame:
            if steps != 0:
                menuloc = self.menuLocation.pop()
                menulen = len(menuloc)
                if menulen > 1:
                    removeselected = self.GetSelected(menuloc)
                    setselected = removeselected+steps
                    if setselected < 0: setselected = menulen-1
                    elif setselected > menulen-1: setselected = 0
                    try: menuloc[removeselected]["selected"]=False
                    except: pass
                    try: menuloc[setselected]["selected"] = True
                    except: menuloc[self.GetSelected(menuloc)]["selected"] = True
                    self.windowFrame.menuSelected = setselected
                self.menuLocation += [dc(menuloc)]
            if redraw: wx.CallAfter(self.DisplayMenu)

    def ExecuteCommand(self, **data):
        self.plugin.SERVER.send(**data)

    def GetSelected(self, menuList):
        for i, item in enumerate(menuList):
            if item['selected']: return i
        return 0

    def ReloadMenu(self, newMenu):
        menuloc = dc(self.menuLocation)
        self.menuData = dc(newMenu)
        if menuloc:
            newloc = []
            menuindex = [self.GetSelected(item) for item in menuloc]
            menudata = dc(newMenu)
            for i, locidx in enumerate(menuindex):
                print locidx
                if i < len(menuindex):
                    menudata[self.GetSelected(menudata)]['selected'] = False
                    menudata[locidx]['selected'] = True
                    newloc += [dc(menudata)]
                    menudata = menudata[locidx]['event']
                else: menudata = menudata[locidx]
            self.menuLocation = dc(newloc)
            wx.CallAfter(self.DisplayMenu)
        else: self.menuLocation = [dc(self.menuData)]

    def LoadMenu(self, newData):
        oldData = dc(self.menuData)
        if newData != oldData:
            self.ReloadMenu(dc(newData))

    def DisplayMenu(self):
        while self.menuLocation is None: pass

        try: menuList = dc(self.menuLocation[-1:][0])
        except: pass
        else:
            menuSelected = self.GetSelected(menuList)
            if self.windowFrame:
                self.windowFrame.UpdateWindow(menuList, menuSelected)
                wx.CallAfter(self.windowFrame.DrawWindow)
            elif not self.windowFrame:
               self.windowFrame = MenuDisplay(self, menuList, menuSelected, *self.storedSettings)
               wx.CallAfter(self.windowFrame.FadeIn)

class MenuDisplay(wx.Frame):

    def __init__(
                self,
                plugin,
                menuList,
                menuSelected,
                fontinfo,
                fontcolor,
                selectedfontcolor,
                backgroundcolor,
                backgroundtransparency,
                bordercolor,
                bordertransparency,
                bordercornerradius,
                borderwidth,
                menutimeout,
                windowtransparency,
                menufadeIn,
                menufadeOut,
                displaymonitor,
                menuwidth,
                menuheight,
                ):

        self.plugin = plugin
        self.menuList = menuList
        self.menuSelected = menuSelected
        self.fontInfo = fontinfo
        self.foreColor = fontcolor
        self.selForeColor = selectedfontcolor
        self.backColor = backgroundcolor+(backgroundtransparency,)
        self.borderColor = bordercolor+(bordertransparency,)
        self.cornerRadius = bordercornerradius
        self.borderWidth = borderwidth
        self.menuTimeOut = menutimeout
        self.windowTransparency = windowtransparency
        self.fadeIn = menufadeIn
        self.fadeOut = menufadeOut
        self.monitor = displaymonitor
        self.menuWidth = menuwidth
        self.menuHeight = menuheight
        self.scrollMenu = None
        self.infocus = True
        self.selectedCell = 0

        wx.Frame.__init__(self, None, title="MicasaVerde Vera On Screen",
                           style=wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.NO_BORDER)# | wx.TRANSPARENT_WINDOW)

        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDouble)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onWheel)

        self.ProcessFont()
        self.DetermineSize()
        
        wx.CallAfter(self.UpdateWindow, menuList, menuSelected)

    def onClose(self, evt=None):
        wx.CallAfter(self.plugin.EVENT.set)
        if evt: evt.Skip()

    def onEnter(self, evt):
        try: self.closeMenuTimer.Stop()
        except: pass
        self.infocus = True
        self.SetFocus()
        evt.Skip()

    def onLeave(self, evt):
        self.closeMenuTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onClose, self.closeMenuTimer)
        wx.CallAfter(self.closeMenuTimer.Start, self.menuTimeOut*1000)
        self.infocus = False
        evt.Skip()

    def GetMousePos(self, pos):
        for cellnum, cellpos in enumerate(self.cellSpacing):
            if pos[0] > cellpos[0][0] and pos[1] < cellpos[1][1]:
                if cellnum+self.menuSelected > len(self.menuList)-2:
                    cellnum = -len(self.menuList)+cellnum
                return cellnum
        return None

    def onLeftDown(self, evt):
        self.doublepresstimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onLeft, self.doublepresstimer)
        wx.CallAfter(self.doublepresstimer.Start, 200)
        if self.infocus:
            self.scrollMenu = self.GetMousePos(evt.GetPosition())
        evt.Skip()
        
    def onLeft(self, evt):
        self.doublepresstimer.Stop()
        if self.scrollMenu is not None and self.infocus:
            wx.CallAfter(self.plugin.MoveMenuCursor, self.scrollMenu)
        evt.Skip()

    def onLeftDouble(self, evt):
        self.doublepresstimer.Stop()
        if self.scrollMenu is not None and self.infocus:
            self.plugin.MoveMenuCursor(self.scrollMenu, redraw=False)
            item = self.menuList[self.menuSelected]['event']
            self.plugin.MoveMenuCursor(0)
            if isinstance(item, list):
                wx.CallAfter(self.plugin.UpLevel, item)
            elif isinstance(item, dict):
                wx.CallAfter(self.plugin.ExecuteCommand, **item)
        evt.Skip()

    def onWheel(self, evt):
        if self.infocus:
            rotation = evt.GetWheelRotation()
            delta = evt.GetWheelDelta()
            steps = rotation/(-(delta))
            self.plugin.MoveMenuCursor(steps)
        evt.Skip()

    def onKey(self, evt):
        if self.infocus:
            key = evt.GetKeyCode()
            if key == wx.WXK_HOME:
                wx.CallAfter(self.plugin.MenuHome)
            if key == wx.WXK_ESCAPE:
                wx.CallAfter(self.onClose)
            if key in [wx.WXK_UP, wx.WXK_NUMPAD_UP]:
                wx.CallAfter(self.plugin.MoveMenuCursor, -1)
            elif key in [wx.WXK_DOWN, wx.WXK_NUMPAD_DOWN] :
                wx.CallAfter(self.plugin.MoveMenuCursor, +1)
            elif key in [wx.WXK_LEFT, wx.WXK_NUMPAD_LEFT, wx.WXK_BACK]:
                wx.CallAfter(self.plugin.DownLevel)
            elif key in [wx.WXK_RIGHT, wx.WXK_NUMPAD_RIGHT, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
                item = self.menuList[self.menuSelected]['event']
                if isinstance(item, list):
                    wx.CallAfter(self.plugin.UpLevel, item)
                elif isinstance(item, dict):
                    wx.CallAfter(self.plugin.ExecuteCommand, **item)
        evt.Skip()
        
    def ProcessFont(self): 
        self.font = wx.Font(18, wx.FONTFAMILY_TELETYPE,wx.NORMAL,wx.BOLD, faceName="Arial")
        nativeFontInfo = wx.NativeFontInfo()
        nativeFontInfo.FromString(self.fontInfo)
        self.font.SetNativeFontInfo(nativeFontInfo)

    def DetermineSize(self):
        monitor = self.monitor
        memoryDC = wx.MemoryDC()
        memoryDC.SetFont(self.font)

        try: screenDimensions = GetMonitorDimensions()[monitor]
        except IndexError: screenDimensions = GetMonitorDimensions()[0]
        screenXPos, screenYPos, screenWidth, screenHeight = screenDimensions

        lineWidth = 0
        numLineChars = 0
        charWidth = 0
        charHeight = memoryDC.GetCharHeight()-20

        for item in self.menuList:
            line = dc(item["txt"])+"   ->"
            lineWidth = max([lineWidth, memoryDC.GetTextExtent(line)[0]])
            numLineChars = max([numLineChars, len(line)])
            charWidth = lineWidth/numLineChars

        menuLength = len(self.menuList)
        maxLineNum = int(int(screenHeight*self.menuHeight)/charHeight)
        leftBorder =  charHeight
        rightBorder = charHeight/2
        borderTotal = leftBorder+rightBorder
        userWidth = int(screenWidth*self.menuWidth)+borderTotal
        autoWidth = lineWidth+borderTotal

        if autoWidth < userWidth:
            if int(float(float(autoWidth)/float(userWidth))*100.0) < 60: menuWidth = autoWidth
            else: menuWidth = userWidth
        else: menuWidth = userWidth

        menuHeight = charHeight+(maxLineNum*charHeight) if maxLineNum < menuLength else charHeight+(menuLength*charHeight)

        numcells = maxLineNum if maxLineNum < menuLength else menuLength
       
        screenXPos = screenXPos+(screenWidth-menuWidth)/2
        screenYPos = screenYPos+(screenHeight-menuHeight)/2
        self.SetSize(wx.Size(menuWidth, menuHeight))
        self.SetPosition((screenXPos, screenYPos))
        self.roundedBox = (0, 0, menuWidth, menuHeight, self.cornerRadius)
        self.menuDimensions = ((leftBorder, charHeight/2), (menuWidth-rightBorder, menuHeight-(charHeight/2)))
        self.cellDimensions = (lineWidth, charHeight)
        self.cellChar = (charWidth, charHeight)
        self.cellNumber = numcells
        self.cellSpacing = ()
        for i in range(numcells):
            start = (leftBorder, (i*charHeight)+(charHeight/2))
            stop = (start[0]+lineWidth, start[1]+charHeight)
            self.cellSpacing += (start, stop),

    def UpdateWindow(self, menuList=None, menuSelected=None):

        if menuList is None and menuSelected is None:
            menuList = dc(self.menuList)
            menuSelected = self.menuSelected
        else:
            menuList += [None]
            self.menuSelected = menuSelected
            self.menuList = dc(menuList)

        menuStart, menuStop = self.menuDimensions
        border = menuStart[0]
        cellWidth, cellHeight = self.cellDimensions
        charWidth, charHeight = self.cellChar
        cellNumber = self.cellNumber
        listLength = len(menuList)
        posY = menuStart[1]
        linecommand = []

        for i in range(menuSelected, menuSelected+cellNumber):
            line = menuList[i] if i < listLength else menuList[i-listLength]
            if line is not None:
                linecommand += [[[line['txt'], border, posY], None, [self.foreColor]]]
                if line['selected']:
                    linecommand.pop()
                    if line['selectforeground']:
                         linecommand += [[[line['txt'], border/2, posY], None, [self.selForeColor]]]
                    else:
                        linecommand += [[[line['txt'], border/2, posY], None, [self.foreColor]]]
                if isinstance(line['event'], list) or isinstance(line['event'], dict):
                    txt = "  -->"
                    if isinstance(line['event'], dict): txt = "  -*-"
                    changeline = linecommand.pop()
                    linecommand += [[changeline[0], [txt, menuStop[0]-(charWidth*5), posY], changeline[2]]]
            else:
                linecommand += [[[" ", menuStart[0], posY], None, [self.foreColor]]]
            posY += cellHeight

        self.lineCommand = linecommand
       
    def DrawWindow(self, windowTransparency=None):
        if windowTransparency is None: windowTransparency = self.windowTransparency

        DC = wx.MemoryDC()
        self.bmp = wx.EmptyBitmap(*self.GetClientSizeTuple())
        DC.SelectObject(self.bmp)
        DC = wx.GCDC(DC)
        DC.SetBrush(wx.Brush(wx.Colour(*self.backColor)))
        DC.SetPen(wx.Pen(wx.Colour(*self.borderColor), self.borderWidth))
        DC.DrawRoundedRectangle(*self.roundedBox)
        DC.SetFont(self.font)
 
        lines = self.lineCommand

        for line in lines:
            DC.SetTextForeground(*line[2])
            DC.DrawText(*line[0])
            try: DC.DrawText(*line[1])
            except: pass
        DC.Destroy()
        del DC

        self.DrawAlpha(windowTransparency)

    def DrawAlpha(self, windowTransparency):
        hndl = self.GetHandle()
        cRef = ctypes.byref
        style = win32gui.GetWindowLong(hndl, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hndl, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
        
        sDC = win32gui.GetDC(win32gui.GetDesktopWindow())
        cDC = win32gui.CreateCompatibleDC(sDC)
       
        win32gui.SelectObject(cDC, self.bmp.GetHandle())
        ret = ctypes.windll.user32.UpdateLayeredWindow(
                hndl, sDC, cRef(POINT(*self.GetPositionTuple())), cRef(SIZE(*self.GetClientSizeTuple())),
                cDC, cRef(POINT(0,0)), win32api.RGB(0,0,0), cRef(BLENDFUNCTION(0, 0, windowTransparency, 1)), win32con.ULW_ALPHA)

    def FadeIn(self):
        for i in range(0, self.fadeIn):
            self.DrawWindow((self.windowTransparency//self.fadeIn)*i)
            self.Show(True)
        self.DrawWindow(self.windowTransparency)
        self.Show(True)

    def FadeOut(self):
        try: self.closeMenuTimer.Stop()
        except: pass
        self.plugin.clearingMenu = True
        self.plugin.windowFrame = False
        for i in range(0, self.fadeOut):
            self.DrawWindow(self.windowTransparency*(self.fadeOut-i)//self.fadeOut)
            time.sleep(.01)
        self.plugin.clearingMenu = False        
        wx.CallAfter(self.Show, False)
        wx.CallAfter(self.Destroy)

class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_long), ('y', ctypes.c_long)]

class SIZE(ctypes.Structure):
    _fields_ = [('cx', ctypes.c_long),('cy', ctypes.c_long)]

class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [('BlendOp', ctypes.c_ubyte),('BlendFlags', ctypes.c_ubyte),
                ('SourceConstantAlpha', ctypes.c_ubyte),('AlphaFormat', ctypes.c_ubyte)]