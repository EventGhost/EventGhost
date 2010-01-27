# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2010 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import eg

eg.RegisterPlugin(
    name = "Raw Input",
)


from os.path import abspath, join, dirname
import threading
from eg.WinApi.SendKeys import VK_CODES
from eg.WinApi.Dynamic import (
    c_int,
    byref,
    sizeof,
    cast,
    create_string_buffer,
    create_unicode_buffer,
    Structure,
    POINTER,
    CDLL,
    WinError,

    GetRawInputDeviceList,
    GetRawInputDeviceInfo,
    RegisterRawInputDevices,
    GetRawInputData,
    DefWindowProc,
    PeekMessage,
    MSG,
    PM_REMOVE,
    COPYDATASTRUCT,
    PCOPYDATASTRUCT,

    UINT,
    RAWINPUTDEVICE,
    RAWINPUTHEADER,
    RAWINPUT,
    RAWINPUTDEVICELIST,
    PRAWINPUTDEVICELIST,
    RID_DEVICE_INFO,
    RID_INPUT,

    RIDI_PREPARSEDDATA,
    RIDI_DEVICENAME,
    RIDI_DEVICEINFO,
    RIM_TYPEHID,
    RIM_TYPEKEYBOARD,
    RIM_TYPEMOUSE,
    RIM_INPUT,
    RIDEV_NOLEGACY,
    RIDEV_INPUTSINK,
    WM_INPUT,
    WM_KEYDOWN,
    WM_KEYUP,
    WM_COPYDATA,
    GET_RAWINPUT_CODE_WPARAM,
    DWORD,
    WPARAM,
    LPARAM,
    WH_KEYBOARD,
)


VK_KEYS = dict((code, name) for name, code in VK_CODES)
RIM_TYPES = {
    RIM_TYPEHID: "HID",
    RIM_TYPEKEYBOARD: "Keyboard",
    RIM_TYPEMOUSE: "Mouse",
}


class HEVENT(Structure):
    _fields_ = [
        ("nCode", c_int),
        ("dwHookType", DWORD),
        ("wParam", WPARAM),
        ("lParam", LPARAM),        
    ]
    


class RawInput(eg.PluginBase):
    
    def __start__(self):
        self.ScanDevices()
        self.hookDll = CDLL(abspath(join(dirname(__file__), "hook.dll")))
        eg.messageReceiver.AddHandler(WM_INPUT, self.OnRawInput)
        eg.messageReceiver.AddHandler(WM_COPYDATA, self.OnCopyData)
        rid = (RAWINPUTDEVICE * 1)()
        rid[0].usUsagePage = 0x01
        rid[0].usUsage = 0x06
        rid[0].dwFlags = RIDEV_INPUTSINK
        rid[0].hwndTarget = eg.messageReceiver.hwnd
        RegisterRawInputDevices(rid, 1, sizeof(rid[0]))        
        self.hookDll.SetHook(eg.messageReceiver.hwnd)


    def __stop__(self):
        self.hookDll.RemoveHook()
        eg.messageReceiver.RemoveHandler(WM_COPYDATA, self.OnCopyData)
        eg.messageReceiver.RemoveHandler(WM_INPUT, self.OnRawInput)


    def ScanDevices(self):
        nDevices = UINT(0)
        if -1 == GetRawInputDeviceList(
            None, 
            byref(nDevices), 
            sizeof(RAWINPUTDEVICELIST)
        ):
            raise WinError()
        rawInputDeviceList = (RAWINPUTDEVICELIST * nDevices.value)()
        if -1 == GetRawInputDeviceList(
            cast(rawInputDeviceList, PRAWINPUTDEVICELIST), 
            byref(nDevices), 
            sizeof(RAWINPUTDEVICELIST)
        ):
            raise WinError()
        
        cbSize = UINT()
        for i in range(nDevices.value):
            print "hDevice:", rawInputDeviceList[i].hDevice
            print "Type:", RIM_TYPES[rawInputDeviceList[i].dwType]
            GetRawInputDeviceInfo(
                rawInputDeviceList[i].hDevice,
                RIDI_DEVICENAME,
                None,
                byref(cbSize)
            )
            buf = create_unicode_buffer(cbSize.value)
            GetRawInputDeviceInfo(
                rawInputDeviceList[i].hDevice,
                RIDI_DEVICENAME,
                byref(buf),
                byref(cbSize)
            )
            print "DeviceName:", buf.value
            ridDeviceInfo = RID_DEVICE_INFO()
            cbSize.value = ridDeviceInfo.cbSize = sizeof(RID_DEVICE_INFO)
            GetRawInputDeviceInfo(
                rawInputDeviceList[i].hDevice,
                RIDI_DEVICEINFO,
                byref(ridDeviceInfo),
                byref(cbSize)
            )
            if ridDeviceInfo.dwType == RIM_TYPEHID:
                print "dwVendorId: %04X" % ridDeviceInfo.hid.dwVendorId
                print "dwProductId: %04X" % ridDeviceInfo.hid.dwProductId
                print "dwVersionNumber: %04X" % ridDeviceInfo.hid.dwVersionNumber
                print "usUsagePage:", ridDeviceInfo.hid.usUsagePage
                print "usUsage:", ridDeviceInfo.hid.usUsage
            elif ridDeviceInfo.dwType == RIM_TYPEKEYBOARD:
                print "dwType:", ridDeviceInfo.keyboard.dwType
                print "dwSubType:", ridDeviceInfo.keyboard.dwSubType
                print "dwKeyboardMode:", ridDeviceInfo.keyboard.dwKeyboardMode
                print "dwNumberOfFunctionKeys:", ridDeviceInfo.keyboard.dwNumberOfFunctionKeys
                print "dwNumberOfIndicators:", ridDeviceInfo.keyboard.dwNumberOfIndicators
                print "dwNumberOfKeysTotal:", ridDeviceInfo.keyboard.dwNumberOfKeysTotal
            elif ridDeviceInfo.dwType == RIM_TYPEMOUSE:
                print "dwId:", ridDeviceInfo.mouse.dwId
                print "dwNumberOfButtons:", ridDeviceInfo.mouse.dwNumberOfButtons
                print "dwSampleRate:", ridDeviceInfo.mouse.dwSampleRate
                print "fHasHorizontalWheel:", ridDeviceInfo.mouse.fHasHorizontalWheel
            print
        

    def OnRawInput(self, hwnd, mesg, wParam, lParam):
        pcbSize = UINT()
        GetRawInputData(lParam, RID_INPUT, None, byref(pcbSize), sizeof(RAWINPUTHEADER))
        buf = create_string_buffer(pcbSize.value)
        GetRawInputData(lParam, RID_INPUT, buf, byref(pcbSize), sizeof(RAWINPUTHEADER))
        pb = cast(buf, POINTER(RAWINPUT))
        keyboard = pb.contents.data.keyboard
        if keyboard.VKey == 0xFF:
            return 0
        #print "Device:" , pb.contents.header.hDevice
        #print "Scan code:", keyboard.MakeCode
        print "Vkey:", VK_KEYS[keyboard.VKey],
        #print "Flags:", keyboard.Flags
        if keyboard.Message == WM_KEYDOWN:
            print "Message: WM_KEYDOWN"
        elif keyboard.Message == WM_KEYUP:
            print "Message: WM_KEYUP"
        else:
            print "Message:", keyboard.Message
        if GET_RAWINPUT_CODE_WPARAM(wParam) == RIM_INPUT:
            #print "   RIM"
            return DefWindowProc(hwnd, mesg, wParam, lParam)
        return 0
    

    def OnCopyData(self, hwnd, mesg, wParam, lParam):
        copyData = cast(lParam, PCOPYDATASTRUCT)
        hEvent = cast(copyData.contents.lpData, POINTER(HEVENT))
        if not (
            copyData.contents.dwData == 0
            and copyData.contents.cbData == sizeof(HEVENT)
            and hEvent.contents.dwHookType == WH_KEYBOARD
        ):
            return
        msg = MSG()
        while PeekMessage(byref(msg), 0, WM_INPUT, WM_INPUT, PM_REMOVE):
            self.OnRawInput(0, msg.message, msg.wParam, msg.lParam)
        eg.actionThread.Call(
            eg.Print, 
            repr(
                (
                    VK_KEYS[hEvent.contents.wParam], 
                    hEvent.contents.nCode, 
                    hwnd, 
                    mesg, 
                    wParam, 
                    lParam
                )
            )
        )
        return 0

        
