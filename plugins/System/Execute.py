# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

import eg
import wx
from os.path import basename, dirname, abspath, split, splitext
from threading import Thread
from time import sleep
from win32con import SPI_SETFOREGROUNDLOCKTIMEOUT, SPIF_SENDWININICHANGE, SPIF_UPDATEINIFILE
from win32file import Wow64DisableWow64FsRedirection, Wow64RevertWow64FsRedirection

from eg.WinApi import IsWin64

from eg.WinApi.Dynamic import (
    sizeof, byref, CreateProcess, WaitForSingleObject, FormatError,
    CloseHandle, create_unicode_buffer,
    STARTUPINFO, PROCESS_INFORMATION,
    CREATE_NEW_CONSOLE, STARTF_USESHOWWINDOW, INFINITE,
    GetExitCodeProcess, DWORD,
    IsWindowVisible, RegisterWindowMessage,
    AttachThreadInput, GetCurrentThreadId, GetForegroundWindow,
    GetWindowThreadProcessId, SystemParametersInfoW,
)

from eg.WinApi.Utils import (
    BringHwndToFront, GetHwnds, GetPids, PluginIsEnabled, ProcessExists,
)

WINSTATE_FLAGS = (
    1, # SW_SHOWNORMAL
    6, # SW_MINIMIZE | SW_HIDE
    3, # SW_SHOWMAXIMIZED
    0, # SW_HIDE
)

PRIORITY_FLAGS = (
    64,    # IDLE_PRIORITY_CLASS
    16384, # BELOW_NORMAL_PRIORITY_CLASS
    32,    # NORMAL_PRIORITY_CLASS
    32768, # ABOVE_NORMAL_PRIORITY_CLASS
    256,   # REALTIME_PRIORITY_CLASS
)


class Execute(eg.ActionBase):
    name = "Start Application"
    description = "Starts an executable file."
    iconFile = "icons/Execute"
    class text:
        label = "Start Program: %s"
        FilePath = "Executable:"
        WorkingDir = "Working directory:"
        Parameters = "Command line options:"
        WindowOptionsDesc = "Window options:"
        WindowOptions = (
            "Normal window",
            "Minimized",
            "Maximized",
            "Hidden"
        )
        ProcessOptionsDesc = "Process priority:"
        ProcessOptions = (
            "Realtime",
            "Above normal",
            "Normal",
            "Below normal",
            "Idle"
        )
        waitCheckbox = "Wait until application is terminated before proceeding"
        eventCheckbox = "Trigger event when application is terminated"
        wow64Checkbox = "Disable WOW64 filesystem redirection for this application"
        eventSuffix = "Application.Terminated"
        browseExecutableDialogTitle = "Choose the executable"
        browseWorkingDirDialogTitle = "Choose the working directory"


    def __call__(
        self,
        pathname='',
        arguments='',
        winState=0,
        waitForCompletion=False,
        priority=2,
        workingDir="",
        triggerEvent=False,
        disableWOW64=False,
    ):
        returnValue = None
        pathname = eg.ParseString(pathname)
        if not workingDir:
            workingDir = dirname(abspath(pathname))
        arguments = eg.ParseString(arguments)
        commandLine = create_unicode_buffer('"%s" %s' % (pathname, arguments))
        startupInfo = STARTUPINFO()
        startupInfo.cb = sizeof(STARTUPINFO)
        startupInfo.dwFlags = STARTF_USESHOWWINDOW
        startupInfo.wShowWindow = WINSTATE_FLAGS[winState]
        priorityFlag = PRIORITY_FLAGS[priority]
        processInformation = self.processInformation = PROCESS_INFORMATION()
        disableWOW64 = disableWOW64 and IsWin64()
        if disableWOW64:
            prevVal = Wow64DisableWow64FsRedirection()
        activeThread = GetWindowThreadProcessId(GetForegroundWindow(), None)
        currentThread = GetCurrentThreadId()
        attached = AttachThreadInput(currentThread, activeThread, True)
        SystemParametersInfoW(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, 0, SPIF_SENDWININICHANGE | SPIF_UPDATEINIFILE)
        res = CreateProcess(
            None,              # lpApplicationName
            commandLine,       # lpCommandLine
            None,              # lpProcessAttributes
            None,              # lpThreadAttributes
            False,             # bInheritHandles
            priorityFlag|CREATE_NEW_CONSOLE, # dwCreationFlags
            None,              # lpEnvironment
            workingDir,        # lpCurrentDirectory
            startupInfo,       # lpStartupInfo
            processInformation # lpProcessInformation
        )
        if attached:
            AttachThreadInput(currentThread, activeThread, False)
        if disableWOW64:
            Wow64RevertWow64FsRedirection(prevVal)
        suffix = "%s.%s" % (
                self.text.eventSuffix,
                splitext(split(pathname)[1])[0]
            )
        prefix = self.plugin.name.replace(' ', '')
        if res == 0:
            raise self.Exception(FormatError())
        if waitForCompletion:
            WaitForSingleObject(processInformation.hProcess, INFINITE)
            exitCode = DWORD()
            if not GetExitCodeProcess(
                processInformation.hProcess,
                byref(exitCode)
            ):
                raise self.Exception(FormatError())
            returnValue = exitCode.value
            if triggerEvent:
                eg.TriggerEvent(suffix, prefix = prefix)
            CloseHandle(processInformation.hProcess)
            CloseHandle(processInformation.hThread)
            return returnValue
        elif triggerEvent:
            te=self.TriggerEvent(processInformation, suffix, prefix)
            te.start()
        else:
            CloseHandle(processInformation.hProcess)
            CloseHandle(processInformation.hThread)


    class TriggerEvent(Thread):

        def __init__(self, processInformation, suffix, prefix):
            Thread.__init__(self)
            self.processInformation = processInformation
            self.suffix = suffix
            self.prefix = prefix

        def run(self):
            WaitForSingleObject(self.processInformation.hProcess, INFINITE)
            exitCode = DWORD()
            if not GetExitCodeProcess(
                self.processInformation.hProcess,
                byref(exitCode)
            ):
                raise self.Exception(FormatError())
            CloseHandle(self.processInformation.hProcess)
            CloseHandle(self.processInformation.hThread)
            eg.TriggerEvent(self.suffix, prefix = self.prefix)


    def GetLabel(self, pathname='', *dummyArgs):
        return self.text.label % basename(pathname)


    def Configure(
        self,
        pathname='',
        arguments='',
        winState=0,
        waitForCompletion=False,
        priority=2,
        workingDir="",
        triggerEvent=False,
        disableWOW64=False,
    ):
        panel = eg.ConfigPanel()
        text = self.text
        filepathCtrl = panel.FileBrowseButton(
            pathname,
            fileMask="*.*",
            dialogTitle=text.browseExecutableDialogTitle
        )
        argumentsCtrl = panel.TextCtrl(arguments)
        workingDirCtrl = panel.DirBrowseButton(
            workingDir or "",
            dialogTitle=text.browseWorkingDirDialogTitle
        )
        #workingDirCtrl.SetValue(workingDir)
        winStateChoice = panel.Choice(winState, text.WindowOptions)
        priorityChoice = panel.Choice(4 - priority, text.ProcessOptions)
        waitCheckBox = panel.CheckBox(
            bool(waitForCompletion),
            text.waitCheckbox
        )
        eventCheckBox = panel.CheckBox(
            bool(triggerEvent),
            text.eventCheckbox
        )
        wow64CheckBox = panel.CheckBox(
            bool(disableWOW64),
            text.wow64Checkbox
        )

        SText = panel.StaticText
        lowerSizer = wx.GridBagSizer(0, 0)
        lowerSizer.AddGrowableCol(1)
        lowerSizer.AddGrowableCol(3)
        lowerSizer.AddMany([
            (SText(text.WindowOptionsDesc), (0, 0), (1, 1), wx.ALIGN_BOTTOM),
            (winStateChoice, (1, 0)),
            ((1, 1), (0, 1), (1, 1), wx.EXPAND),
            (SText(text.ProcessOptionsDesc), (0, 2), (1, 1), wx.ALIGN_BOTTOM),
            (priorityChoice, (1, 2)),
            ((1, 1), (0, 3), (1, 1), wx.EXPAND),
        ])

        panel.sizer.AddMany([
            (SText(text.FilePath)),
            (filepathCtrl, 0, wx.EXPAND),
            ((10, 10)),
            (SText(text.Parameters)),
            (argumentsCtrl, 0, wx.EXPAND),
            ((10, 10)),
            (SText(text.WorkingDir)),
            (workingDirCtrl, 0, wx.EXPAND),
            (lowerSizer, 0, wx.EXPAND),
            ((10, 15)),
            (waitCheckBox),
            ((10, 8)),
            (eventCheckBox),
            ((10, 8)),
            (wow64CheckBox),
        ])

        while panel.Affirmed():
            panel.SetResult(
                filepathCtrl.GetValue(),
                argumentsCtrl.GetValue(),
                winStateChoice.GetValue(),
                waitCheckBox.GetValue(),
                4 - priorityChoice.GetValue(),
                workingDirCtrl.GetValue(),
                eventCheckBox.GetValue(),
                wow64CheckBox.GetValue()
            )

