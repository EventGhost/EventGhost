OUTFILE_NAME = "USB-Remote-Driver.exe"

DDK_PATH = r"C:\WinDDK\6001.18002"

DEVICES = [
    (
        "WinUSB Test Device #1",
        "USB\\VID_0000&PID_0000",
        "{5607ED2F-AD3C-4CE8-9DE6-97CD4B0FFEF1}"
    ),
    (
        "WinUSB Test Device #2",
        "USB\\VID_0000&PID_0000",
        "{0A51286F-B9A6-471D-BDCA-8C2E68C3916B}"
    ),
    (
        "Logitech UltraX Media Remote (Keypad)", 
        "USB\\VID_046D&PID_C101&MI_00", 
        "{F73227F9-6CBD-45F9-83C4-A48B3F9F56A4}"
    ),
    (
        "Logitech UltraX Media Remote (Buttons)", 
        "USB\\VID_046D&PID_C101&MI_01", 
        "{4C6BCF9C-8F5B-4CEB-8CEA-4713E31B125F}"
    ),
    (
        "Conceptronic CLLRCMCE (Keypad)", 
        "USB\\VID_1784&PID_0004&MI_00", 
        "{8C3D8375-AF7B-4AF6-8CD7-463C8E935675}"
    ),
    (
        "Conceptronic CLLRCMCE (Buttons)", 
        "USB\\VID_1784&PID_0004&MI_01", 
        "{4228C963-EE0F-4B33-9E5E-D17FB07FB80F}"
    ),
    (
        "TechniSat USB IR Receiver", 
        "USB\\VID_147A&PID_E02D", 
        "{108E11FA-7EA0-4F13-AA64-1926E14A9C31}"
    ),
    (
        "USB PC Remote Controller", 
        "USB\\VID_06B4&PID_1C70", 
        "{72679574-1865-499d-B182-4B099D6D1391}"
    ),
]

HEADER = r"""
; This file is automatically created by the BuildDriver.py script. Don't edit
; this file directly. Edit BuildDriver.py instead.

[Version]
Signature="$Windows NT$"
Class=HIDClass
ClassGuid={745a17a0-74d3-11d0-b6fe-00a0c90f57da}
Provider=%ProviderName%
DriverVer=07/01/2009,1.0.0.9
DriverPackageDisplayName=%DisplayName%

; ========== Manufacturer/Models sections ===========

[Manufacturer]
%ProviderName%=Remotes,NTx86,NTamd64

"""

DEVICE_SECTION = r"""
; ========== $DESCR ==========

[Install$NR]
Include=winusb.inf
Needs=WINUSB.NT

[Install$NR.Services]
Include=winusb.inf
AddService=WinUSB,0x00000002,WinUSB_ServiceInstall

[Install$NR.Wdf]
KmdfService=WINUSB, WinUsb_Install

[Install$NR.CoInstallers]
AddReg=CoInstallers_AddReg
CopyFiles=CoInstallers_CopyFiles

[Install$NR.HW]
AddReg=Dev_AddReg$NR

[Dev_AddReg$NR]
HKR,,DeviceInterfaceGUIDs,0x10000,"$GUID"
HKR,,"SystemWakeEnabled",0x00010001,1

"""

FOOTER = r"""
; ========== Global sections ===========

[WinUSB_Install]
KmdfLibraryVersion=1.7

[WinUSB_ServiceInstall]
DisplayName=%WinUSB_SvcDesc%
ServiceType=1
StartType=3
ErrorControl=1
ServiceBinary=%12%\WinUSB.sys

[CoInstallers_AddReg]
HKR,,CoInstallers32,0x00010000,"WdfCoInstaller01007.dll,WdfCoInstaller","WinUSBCoInstaller.dll","WUDFUpdate_01007.dll"

[CoInstallers_CopyFiles]
WinUSBCoInstaller.dll
WdfCoInstaller01007.dll

[DestinationDirs]
CoInstallers_CopyFiles=11

; ================= Source Media Section =====================

[SourceDisksNames]
1=%DISK_NAME%,,,\x86

[SourceDisksNames.amd64]
1=%DISK_NAME%,,,\amd64

[SourceDisksFiles]
WinUSBCoInstaller.dll=1
WdfCoInstaller01007.dll=1
WUDFUpdate_01007.dll=1

; =================== Strings ===================

[Strings]
ProviderName="EventGhost"
WinUSB_SvcDesc="WinUSB Driver"
DISK_NAME="My Install Disk"
DisplayName="USB Remote Driver"
"""

CONFIG_7Z = r""";!@Install@!UTF-8!
Title="USB Remote Driver"
Progress="no"
ExecuteFile="DPInstSwitcher.exe"
;!@InstallEnd@!"""

MANIFEST = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
         <security>
           <requestedPrivileges>
             <requestedExecutionLevel level="requireAdministrator"/>
           </requestedPrivileges>
         </security>
       </trustInfo>
</assembly>
"""


import os
import string
import subprocess
import shutil
import ctypes

from os.path import join

outfile = open("driver.inf", "wt")
outfile.write(HEADER)

outfile.write("[Remotes.NTx86]\n")
for i, (descr, hardwareId, guid) in enumerate(DEVICES):
    nr = "%03i" % (i + 1)
    outfile.write("%Device" + nr + ".DeviceDesc%=Install" + nr + "," + hardwareId + "\n")
        
outfile.write("\n[Remotes.NTamd64]\n")
for i, (descr, hardwareId, guid) in enumerate(DEVICES):
    nr = "%03i" % (i + 1)
    outfile.write("%Device" + nr + ".DeviceDesc%=Install" + nr + "," + hardwareId + "\n")
        
template = string.Template(DEVICE_SECTION)
for i, (descr, hardwareId, guid) in enumerate(DEVICES):
    nr = "%03i" % (i + 1)
    outfile.write(template.substitute(NR=nr, GUID=guid, DESCR=descr))
outfile.write(FOOTER)

for i, (descr, hardwareId, guid) in enumerate(DEVICES):
    nr = "%03i" % (i + 1)
    outfile.write("Device" + nr + '.DeviceDesc="' + descr + '"\n')

outfile.close()

redistFolder = join(DDK_PATH, "redist")
tmpFolder = os.path.dirname(__file__)
for osType in ("x86", "amd64"):
    if not os.path.exists(join(tmpFolder, osType)):
        os.mkdir(join(tmpFolder, osType))
        
    src = join(redistFolder, "DIFx", "DPInst", "MultiLin", osType, "DPInst.exe")
    dst = join(tmpFolder, "DPInst_%s.exe" % osType)
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
        
    src = join(redistFolder, "winusb", osType, "WinUSBCoInstaller.dll")
    dst = join(tmpFolder, osType, "WinUSBCoInstaller.dll")
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
        
    src = join(redistFolder, "wdf", osType, "WdfCoInstaller01007.dll")
    dst = join(tmpFolder, osType, "WdfCoInstaller01007.dll")
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
        
    src = join(redistFolder, "wdf", osType, "WUDFUpdate_01007.dll")
    dst = join(tmpFolder, osType, "WUDFUpdate_01007.dll")
    if not os.path.exists(dst):
        shutil.copy2(src, dst)

subprocess.call(
    [
        os.environ["ProgramFiles"] + "\\7-zip\\7z.exe", 
        'a', 
        'archive.7z', 
        'driver.inf', 
        "-i!DPInstSwitcher.exe",
        "-i!DPInst_x86.exe",
        "-i!DPInst_amd64.exe",
        "-ir!x86\\*", 
        "-ir!amd64\\*",
    ]
)

# start creating the SFX by copying the SFX module
outfile = open(OUTFILE_NAME, "wb")
outfile.write(open("7zSD.sfx", "rb").read())
outfile.close()

# update the manifest of the copied SFX module, so we will run as administrator
kernel32 = ctypes.windll.kernel32
handle = kernel32.BeginUpdateResourceA(OUTFILE_NAME, 0)
if handle == 0:
    raise
if kernel32.UpdateResourceA(handle, 24, 1, 1033, MANIFEST, len(MANIFEST)):
    kernel32.EndUpdateResourceA(handle, 0)

# now append the config and data to the SFX
outfile = open(OUTFILE_NAME, "ab")
outfile.write(CONFIG_7Z)
outfile.write(open("archive.7z", "rb").read())
outfile.close()

os.remove("archive.7z")

print "Done!"
