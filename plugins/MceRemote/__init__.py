#
# plugins/MceRemote/__init__.py
#
# Copyright (C) 2005 Lars-Peter Voss
#
# This file is part of EventGhost.
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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import eg

eg.RegisterPlugin(
    name = "Microsoft MCE Remote",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Plugin for the Microsoft MCE remote.'
        '\n\n<p>'
        'Will only work, if you have installed the replacement driver for '
        'the MCE remote. You find detailed installation instructions here:'
        '<br><a href="http://www.eventghost.org/wiki/MCE_Remote_FAQ">'
        'MCE Remote FAQ'
        '</a><p><center><img src="MCEv2.jpg"/></center>'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACfklEQVR42q2TS2gTQRyH"
        "f5N9NNlts20abYyxVirWShGLUh8XoSpUUBEVUU+5CXoQr+LNm14UtRCpRcGLHnqoiooN"
        "VO1FRWrTaKgmqdJqGuwj3TTZ947bbLV37cAMM8zMx39+fEPwn42sGKD7zk3aeWg3TEut"
        "rC3bdrpZmZuWBlVXYFgGKKEQOAHDg+M4f/YCqQBuxa7T7XtaEWloRkkrwDQt6KZzwdZR"
        "VGSU1DmoRgm6pUBWC1DUMoK1q2BmQ24F77/G6ZfvI2isb0FRnYVYZtAe8aCUkzGSyuCj"
        "tADFLsEwNOi0CM1QYDnVrNcOuICHQzfoWCaJoD8MWZnGfoPB1k0BpN/k8DKbxvAGE1JA"
        "QHidF9lMHvnChPMuii3sCRdwre8czUykwDAMuLKKU1oV2CCL7Itx9LMycmtqsa2jAY1N"
        "EgaepWBxc2A5Dq30mAu40neGpr59AKUUliHB5z8KUwxi5vUDWCQNW2TRvrOpknkykYRQ"
        "7wXr4bFRO+ICrj6J0tHcq0ris3MHwbdcgiaX8XMohl2B+xAF4jyhBsqCgqQTsOhnwXNe"
        "NM4fdgG3By7S4amnoBaHT4m9gP84ivkUquf7cTL8Fh1tPjSv9eHxqIw48YL3MfBWiQj/"
        "6nIBzxN3afxHDJYTzLvBOvBMGfMFPyLcZ3QFCtixWcCiET1pFVpIAiE2aqrrEM4vAZIT"
        "Q/RR6jKo1zmgOrLYtAIzphSEZ2cQ8gGTio0E5SGFa6BrBiJSKxqm97mAWE83VUJjSEzG"
        "nXT5v34ugkqKDkPW4OEZCCIH4iEg1IPOttPQ0quXVe6910vh6EuX/F5U1hmWZV/a+LP0"
        "EBbRaJSs3Gf61/YbN1kg0OJlna4AAAAASUVORK5CYII="
    ),
)


import os
from threading import Timer
import threading
import time
import win32event
import win32api
import win32gui
import win32con

import wx

from ctypes import *

#BOOL WINAPI MceIrRegisterEvents(HWND hWnd)
#------------------------------------------
#To register the window that will receives messages on keystroke events (from MceIr only)
#(IR code analysis is automatically suspended during a learning phase)
#
#hWnd : handle to the window which will receives WM_USER messages
#       wParam values is ID_MCEIR_KEYCODE
#       LOWORD(lParam) contains the key code (see MceIr.h for the list)
#       HIWORD(lParam) contains the repeat count (0 means a new keystroke)
#returns TRUE is successfull
#
#BOOL WINAPI MceIrUnregisterEvents()
#-----------------------------------
#To stop receiving keystrokes from IR
#
#returns TRUE is successfull
#
#BOOL WINAPI MceIrSetRepeatTimes(DWORD FirstRepeat, DWORD NextRepeats)
#---------------------------------------------------------------------
#To specify the repeat rate when a key remains pressed
#FirstRepeat : Time (in ms) to wait before sending a second WM_USER message (HIWORD(lParam) will be 1)
#NextRepeats : Interval between next messages until the key is released
#
#returns TRUE is successfull
#
#BOOL WINAPI MceIrRecordToFile(HANDLE hFile, DWORD Timeout)
#----------------------------------------------------------
#To record raw IR code (learning function). This function waits for the IR receiver to become silent for 1 second,
#then enters the recording phase. 
#
#hFile  : handle to the file in which raw IR codes will be stored
#        (must be opened previously then closed when function returns)
#Timeout: applies to the recording phase and occurs is nothing is received from the MceIr (in ms) 
#
#returns TRUE is successfull
#
#BOOL WINAPI MceIrPlaybackFromFile(HANDLE hFile)
#-----------------------------------------------
#To playback a previously recorded file.
#
#hFile  : handle to the file in which raw IR codes has been stored
#        (must be opened previously then closed when function returns)
#
#returns TRUE is successfull
#
#BOOL WINAPI MceIrSuspend()
#-----------------------------------------------
#Call this function before entering a suspend power state (WM_POWERBROADCAST + PBT_APMSUSPEND event)
#
#BOOL WINAPI MceIrResume()
#-----------------------------------------------
#Call this function on resuming a suspend power state (WM_POWERBROADCAST + PBT_APMRESUMEAUTOMATIC event)
#
#BOOL WINAPI MceIrSelectBlaster()
#-----------------------------------------------
#To select a blaster port on which further IR playback will be send
#
#BOOL WINAPI MceIrCheckFile(HANDLE hFile)
#-----------------------------------------------
#To check in the API support playing this file



KEY_MAP = {
    0x7b9a: "TV_Power", 0x7ba1: "Blue", 0x7ba2: "Yellow", 0x7ba3: "Green",
    0x7ba4: "Red", 0x7ba5: "Teletext", 0x7baf: "Radio", 0x7bb1: "Print",
    0x7bb5: "Videos", 0x7bb6: "Pictures", 0x7bb7: "Recorded_TV",
    0x7bb8: "Music", 0x7bb9: "TV", 0x7bd9: "Guide", 0x7bda: "LiveTV",
    0x7bdb: "DVD_Menu", 0x7bdc: "Back", 0x7bdd: "Ok", 0x7bde: "Right",
    0x7bdf: "Left", 0x7be0: "Down", 0x7be1: "Up", 0x7be2: "Star",
    0x7be3: "Pound", 0x7be4: "Replay", 0x7be5: "Skip", 0x7be6: "Stop",
    0x7be7: "Pause", 0x7be8: "Record", 0x7be9: "Play", 0x7bea: "Rewind",
    0x7beb: "Forward", 0x7bec: "ChannelDown", 0x7bed: "ChannelUp",
    0x7bee: "VolumeDown", 0x7bef: "VolumeUp", 0x7bf0: "Details",
    0x7bf1: "Mute", 0x7bf2: "Start", 0x7bf3: "Power", 0x7bf4: "Enter",
    0x7bf5: "Escape", 0x7bf6: "Num9", 0x7bf7: "Num8", 0x7bf8: "Num7",
    0x7bf9: "Num6", 0x7bfa: "Num5", 0x7bfb: "Num4", 0x7bfc: "Num3",
    0x7bfd: "Num2", 0x7bfe: "Num1", 0x7bff: "Num0",
}


pluginDir = os.path.abspath(os.path.split(__file__)[0])
dllPath = os.path.join(pluginDir, "MceIr.dll")



class MceRemote(eg.PluginClass):
    
    class text:
        buttonTimeout = "Button release timeout (seconds):"
        buttonTimeoutDescr = (
            "(If you get unintended double presses of the buttons, "
            "increase this value.)"
        )

    def __init__(self):
        self.device = None
        self.isEnabled = False
        self.waitTime = 0.15
        self.repeatCounter = -1
        self.timer = Timer(0, self.OnTimeOut)
        self.lastEventString = ""
        self.lastEvent = eg.EventGhostEvent()
        
        
    def __start__(self, waitTime=0.15):
        self.waitTime = waitTime
        self.isEnabled = True
        # create a dummy window
        def Init():
            self.frame = wx.Frame(None, -1, "MceIr Monitor")
            # we are only interested in the hwnd
            self.hwnd = self.frame.GetHandle()
            # insert our WndProc
            self.oldWndProc = win32gui.SetWindowLong(
                self.hwnd, 
                win32con.GWL_WNDPROC, 
                self.MyWndProc
            )
            self.dll = WinDLL(dllPath)
            self.dll.MceIrRegisterEvents(self.hwnd)
            self.dll.MceIrSetRepeatTimes(1,1)
            
            #Bind to suspend notifications so we can go into suspend
            eg.Bind("System.Suspend", self.OnSuspend)
            eg.Bind("System.Resume", self.OnResume)
        wx.CallAfter(Init)


    def __stop__(self):
        self.isEnabled = False
        
        #Unbind from power notification events
        eg.Unbind("System.Suspend", self.OnSuspend)
        eg.Unbind("System.Resume", self.OnResume)
        
        self.dll.MceIrUnregisterEvents()
        if self.frame:
            self.frame.Close()
            self.frame = None
        
        
    def OnSuspend(self, event):
        if self.isEnabled:
            self.dll.MceIrSuspend()
    
    
    def OnResume(self, event):
        if self.isEnabled:
            self.dll.MceIrResume()       
          
                        
    @eg.LogIt
    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        if mesg == win32con.WM_DESTROY:
            # Restore the old WndProc.  Notice the use of win32api
            # instead of win32gui here.  This is to avoid an error due to
            # not passing a callable object.
            win32api.SetWindowLong(
                self.hwnd, 
                win32con.GWL_WNDPROC,
                self.oldWndProc
            )
        elif mesg == win32con.WM_USER:
            key = lParam & 0xFFFF
            repeatCounter = (lParam >> 16)
            if not self.isEnabled:
                return
            if key in KEY_MAP:
                eventString = KEY_MAP[key]
            else:
                eventString = "%X" % key
            self.timer.cancel()       
            if self.lastEventString != eventString:
                if self.lastEventString != "":
                    self.lastEvent.SetShouldEnd()
                self.lastEvent = self.TriggerEnduringEvent(eventString)
                self.lastEventString = eventString
                self.repeatCounter = repeatCounter
            else:
                self.repeatCounter += 1
                if self.repeatCounter != repeatCounter:
                    if self.lastEventString != "":
                        self.lastEvent.SetShouldEnd()
                    self.lastEvent = self.TriggerEnduringEvent(eventString)
                    self.lastEventString = eventString
                    
            self.timer = Timer(self.waitTime, self.OnTimeOut)
            self.timer.start()
        else:
            return win32gui.CallWindowProc(
                self.oldWndProc, 
                hwnd, 
                mesg,
                wParam, 
                lParam
            )
        
        
    def OnTimeOut(self):
        self.lastEvent.SetShouldEnd()
        self.lastEventString = ""
        
        
    def Configure(self, waitTime=0.15):
        dialog = eg.ConfigurationDialog(self)
        staticText = wx.StaticText(dialog, -1, self.text.buttonTimeout)
        dialog.sizer.Add(staticText)
        waitTimeCtrl = eg.SpinNumCtrl(
            dialog, 
            -1,
            waitTime,
            integerWidth=3
        )
        dialog.sizer.Add(waitTimeCtrl)
        staticText = wx.StaticText(dialog, -1, self.text.buttonTimeoutDescr)
        dialog.sizer.Add(staticText, 0, wx.TOP, 5)
        
        yield dialog
        yield (waitTimeCtrl.GetValue(), )
