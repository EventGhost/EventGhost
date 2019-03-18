# -*- coding: utf-8 -*-
version="0.0"

# Plugins/Digispark-LCD/__init__.py
#
# Copyright (C)  2017 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
# Copyright � 2005-2017 EventGhost Project <http://www.eventghost.net/>
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0 by Pako 2017-03-18 14:09 UTC+1
#       - initial version

import eg

eg.RegisterPlugin(
    name = "Digispark-LCD",
    author = "Pako",
    guid = "{CD4BCDDE-991E-4100-8EA0-0B4C2E6294DD}",
    version = version,
    kind = "external",
    canMultiLoad = False,
    description = ur'''<rst>
Alphanumeric LCD display connected to a PC using the Digispark.

**Basic features:**

| \u2022 Each line of the display is controlled separately.
| \u2022 If the text exceeds the length of the line, scrolling is automatically applied.
| \u2022 Maximum length of text (for one line) is 64 characters.
| \u2022 Non - ASCII characters are supported.
| \u2022 Due to the limitations of displays with controller HD44780, 
  you can not display more than 8 non - ASCII characters at a time.
| \u2022 If more characters is needed, some of the characters are replaced 
  with a similar ASCII character.
| \u2022 For easier management, patterns of custom characters are "burned" 
  into the EEPROM memory ATtiny85 (the main component of Digispark).
| \u2022 The maximum number of custom characters (located in EEPROM): 56.
| \u2022 A set of custom characters can be exported to a file, 
  making it easy to exchange them among users.
| \u2022 Undisplayable characters are replaced with \u25AF.

Plugin version: %s
''' % version,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeT"
        "AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QMPDzoDufPA/wAAAB1pVFh0Q29t"
        "bWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAABFUlEQVRYw2NgGAWjYBSMglEw"
        "CkbBSAeMDAwM/wfSAUwDHQIsMEbVbw66WtzG+mNwhMDgiQL04MEWJb++/mc4UPOH4ca6"
        "vww/3jMwSBgyMsQdZMfQy8jMwMAtxsCg6svM4NzFwsDGzUidENhb+ofh+9v/DEmn2Bmy"
        "77IziOtj117xnZ0h7hAbw7dX/xn2lv2hXhTcXP+XwaWXlYFHnJGBW5SRwX0SK/a8zcjI"
        "IKDAxOA+hZXh5rq/gzsNkOQAtQBmhj3Fvxm+vvrP8OnJf4ZdBb+xqvv//z/Dhwf/GHbm"
        "/GZQD2ImPREi51PkMsKlm4Vhf9UfhrkmPxm+v2NgEDfAnrg6OH8ycIkgEiFRRfFoQTRa"
        "Gw4UAADt2lGM0w991wAAAABJRU5ErkJggg=="
    ),
)

from base64 import b64decode
from codecs import open as codecs_open
from copy import deepcopy as cpy
from cStringIO import StringIO
from datetime import datetime as dt
from functools import partial
from json import dumps, loads
from os.path import splitext
from Queue import Queue
from threading import Timer
from time import sleep, time as ttime
from winsound import PlaySound, SND_ASYNC
from xml.dom import minidom as miniDom

import wx
from usb.core import find as usbfind

# https://github.com/follower/vusb-for-arduino/tree/master/examples/arduino
from arduino.usbdevice import ArduinoUsbDevice
from eg.WinApi.Dynamic import CreateEvent, SetEvent

#===============================================================================
COMMANDS = {
    "BacklightON":4,
    "BacklightOFF":5,
    "Clear":6,
    "Home":7,
    "DisplayON":8,
    "DisplayOFF":9,
    "Repeat":10,
    "InitCGRAM":11,
    "Burn":13,
    "Remap":14
}

SQUARE_0 = (
        "iVBORw0KGgoAAAANSUhEUgAAABoAAAAaCAYAAACpSkzOAAAACXBIWXMAAAsTAAALEwEA"
        "mpwYAAAAB3RJTUUH4QMICxQfPCsF+QAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3"
        "aXRoIEdJTVBkLmUHAAAAPklEQVRIx2Pct2/ffwY6ACYGOgEWGOO37QGaWMB62IG+Phq1"
        "aNSiUYtGLRq1aNSiUYtGLSKpFQRrrQx5HwEAa8AHeQ4FZ0QAAAAASUVORK5CYII="
)

SQUARE_1 = (
        "iVBORw0KGgoAAAANSUhEUgAAABoAAAAaCAYAAACpSkzOAAAACXBIWXMAAAsTAAALEwEA"
        "mpwYAAAAB3RJTUUH4QMICxQ2fpmdlQAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3"
        "aXRoIEdJTVBkLmUHAAAAPklEQVRIx2Pct2/ffwY6ACYGOgEWGMPJyYkmFuzbt4++Phq1"
        "aNSiUYtGLRq1aNSiUYtGLSKpFQRrrQx5HwEA8dsIqxMoIxIAAAAASUVORK5CYII="
)

SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ACV           = wx.ALIGN_CENTER_VERTICAL
EMPTY_CHAR = ["", "", [0, 0, 0, 0, 0, 0, 0, 0]]
MAX_CHAR = 56
STX = 2
ETX = 3
ENQ = 5 

class Text:
    connect = "Digispark-LCD: Device %ix%i connected"
    cust_chr = "Digispark-LCD: The number of custom characters: %i"
    ee_char =   "Digispark-LCD: The number of character patterns, burned in EEPROM: %i"
    cust_char = "Digispark-LCD: The number of created custom characters is different: %i"
    edit = "Digispark-LCD: Please make burning or edit custom characters."

    buttons = (
        'Delete',
        'Insert new',
        'Import set',
        'Export set',
    )
    choose = 'Choose a XML file to be import'
    save = 'Save set of custom  characters as XML file ...'
    wildcard = "XML file (*.xml)|*.xml"
    userCharList = "List:"
    userCharLabel = "Character:"
    replLabel = "Replacement char.:"
    cancel = 'Cancel'
    ok = 'OK'
    burn = "Burn to EEPROM"
    progress = "Burning progress"
    done = "Done !!!"
    wait = "Please wait a moment ..."
    auto = "Auto close after %i s"
    messBoxTit0 = "EventGhost - Digispark-LCD"
    messBoxTit1 = "Attention !"
    messBoxTit2 = "Burning failed !"
    messBoxTit4 = "No data !"
    messBoxTit7 = 'Invalid character !'
    messBoxTit8 = 'Invalid entry !'
    message1 = 'It is not possible to use more than %i custom characters!'
    message2 = "No display is connected."
    message3 ='No data to burn.'
    message4 ='Import failed - file "%s" does not contain data.'
    message5 = 'It is not possible to import selected file, because there is a problem.\n\
The file "%s" does not have the expected structure.'
    message7 = u'The character " %s " can not be used.\n\
The replacement character must be a plain ASCII.'
    message8 = u'The string " %s " can not be used.\n\
The replacement character must be the only one character.'
    xmlComment1 = "User character definition file."
    xmlComment2 = 'Saved at %s by EventGhost plugin "Digispark-LCD".'
#===============================================================================

def Move(lst, index, direction):
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
        index2 = index + direction
        tmpList[index] = lst[index2]
        tmpList[index2] = lst[index]
    return index2, tmpList
#===============================================================================

class MyListCtrl(wx.ListCtrl):
    currentItem = -1

    def __init__(
        self,
        parent,
        id,
        size,
        style
    ):
        wx.ListCtrl.__init__(
            self,
            parent,
            id,
            size = size,
            style = style 
        )
        self.InsertColumn(0, "")
        self.SetColumnWidth(0, 30)
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)


    def OnItemSelected(self, event):
        self.currentItem = event.GetSelection()
        event.Skip()


    def SetSelection(self, ix):
        self.SetItemState(ix, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.currentItem = ix


    def GetSelection(self):
        return self.currentItem      


    def SelRow(self, row):
        if row != self.currentItem:
            if self.currentItem in range(self.GetItemCount()):
                item = self.GetItem(self.currentItem)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
        self.SetSelection(row)
#===============================================================================

class ArdUsbDev(ArduinoUsbDevice):
    def __init__(self, idVendor, idProduct, deviceName = None):
        """
        """
        self.idVendor = idVendor
        self.idProduct = idProduct

        if deviceName is None:
            self.device = usbfind(idVendor = self.idVendor,
                                        idProduct = self.idProduct)
        else:
            def deviceName_match(dev):
                if hasattr(dev, "product"):
                    if dev.product == deviceName:
                        return True
                else:
                    from usb.util import get_string
                    product = get_string(dev, 64, dev.iProduct)
                    if product == deviceName:
                        return True
            self.device = usbfind(idVendor = self.idVendor,
                                        idProduct = self.idProduct,
                                        custom_match = deviceName_match)
        if not self.device:
            raise Exception("Device not found")
#===============================================================================

class ExtStaticBitmap(wx.StaticBitmap):
    value = 0

    def SetValue(self, val):
        self.value = val

    def GetValue(self):
        return self.value

    def SetBitmapExt(self, bm, val):
        self.SetBitmap(bm)
        self.SetValue(val)
#===============================================================================

class DigisparkThreadWorker(eg.ThreadWorker):
    run     = True
    plugin  = None
    lcd  = None
    message = ""
    lastMessage = ""
    starttime = 0
    free = True


    def Run(self):
        while self.run:
            if self.lcd is not None:
                if self.free:
                    item = self.queue.get()
                    event = item[1]
                    item = item[0]
                    test = self.flush()
                    if test != "No Data":
                        self.lcd = None
                        self.Init()
                    if item != "STOP":
                        self.free = False
                        self.udprint(*item)
                        if event is not None:
                            SetEvent(event)
                        self.free = True
                    else:
                        break
                else:
                    sleep(2.0)
            else:
                self.Init()


    def Setup(self, plugin, queue):
        self.plugin = plugin
        self.timeout = None
        self.suffs = None
        self.queue = queue
        tmr = Timer(0.1, self.Run)
        tmr.start()


    def Finish(self):
        self.run = False


    def flush(self):
        while True:
            try:
                self.lcd.read()
            except Exception as e:
                return e.message


    def GetConnected(self):
        if self.lcd is None:
            return False
        if self.free:
            self.free = False
            resp = True if self.flush() == "No Data" else False
            self.free = True
            return resp
        else:
            return "Busy"
        

    def Init(self):
        while self.run and self.lcd is None:
            try:
                self.lcd = ArdUsbDev(idVendor = 0x16c0, idProduct = 0x05df, deviceName = 'Digispark-LCD')
                self.lcd.write(ENQ)
                sleep(1.0)
                ch = None
                while True:
                    try:
                        ch = self.lcd.read()
                    except:
                        ch = None
                        break 
                    if ch == STX:
                        try:
                            ch = self.lcd.read()
                            rows = ch
                        except:
                            ch = None
                            break 
                        try:
                            ch = self.lcd.read()
                            cols = ch
                        except:
                            ch = None
                            break 
                        try:
                            ch = self.lcd.read()
                            user_chars = ch
                        except:
                            ch = None
                            break 
                        try:
                            ch = self.lcd.read()
                            if ch != ETX:
                                ch = None
                            break
                        except:
                            ch = None
                            break
                    else:
                        ch = None   
                if ch is None:
                    raise ValueError('Dummy error')
                else:
                    eg.PrintNotice(self.plugin.text.connect % (rows, cols))
                    self.plugin.eechars = user_chars if user_chars < 57 else 0
                    if len(self.plugin.userchars) != self.plugin.eechars:
                        eg.PrintNotice(self.plugin.text.ee_char % self.plugin.eechars)
                        eg.PrintNotice(self.plugin.text.cust_char  % len(self.plugin.userchars))
                        eg.PrintNotice(self.plugin.text.edit)
                    else:
                        eg.PrintNotice(self.plugin.text.cust_chr % self.plugin.eechars)
                    self.plugin.rows = rows
                    self.plugin.cols = cols
                    self.udprint(2, "Digispark-LCD")
                    self.udprint(COMMANDS["InitCGRAM"])
                    self.udprint(COMMANDS["Clear"])
                    self.plugin.InitCGRAM() # synchronization ...
            except:
                sleep(5.0)


    def udprint(self, cmd, data=None):
        now = ttime()
        self.lcd.write(STX)
        ch=None
        while ch != ord("B") and (ttime()-now) < 30:
           try:
               ch = self.lcd.read()
           except:
               ch = None
        if (ttime()-now) > 30:
            return False                
        self.lcd.write(cmd)
        if data is not None:
            self.lcd.write(len(data))
            for elem in data:
                ch = elem if isinstance(data, (list, tuple)) else ord(elem)
                self.lcd.write(ch)
        ch = None
        while ch != ord("F") and (ttime()-now) < 30:
           try:
               ch = self.lcd.read()
           except:
               ch = None
        if (ttime() - now) > 30:
            return False            
        return True
#===============================================================================

class Digispark_LCD(eg.PluginBase):
    text = Text
    suffText = None
    repldict = {}
    cols = None
    rows = None
    eechars = None
    content = ["", "", "", ""]
    reploverdict = {}

    oldSel = 0

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    def InitCGRAM(self):
        self.repldict = {}
        self.content = ["", "", "", ""]
        for i, item in enumerate(self.userchars):
            if i == 8:
                break
            self.repldict[item[0]] = i        


    def __start__(
        self,
        userchars = []   
        ):
        self.queue = Queue()
        self.userchars = userchars
        self.InitCGRAM()
        self.workerThread = DigisparkThreadWorker(self, self.queue)
        try:
            self.workerThread.Start(10)
        except:
            eg.PrintTraceback()


    def __stop__(self):
        self.queue.put(("STOP", None))
        self.queue.queue.clear()
        self.queue = None
        self.workerThread.Stop(10)


    def OnComputerSuspend(self, dummy):
        self.__stop__()


    def OnComputerResume(self, dummy):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        self.__start__(*args)


    def GetConnected(self):
        return self.workerThread.CallWait( partial( self.workerThread.GetConnected ), 10 )


    def ShortCommand(self, cmd):
        if self.workerThread:
            self.queue.put(((cmd,), None))
        if cmd == COMMANDS['Clear']:
            self.content = ["", "", "", ""]


    def PrintCommand(self, ln, txt = ""):
        limit = min(self.eechars, len(self.userchars))
        self.content[ln] = txt
        if txt  == "":
            if self.workerThread:
                self.queue.put(((ln, ""), None))
            return

        usercharlst = [j[0] for j in self.userchars][:limit]
        usedchars = []
        for i in range(4):
            content = self.content[i] if i == ln else self.content[i][:self.cols]
            for c in content:
                if c in usercharlst and not c in usedchars:
                    usedchars.append(c)                   
        #find missing chars:
        missing = list(set(usedchars)-set(self.repldict.iterkeys()))
        # if len(missing) > 0   remaping is need
        if missing:
            needless = list(set(self.repldict.iterkeys())-set(usedchars)) 
            # if len(needless) > 0 remap user chars
            remapcmd = []
            for k in range(min(len(missing), len(needless))):
                m = self.repldict[needless[k]]
                self.repldict[missing[k]] = m
                remapcmd.extend((usercharlst.index(missing[k]), m))
                del self.repldict[needless[k]]
            #if missing > needless, to use replacement char
            if len(missing) > len(needless):
                overdict = dict((p[0],p[1]) for p in self.userchars)
                missing = list(set(usedchars)-set(self.repldict.iterkeys()))
                self.reploverdict = {}
                for n in range(len(missing)):
                    miss = missing[n]
                    self.reploverdict[miss] = overdict[miss]
            if remapcmd:
                if self.workerThread:
                    self.queue.put(((COMMANDS["Remap"], remapcmd), None))
        for k, v in self.repldict.iteritems():
            txt = txt.replace(k, chr(v))
        for key, val in self.reploverdict.iteritems():
            txt = txt.replace(key, val)

        txt = [ord(ch) for ch in txt]
        for i, ch in enumerate(txt):
            if ch > 255:
                eg.PrintNotice(u"Digispark-LCD: UNICODE CHARACTER: %s, code U%i" % (unichr(ch), ch))
                txt[i] = 219
        if self.workerThread:
            self.queue.put(((ln, txt), None))


    def parseArgument(self, arg):
        if not arg:
            return 0
        if isinstance(arg, int):
            return arg
        else:
            return eg.ParseString(arg)


    def Configure(
        self,
        userchars = [] 
    ):
        panel = eg.ConfigPanel(self)
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        self.panel = panel
        self.data = cpy(userchars)
        if self.data == []:
            self.data = [cpy(EMPTY_CHAR)]
        text = self.text
        jpg_0 = b64decode(SQUARE_0)
        stream_0 = StringIO(jpg_0)
        jpg_1 = b64decode(SQUARE_1)
        stream_1 = StringIO(jpg_1)
        self.bitmaps = (
             wx.Bitmap(wx.Image(stream_0)),
             wx.Bitmap(wx.Image(stream_1))
        )
        self.ids={}


        def onClick(evt):
            id = evt.GetId()
            bm = wx.FindWindowById(id)
            oldVal = bm.GetValue()
            row, bit = self.ids[id]
            newVal = int(not oldVal)
            bm.SetBitmapExt(self.bitmaps[newVal], newVal)
            wx.CallAfter(validation, True)
            evt.Skip()


        patternSizer = wx.GridBagSizer(-2, -2)
        for r in range(8):
            for c in range(4, -1, -1):
                id = wx.NewIdRef()
                self.ids[id]=(r, c)
                bitmap = ExtStaticBitmap(panel, id, self.bitmaps[0], (26, 26))
                bitmap.SetValue(0)
                patternSizer.Add(bitmap,(r, 4-c))
                bitmap.Bind(wx.EVT_LEFT_DOWN, onClick)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)

        leftSizer = wx.GridBagSizer(1, 3)
        previewLbl = wx.StaticText(panel, -1, text.userCharList)
        charListCtrl = MyListCtrl(
            panel,
            -1,
            size = wx.Size(40, -1),
            style = wx.LC_SINGLE_SEL|wx.LC_NO_HEADER|wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES
        )
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(panel, -1, bmp)
        btnUP.Enable(False)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(panel, -1, bmp)
        btnDOWN.Enable(False)
        #Buttons 'Delete' and 'Insert new'
        lenLst = [panel.GetTextExtent(item)[0] for item in text.buttons]
        dummBttn = wx.Button(panel,-1,text.buttons[(lenLst).index(max(lenLst))])
        sz = dummBttn.GetSize()
        dummBttn.Destroy()
        btnDEL = wx.Button(panel, -1, text.buttons[0], size = sz)
        btnApp = wx.Button(panel, -1, text.buttons[1], size = sz)
        btnIMP = wx.Button(panel, -1, text.buttons[2], size = sz)
        btnEXP = wx.Button(panel, -1, text.buttons[3], size = sz)
        btnDEL.Enable(False)
        btnApp.Enable(False)
        labelLbl = wx.StaticText(panel, -1, text.userCharLabel)
        userCharLabelCtrl = wx.TextCtrl(
            panel,
            -1,
            '',
            size = wx.Size(40, -1),
        )
        leftSizer.Add(previewLbl, (0, 0), flag = wx.TOP, border = -2)
        leftSizer.Add(charListCtrl, (1, 0), (6, 1), flag = wx.TOP|wx.EXPAND)
        leftSizer.Add(btnUP, (1, 1))
        leftSizer.Add(btnDOWN, (2, 1), flag = wx.TOP, border = 2)
        leftSizer.Add(btnDEL, (3, 1), flag = wx.TOP, border = 2)
        leftSizer.AddGrowableRow(4, 1)
        leftSizer.Add((-1, 20), (4, 1), flag = wx.EXPAND)
        leftSizer.Add(btnIMP, (5, 1), flag = wx.BOTTOM, border = 2)
        leftSizer.Add(btnEXP, (6, 1))
        leftSizer.Add(labelLbl, (7, 0), flag = wx.TOP, border = 6)
        leftSizer.Add(userCharLabelCtrl, (8, 0), flag = wx.EXPAND)
        leftSizer.Add(btnApp, (8, 1), flag = ACV)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(leftSizer, 1, wx.EXPAND)
        topSizer.Add((-1, -1), 0, wx.LEFT|wx.RIGHT|wx.EXPAND,10)
        topSizer.Add(rightSizer,0,wx.ALIGN_RIGHT)

        replLbl = wx.StaticText(panel, -1, text.replLabel)
        replCtrl = wx.TextCtrl(
            panel,
            -1,
            '',
            size = wx.Size(24, -1),
        )
        font = wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD)
        replCtrl.SetFont(font)
        userCharLabelCtrl.SetFont(font)
        charListCtrl.SetFont(font)

        replSizer = wx.BoxSizer(wx.HORIZONTAL)
        replSizer.Add(replLbl, 0, ACV)
        replSizer.Add((-1, -1), 1, wx.EXPAND)
        replSizer.Add(replCtrl,0,wx.ALIGN_RIGHT)
        rightSizer.Add(patternSizer, 0, wx.ALIGN_RIGHT)
        rightSizer.Add(replSizer, 0, wx.TOP|wx.ALIGN_LEFT|wx.EXPAND, 5)
        btn0 = wx.Button(panel.dialog, -1, text.burn)
        panel.sizer.Add(topSizer,1,wx.EXPAND|wx.ALL,5)


        def GetPattern():
            val = [0, 0, 0, 0, 0, 0, 0, 0]
            for id in self.ids:
                bm = wx.FindWindowById(id)
                row, bit = self.ids[id]
                val[row] += bm.GetValue()*2**bit
            return val 


        def SetPattern(pttrn):
            for id in self.ids:
                bm = wx.FindWindowById(id)
                row, bit = self.ids[id]
                val = int(pttrn[row] & 2**bit > 0)
                bm.SetBitmapExt(self.bitmaps[val], val)


        def ResetPattern():
            SetPattern([0, 0, 0, 0, 0, 0, 0, 0])


        def FillData(item):
            userCharLabelCtrl.ChangeValue(item[0])
            replCtrl.ChangeValue(item[1])
            SetPattern(item[2])


        def Fill_ListCtrl():
            charListCtrl.DeleteAllItems()
            for i, chr in enumerate(self.data):
                charListCtrl.InsertItem(i, chr[0])   


        def SelRow(row):
            charListCtrl.SelRow(row)
            self.oldSel = row


        def Init_panel():
            FillData(self.data[0])
            Fill_ListCtrl()
            SelRow(0)
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
            btnApp.Enable(True)

        if len(self.data):
            Init_panel()


        def validation(patt = False):
            flag = True
            label = userCharLabelCtrl.GetValue()
            if len(label) != 1:
                flag = False
            else:
                if len([i[0] for i in self.data if i[0] == label]) != 1:
                    flag = False
            repl = replCtrl.GetValue()
            if len(repl) != 1 or len(repr(repl)) > 4:
                flag = False
            pttrn = GetPattern()
            if pttrn == [0, 0, 0, 0, 0, 0, 0, 0]:
                flag = False
            elif patt:
                self.data[self.oldSel][2] = pttrn
            self.panel.dialog.buttonRow.okButton.Enable(flag)
            btnApp.Enable(flag)


        def OnLabelText(evt):
            strng = userCharLabelCtrl.GetValue()
            ix = charListCtrl.GetSelection()
            if ix == -1:
                if charListCtrl.GetItemCount() == 0:
                    charListCtrl.InsertItem(wx.ListItem())
                    ix = 0
                    SelRow(0)
            self.data[ix][0] = strng
            charListCtrl.SetItem(ix, 0, strng)
            validation()
            evt.Skip()
        userCharLabelCtrl.Bind(wx.EVT_TEXT, OnLabelText)       


        def OnReplCtrl(evt):
            ix = charListCtrl.GetSelection()
            oldVal = self.data[ix][1]
            repl = replCtrl.GetValue()
            if len(repl) > 1:
                MessageBox(
                    self.panel,
                    text.message8 % (repl),
                    text.messBoxTit8,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    )
                replCtrl.ChangeValue(oldVal)
                evt.Skip()
                return
            elif len(repr(repl)) > 4:
                MessageBox(
                    self.panel,
                    text.message7 % (repl),
                    text.messBoxTit7,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    )
                replCtrl.ChangeValue(oldVal)
                evt.Skip()
                return
            if ix == -1:
                if charListCtrl.GetItemCount() == 0:
                    charListCtrl.InsertItem(wx.ListItem())
                    ix = 0
                    SelRow(0)
            self.data[ix][1] = repl
            validation()
            evt.Skip()
        replCtrl.Bind(wx.EVT_TEXT, OnReplCtrl)       


        def OnCharSelect(evt):
            row = evt.GetIndex()
            charListCtrl.SetItemState(row, 0, wx.LIST_STATE_SELECTED)
            if row == self.oldSel:
                evt.Skip()            
                return                
            SelRow(row)
            userCharLabelCtrl.ChangeValue(charListCtrl.GetItem(row, 1).GetText())
            evt.Skip()            
        charListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, OnCharSelect)        
        

        def OnButtonAppend(evt):
            if len(self.data)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            elif len(self.data)==MAX_CHAR:
                MessageBox(
                    self.panel,
                    text.message1 % MAX_CHAR,
                    text.messBoxTit1,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    time = 10
                    )
                evt.Skip()
                return                
            replCtrl.ChangeValue("")
            sel = charListCtrl.GetSelection() + 1
            self.data.insert(sel, cpy(EMPTY_CHAR))
            charListCtrl.InsertItem(sel, "")
            SelRow(sel)
            charListCtrl.EnsureVisible(sel)
            ResetPattern()
            userCharLabelCtrl.ChangeValue("")
            userCharLabelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            self.panel.dialog.buttonRow.okButton.Enable(False)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)


        def OnButtonDel(evt):
            sel = charListCtrl.GetSelection()
            charListCtrl.DeleteItem(sel)
            self.data.pop(sel)
            lngth = len(self.data)
            if lngth > 0:
                if sel == lngth:
                    sel = lngth - 1
                charListCtrl.SetSelection(sel)
            else:
                userCharLabelCtrl.ChangeValue("")
                self.data = [cpy(EMPTY_CHAR)]
                sel = 0
                charListCtrl.InsertItem(0, "")
                btnDEL.Enable(False)
            FillData(self.data[sel])
            SelRow(sel)
            charListCtrl.EnsureVisible(sel)
            userCharLabelCtrl.SetFocus()
            validation()
            if len(self.data) == 1:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, OnButtonDel)


        def onButtonUp(evt):
            newSel, self.data = Move(self.data, self.oldSel, -1)
            Fill_ListCtrl()
            SelRow(newSel)
            charListCtrl.EnsureVisible(newSel)
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)


        def onButtonDown(evt):
            newSel, self.data = Move(self.data, self.oldSel, 1)
            Fill_ListCtrl()
            SelRow(newSel)
            charListCtrl.EnsureVisible(newSel)
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)


        def OnBtnEXP(evt):
            ix = charListCtrl.GetSelection()
            dlg = wx.FileDialog(
                panel,
                message = text.save,
                defaultDir = eg.configDir, 
                defaultFile = "Digispark-LCD.xml",
                wildcard = text.wildcard,
                style=wx.FD_SAVE
                )
            if dlg.ShowModal() == wx.ID_OK:
                self.dataToXml(self.data, dlg.GetPath(), splitext(dlg.GetFilename())[0])
            dlg.Destroy()
            evt.Skip()
        btnEXP.Bind(wx.EVT_BUTTON, OnBtnEXP)


        def OnBtnIMP(evt):
            dlg = wx.FileDialog(
                panel,
                message = text.choose,
                defaultDir = eg.configDir, 
                defaultFile = "",
                wildcard = text.wildcard,
                style = wx.FD_OPEN | wx.FD_CHANGE_DIR
                )
            if dlg.ShowModal() == wx.ID_OK:
                filePath = dlg.GetPath()
                newdata = self.xmlToData(filePath)
                dlg.Destroy()
            else:
                dlg.Destroy()
                evt.Skip()
                return
            if not newdata:
                MessageBox(
                    self.panel,
                    text.message5 % path.split(dlg.GetPath())[1],
                    text.messBoxTit1,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    )
                evt.Skip()
                return
            if len(newdata):
                self.data = newdata
                Init_panel()
            else:
                MessageBox(
                    self.panel,
                    text.message4 % path.split(dlg.GetPath())[1],
                    text.messBoxTit4,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    )

            evt.Skip()
        btnIMP.Bind(wx.EVT_BUTTON, OnBtnIMP)


        def OnCharSelect(evt):
            row = evt.GetIndex()
            item = self.data[row]
            FillData(item)
            SelRow(row)
            validation()
            evt.Skip()            
        charListCtrl.Bind(wx.EVT_LIST_ITEM_FOCUSED, OnCharSelect)


        def onBurn(evt): 
            if self.data == [cpy(EMPTY_CHAR)]:
                MessageBox(
                    self.panel,
                    text.message3,
                    text.messBoxTit4,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    time = 10
                    )
                return

            if not self.GetConnected():
                MessageBox(
                    self.panel,
                    text.message2,
                    text.messBoxTit2,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    time = 10
                    )
                return

            max = 1 + len(self.data)
            dlg = wx.ProgressDialog(self.text.progress,
                                   self.text.wait,
                                   maximum = max,
                                   parent = self.panel,
                                   style = wx.PD_CAN_ABORT
                                    | wx.PD_APP_MODAL
                                    )
            dlg.SetIcon(self.info.icon.GetWxIcon())

            keepGoing = True
            count = 0
            for i, ch in enumerate(self.data):
                event = CreateEvent(None, 0, 0, None)
                item = list(ch[2])
                item.append(i)
                item.append(ord(ch[1]))
                self.queue.put(((COMMANDS["Burn"], item), event))
                eg.actionThread.WaitOnEvent(event)
                count += 1
                (keepGoing, skip) = dlg.Update(count)
            self.queue.put(((COMMANDS["Burn"], (len(self.data),)), event))
            count += 1
            eg.actionThread.WaitOnEvent(event)
            (keepGoing, skip) = dlg.Update(count, self.text.done)
            self.eechars = len(self.data)

        btn0.Bind(wx.EVT_BUTTON, onBurn)
        panel.dialog.buttonRow.Add(btn0)

        while panel.Affirmed():
            if self.data == [cpy(EMPTY_CHAR)]:
                self.data = []
            panel.SetResult(
                self.data,
            )


    def dataToXml(self, data, xmlpath, filename):
        impl = miniDom.getDOMImplementation()
        dom = impl.createDocument(None, u'Set', None)
        root = dom.documentElement
        commentNode1 = dom.createComment(self.text.xmlComment1)
        dom.insertBefore(commentNode1, root)
        commentNode2 = dom.createComment(self.text.xmlComment2 % str(dt.now())[:19])
        dom.insertBefore(commentNode2, root)
        root.setAttribute(u'Name', unicode(filename))
        charactersNode = dom.createElement(u'Characters')
        for item in data:
            characterNode = dom.createElement(u'Character')
            charNode = dom.createElement(u'User_character')
            charText = dom.createTextNode(unicode(item[0]))
            charNode.appendChild(charText)
            characterNode.appendChild(charNode)
            replNode = dom.createElement(u'Replacement_character')
            replText = dom.createTextNode(unicode(item[1]))
            replNode.appendChild(replText)
            characterNode.appendChild(replNode)
            patternNode = dom.createElement(u'Character_pattern')
            patternText = dom.createTextNode(dumps(item[2]))
            patternNode.appendChild(patternText)
            characterNode.appendChild(patternNode)
            charactersNode.appendChild(characterNode)
        root.appendChild(charactersNode)
        with codecs_open(xmlpath, "w", "utf-8") as out:
            dom.writexml(out)


    def xmlToData(self, xmlfile):
        xmldoc = miniDom.parse(xmlfile)
        document = xmldoc.getElementsByTagName('Set')
        if len(document) == 0:
            return None
        charset = document[0]
        characters = charset.getElementsByTagName('Characters')
        if len(characters) == 0:
            return None
        chars = characters[0].getElementsByTagName('Character')
        if len(chars) == 0:
            return None
        data = []
        for character in chars:
            dataItem = []
            chr = character.getElementsByTagName('User_character')
            if len(chr) == 0:
                return None
            dataItem.append(chr[0].firstChild.data)
            repl = character.getElementsByTagName('Replacement_character')
            if len(repl) == 0:
                return None
            dataItem.append(repl[0].firstChild.data)
            pattern = character.getElementsByTagName('Character_pattern')
            if len(pattern) == 0:
                return None
            dataItem.append(loads(pattern[0].firstChild.data))
            data.append(dataItem)
        return data
#===============================================================================

class MessageBox(wx.Dialog):

    def __init__(self, parent, message, caption='', flags=0, time = 0, plugin = None):
        PlaySound('SystemExclamation', SND_ASYNC)
        wx.Dialog.__init__(self, parent, style = wx.DEFAULT_DIALOG_STYLE )
        self.SetTitle(plugin.text.messBoxTit0)
        self.SetIcon(plugin.info.icon.GetWxIcon())
        if flags:
            art = None
            if flags & wx.ICON_EXCLAMATION:
                art = wx.ART_WARNING            
            elif flags & wx.ICON_ERROR:
                art = wx.ART_ERROR
            elif flags & wx.ICON_QUESTION:
                art = wx.ART_QUESTION
            elif flags & wx.ICON_INFORMATION:
                art = wx.ART_INFORMATION
            if art is not None:
                bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MESSAGE_BOX, (32, 32))
                icon = wx.StaticBitmap(self, -1, bmp)
                icon2 = wx.StaticBitmap(self, -1, bmp)
            else:
                icon = (32, 32)
                icon2 = (32, 32)
        if caption:
            caption = wx.StaticText(self, -1, caption)
            caption.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        message = wx.StaticText(self, -1, message)
        line = wx.StaticLine(self, -1, size = (1,-1), style = wx.LI_HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add((10, 1)) 

        if time:
            self.cnt = time
            txt = plugin.text.auto % self.cnt
            info = wx.StaticText(self, -1, txt)
            info.Enable(False)
            bottomSizer.Add(info, 0, wx.TOP, 3)
            
            def UpdateInfoLabel(evt):
                self.cnt -= 1
                txt = plugin.text.auto % self.cnt
                info.SetLabel(txt)
                if not self.cnt:
                    self.Close()

            self.Bind(wx.EVT_TIMER, UpdateInfoLabel)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
        else:
            self.timer = None

        button = wx.Button(self, -1, plugin.text.ok)
        button.SetDefault()
        bottomSizer.Add((1,1),1,wx.EXPAND) 
        bottomSizer.Add(button, 0, wx.RIGHT, 10)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(icon,0,wx.LEFT|wx.RIGHT,10)
        topSizer.Add((1,1),1,wx.EXPAND)
        topSizer.Add(caption,0,wx.TOP,5)
        topSizer.Add((1,1),1,wx.EXPAND)
        topSizer.Add(icon2,0,wx.LEFT|wx.RIGHT,10)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM,10)
        mainSizer.Add(message, 0, wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALL,5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND|wx.BOTTOM,5)
        
        def OnButton(evt):
            self.Close()
            evt.Skip()
        button.Bind(wx.EVT_BUTTON, OnButton)

        def onClose(evt):
            if self.timer:
                self.timer.Stop()
                del self.timer
            self.MakeModal(False)
            self.GetParent().Raise()
            self.Destroy()

        self.Bind(wx.EVT_CLOSE, onClose)
        self.SetSizer(mainSizer)
        self.Fit()
        self.MakeModal(True)
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

#===============================================================================

class ShortCommand(eg.ActionBase):

    def __call__(self):
        self.plugin.ShortCommand(COMMANDS[self.value])
#===============================================================================

class PrintCommand(eg.ActionBase):

    class text:
        line = "Line:"
        txt = "Text:"

    def __call__(self, line = 1, txt = ""):
        line = self.plugin.parseArgument(line) -1
        txt = eg.ParseString(txt)
        if line < self.plugin.rows:
            return self.plugin.PrintCommand(line, txt[:64])
        else:
            eg.PrintError("XXXXXXXXXXXXXXXXXXX BAD LINE XXXXXXXXXXXXXXXXXXXXXXXXXX")


    def GetLabel(self, line, txt):
        return "%s: %s: %s" % (self.name, line, txt)
        

    def Configure(self, line=1, txt=""):
        text = self.text
        panel = eg.ConfigPanel(self) 
        lnLabel = wx.StaticText(panel, -1, self.text.line)
        lnCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            line,
            min = 1,
            max = 4
        ) 
        txtLabel = wx.StaticText(panel, -1, self.text.txt)
        txtCtrl = wx.TextCtrl(panel, -1, txt)
        sizer = wx.FlexGridSizer(2, 2, 10, 9)
        sizer.AddGrowableCol(1)
        sizer.Add(lnLabel, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(lnCtrl)
        sizer.Add(txtLabel, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(txtCtrl, 1, wx.EXPAND)
        panel.sizer.Add(sizer, 1, wx.ALL|wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                lnCtrl.GetValue(),
                txtCtrl.GetValue()
            )
#===============================================================================

class ClearLine(eg.ActionBase):

    class text:
        line = "Line:"

    def __call__(self, line = 1):
        line = self.plugin.parseArgument(line) -1
        if line < self.plugin.rows:
            return self.plugin.PrintCommand(line)
        else:
            eg.PrintError("XXXXXXXXXXXXXXXXXXX BAD LINE XXXXXXXXXXXXXXXXXXXXXXXXXX")


    def GetLabel(self, line):
        return "%s: %s" % (self.name, line)
        

    def Configure(self, line = 1):
        text = self.text
        panel = eg.ConfigPanel(self) 
        lnLabel = wx.StaticText(panel, -1, self.text.line)
        lnCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            line,
            min = 1,
            max = 4
        ) 
        sizer = wx.FlexGridSizer(2, 2, 10, 9)
        sizer.AddGrowableCol(1)
        sizer.Add(lnLabel, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(lnCtrl)
        panel.sizer.Add(sizer, 1, wx.ALL|wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                lnCtrl.GetValue(),
            )
#===============================================================================    

ACTIONS = (
    (
        ShortCommand,
        'BacklightON',
        'Turn backlight ON',
        "Turn backlight ON.",
        'BacklightON'
    ),
    (
        ShortCommand,
        'BacklightOFF',
        'Turn backlight OFF',
        "Turn backlight OFF.",
        'BacklightOFF'
    ),
    (
        ShortCommand,
        'DisplayON',
        'Show text',
        "Show text.",
        'DisplayON'
    ),
    (
        ShortCommand,
        'DisplayOFF',
        'Hide text',
        "Hides text.",
        'DisplayOFF'
    ),
    (
        ShortCommand,
        'Clear',
        'Clear the entire display',
        "Clears the entire display.",
        'Clear'
    ),
    (
        PrintCommand,
        'PrintOnTheLine',
        'Print on the line',
        'Prints on the line.',
        None
    ),
    (
        ClearLine,
        'ClearLine',
        'Clear the line',
        'Clears the line.',
        None
    ),
)
