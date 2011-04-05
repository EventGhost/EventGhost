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
    name = "System",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    description = (
        "Controls different aspects of your system, like sound card, "
        "graphics card, power management, et cetera."
    ),
    kind = "core",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/"
        "AAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH1QsEFTMTHK3EDwAAAUhJREFUOMul"
        "k0FLAlEQx39vd/VLeJSV7hH0ASLqLBEU3u0UQUGHUBJvfYAkukWiKV2DvkHUNeiyxCai"
        "bAqlVHbYnQ6ur8Qktbm8mcf7/+bNezPwT1MAuXy2CiSn1BYyB4dbVhgkl5dWsO3ERMp2"
        "u0XpopgGNADbTrC6eTQR4Lq0r30NiEajACwuzCFjahXg5vZhaF8DfN8HwLBMkP5hpcIV"
        "QVB43ssIWAOCIOgDDBOU/MipAHh88njt9gAQkVHAwEzLDD2h+dzh/eOT7lsPUFgR62+A"
        "YRp47Q7NVgdEhdAIICjF+BIG1HunOST6fkCl419vMPgFz61P1U0aUKvVuDrfm0jUaDRG"
        "AIXqZTk9ZStnAFQun50H7na2d/F9H9d1icViQ3UCOI6jeyUej3NyegyQUrl8VtbXNmaa"
        "xHKliAWkypXi2YzTnPoC/MF4O/QjGPgAAAAASUVORK5CYII="
    ),
)

import wx
import time
import sys
import os
import thread
import _winreg
import ctypes
import socket
import struct
import Image
from threading import Timer

from eg.WinApi.Dynamic import (
    # functions:
    GetDriveType, SendMessage, SetThreadExecutionState, GetCurrentProcess,
    InitiateSystemShutdown, CreateFile, CloseHandle, DeviceIoControl,
    SystemParametersInfo, ExitWindowsEx, OpenProcessToken, GetForegroundWindow,
    LookupPrivilegeValue, AdjustTokenPrivileges, GetClipboardOwner,
    create_unicode_buffer, byref, sizeof,

    # types:
    DWORD, HANDLE, LUID, TOKEN_PRIVILEGES,

    # constants:
    GENERIC_READ, FILE_SHARE_READ, OPEN_EXISTING, WM_SYSCOMMAND, SC_SCREENSAVE,
    SC_MONITORPOWER, TOKEN_ADJUST_PRIVILEGES, TOKEN_QUERY, SE_SHUTDOWN_NAME,
    SE_PRIVILEGE_ENABLED, EWX_LOGOFF, SPI_SETDESKWALLPAPER, SPIF_SENDCHANGE,
    SPIF_UPDATEINIFILE, INVALID_HANDLE_VALUE
)

import eg.WinApi.SoundMixer as SoundMixer
from eg.WinApi import GetWindowThreadProcessId
from eg.WinApi.Utils import BringHwndToFront
from eg.WinApi.Utils import GetMonitorDimensions
from eg.cFunctions import StartHooks, StopHooks
from eg.cFunctions import ResetIdleTimer as HookResetIdleTimer
from eg.cFunctions import SetIdleTime as HookSetIdleTime

from ChangeDisplaySettings import ChangeDisplaySettings
from Execute import Execute
from DeviceChangeNotifier import DeviceChangeNotifier
from PowerBroadcastNotifier import PowerBroadcastNotifier
import Registry



class Text:
    class MonitorGroup:
        name = "Display"
        description = \
            "These actions control the powerstate of the computers "\
            "display."

    class SoundGroup:
        name = "Sound Card"
        description = \
            "These actions control the souncard of your computer."

    class PowerGroup:
        name = "Power Management"
        description = (
            "These actions suspends, hibernates, reboots or shutsdown "
            "the computer. Can also lock the workstation and logoff the "
            "current user."
        )
    forced   = "Forced: %s"
    forcedCB = "Force close of all programs"

    RegistryGroup = Registry.Text



def getDeviceHandle(drive):
    '''Returns a properly formatted device handle for DeviceIOControl call.'''
    return "\\\\.\\%s:" % drive[:1].upper()


EVENT_LIST = (
    ("Idle", None),
    ("UnIdle", None),
    ("DriveMounted", None),
    ("DriveRemoved", None),
    ("DeviceAttached", None),
    ("DeviceRemoved", None),
)


class System(eg.PluginBase):
    text = Text
    hookStarted = False

    def __init__(self):
        text = self.text

        self.AddEvents(*EVENT_LIST)

        self.AddAction(Execute)
        self.AddAction(OpenDriveTray)
        self.AddAction(SetClipboard)
        self.AddAction(WakeOnLan)
        self.AddAction(SetIdleTime)
        self.AddAction(ResetIdleTimer)

        group = self.AddGroup(
            text.SoundGroup.name,
            text.SoundGroup.description,
            "icons/SoundCard"
        )
        group.AddAction(MuteOn)
        group.AddAction(MuteOff)
        group.AddAction(ToggleMute)
        group.AddAction(GetMute)
        group.AddAction(SetMasterVolume)
        group.AddAction(ChangeMasterVolumeBy)
        group.AddAction(PlaySound)

        group = self.AddGroup(
            text.MonitorGroup.name,
            text.MonitorGroup.description,
            "icons/Display"
        )
        group.AddAction(StartScreenSaver)
        group.AddAction(MonitorStandby)
        group.AddAction(MonitorPowerOff)
        group.AddAction(MonitorPowerOn)
        group.AddAction(ShowPicture)
        group.AddAction(SetWallpaper)
        group.AddAction(ChangeDisplaySettings)
        group.AddAction(SetDisplayPreset)

        group = self.AddGroup(
            text.PowerGroup.name,
            text.PowerGroup.description,
            "icons/Shutdown"
        )
        group.AddAction(PowerDown)
        group.AddAction(Reboot)
        group.AddAction(Standby)
        group.AddAction(Hibernate)
        group.AddAction(LogOff)
        group.AddAction(LockWorkstation)
        group.AddAction(SetSystemIdleTimer)

        group = self.AddGroup(
            text.RegistryGroup.name,
            text.RegistryGroup.description,
            "icons/Registry"
        )
        group.AddAction(Registry.RegistryQuery)
        group.AddAction(Registry.RegistryChange)


    def __start__(self):
        eg.Bind("ClipboardChange", self.OnClipboardChange)
        #Assign all available cd drives to self.drives. If CdRom.drive
        #is not already set, the first drive returned becomes the default.
        cdDrives = []
        letters = [l + ':' for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        for drive in letters:
            if GetDriveType(drive)==5:
                cdDrives.append(drive)
        self.cdDrives = cdDrives

        # start the drive changed notifications
        self.deviceChangeNotifier = DeviceChangeNotifier(self)

        # start the power broadcast notifications
        self.powerBroadcastNotifier = PowerBroadcastNotifier(self)

        # start the session change notifications (only on Win XP and above)
        majorVersion, minorVersion = sys.getwindowsversion()[0:2]
        if majorVersion > 5 or (majorVersion == 5 and minorVersion > 0):
            from SessionChangeNotifier import SessionChangeNotifier
            self.sessionChangeNotifier = SessionChangeNotifier(self)

        self.StartHookCode()
        eg.Bind("System.SessionLock", self.StopHookCode)
        eg.Bind("System.SessionUnlock", self.StartHookCode)

        # Use VistaVolume.dll from stridger for sound volume control on Vista
        if majorVersion > 5:
            pluginDir = os.path.abspath(os.path.split(__file__)[0])
            dllPath = os.path.join(pluginDir, "VistaVolume.dll")
            vistaVolumeDll = ctypes.cdll.LoadLibrary(dllPath)
            vistaVolumeDll.SetMasterVolume.argtypes = [ctypes.c_float]
            vistaVolumeDll.GetMasterVolume.restype = ctypes.c_float

            def MuteOn2(self, deviceId=0):
                vistaVolumeDll.SetMute(1)
                return True

            def MuteOff2(self, deviceId=0):
                vistaVolumeDll.SetMute(0)
                return False

            def ToggleMute2(self, deviceId=0):
                newValue = not vistaVolumeDll.GetMute()
                vistaVolumeDll.SetMute(newValue)
                return newValue

            def GetMute2(self, deviceId=0):
                return vistaVolumeDll.GetMute()
               
            def SetMasterVolume2(self, value, deviceId=0):
                vistaVolumeDll.SetMasterVolume(value / 100.0)
                return vistaVolumeDll.GetMasterVolume() * 100.0

            def ChangeMasterVolumeBy2(self, value, deviceId=0):
                old = vistaVolumeDll.GetMasterVolume()
                vistaVolumeDll.SetMasterVolume((old * 100.0 + value) / 100.0)
                return vistaVolumeDll.GetMasterVolume() * 100.0

            self.info.actions["MuteOn"].__call__ = MuteOn2
            self.info.actions["MuteOff"].__call__ = MuteOff2
            self.info.actions["ToggleMute"].__call__ = ToggleMute2
            self.info.actions["GetMute"].__call__ = GetMute2
            self.info.actions["SetMasterVolume"].__call__ = SetMasterVolume2
            self.info.actions["ChangeMasterVolumeBy"].__call__ = ChangeMasterVolumeBy2


    @eg.LogItWithReturn
    def __stop__(self):
        eg.Unbind("System.SessionLock", self.StopHookCode)
        eg.Unbind("System.SessionUnlock", self.StartHookCode)
        eg.Unbind("ClipboardChange", self.OnClipboardChange)
        self.deviceChangeNotifier.Close()
        self.powerBroadcastNotifier.Close()
        self.StopHookCode()


    def OnComputerSuspend(self, dummySuspendType):
        self.StopHookCode()


    def OnComputerResume(self, dummySuspendType):
        self.StartHookCode()


    def IdleCallback(self):
        self.TriggerEvent("Idle")


    def UnIdleCallback(self):
        self.TriggerEvent("UnIdle")


    def StartHookCode(self, event=None):
        if self.hookStarted:
            return
        try:
            StartHooks(
                self.IdleCallback,
                self.UnIdleCallback,
            )
        except:
            eg.PrintTraceback()
        self.hookStarted = True


    def StopHookCode(self, event=None):
        if not self.hookStarted:
            return
        StopHooks()
        self.hookStarted = False


    def OnClipboardChange(self, value):
        ownerHwnd = GetClipboardOwner()
        if GetWindowThreadProcessId(ownerHwnd)[1] != eg.processId:
            self.TriggerEvent("ClipboardChanged")



class SetIdleTime(eg.ActionBase):
    class text:
        name = "Set Idle Time"
        label1 = "Wait"
        label2 = "seconds before triggering idle event."


    def __call__(self, idleTime):
        HookSetIdleTime(int(idleTime * 1000))


    def Configure(self, waitTime=60.0):
        panel = eg.ConfigPanel()
        waitTimeCtrl = panel.SpinNumCtrl(waitTime, integerWidth=5)
        panel.AddLine(self.text.label1, waitTimeCtrl, self.text.label2)
        while panel.Affirmed():
            panel.SetResult(waitTimeCtrl.GetValue())



class ResetIdleTimer(eg.ActionBase):
    name = "Reset Idle Timer"

    def __call__(self):
        HookResetIdleTimer()



class OpenDriveTray(eg.ActionBase):
    name = "Open/close drive tray"
    description = "Controls the tray of a CD/DVD-ROM drive."
    iconFile = "icons/cdrom"
    class text:
        labels = [
            "Toggle drive tray: %s",
            "Eject drive tray: %s",
            "Close drive tray: %s"
        ]
        options = [
            "Toggle between open and close drive tray",
            "Only open drive tray",
            "Only close drive tray"
        ]
        optionsLabel = "Choose action"
        driveLabel = "Drive:"


    def __call__(self, drive=None, action=0):
        drive = drive or self.plugin.cdDrives[0]

        def SendCodeToDrive(code):
            device = getDeviceHandle(drive)
            try:
                hDevice = CreateFile(
                    device,
                    GENERIC_READ,
                    FILE_SHARE_READ,
                    None,
                    OPEN_EXISTING,
                    0,
                    0
                )
            except Exception, exc:
                self.PrintError(
                    "Couldn't find drive %s:" % drive[:1].upper()
                )
                return
            bytesReturned = DWORD()
            DeviceIoControl(
                hDevice, # handle to the device
                code,    # control code for the operation
                None,    # pointer to the input buffer
                0,       # size of the input buffer
                None,    # pointer to the output buffer
                0,       # size of the output buffer
                byref(bytesReturned),
                None     # pointer to an OVERLAPPED structure
            )
            CloseHandle(hDevice)

        def ToggleMedia():
            start = time.clock()
            SendCodeToDrive(2967560)
            end = time.clock()
            if end - start < 0.1:
                SendCodeToDrive(2967564)

        if action is 0:
            thread.start_new_thread(ToggleMedia, ())
        elif action is 1:
            thread.start_new_thread(SendCodeToDrive, (2967560, ))
        elif action is 2:
            thread.start_new_thread(SendCodeToDrive, (2967564, ))


    def GetLabel(self, drive, action):
        return self.text.labels[action] % drive


    def Configure(self, drive=None, action=0):
        panel = eg.ConfigPanel()
        text = self.text
        radiobox = wx.RadioBox(
            panel,
            -1,
            text.optionsLabel,
            choices=text.options,
            majorDimension=1
        )
        radiobox.SetSelection(action)
        #Assign all available cd drives to self.drives. If CdRom.drive
        #is not already set the first drive returned becomes the default.
        cdDrives = []
        letters = [letter + ':' for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        for driveLetter in letters:
            if GetDriveType(driveLetter) == 5:
                cdDrives.append(driveLetter)

        choice = wx.Choice(panel, -1, choices=cdDrives)
        if drive is None:
            drive = ''
        if not choice.SetStringSelection(drive):
            choice.SetSelection(0)
        mySizer = eg.HBoxSizer(
            (panel.StaticText(text.driveLabel), 0, wx.ALIGN_CENTER_VERTICAL),
            ((5,5)),
            (choice),
        )
        panel.sizer.AddMany(
            (
                (radiobox, 0, wx.EXPAND),
                ((5,5)),
                (mySizer, 0, wx.EXPAND|wx.ALL, 5),
            )
        )
        while panel.Affirmed():
            panel.SetResult(
                str(choice.GetStringSelection()),
                radiobox.GetSelection()
            )



class PlaySound(eg.ActionWithStringParameter):
    name = "Play Sound"
    iconFile = "icons/SoundCard"
    class text:
        text1 = "Path to soundfile:"
        text2 = "Wait for completion"
        fileMask = "Wav-Files (*.WAV)|*.wav|All-Files (*.*)|*.*"


    def __call__(self, wavfile, flags=wx.SOUND_ASYNC):
        self.sound = wx.Sound(wavfile)
        self.sound.Play(flags)


    def Configure(self, wavfile='', flags=wx.SOUND_ASYNC):
        panel = eg.ConfigPanel()
        text = self.text
        filepathCtrl = panel.FileBrowseButton(wavfile, fileMask=text.fileMask)
        waitCheckbox = panel.CheckBox(flags == wx.SOUND_SYNC, text.text2)

        panel.sizer.Add(panel.StaticText(text.text1), 0, wx.EXPAND)
        panel.sizer.Add(filepathCtrl, 0, wx.EXPAND)
        panel.sizer.Add(waitCheckbox, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)

        while panel.Affirmed():
            if waitCheckbox.IsChecked():
                flags = wx.SOUND_SYNC
            else:
                flags = wx.SOUND_ASYNC
            panel.SetResult(filepathCtrl.GetValue(), flags)



class SetClipboard(eg.ActionWithStringParameter):
    name = "Copy string to clipboard"
    description = "Copies the string parameter to the system clipboard."
    iconFile = "icons/SetClipboard"
    class text:
        error = "Can't open clipboard"


    def __call__(self, text):
        self.clipboardString = eg.ParseString(text)
        if wx.TheClipboard.Open():
            tdata = wx.TextDataObject(self.clipboardString)
            wx.TheClipboard.SetData(tdata)
            wx.TheClipboard.Close()
            wx.TheClipboard.Flush()
        else:
            self.PrintError(self.text.error)



class StartScreenSaver(eg.ActionBase):
    name = "Start windows screen saver"
    description = "Starts the currently in windows selected screensaver."
    iconFile = "icons/StartScreenSaver"

    def __call__(self):
        SendMessage(GetForegroundWindow(), WM_SYSCOMMAND, SC_SCREENSAVE, 0)



class MonitorStandby(eg.ActionBase):
    name = "Set monitor into stand-by mode"
    description = "Sets the state of the display to low power mode."
    iconFile = "icons/Display"

    def __call__(self):
        SendMessage(GetForegroundWindow(), WM_SYSCOMMAND, SC_MONITORPOWER, 1)



class MonitorPowerOff(eg.ActionBase):
    name = "Set monitor into power-off mode"
    description = \
        "Sets the state of the display to power-off mode. This will "\
        "be the most power-saving mode the display supports."
    iconFile = "icons/Display"

    def __call__(self):
        SendMessage(GetForegroundWindow(), WM_SYSCOMMAND, SC_MONITORPOWER, 2)



class MonitorPowerOn(eg.ActionBase):
    name = "Re-enable monitor"
    description = \
        "Turns on a display, when it is in low power or power-off "\
        "mode. Will also stop a running screensaver."
    iconFile = "icons/Display"

    def __call__(self):
        SendMessage(GetForegroundWindow(), WM_SYSCOMMAND, SC_MONITORPOWER, -1)



class __ComputerPowerAction(eg.ActionBase):
    iconFile = "icons/Shutdown"

    def GetLabel(self, bForceClose=False):
        s = eg.ActionBase.GetLabel(self)
        if bForceClose:
            return self.plugin.text.forced % s
        else:
            return s


    def Configure(self, bForceClose=False):
        panel = eg.ConfigPanel()
        checkbox = panel.CheckBox(bForceClose, self.plugin.text.forcedCB)
        panel.sizer.Add(checkbox, 0, wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(checkbox.GetValue())



def AdjustPrivileges():
    """
    Adjust privileges to allow power down and reboot.
    """
    hToken = HANDLE()
    luid = LUID()
    OpenProcessToken(
        GetCurrentProcess(),
        TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY,
        byref(hToken)
    )
    LookupPrivilegeValue(None, SE_SHUTDOWN_NAME, byref(luid))
    newState = TOKEN_PRIVILEGES()
    newState.PrivilegeCount = 1
    newState.Privileges[0].Luid = luid
    newState.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED
    AdjustTokenPrivileges(
        hToken,           # TokenHandle
        0,                # DisableAllPrivileges
        newState,         # NewState
        sizeof(newState), # BufferLength
        None,             # PreviousState
        None              # ReturnLength
    )



class PowerDown(__ComputerPowerAction):
    name = "Turn Off Computer"
    description = \
        "Shuts down the system and turns off the power. The system "\
        "must support the power-off feature."
    iconFile = "icons/PowerDown"

    def __call__(self, bForceClose=False):
        AdjustPrivileges()
        InitiateSystemShutdown(None, None, 0, bForceClose, False)



class Reboot(__ComputerPowerAction):
    name = "Reboot Computer"
    description = "Shuts down the system and then restarts the system."
    iconFile = "icons/Reboot"

    def __call__(self, bForceClose=False):
        AdjustPrivileges()
        InitiateSystemShutdown(None, None, 0, bForceClose, True)



class Standby(__ComputerPowerAction):
    name = "Stand By"
    description = \
        "This function suspends the system by shutting power down "\
        "and enters a suspend (sleep) state."
    iconFile = "icons/Standby"

    def __call__(self, bForceClose=False):
        thread.start_new_thread(
            ctypes.windll.Powrprof.SetSuspendState,
            (False, bForceClose, False)
        )



class Hibernate(__ComputerPowerAction):
    name = "Hibernate Computer"
    description = \
        "This function suspends the system by shutting power down "\
        "and enters a hibernation (S4) state."
    iconFile = "icons/Hibernate"

    def __call__(self, bForceClose=False):
        thread.start_new_thread(
            ctypes.windll.Powrprof.SetSuspendState,
            (True, bForceClose, False)
        )



class LogOff(eg.ActionBase):
    name = "Log-off current user"
    description = "Shuts down all processes running in the current "\
        "logon session. Then it logs the user off."
    iconFile = "icons/LogOff"

    def __call__(self):
        #SHTDN_REASON_MAJOR_OPERATINGSYSTEM = 0x00020000
        #SHTDN_REASON_MINOR_UPGRADE         = 0x00000003
        #SHTDN_REASON_FLAG_PLANNED          = 0x80000000
        #                                     ----------
        #                                     0x80020003
        ExitWindowsEx(EWX_LOGOFF, 0x80020003)



class LockWorkstation(eg.ActionBase):
    name = "Lock Workstation"
    description = \
        "This function submits a request to lock the workstation's "\
        "display. Locking a workstation protects it from "\
        "unauthorized use. This function has the same result as "\
        "pressing Ctrl+Alt+Del and clicking Lock Workstation."
    iconFile = "icons/LockWorkstation"

    def __call__(self):
        ctypes.windll.user32.LockWorkStation()



class SetWallpaper(eg.ActionWithStringParameter):
    name = "Change Wallpaper"
    iconFile = "icons/SetWallpaper"
    class text:
        text1 = "Path to image file:"
        text2 = "Alignment:"
        choices = (
            "Centered",
            "Tiled",
            "Stretched"
        )
        fileMask = "All Image Files|*.jpg;*.bmp;*.gif;*.png|All Files (*.*)|*.*"


    def __call__(self, imageFileName='', style=1):
        if imageFileName:
            image = wx.Image(imageFileName)
            imageFileName = eg.folderPath.RoamingAppData + '\\Microsoft\\Wallpaper1.bmp'
            image.SaveFile(imageFileName, wx.BITMAP_TYPE_BMP)
        tile, wstyle = (("0", "0"), ("1", "0"), ("0", "2"))[style]
        hKey = _winreg.CreateKey(
            _winreg.HKEY_CURRENT_USER,
            "Control Panel\\Desktop"
        )
        _winreg.SetValueEx(
            hKey,
            "TileWallpaper",
            0,
            _winreg.REG_SZ,
            tile
        )
        _winreg.SetValueEx(
            hKey,
            "WallpaperStyle",
            0,
            _winreg.REG_SZ,
            wstyle
        )
        _winreg.CloseKey(hKey)
        res = SystemParametersInfo(
            SPI_SETDESKWALLPAPER,
            0,
            create_unicode_buffer(imageFileName),
            SPIF_SENDCHANGE|SPIF_UPDATEINIFILE
        )
        if res == 0:
            self.PrintError(ctypes.FormatError())



    def Configure(self, imageFileName='', style=1):
        panel = eg.ConfigPanel()
        text = self.text
        filepathCtrl = eg.FileBrowseButton(
            panel,
            size = (340, -1),
            initialValue = imageFileName,
            labelText = "",
            fileMask = text.fileMask,
            buttonText =  eg.text.General.browse,
        )
        choice = wx.Choice(panel, -1, choices=text.choices)
        choice.SetSelection(style)
        sizer = panel.sizer
        sizer.Add(panel.StaticText(text.text1), 0, wx.EXPAND)
        sizer.Add(filepathCtrl, 0, wx.EXPAND)
        sizer.Add(panel.StaticText(text.text2), 0, wx.EXPAND|wx.TOP, 10)
        sizer.Add(choice, 0, wx.BOTTOM, 10)

        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue(), choice.GetSelection())



#-----------------------------------------------------------------------------
# Soundcard actions
#-----------------------------------------------------------------------------

class MuteOn(eg.ActionBase):
    name = "Turn Mute On"
    iconFile = "icons/SoundCard"

    def __call__(self, deviceId=0):
        SoundMixer.SetMute(True, deviceId)
        return True


    def GetLabel(self, *args):
        return self.text.name


    def Configure(self, deviceId=0):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.Choice(deviceId, choices=SoundMixer.GetMixerDevices())
        panel.AddLine("Device:", deviceCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue())



class MuteOff(eg.ActionBase):
    name = "Turn Mute Off"
    iconFile = "icons/SoundCard"

    def __call__(self, deviceId=0):
        SoundMixer.SetMute(False, deviceId)
        return False


    def GetLabel(self, *args):
        return self.text.name


    def Configure(self, deviceId=0):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.Choice(deviceId, choices=SoundMixer.GetMixerDevices())
        panel.AddLine("Device:", deviceCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue())



class ToggleMute(eg.ActionBase):
    name = "Toggle Mute"
    iconFile = "icons/SoundCard"

    def __call__(self, deviceId=0):
        return SoundMixer.ToggleMute(deviceId)


    def GetLabel(self, *args):
        return self.text.name


    def Configure(self, deviceId=0):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.Choice(deviceId, choices=SoundMixer.GetMixerDevices())
        panel.AddLine("Device:", deviceCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue())



class GetMute(eg.ActionBase):
    name = "Get Mute Status"
    iconFile = "icons/SoundCard"
    
    def __call__(self, deviceId=0):
        return SoundMixer.GetMute(deviceId)


    def GetLabel(self, *args):
        return self.text.name
         
        
    def Configure(self, deviceId=0):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.Choice(deviceId, choices=SoundMixer.GetMixerDevices())
        panel.AddLine("Device:", deviceCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetValue())



class SetMasterVolume(eg.ActionBase):
    name = "Set Master Volume"
    description = "Sets the master volume to an absolute value."
    iconFile = "icons/SoundCard"

    class text:
        text1 = "Set master volume to"
        text2 = "percent."


    def __call__(self, value, deviceId=0):
        SoundMixer.SetMasterVolume(value, deviceId)
        return SoundMixer.GetMasterVolume(deviceId)


    def GetLabel(self, value, deviceId=0):
        if deviceId > 0:
            return "%s #%i: %.2f %%" % (self.name, deviceId+1, value)
        else:
            return "%s: %.2f %%" % (self.name, value)


    def Configure(self, value=0, deviceId=0):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.Choice(deviceId, SoundMixer.GetMixerDevices())
        valueCtrl = panel.SpinNumCtrl(value, min=0, max=100)
        sizer = eg.HBoxSizer(
            (panel.StaticText(self.text.text1), 0, wx.ALIGN_CENTER_VERTICAL),
            (valueCtrl, 0, wx.LEFT|wx.RIGHT, 5),
            (panel.StaticText(self.text.text2), 0, wx.ALIGN_CENTER_VERTICAL),
        )
        panel.AddLine("Device:", deviceCtrl)
        panel.AddLine(sizer)
        while panel.Affirmed():
            panel.SetResult(
                float(valueCtrl.GetValue()),
                deviceCtrl.GetValue(),
            )



class ChangeMasterVolumeBy(eg.ActionBase):
    name = "Change Master Volume"
    description = "Changes the master volume relative to the current value."
    iconFile = "icons/SoundCard"
    class text:
        text1 = "Change master volume by"
        text2 = "percent."


    def __call__(self, value, deviceId=0):
        SoundMixer.ChangeMasterVolumeBy(value, deviceId)
        return SoundMixer.GetMasterVolume(deviceId)


    def GetLabel(self, value, deviceId=0):
        if deviceId > 0:
            return "%s #%i: %.2f %%" % (self.name, deviceId+1, value)
        else:
            return "%s: %.2f %%" % (self.name, value)


    def Configure(self, value=0, deviceId=0):
        panel = eg.ConfigPanel()
        deviceCtrl = panel.Choice(
            deviceId,
            choices=SoundMixer.GetMixerDevices()
        )
        valueCtrl = panel.SpinNumCtrl(value, min=-100, max=100)
        sizer = eg.HBoxSizer(
            (panel.StaticText(self.text.text1), 0, wx.ALIGN_CENTER_VERTICAL),
            (valueCtrl, 0, wx.LEFT|wx.RIGHT, 5),
            (panel.StaticText(self.text.text2), 0, wx.ALIGN_CENTER_VERTICAL),
        )
        panel.AddLine("Device:", deviceCtrl)
        panel.AddLine(sizer)
        while panel.Affirmed():
            panel.SetResult(
                float(valueCtrl.GetValue()),
                deviceCtrl.GetValue(),
            )



class ShowPictureFrame(wx.Frame):
    def __init__(self, size=(-1,-1), pic_path=None, display=0):
        wx.Frame.__init__(
            self,
            None,
            -1,
            "ShowPictureFrame",
            style=wx.NO_BORDER|wx.FRAME_NO_TASKBAR #| wx.STAY_ON_TOP
        )
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.Bind(wx.EVT_LEFT_DCLICK, self.LeftDblClick)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        bitmap = wx.EmptyBitmap(1, 1)
        self.staticBitmap = wx.StaticBitmap(self, -1, bitmap)
        self.staticBitmap.Bind(wx.EVT_LEFT_DCLICK, self.LeftDblClick)
        self.staticBitmap.Bind(wx.EVT_MOTION, self.ShowCursor)
        self.timer = Timer(2.0, self.HideCursor)


    def SetPicture(self, picturePath=None, display=0):
        if not picturePath:
            return
        dimension = GetMonitorDimensions()[display]
        pil = Image.open(picturePath)
        width, height = pil.size
        if (width > dimension.width) or (height > dimension.height):
            xfactor = (width * 1.0 / dimension.width)
            yfactor = (height * 1.0 / dimension.height)
            if xfactor > yfactor:
                width = dimension.width
                height = int(round(height / xfactor))
            else:
                width = int(round(width / yfactor))
                height = dimension.height
            pil = pil.resize((width, height), Image.NEAREST)

        bitmap = wx.BitmapFromBuffer(
            width, height, pil.convert('RGB').tostring()
        )
        self.staticBitmap.SetBitmap(bitmap)
        x = dimension.x + (dimension.width - width) / 2
        y = dimension.y + (dimension.height - height) / 2
        self.SetDimensions(x, y, width, height)


    def LeftDblClick(self, dummyEvent):
        self.Show(False)


    def OnClose(self, dummyEvent):
        self.Hide()


    def OnShowMe(self):
        self.Show()
        BringHwndToFront(self.GetHandle())
        self.Raise()
        self.Update()
        self.staticBitmap.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))


    def ShowCursor(self, event):
        self.staticBitmap.SetCursor(wx.NullCursor)
        self.timer.cancel()
        self.timer = Timer(2.0, self.HideCursor)
        self.timer.start()
        event.Skip()


    def HideCursor(self):
        wx.CallAfter(
            self.staticBitmap.SetCursor,
            wx.StockCursor(wx.CURSOR_BLANK)
        )



class ShowPicture(eg.ActionBase):
    name = "Show Picture"
    description = "Shows a picture on the screen."
    iconFile = "icons/ShowPicture"
    class text:
        path = "Path to picture (use an empty path to clear):"
        display = "Monitor"
        allImageFiles = 'All Image Files'
        allFiles = "All files"



    def __call__(self, imageFile='', display=0):
        imageFile = eg.ParseString(imageFile)
        if imageFile:
            self.pictureFrame.SetPicture(imageFile, display)
            wx.CallAfter(self.pictureFrame.OnShowMe)
        else:
            self.pictureFrame.Show(False)


    def Configure(self, imageFile='', display=0):
        panel = eg.ConfigPanel()
        text = self.text
        filepathCtrl = eg.FileBrowseButton(
            panel,
            size=(340, -1),
            initialValue=imageFile,
            labelText="",
            fileMask='%s|*.jpg;*.bmp;*.gif;*.png|%s (*.*)|*.*' % (
                text.allImageFiles,
                text.allFiles
            ),
            buttonText=eg.text.General.browse,
        )
        displayChoice = eg.DisplayChoice(panel, display)

        panel.AddLabel(text.path)
        panel.AddCtrl(filepathCtrl)
        panel.AddLabel(text.display)
        panel.AddCtrl(displayChoice)

        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue(), displayChoice.GetValue())

def _CreateShowPictureFrame():
    ShowPicture.pictureFrame = ShowPictureFrame()
wx.CallAfter(_CreateShowPictureFrame)



class SetDisplayPreset(eg.ActionBase):
    name = "Set Display Preset"
    iconFile = "icons/Display"
    class text:
        query = "Query current display settings"
        fields = (
            "Device", "Left  ", "Top   ", "Width", "Height", "Frequency",
            "Colour Depth", "Attached", "Primary", "Flags"
        )


    def __call__(self, *args):
        eg.WinApi.Display.SetDisplayModes(*args)


    def GetLabel(self, *args):
        return self.name


    def Configure(self, *args):
        result = [None]
        panel = eg.ConfigPanel()
        panel.dialog.buttonRow.okButton.Enable(False)
        panel.dialog.buttonRow.applyButton.Enable(False)
        def OnButton(event):
            FillList(eg.WinApi.Display.GetDisplayModes())
            panel.dialog.buttonRow.okButton.Enable(True)
            panel.dialog.buttonRow.applyButton.Enable(True)

        button = wx.Button(panel, -1, self.text.query)
        button.Bind(wx.EVT_BUTTON, OnButton)
        panel.sizer.Add(button)
        panel.sizer.Add((5, 5))
        listCtrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        fields = self.text.fields
        for col, name in enumerate(fields):
            listCtrl.InsertColumn(col, name)
        def FillList(args):
            result[0] = args
            listCtrl.DeleteAllItems()
            for i, argLine in enumerate(args):
                listCtrl.InsertStringItem(i, "")
                for col, arg in enumerate(argLine):
                    listCtrl.SetStringItem(i, col, str(arg))
        FillList(args)
        for i in range(1, len(fields)):
            listCtrl.SetColumnWidth(i, -2)
        x = 0
        for i in range(len(fields)):
            x += listCtrl.GetColumnWidth(i)
        listCtrl.SetMinSize((x+4, -1))
        panel.sizer.Add(listCtrl, 1, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(*result[0])



class WakeOnLan(eg.ActionBase):
    name = "Wake on LAN"
    description = (
        "Wakes up another computer through sending a special "
        "network packet."
    )
    iconFile = "icons/WakeOnLan"
    class text:
        parameterDescription = "Ethernet adapter MAC address to wake up:"


    def __call__(self, macAddress):
        # Check macaddress format and try to compensate.
        if len(macAddress) == 12:
            pass
        elif len(macAddress) == 12 + 5:
            sep = macAddress[2]
            macAddress = macAddress.replace(sep, '')
        else:
            raise ValueError('Incorrect MAC address format')

        # Pad the synchronization stream.
        data = ''.join(['FFFFFFFFFFFF', macAddress * 20])
        send_data = ''

        # Split up the hex values and pack.
        for i in range(0, len(data), 2):
            send_data = ''.join(
                [send_data, struct.pack('B', int(data[i: i + 2], 16))]
            )

        # Broadcast it to the LAN.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, ('<broadcast>', 7))


    def Configure(self, macAddress=""):
        from wx.lib.masked import TextCtrl
        panel = eg.ConfigPanel()
        macCtrl  = TextCtrl(
            panel,
            mask = "##-##-##-##-##-##",
            includeChars = "ABCDEF",
            choiceRequired = True,
            defaultValue = macAddress.upper(),
            formatcodes = "F!",
        )
        panel.AddLine(self.text.parameterDescription, macCtrl)
        while panel.Affirmed():
            panel.SetResult(macCtrl.GetValue())



class SetSystemIdleTimer(eg.ActionBase):
    name = "Set System Idle Timer"
    class text:
        text = "Choose option:"
        choices = [
            "Disable system idle timer",
            "Enable system idle timer"
        ]

    def __call__(self, flag=False):
        # ES_CONTINUOUS       = 0x80000000
        # ES_DISPLAY_REQUIRED = 0x00000002
        # ES_SYSTEM_REQUIRED  = 0x00000001
        #      or-ed together = 0x80000003
        if flag:
            SetThreadExecutionState(0x80000000)
        else:
            SetThreadExecutionState(0x80000003)


    def GetLabel(self, flag=0):
        return self.text.choices[flag]


    def Configure(self, flag=False):
        panel = eg.ConfigPanel()
        text = self.text
        radioBox = wx.RadioBox(
            panel,
            -1,
            text.text,
            choices=text.choices,
            majorDimension=1
        )
        radioBox.SetSelection(int(flag))
        panel.sizer.Add(radioBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(bool(radioBox.GetSelection()))

