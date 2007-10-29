'==========================================================================
'
' MediaMonkey Script
'
' NAME: EventGhost
'
' DESCRIPTION:
'(To be add ...)
'
' AUTHOR: Pako
' DATE  : 29.10.2007
'
' INSTALL:
' - Put script to MediaMonkey's "Scripts\Auto" folder and (re)start MediaMonkey
'
'========================================================================== 
Option Explicit
'-------------------------------------------------------
Function EGrunning()
EGrunning=False
Dim strComputer : strComputer = "."
Dim objWMIService : Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate}!\\" _
    & strComputer & "\root\cimv2")
Dim colProcessList : Set colProcessList = objWMIService.ExecQuery( _
    "Select * from Win32_Process" & _
    " WHERE Name = 'EventGhost.exe'")
Dim objProcess
For Each objProcess in colProcessList
EGrunning=True
Next
End Function
'-------------------------------------------------------

'Global variables:
Dim oEG
Dim path
Dim ws

Sub OnStartup
  Set oEG = CreateObject("WScript.Shell") 
  Script.RegisterEvent SDB, "OnPlay", "SDBPlay" 
  Script.RegisterEvent SDB, "OnStop", "SDBStop" 
  Script.RegisterEvent SDB, "OnSeek", "SDBSeek" 
  Script.RegisterEvent SDB, "OnPause", "SDBPause" 

  Dim Sheet : Sheet = SDB.UI.AddOptionSheet ("EventGhost", Script.ScriptPath, "InitSheet", "SaveSheet", -1)  
  Dim Regs : Set Regs = SDB.Registry
  If Regs.OpenKey( "EG_Path", True) Then
    If Regs.ValueExists( "Edit value") And Right(Regs.StringValue( "Edit value"),14)="EventGhost.exe" Then
      path = Regs.StringValue( "Edit value")
    Else 
      Set ws=CreateObject("WScript.Shell")
      path=ws.RegRead ("HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\EventGhost_is1\InstallLocation")&"EventGhost.exe"
      Set ws=Nothing
      Regs.StringValue("Edit value") = path      
    End If
    Regs.CloseKey
  End If
End Sub 

Sub InitSheet( Sheet)
  ' Create a simple sheet with an edit line and a button
  
  'Create Label
  Dim pathLabel : Set pathLabel = SDB.UI.NewLabel( Sheet)
  pathLabel.Common.SetRect 20, 20, 440, 20
  pathLabel.Caption = "Path to EventGhost.exe (If you would like to select a different folder, click Browse):"
  
  ' Create an edit line
  Dim edtProgramPath :  Set edtProgramPath = SDB.UI.NewEdit( Sheet)
  edtProgramPath.Common.SetRect 20, 40, 350, 20
  edtProgramPath.Common.Hint = "If you would like to select a different folder, click Browse"         ' Just for fun - we can even show tooltips
  Dim Regs : Set Regs = SDB.Registry
  If Regs.OpenKey( "EG_Path", True) Then
    If Regs.ValueExists( "Edit value") Then
      edtProgramPath.Text = Regs.StringValue( "Edit value")
    End If
    Regs.CloseKey
  End If
  edtProgramPath.Common.ControlName = "Edit1"
 
  ' Create a button
  Dim btnProgramPath : Set btnProgramPath = SDB.UI.NewButton( Sheet)
  btnProgramPath.Caption = "Browse"
  btnProgramPath.Common.SetRect 380, 38, 80, 25
  btnProgramPath.UseScript = Script.ScriptPath
  btnProgramPath.OnClickFunc = "btnProgramPath_OnClick"
 
End Sub
 
Sub SaveSheet( Sheet)
   ' Save entered value to registry in order to be able to shown it next time
Dim Regs :  Set Regs = SDB.Registry
Dim edtProgramPath : Set edtProgramPath = Sheet.Common.ChildControl( "Edit1")
  If Regs.OpenKey( "EG_Path", True) Then
    Regs.StringValue("Edit value") = edtProgramPath.Text
    Regs.CloseKey
  End If
End Sub

Sub btnProgramPath_OnClick(btnProgramPath)

    Dim Sheet : Set Sheet = btnProgramPath.Common.Parent

    Dim Dlg : Set Dlg = SDB.CommonDialog
    Set ws=CreateObject("WScript.Shell")
    Dlg.InitDir=ws.RegRead ("HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\EventGhost_is1\InstallLocation")&"EventGhost.exe"
    Set ws=Nothing
    Dlg.DefaultExt = "exe"
    Dlg.Filter = "Program Files (*.exe, *.com)|*.exe;*.com|Command Files (*.cmd; *.bat)|*.cmd; *.bat|All Files (*.*)|*.*"
    Dlg.Flags = cdlOFNHideReadOnly + cdlOFNExtensionDifferent + cdlOFNPathMustExist + cdlOFNFileMustExist
    Dlg.Title = "Select the path for EventGhost.exe"
    Dlg.ShowOpen
    
    If Not Dlg.Ok Then
        Exit Sub
    End If
    
    Sheet.Common.ChildControl("Edit1").Text = Dlg.FileName
    SDB.MessageBox "Path changes only take effect after restarting the application !", mtInformation, Array(mbOk) 
End Sub

'Events Handling 
Sub SDBShutdown 
    On Error Resume Next 
    If EGrunning Then
        oEG.Run(path&" -e MM_finishing")
    End If
End Sub 
 
Sub SDBPlay
    On Error Resume Next 
    If EGrunning Then
       oEG.Run(path&" -e MM_playing")
    End If
End Sub
 
Sub SDBStop 
    On Error Resume Next 
    If EGrunning Then
        oEG.Run(path&" -e MM_stoped")
    End If
End Sub

Sub SDBSeek 
    On Error Resume Next 
    If EGrunning Then
        oEG.Run(path&" -e MM_seeked")
    End If
End Sub 
 
Sub SDBPause
    On Error Resume Next 
    If EGrunning Then
       If SDB.Player.isPaused Then
        oEG.Run(path&" -e MM_paused")
       else
        oEG.Run(path&" -e MM_unpaused")
       End If
   End If 
End Sub 
 
