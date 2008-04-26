#
# plugins/HauppaugeIR/__init__.py
#
# Copyright (C) 2008 Stefan Gollmer
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
# $LastChangedDate: 2008-04-19 10:11:41 +0200  $
# $LastChangedRevision: 382 $
# $LastChangedBy: bitmonster $


eg.RegisterPlugin(
    name        = "Hauppauge IR",
    author      = "Stefan Gollmer",
    version     = "1.02." + "$LastChangedRevision: 382 $".split()[1],
    kind        = "remote",
    description = (
                    'Hardware plugin for the '
                    '<a href="http://www.hauppauge.com">'
                    'Hauppauge IR Control</a>, '
                    'delivered with several Hauppauge TV cards'
        
                  ),
    help        = (
                    'This plugin is using the file "irremote.DLL" which is located in '
                    'the installation path of the Hauppauge IR software. The version '
                    'of this dll must be at least 2.45.<br><br>'
                    'The Hauppauge program "Ir.exe" should not be started anymore.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=821",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAaElEQVR42mNkoBAwYhH7"
        "DyIcHBwYDhw4AKdxqWfEphlmAAwgGYChB6cBxLoawwCYzQ8ePGBQUFCA00guwW9AQ0MD"
        "XDFyOIAAVI7GXqDYBRSHwTAKRGyAKBfg1g40gBgXUOoFQoZgqAcAnwlSETUFcqwAAAAA"
        "SUVORK5CYII="
    )    
)


import os
from threading import Timer
from msvcrt import get_osfhandle
import _winreg



from eg.WinApi.Dynamic import (
    WinDLL,
    windll,
    WINFUNCTYPE,
    POINTER,
    HWND ,
    HMODULE ,
    c_int,
    c_uint,
    c_byte,
    c_void_p,
    c_char_p,
    WNDCLASS,
    GetDesktopWindow,
    WNDPROC,
    CreateWindow,
    WinError,
    byref,
    WM_TIMER,
    RegisterClass,
    WS_OVERLAPPEDWINDOW,
    CW_USEDEFAULT,
    WM_TIMER,
    pointer,
    DestroyWindow,
    UnregisterClass,
    GetTickCount,
    DWORD
)


#c_int WINAPI IR_Open(HWND hWnd, c_int, c_byte, c_int)
#------------------------------------------
#To register the window that will receives messages on keystroke events (from Hauppauge IR only)
# and enables the receiver
#
#hWnd : handle to the window which will receives WM_USER messages
#returns value != 0 is successfull
#
#
#c_int WINAPI IR_Close(HWND hWnd, c_int)
#------------------------------------------
#To unregister the window that will receives messages on keystroke events (from Hauppauge IR only)
# and disables the receiver
#
#hWnd : handle to the window which will receives WM_USER messages
#returns value != 0 is successfull
#
#
#c_int WINAPI IR_GetSystemKeyCode(POINTER( c_int) repeatCode, POINTER( c_int) systemCode, POINTER( c_int) keycCode )
#------------------------------------------
#To unregister the window that will receives messages on keystroke events (from Hauppauge IR only)
# and disables the receiver
#
#repeatCode : return value containing 0, if the key is pressed continues, otherwise 2. Not working fine, not usable
#systemCode : return value containing the system code of the remote control (0,30,31,0x800f), see Irremote.ini
#keyCode    : return value containing the key code (0-99)
#
#returns value ==1 if key is pressed


HCWClassic = {
0: "OLD0",
1: "1",
2: "2",
3: "3",
4: "4",
5: "5",
6: "6",
7: "7",
8: "8",
9: "9",
12: "RADIO",
13: "MUTE",
15: "TV",
16: "VOLUP",
17: "VOLDOWN",
30: "RESERVED",
32: "CHNLUP",
33: "CHNLDOWN",
34: "SOURCE",
38: "MINIMIZE",
46: "FULLSCREEN",
}


HCWPVR = {
 0:"0",
 1:"1",
 2:"2",
 3:"3",
 4:"4",
 5:"5",
 6:"6",
 7:"7",
 8:"8",
 9:"9",
46:"GREEN",
56:"YELLOW",
11:"RED",
41:"BLUE",
12:"FUNC",
13:"MENU",
15:"MUTE",
16:"VOLUP",
17:"VOLDOWN",
32:"CHNLUP",
33:"CHNLDOWN",
61:"GRNPOWER",
31:"BACK",
37:"OK",
59:"GO",
60:"FULLSCREEN",
55:"REC",
54:"STOP",
48:"PAUSE",
53:"PLAY",
50:"REWIND",
52:"FASTFWD",
30:"SKIPFWD",
36:"SKIPREV",
}


HCWPVR2 = {
0: "0",
1: "1",
2: "2",
3: "3",
4: "4",
5: "5",
6: "6",
7: "7",
8: "8",
9: "9",
46: "GREEN",
56: "YELLOW",
11: "RED",
41: "BLUE",
13: "MENU",
15: "MUTE",
16: "VOLUP",
17: "VOLDOWN",
32: "CHNLUP",
33: "CHNLDOWN",
61: "GRNPOWER",
31: "BACK",
37: "OK",
59: "GO",
55: "REC",
54: "STOP",
48: "PAUSE",
53: "PLAY",
50: "REWIND",
52: "FASTFWD",
30: "SKIPFWD",
36: "SKIPREV",
#new to hcwpvr2
12: "RADIO",
28: "TVNEW",
24: "VIDEOS",
25: "MUSIC",
26: "PICTURES",
27: "GUIDE",
22: "NAVLEFT",
23: "NAVRIGHT",
20: "NAVUP",
21: "NAVDOWN",
10: "TEXT",
14: "SUBCC",
18: "CHNLPREV",
}


HauppaugeIRTable = {
 0:     HCWClassic ,
30:     HCWPVR2 ,
31:     HCWPVR ,
}



class HauppaugeIRMessageReceiver(eg.ThreadWorker):
    """
    A thread with a hidden window to receive win32 messages from the driver
    """
    hwnd = None
    dll = None
    
    @eg.LogIt
    def Setup(self, plugin, waitTime):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin
        self.waitTime = float(waitTime)/1000.0

        self.LastKeyCode = -1
        
        self.pollTime = 90

        self.RepeatCode = c_int(0)        
        self.systemCode = c_int(0)
        self.keyCode    = c_int(0)
        
        self.timer = Timer(0, self.OnTimeOut)
        self.lastEvent = eg.EventGhostEvent()
        self.keyStillPressed = False

        # load irremote.dll
        
        try:
            regHandle = _winreg.OpenKey(
                           _winreg.HKEY_LOCAL_MACHINE, 
                           'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Hauppauge WinTV Infrared Remote', 
                           0, 
                           _winreg.KEY_READ
                        )

            InstallString = _winreg.QueryValueEx(regHandle, 'UninstallString')[0]

            _winreg.CloseKey( regHandle )

            irremoteDir = InstallString.partition(' ')[0].rsplit('\\',1)[0]

            dllPath = os.path.join(irremoteDir, "irremote.DLL")

            self.dll = windll.LoadLibrary(dllPath)
            self.dll = WinDLL(dllPath)

        except:
            plugin.PrintError("Couldn't find irremote.dll! Reinstalling the Hauppauge "
                   "WinTV Infrared Remote package can solve the problem."
                  )
            raise self.plugin.Exceptions.DeviceNotFound

        self.IR_Open             = WINFUNCTYPE( c_int, HWND, c_int, c_byte, c_int )
        self.IR_Close            = WINFUNCTYPE( c_int, HWND, c_int )
        self.IR_GetSystemKeyCode = WINFUNCTYPE( c_int, POINTER( c_int), POINTER( c_int), POINTER( c_int) )
        
        self.IR_Open             = self.dll.IR_Open
        self.IR_Close            = self.dll.IR_Close
        self.IR_GetSystemKeyCode = self.dll.IR_GetSystemKeyCode
        
        wc = WNDCLASS()
        wc.hInstance = GetDesktopWindow()
        wc.lpszClassName = "HaupPluginEventSinkWndClass"
        wc.lpfnWndProc = WNDPROC(self.MyWndProc)
        if not RegisterClass(byref(wc)):
            raise WinError()
        self.hwnd = CreateWindow(
            wc.lpszClassName,
            "HaupaugePlugin Event Window",
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT, 
            CW_USEDEFAULT,
            CW_USEDEFAULT, 
            CW_USEDEFAULT,
            0, 
            0,
            wc.hInstance, 
            None
        )
        if not self.hwnd:
            raise WinError()
        self.wc = wc
        self.hinst = wc.hInstance
        
        regHandle = _winreg.OpenKey(
                        _winreg.HKEY_LOCAL_MACHINE, 
                        'SOFTWARE\hauppauge\IR', 
                        0, 
                        _winreg.KEY_WRITE | _winreg.KEY_READ
        )

        defaultPollTime = int( _winreg.QueryValueEx(regHandle, 'PollRate')[0] )
        _winreg.SetValueEx( regHandle, 'PollRate', 0, _winreg.REG_DWORD, int(self.pollTime) )

        returnVal = self.IR_Open(self.hwnd, 0, 0, 0);

        _winreg.SetValueEx( regHandle, 'PollRate', 0, _winreg.REG_DWORD, int(defaultPollTime) )

        _winreg.CloseKey( regHandle )

        if not returnVal:
            plugin.PrintError("Couldn't create the EventSinkWindow")
            raise WinError()
        
        #print "Irremote is started"


        
    @eg.LogIt
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        if self.hwnd:
            windll.user32.KillTimer(self.hwnd, 1)
        if self.dll:
            self.dll.IR_Close(self.hwnd, 0);
        
        #print "Irremote is stopped"

        if self.hwnd:
            DestroyWindow(self.hwnd)
            UnregisterClass(self.wc.lpszClassName, self.hinst)


        #self.Stop() # is this needed? No!
        
        
    #@eg.LogIt
    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        if mesg == WM_TIMER:
            keyHit = self.IR_GetSystemKeyCode(byref(self.RepeatCode), byref(self.systemCode), byref(self.keyCode) );
            if  keyHit == 1:
                self.timer.cancel()
                key = self.keyCode.value
                if self.LastKeyCode != key or not self.keyStillPressed:
                    self.LastKeyCode = key
                    
                    if not self.systemCode.value in HauppaugeIRTable:
                        eventString = "%d" % key
                    elif key in HauppaugeIRTable[ self.systemCode.value ]:
                        eventString = HauppaugeIRTable[ self.systemCode.value ][key]
                    else:
                        eventString = "%d" % key
                    
                    self.lastEvent = self.plugin.TriggerEnduringEvent(eventString)
                    self.keyStillPressed = True

                self.timer = Timer(self.waitTime, self.OnTimeOut)
                self.timer.start()
        return 1
    
    def OnTimeOut(self):
        self.keyStillPressed = False
        self.lastEvent.SetShouldEnd()

        
        

class HauppaugeIR(eg.PluginClass):
    
    class text:
        buttonTimeout = "Button release timeout (seconds):"
        buttonTimeoutDescr = (
            "(If you get unintended double presses of the buttons, "
            "increase this value.)"
        )

    def __start__(self, waitTime=0.15):
        self.msgThread = HauppaugeIRMessageReceiver(self, waitTime)
        self.msgThread.Start()


    @eg.LogIt
    def OnComputerSuspend(self, suspendType):
        self.__stop__()
    
    
    @eg.LogIt
    def OnComputerResume(self, suspendType):
        self.__start__()     
          
                        
    def __stop__(self):
        self.msgThread.Stop()
        
    def Configure(self, waitTime=300):
        panel = eg.ConfigPanel(self)
        waitTimeCtrl = panel.SpinNumCtrl(waitTime, min=0, max=999, fractionWidth=0, integerWidth=3)
        panel.AddLine(self.text.buttonTimeout, waitTimeCtrl)
        panel.AddLine(self.text.buttonTimeoutDescr)
        
        while panel.Affirmed():
            panel.SetResult(waitTimeCtrl.GetValue())
        
