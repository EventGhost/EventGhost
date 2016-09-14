# -*- coding: utf-8 -*-
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

import eg

eg.RegisterPlugin(
    name = "Raw Input",
    author = "Bitmonster",
    guid = "{07601B3B-BC6E-4E15-81A2-07E15A88DDC2}",
)

import time
import threading
import collections
from os.path import abspath, join, dirname
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
    GetAsyncKeyState,
    GetMessageTime,
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
    WM_SYSKEYDOWN,
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



class RawKeyboardData(object):

    def __init__(self, vKey, device, state, tick):
        self.vKey = vKey
        self.device = device
        self.state = state
        self.tick = tick



class RawInput(eg.PluginBase):

    def __start__(self):
        self.buf = collections.deque()
        self.ScanDevices()
        self.hookDll = CDLL(
            abspath(join(dirname(__file__), "RawInputHook.dll"))
        )
        self.messageReceiver = eg.MessageReceiver("RawInputWindow")
        self.messageReceiver.AddHandler(WM_INPUT, self.OnRawInput)
        self.messageReceiver.AddHandler(WM_COPYDATA, self.OnCopyData)
        self.messageReceiver.Start()
        rid = (RAWINPUTDEVICE * 1)()
        rid[0].usUsagePage = 0x01
        rid[0].usUsage = 0x06
        rid[0].dwFlags = RIDEV_INPUTSINK
        rid[0].hwndTarget = self.messageReceiver.hwnd
        RegisterRawInputDevices(rid, 1, sizeof(rid[0]))
        self.hookDll.Start(self.messageReceiver.hwnd)


    def __stop__(self):
        self.hookDll.Stop()
        self.messageReceiver.Stop()


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
            GetRawInputDeviceInfo(
                rawInputDeviceList[i].hDevice,
                RIDI_DEVICENAME,
                None,
                byref(cbSize)
            )
            deviceName = create_unicode_buffer(cbSize.value)
            GetRawInputDeviceInfo(
                rawInputDeviceList[i].hDevice,
                RIDI_DEVICENAME,
                byref(deviceName),
                byref(cbSize)
            )
            ridDeviceInfo = RID_DEVICE_INFO()
            cbSize.value = ridDeviceInfo.cbSize = sizeof(RID_DEVICE_INFO)
            GetRawInputDeviceInfo(
                rawInputDeviceList[i].hDevice,
                RIDI_DEVICEINFO,
                byref(ridDeviceInfo),
                byref(cbSize)
            )
            if ridDeviceInfo.dwType != RIM_TYPEKEYBOARD:
                continue
            print "hDevice:", rawInputDeviceList[i].hDevice
            print "Type:", RIM_TYPES[rawInputDeviceList[i].dwType]
            print "DeviceName:", deviceName.value
            if ridDeviceInfo.dwType == RIM_TYPEHID:
                hid = ridDeviceInfo.hid
                print "dwVendorId: %04X" % hid.dwVendorId
                print "dwProductId: %04X" % hid.dwProductId
                print "dwVersionNumber: %04X" % hid.dwVersionNumber
                print "usUsagePage:", hid.usUsagePage
                print "usUsage:", hid.usUsage
            if ridDeviceInfo.dwType == RIM_TYPEKEYBOARD:
                kbd = ridDeviceInfo.keyboard
                print "dwType:", kbd.dwType
                print "dwSubType:", kbd.dwSubType
                print "dwKeyboardMode:", kbd.dwKeyboardMode
                print "dwNumberOfFunctionKeys:", kbd.dwNumberOfFunctionKeys
                print "dwNumberOfIndicators:", kbd.dwNumberOfIndicators
                print "dwNumberOfKeysTotal:", kbd.dwNumberOfKeysTotal
            if ridDeviceInfo.dwType == RIM_TYPEMOUSE:
                mouse = ridDeviceInfo.mouse
                print "dwId:", mouse.dwId
                print "dwNumberOfButtons:", mouse.dwNumberOfButtons
                print "dwSampleRate:", mouse.dwSampleRate
                print "fHasHorizontalWheel:", mouse.fHasHorizontalWheel
            print


    def OnRawInput(self, hwnd, mesg, wParam, lParam):
        pcbSize = UINT()
        GetRawInputData(
            lParam, RID_INPUT, None, byref(pcbSize), sizeof(RAWINPUTHEADER)
        )
        buf = create_string_buffer(pcbSize.value)
        GetRawInputData(
            lParam, RID_INPUT, buf, byref(pcbSize), sizeof(RAWINPUTHEADER)
        )
        pRawInput = cast(buf, POINTER(RAWINPUT))
        keyboard = pRawInput.contents.data.keyboard
        if keyboard.VKey == 0xFF:
            eg.eventThread.Call(eg.Print, "0xFF")
            return 0
         #print "Scan code:", keyboard.MakeCode
        info = ""
        mTime = time.clock()
        if keyboard.Message == WM_KEYDOWN:
            transition = "KEYDOWN"
        elif keyboard.Message == WM_KEYUP:
            transition = "KEYUP"
        else:
            transition = " %d" % keyboard.Message
        info = "%f " % mTime
        info += "RawI %s: %s(%d), " % (
            transition,
            VK_KEYS[keyboard.VKey],
            keyboard.VKey
        )
        if GetAsyncKeyState(162): #LCtrl
            info += "LCtrl "
        if GetAsyncKeyState(163): #RCtrl
            info += "RCtrl "
        info += "Scan: %d, " % keyboard.MakeCode
        info += "Extra: %d, " % keyboard.ExtraInformation
        info += "Device: %r, " % pRawInput.contents.header.hDevice
        #print "Flags:", keyboard.Flags
        rawKeyboardData = RawKeyboardData(
            keyboard.VKey,
            pRawInput.contents.header.hDevice,
            keyboard.Message in (WM_KEYDOWN, WM_SYSKEYDOWN),
            time.clock()
        )
        self.buf.append(rawKeyboardData)
        eg.eventThread.Call(eg.Print, info)
        if GET_RAWINPUT_CODE_WPARAM(wParam) == RIM_INPUT:
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
            eg.eventThread.Call(eg.Print, "return")
            return
        mTime = time.clock()
        msg = MSG()
        while PeekMessage(byref(msg), 0, WM_INPUT, WM_INPUT, PM_REMOVE):
            self.OnRawInput(0, msg.message, msg.wParam, msg.lParam)
        vKey = hEvent.contents.wParam
        repeatCount = hEvent.contents.lParam & 0xFFFF
        keyState = (hEvent.contents.lParam >> 30) & 0x01
        extended = (hEvent.contents.lParam >> 24) & 0x01
        if (hEvent.contents.lParam >> 31) & 0x01:
            transition = "KEYUP"
            state = False
        else:
            transition = "KEYDOWN"
            state = True
        info = "%f Hook %s: %s(%d), keyState=%d, extended=%d" % (
            mTime,
            transition,
            VK_KEYS[vKey],
            hEvent.contents.wParam,
            keyState,
            extended,
        )
        if GetAsyncKeyState(162): #LCtrl
            info += "LCtrl "
        if GetAsyncKeyState(163): #RCtrl
            info += "RCtrl "
        i = 0
        while i < len(self.buf):
            rawKeyboardData = self.buf[i]
            if rawKeyboardData.tick < time.clock() - 0.2:
                eg.eventThread.Call(eg.Print, "*** removed to old message")
                del self.buf[i]
                continue
            if (
                rawKeyboardData.vKey == vKey
                and rawKeyboardData.state == state
            ):
                del self.buf[i]
#                if rawKeyboardData.device != 65603:
#                    eg.eventThread.Call(eg.Print, "blocked")
#                    return 1
                eg.eventThread.Call(eg.Print, info)
                return 0
            i += 1
        eg.eventThread.Call(eg.Print, "not found")


