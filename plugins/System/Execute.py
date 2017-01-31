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

import os
import wx
from os.path import (
    abspath, basename, dirname, expandvars, isdir, split, splitext
)
from threading import Thread
from win32file import (
    Wow64DisableWow64FsRedirection, Wow64RevertWow64FsRedirection
)
from win32process import GetPriorityClass, SetPriorityClass

# Local imports
import eg
from eg.WinApi import IsWin64
from eg.WinApi.Dynamic import (
    AttachThreadInput, byref, CloseHandle, DWORD, FormatError,
    GetCurrentThreadId, GetExitCodeProcess, GetForegroundWindow,
    GetWindowThreadProcessId, INFINITE, SEE_MASK_NOCLOSEPROCESS,
    SHELLEXECUTEINFO, sizeof, WaitForSingleObject, windll,
)

PATHEXT = tuple(os.environ.get(
    "PATHEXT",
    ".COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC"
).upper().split(os.path.pathsep) + [".MSC"])

PRIORITY_FLAGS = (
    64,     # IDLE_PRIORITY_CLASS
    16384,  # BELOW_NORMAL_PRIORITY_CLASS
    32,     # NORMAL_PRIORITY_CLASS
    32768,  # ABOVE_NORMAL_PRIORITY_CLASS
    128,    # HIGH_PRIORITY_CLASS
    256,    # REALTIME_PRIORITY_CLASS
)

WINSTATE_FLAGS = (
    1,  # SW_SHOWNORMAL
    6,  # SW_MINIMIZE | SW_HIDE
    3,  # SW_SHOWMAXIMIZED
    0,  # SW_HIDE
)

class Execute(eg.ActionBase):
    name = "Run Application"
    description = "Runs an executable file or opens any file or folder."
    iconFile = "icons/Execute"

    class text:
        label = "Run Application: %s"
        labelFile = "Open File: %s"
        labelFolder = "Open Folder: %s"
        FilePath = "File or folder to open:"
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
            "High",
            "Above normal",
            "Normal",
            "Below normal",
            "Idle"
        )
        waitCheckbox = "Wait until application is terminated before proceeding"
        eventCheckbox = "Trigger event when application is terminated"
        wow64Checkbox = (
            "Disable WOW64 filesystem redirection for this application"
        )
        runAsAdminCheckbox = (
            "Run as Administrator (UAC prompt will appear if UAC is enabled!)"
        )
        eventSuffix = "Application.Terminated"
        browseExecutableDialogTitle = "Choose the executable"
        browseWorkingDirDialogTitle = "Choose the working directory"
        disableParsing = "Disable parsing of string"
        additionalSuffix = "Additional Suffix:"
        priorityIssue = "WARNING: Couldn't set priority!"

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
            if hasattr(self.processInformation, "hThread"):
                CloseHandle(self.processInformation.hThread)
            eg.TriggerEvent(self.suffix, prefix = self.prefix)

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
        additionalSuffix="",
        disableParsingPathname=False,
        disableParsingArguments=False,
        disableParsingAdditionalSuffix=False,
        runAsAdmin = False,
    ):
        if eg.config.refreshEnv:
            eg.Environment.Refresh()
        returnValue = None
        pathname = expandvars(pathname)
        arguments = expandvars(arguments)
        workingDir = expandvars(workingDir)
        if not disableParsingPathname:
            pathname = eg.ParseString(pathname)
        if not disableParsingArguments:
            arguments = eg.ParseString(arguments)
        if not disableParsingAdditionalSuffix:
            additionalSuffix = eg.ParseString(additionalSuffix)
        if not workingDir:
            workingDir = dirname(abspath(pathname))
        processInformation = self.processInformation = SHELLEXECUTEINFO()
        processInformation.cbSize = sizeof(processInformation)
        processInformation.hwnd = 0
        processInformation.lpFile = pathname
        processInformation.lpParameters = arguments
        processInformation.lpDirectory = workingDir
        processInformation.nShow = WINSTATE_FLAGS[winState]
        processInformation.hInstApp = 0
        processInformation.fMask = SEE_MASK_NOCLOSEPROCESS
        if runAsAdmin:
            processInformation.lpVerb = "runas"
        disableWOW64 = disableWOW64 and IsWin64()
        if disableWOW64:
            prevVal = Wow64DisableWow64FsRedirection()
        activeThread = GetWindowThreadProcessId(GetForegroundWindow(), None)
        currentThread = GetCurrentThreadId()
        attached = AttachThreadInput(currentThread, activeThread, True)

        if not windll.shell32.ShellExecuteExW(byref(processInformation)):
            raise self.Exception(FormatError())

        if attached:
            AttachThreadInput(currentThread, activeThread, False)
        if disableWOW64:
            Wow64RevertWow64FsRedirection(prevVal)
        if priority != 2:
            try:
                SetPriorityClass(
                    processInformation.hProcess,
                    PRIORITY_FLAGS[priority]
                )
                priorityClass = GetPriorityClass(processInformation.hProcess)
                if priorityClass != PRIORITY_FLAGS[priority]:
                    raise
            except:
                pid = windll.kernel32.GetProcessId(processInformation.hProcess)
                pi = SHELLEXECUTEINFO()
                pi.cbSize = sizeof(pi)
                pi.lpFile = r"C:\Windows\System32\wbem\wmic.exe"
                pi.lpParameters = (
                    "process where processid=%d CALL setpriority %d"
                    % (pid, PRIORITY_FLAGS[priority])
                )
                pi.lpVerb = "runas"
                if not windll.shell32.ShellExecuteExW(byref(pi)):
                    eg.PrintError(self.text.priorityIssue)
        suffix = "%s.%s" % (
            self.text.eventSuffix,
            splitext(split(pathname)[1])[0]
        )
        if additionalSuffix != "":
            suffix = suffix + "." + additionalSuffix
        prefix = self.plugin.name.replace(' ', '')
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
            return returnValue
        elif triggerEvent:
            te = self.TriggerEvent(processInformation, suffix, prefix)
            te.start()
        else:
            CloseHandle(processInformation.hProcess)

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
        additionalSuffix="",
        disableParsingPathname=False,
        disableParsingArguments=False,
        disableParsingAdditionalSuffix=False,
        runAsAdmin = False,
    ):
        panel = eg.ConfigPanel()
        text = self.text
        filepathCtrl = panel.FileBrowseButton(
            pathname,
            fileMask="*.*",
            dialogTitle=text.browseExecutableDialogTitle
        )
        disableParsingPathnameBox = panel.CheckBox(
            bool(disableParsingPathname),
            text.disableParsing
        )
        argumentsCtrl = panel.TextCtrl(arguments)
        disableParsingArgumentsBox = panel.CheckBox(
            bool(disableParsingArguments),
            text.disableParsing
        )
        workingDirCtrl = panel.DirBrowseButton(
            workingDir or "",
            dialogTitle=text.browseWorkingDirDialogTitle
        )
        #workingDirCtrl.SetValue(workingDir)
        winStateChoice = panel.Choice(winState, text.WindowOptions)
        priorityChoice = panel.Choice(5 - priority, text.ProcessOptions)
        waitCheckBox = panel.CheckBox(
            bool(waitForCompletion),
            text.waitCheckbox
        )
        eventCheckBox = panel.CheckBox(
            bool(triggerEvent),
            text.eventCheckbox
        )
        additionalSuffixCtrl = panel.TextCtrl(additionalSuffix)
        disableParsingAdditionalSuffixBox = panel.CheckBox(
            bool(disableParsingAdditionalSuffix),
            text.disableParsing
        )
        wow64CheckBox = panel.CheckBox(
            bool(disableWOW64),
            text.wow64Checkbox
        )
        runAsAdminCheckBox = panel.CheckBox(
            bool(runAsAdmin),
            text.runAsAdminCheckbox
        )

        SText = panel.StaticText
        procPriorLabel = SText(text.ProcessOptionsDesc)
        lowerSizer = wx.GridBagSizer(0, 0)
        lowerSizer.AddMany([
            (SText(text.WindowOptionsDesc), (0, 0), (1, 1), wx.ALIGN_BOTTOM),
            (winStateChoice, (1, 0)),
            ((1, 1), (0, 1), (1, 1), wx.EXPAND),
            (procPriorLabel, (0, 2), (1, 1), wx.ALIGN_BOTTOM),
            (priorityChoice, (1, 2)),
            ((1, 1), (0, 3), (1, 1), wx.EXPAND),
        ])
        lowerSizer.AddGrowableCol(1)
        lowerSizer.AddGrowableCol(3)

        lowerSizer2 = wx.GridBagSizer(2, 0)
        stTxt = SText(text.additionalSuffix)
        lowerSizer2.AddMany([
            ((eventCheckBox), (0, 0), (1, 1), wx.ALIGN_BOTTOM),
            ((1, 1), (0, 1), (1, 1), wx.EXPAND),
            (stTxt, (0, 2), (1, 1), wx.ALIGN_BOTTOM),
            (additionalSuffixCtrl, (1, 2)),
            (disableParsingAdditionalSuffixBox, (2, 2)),
            ((1, 1), (0, 3), (1, 1), wx.EXPAND),
        ])
        lowerSizer2.AddGrowableCol(1)
        lowerSizer2.AddGrowableCol(3)

        def OnPathnameChanged(evt = None):
            path = filepathCtrl.GetValue().upper()
            if not isdir(path):
                enable = True
            else:
                enable = False
                wow64CheckBox.SetValue(False)
                runAsAdminCheckBox.SetValue(False)
            argumentsCtrl.Enable(enable)
            disableParsingArgumentsBox.Enable(enable)
            workingDirCtrl.Enable(enable)
            wow64CheckBox.Enable(enable)
            runAsAdminCheckBox.Enable(enable)
        filepathCtrl.changeCallback = OnPathnameChanged
        OnPathnameChanged()

        def OnEventCheckBox(evt = None):
            enable = eventCheckBox.GetValue()
            stTxt.Enable(enable)
            additionalSuffixCtrl.Enable(enable)
            disableParsingAdditionalSuffixBox.Enable(enable)
            if not enable:
                additionalSuffixCtrl.ChangeValue("")
            if evt:
                evt.Skip()
        eventCheckBox.Bind(wx.EVT_CHECKBOX, OnEventCheckBox)
        OnEventCheckBox()

        panel.sizer.AddMany([
            (SText(text.FilePath)),
            (filepathCtrl, 0, wx.EXPAND),
            (disableParsingPathnameBox),
            ((10, 10)),
            (SText(text.Parameters)),
            (argumentsCtrl, 0, wx.EXPAND),
            ((10, 2)),
            (disableParsingArgumentsBox),
            ((10, 10)),
            (SText(text.WorkingDir)),
            (workingDirCtrl, 0, wx.EXPAND),
            (lowerSizer, 0, wx.EXPAND),
            ((10, 15)),
            (waitCheckBox),
            ((10, 8)),
            (lowerSizer2, 0, wx.EXPAND),
            ((10, 8)),
            (wow64CheckBox),
            ((10, 8)),
            (runAsAdminCheckBox),
        ])

        while panel.Affirmed():
            panel.SetResult(
                filepathCtrl.GetValue(),
                argumentsCtrl.GetValue(),
                winStateChoice.GetValue(),
                waitCheckBox.GetValue(),
                5 - priorityChoice.GetValue(),
                workingDirCtrl.GetValue(),
                eventCheckBox.GetValue(),
                wow64CheckBox.GetValue(),
                additionalSuffixCtrl.GetValue(),
                disableParsingPathnameBox.GetValue(),
                disableParsingArgumentsBox.GetValue(),
                disableParsingAdditionalSuffixBox.GetValue(),
                runAsAdminCheckBox.GetValue()
            )

    def GetLabel(self, pathname='', *dummyArgs):
        path = expandvars(pathname).upper()
        if isdir(path):
            return self.text.labelFolder % basename(pathname)
        elif path.endswith(PATHEXT):
            return self.text.label % basename(pathname)
        else:
            return self.text.labelFile % basename(pathname)
