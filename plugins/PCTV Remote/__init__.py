# -*- coding: utf-8 -*-
#
# plugins/PCTV Remote/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
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
#
# Changelog:
# 1.0.0 by Wiedmann
#       - initial release
# 1.1.0 by Wiedmann
#       - use Poll and a Queue instead of Timers
#

import eg

eg.RegisterPlugin(
    name = "PCTV Remote",
    author = "Carsten Wiedmann",
    version = "1.1.0",
    kind = "remote",
    guid = "{38121B62-9F24-11E1-BEE6-9AEC6188709B}",
    description = "Plugin for the PCTV Remote Control.",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&amp;t=3863",
    help = """
        <h5>Prerequirement</h5>
        <ul>
            <li>
                You have to install the TVCenter 6 Software from
                <a href='http://www.pctvsystems.com/'>PCTV Systems</a>
                (to get 'RemoTerm 3.x').
            </li>
            <li>
                Your remote must be configured and 'remoterm.exe' must
                be started.
            </li>
        </ul>
        <h5>Configuration</h5>
        <p>
            <ol>
                <li>
                    Backup the file 'profiles.ini'.<br />
                    (in '%ProgramData%\\PCTV Systems\\RemoTerm\\Profiles\\')
                </li>
                <li>
                    Copy the 'profiles.ini' from the plugin directory
                    to the above directory.
                </li>
                <li>Copy 'n paste the lines:
                    <ul>
                        <li>HWID=</li>
                        <li>port=</li>
                        <li>protocol=</li>
                        <li>keymap=</li>
                    </ul>
                    from your backup to the new one (override existing lines).
                </li>
                <li>
                    Restart 'remoterm.exe'.<br />
                    (in '%CommonProgramFiles%\\PCTV Systems\\RemoTerm\\')
                </li>
            </ol>
        </p>
        <p>
            In the directory '%ProgramFiles%\\PCTV Systems\\TVCenter\\' you
            can find the file 'Remote_XX.pdf' which shows the keycodes
            for your remote.
        </p>
        <p>
            Each button is generating two keycodes. One for a short, and one
            for a long keypress (+64 after a half second). A long keypress
            can be used together with the EventGhost autorepeat macro.
        </p>
        <p>
            In the plugin directory you can also find an EventGhost
            configuration example to control the PCTV TVCenter software
            (keymapping is for a Remote Control Typ C).
        </p>
    """,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7EAAAOxAGV"
        "Kw4bAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAG+"
        "SURBVHjajJI9aBRRFIW/+2Y2mR3UiEbBqGQTfxEsbEVEsBALtRLsBMEqlQgBEVOJoKBB"
        "LWIjCBKTQoQUFiqBRUEsRIWALjGgEcJG86OYdXZ2dmauxeDCZjZxLrzm3nc+zjv3iaqS"
        "tRT02XzI4NeA4mLI9d0OdhZhNUKHy3UGpwM+LkWN/sufYTNAfU/rr55i7dqPVdgrAMPl"
        "ul4o1ZgLWjtNAKpaL45RfXADXfyOtOdZc++Fms4tcvlzsKIYwERfPmml/zTerYvEC7MJ"
        "r1bFH7kLQBCvnpHxH94kKr1PDYLxx8Tlb2rL6vkY52w/pquQnoQh/sgdXGtlQnfeIKqK"
        "+p76QwPUxp8gIv9iwT56kuKZPj543VQiTU6oVELodYUrO9oTQMN2cUz9oQHEXYtz7hIT"
        "PVOU5kbpWneQA1v76HB6U3Zk+UdS31Ox21gIJnk+eR7VOLkoFocKV9m+/kgTxKSIjiux"
        "BW+mrzXEyZMi5v9MpENsFU7pxyN+VadS/XyuMxtg5vfrlqnnc5uyAXZuPIWRXKrvZgX0"
        "bDguJ/aNsq3jcDOgbTP/3cLyml16q+9mbmPE5tie+wimaQt/BwDFxL0/5O+XdAAAAABJ"
        "RU5ErkJggg=="
    )
)

import Queue

from eg.WinApi.Dynamic import (
    _user32,
    byref,
    WinError,
    CreateWindow,
    DestroyWindow,
    GetModuleHandle,
    RegisterClass,
    UnregisterClass,
    BOOL,
    HANDLE,
    HWND,
    LPCWSTR,
    WINFUNCTYPE,
    WNDCLASS,
    WNDPROC,
    CW_USEDEFAULT,
    WM_KEYDOWN,
    WS_OVERLAPPEDWINDOW
)

prototype = WINFUNCTYPE(BOOL, HWND, LPCWSTR, HANDLE)
paramflags = (1, "hWnd", 0), (1, "lpString", None), (1, "hData", 0)
SetProp = prototype(("SetPropW", _user32), paramflags)

prototype = WINFUNCTYPE(HANDLE, HWND, LPCWSTR)
paramflags = (1, "hWnd", 0), (1, "lpString", None)
RemoveProp = prototype(("RemovePropW", _user32), paramflags)



class PCTVMessageReceiver(eg.ThreadWorker):
    def Setup(self, plugin, msgQueue):
        self.plugin = plugin
        self.msgQueue = msgQueue

        self.wndClass = WNDCLASS(
            lpfnWndProc = WNDPROC(self.WindowProc),
            hInstance = GetModuleHandle(None),
            lpszClassName = "HiddenPCTVMessageReceiver"
        )
        if not RegisterClass(byref(self.wndClass)):
            raise WinError()

        self.hWnd = CreateWindow(
            self.wndClass.lpszClassName,
            self.wndClass.lpszClassName,
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            None,
            None,
            self.wndClass.hInstance,
            None
        )
        if not self.hWnd:
            raise WinError()

        if not SetProp(self.hWnd, self.wndClass.lpszClassName, 658020):
            raise WinError()


    def Finish(self):
        if not RemoveProp(self.hWnd, self.wndClass.lpszClassName):
            raise WinError()

        if not DestroyWindow(self.hWnd):
            raise WinError()

        if not (
            UnregisterClass(
                self.wndClass.lpszClassName,
                self.wndClass.hInstance
            )
        ):
            raise WinError()


    def WindowProc(self, hWnd, Mesg, wParam, lParam):
        if Mesg == WM_KEYDOWN:
            self.msgQueue.put([wParam, lParam])

        return 1



class PCTVProcessMessage(eg.ThreadWorker):
    def Setup(self, plugin, msgQueue):
        self.plugin = plugin
        self.msgQueue = msgQueue


    def Finish(self):
        print "{0!s} is stopped.".format(self.plugin.name)


    def Poll(self):
        lastMessage = None
        msgList = []

        waitTimeSingle = 0.500
        waitTimeDouble = 0.250
        waitTime = waitTimeSingle

        while not self.msgQueue.empty():
            self.msgQueue.get(False)
            self.msgQueue.task_done()

        print "{0!s} is started.".format(self.plugin.name)

        while True:
            if not self.plugin.alive:
                return

            try:
                for x in range(2):
                    msgList.append(self.msgQueue.get(True, waitTime))
            except Queue.Empty:
                if lastMessage:
                    lastMessage.SetShouldEnd()
                    lastMessage = None
                    msgList = []
                    waitTime = waitTimeSingle
                    if 0 < len(msgList):
                        self.msgQueue.task_done()
                    continue

            while 0 < len(msgList):
                if (
                    2 == len(msgList) and
                    2 == msgList[1][1] and
                    64 == msgList[1][0] - msgList[0][0]
                ):
                    msgList.pop(0)
                    self.msgQueue.task_done()
                    continue

                currMessage = msgList.pop(0)

                if 1 == currMessage[1]:
                    self.plugin.TriggerEvent(
                        str(currMessage[0]), str(currMessage[1])
                    )
                    lastMessage = None
                    waitTime = waitTimeSingle
                elif (
                    2 == currMessage[1] and not
                    (
                        lastMessage and
                        int(lastMessage.suffix) == currMessage[0]
                    )
                ):
                    lastMessage = self.plugin.TriggerEnduringEvent(
                        str(currMessage[0]), str(currMessage[1])
                    )
                    waitTime = waitTimeDouble

                self.msgQueue.task_done()



class PCTVRemote(eg.PluginBase):
    def __init__(self):
        self.AddEvents()


    def __start__(self):
        self.alive = True
        self.msgQueue = Queue.Queue()
        self.msgThread = PCTVMessageReceiver(
            self, self.msgQueue
        )
        self.msgThread.Start()
        self.procThread = PCTVProcessMessage(
            self, self.msgQueue
        )
        self.procThread.Start()


    def __stop__(self):
        self.alive = False
        self.msgThread.Stop()
        self.procThread.Stop()
