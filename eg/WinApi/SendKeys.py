# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

# Local imports
import eg
from eg.WinApi.Dynamic import (
    AttachThreadInput, byref, c_ubyte, CloseHandle, DWORD, GetCurrentThreadId,
    GetFocus, GetForegroundWindow, GetGUIThreadInfo, GetKeyboardState,
    GetMessage, GetWindowThreadProcessId, GUITHREADINFO, INPUT, INPUT_KEYBOARD,
    KEYEVENTF_KEYUP, MapVirtualKey, MSG, OpenProcess, pointer, PostMessage,
    PROCESS_QUERY_INFORMATION, SendInput, SetKeyboardState, SetTimer, sizeof,
    VK_CONTROL, VK_LCONTROL, VK_LSHIFT, VK_MENU, VK_SHIFT, VkKeyScanW,
    WaitForInputIdle, WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, WM_SYSKEYUP,
    WM_TIMER,
)

VK_CODES = (
    ('AltGr', 10),
    ('Shift', 16),
    ('LShift', 160),
    ('RShift', 161),
    ('Ctrl', 17),
    ('LCtrl', 162),
    ('RCtrl', 163),
    ('Alt', 18),
    ('LAlt', 164),
    ('RAlt', 165),
    ('LWin', 91),
    ('RWin', 92),
    ('Apps', 93),
    ('LButton', 1),
    ('RButton', 2),
    ('MButton', 4),
    ('XButton1', 5),
    ('XButton2', 6),

    ('CapsLock', 20),
    ('NumLock', 144),
    ('ScrollLock', 145),

    ('Cancel', 3),
    ('Backspace', 8),
    ('Tabulator', 9),
    ('Clear', 12),
    ('Pause', 19),
    ('Kana', 21),
    ('Junja', 23),
    ('Final', 24),
    ('Hanja', 25),
    ('Escape', 27),
    ('Convert', 28),
    ('NonConvert', 29),
    ('Accept', 30),
    ('ModeChange', 31),
    ('Space', 32),
    ('PageUp', 33),
    ('PageDown', 34),
    ('End', 35),
    ('Home', 36),
    ('Left', 37),
    ('Up', 38),
    ('Right', 39),
    ('Down', 40),
    ('Select', 41),
    ('Print', 42),
    ('Execute', 43),
    ('PrintScreen', 44),
    ('Insert', 45),
    ('Delete', 46),
    ('Help', 47),
    ('A', 65),
    ('B', 66),
    ('C', 67),
    ('D', 68),
    ('E', 69),
    ('F', 70),
    ('G', 71),
    ('H', 72),
    ('I', 73),
    ('J', 74),
    ('K', 75),
    ('L', 76),
    ('M', 77),
    ('N', 78),
    ('O', 79),
    ('P', 80),
    ('Q', 81),
    ('R', 82),
    ('S', 83),
    ('T', 84),
    ('U', 85),
    ('V', 86),
    ('W', 87),
    ('X', 88),
    ('Y', 89),
    ('Z', 90),
    ('Sleep', 95),
    ('0', 48),
    ('1', 49),
    ('2', 50),
    ('3', 51),
    ('4', 52),
    ('5', 53),
    ('6', 54),
    ('7', 55),
    ('8', 56),
    ('9', 57),
    ('Numpad0', 96),
    ('Numpad1', 97),
    ('Numpad2', 98),
    ('Numpad3', 99),
    ('Numpad4', 100),
    ('Numpad5', 101),
    ('Numpad6', 102),
    ('Numpad7', 103),
    ('Numpad8', 104),
    ('Numpad9', 105),
    ('Multiply', 106),
    ('Add', 107),
    ('Separator', 108),
    ('Subtract', 109),
    ('Decimal', 110),
    ('Divide', 111),
    ('F1', 112),
    ('F2', 113),
    ('F3', 114),
    ('F4', 115),
    ('F5', 116),
    ('F6', 117),
    ('F7', 118),
    ('F8', 119),
    ('F9', 120),
    ('F10', 121),
    ('F11', 122),
    ('F12', 123),
    ('F13', 124),
    ('F14', 125),
    ('F15', 126),
    ('F16', 127),
    ('F17', 128),
    ('F18', 129),
    ('F19', 130),
    ('F20', 131),
    ('F21', 132),
    ('F22', 133),
    ('F23', 134),
    ('F24', 135),

    ('BrowserBack', 166),
    ('BrowserForward', 167),
    ('BrowserRefresh', 168),
    ('BrowserStop', 169),
    ('BrowserSearch', 170),
    ('BrowserFavorites', 171),
    ('BrowserHome', 172),
    ('VolumeMute', 173),
    ('VolumeDown', 174),
    ('VolumeUp', 175),
    ('MediaNextTrack', 176),
    ('MediaPrevTrack', 177),
    ('MediaStop', 178),
    ('MediaPlayPause', 179),
    ('LaunchMail', 180),
    ('LaunchMediaSelect', 181),
    ('LaunchApp1', 182),
    ('LaunchApp2', 183),

    ('OemPlus', 187),
    ('OemComma', 188),
    ('OemMinus', 189),
    ('OemPeriod', 190),
    ('Oem1', 186),
    ('Oem2', 191),
    ('Oem3', 192),
    ('Oem4', 219),
    ('Oem5', 220),
    ('Oem6', 221),
    ('Oem7', 222),
    ('Oem8', 223),
    ('Oem92', 146),
    ('Oem93', 147),
    ('Oem94', 148),
    ('Oem95', 149),
    ('Oem96', 150),
    ('OemE1', 225),
    ('Oem102', 226),
    ('OemE3', 227),
    ('OemE4', 228),
    ('ProcessKey', 229),
    ('OemE6', 230),
    ('Packet', 231),
    ('OemE9', 233),
    ('OemEA', 234),
    ('OemEB', 235),
    ('OemEC', 236),
    ('OemED', 237),
    ('OemEE', 238),
    ('OemEF', 239),
    ('OemF0', 240),
    ('OemF1', 241),
    ('OemF2', 242),
    ('OemF3', 243),
    ('OemF4', 244),
    ('OemF5', 245),
    ('Attn', 246),
    ('CrSel', 247),
    ('ExSel', 248),
    ('EraseEof', 249),
    ('Play', 250),
    ('Zoom', 251),
    ('Noname', 252),
    ('PA1', 253),
    ('OemClear', 254),

    ('U00', 0),
    ('U07', 7),
    #('Reserved_0A', 10), we use this code as AltGr
    ('U0B', 11),
    ('U0E', 14),
    ('U0F', 15),
    ('U16', 22),
    ('U1A', 26),
    ('U3A', 58),
    ('U3B', 59),
    ('U3C', 60),
    ('U3D', 61),
    ('U3E', 62),
    ('U3F', 63),
    ('U40', 64),
    ('U5E', 94),
    ('U88', 136),
    ('U89', 137),
    ('U8A', 138),
    ('U8B', 139),
    ('U8C', 140),
    ('U8D', 141),
    ('U8E', 142),
    ('U8F', 143),
    ('U97', 151),
    ('U98', 152),
    ('U99', 153),
    ('U9A', 154),
    ('U9B', 155),
    ('U9C', 156),
    ('U9D', 157),
    ('U9E', 158),
    ('U9F', 159),
    ('UB8', 184),
    ('UB9', 185),
    ('UC1', 193),
    ('UC2', 194),
    ('UC3', 195),
    ('UC4', 196),
    ('UC5', 197),
    ('UC6', 198),
    ('UC7', 199),
    ('UC8', 200),
    ('UC9', 201),
    ('UCA', 202),
    ('UCB', 203),
    ('UCC', 204),
    ('UCD', 205),
    ('UCE', 206),
    ('UCF', 207),
    ('UD0', 208),
    ('UD1', 209),
    ('UD2', 210),
    ('UD3', 211),
    ('UD4', 212),
    ('UD5', 213),
    ('UD6', 214),
    ('UD7', 215),
    ('UD8', 216),
    ('UD9', 217),
    ('UDA', 218),
    ('UE0', 224),
    ('UE8', 232),
    ('UFF', 255),

    ('Return', 13),
)

del GetKeyboardState.argtypes
del SetKeyboardState.argtypes
del SetTimer.argtypes

PBYTE256 = c_ubyte * 256

VK_KEYS = {
    'BACK': 0x08,
    'TAB': 0x09,
    'ENTER': 0x0D,
    'CONTROL': 0x11,
    'CAPITAL': 0x14,
    'ESC': 0x1B,
    'SPC': 0x20,
    'PGUP': 0x21,
    'PGDOWN': 0x22,
    'INS': 0x012D,
    'DEL': 0x012E,
    'WIN': 0x015B,
}

for keyword, code in VK_CODES:
    VK_KEYS[keyword.upper()] = code

class SendKeysParser:
    @eg.LogIt
    def __init__(self):
        self.dummyWindow = wx.Frame(None, -1, "Dummy Window")
        self.dummyHwnd = self.dummyWindow.GetHandle()
        self.msg = MSG()
        self.isSysKey = False
        self.sendInputStruct = INPUT()
        self.sendInputStruct.type = INPUT_KEYBOARD
        self.keyboardStateBuffer = PBYTE256()
        self.procHandle = None
        self.guiTreadInfo = GUITHREADINFO()
        self.guiTreadInfo.cbSize = sizeof(GUITHREADINFO)

    def __call__(self, hwnd, keystrokeString, useAlternateMethod=False, mode=2):
        keyData = ParseText(keystrokeString)
        if keyData:
            needGetFocus = False
            sendToFront = False
            if hwnd is None:
                sendToFront = True
                hwnd = GetForegroundWindow()
                needGetFocus = True

            dwProcessId = DWORD()
            threadID = GetWindowThreadProcessId(hwnd, byref(dwProcessId))
            processID = dwProcessId.value
            ourThreadID = GetCurrentThreadId()

            # If not, attach our thread's 'input' to the foreground thread's
            if threadID != ourThreadID:
                AttachThreadInput(threadID, ourThreadID, True)

            if needGetFocus:
                hwnd = GetFocus()
            if not sendToFront:
                if GetGUIThreadInfo(0, byref(self.guiTreadInfo)):
                    sendToFront = (self.guiTreadInfo.hwndFocus == hwnd)
                else:
                    sendToFront = False
            if not hwnd:
                hwnd = None
            self.procHandle = OpenProcess(
                PROCESS_QUERY_INFORMATION,
                0,
                processID
            )
            #self.WaitForInputProcessed()

            oldKeyboardState = PBYTE256()
            GetKeyboardState(byref(oldKeyboardState))

            keyData = ParseText(keystrokeString)
            if sendToFront and not useAlternateMethod:
                self.SendRawCodes1(keyData, mode)
            else:
                self.SendRawCodes2(keyData, hwnd, mode)

            SetKeyboardState(byref(oldKeyboardState))
            self.WaitForInputProcessed()
            if threadID != ourThreadID:
                AttachThreadInput(threadID, ourThreadID, False)
            if self.procHandle:
                CloseHandle(self.procHandle)

    def SendRawCodes1(self, keyData, mode):
        """
        Uses the SendInput-API function to send the virtual keycode.
        Can only send to the frontmost window.
        """
        sendInputStruct = self.sendInputStruct
        sendInputStructPointer = pointer(sendInputStruct)
        sendInputStructSize = sizeof(sendInputStruct)
        keyboardStruct = sendInputStruct.ki
        for block in keyData:
            if mode == 1 or mode == 2:
                keyboardStruct.dwFlags = 0
                for virtualKey in block:
                    keyboardStruct.wVk = virtualKey & 0xFF
                    SendInput(1, sendInputStructPointer, sendInputStructSize)
                    self.WaitForInputProcessed()
            if mode == 0 or mode == 2:
                keyboardStruct.dwFlags = KEYEVENTF_KEYUP
                for virtualKey in reversed(block):
                    keyboardStruct.wVk = virtualKey & 0xFF
                    SendInput(1, sendInputStructPointer, sendInputStructSize)
                    self.WaitForInputProcessed()

    def SendRawCodes2(self, keyData, hwnd, mode):
        """
        Uses PostMessage and SetKeyboardState to emulate the the virtual
        keycode. Can send to a specified window handle.
        """
        keyboardStateBuffer = self.keyboardStateBuffer
        for block in keyData:
            if mode == 1 or mode == 2:
                for virtualKey in block:
                    keyCode = virtualKey & 0xFF
                    highBits = virtualKey & 0xFF00
                    lparam = ((MapVirtualKey(keyCode, 0) | highBits) << 16) | 1

                    keyboardStateBuffer[keyCode] |= 128

                    if keyCode == VK_LSHIFT:
                        keyboardStateBuffer[VK_SHIFT] |= 128
                    #elif keyCode == VK_MENU:
                    #    self.isSysKey = True
                    elif keyCode == VK_CONTROL:
                        keyboardStateBuffer[VK_LCONTROL] |= 128

                    if self.isSysKey:
                        mesg = WM_SYSKEYDOWN
                        lparam |= 0x20000000
                    else:
                        mesg = WM_KEYDOWN

                    SetKeyboardState(byref(keyboardStateBuffer))
                    PostMessage(hwnd, mesg, keyCode, lparam)
                    self.WaitForInputProcessed()

            if mode == 0 or mode == 2:
                for virtualKey in reversed(block):
                    keyCode = virtualKey & 0xFF
                    highBits = virtualKey & 0xFF00
                    lparam = (
                        ((MapVirtualKey(keyCode, 0) | highBits) << 16) |
                        0xC0000001
                    )
                    keyboardStateBuffer[keyCode] &= ~128

                    if keyCode == VK_LSHIFT:
                        keyboardStateBuffer[VK_SHIFT] &= ~128
                    #elif keyCode == VK_MENU:
                    #    self.isSysKey = False
                    elif keyCode == VK_CONTROL:
                        keyboardStateBuffer[VK_LCONTROL] &= ~128

                    if self.isSysKey:
                        mesg = WM_SYSKEYUP
                        lparam |= 0x20000000
                    else:
                        mesg = WM_KEYUP

                    SetKeyboardState(byref(keyboardStateBuffer))
                    PostMessage(hwnd, mesg, keyCode, lparam)
                    self.WaitForInputProcessed()

    def WaitForInputProcessed(self):
        if self.procHandle:
            WaitForInputIdle(self.procHandle, 100)

        def DoIt():
            SetTimer(self.dummyHwnd, 1, 0, None)
            self.msg.message = 0
            while self.msg.message != WM_TIMER:
                GetMessage(byref(self.msg), self.dummyHwnd, 0, 0)
        eg.CallWait(DoIt)


def ParseSingleChar(char):
    """
    Translates a single character to the needed key sequence.
    """
    vkCode = VkKeyScanW(char) & 0xFFFF
    if vkCode == 0xFFFF:
        eg.PrintError(
            "SendKeys: Can't translate character '%s' to key sequence!" % char
        )
        return
    data = []
    if vkCode & 0x200:
        data.append(VK_CONTROL)
    if vkCode & 0x400:
        data.append(VK_MENU)
    if vkCode & 0x100:
        data.append(VK_LSHIFT)
    data.append(vkCode)
    return data

def ParseText(text):
    """
    Translates a string to a key sequence.
    """
    data = []
    i = 0
    strLen = len(text)
    while i < strLen:
        char = text[i]
        if char == "{":
            if i + 1 < strLen and text[i + 1] == "{":
                i += 2
                if i < strLen and text[i] == "}":
                    i += 1
                temp = ParseSingleChar(char)
                if temp:
                    data.append(temp)
            else:
                end = text.find("}", i + 1)
                if end == -1:
                    raise SyntaxError("Matching closing brace not found")
                key = text[i + 1:end]
                i = end + 1
                key2 = key.replace("_", "+").replace("-", "+").upper()
                words = key2.split("+")
                for word in words:
                    if word not in VK_KEYS:
                        try:
                            res = unicode(eval(key, {}, eg.globals.__dict__))
                        except:
                            res = key
                        data.extend(ParseText(res))
                        break
                else:
                    data.append([VK_KEYS[word] for word in words])
        else:
            i += 1
            temp = ParseSingleChar(char)
            if temp:
                data.append(temp)
    return data
