# -*- coding: utf-8 -*-
#
# plugins/MyTheatre/__init__.py
#
# This file is a plugin for EventGhost.
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

import eg

eg.RegisterPlugin(
    name = "MyTheatre",
    author = "Milbrot",
    version = "1.1.1093",
    kind = "program",
    guid = "{2347B12C-FB95-4F9E-A89E-61DD72669DB8}",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control the <a href="http://www.dvbcore.com/">'
        'MyTheatre</a> multimedia application.'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADMklEQVR42m1TX0xScRT+"
        "Ln+7dCkEiTCFm5ZiW2WLP0FZuVHZU6tcL2091dbW5nzsqS3XWy++Vw/W2mpzPeVsjbUF"
        "BiikBs7WNBVUQpA/FxHw3gt14YFZ9m3n4bed853vfL9zCPwH60sz3eks44SMovco9oEk"
        "yWWK2uuiqAbPv7nEzkdkPejIzbqGRFHWslhWoKLS40CTEfThVjQ2asFxpUC5zA0olWrv"
        "LgL37PjtH/LPzw7GY2Tb/F4kCR22tUYcMraDbm2DQqGo5VUqlWI6Hbun1ba8rhOEvy84"
        "hj2Ei9V/I03t0zgTK0Oe0GFd2YImugOtR45CKpXWlZbLfJFhNpwajd5bI3j+fHgyvEJb"
        "CkKB7tQKTGoPiu+j8MxuoEF3CDdu9sFsNtdVVBGPRwN6vdFKzIa93TO+gDubq4CTGJGR"
        "GDAz9wprk250dh6HkqKwtraKvr6+WsjlcrAsi83NnBCJ84T78+jjlUjikUQsAimTYikS"
        "x7v3ozh31g6tVguRSASe5xAMBtHf3w+appHP55FKbUAsZgeJiQn3cCadv6NUKgWJJPw+"
        "P7z+CfT09CAUCiGbzcJmOyMQBARFJtisNuQLBWzlN6HXa14SX79+GSZJ1R21WlObMRwO"
        "482bt7BYLNjeLgmd0tU9qBG0GZpgMplQ2GaFMTjB3OaXxPj4h8cnTjgeVYvFYjEYhhFM"
        "fVEzSqVSoVQqCYbF4Q0twdbVAz2VQ4VjIJKJYDjSPEhMT3u6DQaTW61urDsci8UwMjKC"
        "pcVF5LIZSH4n0XDFLEi/Di6yBSUbhkbxC86rF87XvnFs7O1kb+8ty86trHadmQoiEVkA"
        "TaRROFaAT3IQ80EbuLX9OCwbCzx98tBaI5iacjsIQubq6rKR1TfP80gmk1hcmEdi9Seo"
        "zCr2y5IItRcwx7cgPaErPrjU6bRaLnrrqzw6+uo2Reme2e0Xyarz1TFWostIxVchZX6h"
        "hU1jy1CCh98smtW9925cu/v6r1uoIhD45PD5PEPNzR0Wcg8FJpdDPpMAn4mDSEWRItiA"
        "89b9AavVufuYdsLv/9gdCn1zsixPVyplyKTi5ZNdp112++Vd5/wHnkdmfX7nue8AAAAA"
        "SUVORK5CYII="
    ),
)

# Changelog:
# ----------
# 2006-08-14 Milbrot
#     * initial version
# 2008-05-03 bitmonster
#     * removed ScanListRecursive. Now uses AddActionsFromList.
#     * increased version to 1.1


import _winreg
from eg.WinApi import FindWindow, SendMessageTimeout
from win32api import ShellExecute


class MsgAction(eg.ActionClass):
    def __call__(self):
        try:
            hWnd = FindWindow("TDVBMainForm", "MyTheatre")
            return SendMessageTimeout(hWnd, 3025, self.value, 0)
        except:
            raise self.Exceptions.ProgramNotRunning



class ExeAction(eg.ActionClass):
    def __call__(self):
        try:
            ShellExecute(
                0,
                None,
                "MTStart.exe",
                self.value,
                self.plugin.myTheatrePath,
                0
            )
            return True
        except:
            raise self.Exceptions.ProgramNotFound


MyActionList = (
(eg.ActionGroup, 'GroupCommon', 'Common Functions', None,
  (
    (MsgAction, 'Number0', 'Number 0', None, 2399142008), #SHORTCUT_0
    (MsgAction, 'Number1', 'Number 1', None, 2399142009), #SHORTCUT_1
    (MsgAction, 'Number2', 'Number 2', None, 2399142010), #SHORTCUT_2
    (MsgAction, 'Number3', 'Number 3', None, 2399142011), #SHORTCUT_3
    (MsgAction, 'Number4', 'Number 4', None, 2399142012), #SHORTCUT_4
    (MsgAction, 'Number5', 'Number 5', None, 2399142013), #SHORTCUT_5
    (MsgAction, 'Number6', 'Number 6', None, 2399142014), #SHORTCUT_6
    (MsgAction, 'Number7', 'Number 7', None, 2399142015), #SHORTCUT_7
    (MsgAction, 'Number8', 'Number 8', None, 2399142016), #SHORTCUT_8
    (MsgAction, 'Number9', 'Number 9', None, 2399142017), #SHORTCUT_9
    (MsgAction, 'Pause', 'Pause', None, 2399141991), #SHORTCUT_PAUSE
    (MsgAction, 'Forward', 'Forward', None, 2399141990), #SHORTCUT_FF
    (MsgAction, 'Rewind', 'Rewind', None, 2399141989), #SHORTCUT_RW
    (MsgAction, 'VolumeUp', 'Volume Up', None, 2399141993), #SHORTCUT_VOLUP
    (MsgAction, 'VolumeDown', 'Volume Down', None, 2399141992), #SHORTCUT_VOLDN
    (MsgAction, 'Mute', 'Mute', None, 2399141994), #SHORTCUT_MUTE
    (MsgAction, 'SleepTimer', 'Sleep Timer', None, 2399142001), #SHORTCUT_SLEEP
    (MsgAction, 'Fullscreen', 'Fullscreen', None, 2399141995), #SHORTCUT_FS
    (MsgAction, 'OSDInfo', 'OSD Info', None, 2399141996), #SHORTCUT_INFO
    (MsgAction, 'DvdFileToLive', 'DVD/File to Live', None, 2399141997), #SHORTCUT_TOLIVE
    (MsgAction, 'LiveToDvdFile', 'Live to DVD/File', None, 2399141998), #SHORTCUT_TOPLAY
    (MsgAction, 'OsdMenu', 'OSD Menu', None, 2399142000), #SHORTCUT_OSD
    (MsgAction, 'OptimizeForWidescreen', 'Optimize for Widescreen', None, 2399142022), #SHORTCUT_OPTWS
    (MsgAction, 'Cancel', 'Cancel', None, 2399142087), #SHORTCUT_CANCEL
    (MsgAction, 'ExitProgram', 'Exit Program', None, 2399141999), #SHORTCUT_EXIT
    (MsgAction, 'Favorit1', 'Favorit 1', None, 2399142019), #SHORTCUT_FAV1
    (MsgAction, 'Favorit2', 'Favorit 2', None, 2399142020), #SHORTCUT_FAV2
    (MsgAction, 'Favorit3', 'Favorit 3', None, 2399142021), #SHORTCUT_FAV3
    (MsgAction, 'OpenFile', 'Open File', None, 2399142023), #SHORTCUT_OPENFILE
    (MsgAction, 'SleepTimerSetup', 'Sleep Timer Setup', None, 2399142024), #SHORTCUT_SLTIMERSET
    (MsgAction, 'BestFit', 'Best Fit', None, 2399142025), #SHORTCUT_BESTFIT
    (MsgAction, 'StayOnTop', 'Stay on Top', None, 2399142026), #SHORTCUT_STAYONTOP
    (MsgAction, 'ShowOnPrimaryMonitor', 'Show on Primary Monitor', None, 2399142027), #SHORTCUT_MAKEVISIBLE
    (MsgAction, 'Settings', 'Settings', None, 2399142028), #SHORTCUT_SETTINGS
    (MsgAction, 'BackgroundMode', 'Background Mode', None, 2399142029), #SHORTCUT_BKGMODE
  )
),
(eg.ActionGroup, 'GroupLiveMode', 'Live Mode Functions', None,
  (
    (MsgAction, 'SideChannelList', 'Side Channel List', None, 2399142089), #SHORTCUT_SIDECLIST
    (MsgAction, 'OsdFavoritChannelList', 'OSD Favorit Channel List', None, 2399142090), #SHORTCUT_OSDCHLIST
    (MsgAction, 'Last', 'Last', None, 2399142091), #SHORTCUT_LAST
    (MsgAction, 'Record', 'Record', None, 2399142092), #SHORTCUT_RECORD
    (MsgAction, 'GotoRecordPosition', 'Goto Record Position', None, 2399142098), #SHORTCUT_RECPOS
    (MsgAction, 'IncreaseSpeed', 'Increase Speed', None, 2399142101), #SHORTCUT_INCSPEED
    (MsgAction, 'DecreaseSpeed', 'Decrease Speed', None, 2399142102), #SHORTCUT_DECSPEED
    (MsgAction, 'EpgWindow', 'EPG Window', None, 2399142093), #SHORTCUT_EPGWIN
    (MsgAction, 'EpgOsd', 'EPG OSD', None, 2399142099), #SHORTCUT_EPGOSD
    (MsgAction, 'NextFavoritChannel', 'Next Favorit Channel', None, 2399142095), #SHORTCUT_NEXTFAV
    (MsgAction, 'PreviousFavoritChannel', 'Previous Favorit Channel', None, 2399142094), #SHORTCUT_PREVFAV
    (MsgAction, 'NextEnumerateChannel', 'Next Enumerate Channel', None, 2399141997), #SHORTCUT_NEXTENUM
    (MsgAction, 'PreviousEnumerateChannel', 'Previous Enumerate Channel', None, 2399141996), #SHORTCUT_PREVENUM
    (MsgAction, 'ShowStreamInfo', 'Show Stream Info', None, 2399142100), #SHORTCUT_STREAMINF
    (MsgAction, 'Video', 'Video', None, 2399142103), #SHORTCUT_VIDEO
    (MsgAction, 'IvrGeneric', 'IVR/Generic', None, 2399142104), #SHORTCUT_IVRGEN
    (MsgAction, 'AutoPid', 'Auto Pid', None, 2399142105), #SHORTCUT_APID
    (MsgAction, 'AudioAb', 'Audio AB/A+B', None, 2399142106), #SHORTCUT_AB
    (MsgAction, 'Subtitles', 'Subtitles', None, 2399142107), #SHORTCUT_SUBS
    (MsgAction, 'RecordTimerWindow', 'Record Timer Window', None, 2399142108), #SHORTCUT_RECTIMERWND
    (MsgAction, 'OpenScheduler', 'Open Scheduler', None, 2399142109), #SHORTCUT_OPENSCHED
    (MsgAction, 'PidGrabber', 'Pid Grabber', None, 2399142111), #SHORTCUT_PIDGRABBER
    (MsgAction, 'PidList', 'Pid List', None, 2399142112), #SHORTCUT_PIDLIST
    (MsgAction, 'PidStatistic', 'Pid Statistic', None, 2399142113), #SHORTCUT_PIDSTAT
    (MsgAction, 'LnbSettings', 'LNB Settings', None, 2399142114), #SHORTCUT_LNBSETTINGS
    (MsgAction, 'PositionerConsole', 'Positioner Console', None, 2399142115), #SHORTCUT_POSCONSOLE
    (MsgAction, 'CiConsole', 'CI Console', None, 2399142116), #SHORTCUT_CICONSOLE
  )
),
(eg.ActionGroup, 'GroupFileMode', 'File Mode', None,
  (
    (MsgAction, 'SideFileList', 'Side File List', None, 2399142189), #SHORTCUT_SIDEFILST
    (MsgAction, 'OsdFileList', 'OSD File List', None, 2399142190), #SHORTCUT_OSDFLIST
    (MsgAction, 'NextFile', 'Next File', None, 2399142192), #SHORTCUT_NEXTFILE
    (MsgAction, 'PreviousFile', 'Previous File', None, 2399142191), #SHORTCUT_PREVFILE
  )
),
(eg.ActionGroup, 'GroupDvdMode', 'DVD Mode', None,
  (
    (MsgAction, 'DvdSubtitles', 'DVD Subtitles', None, 2399142291), #SHORTCUT_DVDSUBS
    (MsgAction, 'NextChapter', 'Next Chapter', None, 2399142293), #SHORTCUT_NEXTCHAP
    (MsgAction, 'PreviousChapter', 'Previous Chapter', None, 2399142292), #SHORTCUT_PREVCHAP
    (MsgAction, 'OsdChapterList', 'OSD Chapter List', None, 2399142294), #SHORTCUT_OSDCHPLIST
    (MsgAction, 'ChapterList', 'Chapter List', None, 2399142290), #SHORTCUT_CHAPLIST
    (MsgAction, 'DvdMenu', 'DVD Menu', None, 2399142289), #SHORTCUT_DVDMENU
    (MsgAction, 'DvdMoveUp', 'DVD Move Up', None, 2399142295), #SHORTCUT_DVDMUP
    (MsgAction, 'DvdMoveDown', 'DVD Move Down', None, 2399142296), #SHORTCUT_DVDMDN
    (MsgAction, 'DvdMoveLeft', 'DVD Move Left', None, 2399142297), #SHORTCUT_DVDMLEFT
    (MsgAction, 'DvdMoveRight', 'DVD Move Right', None, 2399142298), #SHORTCUT_DVDMRIGHT
    (MsgAction, 'DvdSelect', 'DVD Select', None, 2399142299), #SHORTCUT_DVDMSELECT
  )
),
(eg.ActionGroup, 'GroupOsd', 'OSD', None,
  (
    (MsgAction, 'OsdUp', 'OSD Up', None, 2399142389), #SHORTCUT_OSDUP
    (MsgAction, 'OsdDown', 'OSD Down', None, 2399142390), #SHORTCUT_OSDDN
    (MsgAction, 'OsdLeft', 'OSD Left', None, 2399142391), #SHORTCUT_OSDLEFT
    (MsgAction, 'OsdRight', 'OSD Right', None, 2399142392), #SHORTCUT_OSDRIGHT
    (MsgAction, 'OsdPageCategoryUp', 'OSD Page/Category Up', None, 2399142393), #SHORTCUT_CATUP
    (MsgAction, 'OsdPageCategoryDown', 'OSD Page/Category Down', None, 2399142394), #SHORTCUT_CATDN
    (MsgAction, 'Select', 'Select', None, 2399142395), #SHORTCUT_SELECT
    (MsgAction, 'EventInfo', 'Event Info', None, 2399142397), #SHORTCUT_EVINFO
  )
),
(eg.ActionGroup, 'GroupSideChannel', 'Side Channel/File List Functions', None,
  (
    (MsgAction, 'SideChannelFileUp', 'Side Channel File Up', None, 2399142489), #SHORTCUT_SCFUP
    (MsgAction, 'SideChannelFileDown', 'Side Channel File Down', None, 2399142490), #SHORTCUT_SCFDN
    (MsgAction, 'SideChannelFileSelect', 'Side Channel File Select', None, 2399142491), #SHORTCUT_SCFSELECT
    (MsgAction, 'SideChannelFileDelete', 'Side Channel File Delete', None, 2399142492), #SHORTCUT_SCFDELETE
    (MsgAction, 'SideChannelFileSatellit', 'Side Channel File Satellit', None, 2399142493), #SHORTCUT_SCFSAT
    (MsgAction, 'SideChannelFileProvider', 'Side Channel File Provider', None, 2399142494), #SHORTCUT_SCFPROV
    (MsgAction, 'SideChannelFileNetid', 'Side Channel File NetID', None, 2399142495), #SHORTCUT_SCFPROVID
    (MsgAction, 'SideChannelFileTransponder', 'Side Channel File Transponder', None, 2399142496), #SHORTCUT_
    (MsgAction, 'SideChannelFileFavorit', 'Side Channel File Favorit', None, 2399142497), #SHORTCUT_SCFTRANSP
    (MsgAction, 'SideChannelFileAll', 'Side Channel File All', None, 2399142498), #SHORTCUT_SCFALL
  )
),
(eg.ActionGroup, 'GroupEpgWindow', 'EPG Window Mode', None,
  (
    (MsgAction, 'EpgWindowUp', 'EPG Window Up', None, 2399142589), #SHORTCUT_EPGWUP
    (MsgAction, 'EpgWindowDown', 'EPG Window Down', None, 2399142590), #SHORTCUT_EPGWDN
    (MsgAction, 'EpgWindowPageUp', 'EPG Window Page Up', None, 2399142591), #SHORTCUT_EPGWPGUP
    (MsgAction, 'EpgWindowPageDown', 'EPG Window Page Down', None, 2399142592), #SHORTCUT_EPGWPGDN
    (MsgAction, 'EpgWindowChannelUp', 'EPG Window Channel Up', None, 2399142593), #SHORTCUT_EPGWCHUP
    (MsgAction, 'EpgWindowChannelDown', 'EPG Window Channel Down', None, 2399142594), #SHORTCUT_EPGWCHDN
    (MsgAction, 'EpgWindowSelect', 'EPG Window Select', None, 2399142595), #SHORTCUT_EPGWSEL
    (MsgAction, 'EpgWindowShedule', 'EPG Window Shedule', None, 2399142596), #SHORTCUT_EPGWSHED
    (MsgAction, 'EpgWindowAllNowNext', 'EPG Window All/Now/Next', None, 2399142597), #SHORTCUT_EPGWANN
  )
),
(eg.ActionGroup, 'GroupPresets', 'Presets', None,
  (
    (MsgAction, 'Preset1', 'Preset 1', None, 2399142689), #SHORTCUT_PRESET1
    (MsgAction, 'Preset2', 'Preset 2', None, 2399142690), #SHORTCUT_PRESET2
    (MsgAction, 'Preset3', 'Preset 3', None, 2399142691), #SHORTCUT_PRESET3
    (MsgAction, 'Preset4', 'Preset 4', None, 2399142692), #SHORTCUT_PRESET4
    (MsgAction, 'Preset5', 'Preset 5', None, 2399142693), #SHORTCUT_PRESET5
    (MsgAction, 'Preset6', 'Preset 6', None, 2399142694), #SHORTCUT_PRESET6
  )
),
(eg.ActionGroup, 'GroupPlugin', 'Plugin controls', None,
  (
    (MsgAction, 'PluginUp', 'Plugin Up', None, 2399142789), #SHORTCUT_PLGUP
    (MsgAction, 'PluginDown', 'Plugin Down', None, 2399142790), #SHORTCUT_PLGDN
    (MsgAction, 'PluginLeft', 'Plugin Left', None, 2399142791), #SHORTCUT_PLGLEFT
    (MsgAction, 'PluginRight', 'Plugin Right', None, 2399142792), #SHORTCUT_PLGRIGHT
    (MsgAction, 'PluginPageUp', 'Plugin Page Up', None, 2399142793), #SHORTCUT_PLGPGUP
    (MsgAction, 'PluginPageDown', 'Plugin Page Down', None, 2399142794), #SHORTCUT_PLGPGDN
    (MsgAction, 'PluginSelect', 'Plugin Select', None, 2399142795), #SHORTCUT_PLGSEL
    (MsgAction, 'PluginAlternateSelect', 'Plugin Alternate Select', None, 2399142796), #SHORTCUT_PLGALTSEL
    (MsgAction, 'PluginCancel', 'Plugin Cancel', None, 2399142797), #SHORTCUT_PLGCANCEL
    (MsgAction, 'PluginTab', 'Plugin Tab', None, 2399142798), #SHORTCUT_PLGTAB
  )
),
(eg.ActionGroup, 'GroupStartMode', 'Start MyTheatre', None,
  (
    (ExeAction, 'StartLiveMode', 'Start in Live Mode', None, '/remote F9'),
    (ExeAction, 'StartDvdMode', 'Start in DVD Mode', None, '/dvd'),
    (ExeAction, 'StartFileMode', 'Start in File Mode', None, '/remote F10'),
  )
),
)


class MyTheatre(eg.PluginClass):

    def __init__(self):
        self.AddActionsFromList(MyActionList)


    def __start__(self):
        try:
            key = _winreg.OpenKey(
                _winreg.HKEY_LOCAL_MACHINE,
                "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\MyTheatre"
            )
            self.myTheatrePath, dummy = _winreg.QueryValueEx(key, "InstallLocation")
        except WindowsError:
            self.PrintError("MyTheatre installation path not found!")
            self.myTheatrePath = ""

