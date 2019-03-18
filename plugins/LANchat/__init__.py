version = "0.0.1"

# Plugins/LANchat/__init__.py
#
# Copyright (C)  2010 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
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
# Revision history:
# =================
# 0.0.1 by Pako 2010-10-01 10:45 GMT+1
#     - initial version

import eg

eg.RegisterPlugin(
    name="LANchat",
    author="Pako",
    version=version,
    kind="program",
    guid="{4385E4ED-8987-4F80-9708-38F83198DD1C}",
    description=(
        'Adds actions to control the <a href="http://www.fomine.com/lan-chat.html">Fomine LAN Chat</a>. \n\n<p>'
    ),
    createMacrosOnAdd=True,
    #    url = "http://www.eventghost.org/forum/viewtopic.php?.....",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAAB0AAAAdCAMAAABhTZc9AAADAFBMVEUA////AAD///8A"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABGQBpZUgCdGhhQwdvaXRD"
        "JgZpYm0gcmVjZXYgYWxuYXJyYXBlY250Y2FsbGVoQwdla2NUCAlyT2ICcmVhVAdvdFNP"
        "BwlpbEMMB2tpdHBoQ25lZ25UDABpZGF0dUILbm9lUkJhbHAEcmV0ZmVUAwiMA3BpVwUD"
        "aHRIBgFoZ2kHEQJ0cGEGbm9tZVJjYWxsIHJydCBwc25uZXJhIGVldXQIZWxPYmFyZWRP"
        "BwJpbEMMB2tpdHBoQ25lZ25UCgBvbG9pZEVvQwlFcm8EdGl0ZmVUAwgYAnBkaVdZAmhp"
        "ZUgCdGhvQgtyZWRseXRiCAduaVMFZWxvbG9jBwdhbEJDCmtvdHN4ZVRBEgZlcnRvYyB1"
        "ZWwuLnNlUghuT2QICXloQ25lZ25wTwxub2luYWgAAGVDVAlrY2UPeG9uQUJlbHVhclQE"
        "cHN0ZmVUAxG0A3BpVwUDaHRIBgFoZ2kHEQJ0cGEUbm8AAABzqcNpdGMgcmV0IGFzbmFl"
        "cmEIZWNPYmFyZWRPBwRpbEMUB2tuQUJlbHVhclRDcHNrY2kAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADUGbfeAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAC1JREFUeNpjYGBgYMQKGKBg"
        "QGWZkAGdZfG7inaySG6isuxA+WggZClJdVSXBQBDpgMEBWTyaQAAAABJRU5ErkJggg=="
    ),
)

import _winreg
import wx
from os import path
from subprocess import Popen
from win32gui import SendMessage, GetDlgItem
from eg.WinApi.Dynamic import ShowWindow
from eg.WinApi.Utils import BringHwndToFront, CloseHwnd
from ctypes import addressof, create_string_buffer
from threading import Thread, Event
from time import sleep

WM_SETTEXT = 12
WM_COMMAND = 273
EM_GETLINECOUNT = 186
EM_GETLINE = 196
BN_CLICKED = 0
SW_MINIMIZE = 6
BST_CHECKED = 1
BM_GETCHECK = 240
BM_SETCHECK = 241
BM_SETSTATE = 243
TVM_GETCOUNT = 0x1105


# ===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):

    def GetTextCtrl(self):  # now I can make build-in textCtrl
        return self.textControl  # non-editable !!!


# ===============================================================================

def HandleLch():
    FindLch = eg.WindowMatcher(
        u'LAN{*}hat.exe',
        None,
        u'#32770',
        None,
        None,
        None,
        True,
        0.2,
        0
    )

    hwnds = FindLch()
    if len(hwnds) > 0:
        return hwnds[0]
    return None


# ===============================================================================

class ObservationThread(Thread):

    def __init__(
        self,
        period,
        bring,
        suffix,
        hwnd
    ):
        self.abort = False
        self.threadFlag = Event()
        self.period = period
        self.bring = bring
        self.suffix = suffix
        self.lastMessage = ""
        self.lines = self.GetLineCount(hwnd)[0] if hwnd else 0
        self.users = self.GetUserCount(hwnd) if hwnd else 0
        Thread.__init__(self, name='Fomine_LANchat_Thread')

    def ResetLinesCount(self):
        self.lines = 1

    def GetLastMessage(self):
        return self.lastMessage

    def GetUserCount(self, hWnd=None):
        hwnd = hWnd or HandleLch()
        if hwnd:
            treeView = GetDlgItem(hwnd, 1000)
            if treeView:
                return SendMessage(treeView, TVM_GETCOUNT, 0, 0)
        return None

    def GetLineCount(self, hWnd=None, lines=None):
        hwnd = hWnd or HandleLch()
        if hwnd:
            edit = GetDlgItem(hwnd, 1001)
            if edit:
                count = SendMessage(edit, EM_GETLINECOUNT, 0, 0)
                lns = []
                if lines is not None and count > lines:
                    rows = count - lines
                    locBuf = create_string_buffer(512)
                    locBuf.value = "\x00\x01\x00\x00" + 508 * "\x00"
                    for row in range(rows):
                        tchars = SendMessage(
                            edit,
                            EM_GETLINE,
                            count - (rows + 1 - row),
                            addressof(locBuf)
                        )
                        lns.append(locBuf.value[:tchars].replace("\x0D", ""))
                    self.lastMessage = "".join(lns).decode(eg.systemEncoding)
                return count, self.lastMessage
        return None, None

    def run(self):
        while not self.abort:
            hwnd = HandleLch()
            if hwnd:
                lines, mess = self.GetLineCount(hwnd, self.lines)
                if lines > self.lines:
                    self.lines = lines
                    eg.TriggerEvent(self.suffix[0], prefix="FomineLANChat", payload=mess)
                    if self.bring:
                        BringHwndToFront(hwnd)
                users = self.GetUserCount(hwnd)
                if users != self.users:
                    self.users = users
                    eg.TriggerEvent(self.suffix[1], prefix="FomineLANChat", payload=self.users)
            if self.abort:
                break
            self.threadFlag.wait(self.period)
            self.threadFlag.clear()

    def AbortObservation(self):
        self.abort = True
        self.threadFlag.set()


# ===============================================================================

class Text:
    label1 = "Fomine LAN Chat installation folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    browseTitle = "Selected folder:"
    intervalLabel = "Refresh period of detect changes:"
    bring = "Automatically bring window to top when new message arrives"
    suffix = "NewMessage"
    suffix_2 = "UsersChanged"
    suff_1_Label = "New message event suffix:"
    suff_2_Label = "Event suffix when number of users has changed:"


# ===============================================================================

class Run(eg.ActionBase):
    name = "Launch Fomine LAN Chat"
    description = "Launch Fomine LAN Chat."

    def __call__(self):
        if HandleLch() is None:
            lch = '%s\\LANchat.exe' % self.plugin.lchPath
            if path.isfile(lch):
                Popen([lch])


# ===============================================================================

class Minimize(eg.ActionBase):
    name = "Minimize Fomine LAN Chat window"
    description = "Minimize Fomine LAN Chat window."

    def __call__(self):
        hwnd = HandleLch()
        if hwnd:
            ShowWindow(hwnd, SW_MINIMIZE)


# ===============================================================================

class BringToFront(eg.ActionBase):
    name = "Bring Fomine LAN Chat window to front"
    description = "Bring Fomine LAN Chat window to front."

    def __call__(self):
        hwnd = HandleLch()
        if hwnd:
            BringHwndToFront(hwnd)


# ===============================================================================

class Close(eg.ActionBase):
    name = "Close Fomine LAN Chat window"
    description = "Close Fomine LAN Chat window."

    def __call__(self):
        hwnd = HandleLch()
        if hwnd:
            CloseHwnd(hwnd)


# ===============================================================================

class GetLastMessage(eg.ActionBase):
    name = "Get last message"
    description = "Return last message as eg.result."

    def __call__(self):
        hwnd = HandleLch()
        if hwnd:
            return self.plugin.observThread.GetLastMessage()


# ===============================================================================

class Broadcast(eg.ActionBase):
    name = "Send message"
    description = "Send message."

    class text:
        label = "Message to be sent:"
        tooltip = """Enter the message to be sent.
It may also be a Python expression, such as {eg.result} or {eg.event.payload} !"""

    def __call__(self, message=u""):
        hwnd = HandleLch()
        if hwnd:
            message = eg.ParseString(message)
            edit = GetDlgItem(hwnd, 1002)
            buttonId = 1003
            button = GetDlgItem(hwnd, buttonId)
            for line in message.strip().split("\n"):
                locBuf = create_string_buffer(line.encode(eg.systemEncoding))
                SendMessage(edit, WM_SETTEXT, 0, addressof(locBuf))
                SendMessage(hwnd, WM_COMMAND, buttonId + 65536 * BN_CLICKED, button)
                sleep(0.5)

    def Configure(self, message=u""):
        text = self.text
        panel = eg.ConfigPanel(self)
        labelText = wx.StaticText(panel, -1, text.label)
        messCtrl = wx.TextCtrl(
            panel,
            -1,
            message,
            style=wx.TE_BESTWRAP | wx.TE_MULTILINE
        )
        messCtrl.SetToolTip(text.tooltip)
        panel.sizer.Add(labelText, 0, wx.TOP, 15)
        panel.sizer.Add(messCtrl, 1, wx.TOP | wx.EXPAND, 2)
        while panel.Affirmed():
            panel.SetResult(
                messCtrl.GetValue(),
            )
        # ===============================================================================


class GetStatus(eg.ActionBase):
    name = "Get Fomine LAN Chat status"
    description = "Return Fomine LAN Chat status (Online, Busy, Disconnect) as eg.result."

    class text:
        modeLabel = "Result return as"
        modes = ("Text", "Number (zero based index)")
        states = ("Online", "Busy (no sounds)", "Disconnect")
        status = "Status:"

    def __call__(self, mode=0):
        hwnd = HandleLch()
        if hwnd:
            onLineId = 1009
            busyId = 1010
            disconnectId = 1011
            buttonId = (onLineId, busyId, disconnectId)
            for i in range(len(buttonId)):
                button = GetDlgItem(hwnd, buttonId[i])
                state = SendMessage(button, BM_GETCHECK, 0, 0)
                if state & BST_CHECKED:
                    break
            return i if mode else self.text.status + " " + self.text.states[i]

    def GetLabel(self, mode):
        return "%s: %s" % (
            self.name,
            self.text.modeLabel + " " + self.text.modes[mode].lower()
        )

    def Configure(self, mode=0):
        text = self.text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            text.modeLabel,
            choices=text.modes,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(mode)
        panel.sizer.Add(radioBox, 0, wx.TOP, 15)
        while panel.Affirmed():
            panel.SetResult(
                radioBox.GetSelection(),
            )
        # ===============================================================================


class SetStatus(eg.ActionBase):
    name = "Set Fomine LAN Chat status"
    description = "Set Fomine LAN Chat status (Online, Busy or Disconnect)."

    class text:
        label = "Status"
        states = ("Online", "Busy (no sounds)", "Disconnect")

    def __call__(self, state=0):
        hwnd = HandleLch()
        if hwnd:
            onLineId = 1009
            busyId = 1010
            disconnectId = 1011
            buttonId = (onLineId, busyId, disconnectId)
            for current in range(len(buttonId)):
                button = GetDlgItem(hwnd, buttonId[current])
                st = SendMessage(button, BM_GETCHECK, 0, 0)
                if st & BST_CHECKED:
                    break
            if current == 2 and state == 1:
                SendMessage(hwnd, WM_COMMAND, buttonId[0] + 65536 * BN_CLICKED, GetDlgItem(hwnd, buttonId[0]))
                button = GetDlgItem(hwnd, buttonId[current])
                SendMessage(button, BM_SETSTATE, 0, 0)
                SendMessage(button, BM_SETCHECK, False, 0)
                button = GetDlgItem(hwnd, buttonId[0])
                SendMessage(button, BM_SETSTATE, 1, 0)
                SendMessage(button, BM_SETCHECK, True, 0)
                current = 0
                sleep(2)
            SendMessage(hwnd, WM_COMMAND, buttonId[state] + 65536 * BN_CLICKED, GetDlgItem(hwnd, buttonId[state]))
            button = GetDlgItem(hwnd, buttonId[current])
            SendMessage(button, BM_SETSTATE, 0, 0)
            SendMessage(button, BM_SETCHECK, False, 0)
            button = GetDlgItem(hwnd, buttonId[state])
            SendMessage(button, BM_SETSTATE, 1, 0)
            SendMessage(button, BM_SETCHECK, True, 0)

    def GetLabel(self, state):
        return "%s: %s" % (self.name, self.text.states[state])

    def Configure(self, state=0):
        text = self.text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            text.label,
            choices=text.states,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(state)
        panel.sizer.Add(radioBox, 0, wx.TOP, 15)
        while panel.Affirmed():
            panel.SetResult(
                radioBox.GetSelection(),
            )
        # ===============================================================================


class ClearCommunicationWindow(eg.ActionBase):
    name = "Clear Fomine LAN Chat communication window"
    description = "Clear Fomine LAN Chat communication window."

    def __call__(self):
        hwnd = HandleLch()
        if hwnd:
            buff = create_string_buffer("")
            SendMessage(GetDlgItem(hwnd, 1001), WM_SETTEXT, 0, addressof(buff))
            self.plugin.observThread.ResetLinesCount()


# ===============================================================================

class LANchat(eg.PluginBase):
    text = Text

    def __init__(self):
        self.hwnd = None
        self.observThread = None
        self.AddAction(Run)
        self.AddAction(Minimize)
        self.AddAction(BringToFront)
        self.AddAction(Close)
        self.AddAction(ClearCommunicationWindow)
        self.AddAction(GetLastMessage)
        self.AddAction(Broadcast)
        self.AddAction(GetStatus)
        self.AddAction(SetStatus)

    def __start__(self, path=None, period=1.0, bring=True, suffix_1="NewMessage", suffix_2=""):
        if self.hwnd is None:
            self.hwnd = HandleLch()
        self.lchPath = path
        self.observThread = ObservationThread(
            period,
            bring,
            (suffix_1, suffix_2),
            self.hwnd
        )
        self.observThread.start()

    def __stop__(self):
        if self.observThread:
            if self.observThread.isAlive():
                self.observThread.AbortObservation()
            del self.observThread
        self.observThread = None

    def Configure(self, path="", period=1.0, bring=True, suffix="", suffix_2=""):
        if not suffix:
            suffix = self.text.suffix
        if not suffix_2:
            suffix_2 = self.text.suffix_2
        self.lchPath = path
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        lchPathCtrl = MyDirBrowseButton(
            panel,
            size=(410, -1),
            toolTip=self.text.toolTipFolder,
            dialogTitle=self.text.browseTitle,
            buttonText=eg.text.General.browse
        )
        lchPathCtrl.startDirectory = self.lchPath
        lchPathCtrl.GetTextCtrl().SetEditable(False)
        if self.lchPath == "":
            self.lchPath = self.LANchatPath()
        lchPathCtrl.SetValue(self.lchPath)
        periodNumCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            period,
            integerWidth=5,
            fractionWidth=1,
            allowNegative=False,
            min=0.1,
            increment=0.1,
        )
        intervalLbl = wx.StaticText(panel, -1, self.text.intervalLabel)
        bringCheck = wx.CheckBox(panel, -1, self.text.bring)
        bringCheck.SetValue(bring)
        suffixLbl = wx.StaticText(panel, -1, self.text.suff_1_Label)
        suffixCtrl = wx.TextCtrl(panel, -1, suffix)
        suffix2Lbl = wx.StaticText(panel, -1, self.text.suff_2_Label)
        suffix2Ctrl = wx.TextCtrl(panel, -1, suffix_2)
        suffixSizer = wx.FlexGridSizer(2, 2, 2, 8)
        suffixSizer.Add(suffixLbl, 0, wx.TOP, 2)
        suffixSizer.Add(suffixCtrl, 0)
        suffixSizer.Add(suffix2Lbl, 0, wx.TOP, 7)
        suffixSizer.Add(suffix2Ctrl, 0, wx.TOP, 5)
        periodSizer = wx.BoxSizer(wx.HORIZONTAL)
        periodSizer.Add(intervalLbl, 0, wx.TOP, 2)
        periodSizer.Add(periodNumCtrl, 0, wx.LEFT, 5)
        panelAdd = panel.sizer.Add
        panelAdd(label1Text, 0, wx.TOP, 15)
        panelAdd(lchPathCtrl, 0, wx.TOP, 2)
        panelAdd(periodSizer, 0, wx.TOP, 20)
        panelAdd(suffixSizer, 0, wx.TOP, 20)
        panelAdd(bringCheck, 0, wx.TOP, 20)
        while panel.Affirmed():
            self.hwnd = HandleLch()
            panel.SetResult(
                lchPathCtrl.GetValue(),
                periodNumCtrl.GetValue(),
                bringCheck.IsChecked(),
                suffixCtrl.GetValue(),
                suffix2Ctrl.GetValue(),
            )

    def LANchatPath(self):
        """
        Get the path of LAN Chat's installation directory through querying 
        the Windows registry.
        """
        LANchatPath = ""
        try:
            lch = _winreg.OpenKey(
                _winreg.HKEY_CURRENT_USER,
                "Software\\Fomine Software\\LANChat"
            )
            try:
                LANchatPath = _winreg.QueryValueEx(lch, "Install_Dir")[0]
            except:
                pass
            _winreg.CloseKey(lch)
        except:
            pass
        return LANchatPath
# ===============================================================================
