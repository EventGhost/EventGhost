# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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

class PluginInfo(eg.PluginInfo):
    name = "ffdshow"
    author = "Bitmonster"
    version = "1.0.0"
    kind = "program"
    description = (
        'Adds actions to control the '
        '<a href="http://ffdshow-tryout.sourceforge.net/">'
        'ffdshow DirectShow filter</a>.'
    )
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADMElEQVR42nVSXUiTYRR+"
        "v+/bn6hbapqoTEf400R3YWmQ6E2gIoIk02Y3BZoadVEIGsxCZAkpSZB6YUiDdlFmNAzC"
        "QeDUFGXI7GcmBlEauh+dujnWtm/receMbjrwcF7Oe87zPue8hxkfHyccxxGlUkkYhiEy"
        "mYwcm9/vJy6XizgcDqJQKEhSUlI0TvN8Ph/Z2NggzNjYGCMQCEhRUVE5z/MyqVTKsywb"
        "AWk4FAqxu7u7n7e2tpjs7GxVcnIyUvhIYmJi+OjoiAXBHON0OoUIBt1u95fMzExlJBIh"
        "gUAgqspms5GBgQFTf3+/F3eXwuFwVAF9fXNzk/T09HgYyORQlLG/v/8eLytqa2s/HRwc"
        "mNPS0khKSkry9vb29Pz8/GO0caKtrW1nYWHhFZTQtmTp6elSZnFxkfZaXVZW9m5mZoYf"
        "HBx8X1xc/EQul7MNDQ3G5eXlczU1NWar1SrWarWvU1NTn2VlZQmGhoaM0XmAkROJRNqC"
        "goL7tO+9vT0uIyODzM7OksnJyZsoEkkkkkdCoTBweHgoosrMZjOZm/vwwOFw3mNQQCdt"
        "ycnJKTEYDL6VlRUuPj7+CNLDdru9Va/Xq9GKZnR0NDA9PR3EbwUwPMHq6uqNYDBgYND7"
        "FY/H04ciRWtr61OoGcRre83NzaH19XV3fX29XwxraWlxVVZWKjs7O8P5+fmMTqdz5ebm"
        "EWZpaclWWlqaBx/u6OiYgtyGpqYmUlhYSKCgWqPRvMBrcY2NjYb29vZrw8PDJCEhgajV"
        "akKHyfT29r2sqChXm0wmMjExcR3THe/u7hbX1dX5sTDdXq9Xh1nQu1sgHFGpVMK1tbXf"
        "+DEmagKBCHvEXeT5UHowGNRjsBEoIpg+wfeyVVVVGovFIh4ZGZlF+jcsFenq6mKRF12K"
        "6BYi8SouJWB9i7MSRIm42wZclBC/Q1fwLM6LAIsaC/wZQEkJ4nC4Cwyg+Db8RxAdoKgE"
        "5wIUihE3ImaFv4zYDrwbPhcwUQIRDg+BKVoA/ADkgAD4DpwHvlK1wC/AC9yJ5T+PtgC7"
        "AJwC3gCnAQlgp/JjvZ6MkRtjdzTnJyU7Jji2v8P5j3EA/2/gD9tgef0euQO8AAAAAElF"
        "TkSuQmCC"
    )




##define FFDSHOW_REMOTE_MESSAGE "ffdshow_remote_message"
##define FFDSHOW_REMOTE_CLASS "ffdshow_remote_class"
#
#//lParam - parameter id to be used by WPRM_PUTPARAM, WPRM_GETPARAM and COPY_PUTPARAMSTR
##define WPRM_SETPARAM_ID 0
#
#//lParam - new value of parameter
#//returns TRUE or FALSE
##define WPRM_PUTPARAM    1
#
#//lParam - unused
#//return the value of parameter
##define WPRM_GETPARAM    2
#
#//lParam - parameter id
##define WPRM_GETPARAM2   3
#
##define WPRM_STOP        4
##define WPRM_RUN         5
#
#//returns playback status
#// -1 - if not available
#//  0 - stopped
#//  1 - paused
#//  2 - running
##define WPRM_GETSTATE    6
#
#//returns movie duration in seconds
##define WPRM_GETDURATION 7
#//returns current position in seconds
##define WPRM_GETCURTIME  8
#
##define WPRM_PREVPRESET 11
##define WPRM_NEXTPRESET 12 
#
#//Set current time in seconds
##define WPRM_SETCURTIME 13
#
#
#
#
#//WM_COPYDATA 
#//COPYDATASTRUCT.dwData=
##define COPY_PUTPARAMSTR        9 // lpData points to new param value
##define COPY_SETACTIVEPRESET   10 // lpData points to new preset name
##define COPY_AVAILABLESUBTITLE_FIRST 11 // lpData points to buffer where first file name will be stored  - if no subtitle file is available, lpData will contain empty string
##define COPY_AVAILABLESUBTITLE_NEXT  12 // lpData points to buffer where next file name will be stored  - if no subtitle file is available, lpData will contain empty string
##define COPY_GETPARAMSTR       13 // lpData points to buffer where param value will be stored
##define COPY_GET_PRESETLIST		14 //Get the list of presets (array of strings)
##define COPY_GET_SOURCEFILE		15 //Get the filename currently played

import win32gui
import win32con
import ctypes
from ctypes.wintypes import DWORD

class COPYDATASTRUCT(ctypes.Structure):
    """This is a mapping to the Win32 COPYDATASTRUCT.
    
    typedef struct tagCOPYDATASTRUCT {
        ULONG_PTR dwData;
        DWORD cbData;
        PVOID lpData;
    } COPYDATASTRUCT, *PCOPYDATASTRUCT;
    """
    _fields_ = [ 
        ('dwData', DWORD), #I think this is right
        ('cbData', DWORD),
        ('lpData', ctypes.c_char_p)
    ]

PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)


WPRM_STOP = 4
WPRM_RUN = 5
WPRM_PREVPRESET = 11
WPRM_NEXTPRESET = 12 
COPY_SETACTIVEPRESET = 10
COPY_GET_PRESETLIST = 14
COPY_GET_SOURCEFILE = 15


class Ffdshow(eg.PluginClass):
    
    def __start__(self):
        self.mesg = win32gui.RegisterWindowMessage("ffdshow_remote_message")
        eg.messageReceiver.AddHandler(win32con.WM_COPYDATA, self.Handler)
        
        
    @eg.LogIt
    def Handler(self, hwnd, mesg, wParam, lParam):
        cdsPointer = ctypes.cast(lParam, PCOPYDATASTRUCT)
        #print repr(cdsPointer.contents.lpData)
        return True


    def SendFfdshowMessage(self, wParam, lParam=0):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            self.PrintError("ffdshow instance not found")
            return None
        return win32gui.SendMessage(hwnd, self.mesg, wParam, lParam)



class Stop(eg.ActionClass):
    
    def __call__(self):
        return self.plugin.SendFfdshowMessage(WPRM_STOP)
        


class Run(eg.ActionClass):
    
    def __call__(self):
        return self.plugin.SendFfdshowMessage(WPRM_RUN)
        


class PreviousPreset(eg.ActionClass):
    name = "Previous Preset"
    
    def __call__(self):
        return self.plugin.SendFfdshowMessage(WPRM_PREVPRESET)
        


class NextPreset(eg.ActionClass):
    name = "Next Preset"
    
    def __call__(self):
        return self.plugin.SendFfdshowMessage(WPRM_NEXTPRESET)
        


class SetPreset(eg.ActionWithStringParameter):
    class text:
        name = "Set Preset"
        parameterDescription = "Preset Name:"
        
    def __call__(self, preset):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            self.PrintError("ffdshow instance not found")
            return
        cds = COPYDATASTRUCT()
        cds.dwData = COPY_SETACTIVEPRESET
        cds.lpData = ctypes.c_char_p(preset)
        cds.cbData = len(preset) + 1
        win32gui.SendMessage(
            hwnd, 
            win32con.WM_COPYDATA, 
            eg.messageReceiver.hwnd, 
            ctypes.addressof(cds)
        )
        
        
    
class GetPresets(eg.ActionClass):
    
    def __call__(self):
        try:
            hwnd = win32gui.FindWindow("ffdshow_remote_class", None)
        except:
            self.PrintError("ffdshow instance not found")
            return
        
        cds = COPYDATASTRUCT()
        cds.dwData = COPY_GET_PRESETLIST
        win32gui.SendMessage(
            hwnd, 
            win32con.WM_COPYDATA, 
            eg.messageReceiver.hwnd, 
            ctypes.addressof(cds)
        )
        
        