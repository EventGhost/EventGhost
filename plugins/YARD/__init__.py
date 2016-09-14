# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#                       André Weber <WeberAndre@gmx.de>
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

import eg

eg.RegisterPlugin(
    name = "Y.A.R.D.",
    author = (
        u"André Weber",
        "Bitmonster",
    ),
    version = "1.1.0",
    kind = "remote",
    guid = "{1119068D-44AD-40E0-BDB6-B00D9F88F5A0}",
    description = (
        'Hardware plugin for the <a href="http://eldo.gotdns.com/yard/">'
        'Y.A.R.D.</a> IR-transceiver from Andre Weber.'
        '\n\n<p>'
        '<a href="http://eldo.gotdns.com/yard/">'
        '<img src="logo.png" alt="Y.A.R.D." /></a>'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAfklEQVR42rWTCQrAMAgE"
        "4/8fbYnV4rG22FIJSYjsuLloDYOlrUXStPsCoS5pQa6IF+55AGRhDgOZ0MFUzIwMKf3M"
        "JaG5cADJUBXrOnJBwXqGAKjffwV40aWIjp4BTeX/APAKGwA8xCkAXmOBNKefq+t62v7b"
        "pzyJ2880Ee/xAO1+Z/119F9AAAAAAElFTkSuQmCC"
    ),
)

import wx
import os

from win32api import RegOpenKeyEx, RegQueryValueEx
from win32con import CREATE_NEW_CONSOLE, HKEY_CURRENT_USER
from win32process import CreateProcess, STARTUPINFO
from win32event import WaitForInputIdle
from win32com.client import DispatchWithEvents, Dispatch
from pythoncom import GetActiveObject, com_error
from threading import Timer
from ctypes import FormatError

YARD_CLSID = '{9AFE3574-1FAF-437F-A8C5-270ED1C84B2E}'
TERMINATE_TIMEOUT = 120

class EventHandler:

    def OngetName(self):
        return "EventGhost YARD Plugin"


    def OnShutdown(self):
        eg.PrintNotice("Y.A.R.D.-Server shutdown")
        try:
           self.plugin.workerThread.comobj_yard.close()
        except:
           raise eg.Exception("YARD server not found")
        del self.plugin.workerThread.comobj_yard
        del self.plugin.comObj
        self.plugin.workerThread.comobj_yard = None
        self.plugin.comObj = None


    def OnReceivedKeyEx(self, keyhex, keymapped, keytype, keyevent):
        self.plugin.HandleEventEx(keyhex, keymapped, keytype, keyevent)


    def OnReceivedKey(self, key):
        self.plugin.HandleEvent(key)



class YardWorkerThread(eg.ThreadWorker):
    """
    Handles the COM interface in a thread of its own
    """
    comobj_yard = None
    plugin = None
    eventHandler = None

    @eg.LogItWithReturn
    def Setup(self, plugin, eventHandler):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin
        self.eventHandler = eventHandler
        self.comobj_yard = DispatchWithEvents(YARD_CLSID, self.eventHandler)


    @eg.LogIt
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        if self.comobj_yard:
           self.comobj_yard.close()
           del self.comobj_yard



class YARD(eg.PluginBase):

    def __init__(self):
        self.AddEvents()
        self.isEnabled = False
        self.mapTable = {}
        self.timer = Timer(0, self.OnTimeOut)
        self.lastEvent = ""
        self.timeout = 0.2
        self.remote_control_timeout = 0.4
        self.disableUnmapped = False
        self.thread = None
        self.comObj = None
        self.workerThread = None
        self.buttons = [False] * 16
        self.AddAction(SendRemoteKey)
        self.AddAction(ClearScreen)
        self.AddAction(Print)


    def __start__(self):
        try:
            self.comObj = GetActiveObject(YARD_CLSID)
        except com_error:
            self.StartYardServer()
            try:
                self.comObj = GetActiveObject(YARD_CLSID)
            except:
                raise
            if self.comObj:
                self.comObj = Dispatch(YARD_CLSID)

        class SubEventHandler(EventHandler):
            plugin = self
            TriggerEvent = self.TriggerEvent

        self.workerThread = YardWorkerThread(self, SubEventHandler)
        try:
            self.workerThread.Start( 60.0 )
        except:
            self.workerThread = None
            raise self.Exception( self.text.errorMesg )

        self.isEnabled = True


    def __stop__(self):
        self.isEnabled = False

        if self.workerThread is not None :
           if self.workerThread.Stop( TERMINATE_TIMEOUT ) :
              eg.PrintError("Could not terminate YARD thread")
           self.workerThread = None

        if self.comObj:
           del self.comObj
           self.comObj = None


    def OnTimeOut(self):
        self.EndLastEvent()
        self.lastEvent = ""


    def HandleEventEx(self, keyhex, keymapped, keytype, keyevent):
        if not self.isEnabled:
            return
        # keytype
        #  0 = remote control
        #  1 = rotary encoder
        #  2 = keypad from keylcd
        # keyevent
        #  0 - a key (without up down detection)
        #  1 - key down event
        #  2 - key repeat event
        #  3 - key up event
        # keymapped - Yard Mapped keyname (symbolic one)
        # keyhex - native hex code of the key (just info?)

        if keytype == 0:
            if keyevent == 0:
                # 0 up down detection in yards disabled
                if self.timer:
                    self.timer.cancel()
                self.TriggerEnduringEvent(keymapped)
                self.timer = Timer(self.remote_control_timeout, self.OnTimeOut)
                self.timer.start()
            elif keyevent == 1:
                # Yard Received a new key down...
                self.TriggerEnduringEvent(keymapped)
            elif keyevent == 2:
                # Yard Received a repeated key...
                if self.timer:
                    self.timer.cancel()
                self.timer = Timer(self.remote_control_timeout, self.OnTimeOut)
                self.timer.start()
            elif keyevent == 3:
                # Yard detected a keyup...
                if self.timer:
                    self.timer.cancel()
                    self.timer = None
                self.EndLastEvent()
        elif keytype == 1:
            self.TriggerEvent(keymapped)
        elif keytype == 2:
            # key pad keylcd
            if keyevent == 1:
                self.TriggerEvent(keymapped+".down")
            elif keyevent == 2:
                # +".repeat"
                self.TriggerEvent(keymapped)
            elif keyevent == 3:
                self.TriggerEvent(keymapped+".up")


    def HandleEvent(self, eventString):
        if not self.isEnabled:
            return
        if eventString[:2] == "07":
            if eventString[6:8] == "01":
                i = int(eventString[10:12])
                self.buttons[i] = True
                buttons = [
                    "Button%i" % i
                    for i, btn in enumerate(self.buttons) if btn
                ]
                self.TriggerEvent("+".join(buttons))
            elif eventString[6:8] == "03":
                i = int(eventString[10:12])
                self.buttons[i] = False
                self.EndLastEvent()
            elif eventString == "070000001080FF":
                buttons = [
                    "Button%i" % i
                    for i, btn in enumerate(self.buttons) if btn
                ]
                buttons.append("JogLeft")
                self.TriggerEvent("+".join(buttons))
            elif eventString == "070000001081FF":
                buttons = [
                    "Button%i" % i
                    for i, btn in enumerate(self.buttons) if btn
                ]
                buttons.append("JogRight")
                self.TriggerEvent("+".join(buttons))
            else:
                self.TriggerEvent(eventString)
            return
        if eventString in self.mapTable:
            eventString, timeout = self.mapTable[eventString]
        else:
            if self.disableUnmapped:
                return
            timeout = self.timeout
        self.timer.cancel()
        if self.lastEvent != eventString:
            self.TriggerEnduringEvent(eventString)
            self.lastEvent = eventString
        self.timer = Timer(timeout, self.OnTimeOut)
        self.timer.start()


    def Map(self, what, to, timeout=None):
        self.mapTable[what] = (to, timeout or self.timeout)


    def StartYardServer(self):
        try:
            rkey = RegOpenKeyEx(HKEY_CURRENT_USER, "Software\\Webers\\Y.A.R.D")
            path = RegQueryValueEx(rkey, "program")[0]
            if not os.path.exists(path):
                raise Exception
        except:
            raise self.Exception(
                "Please start Yards.exe first and configure it."
            )
        try:
            hProcess = CreateProcess(
                None,
                path,
                None,
                None,
                0,
                CREATE_NEW_CONSOLE,
                None,
                None,
                STARTUPINFO()
            )[0]
        except Exception, exc:
            raise eg.Exception(FormatError(exc[0]))
        WaitForInputIdle(hProcess, 10000)



class SendRemoteKey(eg.ActionBase):
    name = "Sende IR"
    description = (
        "Mit dieser Funktion werden IR-Befehle gesendet, die im YARD-Server "
        "konfiguriert wurden."
    )
    remoteName = None
    keyName = None
    numRepeats = None

    def __call__(self, remoteName, keyName, numRepeats):
        if self.plugin.comObj is None:
            raise eg.Exception("YARD-Error: No connection")
        try:
            self.plugin.comObj.SendRemoteKey(remoteName, keyName, numRepeats)
        except com_error, err:
            raise eg.Exception("YARD-Error: " + err[1])


    def GetLabel(self, remoteName, keyName, numRepeats):
        return "YARD: Sende " + remoteName + ", " + keyName


    def Configure(self, remoteName=None, keyName=None, numRepeats=None):
        panel = eg.ConfigPanel()

        remoteName = remoteName or self.remoteName or ""
        keyName = keyName or self.keyName or ""
        numRepeats = numRepeats or self.numRepeats or 1

        mySizer = wx.FlexGridSizer(3, 2, 5, 5)

        st1 = wx.StaticText(panel, -1, "Fernbedienung")
        mySizer.Add(st1, 0, wx.ALIGN_CENTER_VERTICAL)

        rchoices = []
        kchoices = []
        foundRemoteIndex = 0
        comObj = None
        try:
            comObj = Dispatch(YARD_CLSID)
        except:
            pass
        else:
            remotes = comObj.GetRemotes()
            for i in xrange(len(remotes)):
                rName = remotes.Item(i).Name
                rchoices.append(rName)
                if rName == remoteName:
                    foundRemoteIndex = i

        remoteCtrl = wx.Choice(panel, -1, choices=rchoices)#, size=(150,-1))
        mySizer.Add(remoteCtrl, 1, wx.EXPAND)

        st2 = wx.StaticText(panel, -1, "Name der Taste")
        mySizer.Add(st2, 0, wx.ALIGN_CENTER_VERTICAL)

        keyCtrl = wx.Choice(panel, -1, choices=kchoices)#, size=(150,-1))
        mySizer.Add(keyCtrl, 1, wx.EXPAND)

        def UpdateKeys(event=None):
            foundKeyIndex = 0
            remoteIndex = remoteCtrl.GetSelection()
            remote = remotes.Item(remoteIndex)
            keyCtrl.Clear()
            for i in xrange(remote.count):
                key = remote.Keys(i).Name
                keyCtrl.Append(key)
                if key == keyName:
                    foundKeyIndex = i
            keyCtrl.Select(foundKeyIndex)

        remoteCtrl.Bind(wx.EVT_CHOICE, UpdateKeys)
        remoteCtrl.Select(foundRemoteIndex)
        if comObj:
            UpdateKeys()

        st3 = wx.StaticText(panel, -1, "Anzahl der Wiederholungen")
        mySizer.Add(st3, 0, wx.ALIGN_CENTER_VERTICAL)

        numRepeatsCtrl = eg.SpinIntCtrl(panel, value=numRepeats,  min=1)
        mySizer.Add(numRepeatsCtrl)

        panel.sizer.Add(mySizer, 1, wx.EXPAND)

        while panel.Affirmed():
            self.remoteName = remoteCtrl.GetStringSelection()
            self.keyName = keyCtrl.GetStringSelection()
            self.numRepeats = numRepeatsCtrl.GetValue()
            panel.SetResult(self.remoteName, self.keyName, self.numRepeats)



class ClearScreen(eg.ActionBase):

    def __call__(self):
        lcd = self.plugin.comObj.GetLcd(0)
        lcd.ClrScr()



class Print(eg.ActionWithStringParameter):

    def __call__(self, theString):
        lcd = self.plugin.comObj.GetLcd(0)
        lcd.Print(eg.ParseString(theString))

