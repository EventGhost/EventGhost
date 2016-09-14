#!/usr/bin/env python
# -*- coding: UTF-8 -*-

PLUGIN_VERSION                       = "3.0.1"
SUPPORTED_DVBVIEWER_VERSIONS         = '4.9.x (older versions might work but are untested)'
SUPPORTED_RECORDING_SERVICE_VERSIONS = '1.10.x (older versions might work but are untested)'

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
#
# Version history (newest on top):
# 3.0.1: Debug log output reduced
#        Renamed GetRecordingIDs -> GetRecordingsIDs because of accidentally broken backward compatibility in 3.0.0
# 3.0.0: Improved stability and robustness by refactoring thread synchronisation and error handling.
#        - Fixed most situations of EG hangers when DVBViewer crashes
#        - Fixed most situations of error 'Lock released to prevent a dead lock' (some situations can't be fixed, like RS unavailable)
#        - EG no longer hangs at startup when DVBViewer recording service address is wrong / unavailable
#        - Fixed behavior in GetNumberOfActiveRecordings, GetRecordingsIDs, GetDateOfRecordings when RS is not enabled by plugin config.
#        - Fixed a lock timeout in case that system performs suspend just while WatchDogThread executes server requests.
#        Added action DeleteRecordings
#        - supposed to implement an automated housekeeping
#        Added action GetRecordingDetails
#        Added action IsDVBViewerProcessRunning
#        Added action WaitUntilPluginIdle
#        - supposed to be called before suspend
#        Added action GetCurrentShowDetails
#        - provides details about what is currently shown in DVBViewer
#        Added action GetDataManagerValues
#        - provides all available information of DVBViewer's data manager
#        Added event 'DVBViewer.SevereError.WMI' - triggered on exceptions in WMI
#        Added event 'DVBViewer.SevereError.LockTimeout' - triggered on dead locks / lock timeouts
#        Added event 'DVBViewer.SevereError.COM' - triggered on COM initialization errors
#        Added event 'DVBViewer.SevereError.Connect' - triggered on connection errors between EG and DVBV (replaces earlier DVBViewerCouldNotBeConnected event)
#        Suppress repeated identical events like 'DVBViewer.ControlChange (603, 0)'
#        Grouped and reorderded all actions, put them into subfolders; improved action names and descriptions
#        Plugin config: auto correct os path to dvbviewer.exe while opening plugin config and start plugin
#        Updated plugin documentation (HTML help)
#        Updated source documentation of main classes and methods
#        Many other refactorings and minor improvements
# 2.1.2: Fixed Unicode problem in GetChannelDetails;
#        channel names with special characters or umlauts caused an exception.
# 2.1.1: Documentation and exception handling improved (minor changes)
#        Return type of GetChannelDetails is now always a dictionary with the channelID as key.
# 2.1.0: Added action GetTimerDetails
#        Added action TuneChannel
#        Added action GetChannelDetails
#        Improved creation of channelIDs: generate 64 bit IDs (new format introduced in 2011)
#        Extracted help into separate html file
#        Some Eclipse (IDE) warnings fixed

import eg
from os.path import join, dirname, abspath, isfile
import codecs

HELPFILE = abspath(join(dirname(__file__.decode('mbcs')), "DVBViewer-Help.html"))

def GetHelp():
    try:
        f = codecs.open(HELPFILE, mode="r", encoding="latin_1", buffering=-1)
        hlp = f.read()
        f.close()
        hlp = hlp % (PLUGIN_VERSION, SUPPORTED_DVBVIEWER_VERSIONS, SUPPORTED_RECORDING_SERVICE_VERSIONS)
        return hlp
    except Exception, exc:
        msg = "Error reading help file " + HELPFILE + ", error=" + unicode(exc)
        eg.PrintTraceback(msg)
        return msg

HELP = GetHelp()

eg.RegisterPlugin(
    name = "DVBViewer",
    author = (
        "Bitmonster",
        "Stefan Gollmer",
        "Nativityplay",
        "Daniel Brugger",
    ),
    version = PLUGIN_VERSION,
    kind = "program",
    guid = "{747B54F6-59F6-4602-A777-984EA76D2D8C}",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1564",
    description = (
        'Adds support functions to control <a href="http://www.dvbviewer.com/">'
        'DVBViewer Pro/GE and DVBViewerService</a> and returns events.'
    ),
    help = HELP,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADK0lEQVR42j2TXWgcVRTH"
        "f/fOzM5uNknJxvoRt6kaCwlBjFJRsIgasUFLH1KFCqIIBTHUh9aCRQTRPviSokiLFREh"
        "iCXRh5ZiH6TWj1KxUqG2xmKwSlsrtKFu0/2a2Ttzr2d2jXMZLveee875n//5H5XWz6C7"
        "RsAkoBU4D2qX5RyBys50vp4bIQjBJp07P0/z2Guo+pGts0oXB12SSgAtFnFKY/lTnMpO"
        "qu3v/BxKS3CbZv5WezmdVs7OKTM/63SwEmctKk1wSYzqWYkq9uGCoty1cHEVV10UVGLL"
        "dclbI3sv8cIMKv7qbaOCknK1a+JUwhvbgOq9uZ01y71cgatfxf5xAvvXL6hCDzpfpPn3"
        "Yaean7/kqErEvjK58SnSS2exf/6IWxIewiL61lH80cdQXYJIVnpyjta3M3g3rcboc6jq"
        "9JjT9OLft5nk5EHSiz/j3/lg29ElEfb3H7CVSwQT2wkfmcIJP43pDbjLP2GHpdTrb/Q7"
        "nbsFe3VRspTIP7sXPXi3wCz9Rx+ScR/RJy8TbtpFOLETM/8lrY+fIh0eQNV2Dzn3T13g"
        "9otxB8nCMZIzh6G5hB4YJVy/E39sE+b0QZr7Jim+fgpdup1oz/2Yrqq08d3bnKsKu92r"
        "cDUh6so5/Hsm0eW1pAtHSOePkpt4hXDjNM0PnoBckcILnxF9NE6rcUoCvFd2RFpaZQXr"
        "ErnH3yRYt63DfAb/0HbM0XcobPseV7lA/MWrFHb8itn/JLGIUNXfX+VUrCSAKEzaWNhy"
        "XLJ0t/WgRW22sUhz95Cgeg5/ZCPxgRcJnzmAOfQ0JtdCNT4ccsoobBShewYIn/8a5YVY"
        "l7aV56LrxHuHpaQHUIPrpKQ5/LVbSb+ZwtxQRjVn7jUSQNlEZBxXCB7ehXfXZpa/5MQe"
        "zHdv4Y1MCkfZjIgqrUJHv9HK+4L+04ec8n1EDChnBXoL7471qNIa3JXTpOc7iAh7JcG1"
        "DjfyRncHmEbWhdlHZ5WrrrZkU9aOIi2stFWXDZcK+zpQRP/oYFncVvueTm3/fpHyuGRo"
        "YGVlk+dkZ+kiztQgv0IyleVOLNmEesH/3ZEAJPEK/gVNWWvcNcmGsgAAAABJRU5ErkJg"
        "gg=="
    ),
)


CALLWAIT_TIMEOUT  = 60.0
TERMINATE_TIMEOUT = 120
DUMMY_ACTION      = 27536
ACCOUNT_CHOICES   = ['DVBService','Task scheduler']
INDEX_DVBSERVICE  = ACCOUNT_CHOICES.index( 'DVBService' )
INDEX_SCHEDULER   = ACCOUNT_CHOICES.index( 'Task scheduler' )

UPDATE_TIMERS     = 1
UPDATE_STREAM     = 2
UPDATE_RECORDINGS = 4
UPDATE_ALL        = UPDATE_TIMERS | UPDATE_STREAM | UPDATE_RECORDINGS

#connectionMode:
WAIT_CHECK_START_CONNECT  = 0   #wait for free, check if executing, start if not executing, connect
CONNECT                   = 1   #connect
CHECK_CONNECT             = 2   #connect only, if executing

DVBVIEWER_WINDOWS = {
    2007: "SLIDESHOW",
    2000: "TELETEXT",
}

DVBVIEWER_CLOSE = ( "Close DVBViewer", 12326)

FIND_DVBVIEWER_PROCESS = 'select * from Win32_Process where Name="dvbviewer.exe"'

# Channel list properties
CH_1_NAME        = 1
CH_3_FLAGS       = 3
CH_4_TUNERTYPE   = 4
CH_5_FREQUENCY   = 5
CH_15_ORBITALPOS = 15
CH_20_AUDIOPID   = 20
CH_22_VIDEOPID   = 22
CH_23_TSID       = 23
CH_26_SID        = 26

# GetTimerList properties
TI_0_DESCRIPTION  = 0
TI_1_CHANNEL      = 1
TI_4_ID           = 4
TI_5_DATE         = 5
TI_6_STARTTIME    = 6
TI_7_ENDTIME      = 7
TI_8_ENABLED      = 8
TI_11_RECORDING   = 11
TI_15_DAYS        = 15
TI_18_TIMERACTION = 18

# Recording Entry properties
RE_RECID = 'recID'
RE_CHANNEL = 'channel'
RE_STARTDATE = 'startdate'
RE_DESCRIPTION = 'description'
RE_DURATION = 'duration'
RE_FILENAME = 'filename'
RE_PLAYED = 'played'
RE_TITLE = 'title'
RE_SERIES = 'series'
RE_FROMRS = 'fromRS'

EVENT_LIST = (
    ("Action",                          "Gets fired whenever a new action is processed"),
    ("Channel",                         "Gets fired on every channelchange"),
    ("AddRecord",                       "Gets fired whenever a new Timer is added"),
    ("TimerListUpdated",                "Gets fired whenever the timer list is changed. Watch dog must be enabled."),
    ("StartRecord",                     "Gets fired whenever a recording starts"),
    ("AllActiveRecordingsFinished",     "Gets fired whenever the last active recording finishs"),
    ("Window",                          "Gets fired whenever a OSD-window is activated"),
    ("ControlChange",                   "Gets fired whenever an OSD Control gets the focus"),
    ("SelectedItemChange",              "Gets fired whenever the selectedItem in an OSD list changes"),
    ("RDS",                             "Gets fired whenever a new RDS Text arrives"),
    ("Playlist",                        "Gets fired whenever a new playlistitem starts playing"),
    ("Playbackstart",                   "Gets fired whenever a media playback starts"),
    ("PlaybackEnd",                     "Gets fired whenever a media playback ends"),
    ("Close",                           "Gets fired when the DVBViewer is shutting down"),
    ("PlaystateChange",                 "Gets fired whenever the play state changes"),
    ("RatioChange",                     "Gets fired whenever the ratio changes"),
    ("DisplayChange",                   "Gets fired whenever the display type changes"),
    ("RenderPlaystateChange",           "Gets fired whenever the internal playstate changes"),
    ("RendererChange",                  "Gets fired whenever the renderer changes"),
    ("DVBViewerIsConnected",            "Gets fired whenever the DVBViewer is connected to the plugin"),
    ("DVBViewerCouldNotBeTerminated",   "Gets fired whenever the DVBViewer can't terminated by the plugin"),
    ("DVBViewerEventHandlingNotAlive",  "Gets fired whenever the plugin can't receive events from the DVBViewer" ),
    ("SevereError.WMI",                 "Gets fired when WMI is not available"),
    ("SevereError.LockTimeout",         "Gets fired when a lock timeout or deadlock occurs"),
    ("SevereError.COM",                 "Gets fired on COM initialization errors"),
    ("SevereError.Connect",             "Gets fired on connection errors between EG and DVBViewer"),
    ("Close",                           "Gets fired when the DVBViewer is shutting down"),
)


PGM_ACTIONS = (
    ("WindowMinimize",                   "WindowMinimize",                      None, (16382,True )),
    ("WindowRestore",                    "WindowRestore",                       None, (16397,True )),
    ("Fullscreen",                       "Fullscreen",                          None,     (5,True )),
    ("Screenshot",                       "Screenshot",                          None,   (115,True )),
    ("OnTop",                            "Window always On Top",                None,     (1,True )),
    ("HideMenu",                         "Toggle Menubar",                      None,     (2,True )),
    ("ShowStatusbar",                    "Toggle Statusbar",                    None,     (3,True )),
    ("TitlebarHide",                     "Toggle Window Frame",                 None,    (54,True )),
    ("Toolbar",                          "Toggle Toolbar",                      None,     (4,True )),
    ("HideAll",                          "Toggle Show / Hide All",              None,    (71,True )),

    ("Teletext",                         "Toggle Teletext window",              None,    (35,True )),
    ("EPG",                              "Toggle EPG window",                   None,    (37,True )),
    ("Options",                          "Show Options window",                 None,    (24,True )),

    ("ShutdownCard",                     "Shutdown Card",                       None, (12327,True )),
    ("ShutdownMonitor",                  "Shutdown Monitor",                    None, (12328,True )),
    ("Hibernate",                        "Hibernate",                           None, (12323,True )),
    ("Standby",                          "Standby",                             None, (12324,True )),
    ("Slumbermode",                      "Slumbermode",                         None, (12325,True )),
    ("Reboot",                           "Reboot",                              None, (12329,True )),
    ("Shutdown",                         "Shutdown",                            None, (12325,True )),
    ("Exit1",                            "Exit DVBViewer (method I)",           None,     (6,False)),  # ? see 12294?
    ("Exit2",                            "Exit DVBViewer (method II)",          None, (12294,False)),
)

TIMER_ACTIONS = (
    ("RecordSettings",                   "Show Recording dialog",               None,    (33,True )),
    ("Record",                           "Direct Recording",                    None,    (34,True )),
    ("TimeShift",                        "TimeShift Start",                     None,    (50,True )),
    ("TimeShiftWindow",                  "TimeShift Window",                    None,    (51,True )),
    ("TimeshiftStop",                    "Timeshift Stop",                      None,    (52,True )),
    ("KeepTimeshiftFile",                "Toggle keep Timeshift file",          None,  (2012,True )),
)

RECORDING_ACTIONS = (
    ("RecordedShowsAndTimerStatistics",  "Show Recordings window",              None,  (2011,True )),
    ("RefreshRecDB",                     "Refresh Recording DB",                None,  (8260,True )),
    ("CleanupRecDB",                     "Cleanup Recording DB",                None,  (8261,True )),
    ("CompressRecDB",                    "Compress Recording DB",               None,  (8262,True )),
    ("RefreshCleanupCompressRecDB",      "Refresh Cleanup Compress RecDB",      None,  (8263,True )),
)

CHANNEL_ACTIONS = (
    ("Channellist",                      "Channellist",                         None,     (7,True )),
    ("ChannelMinus",                     "Channel -",                           None,     (8,True )),
    ("ChannelPlus",                      "Channel +",                           None,     (9,True )),
    ("Channel0",                         "Channel 0",                           None,    (40,True )),
    ("Channel1",                         "Channel 1",                           None,    (41,True )),
    ("Channel2",                         "Channel 2",                           None,    (42,True )),
    ("Channel3",                         "Channel 3",                           None,    (43,True )),
    ("Channel4",                         "Channel 4",                           None,    (44,True )),
    ("Channel5",                         "Channel 5",                           None,    (45,True )),
    ("Channel6",                         "Channel 6",                           None,    (46,True )),
    ("Channel7",                         "Channel 7",                           None,    (47,True )),
    ("Channel8",                         "Channel 8",                           None,    (48,True )),
    ("Channel9",                         "Channel 9",                           None,    (49,True )),
    ("LastChannel",                      "Last Channel",                        None,    (63,True )),
    ("ClearChannelUsageCounter",         "Clear Channel usage counter",         None,  (8255,True )),
    ("ChannelScan",                      "ChannelScan",                         None,   (119,True )),
    ("ChannelEdit",                      "ChannelEdit",                         None,   (117,True )),
    ("ChannelSave",                      "Channel Save",                        None,    (10,True )),
    ("FavouritePlus",                    "Favourite +",                         None,    (20,True )),
    ("FavouriteMinus",                   "Favourite -",                         None,    (21,True )),
    ("Favourite0",                       "Favourite 0",                         None,    (38,True )),
    ("Favourite1",                       "Favourite 1",                         None,    (11,True )),
    ("Favourite2",                       "Favourite 2",                         None,    (12,True )),
    ("Favourite3",                       "Favourite 3",                         None,    (13,True )),
    ("Favourite4",                       "Favourite 4",                         None,    (14,True )),
    ("Favourite5",                       "Favourite 5",                         None,    (15,True )),
    ("Favourite6",                       "Favourite 6",                         None,    (16,True )),
    ("Favourite7",                       "Favourite 7",                         None,    (17,True )),
    ("Favourite8",                       "Favourite 8",                         None,    (18,True )),
    ("Favourite9",                       "Favourite 9",                         None,    (19,True )),
)

OSD_ACTIONS = (
    ("OSDMenu",                          "OSD-Menu",                            None,   (111,True )),
    ("OSDLeft",                          "OSD-Left",                            None,  (2000,True )),
    ("OSDRight",                         "OSD-Right",                           None,  (2100,True )),
    ("OSDUp",                            "OSD-Up",                              None,    (78,True )),
    ("OSDDown",                          "OSD-Down",                            None,    (79,True )),
    ("OSDOK",                            "OSD-OK",                              None,    (73,True )),
    ("OSDRed",                           "OSD-Red",                             None,    (74,True )),
    ("OSDGreen",                         "OSD-Green",                           None,    (75,True )),
    ("OSDYellow",                        "OSD-Yellow",                          None,    (76,True )),
    ("OSDBlue",                          "OSD-Blue",                            None,    (77,True )),
    ("OSDFirst",                         "OSD-First",                           None,    (80,True )),
    ("OSDLast",                          "OSD-Last",                            None,    (81,True )),
    ("OSDPrevious",                      "OSD-Previous",                        None,    (82,True )),
    ("OSDNext",                          "OSD-Next",                            None,    (83,True )),
    ("OSDClose",                         "OSD-Close",                           None,    (84,True )),
    ("OSDPositioning",                   "OSD-Positioning",                     None,    (85,True )), #???
    ("OSDClock",                         "OSD-Clock",                           None,  (2010,True )),
    ("OSDShowHTPC",                      "OSD-Show HTPC",                       None,  (2110,True )),
    ("OSDBackgroundToggle",              "OSD-Background Toggle",               None,  (8194,True )),
    ("ToggleBackground",                 "OSD Toggle Background",               None, (12297,True )),
    ("OSDTeletext",                      "OSD-Teletext",                        None,   (101,True )),
    ("OSDShowTimer",                     "OSD-Show Timer",                      None,  (8195,True )),
    ("OSDShowRecordings",                "OSD-Show Recordings",                 None,  (8196,True )),
    ("OSDShowNow",                       "OSD-Show Now",                        None,  (8197,True )),
    ("OSDShowEPG",                       "OSD-Show EPG",                        None,  (8198,True )),
    ("OSDShowChannels",                  "OSD-Show Channels",                   None,  (8199,True )),
    ("OSDShowFavourites",                "OSD-Show Favourites",                 None,  (8200,True )),
    ("OSDShowTimeline",                  "OSD-Show Timeline",                   None,  (8201,True )),
    ("OSDShowSubtitlemenu",              "OSD-Show Subtitlemenu",               None,  (8247,True )),
    ("OSDShowAudiomenu",                 "OSD-Show Audiomenu",                  None,  (8248,True )),
    ("OSDShowPicture",                   "OSD-Show Picture",                    None,  (8202,True )),
    ("OSDShowMusic",                     "OSD-Show Music",                      None,  (8203,True )),
    ("OSDShowVideo",                     "OSD-Show Video",                      None,  (8204,True )),
    ("OSDShowNews",                      "OSD-Show News",                       None,  (8205,True )),
    ("OSDShowWeather",                   "OSD-Show Weather",                    None,  (8206,True )),
    ("OSDShowMiniepg",                   "OSD-Show Miniepg",                    None,  (8207,True )),
    ("OSDShowMusicPlaylist",             "OSD-Show Music playlist",             None,  (8208,True )),
    ("OSDShowVideoPlaylist",             "OSD-Show Video playlist",             None,  (8209,True )),
    ("OSDShowComputer",                  "OSD-Show Computer",                   None,  (8210,True )),
    ("OSDShowAlarms",                    "OSD-Show Alarms",                     None,  (8212,True )),
    ("ShowVersion",                      "OSD-Show Version",                    None, (16384,True )),
    ("ShowCurrentInfo",                  "OSD-Show Current Info",               None,  (8264,True )),
    ("ShowRadioList",                    "OSD-Show Radio List",                 None,  (8265,True )),
    ("OSDCAM",                           "OSD-CAM",                             None,  (8259,True )),
)

PLAY_ACTIONS = (
    ("Play",                             "Play",                                None,    (92,True )),
    ("Pause",                            "Pause",                               None,     (0,True )),
    ("Previous",                         "Previous",                            None,   (112,True )),
    ("Next",                             "Next",                                None,   (113,True )),
    ("Stop",                             "Stop",                                None,   (114,True )),
    ("JumpMinus10",                      "Jump Minus 10",                       None,   (102,True )),
    ("JumpPlus10",                       "Jump Plus 10",                        None,   (103,True )),
    ("Forward",                          "Forward",                             None, (12304,True )),
    ("Rewind",                           "Rewind",                              None, (12305,True )),
    ("SpeedUp",                          "Speed Up",                            None, (12382,True )),
    ("SpeedDown",                        "Speed Down",                          None, (12383,True )),
    ("Playlist",                         "Playlist",                            None,    (64,True )),
    ("PlaylistFirst",                    "Playlist First",                      None,    (65,True )),
    ("PlaylistNext",                     "Playlist Next",                       None,    (66,True )),
    ("PlaylistPrevious",                 "Playlist Previous",                   None,    (67,True )),
    ("PlaylistLoop",                     "Playlist Loop",                       None,    (68,True )),
    ("PlaylistStop",                     "Playlist Stop",                       None,    (69,True )),
    ("PlaylistRandom",                   "Playlist Random",                     None,    (70,True )),
    ("AddBookmark",                      "Add Bookmark",                        None, (12306,True )),
    ("ShowPlaylist",                     "Show Playlist",                       None, (12384,True )),
    ("OpenFile",                         "Open File",                           None,    (94,True )),
    ("LastFile",                         "Last File",                           None,   (118,True )),
    ("ShowHelp",                         "Show Help",                           None,  (8213,True )),
    ("PlayAudioCD",                      "Play AudioCD",                        None,  (8257,True )),
    ("PlayDVD",                          "Play DVD",                            None,  (8250,True )),
    ("EjectCD",                          "Eject CD",                            None, (12299,True )),
    ("DVDMenu",                          "DVD Menu",                            None,  (8246,True )),
)

VIDEO_AUDIO_ACTIONS = (
    ("RebuildGraph",                     "Rebuild Graph",                       None,    (53,True )),
    ("StopGraph",                        "Stop Graph",                          None, (16383,False)),
    ("StopRenderer",                     "Stop Renderer",                       None,  (8256,False)),
    ("TogglePreview",                    "Toggle Preview",                      None, (16395,True )),
    ("ToggleMosaicpreview",              "Toggle Mosaic preview",               None,  (8211,True )),
    ("Desktop",                          "Desktop",                             None,    (32,True )),
    ("PortalSelect",                     "Portal select",                       None,  (8254,True )),
    ("Display",                          "Show Display dialog",                 None,    (28,True )),
    ("Aspect",                           "Toggle Aspect Ratio",                 None,    (22,True )),
    ("BestWidth",                        "Set Best Window Width",               None,    (89,True )),
    ("BrightnessUp",                     "Brightness Up",                       None,    (55,True )),
    ("BrightnessDown",                   "Brightness Down",                     None,    (56,True )),
    ("SaturationUp",                     "Saturation Up",                       None,    (57,True )),
    ("SaturationDown",                   "Saturation Down",                     None,    (58,True )),
    ("ContrastUp",                       "Contrast Up",                         None,    (59,True )),
    ("ContrastDown",                     "Contrast Down",                       None,    (60,True )),
    ("HueUp",                            "Hue Up",                              None,    (61,True )),
    ("HueDown",                          "Hue Down",                            None,    (62,True )),
    ("RestoreDefaultColors",             "Restore Default Colors",              None, (16396,True )),
    ("ShowVideowindow",                  "Show Video window",                   None,   (821,True )),
    ("HideVideowindow",                  "Hide Video window",                   None,  (8214,True )),

    ("Mute",                             "Toggle Mute",                         None,    (25,True )),
    ("VolumeUp",                         "Volume Up",                           None,    (26,True )),
    ("VolumeDown",                       "Volume Down",                         None,    (27,True )),
    ("AudioChannel",                     "Toggle Audio Channel",                None,    (72,True )),
    ("Equalizer",                        "Show Equalizer dialog",               None,   (116,True )),
    ("StereoLeftRight",                  "Stereo/Left/Right",                   None,    (95,True )),

    ("DisableAudio",                     "Disable Audio",                       None, (16385,True )),
    ("DisableAudioVideo",                "Disable AudioVideo",                  None, (16386,True )),
    ("DisableVideo",                     "Disable Video",                       None, (16387,True )),
    ("EnableAudioVideo",                 "Enable AudioVideo",                   None, (16388,True )),
    ("VideoOutputAB",                    "Video Output A/B",                    None,   (132,True )),
    ("AudioOutputAB",                    "Audio Output A/B",                    None,   (133,True )),
    ("DVBSourceProperties",              "Show DVB Source Properties dialog",   None,   (134,True )),

    ("Zoom",                             "Show Zoom dialog",                    None,    (23,True )),
    ("Zoom50",                           "Zoom window 50%",                     None,    (29,True )),
    ("Zoom75",                           "Zoom window 75%",                     None,  (2013,True )),
    ("Zoom100",                          "Zoom window 100%",                    None,    (30,True )),
    ("Zoom200",                          "Zoom window 200%",                    None,    (31,True )),
    ("ZoomUp",                           "Zoom image Up",                       None,   (104,True )),
    ("ZoomDown",                         "Zoom image Down",                     None,   (105,True )),
    ("ZoomlevelStandard",                "Zoomlevel Standard",                  None, (16389,True )),
    ("Zoomlevel0",                       "Zoomlevel 0",                         None, (16390,True )),
    ("Zoomlevel1",                       "Zoomlevel 1",                         None, (16391,True )),
    ("Zoomlevel2",                       "Zoomlevel 2",                         None, (16392,True )),
    ("Zoomlevel3",                       "Zoomlevel 3",                         None, (16393,True )),
    ("ZoomlevelToggle",                  "Zoomlevel Toggle",                    None, (16394,True )),
    ("StretchHUp",                       "StretchH Up",                         None,   (106,True )),
    ("StretchHDown",                     "StretchH Down",                       None,   (107,True )),
    ("StretchVUp",                       "StretchV Up",                         None,   (108,True )),
    ("StretchVDown",                     "StretchV Down",                       None,   (109,True )),
    ("StretchReset",                     "Stretch Reset",                       None,   (110,True )),
)

RS_ACTIONS = (
    ("ServiceStandby",                   "Recording Service Standby",           None,  (8272,True )),
    ("ServiceHibernate",                 "Recording Service Hibernate",         None,  (8274,True )),
    ("ServiceShutdown",                  "Recording Service Shutdown",          None,  (8273,True )),
    ("ServiceWakeOnLAN",                 "Recording Service Wake on LAN",       None,  (8275,True )),
    ("ServiceGetEPG",                    "Recording Service Get EPG",           None,  (8276,True )),
)


import wx
import sys
import os
import random
import hashlib
import inspect
from pythoncom import CoInitialize, CoUninitialize
from pythoncom import CoCreateInstance, CLSCTX_INPROC_SERVER, IID_IPersistFile
from pywintypes import Time as PyTime
import wx.lib.masked as masked
from functools import partial
from copy import deepcopy as cpy
from win32com.client import Dispatch, DispatchWithEvents
from win32com.client.gencache import EnsureDispatch
from win32com.client import GetObject
from win32com.taskscheduler import taskscheduler
from eg.WinApi import SendMessageTimeout
from threading import Thread, Event, Timer, Lock
from time import time, strptime, mktime, ctime, strftime, localtime, asctime, sleep
from datetime import datetime as dt, timedelta as td
from eg.WinApi.Dynamic import (
    byref, sizeof, CreateProcess, WaitForSingleObject, FormatError,
    CloseHandle, create_unicode_buffer,
    STARTUPINFO, PROCESS_INFORMATION,
    CREATE_NEW_CONSOLE, STARTF_USESHOWWINDOW
)
from urllib2 import ( HTTPPasswordMgrWithDefaultRealm, HTTPPasswordMgr, HTTPBasicAuthHandler,
                      install_opener, urlopen, Request, build_opener
                    )
from urlparse import urlparse
from re import search as reSearch
from base64 import encodestring as encodestring64
from xml.etree import cElementTree as ElementTree
from tempfile import NamedTemporaryFile
from _winreg import OpenKey, QueryValue, CloseKey, HKEY_LOCAL_MACHINE, KEY_READ


class Text:
    interfaceBox          = "Interface API"
    useComApi             = "COM-API (for DVBViewer Pro)"
    useSendMessage        = "SendMessage-API (for DVBViewer GE)"
    eventType             = "Events"
    useOldEvents          = "Like version 1.2       "
    useNewEvents          = "New definitions       "
    eventFormat           = "Event format"
    playStateFormat       = "PlayState format"
    displayChangeFormat   = "DisplayChange format"
    long                  = "Long "
    short                 = "Short"
    dvbViewerStart        = "Start DVBViewer"
    useCommandLine        = "Through command line"
    dvbviewerFile         = "DVBViewer filepath: "
    dvbviewerArguments    = "Arguments: "
    waitTimeBeforeConnect = "Waiting time after detection of the window: "
    dvbviewerBox          = "Choose the DVBViewer"
    watchDog              = "Watch dog"
    useWatchDog           = "Enable"
    watchDogTime          = "Watch dog cycle time: "
    accountInfo           = "Account information"
    accountName           = "Account name: "
    password1             = "Password: "
    password2             = "Repeat password: "
    changePassword        = "Change password"
    taskSchedulerInfo     = "Task scheduler information"
    schedulerPrefix       = "Task name prefix: "
    schedulerEvent        = "Event: "
    schedulerLead         = "Lead time [min]: "
    scheduleAllRecordings = "All recordings"
    schedulerEntryHidden  = "Hidden"
    accountChoices        = ACCOUNT_CHOICES
    accountType           = "Account type: "
    serviceHeader         = "DVBViewerService"
    serviceEnable         = "Enable     "
    serviceAddress        = "Address and Web port"
    serviceEvent          = "Source event name"

    serviceDVBViewer      = "By DVBViewer"
    serviceDVBService     = "By DVBViewerService"
    serviceUpdate         = "Update from DVBViewerService"


    class Start :
        name = "Start DVBViewer"
        description = "Start DVBViewer through COM-API. For DVBViewer Pro only."

    class IsConnected :
        name = "Is DVBViewer running and connected"
        description = "Returns True if DVBViewer is running and the plugin is connected to DVBViewer's COM API."

    class IsDVBViewerProcessRunning :
        name = "Is dvbviewer.exe running"
        description = "Returns True if program 'dvbviewer.exe' is running"

    class CloseDVBViewer :
        name = DVBVIEWER_CLOSE[0]
        checkBoxText = "Wait until DVBViewer is terminated"

    class StopAllActiveRecordings :
        name = "Stop all active recording timers"
        description = "Remove all active recording timers from the timer list."

    class SendAction :
        name   = "Send generic action to DVBViewer"
        action = "Action ID: "

    class GetSetupValue :
        name = "Get a value from the setup.xml of DVBViewer"
        section = "Section: "
        setupName = "Name: "
        default = "Default: "

    class GetDateOfRecordings :
        name = "Get dates of next recording timers"
        description =   (
                            "Deprecated, will be removed in a future release - use GetTimerDetails instead. "
                            "Return the date(s) of the recording timers as a floating "
                            "point number expressed in seconds since the epoch, in UTC. "
                            "The date is negative if no recording is planed. "
                        )
        allDates = "Get dates of all recoding timers (otherwise: get date of next timer)"

    class GetRecordingsIDs :
        name   = "Get IDs of recording timers"
        description = "Returns a list of recording IDs"
        active = "Get only IDs of active recording timers"

    class IsRecording :
        name = "Is Recording"
        description = "Returns True if recording is ongoing"

    class GetNumberOfActiveRecordings :
        name = "Get number of active recordings"
        description = "Returns the number of currently ongoing recordings."

    class GetTimerDetails :
        name = "Get recording timer details"
        description = (
            "Returns a list of planned recording timer details."
        )
        allRecordings = "Get all recording timers (otherwise: just the next one)"
        enabled = "Skip disabled timers"
        active = "Get only currently active recording timers"

    class GetChannelDetails:
        name = "Get channel details"
        description = (
            "Get the details of one or all DVBViewer channels. The result is a data dictionary provided in 'eg.result'. "
            "The returned list items correspond to DVBViewer's COM API."
        )
        allChannelsDescr = "Get the details of all channels (full channel list)"
        currentChannelDescr = "Get the details of current channel"
        channelIDDescr = "Channel by ID (note that the channel list might be empty if DVBViewer is not running)"
        channelID = "Channel ID"
        fromVariableDescr = "Evaluate channelID from global variable"
        variableName = "Variable name"
        tvButton = "TV"
        radioButton = "Radio"
        allChannels = "All channels"
        currentChannel = "Current channel"

    class TuneChannel :
        name = "Tune to a channel"
        description =   (
            "Tunes to an arbitrary channel as designated with the given channelID. "
            "This action is mainly intended to be called by other actions or to be called by scripts. "
        )
        channelIDDescr = "Channel by ID (note that the channel list might be empty if DVBViewer is not running)"
        channelID = "Channel ID"
        fromVariableDescr = "Evaluate channelID from global variable"
        variableName = "Variable name"
        tvButton = "TV"
        radioButton = "Radio"

    class ShowWindow :
        name     = "Show specific OSD window"
        windowID = "WindowID"

    class ShowInfoinTVPic :
        name  = "Show OSD info bar in TV picture"
        text  = "Displayed message: "
        time  = "Timeinterval [s]: "
        force = "Start DVBViewer if not executing"

    class DeleteInfoinTVPic :
        name  = "Hide OSD info bar in TV picture"

    class UpdateEPG :
        name = "Update EPG"
        description =   (
                            "For updating, one channel change for each transponder/booklet "
                            "will be done. If a recording is active, the executing of the EPG "
                            "update will be delayed until the recording is finished. "
                        )
        disableAV             = "Disable AV"
        time  = "Time between channel change: "
        event = "Fired event after update finished: "

    class AddRecording :
        name = "Add a recording timer"
        description = (
                    'Add a recording timer . This action should '
                    'be used by scripts or other plugins. The configuration '
                    'tool is only for demonstration. '
                    'This command might not be supported in newer versions because '
                    'DVBViewer might not support functions which are necessary '
                    'for this macro in future. '
                    )

        source                = "Source"
        station               = "Station: "
        tvButton              = "TV"
        radioButton           = "Radio"
        recordingDate         = "Date"
        date                  = "Date of recording: "
        start                 = "Start time: "
        end                   = "End time: "
        days                  = ( "Mo","Tu", "We","Th","Fr","Sa","Su" )
        recordingDescription  = "Description: "
        disableAV             = "Disable AV"
        enabled               = "Enable recording"
        mode                  = "Mode: "
        recActionChoices      = ( "intern", "tune only",  "AudioPlugin", "Videoplugin" )
        afterRecording        = "After recording: "
        actionAfterRecChoices = ( "No action","PowerOff", "Standby", "Hibernate",
                                  "Close", "Playlist", "Slumbermode" )


    class TaskScheduler :
        name = "Update Windows task scheduler"
        description = (
                    'Add the DVBViewer timer list entries to the Windows task scheduler. '
                    'To use this feature, the account name and the password should be entered '
                    'in the configuration of the DVBViewer plugin. The password is written '
                    'encryped in the file "DVBViewerAccount.dat" located in the event ghost user '
                    'directory.'
                    )


    class GetNumberOfClients :
        name =          "Get the number of clients connected to the service"
        serviceUpdate = " Update from DVBViewerService"


    class IsEPGUpdating :
        name =          "Get the DVBViewerService EPG update status"
        serviceUpdate = " Update from DVBViewerService"


def toDateTime( dateP, timeP ) :
    temp = mktime( localtime(int(dateP)) ) + float( timeP ) * 60 * 60 * 24
    #print localtime( temp )
    return temp


def toTimerEntry(timerID, channelID, channelName, dateStr, startTimeStr, endTimeStr, startDateTime, endDateTime,
                 days, description, enabled, recording, action, fromRS):
        timerentry = {
            'timerID': str(timerID),
            'channelID': long(channelID),
            'channelName': unicode(channelName),
            'date': str(dateStr),
            'startTime': str(startTimeStr),
            'endTime': str(endTimeStr),
            'startDateTime': float(startDateTime),
            'endDateTime': float(endDateTime),
            'days': str(days),
            'description': unicode(description),
            'enabled': bool(enabled),
            'recording': bool(recording),
            'action': int(action),
            'fromRS': bool(fromRS)
        }
        #print "timerentry=", timerentry
        return timerentry


def toRecordingEntry(recID, channel, startDate, description, duration, filename, played, title, series, fromRS):
        recordingEntry = {
            RE_RECID:       int(recID),
            RE_CHANNEL:     unicode(channel),
            RE_STARTDATE:   startDate,
            #RE_DESCRIPTION: unicode(description),
            RE_DURATION:    duration,
            RE_FILENAME:    unicode(filename),
            RE_PLAYED:      played,
            RE_TITLE:       unicode(title),
            RE_SERIES:      unicode(series),
            RE_FROMRS:      bool(fromRS)
        }
        #print "recordingEntry=", recordingEntry
        return recordingEntry


@eg.LogItWithReturn
def WaitForDVBViewerWindow( timeout=60.0 ) :
    winmatcher = eg.WindowMatcher( u'dvbviewer.exe',
                          winName=u'DVB Viewer{*}',
                          includeInvisible=True,
                          timeout=timeout )
    return winmatcher()


class DVBViewer(eg.PluginClass):
    '''
    The DVBViewer plugin main class. Responsible for configuration, setup and runstate management of the plugin.
    One of the central points in the plugin class is 'Connect()' - see there
    A few other "hot spots" in the plugin:
    - DVBViewerWatchdogThread - background thread which monitors the dvbviewer.exe program state and initializes the DVBViewerWorkerThread
    - DVBViewerWorkerThread - a "standby thread". Connects to DVBViewer's COM API and provides all methods to be executed on COM.
    - ComEventHandler - handles events from DVBViewer and triggers EventGhost events from it
    - DVBViewerService - provides methods to access and manage information from Recording Service
    '''
    text = Text

    @eg.LogIt
    def __init__(self):
        self.AddEvents(*EVENT_LIST)

        group = self.AddGroup("DVBViewer program actions", "DVBViewer program management")
        group.AddAction(Start)
        group.AddAction(IsConnected)
        group.AddAction(IsDVBViewerProcessRunning)
        group.AddAction(GetNumberOfClients)
        group.AddAction(GetSetupValue)
        group.AddAction(GetDataManagerValues)
        group.AddAction(WaitUntilPluginIdle)
        group.AddAction(CloseDVBViewer)
        group.AddActionsFromList(PGM_ACTIONS, ActionPrototype)

        group = self.AddGroup("Timer actions", "Timer related actions")
        group.AddAction(GetTimerDetails)
        group.AddAction(AddRecording)
        group.AddAction(GetDateOfRecordings)
        group.AddAction(GetRecordingsIDs)
        group.AddAction(IsRecording)
        group.AddAction(GetNumberOfActiveRecordings)
        group.AddAction(StopAllActiveRecordings)
        group.AddAction(TaskScheduler)
        group.AddActionsFromList(TIMER_ACTIONS, ActionPrototype)

        group = self.AddGroup("Recording actions", "Recording related actions")
        group.AddAction(GetRecordingDetails)
        group.AddAction(DeleteRecordings)
        group.AddActionsFromList(RECORDING_ACTIONS, ActionPrototype)

        group = self.AddGroup("Channel actions", "Channel related actions")
        group.AddAction(GetChannelDetails)
        group.AddAction(TuneChannel)
        group.AddAction(GetCurrentShowDetails)
        group.AddActionsFromList(CHANNEL_ACTIONS, ActionPrototype)

        group = self.AddGroup("OSD actions", "OSD related actions")
        group.AddAction(ShowInfoinTVPic)
        group.AddAction(DeleteInfoinTVPic)
        group.AddAction(ShowWindow)
        group.AddActionsFromList(OSD_ACTIONS, ActionPrototype)

        group = self.AddGroup("Play actions", "Player related actions")
        group.AddActionsFromList(PLAY_ACTIONS, ActionPrototype)

        group = self.AddGroup("Video and audio actions", "Video and audio related actions")
        group.AddActionsFromList(VIDEO_AUDIO_ACTIONS, ActionPrototype)

        group = self.AddGroup("Various actions", "Various DVBViewer and Recording Service actions")
        group.AddAction(SendAction)
        group.AddAction(UpdateEPG)
        group.AddAction(IsEPGUpdating)
        group.AddActionsFromList(RS_ACTIONS, ActionPrototype)

        self.AddAction(GetDVBViewerObject, hidden = True)
        self.AddAction(ExecuteDVBViewerCommandViaCOM, hidden = True)

        # create a new subclass of the EventHandler with the ability to use
        # the plugin's TriggerEvent method
        class SubEventHandler(ComEventHandler):
            plugin = self
            TriggerEvent = self.TriggerEvent
        self.EventHandler = SubEventHandler

        self.workerThread    = None
        self.terminateThread = None
        self.watchDogThread  = None

        self.oldInterface = False
        self.newInterface = True
        self.startDVBViewerByCOM = False,
        self.pathDVBViewer = ""

        #new status variables
        self.DVBViewerStartedByCOM = False

        self.numberOfActiveTimers = 0
        self.actualWindowID = -1
        self.actualDisplayMode=""
        self.lastDisplayMode=""
        self.actualChannel = -1
        self.actualRendererType = 0
        self.lastRendererType = -1
        self.actualPlayState = "STOP"
        self.lastPlayState = ""
        self.playBackMode = "NONE"
        self.lastRatio   = -1
        self.actualRatio = -1

        self.tvChannels = []
        self.radioChannels = []
        self.channelIDbyIDList = {}
        self.IDbychannelIDList = {}
        self.channelDetailsList = {}

        self.frequencies = {}

        self.completeTimerInfo = []

        self.indexTV    = 0
        self.indexRadio = 0

        self.tuneEPGThread = None
        self.disableAV = False

        self.accounts  = self.HandlePasswordFile()
        if self.accounts is None or len( self.accounts ) != len( self.text.accountChoices ) :
            self.accounts  = [('','')]*len( self.text.accountChoices )

        self.key = []
        self.scheduledRecordings = []
        self.numberOfScheduledRecordings = -1

        self.updateRecordingsLock      = LockWithTimeout( self, "UpdateDVTimers" )
        self.updateDVTimer = None

        self.executionStatusChangeLock = LockWithTimeout( self, "ExecutionStatusChange" )
        self.lockedByTerminate = False

        def CheckEventHandlingTimeoutFunc(self) :
            self.checkEventHandlingLock.release()
            self.eventHandlingIsAlive = False
            eg.PrintDebugNotice("DVBViewer event handling not alive")
            self.TriggerEvent( "DVBViewerEventHandlingNotAlive" )
            return False

        # purpose of checkEventHandlingLock is just to TriggerEvent( "DVBViewerEventHandlingNotAlive" ) in case that event handling does not work
        self.checkEventHandlingLock = LockWithTimeout(self, "CheckEventHandling", partial(CheckEventHandlingTimeoutFunc, self))
        self.eventHandlingIsAlive = True

        def WaitForTerminationTimeoutFunc(self) :
            self.closeWaitLock.release()
            self.closeWaitActive = False
            self.timeout=True
            eg.PrintDebugNotice("DVBViewer could not be terminated")
            self.TriggerEvent( "DVBViewerCouldNotBeTerminated" )
            return False

        # purpose of closeWaitLock is just to TriggerEvent( "DVBViewerCouldNotBeTerminated" ) in case that DVBViewer does not terminate
        self.closeWaitLock    = LockWithTimeout(self, "CloseWait", partial(WaitForTerminationTimeoutFunc, self))
        self.closeWaitActive  = False
        self.timeout=False

        self.infoInTVPictimeout=0.0

        self.serviceInUse = LockWithTimeout( self, 'ServiceInUse', severeErrorEventOnTimeout=False )
        self.DVBViewerService = None
        self.useService = False



    @eg.LogItWithReturn
    def __start__(  self,
                    useSendMessage=False,
                    oldInterface=True,
                    newInterface=False,
                    startDVBViewerByCOM=False,
                    pathDVBViewer="",
                    argumentsDVBViewer="",
                    longDisplay=True,
                    shortDisplay=False,
                    longPlayState=True,
                    shortPlayState=False,
                    useService=False,
                    watchDogTime=60.0,
                    schedulerTaskNamePrefix="StartRecording",
                    schedulerEventName     ="StartRecording",
                    schedulerLeadTime      =3.0,
                    scheduleAllRecordings  =False,
                    schedulerEntryHidden   =False,
                    waitTimeBeforeConnect=5.0,
                    serviceAddress='127.0.0.1:80',
                    serviceEvent='DVBViewerService',
                    dummy=False
                    ) :

        eg.PrintDebugNotice("DVBViewer plugin " + PLUGIN_VERSION)

        pathDVBViewer = self.CheckGetDVBViewerPath(pathDVBViewer)

        if useSendMessage:
            self.SendCommand = self.SendCommandThroughSendMessage
        else:
            self.SendCommand = self.SendCommandThroughCOM
            self.watchDogThread = DVBViewerWatchDogThread( self, watchDogTime )
            self.watchDogThread.start()

        self.oldInterface = oldInterface
        self.newInterface = newInterface
        self.startDVBViewerByCOM   = startDVBViewerByCOM
        self.waitTimeBeforeConnect = waitTimeBeforeConnect
        self.pathDVBViewer         = eg.ParseString(pathDVBViewer)
        self.argumentsDVBViewer    = eg.ParseString(argumentsDVBViewer)
        self.longDisplayEvent      = longDisplay
        self.shortDisplayEvent     = shortDisplay
        self.longPlayStateEvent    = longPlayState
        self.shortPlayStateEvent   = shortPlayState

        self.schedulerTaskNamePrefix = schedulerTaskNamePrefix
        self.schedulerEventName      = schedulerEventName
        self.schedulerLeadTime       = schedulerLeadTime
        self.scheduleAllRecordings   = scheduleAllRecordings
        self.schedulerEntryHidden    = schedulerEntryHidden

        self.scheduledRecordings = []
        self.numberOfScheduledRecordings = -1

        self.firedRecordingsIDs = []

        eg.PrintDebugNotice( "DVBViewer plugin started on " + strftime("%d %b %Y %H:%M:%S", localtime() ))

        self.useService     = useService
        self.serviceAddress = serviceAddress
        self.serviceEvent   = serviceEvent

        if not self.useService :
            return True

        #DVBViewerService:
        self.service = DVBViewerService( self, serviceAddress = self.serviceAddress,
                                         account = self.accounts[INDEX_DVBSERVICE],
                                         serviceEvent = self.serviceEvent )
        return True


    @eg.LogItWithReturn
    def __stop__(self):
        # If watchDogThread has been paused, resume it again
        if self.watchDogThread is not None:
            self.watchDogThread.pauseEvent.set()

        # If the DVBViewer was started by the COM interface, the DVBViewer must be terminated before
        # stopping the DVBViewer Thread. Otherwise the DVBViewer is going into an endless loop.
        if self.tuneEPGThread is not None :
            self.tuneEPGThread.Finish()

        if self.watchDogThread is not None :
            self.watchDogThread.Finish()
            self.watchDogThread.join()
            self.watchDogThread = None

        self.executionStatusChangeLock.acquire( timeout=TERMINATE_TIMEOUT )
        if self.workerThread is not None :
            if self.DVBViewerStartedByCOM :
                self.executionStatusChangeLock.release()
                StopAllActiveRecordings()
                self.WaitForTermination( sendCloseCommand = True )
            else :
                if self.workerThread.Stop( TERMINATE_TIMEOUT ) :
                    eg.PrintError("Could not terminate DVBViewer thread")
                self.executionStatusChangeLock.release()
        else :
            self.executionStatusChangeLock.release()

        if self.DVBViewerService is not None :
            del self.DVBViewerService

        return True


    @eg.LogIt
    def OnComputerSuspend(self, suspendType):
        pass

    @eg.LogIt
    def OnComputerResume(self, suspendType):
        # If watchDogThread has been paused, resume it again
        if self.watchDogThread is not None:
            self.watchDogThread.pauseEvent.set()

    @eg.LogIt
    def DVBViewerIsFinished( self ) :
        self.UpdateDVTimers( lock = False )
        self.TriggerEvent( "Close" )
        if self.closeWaitActive :
            self.closeWaitActive = False
            self.closeWaitLock.release()
        self.checkEventHandlingLock.acquire( blocking = False )
        self.checkEventHandlingLock.release()
        return True


    @eg.LogIt
    def UpdateDisplayMode( self ) :
        windowID = self.actualWindowID
        if windowID in DVBVIEWER_WINDOWS :
            self.actualDisplayMode = DVBVIEWER_WINDOWS[ windowID ]
        elif windowID != -1 and windowID != 500 :
            self.actualDisplayMode="OSD"
        else :
            if self.actualChannel >= 0 :
                self.actualDisplayMode="TV"
            else :
                self.actualDisplayMode = self.playBackMode
        if self.lastDisplayMode != self.actualDisplayMode :
            self.lastDisplayMode = self.actualDisplayMode
            if self.longDisplayEvent :
                self.TriggerEvent( "DisplayChange:"+ self.actualDisplayMode, self.actualDisplayMode )
            if self.shortDisplayEvent :
                self.TriggerEvent( "DisplayChange", self.actualDisplayMode )
        return True


    @eg.LogIt
    def UpdateDVTimersByDVEvent( self ) :

        @eg.LogItWithReturn
        def UpdateDVTimers(self) :
            plugin = self
            plugin.updateRecordingsLock.acquire()
            plugin.updateDVTimer = None
            plugin.updateRecordingsLock.release()
            plugin.UpdateDVTimers()

        self.updateRecordingsLock.acquire()

        if self.updateDVTimer is not None :
            self.updateDVTimer.cancel()

        self.updateDVTimer = Timer( 1.1, self.UpdateDVTimers )  #A thread is necessary in case of a DVBViewer dead lock
        self.updateDVTimer.start()

        self.updateRecordingsLock.release()

        return True


    @eg.LogIt
    def UpdateDVTimers( self, lock=True, updateService=False ) :

        timerIDs = []
        completeTimerInfo = []

        updatedTimers = 0
        started = False

        try:
            if self.workerThread is not None :
                if lock:
                    self.executionStatusChangeLock.acquire()
                try:
                    completeTimerInfo = self.workerThread.CallWait(
                        partial(self.workerThread.GetTimers, False, updateService ),
                        CALLWAIT_TIMEOUT
                    )
                finally:
                    if lock:
                        self.executionStatusChangeLock.release()

                timerIDs = [ record[ TI_4_ID ] for record in completeTimerInfo if record[ TI_11_RECORDING ] ]
                started = True

            numberOfActiveTimers = len( timerIDs )

            newTimerIDs = [ ID for ID in timerIDs if ID not in self.firedRecordingsIDs ]
            #print "newTimerIDs = ", newTimerIDs


            if self.numberOfActiveTimers != numberOfActiveTimers or len( newTimerIDs ) != 0 :

                deletedTimerIDs = [ ( count, ID ) for count, ID in enumerate( self.firedRecordingsIDs ) if ID not in timerIDs ]
                #print "deletedTimerIDs = ", deletedTimerIDs
                #print "self.firedRecordingsIDs = ", self.firedRecordingsIDs

                removed = 0
                for v in deletedTimerIDs :
                    self.numberOfActiveTimers -= 1
                    if self.oldInterface :
                        self.TriggerEvent( "EndRecord" )
                    if self.newInterface :
                        self.TriggerEvent( "EndRecord", ( v[1], self.numberOfActiveTimers ) )
                    del self.firedRecordingsIDs[ v[0] - removed ]
                    removed += 1

                for ID in newTimerIDs :
                    self.numberOfActiveTimers += 1
                    if self.oldInterface :
                        self.TriggerEvent("StartRecord", str(ID) )
                    if self.newInterface :
                        self.TriggerEvent( "StartRecord", ( ID, self.numberOfActiveTimers ) )
                    self.firedRecordingsIDs.append( ID )

                newRecordings     = len( newTimerIDs )
                updatedTimers = newRecordings + removed

                if self.numberOfActiveTimers == 0 :
                    self.TriggerEvent( "AllActiveRecordingsFinished" )

            if started :
                if completeTimerInfo != self.completeTimerInfo :
                    self.TriggerEvent( "TimerListUpdated" )
                    self.completeTimerInfo = completeTimerInfo
        except Exception, exc:
            msg = 'Unexpected error: ' + unicode(exc)
            eg.PrintTraceback(msg)

        return updatedTimers


    @eg.LogIt
    def SendCommandThroughSendMessage(self, value, lock=True, connectionMode=WAIT_CHECK_START_CONNECT):
        try:
            hwnd = WaitForDVBViewerWindow()[0]
            return SendMessageTimeout(hwnd, 45762, 2069, 100 + value)
        except:
            raise self.Exceptions.ProgramNotRunning
        return True


    @eg.LogIt
    def SendCommandThroughCOM(self, value, lock=True, connectionMode=WAIT_CHECK_START_CONNECT ):
        executed = False
        if lock :
            self.executionStatusChangeLock.acquire()
        try:
            if self.Connect( connectionMode ) :
                self.workerThread.CallWait(
                    partial(self.workerThread.dvbviewer.SendCommand, value),
                    CALLWAIT_TIMEOUT
                )
                executed = True
        finally:
            if lock :
                self.executionStatusChangeLock.release()
        return executed


    #@eg.LogIt
    def IsDVBViewerProcessRunning(self, WMI=None, eventOnException=True):
        '''Checks if the dvbviewer.exe process is running'''
        wmiCreated = WMI is None
        if wmiCreated:
            try:
                WMI = None
                WMI = GetObject('winmgmts:')
            except Exception, exc:
                msg = 'Error getting WMI object: ' + unicode(exc)
                eg.PrintError(msg)
                if eventOnException:
                    self.TriggerEvent('SevereError.WMI', msg)
                del WMI
                return False

        running = False
        try:
            running = len( WMI.ExecQuery(FIND_DVBVIEWER_PROCESS) ) > 0
        except Exception, exc:
            msg = 'Error getting WMI process list' + unicode(exc)
            eg.PrintError(msg)
            if eventOnException:
                self.TriggerEvent('SevereError.WMI', msg)
            return False
        finally:
            if wmiCreated:
                del WMI

        return running


    @eg.LogIt
    def GetChannelLists( self, lock=True ) :

        def GetChannelList( rawlist, isTV, channelIDbyIDList, IDbychannelIDList, channelList ) :
            for ix in xrange( len(rawlist) ) :
                nr = ( ix, isTV )
                entry = rawlist[ix]
                channelID = str( entry[0] ) + '|' + entry[1]
                channelIDbyIDList[ nr ] = channelID
                IDbychannelIDList[ channelID ] = nr
                channelList.append( entry[1] )

        tvChannels = []
        radioChannels = []
        self.channelDetailsList = {}

        if lock:
            self.executionStatusChangeLock.acquire()
        try:
            rawlist = self.workerThread.CallWait( partial( self.workerThread.GetChannelList ), CALLWAIT_TIMEOUT )
        finally:
            if lock:
                self.executionStatusChangeLock.release()

        channelNr = 0
        for channel in rawlist[1] :
            tv = not ( channel[CH_22_VIDEOPID] == 0 )
            channelID = str(
                int(tv) << 61
                | channel[CH_15_ORBITALPOS] << 48
                | channel[CH_23_TSID] << 32
                | (channel[CH_4_TUNERTYPE] + 1) << 29
                | channel[CH_20_AUDIOPID] << 16
                | channel[CH_26_SID]
            )
            self.channelDetailsList[channelID] = channel

            if tv :
                tvChannels.append( ( channelID, channel[CH_1_NAME] ) )
            else :
                radioChannels.append( ( channelID, channel[CH_1_NAME] ) )
            if ( channel[ CH_3_FLAGS ] & 2 ) == 0 : # encrypted?
                if not self.frequencies.has_key( channel[CH_5_FREQUENCY] ) :
                    self.frequencies[ channel[CH_5_FREQUENCY] ] = ( channelNr, tv )
                elif not self.frequencies[ channel[CH_5_FREQUENCY] ][1] and tv :
                    self.frequencies[ channel[CH_5_FREQUENCY] ] = ( channelNr, tv )
            channelNr += 1

        radioChannels.sort( cmp=lambda x,y: cmp(x[CH_1_NAME].lower(), y[CH_1_NAME].lower()) )
        tvChannels.sort( cmp=lambda x,y: cmp(x[CH_1_NAME].lower(), y[CH_1_NAME].lower()) )

        GetChannelList( tvChannels, True, self.channelIDbyIDList, self.IDbychannelIDList, self.tvChannels )
        GetChannelList( radioChannels, False, self.channelIDbyIDList, self.IDbychannelIDList, self.radioChannels )

        #print "self.frequencies=", self.frequencies
        #print "self.channelIDbyIDList=", self.channelIDbyIDList
        #print "self.IDbychannelIDList=", self.IDbychannelIDList
        #print "self.tvChannels=", self.tvChannels

        return True


    @eg.LogIt
    def TuneChannelIfNotRecording( self, channelNr, text = "", time=0.0) :
        ret = False
        self.executionStatusChangeLock.acquire()
        try :
            if self.Connect( WAIT_CHECK_START_CONNECT ) :
                ret = self.workerThread.CallWait(
                        partial( self.workerThread.TuneChannelIfNotRecording, channelNr, text, time ),
                        CALLWAIT_TIMEOUT
                     )
        finally:
            self.executionStatusChangeLock.release()
        return ret


    @eg.LogItWithReturn
    def WaitForTermination( self, sendCloseCommand=False, block=True ) :

        self.executionStatusChangeLock.acquire()
        try:
            if block :
                self.closeWaitActive = True

            if sendCloseCommand :
                self.SendCommand( DVBVIEWER_CLOSE[1], lock=False )

            if block :
                self.closeWaitLock.acquire( timeout=TERMINATE_TIMEOUT )

            self.timeout = False

        finally:
            self.executionStatusChangeLock.release()

        if block :
            self.closeWaitLock.acquire()
            self.closeWaitLock.release()

        return not self.timeout


    @eg.LogIt #WithReturn
    def Connect( self, connectingMode=WAIT_CHECK_START_CONNECT, lock=False ):
        '''
        This is one of the key methods of the plugin. The method has three modes:
        # WAIT_CHECK_START_CONNECT  = 0   # check if executing, start if not executing, connect
        # CONNECT                   = 1   # connect to a running DVBViewer instance (only to be used by the watchdog thread)
        # CHECK_CONNECT             = 2   # check if executing, connect only if already executing

        So basically, the method searches for a running DVBViewer instance or starts a new one
        and then starts the worker thread which connects to the COM interface.

        The method returns None if not connected and (not None) if connected.
        '''

        self.closeWaitLock.acquire()
        self.closeWaitLock.release()

        if lock :
            self.executionStatusChangeLock.acquire()

        try:
            started = False

            if self.workerThread is None:
                timeout = 20.0
                if connectingMode in (CHECK_CONNECT, WAIT_CHECK_START_CONNECT):
                    if self.IsDVBViewerProcessRunning() :
                        self.DVBViewerStartedByCOM = False
                        #print "DVBViewer is executing"
                        started = True
                    elif connectingMode == WAIT_CHECK_START_CONNECT:
                        if not self.startDVBViewerByCOM :
                            startupInfo = STARTUPINFO()
                            startupInfo.cb = sizeof(STARTUPINFO)
                            startupInfo.dwFlags = STARTF_USESHOWWINDOW
                            startupInfo.wShowWindow = 1
                            processInformation = PROCESS_INFORMATION()
                            commandLine = create_unicode_buffer(
                                '"%s" %s' % (self.pathDVBViewer, self.argumentsDVBViewer)
                            )
                            res = CreateProcess(
                                    None,                   # lpApplicationName
                                    commandLine,            # lpCommandLine
                                    None,                   # lpProcessAttributes
                                    None,                   # lpThreadAttributes
                                    False,                  # bInheritHandles
                                    32|CREATE_NEW_CONSOLE,  # dwCreationFlags
                                    None,                   # lpEnvironment
                                    None,                   # lpCurrentDirectory
                                    startupInfo,            # lpStartupInfo
                                    processInformation      # lpProcessInformation
                                    )
                            CloseHandle(processInformation.hProcess)
                            CloseHandle(processInformation.hThread)
                            if res == 0 :
                                eg.PrintError( "DVBViewer couldn't started" )
                                return False
                            self.DVBViewerStartedByCOM = False
                            timeout = 60.0
                        else:
                            self.DVBViewerStartedByCOM = True
                        started = True
                    else:
                        started = False

                elif connectingMode == CONNECT:
                    self.DVBViewerStartedByCOM = False
                    started = True

                if started :
                    if not self.DVBViewerStartedByCOM :
                        found = len(WaitForDVBViewerWindow(timeout)) > 0
                        if not found:
                            eg.PrintError( "Warning: DVBViewer window not found. Hidden?" )
                            eg.PrintDebugNotice( "DVBViewer window not found. Hidden?" )
                        eg.Wait( self.waitTimeBeforeConnect )    #  necessary otherwise hang up
                    self.workerThread = DVBViewerWorkerThread(self)
                    try:
                        self.workerThread.Start( 60.0 )
                    except:
                        msg = "DVBViewer process running but couldn't be connected. Restart of DVBViewer is suggested."
                        self.TriggerEvent( "SevereError.Connect" )
                        eg.PrintError(msg)
                        eg.PrintDebugNotice( msg )
                        # cleanup! - essential in order to avoid that EG hangs!
                        self.workerThread.Stop()
                        del self.workerThread
                        self.workerThread = None
                        return False

                    if self.workerThread and len( self.tvChannels ) == 0 and len( self.radioChannels ) == 0 :
                        self.GetChannelLists(lock=False)
                        #print self.tvChannels
                        #print self.radioChannels

        finally:
            if lock :
                self.executionStatusChangeLock.release()

        return self.workerThread


    @eg.LogIt
    def InitAfterDVBViewerConnected( self ) :
        thread = self.workerThread
        self.actualChannel = thread.GetCurrentChannelNr()
        self.numberOfActiveTimers = 0
        self.firedRecordingsIDs = []
        self.actualWindowID = -1
        self.actualDisplayMode=""
        self.lastDisplayMode=""
        self.actualRendererType = 0
        self.lastRendererType = -1
        self.actualPlayState = "STOP"
        self.lastPlayState = ""
        self.lastRatio   = -1
        self.actualRatio = -1
        self.controlChangeData = None
        thread.ProcessMediaplayback()
        self.UpdateDisplayMode()
        self.eventHandlingIsAlive = True
        return True


    def ServiceConfigure(  self, enableDVBViewer=True, enableDVBService=False, updateDVBService=False, affirmed=True, panel=None ) :

        def onCheckBox( event ) :
            viewer  =  viewerCheckBoxCtrl.GetValue()
            service = serviceCheckBoxCtrl.GetValue()

            if viewer == False and service == False :
                viewerCheckBoxCtrl.SetValue(  not self.lastEnableDVBViewer )
                serviceCheckBoxCtrl.SetValue( not self.lastEnableDVBService )
            self.lastEnableDVBViewer  = viewerCheckBoxCtrl.GetValue()
            self.lastEnableDVBService = serviceCheckBoxCtrl.GetValue()
            event.Skip()

        def getFlags() :
            return viewerCheckBoxCtrl.GetValue(), serviceCheckBoxCtrl.GetValue(), updateCheckBoxCtrl.GetValue()

        if panel is None :
            panel = eg.ConfigPanel()

        text = self.text

        self.lastEnableDVBViewer  = enableDVBViewer
        self.lastEnableDVBService = enableDVBService

        viewerCheckBoxCtrl = wx.CheckBox(panel, -1, text.serviceDVBViewer)
        viewerCheckBoxCtrl.SetValue( enableDVBViewer )
        viewerCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onCheckBox)

        serviceCheckBoxCtrl = wx.CheckBox(panel, -1, text.serviceDVBService)
        serviceCheckBoxCtrl.SetValue( enableDVBService )
        serviceCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onCheckBox)

        updateCheckBoxCtrl = wx.CheckBox(panel, -1, text.serviceUpdate)
        updateCheckBoxCtrl.SetValue( updateDVBService )

        panel.sizer.Add( viewerCheckBoxCtrl )
        panel.sizer.Add(wx.Size(0,5))
        panel.sizer.Add( serviceCheckBoxCtrl )
        panel.sizer.Add(wx.Size(0,10))
        panel.sizer.Add( updateCheckBoxCtrl )


        if affirmed :
            while panel.Affirmed():

                panel.SetResult(
                                viewerCheckBoxCtrl.GetValue(),
                                serviceCheckBoxCtrl.GetValue(),
                                updateCheckBoxCtrl.GetValue()
                               )
        else :
            return getFlags


    def CheckGetDVBViewerPath(self, pathDVBViewer) :
        if pathDVBViewer is None:
            pathDVBViewer = ''
        else:
            pathDVBViewer = unicode(pathDVBViewer).strip()
            if pathDVBViewer != '' and (not os.path.isfile(pathDVBViewer) \
                                        or pathDVBViewer.lower().find('dvbviewer.exe') < 0):
                pathDVBViewer = ''

        if pathDVBViewer == '':
            try :
                regHandle = OpenKey(
                           HKEY_LOCAL_MACHINE,
                           'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths'
                        )
                pathDVBViewer = QueryValue(regHandle, 'dvbviewer.exe')
                CloseKey( regHandle )
            except :
                pass
        return pathDVBViewer


    @eg.LogIt
    def Configure(  self,
                    useSendMessage=False,
                    oldInterface=False,
                    newInterface=True,
                    startDVBViewerByCOM=False,
                    pathDVBViewer='',
                    argumentsDVBViewer="",
                    longDisplay=True,
                    shortDisplay=False,
                    longPlayState=True,
                    shortPlayState=False,
                    useService=False,
                    watchDogTime=60.0,
                    schedulerTaskNamePrefix="StartRecording",
                    schedulerEventName     ="StartRecording",
                    schedulerLeadTime      =3.0,
                    scheduleAllRecordings  =False,
                    schedulerEntryHidden   =False,
                    waitTimeBeforeConnect=5.0,
                    serviceAddress='127.0.0.1:8089',
                    serviceEvent='DVBViewerService',
                    dummy=False
                    ) :


        def onRadioBox( event ) :
            pro = radioBox.GetSelection() != 1
            for ctrl in enableControls :
                ctrl.Enable( pro )

            if pro :
                onCommandCheckBox(wx.CommandEvent())
                onPasswordChange(wx.CommandEvent())
                onServiceCheckBox(wx.CommandEvent())

            event.Skip()


        def onEventCheckBox( event ) :
            old = oldEventsCheckBoxCtrl.GetValue()
            new = newEventsCheckBoxCtrl.GetValue()
            if not old and not new :
                old = not self.lastOld
                new = not self.lastNew
                oldEventsCheckBoxCtrl.SetValue(old)
                newEventsCheckBoxCtrl.SetValue(new)
            self.lastOld = old
            self.lastNew = new
            event.Skip()


        def onCommandCheckBox( event ) :
            enable = useCommandCheckBoxCtrl.GetValue()
            dvbviewerFileCtrl.Enable( enable )
            argumentsCtrl.Enable( enable )
            event.Skip()


        def onServiceCheckBox( event ) :
            enable = serviceCheckBoxCtrl.GetValue()
            serviceAddressCtrl.Enable( enable )
            serviceEventCtrl.Enable( enable )
            index = INDEX_SCHEDULER
            if enable :
                index = INDEX_DVBSERVICE
            onPasswordChange(wx.CommandEvent(), index)
            event.Skip()


        def onAccountTypeChange( event ) :
            accountTypeIndex = text.accountChoices.index( accountTypeCtrl.GetValue() )

            if self.lastAccountTypeIndex >= 0 :
                self.accounts[ self.lastAccountTypeIndex ]  = ( accountCtrl.GetValue(), password1Ctrl.GetValue())

            accountCtrl.SetValue( self.accounts[ accountTypeIndex ][0] )
            password1Ctrl.SetValue( self.accounts[ accountTypeIndex ][1] )
            password2Ctrl.SetValue( self.accounts[ accountTypeIndex ][1] )

            self.lastAccountTypeIndex = accountTypeIndex
            #event.Skip()


        def onPasswordChange( event, forceAccount=-1 ) :
            p1 = password1Ctrl.GetValue()
            p2 = password2Ctrl.GetValue()
            enable = ( p1 == p2 )
            panel.EnableButtons( enable )
            accountTypeCtrl.Enable( enable )
            if enable and forceAccount >= 0 :
                accountTypeCtrl.SetValue( text.accountChoices[forceAccount] )
                onAccountTypeChange(wx.CommandEvent())
            event.Skip()

        self.lastOld = oldInterface
        self.lastNew = newInterface
        self.lastPlayStateLong  = longPlayState
        self.lastPlayStateShort = shortPlayState
        self.lastDisplayLong    = longDisplay
        self.lastDisplayShort = shortDisplay

        pathDVBViewer = self.CheckGetDVBViewerPath(pathDVBViewer)

        enableControls = []

        text = self.text
        panel = eg.ConfigPanel()
        radioBox = wx.RadioBox(
            panel,
            -1,
            text.interfaceBox,
            choices=[text.useComApi, text.useSendMessage],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(int(useSendMessage))
        radioBox.Bind(wx.EVT_RADIOBOX, onRadioBox)

        watchDogTimeCtrl = panel.SpinNumCtrl(watchDogTime, min=0, max=999, fractionWidth=0, integerWidth=3)
        enableControls.append( watchDogTimeCtrl )

        oldEventsCheckBoxCtrl = wx.CheckBox(panel, -1, text.useOldEvents)
        oldEventsCheckBoxCtrl.SetValue( oldInterface )
        oldEventsCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onEventCheckBox)
        enableControls.append( oldEventsCheckBoxCtrl )

        newEventsCheckBoxCtrl = wx.CheckBox(panel, -1, text.useNewEvents)
        newEventsCheckBoxCtrl.SetValue( newInterface )
        newEventsCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onEventCheckBox)
        enableControls.append( newEventsCheckBoxCtrl )

        longDisplayCheckBoxCtrl = wx.CheckBox(panel, -1, text.long)
        longDisplayCheckBoxCtrl.SetValue( longDisplay )
        enableControls.append( longDisplayCheckBoxCtrl )

        shortDisplayCheckBoxCtrl = wx.CheckBox(panel, -1, text.short)
        shortDisplayCheckBoxCtrl.SetValue( shortDisplay )
        enableControls.append( shortDisplayCheckBoxCtrl )

        longPlayStateCheckBoxCtrl = wx.CheckBox(panel, -1, text.long)
        longPlayStateCheckBoxCtrl.SetValue( longPlayState )
        enableControls.append( longPlayStateCheckBoxCtrl )

        shortPlayStateCheckBoxCtrl = wx.CheckBox(panel, -1, text.short)
        shortPlayStateCheckBoxCtrl.SetValue( shortPlayState )
        enableControls.append( shortPlayStateCheckBoxCtrl )

        useCommandCheckBoxCtrl = wx.CheckBox(panel, -1, text.useCommandLine)
        useCommandCheckBoxCtrl.SetValue( not startDVBViewerByCOM )
        #useCommandCheckBoxCtrl.SetValue( True )
        #useCommandCheckBoxCtrl.Enable(False)
        useCommandCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onCommandCheckBox)
        enableControls.append( useCommandCheckBoxCtrl )

        dvbviewerFileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            size=(320,-1),
            initialValue=pathDVBViewer,
            labelText="",
            fileMask="*.exe",
            dialogTitle=text.dvbviewerBox
        )
        enableControls.append( dvbviewerFileCtrl )

        argumentsCtrl = wx.TextCtrl( panel, size=(200,-1) )
        argumentsCtrl.SetValue( argumentsDVBViewer )
        enableControls.append( argumentsCtrl )

        waitTimeBeforeConnectCtrl = panel.SpinNumCtrl(waitTimeBeforeConnect, min=0, max=99, fractionWidth=0, integerWidth=2)
        waitTimeBeforeConnectCtrl.Enable( not startDVBViewerByCOM )
        enableControls.append( waitTimeBeforeConnectCtrl )

        serviceCheckBoxCtrl = wx.CheckBox(panel, -1, text.serviceEnable)
        serviceCheckBoxCtrl.SetValue( useService )
        serviceCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onServiceCheckBox)
        enableControls.append( serviceCheckBoxCtrl )

        serviceAddressCtrl = wx.TextCtrl( panel )#, size=(200,-1) )
        serviceAddressCtrl.SetValue( serviceAddress )
        enableControls.append( serviceAddressCtrl )

        serviceEventCtrl = wx.TextCtrl( panel , size=(150,-1) )
        serviceEventCtrl.SetValue( serviceEvent )
        enableControls.append( serviceEventCtrl )

        self.lastAccountTypeIndex = -1

        accountTypeCtrl = wx.ComboBox( panel,
                                    -1,
                                    value=text.accountChoices[INDEX_SCHEDULER],
                                    choices = text.accountChoices,
                                    style = wx.CB_READONLY
                                    )
        accountTypeCtrl.Bind(wx.EVT_COMBOBOX, onAccountTypeChange)
        enableControls.append( accountTypeCtrl )

        accountCtrl = wx.TextCtrl( panel, size=(125,-1) )
        enableControls.append( accountCtrl )

        password1Ctrl = wx.TextCtrl( panel, size=(125,-1), style=wx.TE_PASSWORD )
        password1Ctrl.Bind(wx.EVT_TEXT, onPasswordChange)
        enableControls.append( password1Ctrl )

        password2Ctrl = wx.TextCtrl( panel, size=(125,-1), style=wx.TE_PASSWORD )
        password2Ctrl.Bind(wx.EVT_TEXT, onPasswordChange)
        enableControls.append( password2Ctrl )

        schedulerPrefixCtrl = wx.TextCtrl( panel, size=(125,-1) )
        schedulerPrefixCtrl.SetValue( schedulerTaskNamePrefix )
        enableControls.append( schedulerPrefixCtrl )

        schedulerEventCtrl = wx.TextCtrl( panel, size=(125,-1) )
        schedulerEventCtrl.SetValue( schedulerEventName )
        enableControls.append( schedulerEventCtrl )

        schedulerLeadCtrl = panel.SpinNumCtrl(schedulerLeadTime, min=0, max=30, fractionWidth=0, integerWidth=2)
        enableControls.append( schedulerLeadCtrl )

        scheduleAllCheckBoxCtrl = wx.CheckBox(panel, -1, text.scheduleAllRecordings)
        scheduleAllCheckBoxCtrl.SetValue( scheduleAllRecordings )
        enableControls.append( scheduleAllCheckBoxCtrl )

        scheduleHiddenCheckBoxCtrl = wx.CheckBox(panel, -1, text.schedulerEntryHidden)
        scheduleHiddenCheckBoxCtrl.SetValue( schedulerEntryHidden )
        enableControls.append( scheduleHiddenCheckBoxCtrl )

        boxSizerO = wx.BoxSizer( wx.HORIZONTAL )
        boxSizerO.Add( radioBox, 1 )

        sb = wx.StaticBox( panel, -1, text.watchDog )
        boxSizerI = wx.StaticBoxSizer( sb, wx.VERTICAL )

        gridBagSizer = wx.GridBagSizer( 2, 10 )

        gridBagSizer.Add( wx.StaticText(panel, -1, text.watchDogTime), (0, 0), flag =  wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        gridBagSizer.Add( watchDogTimeCtrl,        (0, 1), flag =  wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        boxSizerI.Add(wx.Size(0,4))
        boxSizerI.Add( gridBagSizer )

        boxSizerO.Add( boxSizerI, 1, wx.EXPAND | wx.ALIGN_RIGHT )

        panel.sizer.Add(boxSizerO, 0, wx.EXPAND)

        panel.sizer.Add(wx.Size(0,2) )

        sb = wx.StaticBox( panel, -1, text.eventType )
        sBoxSizer = wx.StaticBoxSizer( sb, wx.HORIZONTAL )

        boxSizerI = wx.BoxSizer( wx.VERTICAL )
        boxSizerI.Add( oldEventsCheckBoxCtrl, 1, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        boxSizerI.Add( newEventsCheckBoxCtrl, 1, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sBoxSizer.Add( boxSizerI, 0, wx.EXPAND )


        boxSizerO = wx.BoxSizer( wx.HORIZONTAL )

        sb = wx.StaticBox( panel, -1, text.playStateFormat )
        boxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )
        boxSizer.Add(wx.Size(0,3))

        boxSizerI = wx.BoxSizer( wx.HORIZONTAL )
        boxSizerI.Add(longPlayStateCheckBoxCtrl, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        boxSizerI.Add(shortPlayStateCheckBoxCtrl, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        boxSizer.Add(boxSizerI, 1, wx.EXPAND )

        boxSizerO.Add( boxSizer, 1, wx.EXPAND )

        sb = wx.StaticBox( panel, -1, text.displayChangeFormat )
        boxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )
        boxSizer.Add(wx.Size(0,3))

        boxSizerI = wx.BoxSizer( wx.HORIZONTAL )
        boxSizerI.Add( longDisplayCheckBoxCtrl, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        boxSizerI.Add(shortDisplayCheckBoxCtrl, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        boxSizer.Add(boxSizerI, 1, wx.EXPAND )

        boxSizerO.Add( boxSizer, 1, wx.EXPAND )

        #gridSizer.Add(boxSizerO, (rowCount, 0 ), flag = wx.EXPAND, span = wx.GBSpan( 1, 2 ) )

        sBoxSizer.Add(boxSizerO, 1, wx.EXPAND)
        panel.sizer.Add(sBoxSizer, 0, wx.EXPAND)

        panel.sizer.Add(wx.Size(0,2))

        sb = wx.StaticBox( panel, -1, text.dvbViewerStart )
        boxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )

        #boxSizer.Add(wx.Size(0,3))

        sizer = wx.GridBagSizer( 0, 0 )

        sizer.Add( useCommandCheckBoxCtrl,                            (0,0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT )

        boxSizerI = wx.BoxSizer( wx.HORIZONTAL )
        boxSizerI.Add( wx.StaticText(panel, -1, text.waitTimeBeforeConnect), 0, wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT)
        boxSizerI.Add( waitTimeBeforeConnectCtrl, 1, wx.ALIGN_LEFT)

        sizer.Add( boxSizerI,                                         (0,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT )

        sizer.Add( wx.Size(0,2),                                      (1,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.dvbviewerFile),      (2,0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT )
        sizer.Add( dvbviewerFileCtrl,                                 (2,1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.Size(0,2),                                      (3,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.dvbviewerArguments), (4,0), flag= wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT )
        sizer.Add( argumentsCtrl,                                     (4,1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        boxSizer.Add( sizer, 1, wx.EXPAND)

        panel.sizer.Add(boxSizer, 0, wx.EXPAND)


        sb = wx.StaticBox( panel, -1, text.serviceHeader )
        boxSizer = wx.StaticBoxSizer( sb, wx.HORIZONTAL )

        boxSizer.Add( serviceCheckBoxCtrl, 0, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        boxSizerI = wx.BoxSizer( wx.VERTICAL )
        boxSizerI.Add( wx.StaticText(panel, -1, text.serviceAddress), 0, flag = wx.EXPAND | wx.ALIGN_BOTTOM )
        boxSizerI.Add( wx.Size(0,4) )
        boxSizerI.Add( serviceAddressCtrl                           , 1, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        boxSizer.Add( boxSizerI, 1 )
        boxSizer.Add( wx.Size(10,0) )

        boxSizerI = wx.BoxSizer( wx.VERTICAL )
        boxSizerI.Add( wx.StaticText(panel, -1, text.serviceEvent)  , 0, flag = wx.EXPAND | wx.ALIGN_BOTTOM )
        boxSizerI.Add( wx.Size(0,4) )
        boxSizerI.Add( serviceEventCtrl                             , 1, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        boxSizer.Add( boxSizerI, 0 )

        panel.sizer.Add(boxSizer, 0, wx.EXPAND)


        panel.sizer.Add(wx.Size(0,2))

        boxSizer = wx.BoxSizer( wx.HORIZONTAL )

        sb = wx.StaticBox( panel, -1, text.accountInfo )
        boxSizerI = wx.StaticBoxSizer( sb, wx.HORIZONTAL )

        sizer = wx.GridBagSizer( 0, 0 )

        sizer.Add(wx.Size(0,3),                                    (0,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.accountType),     (1,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( accountTypeCtrl,                                (1,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add(wx.Size(0,4),                                    (2,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.accountName),     (3,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( accountCtrl,                                    (3,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.password1),       (4,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( password1Ctrl,                                  (4,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.password2),       (5,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( password2Ctrl,                                  (5,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        boxSizerI.Add( sizer, 0, wx.EXPAND )
        boxSizer.Add( boxSizerI, 1, wx.EXPAND )


        sb = wx.StaticBox( panel, -1, text.taskSchedulerInfo )
        boxSizerI = wx.StaticBoxSizer( sb, wx.HORIZONTAL )
        sizer = wx.GridBagSizer( 0, 0 )

        sizer.Add(wx.Size(0,7),                                    (0,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( scheduleAllCheckBoxCtrl,                        (1,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        sizer.Add( scheduleHiddenCheckBoxCtrl,                     (1,1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add(wx.Size(0,7),                                    (2,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.schedulerPrefix), (3,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( schedulerPrefixCtrl,                            (3,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.schedulerEvent),  (4,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( schedulerEventCtrl,                             (4,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.schedulerLead),   (5,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( schedulerLeadCtrl,                              (5,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )


        boxSizerI.Add( sizer, 0, wx.EXPAND )
        boxSizer.Add( boxSizerI, 1, wx.EXPAND )

        panel.sizer.Add(boxSizer, 1, wx.EXPAND)

        onPasswordChange( wx.CommandEvent() )
        onAccountTypeChange( wx.CommandEvent() )
        onRadioBox( wx.CommandEvent() )

        while panel.Affirmed():
            useSendMessage        = radioBox.GetSelection() == 1
            oldInterface          = oldEventsCheckBoxCtrl.GetValue()
            newInterface          = newEventsCheckBoxCtrl.GetValue()
            startDVBViewerByCOM   = not useCommandCheckBoxCtrl.GetValue()
            argumentsDVBViewer    = argumentsCtrl.GetValue()
            pathDVBViewer         = dvbviewerFileCtrl.GetValue()
            waitTimeBeforeConnect = waitTimeBeforeConnectCtrl.GetValue()
            longDisplay           =  longDisplayCheckBoxCtrl.GetValue()
            shortDisplay          = shortDisplayCheckBoxCtrl.GetValue()
            longPlayState         =  longPlayStateCheckBoxCtrl.GetValue()
            shortPlayState        = shortPlayStateCheckBoxCtrl.GetValue()
            watchDogTime          = watchDogTimeCtrl.GetValue()

            useService            = serviceCheckBoxCtrl.GetValue()
            serviceAddress        = serviceAddressCtrl.GetValue()
            serviceEvent          = serviceEventCtrl.GetValue()

            schedulerTaskNamePrefix = schedulerPrefixCtrl.GetValue()
            schedulerEventName      = schedulerEventCtrl.GetValue()
            schedulerLeadTime       = schedulerLeadCtrl.GetValue()
            scheduleAllRecordings   = scheduleAllCheckBoxCtrl.GetValue()
            schedulerEntryHidden    = scheduleHiddenCheckBoxCtrl.GetValue()


            if accountCtrl.IsModified() or password1Ctrl.IsModified() :
                onAccountTypeChange( wx.CommandEvent() )
                self.HandlePasswordFile( write = True,accounts = self.accounts )
                dummy = not dummy

            if not oldInterface and not newInterface :
                newInterface = True

            panel.SetResult( useSendMessage,
                             oldInterface,
                             newInterface,
                             startDVBViewerByCOM,
                             pathDVBViewer,
                             argumentsDVBViewer,
                             longDisplay,
                             shortDisplay,
                             longPlayState,
                             shortPlayState,
                             useService,
                             watchDogTime,
                             schedulerTaskNamePrefix,
                             schedulerEventName,
                             schedulerLeadTime,
                             scheduleAllRecordings,
                             schedulerEntryHidden,
                             waitTimeBeforeConnect,
                             serviceAddress,
                             serviceEvent,
                             dummy
                           )



    def HandlePasswordFile( self, write=False, accounts=[('','')] ) :

        passwordFileName = os.path.join(eg.folderPath.RoamingAppData, eg.APP_NAME, 'DVBViewerAccount.dat')

        crypt = self.Crypt

        previousAccounts  = []

        if not write :
            tree = ElementTree.ElementTree()

            try:
                tree.parse( passwordFileName )
            except :
                previousAccounts  = None
            else :
                key = tree.find("Key").text

                for account in tree.findall("Account") :
                    accountName = account.get("Name","" )
                    passwordCrypted    = account.get("Password","" )
                    coded = "".join( [ chr(int(passwordCrypted[i:i+2],16)) for i in range(0,len(passwordCrypted),2) ] )
                    password = crypt( coded, key, False )
                    previousAccounts.append( ( accountName, password ) )

            return ( previousAccounts )

        key = ''
        for i in xrange(16):
            r = random.randint(0,255)
            key += '%02x'%r

        root = ElementTree.Element( 'Accounts' )

        subElement = ElementTree.Element( 'Key' )
        subElement.text = key
        root.append( subElement )

        for account in accounts :
            name = account[0]
            password = account[1]
            attributes = {}
            attributes['Name' ] = name
            attributes['Password' ] = "".join( ['%02x'%ord(c) for c in crypt( password, key, True ) ] )
            subElement = ElementTree.Element( 'Account', attributes )
            root.append( subElement )

        tree = ElementTree.ElementTree( root )
        tree.write(passwordFileName, sys.getdefaultencoding() )

        return True



    def Crypt( self, string, key, gen=True ) :
        m=hashlib.md5()
        m.update('37c710146322502a230dd8781ec3f5a')
        m.update(key)
        digest = m.digest()
        result = ''
        for index in xrange( len(string) ) :
            char = chr(ord(digest[index%16]) ^ ord(string[index]))
            modifier = char
            if gen :
                modifier = string[index]
            result += char
            m.update(modifier)
            digest = m.digest()

        #print result
        return result




class ComEventHandler:
    '''
    Handles all events from DVBViewer's COM interface
    '''

    def __init__( self ) :
        self.lastActiveChannelNr = -1


    # The event gets fired whenever a new action is processed.
    # Parameter :
    #       ActionID        ID of the action ( see actions.ini in the DVBViewer folder)
    #
    @eg.LogIt
    def OnonAction(self, ActionID):
        plugin = self.plugin
        plugin.eventHandlingIsAlive = True
        if ActionID == DUMMY_ACTION :
            plugin.checkEventHandlingLock.acquire( blocking = False )
            plugin.checkEventHandlingLock.release()
            return True

        if plugin.oldInterface :
            self.TriggerEvent("Action:" + str(ActionID))
        if plugin.newInterface :
            self.TriggerEvent("Action", ActionID )
        return True


    # The event gets fired on every channelchange.
    # Parameter :
    #       ChannelNr       The new channel number.
    #
    @eg.LogIt
    def OnChannelChange(self, ChannelNr):
        def DisableAV() :
            #print "DisableAV"
            #CoInitialize() # FIXME - I cannot imagine why CoInitialize should be needed here
            self.plugin.SendCommand( 16386 )
            #CoUninitialize()
        plugin = self.plugin
        plugin.eventHandlingIsAlive = True
        self.TriggerEvent("Channel", ChannelNr)
        plugin.actualChannel = ChannelNr
        plugin.UpdateDisplayMode()
        if ChannelNr != -1 :
            if plugin.disableAV :
                #print "DisableAV", ChannelNr
                disableAVTimer = Timer( 3.0, DisableAV )
                disableAVTimer.start()
            self.lastActiveChannelNr = ChannelNr
        return True


    # The event gets fired whenever a new Timer is added.
    # Parameter :
    #       ID              ID of the newly added timer.
    #
    @eg.LogIt
    def OnonAddRecord(self, ID):
        plugin = self.plugin
        plugin.eventHandlingIsAlive = True
        plugin.UpdateDVTimersByDVEvent()
        if plugin.oldInterface :
            self.TriggerEvent( "AddRecord:" + str(ID) )
        if plugin.newInterface :
            self.TriggerEvent( "AddRecord", ID )
        return True


    # The event gets fired whenever a recording starts.
    # Parameter :
    #       ID                          ID of the timer.
    #
    @eg.LogIt
    def OnonStartRecord(self, ID):
        self.plugin.eventHandlingIsAlive = True
        self.plugin.UpdateDVTimersByDVEvent()
        return True


    # The event gets fired whenever a recording ends.
    #
    @eg.LogIt
    def OnonEndRecord(self):
        self.plugin.eventHandlingIsAlive = True
        self.plugin.UpdateDVTimersByDVEvent()
        return True


    # The event gets fired whenever a OSD-window is activated.
    # Parameter :
    #       WindowID        ID of the OSD-window.
    #
    @eg.LogIt
    def OnonOSDWindow(self, WindowID):
        plugin = self.plugin
        plugin.eventHandlingIsAlive = True
        plugin.actualWindowID = WindowID
        if plugin.oldInterface :
            self.TriggerEvent("Window:" + str(WindowID))
        if plugin.newInterface :
            self.TriggerEvent("Window", WindowID )
        plugin.UpdateDisplayMode()
        return True


    # The event gets fired whenever an OSD Control gets the focus.
    # Parameters
    #       WindowID        ID of the OSD window the control belongs to.
    #       ControlID       ID of the OSD-control.
    #
    @eg.LogIt
    def OnonControlChange(self, WindowID, ControlID):
        plugin = self.plugin
        plugin.eventHandlingIsAlive = True
        controlChangeData = (WindowID, ControlID)
        if controlChangeData != plugin.controlChangeData:
            plugin.controlChangeData = controlChangeData
            if plugin.oldInterface :
                self.TriggerEvent("ControlChange:WindID" + str(WindowID) + "ContrID"+ str(ControlID))
            if plugin.newInterface :
                self.TriggerEvent("ControlChange", controlChangeData)
        return True


    # The event gets fired whenever the selectedItem in an OSD list changes.
    #
    @eg.LogIt
    def OnonSelectedItemChange(self):
        self.plugin.eventHandlingIsAlive = True
        self.TriggerEvent("SelectedItemChange")
        return True


    # The event gets fired whenever a new RDS Text arrives.
    # Parameters
    #       RDS             The RDS text.
    #
    @eg.LogIt
    def OnonRDS(self, RDS):
        plugin = self.plugin
        plugin.eventHandlingIsAlive = True
        if plugin.oldInterface :
            self.TriggerEvent("RDS:" + unicode(RDS))
        if plugin.newInterface :
            self.TriggerEvent("RDS", unicode(RDS))
        return True


    # The event gets fired whenever a new playlistitem starts playing.
    # Parameter :
    #       Filename        Filename of the starting playlistitem.
    #
    @eg.LogIt
    def OnonPlaylist(self, Filename):
        self.plugin.eventHandlingIsAlive = True
        self.TriggerEvent("Playlist", str(Filename))
        return True


    # The event gets fired whenever a media playback starts.
    #
    @eg.LogIt
    def OnonPlaybackstart(self):
        self.plugin.eventHandlingIsAlive = True
        thread = self.plugin.workerThread
        thread.Call( thread.ProcessMediaplayback )
        return True


    # The event gets fired whenever a media playback ends.
    #
    @eg.LogIt
    def OnPlaybackEnd(self):
        self.plugin.eventHandlingIsAlive = True
        thread = self.plugin.workerThread
        thread.Call( thread.ProcessMediaplayback )
        return True


    # The event gets fired whenever the internal playstate changes.
    # Parameter :
    #       RendererType    Type of renderer causing the event.
    #                       :=  0   Unknown
    #                       :=  1   VideoAudioDVD
    #                       :=  2   DVB
    #                       :=  3   MPG2TS
    #                       := -1   Ratio changed, state shows ratio
    #
    #       State           state changed into.
    #                       :=  0   Stop
    #                       :=  1   Pause
    #                       :=  2   Play
    #
    @eg.LogIt
    def OnPlaystatechange(self, RendererType, State):
        plugin = self.plugin
        plugin.eventHandlingIsAlive = True
        if plugin.oldInterface :
            self.TriggerEvent( "Playstatechange:RenderTy" + str(RendererType) + "State"+ str(State) )
        if plugin.newInterface :
            self.TriggerEvent( "RenderPlaystateChange", ( RendererType, State ) )
            pass
        if RendererType == -1 :
            plugin.actualRatio = State
            if plugin.lastRatio != plugin.actualRatio :
                plugin.lastRatio = plugin.actualRatio
                self.TriggerEvent( "RatioChange", State )
        else :
            plugin.actualRendererType = RendererType
            if plugin.lastRendererType != plugin.actualRendererType :
                plugin.lastRendererType = plugin.actualRendererType
                self.TriggerEvent( "RendererChange", plugin.actualRendererType )
                plugin.UpdateDisplayMode()
            if State == 2:
                plugin.actualPlayState = "PLAY"
            elif State == 1 :
                plugin.actualPlayState = "PAUSE"
            else :
                plugin.actualPlayState = "STOP"
            if plugin.lastPlayState != plugin.actualPlayState :
                plugin.lastPlayState = plugin.actualPlayState
                if plugin.longPlayStateEvent :
                    self.TriggerEvent( "PlaystateChange:"+plugin.actualPlayState, plugin.actualPlayState )
                if plugin.shortPlayStateEvent :
                    self.TriggerEvent( "PlaystateChange", plugin.actualPlayState )
        return True


    # The event gets fired when the DVBViewer is shutting down.
    @eg.LogIt
    def OnonDVBVClose(self):
        plugin = self.plugin

        plugin.lockedByTerminate = plugin.executionStatusChangeLock.acquire( blocking=False, timeout = TERMINATE_TIMEOUT )
        plugin.eventHandlingIsAlive = True

        if not plugin.closeWaitActive :
            plugin.closeWaitActive = True
            plugin.closeWaitLock.acquire( timeout=TERMINATE_TIMEOUT )

        plugin.terminateThread = DVBViewerTerminateThread( plugin )
        plugin.terminateThread.start()
        return True



class DVBViewerWorkerThread(eg.ThreadWorker):
    """
    This thread connects to DVBViewer's COM interface and performs all tasks related to this.
    It is started by the plugin.Connect() method which is called from the watchdog thread
    as soon as a running dvbviewer.exe instance is detected.
    This thread is kind of a 'standby thread' since it has no continuous task, but it waits for methods to be
    executed asynchronously.
    Other threads calling methods of this thread...
    - must acquire the 'ExecutionStatusChange' lock before the method call and release it afterwards
    - pack method calls into a worker.CallWait() or worker.Call() method to be executed in background.
    """

    @eg.LogItWithReturn
    def Setup(self, plugin):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin

        self.dvbviewer                 = None
        self.recordManager             = None
        self.comObj_IDVBViewerEvents   = None

        try:
            self.dvbviewer = EnsureDispatch("DVBViewerServer.DVBViewer")
            #self.dvbviewer = GetObject(Class="DVBViewerServer.DVBViewer")

            # try if we can get an attribute from the COM instance
            self.dvbviewer.CurrentChannelNr
            com_IDVBViewerEvents = self.dvbviewer.Events
            self.comObj_IDVBViewerEvents = DispatchWithEvents(com_IDVBViewerEvents, self.plugin.EventHandler)
            plugin.TriggerEvent( "DVBViewerIsConnected" )
            plugin.InitAfterDVBViewerConnected()
        except Exception, exc:
            msg = 'Failed to initialize COM interface: ' + unicode(exc)
            eg.PrintError(msg)
            eg.PrintDebugNotice(msg)
            plugin.TriggerEvent('SevereError.COM', msg)
            return False
        else:
            return True


    @eg.LogIt
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        if self.comObj_IDVBViewerEvents is not None :
            del self.comObj_IDVBViewerEvents
        if self.dvbviewer is not None:
            del self.dvbviewer
        self.plugin.workerThread = None
        return True


    @eg.LogItWithReturn
    def GetCurrentChannelNr( self ) :
        return self.dvbviewer.CurrentChannelNr


    @eg.LogItWithReturn
    def GetCurrentChannel( self ) :
        return self.dvbviewer.CurrentChannel


    @eg.LogItWithReturn
    def GetSetupValue( self, section, name, default ) :
        return self.dvbviewer.GetSetupValue( section, name, default )


    @eg.LogIt
    def GetChannelList( self ) :
        channelManager = self.dvbviewer.ChannelManager
        return channelManager.GetChannelList( )


    @eg.LogItWithReturn
    def GetChannelDetails(self, allChannels, currentChannel, channelID):
        result = None
        if allChannels:
            result = cpy(self.plugin.channelDetailsList) # return a deep copy, not the original
            channelID = None
        elif currentChannel:
            channelID = None
            channel = self.GetCurrentChannel()
            if channel:
                channelID = channel.ChannelID

        if channelID != None:
            try:
                channelID = unicode(channelID).split('|')[0]
                result = { channelID: cpy(self.plugin.channelDetailsList[channelID]) }
            except:
                eg.PrintError("No details for channel with ID '" + unicode(channelID) + "' found.")
                result = None

        return result


    @eg.LogIt
    def TuneChannel(self, channelID) :
        channelNr = self.dvbviewer.ChannelManager.GetNr(channelID)
        if channelNr >= 0:
            self.dvbviewer.CurrentChannelNr = channelNr
            return True
        else:
            eg.PrintError("Failed to tune channel with ID '" + str(channelID) + "'.")
            return False


    @eg.LogItWithReturn
    def TuneChannelIfNotRecording( self, channelNr, text="", time=0.0) :
        dvbviewer = self.dvbviewer
        timerCollection = dvbviewer.TimerManager

        if not timerCollection.Recording :
            dvbviewer.CurrentChannelNr = channelNr
            self.ShowInfoinTVPic( text, time + 2 )
            return True
        else :
            return False


    def ShowInfoinTVPic( self, text="", time=10.0 ) :
        dvbviewer = self.dvbviewer
        if text != "" :
            dvbviewer.OSD.ShowInfoinTVPic( text, time * 1000 )
        return True


    def ShowWindow( self, windowID ) :
        dvbviewer = self.dvbviewer
        dvbviewer.WindowManager.ShowWindow( windowID )
        return True


    @eg.LogIt
    def StopAllActiveRecordings( self ) :
        timerManager = self.dvbviewer.TimerManager
        timerlist = timerManager.GetTimerList( )
        for timer in timerlist[1] :
            #print "Record = ", timer
            #print "Recording: ", timer[ TI_11_RECORDING ]
            if timer[ TI_11_RECORDING ] :
                #print "Recording terminated"
                timerManager.StopRecording( timer[ TI_4_ID ] )
            else :
                #print "Recording not terminated"
                pass
        return True


    def IfMustInList( self, now, record, active, recordingsIDsService ) :
        """
        Returns True if timer is NOT in RS timer list and timer has not ended yet.
        """
        if record[ TI_4_ID ] not in recordingsIDsService :
            tStart = toDateTime( record[ TI_5_DATE ], record[ TI_6_STARTTIME ] )
            if tStart <= now :
                tStop  = toDateTime( record[ TI_5_DATE ], record[ TI_7_ENDTIME ] )
                if tStart > tStop :
                    tStop = tStop + 24*60*60
                if tStop <= now :
                    return False
            if active and not record[ TI_11_RECORDING ] :
                return False
            return True
        return False


    @eg.LogIt
    def GetTimers( self, active=True, update=False ) :
        plugin = self.plugin
        recordingsIDsService = {}
        if plugin.useService and self.GetSetupValue( 'Service', 'Timerlist', '0' ) != '0' :
            recordingsIDsService = plugin.service.GetPseudoIDs( update )

        timerlist = self.dvbviewer.TimerManager.GetTimerList()[1]
        now = time()
        recordinglist = [ record for record in timerlist if self.IfMustInList( now, record, active, recordingsIDsService ) ]
        #print "active = ", active, "  recordinglist = ", recordinglist
        return recordinglist


    @eg.LogIt
    def GetTimerIDs( self, active=True, update=False ) :
        plugin = self.plugin
        recordingsIDsService = {}
        if plugin.useService and self.GetSetupValue( 'Service', 'Timerlist', '0' ) != '0' :
            recordingsIDsService = plugin.service.GetPseudoIDs( update )

        timerlist = self.dvbviewer.TimerManager.GetTimerList()[1]
        now = time()
        IDs = [ record[ TI_4_ID ] for record in timerlist if self.IfMustInList( now, record, active, recordingsIDsService ) ]
        return IDs

    @eg.LogIt
    def GetRecordings(self) :
        recordings = {}
        recMgr = self.dvbviewer.RecordManager
        if recMgr is not None:
            count = recMgr.Count
            for i in range(count):
                item = recMgr.Items(i)
                dtDate = dt.fromtimestamp(int(item.Date))
                timeInSecs = float(item.Duration) * 60 * 60 * 24
                dtDuration = td( seconds = timeInSecs ) # timedelta
                entry = toRecordingEntry(
                    recID = item.recID,
                    channel = item.Channel,
                    startDate = dtDate,
                    description = item.Description,
                    duration = dtDuration,
                    filename = item.Filename,
                    played = item.Played,
                    title = item.Title,
                    series = "",
                    fromRS = False)
                recordings[entry[RE_RECID]] = entry
        return recordings

    @eg.LogIt
    def DeleteRecording(self, recID) :
        recMgr = self.dvbviewer.RecordManager
        if recMgr is not None:
            recMgr.DeleteEntry(recID)


    def ProcessMediaplayback( self ) :
        plugin = self.plugin
        last = plugin.playBackMode
        playBackIsStarted = self.dvbviewer.isMediaplayback()
        isDVD = self.dvbviewer.isDVD()
        if not playBackIsStarted :
            plugin.playBackMode = "NONE"
        elif isDVD :
            plugin.playBackMode = "DVD"
        else :
            plugin.playBackMode = "MEDIA"

        if last != plugin.playBackMode :
            if plugin.playBackMode != "NONE" :
                plugin.TriggerEvent("Playbackstart")
                plugin.UpdateDisplayMode()
            else :
                plugin.TriggerEvent("PlaybackEnd")
                plugin.UpdateDisplayMode()
        return True


    def IsDVD( self ) :
        return self.dvbviewer.isDVD


    @eg.LogIt
    def AddTimer( self,
        channelID,
        date,                 # dd.mm.yyyy
        startTime,            # hh:mm
        endTime,              # hh:mm
        description="",
        disableAV=False,
        enabled=True,
        recAction=0,          # intern = 0, tune only = 1,
                              # AudioPlugin = 2, Videoplugin = 3

        actionAfterRec=0,     # No action = 0, PowerOff = 1,
                              # Standby = 2, Hibernate = 3, Close = 4,
                              # Playlist = 5, Slumbermode: = 6
        days="-------"
    ) :
        pDate  = PyTime( strptime( date, "%d.%m.%Y" ) )
        pStart = PyTime( strptime( startTime, "%H:%M" ) ) #- PyTime( strptime( "00:00", "%H:%M" ) )
        pEnd   = PyTime( strptime( endTime,   "%H:%M" ) ) #- PyTime( strptime( "00:00", "%H:%M" ) )
        #count = self.dvbviewer.TimerManager.Count
        try :
            self.dvbviewer.TimerManager.AddItem( channelID, pDate, pStart, pEnd,
                                                 description, disableAV, enabled,
                                                 recAction, actionAfterRec, days )
        except :
            pass        #in case of "this is deprecated and will go away on"

        return True


    @eg.LogIt
    def GetCurrentShowDetails(self) :
        dataDict = {}
        dataDict['mode'] = self.plugin.actualDisplayMode
        if self.plugin.actualDisplayMode == 'TV':
            dataDict['title'] = self.DataManagerGetValue('#TV.Now.title')
            dataDict['channel'] = self.DataManagerGetValue('#channelname')
            dataDict['description'] = self.DataManagerGetValue('#TV.Now.description')
            dataDict['starttime'] = self.DataManagerGetValue('#TV.Now.start')
            dataDict['endtime'] = self.DataManagerGetValue('#TV.Now.stop')
            dataDict['duration'] = self.DataManagerGetValue('#TV.Now.duration')
            dataDict['remaining'] = self.DataManagerGetValue('#TV.Now.remain')
        elif self.plugin.actualDisplayMode == 'MEDIA':
            dataDict['title'] = self.DataManagerGetValue('#Media.title')
            dataDict['channel'] = self.DataManagerGetValue('#Media.Artist')
            dataDict['description'] = ''
            dataDict['starttime'] = ''
            dataDict['endtime'] = ''
            dataDict['duration'] = self.DataManagerGetValue('#duration')
            dataDict['remaining'] = self.DataManagerGetValue('#remain')
        elif self.plugin.actualDisplayMode == 'DVD':
            dataDict['title'] = self.DataManagerGetValue('#MR.MediaTitle')
            dataDict['channel'] = ''
            dataDict['description'] = ''
            dataDict['starttime'] = ''
            dataDict['endtime'] = ''
            dataDict['duration'] = self.DataManagerGetValue('#duration')
            dataDict['remaining'] = self.DataManagerGetValue('#remain')
        else:
            dataDict['title'] = ''
            dataDict['channel'] = ''
            dataDict['description'] = ''
            dataDict['starttime'] = ''
            dataDict['endtime'] = ''
            dataDict['duration'] = ''
            dataDict['remaining'] = ''

        return dataDict


    def DataManagerGetValue(self, keyName) :
        value = ''
        try:
            dataMgr = self.dvbviewer.DataManager
            if dataMgr is not None:
                value = dataMgr.Value(keyName)
        except Exception:
            pass  # silently ignore. DataManager no longer available after shutdown, however, we don't care.
        return value


    @eg.LogIt
    def DataManagerGetAllValues(self) :
        dataDict = {}
        try:
            dataMgr = self.dvbviewer.DataManager
            if dataMgr is not None:
                dataStr = dataMgr.GetAll()
                dataDict = dict(
                    (k.strip(), v.strip()) for k,v in (item.split('=') for item in dataStr.split(';'))
                )
        except Exception, exc:
            eg.PrintError('Failed dvbviewer.DataManager.DataManagerGetAllValues():', unicode(exc))
        return dataDict



class DVBViewerWatchDogThread( Thread ) :
    '''
    The watchdog thread is started by the plugin during startup. It monitors continuously the process list and waits
    for the dvbviewer.exe process. As soon as it detects the process, it starts the worker thread, which connects
    to DVBViewer's COM interface. As soon as it detects the process termination, it stops the worker thread
    and cleans up ressources.
    As a second task the watchdog thread periodically requests timers and recordings from Recording Service.
    '''

    def __init__( self, plugin, watchDogTime ) :

        Thread.__init__(self, name="DVBViewerWatchDogThread")
        self.plugin = plugin
        self.abort = False
        self.watchDogTime = watchDogTime
        self.started = False
        self.pauseEvent = Event()


    @eg.LogItWithReturn
    def run(self) :
        if self.watchDogTime == 0 :
            return False
        plugin = self.plugin

        try:
            self.pauseEvent.set()

            CoInitialize()

            queryTime = 5
            if queryTime > self.watchDogTime:
                queryTime = self.watchDogTime

            queryU = (
                    "SELECT * FROM __InstanceOperationEvent  WITHIN " + str( queryTime) +
                    " WHERE TargetInstance ISA 'Win32_Process' "
                    "AND TargetInstance.Name='dvbviewer.exe'" )

            queryA = ( "SELECT * FROM Win32_ProcessTrace WHERE ProcessName='dvbviewer.exe'" )

            WMI = GetObject('winmgmts:')

            eventSource = None
            eventsUsed = True

            try :
                eventSource = WMI.ExecNotificationQuery( queryA )
                START_EVENT = 'Win32_ProcessStartTrace'
                STOP_EVENT  = 'Win32_ProcessStopTrace'
                #print "Administrator rights"
            except :
                try :
                    eventSource = WMI.ExecNotificationQuery( queryU )
                    START_EVENT = '__InstanceCreationEvent'
                    STOP_EVENT  = '__InstanceDeletionEvent'
                    #print "User rights"
                except :
                    eventsUsed = False
                    eg.PrintDebugNotice('Getting WMI eventSource failed')
                    #print "Fallback"

            try:
                self.started = plugin.IsDVBViewerProcessRunning(WMI, eventOnException=False)
            except:
                self.started = False

            nextTimeViewer = time()
            timeout=True

            while not self.abort :
                try:
                    if ( eventsUsed ) :
                        try :
                            eventType = eventSource.NextEvent( 500 ).Path_.Class  # 500 = timeout in ms
                            if eventType == START_EVENT and not self.started :
                                #print "DVBViewer started"
                                eg.PrintDebugNotice("DVBViewer started")
                            elif eventType == STOP_EVENT and self.started:
                                #print "DVBViewer terminated"
                                eg.PrintDebugNotice("DVBViewer terminated")
                            elif time() < nextTimeViewer :
                                continue
                        except :
                            #print "Timeout"
                            if time() < nextTimeViewer :
                                continue
                            timeout = True

                    else :
                        while time() < nextTimeViewer and not self.abort :
                            started = plugin.IsDVBViewerProcessRunning(WMI, eventOnException=False)
                            if started and not self.started :
                                #print "DVBViewer started"
                                eg.PrintDebugNotice("DVBViewer started")
                                break
                            elif not started and self.started:
                                #print "DVBViewer terminated"
                                eg.PrintDebugNotice("DVBViewer terminated")
                                break
                            else :
                                timeCount = queryTime * 2
                                while ( timeCount > 0 and not self.abort ) :
                                    sleep( 0.5 )
                                    timeCount -= 1
                                    #print "wait"

                    # This event-object should be set before suspend (action: WaitUntilPluginIdle) and reset after resume
                    # It pauses background execution of DVBViewer- and RS-requests while system is going to suspend state.
                    # Otherwise acquired lock-objects would timeout after resume.
                    self.pauseEvent.wait(120) # timeout = 120 sec
                    self.pauseEvent.set()  # in case of timeout

                    plugin.executionStatusChangeLock.acquire( timeout=TERMINATE_TIMEOUT )

                    try:

                        if plugin.useService and timeout :
                            plugin.service.UpdateWithLock( UPDATE_ALL )

                        if plugin.closeWaitActive and plugin.eventHandlingIsAlive :
                            continue

                        started = plugin.IsDVBViewerProcessRunning(WMI, eventOnException=False)

                        if self.started == started and not timeout :
                            continue

                        self.started = started
                        timeout=False

                        #print "started = ", self.started, "  workerThread = ", plugin.workerThread

                        nextTimeViewer = time() + self.watchDogTime

                        if not self.started and plugin.workerThread is not None :
                            #print "WatchDog: Disconnect"
                            eg.PrintDebugNotice( "Termination of DVBViewer detected by watch dog" )
                            if plugin.workerThread.Stop( TERMINATE_TIMEOUT ) :
                                eg.PrintError("Could not terminate DVBViewer worker thread")
                            plugin.workerThread = None
                            plugin.DVBViewerIsFinished()

                        elif self.started and plugin.workerThread is None :
                            #print "WatchDog: Connect"
                            eg.PrintDebugNotice( "DVBViewer will be connected by watch dog" )
                            plugin.Connect( CONNECT )

                        if plugin.workerThread is not None :
                            #print "WatchDog: Update recording timers"
                            updatedRecordings = 0
                            try :
                                plugin.checkEventHandlingLock.acquire( blocking = False, timeout = CALLWAIT_TIMEOUT )
                                if plugin.SendCommand( DUMMY_ACTION, lock = False, connectionMode = CHECK_CONNECT ) :
                                    updatedRecordings = plugin.UpdateDVTimers( lock = False, updateService = False )
                                else :
                                    plugin.checkEventHandlingLock.acquire( blocking = False )
                                    plugin.checkEventHandlingLock.release()
                                    plugin.eventHandlingIsAlive = True

                            except :
                                msg = "DVBViewer process running but could not accessed by the Watch Dog Thread. Restart of DVBViewer is suggested."
                                plugin.TriggerEvent( "SevereError.Connect" )
                                eg.PrintDebugNotice(msg)
                                eg.PrintError(msg)
                                plugin.checkEventHandlingLock.acquire( blocking = False )
                                plugin.checkEventHandlingLock.release()
                                plugin.eventHandlingIsAlive = True
                            else :
                                if updatedRecordings > 0 :
                                    eg.PrintDebugNotice(    "Number of recording timers ("
                                                          + str(updatedRecordings)
                                                          + ") was updated  by watch dog" )

                    finally:
                        plugin.executionStatusChangeLock.release()

                except Exception, exc:
                    eg.PrintDebugNotice('Unexpected error: ', unicode(exc))

        finally:
            del eventSource
            del WMI

            # see also http://msdn.microsoft.com/en-us/library/ms688715%28VS.85%29.aspx
            # Closes the COM library on the current thread, unloads all DLLs loaded by the thread,
            # frees any other resources that the thread maintains, and forces all RPC connections on the thread to close.
            CoUninitialize()
        return True


    @eg.LogIt
    def Finish( self ) :
        plugin = self.plugin
        plugin.checkEventHandlingLock.acquire( blocking = False )
        plugin.checkEventHandlingLock.release()
        plugin.eventHandlingIsAlive = True
        self.abort = True
        self.started = False
        return True



class DVBViewerTerminateThread( Thread ) :
    '''
    This thread is responsible for cleaning up allocated ressources when DVBViewer closes.
    It is called by ComEventHandler.OnonDVBVClose()
    '''

    def __init__( self, plugin ) :

        Thread.__init__(self, name="DVBViewerTerminateThread")
        self.plugin = plugin


    @eg.LogItWithReturn
    def run(self) :
        plugin = self.plugin

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking=False, timeout=TERMINATE_TIMEOUT )

        workerThread = plugin.workerThread

        if workerThread is None :
            plugin.executionStatusChangeLock.release()
            plugin.lockedByTerminate = False
            eg.PrintDebugNotice( "DVBViewer is not disconnected by the close event processing" )
            return True

        try:
            plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )
            plugin.workerThread = None
            CoInitialize()

            queryA = "SELECT * FROM Win32_ProcessStopTrace WHERE ProcessName='dvbviewer.exe'"
            queryU = (
                       "SELECT * FROM __InstanceDeletionEvent  WITHIN 1 "
                       "WHERE TargetInstance ISA 'Win32_Process' "
                       "AND TargetInstance.Name='dvbviewer.exe'"
                     )

            WMI = GetObject('winmgmts:')

            plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

            events = None
            finished = True
            eventsUsed = True

            try :
                events = WMI.ExecNotificationQuery( queryA )
            except :
                try :
                    events = WMI.ExecNotificationQuery( queryU )
                except :
                    timeCounter = TERMINATE_TIMEOUT
                    finished   = False
                    while ( timeCounter > 0 ) :
                        if not plugin.IsDVBViewerProcessRunning(WMI, eventOnException=False):
                            finished = True
                            break
                        sleep( 1.0 )
                        timeCounter -= 1
                    eventsUsed = False

            plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

            if plugin.IsDVBViewerProcessRunning(WMI, eventOnException=False) and eventsUsed :
                try :
                    events.NextEvent( TERMINATE_TIMEOUT * 1000 )
                except :
                    finished = False

            if not finished :
                eg.PrintDebugNotice("DVBViewer could not be terminated")
                plugin.TriggerEvent( "DVBViewerCouldNotBeTerminated" )

            if finished :
                plugin.DVBViewerIsFinished()

            plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

            if workerThread is not None :
                if workerThread.Stop( TERMINATE_TIMEOUT ) :
                    eg.PrintError("Could not terminate DVBViewer thread")
                    plugin.TriggerEvent( "DVBViewerCouldNotBeTerminated" )

            plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )
            del events

        finally:
            del WMI
            CoUninitialize()
            plugin.terminateThread = None

            plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking=False, timeout=TERMINATE_TIMEOUT )
            if plugin.lockedByTerminate :
                plugin.executionStatusChangeLock.release()
                plugin.lockedByTerminate = False

        return finished



class LockWithTimeout :

    def LockTimeout( self ) :
        '''This method is called whenever an acquired lock is not released within the specified time.
        Sounds good... but... what happens then? Release the lock, really??
        So we acquired a lock in order to avoid that multiple threads modify objects at the same time
        (thread synchronization), but suddenly, when we are in trouble anyway, we allow unsynchronized access?
        Friends of the binary way of live, I think that wasn't a brilliant idea... :D
        Best we can do in this situation: Restart EventGhost, truly! That's why we trigger an event.
        '''
        try:
            msg = "Error: Timeout detected, DVBViewer plugin lock '" + self.name + "' force released. "
            eg.PrintDebugNotice(msg)
            eg.PrintError( msg )
            eg.PrintError( "Restart of EventGhost and DVBViewer is suggested." )
            self.printCaller('*** timeout!')
            if self.severeErrorEventOnTimeout:
                self.plugin.TriggerEvent( "SevereError.LockTimeout", msg )
            self.lock.release()
        except:
            pass
        return True

    def __init__( self, plugin, name, timeoutFunc=None, timeout=CALLWAIT_TIMEOUT-10, severeErrorEventOnTimeout=True) :
        self.plugin = plugin
        if timeoutFunc is None:
            self.timeoutFunc = self.LockTimeout
        else:
            self.timeoutFunc = timeoutFunc
        self.timer = None
        self.lock = Lock()
        self.name = name
        self.timeout = timeout
        self.severeErrorEventOnTimeout = severeErrorEventOnTimeout


    def __del__(self) :
        if self.timer is not None :
            self.timer.cancel()
            del self.timer
            self.timer = None
            eg.PrintDebugNotice('Warning: Lock object "' + self.name + ' deleted while locked')
        del self.lock


    def printCaller(self, prefix, blocking=None):
        '''Debug helper function. Prints the calling classname, method and code line for
        acquire and release locks. Helpful in order to find dead locks.'''
        if False: #eg.debugLevel > 0: # TODO
            try:
                stack = inspect.stack()
                frame, lineno, funcname = 0, 2, 3
                lockName = self.name
                sl = stack[2]
                callingClass = sl[frame].f_locals['self'].__class__.__name__
                eg.PrintDebugNotice(callingClass, sl[funcname], sl[lineno], lockName, prefix, 'lock', "blocking="+str(blocking) if blocking is not None else "")
            except:
                pass
            finally:
                if stack is not None:
                    del stack


    def acquire( self, blocking=True, timeout=None ) :
        self.printCaller('+++ acquire', blocking)
        if timeout is None:
            timeout = self.timeout
        blocked = self.lock.acquire( blocking )
        if blocked :
            self.printCaller('+++ ACQUIRE', blocking)
            self.timer = Timer( timeout, self.timeoutFunc )
            self.timer.start()
        return blocked


    def release( self ) :
        self.printCaller('--- RELEASE')
        ret = True
        try:
            if self.timer is not None :
                self.timer.cancel()
                del self.timer
                self.timer = None
                self.lock.release()
            else :
                eg.PrintDebugNotice('DVBViewer plugin unlocked lock "' + self.name + '" release detected')
                eg.PrintError( "Error: unlock lock '" + self.name + "' released" )
                ret = False
            #print "Released"
        except Exception, exc:
            eg.PrintError('Error releasing lock ' + self.name + ':', unicode(exc))
        return ret


class ActionPrototype(eg.ActionClass):
    def __call__(self):
        if self.value[1] :
            connectionMode = WAIT_CHECK_START_CONNECT
        else :
            connectionMode = CHECK_CONNECT
        return self.plugin.SendCommand(self.value[0], connectionMode = connectionMode )


class Start(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(self):
        self.plugin.Connect( WAIT_CHECK_START_CONNECT, lock = True )
        return True


class IsDVBViewerProcessRunning(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(self):
        return self.plugin.IsDVBViewerProcessRunning(eventOnException=False)


class WaitUntilPluginIdle(eg.ActionClass):
    name = "Prepare for Standby"
    description = u"""Prepares for Standby or Hibernate and waits until the plugin is idle. This action should be called before
suspending the system (i.e. before calling Standby or Hibernate). See Description page for more info.

This action waits until the plugin is idle and pauses background execution of the WatchDogThread.
It should be called before suspending the system (i.e. before calling Standby or Hibernate).
Otherwise lock-timeouts might occur, e.g. if the plugin gets interrupted in the middle of a background
task, like a COM- or service-request.
<p>
This action should be called as the <i>last</i> DVBViewer plugin action before suspending the system.
It should not be called without performing Standby / Hibernate immediately afterwards."""

    @eg.LogItWithReturn
    def __call__(self):
        plugin = self.plugin

        # This event-object pauses the WatchDogThread. Background requests to RS and DVBViewer (getting timer lists)
        # should be paused while system performs suspend. WatchDogThread continues after resume
        if plugin.watchDogThread is not None:
            plugin.watchDogThread.pauseEvent.clear()

        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.useService:
                plugin.serviceInUse.acquire()
                try:
                    pass
                finally:
                    plugin.serviceInUse.release()
        finally:
            plugin.executionStatusChangeLock.release()
        return True


class CloseDVBViewer( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, waitForTermination = False ) :
        plugin = self.plugin
        if plugin.workerThread is None :
            return False

        return plugin.WaitForTermination( sendCloseCommand = True, block = waitForTermination )


    def Configure(  self, waitForTermination = False ) :

        self.panel = eg.ConfigPanel()
        panel = self.panel

        checkBox = wx.CheckBox( panel, -1, self.text.checkBoxText )
        checkBox.SetValue( waitForTermination )

        panel.AddLine( checkBox )

        while panel.Affirmed():
            waitForTermination = checkBox.GetValue()
            panel.SetResult( waitForTermination )
        return True


class StopAllActiveRecordings( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self ) :
        plugin = self.plugin
        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( CHECK_CONNECT ) :
                plugin.workerThread.CallWait(
                    partial(plugin.workerThread.StopAllActiveRecordings ),
                    CALLWAIT_TIMEOUT
                )
        finally:
            plugin.executionStatusChangeLock.release()
        return True


class GetNumberOfActiveRecordings( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :
        plugin = self.plugin

        count = 0
        if plugin.useService and enableDVBService :
            count = plugin.service.GetNumberOfActiveRecordings( updateDVBService )

        plugin.executionStatusChangeLock.acquire()
        try:
            if enableDVBViewer :
                if plugin.Connect( CHECK_CONNECT ) :
                    idList =  plugin.workerThread.CallWait(
                        partial(plugin.workerThread.GetTimerIDs,
                                True, not enableDVBService and updateDVBService ),
                        CALLWAIT_TIMEOUT
                    )
                    count += len( idList )
        finally:
            plugin.executionStatusChangeLock.release()
        return count


    def Configure(  self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        self.plugin.ServiceConfigure( enableDVBViewer, enableDVBService, updateDVBService )


class GetRecordingsIDs( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, active = True, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :
        plugin = self.plugin

        idList = []

        if plugin.useService and enableDVBService :

            plugin.executionStatusChangeLock.acquire()
            try:
                timerIDs = plugin.service.GetTimerIDs( updateDVBService )
                if timerIDs is None :
                    timerIDs = {}
            finally:
                plugin.executionStatusChangeLock.release()

            for k, v in timerIDs.iteritems() :
                if v[0] or not active :
                    idList.append( v[2] )

        if enableDVBViewer :

            connectionMode = WAIT_CHECK_START_CONNECT
            if active :
                connectionMode = CHECK_CONNECT

            plugin.executionStatusChangeLock.acquire()
            try:
                if plugin.Connect( connectionMode ) :
                    idList.extend( plugin.workerThread.CallWait(
                         partial(plugin.workerThread.GetTimerIDs, active,
                                 not enableDVBService and updateDVBService ),
                         CALLWAIT_TIMEOUT
                     ) )
            finally:
                plugin.executionStatusChangeLock.release()

        return idList


    def Configure(  self, active = True, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        plugin = self.plugin

        panel = eg.ConfigPanel()

        checkBox = wx.CheckBox( panel, -1, self.text.active )
        checkBox.SetValue( active )

        panel.sizer.Add( checkBox )
        panel.sizer.Add(wx.Size(0,10))

        getFlags = plugin.ServiceConfigure(  enableDVBViewer, enableDVBService, updateDVBService, affirmed = False, panel = panel )

        while panel.Affirmed():
            active      = checkBox.GetValue()
            enableDVBViewer, enableDVBService, updateDVBService = getFlags()
            panel.SetResult( active, enableDVBViewer, enableDVBService, updateDVBService )
        return True


class IsConnected( eg.ActionClass ) :

    #@eg.LogItWithReturn
    def __call__( self ) :
        plugin = self.plugin
        plugin.executionStatusChangeLock.acquire()
        try:
            return self.plugin.workerThread is not None
        finally:
            plugin.executionStatusChangeLock.release()


class IsRecording( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :
        return eg.plugins.DVBViewer.GetNumberOfActiveRecordings(enableDVBViewer,
                                                        enableDVBService,
                                                        updateDVBService ) != 0

    def Configure(  self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        self.plugin.ServiceConfigure( enableDVBViewer, enableDVBService, updateDVBService )


class SendAction( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, action ) :
        if action != -1 :
            return self.plugin.SendCommand(action)
        else :
            return False

    def Configure( self, action=-1 ) :
        panel = eg.ConfigPanel()
        if action < 0 :
            action = 0
        actionCtrl = panel.SpinNumCtrl( action, min=0, max=999999, fractionWidth=0, integerWidth=6)
        panel.AddLine( self.text.action, actionCtrl )

        while panel.Affirmed() :
            action = actionCtrl.GetValue()

            panel.SetResult( action )
        return True


class ShowWindow( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, windowID ) :

        plugin = self.plugin

        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                plugin.workerThread.CallWait( partial( plugin.workerThread.ShowWindow, windowID ), CALLWAIT_TIMEOUT )
                return True
        finally:
            plugin.executionStatusChangeLock.release()

        return False


    def Configure( self, windowID=-1 ) :
        panel = eg.ConfigPanel()
        if windowID < 0 :
            windowID = 0
        windowIDCtrl = panel.SpinNumCtrl( windowID, min=0, max=999999, fractionWidth=0, integerWidth=6)
        panel.AddLine( self.text.windowID, windowIDCtrl )

        while panel.Affirmed() :
            windowID = windowIDCtrl.GetValue()

            panel.SetResult( windowID )
        return True


class ShowInfoinTVPic( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, text = "", timeout=15.0, force = False ) :

        connectMode = CHECK_CONNECT
        if force :
            connectMode = WAIT_CHECK_START_CONNECT

        plugin = self.plugin

        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( connectMode ) :
                plugin.workerThread.CallWait( partial( plugin.workerThread.ShowInfoinTVPic, " "+ text + " ", timeout ), CALLWAIT_TIMEOUT )
                plugin.infoInTVPicTimeout = time() + timeout
                return True
        finally:
            plugin.executionStatusChangeLock.release()

        return False


    def Configure( self, displayText="", timeout=15.0, force=False ) :

        plugin = self.plugin
        text = self.text

        panel = eg.ConfigPanel( resizable=True )

        textCtrl = panel.TextCtrl("\n", style=wx.TE_MULTILINE)
        w, h = textCtrl.GetBestSize()
        textCtrl.ChangeValue(displayText)
        textCtrl.SetMinSize((-1, h))

        timeCtrl = panel.SpinNumCtrl(timeout, min=0, max=999, fractionWidth=0, integerWidth=3)

        forceCheckBoxCtrl = wx.CheckBox(panel, -1, text.force)
        forceCheckBoxCtrl.SetValue( force )

        sizer = wx.GridBagSizer(5, 5)

        rowCount = 0
        sizer.Add(wx.StaticText(panel, -1, text.text), (rowCount, 0))
        sizer.Add(textCtrl,                            (rowCount, 1), flag=wx.EXPAND)

        rowCount += 1
        sizer.Add(wx.StaticText(panel, -1, text.time), (rowCount, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(timeCtrl,                            (rowCount, 1) )

        rowCount += 1
        sizer.Add(forceCheckBoxCtrl,                   (rowCount, 0), (1,2), flag=wx.EXPAND)

        sizer.AddGrowableCol(1)
        panel.sizer.Add(sizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            displayText = textCtrl.GetValue()
            timeout     = timeCtrl.GetValue()
            force       = forceCheckBoxCtrl.GetValue()

            panel.SetResult( displayText, timeout, force )


class DeleteInfoinTVPic( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self ) :

        plugin = self.plugin
        if plugin.infoInTVPicTimeout > time() + 0.01 :
            plugin.infoInTVPictimeout=0.0
            plugin.executionStatusChangeLock.acquire()
            try:
                if plugin.Connect( CHECK_CONNECT ) :
                    plugin.workerThread.CallWait( partial( plugin.workerThread.ShowInfoinTVPic, " ", 0 ), CALLWAIT_TIMEOUT )
                    return True
            finally:
                plugin.executionStatusChangeLock.release()
        return False


class UpdateEPG( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, timeBetweenChannelChange = 60.0, disableAVafterChannelChange = True, event = "EPGUpdateFinished" ) :

        plugin = self.plugin
        self.event = event

        if not plugin.frequencies :
            if not plugin.Connect( WAIT_CHECK_START_CONNECT, lock = True ) :
                plugin.TriggerEvent( event )
                return False

        plugin.tuneEPGThread = self.EPGTuneThread( plugin, timeBetweenChannelChange, event, disableAVafterChannelChange )
        plugin.tuneEPGThread.start()

        return True


    class EPGTuneThread( Thread ) :

        def __init__( self, plugin, timeBetweenChannelChange, eventText, disableAVafterChannelChange ) :

            Thread.__init__(self, name="DVBViewerEPGTuneThread")
            self.plugin = plugin
            self.timeBetweenChannelChange = timeBetweenChannelChange
            self.event = Event()
            self.eventText = eventText
            self.disableAVafterChannelChange = disableAVafterChannelChange

        @eg.LogItWithReturn
        def run( self ) :
            plugin = self.plugin
            abort = False

            saveDisableAV = plugin.disableAV

            CoInitialize()

            for frequency, channel in plugin.frequencies.iteritems() :
                changed = False
                while not changed and not abort:
                    if plugin.numberOfActiveTimers == 0 :
                        plugin.disableAV = self.disableAVafterChannelChange
                        changed =  plugin.TuneChannelIfNotRecording( channel[0], "Updating EPG", self.timeBetweenChannelChange )
                    self.event.wait( self.timeBetweenChannelChange )
                    plugin.disableAV = saveDisableAV
                    abort = self.event.isSet()
                if abort :
                    break

            plugin.SendCommand( 16383 )  #Stop Graph

            CoUninitialize()
            plugin.tuneEPGThread = None

            if not abort :
                plugin.TriggerEvent( self.eventText )

            return not abort

        def Finish( self ) :
            self.event.set()


    def Configure(  self, timeBetweenChannelChange=60.0, disableAVafterChannelChange=True, event="EPGUpdateFinished" ) :

        text = self.text

        panel = eg.ConfigPanel()

        disableAVCheckBoxCtrl = wx.CheckBox(panel, -1, text.disableAV)
        disableAVCheckBoxCtrl.SetValue( disableAVafterChannelChange )
        eventCtrl = panel.TextCtrl( event )

        epgTimeCtrl = panel.SpinNumCtrl(timeBetweenChannelChange, min=0, max=999, fractionWidth=0, integerWidth=3)

        panel.AddLine( disableAVCheckBoxCtrl )
        panel.AddLine( text.time,  epgTimeCtrl )
        panel.AddLine( text.event, eventCtrl )

        while panel.Affirmed():
            disableAVafterChannelChange                = disableAVCheckBoxCtrl.GetValue()
            timeBetweenChannelChange = epgTimeCtrl.GetValue()
            event                    = eventCtrl.GetValue()

            panel.SetResult( timeBetweenChannelChange, disableAVafterChannelChange, event )


class AddRecording( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__(self,
                 channelID,
                 date,                 # dd.mm.yyyy
                 startTime,            # hh:mm
                 endTime,              # hh:mm
                 description="",
                 disableAV=False,
                 enabled=True,
                 recAction=0,          # intern = 0, tune only = 1,
                                       # AudioPlugin = 2, Videoplugin = 3

                 actionAfterRec=0,     # No action = 0, PowerOff = 1,
                                       # Standby = 2, Hibernate = 3, Close = 4,
                                       # Playlist = 5, Slumbermode: = 6

                 days="-------"
                ) :
        plugin = self.plugin

        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                plugin.workerThread.CallWait(
                    partial( plugin.workerThread.AddTimer,
                             channelID, date, startTime, endTime, description, disableAV,
                             enabled, recAction, actionAfterRec, days
                    ),
                    CALLWAIT_TIMEOUT
                )

        finally:
            plugin.executionStatusChangeLock.release()
        return True


    def Configure(  self,
                 channelID   = "",
                 date        = "",     # dd.mm.yyyy
                 startTime   = "",     # hh:mm
                 endTime     = "",     # hh:mm
                 description = "",
                 disableAV   = False,
                 enabled     = True,
                 recAction   = 0,      # intern = 0, tune only = 1,
                                       # AudioPlugin = 2, Videoplugin = 3

                 actionAfterRec = 0,   # No action = 0, PowerOff = 1,
                                       # Standby = 2, Hibernate = 3, Close = 4,
                                       # Playlist = 5, Slumbermode: = 6

                 days = "-------"
                ) :

        plugin = self.plugin
        text = self.text

        if len(plugin.tvChannels) == 0 and len(plugin.radioChannels) == 0 :
            plugin.Connect( WAIT_CHECK_START_CONNECT, lock = True )

        ix = 0
        if plugin.IDbychannelIDList.has_key( channelID ) :

            key = plugin.IDbychannelIDList[ channelID ]
            self.tv = key[1]
            if ( self.tv ) :
                self.choices = plugin.tvChannels
            else :
                self.choices = plugin.radioChannels
            ix = key[0]
        else :
            self.tv = True
            self.choices = plugin.tvChannels


        def onRadioButton( event ) :

            ix = channelChoiceCtrl.GetSelection()

            if ix != wx.NOT_FOUND :
                if self.tv :
                    plugin.indexTV = ix
                else :
                    plugin.indexRadio = ix

            tvMode = tvCtrl.GetValue()

            if tvMode :
                ix = plugin.indexTV
                self.choices = plugin.tvChannels
            else :
                ix = plugin.indexRadio
                self.choices = plugin.radioChannels
            self.tv = tvMode
            channelChoiceCtrl.Clear()
            channelChoiceCtrl.SetItems( self.choices )
            channelChoiceCtrl.SetSelection( ix )
            event.Skip()


        self.panel = eg.ConfigPanel()
        panel = self.panel

        tvCtrl = wx.RadioButton( panel, -1, text.tvButton, style = wx.RB_GROUP )
        tvCtrl.SetValue( self.tv )
        tvCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButton)

        radioCtrl = wx.RadioButton( panel, -1, text.radioButton )
        radioCtrl.SetValue( not self.tv )
        radioCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButton )



        channelChoiceCtrl = panel.Choice(ix, choices=plugin.tvChannels + plugin.radioChannels)
        wSize = channelChoiceCtrl.GetSize()
        channelChoiceCtrl.Clear()
        channelChoiceCtrl.SetItems( self.choices )
        channelChoiceCtrl.SetSizeHintsSz( wSize )
        channelChoiceCtrl.SetSelection( ix )

        wxDate = wx.DateTime()
        if date == "" :
            wxDate = wx.DateTime.Now()
        else :
            wxDate.ParseFormat( date, "%d.%m.%Y" )
        dateCtrl = wx.DatePickerCtrl( panel, dt = wxDate, style=wx.DP_DEFAULT|wx.DP_DROPDOWN )#|wx.DP_ALLOWNONE )

        wxStartTime = wx.DateTime()
        if startTime == "" :
            wxStartTime = wx.DateTime.Now()
        else :
            wxStartTime.ParseFormat( startTime, "%H:%M" )
        startTimeCtrl = masked.timectrl.TimeCtrl( panel, format = "24HHMMSS", value = wxStartTime )

        wxEndTime = wx.DateTime()
        if endTime == "" :
            wxEndTime = wxStartTime
        else :
            wxEndTime.ParseFormat( endTime, "%H:%M" )
        endTimeCtrl = masked.timectrl.TimeCtrl( panel, format = "24HHMMSS", value = wxEndTime )

        descriptionCtrl = wx.TextCtrl( panel, size=(200,-1) )
        descriptionCtrl.SetValue( description )

        disableAVCheckBoxCtrl = wx.CheckBox(panel, -1, text.disableAV)
        disableAVCheckBoxCtrl.SetValue( disableAV )

        enabledCheckBoxCtrl = wx.CheckBox(panel, -1, text.enabled)
        enabledCheckBoxCtrl.SetValue( enabled )

        recActionChoiceCtrl = panel.Choice( recAction, choices=text.recActionChoices)
        actionAfterRecChoiceCtrl = panel.Choice( actionAfterRec, choices=text.actionAfterRecChoices)

        sb = wx.StaticBox( panel, -1, text.source )
        sBoxSizer = wx.StaticBoxSizer( sb, wx.HORIZONTAL )

        sizer = wx.GridSizer(2,2,5,5)
        sizer.Add( tvCtrl,    0, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add( wx.StaticText(panel, -1, text.station), 0, flag = wx.ALIGN_BOTTOM)
        sizer.Add( radioCtrl, 0, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add( channelChoiceCtrl, 0, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

        sBoxSizer.Add( sizer, 0 , flag = wx.EXPAND )

        panel.sizer.Add(sBoxSizer, 0, flag = wx.EXPAND )

        panel.sizer.Add(wx.Size(0,3))

        sb = wx.StaticBox( panel, -1, text.recordingDate )
        sBoxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )
        sBoxSizer.Add(wx.Size(0,3))

        sizer = wx.GridSizer(2,3,5,5)
        sizer.Add( wx.StaticText(panel, -1, text.date), 0, flag = wx.ALIGN_BOTTOM)
        sizer.Add( wx.StaticText(panel, -1, text.start), 0, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL )
        sizer.Add(startTimeCtrl, 0, flag = wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(dateCtrl, 0, flag = wx.ALIGN_CENTER_VERTICAL)
        sizer.Add( wx.StaticText(panel, -1, text.end), 0, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL )
        sizer.Add(endTimeCtrl, 0, flag = wx.ALIGN_CENTER_VERTICAL)

        sBoxSizer.Add( sizer, 0, flag = wx.EXPAND )

        sizer = wx.GridBagSizer( 0,3)

        dayCount = 0
        dayCheckBoxCtrl = []
        for day in text.days :
            dayCount += 1
            sizer.Add( wx.StaticText(panel, -1, day),( 0, dayCount ), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL )
            checkBox = wx.CheckBox( panel, -1, "" )
            checkBox.SetValue( days[ dayCount-1 : dayCount ] != "-" )
            dayCheckBoxCtrl.append( checkBox )
            sizer.Add( checkBox,( 1, dayCount ), flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL )

        sBoxSizer.Add(wx.Size(0,5))
        sBoxSizer.Add( sizer, 0 )


        panel.sizer.Add(sBoxSizer, 0, flag = wx.EXPAND )

        panel.sizer.Add(wx.Size(0,3))

        sb = wx.StaticBox( panel, -1, "" )
        sBoxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )
        sBoxSizer.Add(wx.Size(0,10))

        sizer = wx.BoxSizer( wx.HORIZONTAL )
        sizer.Add( wx.StaticText(panel, -1, text.recordingDescription), 0, flag = wx.ALIGN_CENTER_VERTICAL )
        sizer.Add(descriptionCtrl, 0, flag = wx.EXPAND )
        sBoxSizer.Add( sizer, 0, flag = wx.EXPAND )

        sBoxSizer.Add(wx.Size(0,10))

        sizer = wx.GridSizer(2,3,5,5)

        sizer.Add(disableAVCheckBoxCtrl, 0 )
        sizer.Add( wx.StaticText(panel, -1, text.mode), 0, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL )
        sizer.Add(recActionChoiceCtrl, 0 )

        sizer.Add(enabledCheckBoxCtrl, 0 )
        sizer.Add( wx.StaticText(panel, -1, text.afterRecording), 0, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL )
        sizer.Add(actionAfterRecChoiceCtrl, 0 )

        sBoxSizer.Add( sizer, 0, flag = wx.EXPAND )

        panel.sizer.Add(sBoxSizer, 0, flag = wx.EXPAND )

        while panel.Affirmed():
            channelID       = plugin.channelIDbyIDList[ ( channelChoiceCtrl.GetValue(), self.tv ) ]
            date            = dateCtrl.GetValue().Format( "%d.%m.%Y" )
            startTime       = startTimeCtrl.GetValue( as_wxDateTime=True ).Format( "%H:%M" )
            endTime         = endTimeCtrl.GetValue( as_wxDateTime=True ).Format( "%H:%M" )
            description     = descriptionCtrl.GetValue()
            disableAV       = disableAVCheckBoxCtrl.GetValue()
            enabled         = enabledCheckBoxCtrl.GetValue()
            recAction       = recActionChoiceCtrl.GetValue()
            actionAfterRec  = actionAfterRecChoiceCtrl.GetValue()

            days = ""
            dayCount = -1
            for checkBox in dayCheckBoxCtrl :
                dayCount += 1
                if checkBox.GetValue() :
                    days += "T"
                else :
                    days += "-"

            panel.SetResult( channelID,
                             date,
                             startTime,
                             endTime,
                             description,
                             disableAV,
                             enabled,
                             recAction,
                             actionAfterRec,
                             days )


class GetSetupValue( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, section="", name="", default="" ) :

        plugin = self.plugin
        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                res = plugin.workerThread.CallWait(
                    partial( plugin.workerThread.GetSetupValue, section, name, default ),
                    CALLWAIT_TIMEOUT
                )
                return res
        finally:
            plugin.executionStatusChangeLock.release()

        return default


    def Configure(  self, section="", name="", default="" ) :

        self.panel = eg.ConfigPanel()
        panel = self.panel

        sectionCtrl = wx.TextCtrl( panel, size=(200,-1) )
        sectionCtrl.SetValue( section )

        nameCtrl = wx.TextCtrl( panel, size=(200,-1) )
        nameCtrl.SetValue( name )

        defaultCtrl = wx.TextCtrl( panel, size=(200,-1) )
        defaultCtrl.SetValue( default )

        panel.AddLine( self.text.section, sectionCtrl )
        panel.AddLine( self.text.setupName,    nameCtrl )
        panel.AddLine( self.text.default, defaultCtrl )

        while panel.Affirmed():
            section      = sectionCtrl.GetValue()
            name         =    nameCtrl.GetValue()
            default      = defaultCtrl.GetValue()

            panel.SetResult( section, name, default )


# TODO: re-implement using action 'GetTimerDetails' (simplifies a lot)
class GetDateOfRecordings( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self,
                  allRecordings=False,
                  enableDVBViewer=True,
                  enableDVBService=False,
                  updateDVBService=False
                ) :

        plugin = self.plugin

        readOutSuccessfull = plugin.useService and enableDVBService or enableDVBViewer
        timerDates = []
        if plugin.useService and enableDVBService :
            timerDates = plugin.service.GetTimerDates( active = False, update = updateDVBService )
            if timerDates is None :
                timerDates = []
                readOutSuccessfull = False

        if enableDVBViewer :
            recordingList = []
            plugin.executionStatusChangeLock.acquire()
            try:
                if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                    recordingList = plugin.workerThread.CallWait(
                        partial( plugin.workerThread.GetTimers, False, updateDVBService and not enableDVBService ),
                        CALLWAIT_TIMEOUT )
            finally:
                plugin.executionStatusChangeLock.release()

            readOutSuccessfull &= len(recordingList) > 0

            now = time()
            for record in recordingList :
                if record[TI_8_ENABLED] :
                    if record[TI_18_TIMERACTION] == 1 and record[TI_0_DESCRIPTION] == "EPG-Update by EventGhost" :
                        continue

                    t = toDateTime( record[TI_5_DATE], record[TI_6_STARTTIME] )

                    if t < now :
                        continue
                    if not t in timerDates :
                        timerDates.append(t)
                    #print "date = ", ctime(t)


        timerDates.sort()

        if allRecordings :
            return ( readOutSuccessfull, timerDates )
        else :
            if len( timerDates ) == 0 :
                return ( readOutSuccessfull, -1 )
            else :
                return ( readOutSuccessfull, timerDates[ 0 ] )


    def Configure(  self, allRecordings=False, enableDVBViewer=True, enableDVBService=False, updateDVBService=False ) :

        plugin = self.plugin

        panel = eg.ConfigPanel()

        checkBox = wx.CheckBox( panel, -1, self.text.allDates )
        checkBox.SetValue( allRecordings )

        panel.sizer.Add( checkBox )
        panel.sizer.Add(wx.Size(0,10))

        getFlags = plugin.ServiceConfigure(  enableDVBViewer, enableDVBService, updateDVBService, affirmed = False, panel = panel )

        while panel.Affirmed():
            allRecordings      = checkBox.GetValue()
            enableDVBViewer, enableDVBService, updateDVBService = getFlags()
            panel.SetResult( allRecordings, enableDVBViewer, enableDVBService, updateDVBService )


class GetTimerDetails( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self,
        allRecordings=False,
        enableDVBViewer=True,
        enableDVBService=True,
        updateDVBService=False,
        enabled=True,
        active=False
    ) :

        def mergeAndSort(rsTimerList, dvbvTimerList, enabled, active, now):
            resultList=[]
            for record in rsTimerList:
                if enabled and not record['enabled']:
                    continue
                if record['endDateTime'] < now:
                    continue
                if active and not record['recording']:
                    continue
                resultList.append(record)

            for record in dvbvTimerList:
                if record[TI_18_TIMERACTION] == 1 and record[TI_0_DESCRIPTION] == "EPG-Update by EventGhost" :
                    continue
                if enabled and not record[TI_8_ENABLED]:
                    continue
                startDatetime = toDateTime(record[TI_5_DATE], record[TI_6_STARTTIME])
                endDatetime = toDateTime(record[TI_5_DATE], record[TI_7_ENDTIME])
                if endDatetime < startDatetime:
                    endDatetime += 24 * 60 * 60
                if endDatetime < now:
                    continue
                if active and not record[TI_11_RECORDING]:
                    continue

                timerentry = toTimerEntry(
                    timerID = record[TI_4_ID],
                    channelID = record[TI_1_CHANNEL].split('|')[0],
                    channelName = record[TI_1_CHANNEL].split('|')[1],
                    dateStr = strftime("%d.%m.%Y", localtime(startDatetime)),
                    startTimeStr = strftime("%H:%M:%S", localtime(startDatetime)),
                    endTimeStr = strftime("%H:%M:%S", localtime(endDatetime)),
                    startDateTime = startDatetime,
                    endDateTime = endDatetime,
                    days = record[TI_15_DAYS],
                    description = record[TI_0_DESCRIPTION],
                    enabled = record[TI_8_ENABLED],
                    recording = record[TI_11_RECORDING],
                    action = record[TI_18_TIMERACTION],
                    fromRS = False
                )

                resultList.append(timerentry)

            resultList.sort(cmp=lambda x, y: cmp(x['startDateTime'], y['startDateTime']))
            return resultList


        plugin = self.plugin
        plugin.executionStatusChangeLock.acquire()
        try:
            readOutSuccessfull = True

            rsTimerList = []
            dvbvTimerList = []

            if plugin.useService and enableDVBService :
                rsTimerList = plugin.service.GetTimerList( update = updateDVBService )
                if rsTimerList is None :
                    rsTimerList = []
                    readOutSuccessfull = False
        finally:
            plugin.executionStatusChangeLock.release()

        if enableDVBViewer :
            plugin.executionStatusChangeLock.acquire()
            try:
                if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                    dvbvTimerList = plugin.workerThread.CallWait(
                        partial( plugin.workerThread.GetTimers, active=active, update=(updateDVBService and not enableDVBService)),
                        CALLWAIT_TIMEOUT )
                else :
                    readOutSuccessfull = False
            finally:
                plugin.executionStatusChangeLock.release()

        resultList = mergeAndSort(rsTimerList, dvbvTimerList, enabled, active, time())
        #print "resultList=", resultList

        if allRecordings :
            return ( readOutSuccessfull, resultList )
        else :
            if not resultList or len( resultList ) == 0 :
                return ( readOutSuccessfull, [] )
            else :
                return ( readOutSuccessfull, resultList[ 0 ] )


    def Configure(  self,
        allRecordings=False,
        enableDVBViewer=True,
        enableDVBService=True,
        updateDVBService=True,
        enabled=True,
        active=False
    ) :
        plugin=self.plugin
        panel = eg.ConfigPanel()

        allRecCB = wx.CheckBox( panel, -1, self.text.allRecordings )
        allRecCB.SetValue( allRecordings )
        enabledCB = wx.CheckBox( panel, -1, self.text.enabled )
        enabledCB.SetValue( enabled )
        activeCB = wx.CheckBox( panel, -1, self.text.active )
        activeCB.SetValue( active )

        panel.sizer.Add(wx.Size(0,5))
        panel.sizer.Add( allRecCB )
        panel.sizer.Add(wx.Size(0,5))
        panel.sizer.Add( enabledCB )
        panel.sizer.Add(wx.Size(0,5))
        panel.sizer.Add( activeCB )
        panel.sizer.Add(wx.Size(0,10))

        getFlags = plugin.ServiceConfigure(  enableDVBViewer, enableDVBService, updateDVBService, affirmed = False, panel = panel )

        while panel.Affirmed():
            allRecordings = allRecCB.GetValue()
            enabled = enabledCB.GetValue()
            active = activeCB.GetValue()
            enableDVBViewer, enableDVBService, updateDVBService = getFlags()
            panel.SetResult( allRecordings, enableDVBViewer, enableDVBService, updateDVBService, enabled, active )


class GetRecordingDetails( eg.ActionClass ) :
    name = "Get Recordings Details"
    description = """Returns recordings details like name, date, series, channel, play status etc. from DVBViewer
as well as from Recording Service.

The recording lists of both sources (DVBViewer and RS) are combined, however, 'playstatus' attribute is only available
while DVBViewer is running and 'series' attribute is only supported by Recording Service.
The result is provided as a data dictionary in 'eg.result'."""

    @eg.LogIt
    def __call__( self,
        enableDVBViewer=True,
        enableDVBService=True,
        updateDVBService=False
    ) :
        def merge(rsList, dvbvList):
            """
            Merge result from DVBViewer and Recording Service.
            RS knows attribute 'series', but not 'played',
            DVBV knows attribute 'played', but not 'series'.
            """
            resultList = {}
            if rsList is not None and len(rsList) > 0 and dvbvList is not None and len(dvbvList) > 0:
                # copy the 'played' attribute from DVBViewer into the list from RS
                for rsKey, rsVal in rsList.items():
                    retVal = cpy(rsVal) # deep copy
                    dvbvVal = dvbvList.get(rsKey, None)
                    if dvbvVal is not None:
                        if (rsVal[RE_TITLE] == dvbvVal[RE_TITLE] # just to make sure that the recID key is the same...
                            #and rsVal[RE_STARTDATE] == dvbvVal[RE_STARTDATE]
                            and rsVal[RE_FILENAME] == dvbvVal[RE_FILENAME]
                        ):
                            retVal[RE_PLAYED] = dvbvVal[RE_PLAYED]
                        else:
                            eg.PrintError("Unexpected: rsVal is not equal to dvbvVal! rsVal=%s dvbvVal=%s" % (rsVal, dvbvVal))

                    resultList[rsKey] = retVal

                # copy missing DVBViewer recordings (direct recordings) into the list from RS
                for dvbvKey, dvbvVal in dvbvList.items():
                    if not dvbvKey in resultList:
                        resultList[dvbvKey] = cpy(dvbvVal)

            elif rsList is not None and len(rsList) > 0:
                resultList = cpy(rsList)
            elif dvbvList is not None and len(dvbvList) > 0:
                resultList = cpy(dvbvList)
            return resultList

        plugin = self.plugin
        readOutSuccessfull = True
        rsRecordingList = {}
        dvbvRecordingList = {}

        if plugin.useService and enableDVBService :
            rsRecordingList = plugin.service.GetRecordingList( update = updateDVBService )
            if rsRecordingList is None :
                rsRecordingList = {}
                readOutSuccessfull = False

        if enableDVBViewer :
            plugin.executionStatusChangeLock.acquire()
            try:
                if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                    dvbvRecordingList = plugin.workerThread.CallWait(
                        partial( plugin.workerThread.GetRecordings),
                        CALLWAIT_TIMEOUT )
                else :
                    readOutSuccessfull = False
            finally:
                plugin.executionStatusChangeLock.release()

        resultList = merge(rsRecordingList, dvbvRecordingList)


        return ( readOutSuccessfull, resultList )


    def Configure(  self,
        enableDVBViewer=True,
        enableDVBService=True,
        updateDVBService=True
    ) :
        plugin = self.plugin
        panel = eg.ConfigPanel()

        getFlags = plugin.ServiceConfigure(  enableDVBViewer, enableDVBService, updateDVBService, affirmed = False, panel = panel )

        while panel.Affirmed():
            enableDVBViewer, enableDVBService, updateDVBService = getFlags()
            panel.SetResult( enableDVBViewer, enableDVBService, updateDVBService )


class DeleteRecordings( eg.ActionClass ) :
    name = "Delete Recordings"
    description = u'''Delete Recordings according to search criteria and filters.
May be used to implement an automated housekeeping, especially for recorded TV series.
IT'S POWERFUL, USE IT WITH CARE !

Suppose that you daily record some News program, or a weekly talk show or whatever.
Tired of deleting old recordings? Let this action do the job for you.
<p>
Delete Recordings (aka 'series killer' or 'Putzfisch' ;)) is a powerful tool which lets you search and delete
recordings with a variety of search options.
Its intendeded usage is for automatic deletion of outdated recordings (housekeeping),
especially for recorded TV series.
<p>
The configuration of this action should be self-explaining, however some hints:
<ul>
<li> If you want to implement an automated daily housekeeping, just call the 'Delete Recordings'
macros from an appropriate event, I'd suggest to use 'DVBViewerService.AllRecordingsFinished'.
<li> ALWAYS TEST YOUR QUERY IN DRY MODE FIRST! 'Dry Mode' let's you play and try to see which recordings
would be deleted, once the query is armed. As long as you are in Dry Mode, no recording will be deleted, never.
<li> It's recommended to specify the delete query as exact as possible, i.e. for example use not only
the title of the recording, but also the channel name if you can etc.
As a thumb rule, the more options you specify, the smaller the risk that you delete something you regret afterwards.
<li> Partial strings search is supported, for example if you search for 'ind' you would
find 'Indiana Jones', 'Gone with the Wind' etc.
<li> Series are only supported by Recording Service, not by DVBViewer. Series names can be configured
in the timer configuration details of the Recording Service.
<li> The Played / Unplayed status is only supported by DVBViewer, not by the Recording Service.
If you want to use it as a criteria in your search, DVBViewer must be running while the action is executed.
If not, nothing bad will happen, it's just not working, but no recordings are deleted.
<li> The action can handle and delete 'Direct Recordings' from DVBViewer as well as Recordings
from the Recording Service. This is done transparently, you don't have to care for.
</ul>
'''

    class Text:
        filterTitle = "Filter criteria (all filters are AND combined)"
        resultTitle = "Query result"

        deleteByAge = "Delete by age"
        minAgeDays1 = "Delete recordings older than"
        minAgeDays2 = "days"

        deleteBySeries = "Delete by series"
        seriesName = "Recording series name:"

        deleteByName = "Delete by title name"
        titleName = "Recording title:"

        deleteByChannel = "Delete by channel"
        channelName = "TV channel name:"

        deleteByPlaystatus = "Delete by play status (data only available while DVBViewer is running!)"
        onlyPlayed = "Delete only played recordings"
        onlyUnplayed = "Delete only unplayed recordings"

        keepMinimum = "Keep the youngest recordings"
        keepAtLeast1 = "Keep at least the last"
        keepAtLeast2 = "recordings that match the filters, regardless of age"

        dryMode = "Dry mode => do not really perform the delete operation but print the result to the log file"
        dryModeHint = "Hint: You're in dry mode. Simply press the 'Test' button to check the query results."

        deletePreview1 = "*** DryMode - Nothing will be deleted. ***"
        deletePreview2 = "*** This operation would delete %s records! ***"
        deletePreview3 = "Empty result, nothing to delete"

        dryPrefix = 'DryMode: '
        deletePrefix = 'Delete: '

        queryResult1 = "The current query results in"
        queryResult2 = "deletions!"

        errorDelAllRec = "ERROR: Current settings would delete %s recordings, i.e. ALL OF YOUR RECORDINGS! Refine your query!"
        errorDelTooManyRec = "ERROR: Current settings would delete %s recordings, that's MORE THAN HALF of your recordings! Refine your query!"

        dryMode_t = "[Dry Mode]: "
        realMode_t = "[Really!]: "
        delete_t = 'Delete all '
        played_t = 'played '
        unplayed_t = 'unplayed '
        any_t = 'any '
        recordings_t = 'recordings '
        title_t = 'with title "%s" '
        fromSeries_t = 'from series "%s" '
        onChannel_t = 'from channel "%s" '
        olderThan_t = 'which are older than %s days '
        keepAtLeast_t = 'but keep at least the last %s recordings '

    # class holding the parameters for the delete query
    class DeleteQuery:
        def __init__(self,
            dryMode=True,
            deleteByAge=False, minAgeDays=0,
            deleteBySeries=False, seriesName='',
            deleteByName=False, titleName='',
            deleteByChannel=False, channelName='',
            deleteByPlaystatus=False, onlyPlayed=True,
            keepMinimum=False, keepAtLeast=0
        ):
            self.dryMode = dryMode
            self.deleteByAge, self.minAgeDays = self.checkIntArg(deleteByAge, minAgeDays)
            self.deleteBySeries, self.seriesName = self.checkStringArg(deleteBySeries, seriesName)
            self.deleteByName, self.titleName = self.checkStringArg(deleteByName, titleName)
            self.deleteByChannel, self.channelName = self.checkStringArg(deleteByChannel, channelName)
            self.deleteByPlaystatus, self.onlyPlayed = deleteByPlaystatus, onlyPlayed
            self.keepMinimum, self.keepAtLeast = self.checkIntArg(keepMinimum, keepAtLeast)

        # workaround since GetLabel() does not accept custom objects as argument (I guess it's a bug in EG framework?)
        def ToTupel(self):
            return (self.dryMode,
                self.deleteByAge, self.minAgeDays,
                self.deleteBySeries, self.seriesName,
                self.deleteByName, self.titleName,
                self.deleteByChannel, self.channelName,
                self.deleteByPlaystatus, self.onlyPlayed,
                self.keepMinimum, self.keepAtLeast
            )

        # workaround since GetLabel() does not accept custom objects as argument (I guess it's a bug in EG framework?)
        @classmethod
        def FromTupel(cls, tpl):
            return cls(tpl[0], tpl[1], tpl[2], tpl[3], tpl[4], tpl[5], tpl[6], tpl[7], tpl[8], tpl[9], tpl[10], tpl[11], tpl[12])


        # helper method: strips the string value and sets the flag to False if value is empty or None
        def checkIntArg(self, flag, value, default=0):
            if value is None or value == 0:
                return (False, default)
            else:
                return (flag, value)


        # helper method: strips the string value and sets the flag to False if value is empty or None
        def checkStringArg(self, flag, value, default=''):
            if value is not None:
                value = value.strip()
                if value == '':
                    value = None
            if value is None:
                return (False, default)
            else:
                return (flag, value)


        # constructs a prosa text from the query
        def QueryAsText(self):
            text = DeleteRecordings.Text

            label = ''
            if self.dryMode:
                label += text.dryMode_t
            else:
                label += text.realMode_t

            label += text.delete_t

            if self.deleteByPlaystatus:
                if self.onlyPlayed:
                    label += text.played_t
                else:
                    label += text.unplayed_t
            #elif not self.deleteByName:
            #    label += text.any_t

            label += text.recordings_t

            if self.deleteByName:
                label += text.title_t % self.titleName

            if self.deleteBySeries:
                label += text.fromSeries_t % self.seriesName

            if self.deleteByChannel:
                label += text.onChannel_t % self.channelName

            if self.deleteByAge:
                label += text.olderThan_t % self.minAgeDays

            if self.keepMinimum:
                label += text.keepAtLeast_t % self.keepAtLeast

            label = label.strip() + '. '

            return label


    # convenience method
    def LoadRecordingsData(self, deleteQueryTpl):
        if deleteQueryTpl is None:
            query = self.DeleteQuery() # new query with defaults
        else:
            query = self.DeleteQuery.FromTupel(deleteQueryTpl) # convert tupel into DeleteQuery object

        if self.plugin.workerThread is not None:
            enableDVBViewer = True
        else:
            enableDVBViewer = False

        # call action GetRecordingDetails
        recDetails = eg.plugins.DVBViewer.GetRecordingDetails(enableDVBViewer, enableDVBService=True, updateDVBService=True)

        recordings = {}
        if recDetails is not None:
            readoutSuccessful = recDetails[0]
            if readoutSuccessful:
                recordings = recDetails[1]
            else:
                eg.PrintError("GetRecordingDetails failed")

        return (recordings, query)


    # computes the query result
    # This code was hard to write, so it's OK if it's hard to read :)
    def ComputeQueryResult(self, recordings, deleteQuery, silent=False):
        emptyResult = (0, [])
        if recordings is None or len(recordings) == 0:
            return emptyResult

        if deleteQuery is None:
            return emptyResult
        else:
            q = deleteQuery

        numRecsBefore = len(recordings)

        dellist = recordings.values()
        dellist.sort(cmp=lambda x, y: cmp(y[RE_STARTDATE], x[RE_STARTDATE])) # sort by age in reverse order

        if q.deleteByName and q.titleName is not None:
            dellist = [ v for v in dellist if v[RE_TITLE].lower().find(q.titleName.lower()) >= 0 ]

        if q.deleteBySeries and q.seriesName is not None:
            dellist = [ v for v in dellist if v[RE_SERIES].lower().find(q.seriesName.lower()) >= 0 ]

        if q.deleteByChannel and q.channelName is not None:
            dellist = [ v for v in dellist if v[RE_CHANNEL].lower().find(q.channelName.lower()) >= 0 ]

        if q.deleteByPlaystatus:
            dellist = [ v for v in dellist
                          if v[RE_PLAYED] is not None
                            and (v[RE_PLAYED] >= 0 and q.onlyPlayed or v[RE_PLAYED] < 0 and not q.onlyPlayed) ]

        # Note: the 'keepAtLeast' logic IS different if combined with name searches (as above)
        # than when combined with the 'deleteByAge' logic - it's different because
        # our natural expectation is different in these two situations.
        # Expl: "Delete name='denver clan' keepAtLeast=2"   -> keeps 2 records and deletes the rest
        #       "Delete older than (today+7) keepAtLeast=2" -> keeps *at least* 2 records and deletes the older ones.
        if q.keepMinimum:
            if len(dellist) > q.keepAtLeast:
                dellist = dellist[q.keepAtLeast:] # remove 'keepAtLeast' elements from the beginning of the deletion list
            else:
                return emptyResult

        if q.deleteByAge:
            maxDate = dt.now() - td(days=q.minAgeDays)
            dellist = [ v for v in dellist if v[RE_STARTDATE] < maxDate ] # records which are older than maxDays

        numRecsDelete = len(dellist)

        if numRecsDelete == numRecsBefore:
            if not silent:
                eg.PrintError(self.Text.errorDelAllRec % numRecsDelete)
            dellist = []
        elif float(numRecsDelete) / float(numRecsBefore) > 0.5:
            if not silent:
                eg.PrintError(self.Text.errorDelTooManyRec % numRecsDelete)
            dellist = []

        return (numRecsDelete, dellist)


    @eg.LogItWithReturn
    def __call__( self,
        deleteQueryTpl=None
    ) :
        def printRecord(rec, prefix=''):
            delim  = ' | '
            print prefix + str(rec[RE_STARTDATE])  + delim + rec[RE_TITLE] + delim + rec[RE_CHANNEL] + delim + rec[RE_SERIES] + delim + rec[RE_FILENAME] + delim + str(rec[RE_PLAYED]) + delim + ('From RS' if rec[RE_FROMRS] else 'From DVBViewer')

        plugin = self.plugin
        text = self.Text

        recordings, q = self.LoadRecordingsData(deleteQueryTpl)

        dellist = self.ComputeQueryResult(recordings, q, False)[1]

        if q.dryMode:
            print text.deletePreview1
            if len(dellist) > 0:
                print text.deletePreview2 % len(dellist)
                for v in dellist:
                    printRecord(v, text.dryPrefix)
            else:
                print text.deletePreview3
            return False

        elif len(dellist) > 0:
            success = True
            for v in dellist:
                printRecord(v, text.deletePrefix)
                if v[RE_FROMRS]:
                    # recordings created by RS have to be deleted by the RS
                    success &= plugin.service.DeleteRecording(v[RE_RECID])
                else:
                    plugin.executionStatusChangeLock.acquire()
                    try:
                        # all other recordings have to be deleted by DVBViewer
                        if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                            success &= plugin.workerThread.CallWait(
                                partial( plugin.workerThread.DeleteRecording, v[RE_RECID]),
                                CALLWAIT_TIMEOUT
                            )
                        else :
                            success = False
                    finally:
                        plugin.executionStatusChangeLock.release()
                if not success:
                    break
            return success
        else:
            return False


    @eg.LogIt
    def Configure(  self,
        deleteQueryTpl=None
    ) :
        def UpdateQueryFromGuiSettings(q):
            q.deleteByName, q.titleName = q.checkStringArg(deleteByNameCB.GetValue(), titleNameComboCtrl.GetValue())
            q.deleteBySeries, q.seriesName = q.checkStringArg(deleteBySeriesCB.GetValue(), seriesNameComboCtrl.GetValue())
            q.deleteByChannel, q.channelName = q.checkStringArg(deleteByChannelCB.GetValue(), channelNameComboCtrl.GetValue())
            q.deleteByAge, q.minAgeDays = q.checkIntArg(deleteByAgeCB.GetValue(), minAgeNumCtrl.GetValue())
            q.deleteByPlaystatus, q.onlyPlayed = deleteByPlaystatusCB.GetValue(), onlyPlayedCtrl.GetValue()
            q.keepMinimum, q.keepAtLeast = q.checkIntArg(keepMinimumCB.GetValue(), keepAtLeastNumCtrl.GetValue())
            q.dryMode = dryModeCB.GetValue()
            return q

        #plugin = self.plugin
        text = self.Text
        panel = eg.ConfigPanel()
        dlgWindow = panel.GetTopLevelParent()

        # -------------- Get Data, Compute Query -------------------
        recordings, q = self.LoadRecordingsData(deleteQueryTpl)

        # -------------- Event Handlers -------------------
        def onGuiChange(event):
            def backupValues():
                backup = eg.Bunch()
                backup.titleNameStr = titleNameComboCtrl.GetValue()
                backup.titleNamePos = titleNameComboCtrl.GetInsertionPoint()
                backup.seriesNameStr = seriesNameComboCtrl.GetValue()
                backup.seriesNamePos = seriesNameComboCtrl.GetInsertionPoint()
                backup.channelNameStr = channelNameComboCtrl.GetValue()
                backup.channelNamePos = channelNameComboCtrl.GetInsertionPoint()
                return backup

            def restoreValues(backup):
                titleNameComboCtrl.SetValue(backup.titleNameStr)
                titleNameComboCtrl.SetInsertionPoint(backup.titleNamePos)
                seriesNameComboCtrl.SetValue(backup.seriesNameStr)
                seriesNameComboCtrl.SetInsertionPoint(backup.seriesNamePos)
                channelNameComboCtrl.SetValue(backup.channelNameStr)
                channelNameComboCtrl.SetInsertionPoint(backup.channelNamePos)

            # Workaround for an ugly behaviour of wx.ComboBox:
            # When calling 'Layout()' on an arbitrary component in the same frame, the ComboBox
            # performs some very strange autocomplete operation for which I didn't find a way
            # to turn it off (I'd say it's a bug in wx framework?)
            backup = backupValues()

            labelTxt = UpdateQueryFromGuiSettings(q).QueryAsText()
            proseQueryLabel.SetLabel(labelTxt)
            proseQueryLabel.Wrap(minwidth-10)
            hits = self.ComputeQueryResult(recordings, q, silent=True)[0]
            numDeletionsLabel.SetLabel(str(hits))
            numDeletionsLabel.SetInitialSize()
            numDeletionsLabel.GetParent().Layout() # give numDeletionsLabel enough space to grow
                # but this also causes improper autocomplete of wx.ComboBox
            dlgWindow.SetInitialSize()
            dlgWindow.Layout() # let the whole dialog dlgWindow shrink / enlarge

            restoreValues(backup)


        def onDeleteByNameCB(event):
            titleNameComboCtrl.Enable(deleteByNameCB.GetValue())
            if event is not None:
                onGuiChange(event)

        def onDeleteBySeriesCB(event):
            seriesNameComboCtrl.Enable(deleteBySeriesCB.GetValue())
            if event is not None:
                onGuiChange(event)

        def onDeleteByChannelCB(event):
            channelNameComboCtrl.Enable(deleteByChannelCB.GetValue())
            if event is not None:
                onGuiChange(event)

        def onDeleteByAgeCB(event):
            minAgeNumCtrl.Enable(deleteByAgeCB.GetValue())
            if event is not None:
                onGuiChange(event)

        def onDeleteByPlaystatusCB(event):
            onlyPlayedCtrl.Enable(deleteByPlaystatusCB.GetValue())
            onlyUnplayedCtrl.Enable(deleteByPlaystatusCB.GetValue())
            if event is not None:
                onGuiChange(event)

        def onKeepMinimumCB(event):
            keepAtLeastNumCtrl.Enable(keepMinimumCB.GetValue())
            if event is not None:
                onGuiChange(event)

        def onDryModeCB(event):
            if dryModeCB.GetValue():
                proseQueryLabel.SetForegroundColour((0,0,0))
                dryModeHintLabel.Show()
            else:
                proseQueryLabel.SetForegroundColour((255,0,0))
                dryModeHintLabel.Hide()
            if event is not None:
                onGuiChange(event)


        # -------------- GUI Components -------------------
        leftindent = 12
        blockgap = 5
        minwidth = 520

        deleteByNameCB = wx.CheckBox(panel, -1, text.deleteByName)
        deleteByNameCB.SetValue(q.deleteByName)
        deleteByNameCB.Bind(wx.EVT_CHECKBOX, onDeleteByNameCB)
        titleNames = [v[RE_TITLE] for v in recordings.values()]
        titleNames = list(set(titleNames)) # remove duplicates
        titleNames.sort(lambda a,b: cmp(a.lower(), b.lower()))
        titleNameComboCtrl = wx.ComboBox( panel, -1,
            value=q.titleName,
            choices=titleNames,
            size=(300,-1)
        )
        titleNameComboCtrl.Bind(wx.EVT_TEXT, onGuiChange)
        titleNameComboCtrl.Bind(wx.EVT_TEXT_ENTER, onGuiChange)
        titleNameComboCtrl.Bind(wx.EVT_COMBOBOX, onGuiChange)
        titleNameComboCtrl.Bind(wx.EVT_KILL_FOCUS, onGuiChange)

        deleteBySeriesCB = wx.CheckBox(panel, -1, text.deleteBySeries)
        deleteBySeriesCB.SetValue(q.deleteBySeries)
        deleteBySeriesCB.Bind(wx.EVT_CHECKBOX, onDeleteBySeriesCB)
        seriesNames = [v[RE_SERIES] for v in recordings.values()]
        seriesNames = list(set(seriesNames))
        seriesNames.sort(lambda a,b: cmp(a.lower(), b.lower()))
        seriesNameComboCtrl = wx.ComboBox( panel, -1,
            value=q.seriesName,
            choices=seriesNames,
            size=(300,-1)
        )
        seriesNameComboCtrl.Bind(wx.EVT_TEXT, onGuiChange)
        seriesNameComboCtrl.Bind(wx.EVT_TEXT_ENTER, onGuiChange)
        seriesNameComboCtrl.Bind(wx.EVT_COMBOBOX, onGuiChange)
        seriesNameComboCtrl.Bind(wx.EVT_KILL_FOCUS, onGuiChange)

        deleteByChannelCB = wx.CheckBox(panel, -1, text.deleteByChannel)
        deleteByChannelCB.SetValue(q.deleteByChannel)
        deleteByChannelCB.Bind(wx.EVT_CHECKBOX, onDeleteByChannelCB)
        channelNames = [v[RE_CHANNEL] for v in recordings.values()]
        channelNames = list(set(channelNames))
        channelNames.sort(lambda a,b: cmp(a.lower(), b.lower()))
        channelNameComboCtrl = wx.ComboBox( panel, -1,
            value=q.channelName,
            choices=channelNames,
            size=(300,-1)
        )
        channelNameComboCtrl.Bind(wx.EVT_TEXT, onGuiChange)
        channelNameComboCtrl.Bind(wx.EVT_TEXT_ENTER, onGuiChange)
        channelNameComboCtrl.Bind(wx.EVT_COMBOBOX, onGuiChange)
        channelNameComboCtrl.Bind(wx.EVT_KILL_FOCUS, onGuiChange)

        deleteByAgeCB = wx.CheckBox(panel, -1, text.deleteByAge)
        deleteByAgeCB.SetValue(q.deleteByAge)
        deleteByAgeCB.Bind(wx.EVT_CHECKBOX, onDeleteByAgeCB)
        minAgeNumCtrl = panel.SpinNumCtrl(q.minAgeDays, min=0, max=9999, fractionWidth=0, integerWidth=4)
        minAgeNumCtrl.Bind(wx.EVT_TEXT, onGuiChange)

        deleteByPlaystatusCB = wx.CheckBox(panel, -1, text.deleteByPlaystatus)
        deleteByPlaystatusCB.SetValue(q.deleteByPlaystatus)
        deleteByPlaystatusCB.Bind(wx.EVT_CHECKBOX, onDeleteByPlaystatusCB)

        onlyPlayedCtrl = wx.RadioButton( panel, -1, text.onlyPlayed, style = wx.RB_GROUP )
        onlyPlayedCtrl.SetValue( q.onlyPlayed )
        onlyPlayedCtrl.Bind(wx.EVT_RADIOBUTTON, onGuiChange)

        onlyUnplayedCtrl = wx.RadioButton( panel, -1, text.onlyUnplayed )
        onlyUnplayedCtrl.SetValue( not q.onlyPlayed )
        onlyUnplayedCtrl.Bind(wx.EVT_RADIOBUTTON, onGuiChange)

        keepMinimumCB = wx.CheckBox(panel, -1, text.keepMinimum)
        keepMinimumCB.SetValue(q.keepMinimum)
        keepMinimumCB.Bind(wx.EVT_CHECKBOX, onKeepMinimumCB)
        keepAtLeastNumCtrl = panel.SpinNumCtrl(q.keepAtLeast, min=0, max=9999, fractionWidth=0, integerWidth=4)
        keepAtLeastNumCtrl.Bind(wx.EVT_TEXT, onGuiChange)

        dryModeCB = wx.CheckBox(panel, -1, text.dryMode)
        dryModeCB.SetValue(q.dryMode)
        dryModeCB.Bind(wx.EVT_CHECKBOX, onDryModeCB)

        proseQueryLabel = wx.StaticText(panel, -1, "", style = wx.TE_READONLY | wx.TE_LEFT | wx.TE_LINEWRAP)

        numDeletionsLabel = wx.StaticText(panel, -1, "", style=wx.TE_READONLY | wx.TE_LEFT)
        numDeletionsLabel.SetForegroundColour((255,0,0))

        dryModeHintLabel = wx.StaticText(panel, -1, text.dryModeHint, style=wx.TE_READONLY | wx.TE_LEFT)

        # -------------- GUI Layout -------------------
        filterGBSizer = wx.GridBagSizer(hgap=5, vgap=3)
        filterGBrow = 0
        filterGBSizer.Add(wx.Size(0, 5), (filterGBrow, 0))
        filterGBrow += 1

        filterGBSizer.Add(deleteByNameCB, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(leftindent, 0), (filterGBrow, 0))
        filterGBSizer.Add(wx.StaticText(panel, -1, text.titleName), (filterGBrow, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBSizer.Add(titleNameComboCtrl, (filterGBrow, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(0, blockgap), (filterGBrow, 0))
        filterGBrow += 1

        filterGBSizer.Add(deleteBySeriesCB, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(leftindent, 0), (filterGBrow, 0))
        filterGBSizer.Add(wx.StaticText(panel, -1, text.seriesName), (filterGBrow, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBSizer.Add(seriesNameComboCtrl, (filterGBrow, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(0, blockgap), (filterGBrow, 0))
        filterGBrow += 1

        filterGBSizer.Add(deleteByChannelCB, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(leftindent, 0), (filterGBrow, 0))
        filterGBSizer.Add(wx.StaticText(panel, -1, text.channelName), (filterGBrow, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBSizer.Add(channelNameComboCtrl, (filterGBrow, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(0, blockgap), (filterGBrow, 0))
        filterGBrow += 1

        filterGBSizer.Add(deleteByPlaystatusCB, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        innerFGSizer = wx.FlexGridSizer(rows=2, cols=2, hgap=5, vgap=5)
        innerFGSizer.Add(wx.Size(leftindent, 0))
        innerFGSizer.Add(onlyPlayedCtrl, flag = wx.ALIGN_CENTER_VERTICAL)
        innerFGSizer.Add(wx.Size(leftindent, 0))
        innerFGSizer.Add(onlyUnplayedCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBSizer.Add(innerFGSizer, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(0, blockgap), (filterGBrow, 0))
        filterGBrow += 1

        filterGBSizer.Add(deleteByAgeCB, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        innerFGSizer = wx.FlexGridSizer(rows=1, hgap=5, vgap=5)
        innerFGSizer.Add(wx.Size(leftindent, 0))
        innerFGSizer.Add(wx.StaticText(panel, -1, text.minAgeDays1), flag=wx.ALIGN_CENTER_VERTICAL)
        innerFGSizer.Add(minAgeNumCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
        innerFGSizer.Add(wx.StaticText(panel, -1, text.minAgeDays2), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBSizer.Add(innerFGSizer, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(0, blockgap), (filterGBrow, 0))
        filterGBrow += 1

        filterGBSizer.Add(keepMinimumCB, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        innerFGSizer = wx.FlexGridSizer(rows=1, hgap=5, vgap=5)
        innerFGSizer.Add(wx.Size(leftindent, 0))
        innerFGSizer.Add(wx.StaticText(panel, -1, text.keepAtLeast1), flag=wx.ALIGN_CENTER_VERTICAL)
        innerFGSizer.Add(keepAtLeastNumCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
        innerFGSizer.Add(wx.StaticText(panel, -1, text.keepAtLeast2), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBSizer.Add(innerFGSizer, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(0, blockgap), (filterGBrow, 0))
        filterGBrow += 1

        filterGBSizer.Add(dryModeCB, (filterGBrow, 0), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL)
        filterGBrow += 1
        filterGBSizer.Add(wx.Size(0, blockgap), (filterGBrow, 0))
        filterGBrow += 1

        filterSBox = wx.StaticBox(panel, -1, text.filterTitle)
        filterSBoxSizer = wx.StaticBoxSizer(filterSBox, wx.VERTICAL)
        filterSBoxSizer.Add(filterGBSizer, proportion=1, flag=wx.EXPAND)

        # ---- Result Static Box
        resultGBSizer = wx.GridBagSizer(hgap=5, vgap=5)
        resultGBrow = 0

        resultGBSizer.Add(proseQueryLabel, (resultGBrow, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        resultGBrow += 1
        resultGBSizer.Add(wx.Size(0, blockgap), (resultGBrow, 0))
        resultGBrow += 1

        resultFGSizer = wx.FlexGridSizer(rows=1, hgap=5, vgap=5)
        resultFGSizer.Add(wx.StaticText(panel, -1, text.queryResult1), flag=wx.ALIGN_CENTER_VERTICAL)
        resultFGSizer.Add(numDeletionsLabel, flag=wx.ALIGN_CENTER_VERTICAL)
        resultFGSizer.Add(wx.StaticText(panel, -1, text.queryResult2), flag=wx.ALIGN_CENTER_VERTICAL)

        resultGBSizer.Add(resultFGSizer, (resultGBrow, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        resultGBrow += 1
        resultGBSizer.Add(wx.Size(0, blockgap), (resultGBrow, 0))
        resultGBrow += 1

        resultGBSizer.Add(dryModeHintLabel, (resultGBrow, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        resultGBrow += 1

        resultSBox = wx.StaticBox(panel, -1, text.resultTitle)
        resultSBoxSizer = wx.StaticBoxSizer(resultSBox, wx.VERTICAL)
        resultSBoxSizer.Add(resultGBSizer, proportion=1, flag=wx.EXPAND)

        mainGBSizer = wx.GridBagSizer(hgap=5, vgap=5)
        mainGBrow = 0
        mainGBSizer.Add(wx.Size(minwidth, blockgap), (mainGBrow, 0))
        mainGBrow += 1

        mainGBSizer.Add(filterSBoxSizer, (mainGBrow, 0), span=(1, 1), flag=wx.EXPAND)
        mainGBrow += 1
        mainGBSizer.Add(wx.Size(0, blockgap), (mainGBrow, 0))
        mainGBrow += 1

        mainGBSizer.Add(resultSBoxSizer, (mainGBrow, 0), span=(1, 1), flag=wx.EXPAND)
        mainGBrow += 1
        mainGBSizer.Add(wx.Size(0, blockgap), (mainGBrow, 0))
        mainGBrow += 1

        # -------------- Run & show -------------------
        panel.sizer.Add(mainGBSizer, proportion=1, flag=wx.EXPAND)

        onDeleteByNameCB(None)
        onDeleteBySeriesCB(None)
        onDeleteByChannelCB(None)
        onDeleteByAgeCB(None)
        onDeleteByPlaystatusCB(None)
        onKeepMinimumCB(None)
        onDryModeCB(None)
        onGuiChange(None)

        while panel.Affirmed():
            deleteQueryTpl = UpdateQueryFromGuiSettings(q).ToTupel()

            panel.SetResult(
                deleteQueryTpl
            )


    def GetLabel(self,
        deleteQueryTpl,
        *dummyArgs
    ):
        if deleteQueryTpl is None:
            q = self.DeleteQuery() # new query with defaults
        else:
            q = self.DeleteQuery.FromTupel(deleteQueryTpl) # convert tupel into DeleteQuery object

        return q.QueryAsText()



class TuneChannel( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__(self,
        channelID=None,      # 32bit or 64bit channelID
        fromVariable=False,  # get channelID from a variable
        variableName=None    # for example "eg.result"
    ) :
        plugin=self.plugin

        if fromVariable:
            channelID = eval(variableName)

        if channelID is None or channelID == '':
            eg.PrintError("Invalid arguments: missing channelID")
            return False

        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                result = plugin.workerThread.CallWait(
                    partial(plugin.workerThread.TuneChannel, channelID ),
                    CALLWAIT_TIMEOUT
                )
        finally:
            plugin.executionStatusChangeLock.release()
        return result


    def Configure(  self,
        channelID = "",             # 32bit or 64bit channelID (see WIKI for description)
        fromVariable = False,       # get channelID from a variable
        variableName = "eg.result"  # for example "eg.result"
    ) :

        def OnModeSelect( event ) :
            fromVariable = fromVarRadioCtrl.GetValue()
            fromVariableTextCtrl.Enable(fromVariable)
            tvCtrl.Enable(not fromVariable)
            radioCtrl.Enable(not fromVariable)
            channelChoiceCtrl.Enable(not fromVariable)
            channelIDTextCtrl.Enable(not fromVariable)
            event.Skip()

        def OnTvRadioSelect( event ) :
            ix = channelChoiceCtrl.GetSelection()
            if ix != wx.NOT_FOUND :
                if self.tv :
                    plugin.indexTV = ix
                else :
                    plugin.indexRadio = ix

            self.tv = tvCtrl.GetValue()
            if self.tv:
                ix = plugin.indexTV
                self.choices = plugin.tvChannels
            else:
                ix = plugin.indexRadio
                self.choices = plugin.radioChannels
            channelChoiceCtrl.Clear()
            channelChoiceCtrl.SetItems( self.choices )
            channelChoiceCtrl.SetSelection( ix )
            OnChannelChoice(wx.CommandEvent())
            event.Skip()

        def OnChannelChoice(event):
            ix = channelChoiceCtrl.GetSelection()
            key = (ix, self.tv)
            channelID = plugin.channelIDbyIDList[key]
            channelIDTextCtrl.SetValue( channelID )
            event.Skip()

        self.panel = eg.ConfigPanel()
        panel = self.panel
        plugin = self.plugin
        text = self.text

        ix = -1
        if plugin.IDbychannelIDList.has_key( channelID ) :
            key = plugin.IDbychannelIDList[ channelID ]
            ix = key[0]
            self.tv = key[1]
            if ( self.tv ) :
                self.choices = plugin.tvChannels
            else :
                self.choices = plugin.radioChannels
        else :
            self.tv = True
            self.choices = plugin.tvChannels

        channelChoiceCtrl = panel.Choice(ix, choices=plugin.tvChannels + plugin.radioChannels)
        wSize = channelChoiceCtrl.GetSize()
        channelChoiceCtrl.Clear()
        channelChoiceCtrl.SetItems( self.choices )
        channelChoiceCtrl.SetSizeHintsSz( wSize )
        channelChoiceCtrl.SetSelection( ix )
        channelChoiceCtrl.Bind(wx.EVT_CHOICE, OnChannelChoice)

        tvCtrl = wx.RadioButton( panel, -1, text.tvButton, style = wx.RB_GROUP )
        tvCtrl.SetValue( self.tv )
        tvCtrl.SetMinSize((60, -1))
        tvCtrl.Bind(wx.EVT_RADIOBUTTON, OnTvRadioSelect)

        radioCtrl = wx.RadioButton( panel, -1, text.radioButton )
        radioCtrl.SetValue( not self.tv )
        radioCtrl.SetMinSize((60, -1))
        radioCtrl.Bind(wx.EVT_RADIOBUTTON, OnTvRadioSelect)

        chanIdRadioCtrl = wx.RadioButton( panel, -1, text.channelIDDescr, style = wx.RB_GROUP )
        chanIdRadioCtrl.SetValue( not fromVariable )
        chanIdRadioCtrl.Bind(wx.EVT_RADIOBUTTON, OnModeSelect)

        fromVarRadioCtrl = wx.RadioButton( panel, -1, text.fromVariableDescr )
        fromVarRadioCtrl.SetValue( fromVariable )
        fromVarRadioCtrl.Bind(wx.EVT_RADIOBUTTON, OnModeSelect)

        channelIDTextCtrl = wx.TextCtrl( panel, size=(200,-1) )
        channelIDTextCtrl.SetValue( channelID )

        fromVariableTextCtrl = wx.TextCtrl( panel, size=(200,-1) )
        fromVariableTextCtrl.SetValue( variableName )

        boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer.Add(tvCtrl, flag=wx.EXPAND)
        boxSizer.Add(radioCtrl, flag=wx.EXPAND)

        gridBagSizer = wx.GridBagSizer(5, 5)
        rowcount = 0
        gridBagSizer.Add(wx.Size(0, 5), (rowcount, 0))
        rowcount += 1

        # channelID from list
        gridBagSizer.Add(chanIdRadioCtrl, (rowcount, 0), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(20, 0), (rowcount, 0))
        gridBagSizer.Add(boxSizer, (rowcount, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(channelChoiceCtrl, (rowcount, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.StaticText(panel, -1, text.channelID), (rowcount, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        gridBagSizer.Add(channelIDTextCtrl, (rowcount, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(0, 20), (rowcount, 0))
        rowcount += 1

        # channelID from variable
        gridBagSizer.Add(fromVarRadioCtrl, (rowcount, 0), span=(1, 3), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(20, 0), (rowcount, 0))
        gridBagSizer.Add(wx.StaticText(panel, -1, text.variableName), (rowcount, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        gridBagSizer.Add(fromVariableTextCtrl, (rowcount, 2), span=(1, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(0, 5), (rowcount, 0))
        rowcount += 1

        panel.sizer.Add(gridBagSizer, 1, flag=wx.EXPAND)

        OnModeSelect(wx.CommandEvent())

        while panel.Affirmed():
            panel.SetResult( channelIDTextCtrl.GetValue(),
                             fromVarRadioCtrl.GetValue(),
                             fromVariableTextCtrl.GetValue())


    def GetLabel(self, channelID, fromVariable, variableName, *dummyArgs):
        if fromVariable:
            return self.text.name + ": " + variableName
        else:
            return self.text.name + ": " + channelID


class GetChannelDetails( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__(self,
        allChannels=False,    # returns a list of all channels
        currentChannel=False, # returns just the current channel
        channelID=None,       # 32bit or 64bit channelID
        fromVariable=False,   # get channelID from a variable
        variableName=None     # for example "eg.result"
    ) :
        plugin = self.plugin

        if fromVariable:
            channelID = eval(variableName)

        if not allChannels and not currentChannel and (channelID is None or channelID == ""):
            eg.PrintError("Illegal argument combination: One of the arguments 'allChannels', 'currentChannel', 'fromVariable' or 'channelID' must be set.")
            return None

        if allChannels and currentChannel or allChannels and fromVariable or currentChannel and fromVariable:
            eg.PrintError("Illegal argument combination: Just one of the arguments 'allChannels', 'currentChannel' and 'fromVariable' must be True.")
            return None

        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                channelDetails = plugin.workerThread.CallWait(
                    partial(plugin.workerThread.GetChannelDetails, allChannels, currentChannel, channelID ),
                    CALLWAIT_TIMEOUT
                )
        finally:
            plugin.executionStatusChangeLock.release()

        return channelDetails


    def Configure(  self,
        allChannels=False,        # returns a list of all channels
        currentChannel=True,      # returns just the current channel
        channelID="",             # 32bit or 64bit channelID (see WIKI for description)
        fromVariable=False,       # get channelID from a variable
        variableName="eg.result"  # for example "eg.result"
    ) :

        def OnModeSelect( event ) :
            fromChanID = chanIdRadioCtrl.GetValue()
            tvCtrl.Enable(fromChanID)
            radioCtrl.Enable(fromChanID)
            channelChoiceCtrl.Enable(fromChanID)
            channelIDTextCtrl.Enable(fromChanID)
            fromVariable = fromVarRadioCtrl.GetValue()
            fromVariableTextCtrl.Enable(fromVariable)
            event.Skip()

        def OnTvRadioSelect( event ) :
            ix = channelChoiceCtrl.GetSelection()
            if ix != wx.NOT_FOUND :
                if self.tv :
                    plugin.indexTV = ix
                else :
                    plugin.indexRadio = ix

            self.tv = tvCtrl.GetValue()
            if self.tv:
                ix = plugin.indexTV
                self.choices = plugin.tvChannels
            else:
                ix = plugin.indexRadio
                self.choices = plugin.radioChannels
            channelChoiceCtrl.Clear()
            channelChoiceCtrl.SetItems( self.choices )
            channelChoiceCtrl.SetSelection( ix )
            OnChannelChoice(wx.CommandEvent())
            event.Skip()

        def OnChannelChoice(event):
            ix = channelChoiceCtrl.GetSelection()
            key = (ix, self.tv)
            channelID = plugin.channelIDbyIDList[key]
            channelIDTextCtrl.SetValue( channelID )
            event.Skip()

        self.panel = eg.ConfigPanel()
        panel = self.panel
        plugin = self.plugin
        text = self.text

        ix = -1
        if plugin.IDbychannelIDList.has_key( channelID ) :
            key = plugin.IDbychannelIDList[ channelID ]
            ix = key[0]
            self.tv = key[1]
            if ( self.tv ) :
                self.choices = plugin.tvChannels
            else :
                self.choices = plugin.radioChannels
        else :
            self.tv = True
            self.choices = plugin.tvChannels

        channelChoiceCtrl = panel.Choice(ix, choices=plugin.tvChannels + plugin.radioChannels)
        wSize = channelChoiceCtrl.GetSize()
        channelChoiceCtrl.Clear()
        channelChoiceCtrl.SetItems( self.choices )
        channelChoiceCtrl.SetSizeHintsSz( wSize )
        channelChoiceCtrl.SetSelection( ix )
        channelChoiceCtrl.Bind(wx.EVT_CHOICE, OnChannelChoice)

        tvCtrl = wx.RadioButton( panel, -1, text.tvButton, style = wx.RB_GROUP )
        tvCtrl.SetValue( self.tv )
        tvCtrl.SetMinSize((60, -1))
        tvCtrl.Bind(wx.EVT_RADIOBUTTON, OnTvRadioSelect)

        radioCtrl = wx.RadioButton( panel, -1, text.radioButton )
        radioCtrl.SetValue( not self.tv )
        radioCtrl.SetMinSize((60, -1))
        radioCtrl.Bind(wx.EVT_RADIOBUTTON, OnTvRadioSelect)

        allChnlRadioCtrl = wx.RadioButton( panel, -1, text.allChannelsDescr, style = wx.RB_GROUP )
        allChnlRadioCtrl.SetValue( allChannels )
        allChnlRadioCtrl.Bind(wx.EVT_RADIOBUTTON, OnModeSelect)

        currChnlRadioCtrl = wx.RadioButton( panel, -1, text.currentChannelDescr )
        currChnlRadioCtrl.SetValue( currentChannel )
        currChnlRadioCtrl.Bind(wx.EVT_RADIOBUTTON, OnModeSelect)

        chanIdRadioCtrl = wx.RadioButton( panel, -1, text.channelIDDescr )
        chanIdRadioCtrl.SetValue( not allChannels and not currentChannel and not fromVariable )
        chanIdRadioCtrl.Bind(wx.EVT_RADIOBUTTON, OnModeSelect)

        fromVarRadioCtrl = wx.RadioButton( panel, -1, text.fromVariableDescr )
        fromVarRadioCtrl.SetValue( fromVariable )
        fromVarRadioCtrl.Bind(wx.EVT_RADIOBUTTON, OnModeSelect)

        channelIDTextCtrl = wx.TextCtrl( panel, size=(200,-1) )
        channelIDTextCtrl.SetValue( channelID )

        fromVariableTextCtrl = wx.TextCtrl( panel, size=(200,-1) )
        fromVariableTextCtrl.SetValue( variableName )

        boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer.Add(tvCtrl, flag=wx.EXPAND)
        boxSizer.Add(radioCtrl, flag=wx.EXPAND)

        gridBagSizer = wx.GridBagSizer(5, 5)
        rowcount = 0
        gridBagSizer.Add(wx.Size(0, 5), (rowcount, 0))
        rowcount += 1

        # all channels
        gridBagSizer.Add(allChnlRadioCtrl, (rowcount, 0), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(0, 10), (rowcount, 0))
        rowcount += 1

        # current channel
        gridBagSizer.Add(currChnlRadioCtrl, (rowcount, 0), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(0, 10), (rowcount, 0))
        rowcount += 1

        # channel by ID
        gridBagSizer.Add(chanIdRadioCtrl, (rowcount, 0), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(20, 0), (rowcount, 0))
        gridBagSizer.Add(boxSizer, (rowcount, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(channelChoiceCtrl, (rowcount, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.StaticText(panel, -1, text.channelID), (rowcount, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        gridBagSizer.Add(channelIDTextCtrl, (rowcount, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(0, 10), (rowcount, 0))
        rowcount += 1

        # channelID from variable
        gridBagSizer.Add(fromVarRadioCtrl, (rowcount, 0), span=(1, 3), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(20, 0), (rowcount, 0))
        gridBagSizer.Add(wx.StaticText(panel, -1, text.variableName), (rowcount, 1), flag = wx.ALIGN_CENTER_VERTICAL)
        gridBagSizer.Add(fromVariableTextCtrl, (rowcount, 2), span=(1, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        rowcount += 1
        gridBagSizer.Add(wx.Size(0, 5), (rowcount, 0))
        rowcount += 1

        panel.sizer.Add(gridBagSizer, 1, flag=wx.EXPAND)

        OnModeSelect(wx.CommandEvent())

        while panel.Affirmed():
            allChannels = allChnlRadioCtrl.GetValue()
            currentChannel = currChnlRadioCtrl.GetValue()
            channelID = channelIDTextCtrl.GetValue()
            fromVariable = fromVarRadioCtrl.GetValue()
            variableName = fromVariableTextCtrl.GetValue()
            panel.SetResult(
                allChannels,
                currentChannel,
                channelID,
                fromVariable,
                variableName
            )


    def GetLabel(self, allChannels, currentChannel, channelID, fromVariable, variableName, *dummyArgs):
        if allChannels:
            return self.text.name + ": " + self.text.allChannels
        elif currentChannel:
            return self.text.name + ": " + self.text.currentChannel
        elif fromVariable:
            return self.text.name + ": " + variableName
        else:
            return self.text.name + ": " + channelID


class GetCurrentShowDetails( eg.ActionClass ) :
    name = 'Get Details of Current Show'
    description = '''Gets information about the currently played show, either the live TV show or the media playback.
Returns a dictionary with attributes 'title', 'duration', 'remaining'
'''

    @eg.LogItWithReturn
    def __call__(self) :
        plugin = self.plugin

        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( CHECK_CONNECT ) :
                showInfo = plugin.workerThread.CallWait(
                    partial(plugin.workerThread.GetCurrentShowDetails),
                    CALLWAIT_TIMEOUT
                )
            else:
                showInfo = {}
        finally:
            plugin.executionStatusChangeLock.release()

        return showInfo


class GetDataManagerValues( eg.ActionClass ) :
    name = 'Get all DVBViewer data manager values'
    description = '''Gets all available information about the currently played show, EGP, play times etc.
Returns a dictionary
'''

    @eg.LogItWithReturn
    def __call__(self) :
        plugin = self.plugin

        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( CHECK_CONNECT ) :
                showInfo = plugin.workerThread.CallWait(
                    partial(plugin.workerThread.DataManagerGetAllValues),
                    CALLWAIT_TIMEOUT
                )
            else:
                showInfo = {}
        finally:
            plugin.executionStatusChangeLock.release()

        return showInfo



class TaskScheduler( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, enableDVBViewer=True, enableDVBService=False, updateDVBService=False ) :

        plugin = self.plugin

        leadTime = plugin.schedulerLeadTime * 60.0

        timerDates = eg.plugins.DVBViewer.GetDateOfRecordings(
                                                    allRecordings = plugin.scheduleAllRecordings,
                                                    enableDVBViewer = enableDVBViewer,
                                                    enableDVBService = enableDVBService,
                                                    updateDVBService = updateDVBService )

        if not timerDates[0] :
            eg.PrintError( "dates not valid" )
            return False

        dates = []

        if plugin.scheduleAllRecordings :
            dates = timerDates[1]

        elif timerDates[1] > 0 :
            dates = [ timerDates[1] ]

        ts = CoCreateInstance(taskscheduler.CLSID_CTaskScheduler,None,
                              CLSCTX_INPROC_SERVER,
                              taskscheduler.IID_ITaskScheduler)

        tasks=ts.Enum()

        if plugin.numberOfScheduledRecordings < 0 :
            for task in tasks:
                #print task, "    task[0:len(plugin.schedulerTaskNamePrefix)] = ", task[0:len(plugin.schedulerTaskNamePrefix)]
                if task[0:len(plugin.schedulerTaskNamePrefix)] == plugin.schedulerTaskNamePrefix :
                    ts.Delete( task )

            plugin.scheduledRecordings = []

            eg.PrintDebugNotice("All scheduled jobs deleted" )


        actuals = []
        now = time() + leadTime

        for date in plugin.scheduledRecordings :

            if date < 0 :
                continue

            if date not in dates :          # remove deleted recording timers
                ix = plugin.scheduledRecordings.index(date)
                name = plugin.schedulerTaskNamePrefix + "%03d" % ix + ".job"
                if name in tasks :
                    eg.PrintDebugNotice( name + " deleted" )
                    ts.Delete( name )
                plugin.scheduledRecordings[ ix ] = -1.0          #erased
                plugin.numberOfScheduledRecordings -= 1
                #print "deleted: ", no
            else :
                dates[ dates.index(date) ] = -1.0
                if date > now :
                    actuals.append( date )

        for date in dates :

            if date < 0 or date <= now :
                continue

            actuals.append( date )

            # get new index

            ix = 0

            if -1.0 in plugin.scheduledRecordings :
                ix = plugin.scheduledRecordings.index( -1.0 )
                plugin.scheduledRecordings[ ix ] = date
            else :
                ix = len(plugin.scheduledRecordings)
                plugin.scheduledRecordings.append( date )

            #print "added: ", ix
            plugin.numberOfScheduledRecordings += 1

            runTime = localtime(date - leadTime )

            taskName = plugin.schedulerTaskNamePrefix + "%03d" % ix + ".job"

            workItem = ts.NewWorkItem( taskName )

            workItem.SetApplicationName( sys.argv[0] )
            workItem.SetParameters( "-e " + plugin.schedulerEventName )
            workItem.SetPriority( taskscheduler.NORMAL_PRIORITY_CLASS )
            flags = taskscheduler.TASK_FLAG_SYSTEM_REQUIRED | taskscheduler.TASK_FLAG_DELETE_WHEN_DONE
            if plugin.schedulerEntryHidden :
                flags |= taskscheduler.TASK_FLAG_HIDDEN
            workItem.SetFlags( flags )
            workItem.SetAccountInformation(
                                plugin.accounts[INDEX_SCHEDULER][0],
                                plugin.accounts[INDEX_SCHEDULER][1]
                                )

            taskTrigger = workItem.CreateTrigger()[1]
            trigger = taskTrigger.GetTrigger()
            trigger.Flags = 0
            trigger.BeginYear =   runTime.tm_year
            trigger.BeginMonth =  runTime.tm_mon
            trigger.BeginDay =    runTime.tm_mday
            trigger.StartHour =   runTime.tm_hour
            trigger.StartMinute = runTime.tm_min

            trigger.TriggerType = int( taskscheduler.TASK_TIME_TRIGGER_ONCE )
            try :
                #print "SetTrigger"
                taskTrigger.SetTrigger( trigger )
                #print "QueryInterface"
                persistFile = workItem.QueryInterface( IID_IPersistFile )
                #print "Save"
                persistFile.Save( None, True )
            except Exception, exc:
                eg.PrintError( 'Error on adding a task scheduler entry:', unicode(exc) )
                try :
                    ts.Delete( taskName )
                except :
                    pass
                actuals = []
                break

        actuals.sort()

        if len( actuals ) > 0 :
            nextStartup = "Scheduled next wakeup at " + asctime( localtime( actuals[0] - leadTime ) )
            #print nextStartup
            eg.PrintDebugNotice( nextStartup )
            return True
        else :
            #print "No recording scheduled"
            eg.PrintDebugNotice( "No recording scheduled" )
            return False


    def Configure(  self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        self.plugin.ServiceConfigure( enableDVBViewer, enableDVBService, updateDVBService )


class GetDVBViewerObject( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self ) :
        plugin = self.plugin
        if plugin.Connect( WAIT_CHECK_START_CONNECT, lock = True ) :
            return plugin.workerThread.dvbviewer
        return None


class ExecuteDVBViewerCommandViaCOM( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, command, *args, **kwargs ) :
        plugin = self.plugin
        result = None
        plugin.executionStatusChangeLock.acquire()
        try:
            if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                result = plugin.workerThread.CallWait(
                    partial( command, *args, **kwargs ),
                    CALLWAIT_TIMEOUT
                )
        finally:
            plugin.executionStatusChangeLock.release()
        return result


class GetNumberOfClients( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, update=False ) :
        plugin = self.plugin

        if not plugin.useService :
            return -1

        return self.plugin.service.GetNumberOfClients( update )

    def Configure( self, updateDVBService=False ) :

        panel = eg.ConfigPanel()

        text = self.text

        updateCheckBoxCtrl = wx.CheckBox(panel, -1, text.serviceUpdate)
        updateCheckBoxCtrl.SetValue( updateDVBService )

        panel.sizer.Add( updateCheckBoxCtrl )


        while panel.Affirmed():

            panel.SetResult(updateCheckBoxCtrl.GetValue() )


class IsEPGUpdating( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, update=False ) :
        plugin = self.plugin

        if not plugin.useService :
            return False

        return self.plugin.service.IsEPGUpdating( update )


    def Configure( self, updateDVBService=False ) :

        panel = eg.ConfigPanel()

        text = self.text

        updateCheckBoxCtrl = wx.CheckBox(panel, -1, text.serviceUpdate)
        updateCheckBoxCtrl.SetValue( updateDVBService )

        panel.sizer.Add( updateCheckBoxCtrl )


        while panel.Affirmed():

            panel.SetResult(updateCheckBoxCtrl.GetValue() )


class DVBViewerService() :

    def __init__( self, plugin, serviceAddress='127.0.0.1:80',
                  account=( 'admin', 'admin' ),
                  serviceEvent='DVBViewerService') :

        self.serviceAddress = serviceAddress
        self.account = account

        self.timerIDs = {}       #Key: ID, Value: Timer
        self.pseudoIDs = {}
        self.recordingList = {}
        self.numberOfTimers = 0
        self.timerDates = []
        self.activeTimerDates = []

        self.versionDVBViewerService = None

        self.serviceEvent = serviceEvent

        self.failing = False

        self.plugin = plugin

        self.numberOfClients = -1
        self.updateEPG = False

        self.serviceInUse = plugin.serviceInUse


    def TriggerEvent( self, suffix, payload=None ):
            return eg.TriggerEvent( suffix, payload = payload, prefix=self.serviceEvent, source=self.plugin)


    def GetData( self, interface, params=None ) :

        def ErrorProcessing( e ) :
            self.failing = True
            if hasattr(e, 'code') and e.code == 401 :
                eg.PrintError( "Setup error: DVBViewer Service password not correct" )
                return None
            elif hasattr(e, 'errno') :
                if e.errno != 10054 :
                    eg.PrintError( "DVBViewer Service not alive or service address/port are not correct" )
                    self.TriggerEvent( "ServiceNotAlive" )
                    return None
                else :
                    print "DVBViewer Service errno: ", e.errno, ", http code: ", e.code,
                    raise
            else :
                raise
            return

        theurl = 'http://' + self.serviceAddress + '/api/' + interface.lower() + '.html'

        if params is not None:
            first = True
            for k, v in params.iteritems():
                theurl += '?' if first else '&'
                first = False
                theurl += str(k) + '=' + str(v)

        #print "*** URL=", theurl
        req = Request(theurl)

        if self.account[0] != "" :
                authheader = "Basic " + encodestring64( self.account[0] + ':' + self.account[1])[:-1]
                req.add_header("Authorization", authheader)

        try :
            pageHandle = urlopen(req)
            self.failing = False
        except IOError, e :
            ErrorProcessing( e )
            return None

        xml = pageHandle.read()
        pageHandle.close()

        return xml


    @eg.LogIt
    def Update( self, updateMode=UPDATE_TIMERS ) :

        def GetID( *args ) :

            m = hashlib.md5()
            for arg in args:
                m.update(arg.encode("utf-8"))
            result = 0
            for c in m.hexdigest() :
                result = result * 251 + ord(c)

            return result


        def GetText( parent, key, default = '' ) :

            if parent is None :
                #print "Parent not found"
                return default

            element = parent
            if key is not None :
                element = parent.find( key )
            if element is None :
                #print "Key '", key, "' not found"
                return default
            else :
                return element.text

        def GetRSVersion():
            xmlData = self.GetData( 'version' )
            if xmlData is None :
                return False

            # EXAMPLE of xmldata:
            #<?xml version="1.0" encoding="utf-8" ?>
            #<version>DVBViewer Recording Service 1.5.0.2 (beta) (TOWER2008)</version>

            tree = ElementTree.fromstring( xmlData )
            matchObject = reSearch( r'(\d+\.\d+\.\d+\.\d+)', tree.text )
            self.versionDVBViewerService = matchObject.group(1)

        #@eg.LogIt
        def UpdateRSTimers():
            xmlData = self.GetData( 'timerlist' )

            if xmlData is None :
                xmlData = '<?xml version="1.0" encoding="iso-8859-1"?><Timers/>'

            self.timerDates = []
            self.activeTimerDates = []
            self.timerList = []

            #print xmlData

            """
             EXAMPLE of xmldata:

            <?xml version="1.0" encoding="iso-8859-1"?>
            <Timers>
                <Timer Type="1" ID="{FE6AA9F3-1A14-403F-9F3D-13B726A06624}" Enabled="-1"
                    Priority="20" Charset="0" Date="01.03.2012" Start="20:55:00" Dur="85" End="22:20:00" Days="---T---" Action="0">
                  <Descr>Einstein</Descr>
                  <Options AdjustPAT="-1"/>
                  <Format>1</Format>
                  <Folder>Auto</Folder>
                  <NameScheme>%year_%date_%time_%station_%event</NameScheme>
                  <Series>Einstein</Series>
                  <Channel ID="3431745497999804388|SF 1 (deu)"/>
                  <Executeable>-1</Executeable>
                  <Recording>0</Recording>
                  <ID>3</ID>
                  <GUID>{FE6AA9F3-1A14-403F-9F3D-13B726A06624}</GUID>
                </Timer>
            </Timers>
            """

            tree = ElementTree.fromstring( xmlData )

            IDs = {}
            pseudoIDs = {}

            for timer in tree.findall("Timer"):

                enabled     = ( timer.get( "Enabled","-1" ) != '0')
                recording   = ( GetText( timer, "Recording" ) != '0' )
                action      = timer.get( "Action","0" )

                date        = timer.get( "Date","" )
                startTime   = timer.get( "Start","" )
                endTime     = timer.get( "End","" )
                days        = timer.get( "Days", "" )
                channelID   = timer.find( "Channel" ).get( "ID","")
                description = GetText( timer, "Descr" )
                pseudoID    = int( GetText( timer, "ID" ) )

                tStart = mktime( strptime( date + startTime,"%d.%m.%Y%H:%M:%S" ) )
                tEnd   = mktime( strptime( date + endTime,"%d.%m.%Y%H:%M:%S" ) )
                if tEnd < tStart:
                    tEnd += 24 * 60 * 60

                result = GetID( date, startTime, endTime, action, channelID, str( pseudoID ) )

                pseudoIDs[ pseudoID ] = result

                if result not in self.timerIDs :
                    if plugin.oldInterface :
                        self.TriggerEvent( "AddRecord:" + str(pseudoID) )
                    if plugin.newInterface :
                        self.TriggerEvent( "AddRecord", pseudoID )

                IDs[ result ] = ( recording, enabled, pseudoID )

                #print "ID = ", result, "  recording = ", recording, "  IDs[ result ] = ", IDs[ result ]

                timerentry = toTimerEntry(
                    timerID = pseudoID,
                    channelID = channelID.split('|')[0],
                    channelName = channelID.split('|')[1],
                    dateStr = date,
                    startTimeStr = startTime,
                    endTimeStr = endTime,
                    startDateTime = tStart,
                    endDateTime = tEnd,
                    days = days,
                    description = description,
                    enabled = enabled,
                    recording = recording,
                    action = action,
                    fromRS = True
                )
                self.timerList.append(timerentry)

                if enabled and not tStart in self.timerDates:
                    self.timerDates.append(tStart)
                    if recording :
                        self.activeTimerDates.append(tStart)
                    #print "date = ", ctime(tStart)

            numberOfTimers = self.numberOfTimers

            #print self.timerDates
            #print "isRecording = ", isRecording

            if self.timerIDs != IDs :

                for k, v in self.timerIDs.iteritems() :
                    g = IDs.get( k )
                    if v[0] and ( g is None or not g[0] ) :    # last query time recording but not now
                        numberOfTimers -= 1
                        if plugin.oldInterface :
                            self.TriggerEvent( "EndRecord" )
                        if plugin.newInterface :
                            self.TriggerEvent( "EndRecord", ( v[2], numberOfTimers ) )

                for k, v in IDs.iteritems() :
                    g = self.timerIDs.get( k )

                    if v[0] and ( g is None or not g[0] ) :    # last query time not recording but now
                        numberOfTimers += 1
                        if plugin.oldInterface :
                            self.TriggerEvent( "StartRecord" )
                        if plugin.newInterface :
                            self.TriggerEvent( "StartRecord", ( v[2], numberOfTimers ) )

                self.TriggerEvent( "TimerListUpdated" )

                #print "numberOfTimers = ", numberOfTimers
                if numberOfTimers == 0 and self.numberOfTimers != 0 :
                    self.TriggerEvent( "AllActiveRecordingsFinished" )
                self.numberOfTimers = numberOfTimers

                self.timerIDs = IDs
                self.pseudoIDs = pseudoIDs


        #@eg.LogIt
        def UpdateRSStream():
            page = 'status'

            xmlData = self.GetData( page )

            #print xmlData

            # EXAMPLE of xmldata:

            #<?xml version="1.0" encoding="utf-8" ?>
            #<status>
            #   <recordcount>0</recordcount>
            #   <clientcount>0</clientcount>
            #   <epgudate>0</epgudate>
            #</status>

            if xmlData is None :
                xmlData = '<?xml version="1.0" encoding="utf-8" ?><clientcount>0</clientcount>'

            tree = ElementTree.fromstring( xmlData )
            element = tree.find( 'clientcount' )
            numberOfClients = int( GetText( element, None, '0' ) ) - self.numberOfTimers

            if self.numberOfClients != numberOfClients :
                if numberOfClients != 0 :
                    self.TriggerEvent( "NumberOfClientsChanged", numberOfClients )
                else :
                    self.TriggerEvent( "NoClientActive" )
                self.numberOfClients = numberOfClients

            updateEPG = int( GetText( tree, 'epgudate', default = '0' ) ) != 0
            if self.updateEPG != updateEPG :
                if updateEPG :
                    self.TriggerEvent( "UpdateEPGstarted" )
                else :
                    self.TriggerEvent( "UpdateEPGfinished" )
                self.updateEPG = updateEPG



        #@eg.LogIt
        def UpdateRSRecordings():
            xmlData = self.GetData( 'recordings' )

            if xmlData is None :
                xmlData = '<?xml version="1.0" encoding="iso-8859-1"?><recordings/>'

            newRecordingList = {}

            #print xmlData

            """
             EXAMPLE of xmldata:
            <?xml version="1.0" encoding="iso-8859-1" ?>
            <!-- by DVBViewer Recording service -->
            <recordings Ver="1">
                <recording id="2218" idfile="" charset="1" content="32" minimumage="0" startStr="20120524210000" durStr="005000" runtime="000000" epgid="36948">
                    <channel>SF 1 HD (deu)</channel>
                    <file>d:\benutzer\videos\dvbviewer recording service\2012_05-24_20-55-01_sf 1 hd (deu)_einstein.ts</file>
                    <title>Einstein</title>
                    <desc>Moderation: Nicole Ulrich
                        [16:9] [H.264] [HD]
                        [stereo] [deu]
                        [stereo] [deu]
                        [AC-3] [mul]
                        [Teletext subtitles] [deu]</desc>
                    <series>Einstein</series>
                </recording>
            </recordings>

            """

            tree = ElementTree.fromstring( xmlData )

            for recording in tree.findall("recording"):
                recID       = recording.get("id")
                channel     = GetText(recording, "channel")
                startStr    = recording.get("start")
                durStr      = recording.get("duration")
                description = GetText(recording, "desc")
                filename    = GetText(recording, "file")
                title       = GetText(recording, "title")
                series      = GetText(recording, "series")
                played      = None

                startDate = dt.strptime(startStr, '%Y%m%d%H%M%S')
                durSecs = int(durStr[0:2]) * 60 * 60 + int(durStr[2:4]) * 60 + int(durStr[4:6])
                duration = td(seconds=durSecs)
                entry = toRecordingEntry(recID, channel, startDate, description,
                                         duration, filename, played, title, series,
                                         fromRS=True)

                newRecordingList[entry[RE_RECID]] = entry

            if newRecordingList != self.recordingList:
                self.recordingList = newRecordingList
                self.TriggerEvent( "RecordingListUpdated" )


        plugin = self.plugin

        if self.versionDVBViewerService is None:
            GetRSVersion()

        if updateMode & UPDATE_TIMERS != 0 :
            UpdateRSTimers()

        if updateMode & UPDATE_STREAM != 0:
            UpdateRSStream()

        if updateMode & UPDATE_RECORDINGS != 0 :
            UpdateRSRecordings()

        return True


    def UpdateWithLock( self, updateType=UPDATE_TIMERS ) :
        self.serviceInUse.acquire()
        try:
            res = self.Update( updateType )
        finally:
            self.serviceInUse.release()
        return res


    def GetNumberOfClients( self, update=True ) :
        self.serviceInUse.acquire()
        try:
            if update or self.failing :
                self.Update( UPDATE_STREAM )
            res=self.numberOfClients
        finally:
            self.serviceInUse.release()
        return res


    def GetNumberOfActiveRecordings( self, update=True ) :
        self.serviceInUse.acquire()
        try:
            if update or self.failing :
                self.Update( UPDATE_TIMERS )
            res=self.numberOfTimers
        finally:
            self.serviceInUse.release()
        return res


    def IsRecording( self, update=True ) :
        return GetNumberOfActiveRecordings( update ) != 0


    def IsEPGUpdating( self, update=True ) :
        self.serviceInUse.acquire()
        try:
            if update or self.failing :
                self.Update( UPDATE_STREAM )
            res=self.updateEPG
        finally:
            self.serviceInUse.release()
        return res


    def GetTimerList( self, update=True ) :
        self.serviceInUse.acquire()
        try:
            if update or self.failing :
                self.Update( UPDATE_TIMERS )
            res =  self.timerList
        finally:
            self.serviceInUse.release()
        return res


    def GetTimerDates( self, active=True, update=True ) :
        self.serviceInUse.acquire()
        try:
            if update or self.failing :
                self.Update( UPDATE_TIMERS )
            if active :
                res =  self.activeTimerDates
            else :
                res =  self.timerDates
        finally:
            self.serviceInUse.release()
        return res


    def GetTimerIDs( self, update=True ) :
        self.serviceInUse.acquire()
        try:
            if update or self.failing :
                self.Update( UPDATE_TIMERS )
            res = self.timerIDs
        finally:
            self.serviceInUse.release()
        return res


    def GetPseudoIDs( self, update=True ) :
        self.serviceInUse.acquire()
        try:
            if update or self.failing :
                self.Update( UPDATE_TIMERS )
            res = self.pseudoIDs
        finally:
            self.serviceInUse.release()
        return res


    def GetRecordingList( self, update=True ) :
        self.serviceInUse.acquire()
        try:
            if update or self.failing :
                self.Update( UPDATE_RECORDINGS )
            res =  self.recordingList
        finally:
            self.serviceInUse.release()
        return res


    def DeleteRecording(self, recID) :
        self.serviceInUse.acquire()
        try:
            if not self.failing :
                params = { 'recid': recID, 'delfile': '1' }
                self.GetData('recdelete', params)
                return True
            else:
                return False
        finally:
            self.serviceInUse.release()
        return False # error case

    def GetVersion( self ) :
        self.serviceInUse.acquire()
        try:
            if self.versionDVBViewerService is None :
                self.Update( UPDATE_TIMERS )
            res = self.versionDVBViewerService
        finally:
            self.serviceInUse.release()
        return res

