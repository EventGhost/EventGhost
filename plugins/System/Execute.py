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


from os.path import basename, dirname, abspath

from eg.WinApi.Dynamic import (
    byref, sizeof, CreateProcess, WaitForSingleObject, FormatError,
    CloseHandle, create_unicode_buffer, 
    STARTUPINFO, PROCESS_INFORMATION, TCHAR, 
    CREATE_NEW_CONSOLE, STARTF_USESHOWWINDOW, INFINITE
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


class Execute(eg.ActionClass):
    name = "Start Application"
    description = "Starts an executable file."
    iconFile = "icons/Execute"
    class text:
        label = "Start Program: %s"
        FilePath = "Filepath to executable:"
        WorkingDir = "Working directory:"
        Parameters = "Command line options:"
        WindowOptionsDesc = "Window options:"
        WindowOptions = (
            "Normal", 
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
        WaitCheckbox = "Wait till application is terminated before proceed"
        browseExecutableDialogTitle = "Choose the executable"
        browseWorkingDirDialogTitle = "Choose the working directory"

    
    def __call__(
        self, 
        pathname='', 
        arguments='', 
        winState=0,
        waitForCompletion=False, 
        priority=2, 
        workingDir=""
    ):
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
        processInformation = PROCESS_INFORMATION()
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
        if res == 0:
            raise self.Exception(FormatError().decode('mbcs').strip())
        if waitForCompletion:
            WaitForSingleObject(processInformation.hProcess, INFINITE)
        CloseHandle(processInformation.hProcess)
        CloseHandle(processInformation.hThread)
        
    
    def GetLabel(
        self, 
        pathname='', 
        arguments=None, 
        winState=0,
        waitForCompletion=False, 
        priority=2,
        workingDir=""
    ):
        return self.text.label % basename(pathname)


    def Configure(
        self, 
        pathname='', 
        arguments='', 
        winState=0, 
        waitForCompletion=False, 
        priority=2,
        workingDir=""
    ):
        if not workingDir:
            workingDir = ""
        panel = eg.ConfigPanel(self)
        text = self.text
        waitForCompletion = bool(waitForCompletion)
        fileText = wx.StaticText(panel, -1, text.FilePath)
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            -1, 
            size=(320,-1),
            initialValue=pathname,
            labelText="",
            fileMask="*.*",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseExecutableDialogTitle
        )
    
        argumentsText = wx.StaticText(panel, -1, text.Parameters)
        argumentsCtrl = wx.TextCtrl(panel, -1, arguments)
        
        workingDirText = wx.StaticText(panel, -1, text.WorkingDir)
        workingDirCtrl = eg.DirBrowseButton(
            panel, 
            -1, 
            size=(320,-1),
            startDirectory=workingDir,
            labelText="",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseWorkingDirDialogTitle
        )
        workingDirCtrl.SetValue(workingDir)
        
        winStateText = wx.StaticText(panel, -1, text.WindowOptionsDesc)
        winStateChoice = wx.Choice(panel, -1, choices=text.WindowOptions)
        winStateChoice.SetSelection(winState)
        
        prioritiesText = wx.StaticText(panel, -1, text.ProcessOptionsDesc)
        priorityChoice = wx.Choice(panel, -1, choices=text.ProcessOptions)
        priorityChoice.SetSelection(4 - priority)
    
        waitCheckBox = wx.CheckBox(panel, -1, text.WaitCheckbox)
        waitCheckBox.SetValue(waitForCompletion)
        
        lowerSizer = wx.GridBagSizer(0, 0)
        lowerSizer.AddGrowableCol(1)
        lowerSizer.AddGrowableCol(3)
        Add = lowerSizer.Add
        Add(winStateText, (0, 0), flag=wx.ALIGN_BOTTOM)
        Add(winStateChoice, (1, 0))
        Add((1, 1), (0, 1), flag=wx.EXPAND)
        Add(prioritiesText, (0, 2), flag=wx.ALIGN_BOTTOM)
        Add(priorityChoice, (1, 2))
        Add((1, 1), (0, 3), flag=wx.EXPAND)

        Add = panel.sizer.Add
        Add(fileText)
        Add(filepathCtrl, 0, wx.EXPAND)
        Add((10,10))
        Add(argumentsText)
        Add(argumentsCtrl, 0, wx.EXPAND)
        Add((10,10))
        Add(workingDirText)
        Add(workingDirCtrl, 0, wx.EXPAND)
        Add(lowerSizer, 0, wx.EXPAND)
        Add((10,15))
        Add(waitCheckBox)
        
        while panel.Affirmed():
            panel.SetResult(
                filepathCtrl.GetValue(),
                argumentsCtrl.GetValue(),
                winStateChoice.GetSelection(),
                waitCheckBox.IsChecked(),
                4 - priorityChoice.GetSelection(),
                workingDirCtrl.GetValue()
            )        
