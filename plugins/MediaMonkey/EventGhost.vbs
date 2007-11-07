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

Dim EventGhost:Set EventGhost = CreateObject("EventGhost")

Sub OnStartup
  Script.RegisterEvent SDB, "OnShutdown", "SDBShutdown" 
  Script.RegisterEvent SDB, "OnPlay", "SDBPlay" 
  Script.RegisterEvent SDB, "OnStop", "SDBStop" 
  Script.RegisterEvent SDB, "OnSeek", "SDBSeek" 
  Script.RegisterEvent SDB, "OnPause", "SDBPause" 
End Sub 

'Events Handling 
Sub SDBShutdown 
    On Error Resume Next 
    If EGrunning Then
       EventGhost.TriggerEvent("MM_finishing")
    End If
End Sub 
 
Sub SDBPlay
    On Error Resume Next 
    If EGrunning Then
       EventGhost.TriggerEvent("MM_playing")
    End If
End Sub
 
Sub SDBStop 
    On Error Resume Next 
    If EGrunning Then
       EventGhost.TriggerEvent("MM_stoped")
    End If
End Sub

Sub SDBSeek 
    On Error Resume Next 
    If EGrunning Then
       EventGhost.TriggerEvent("MM_seeked")
    End If
End Sub 
 
Sub SDBPause
    On Error Resume Next 
    If EGrunning Then
       If SDB.Player.isPaused Then
          EventGhost.TriggerEvent("MM_paused")
       else
          EventGhost.TriggerEvent("MM_unpaused")
       End If
   End If 
End Sub 
 
