# -*- coding: utf-8 -*-

PLUGIN_NAME    = "SoundGraph iMON VFD/LCD Display"
PLUGIN_VERSION = "0.3.2"

#
# plugins/EG App Control/__init__.py
#
# Copyright (C) 2013 by Daniel Brugger
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
# Version history (newest on top):
# 0.3.2: Fix: Avoid display of 'None' if display text is None 
# 0.3.1: Fix: Conversion to unicode for all texts, especially when passing numeric values
# 0.3.0: Add: New mode 'Simple, dynamic text mode' 
#            The text to be displayed supports now variables of the format {eg.globals.MyVariable} 
#            or {eg.event.payload} which will be dynamically evaluated at runtime 
#        Fix: DisplayText config dialog requires initialisation
# 0.2.2: Change: Startup sequence improved. Plugin waits now during initialization until iMON Manager is ready
#                with a configurable timeout. If initialization fails within this time, the API part is shutdown 
#                and no longer printing error messages.
# 0.2.1: Workaround for unicode->ascii conversion error in method DebugPrint (actually a bug in eg.PrintDebugNotice).
#        Code cleanup / log output reduced
#        Updated documentation
# 0.2.0: Finalization of the VFD part.
#        Documentation added
#        Still experimental: Improved scrolling on LCD screens. Aim to support all scroll modes on LCD too.
#        DebugPrint function added
# 0.1.1: Added action 'GetCurrentDisplayText'
#        Added action 'GetMessageStack'
#        Fixed timeout exception after resume, caused by UserCallbackThread
#        Fixed management of display objects, they were stopped-started too often (more than necessary)
#        Fixed thread handling, scroll thread and callback thread wasn't properly terminated in some situations
#        Fixed 'DisplayText' configuration panel when no iMON display has been detected
#        Added feature 'Auto clear after N loops'
#        Added feature 'Fly-In'
#        'DisplayText' configuration panel: auto switch to 'Advanced Settings' if msgPriority != DEFAULT_PRIORITY
# 0.1.0: First version released 

import eg

eg.RegisterPlugin(
    name=PLUGIN_NAME,
    label="iMON Display",
    description="""<rst>
Displays text on a SoundGraph iMON VFD or LCD Display

Displays arbitrary text on a `SoundGraph iMON VFD or LCD Display <http://www.soundgraph.com/vfd-feature-en/>`__

Supports many scroll options and other features, even dynamically changing text is supported. 

|imonDispImg|_

**Prerequisites**

- The plugin is built on top of the 'SoundGraph iMON Display API' and therefore requires `iMON Manager <http://www.soundgraph.com/forums/showthread.php?t=9857>`__ software installed (current version; it has been tested with 8.12.1202).
- Make sure to configure Frontview to mode 'Automatically'! (iMON Manager > iMON Utilities > FrontView > Common > Run FrontView When iMON Starts: Automatically)

**An extensive documentation can be found in the 'Display Text' action.**

.. |imonDispImg| image:: Pro_vfd02.jpg
.. _imonDispImg: http://www.soundgraph.com/vfd-feature-en/ 
"""
,
    author="Daniel Brugger",
    version=PLUGIN_VERSION,
    kind="external",
    guid="{A13E8F21-69CC-4E4D-895D-F24C1656BD9E}", 
    createMacrosOnAdd = True,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=3970",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAMAAABhq6zVAAAAB3RJTUUH3AgYFDEmA4rL"
        "pgAAAAlwSFlzAAAK8AAACvABQqw0mAAAAwBQTFRFAAAACAgIEBAQGBgYISEhKSkpMSkp"
        "MTEpKTExMTExCBg5CCE5ECE5MTE5MTk5EClCFC1SITFCITFKITlSKTVCKTlKMTVCKTlS"
        "GDlaGEJrKUJSKUFdGEJzIUJzIUpzKUpzOTExOTE5OTkxOTk5OTlCPz88QkJCSkJCO0RO"
        "RkpGOUhaQk9dMUxtNlJwQlJrQlprSkpKSkpSSlJSUk5KSlJaV1RST1hjWlZaY1pWY2Na"
        "Wl1lWmNrY2NjZ2dna2trc29rKlKDPlt/LmKdP2mcT150UmiAUnCUS3SoOXW+RHzDUoK7"
        "U4rLPoXZSonYUJDaWpDWZ253ZXCEc3Nzb3d/eHh1c3eEe3t7f39/Y3OMbXyPhISIioqI"
        "d4ymdpjCYpjWfaTSOYTnOYznQoznQozvQpTnQpTvQpT3SoznSpTnSpTvSpT3Spz3Upbs"
        "WpnpUpz3Wpz3Y5nhbZzhZaLobafoWqX3WqX/Y6X3aav5d6nnd7Hzc7X3e633ibTmf7X3"
        "hL33jL33lIyElIyMlJSMlJSUnJSUnJyUlJSclJyclJypnZ+jpaWcpaWlraWgra2lpaWt"
        "ta2lpa2tra2tta2ttbWtnKW1nK21pa21ra21rbW1tbW1vbW1vb21lKW9lK29nK29pa29"
        "lKXGlK3GlK3OlLXOnK3KnLXGnLXOpa3GpbXGpbXOpb3OrbW9rbXGrbXOrb3Grb3OtbW9"
        "tb29tb3Gtb3OtcbOvb29vb3GvcbGvcbOxr29xsa9xsbGxsbOxs7OzsbGzs7GlK3WlLXW"
        "lLXeorfWnLXenL3elLXnmL3vlL33lMb3nMb3jL3/lL3/lMb/nMb/nM7/pb3er8PWrcHe"
        "p8fvtcbewcrWvc/hwNfvpcb/pc7/rc7/rdb/tdb/vdj8xt73xt7/zs7O1s7O1tbOzs7W"
        "ztbW1tbWztbe1tbe0tri0t7r1t7v1ufv1t731uf3zt7/zuf/3trW4uDg3ufn5+fn3ufz"
        "1uf/1u//3u//6+vr7+/n5+//5/f/7+/v7/P39PT0/fr3xXjvRAAAALx0Uk5T////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "/////////////////////////////////////wACLglrAAAAUklEQVR42lWOsRHAMAgD"
        "abMjbabxPFRahsY9uiwQkVycsyr9IQQGYBytAVj7syWy9j5JFxnks1ghaoisixkfKDYX"
        "FNfEk4o9O90meNu2O/sHv24W+U3xCPgEiQAAAABJRU5ErkJggg=="
    )
)

import os
import wx
import sys
import time
import datetime
from threading import Thread, Event, Timer
from functools import partial
from copy import deepcopy as cpy


from eg.WinApi.Dynamic import (
    CDLL,
    HWND,
    WNDCLASS,
    WNDPROC,
    WM_USER,
    WS_OVERLAPPEDWINDOW,
    CW_USEDEFAULT,
    CFUNCTYPE,
    GetModuleHandle,
    CreateWindowEx,
    DestroyWindow,
    RegisterClass,
    UnregisterClass,
    WinError,
    byref,
    c_uint,
    LPCTSTR,
)

PLUGIN_DIR = os.path.abspath( os.path.split( __file__ )[0] )

# DSPType
DSPN_DSP_NONE = 0
DSPN_DSP_VFD  = 0x01
DSPN_DSP_LCD  = 0x02

# DSPNInitResult
DSPN_SUCCEEDED            = 0
DSPN_ERR_IN_USING         = 0x0100
DSPN_ERR_HW_DISCONNECTED  = 0x0101
DSPN_ERR_NOT_SUPPORTED_HW = 0x0102
DSPN_ERR_PLUGIN_DISABLED  = 0x0103
DSPN_ERR_IMON_NO_REPLY    = 0x0104
DSPN_ERR_UNKNOWN          = 0x0200

# DSPResult
RC_UNKNOWN                = -1
DSP_SUCCEEDED             = 0       # Function Call Succeeded Without Error
DSP_E_FAIL                = 1       # Unspecified Failure
DSP_E_OUTOFMEMORY         = 2       # Failed to Allocate Necessary Memory
DSP_E_INVALIDARG          = 3       # One or More Arguments Are Not Valid
DSP_E_NOT_INITED          = 4       # API is Not Initialized
DSP_E_POINTER             = 5       # Pointer is Not Valid
DSP_S_INITED              = 0x1000  # API is Initialized
DSP_S_NOT_INITED          = 0x1001  # API is Not Initialized
DSP_S_IN_PLUGIN_MODE      = 0x1002  # API Can Control iMON Display (Display Plug-in Mode)
DSP_S_NOT_IN_PLUGIN_MODE  = 0x1003  # API Can't Control iMON Display

# DSPNotifyCode
DSPN_PLUGIN_SUCCEED       = 0
DSPN_PLUGIN_FAILED        = 1
DSPN_IMON_RESTARTED       = 2
DSPN_IMON_CLOSED          = 3
DSPN_HW_CONNECTED         = 4
DSPN_HW_DISCONNECTED      = 5
DSPN_LCD_TEXT_SCROLL_DONE = 0x1000

VFD_NUM_CHAR          = 16    # Number of displayable chars on VFD
CALLBACK_TIMEOUT      = 60    # timeout for user callback functions
SLEEP_TIME_SLICE      = 0.2   # time in sec. Controls the interval how often threads can be interrupted or stopped.
LCD_NO_SCROLL_PULSE   = 0.2
LCD_CONCAT_CHAR       = ' | '

SCROLL_MODE_NO_SCROLL           = 0
SCROLL_MODE_ENDLESS_LOOP        = 1
SCROLL_MODE_STOP_SCROLL_STOP    = 2

DEFAULT_PRIORITY            = 100
DEFAULT_SCROLL_SPEED        = 8.0
DEFAULT_SCROLL_MODE         = SCROLL_MODE_STOP_SCROLL_STOP
DEFAULT_SCROLL_WAIT         = 1.0
DEFAULT_SCROLL_LOOPS        = -1
DEFAULT_AUTO_CLEAR_SECS     = -1
DEFAULT_AUTO_CLEAR_LOOPS    = -1
DEFAULT_CALLBACK_FREQUENCY  = 60.0
DEFAULT_INIT_WAIT_TIME      = 30

EFFECT_NONE             = 0
EFFECT_FLY_IN           = 1
EFFECT_FLY_OUT          = 2
EFFECT_FLY_IN_DELAY     = 0.05

ACTION_STATUS_IDLE      = 0
ACTION_STATUS_WAITING   = 1
ACTION_STATUS_RUNNING   = 2

THREAD_STOPPED          = 0
THREAD_RUNNING          = 1
THREAD_SUSPENDED        = 2

from os.path import join, dirname, abspath, isfile
import codecs

# Utility method to read HTML help files
def GetFileAsStr(filename):
    try:
        filepath = abspath(join(dirname(__file__.decode('mbcs')), filename))
        f = codecs.open(filepath, mode="r", encoding="latin_1", buffering=-1)
        doc = f.read()
        f.close()
        return doc
    except Exception, exc:
        msg = "Error reading help file " + filepath + ", error=" + unicode(exc)
        eg.PrintTraceback(msg)
        return msg

# The plugin class
class iMON_Display( eg.PluginBase ):
    
    @eg.LogIt
    def __init__( self ):
        self.AddAction( DisplayText )
        self.AddAction( ClearText )
        
        group = self.AddGroup("Advanced actions", "Advanced actions")
        group.AddAction( AcquireDisplay )
        group.AddAction( GetDisplayType )
        group.AddAction( IsInitialized )
        group.AddAction( IsPluginMode )
        group.AddAction( GetCurrentDisplayText )
        group.AddAction( GetMessageStack )
        group.AddAction( ReleaseDisplay )

        self.displayType = DSPN_DSP_NONE
        self.displayTypeStr = 'None'

        self.isSetup = False
        self.isInitialized = False
        self.started = False
        self.debugLevel = 0

        self.setupEvent = Event()   # used to wait until API ready
        self.lcdEvent = Event()     # used for LCD scrolling
        self.actionEvent = Event()  # used to wait until ACTION_STATUS_IDLE

        self.apiWorker = None
        self.displayEngine = None
        

    @eg.LogIt
    def Configure(  self,
        lcdNoScrollPulse=LCD_NO_SCROLL_PULSE,
        debugLevel=0,
        initWaitTime=DEFAULT_INIT_WAIT_TIME
    ):
        panel = eg.ConfigPanel()
        
        initWaitTimeCtrl = panel.SpinNumCtrl( initWaitTime, min=1, max=999, fractionWidth=0 )
        panel.AddLine( "Maximum initialization wait time", initWaitTimeCtrl, "Maximum wait time in seconds until iMON Manager is ready" )

        dbgLevelCtrl = panel.SpinNumCtrl( debugLevel, min=0, max=4, fractionWidth=0, integerWidth=1 )
        panel.AddLine( "Debug Level", dbgLevelCtrl, "Set to 0 to turn debug log off" )

        pulseNumCtrl = panel.SpinNumCtrl( lcdNoScrollPulse, min=0.0, max=9, fractionWidth=2, integerWidth=1, increment=0.1 )
        panel.AddLine( "LCD no scroll pulse frequency (experimental!)", pulseNumCtrl, "Set to 0.00 to turn feature off" )
        
        while panel.Affirmed():
            lcdNoScrollPulse = pulseNumCtrl.GetValue()
            debugLevel = dbgLevelCtrl.GetValue()
            initWaitTime = initWaitTimeCtrl.GetValue()
            panel.SetResult( 
                lcdNoScrollPulse, debugLevel, initWaitTime )
    

    @eg.LogIt
    def __start__( self,
        lcdNoScrollPulse=LCD_NO_SCROLL_PULSE,
        debugLevel=0,
        initWaitTime=DEFAULT_INIT_WAIT_TIME
    ):
        eg.PrintDebugNotice( PLUGIN_NAME, PLUGIN_VERSION, 'plugin started on', time.strftime( "%d %b %Y %H:%M:%S" ))
        
        LCD_NO_SCROLL_PULSE = lcdNoScrollPulse
        self.debugLevel = debugLevel
        self.initWaitTime = initWaitTime
        
        eg.Bind( 'ProcessingChange', self.StatusChangeListener )
        self.started = True
        

    @eg.LogItWithReturn
    def __stop__( self ):
        self.TearDown( )
        eg.Unbind( 'ProcessingChange', self.StatusChangeListener )
        self.started = False


    @eg.LogIt
    def OnComputerSuspend(self, suspendType):
        self.TearDown( )


    # Register an event listener for EG status change events.
    def StatusChangeListener(self, status):
        # Deadlock prevention:
        # This listener ensures that the UserCallbackThread waits calling the user callback method until EG is in idle state.
        # This is necessary because the user callback method probably calls other Actions and this might lead to deadlocks.
        if status == ACTION_STATUS_IDLE:
            self.actionEvent.set()
        else:
            self.actionEvent.clear()


    @eg.LogIt
    def Setup( self, initWaitTime=None ):
        self.DebugPrint( 3, 'iMON_Display.Setup' )

        if self.isSetup:
            self.TearDown( )
        
        if not initWaitTime:
            initWaitTime = self.initWaitTime
        
        self.apiWorker = IMonApiWorker( self )
        try:
            self.apiWorker.Start( initWaitTime ) # timeout for Setup() function
            
        except Exception, exc:
            self.isSetup = False
            try:
                self.apiWorker.Stop()
            except:
                pass
            del self.apiWorker
            self.apiWorker = None
            eg.PrintError( 'self.apiWorker.Start() failed: ' + repr( exc ) )

        else:
            self.displayEngine = DisplayEngine( self )
            try:
                self.displayEngine.Start( 10.0 )
    
            except Exception, exc:
                self.isSetup = False
                try:
                    self.displayEngine.Stop()
                except:
                    pass
                del self.displayEngine
                self.displayEngine = None
                eg.PrintError( 'self.displayEngine.Start() failed: ' + repr( exc ) )
            else:
                self.isSetup = True


    @eg.LogIt
    def InitDisplay( self, initWaitTime=None ):
        rc = RC_UNKNOWN

        if not initWaitTime:
            initWaitTime = self.initWaitTime
        
        if not self.isSetup:
            self.Setup( initWaitTime )
            
        if self.isSetup:
            if not self.isInitialized:
                self.DebugPrint( 2, 'iMON_Display.InitDisplay' )
                self.setupEvent.clear()
                rc = self.apiWorker.ApiDisplayInit()
                self.setupEvent.wait( initWaitTime ) # async - wait until API completed
                if self.setupEvent.isSet():
                    if rc != DSP_SUCCEEDED:
                        msg = "iMON API init failed with rc=" + str( rc )
                        eg.PrintError( msg )
                    else:
                        self.isInitialized = True
                else:
                    msg = 'iMON API init failed.'
                    eg.PrintError( msg )
                    rc = DSP_E_FAIL
                    self.TearDown()
            else:
                rc = DSP_SUCCEEDED
        else:
            eg.PrintError( 'Setup failed!' )
            rc = DSP_E_FAIL

        return rc
        

    @eg.LogItWithReturn
    def TearDown( self ):
        rc = DSP_SUCCEEDED
        
        if self.isSetup:
            try:
                self.DebugPrint( 2, 'iMON_Display.TearDown' )
                self.displayEngine.Stop( 30.0 )
                del self.displayEngine
                self.displayEngine = None
                
                self.apiWorker.Stop( 30.0 ) # timeout is important, ThreadWorker will thread.join(), otherwise not
                del self.apiWorker
                self.apiWorker = None
                
            finally:
                self.isSetup = False
                self.isInitialized = False
                
        return rc


    # as the name says...
    def DebugPrint( self, level, *args ):
        if level <= self.debugLevel:
            strs = " ".join( [ unicode( arg ) for arg in args ] )
            print strs
            eg.PrintDebugNotice( strs.encode( 'ascii', 'replace' ) ) # PrintDebugNotice can't handle unicode :(



class IMonApiWorker( eg.ThreadWorker ):
    '''Responsible for all iMON Display API calls.
        API calls are done asynchronously, using ThreadWorker functionality.
    '''
    
    @eg.LogIt
    def Setup( self, plugin ):
        # Credits: The DLL handling of this plugin is based on brand10's iMON-API plugin - many thanks, great work!
        self.plugin = plugin
        plugin.DebugPrint( 3, 'IMonApiWorker.Setup' )

        wc = WNDCLASS()
        wc.hInstance = GetModuleHandle( None )
        wc.lpszClassName = "DisplayMessageReceiver"
        wc.lpfnWndProc = WNDPROC( self.MyWndProc )

        if not RegisterClass( byref( wc ) ):
            raise WinError()

        self.hwnd = CreateWindowEx( 
            0,
            wc.lpszClassName,
            "iMON Display Message Receiver",
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
            0, 0, wc.hInstance, None
        )

        if not self.hwnd:
            raise WinError()

        self.wc = wc
        self.hinst = wc.hInstance
        self.dll = CDLL( os.path.join( PLUGIN_DIR, "iMONDisplay.dll" ) )

        # API Method-Definitions
        self.DisplayInit = CFUNCTYPE( HWND, c_uint )
        self.DisplayInit = self.dll.IMON_Display_Init
        
        self.DisplayUninit = CFUNCTYPE( None )
        self.DisplayUninit = self.dll.IMON_Display_Uninit
        
        self.IsInited = CFUNCTYPE( None )
        self.IsInited = self.dll.IMON_Display_IsInited
        
        self.IsPluginMode = CFUNCTYPE( None )
        self.IsPluginMode = self.dll.IMON_Display_IsPluginModeEnabled

        self.SetVfdText = CFUNCTYPE( LPCTSTR, LPCTSTR )
        self.SetVfdText = self.dll.IMON_Display_SetVfdText

        self.SetLcdText = CFUNCTYPE( LPCTSTR )
        self.SetLcdText = self.dll.IMON_Display_SetLcdText

        # Public ThreadWorker methods
        self.ApiDisplayInit   = self.Func( partial( self.DisplayInit, self.hwnd, WM_USER ) )
        self.ApiIsInited      = self.Func( self.IsInited )
        self.ApiIsPluginMode  = self.Func( self.IsPluginMode )
        self.ApiSetVfdText    = self.Func( self.SetVfdText )
        self.ApiSetLcdText    = self.Func( self.SetLcdText )


    @eg.LogIt
    def Finish( self ):
        # This method is called by the eg.ThreadWorker super class. Never call it directly.
        self.DisplayUninit()
        DestroyWindow( self.hwnd )
        UnregisterClass( self.wc.lpszClassName, self.hinst )


    #@eg.LogIt
    def MyWndProc( self, dummyHwnd, mesg, wdispObj, ldispObj ):
        if mesg == WM_USER:
            # All OK
            plugin = self.plugin
            if ( wdispObj == DSPN_PLUGIN_SUCCEED ) or ( wdispObj == DSPN_IMON_RESTARTED ) or ( wdispObj == DSPN_HW_CONNECTED ):
                if ldispObj & DSPN_DSP_VFD:
                    plugin.DebugPrint( 1, "iMON_Display: VFD init successful" )
                    plugin.displayType    = DSPN_DSP_VFD
                    plugin.displayTypeStr = 'VFD'
                elif ldispObj & DSPN_DSP_LCD:
                    plugin.DebugPrint( 1, "iMON_Display: LCD init successful" )
                    plugin.displayType    = DSPN_DSP_LCD
                    plugin.displayTypeStr = 'LCD'
                else:
                    msg = 'iMON_Display: init successful, but unknown display type: ' + str( ldispObj )
                    eg.PrintError( msg )
                    plugin.displayType    = DSPN_DSP_NONE
                    plugin.displayTypeStr = 'None'
                plugin.setupEvent.set()

            # LCD scroll done -> restart
            elif wdispObj == DSPN_LCD_TEXT_SCROLL_DONE:
                # signal to call ApiSetLcdText again
                plugin.DebugPrint( 2, "MyWndProc: got event DSPN_LCD_TEXT_SCROLL_DONE" )
                plugin.lcdEvent.set()
                    
            # Error handling
            elif wdispObj == DSPN_PLUGIN_FAILED:
                plugin.PrintError( "iMON_Display: Can't get control of display. Is FrontView in auto mode?" )

            elif wdispObj == DSPN_HW_DISCONNECTED:
                plugin.PrintError( "iMON_Display: Hardware disconnected" )

            elif wdispObj == DSPN_IMON_CLOSED:
                plugin.PrintError( "iMON_Display: iMON Manager is not running" )
            
            else:
                plugin.DebugPrint( 1, "MyWndProc: Unhandled message wdispObj:", wdispObj )

        return 1



class DisplayEngine( eg.ThreadWorker ):
    '''
    This class manages scrolling, user callbacks and display priorities. It's the living heart of the plugin :)
    In order to guarantee synchronized access to the DisplayObjects, the class is implemented as ThreadWorker.
    '''
    
    #def __init__( self, plugin ):
    @eg.LogIt
    def Setup( self, plugin ):
        self.plugin = plugin

        self.displayObjs = {}       # dict with all display objects
        self.currentDispObj = None  # the currently displayed dispObj
        
        self.scrollManager   = ScrollManager( plugin )
        self.callbackManager = CallbackManager( plugin )
        
        # Public ThreadWorker methods - synchronized access to critical sections
        self.DisplayText                = self.Func( self._displayText )
        self.ClearText                  = self.Func( self._clearText )
        self.GetCurrentDisplayText      = self.Func( self._getCurrentDisplayText )
        self.CreateDisplayObject        = self.Func( self._createDisplayObject )
        self.GetDisplayObject           = self.Func( self._getDisplayObject )
        self.DisplayObjectExpired       = self.Func( self._displayObjectExpired )
        self.SetDisplayText             = self.Func( self._setDisplayText )
        self.GetParsedText              = self.Func( self._getParsedText )
        self.GetMessageStack            = self.Func( self._getMessageStack )


    @eg.LogIt
    def _displayText( self, dispObj, clearExisting=True ):

        self.setAutoClearTimer( dispObj, absolute=True )
            
        if clearExisting:
            # clear, stop and delete the disp obj with same priority
            self._clearText( dispObj.msgPriority, displayNext=False )
        
        # add to dict
        self.displayObjs[dispObj.msgPriority] = dispObj
        
        # Display priorities. 
        # The rules are:
        # - Only the text with the highest priority is displayed, it hides all other texts with lower priorities.
        # - As soon as 'ClearText' on the text with highest priority is called, the text with next lower priority is displayed. 
        # - Two texts with same priority can't exist together, the later one replaces the earlier one.
        newObj = False
        if self.currentDispObj is not None:
            if dispObj.msgPriority < self.currentDispObj.msgPriority:
                newObj = True
                self.suspendDispObj( self.currentDispObj )
                self.currentDispObj = dispObj
        else:
            newObj = True
            self.currentDispObj = dispObj
        if not newObj:
            return False

        if self.currentDispObj.runState == THREAD_SUSPENDED:
            self.resumeDispObj( self.currentDispObj )
        else:
            self.setAutoClearTimer( self.currentDispObj, absolute=False )
            # let's go!
            self.startDispObj( self.currentDispObj )


    @eg.LogIt
    def _clearText( self, msgPriority=None, displayNext=True ):
        if msgPriority is None and self.currentDispObj is not None:
            msgPriority = self.currentDispObj.msgPriority
        
        delObj = None
        if msgPriority is not None:
            # remove from dict
            delObj = self.displayObjs.pop( msgPriority, None )
            if delObj is not None:
                self.stopDispObj( delObj )
        
        if displayNext:
            nextObj = self.findNextDispObj()
            if nextObj is not None and nextObj != self.currentDispObj:
                self._displayText( nextObj, clearExisting=False )

        return len( self.displayObjs ) == 0



    def _getCurrentDisplayText( self ):
        if self.currentDispObj is not None:
            data = { }
            data['line1'] = self._getParsedText( self.currentDispObj, 0 )
            data['line2'] = self._getParsedText( self.currentDispObj, 1 )
            data['msgPriority'] = self.currentDispObj.msgPriority
            return data

        
    @eg.LogIt
    def _createDisplayObject( self, msgPriority, dispLine ):
        '''Creates a display object with default arguments'''

        dispObj = eg.Bunch()

        if msgPriority is None or not isinstance( msgPriority, int ):
            dispObj.msgPriority = DEFAULT_PRIORITY
        else:
            dispObj.msgPriority = msgPriority
        
        dispObj.line            = [ None, None ]
        dispObj.isVariableText  = [ True, True ]

        for i in range( 2 ):
            dispObj.line[i] = unicode( dispLine[i] ) if dispLine[i] else ''
            if dispObj.line[i] == self._getParsedText( dispObj, i ):
                dispObj.isVariableText[i] = False

        dispObj.runState                = THREAD_STOPPED

        dispObj.scrollMode              = DEFAULT_SCROLL_MODE
        dispObj.scrollSpeed             = DEFAULT_SCROLL_SPEED
        dispObj.scrollWaitSec           = DEFAULT_SCROLL_WAIT
        dispObj.maxScrollLoops          = DEFAULT_SCROLL_LOOPS
        dispObj.effects                 = EFFECT_NONE
        dispObj.scrollThread            = None

        dispObj.autoClearAfterSec       = DEFAULT_AUTO_CLEAR_SECS
        dispObj.autoClearAfterLoops     = DEFAULT_AUTO_CLEAR_LOOPS
        dispObj.autoClearTimeAbsolute   = True
        dispObj.autoClearTask           = None
        dispObj.expiresAfterTimestamp   = None

        dispObj.userCallbackFunc        = None
        dispObj.userCallbackFreqInSec   = DEFAULT_CALLBACK_FREQUENCY
        dispObj.userCallbackObj         = None
        dispObj.callbackThread          = None

        return dispObj


    #@eg.LogIt
    def _getDisplayObject( self, msgPriority ):
        '''Gets the display object with the given priority'''
        
        # the primary key for a display object is its priority
        dispObj = self.displayObjs.get( msgPriority )
        return dispObj


    @eg.LogIt
    def _displayObjectExpired( self, msgPriority ):
        self.plugin.DebugPrint( 2, '_displayObjectExpired ', msgPriority )
        dispObj = self._getDisplayObject( msgPriority )
        if dispObj is not None:
            dispObj.autoClearTask = None
            #self.printCatalogue( '_displayObjectExpired' )
            self._clearText( dispObj.msgPriority )


    def _setDisplayText( self, msgPriority, line1, line2 ):
        dispObj = self._getDisplayObject( msgPriority )
        if dispObj is not None:
            dispObj.line = [ line1, line2 ]

        
    def _getParsedText( self, dispObj, i ):
        parsed = None
        if dispObj.isVariableText[i]:
            if dispObj.line[i]:
                parsed = eg.ParseString( dispObj.line[i], self.evalExpression )
        else:
            parsed = dispObj.line[i]
        return parsed


    def _getMessageStack( self ):
        msgStack = {}
        if self.displayObjs is not None and len( self.displayObjs ) > 0: # todo - there's a more elegant way...
            for dispObj in self.displayObjs.itervalues():
                msgStack[dispObj.msgPriority] = self.dispObj2Dict( dispObj )
        return msgStack
        

    def findNextDispObj( self ):
        nextObj = None
        now = time.time()
        for dispObj in self.displayObjs.itervalues():
            if dispObj.expiresAfterTimestamp is not None: 
                if dispObj.expiresAfterTimestamp > now: # not yet expired
                    if nextObj is None or dispObj.msgPriority < nextObj.msgPriority:
                        nextObj = dispObj
            else:
                if nextObj is None or dispObj.msgPriority < nextObj.msgPriority:
                    nextObj = dispObj
                    
        return nextObj


    def setAutoClearTimer( self, dispObj, absolute ):
        # absolute - the autoClear countdown starts after calling the action
        # relative - the autoClear countdown starts after the message is first displayed
        if (dispObj.autoClearAfterSec > 0 
            and dispObj.autoClearTimeAbsolute == absolute
        ):
            dispObj.expiresAfterTimestamp = time.time() + dispObj.autoClearAfterSec
            dispObj.autoClearTask = eg.scheduler.AddTaskAbsolute( 
                dispObj.expiresAfterTimestamp, self.DisplayObjectExpired, dispObj.msgPriority )


    @eg.LogIt
    def startDispObj( self, dispObj ):
        # init user callback function
        self.callbackManager.StartCallbackThread( dispObj )

        # display the text, with or w/o scrolling
        self.scrollManager.ScrollText( dispObj )
        
        dispObj.runState = THREAD_RUNNING


    @eg.LogIt
    def suspendDispObj( self, dispObj ):
        self.callbackManager.SuspendCallbackThread( dispObj )
        self.scrollManager.SuspendScroll( dispObj )
        dispObj.runState = THREAD_SUSPENDED
        

    @eg.LogIt
    def resumeDispObj( self, dispObj ): 
        self.callbackManager.ResumeCallbackThread( dispObj )
        self.scrollManager.ResumeScroll( dispObj )
        dispObj.runState = THREAD_RUNNING
        

    @eg.LogIt
    def stopDispObj( self, dispObj ):
        if dispObj.autoClearTask is not None:
            try:
                eg.scheduler.CancelTask( dispObj.autoClearTask )
            except Exception, exc:
                eg.PrintError( "CancelTask failed: " + repr( exc ) )
            dispObj.autoClearTask = None
            
        if dispObj.runState != THREAD_STOPPED:
            self.callbackManager.FinishCallbackThread( dispObj )
    
            if dispObj.runState == THREAD_RUNNING:
                self.scrollManager.ClearText( dispObj )
            else:
                self.scrollManager.FinishScroll( dispObj )
            
            if self.currentDispObj is not None and dispObj.msgPriority == self.currentDispObj.msgPriority:
                self.currentDispObj = None
                
            dispObj.runState = THREAD_STOPPED


    def evalExpression( self, expr ):
        t = ''
        try:
            t = eval( expr, {}, eg.globals.__dict__ )
            if not t:
                t = ''
        except Exception, exc:
            t = '{' + expr + '}'
            msg = "Error evaluating expression '" + unicode(expr) + "'"
            self.plugin.DebugPrint( 3, msg, exc )
            eg.PrintError( msg + repr( exc ))
        return t


    # debug function
    def printDisplayObject( self, dispObj ):
        print '    dispObj.msgPriority ',   dispObj.msgPriority,  \
            'autoClearTask',                dispObj.autoClearTask,  \
            'line',                         dispObj.line,  \
            'scrollMode',                   dispObj.scrollMode,  \
            'scrollSpeed',                  dispObj.scrollSpeed,  \
            'scrollWaitSec',                dispObj.scrollWaitSec,  \
            'maxScrollLoops',               dispObj.maxScrollLoops,  \
            'expiresAfterTimestamp',        dispObj.expiresAfterTimestamp,  \
            'userCallbackFunc',             dispObj.userCallbackFunc,  \
            'userCallbackFreqInSec',        dispObj.userCallbackFreqInSec,  \
            'userCallbackObj',              dispObj.userCallbackObj,  \
            'runState',                     dispObj.runState,  \
            'scrollThread',                 dispObj.scrollThread,  \
            'callbackThread',               dispObj.callbackThread,  \
            ''


    # debug function
    def printCatalogue( self, label='' ):
        if self.displayObjs is not None and len( self.displayObjs ) > 0:
            print label + ': '
            for dispObj in self.displayObjs.itervalues():
                self.printDisplayObject(dispObj)
        else:
            print label + ': <empty dict>'
    
    
    def dispObj2Dict( self, dispObj ):
        doDict = {}
        for k, v in dispObj.__dict__.iteritems():
            doDict[k] = v
        return doDict


    @eg.LogItWithReturn
    def Finish( self ):
        eg.PrintDebugNotice( 'DisplayEngine about to finish' )
        
        for dispObj in self.displayObjs.itervalues():
            self.stopDispObj( dispObj )
            
        self.displayObjs = {}
        self.currentDispObj = None
            


class ScrollManager:
    '''Manages actual displaying and scrolling of text. Supports scrolling on VFD as well as LCD displays. '''
    
    def __init__( self, plugin ):
        self.plugin = plugin

    
    def ScrollText( self, dispObj ):
        plugin = self.plugin
        plugin.DebugPrint( 1, 'ScrollManager.ScrollText ', dispObj.msgPriority, dispObj.line[0], dispObj.line[1] )
        
        if plugin.displayType == DSPN_DSP_VFD:
            dispObj.scrollThread = ScrollVfdThread( plugin, dispObj )
        
        elif plugin.displayType == DSPN_DSP_LCD:
            dispObj.scrollThread = ScrollLcdThread( plugin, dispObj )

        if dispObj.scrollThread:
            dispObj.scrollThread.start()
    
    
    def ClearText( self, dispObj ):
        plugin = self.plugin
        rc = RC_UNKNOWN
        plugin.DebugPrint( 1, 'ScrollManager.ClearText ', dispObj.msgPriority )
        
        self.FinishScroll( dispObj )
        
        if plugin.displayType == DSPN_DSP_VFD:
            rc = plugin.apiWorker.ApiSetVfdText( LPCTSTR( '' ), LPCTSTR( '' ) )
            
        elif plugin.displayType == DSPN_DSP_LCD:
            rc = plugin.apiWorker.ApiSetLcdText( LPCTSTR( '' ) )
        
        return rc
            
    
    def SuspendScroll( self, dispObj ):
        self.plugin.DebugPrint( 2, 'ScrollManager.SuspendScroll ', dispObj.msgPriority )
        if dispObj.scrollThread is not None and dispObj.scrollThread.isAlive():
            dispObj.scrollThread.Suspend()
    
    
    def ResumeScroll( self, dispObj ):
        self.plugin.DebugPrint( 2, 'ScrollManager.ResumeScroll ', dispObj.msgPriority )
        if dispObj.scrollThread is not None and dispObj.scrollThread.isAlive():
            dispObj.scrollThread.Resume()
        else:
            self.ScrollText( dispObj )
        
       
    def FinishScroll( self, dispObj ):
        self.plugin.DebugPrint( 2, 'ScrollManager.FinishScroll ', dispObj.msgPriority )
        if dispObj.scrollThread is not None and dispObj.scrollThread.isAlive():
            dispObj.scrollThread.Finish()
            dispObj.scrollThread = None
    


class CallbackManager:
    '''Manages User Callback Threads '''
    
    def __init__( self, plugin ):
        self.plugin = plugin

    
    def StartCallbackThread( self, dispObj ):
        if ( dispObj.userCallbackFunc is not None 
            and hasattr( dispObj.userCallbackFunc, '__call__' ) # it's a callable
            and dispObj.userCallbackFreqInSec > 0
        ):
            self.plugin.DebugPrint( 2, 'CallbackManager.StartCallbackThread ', dispObj.msgPriority )
            dispObj.callbackThread = UserCallbackThread( self.plugin, dispObj )
            dispObj.callbackThread.start()
            

    def SuspendCallbackThread( self, dispObj ): 
        if dispObj.callbackThread is not None and dispObj.callbackThread.isAlive():
            self.plugin.DebugPrint( 2, 'CallbackManager.SuspendCallbackThread ', dispObj.msgPriority )
            dispObj.callbackThread.Suspend()
            

    def ResumeCallbackThread( self, dispObj ): 
        if dispObj.callbackThread is not None and dispObj.callbackThread.isAlive():
            self.plugin.DebugPrint( 2, 'CallbackManager.ResumeCallbackThread ', dispObj.msgPriority )
            dispObj.callbackThread.Resume()
        else:
            self.StartCallbackThread( dispObj )
            

    def FinishCallbackThread( self, dispObj ): 
        if dispObj.callbackThread is not None and dispObj.callbackThread.isAlive():
            self.plugin.DebugPrint( 2, 'CallbackManager.FinishCallbackThread ', dispObj.msgPriority )
            dispObj.callbackThread.Finish()
            dispObj.callbackThread = None



class SuspendableThread ( Thread ):
    
    def __init__( self, name, plugin ):
        Thread.__init__( self, name=name )

        self.plugin = plugin
        self.displayEngine = plugin.displayEngine
        self.plugin.DebugPrint( 3, self.name, '__init__' )

        self.threadStop = False
        self.threadState = THREAD_STOPPED
        
        self.runEvent = Event()
        self.runEvent.set()


    @eg.LogIt
    def Suspend( self ):
        self.plugin.DebugPrint( 3, self.name, 'Suspend' )
        self.runEvent.clear()
        self.threadState = THREAD_SUSPENDED


    @eg.LogIt
    def Resume( self ):
        self.plugin.DebugPrint( 3, self.name, 'Resume' )
        self.runEvent.set()
        self.threadState = THREAD_RUNNING


    @eg.LogIt
    def Finish( self ):
        self.plugin.DebugPrint( 3, self.name, 'Finish' )
        self.threadStop = True
        self.runEvent.set()
        self.threadState = THREAD_STOPPED



class ScrollVfdThread ( SuspendableThread ):

    def __init__( self, plugin, dispObj ):
        SuspendableThread.__init__( self, "iMonVfdScrollThread", plugin )
        
        self.dispObj = dispObj
        
        if dispObj.scrollSpeed > 0:
            self.sleepTime = 1.0 / dispObj.scrollSpeed
        else:
            self.sleepTime = 1

        self.line = [ None, None ]
        
    
    @eg.LogIt
    def run( self ):
        self.threadState = THREAD_RUNNING
        plugin = self.plugin
        rc = RC_UNKNOWN

        plugin.DebugPrint( 2, 'ScrollVfdThread.run ', self.dispObj.msgPriority )
        
        t, l, ol, il, sw = ['', ''], [0, 0], [0, 0], [0, 0], [self.dispObj.scrollWaitSec, self.dispObj.scrollWaitSec]
        # t = texts
        # l = len(t[i])
        # ol = outer loop cnt: display cycles
        # il = inner loop cnt: scroll characters
        # sw = scroll wait
        
        for i in range(2):
            self.line[i] = self.displayEngine.GetParsedText( self.dispObj, i )
            t[i], l[i] = self.padText( i )
            plugin.DebugPrint( 2, 'ScrollVfdThread: initial text', i, "'" + t[i] + "'" )

        if self.dispObj.effects & EFFECT_FLY_IN:
            self.flyInEffect( t, l )
            
        while not self.threadStop:
            while not self.runEvent.isSet() and not self.threadStop:
                # thread suspended
                self.runEvent.wait( SLEEP_TIME_SLICE )
            
            if self.threadStop:
                break
            
            for i in range( 2 ):
                if self.textChanged( i ):
                    # pad / format the text
                    t[i], l[i] = self.padText( i )
                    plugin.DebugPrint( 4, 'ScrollVfdThread: text changed', i, "'" + t[i] + "'" )
                    il[i] = 0
                    ol[i] = 0

            # ...yes, show me!
            rc = plugin.apiWorker.ApiSetVfdText( LPCTSTR( t[0] ), LPCTSTR( t[1] ) )

            # the thread shall be interruptible at least every SLEEP_TIME_SLICE seconds
            secs = self.sleepTime
            napTime = SLEEP_TIME_SLICE # 0.2
            while secs > 0 and not self.threadStop:
                if napTime > secs:
                    napTime = secs
                time.sleep( napTime )
                secs -= napTime
                sw[0] -= napTime
                sw[1] -= napTime
                
            # scroll one char
            for i in range( 2 ):
                t[i], il[i], ol[i], sw[i] = self.scrollOneChar( i, l[i], t[i], il[i], ol[i], sw[i] )
                #if i == 0:
                #print i, 'scrollOneChar "' + t[i] + '"', il[i], ol[i], sw[i]
            
            if self.dispObj.autoClearAfterLoops > 0:
                if ol[0] >= self.dispObj.autoClearAfterLoops and ol[1] >= self.dispObj.autoClearAfterLoops:
                    # async call with no wait
                    self.displayEngine.Call(
                        partial( self.displayEngine._displayObjectExpired, self.dispObj.msgPriority ))
                
        self.threadState = THREAD_STOPPED
        plugin.DebugPrint( 2, 'ScrollVfdThread stopped ', self.dispObj.msgPriority )
        return rc

    
    def textChanged( self, i ):
        parsed = self.displayEngine.GetParsedText( self.dispObj, i )
        if self.line[i] != parsed:
            self.line[i] = parsed
            return True
        else:
            return False


    def padText( self, i ):
        t = unicode( self.line[i] ) if self.line[i] is not None else ''
        l = len( t )
        
        if len( t.strip() ) > 0:
            if self.dispObj.scrollMode == SCROLL_MODE_ENDLESS_LOOP:
                t = t + ( '  ' if l > VFD_NUM_CHAR else ' ' * ( VFD_NUM_CHAR - l ) )
        else:
            t = ''
        l = len( t )

        return t, l
    
    
    def scrollOneChar( self, i, l, t, il, ol, wait ):
        if self.dispObj.maxScrollLoops > 0 and ol >= self.dispObj.maxScrollLoops:
            il += 1
            if il >= l:
                ol += 1
                il = 0 
            return t, il, ol, 0
            
        if self.dispObj.scrollMode == SCROLL_MODE_ENDLESS_LOOP:
            il += 1
            if il >= l:
                ol += 1
                il = 0 
            t = t if l <= VFD_NUM_CHAR else t[1:] + t[0:1]
            return t, il, ol, wait
        
        elif self.dispObj.scrollMode == SCROLL_MODE_STOP_SCROLL_STOP:
            
            if l > VFD_NUM_CHAR and wait <= 0:
                
                if il == l - VFD_NUM_CHAR: # end scroll
                    #print 'end scroll!'
                    il += 1
                    wait = self.dispObj.scrollWaitSec

                elif il > 0 and il % (l - VFD_NUM_CHAR +1) == 0: # start over
                    #print 'start over!'
                    il = 0
                    ol += 1
                    wait = self.dispObj.scrollWaitSec
                    t = self.line[i]
                
                else:
                    il += 1
                    t = t[1:] + t[0:1]
                    wait = 0
                    #print il, 'il % (l - VFD_NUM_CHAR)', il % (l - VFD_NUM_CHAR), (l - VFD_NUM_CHAR)

                return t, il, ol, wait

            elif wait > 0:
                return t, il, ol, wait
                
            else:
                il += 1
                if il >= l:
                    ol += 1
                    il = 0 
                return t, il, ol, wait
        
        else:
            # increasing loop counters is necessary for 'auto clear after loops' feature
            il += 1
            if il >= l:
                ol += 1
                il = 0 
            return t, il, ol, 0
    
    
    def flyInEffect( self, t, l ):
        it, stb, ste, ot = ['', ''], ['', ''], ['', ''], ['', '']
        now, last = 0.0, 0
        slp = EFFECT_FLY_IN_DELAY
        
        for i in range(2):
            # pad with blanks
            it[i] = t[i]
            if l[i] < VFD_NUM_CHAR:
                it[i] = it[i] + ' ' * ( VFD_NUM_CHAR - l[i] )
                
        for ol in range( VFD_NUM_CHAR ):
            for i in range(2):
                # static: begin + end string
                stb[i] = it[i][0:ol]
                ste[i] = it[i][ol:ol+1]
                
            for il in range( VFD_NUM_CHAR-1, ol, -1 ):
                for i in range(2):
                    ot[i] = stb[i] + ' ' * il + ste[i]
                    
                self.plugin.apiWorker.ApiSetVfdText( LPCTSTR( ot[0] ), LPCTSTR( ot[1] ) )
                
                if self.threadStop or not self.runEvent.isSet():
                    return

                now = time.time()
                d = now - last
                if last > 0 and d < slp:
                    time.sleep(slp - d)
                last = now



class ScrollLcdThread ( SuspendableThread ):

    def __init__( self, plugin, dispObj ):
        SuspendableThread.__init__( self, "iMonLcdScrollThread", plugin )
        
        self.dispObj = dispObj
        self.line = [ None, None ]
        
    
    @eg.LogIt
    def run( self ):
        self.threadState = THREAD_RUNNING
        plugin = self.plugin
        rc = RC_UNKNOWN

        plugin.DebugPrint( 2, 'ScrollLcdThread.run ', self.dispObj.msgPriority )

        t = ''  # final display text
        ol = 0  # outer loop count
        if self.textChanged( ):
            t = self.padText( )
            plugin.DebugPrint( 2, 'ScrollLcdThread: initial text', "'" + t + "'" )
        
        while not self.threadStop:
            while not self.runEvent.isSet() and not self.threadStop:
                # thread suspended
                self.runEvent.wait( SLEEP_TIME_SLICE )
            
            if self.threadStop:
                break
            
            if self.textChanged( ):
                # pad / format the text
                t = self.padText( )
                ol = 0
                plugin.DebugPrint( 4, 'ScrollLcdThread: textChanged:', t )

            rc = self.setLcdTextAndScrollWait(plugin, t, ol, True)
            
            while not plugin.lcdEvent.isSet() and self.scrollContinue():
                # wait for the signal - it is set by the DSPN_LCD_TEXT_SCROLL_DONE event or by self.Finish()
                plugin.lcdEvent.wait( SLEEP_TIME_SLICE )

            if self.threadStop:
                break
            
            rc = self.setLcdTextAndScrollWait(plugin, t, ol, False)

            ol += 1
            if self.dispObj.autoClearAfterLoops > 0:
                if ol >= self.dispObj.autoClearAfterLoops:
                    # async call with no wait
                    self.displayEngine.Call(
                        partial( self.displayEngine._displayObjectExpired, self.dispObj.msgPriority ))
                

        self.threadState = THREAD_STOPPED
        plugin.DebugPrint( 2, 'ScrollLcdThread stopped ', self.dispObj.msgPriority )
        return rc
    
    
    def scrollContinue( self ):
        return not self.threadStop and self.runEvent.isSet()


    def textChanged( self ):
        textChanged = False
        for i in range( 2 ):
            parsed = self.displayEngine.GetParsedText( self.dispObj, i )
            if self.line[i] != parsed:
                self.line[i] = parsed
                textChanged = True
        return textChanged


    def padText( self ):
        pad = ['', '']
        for i in range(2):
            pad[i] = unicode( self.line[i] ) if self.line[i] is not None else ''
        t = pad[0]
        if pad[1] is not None and len( pad[1].strip() ) > 0:
            t = t + LCD_CONCAT_CHAR + pad[1]
        return t


    @eg.LogIt
    def setLcdTextAndScrollWait( self, plugin, t, ol, startScroll ):
        '''Displays the text on the lcd and stops lcd scrolling at the beginning or at the end, depending on scroll parameters'''
        rc = RC_UNKNOWN
        lpcstr = LPCTSTR( t )

        wait = 0
        if LCD_NO_SCROLL_PULSE > 0:
            if self.dispObj.scrollMode == SCROLL_MODE_STOP_SCROLL_STOP:
                wait = self.dispObj.scrollWaitSec
    
            if startScroll:
                if self.dispObj.maxScrollLoops > 0 and ol >= self.dispObj.maxScrollLoops:
                    wait = sys.maxint
                elif self.dispObj.scrollMode == SCROLL_MODE_NO_SCROLL:
                    wait = sys.maxint

        plugin.DebugPrint( 1, 'setLcdTextAndScrollWait: start=', startScroll, ', wait=', wait, ', t=', t, ', LCD_NO_SCROLL_PULSE=', LCD_NO_SCROLL_PULSE )
        if wait > 0:        
            while wait > 0 and self.scrollContinue():
                if startScroll:
                    # The lcd automatically starts scrolling after a short time
                    # By refreshing the lcd in a shorter period the autostart scrolling can be delayed (todo: still experimental!)
                    self.plugin.lcdEvent.clear()
                    rc = self.plugin.apiWorker.ApiSetLcdText( lpcstr )
                # else:
                    # The lcd stops scrolling when the text arrives at the end, so the tail is displayed already
                time.sleep( LCD_NO_SCROLL_PULSE )
                wait -= LCD_NO_SCROLL_PULSE
 
        elif wait == 0 and startScroll and self.scrollContinue():
            self.plugin.lcdEvent.clear()
            rc = self.plugin.apiWorker.ApiSetLcdText( lpcstr )

        return rc


    @eg.LogIt
    def Finish( self ):
        self.plugin.lcdEvent.set()
        SuspendableThread.Finish( self )



class UserCallbackThread ( SuspendableThread ):

    def __init__( self, plugin, dispObj ):
        SuspendableThread.__init__( self, "iMONDisplayScrollThread", plugin )
        self.plugin.DebugPrint( 3, 'UserCallbackThread.__init__' )

        self.dispObj = dispObj
        
        self.userCallbackFunc = dispObj.userCallbackFunc
        self.userCallbackObj = dispObj.userCallbackObj

        if dispObj.userCallbackFreqInSec and dispObj.userCallbackFreqInSec > 0:
            self.userCallbackFreqInSec = dispObj.userCallbackFreqInSec
            self.sleepTime = dispObj.userCallbackFreqInSec
        else:
            self.userCallbackFreqInSec = -1

    @eg.LogIt
    def run( self ):
        self.threadState = THREAD_RUNNING
        plugin = self.plugin
        dispObj = self.dispObj
        line1, line2 = '', ''

        # this code was hard to write, so it's ok if it's hard to read :)
        try:
            while not self.threadStop:
                while not self.runEvent.isSet() and not self.threadStop:
                    # thread suspended
                    self.runEvent.wait( SLEEP_TIME_SLICE )
                
                if self.threadStop:
                    break
            
                while not plugin.actionEvent.isSet() and not self.threadStop:
                    # another action or macro is executing - wait, otherwise we risk a deadlock + timeout, especially before suspend / after resume
                    plugin.actionEvent.wait( SLEEP_TIME_SLICE )
                
                if self.threadStop:
                    break
        
                try:
                    # Call the user callback in the action thread! Since the user callback itself might call other actions.
                    line1, line2 = eg.actionThread.CallWait( 
                        partial( dispObj.userCallbackFunc, plugin.displayTypeStr, dispObj.msgPriority, dispObj.userCallbackObj ), timeout=CALLBACK_TIMEOUT ) 

                    plugin.DebugPrint( 4, 'UserCallbackThread: after calling userCallbackFunc. result=', line1, line2 )

                except Exception, exc:
                    msg = 'Failed to call user callback, exception=' + repr( exc )
                    eg.PrintError( msg )
                    line1, line2 = '', ''
                    
                if self.threadStop:
                    break

                # synchronized write back of the result - it will be picked up by the ScrollThread
                plugin.displayEngine.SetDisplayText( dispObj.msgPriority, line1, line2 )

                if self.userCallbackFreqInSec > 0:
                    # the thread shall be interruptible once a second
                    secs = self.sleepTime
                    napTime = SLEEP_TIME_SLICE
                    while secs > 0 and not self.threadStop:
                        if napTime > secs:
                            napTime = secs
                        time.sleep( napTime )
                        secs -= napTime
                else:
                    self.threadStop = True
                    break
        except Exception, exc:
            msg = 'User callback thread failed, exception=' + repr( exc )
            eg.PrintError( msg )
            raise exc

        plugin.DebugPrint( 3, 'UserCallbackThread.Finished' )
        self.threadState = THREAD_STOPPED



class AcquireDisplay( eg.ActionBase ):
    name = "Acquire Display"
    description = """<rst>
       Acquires the display.
       
       Grants exclusive access to the display, i.e. no other application can 
       acquire it until calling action *Release Display* or termination of EventGhost.
        
       This action has to be called as the first action before calling *Display Text*. 
       However, the display is also implicitly acquired when the *Display Text* action is called, 
       therefore it's optional to call this action first.
    """
    
    @eg.LogIt
    def __call__( self ):
        if not self.plugin.started:
            return False
        return self.plugin.InitDisplay()



class DisplayText( eg.ActionBase ):
    name = "Display Text"
    description = (
         "Displays an arbitrary text on the LCD or VFD display. See description page for details."
         "\n\n"
    ) + GetFileAsStr("DisplayText.html")

    @eg.LogIt
    def __call__( self,
        msgPriority=DEFAULT_PRIORITY,
        line1=None, 
        line2=None,
        scrollMode=DEFAULT_SCROLL_MODE,
        scrollSpeed=DEFAULT_SCROLL_SPEED,
        scrollWaitSec=DEFAULT_SCROLL_WAIT,
        maxScrollLoops=DEFAULT_SCROLL_LOOPS,
        autoClearAfterSec=DEFAULT_AUTO_CLEAR_SECS,
        autoClearAfterLoops=DEFAULT_AUTO_CLEAR_LOOPS,
        autoClearTimeAbsolute=True,
        effects=EFFECT_NONE,
        userCallbackFunc=None,
        userCallbackFreqInSec=DEFAULT_CALLBACK_FREQUENCY,
        userCallbackObj=None
    ):
        if not self.plugin.started or self.plugin.InitDisplay() != DSP_SUCCEEDED:
            return False
            
        dispObj = self.plugin.displayEngine.CreateDisplayObject( msgPriority, [ line1, line2 ] )
        
        if scrollSpeed <= 0:
            scrollMode      = SCROLL_MODE_NO_SCROLL
            scrollWaitSec   = -1
            maxScrollLoops  = -1

        if autoClearAfterSec > 0:
            dispObj.autoClearAfterSec   = autoClearAfterSec
            dispObj.autoClearAfterLoops = DEFAULT_AUTO_CLEAR_LOOPS
        elif autoClearAfterLoops > 0:
            dispObj.autoClearAfterLoops = autoClearAfterLoops
            dispObj.autoClearAfterSec   = DEFAULT_AUTO_CLEAR_SECS
        else:
            dispObj.autoClearAfterSec   = DEFAULT_AUTO_CLEAR_SECS
            dispObj.autoClearAfterLoops = DEFAULT_AUTO_CLEAR_LOOPS
        
        dispObj.autoClearTimeAbsolute   = autoClearTimeAbsolute
        dispObj.effects                 = effects
        dispObj.scrollMode              = scrollMode
        dispObj.scrollSpeed             = scrollSpeed
        dispObj.scrollWaitSec           = scrollWaitSec
        dispObj.maxScrollLoops          = maxScrollLoops
        dispObj.userCallbackFunc        = userCallbackFunc
        dispObj.userCallbackFreqInSec   = userCallbackFreqInSec
        dispObj.userCallbackObj         = userCallbackObj
        
        self.plugin.displayEngine.DisplayText( dispObj )
        
        
    class Text:
        msgBoxLabel = "Static Text"
        line1Label = "VFD display line 1"
        line2Label = "VFD display line 2"
        lcdLineLabel = "LCD display message"
        box1Footer1 = "Hint: Dynamic texts can either be implemented using variables like {eg.globals.MyVar}"
        box1Footer2 = "or by using a callback function. See help page for details."

        advancedModeLabel = "Advanced Settings"
        
        prioBoxLabel = "Display Priority"
        prioLabel = "Display priority"
        prioFooter1 = "Always the message with the highest priority (i.e. the smallest number) will be displayed, it overlays messages with lower priorities."
        prioFooter2 = "As soon as it gets cleared, the message with the next lower priority will be displayed."
        
        scrollBoxLabel = "Scroll Settings"
        scrollNoScrollLabel = "Don't scroll. Long messages will be clipped."
        scrollContLabel = "Scroll continuously in an endless loop"
        scrollWaitLabel = "Wait at the beginning -> Scroll -> Wait at the end"
        scrollWaitTimeLabel = "Wait time at the beginning and end"
        
        scrollSpeedLabel = "Scroll speed"
        scrollLoopsLabel = "Scroll Loops"
        scrollSteadilyLabel = "Scroll continuously, never stop"
        scrollNtimesLabel1 = "Scroll"
        scrollNtimesLabel2 = "times, then stop scrolling"
        
        expiryBoxLabel = "Auto Clear Message"
        expiryNoneLabel = "Message does not expire"
        expiryExpiryLabel1 = "Auto clear message after"
        expiryExpiryLabel2 = "seconds"
        expiryExpiryLabel3 = "scroll loops"
        absoluteTimeLabel = "Expiry time is absolute, i.e. time counts when calling this action. Otherwise, time counts when message is shown."
        
        cpsUnitLabel = "[characters/second] (setting has no effect on LCD screens)"
        secUnitLabel = "[seconds]"

        effectsBoxLabel = "Display Effects (only supported on VFD screens)"
        flyInLabel = "Fly-In at the beginning"
        flyOutLabel = "Fly-Out at the end"


    @eg.LogIt
    def Configure( self, 
        msgPriority=DEFAULT_PRIORITY,
        line1='',
        line2='',
        scrollMode=DEFAULT_SCROLL_MODE,
        scrollSpeed=DEFAULT_SCROLL_SPEED,
        scrollWaitSec=DEFAULT_SCROLL_WAIT,
        maxScrollLoops=DEFAULT_SCROLL_LOOPS,
        autoClearAfterSec=DEFAULT_AUTO_CLEAR_SECS,
        autoClearAfterLoops=DEFAULT_AUTO_CLEAR_LOOPS,
        autoClearTimeAbsolute=True,
        effects=EFFECT_NONE,
        userCallbackFunc=None,
        userCallbackFreqInSec=DEFAULT_CALLBACK_FREQUENCY,
        userCallbackObj=None
    ) :
    
        class StaticTextPanel ( wx.Panel ):
            def __init__(self, parent ):
                wx.Panel.__init__( self, parent )

                self.line1TextCtrl = wx.TextCtrl( self, size=( 500,-1 ) )
                self.line1TextCtrl.SetValue( line1 )
                line1Label = text.lcdLineLabel
                    
                if plugin.displayType == DSPN_DSP_VFD:
                    line1Label = text.line1Label 
                    self.line2TextCtrl = wx.TextCtrl( self, size=( 500,-1 ) )
                    self.line2TextCtrl.SetValue( line2 )
            
                self.box1FooterLabel1 = wx.StaticText( self, -1, text.box1Footer1 )
                self.box1FooterLabel2 = wx.StaticText( self, -1, text.box1Footer2 )
                
                gridBagSizer = wx.GridBagSizer( 5, 5 )
                rowcount = 0
        
                gridBagSizer.Add( wx.StaticText( self, -1, line1Label ), ( rowcount, 0 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                gridBagSizer.Add( self.line1TextCtrl, ( rowcount, 1 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                rowcount += 1
                
                if plugin.displayType == DSPN_DSP_VFD:
                    gridBagSizer.Add( wx.Size( 20, 0 ), ( rowcount, 0 ) )
                    rowcount += 1
                    gridBagSizer.Add( wx.StaticText( self, -1, text.line2Label ), ( rowcount, 0 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                    gridBagSizer.Add( self.line2TextCtrl, ( rowcount, 1 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                    rowcount += 1

                gridBagSizer.Add( self.box1FooterLabel1, ( rowcount, 1 ), span=( 1, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( self.box1FooterLabel2, ( rowcount, 1 ), span=( 1, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                
                staticBox = wx.StaticBox(self, -1, text.msgBoxLabel)
                staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
                staticBoxSizer.Add(gridBagSizer, 1, flag=wx.EXPAND)
                
                self.SetSizer( staticBoxSizer )


        class DispPrioPanel ( wx.Panel ):
            def __init__(self, parent ):
                wx.Panel.__init__( self, parent )
                
                self.msgPrioNumCtrl = eg.SpinNumCtrl(self, value=msgPriority, min=1, max=999, fractionWidth=0, integerWidth=3)
        
                gridBagSizer = wx.GridBagSizer( 5, 5 )
                rowcount = 0
        
                gridBagSizer.Add( wx.StaticText( self, -1, text.prioLabel ), ( rowcount, 0 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                gridBagSizer.Add( self.msgPrioNumCtrl, ( rowcount, 1 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                rowcount += 1
                
                gridBagSizer.Add( wx.StaticText( self, -1, text.prioFooter1 ), ( rowcount, 0 ), span=( 1, 2 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.prioFooter2 ), ( rowcount, 0 ), span=( 1, 2 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                
                staticBox = wx.StaticBox(self, -1, text.prioBoxLabel)
                staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
                staticBoxSizer.Add(gridBagSizer, 1, flag=wx.EXPAND)
                
                self.SetSizer( staticBoxSizer )


        class ScrollSettingsPanel ( wx.Panel ):
            def OnScrollModeChange(self, event):
                self.waitTimeNumCtrl.Enable( self.stopStartScrollRbCtrl.GetValue()  )
                
                scroll = not self.noScrollRbCtrl.GetValue()
                self.scrollSpeedNumCtrl.Enable ( scroll )
                self.steadilyRbCtrl.Enable( scroll )
                self.scrollNtimesRbCtrl.Enable( scroll )
                
                enabled = self.scrollNtimesRbCtrl.GetValue()
                self.maxScrollsNumCtrl.Enable( enabled and scroll )

                if enabled:
                    val = self.maxScrollsNumCtrl.GetValue()
                    self.maxScrollsNumCtrl.SetValue( val if val > 0 else 1 )
                else:
                    self.maxScrollsNumCtrl.SetValue( DEFAULT_SCROLL_LOOPS )
                
                event.Skip()


            def __init__(self, parent ):
                wx.Panel.__init__( self, parent )

                self.noScrollRbCtrl = wx.RadioButton( self, -1, text.scrollNoScrollLabel, style = wx.RB_GROUP )
                self.noScrollRbCtrl.SetValue( scrollMode == SCROLL_MODE_NO_SCROLL )
                self.noScrollRbCtrl.Bind(wx.EVT_RADIOBUTTON, self.OnScrollModeChange)
        
                self.endlessScrollRbCtrl = wx.RadioButton( self, -1, text.scrollContLabel )
                self.endlessScrollRbCtrl.SetValue( scrollMode == SCROLL_MODE_ENDLESS_LOOP )
                self.endlessScrollRbCtrl.Bind(wx.EVT_RADIOBUTTON, self.OnScrollModeChange)
        
                self.stopStartScrollRbCtrl = wx.RadioButton( self, -1, text.scrollWaitLabel )
                self.stopStartScrollRbCtrl.SetValue( scrollMode == SCROLL_MODE_STOP_SCROLL_STOP )
                self.stopStartScrollRbCtrl.Bind(wx.EVT_RADIOBUTTON, self.OnScrollModeChange)
        
                self.scrollSpeedNumCtrl = eg.SpinNumCtrl( self, value=scrollSpeed, min=0, max=50, fractionWidth=1, integerWidth=2 )
                self.waitTimeNumCtrl = eg.SpinNumCtrl( self, value=scrollWaitSec, min=0, max=999, fractionWidth=1, integerWidth=3 )
                
                self.steadilyRbCtrl = wx.RadioButton( self, -1, text.scrollSteadilyLabel, style = wx.RB_GROUP )
                self.steadilyRbCtrl.SetValue( maxScrollLoops <= 0 )
                self.steadilyRbCtrl.Bind( wx.EVT_RADIOBUTTON, self.OnScrollModeChange )
        
                self.scrollNtimesRbCtrl = wx.RadioButton( self, -1, text.scrollNtimesLabel1 )
                self.scrollNtimesRbCtrl.SetValue( maxScrollLoops > 0 )
                self.scrollNtimesRbCtrl.Bind( wx.EVT_RADIOBUTTON, self.OnScrollModeChange )
        
                self.maxScrollsNumCtrl = eg.SpinNumCtrl( self, value=maxScrollLoops, min=-1, max=999, fractionWidth=0, integerWidth=3 )
                
                gridBagSizer = wx.GridBagSizer( 5, 5 )
                rowcount = 0

                gridBagSizer.Add( self.noScrollRbCtrl, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                rowcount += 1
                gridBagSizer.Add( self.endlessScrollRbCtrl, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                rowcount += 1
                gridBagSizer.Add( self.stopStartScrollRbCtrl, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                rowcount += 1
                
                innerFGSizer = wx.FlexGridSizer(rows=1, cols=4, hgap=5, vgap=5)
                innerFGSizer.Add(wx.Size(leftindent, 0))
                innerFGSizer.Add(wx.StaticText(self, -1, text.scrollWaitTimeLabel), flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.waitTimeNumCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(wx.StaticText(self, -1, text.secUnitLabel), flag=wx.ALIGN_CENTER_VERTICAL) 
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 0 ) )
                rowcount += 1
                innerFGSizer = wx.FlexGridSizer(rows=1, cols=3, hgap=5, vgap=5)
                innerFGSizer.Add(wx.StaticText(self, -1, text.scrollSpeedLabel), flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.scrollSpeedNumCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(wx.StaticText(self, -1, text.cpsUnitLabel), flag=wx.ALIGN_CENTER_VERTICAL) 
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1

                
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 0 ) )
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.scrollLoopsLabel ), ( rowcount, 0 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( self.steadilyRbCtrl, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                rowcount += 1

                innerFGSizer = wx.FlexGridSizer(rows=1, cols=3, hgap=5, vgap=5)
                innerFGSizer.Add(self.scrollNtimesRbCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.maxScrollsNumCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(wx.StaticText(self, -1, text.scrollNtimesLabel2), flag=wx.ALIGN_CENTER_VERTICAL) 
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1

                self.staticBox = wx.StaticBox(self, -1, text.scrollBoxLabel)
                staticBoxSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
                staticBoxSizer.Add(gridBagSizer, 1, flag=wx.EXPAND)
                
                self.SetSizer( staticBoxSizer )


        class MsgExpiryPanel ( wx.Panel ):
            def OnAutoClearChange(self, event):
                secEnabled = self.expirySecRbCtrl.GetValue()
                loopEnabled = self.expiryLoopsRbCtrl.GetValue()
                
                self.expireTimeNumCtrl.Enable( secEnabled )
                if secEnabled:
                    val = self.expireTimeNumCtrl.GetValue()
                    self.expireTimeNumCtrl.SetValue( val if val > 0 else 3 )
                else:
                    self.expireTimeNumCtrl.SetValue( DEFAULT_AUTO_CLEAR_SECS )

                self.absoluteTimeCB.Enable( secEnabled )
                    
                self.expireLoopsNumCtrl.Enable( loopEnabled )
                if loopEnabled:
                    val = self.expireLoopsNumCtrl.GetValue()
                    self.expireLoopsNumCtrl.SetValue( val if val > 0 else 1 )
                else:
                    self.expireLoopsNumCtrl.SetValue( DEFAULT_AUTO_CLEAR_LOOPS )
                    
                event.Skip()


            def __init__(self, parent ):
                wx.Panel.__init__( self, parent )

                self.noExpiryRbCtrl = wx.RadioButton( self, -1, text.expiryNoneLabel, style = wx.RB_GROUP )
                self.noExpiryRbCtrl.SetValue( autoClearAfterSec <= 0 )
                self.noExpiryRbCtrl.Bind( wx.EVT_RADIOBUTTON, self.OnAutoClearChange )
        
                self.expirySecRbCtrl = wx.RadioButton( self, -1, text.expiryExpiryLabel1 )
                self.expirySecRbCtrl.SetValue( autoClearAfterSec > 0 )
                self.expirySecRbCtrl.Bind( wx.EVT_RADIOBUTTON, self.OnAutoClearChange )
        
                self.expireTimeNumCtrl = eg.SpinNumCtrl( self, value=autoClearAfterSec, min=-1, max=999, fractionWidth=1, integerWidth=3)

                self.expiryLoopsRbCtrl = wx.RadioButton( self, -1, text.expiryExpiryLabel1 )
                self.expiryLoopsRbCtrl.SetValue( autoClearAfterLoops > 0 )
                self.expiryLoopsRbCtrl.Bind( wx.EVT_RADIOBUTTON, self.OnAutoClearChange )
        
                self.expireLoopsNumCtrl = eg.SpinNumCtrl( self, value=autoClearAfterLoops, min=-1, max=999, fractionWidth=0, integerWidth=3)

                self.absoluteTimeCB = wx.CheckBox( self, -1, text.absoluteTimeLabel )
                self.absoluteTimeCB.SetValue( autoClearTimeAbsolute )
                
                gridBagSizer = wx.GridBagSizer( 5, 5 )
                rowcount = 0
        
                gridBagSizer.Add( self.noExpiryRbCtrl, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                rowcount += 1

                innerFGSizer = wx.FlexGridSizer(rows=1, cols=3, hgap=5, vgap=5)
                innerFGSizer.Add(self.expirySecRbCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.expireTimeNumCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(wx.StaticText(self, -1, text.expiryExpiryLabel2), flag=wx.ALIGN_CENTER_VERTICAL) 
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1

                innerFGSizer = wx.FlexGridSizer(rows=1, cols=2, hgap=5, vgap=5)
                innerFGSizer.Add(wx.Size(leftindent, 0))
                innerFGSizer.Add(self.absoluteTimeCB, flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1

                innerFGSizer = wx.FlexGridSizer(rows=1, cols=3, hgap=5, vgap=5)
                innerFGSizer.Add(self.expiryLoopsRbCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.expireLoopsNumCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(wx.StaticText(self, -1, text.expiryExpiryLabel3), flag=wx.ALIGN_CENTER_VERTICAL) 
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1

                staticBox = wx.StaticBox(self, -1, text.expiryBoxLabel)
                staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
                staticBoxSizer.Add(gridBagSizer, 1, flag=wx.EXPAND)
                
                self.SetSizer( staticBoxSizer )


        class EffectsPanel ( wx.Panel ):

            def __init__(self, parent ):
                wx.Panel.__init__( self, parent )

                self.flyInCB = wx.CheckBox( self, -1, text.flyInLabel )
                self.flyInCB.SetValue( effects & EFFECT_FLY_IN )
                
                #self.flyOutCB = wx.CheckBox( self, -1, text.flyOutLabel )
                #self.flyOutCB.SetValue( effects & EFFECT_FLY_OUT )
                
                gridBagSizer = wx.GridBagSizer( 5, 5 )
                rowcount = 0
        
                gridBagSizer.Add( self.flyInCB, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                rowcount += 1

                #gridBagSizer.Add( self.flyOutCB, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
                #rowcount += 1

                staticBox = wx.StaticBox(self, -1, text.effectsBoxLabel)
                staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
                staticBoxSizer.Add(gridBagSizer, 1, flag=wx.EXPAND)
                
                self.SetSizer( staticBoxSizer )


        def onAdvancedButton( event ):
            if advancedButton.GetValue():
                dispPrioPanel.Show()
                scrollSettingsPanel.Show()
                msgExpiryPanel.Show()
                effectsPanel.Show()
                staticTextPanel.box1FooterLabel1.Show()
                staticTextPanel.box1FooterLabel2.Show()
            else:
                dispPrioPanel.Hide()
                scrollSettingsPanel.Hide()
                msgExpiryPanel.Hide()
                effectsPanel.Hide()
                staticTextPanel.box1FooterLabel1.Hide()
                staticTextPanel.box1FooterLabel2.Hide()
                            
        def onWindowShow( event ):
            advancedButton.SetValue( msgPriority != DEFAULT_PRIORITY )
            onAdvancedButton( wx.CommandEvent() )

        plugin = self.plugin
        text = self.Text
        panel = eg.ConfigPanel()
        dlgWindow = panel.GetTopLevelParent()
        leftindent = 12
        plugin.InitDisplay( initWaitTime=4 )
        
        staticTextPanel = StaticTextPanel( panel )    
        dispPrioPanel = DispPrioPanel( panel )
        scrollSettingsPanel = ScrollSettingsPanel( panel )
        msgExpiryPanel = MsgExpiryPanel( panel )
        effectsPanel = EffectsPanel( panel )

        advancedButton = wx.ToggleButton(panel, -1, text.advancedModeLabel )
        advancedButton.Bind(wx.EVT_TOGGLEBUTTON, onAdvancedButton)
        advancedButton.SetValue( True )

        tableSizer = wx.GridBagSizer(5, 5)
        tableSizer.AddGrowableCol( 0 )
        rowCount = 0
        tableSizer.Add(staticTextPanel, (rowCount,0), flag=wx.EXPAND)
        tableSizer.AddGrowableRow(rowCount)
        rowCount += 1
        tableSizer.Add( advancedButton, (rowCount,0), flag=wx.ALIGN_RIGHT )
        rowCount += 1
        tableSizer.Add(dispPrioPanel, (rowCount,0), flag=wx.EXPAND)
        tableSizer.AddGrowableRow(rowCount)
        rowCount += 1
        tableSizer.Add(scrollSettingsPanel, (rowCount,0), flag=wx.EXPAND)
        tableSizer.AddGrowableRow(rowCount)
        rowCount += 1
        tableSizer.Add(msgExpiryPanel, (rowCount,0), flag=wx.EXPAND)
        tableSizer.AddGrowableRow(rowCount)
        rowCount += 1
        tableSizer.Add(effectsPanel, (rowCount,0), flag=wx.EXPAND)
        tableSizer.AddGrowableRow(rowCount)
        rowCount += 1

        panel.sizer.Add( tableSizer, 1, flag=wx.EXPAND )
        dlgWindow.Bind( wx.EVT_SHOW, onWindowShow )
        
        scrollSettingsPanel.OnScrollModeChange( wx.CommandEvent() )
        msgExpiryPanel.OnAutoClearChange( wx.CommandEvent() )

        while panel.Affirmed():
            line1 = unicode( staticTextPanel.line1TextCtrl.GetValue() )
            if plugin.displayType == DSPN_DSP_VFD:
                line2 = unicode( staticTextPanel.line2TextCtrl.GetValue() )
            else:
                line2 = ''
                
            msgPriority = dispPrioPanel.msgPrioNumCtrl.GetValue()
            if msgPriority == '':
                msgPriority = DEFAULT_PRIORITY
                
            scrollMode = SCROLL_MODE_NO_SCROLL
            if scrollSettingsPanel.endlessScrollRbCtrl.GetValue():
                scrollMode = SCROLL_MODE_ENDLESS_LOOP
            elif scrollSettingsPanel.stopStartScrollRbCtrl.GetValue():
                scrollMode = SCROLL_MODE_STOP_SCROLL_STOP
                
            scrollSpeed = scrollSettingsPanel.scrollSpeedNumCtrl.GetValue()
            scrollWaitSec = scrollSettingsPanel.waitTimeNumCtrl.GetValue()

            if scrollSettingsPanel.scrollNtimesRbCtrl.GetValue():
                maxScrollLoops = scrollSettingsPanel.maxScrollsNumCtrl.GetValue()
            else:
                maxScrollLoops = DEFAULT_SCROLL_LOOPS
            
            autoClearAfterSec = msgExpiryPanel.expireTimeNumCtrl.GetValue()
            autoClearAfterLoops = msgExpiryPanel.expireLoopsNumCtrl.GetValue()
            autoClearTimeAbsolute = msgExpiryPanel.absoluteTimeCB.GetValue()
            
            effects = EFFECT_NONE
            if effectsPanel.flyInCB.GetValue():
                effects = effects | EFFECT_FLY_IN
            #if effectsPanel.flyOutCB.GetValue():
            #    effects = effects | EFFECT_FLY_OUT

            panel.SetResult( 
                msgPriority,
                line1,
                line2,
                scrollMode,
                scrollSpeed,
                scrollWaitSec,
                maxScrollLoops,
                autoClearAfterSec,
                autoClearAfterLoops,
                autoClearTimeAbsolute,
                effects,
                userCallbackFunc,
                userCallbackFreqInSec,
                userCallbackObj
            )


    def GetLabel(self, 
        msgPriority,
        line1,
        line2,
        *dummyArgs
    ):
        ret = '[P' + str(msgPriority) + '] '
        ret = ret + '"' + unicode(line1) + '"' if line1 is not None else ''
        l2 = unicode(line2) if line2 is not None else ''
        if l2 != '':
            ret = ret + LCD_CONCAT_CHAR + '"' + l2 + '"'
        return ret



class ClearText( eg.ActionBase ):
    name = "Clear text"
    description = """<rst>
        Clears text on the display.
        
        This action is the counterpart of action *Display Text*. 
        Either the currently displayed message can be deleted or a message with a specific display priority.
        
        Optionally, if the last message has been cleared, the display can be released at the same time
        (see action *Release Display* for more details).
    """
    
    @eg.LogIt
    def __call__( self, 
        msgPriority=None,
        releaseDisplay=False
    ):
        if not self.plugin.started or self.plugin.InitDisplay() != DSP_SUCCEEDED:
            return False
            
        lastObjDeleted = self.plugin.displayEngine.ClearText( msgPriority )
        if lastObjDeleted and releaseDisplay:
            eg.plugins.iMON_Display.ReleaseDisplay()


    class Text:
        clearCurrentLabel = "Clear the current message"
        clearPrioLabel = "Clear the message with priority"
        releaseDisplayLabel = "Release the display if last message cleared"


    @eg.LogIt
    def Configure( self, 
        msgPriority=None,
        releaseDisplay=True
    ) :
        def OnClearModeChange( event ):
            enabled = clearPrioRbCtrl.GetValue()
            msgPrioNumCtrl.Enable( enabled )
            event.Skip()
        
        plugin = self.plugin
        text = self.Text
        panel = eg.ConfigPanel()
        
        if plugin.InitDisplay() != DSP_SUCCEEDED:
            return False

        clearCurrRbCtrl = wx.RadioButton( panel, -1, text.clearCurrentLabel, style = wx.RB_GROUP )
        clearCurrRbCtrl.SetValue( msgPriority is None )
        clearCurrRbCtrl.Bind( wx.EVT_RADIOBUTTON, OnClearModeChange )

        clearPrioRbCtrl = wx.RadioButton( panel, -1, text.clearPrioLabel )
        clearPrioRbCtrl.SetValue( msgPriority is not None )
        clearPrioRbCtrl.Bind( wx.EVT_RADIOBUTTON, OnClearModeChange )
        
        msgPrioNumCtrl = panel.SpinNumCtrl( msgPriority if msgPriority is not None else DEFAULT_PRIORITY, min=1, max=999, fractionWidth=0, integerWidth=3)
        releaseDispCB = wx.CheckBox( panel, -1, text.releaseDisplayLabel )
        releaseDispCB.SetValue( releaseDisplay )
        

        gridBagSizer = wx.GridBagSizer( 5, 5 )
        rowcount = 0

        gridBagSizer.Add( clearCurrRbCtrl, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
        rowcount += 1
                
        innerFGSizer = wx.FlexGridSizer(rows=1, hgap=5, vgap=5)
        innerFGSizer.Add(clearPrioRbCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
        innerFGSizer.Add(msgPrioNumCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
        gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1

        gridBagSizer.Add( releaseDispCB, ( rowcount, 0 ), span=( 1, 1 ), flag=wx.ALIGN_CENTER_VERTICAL )
        rowcount += 1

        panel.sizer.Add(gridBagSizer, proportion=1, flag=wx.EXPAND)
        
        OnClearModeChange( wx.CommandEvent() )
        
        while panel.Affirmed():
            msgPriority = msgPrioNumCtrl.GetValue()
            if clearCurrRbCtrl.GetValue():
                msgPriority = None
            
            releaseDisplay = releaseDispCB.GetValue()
            
            panel.SetResult( 
                msgPriority,
                releaseDisplay
            )



class IsInitialized( eg.ActionBase ):
    name = "Is Initialized"
    description = "Returns 'True' if the display is initialized and ready."

    @eg.LogIt
    def __call__( self ):
        plugin = self.plugin
        rc = RC_UNKNOWN
        if not self.plugin.started:
            return False
        elif not plugin.isSetup:
            return False
        else:
            rc = plugin.apiWorker.ApiIsInited()
            return rc == DSP_S_INITED



class IsPluginMode( eg.ActionBase ):
    name = "Is Plugin Mode"
    description = "Returns 'True' if the iMON display is in plugin mode."

    @eg.LogIt
    def __call__( self ):
        if not self.plugin.started:
            return False
        plugin = self.plugin 
        rc = RC_UNKNOWN
        if not plugin.isSetup:
            plugin.Setup()
        if plugin.isSetup:
            rc = plugin.apiWorker.ApiIsPluginMode()
            
        return rc == DSP_S_IN_PLUGIN_MODE



class GetDisplayType( eg.ActionBase ):
    name = "Get Display Type"
    description = "Returns the type of the display, either 'VFD', 'LCD' or None."

    @eg.LogIt
    def __call__( self ):
        if not self.plugin.started or self.plugin.InitDisplay() != DSP_SUCCEEDED:
            return None
            
        return self.plugin.displayTypeStr



class GetCurrentDisplayText( eg.ActionBase ):
    name = "Get Current Display Text"
    description = "Returns the currently displayed text and some more information (mainly for debugging purposes)"

    @eg.LogIt
    def __call__( self ):
        if not self.plugin.started or self.plugin.InitDisplay() != DSP_SUCCEEDED:
            return None
 
        return self.plugin.displayEngine.GetCurrentDisplayText( )



class GetMessageStack( eg.ActionBase ):
    name = "Get Message Stack"
    description = "Returns the current stack of messages (mainly for debugging purposes)"

    @eg.LogIt
    def __call__( self ):
        if not self.plugin.started or self.plugin.InitDisplay() != DSP_SUCCEEDED:
            return None
 
        return self.plugin.displayEngine.GetMessageStack( )
        


class ReleaseDisplay( eg.ActionBase ):
    name = "Release Display"
    description = """<rst>
        Releases the display. 
    
        This is the counterpart of action *Acquire Display*. 
        
        The display is released so that
        ather applications (or this plugin) can acquire it again. 
        iMON FrontView will acquire the display if no other
        application acquires it.
        
        All stacked display texts are cleared. 
        
        Note that the display is automatically released before 
        the computer enters suspend state (i.e. hibernate or standby).
        """

    @eg.LogIt
    def __call__( self ):
        if not self.plugin.started:
            return False
        return self.plugin.TearDown( )

