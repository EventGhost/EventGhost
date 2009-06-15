import eg

eg.RegisterPlugin(
    name = "Y.A.R.D.",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
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
from win32com.client.CLSIDToClass import RegisterCLSID
from pythoncom import GetActiveObject, com_error
from threading import Timer
from wx.lib.intctrl import IntCtrl
from ctypes import FormatError

YARD_CLSID = '{9AFE3574-1FAF-437F-A8C5-270ED1C84B2E}'


    
class YARD(eg.PluginBase):

    def __init__(self):
        self.AddEvents()

        self.isEnabled = False
        self.mapTable = {}
        self.timer = Timer(0, self.OnTimeOut)
        self.lastEvent = ""
        self.timeout = 0.2
        self.disableUnmapped = False
        self.thread = None
        self.comObj = None
        self.buttons = [False] * 16
        self.AddAction(SendRemoteKey)
        self.AddAction(ClearScreen)
        self.AddAction(Print)
        
        class EventHandler:
            def __init__(self2):
                pass
                
            def OngetName(self2):
                return "EventGhost YARD Plugin"
            
            def OnShutdown(self2):
                try:
                    self.comObj.close()
                except:
                    raise eg.Exception("YARD server not found") 
                del self.comObj
                self.comObj = None
            
            def OnReceivedKey(self2, key):
                self.HandleEvent(key)
        self.EventHandler = EventHandler
        
        
        
    def __start__(self):
        try:
            GetActiveObject(YARD_CLSID)
        except com_error:
            self.StartYardServer()
        try:
            self.comObj = DispatchWithEvents(YARD_CLSID, self.EventHandler)
        except:
            raise eg.Exception("Can't connect to YARD server!") 
        self.isEnabled = True
    
    
    def __stop__(self):
        self.isEnabled = False
        if self.comObj:
            try:
                self.comObj.close()
            except:
                raise eg.Exception("YARD server not found") 
            del self.comObj
            self.comObj = None
    
    
    def OnTimeOut(self):
        self.EndLastEvent()
        self.lastEvent = ""
        
        
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

