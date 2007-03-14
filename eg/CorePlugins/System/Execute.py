import eg
import wx

import win32api
import win32event
from win32con import *
from win32process import *
from os.path import basename, dirname, abspath



class Execute(eg.ActionClass):
    name = "Start Application"
    description = "Starts an executable file."
    iconFile = "Execute"
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
        commandLine = '"' + pathname + '" ' + arguments
        si = STARTUPINFO()
        si.dwFlags = STARTF_USESHOWWINDOW
        si.wShowWindow = (
            SW_SHOWNORMAL,
            SW_MINIMIZE|SW_HIDE,
            SW_SHOWMAXIMIZED,
            SW_HIDE 
        )[winState]
        priorityFlag = (
            IDLE_PRIORITY_CLASS,
            BELOW_NORMAL_PRIORITY_CLASS,
            NORMAL_PRIORITY_CLASS,
            ABOVE_NORMAL_PRIORITY_CLASS,
            REALTIME_PRIORITY_CLASS 
        )[priority]
        try:
            hProcess, _, _, _ = CreateProcess(
                None,         # AppName
                commandLine,  # Command line
                None,         # Process Security
                None,         # ThreadSecurity
                0,            # Inherit Handles?
                priorityFlag|CREATE_NEW_CONSOLE,
                None,         # New environment
                workingDir,   # Current directory
                si            # startup info
            )
        except:
            s = win32api.FormatMessage(0).strip()
            raise eg.Exception(s)
        else:
            if waitForCompletion:
                win32event.WaitForSingleObject(hProcess, win32event.INFINITE)
    
    
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
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        waitForCompletion = bool(waitForCompletion)
        fileText = wx.StaticText(dialog, -1, text.FilePath)
        filepathCtrl = eg.FileBrowseButton(
            dialog, 
            -1, 
            size=(320,-1),
            initialValue=pathname,
            labelText="",
            fileMask="*.*",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseExecutableDialogTitle
        )
    
        argumentsText = wx.StaticText(dialog, -1, text.Parameters)
        argumentsCtrl = wx.TextCtrl(dialog, -1, arguments)
        
        workingDirText = wx.StaticText(dialog, -1, text.WorkingDir)
        workingDirCtrl = eg.DirBrowseButton(
            dialog, 
            -1, 
            size=(320,-1),
            startDirectory=workingDir,
            labelText="",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseWorkingDirDialogTitle
        )
        
        winStateText = wx.StaticText(dialog, -1, text.WindowOptionsDesc)
        winStateChoice = wx.Choice(dialog, -1, choices=text.WindowOptions)
        winStateChoice.SetSelection(winState)
        
        prioritiesText = wx.StaticText(dialog, -1, text.ProcessOptionsDesc)
        priorityChoice = wx.Choice(dialog, -1, choices=text.ProcessOptions)
        priorityChoice.SetSelection(4 - priority)
    
        waitCheckBox = wx.CheckBox(dialog, -1, text.WaitCheckbox)
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

        Add = dialog.sizer.Add
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
        
    
        if dialog.AffirmedShowModal():
            return (
                filepathCtrl.GetValue(),
                argumentsCtrl.GetValue(),
                winStateChoice.GetSelection(),
                waitCheckBox.IsChecked(),
                4 - priorityChoice.GetSelection(),
                workingDirCtrl.GetValue()
            )        
