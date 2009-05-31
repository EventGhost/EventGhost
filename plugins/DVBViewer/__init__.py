
SUPPORTED_DVBVIEWER_VERSIONS = '4.0.0.0, 4.1.x.0, '

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

README = (
'Supported DVBViewer versions: ' + SUPPORTED_DVBVIEWER_VERSIONS +
"""
 
The supported DVBViewer actions are documented in
 <a href="http://wiki.dvbviewer.info/index.php/Actions.ini">this wiki</a>
 
This plugin supports following additional actions, which are executed via the COM interface of the DVBViewer: 
<table border="1">
    <tr>
        <th align="right">  <b>Action</b></th>
        <th align="left">   <b>Description</b></th>
    </tr>
    <tr>
        <td align="right">Start</right></td>
        <td>Start DVBViewer</td>
    </tr>
    <tr>
        <td align="right">StopActiveRecordings</td>
        <td>Terminate all active recordings</td>
    </tr>
    <tr>
        <td align="right">GetNumberOfActiveRecordings</td>
        <td>Return value will be the number of active recordings</td>
    </tr>
    <tr>
        <td align="right">IsRecording</td>
        <td>True if there is a recording running</td>
    </tr>
    <tr>
        <td align="right">AddRecording</td>
        <td>Add a recording entry to the DVBViewer timer</td>
    </tr>
    <tr>
        <td align="right">GetDateOfRecordings</td>
        <td>Get the list of recording entries of the timer</td>
    </tr>
    <tr>
        <td align="right">GetRecordingsIDs</td>
        <td>Get a list of recording IDs of the timer</td>
    </tr>
    <tr>
        <td align="right">IsConnected</td>
        <td>True if DVBViewer ist started and connected to the plugin</td>
    </tr>
    <tr>
        <td align="right">UpdateEPG</td>
        <td>Update the EPG database of the DVBViewer</td>
    </tr>
    <tr>
        <td align="right">TaskScheduler</td>
        <td>
            Add the next recording date or all recording dates to the Windows task scheduler
            (The DVBTaskScheduler can be replaced by this method)
        </td>
    </tr>
    <tr>
        <td align="right">SendAction</td>
        <td>
            Send an action to the DVBViewer
            (Values are defined in the action.ini of the DVBViewer)
        </td>
    </tr>
</table>
 
The plugin supports two types of generation events. 
<ol>
    <li>Compatible to the events.of plugin version 1.2</li> 
    <li>The event messages is splited into the event string and the payload.
    In this case, a event can be better interpreted by a python script or command.</li>
</ol>
 
Both types can be used in parallel 
 
  
Following events can be fired:
<table border="1">
    <tr>
        <th align="right">  <b>Event</b></th>
        <th align="center"> <b>Result(s)</b></th>
        <th align="left">   <b>Description</b></th>
    </tr>
    <tr>
        <td align="right"> DVBViewerIsConnected</td>
        <td></td>
        <td>The event gets fired when the DVBViewer is connected to the plugin.</td>
    </tr>
    <tr>
        <td align="right"> Action</td>
        <td align="center">Action ID</td>
        <td>The event gets fired whenever a new action is processed. (Description
            <a href="http://wiki.dvbviewer.info/index.php/Actions.ini"> here</a>)</td>
    </tr>
    <tr>
        <td align="right"> Channel</right></td>
        <td align="center">ChannelNr</td>
        <td>The event gets fired on every channelchange</td>
    </tr>
    <tr>
        <td align="right"> AddRecord</right></td>
        <td align="center">Timer ID</td>
        <td>The event gets fired whenever a new Timer is added.</td>
    </tr>
    <tr>
        <td align="right"> StartRecord</right></td>
        <td align="center">Timer ID, Number of active recordings</td>
        <td>The event gets fired whenever a recording starts.</td>
    </tr>
    <tr>
        <td align="right"> EndRecord</right></td>
        <td align="center">Timer ID, Number of active recordings</td>
        <td>The event gets fired whenever a recording ends.</td>
    </tr>
    <tr>
        <td align="right">AllActiveRecordings<br>Finished</right></td>
        <td align="center"></td>
        <td>The event gets fired whenever the last active recording finishs.</td>
    </tr>
    <tr>
        <td align="right"> Window</right></td>
        <td align="center">OSD Window ID</td>
        <td>The event gets fired whenever a OSD-window is activated.</td>
    <tr>
    <tr>
        <td align="right"> ControlChange</right></td>
        <td align="center">OSD Window ID, Control ID</td>
        <td>The event gets fired whenever an OSD Control gets the focus.</td>
    <tr>
    <tr>
        <td align="right"> SelectedItemChange</right></td>
        <td></td>
        <td>The event gets fired whenever the selectedItem in an OSD list changes.</td>
    <tr>
    <tr>
        <td align="right"> RDS</td>
        <td align="center">RDS Text</td>
        <td>The event gets fired whenever a new RDS Text arrives.</td>
    <tr>
    <tr>
        <td align="right"> Playlist</td>
        <td align="center">Filename</td>
        <td>The event gets fired whenever a new playlistitem starts playing.</td>
    <tr>
    <tr>
        <td align="right"> Playbackstart</td>
        <td align="center"></td>
        <td>The event gets fired whenever a media playback starts.</td>
    <tr>
    <tr>
        <td align="right"> PlaybackEnd</td>
        <td align="center"></td>
        <td>The event gets fired whenever a media playback ends.</td>
    <tr>
    <tr>
        <td align="right"> Close</td>
        <td align="center"></td>
        <td>The event gets fired when the DVBViewer is shutting down.</td>
    <tr>
    <tr>
        <td align="right"> EPGUpdateFinished</td>
        <td align="center"></td>
        <td>The event gets fired whenever the UpdateEPG action finishs.</td>
    <tr>
    <tr>
        <td align="right"> PlaystateChange</td>
        <td align="center">PlayerState</td>
        <td>The event gets fired whenever the play state changes. (PLAY, PAUSE or STOP)</td>
    <tr>
    <tr>
        <td align="right"> RatioChange</td>
        <td align="center">Ratio</td>
        <td>The event gets fired whenever the ratio changes. (133 = 4:3, 178 = 16:9)</td>
    <tr>
    <tr>
        <td align="right"> DisplayChange</td>
        <td align="center">DisplayType</td>
        <td>The event gets fired whenever the display type changes. (NONE, OSD, TV, DVD, MEDIA, SLIDESHOW, TELETEXT)</td>
    <tr>
    <tr>
        <td align="right"> RenderPlaystateChange</td>
        <td align="center">RendererType, PlaysState</td>
        <td>The event gets fired whenever the internal playstate changes.</td>
    <tr>
    <tr>
        <td align="right"> RendererChange</td>
        <td align="center">RendererType</td>
        <td>The event gets fired whenever the renderer changes.</td>
    <tr>
</table>
 
 

Follwing table shows the possible RendererTyes and PlaysStates:

<table border="1">
    <tr>
        <th align="right">  <b>RendererType</b></th>
        <th align="left">   <b>Type of renderer causing the event</b></th>
    </tr>
    <tr>
        <td align="right">-1</td>    
        <td>Ratio changed, PlaysState shows ratio  (only on RenderPlaystateChange event)</td>    
    </tr>
    <tr>
        <td align="right">0</td>    
        <td>Unknown</td>    
    </tr>
    <tr>
        <td align="right">1</td>    
        <td>VideoAudioDVD</td>    
    </tr>
    <tr>
        <td align="right">2</td>    
        <td>DVB</td>    
    </tr>
    <tr>
        <td align="right">3</td>    
        <td>MPG2TS</td>    
    </tr>
</table>


<table border="1">
    <tr>
        <th align="right">  <b>PlaysState</b></th>
        <th align="left">   <b>state changed into</b></th>
    </tr>
    <tr>
        <td align="right">0</td>    
        <td>Stop</td>    
    </tr>
    <tr>
        <td align="right">1</td>    
        <td>Pause</td>    
    </tr>
    <tr>
        <td align="right">2</td>    
        <td>Play</td>    
    </tr>
</table>

This plugin contains a watch dog, which detects if DVBViewer is running
and is synchronising the number of active recordings with the internal recording counter.
The watch dog can be enabled and disabled (Default: disabled) and the period time of
checking can be modified (Default: 60s) in the configuration.

Two different start methods of the DVBViewer are supported and can be selected in the configuration:
<ol>
    <li>Via the COM interface (like plugin version 1.2) (Default)</li> 
    <li>By command line. Solves some DVBViewer plugin problems.</li>
</ol>

"""
)


eg.RegisterPlugin(
    name = "DVBViewer",
    author = "Bitmonster & Stefan Gollmer & Nativityplay",
    version = "2.0." + "$LastChangedRevision$".split()[1],
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds support functions to control <a href="http://www.dvbviewer.com/">'
        'DVBViewer Pro/GE</a> and returns events.'
    ),
    help = README,
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


CALLWAIT_TIMEOUT = 60.0  

DVBVIEWER_WINDOWS = {
    2007: "SLIDESHOW",
    2000: "TELETEXT",
}

DVBVIEWER_CLOSE = ( "Close DVBViewer", 12326)


EVENT_LIST = (
    ("Action",                          "Gets fired whenever a new action is processed"),
    ("Channel",                         "Gets fired on every channelchange"),
    ("AddRecord",                       "Gets fired whenever a new Timer is added"),
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
    ("EPGUpdateFinished",               "Gets fired whenever the UpdateEPG action finishs"),
    ("PlaystateChange",                 "Gets fired whenever the play state changes"),
    ("RatioChange",                     "Gets fired whenever the ratio changes"),
    ("DisplayChange",                   "Gets fired whenever the display type changes"),
    ("RenderPlaystateChange",           "Gets fired whenever the internal playstate changes"),
    ("RendererChange",                  "Gets fired whenever the renderer changes"),
    ("DVBViewerIsConnected",            "Gets fired when the DVBViewer is connected to the plugin"),
    ("DVBViewerCouldNotBeTerminated",   "Gets fired when the DVBViewer couldn't terminated by the plugin"),
    ("DVBViewerCouldNotBeConnected",    "Gets fired when the plugin couldn't connected with the DVBViewer"),
    ("Close",                           "Gets fired when the DVBViewer is shutting down"),
)



ACTIONS = (
    ("OSDMenu",                          "OSD-Menu",                            None,   111),
    ("OSDShowSubtitlemenu",              "OSD-Show Subtitlemenu",               None,  8247),
    ("OSDShowAudiomenu",                 "OSD-Show Audiomenu",                  None,  8248),
    ("OSDLeft",                          "OSD-Left",                            None,  2000),
    ("OSDRight",                         "OSD-Right",                           None,  2100),
    ("OSDUp",                            "OSD-Up",                              None,    78),
    ("OSDDown",                          "OSD-Down",                            None,    79),
    ("OSDOK",                            "OSD-OK",                              None,    73),
    ("OSDRed",                           "OSD-Red",                             None,    74),
    ("OSDGreen",                         "OSD-Green",                           None,    75),
    ("OSDYellow",                        "OSD-Yellow",                          None,    76),
    ("OSDBlue",                          "OSD-Blue",                            None,    77),
    ("OSDFirst",                         "OSD-First",                           None,    80),
    ("OSDLast",                          "OSD-Last",                            None,    81),
    ("OSDPrevious",                      "OSD-Previous",                        None,    82),
    ("OSDNext",                          "OSD-Next",                            None,    83),
    ("OSDClose",                         "OSD-Close",                           None,    84),
    ("OSDPositioning", "OSD-Positioning", None, 85),                        #??????????
    ("OSDClock",                         "OSD-Clock",                           None,  2010),
    ("OSDShowHTPC",                      "OSD-Show HTPC",                       None,  2110),
    ("OSDBackgroundToggle",              "OSD-Background Toggle",               None,  8194),
    ("OSDTeletext",                      "OSD-Teletext",                        None,   101),
    ("OSDShowTimer",                     "OSD-Show Timer",                      None,  8195),
    ("OSDShowRecordings",                "OSD-Show Recordings",                 None,  8196),
    ("OSDShowNow",                       "OSD-Show Now",                        None,  8197),
    ("OSDShowEPG",                       "OSD-Show EPG",                        None,  8198),
    ("OSDShowChannels",                  "OSD-Show Channels",                   None,  8199),
    ("OSDShowFavourites",                "OSD-Show Favourites",                 None,  8200),
    ("OSDShowTimeline",                  "OSD-Show Timeline",                   None,  8201),
    ("OSDShowPicture",                   "OSD-Show Picture",                    None,  8202),
    ("OSDShowMusic",                     "OSD-Show Music",                      None,  8203),
    ("OSDShowVideo",                     "OSD-Show Video",                      None,  8204),
    ("OSDShowNews",                      "OSD-Show News",                       None,  8205),
    ("OSDShowWeather",                   "OSD-Show Weather",                    None,  8206),
    ("OSDShowMiniepg",                   "OSD-Show Miniepg",                    None,  8207),
    ("OSDShowMusicPlaylist",             "OSD-Show Music playlist",             None,  8208),  #???
    ("OSDShowVideoPlaylist",             "OSD-Show Video playlist",             None,  8209),  #???
    ("OSDShowComputer",                  "OSD-Show Computer",                   None,  8210),
    ("OSDShowAlarms",                    "OSD-Show Alarms",                     None,  8212),
    ("OSDCAM",                           "OSD-CAM",                             None,  8259),
    ("PortalSelect",                     "Portal select",                       None,  8254),
    ("Pause",                            "Pause",                               None,     0),
    ("OnTop",                            "On Top",                              None,     1),
    ("HideMenu",                         "Hide Menu",                           None,     2),
    ("ShowStatusbar",                    "Show Statusbar",                      None,     3),
    ("Toolbar",                          "Toolbar",                             None,     4),
    ("Fullscreen",                       "Fullscreen",                          None,     5),
    ("Exit",                             "Exit",                                None,     6),
    ("ClearChannelUsageCounter",         "Clear Channel usage counter",         None,  8255),
    ("Channellist",                      "Channellist",                         None,     7),
    ("ChannelMinus",                     "Channel -",                           None,     8),
    ("ChannelPlus",                      "Channel +",                           None,     9),
    ("ChannelSave",                      "Channel Save",                        None,    10),
    ("Channel0",                         "Channel 0",                           None,    40),
    ("Channel1",                         "Channel 1",                           None,    41),
    ("Channel2",                         "Channel 2",                           None,    42),
    ("Channel3",                         "Channel 3",                           None,    43),
    ("Channel4",                         "Channel 4",                           None,    44),
    ("Channel5",                         "Channel 5",                           None,    45),
    ("Channel6",                         "Channel 6",                           None,    46),
    ("Channel7",                         "Channel 7",                           None,    47),
    ("Channel8",                         "Channel 8",                           None,    48),
    ("Channel9",                         "Channel 9",                           None,    49),
    ("LastChannel",                      "Last Channel",                        None,    63),
    ("ChannelEdit",                      "ChannelEdit",                         None,   117),
    ("ChannelScan",                      "ChannelScan",                         None,   119),
    ("Favourite0",                       "Favourite 0",                         None,    38),
    ("Favourite1",                       "Favourite 1",                         None,    11),
    ("Favourite2",                       "Favourite 2",                         None,    12),
    ("Favourite3",                       "Favourite 3",                         None,    13),
    ("Favourite4",                       "Favourite 4",                         None,    14),
    ("Favourite5",                       "Favourite 5",                         None,    15),
    ("Favourite6",                       "Favourite 6",                         None,    16),
    ("Favourite7",                       "Favourite 7",                         None,    17),
    ("Favourite8",                       "Favourite 8",                         None,    18),
    ("Favourite9",                       "Favourite 9",                         None,    19),
    ("FavouritePlus",                    "Favourite +",                         None,    20),
    ("FavouriteMinus",                   "Favourite -",                         None,    21),
    ("Aspect",                           "Aspect",                              None,    22),
    ("Zoom",                             "Zoom",                                None,    23),
    ("Options",                          "Options",                             None,    24),
    ("Mute",                             "Mute",                                None,    25),
    ("VolumeUp",                         "Volume Up",                           None,    26),
    ("VolumeDown",                       "Volume Down",                         None,    27),
    ("Display",                          "Display",                             None,    28),
    ("Zoom50",                           "Zoom 50%",                            None,    29),
    ("Zoom75",                           "Zoom 75%",                            None,  2013),
    ("Zoom100",                          "Zoom 100%",                           None,    30),
    ("Zoom200",                          "Zoom 200%",                           None,    31),
    ("Desktop",                          "Desktop",                             None,    32),
    ("RecordSettings",                   "Record Settings",                     None,    33),
    ("Record",                           "Record",                              None,    34),
    ("Teletext",                         "Teletext",                            None,    35),
    ("EPG",                              "EPG",                                 None,    37),
    ("TimeShift",                        "TimeShift",                           None,    50),
    ("TimeShiftWindow",                  "TimeShift Window",                    None,    51),
    ("TimeshiftStop",                    "Timeshift Stop",                      None,    52),
    ("KeepTimeshiftFile",                "Keep Timeshift File",                 None,  2012),
    ("RecordedShowsAndTimerStatistics",  "Recorded Shows and Timer statistics", None,  2011),
    ("RefreshRecDB",                     "Refresh RecDB",                       None,  8260),
    ("CleanupRecDB",                     "Cleanup RecDB",                       None,  8261),
    ("CompressRecDB",                    "Compress RecDB",                      None,  8262),
    ("RefreshCleanupCompressRecDB",      "Refresh Cleanup Compress RecDB",      None,  8263),
    ("TitlebarHide",                     "Titlebar Hide",                       None,    54),
    ("BrightnessUp",                     "Brightness Up",                       None,    55),
    ("BrightnessDown",                   "Brightness Down",                     None,    56),
    ("SaturationUp",                     "Saturation Up",                       None,    57),
    ("SaturationDown",                   "Saturation Down",                     None,    58),
    ("ContrastUp",                       "Contrast Up",                         None,    59),
    ("ContrastDown",                     "Contrast Down",                       None,    60),
    ("HueUp",                            "Hue Up",                              None,    61),
    ("HueDown",                          "Hue Down",                            None,    62),
    ("Equalizer",                        "Equalizer",                           None,   116),
    ("Playlist",                         "Playlist",                            None,    64),
    ("PlaylistFirst",                    "Playlist First",                      None,    65),
    ("PlaylistNext",                     "Playlist Next",                       None,    66),
    ("PlaylistPrevious",                 "Playlist Previous",                   None,    67),
    ("PlaylistLoop",                     "Playlist Loop",                       None,    68),
    ("PlaylistStop",                     "Playlist Stop",                       None,    69),
    ("PlaylistRandom",                   "Playlist Random",                     None,    70),
    ("HideAll",                          "Hide All",                            None,    71),
    ("AudioChannel",                     "Audio Channel",                       None,    72),
    ("BestWidth",                        "Best Width",                          None,    89),
    ("Play",                             "Play",                                None,    92),
    ("OpenFile",                         "Open File",                           None,    94),
    ("LastFile",                         "Last File",                           None,   118),
    ("StereoLeftRight",                  "Stereo/Left/Right",                   None,    95),
    ("JumpMinus10",                      "Jump Minus 10",                       None,   102),
    ("JumpPlus10",                       "Jump Plus 10",                        None,   103),
    ("ZoomUp",                           "Zoom Up",                             None,   104),
    ("ZoomDown",                         "Zoom Down",                           None,   105),
    ("StretchHUp",                       "StretchH Up",                         None,   106),
    ("StretchHDown",                     "StretchH Down",                       None,   107),
    ("StretchVUp",                       "StretchV Up",                         None,   108),
    ("StretchVDown",                     "StretchV Down",                       None,   109),
    ("StretchReset",                     "Stretch Reset",                       None,   110),
    ("Previous",                         "Previous",                            None,   112),
    ("Next",                             "Next",                                None,   113),
    ("Stop",                             "Stop",                                None,   114),
    ("RebuildGraph",                     "Rebuild Graph",                       None,    53),
    ("StopGraph",                        "Stop Graph",                          None, 16383),
    ("StopRenderer",                     "Stop Renderer",                       None,  8256),
    ("ShowVideowindow",                  "Show Videowindow",                    None,   821),
    ("ToggleMosaicpreview",              "Toggle Mosaicpreview",                None,  8211),
    ("ShowHelp",                         "Show Help",                           None,  8213),
    ("HideVideowindow",                  "Hide Videowindow",                    None,  8214),
    ("ToggleBackground",                 "Toggle Background",                   None, 12297),
    ("PlayAudioCD",                      "Play AudioCD",                        None,  8257),
    ("PlayDVD",                          "Play DVD",                            None,  8250),
    ("EjectCD",                          "Eject CD",                            None, 12299),
    ("Forward",                          "Forward",                             None, 12304),
    ("Rewind",                           "Rewind",                              None, 12305),
    ("AddBookmark",                      "Add Bookmark",                        None, 12306),
    ("SpeedUp",                          "Speed Up",                            None, 12382),
    ("SpeedDown",                        "Speed Down",                          None, 12383),
    ("ShowPlaylist",                     "Show Playlist",                       None, 12384),
    ("ShowVersion",                      "Show Version",                        None, 16384),
    ("ShowCurrentInfo",                  "Show Current Info",                   None,  8264),
    ("ShowRadioList",                    "Show Radio List",                     None,  8265),
    ("DisableAudio",                     "Disable Audio",                       None, 16385),
    ("DisableAudioVideo",                "Disable AudioVideo",                  None, 16386),
    ("DisableVideo",                     "Disable Video",                       None, 16387),
    ("EnableAudioVideo",                 "Enable AudioVideo",                   None, 16388),
    ("VideoOutputAB",                    "Video Output A/B",                    None,   132),
    ("AudioOutputAB",                    "Audio Output A/B",                    None,   133),
    ("WindowMinimize",                   "WindowMinimize",                      None, 16382),
    ("WindowRestore",                    "WindowRestore",                       None, 16397),
    ("Screenshot",                       "Screenshot",                          None,   115),
    ("ZoomlevelStandard",                "Zoomlevel Standard",                  None, 16389),
    ("Zoomlevel0",                       "Zoomlevel 0",                         None, 16390),
    ("Zoomlevel1",                       "Zoomlevel 1",                         None, 16391),
    ("Zoomlevel2",                       "Zoomlevel 2",                         None, 16392),
    ("Zoomlevel3",                       "Zoomlevel 3",                         None, 16393),
    ("ZoomlevelToggle",                  "Zoomlevel Toggle",                    None, 16394),
    ("TogglePreview",                    "Toggle Preview",                      None, 16395),
    ("RestoreDefaultColors",             "Restore Default Colors",              None, 16396),
    ("DVDMenu",                          "DVD Menu",                            None,  8246),
    ("ShutdownCard",                     "Shutdown Card",                       None, 12327),
    ("ShutdownMonitor",                  "Shutdown Monitor",                    None, 12328),
    ("Hibernate",                        "Hibernate",                           None, 12323),
    ("Standby",                          "Standby",                             None, 12324),
    ("Slumbermode",                      "Slumbermode",                         None, 12325),
    ("Reboot",                           "Reboot",                              None, 12329),
    ("Shutdown",                         "Shutdown",                            None, 12325),
    ("Exit",                             "Exit",                                None, 12294),
    ("ServiceStandby",                   "Service Standby",                     None,  8272),
    ("ServiceHibernate",                 "Service Hibernate",                   None,  8274),
    ("ServiceShutdown",                  "Service Shutdown",                    None,  8273),
    ("ServiceWakeOnLAN",                 "Service Wake on LAN",                 None,  8275),
    ("ServiceGetEPG",                    "Service get EPG",                     None,  8276)
)




windowDVBViewer = eg.WindowMatcher( u'dvbviewer.exe',
                                    winName=u'DVB Viewer',
                                    timeout=20 )



import sys
import os
import random
import hashlib
from pythoncom import CoInitialize, CoUninitialize
from pythoncom import CoCreateInstance, CLSCTX_INPROC_SERVER, IID_IPersistFile
from pywintypes import Time as PyTime
import wx.lib.masked as masked
from functools import partial
from win32com.client import Dispatch, DispatchWithEvents
from win32com.client.gencache import EnsureDispatch
from win32com.client import GetObject
from win32com.taskscheduler import taskscheduler
from eg.WinApi import SendMessageTimeout
from threading import Thread, Event, Timer, Lock
from time import sleep, time, strptime, mktime, ctime, strftime, localtime, asctime
from eg.WinApi.Dynamic import (
    byref, sizeof, CreateProcess, WaitForSingleObject, FormatError,
    CloseHandle, create_unicode_buffer, 
    STARTUPINFO, PROCESS_INFORMATION, 
    CREATE_NEW_CONSOLE, STARTF_USESHOWWINDOW
)


class Text:
    interfaceBox          = "Interface API"
    useComApi             = "COM-API (for DVBViewer Pro)"
    useSendMessage        = "SendMessage-API (for DVBViewer GE)"
    eventType             = "Events"
    useOldEvents          = "Events of version 1.2"
    useNewEvents          = "New event definitions"
    eventFormat           = "Event format"
    playStateFormat       = "PlayState format"
    displayChangeFormat   = "DisplayChange format"
    long                  = "Long "
    short                 = "Short"
    dvbViewerStart        = "Start DVBViewer"
    useCommandLine        = "by command line (if the COM interface should also be used by other applications)"
    dvbviewerFile         = "Filepath of DVBViewer (if started by command line):"
    dvbviewerArguments    = "Arguments: "
    dvbviewerBox          = "Choose the DVBViewer"
    watchDog              = "Watch dog"
    useWatchDog           = "Enable"
    watchDogTime          = "Watch dog cycle time: "
    taskSchedulerInfo     = "Task scheduler information"
    accountName           = "Account name: "
    password1             = "Password: "
    password2             = "Repeat password: "
    changePassword        = "Change password"
    schedulerPrefix       = "Task name prefix: "
    schedulerEvent        = "Event: "
    schedulerLead         = "Lead time [min]: "
    scheduleAllRecordings = "All recordings"
    schedulerEntryHidden  = "Hidden"


    class Start :
        name = "Start DVBViewer"
        description = "Start DVBViewer through COM-API. For DVBViewer Pro only."

    class CloseDVBViewer :
        name = DVBVIEWER_CLOSE[0]
        checkBoxText = "Wait until DVBViewer is terminated"

    class StopAllActiveRecordings :
        name = "Stop all active recordings"
        description = "Remove all active recordings from the timer list."

    class SendAction :
        name   = "Send action to DVBViewer"
        action = "Action: "

    class GetDateOfRecordings :
        name = "Get dates of next recordings"
        description =   (   
                            "Return the date(s) of the recordings as a floating "
                            "point number expressed in seconds since the epoch, in UTC."
                            "The date is negative if no recording is planed."
                        )
        all = "Get dates of all recodings"

    class GetRecordingsIDs :
        name   = "Get IDs of recordings"
        active = "Get only IDs of active recordings"

    class UpdateEPG :
        name = "Update EPG"
        description =   (   
                            "For updating, one channel change for each transponder/booklet"
                            "will be done. If a recording is active, the executing of the EPG"
                            "update will be delayed until the recording is finished."
                        )
        disableAV             = "Disable AV"
        time = "Time between channel change: "
    
    class AddRecording :
        name = "Add recording to the timer"
        description = (
                    'Add a recording to the timer list. This action should '
                    'be used by scripts or other plugins. The configuration '
                    'tool is only for demonstration.'
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
                    'Add the DVBViewer timer list entries to the Windows task scheduler.'
                    ' To use this feature, the account name and the password should be entered'
                    ' in the configuration of the DVBViewer plugin. The password is written'
                    ' encryped in the file "DVBViewerAccount.dat" located in the event ghost user'
                    ' directory.'
                    )




class EventHandler:

    # The event gets fired whenever a new action is processed. 
    # Parameter :
    #       ActionID        ID of the action ( see actions.ini in the DVBViewer folder)
    #
    
    def __init__( self ) :
        self.lastActiveChannelNr = -1
    
    def OnonAction(self, ActionID):
        plugin = self.plugin
        if plugin.oldInterface :
            self.TriggerEvent("Action:" + str(ActionID))
        if plugin.newInterface :
            self.TriggerEvent("Action", ActionID )


    # The event gets fired on every channelchange.
    # Parameter :
    #       ChannelNr       The new channel number.
    #
    def OnChannelChange(self, ChannelNr):
        def DisableAV() :
            #print "DisableAV"
            CoInitialize()
            self.plugin.SendCommand( 16386 )
            CoUninitialize()
        plugin = self.plugin
        self.TriggerEvent("Channel", ChannelNr)
        plugin.actualChannel = ChannelNr
        plugin.UpdateDisplayMode()
        if ChannelNr != -1 :
            if plugin.timerEPG and ChannelNr != self.lastActiveChannelNr and plugin.EPGdisableAV :
                #print "DisableAV", ChannelNr
                disableAVTimer = Timer( 3.0, DisableAV )
                disableAVTimer.start()
            self.lastActiveChannelNr = ChannelNr




    # The event gets fired whenever a new Timer is added.
    # Parameter :
    #       ID              ID of the newly added timer. 
    #
    def OnonAddRecord(self, ID):
        plugin = self.plugin
        if plugin.oldInterface :
            self.TriggerEvent( "AddRecord:" + str(ID) )
        if plugin.newInterface :
            self.TriggerEvent( "AddRecord", ID )


    # The event gets fired whenever a recording starts. 
    # Parameter :
    #       ID                          ID of the timer. 
    #       numberOfActiveRecordings    Number of recordings which are now active
    #
    @eg.LogIt
    def OnonStartRecord(self, ID):
        self.plugin.UpdateRecordingsByDVBViewerEvent( ID )


    # The event gets fired whenever a recording ends.
    # Parameter :
    #       numberOfActiveRecordings    Number of recordings which are still active
    #
    @eg.LogIt
    def OnonEndRecord(self):
        self.plugin.UpdateRecordingsByDVBViewerEvent()


    # The event gets fired whenever a OSD-window is activated. 
    # Parameter :
    #       WindowID        ID of the OSD-window.
    #
    def OnonOSDWindow(self, WindowID):
        plugin = self.plugin
        plugin.actualWindowID = WindowID
        if plugin.oldInterface :
            self.TriggerEvent("Window:" + str(WindowID))
        if plugin.newInterface :
            self.TriggerEvent("Window", WindowID )
        plugin.UpdateDisplayMode()


    # The event gets fired whenever an OSD Control gets the focus. 
    # Parameters
    #       WindowID        ID of the OSD window the control belongs to. 
    #       ControlID       ID of the OSD-control.
    #
    def OnonControlChange(self, WindowID, ControlID):
        plugin = self.plugin
        if plugin.oldInterface :
            self.TriggerEvent("ControlChange:WindID" + str(WindowID) + "ContrID"+ str(ControlID))
        if plugin.newInterface :
            self.TriggerEvent("ControlChange", ( WindowID, ControlID ))


    # The event gets fired whenever the selectedItem in an OSD list changes.
    #
    def OnonSelectedItemChange(self):
        self.TriggerEvent("SelectedItemChange")


    # The event gets fired whenever a new RDS Text arrives. 
    # Parameters
    #       RDS             The RDS text.
    #
    def OnonRDS(self, RDS):
        plugin = self.plugin
        if plugin.oldInterface :
            self.TriggerEvent("RDS:" + unicode(RDS))
        if plugin.newInterface :
            self.TriggerEvent("RDS", unicode(RDS))


    # The event gets fired whenever a new playlistitem starts playing. 
    # Parameter :
    #       Filename        Filename of the starting playlistitem. 
    #
    def OnonPlaylist(self, Filename):
        self.TriggerEvent("Playlist", str(Filename))


    # The event gets fired whenever a media playback starts.
    #
    def OnonPlaybackstart(self):
        thread = self.plugin.workerThread
        thread.Call( partial( thread.ProcessMediaplayback ) )
        


    # The event gets fired whenever a media playback ends.
    #
    def OnPlaybackEnd(self):
        thread = self.plugin.workerThread
        thread.Call( partial( thread.ProcessMediaplayback ) )


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
    def OnPlaystatechange(self, RendererType, State):
        plugin = self.plugin
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


    # The event gets fired when the DVBViewer is shutting down.
    @eg.LogIt
    def OnonDVBVClose(self):
        plugin = self.plugin
        plugin.terminateThread = DVBViewerTerminateThread( self.plugin )
        plugin.terminateThread.start()
        #pass
        


terminateTimeOut = 120




class DVBViewerTerminateThread( Thread ) :

    def __init__( self, plugin ) :
    
        Thread.__init__(self, name="DVBViewerTerminateThread")
        self.plugin = plugin



    @eg.LogItWithReturn
    def run(self) :
        plugin = self.plugin
        if plugin.workerThread:
            if plugin.workerThread.Stop( terminateTimeOut ) :
                eg.PrintError("Could not terminate DVBViewer thread")
                plugin.TriggerEvent( "DVBViewerCouldNotBeTerminated" )
                plugin.workerThread = None
        CoInitialize()
        WMI = GetObject('winmgmts:')
        
        events = WMI.ExecNotificationQuery(
                        "SELECT * FROM __InstanceDeletionEvent  WITHIN 0.1 "
                        "WHERE TargetInstance ISA 'Win32_Process' "
                        "AND TargetInstance.Name='dvbviewer.exe'" )
                        
        finished = True

        if len( WMI.ExecQuery('select * from Win32_Process where Name="dvbviewer.exe"') ) > 0 :
        
            try :
                events.NextEvent( terminateTimeOut * 1000 )

            except :

                eg.PrintDebugNotice("DVBViewer could not be terminated")
                plugin.TriggerEvent( "DVBViewerCouldNotBeTerminated" )
                finished = False

        if finished :
            plugin.DVBViewerIsFinished()

        del events
        del WMI
        CoUninitialize()
        plugin.terminateThread = None




class DvbViewerWorkerThread(eg.ThreadWorker):
    """
    Handles the COM interface in a thread of its ownn
    """
    
    @eg.LogItWithReturn
    def Setup(self, plugin):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin
        
        self.dvbviewer                 = None
        self.comObj_IDVBViewerEvents   = None
        
        self.dvbviewer = EnsureDispatch("DVBViewerServer.DVBViewer")
        # try if we can get an attribute from the COM instance
        self.dvbviewer.CurrentChannelNr
        com_IDVBViewerEvents = self.dvbviewer.Events
        self.comObj_IDVBViewerEvents = DispatchWithEvents(com_IDVBViewerEvents, self.plugin.EventHandler)
        plugin.TriggerEvent( "DVBViewerIsConnected" )
        plugin.InitAfterDVBViewerConnected()



    @eg.LogIt
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        if self.comObj_IDVBViewerEvents :
            del self.comObj_IDVBViewerEvents
        if self.dvbviewer :
            del self.dvbviewer
        self.plugin.workerThread = None



    def GetCurrentChannelNr( self ) :
        return self.dvbviewer.CurrentChannelNr


    def GetChannelList( self ) :
        channelManager = self.dvbviewer.ChannelManager
        return channelManager.GetChannelList( )



    @eg.LogItWithReturn
    def TuneChannelIfNotRecording( self, channelNr, text = "", time = 0.0) :
        dvbviewer = self.dvbviewer
        timerCollection = dvbviewer.TimerManager
        
        if not timerCollection.Recording :
            dvbviewer.CurrentChannelNr = channelNr
            if text != "" :
                dvbviewer.OSD.ShowInfoinTVPic( text, time * 1000 + 2000 )
            return True
        else :
                return False



    @eg.LogIt
    def StopAllActiveRecordings( self ) :
        timerManager = self.dvbviewer.TimerManager
        list = timerManager.GetTimerList( )
        for record in list[1] :
            #print "Record = ", record
            #print "Recording: ", record[ 11 ]
            if record[ 11 ] :
                #print "Recording terminated"
                timerManager.StopRecording( record[ 4 ] )
            else :
                #print "Recording not terminated"
                pass



    @eg.LogIt
    def GetAllRecordings( self ) :
        timerManager = self.dvbviewer.TimerManager
        return timerManager.GetTimerList( )



    def GetRecordingsIDs( self, active = True ) :
        timerManager = self.dvbviewer.TimerManager
        list = timerManager.GetTimerList( )
        if active :
            IDs = [ record[ 4 ] for record in list[1] if record[ 11 ] ]
        else :
            IDs = [ record[ 4 ] for record in list[1] ]
        return IDs



    # This method is necessary in case of a DVBViewer bug (Too many OnPlaybackEnd events )
    # DVBViewer Version: 3.9.4.0
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



    def IsDVD( self ) :
        return self.dvbviewer.isDVD



    def AddRecording( self,
                      channelID, 
                      date,                 # dd.mm.yyyy
                      startTime,            # hh:mm
                      endTime,              # hh:mm
                      description = "",
                      disableAV = False,
                      enabled = True,
                      recAction = 0,        # intern = 0, tune only = 1, 
                                            # AudioPlugin = 2, Videoplugin = 3 
                                            
                      actionAfterRec = 0,   # No action = 0, PowerOff = 1, 
                                            # Standby = 2, Hibernate = 3, Close = 4,
                                            # Playlist = 5, Slumbermode: = 6 
                      days = "-------"
                      ) :

        pDate = PyTime( strptime( date, "%d.%m.%Y" ) )

        pStart = PyTime( strptime( startTime, "%H:%M" ) ) #- PyTime( strptime( "00:00", "%H:%M" ) )
        pEnd   = PyTime( strptime( endTime,   "%H:%M" ) ) #- PyTime( strptime( "00:00", "%H:%M" ) )
        
        timerItem = self.dvbviewer.TimerManager.AddItem( channelID, pDate, pStart, pEnd, 
                                             description, disableAV, enabled, 
                                             recAction, actionAfterRec, days )
                                             
        return timerItem.ID



#connectionMode:
WAIT_CHECK_START_CONNECT  = 0   #wait for free, check if executing, start if not executing, connect
CONNECT                   = 1   #connect
CHECK_CONNECT             = 2   #connect only, if executing




class DVBViewerWatchDogThread( Thread ) :

    def __init__( self, plugin, watchDogTime ) :
    
        Thread.__init__(self, name="DVBViewerWatchDogThread")
        self.plugin = plugin
        self.abort = False
        self.watchDogTime = watchDogTime
        self.started = False
        self.event = Event()



    @eg.LogItWithReturn
    def run(self) :
        plugin = self.plugin
        CoInitialize()
        
        queryTime = 5
        
        if self.watchDogTime < queryTime :
            queryTime = self.watchDogTime
            
        query = (
                "SELECT * FROM __InstanceOperationEvent  WITHIN " + str( queryTime) +
                " WHERE TargetInstance ISA 'Win32_Process' "
                "AND TargetInstance.Name='dvbviewer.exe'" )
                
        WMI = GetObject('winmgmts:')
        
        eventSource = WMI.ExecNotificationQuery( query )
        
        self.started = len( WMI.ExecQuery('select * from Win32_Process where Name="dvbviewer.exe"') ) > 0

        nextTime = time()

        while not self.abort :
            try :
                eventType = eventSource.NextEvent( 500 ).Path_.Class
                if eventType == '__InstanceCreationEvent':
                    self.started = True
                    #print "DVBViewer started"
                elif eventType == '__InstanceDeletionEvent':
                    self.started = False
                    #print "DVBViewer terminated"
                elif time() < nextTime :
                    continue
            except :
                #print "Timeout"
                if time() < nextTime :
                    continue
                    
            nextTime = time() + self.watchDogTime
            
            if not plugin.terminateThread and not plugin.connecting:
                if not self.started and plugin.workerThread and not plugin.terminateThread :
                    eg.PrintDebugNotice( "Termination of DVBViewer detected by watch dog" )
                    if plugin.workerThread.Stop( terminateTimeOut ) :
                        eg.PrintError("Could not terminate DVBViewer thread")
                    plugin.workerThread = None
                    plugin.DVBViewerIsFinished()
                elif self.started and not plugin.workerThread :
                    eg.PrintDebugNotice( "DVBViewer will be connected by watch dog" )
                    plugin.Connect( CONNECT )
                elif plugin.workerThread :
                    #print "Look for active recordings"
                    try :
                        updatedRecordings = plugin.UpdateRecordings()
                    except :
                        eg.PrintDebugNotice("DVBViewer could not accessed by the Watch Dog Thread")
                        plugin.TriggerEvent( "DVBViewerCouldNotBeConnected" )
                    else :
                        if updatedRecordings > 0 :
                            eg.PrintDebugNotice(    "Number of recordings ("
                                                  + str(updatedRecordings)
                                                  + ") was updated  by watch dog" )
        del eventSource
        del WMI
        CoUninitialize()



    @eg.LogIt
    def Finish( self ) :
        self.abort = True
        self.event.set()




class DVBViewer(eg.PluginClass):
    text = Text
    
    def __init__(self):
        self.AddEvents(*EVENT_LIST)
        self.AddAction(Start)
        self.AddAction(CloseDVBViewer)
        self.AddAction(StopAllActiveRecordings)
        self.AddAction(GetNumberOfActiveRecordings)
        self.AddAction(IsRecording)
        self.AddAction(AddRecording)
        self.AddAction(GetDateOfRecordings)
        self.AddAction(GetRecordingsIDs)
        self.AddAction(IsConnected)
        self.AddAction(UpdateEPG)
        self.AddAction(TaskScheduler)
        self.AddAction(SendAction)
        self.AddAction(GetDVBViewerObject, hidden = True)
        self.AddAction(ExecuteDVBViewerCommandViaCOM, hidden = True)
        
        class ActionPrototype(eg.ActionClass):
            def __call__(self2):
                return self.SendCommand(self2.value)
        self.AddActionsFromList(ACTIONS, ActionPrototype)
            
        # create a new subclass of the EventHandler with the ability to use 
        # the plugin's TriggerEvent method
        class SubEventHandler(EventHandler):
            plugin = self
            TriggerEvent = self.TriggerEvent
        self.EventHandler = SubEventHandler
        self.workerThread = None
        self.connecting = False
        self.checking = False
        self.watchDogThread = None
        
        self.oldInterface = False
        self.newInterface = True
        self.startDVBViewerByCOM = False,
        self.pathDVBViewer = ""
        
        #new status variables
        self.DVBViewerStartedByCOM = False
        
        self.numberOfActiveRecordings = 0
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

        self.frequencies = {}

        self.indexTV    = 0
        self.indexRadio = 0

        self.timerEPG = None
        self.EPGdisableAV = True

        self.terminateThread = None
        
        self.account  = ""
        self.password = ""
        self.key = []
        self.scheduledRecordings = []
        self.numberOfScheduledRecordings = -1
        self.updateRecordingsThread = None
        self.updateRecordingsLock = Lock()



    @eg.LogIt
    def InitAfterDVBViewerConnected( self ) :
        thread = self.workerThread
        self.actualChannel     = thread.GetCurrentChannelNr()
        self.numberOfActiveRecordings = 0
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
        thread.ProcessMediaplayback()
        self.UpdateDisplayMode()



    @eg.LogIt
    def __start__(  self,
                    useSendMessage=False, 
                    oldInterface = True,
                    newInterface = False,
                    startDVBViewerByCOM = True,
                    pathDVBViewer = "",
                    argumentsDVBViewer = "",
                    longDisplay = True,
                    shortDisplay = False,
                    longPlayState = True,
                    shortPlayState = False,
                    watchDogEnable = False,
                    watchDogTime = 60.0,
                    schedulerTaskNamePrefix = "StartRecording",
                    schedulerEventName      = "StartRecording",
                    schedulerLeadTime       = 3.0,
                    scheduleAllRecordings   = False,
                    schedulerEntryHidden    = False
                    ) :
        if useSendMessage:
            self.SendCommand = self.SendCommandThroughSendMessage
        else:
            self.SendCommand = self.SendCommandThroughCOM
            if watchDogEnable :
                self.watchDogThread = DVBViewerWatchDogThread( self, watchDogTime )
                self.watchDogThread.start()
        self.oldInterface = oldInterface
        self.newInterface = newInterface
        self.startDVBViewerByCOM = startDVBViewerByCOM
        self.pathDVBViewer       = eg.ParseString(pathDVBViewer)
        self.argumentsDVBViewer  = eg.ParseString(argumentsDVBViewer)
        self.longDisplayEvent    = longDisplay
        self.shortDisplayEvent   = shortDisplay
        self.longPlayStateEvent  = longPlayState
        self.shortPlayStateEvent = shortPlayState
        
        self.account, self.password  = self.HandlePasswordFile()
        self.schedulerTaskNamePrefix = schedulerTaskNamePrefix
        self.schedulerEventName      = schedulerEventName
        self.schedulerLeadTime       = schedulerLeadTime
        self.scheduleAllRecordings   = scheduleAllRecordings
        self.schedulerEntryHidden    = schedulerEntryHidden
        
        self.scheduledRecordings = []
        self.numberOfScheduledRecordings = -1
        
        self.firedRecordingsIDs = []
        
        eg.PrintDebugNotice( "DVBViewer plugin started on " + strftime("%d %b %Y %H:%M:%S", localtime() ))
        
        return True



    @eg.LogIt
    def __stop__(self):
        # If the DVBViewer was started by the COM interface, the DVBViewer must be terminated before
        # stopping the DVBViewer Thread. Otherwise the DVBViewer is going into an endless loop.
        if self.workerThread:
            if self.DVBViewerStartedByCOM :
                StopAllActiveRecordings()
                self.SendCommand(12326)             # Close DVBViewer
                count = terminateTimeOut / 0.1
                while self.workerThread:
                    sleep( 0.1 )
                    count -= 1
                    if count == 0 :
                        eg.PrintError("Could not terminate DVBViewer thread")
                        break
            else :
                if self.workerThread.Stop( terminateTimeOut ) :
                    eg.PrintError("Could not terminate DVBViewer thread")
        
        if self.watchDogThread :
            self.watchDogThread.Finish()
            self.watchDogThread.join()
            self.watchDogThread = None
        
        if self.timerEPG :
            self.timerEPG.cancel()
        
        return True



    def DVBViewerIsFinished( self ) :
        self.UpdateRecordings()
        self.TriggerEvent( "Close" )



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



    def UpdateRecordingsByDVBViewerEvent( self, ID = -1 ) :
    
        class UpdateRecordingsThread( Thread ) :


            def __init__( self, plugin, ID ) :

                Thread.__init__(self, name="DVBViewerUpdateRecordingsThread")
                self.plugin = plugin
                self.ID = ID
                self.update = True


            @eg.LogItWithReturn
            def run(self) :
                plugin = self.plugin
                lock = plugin.updateRecordingsLock
                lock.acquire()
                while self.update :
                    self.update = False
                    lock.release()
                    plugin.UpdateRecordings( self.ID )
                    lock.acquire()
                plugin.updateRecordingsThread = None
                lock.release()
                
            def repeat( self ) :
                self.update = True

        lock = self.updateRecordingsLock
        lock.acquire()
        if ID >= 0 and not self.updateRecordingsThread :
            if ID not in self.firedRecordingsIDs :
                self.numberOfActiveRecordings += 1
                if self.oldInterface :
                    self.TriggerEvent( "StartRecord" )               
                if self.newInterface :
                    self.TriggerEvent( "StartRecord", ( ID, self.numberOfActiveRecordings ) )
                self.firedRecordingsIDs.append( ID )
            lock.release()
            return True

        if self.updateRecordingsThread :
            self.updateRecordingsThread.repeat()
            lock.release()
            return True

        self.updateRecordingsThread = UpdateRecordingsThread( self, ID )    #A thread is necessary in case of a DVBViewer dead lock
        lock.release()
            
        self.updateRecordingsThread.start()
        
        return True



            
    def UpdateRecordings( self, ID = -1 ) :
        if self.workerThread :
            recordingsIDs = self.workerThread.CallWait(
                        partial(self.workerThread.GetRecordingsIDs ),
                        CALLWAIT_TIMEOUT
            )
        else :
            recordingsIDs = []
        numberOfActiveRecordings = len( recordingsIDs )
        
        newRecordingsIDs     = [ ID for ID in recordingsIDs if ID not in self.firedRecordingsIDs ]
        #print "newRecordingsIDs = ", newRecordingsIDs
        
        if self.numberOfActiveRecordings == numberOfActiveRecordings and len( newRecordingsIDs ) == 0:
            return 0
        
        deletedRecordingsIDs = [ ( count, ID ) for count, ID in enumerate( self.firedRecordingsIDs ) if ID not in recordingsIDs ]
        #print "deletedRecordingsIDs = ", deletedRecordingsIDs
        #print "self.firedRecordingsIDs = ", self.firedRecordingsIDs
        
        removed = 0
        for v in deletedRecordingsIDs :
            self.numberOfActiveRecordings -= 1
            if self.oldInterface :
                self.TriggerEvent( "EndRecord" )               
            if self.newInterface :
                self.TriggerEvent( "EndRecord", ( v[1], self.numberOfActiveRecordings ) )
            del self.firedRecordingsIDs[ v[0] - removed ]
            removed += 1
        
        for ID in newRecordingsIDs :
            self.numberOfActiveRecordings += 1
            if self.oldInterface :
                self.TriggerEvent("StartRecord", str(ID) )               
            if self.newInterface :
                self.TriggerEvent( "StartRecord", ( ID, self.numberOfActiveRecordings ) )
            self.firedRecordingsIDs.append( ID )
        
        newRecordings     = len( newRecordingsIDs )
        deletedRecordings = len( deletedRecordingsIDs )
        updatedRecordings = newRecordings + deletedRecordings
        
        if self.numberOfActiveRecordings == 0 :
            self.TriggerEvent( "AllActiveRecordingsFinished" )
        
        return updatedRecordings



    def SendCommandThroughSendMessage(self, value):
        try:
            hwnd = gWindowMatcher()[0]
            return SendMessageTimeout(hwnd, 45762, 2069, 100 + value)
        except:
            raise self.Exceptions.ProgramNotRunning



    def SendCommandThroughCOM(self, value):
        if self.Connect( WAIT_CHECK_START_CONNECT ) :
            self.workerThread.CallWait(
                partial(self.workerThread.dvbviewer.SendCommand, value),
                CALLWAIT_TIMEOUT
            )



    def GetChannelLists( self ) :

        def GetChannelList( list, isTV, channelIDbyIDList, IDbychannelIDList, channelList ) :
            for ix in xrange( len(list) ) :
                id = ( ix, isTV )
                entry = list[ix]
                channelID = str( entry[0] ) + '|' + entry[1]
                channelIDbyIDList[ id ] = channelID
                IDbychannelIDList[ channelID ] = id
                channelList.append( entry[1] )
            
        tvChannels = []
        radioChannels = []
        
        list = self.workerThread.CallWait( partial( self.workerThread.GetChannelList ), CALLWAIT_TIMEOUT )
        channelNr = 0
        for channel in list[1] :
            channelID = str( ( channel[4] + 1 ) << 29 | ( channel[20] << 16 ) | channel[26] )
            tv = not ( channel[22] == 0 )
            if tv :
                tvChannels.append( ( channelID, channel[1] ) )
            else :
                radioChannels.append( ( channelID, channel[1] ) )
            if ( channel[ 3 ] & 2 ) == 0 :
                if not self.frequencies.has_key( channel[5] ) :
                    self.frequencies[ channel[5] ] = ( channelNr, tv )
                elif not self.frequencies[ channel[5] ][1] and tv :
                    self.frequencies[ channel[5] ] = ( channelNr, tv )
            channelNr += 1

        radioChannels.sort( cmp=lambda x,y: cmp(x[1].lower(), y[1].lower()) )
        tvChannels.sort( cmp=lambda x,y: cmp(x[1].lower(), y[1].lower()) )
        
        GetChannelList( tvChannels, True, self.channelIDbyIDList, self.IDbychannelIDList, self.tvChannels )
        GetChannelList( radioChannels, False, self.channelIDbyIDList, self.IDbychannelIDList, self.radioChannels )
                
        #print self.frequencies
        
        return True



    def TuneChannelIfNotRecording( self, channelNr, text = "", time = 0.0) :
        ret = False
        try:
            if self.Connect( WAIT_CHECK_START_CONNECT ) :
                ret = self.workerThread.CallWait(
                        partial( self.workerThread.TuneChannelIfNotRecording, channelNr, text, time ),
                        CALLWAIT_TIMEOUT
                     )
        except:
            return False
        return ret



    @eg.LogItWithReturn
    def Connect( self, connectingMode = WAIT_CHECK_START_CONNECT ) :
        #WAIT_CHECK_START_CONNECT  = 0   #wait for free, check if executing, start if not executing, connect
        #CONNECT                   = 1   #connect
        #CHECK_CONNECT             = 2   #connect only, if executing

        def WaitForDVBViewerWindow() :
            hwnds = windowDVBViewer()
            return len(hwnds)>0

        if connectingMode != CONNECT and ( self.connecting or self.checking  or (
                   self.terminateThread and connectingMode == WAIT_CHECK_START_CONNECT )
           ):
            timeout = 0
            while ( self.connecting or self.terminateThread or self.checking ) and timeout < 120:
                sleep( 1.0 )
                timeout += 1
            if timeout >= 120 :
                eg.PrintError( "DVBViewer couldn't connected" )
                eg.PrintDebugNotice( "DVBViewer couldn't connected" )
                raise
        
        started = False
        
        if not self.workerThread and not self.connecting and not self.terminateThread :
            if connectingMode == CHECK_CONNECT :
                self.checking = True
            else :
                self.connecting = True

            if self.terminateThread :
                #print "is terminating"
                self.terminateThread.join( 30.0 )

            if connectingMode != CONNECT :
                WMI = GetObject('winmgmts:')
                if len( WMI.ExecQuery('select * from Win32_Process where Name="dvbviewer.exe"') ) > 0 :
                    self.DVBViewerStartedByCOM = False
                    #print "DVBViewer is executing"
                    started = True
                elif connectingMode != CHECK_CONNECT:
                    if not self.startDVBViewerByCOM :
                        startupInfo = STARTUPINFO()
                        startupInfo.cb = sizeof(STARTUPINFO)
                        startupInfo.dwFlags = STARTF_USESHOWWINDOW
                        startupInfo.wShowWindow = 1
                        processInformation = PROCESS_INFORMATION()
                        commandLine = create_unicode_buffer(
                                            '"%s" %s' % (self.pathDVBViewer,
                                                         self.argumentsDVBViewer)
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
                            self.connecting = False
                            return False
                        self.DVBViewerStartedByCOM = False
                    else :
                        self.DVBViewerStartedByCOM = True
                    started = True
                del WMI
            else :
                self.DVBViewerStartedByCOM = False
                started = True
            if started :
                if not self.DVBViewerStartedByCOM :
                    found = WaitForDVBViewerWindow()
                    if not found:
                        eg.PrintError( "Warning: DVBViewer window not found. Hidden?" )
                        eg.PrintDebugNotice( "DVBViewer window not found. Hidden?" )
                    sleep( 5 )                  #  necessary otherwise hang up
                self.workerThread = DvbViewerWorkerThread(self)
                try:
                    self.workerThread.Start(20.0)
                except:
                    self.TriggerEvent( "DVBViewerCouldNotBeConnected" )
                    eg.PrintDebugNotice( "DVBViewer couldn't be connected" )
                    self.connecting = False
                    self.checking = False
                    self.workerThread = None
                    return False
            self.checking = False
            self.connecting = False

            if started :
                if len( self.tvChannels ) == 0 and len( self.radioChannels ) == 0 :
                    self.GetChannelLists()
                    #print self.tvChannels
                    #print self.radioChannels

        return self.workerThread and not self.terminateThread and not self.connecting



    def Configure(  self,
                    useSendMessage=False,
                    oldInterface = True,
                    newInterface = False,
                    startDVBViewerByCOM = True,
                    pathDVBViewer = "",
                    argumentsDVBViewer = "",
                    longDisplay = True,
                    shortDisplay = False,
                    longPlayState = True,
                    shortPlayState = False,
                    watchDogEnable = False,
                    watchDogTime = 60.0,
                    schedulerTaskNamePrefix = "StartRecording",
                    schedulerEventName      = "StartRecording",
                    schedulerLeadTime       = 3.0,
                    scheduleAllRecordings   = False,
                    schedulerEntryHidden    = False
                    ) :


        def onCommandCheckBox( event ) :
            enable = useCommandCheckBoxCtrl.GetValue()
            dvbviewerFileCtrl.Enable( enable )        
            argumentsCtrl.Enable( enable )
            event.Skip()


        def onRadioBox( event ) :
            pro = radioBox.GetSelection() != 1
            for ctrl in enableControls :
                ctrl.Enable( pro )
            
            if not pro :
                dvbviewerFileCtrl.Enable( False )
                argumentsCtrl.Enable( False )
                watchDogTimeCtrl.Enable( False )
                useWatchDogCheckBoxCtrl.Enable( False )
            else :
                onCommandCheckBox(wx.CommandEvent())
                onUseWatchDogCheckBox(wx.CommandEvent())
                useWatchDogCheckBoxCtrl.Enable( True )

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


        def onUseWatchDogCheckBox( event ) :
            enable = useWatchDogCheckBoxCtrl.GetValue()
            watchDogTimeCtrl.Enable( enable )
            event.Skip()


        def onPasswordChange( event ) :
            p1 = password1Ctrl.GetValue()
            p2 = password2Ctrl.GetValue()
            panel.EnableButtons( p1 == p2 )


        self.lastOld = oldInterface
        self.lastNew = newInterface
        self.lastPlayStateLong  = longPlayState
        self.lastPlayStateShort = shortPlayState
        self.lastDisplayLong    = longDisplay
        self.lastDisplayShort = shortDisplay
        
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
        useCommandCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onCommandCheckBox)
        enableControls.append( useCommandCheckBoxCtrl )
        
        dvbviewerFileCtrl = eg.FileBrowseButton(
            panel, 
            -1, 
            size=(320,-1),
            initialValue=pathDVBViewer,
            labelText="",
            fileMask="*.exe", 
            #buttonText=text.dvbviewerFile,
            dialogTitle=text.dvbviewerBox
        )
        dvbviewerFileCtrl.Enable( not startDVBViewerByCOM )

        argumentsCtrl = wx.TextCtrl( panel, size=(200,-1) )
        argumentsCtrl.SetValue( argumentsDVBViewer )
        argumentsCtrl.Enable( not startDVBViewerByCOM )

        useWatchDogCheckBoxCtrl = wx.CheckBox(panel, -1, text.useWatchDog)
        useWatchDogCheckBoxCtrl.SetValue( watchDogEnable )
        useWatchDogCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onUseWatchDogCheckBox)
        
        watchDogTimeCtrl = panel.SpinNumCtrl(watchDogTime, min=0, max=999, fractionWidth=0, integerWidth=3)


        accountCtrl = wx.TextCtrl( panel, size=(125,-1) )
        accountCtrl.SetValue( self.account )
        enableControls.append( accountCtrl )
        
        password1Ctrl = wx.TextCtrl( panel, size=(125,-1), style=wx.TE_PASSWORD )
        password1Ctrl.SetValue( self.password )
        password1Ctrl.Bind(wx.EVT_TEXT, onPasswordChange)
        enableControls.append( password1Ctrl )
        
        password2Ctrl = wx.TextCtrl( panel, size=(125,-1), style=wx.TE_PASSWORD )
        password2Ctrl.SetValue( self.password )
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
        
        gridBagSizer.Add( useWatchDogCheckBoxCtrl, (0, 0), flag =  wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        gridBagSizer.Add( wx.StaticText(panel, -1, text.watchDogTime), (0, 1), flag =  wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        gridBagSizer.Add( watchDogTimeCtrl,        (1, 1), flag =  wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        
        boxSizerI.Add(wx.Size(0,4))
        boxSizerI.Add( gridBagSizer )

        boxSizerO.Add( boxSizerI, 1, wx.EXPAND | wx.ALIGN_RIGHT )

        panel.sizer.Add(boxSizerO, 0, wx.EXPAND)

        panel.sizer.Add(wx.Size(0,5) )

        sb = wx.StaticBox( panel, -1, text.eventType )
        sBoxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )

        boxSizerO = wx.BoxSizer( wx.HORIZONTAL )
        boxSizerO.Add( oldEventsCheckBoxCtrl, 1, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        boxSizerO.Add( newEventsCheckBoxCtrl, 1, flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sBoxSizer.Add(wx.Size(0,3))
        sBoxSizer.Add( boxSizerO, 0, wx.EXPAND )
        sBoxSizer.Add(wx.Size(0,5))


        boxSizerO = wx.BoxSizer( wx.HORIZONTAL )

        sb = wx.StaticBox( panel, -1, text.playStateFormat )
        boxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )
        boxSizer.Add(wx.Size(0,3))
        boxSizer.Add(longPlayStateCheckBoxCtrl, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        boxSizer.Add(wx.Size(0,10))
        boxSizer.Add(shortPlayStateCheckBoxCtrl, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        
        boxSizerO.Add( boxSizer, 1, wx.EXPAND )
        

        sb = wx.StaticBox( panel, -1, text.displayChangeFormat )
        boxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )
        boxSizer.Add(wx.Size(0,3))
        boxSizer.Add( longDisplayCheckBoxCtrl, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        boxSizer.Add(wx.Size(0,10))
        boxSizer.Add(shortDisplayCheckBoxCtrl, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

        boxSizerO.Add( boxSizer, 1, wx.EXPAND )

        #gridSizer.Add(boxSizerO, (rowCount, 0 ), flag = wx.EXPAND, span = wx.GBSpan( 1, 2 ) )

        sBoxSizer.Add(boxSizerO, 1, wx.EXPAND)
        panel.sizer.Add(sBoxSizer, 0, wx.EXPAND)

        panel.sizer.Add(wx.Size(0,5))

        sb = wx.StaticBox( panel, -1, text.dvbViewerStart )
        boxSizer = wx.StaticBoxSizer( sb, wx.VERTICAL )

        boxSizer.Add(wx.Size(0,3))
        boxSizer.Add( useCommandCheckBoxCtrl, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

        boxSizer.Add(wx.Size(0,10))
        boxSizer.Add( wx.StaticText(panel, -1, text.dvbviewerFile), 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

        boxSizer.Add(wx.Size(0,2))
        boxSizer.Add( dvbviewerFileCtrl, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

        boxSizerI = wx.BoxSizer( wx.HORIZONTAL )

        boxSizerI.Add( wx.StaticText(panel, -1, text.dvbviewerArguments), 0, wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT)
        boxSizerI.Add( argumentsCtrl, 2, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

        boxSizer.Add(wx.Size(0,3))
        boxSizer.Add( boxSizerI, 0, wx.EXPAND)

        panel.sizer.Add(boxSizer, 0, wx.EXPAND)
        
        panel.sizer.Add(wx.Size(0,5))

        
        sb = wx.StaticBox( panel, -1, text.taskSchedulerInfo )
        boxSizer = wx.StaticBoxSizer( sb, wx.HORIZONTAL )
        
        sizer = wx.GridBagSizer( 0, 0 )
        
        sizer.Add(wx.Size(0,3),                                    (0,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( scheduleAllCheckBoxCtrl,                        (1,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        sizer.Add( scheduleHiddenCheckBoxCtrl,                     (1,3), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add(wx.Size(0,5),                                   (2,0), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.accountName),     (3,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( accountCtrl,                                    (3,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.password1),       (4,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( password1Ctrl,                                  (4,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.password2),       (5,0), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( password2Ctrl,                                  (5,1), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )
        
        sizer.Add( wx.StaticText(panel, -1, text.schedulerPrefix), (3,3), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( schedulerPrefixCtrl,                            (3,4), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.schedulerEvent),  (4,3), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( schedulerEventCtrl,                             (4,4), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )

        sizer.Add( wx.StaticText(panel, -1, text.schedulerLead),   (5,3), flag = wx.ALIGN_CENTER_VERTICAL| wx.ALIGN_RIGHT )
        sizer.Add( schedulerLeadCtrl,                              (5,4), flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL )


        boxSizer.Add( sizer, 0, wx.EXPAND )
                
        panel.sizer.Add(boxSizer, 0, wx.EXPAND)

        onRadioBox( wx.CommandEvent() )
        onUseWatchDogCheckBox(wx.CommandEvent())
        onPasswordChange( wx.CommandEvent() )
        
        while panel.Affirmed():
            useSendMessage      = radioBox.GetSelection() == 1
            oldInterface        = oldEventsCheckBoxCtrl.GetValue()
            newInterface        = newEventsCheckBoxCtrl.GetValue()
            startDVBViewerByCOM = not useCommandCheckBoxCtrl.GetValue()
            argumentsDVBViewer  = argumentsCtrl.GetValue()
            pathDVBViewer       = dvbviewerFileCtrl.GetValue()
            longDisplay         =  longDisplayCheckBoxCtrl.GetValue()
            shortDisplay        = shortDisplayCheckBoxCtrl.GetValue()
            longPlayState       =  longPlayStateCheckBoxCtrl.GetValue()
            shortPlayState      = shortPlayStateCheckBoxCtrl.GetValue()
            watchDogEnable      = useWatchDogCheckBoxCtrl.GetValue()
            watchDogTime        = watchDogTimeCtrl.GetValue()
            
            schedulerTaskNamePrefix = schedulerPrefixCtrl.GetValue()
            schedulerEventName      = schedulerEventCtrl.GetValue()
            schedulerLeadTime       = schedulerLeadCtrl.GetValue()
            scheduleAllRecordings   = scheduleAllCheckBoxCtrl.GetValue()
            schedulerEntryHidden    = scheduleHiddenCheckBoxCtrl.GetValue()
            
            
            if accountCtrl.IsModified() or password1Ctrl.IsModified() :
            
                self.account   =   accountCtrl.GetValue()
                self.password  = password1Ctrl.GetValue()
            
                self.HandlePasswordFile( write = True,
                                         account = self.account,
                                         password = self.password
                                       )
            
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
                             watchDogEnable,
                             watchDogTime,
                             schedulerTaskNamePrefix,
                             schedulerEventName,     
                             schedulerLeadTime,      
                             scheduleAllRecordings,
                             schedulerEntryHidden
                           )



    def HandlePasswordFile( self, write = False, account='' , password='' ) :
        
        passwordFileName = os.path.join(eg.folderPath.RoamingAppData, eg.APP_NAME, 'DVBViewerAccount.dat')

        try:
            file = open( passwordFileName, 'r' )
            lines = file.readlines()
            file.close()
            previousAccount  = lines[0][:-1]
            key = lines[2][:-1]
            previousPassword = self.Crypt( "".join( [ chr(int(v,16)) for v in lines[1][:-2].split(' ') ] ), key, False )
            file.close()
        except:
            previousAccount  = ''
            previousPassword = ''
            
        if not write :
            return ( previousAccount, previousPassword )
            
        key = ''
        for i in xrange(16):
            r = random.randint(0,255)
            key += '%02x'%r

        file = open( passwordFileName, 'w' )

        lines = []
        lines.append(  account + '\n' )
        lines.append( "".join( ['%02x '%ord(c) for c in self.Crypt( password, key, True ) ] ) + '\n' )
        lines.append( key + '\n' )
        
        file.writelines( lines )
        file.close()



    def Crypt( self, string, key, gen = True ) :
        m = hashlib.md5()
        m.update('37c710146322502a230dd8781ec3f5a')
        m.update(key)
        digest = m.digest()
        result = ''
        for index in xrange( len(string) ) :
            if gen :
                modifier = string[index]               
            char = chr(ord(digest[index%16]) ^ ord(string[index]))
            if not gen :
                modifier = char
            result += char
            m.update(modifier)
            digest = m.digest()
            
        #print result
        return result




class Start(eg.ActionClass):
   
    def __call__(self):
        self.plugin.Connect( WAIT_CHECK_START_CONNECT )
        return True




class CloseDVBViewer( eg.ActionClass ) :
    
    def __call__( self, waitForTermination = False ) :
        if not self.plugin.workerThread and not self.plugin.terminateThread :
            return False
        plugin = self.plugin
        plugin.SendCommand( DVBVIEWER_CLOSE[1] )
        
        if not waitForTermination :
            return True
        
        checkTime = 0.1
        timeout = 1000
        while ( plugin.workerThread or plugin.terminateThread ) and timeout > 0:
            sleep( checkTime )
            timeout -= 1
        
        if timeout == 0 :
            eg.PrintDebugNotice("DVBViewer could not be terminated")
            plugin.TriggerEvent( "DVBViewerCouldNotBeTerminated" )
            return False
        return True
        
    def Configure(  self, waitForTermination = False ) :



        plugin = self.plugin

        self.panel = eg.ConfigPanel()
        panel = self.panel

        checkBox = wx.CheckBox( panel, -1, self.text.checkBoxText )
        checkBox.SetValue( waitForTermination )

        panel.AddLine( checkBox )

        while panel.Affirmed():
             waitForTermination      = checkBox.GetValue()
 
             panel.SetResult( waitForTermination )




class StopAllActiveRecordings( eg.ActionClass ) :
    
    def __call__( self ) :
        plugin = self.plugin
        if plugin.Connect( CHECK_CONNECT ) :
            plugin.workerThread.CallWait(
                        partial(plugin.workerThread.StopAllActiveRecordings ),
                        CALLWAIT_TIMEOUT
            )
        return True




class GetNumberOfActiveRecordings( eg.ActionClass ) :

    def __call__( self ) :
        plugin = self.plugin
        count = 0
        if plugin.Connect( CHECK_CONNECT ) :
            count = len(
                         plugin.workerThread.CallWait(
                             partial(plugin.workerThread.GetRecordingsIDs ),
                             CALLWAIT_TIMEOUT
                         )
            )
        return count




class GetRecordingsIDs( eg.ActionClass ) :

    def __call__( self, active = True ) :
        plugin = self.plugin
        
        if active :
            connectionMode = CHECK_CONNECT
        else :
            connectionMode = WAIT_CHECK_START_CONNECT
        
        list = []
        if plugin.Connect( connectionMode ) :
            list = plugin.workerThread.CallWait(
                             partial(plugin.workerThread.GetRecordingsIDs, active ),
                             CALLWAIT_TIMEOUT
                         )
        return list



    def Configure(  self, active = True ) :

        plugin = self.plugin

        self.panel = eg.ConfigPanel()
        panel = self.panel

        checkBox = wx.CheckBox( panel, -1, self.text.active )
        checkBox.SetValue( active )

        panel.AddLine( checkBox )

        while panel.Affirmed():
             active      = checkBox.GetValue()
 
             panel.SetResult( active )




class IsConnected( eg.ActionClass ) :

    def __call__( self ) :
        if self.plugin.workerThread or self.plugin.terminateThread :
            return True
        else :
            return False




class IsRecording( eg.ActionClass ) :

    def __call__( self ) :
        return self.plugin.numberOfActiveRecordings != 0




class SendAction( eg.ActionClass ) :

    def __call__( self, action ) :
        if action != -1 :
            return self.plugin.SendCommand(action)
        else :
            return False
    
    def Configure( self, action = -1 ) :
        panel = eg.ConfigPanel()
        if action < 0 :
            action = 0
        actionCtrl = panel.SpinNumCtrl( action, min=0, max=999999, fractionWidth=0, integerWidth=6)
        panel.AddLine( self.text.action, actionCtrl )

        while panel.Affirmed() :
            action = actionCtrl.GetValue()
            
            panel.SetResult( action )




class UpdateEPG( eg.ActionClass ) :

    def __init__(self):

        self.iterator = {}
        self.timeBetweenChannelChange = 60.0
        self.channelNr = -1
        self.repeat = False



    @eg.LogItWithReturn
    def __call__( self, timeBetweenChannelChange = 60.0, disableAV = True ) :
    
        plugin = self.plugin

        self.timeBetweenChannelChange = timeBetweenChannelChange
        
        if not plugin.frequencies :
            if not plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                plugin.TriggerEvent( "EPGUpdateFinished" )
                return False
                
        plugin.EPGdisableAV = disableAV
        
        self.iterator = plugin.frequencies.itervalues()
        
        self.EPGTune()
        
        return True



    @eg.LogItWithReturn
    def EPGTune( self ) :
        plugin = self.plugin
        CoInitialize()
        if not self.repeat :
            try :
                self.channelNr = self.iterator.next()[0]
            except StopIteration :
                plugin.SendCommand( 16383 )  #Stop Graph
                CoUninitialize()
                plugin.TriggerEvent( "EPGUpdateFinished" )
                plugin.timerEPG = None
                return True

        #print self.channelNr
        
        if plugin.TuneChannelIfNotRecording( self.channelNr, "Updating EPG", self.timeBetweenChannelChange ) :
            self.repeat = False
        else :
            self.repeat = True
        CoUninitialize()
                
        plugin.timerEPG = Timer( self.timeBetweenChannelChange, self.EPGTune )
        plugin.timerEPG.start()

        return False



    def Configure(  self, timeBetweenChannelChange = 60.0, disableAV = True ) :
        
        plugin = self.plugin
        text = self.text

        self.panel = eg.ConfigPanel()
        panel = self.panel

        disableAVCheckBoxCtrl = wx.CheckBox(panel, -1, text.disableAV)
        disableAVCheckBoxCtrl.SetValue( disableAV )

        epgTimeCtrl = panel.SpinNumCtrl(timeBetweenChannelChange, min=0, max=999, fractionWidth=0, integerWidth=3)
        
        panel.AddLine( disableAVCheckBoxCtrl )
        panel.AddLine( text.time, epgTimeCtrl )

        while panel.Affirmed():
            disableAV                = disableAVCheckBoxCtrl.GetValue()
            timeBetweenChannelChange = epgTimeCtrl.GetValue()
            
            panel.SetResult( timeBetweenChannelChange, disableAV )




class AddRecording( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__(self,
                 channelID, 
                 date,                 # dd.mm.yyyy
                 startTime,            # hh:mm
                 endTime,              # hh:mm
                 description = "",
                 disableAV = False,
                 enabled = True,
                 recAction = 0,        # intern = 0, tune only = 1, 
                                       # AudioPlugin = 2, Videoplugin = 3 
                                       
                 actionAfterRec = 0,   # No action = 0, PowerOff = 1, 
                                       # Standby = 2, Hibernate = 3, Close = 4,
                                       # Playlist = 5, Slumbermode: = 6 

                 days = "-------"
                ) :
        plugin = self.plugin
        result = False
        if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
            id = plugin.workerThread.CallWait(
               partial( plugin.workerThread.AddRecording, channelID, date, startTime,
                                                          endTime, description, disableAV,
                                                          enabled, recAction, actionAfterRec,
                                                          days
                      ),
               CALLWAIT_TIMEOUT
            )
            return id
        return -1



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
            plugin.Connect( WAIT_CHECK_START_CONNECT )
            
        if plugin.IDbychannelIDList.has_key( channelID ) :
        
            id = plugin.IDbychannelIDList[ channelID ]
            self.tv = id[1]
            
            if ( self.tv ) :
                self.choices = plugin.tvChannels
            else :
                self.choices = plugin.radioChannels

            ix = id[0]
        else :
            self.tv = True
            ix = 0
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




class GetDateOfRecordings( eg.ActionClass ) :

    def __call__( self, allRecordings = False ) :
    
        plugin = self.plugin
        
        recordingDates = []
        
        if plugin.Connect( WAIT_CHECK_START_CONNECT ) :       
            recordingList = plugin.workerThread.CallWait( plugin.workerThread.GetAllRecordings, CALLWAIT_TIMEOUT )
            now = time()
            for record in recordingList[1] :
                if record[8] :                  # Recording enabled
                
                    if record[18] ==1 and record[0] == "EPG-Update by EventGhost" :
                        continue
                
                    nextDate = record[5]
                    nextTime = record[6]
                    
                    #nextDate =  19.07.2008 00:00:00    nextTime =  30.12.1899 05:15:00
                    t = mktime( strptime( str(nextDate)+str(nextTime),"%d.%m.%Y 00:00:0030.12.1899 %H:%M:%S" ) )
                    
                    if t < now :
                        continue
                    if not t in recordingDates:
                        recordingDates.append(t)
                    #print "date = ", ctime(t)
            recordingDates.sort()
            
        else :
            return ( False, None )

        if allRecordings :
            return ( True, recordingDates )
        else :
            if len( recordingDates ) == 0 :
                return ( True, -1 )
            else :
                return ( True, recordingDates[ 0 ] )



    def Configure(  self, allRecordings = False ) :

        plugin = self.plugin

        self.panel = eg.ConfigPanel()
        panel = self.panel

        checkBox = wx.CheckBox( panel, -1, self.text.all )
        checkBox.SetValue( allRecordings )

        panel.AddLine( checkBox )

        while panel.Affirmed():
             allRecordings      = checkBox.GetValue()
 
             panel.SetResult( allRecordings )




class TaskScheduler( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self ) :
        
        plugin = self.plugin
    
        leadTime = plugin.schedulerLeadTime * 60.0

        recordingDates = eg.plugins.DVBViewer.GetDateOfRecordings( allRecordings = plugin.scheduleAllRecordings )
            
        if not recordingDates[0] :
            eg.PrintError( "dates not valid" )
            return False
            

        if plugin.scheduleAllRecordings :
            dates = recordingDates[1]
        else :
            if recordingDates[1] > 0 :
                dates = [ recordingDates[1] ]
            else :
                dates = []
        
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
        
            if date not in dates :          # remove deleted recordings
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
            workItem.SetAccountInformation( plugin.account, plugin.password )
            ts.AddWorkItem(taskName, workItem)
            #runTime = localtime(time() + 300)
            triggerIndex, taskTrigger = workItem.CreateTrigger()
            trigger = taskTrigger.GetTrigger()
            trigger.Flags = 0
            trigger.BeginYear =   runTime.tm_year
            trigger.BeginMonth =  runTime.tm_mon
            trigger.BeginDay =    runTime.tm_mday
            trigger.StartHour =   runTime.tm_hour
            trigger.StartMinute = runTime.tm_min

            trigger.TriggerType = int( taskscheduler.TASK_TIME_TRIGGER_ONCE )
            taskTrigger.SetTrigger( trigger )

            persistFile = workItem.QueryInterface( IID_IPersistFile )
            persistFile.Save( None, True )
            
        actuals.sort()

        if len( actuals ) > 0 :
            nextStartup = "Scheduled next wakeup at " + asctime( localtime( actuals[0] - leadTime ) )
            print nextStartup
            eg.PrintDebugNotice( nextStartup )
            return True
        else :
            print "No recording scheduled"
            eg.PrintDebugNotice( "No recording scheduled" )
            return False




class GetDVBViewerObject( eg.ActionClass ) :

    def __call__( self ) :
        plugin = self.plugin
        result = None
        if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
            return plugin.workerThread.dvbviewer
        return None




class ExecuteDVBViewerCommandViaCOM( eg.ActionClass ) :

    def __call__( self, command, *args, **kwargs ) :
        plugin = self.plugin
        result = None
        if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
            result = plugin.workerThread.CallWait(
                        partial( command, *args, **kwargs ),
                        CALLWAIT_TIMEOUT
            )
        return result




