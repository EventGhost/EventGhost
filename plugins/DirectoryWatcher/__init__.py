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

eg.RegisterPlugin(
    name = "Directory Watcher",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    canMultiLoad = True,
    description = (
        "Monitors a directory and generates events if files are created, "
        "deleted or changed in it."
    ),
)


import wx

import os
import threading

import win32file
import win32con
import win32event
import pywintypes

FILE_LIST_DIRECTORY = 0x0001

class Text:
    watchPath = "Watch path:"
    watchSubDirs = "Watch subdirectories also"
    
    

class DirectoryWatcher(eg.PluginClass):
    text = Text
    
    def __start__(self, path, includeSubdirs):
        self.stopEvent = win32event.CreateEvent(None, 1, 0, None)
        self.path = path
        self.includeSubdirs = includeSubdirs
        startupEvent = threading.Event()
        self.thread = threading.Thread(target=self.ThreadLoop, name="DirectoryWatcherThread", args=(startupEvent,))
        self.thread.start()
        startupEvent.wait(3)
        
        
    def __stop__(self):
        if self.thread is not None:
            win32event.PulseEvent(self.stopEvent)
            self.thread.join(5.0)
        
        
    def TestFile(self, path):
        try:
            handle = win32file.CreateFile(
                path,
                win32file.GENERIC_READ,
                0,
                None,
                win32con.OPEN_EXISTING,
                0,
                None
            )
            win32file.CloseHandle(handle)
            return True
        except:
            return False
        
        
    def ThreadLoop(self, startupEvent):
        try:
            from win32event import (
                INFINITE, 
                QS_ALLINPUT, 
                WAIT_OBJECT_0,
                MsgWaitForMultipleObjects
            )
            from win32file import (
                ReadDirectoryChangesW, 
                GetOverlappedResult,
                FILE_NOTIFY_INFORMATION
            )
                
            try:
                hDir = win32file.CreateFile(
                    self.path,
                    FILE_LIST_DIRECTORY,
                    win32con.FILE_SHARE_READ|win32con.FILE_SHARE_WRITE,
                    None,
                    win32con.OPEN_EXISTING,
                    (
                        win32con.FILE_FLAG_BACKUP_SEMANTICS
                        |win32con.FILE_FLAG_OVERLAPPED
                    ),
                    None
                )
            except pywintypes.error, e:
                self.PrintError(e[2])
                startupEvent.set()
                return
            overlapped = win32file.OVERLAPPED()
            overlapped.hEvent = win32event.CreateEvent(None, 1, 0, None)
            buffer = win32file.AllocateReadBuffer(1024)
            events = (overlapped.hEvent, self.stopEvent)
            flags = (
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY
            )
            includeSubdirs = self.includeSubdirs
            renamePath = None
            startupEvent.set()
            while 1:
                ReadDirectoryChangesW(
                    hDir,
                    buffer,
                    includeSubdirs,
                    flags,
                    overlapped,
                )
                rc = MsgWaitForMultipleObjects(events, 0, INFINITE, QS_ALLINPUT)
                if rc == WAIT_OBJECT_0:    
                    size = GetOverlappedResult(hDir, overlapped, 1)
                    results = FILE_NOTIFY_INFORMATION(buffer, size)
                    for action, file in results:
                        fullFilename = os.path.join(self.path, file)
                        if action ==  1: 
                            self.TriggerEvent("Created", (fullFilename,))
                        elif action ==  2: 
                            self.TriggerEvent("Deleted", (fullFilename,))
                        elif action ==  3: 
                            self.TriggerEvent("Updated", (fullFilename,))
                        elif action == 4:
                            renamePath = fullFilename
                        elif action == 5:
                            self.TriggerEvent(
                                "Renamed", 
                                (renamePath, fullFilename)
                            )
                            renamePath = None
                elif rc == WAIT_OBJECT_0+1:
                    break
            win32file.CloseHandle(hDir)
        except:
            self.thread = None
            raise
                
            
    def Configure(self, path="", includeSubdirs=False):
        panel = eg.ConfigPanel(self)
        dirpathCtrl = panel.DirBrowseButton(path)
        includeSubdirsCB = panel.CheckBox(includeSubdirs, self.text.watchSubDirs)
        
        panel.AddLine(self.text.watchPath, dirpathCtrl)
        panel.AddLine(includeSubdirsCB)

        if panel.Affirmed():
            return (
                dirpathCtrl.GetValue(),
                includeSubdirsCB.GetValue(),
            )
    