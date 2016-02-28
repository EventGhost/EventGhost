[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: Deutsch; MessagesFile: "compiler:Languages\German.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"

[Setup]
ShowLanguageDialog=auto
AppName=EventGhost WinUSB Add-on (x64)
AppID=EventGhost
AppPublisher=EventGhost Project
AppCopyright=? 2005-2009 EventGhost Project
AppVersion=1.0.0.9
AppVerName=EventGhost WinUSB Add-on 1.0.0.9 (x64)
VersionInfoDescription=EventGhost Installer
DefaultDirName={pf}\EventGhost
DefaultGroupName=EventGhost
Compression=lzma/ultra
SolidCompression=yes
InternalCompressLevel=ultra
OutputBaseFilename=EventGhost WinUSB Add-on (x64)
DisableReadyPage=yes
UsePreviousAppDir=yes
CreateUninstallRegKey=no
UpdateUninstallLogAppName=no
OutputDir=.

[Files]
Source: "x64\*.*"; DestDir: "{app}\drivers\WinUSB\x64"; Flags: ignoreversion recursesubdirs

[InstallDelete]
Type: filesandordirs; Name: "{app}\drivers\WinUSB"

