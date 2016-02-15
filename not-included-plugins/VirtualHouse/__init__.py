# -*- coding: utf-8 -*-

version="0.0.1"

# plugins/VirtualHouse/__init__.py
#
# Copyright (C)  2011   Pako (lubos.ruckl@quick.cz)
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
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.1 by Pako 2011-09-26 14:13 UTC+1
#     - initial version
#===============================================================================
# Sources:
# FourWaySplitter wxPython Demo by Andrea Gavana
# http://wiki.wxpython.org/HookingTheWndProc
#===============================================================================

import eg
import wx
import wx.lib.agw.fourwaysplitter as FWS
from win32gui import SendMessage, GetWindowPlacement
from eg.WinApi.Dynamic import ShowWindow
from os.path import join
from cStringIO import StringIO
from base64 import b64decode
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from win32gui import FindWindow, GetWindow, GetWindowText
WM_COMMAND = 273
SW_RESTORE = 9
GW_CHILD = 5
GW_HWNDNEXT = 2

ICON = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAA"
    "As9JREFUOI2Fkk9om3Ucxj+/P+/b5F2ytKlp2LI6YW16EPdHbBVCdQML+4PIBJFBYezU"
    "+y720Ntuu3gZgicFM1DUCoIIelGwQzroNpSaCpayWNLYmKRNmuR937y/nwcXUNjmc3ng"
    "4Xk+fA9feIqKMHobXnpa54m6DZP3T5z47dfjxw++cJxLT+qpx4WfuW7h9MmT343ncuOq"
    "13MSsdjbc75f/qTfv/+/gK9SqXfOzMwsj2Wzh22jge10kEqpZDz+5vkg6F0Kw5XlxwGK"
    "wMKRI4tnCoX3h9NpJyqX2ZSSWj5PulJBaC0S8fjrvTAcvhiG3y7/G1AEcpOTH5w+d+5d"
    "LxYT/vo6m7kc3s2beHNz/NlsktrYQChFwvNeCfr9yQtB8OXyAHDF886/fPnye0PWsr+6"
    "SvnsWUaWljiUSjEyMkJsepqqlCTW1lBK4Q4NvdBotdY+t3ZDFYGpQuHDsWTy2d07d2gu"
    "LJC+dg3P83BdF2MMWmsOnTpFPZvFWVkhpjU9Y45+3O1+JD513ddenZ39vlmtwo0bJKen"
    "kVIihMBaC/Af31tdRS0tITode3dra0Y7kNh68OBn/9ato2NTU6OljRLGGDzPY/zYMXw/"
    "4N76JjLqEsk4z+XG6S4u7nnXr9eHlErqt4Lg62Kt9s0zw8P39vf3Rn9c+QEhBEIILl54"
    "AxMZ7j4EVf+dXup5HFXHy2S2t2u1F+fBlwDzYMIwbCil0VqjlEJKibWGKIrY3m1x0PX5"
    "ZfMvpDCEYdicBx9ADv4gCIImgNYaIQWj3k9YazHG0Ol0cB2F51pijiQMw8Zgpx+5bLfb"
    "bQClNNZamkEBYyzNZpOrhSRCHGYWCPwe7Xb74NG2PwCInZ2dh9lsFiwYYxFCUNvdxXFc"
    "tB7U/lGlUvljcL0YhBMTEzKfz6er1Wq81Wp5QRDEoihyrLUopfqO4/iJRKKTyWQ6pVKp"
    "Xi6XI4C/AVS9KsY8CMWeAAAAAElFTkSuQmCC"
)


eg.RegisterPlugin(
    name="Virtual House",
    description = r"""<rst>
Plugin for control the Virtual house.
""",
    #url="http://www.eventghost.net/",
    author = "Pako",
    version = version,
    guid = "{97E1A82A-986F-4804-8E0E-E4BB88B1C569}",
    kind="external",
    icon = ICON,
    createMacrosOnAdd = True,
)
#===============================================================================

OFF_LAMP = (
        "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"
        "bDcAAAAASUVORK5CYII="
    )

ON_LAMP = (
    "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"
)

EMPTY = (
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEX///8AAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABhFghhFggAFlQAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/fYdSAAAA"
    "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAABJJREFUeNpjYBgFo2AUjALs"
    "AAAEIAABfMHvuAAAAABJRU5ErkJggg=="
)

FAR_SYM = u"°F"
CEL_SYM = u"°C"

COMMANDS = {
    "GetState":        0x080000,
    "SetLightOn":      0x0C0000,
    "SetLightOff":     0x0C0000,
    "ToggleLight":     0x100000,
    "SetTemperature":  0x200000,
    "TemperatureUp":   0x300000,
    "TemperatureDown": 0x400000,
    "SetAllLightsOff": 0x500000,
    "SetAllLightsOn":  0x500000,
}    

EVENTS = {
    0x040000:("UnitChanged",1,0xFFFFFFFF),
    0x080000:("State",1,0xFFFFFFFF),
    0x0C0000:("Light",0x7,1),
    0x200000:("Temperature",0x7,0xFF),
    0x500000:("AllLights",0,0x1),
    0x800000:("MainSwitch",0,0x1)    
}

RESULTS = {
    0x080000: 0x080000,
    0x0C0000: 0x0C0000,
    0x100000: 0x0C0000,
    0x500000: 0x500000,
    0x200000: 0x200000,
    0x300000: 0x200000,
    0x400000: 0x200000
}    
#===============================================================================

#globals:
bmp_off = bmp_on = bmp_empty = None
#===============================================================================

def GetHwnd():   
    vh = FindWindow("wxWindowClassNR", "Virtual house")
    while vh:
        panel = GetWindow(vh, GW_CHILD)
        if GetWindowText(panel) == "FWS panel":
            return panel
        vh = GetWindow(vh, GW_HWNDNEXT)
    return None
#------------------------------------------------------------------------------

class ConfigData(eg.PersistentData):
    minMax = None
    pos = None
#------------------------------------------------------------------------------

class Text:
    err1 = 'HW of "Virtual house" is not present'
    lampHint = "Click to toggle lamp"
    tempLabel = "Temper.:"
    temprLabel = "Temperature:"
    btnOff = "All off"
    btnOn = "All on"
    title = "Virtual house"
    prefix = "VirtualHouse"
    btn = (
        "Open control panel",
        "Close control panel",
    )
    label = "Select room"
    rooms = (
        "Room 1",
        "Room 2",
        "Room 3",
        "Room 4",
    )    
#------------------------------------------------------------------------------

class RoomPanel(wx.Panel):
    def __init__(self, parent, colour, label, plugin):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN, name = label)
        self.plugin = plugin
        text = self.plugin.text
        self.SetBackgroundColour(colour)
        self.roomLabel = wx.StaticText(self, -1, label, (12,1))
        font = self.roomLabel.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.roomLabel.SetFont(font)
        self.bitmap = wx.StaticBitmap(self, -1, bmp_empty, (18, 18))
        self.bitmap.SetToolTipString(text.lampHint)
        label1 = wx.StaticText(self, -1, text.tempLabel, (3,54))
        self.label2 = wx.StaticText(self, -1, CEL_SYM, (89,54))
        sc = wx.TextCtrl(self, -1, "", (48, 51),(24,-1), style = wx.TE_READONLY)
        spinBtn = wx.SpinButton(self, -1, (72, 51), (16, 20), wx.SP_VERTICAL)
        self.sc = sc
        self.Bind(wx.EVT_SPIN_UP, self.OnSpinUp)
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown)
        self.bitmap.Bind(wx.EVT_LEFT_DOWN, self.onClick)


    def Reset(self):
        self.label2.SetLabel(CEL_SYM)
        self.sc.SetValue("")
        self.bitmap.SetBitmap(bmp_empty)


    def SetUnit(self, unit):
        self.label2.SetLabel(unit)


    def onClick(self, evt):
        eg.plugins.VirtualHouse.ToggleLight(int(self.GetName()[-1]))
        evt.Skip()


    def OnSpinUp(self, evt):
        eg.plugins.VirtualHouse.TemperatureUp(int(self.GetName()[-1]))
        evt.Skip()


    def OnSpinDown(self, evt):
        eg.plugins.VirtualHouse.TemperatureDown(int(self.GetName()[-1]))
        evt.Skip()


    def SetValue(self, value):
        self.bitmap.SetBitmap(bmp_on if bool(value & 0x80) else bmp_off)
        self.sc.SetValue(str(value & 0x7f))
        self.Refresh()


    def SetLight(self, value):
        self.bitmap.SetBitmap(bmp_on if bool(value & 0x1) else bmp_off)
        self.Refresh()


    def SetTemperature(self, value):
        self.sc.SetValue(str(value & 0x7f))
        self.Refresh()
#------------------------------------------------------------------------------

class ButtonPanel(wx.Panel):
    def __init__(self, parent, plugin):
        self.plugin = plugin
        text = self.plugin.text
        wx.Panel.__init__(self, parent, name = "Button panel")
        buttonOff = wx.Button(self, -1, text.btnOff, size = (40,22))
        font = buttonOff.GetFont()
        font.SetPointSize(8)
        buttonOff.SetFont(font)
        buttonOn = wx.Button(self, -1, text.btnOn, size = (40,22))
        buttonOn.SetFont(font)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((0, -1), 0, wx.ALL, 3)
        sizer.Add(buttonOff, 0, wx.ALL, 3)
        sizer.Add(buttonOn, 0, wx.ALL, 3)
        self.SetSizer(sizer)
        buttonOn.Bind(wx.EVT_BUTTON, self.OnButtonOn)
        buttonOff.Bind(wx.EVT_BUTTON, self.OnButtonOff)

    def OnButtonOn(self, evt):
        hwnd = GetHwnd()
        if not hwnd:
            eg.PrintError(self.plugin.text.err1)
            return
        eg.plugins.VirtualHouse.SetAllLightsOn()
        evt.Skip()

    def OnButtonOff(self, evt):
        hwnd = GetHwnd()
        if not hwnd:
            eg.PrintError(self.plugin.text.err1)
            return
        eg.plugins.VirtualHouse.SetAllLightsOff()
        evt.Skip()


class FWSPanel_EG(wx.Panel):

    def __init__(self, parent, plugin):
        self.plugin = plugin
        text = self.plugin.text
        self.plugin.controlPanel = self
        wx.Panel.__init__(self, parent, -1, name = "FWS panel EG")
        bp = ButtonPanel(self, plugin)
        splitter = FWS.FourWaySplitter(self, agwStyle = wx.SP_LIVE_UPDATE)
        self.splitter = splitter
        self.unit = CEL_SYM
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        sizer.Add(bp)
        self.SetSizer(sizer)
        colour = "#DDDDDD"
        self.p1 = RoomPanel(splitter, colour, text.rooms[0], plugin)
        splitter.AppendWindow(self.p1)
        self.p2 = RoomPanel(splitter, colour, text.rooms[1], plugin)
        splitter.AppendWindow(self.p2)
        self.p3 = RoomPanel(splitter, colour, text.rooms[2], plugin)
        splitter.AppendWindow(self.p3)
        self.p4 = RoomPanel(splitter, colour, text.rooms[3], plugin)
        splitter.AppendWindow(self.p4)
        self.plugin.SendCommand("GetState", 0, 0, False)


    def SetUnit(self, unit):
        self.p1.SetUnit(unit)
        self.p2.SetUnit(unit)
        self.p3.SetUnit(unit)
        self.p4.SetUnit(unit)


    def SetAllLights(self, value):
        self.p1.SetLight(value)
        self.p2.SetLight(value)
        self.p3.SetLight(value)
        self.p4.SetLight(value)       
#------------------------------------------------------------------------------

class VirtualHouseFrame(wx.Frame):

    def __init__(
        self,
        parent = None,
        id = wx.ID_ANY,
        size=(222, 218),
        style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX),
        plugin = None
    ):
        self.plugin = plugin
        title = self.plugin.text.title
        jpg_off = b64decode(OFF_LAMP)
        stream_off = StringIO(jpg_off)
        jpg_on = b64decode(ON_LAMP)
        stream_on = StringIO(jpg_on)
        jpg_empty = b64decode(EMPTY)
        stream_empty = StringIO(jpg_empty)
        global bmp_off, bmp_on, bmp_empty
        bmp_off = wx.BitmapFromImage(wx.ImageFromStream(stream_off))
        bmp_on = wx.BitmapFromImage(wx.ImageFromStream(stream_on))
        bmp_empty = wx.BitmapFromImage(wx.ImageFromStream(stream_empty))
        wx.Frame.__init__(self, parent, id, title, size = size, style=style, name = "Virtual house frame")
        self.fwsPanel = FWSPanel_EG(self, plugin = plugin)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.fwsPanel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Layout()
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        icn = wx.Icon(join(eg.imagesDir, "Execute.png"), wx.BITMAP_TYPE_PNG)
        self.SetIcon(icn)

        if ConfigData.pos:
            self.SetPosition(ConfigData.pos)
        else:
            self.CenterOnScreen()
        self.Show()


    def OnQuit(self, event):
        hwnd = self.GetHandle()
        wp = GetWindowPlacement(hwnd)[4]
        cdr = wx.GetClientDisplayRect()
        #Note: GetPosition() return (-32000, -32000), if window is minimized !!!
        pos = (wp[0] + cdr[0], wp[1] + cdr[1])
        if pos != ConfigData.pos:
            ConfigData.pos = pos
        self.plugin.controlPanel = None
        self.Show(False)
        self.Destroy()
        event.Skip()
        #self = None
#------------------------------------------------------------------------------

class dummyFwsPanel:
    class p:
        def SetValue(self, value = None):
            pass
        SetLight = SetValue
        ToggleLight = SetValue
        SetTemperature = SetValue
        TemperatureUp = SetValue
        TemperatureDown = SetValue
        Reset = SetValue
    p1 = p()
    p2 = p1
    p3 = p1
    p4 = p1
    def SetUnit(self, unit):
        pass
    SetAllLights = SetUnit
#------------------------------------------------------------------------------

class VirtualHouse(eg.PluginBase):
    text=Text
    minMax = (10, 30)
    controlPanel = None
    event = None
    result = None
    state = []
    
    def __init__(self):
        if ConfigData.minMax:
            self.minMax = ConfigData.minMax
        self.AddActionsFromList(ACTIONS)
    #    self.AddEvents()
        
   
    def __start__(self, dummy = None):
        self.info.eventPrefix = self.text.prefix
        eg.messageReceiver.AddHandler(WM_COMMAND, self.HandleMsg)
        self.SendCommand("GetState", 0, 0, False)
        
        
    def __stop__(self):
        eg.messageReceiver.RemoveHandler(WM_COMMAND, self.HandleMsg)
        if self.controlPanel:
            wx.CallAfter(self.controlPanel.GetParent().OnQuit, wx.CommandEvent())
            self.controlPanel = None


    def HandleMsg(self, dummyHWnd, mesg, wParam, lParam):
        if self.controlPanel:
            fwsPanel = self.controlPanel
        else:
            fwsPanel = dummyFwsPanel()
        rooms = (None, fwsPanel.p1, fwsPanel.p2, fwsPanel.p3, fwsPanel.p4)
        if wParam & 0xFF0000 == 0x40000 or wParam & 0xFF0000 == 0x80000:
            state = [int(wParam & 0x1)]
            fwsPanel.SetUnit((CEL_SYM, FAR_SYM)[wParam & 0x1])
            self.minMax = ((10, 30), (50, 86))[wParam & 0x1]
            if ConfigData.minMax != self.minMax:
                ConfigData.minMax = self.minMax
            room_1 = lParam & 0x000000FF
            state.append((int(room_1 & 0x80)/0x80, int(room_1 & 0x7f)))
            room_2 = (lParam & 0x0000FF00) >> 8
            state.append((int(room_2 & 0x80)/0x80, int(room_2 & 0x7f)))
            room_3 = (lParam & 0x00FF0000) >> 16
            state.append((int(room_3 & 0x80)/0x80, int(room_3 & 0x7f)))
            room_4 = (lParam & 0xFF000000) >> 24
            state.append((int(room_4 & 0x80)/0x80, int(room_4 & 0x7f)))
            self.state = state
            fwsPanel.p1.SetValue(room_1)
            fwsPanel.p2.SetValue(room_2)
            fwsPanel.p3.SetValue(room_3)
            fwsPanel.p4.SetValue(room_4)
        elif wParam & 0xFF0000 == 0xC0000:
            rooms[wParam & 0xF].SetLight(lParam)
        elif wParam & 0xFF0000 == 0x200000:
            rooms[wParam & 0xF].SetTemperature(lParam)
        elif wParam & 0xFF0000 == 0x500000:
            fwsPanel.SetAllLights(lParam)
        elif wParam & 0xFF0000 == 0x800000:
            if not lParam:
                for room in rooms[1:]:
                    room.Reset()
        value = wParam & 0xFF0000
        if value in EVENTS:
            event = EVENTS[value]
            suffix = event[0]
            if not event[1]:
                payload = (lParam & event[2], (lParam & 0x100)>>8)
            else:
                payload = (int(wParam & event[1]), lParam & event[2], (lParam & 0x100)>>8)
            if self.event:
                if self.event[0] in RESULTS:
                    if value == RESULTS[self.event[0]]:
                        if value == 0x080000:
                            self.result = state
                        else:
                            self.result = payload
                        wx.Yield()
                        SetEvent(self.event[1])
                        if value == 0x080000: #No event
                            self.event = None
                            return
            #else:
            payload = state if (value == 0x040000 or value == 0x080000) else payload
            self.TriggerEvent(suffix, payload = payload)
        self.event = None


    def SendCommand(self, cmd, room, value, wait = True):
        if wait:
            event = CreateEvent(None, 0, 0, None)
            self.event = (COMMANDS[cmd], event)
        hwnd = GetHwnd()
        if hwnd:
            SendMessage(hwnd, WM_COMMAND, COMMANDS[cmd]+room, value)
            if wait:
                eg.actionThread.WaitOnEvent(event)
                res = self.result
                self.result = None
                return res
        else:
            eg.PrintError(self.text.err1)
#===============================================================================

class SetRoom(eg.ActionBase):
    #class text:
    #    label = "Select room"
    #    rooms = (
    #        "Room 1",
    #        "Room 2",
    #        "Room 3",
    #        "Room 4",
    #    )

    def __call__(self, room = 0):
        return self.plugin.SendCommand(self.__class__.__name__, room, self.value)


    def GetLabel(self, room):
        return "%s: %s" % (self.name, self.plugin.text.rooms[room-1])


    def Configure(self, room = 0):
        text = self.plugin.text
        panel = eg.ConfigPanel(self)
        bagSizer = wx.GridBagSizer(20, 20)
        staticBox = wx.StaticBox(panel, -1, text.label)
        staticSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        staticSizer.Add(bagSizer, 0, wx.ALL, 15)
        panel.sizer.Add(staticSizer, 0, wx.TOP|wx.LEFT, 20)
        rb1 = wx.RadioButton(panel, -1, text.rooms[0], style=wx.RB_GROUP)
        rb2 = wx.RadioButton(panel, -1, text.rooms[1])
        rb3 = wx.RadioButton(panel, -1, text.rooms[2])
        rb4 = wx.RadioButton(panel, -1, text.rooms[3])
        rb1.SetValue(room == 1)
        rb2.SetValue(room == 2)
        rb3.SetValue(room == 3)
        rb4.SetValue(room == 4)
        bagSizer.Add(rb1,(0,0))
        bagSizer.Add(rb2,(0,1))
        bagSizer.Add(rb3,(1,0))
        bagSizer.Add(rb4,(1,1))

        while panel.Affirmed():
            i = 1
            for rb in (rb1, rb2, rb3, rb4):
                if rb.GetValue():
                    break
                i += 1
            panel.SetResult(i)      
#===============================================================================

class SetTemperature(eg.ActionBase):
    dirty = False
    #class text:
    #    label = "Select room"
    #    rooms = (
    #        "Room 1",
    #        "Room 2",
    #        "Room 3",
    #        "Room 4",
    #    )
    #    temprLabel = "Temperature:"

    def __call__(self, room = 0, tempr = 0):
        return self.plugin.SendCommand(self.__class__.__name__, room, tempr)


    def ConversionTempr(self, tempr):
        if not tempr:
            self.dirty = True
            tempr = 22 if self.plugin.minMax == (10,30) else 72
        if tempr not in range(self.plugin.minMax[0], self.plugin.minMax[1]+1):
            self.dirty = True
            if tempr < self.plugin.minMax[0]:
                tempr = 32 + int(0.5 + 9.0 * tempr / 5.0)
            else:
                tempr = int(0.5 + 5.0 * (tempr - 32) / 9.0)
        return tempr


    def GetLabel(self, room, tempr):
        tempr = self.ConversionTempr(tempr)
        return "%s: %s: %i" % (self.name, self.plugin.text.rooms[room-1], tempr)


    def Configure(self, room = 0, tempr = 0):
        self.dirty = False
        tempr = self.ConversionTempr(tempr)
        text = self.plugin.text
        panel = eg.ConfigPanel(self)
        panel.isDirty = self.dirty
        bagSizer = wx.GridBagSizer(20, 20)
        staticBox = wx.StaticBox(panel, -1, text.label)
        staticSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        staticSizer.Add(bagSizer, 0, wx.ALL, 15)
        panel.sizer.Add(staticSizer, 0, wx.TOP|wx.LEFT, 20)
        rb1 = wx.RadioButton(panel, -1, text.rooms[0], style=wx.RB_GROUP)
        rb2 = wx.RadioButton(panel, -1, text.rooms[1])
        rb3 = wx.RadioButton(panel, -1, text.rooms[2])
        rb4 = wx.RadioButton(panel, -1, text.rooms[3])
        rb1.SetValue(room == 1)
        rb2.SetValue(room == 2)
        rb3.SetValue(room == 3)
        rb4.SetValue(room == 4)
        bagSizer.Add(rb1,(0,0))
        bagSizer.Add(rb2,(0,1))
        bagSizer.Add(rb3,(1,0))
        bagSizer.Add(rb4,(1,1))
        temprLabel = wx.StaticText(panel, -1, text.temprLabel)
        temprCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            tempr,
            min = self.plugin.minMax[0],
            max = self.plugin.minMax[1]
        )
        temprSizer = wx.BoxSizer(wx.HORIZONTAL)
        temprSizer.Add(temprLabel,0,wx.TOP,3)
        temprSizer.Add(temprCtrl,0,wx.LEFT,5)
        panel.sizer.Add(temprSizer, 0, wx.TOP|wx.LEFT, 20)
        if self.value < 2:
            temprLabel.Show(False)
            temprCtrl.Show(False)

        while panel.Affirmed():
            i = 1
            for rb in (rb1, rb2, rb3, rb4):
                if rb.GetValue():
                    break
                i += 1
            if self.value > 1:
                tempr = temprCtrl.GetValue()
            panel.SetResult(i, tempr)      
#===============================================================================

class SetAllLight(eg.ActionBase):

    def __call__(self):
        return self.plugin.SendCommand(self.__class__.__name__, 0, self.value)
#===============================================================================

class GetState(eg.ActionBase):

    def __call__(self):
        return self.plugin.SendCommand(self.__class__.__name__, 0, 0)
#===============================================================================

class ShowControlPanel(eg.ActionBase):

    def __call__(self):
        if not self.plugin.controlPanel:
            wx.CallAfter(VirtualHouseFrame, plugin = self.plugin)
        else:
            if self.plugin.controlPanel.GetParent().GetPosition() == (-32000, -32000):
                ShowWindow(self.plugin.controlPanel.GetParent().GetHandle(), SW_RESTORE) 
            wx.CallAfter(self.plugin.controlPanel.GetParent().Raise)
#===============================================================================

class HideControlPanel(eg.ActionBase):

    def __call__(self):
        if self.plugin.controlPanel:
            wx.CallAfter(self.plugin.controlPanel.GetParent().Close)
#===============================================================================

ACTIONS = (
    (SetRoom, 'SetLightOn', 'Light turn on', 'Light turn on.', 1),
    (SetRoom, 'SetLightOff', 'Light turn off', 'Light turn off.', 0),
    (SetRoom, 'ToggleLight', 'Toggle light', 'Toggle light.', -1),
    (SetAllLight, 'SetAllLightsOff', 'All lights turn off', 'All lights turn off.', 0),
    (SetAllLight, 'SetAllLightsOn', 'All lights turn on', 'All lights turn on.', 1),
    (SetRoom, 'TemperatureUp', 'Temperature up', 'Temperature up.', 1),
    (SetRoom, 'TemperatureDown', 'Temperature down', 'Temperature down.', -1),
    (SetTemperature, 'SetTemperature', 'Set temperature', 'Set temperature.', 2),
    (GetState, 'GetState', 'Get state', 'Get state.', None),
    (ShowControlPanel, 'ShowControlPanel', 'Open control panel', 'Open control panel.', 2),
    (HideControlPanel, 'HideControlPanel', 'Hide control panel', 'Hide control panel.', 2),
)

