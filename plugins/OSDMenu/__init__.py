# ==============================================================================
# On Screen v.0.1.2
# ==============================================================================
#
# Plugins/OSDMenu/__init__.py
#
# Copyright (C) 2007 Easy
#
#Changelog:
# v0.1.2
#   Switched to Graphic Context drawing
#   Some visual improvements (transparency, background)
#   Window drawing is now Windows(R) job
#   More object oriented script
#   Now text entry can be not only strings, but also variables, like {eg.result}
#
#from eg.WinAPI.Utils import GetMonitorDimensions

eg.RegisterPlugin(
    name = "On Screen Menu",
    guid='{91E407C6-CD57-4161-BE2D-1D561296D48F}',
    author = "Easy",
    version = "0.1.1",
    description = (
                    'On screen menu.</p>\n\n<p>To get an onscreen menu generate events '
                    'You\'ll need to compose it using macros:<br> First, add macro called '
                    '"Add item - event" then specify the name wich will be shown in the menu '
                    'and the corresponding name of an event wich will be generated.<br>'
                    'Then add macros "Menu Up", "Menu Down", "Show", "Close" and assign '
                    'Your controls to them.<br>'
                    'Please keep in mind, that plugin is still verry, I mean it - <b>verry '
                    'experimental</b>.'
    ),
    kind = "other",
    createMacrosOnAdd = True,
    icon= (
            "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0"
            "RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAD1SURBVHjapFNLDoIwEJ2GhgUJ"
            "lQRZsOAEnAXXLmQl13LvRnZyEC5hwhIjnzQBO1URMJAik0xJ08frmzdT0rYtrAl6TZLHKgJc"
            "dkFgMMZgrOaz738xy7IEXdfhEscFBUKgaRrwPA/SNL2p3EoIcauqeikgo0Nzf5r9+X4+/paA"
            "4TjOJGiOvCPIskxZReeRJBAeGIYBmqYpK0D8QMHWtqWrqgoQ/27Lt4Q5o5Q8WNKJIYGQsbGs"
            "zoOp2/uB+IEC3/flMEVR5KIXlFJJKAZGJp5hcs5lIr7rAo7mIQyLf98CUXmNeZ7jlDVCDRcl"
            "1yZj9SKCuXgKMACP5GZ5mVX+bAAAAABJRU5ErkJggg=="
    ),
)

import wx
import sys
import time
import ctypes
import win32api
import win32con
import win32gui
import LayeredWindow
from threading import Timer
from eg.WinApi.Utils import GetMonitorDimensions


class Text:
    GrafixBox = 'Font and Color Settings'
    FontText = 'Font: '
    ForeText = 'Font Color: '
    BackText = 'Background Color: '
    SelForeText = 'Selected Font Color: '
    BorderText = 'Border Color: '
    MonitorBox = 'Monitor Settings'
    MonitorText = 'Display Monitor: '
    FadeBox = 'Fade Settings'
    FadeInText = 'Fade in Steps: '
    FadeOutText = 'Fade Out Steps: '
    TransBox = 'Transparency'
    BackTransText = 'Background Transparency: '
    BordWidtBox = 'Border Width'
    BordWidtText = 'Width: '
    ItemBox = 'Menu Item'
    ItemText = 'Item: '
    EvtBox = 'Menu Event'
    EvtText = 'Event: '
    EventBox = 'Event Settings'
    PrefixText = 'Prefix: '
    class CloseMenu:
        name = "Close"
        description = "Close menu window."
        iconFile = 'icons/close'
    class BuildMenu:
        name = "Build Menu"
        description = "Build nested menus in list format" \
                        "in this format: [[item, event, payload],[item, 'LVL', 3], [item, event, payload]]" \
                        "if you want to change a level put LVL in the event field and the index number you want" \
                        "to go to in the payload. do not nest the list keep it one menu per index"
    class AddItem:
        name = "Add item - event"
        description = "Adds an item wich, when selected, triggers an event."
        iconFile = 'icons/add'
    class MenuBack:
        name =  'Menu Back'
        description = 'Backup to the pervious nested menu'
    class MenuForward:
        name = 'Menu Forward'
        description = "Pretty Much the same as Execute except this wont close the menu"
    class MenuDown:
        name = "Menu Down"
        description = "Move selection down."
        iconFile = 'icons/menu_down'
    class MenuUp:
        name = "Menu Up"
        description = "Move selection up."
        iconFile = 'icons/menu_up'
    class ExecuteItem:
        name = "Execute"
        description = "Triggers an event associated with current menu item."
        iconFile = 'icons/enter'
    class DisplayMenu:
        name = "Show"
        description = "Show composed menu. This should be the last action in Your macro."
        iconFile = 'icons/plugin'

class OSMenu(eg.PluginClass):

    text = Text
        
    def __init__(self):
        self.AddAction(AddItem)
        self.AddAction(DisplayMenu)
        self.AddAction(MenuDown)
        self.AddAction(MenuUp)
        self.AddAction(ExecuteItem)
        self.AddAction(CloseMenu)
        self.AddAction(MenuBack)
        self.AddAction(MenuForward)
        self.AddAction(BuildMenu)

    def __start__(self, font, fore, back, selfore, border, trans, width, monitor, fadeIn, fadeOut, prefix):
        self.fontInfo=font
        self.foreColor = fore
        self.backColor = back
        self.selForeColor = selfore
        self.borderColor = border
        self.transparency = int(trans)
        self.borderWidth = int(width)
        self.monitor=monitor
        self.fadeIn=int(fadeIn)
        self.fadeOut=int(fadeOut)
        self.info.eventPrefix = prefix
        self.ProcessFont()

        self.menuList = []
        self.menuLevels = []
        self.menuSelected = 0
        self.menuLevelsSelected = []
        self.currentLevel = 0

        self.windowFrame = False

    def Configure(self, font='0;-96;0;0;0;700;255;0;0;0;3;2;1;82;Gabriola', fore=(0,255,0), back=(32, 32, 32), selfore=(34,24,218), border=(32, 32, 32), trans=50, width=30,
                        monitor=1, fadeIn=20, fadeOut=50, prefix='OSDMenu'):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.FontSelectButton(font)
        st2 = panel.ColourSelectButton(fore)
        st3 = panel.ColourSelectButton(back)
        st4 = panel.ColourSelectButton(selfore)
        st5 = panel.ColourSelectButton(border)
        st6 = panel.SpinNumCtrl(trans, increment=1.0)
        st7 = panel.SpinNumCtrl(width, increment=1.0)
        st8 = panel.DisplayChoice(monitor)
        st9 = panel.SpinNumCtrl(fadeIn, increment=1.0)
        st10 = panel.SpinNumCtrl(fadeOut, increment=1.0)
        st11 = panel.TextCtrl(prefix)

        eg.EqualizeWidths((st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11))
 
        box1 = panel.BoxedGroup(
                            text.GrafixBox,
                            (text.FontText, st1),
                            (text.ForeText, st2),
                            (text.BackText, st3),
                            (text.SelForeText, st4),
                            (text.BorderText, st5)
                            )
        box2 = panel.BoxedGroup(
                            text.TransBox,
                            (text.BackTransText,st6)
                            )
        box3 = panel.BoxedGroup(
                            text.BordWidtBox,
                            (text.BordWidtText,st7)
                            )
        box4 = panel.BoxedGroup(
                            text.MonitorBox,
                            (text.MonitorText,st8)
                            )
        box5 = panel.BoxedGroup(
                            text.FadeBox,
                            (text.FadeInText,st9),
                            (text.FadeOutText,st10)
                            )
        box6 = panel.BoxedGroup(
                            text.EventBox,
                            (text.PrefixText,st11)
                            )
      
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND),
                            (box3, 0, wx.EXPAND),
                            (box4, 0, wx.EXPAND),
                            (box5, 0, wx.EXPAND),
                            (box6, 0, wx.EXPAND)
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue(),
                            st5.GetValue(),
                            st6.GetValue(),
                            st7.GetValue(),
                            st8.GetValue(),
                            st9.GetValue(),
                            st10.GetValue(),
                            st11.GetValue()
                            )

    def ProcessFont(self):
        self.font=wx.Font(18, wx.FONTFAMILY_TELETYPE,wx.NORMAL,wx.BOLD, faceName="Arial")
        if self.fontInfo:
            nativeFontInfo = wx.NativeFontInfo()
            nativeFontInfo.FromString(self.fontInfo)
            self.font.SetNativeFontInfo(nativeFontInfo)

    def CloseMenu(self):
        if self.windowFrame:
            if self.windowFrame.IsShown():
                wx.CallAfter(self.windowFrame.FadeOut,self.fadeOut)
                self.windowFrame = False
            else: print "No window to close"

    def ClearMenu(self):
        self.ResetMultiLevel()
        if len(self.menuList) > 0:
            self.menuSelected = 0
            self.menuList=[]
        else: print "No menu to clear"

    def AddMenuItem(self, item, event, payload=None):
        if self.windowFrame:
            if self.windowFrame.IsShown():
                print "Can't add events while menu on screen"
                return
        parsedItem=eg.ParseString(item)
        tempVal={"txt": parsedItem, "selected": False, "event": event, "payload": payload}
        if tempVal not in self.menuList: self.menuList.append(tempVal)

    def RestartTimer(self):
        try: self.timer.Cancel()
        except: pass
        self.timer=MyTimer(t = 7.0, plugin = self)

    def BuildMenu(self, menu):
        self.LevelStorage = menu
        self.ResetMultiLevel()
        self.currentLevel = 0
        self.menuList = self.IterateLevel(self.LevelStorage[0])
        self.menuLevels.append(self.menuList)
        self.DisplayMenu()

    def MoveMenuCursor(self, direction):
        self.RestartTimer()

        try: self.windowFrame
        except: return
        try:
            l = len(self.menuList)
            if l == 0 or self.menuSelected == l - 1: return True
            self.menuList[self.menuSelected]["selected"]=False
            if direction == 'UP': self.menuSelected-=1
            if direction == 'DOWN': self.menuSelected+=1
            self.menuList[self.menuSelected]["selected"]=True
            def DoIt():
                self.windowFrame.DrawWindow()
                self.windowFrame.UpdateWindow()
            wx.CallAfter(DoIt)
        except: pass

    def SendEvent(self, data):
        self.RestartTimer()
        kwargs = False
        Func = False

        suffix = data["event"].split('.')
        payload = data["payload"]

        if suffix[0] == 'LVL':
            self.UpLevel(payload)
            return False
        try:
            prefix = '.'.join(suffix[:3])
            suffix = '.'.join(suffix[3:])
            kwargs = dict(prefix=prefix,suffix=suffix)
            if payload is not None: kwargs['payload'] = payload
            Func = eg.TriggerEvent
        except:
            kwargs = dict(suffix='.'.join(suffix))
            if payload is not None: kwargs['payload'] = payload
            Func = self.TriggerEvent
        finally:
            Func(**kwargs)
            return True

    def ExecuteItem(self):
        if self.windowFrame:
            if self.SendEvent(self.menuList[self.menuSelected]):
                self.CloseMenu()
        else: print "Can't execute while menu not on screen"

    def OnClose(self):
        self.windowFrame.Show(False)

    def ResetMultiLevel(self):
        self.menuList = []
        self.menuLevels = []
        self.menuSelected = 0
        self.menuLevelsSelected = []
        self.currentLevel = 0
        self.CloseMenu()

    def DownLevel(self):
        self.RestartTimer()
        self.CloseMenu()
        if self.currentLevel == 0:
            self.ResetMultiLevel()
        else:
            self.menuLevels.pop(self.currentLevel)
            self.currentLevel -= 1
            self.menuList = self.menuLevels[self.currentLevel]
            self.menuSelected = self.menuLevelsSelected[-1:][0]
            self.menuLevelsSelected = self.menuLevelsSelected[:-1]
            self.DisplayMenu()

    def IterateLevel(self, ItemList):
        newLevel = []
        for item, event, payload in ItemList:
            item += '\t\t---->' if event == 'LVL' else ''
            newData = {"txt": item, "selected": False, "event": event, "payload": payload}
            newLevel.append(newData)
        return newLevel

    def UpLevel(self, lvl):
        self.RestartTimer()
        try:
            self.CloseMenu()
            self.menuLevelsSelected.append(self.menuSelected)
            self.menuSelected = 0
            self.currentLevel +=1
            self.menuList = self.IterateLevel(self.LevelStorage[lvl])
            self.menuLevels.append(self.menuList)
            self.DisplayMenu()
        except: print sys.exc_info()

    def DisplayMenu(self):
        self.RestartTimer()
        if self.windowFrame:
            self.menuList[self.menuSelected]["selected"] = True
        if not self.windowFrame:            
            def DoIt():
                display = wx.Display(self.monitor)
                x, y, w, h = display.GetGeometry()
                self.windowFrame=MenuDisplay(220, self.menuList, self.font, self.foreColor,
                self.backColor, self.selForeColor, self.borderColor, self.transparency, self.borderWidth)
                self.windowFrame.SetPosition((x, y))
                self.windowFrame.Center(wx.BOTH)
                self.windowFrame.FadeIn(self.fadeIn)
            wx.CallAfter(DoIt)
        else:
            if not self.windowFrame.IsShown():
                def DoIt():
                    self.windowFrame.FadeIn(self.plugin.fadeIn)
                    self.windowFrame.UpdateWindow()
                wx.CallAfter(DoIt)
            else:
                wx.CallAfter(self.windowFrame.UpdateWindow)


class MenuDisplay(LayeredWindow.LayeredWindow):
    def __init__(self, alpha, menuList, font, foreColor, backColor, selForeColor, borderColor, transparency, borderWidth):
        LayeredWindow.LayeredWindow.__init__(self, alpha)
        self.menuList=menuList
        self.font=font
        self.foreColor = foreColor
        self.backColor = backColor
        self.selForeColor = selForeColor
        self.borderColor = borderColor
        self.transparency = transparency
        self.borderWidth = borderWidth

        self.sizeX, self.sizeY = self.DetermineSize()
        self.SetSize(wx.Size(self.sizeX, self.sizeY))
        
    def DetermineSize(self):
        limX=0
        sizeY=0
        memoryDC = wx.MemoryDC()
        memoryDC.SetFont(self.font)
        for item in self.menuList:
            w, h = memoryDC.GetTextExtent(item["txt"])
            if w>limX: limX=w
            sizeY+=h
        sizeX=limX + 40
        sizeY+=+40
        return (sizeX,sizeY)

    def GetStep(self):
        memoryDC = wx.MemoryDC()
        memoryDC.SetFont(self.font)
        w, h = memoryDC.GetTextExtent(self.menuList[0]["txt"])
        return h

    def DrawWindow(self):
        tmpDC = wx.MemoryDC()
        self.bmp = wx.Bitmap(*self.GetClientSize())
        tmpDC.SelectObject(self.bmp)
        ## GetGCDC
        try:
            tmpDC = wx.GCDC(tmpDC)
        except:
            print "Can not get GCDC"    
        # Background
        tmpDC.SetBrush(wx.Brush(wx.Colour(self.backColor[0],self.backColor[1],self.backColor[2],self.transparency)))
        tmpDC.SetPen(wx.Pen(wx.Colour(self.borderColor[0],self.borderColor[1],self.borderColor[2]),self.borderWidth))
        tmpDC.DrawRoundedRectangle(0, 0, self.sizeX, self.sizeY, 4)

        # Menu items
        tmpDC.SetFont(self.font)
        posY=20
        step=self.GetStep()
        for item in self.menuList:
            if item["selected"] : tmpDC.SetTextForeground(self.selForeColor)
            else: tmpDC.SetTextForeground(self.foreColor)
            tmpDC.DrawText(item["txt"], 20, posY)
            posY+=step  

        tmpDC.Destroy()
        del tmpDC



class BuildMenu(eg.ActionBase):
    text = Text
    def __call__(self, menuData):
        self.plugin.BuildMenu(menuData)
        
class CloseMenu(eg.ActionBase):
    text = Text
    def __call__(self):
        self.plugin.ClearMenu()

class MenuForward(eg.ActionBase):
    text = Text
    def  __call__(self):
        self.plugin.SendEvent(
            self.plugin.menuList[self.plugin.menuSelected])

class MenuBack(eg.ActionBase):
    text = Text
    def  __call__(self):
        self.plugin.DownLevel()
        
class MenuDown(eg.ActionBase):
    text = Text
    def __call__(self):
        return self.plugin.MoveMenuCursor('DOWN')
        
class MenuUp(eg.ActionBase):
    text = Text
    def __call__(self):
        return self.plugin.MoveMenuCursor('UP')

class ExecuteItem(eg.ActionBase):
    text = Text    
    def __call__(self):
        self.plugin.ExecuteItem()

class DisplayMenu(eg.ActionBase):
    text = Text
    def __call__(self):
        self.plugin.DisplayMenu()

class AddItem(eg.ActionClass):
    text = Text
    def __call__(self, event, item):
        self.plugin.AddMenuItem(event, item)
        
    def Configure(self, event="", item=""):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.TextCtrl(item)
        st2 = panel.TextCtrl(event)
 
        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.ItemBox,
                            (text.ItemText, st1)
                            )
        box2 = panel.BoxedGroup(
                            text.EvtBox,
                            (text.EvtText,st2),
                            )
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND)
                            ])
        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class MyTimer():

    def __init__(self, t, plugin):
        self.timer = Timer(t, self.Run)
        self.plugin = plugin
        self.timer.start()


    def Run(self):
        try:
            self.plugin.CloseMenu()
        except:
            pass


    def Cancel(self):
        self.timer.cancel()
