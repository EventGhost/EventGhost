# -*- coding: utf-8 -*-
#
# plugins/HauppaugeIR/__init__.py
#
# Copyright (C) 2008 Stefan Gollmer
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

eg.RegisterPlugin(
    name        = "Hauppauge IR",
    author      = "Stefan Gollmer",
    version     = "1.04.1093",
    kind        = "remote",
    guid        = "{B54E7F32-E117-4C24-A892-9D69BC290568}",
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
from threading import Timer, Lock
from time import sleep, time
from msvcrt import get_osfhandle
import _winreg
from threading import Event

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
    c_ulong,
    WNDCLASS,
    TIMERPROC,
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
    DWORD,

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
#------------------------------------------
#
#
#
#
# If the HauppaugeIR driver couldn't be initialized, the event ghost event
#       "HauppaugeIR.InitError"
# will be fired




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

DSR0112 = {
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
28: "TVNEW",
22: "NAVLEFT",
23: "NAVRIGHT",
20: "NAVUP",
21: "NAVDOWN",
10: "TEXT",
18: "CHNLPREV",
}


HauppaugeIRTable = {
 0:     HCWClassic ,
29:     DSR0112 ,
30:     HCWPVR2 ,
31:     HCWPVR ,
}



class HauppaugeIRMessageReceiver(eg.ThreadWorker):
    """
    A thread with a hidden window to receive win32 messages from the driver
    """

    @eg.LogIt
    def Setup(  self,
                plugin,
                waitTime,
                pollTime,
                useDefaultPollTime,
                initTime = 15.0,
                checkRepeatFlag = False,
                repeatReleaseTime = 200 ):
        """
        This will be called inside the thread at the beginning.
        """
        self.lock = Lock()
        self.abort = False

        self.plugin = plugin
        self.waitTime = float(waitTime)/1000.0
        self.repeatReleaseTime = float(repeatReleaseTime)/1000.0
        self.pollTime = pollTime
        self.useDefaultPollTime = useDefaultPollTime
        self.defaultPollTime = -1

        self.LastKeyCode = -1

        self.checkRepeatFlag = checkRepeatFlag

        self.repeatCode = c_int(0)
        self.systemCode = c_int(0)
        self.keyCode    = c_int(0)

        self.lastEvent = eg.EventGhostEvent()
        self.keyStillPressed = False
        self.initTerminated = False

        self.timerInit = None
        self.timerKey = None

        self.hwnd = None
        self.dll  = None

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
        self.TIMERPROC           = WINFUNCTYPE( None, HWND, c_uint, c_uint, DWORD )

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

        self.timerInit = Timer( initTime, self.PostInit)        # Init delayed init timer ( in case of standby problems)
        self.timerInit.start()



    @eg.LogItWithReturn
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """

        self.abort = True
        self.lock.acquire()

        if self.dll:
            self.dll.IR_Close(self.hwnd, 0);

        #print "Irremote is stopped"

        if self.timerInit :
            self.timerInit.cancel()
            #print "Init aborted"

        if self.hwnd:
            windll.user32.KillTimer(self.hwnd, 1)
            DestroyWindow(self.hwnd)
            UnregisterClass(self.wc.lpszClassName, self.hinst)


        if self.defaultPollTime != -1 :

            regHandle = _winreg.OpenKey(
                            _winreg.HKEY_LOCAL_MACHINE,
                            'SOFTWARE\hauppauge\IR',
                            0,
                            _winreg.KEY_WRITE | _winreg.KEY_READ
            )

            _winreg.SetValueEx( regHandle, 'PollRate', 0, _winreg.REG_DWORD, int(self.defaultPollTime) )

            _winreg.CloseKey( regHandle )

        self.lock.release()



    def MyWndProc(self, hwnd, mesg, wParam, lParam) :
        if mesg == WM_TIMER:
            keyHit = self.IR_GetSystemKeyCode(byref(self.repeatCode), byref(self.systemCode), byref(self.keyCode) );
            if  keyHit == 1:
                #print "RepeatCode = ", self.repeatCode, "  systemCode = ", self.systemCode, "  keyCode = ", self.keyCode, "  time = ", time()
                if self.timerKey :
                    self.timerKey.cancel()
                key    = self.keyCode.value
                repeat = ( self.repeatCode.value == 0 )
                if ( not repeat and self.checkRepeatFlag ) or not ( self.keyStillPressed and self.LastKeyCode == key ) :
                    self.LastKeyCode = key

                    if not self.systemCode.value in HauppaugeIRTable:
                        eventString = "%d" % key
                    elif key in HauppaugeIRTable[ self.systemCode.value ]:
                        eventString = HauppaugeIRTable[ self.systemCode.value ][key]
                    else:
                        eventString = "%d" % key

                    self.lastEvent = self.plugin.TriggerEnduringEvent(eventString)
                    self.keyStillPressed = True

                    releaseTime = self.waitTime
                else :
                    releaseTime = self.repeatReleaseTime

                self.timerKey = Timer(releaseTime, self.OnTimeOut)
                self.timerKey.start()
        return 1



    def OnTimeOut(self):
        #print "Release Key"
        self.keyStillPressed = False
        self.lastEvent.SetShouldEnd()



    @eg.LogIt
    def PostInit( self ) :

        self.lock.acquire()
        if self.abort :
            self.lock.release()
            return
        self.timerInit = Timer( 60.0, self.OnPostInitTimeOut)        # Init timeout timer
        self.timerInit.start()

        returnVal = False

        if ( not self.useDefaultPollTime ) :

            regHandle = _winreg.OpenKey(
                            _winreg.HKEY_LOCAL_MACHINE,
                            'SOFTWARE\hauppauge\IR',
                            0,
                            _winreg.KEY_WRITE | _winreg.KEY_READ
            )

            self.defaultPollTime = int( _winreg.QueryValueEx(regHandle, 'PollRate')[0] )

            _winreg.SetValueEx( regHandle, 'PollRate', 0, _winreg.REG_DWORD, int(self.pollTime) )

            returnVal = self.IR_Open(self.hwnd, 0, 0, 0);

            _winreg.SetValueEx( regHandle, 'PollRate', 0, _winreg.REG_DWORD, int(self.defaultPollTime) )

            _winreg.CloseKey( regHandle )

            self.defaultPollTime = -1

        else :
            returnVal = self.IR_Open(self.hwnd, 0, 0, 0);

        self.timerInit.cancel()

        if not self.initTerminated :

            if not returnVal and not self.initTerminated :
                self.plugin.PrintError("Couldn't start the Hauppauge remote control")
                self.Stop()
                self.plugin.TriggerEvent("InitError")
            else :
                #print "Irremote is started"
                pass

        del self.timerInit
        self.timerInit = None
        self.lock.release()



    @eg.LogIt
    def OnPostInitTimeOut( self ) :
        self.initTerminated = True
        self.plugin.PrintError("Couldn't start the Hauppauge remote control")
        self.Stop()
        self.plugin.TriggerEvent("InitError")




class HauppaugeIR(eg.PluginClass):

    class text:
        buttonTimeout = "Button release timeout (seconds):"
        buttonTimeoutDescr = (
            "(If you get unintended double presses of the buttons, "
            "increase this value.)"
        )
        repeatReleaseTime = "Button release timeout (seconds) after repeat detected:"
        pollTime        = "Poll time (seconds)"
        buttonPollTime  = "Use default poll time (0.2s)"
        checkRepeatFlag = "Use the repeat flag of the IR"

    def __init__( self ) :
        self.AddAction(Restart)
        self.AddAction(OnComputerSuspend, hidden = True )   # For test only
        self.AddAction(OnComputerResume, hidden = True )    # For test only

        self.waitTime = -1
        self.repeatReleaseTime = -1
        self.pollTime = -1
        self.initTime = -1
        self.useDefaultPollTime = True

        self.started = False
        self.config = False



    def __start__( self,
                   waitTime=-1,
                   pollTime = -1,
                   useDefaultPollTime = True,
                   checkRepeatFlag = False,
                   repeatReleaseTime = 200,
                   initTime = 15.0 ):

        if waitTime != -1 :
            self.waitTime = waitTime
            self.repeatReleaseTime = repeatReleaseTime
            self.pollTime = pollTime
            self.initTime = initTime
            self.useDefaultPollTime = useDefaultPollTime
            self.checkRepeatFlag = checkRepeatFlag

        if self.config :
            initTime = 1.0
            self.config = False
        else :
            initTime = self.initTime
        self.msgThread = HauppaugeIRMessageReceiver( self,
                                self.waitTime,
                                self.pollTime,
                                self.useDefaultPollTime,
                                initTime,
                                self.checkRepeatFlag,
                                self.repeatReleaseTime )
        self.msgThread.Start( 15.0 )
        self.started = True



    @eg.LogIt
    def OnComputerSuspend(self, suspendType = None):
        if self.started :
            self.Finish()



    @eg.LogIt
    def OnComputerResume(self, suspendType = None):
        if self.started :
            self.__start__()



    @eg.LogItWithReturn
    def Finish(self, timeout = 10.0 ):
        self.msgThread.Stop( timeout )
        return True



    def __stop__(self ):
        self.started = False
        self.Finish()



    def Configure(  self,
                    waitTime=300,
                    pollTime = 90,
                    useDefaultPollTime = True,
                    checkRepeatFlag = False,
                    repeatReleaseTime = 200 ):
        panel = eg.ConfigPanel(self)
        text = self.text

        def onCheckBox( event ) :
            enable = not useDefaultPollTimeCtrl.GetValue()
            pollTimeCtrl.Enable( enable )
            event.Skip()

        waitTimeCtrl = panel.SpinNumCtrl(waitTime, min=0, max=999, fractionWidth=0, integerWidth=3)
        repeatReleaseTimeCtrl = panel.SpinNumCtrl(repeatReleaseTime, min=0, max=999, fractionWidth=0, integerWidth=3)

        useDefaultPollTimeCtrl = wx.CheckBox(panel, -1, text.buttonPollTime)
        useDefaultPollTimeCtrl.SetValue( useDefaultPollTime )
        useDefaultPollTimeCtrl.Bind(wx.EVT_CHECKBOX, onCheckBox)

        pollTimeCtrl = panel.SpinNumCtrl(pollTime, min=0, max=999, fractionWidth=0, integerWidth=3)

        checkRepeatFlagCtrl = wx.CheckBox(panel, -1, text.checkRepeatFlag)
        checkRepeatFlagCtrl.SetValue( checkRepeatFlag )

        sizer = wx.GridBagSizer( 5, 5 )
        sizer.Add( wx.StaticText( panel, -1, text.buttonTimeout ),
                                         ( 0, 0 ),(1,2), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT )
        sizer.Add( waitTimeCtrl, ( 0, 2 ), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText( panel, -1, text.buttonTimeoutDescr ),
                                         ( 1, 0 ),(1,3), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL )


        sizer.Add( wx.StaticText( panel, -1, text.repeatReleaseTime ),
                                         ( 3, 0 ),(1,2), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT )
        sizer.Add( repeatReleaseTimeCtrl, ( 3, 2 ), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL )



        sizer.Add( useDefaultPollTimeCtrl, ( 5, 0 ), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText( panel, -1, text.pollTime ),
                                         ( 5, 1 ), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT )
        sizer.Add( pollTimeCtrl, ( 5, 2 ), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL )
        sizer.Add( checkRepeatFlagCtrl, ( 7, 0 ), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL )



        panel.sizer.Add( sizer, 0 )

        onCheckBox(wx.CommandEvent())

        while panel.Affirmed():

            waitTime           = waitTimeCtrl.GetValue()
            repeatReleaseTime  = repeatReleaseTimeCtrl.GetValue()
            pollTime           = pollTimeCtrl.GetValue()
            useDefaultPollTime = useDefaultPollTimeCtrl.GetValue()
            checkRepeatFlag    = checkRepeatFlagCtrl.GetValue()

            panel.SetResult( waitTime, pollTime, useDefaultPollTime, checkRepeatFlag, repeatReleaseTime )
            self.config = True




class Restart(eg.ActionClass) :

    @eg.LogIt
    def __call__( self ) :
        self.plugin.__stop__(  timeout = 10.0 )
        self.plugin.__start__( initTime = 1.0 )
        return True




class OnComputerSuspend(eg.ActionClass) :
    def __call__( self ) :
        self.plugin.OnComputerSuspend()
        return True




class OnComputerResume(eg.ActionClass) :
    def __call__( self ) :
        self.plugin.OnComputerResume()
        return True
