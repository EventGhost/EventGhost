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


import time
import sys
import os
import os.path
import thread
from threading import Timer

from win32con import *
import win32api
import win32gui
import win32file
import win32con
import win32process
import win32clipboard
from win32security import (
    OpenProcessToken, 
    LookupPrivilegeValue, 
    AdjustTokenPrivileges,
)

import ctypes
import wx
import Image

import eg.WinAPI.SoundMixer as SoundMixer
from eg.WinAPI.Utils import BringHwndToFront
from eg.WinAPI.Utils import GetMonitorDimensions
from eg.cFunctions import RegisterKeyhook, UnregisterKeyhook
from eg.cFunctions import ResetIdleTimer as HookResetIdleTimer
from eg.cFunctions import SetIdleTime as HookSetIdleTime

from ChangeDisplaySettings import ChangeDisplaySettings
from Execute import Execute
from DeviceChangeNotifier import DeviceChangeNotifier
from PowerBroadcastNotifier import PowerBroadcastNotifier
import Registry

class Text:
    name = "System"
    
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
        description = \
            "These actions suspends, hibernates, reboots or shutsdown "\
            "the computer. Can also lock the workstation and logoff the "\
            "current user."
        
    forced   = "Forced: %s"
    forcedCB = "Force close of all programs"
    
    RegistryGroup = Registry.Text



def getDeviceHandle(drive):
    '''Returns a properly formatted device handle for DeviceIOControl call.'''
    return "\\\\.\\%s:" % drive[:1].upper()

        
#=============================================================================
# Plugin: System
#=============================================================================
class System(eg.PluginClass):
    text = Text
    
    def __init__(self):
        text = self.text
        self.AddAction(Execute)
        self.AddAction(OpenDriveTray)
        self.AddAction(SetClipboard)
        self.AddAction(WakeOnLan)
        self.AddAction(SetIdleTime)
        self.AddAction(ResetIdleTimer)
        
        subgroup = self.AddGroup(
            text.SoundGroup.name, 
            text.SoundGroup.description,
            "icons/SoundCard"
        )
        subgroup.AddAction(MuteOn)
        subgroup.AddAction(MuteOff)
        subgroup.AddAction(ToggleMute)
        subgroup.AddAction(SetMasterVolume)
        subgroup.AddAction(ChangeMasterVolumeBy)
        subgroup.AddAction(PlaySound)
        
        subgroup = self.AddGroup(
            text.MonitorGroup.name,
            text.MonitorGroup.description,
            "icons/Display"
        )
        subgroup.AddAction(StartScreenSaver)
        subgroup.AddAction(MonitorStandby)
        subgroup.AddAction(MonitorPowerOff)
        subgroup.AddAction(MonitorPowerOn)
        subgroup.AddAction(ChangeDisplaySettings)
        subgroup.AddAction(ShowPicture)
        subgroup.AddAction(SetWallpaper)
        subgroup.AddAction(SetDisplayPreset)

        subgroup = self.AddGroup(
            text.PowerGroup.name,
            text.PowerGroup.description,
            "icons/Shutdown"
        )
        subgroup.AddAction(PowerDown)
        subgroup.AddAction(Reboot)
        subgroup.AddAction(Standby)
        subgroup.AddAction(Hibernate)
        subgroup.AddAction(LogOff)
        subgroup.AddAction(LockWorkstation)
        subgroup.AddAction(SetSystemIdleTimer)
        
        Registry.Init(self)
        
        
    def __start__(self):
        #Assign all available cd drives to self.drives. If CdRom.drive
        #is not already set, the first drive returned becomes the default.
        cdDrives = []
        letters = [l + ':' for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        for drive in letters:
            if win32file.GetDriveType(drive)==5:
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

        try:
            RegisterKeyhook(
                self.IdleCallback, 
                self.UnIdleCallback, 
            )
        except:
            eg.PrintTraceback()
        
        # Use VistaVolume.dll from stridger for sound volume control on Vista
        if majorVersion > 5:
            pluginDir = os.path.abspath(os.path.split(__file__)[0])
            dllPath = os.path.join(pluginDir, "VistaVolume.dll")
            vistaVolumeDll = ctypes.cdll.LoadLibrary(dllPath)
            vistaVolumeDll.SetMasterVolume.argtypes = [ctypes.c_float]
            vistaVolumeDll.GetMasterVolume.restype = ctypes.c_float
            
            def MuteOn(self):
                vistaVolumeDll.SetMute(1)
                return True
               
            def MuteOff(self):
                vistaVolumeDll.SetMute(0)
                return False
               
            def ToggleMute(self):
                newValue = not vistaVolumeDll.GetMute()
                vistaVolumeDll.SetMute(newValue)
                return newValue
               
            def SetMasterVolume(self, value):
                vistaVolumeDll.SetMasterVolume(value / 100.0)
                return vistaVolumeDll.GetMasterVolume() * 100.0
               
            def ChangeMasterVolumeBy(self, value):
                old = vistaVolumeDll.GetMasterVolume()
                vistaVolumeDll.SetMasterVolume((old * 100.0 + value) / 100.0)
                return vistaVolumeDll.GetMasterVolume() * 100.0
            
            self.MuteOn.__class__.__call__ = MuteOn
            self.MuteOff.__class__.__call__ = MuteOff
            self.ToggleMute.__class__.__call__ = ToggleMute
            self.SetMasterVolume.__class__.__call__ = SetMasterVolume
            self.ChangeMasterVolumeBy.__class__.__call__ = ChangeMasterVolumeBy             
                        
                
    @eg.LogItWithReturn
    def __stop__(self):
        self.deviceChangeNotifier.Close()
        self.powerBroadcastNotifier.Close()
        UnregisterKeyhook()
        
        
    def IdleCallback(self):
        self.TriggerEvent("Idle")
        
        
    def UnIdleCallback(self):
        self.TriggerEvent("UnIdle")
        
        
        
class SetIdleTime(eg.ActionClass):
    class text:
        name = "Set Idle Time"
        label1 = "Wait"
        label2 = "seconds before triggering idle event."
        
        
    def __call__(self, idleTime):
        HookSetIdleTime(int(idleTime * 1000))
        
        
    def Configure(self, waitTime=60.0):
        dialog = eg.ConfigurationDialog(self)
        mySizer = wx.BoxSizer(wx.HORIZONTAL)
        staticText = wx.StaticText(dialog, -1, self.text.label1)
        mySizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        waitTimeCtrl = eg.SpinNumCtrl(dialog, -1, waitTime, integerWidth=5)
        mySizer.Add(waitTimeCtrl, 0, wx.EXPAND)
        staticText = wx.StaticText(dialog, -1, self.text.label2)
        mySizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        dialog.sizer.Add(mySizer, 0, wx.EXPAND)

        if dialog.AffirmedShowModal():
            return (waitTimeCtrl.GetValue(), )
        
        
        
class ResetIdleTimer(eg.ActionClass):
    name = "Reset Idle Timer"
       
    def __call__(self):
        HookResetIdleTimer()



class OpenDriveTray(eg.ActionClass):
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
        drive = drive or self.cdDrives[0]

        def EjectMedia():
            device = getDeviceHandle(drive)
            try:
                hdevice = win32file.CreateFile(
                    device, 
                    GENERIC_READ,
                    FILE_SHARE_READ, 
                    None, 
                    OPEN_EXISTING, 
                    0, 
                    0
                )
            except:
                self.PrintError(
                    "Couldn't find drive %s:" % drive[:1].upper()
                )
                return 
            win32file.DeviceIoControl(hdevice, 2967560, "", 0, None)
            win32file.CloseHandle(hdevice)
    
        def LoadMedia():
            device = getDeviceHandle(drive)
            try:
                hdevice = win32file.CreateFile(
                    device, 
                    GENERIC_READ,
                    FILE_SHARE_READ, 
                    None, 
                    OPEN_EXISTING, 
                    0, 
                    0
                )
            except:
                self.PrintError(
                    "Couldn't find drive %s:" % drive[:1].upper()
                )
                return 
            win32file.DeviceIoControl(hdevice, 2967564, "", 0, None)
            win32file.CloseHandle(hdevice)
    
        def ToggleMedia():
            start = time.clock()
            EjectMedia()
            end = time.clock()
            if end - start < 0.1:
                LoadMedia()
    
        if action is 0:
            thread.start_new_thread(ToggleMedia, ())
        elif action is 1:
            thread.start_new_thread(EjectMedia, ())
        elif action is 2:
            thread.start_new_thread(LoadMedia, ())
            
            
    def GetLabel(self, drive, action):
        return self.text.labels[action] % drive
         
        
    def Configure(self, old_drive=None, action=0):
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        radiobox = wx.RadioBox(
            dialog, 
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
        for drive in letters:
            if win32file.GetDriveType(drive) == 5:
                cdDrives.append(drive)
        label = wx.StaticText(dialog, -1, text.driveLabel)
 
        choice = wx.Choice(dialog, -1, choices=cdDrives)
        if old_drive is None:
            old_drive = ''
        if not choice.SetStringSelection(old_drive):
            choice.SetSelection(0)
        mySizer = wx.BoxSizer(wx.HORIZONTAL)
        mySizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
        mySizer.Add((5,5))
        mySizer.Add(choice)
        
        sizer = dialog.sizer
        sizer.Add(radiobox, 0, wx.EXPAND)
        sizer.Add((5,5))
        sizer.Add(mySizer, 0, wx.EXPAND|wx.ALL, 5)
          
        if dialog.AffirmedShowModal():
            return (str(choice.GetStringSelection()), radiobox.GetSelection())



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
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        fileText = wx.StaticText(dialog, -1, text.text1)
        filepathCtrl = eg.FileBrowseButton(
            dialog, -1, size=(340,-1),
            initialValue=wavfile,
            labelText="",
            fileMask=text.fileMask,
            buttonText=eg.text.General.browse,
        )
    
        wait_checkbox = wx.CheckBox(dialog, -1, text.text2)
        wait_checkbox.SetValue(flags == wx.SOUND_SYNC)
        
        sizer = dialog.sizer
        sizer.Add(fileText, 0, wx.EXPAND)
        sizer.Add(filepathCtrl, 0, wx.EXPAND)
        sizer.Add(wait_checkbox, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
    
        if dialog.AffirmedShowModal():
            if wait_checkbox.IsChecked():
                flags = wx.SOUND_SYNC
            else:
                flags = wx.SOUND_ASYNC
            return (filepathCtrl.GetValue(), flags)



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
            eg.app.clipboardEvent.Fire()
#        if None == win32clipboard.OpenClipboard(0):
#            win32clipboard.EmptyClipboard()
#            win32clipboard.SetClipboardText(self.clipboardString)
#            win32clipboard.CloseClipboard()
        else:
            PrintError(self.text.error)
    


class StartScreenSaver(eg.ActionClass):
    name = "Start windows screen saver"
    description = "Starts the currently in windows selected screensaver."
    iconFile = "icons/StartScreenSaver"
        
    def __call__(self):
        win32api.SendMessage(
            win32gui.GetForegroundWindow(),
            WM_SYSCOMMAND, 
            SC_SCREENSAVE, 
            0
        )



class MonitorStandby(eg.ActionClass):
    name = "Set monitor into stand-by mode"
    description = "Sets the state of the display to low power mode."
    iconFile = "icons/Display"
        
    def __call__(self):
        win32api.SendMessage(
            win32gui.GetForegroundWindow(),
            WM_SYSCOMMAND, 
            SC_MONITORPOWER, 
            1
        )



class MonitorPowerOff(eg.ActionClass):
    name = "Set monitor into power-off mode"
    description = \
        "Sets the state of the display to power-off mode. This will "\
        "be the most power-saving mode the display supports."
    iconFile = "icons/Display"
        
    def __call__(self):
        win32api.SendMessage(
            win32gui.GetForegroundWindow(),
            WM_SYSCOMMAND, 
            SC_MONITORPOWER, 
            2
        )



#-----------------------------------------------------------------------------
# Action: System.MonitorPowerOn
#-----------------------------------------------------------------------------
class MonitorPowerOn(eg.ActionClass):
    name = "Re-enable monitor"
    description = \
        "Turns on a display, when it is in low power or power-off "\
        "mode. Will also stop a running screensaver."
    iconFile = "icons/Display"
        
    def __call__(self):
        win32api.SendMessage(
            win32gui.GetForegroundWindow(),
            WM_SYSCOMMAND, 
            SC_MONITORPOWER, 
            -1
        )
            
            
            
#-----------------------------------------------------------------------------
# Action: System.PowerDown
#-----------------------------------------------------------------------------
class __ComputerPowerAction(eg.ActionClass):
    iconFile = "icons/Shutdown"
    
    def GetLabel(self, bForceClose=False):
        s = eg.ActionClass.GetLabel(self)
        if bForceClose:
            return self.plugin.text.forced % s
        else:
            return s
            
            
    def Configure(self, bForceClose=False):
        dialog = eg.ConfigurationDialog(self)
        checkbox = wx.CheckBox(dialog, -1, self.plugin.text.forcedCB)
        checkbox.SetValue(bForceClose)
        dialog.sizer.Add(checkbox, 0, wx.ALL, 10)
        if dialog.AffirmedShowModal():
            return (checkbox.GetValue(), )
    
            
            
class PowerDown(__ComputerPowerAction):   
    name = "Power down computer"
    description = \
        "Shuts down the system and turns off the power. The system "\
        "must support the power-off feature."
    iconFile = "icons/PowerDown"
    
    def __call__(self, bForceClose=False):
        hToken = OpenProcessToken(  
            win32api.GetCurrentProcess(),
            TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY
        )
        Luid = LookupPrivilegeValue(None, SE_SHUTDOWN_NAME)
        AdjustTokenPrivileges(hToken, False, [(Luid, SE_PRIVILEGE_ENABLED)])
        win32api.InitiateSystemShutdown(None, None, 0, bForceClose, False)
        
        
        
#-----------------------------------------------------------------------------
# Action: System.Reboot
#-----------------------------------------------------------------------------
class Reboot(__ComputerPowerAction):       
    name = "Reboot computer"
    description = "Shuts down the system and then restarts the system."
    iconFile = "icons/Reboot"

    def __call__(self, bForceClose=False):
        hToken = OpenProcessToken(  
            win32api.GetCurrentProcess(),
            TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY
        )
        Luid = LookupPrivilegeValue(None, SE_SHUTDOWN_NAME)
        AdjustTokenPrivileges(hToken, False, [(Luid, SE_PRIVILEGE_ENABLED)])
        win32api.InitiateSystemShutdown(None, None, 0, bForceClose, True)



#-----------------------------------------------------------------------------
# Action: System.Standby
#-----------------------------------------------------------------------------
class Standby(__ComputerPowerAction):
    name = "Put computer into standby mode"
    description = \
        "This function suspends the system by shutting power down "\
        "and enters a suspend (sleep) state."
    iconFile = "icons/Standby"
        
    def __call__(self, bForceClose=False):
        ctypes.windll.Powrprof.SetSuspendState(False, bForceClose, False)
        
        
        
#-----------------------------------------------------------------------------
# Action: System.Hibernate
#-----------------------------------------------------------------------------
class Hibernate(__ComputerPowerAction):  
    name = "Hibernate computer"
    description = \
        "This function suspends the system by shutting power down "\
        "and enters a hibernation (S4) state."
    iconFile = "icons/Hibernate"
    
    def __call__(self, bForceClose=False):
        ctypes.windll.Powrprof.SetSuspendState(True, bForceClose, False)
        
        
        
#-----------------------------------------------------------------------------
# Action: System.LogOff
#-----------------------------------------------------------------------------
class LogOff(eg.ActionClass):   
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
        ctypes.windll.user32.ExitWindowsEx(EWX_LOGOFF, 0x80020003)
            
            
            
#-----------------------------------------------------------------------------
# Action: System.LockWorkstation
#-----------------------------------------------------------------------------
class LockWorkstation(eg.ActionClass):   
    name = "Lock workstation"
    description = \
        "This function submits a request to lock the workstation's "\
        "display. Locking a workstation protects it from "\
        "unauthorized use. This function has the same result as "\
        "pressing Ctrl+Alt+Del and clicking Lock Workstation."
    iconFile = "icons/LockWorkstation"
    
    def __call__(self):
        ctypes.windll.user32.LockWorkStation()
        
        
        
#-----------------------------------------------------------------------------
# Action: System.SetWallpaper
#-----------------------------------------------------------------------------
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
        fileMask = "All Image Files|*.jpg;*.bmp;*.gif|All Files (*.*)|*.*"
        

    def __call__(self, imageFile='', style=1):
        if imageFile:
            im = Image.open(imageFile)
            if im.format != 'BMP':
                imageFile =  eg.APPDATA + '\\Microsoft\\Wallpaper1.bmp'
                im.save(imageFile)
        tile, wstyle = (("0", "0"), ("1", "0"), ("0", "2"))[style]
        hKey = win32api.RegCreateKey(
            win32con.HKEY_CURRENT_USER,
            "Control Panel\\Desktop"
        )
        win32api.RegSetValueEx(
            hKey, 
            "TileWallpaper", 
            0, 
            win32con.REG_SZ, 
            tile
        )
        win32api.RegSetValueEx(
            hKey, 
            "WallpaperStyle", 
            0, 
            win32con.REG_SZ, 
            wstyle
        )
        win32api.RegCloseKey(hKey)
        
        cs = ctypes.c_buffer(imageFile)
        ok = ctypes.windll.user32.SystemParametersInfoA(
            win32con.SPI_SETDESKWALLPAPER, 
            0, 
            cs, 
            win32con.SPIF_SENDCHANGE|win32con.SPIF_UPDATEINIFILE
        )


    def Configure(self, imageFile='', style=1):
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        sizer = dialog.sizer
        
        st_ctrl = wx.StaticText(dialog, -1, text.text1)
        sizer.Add(st_ctrl, 0, wx.EXPAND)
        
        filepathCtrl = eg.FileBrowseButton(
            dialog, 
            -1,
            size = (340,-1),
            initialValue = imageFile,
            labelText = "",
            fileMask = text.fileMask,
            buttonText =  eg.text.General.browse,
        )
        sizer.Add(filepathCtrl, 0, wx.EXPAND)
    
        st_ctrl = wx.StaticText(dialog, -1, text.text2)
        sizer.Add(st_ctrl, 0, wx.EXPAND|wx.TOP, 10)
        
        choice = wx.Choice(dialog, -1, choices=text.choices)
        choice.SetSelection(style)                        
        sizer.Add(choice, 0, wx.BOTTOM, 10)
    
        if dialog.AffirmedShowModal():
            return (filepathCtrl.GetValue(), choice.GetSelection())
        
        
        
#-----------------------------------------------------------------------------
# Action: System.MuteOn
#-----------------------------------------------------------------------------
class MuteOn(eg.ActionClass):
    name = "Turn Mute On"       
    iconFile = "icons/SoundCard"
    
    def __call__(self):
        SoundMixer.SetMute(True)
        return True


#-----------------------------------------------------------------------------
# Action: System.MuteOff
#-----------------------------------------------------------------------------
class MuteOff(eg.ActionClass):
    name = "Turn Mute Off"
    iconFile = "icons/SoundCard"
    
    def __call__(self):
        SoundMixer.SetMute(False)
        return False



#-----------------------------------------------------------------------------
# Action: System.ToggleMute
#-----------------------------------------------------------------------------
class ToggleMute(eg.ActionClass):
    name = "Toggle Mute"
    iconFile = "icons/SoundCard"
    
    def __call__(self):
        return SoundMixer.ToggleMute()



#-----------------------------------------------------------------------------
# Action: System.SetMasterVolume
#-----------------------------------------------------------------------------
class SetMasterVolume(eg.ActionClass):
    name = "Set Master Volume"
    iconFile = "icons/SoundCard"
    class text:
        text1 = "Set master volume to"
        text2 = "percent."
        
        
    def __call__(self, value):
        SoundMixer.SetMasterVolume(value)
        return SoundMixer.GetMasterVolume()
    
        
    def GetLabel(self, value):
        return self.text.name + ": " + str(value) + " %"
         
        
    def Configure(self, value=0):
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        st1 = wx.StaticText(dialog, -1, text.text1)
        sizer.Add(st1, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add((5,5))
        
        valueCtrl = eg.SpinNumCtrl(dialog, -1, value, min=0, max=100)
        sizer.Add(valueCtrl, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add((5,5))
        
        st2 = wx.StaticText(dialog, -1, text.text2)
        sizer.Add(st2, 0, wx.ALIGN_CENTER_VERTICAL)
        
        dialog.sizer.Add(sizer, 1, wx.EXPAND)
        
        if dialog.AffirmedShowModal():
            return (float(valueCtrl.GetValue()), )



#-----------------------------------------------------------------------------
# Action: System.ChangeMasterVolumeBy
#-----------------------------------------------------------------------------
class ChangeMasterVolumeBy(eg.ActionClass):
    name = "Change Master Volume"
    iconFile = "icons/SoundCard"
    class text:
        text1 = "Change master volume by"
        text2 = "percent."
        
    
    def __call__(self, value):
        SoundMixer.ChangeMasterVolumeBy(value)
        return SoundMixer.GetMasterVolume()


    def GetLabel(self, value):
        return self.text.name + ": " + str(value) + " %"
         
        
    def Configure(self, value=0):            
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        st1 = wx.StaticText(dialog, -1, text.text1)
        sizer.Add(st1, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add((5,5))
        
        valueCtrl = eg.SpinNumCtrl(dialog, -1, value, min=-100, max=100)
        sizer.Add(valueCtrl, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add((5,5))
        
        st2 = wx.StaticText(dialog, -1, text.text2)
        sizer.Add(st2, 0, wx.ALIGN_CENTER_VERTICAL)
        
        dialog.sizer.Add(sizer, 1, wx.EXPAND)
        
        if dialog.AffirmedShowModal():
            return (float(valueCtrl.GetValue()), )


#-----------------------------------------------------------------------------
# Action: System.ShowPicture
#-----------------------------------------------------------------------------
class ShowPictureFrame(wx.Frame):
    def __init__(self, size=(-1,-1), pic_path=None, display=0):
        wx.Frame.__init__(
            self, 
            None, 
            -1, 
            "ShowPictureFrame", 
            style=wx.NO_BORDER|wx.FRAME_NO_TASKBAR #| wx.STAY_ON_TOP
        )
        self.SetBackgroundColour(wx.Colour(0,0,0))
        self.Bind(wx.EVT_LEFT_DCLICK, self.LeftDblClick)
        bitmap = wx.EmptyBitmap(1,1)
        self.staticBitmap = wx.StaticBitmap(self, -1, bitmap)
        self.staticBitmap.Bind(wx.EVT_LEFT_DCLICK, self.LeftDblClick)
        self.staticBitmap.Bind(wx.EVT_MOTION, self.ShowCursor)
        self.timer = Timer(2.0, self.HideCursor)

        
    def SetPicture(self, pic_path=None, display=0):
        if pic_path:
            mons = GetMonitorDimensions()
            d = mons[display]
            pil = Image.open(pic_path)
            width, height = pil.size
            if (width > d.width) or (height > d.height):
                xfactor = (width * 1.0 / d.width)
                yfactor = (height * 1.0 / d.height)
                if xfactor > yfactor:
                    width = d.width
                    height = int(round(height / xfactor))
                else:
                    width = int(round(width / yfactor))
                    height = d.height
                pil = pil.resize((width, height), Image.NEAREST)
                
            image = wx.EmptyImage(width, height)
            image.SetData(pil.convert('RGB').tostring())
            bitmap = image.ConvertToBitmap()
            self.staticBitmap.SetBitmap(bitmap)
            x = d.x + (d.width - width) / 2
            y = d.y + (d.height - height) / 2
            self.SetDimensions(x, y, width, height)
        
        
    def LeftDblClick(self, evt):
        self.Show(False)


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
        
        
        
class ShowPicture(eg.ActionClass):
    name = "Show picture"
    description = "Shows a picture on the screen."
    iconFile = "icons/ShowPicture"
    class text:
        path = "Path to picture (use an empty path to clear):"
        display = "Monitor"
        allImageFiles = 'All Image Files'
        allFiles = "All files"
    
    def __init__(self):
        def DoIt():
            self.pictureFrame = ShowPictureFrame()
        wx.CallAfter(DoIt)
        
    
    def __call__(self, imageFile='', display=0):
        imageFile = eg.ParseString(imageFile)
        if imageFile:
            self.pictureFrame.SetPicture(imageFile, display)
            wx.CallAfter(self.pictureFrame.OnShowMe)
        else:
            self.pictureFrame.Show(False)


    def Configure(self, imageFile='', display=0):
        dialog = eg.ConfigurationDialog(self)
        sizer = dialog.sizer
        
        st_ctrl = wx.StaticText(dialog, -1, self.text.path)
        sizer.Add(st_ctrl, 0, wx.EXPAND)
        
        filepathCtrl = eg.FileBrowseButton(
            dialog, 
            -1, 
            size=(340,-1),
            initialValue=imageFile,
            labelText="",
            fileMask='%s|*.jpg;*.bmp;*.gif;*.png|%s (*.*)|*.*' % (
                self.text.allImageFiles, 
                self.text.allFiles
            ),
            buttonText=eg.text.General.browse,
        )
        sizer.Add(filepathCtrl, 0, wx.EXPAND)
    
        staticText = wx.StaticText(dialog, -1, self.text.display)
        sizer.Add(staticText, 0, wx.EXPAND|wx.TOP, 10)
        
        displayChoice = eg.DisplayChoice(dialog, display)
        sizer.Add(choice, 0, wx.BOTTOM, 10)
    
        if dialog.AffirmedShowModal():
            return (filepathCtrl.GetValue(), displayChoice.GetValue())
        
        
        
class SetDisplayPreset(eg.ActionClass):
    name = "Set Display Preset"
    iconFile = "icons/Display"
    class text:
        query = "Query current display settings"
        fields = (
            "Device", "Left  ", "Top   ", "Width", "Height", "Frequency", 
            "Colour Depth", "Attached", "Primary", "Flags"
        )
        
        
    def __call__(self, *args):
        eg.WinAPI.Display.SetDisplayModes(*args)
        
        
    def Configure(self, *args):
        result = [None]
        dialog = eg.ConfigurationDialog(self)
        dialog.buttonRow.okButton.Enable(False)
        def OnButton(event):
            FillList(eg.WinAPI.Display.GetDisplayModes())
            dialog.buttonRow.okButton.Enable(True)
        
        button = wx.Button(dialog, -1, self.text.query)
        button.Bind(wx.EVT_BUTTON, OnButton)
        dialog.sizer.Add(button)
        dialog.sizer.Add((5,5))
        listCtrl = wx.ListCtrl(dialog, style=wx.LC_REPORT)
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
        dialog.sizer.Add(listCtrl, 1, wx.EXPAND)
        
        if dialog.AffirmedShowModal():
            return result[0]
        
        
#-----------------------------------------------------------------------------
# Action: System.WakeOnLan
#-----------------------------------------------------------------------------
import socket
import struct

class WakeOnLan(eg.ActionClass):
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
        import wx.lib.masked
        dialog = eg.ConfigurationDialog(self)
        macCtrl  = wx.lib.masked.TextCtrl( 
            dialog, 
            mask = "##-##-##-##-##-##",
            includeChars = "ABCDEF",
            choiceRequired = True,
            defaultValue = macAddress.upper(),
            formatcodes = "F!",
        )
        dialog.AddLabel(self.text.parameterDescription)
        dialog.AddCtrl(macCtrl)
        if dialog.AffirmedShowModal():
            return (macCtrl.GetValue(), )
    

#-----------------------------------------------------------------------------
# Action: System.SetSystemIdleTimer
#-----------------------------------------------------------------------------
from eg.WinAPI.win32types import SetThreadExecutionState

class SetSystemIdleTimer(eg.ActionClass):
    name = "Set system idle timer"
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
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        radioBox = wx.RadioBox(
            dialog, 
            -1, 
            text.text,
            choices=text.choices, 
            majorDimension=1
        )
        radioBox.SetSelection(int(flag))
        dialog.sizer.Add(radioBox, 0, wx.EXPAND)

        if dialog.AffirmedShowModal():
            return (bool(radioBox.GetSelection()), )
        