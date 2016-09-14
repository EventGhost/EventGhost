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
    name = "Directory Watcher",
    author = "Bitmonster",
    version = "1.0",
    guid = "{003FABA6-AA6A-4395-9DB6-DC88EB07F5FE}",
    canMultiLoad = True,
    description = (
        "Monitors a directory and generates events if files are created, "
        "deleted or changed in it."
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=2&t=3215",
)

import os
import threading

from eg.WinApi.Dynamic import (
# functions:
    FormatError, byref, cast, addressof, wstring_at, sizeof,
    CreateEvent,
    PulseEvent,
    CreateFile,
    CloseHandle,
    MsgWaitForMultipleObjects,
    ReadDirectoryChangesW,
    GetOverlappedResult,
# types:
    c_byte,
    DWORD,
    WCHAR,
    HANDLE,
    OVERLAPPED,
    FILE_NOTIFY_INFORMATION,
    LPOVERLAPPED_COMPLETION_ROUTINE,
    FILE_NOTIFY_INFORMATION,
# constants:
    INFINITE,
    INVALID_HANDLE_VALUE,
    QS_ALLINPUT,
    WAIT_OBJECT_0,
    OPEN_EXISTING,
    FILE_SHARE_READ,
    FILE_SHARE_WRITE,
    FILE_FLAG_BACKUP_SEMANTICS,
    FILE_FLAG_OVERLAPPED,
    FILE_NOTIFY_CHANGE_FILE_NAME,
    FILE_NOTIFY_CHANGE_DIR_NAME,
    FILE_NOTIFY_CHANGE_ATTRIBUTES,
    FILE_NOTIFY_CHANGE_SIZE,
    FILE_NOTIFY_CHANGE_LAST_WRITE,
    FILE_NOTIFY_CHANGE_SECURITY,
    FILE_LIST_DIRECTORY,
    FILE_ACTION_ADDED,
    FILE_ACTION_REMOVED,
    FILE_ACTION_MODIFIED,
    FILE_ACTION_RENAMED_OLD_NAME,
    FILE_ACTION_RENAMED_NEW_NAME,
)

BUFSIZE = 8192
WCHAR_SIZE = sizeof(WCHAR)

class Text:
    watchPath = "Watch path:"
    watchSubDirs = "Watch subdirectories also"



class DirectoryWatcher(eg.PluginClass):
    text = Text

    def __start__(self, path, includeSubdirs):
        self.stopEvent = CreateEvent(None, 1, 0, None)
        self.path = path
        self.startException = None
        self.includeSubdirs = includeSubdirs
        startupEvent = threading.Event()
        self.thread = threading.Thread(
            target=self.ThreadLoop,
            name="DirectoryWatcherThread",
            args=(startupEvent,)
        )
        self.thread.start()
        startupEvent.wait(3)
        if self.startException is not None:
            raise self.Exception(self.startException)


    def __stop__(self):
        if self.thread is not None:
            PulseEvent(self.stopEvent)
            self.thread.join(5.0)


    def ThreadLoop(self, startupEvent):
        try:
            hDir = CreateFile(
                self.path,
                FILE_LIST_DIRECTORY,
                FILE_SHARE_READ|FILE_SHARE_WRITE,
                None,
                OPEN_EXISTING,
                FILE_FLAG_BACKUP_SEMANTICS|FILE_FLAG_OVERLAPPED,
                0
            )
            if hDir == INVALID_HANDLE_VALUE:
                self.startException = FormatError()
                startupEvent.set()
                return
            overlapped = OVERLAPPED()
            overlapped.hEvent = CreateEvent(None, 1, 0, None)
            buffer = (c_byte * BUFSIZE )()
            events = (HANDLE * 2)(overlapped.hEvent, self.stopEvent)
            flags = (
                FILE_NOTIFY_CHANGE_FILE_NAME |
                FILE_NOTIFY_CHANGE_DIR_NAME |
                FILE_NOTIFY_CHANGE_ATTRIBUTES |
                FILE_NOTIFY_CHANGE_SIZE |
                FILE_NOTIFY_CHANGE_LAST_WRITE |
                FILE_NOTIFY_CHANGE_SECURITY
            )
            includeSubdirs = self.includeSubdirs
            renamePath = None
            bytesReturned = DWORD()
            noneCallback = cast(None, LPOVERLAPPED_COMPLETION_ROUTINE)
            startupEvent.set()
            while 1:
                ReadDirectoryChangesW(
                    hDir,
                    buffer,
                    BUFSIZE,
                    includeSubdirs,
                    flags,
                    byref(bytesReturned),
                    byref(overlapped),
                    noneCallback
                )
                rc = MsgWaitForMultipleObjects(
                    2, events, 0, INFINITE, QS_ALLINPUT
                )
                if rc == WAIT_OBJECT_0:
                    res = GetOverlappedResult(
                        hDir, byref(overlapped), byref(bytesReturned), 1
                    )
                    address = addressof(buffer)
                    while True:
                        fni = FILE_NOTIFY_INFORMATION.from_address(address)
                        length = fni.FileNameLength / WCHAR_SIZE
                        fileName = wstring_at(address + 12, length)
                        action = fni.Action
                        fullFilename = os.path.join(self.path, fileName)
                        if action == FILE_ACTION_ADDED:
                            self.TriggerEvent("Created", (fullFilename,))
                        elif action == FILE_ACTION_REMOVED:
                            self.TriggerEvent("Deleted", (fullFilename,))
                        elif action == FILE_ACTION_MODIFIED:
                            self.TriggerEvent("Updated", (fullFilename,))
                        elif action == FILE_ACTION_RENAMED_OLD_NAME:
                            renamePath = fullFilename
                        elif action == FILE_ACTION_RENAMED_NEW_NAME:
                            self.TriggerEvent(
                                "Renamed",
                                (renamePath, fullFilename)
                            )
                            renamePath = None
                        if fni.NextEntryOffset == 0:
                            break
                        address += fni.NextEntryOffset
                elif rc == WAIT_OBJECT_0+1:
                    break
            CloseHandle(hDir)
        except:
            self.thread = None
            raise


    def Configure(self, path="", includeSubdirs=False):
        panel = eg.ConfigPanel()
        dirpathCtrl = panel.DirBrowseButton(path)
        includeSubdirsCB = panel.CheckBox(
            includeSubdirs, self.text.watchSubDirs
        )

        panel.AddLine(self.text.watchPath, dirpathCtrl)
        panel.AddLine(includeSubdirsCB)

        while panel.Affirmed():
            panel.SetResult(
                dirpathCtrl.GetValue(),
                includeSubdirsCB.GetValue(),
            )

