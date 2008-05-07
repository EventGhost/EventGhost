[Setup]
ShowLanguageDialog=auto
AppId=EventGhost
AppName=EventGhost GDI+ Update
AppVerName=EventGhost GDI+ Update for Windows 2000
DefaultDirName={pf}\EventGhost
DefaultGroupName=EventGhost
Compression=lzma/max
SolidCompression=yes
InternalCompressLevel=max
DisableReadyPage=yes
CreateUninstallRegKey=no
UpdateUninstallLogAppName=no

[Files]
Source: "gdiplus.dll"; DestDir: "{app}"; Flags: ignoreversion
