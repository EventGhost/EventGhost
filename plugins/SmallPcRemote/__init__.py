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

ur"""<rst>
Plugin for the Auvisio PC-Remote.
"""

import eg

eg.RegisterPlugin(
    name = "Small PC-Remote",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{B7440E71-AE2F-4928-9270-5728E81FED5B}",
    description = __doc__,
    hardwareId = "USB\\VID_073A&PID_2230",
)

from math import atan2, pi
from threading import Lock
from types import DictType

BUTTONS = {
    (6, 129, 0): ("Power", 3),
    (3, 138, 1, 3, 0, 0): ("eMail", 3),
    (3, 35, 2, 3, 0, 0): ("WWW", 3),
    (1, 4, 61, 1, 0, 0): ("Close", 3),
    (1, 5, 4, 4, 5, 30, 5, 5, 58, 0, 1, 0, 0, 4, 0, 0, 5, 0, 0, 0): ("A", 10),
    (1, 5, 5, 4, 5, 31, 5, 5, 59, 0, 1, 0, 0, 4, 0, 0, 5, 0, 0, 0): ("B", 10),
    (1, 5, 6, 4, 5, 32, 5, 5, 60, 0, 1, 0, 0, 4, 0, 0, 5, 0, 0, 0): ("C", 10),
    (1, 5, 7, 4, 5, 33, 5, 5, 61, 0, 1, 0, 0, 4, 0, 0, 5, 0, 0, 0): ("D", 10),
    (3, 182, 0, 3, 0, 0): ("PreviousTrack", 3),
    (3, 181, 0, 3, 0, 0): ("NextTrack", 3),
    (3, 203, 0, 1, 0, 80, 4, 1, 80, 5, 3, 5, 0): ("FastRewind", 13),
    (3, 202, 0, 1, 0, 79, 4, 1, 79, 5, 3, 9, 0): ("FastForward", 13),
    (3, 205, 0, 3, 0, 0): ("Play", 3),
    (3, 183, 0, 3, 0, 0): ("Stop", 3),
    (3, 48, 2, 1, 4, 40, 4, 1, 32, 3, 0, 0, 1, 0, 0, 4, 0, 0): ("Fullscreen", 9),
    (3, 226, 0, 3, 0, 0): ("Mute", 3),
    (3, 234, 0): ("VolumeDown", 3),
    (3, 233, 0): ("VolumeUp", 3),
    (1, 0, 42): ("Backspace", 3),
    (1, 0, 75): ("PageUp", 3),
    (1, 0, 78): ("PageDown", 3),
    (1, 8, 8, 1, 0, 0): ("MyPc", 3),
    (1, 8, 7, 1, 0, 0): ("Desktop", 3),
    (1, 0, 43): ("Tab", 3),
    (5, 0, 42, 30, 5, 0, 0, 0): ("Tab", 4),
    (5, 0, 42, 54, 5, 0, 0, 0): ("Tab", 4),
    (5, 0, 42, 55, 5, 0, 0, 0): ("Tab", 4),
    (5, 2, 42, 56, 5, 0, 0, 0): ("Tab", 4),
    (5, 0, 0, 54, 5, 0, 0, 0): ("Tab", 4),
    (1, 0, 82): ("Up", 3),
    (5, 0, 0, 4, 5, 0, 0, 0): ("Up", 4),
    (5, 0, 42, 5, 5, 0, 0, 0): ("Up", 4),
    (5, 0, 42, 6, 5, 0, 0, 0): ("Up", 4),
    (5, 0, 42, 31, 5, 0, 0, 0): ("Up", 4),
    (5, 0, 42, 4, 5, 0, 0, 0): ("Up", 4),
    (5, 2, 42, 4, 5, 0, 0, 0): ("Up", 4),
    (5, 2, 42, 5, 5, 0, 0, 0): ("Up", 4),
    (5, 2, 42, 6, 5, 0, 0, 0): ("Up", 4),
    (5, 2, 0, 4, 5, 0, 0, 0): ("Up", 4),
    (1, 8, 0, 1, 0, 0): ("Start", 3),
    (5, 0, 0, 7, 5, 0, 0, 0): ("Start", 4),
    (5, 0, 42, 8, 5, 0, 0, 0): ("Start", 4),
    (5, 0, 42, 9, 5, 0, 0, 0): ("Start", 4),
    (5, 0, 42, 32, 5, 0, 0, 0): ("Start", 4),
    (5, 0, 42, 7, 5, 0, 0, 0): ("Start", 4),
    (5, 2, 0, 7, 5, 0, 0, 0): ("Start", 4),
    (5, 2, 42, 7, 5, 0, 0, 0): ("Start", 4),
    (5, 2, 42, 8, 5, 0, 0, 0): ("Start", 4),
    (5, 2, 42, 9, 5, 0, 0, 0): ("Start", 4),
    (1, 0, 80): ("Left", 3),
    (5, 0, 0, 10, 5, 0, 0, 0): ("Left", 4),
    (5, 0, 42, 10, 5, 0, 0, 0): ("Left", 4),
    (5, 0, 42, 11, 5, 0, 0, 0): ("Left", 4),
    (5, 0, 42, 12, 5, 0, 0, 0): ("Left", 4),
    (5, 0, 42, 33, 5, 0, 0, 0): ("Left", 4),
    (5, 2, 0, 10, 5, 0, 0, 0): ("Left", 4),
    (5, 2, 42, 10, 5, 0, 0, 0): ("Left", 4),
    (5, 2, 42, 11, 5, 0, 0, 0): ("Left", 4),
    (5, 2, 42, 12, 5, 0, 0, 0): ("Left", 4),
    (1, 0, 40): ("Ok", 3),
    (5, 0, 0, 13, 5, 0, 0, 0): ("Ok", 4),
    (5, 0, 42, 14, 5, 0, 0, 0): ("Ok", 4),
    (5, 0, 42, 15, 5, 0, 0, 0): ("Ok", 4),
    (5, 0, 42, 34, 5, 0, 0, 0): ("Ok", 4),
    (5, 0, 42, 13, 5, 0, 0, 0): ("Ok", 4),
    (5, 2, 0, 13, 5, 0, 0, 0): ("Ok", 4),
    (5, 2, 42, 13, 5, 0, 0, 0): ("Ok", 4),
    (5, 2, 42, 14, 5, 0, 0, 0): ("Ok", 4),
    (5, 2, 42, 15, 5, 0, 0, 0): ("Ok", 4),
    (1, 0, 79): ("Right", 3),
    (5, 0, 0, 16, 5, 0, 0, 0): ("Right", 4),
    (5, 0, 42, 16, 5, 0, 0, 0): ("Right", 4),
    (5, 0, 42, 17, 5, 0, 0, 0): ("Right", 4),
    (5, 0, 42, 18, 5, 0, 0, 0): ("Right", 4),
    (5, 0, 42, 35, 5, 0, 0, 0): ("Right", 4),
    (5, 2, 0, 16, 5, 0, 0, 0): ("Right", 4),
    (5, 2, 42, 16, 5, 0, 0, 0): ("Right", 4),
    (5, 2, 42, 17, 5, 0, 0, 0): ("Right", 4),
    (5, 2, 42, 18, 5, 0, 0, 0): ("Right", 4),
    (1, 1, 18): ("Open", 3),
    (5, 0, 0, 19, 5, 0, 0, 0): ("Open", 4),
    (5, 0, 42, 19, 5, 0, 0, 0): ("Open", 4),
    (5, 0, 42, 20, 5, 0, 0, 0): ("Open", 4),
    (5, 0, 42, 21, 5, 0, 0, 0): ("Open", 4),
    (5, 0, 42, 22, 5, 0, 0, 0): ("Open", 4),
    (5, 0, 42, 36, 5, 0, 0, 0): ("Open", 4),
    (5, 2, 0, 19, 5, 0, 0, 0): ("Open", 4),
    (5, 2, 42, 19, 5, 0, 0, 0): ("Open", 4),
    (5, 2, 42, 20, 5, 0, 0, 0): ("Open", 4),
    (5, 2, 42, 21, 5, 0, 0, 0): ("Open", 4),
    (5, 2, 42, 22, 5, 0, 0, 0): ("Open", 4),
    (1, 0, 81): ("Down", 3),
    (5, 0, 0, 23, 5, 0, 0, 0): ("Down", 4),
    (5, 0, 42, 23, 5, 0, 0, 0): ("Down", 4),
    (5, 0, 42, 24, 5, 0, 0, 0): ("Down", 4),
    (5, 0, 42, 25, 5, 0, 0, 0): ("Down", 4),
    (5, 0, 42, 37, 5, 0, 0, 0): ("Down", 4),
    (5, 2, 0, 23, 5, 0, 0, 0): ("Down", 4),
    (5, 2, 42, 23, 5, 0, 0, 0): ("Down", 4),
    (5, 2, 42, 24, 5, 0, 0, 0): ("Down", 4),
    (5, 2, 42, 25, 5, 0, 0, 0): ("Down", 4),
    (1, 0, 41): ("Esc", 3),
    (5, 0, 0, 26, 5, 0, 0, 0): ("Esc", 4),
    (5, 0, 42, 26, 5, 0, 0, 0): ("Esc", 4),
    (5, 0, 42, 27, 5, 0, 0, 0): ("Esc", 4),
    (5, 0, 42, 28, 5, 0, 0, 0): ("Esc", 4),
    (5, 0, 42, 29, 5, 0, 0, 0): ("Esc", 4),
    (5, 0, 42, 38, 5, 0, 0, 0): ("Esc", 4),
    (5, 2, 0, 26, 5, 0, 0, 0): ("Esc", 4),
    (5, 2, 42, 26, 5, 0, 0, 0): ("Esc", 4),
    (5, 2, 42, 27, 5, 0, 0, 0): ("Esc", 4),
    (5, 2, 42, 28, 5, 0, 0, 0): ("Esc", 4),
    (5, 2, 42, 29, 5, 0, 0, 0): ("Esc", 4),
    (1, 4, 43, 1, 0, 0): ("SwitchWindows", 3),
    (5, 0, 0, 44, 5, 0, 0, 0): ("SwitchWindows", 4),
    (5, 2, 42, 31, 5, 0, 0, 0): ("SwitchWindows", 4),
    (5, 2, 42, 37, 5, 0, 0, 0): ("SwitchWindows", 4),
    (5, 2, 42, 32, 5, 0, 0, 0): ("SwitchWindows", 4),
    (5, 0, 42, 39, 5, 0, 0, 0): ("SwitchWindows", 4),
    (5, 0, 42, 44, 5, 0, 0, 0): ("SwitchWindows", 4),
}

def CreateTree():
    tree = {}
    for key, name in BUTTONS.iteritems():
        current = tree
        for value in key[:-1]:
            if value not in current:
                current[value] = {}
            current = current[value]
        current[key[-1]] = name
    return tree

ROOT_NODE = CreateTree()


class SmallPcRemote(eg.PluginBase):

    def __start__(self):
        self.buf = []
        self.currentNode = ROOT_NODE
        self.lastEvent = None
        self.lastDirection = None
        self.lastMouseState = 0
        self.stopCodeLength = 0
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "Small PC Remote Controller",
            "USB\\VID_073A&PID_2230",
            "{FAC603C0-044F-4766-A5C3-A1DBE493579E}",
            self.Callback1,
            1
        )
        self.usb.Open()
        self.timer = eg.ResettableTimer(self.OnTimeOut)


    def __stop__(self):
        self.timer.Stop()
        self.usb.Close()
        

    def ResetState(self):
        self.currentNode = ROOT_NODE
        self.buf = []
        self.lastDirection = None
        

    def Callback1(self, data):
        value = data[0]
        self.buf.append(value)
        if self.buf[0] == 2:
            if len(self.buf) < 4:
                return
            mButton, x, y = self.buf[1:4]
            if mButton != self.lastMouseState:
                self.lastMouseState = mButton
                if mButton == 32:
                    self.TriggerEnduringEvent("LeftMouseButton")
                elif mButton == 64:
                    self.TriggerEnduringEvent("RightMouseButton")
                else:
                    self.EndLastEvent()
            if x != 0 or y != 0:
                if x > 127:
                    x -= 256
                if y > 127:
                    y -= 256
                degree = (round((atan2(x, -y) / pi) * 180)) % 360
                if self.lastDirection != degree:
                    self.TriggerEnduringEvent("MouseDirection.%03d" % degree)
                    self.lastDirection = degree
                self.timer.Reset(75)
            self.buf = []
            self.lastEvent = None
        elif not self.stopCodeLength and self.buf == [1, 0, 0]:
            self.TriggerEvent("NumLock")
            self.ResetState()
            self.lastEvent = None
        elif self.buf == [1, 3, 0]:
            self.ResetState()
        elif value in self.currentNode:
            self.currentNode = self.currentNode[value]
            if type(self.currentNode) is not DictType:
                eventname, self.stopCodeLength = self.currentNode
                if eventname != self.lastEvent:
                    self.lastEvent = eventname
                    self.TriggerEnduringEvent(eventname)
                self.ResetState()
        elif len(self.buf) < self.stopCodeLength:
            return
        else:
            self.ResetState()
            self.lastEvent = None
            self.stopCodeLength = 0
            self.EndLastEvent()


    def OnTimeOut(self):
        self.EndLastEvent()
        self.lastDirection = None

