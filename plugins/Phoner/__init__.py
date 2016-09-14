# -*- coding: utf-8 -*-
#
# /plugins/Phoner/__init__.py
#
# Copyright (C)  2009 Pako  <lubos.ruckl@quick.cz>
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import wx
import _winreg
from win32gui import MessageBox  #rework to eg.MessageBox ?
from win32com.client import Dispatch, DispatchWithEvents
from time import sleep
from os.path import isfile, exists
from functools import partial
from subprocess import Popen
from eg.WinApi.Dynamic import SendMessage,PostMessage
from win32gui import SetWindowPos
import ctypes
from time import time as timtim
from winsound import PlaySound,SND_ASYNC

ShowWindowAsync = ctypes.windll.user32.ShowWindowAsync

WM_COMMAND    = 273
WM_SYSCOMMAND = 0x0112
SC_CLOSE = 0xF060
SW_MINIMIZE = 6
SW_RESTORE = 9
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
HWND_BOTTOM = 1
SWP_NOMOVE = 2
SWP_NOSIZE = 1
SWP_ASYNCWINDOWPOS = 0x4000
SWP_NOACTIVATE = 16

eg.RegisterPlugin(
    name = "Phoner",
    author = "Pako",
    version = "0.0.3",
    kind = "program",
    guid = "{FF763E14-7253-4025-99F2-32D9AC43FA9C}",
    createMacrosOnAdd = True,
#  ToDo:  description - Add some text about CallID ...,
    description = ur'''<rst>
Adds support functions to control Phoner_.

.. _Phoner: http://www.phoner.de/index_en.htm''',
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2170",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUzzMz/AACAAAAA"
        "AAAAAID///+AAIDAwMCAgIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAPAAAAAAEAAAEAAADIG8j/DX0AAAAA"
        "AAAAAAAAAAMAAADYC0MAAAAAAAAAAAAAAAAAAAQAAQEAAQAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAEAAQEAAAAAAAAAAADIG3jIG3gAAGhE9RDIGVjCEnwAAAAAAAgAAGAAAADI"
        "G6DIG6AAAEAAAAAAAAAAAAAAAABFA+zIGVjH15DIImAAABwAAAAAAADDGeAADnQAACfI"
        "CtjIDuTIElDIFejIGVjIHHwAAAAAAADIHATIHAQAAphmZUwAABQAABMAAAAAAAMAACQA"
        "ABMAAAAAAAMAADQAABcAAAAAAAVkaVcAAEgAABcAAAAAAAZpZUgAAFwAABsAAAAAAAhi"
        "YVRlZHIAAHQAAidEGRwAAAAAAAAAAAAAAAAAAAAAAAAAAQgAAAAAAAFBp2RBp3QAAAAA"
        "AABFN1TIHHwAAAwAABwAAXMAAAIACOsAAAAAAQEAAAAAAwEAAADIHtQAAAAAAADIEQD0"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAQAAAAAAAAAAAAAAAAAAAAAAAAAAABGa1gA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAx3qA6AAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAMlJREFUeNq9ktsOwyAMQ8Ep"
        "of//xcsF0maD9WmLKlTJJ45JW8q/qwJbjYhQvbADRJLaIWpgujNYTXDdXj6Rg1qbBoro"
        "oGzQHPDSNMmEFABbvjEom4hOGCHrlTQ8RD+kn1s/eXDjugh/veTZT3mmSQChN9XlAKPe"
        "AMuvOlu/m9Q5AVe/KNYvB8c61eAgX3Lr0T9jgkZEvaGkT/2hW1lwQXL/bdFjQSwmCIPy"
        "BigiJku9pG+00C8Cda3fkY2ekc1//aQHUr7Vk/6LegGQlQV05G+vAAAAAABJRU5ErkJg"
        "gg=="
    ),
)
#===============================================================================

def PhonerWin():
    FindPhonerWindow = eg.WindowMatcher(
        u'phoner.exe',
        None,
        u'T{*}rmMain',
        None,
        None,
        None,
        True,
        0.0,
        0
    )
    hwnds = FindPhonerWindow()
    if len(hwnds)>0:
        return hwnds[0]
    else:
        return None
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

CALL_STATE =	(
    'Idle',
    'Offering',
    'Connecting',
    'Connected',
    'Disconnecting',
    'Disconnected',
    'Parked',
    'Hold',
    'Holding',
    'Unholding',
    'Conferenced',
    'Alerting',
    'B3Connected'
)

DIRECTION = (
        'Incoming',
        'Outgoing'
)
#===============================================================================

class EventHandler:
    def __init__(self):
        self.memo = {}
        self.lastIdle = None
        self.lastTime = timtim()

    def OnChangeState(self, call_id=None):
        """Statusnderung"""
        e = self.thread.phoner.GetState(call_id)
        if e !="":
            if call_id not in self.memo or (call_id in self.memo and self.memo[call_id]!=e):
                if e == 'Idle':
                    if self.lastIdle != call_id:
                        self.TriggerEvent(e,call_id)
                        self.lastIdle = call_id
                        if call_id in self.memo:
                            del self.memo[call_id]
                else:
                    self.TriggerEvent(e, call_id)
                    self.memo[call_id] = e
                    self.lastIdle = None

    def OnFilePlayed(self):
        """Wave-Datei fertig abgespielt"""
        self.TriggerEvent("EndOfPlayedFile")

    def OnDTMF(self, call_id=None, Digit=None):
        """DTMF erkannt"""
        nowTime = timtim()
        if nowTime - self.lastTime > 0.05:
            self.TriggerEvent("DTMF."+chr(Digit), call_id)
        self.lastTime = nowTime
#===============================================================================

class PhonerWorkerThread(eg.ThreadWorker):
    """Handles the COM interface in a thread of its own."""

    def Setup(self, plugin):
        """This will be called inside the thread at the beginning."""
        self.plugin = plugin

        class SubEventHandler(EventHandler):
            thread = self
            TriggerEvent = self.plugin.TriggerEvent
        self.EventHandler = SubEventHandler

        self.phoner = None
        self.events = None
        self.phoner = Dispatch("Phoner.CPhoner")
        self.events=DispatchWithEvents(self.phoner, self.EventHandler)

    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        del self.events
        del self.phoner
        self.plugin.workerThread = None

    def isRunning(self):
        flag = False
        if self.phoner:
            try:
                dummy = self.phoner.NumberOfCalls
                flag = True
            except:
                pass
        return flag

    def GetInfo(self, attrib, call_id):
        if self.isRunning():
            return eval("self.phoner.%s(call_id)" % attrib)

    def CallFunction(self, attrib, call_id):
        if self.isRunning():
            exec('self.phoner.%s(call_id)' % attrib)

    def SetValue(self, attrib, value):
        if self.isRunning():
            exec('self.phoner.%s=%s' % (attrib, str(value)))

    def GetValue(self, attrib):
        if self.isRunning():
            return getattr(self.phoner, attrib)

    def DisconnectReason(self, call_id):
        if self.isRunning():
            return self.phoner.DisconnectReason(call_id)

    def MakeCall(self, number):
        if self.isRunning():
            self.phoner.MakeCall(number)

    def MakeCallOver(self, number, msn):
        if self.isRunning():
            self.phoner.MakeCallOver(number, msn)

    def Transfer(self):
        if self.isRunning():
            self.phoner.Transfer()

    def Conference(self):
        if self.isRunning():
            self.phoner.Conference()

    def SendDTMF(self, call_id, number):
        if self.isRunning():
            self.phoner.SendDTMF(call_id, number)

    def SendWAVE(self, call_id, file):
        if self.isRunning():
            self.phoner.SendWAVE(call_id, file)

    def SendTTS(self, call_id, msg):
        if self.isRunning():
            self.phoner.SendTTS(call_id, msg)

    def SendSMS(self, number, msg):
        if self.isRunning():
            self.phoner.SendSMS(number, msg)

    def SendSMSService(self, number, msg, service):
        if self.isRunning():
            self.phoner.SendSMSService(number, msg, service)
#===============================================================================

class Text:
    errorNoWindow = "Couldn't find Phoner window"
    label1 = "Folder with phoner.exe:"
    filemask = "phoner.exe|phoner.exe|All-Files (*.*)|*.*"
    text1 = "Couldn't find Phoner window !"
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = 'Folder "%s" is incorrect'
    boxMessage1 = 'Missing file %s !'
    call_id_label = 'CallID (if payload is None):'
    exitDescription = """<rst>Exit Phoner.

Beware of setting **X-Button: minimize** (Window menu) !"""
    enable = ("Disabled","Enabled","Stop","Start")
#===============================================================================

class Phoner(eg.PluginBase):
    workerThread = None
    text = Text
    EventHandler = None

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    def __start__(self, path = None):
        self.PhonerPath = path

    def __stop__(self):
        if self.workerThread:
            self.workerThread.Stop()

    def StopThread(self):
        if self.workerThread:
            self.workerThread.Stop()

    def CheckWorkerThread(self):
        if not self.workerThread:
            try:
                self.workerThread = PhonerWorkerThread(self)
                self.workerThread.Start(100.0)
            except:
                return False
        return True

    def GetValue(self, attrib):
        if self.CheckWorkerThread():
            return self.workerThread.CallWait(
                partial(self.workerThread.GetValue, attrib),1000
            )

    def SetValue(self, attrib, value):
        if self.CheckWorkerThread():
            return self.workerThread.CallWait(
                partial(self.workerThread.SetValue, attrib, value),1000
            )

    def Configure(self, path = None):
        path = None
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        phPathCtrl = MyDirBrowseButton(
            panel,
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        phPathCtrlText = phPathCtrl.GetTextCtrl()
        phPathCtrlText.SetEditable(False)

        if path is None:
            try:
                ph_reg = _winreg.OpenKey(
                    _winreg.HKEY_CLASSES_ROOT,
                    "CLSID\\{98898145-96E2-11D3-A1D0-444553540000}\\LocalServer32"
                )
                self.PhonerPath = unicode(_winreg.EnumValue(ph_reg,0)[1])[:-11]
                _winreg.CloseKey(ph_reg)
                phPathCtrlText.ChangeValue(self.PhonerPath)
            except:
                self.PhonerPath = unicode(eg.folderPath.ProgramFiles)+"\\Phoner"
                phPathCtrlText.ChangeValue("")
        else:
            phPathCtrl.SetValue(path)
            self.PhonerPath = path
        phPathCtrl.startDirectory = self.PhonerPath
        sizerAdd = panel.sizer.Add
        sizerAdd(label1Text, 0, wx.TOP,15)
        sizerAdd(phPathCtrl,0,wx.TOP,3)

        def Validation():
            flag = exists(phPathCtrl.GetValue()+"\\phoner.exe")
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)

        def OnPathChange(event = None):
            path = phPathCtrl.GetValue()
            flag = exists(path+"\\phoner.exe")
            if event and not flag:
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % 'phoner.exe',
                    self.text.boxTitle % path,
                        0
                    )
            if path != "":
                phPathCtrl.startDirectory = path
            if event:
                event.Skip()
                Validation()
        phPathCtrl.Bind(wx.EVT_TEXT,OnPathChange)
        OnPathChange()

        while panel.Affirmed():
            panel.SetResult(
                phPathCtrl.GetValue(),
           )
#===============================================================================

class Start(eg.ActionBase):
    def __call__(self):
        #If you run Phoner just over COM/API, a window of Phoner is not drawn !!
        flag = True
        hwnd = PhonerWin()
        if not hwnd:
            ph = self.plugin.PhonerPath+'\\phoner.exe'
            if isfile(ph):
                #wx.CallAfter(Popen,[ph])
                Popen([ph])
                flag = False
                for n in range(500):
                    sleep(.1)
                    hwnd = PhonerWin()
                    if hwnd:
                        flag = True
                        break
            else:
                self.PrintError(self.text.text2 % 'phoner.exe')
                return self.text.text2 % 'phoner.exe'
        if not flag:
            self.PrintError(self.plugin.text.text1)
        dummy = self.plugin.GetValue('NumberOfCalls')
    class text:
        text2 = "Couldn't find file %s !"
#===============================================================================

class WindowControl(eg.ActionClass):
    def __call__(self):
        hwnd = PhonerWin()
        if hwnd:
            if self.value == SW_RESTORE:
                ShowWindowAsync(hwnd, SW_MINIMIZE)
                ShowWindowAsync(hwnd, SW_RESTORE)
                SetWindowPos(hwnd, HWND_TOPMOST,0,0,0,0,SWP_NOMOVE|SWP_NOSIZE|SWP_ASYNCWINDOWPOS)
                SetWindowPos(hwnd, HWND_NOTOPMOST,0,0,0,0,SWP_NOMOVE|SWP_NOSIZE|SWP_ASYNCWINDOWPOS)
            else:
                SetWindowPos(hwnd, HWND_BOTTOM,0,0,0,0,SWP_NOMOVE|SWP_NOSIZE|SWP_ASYNCWINDOWPOS|SWP_NOACTIVATE)
                ShowWindowAsync(hwnd, SW_MINIMIZE)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class Exit(eg.ActionBase):

    def __call__(self):
        hwnd = PhonerWin()
        if hwnd:
            if self.plugin.CheckWorkerThread(): #maybe try "IsConnected" (DVBviewer plugin like)
                self.plugin.workerThread.Stop()
                sleep(1)
            SendMessage(hwnd, WM_SYSCOMMAND, SC_CLOSE, 0)
#===============================================================================

class MakeCall(eg.ActionBase):
    def __call__(self, number=""):
        if number.lower()[:4]=="sip:":
            number = number[4:]
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                self.plugin.workerThread.CallWait(
            partial(self.plugin.workerThread.MakeCall, number),1000
        )
        else:
            self.PrintError(self.plugin.text.text1)

    def Configure(self, number=""):
        panel = eg.ConfigPanel()
        labelText = wx.StaticText(panel, -1, self.text.labelNumber)
        w,h=labelText.GetSize()
        textControl = wx.TextCtrl(panel, -1, number)
        textControl.SetMinSize((w,-1))
        panel.sizer.Add(labelText, 0, wx.TOP,10)
        panel.sizer.Add(textControl,0,wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
    class text:
        labelNumber = "Called party (number or SIP URI address):"
#===============================================================================

class MakeCallOver(eg.ActionBase):
    def __call__(self, number="", msn=""):
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                self.plugin.workerThread.CallWait(
                    partial(self.plugin.workerThread.MakeCallOver, number, msn),1000
                )
        else:
            self.PrintError(self.plugin.text.text1)

    def GetLabel(self, number,msn):
        return self.text.treeLabel % (number,msn)

    def Configure(self, number="",msn=""):
        panel = eg.ConfigPanel()
        labelNumber = wx.StaticText(panel, -1, self.text.labelNumber)
        labelMsn = wx.StaticText(panel, -1, self.text.labelMsn)
        w,h=labelNumber.GetSize()
        numberControl = wx.TextCtrl(panel, -1, number)
        numberControl.SetMinSize((w,-1))
        msnControl = wx.TextCtrl(panel, -1, msn)
        msnControl.SetMinSize((w,-1))
        panel.sizer.Add(labelNumber, 0, wx.TOP,10)
        panel.sizer.Add(numberControl,0,wx.TOP,3)
        panel.sizer.Add(labelMsn, 0, wx.TOP,15)
        panel.sizer.Add(msnControl,0,wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(numberControl.GetValue(), msnControl.GetValue(),)
    class text:
        labelNumber = "Called party number:"
        labelMsn = "MSN:"
        treeLabel = "Call number: %s over MSN: %s"
#===============================================================================

class Transfer(eg.ActionBase):
    def __call__(self):
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                self.plugin.workerThread.CallWait(
                    partial(self.plugin.workerThread.Transfer),1000
                )
        else:
            self.PrintError(self.plugin.text.text1)
#===============================================================================

class Conference(eg.ActionBase):
    def __call__(self):
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                self.plugin.workerThread.CallWait(
                    partial(self.plugin.workerThread.Conference),1000
                )
        else:
            self.PrintError(self.plugin.text.text1)
#===============================================================================

class SendDTMF(eg.ActionBase):
    def __call__(self, call_id='', string=""):
        if eg.event.payload:
            call_id = str(eg.event.payload)
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                for char in string:
                    self.plugin.workerThread.CallWait(partial(
                        self.plugin.workerThread.SendDTMF,
                        eg.ParseString(call_id),
                        char
                    ),1000)
                    sleep(0.2)
        else:
            self.PrintError(self.plugin.text.text1)

    def GetLabel(self, call_id, msg):
        return self.name + ": " + msg

    def Configure(self, call_id='', string=""):
        panel = eg.ConfigPanel()
        labelText = wx.StaticText(panel, -1, self.plugin.text.call_id_label)
        w,h=labelText.GetSize()
        labelDtmf = wx.StaticText(panel, -1, self.text.dtmfLabel)
        textControl = wx.TextCtrl(panel, -1, call_id)
        textControl.SetMinSize((w,-1))
        textControl2 = wx.TextCtrl(panel, -1, string)
        textControl2.SetMinSize((w,-1))
        textControl2.SetToolTip(wx.ToolTip(self.text.toolTip))
        panel.sizer.Add(labelText,0,wx.TOP,10)
        panel.sizer.Add(textControl,0,wx.TOP,3)
        panel.sizer.Add(labelDtmf,0,wx.TOP,10)
        panel.sizer.Add(textControl2,0,wx.TOP,3)

        def onStringChange(evt):
            val = textControl2.GetValue()
            cur = textControl2.GetInsertionPoint()
            lng = len(val)
            tmp = []
            for char in val:
                if char in ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","*","#"]:
                    tmp.append(char)
            val = "".join(tmp)
            textControl2.ChangeValue(val)
            if len(val) < lng:
                PlaySound('SystemExclamation',SND_ASYNC)
                cur += -1
            textControl2.SetInsertionPoint(cur)
            evt.Skip()
        textControl2.Bind(wx.EVT_TEXT,onStringChange)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue(),textControl2.GetValue())
    class text:
        dtmfLabel = "DTMF string to send:"
        toolTip = "Allowed characters: 0,1,2,3,4,5,6,7,8,9,A,B,C,D,*,#"
#===============================================================================

class SendWAVE(eg.ActionBase):
    def __call__(self, call_id='', file=""):
        if eg.event.payload:
            call_id = str(eg.event.payload)
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                self.plugin.workerThread.CallWait(partial(
                    self.plugin.workerThread.SendWAVE,
                    eg.ParseString(call_id),
                    file
                ),1000)
        else:
            self.PrintError(self.plugin.text.text1)

    def GetLabel(self, call_id, file):
        return self.name + ": " + file

    def Configure(self, call_id='', file=""):
        panel = eg.ConfigPanel()
        label1Text = wx.StaticText(panel, -1, self.plugin.text.call_id_label)
        w,h=label1Text.GetSize()
        textControl = wx.TextCtrl(panel, -1, call_id)
        textControl.SetMinSize((w,-1))
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        filepathCtrl = eg.FileBrowseButton(
            panel,
            size=(410,-1),
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse,
            initialValue = file,
            fileMask = self.text.filemask
        )
        panel.sizer.Add(label1Text, 0, wx.TOP,10)
        panel.sizer.Add(textControl,0,wx.TOP,3)
        panel.sizer.Add(label2Text, 0, wx.TOP,15)
        panel.sizer.Add(filepathCtrl,0,wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue(),filepathCtrl.GetValue())
    class text:
        filemask = "Wav-Files (*.WAV)|*.wav|All-Files (*.*)|*.*"
        label2 = "Path to soundfile:"
        browseTitle = "Selected file:"
        toolTipFile = "Press button and browse to select file ..."
#===============================================================================

class SendTTS(eg.ActionBase):
    def __call__(self, call_id='', msg=""):
        if eg.event.payload:
            call_id = str(eg.event.payload)
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                self.plugin.workerThread.CallWait(partial(
                    self.plugin.workerThread.SendTTS,
                    eg.ParseString(call_id),
                    msg
                ),1000)
        else:
            self.PrintError(self.plugin.text.text1)

    def GetLabel(self, call_id, msg):
        sms = msg[:32]+"..." if len(msg) > 32 else msg
        return self.name + ": " + sms

    def Configure(self, call_id='', msg=""):
        panel = eg.ConfigPanel()
        label1Text = wx.StaticText(panel, -1, self.plugin.text.call_id_label)
        w,h=label1Text.GetSize()
        textControl = wx.TextCtrl(panel, -1, call_id)
        textControl.SetMinSize((w,-1))
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        textControl2 = wx.TextCtrl(panel, -1, msg, style = wx.TE_MULTILINE)
        panel.sizer.Add(label1Text, 0, wx.TOP,10)
        panel.sizer.Add(textControl,0,wx.TOP,3)
        panel.sizer.Add(label2Text, 0, wx.TOP,15)
        panel.sizer.Add(textControl2,1,wx.EXPAND|wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue(),textControl2.GetValue())
    class text:
        label2 = "Message to send:"
#===============================================================================

class SendSMS(eg.ActionBase):
    def __call__(self, number="", msg=""):
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                self.plugin.workerThread.CallWait(partial(
                    self.plugin.workerThread.SendSMS,
                    number,
                    msg
                ),1000)
        else:
            self.PrintError(self.plugin.text.text1)

    def GetLabel(self, number, msg):
        sms = msg[:32]+"..." if len(msg) > 32 else msg
        return self.name + ": " + sms


    def Configure(self, number='', msg=""):
        panel = eg.ConfigPanel()
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        w,h=label1Text.GetSize()
        textControl = wx.TextCtrl(panel, -1, number)
        textControl.SetMinSize((w,-1))
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        textControl2 = wx.TextCtrl(panel, -1, msg, style = wx.TE_MULTILINE)
        panel.sizer.Add(label1Text, 0, wx.TOP,10)
        panel.sizer.Add(textControl,0,wx.TOP,3)
        panel.sizer.Add(label2Text, 0, wx.TOP,15)
        panel.sizer.Add(textControl2,1,wx.EXPAND|wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue(),textControl2.GetValue())
    class text:
        label1 = "Recipient number:"
        label2 = "Message to send:"
#===============================================================================

class SendSMSService(eg.ActionBase):
    def __call__(self, number="", msg="",service=""):
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                self.plugin.workerThread.CallWait(partial(
                    self.plugin.workerThread.SendSMSService,
                    number,
                    msg,
                    int(service)
                ),1000)
        else:
            self.PrintError(self.plugin.text.text1)

    def GetLabel(self, number, msg, service):
        sms = msg[:32]+"..." if len(msg) > 32 else msg
        return self.name + ": " + sms

    def Configure(self, number="", msg="", service=""):
        panel = eg.ConfigPanel()
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        label3Text = wx.StaticText(panel, -1, self.text.label3)
        textControl1 = wx.TextCtrl(panel, -1, number)
        textControl2 = wx.TextCtrl(panel, -1, msg)
        textControl3 = wx.TextCtrl(panel, -1, service)
        topSizer = wx.GridSizer(rows=2, cols=2)
        topSizer.Add(label1Text,0,wx.ALIGN_BOTTOM,0)
        topSizer.Add(label3Text,0,wx.ALIGN_BOTTOM,0)
        topSizer.Add(textControl1,0,wx.TOP,3)
        topSizer.Add(textControl3,0,wx.TOP,3)
        panel.sizer.Add(topSizer,0,wx.TOP|wx.EXPAND,0)
        panel.sizer.Add(label2Text,0,wx.TOP,10)
        panel.sizer.Add(textControl2,1,wx.EXPAND|wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(
                textControl1.GetValue(),
                textControl2.GetValue(),
                textControl3.GetValue()
            )
    class text:
        label1 = "Recipient number:"
        label2 = "Message to send:"
        label3 = "SMS service number:"
#===============================================================================

class DisconnectReason(eg.ActionBase):
    def __call__(self,call_id=""):
        if eg.event.payload:
            call_id = str(eg.event.payload)
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                return self.plugin.workerThread.CallWait(partial(
                    self.plugin.workerThread.DisconnectReason,
                    eg.ParseString(call_id)
                ),1000)
        else:
            self.PrintError(self.plugin.text.text1)

    def Configure(self, call_id=""):
        panel = eg.ConfigPanel()
        labelText = wx.StaticText(panel, -1, self.plugin.text.call_id_label)
        w,h=labelText.GetSize()
        textControl = wx.TextCtrl(panel, -1, call_id)
        textControl.SetMinSize((w,-1))
        panel.sizer.Add(labelText,0,wx.TOP,15)
        panel.sizer.Add(textControl,0,wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class CallFunction(eg.ActionBase):
    def __call__(self,call_id=""):
        if eg.event.payload:
            call_id = str(eg.event.payload)
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                res = self.plugin.workerThread.CallWait(partial(
                    self.plugin.workerThread.CallFunction,
                    self.__class__.__name__,
                    eg.ParseString(call_id)
                ),1000)
        else:
            self.PrintError(self.plugin.text.text1)

    def Configure(self, call_id=""):
        panel = eg.ConfigPanel()
        labelText = wx.StaticText(panel, -1, self.plugin.text.call_id_label)
        w,h=labelText.GetSize()
        textControl = wx.TextCtrl(panel, -1, call_id)
        textControl.SetMinSize((w,-1))
        panel.sizer.Add(labelText,0,wx.TOP,15)
        panel.sizer.Add(textControl,0,wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class NumberOfCalls(eg.ActionBase):
    def __call__(self):
        if PhonerWin():
            return self.plugin.GetValue('NumberOfCalls')
        else:
            self.PrintError(self.plugin.text.text1)
#===============================================================================

class GetInfo2(eg.ActionBase):
    def __call__(self):
        if PhonerWin():
            attrib = self.__class__.__name__[3:]
            return self.plugin.GetValue(attrib)
        else:
            self.PrintError(self.plugin.text.text1)
#===============================================================================

class SetState(eg.ActionBase):
    def __call__(self, enabled=True):
        if PhonerWin():
            attrib = self.__class__.__name__[3:]
            return self.plugin.SetValue(attrib,enabled)
        else:
            self.PrintError(self.plugin.text.text1)

    def GetLabel(self, enabled):
        return self.name + ": " + self.plugin.text.enable[int(enabled)+self.value]

    def Configure(self, enabled=True):
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.name,
            choices = self.plugin.text.enable[self.value:self.value+2],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(enabled)
        radioBox.SetMinSize((197,65))
        panel.sizer.Add(radioBox)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection())
#===============================================================================

class ToggleRecording(eg.ActionBase):
    def __call__(self):
        if PhonerWin():
            recState = self.plugin.GetValue("RecordingEnabled")
            self.plugin.SetValue("RecordingEnabled", not recState)
            return self.plugin.GetValue("RecordingEnabled")
        else:
            self.PrintError(self.plugin.text.text1)
#===============================================================================

class GetInfo(eg.ActionBase):
    def __call__(self,call_id=""):
        attrib = self.__class__.__name__
        if eg.event.payload:
            call_id = str(eg.event.payload)
        if PhonerWin():
            if self.plugin.CheckWorkerThread():
                res = self.plugin.workerThread.CallWait(partial(
                    self.plugin.workerThread.GetInfo,
                    attrib,
                    eg.ParseString(call_id)
                ),1000)
                if attrib != "GetCallInfo":
                    return res
                else:  #res[0] (= callID ?) flush
                    return CALL_STATE[res[1]], DIRECTION[res[2]], res[3], res[4]
        else:
            self.PrintError(self.plugin.text.text1)

    def Configure(self, call_id=""):
        panel = eg.ConfigPanel()
        labelText = wx.StaticText(panel, -1, self.plugin.text.call_id_label)
        w,h=labelText.GetSize()
        textControl = wx.TextCtrl(panel, -1, call_id)
        textControl.SetMinSize((w,-1))
        panel.sizer.Add(labelText,0,wx.TOP,15)
        panel.sizer.Add(textControl,0,wx.TOP,3)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

ACTIONS = (
    (Start,"Start","Start/Connect Phoner","Start and/or connect Phoner through COM-API.",None),
    (Exit,"Exit","Exit Phoner ",Text.exitDescription ,None),
    (eg.ActionGroup, 'Phonercontrols', 'Phoner GUI controls', 'Phoner GUI controls.',(
        (WindowControl,"Minimize","Minimize window","Minimize window.",None),
        (WindowControl,"Restore","Restore window","Restore window.",SW_RESTORE),
        (SetState,"SetAutoRecordEnabled","Set autorecord","Set Autorecord.",0),
        (SetState,"SetRecordingEnabled","Start/stop recording","Start/stop recording.",2),
        (SetState,"SetAnsweringMachineEnabled","Set answering machine","Set answering machine.",0),
        (SetState,"SetWindowEnabled","Set incoming call window","Set incoming call window.",0),
        (ToggleRecording,"ToggleRecording","Toggle recording of current call","Toggle recording of current call.",None),
#        (GetVolume,"GetVolume","Get volume","Get volume.", None),
#        (SetVolume,"SetVolume","Set volume","Set volume.", 0),
#        (SetVolume,"VolumeUp","Volume up","Volume up.", 1),
#        (SetVolume,"VolumeDown","Volume down","Volume down.", 2),
    )),
    (eg.ActionGroup, 'CallControl', 'Call and SMS control', 'Call and SMS control.',(
        (MakeCall,"MakeCall","Make call","Make call.", None),
        (MakeCallOver,"MakeCallOver","Make call over MSN","Make call over MSN.", None),
        (CallFunction,"AnswerCall","Answer call","Answer call.", None),
        (CallFunction,"DisconnectCall","Disconnect call","Disconnect call.", None),
        (Transfer,"Transfer","Transfer","Transfer.", None),
        (Conference,"Conference","Conference","Conference.", None),
        (SendDTMF,"SendDTMF","Send DTMF","Send DTMF.", None),
        (SendWAVE,"SendWAVE","Send WAVE","Send WAVE.", None),
        (SendTTS,"SendTTS","Send text to speech (TTS)","Send text to speech (TTS).", None),
        (SendSMS,"SendSMS","Send SMS","Send SMS.", None),
        (SendSMSService,"SendSMSService","Send SMS with service","Send SMS with service.", None),
    )),
    (eg.ActionGroup, 'GetInformation', 'Get information', 'Get information.',(
        (NumberOfCalls,"NumberOfCalls","Get number of calls","Get number of calls.", None),
        (GetInfo,"GetCallInfo","Get call info","Get call info.", None),
        (GetInfo,"GetState","Get state of call","Get state of call.", None),
        (GetInfo,"GetCalledID","Get ID of called party","Get ID of called party.", None),
        (GetInfo,"GetCallerID","Get ID of calling party","Get ID of calling party.", None),
        (GetInfo,"GetSUBCallerID","Get ISDN subaddress","Get ISDN subaddress.", None),
        (GetInfo,"GetDirection","Get call direction","Get call direction.", None),
        (DisconnectReason,"DisconnectReason","Get disconnect reason","Get disconnect reason.", None),
        (GetInfo2,"GetWindowEnabled","Get window enabled state","Get window enabled state.", None),
        (GetInfo2,"GetAutoRecordEnabled","Get autorecord enabled","Get autorecord enabled.", None),
        (GetInfo2,"GetRecordingEnabled","Get recording enabled","Get recording enabled.", None),
        (GetInfo2,"GetAnsweringMachineEnabled","Get answering machine enabled state","Get answering machine enabled state.", None),
        (GetInfo,"GetRecordedWAVE","Get recorded wave file","Get recorded wave file.", None),
    )),
)
