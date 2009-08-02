#!/usr/bin/env python
# -*- coding: UTF-8 -*-


SUPPORTED_DVBVIEWER_VERSIONS        = '4.0.x, 4.1.x, 4.2.x '
SUPPORTED_DVBVIEWERSERVICE_VERSIONS = '1.5.0.2, 1.5.0.21, 1.5.0.25'

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
"""
<table border="0">
    <tr>
        <td align="right"  valign="top">Supported DVBViewer versions: </td>
"""
'       <td align="left"  valign="top">' + SUPPORTED_DVBVIEWER_VERSIONS + '</td>'
"""
    </tr>
    <tr>
        <td align="right"  valign="top">Supported DVBViewerService versions: </td>
"""
'       <td align="left"  valign="top">' + SUPPORTED_DVBVIEWERSERVICE_VERSIONS +'</td>'
"""
    </tr>
</table>

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
        <td align="right">ShowInfoinTVPic</td>
        <td>
            Show the Infobar in the TVPicture.
        </td>
    </tr>
    <tr>
        <td align="right">DeleteInfoinTVPic</td>
        <td>
            Deletes the Infobar in the TVPicture.
        </td>
    </tr>
    <tr>
        <td align="right">GetNumberOfClients</td>
        <td>
            Get the number of clients connected to the DVBViewerService.
        </td>
    </tr>
    <tr>
        <td align="right">GetSetupValue</td>
        <td>
            Get a setup value of the setup.xml of the DVBViewer.
        </td>
    </tr>
    <tr>
        <td align="right">SendAction</td>
        <td>
            Send an action to the DVBViewer
            (Values are defined in the action.ini of the DVBViewer)
        </td>
    </tr>
    <tr>
        <td align="right">GetNumberOfClients</td>
        <td>
            Get the number of clients which are connected with the DVBViewerService
        </td>
    </tr>
    <tr>
        <td align="right">IsEPGUpdating</td>
        <td>
            True while the DVBViewerService is updating the EPG information
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
        <th align="center"> <b>Fired by</b></th>
        <th align="left">   <b>Description</b></th>
    </tr>
    <tr>
        <td align="right"> DVBViewerIsConnected</td>
        <td></td>
        <td>Viewer</td>
        <td>The event gets fired when the DVBViewer is connected to the plugin.</td>
    </tr>
    <tr>
        <td align="right"> Action</td>
        <td align="center">Action ID</td>
        <td>Viewer</td>
        <td>The event gets fired whenever a new action is processed. (Description
            <a href="http://wiki.dvbviewer.info/index.php/Actions.ini"> here</a>)</td>
    </tr>
    <tr>
        <td align="right"> Channel</right></td>
        <td align="center">ChannelNr</td>
        <td>Viewer</td>
        <td>The event gets fired on every channelchange</td>
    </tr>
    <tr>
        <td align="right"> AddRecord</right></td>
        <td align="center">Timer ID</td>
        <td>Viewer / Service</td>
        <td>The event gets fired whenever a new Timer is added.</td>
    </tr>
    <tr>
        <td align="right"> TimerListUpdated</right></td>
        <td></td>
        <td>Viewer / Service</td>
        <td>The event gets fired whenever the timer list is changed. Watch dog must be enabled.</td>
    </tr>
    <tr>
        <td align="right"> StartRecord</right></td>
        <td align="center">Timer ID, Number of active recordings</td>
        <td>Viewer / Service</td>
        <td>The event gets fired whenever a recording starts.</td>
    </tr>
    <tr>
        <td align="right"> EndRecord</right></td>
        <td align="center">Timer ID, Number of active recordings</td>
        <td>Viewer / Service</td>
        <td>The event gets fired whenever a recording ends.</td>
    </tr>
    <tr>
        <td align="right">AllActiveRecordings<br>Finished</right></td>
        <td align="center"></td>
        <td>Viewer / Service</td>
        <td>The event gets fired whenever the last active recording finishs.</td>
    </tr>
    <tr>
        <td align="right"> Window</right></td>
        <td align="center">OSD Window ID</td>
        <td>Viewer</td>
        <td>The event gets fired whenever a OSD-window is activated.</td>
    <tr>
    <tr>
        <td align="right"> ControlChange</right></td>
        <td align="center">OSD Window ID, Control ID</td>
        <td>Viewer</td>
        <td>The event gets fired whenever an OSD Control gets the focus.</td>
    <tr>
    <tr>
        <td align="right"> SelectedItemChange</right></td>
        <td></td>
        <td>Viewer</td>
        <td>The event gets fired whenever the selectedItem in an OSD list changes.</td>
    <tr>
    <tr>
        <td align="right"> RDS</td>
        <td align="center">RDS Text</td>
        <td>Viewer</td>
        <td>The event gets fired whenever a new RDS Text arrives.</td>
    <tr>
    <tr>
        <td align="right"> Playlist</td>
        <td align="center">Filename</td>
        <td>Viewer</td>
        <td>The event gets fired whenever a new playlistitem starts playing.</td>
    <tr>
    <tr>
        <td align="right"> Playbackstart</td>
        <td align="center"></td>
        <td>Viewer</td>
        <td>The event gets fired whenever a media playback starts.</td>
    <tr>
    <tr>
        <td align="right"> PlaybackEnd</td>
        <td align="center"></td>
        <td>Viewer</td>
        <td>The event gets fired whenever a media playback ends.</td>
    <tr>
    <tr>
        <td align="right"> Close</td>
        <td align="center"></td>
        <td>Viewer</td>
        <td>The event gets fired when the DVBViewer is shutting down.</td>
    <tr>
    <tr>
        <td align="right"> EPGUpdateFinished</td>
        <td align="center"></td>
        <td>Viewer</td>
        <td>The event gets fired whenever the UpdateEPG action finishs.</td>
    <tr>
    <tr>
        <td align="right"> PlaystateChange</td>
        <td align="center">PlayerState</td>
        <td>Viewer</td>
        <td>The event gets fired whenever the play state changes. (PLAY, PAUSE or STOP)</td>
    <tr>
    <tr>
        <td align="right"> RatioChange</td>
        <td align="center">Ratio</td>
        <td>Viewer</td>
        <td>The event gets fired whenever the ratio changes. (133 = 4:3, 178 = 16:9)</td>
    <tr>
    <tr>
        <td align="right"> DisplayChange</td>
        <td align="center">DisplayType</td>
        <td>Viewer</td>
        <td>The event gets fired whenever the display type changes. (NONE, OSD, TV, DVD, MEDIA, SLIDESHOW, TELETEXT)</td>
    <tr>
    <tr>
        <td align="right"> RenderPlaystateChange</td>
        <td align="center">RendererType, PlaysState</td>
        <td>Viewer</td>
        <td>The event gets fired whenever the internal playstate changes.</td>
    <tr>
    <tr>
        <td align="right"> RendererChange</td>
        <td align="center">RendererType</td>
        <td>Viewer</td>
        <td>The event gets fired whenever the renderer changes.</td>
    <tr>
    <tr>
        <td align="right"> NumberOfClientsChanged</td>
        <td align="center"></td>
        <td>Service</td>
        <td>The event gets fired whenever the number of clients connected to the service change.</td>
    <tr>
    <tr>
        <td align="right"> NoClientActive</td>
        <td align="center"></td>
        <td>Service</td>
        <td>The event gets fired whenever the last client disconnects from the service.</td>
    <tr>
    <tr>
        <td align="right"> ServiceNotAlive</td>
        <td align="center"></td>
        <td>Service</td>
        <td>The event gets fired whenever the service not alive.</td>
    <tr>
    <tr>
        <td align="right"> DVBViewerEventHandlingNotAlive</td>
        <td align="center"></td>
        <td>Viewer</td>
        <td>The event gets fired whenever the DVBViewer can't sent events.</td>
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

This plugin contains a watchdog which detects if the DVBViewer is running,
and synchronize the number of active recording with the internal counter.
The watchdog is always enabled and the period of checking can be changed in
the configuration (default: 60s).<br>
The watchdog is also responsible for monitoring the DVBViewerService. Through
the watchdog is at the beginning and end of each recording an event fired.

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
    guid = "{747B54F6-59F6-4602-A777-984EA76D2D8C}",
    createMacrosOnAdd = True,
    description = (
        'Adds support functions to control <a href="http://www.dvbviewer.com/">'
        'DVBViewer Pro/GE and DVBViewerService</a> and returns events.'
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


CALLWAIT_TIMEOUT  =  60.0
TERMINATE_TIMEOUT = 120
DUMMY_ACTION      = 27536
ACCOUNT_CHOICES   = ['DVBService','Task scheduler']
INDEX_DVBSERVICE  = ACCOUNT_CHOICES.index( 'DVBService' )
INDEX_SCHEDULER   = ACCOUNT_CHOICES.index( 'Task scheduler' )

UPDATE_RECORDINGS = 1
UPDATE_STREAM     = 2
UPDATE_ALL        = UPDATE_RECORDINGS | UPDATE_STREAM

#connectionMode:
WAIT_CHECK_START_CONNECT  = 0   #wait for free, check if executing, start if not executing, connect
CONNECT                   = 1   #connect
CHECK_CONNECT             = 2   #connect only, if executing

DVBVIEWER_WINDOWS = {
    2007: "SLIDESHOW",
    2000: "TELETEXT",
}

DVBVIEWER_CLOSE = ( "Close DVBViewer", 12326)


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
    ("DVBViewerCouldNotBeConnected",    "Gets fired whenever the plugin can't connect to the DVBViewer"),
    ("DVBViewerEventHandlingNotAlive",  "Gets fired whenever the plugin can't receive events from the DVBViewer" ),
    ("Close",                           "Gets fired when the DVBViewer is shutting down"),
)



ACTIONS = (
    ("OSDMenu",                          "OSD-Menu",                            None,   (111,True )),
    ("OSDShowSubtitlemenu",              "OSD-Show Subtitlemenu",               None,  (8247,True )),
    ("OSDShowAudiomenu",                 "OSD-Show Audiomenu",                  None,  (8248,True )),
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
    ("OSDPositioning", "OSD-Positioning", None, (85,True )),                        #??????????
    ("OSDClock",                         "OSD-Clock",                           None,  (2010,True )),
    ("OSDShowHTPC",                      "OSD-Show HTPC",                       None,  (2110,True )),
    ("OSDBackgroundToggle",              "OSD-Background Toggle",               None,  (8194,True )),
    ("OSDTeletext",                      "OSD-Teletext",                        None,   (101,True )),
    ("OSDShowTimer",                     "OSD-Show Timer",                      None,  (8195,True )),
    ("OSDShowRecordings",                "OSD-Show Recordings",                 None,  (8196,True )),
    ("OSDShowNow",                       "OSD-Show Now",                        None,  (8197,True )),
    ("OSDShowEPG",                       "OSD-Show EPG",                        None,  (8198,True )),
    ("OSDShowChannels",                  "OSD-Show Channels",                   None,  (8199,True )),
    ("OSDShowFavourites",                "OSD-Show Favourites",                 None,  (8200,True )),
    ("OSDShowTimeline",                  "OSD-Show Timeline",                   None,  (8201,True )),
    ("OSDShowPicture",                   "OSD-Show Picture",                    None,  (8202,True )),
    ("OSDShowMusic",                     "OSD-Show Music",                      None,  (8203,True )),
    ("OSDShowVideo",                     "OSD-Show Video",                      None,  (8204,True )),
    ("OSDShowNews",                      "OSD-Show News",                       None,  (8205,True )),
    ("OSDShowWeather",                   "OSD-Show Weather",                    None,  (8206,True )),
    ("OSDShowMiniepg",                   "OSD-Show Miniepg",                    None,  (8207,True )),
    ("OSDShowMusicPlaylist",             "OSD-Show Music playlist",             None,  (8208,True )),  #???
    ("OSDShowVideoPlaylist",             "OSD-Show Video playlist",             None,  (8209,True )),  #???
    ("OSDShowComputer",                  "OSD-Show Computer",                   None,  (8210,True )),
    ("OSDShowAlarms",                    "OSD-Show Alarms",                     None,  (8212,True )),
    ("OSDCAM",                           "OSD-CAM",                             None,  (8259,True )),
    ("PortalSelect",                     "Portal select",                       None,  (8254,True )),
    ("Pause",                            "Pause",                               None,     (0,True )),
    ("OnTop",                            "On Top",                              None,     (1,True )),
    ("HideMenu",                         "Hide Menu",                           None,     (2,True )),
    ("ShowStatusbar",                    "Show Statusbar",                      None,     (3,True )),
    ("Toolbar",                          "Toolbar",                             None,     (4,True )),
    ("Fullscreen",                       "Fullscreen",                          None,     (5,True )),
    ("Exit",                             "Exit",                                None,     (6,False)),
    ("ClearChannelUsageCounter",         "Clear Channel usage counter",         None,  (8255,True )),
    ("Channellist",                      "Channellist",                         None,     (7,True )),
    ("ChannelMinus",                     "Channel -",                           None,     (8,True )),
    ("ChannelPlus",                      "Channel +",                           None,     (9,True )),
    ("ChannelSave",                      "Channel Save",                        None,    (10,True )),
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
    ("ChannelEdit",                      "ChannelEdit",                         None,   (117,True )),
    ("ChannelScan",                      "ChannelScan",                         None,   (119,True )),
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
    ("FavouritePlus",                    "Favourite +",                         None,    (20,True )),
    ("FavouriteMinus",                   "Favourite -",                         None,    (21,True )),
    ("Aspect",                           "Aspect",                              None,    (22,True )),
    ("Zoom",                             "Zoom",                                None,    (23,True )),
    ("Options",                          "Options",                             None,    (24,True )),
    ("Mute",                             "Mute",                                None,    (25,True )),
    ("VolumeUp",                         "Volume Up",                           None,    (26,True )),
    ("VolumeDown",                       "Volume Down",                         None,    (27,True )),
    ("Display",                          "Display",                             None,    (28,True )),
    ("Zoom50",                           "Zoom 50%",                            None,    (29,True )),
    ("Zoom75",                           "Zoom 75%",                            None,  (2013,True )),
    ("Zoom100",                          "Zoom 100%",                           None,    (30,True )),
    ("Zoom200",                          "Zoom 200%",                           None,    (31,True )),
    ("Desktop",                          "Desktop",                             None,    (32,True )),
    ("RecordSettings",                   "Record Settings",                     None,    (33,True )),
    ("Record",                           "Record",                              None,    (34,True )),
    ("Teletext",                         "Teletext",                            None,    (35,True )),
    ("EPG",                              "EPG",                                 None,    (37,True )),
    ("TimeShift",                        "TimeShift",                           None,    (50,True )),
    ("TimeShiftWindow",                  "TimeShift Window",                    None,    (51,True )),
    ("TimeshiftStop",                    "Timeshift Stop",                      None,    (52,True )),
    ("KeepTimeshiftFile",                "Keep Timeshift File",                 None,  (2012,True )),
    ("RecordedShowsAndTimerStatistics",  "Recorded Shows and Timer statistics", None,  (2011,True )),
    ("RefreshRecDB",                     "Refresh RecDB",                       None,  (8260,True )),
    ("CleanupRecDB",                     "Cleanup RecDB",                       None,  (8261,True )),
    ("CompressRecDB",                    "Compress RecDB",                      None,  (8262,True )),
    ("RefreshCleanupCompressRecDB",      "Refresh Cleanup Compress RecDB",      None,  (8263,True )),
    ("TitlebarHide",                     "Titlebar Hide",                       None,    (54,True )),
    ("BrightnessUp",                     "Brightness Up",                       None,    (55,True )),
    ("BrightnessDown",                   "Brightness Down",                     None,    (56,True )),
    ("SaturationUp",                     "Saturation Up",                       None,    (57,True )),
    ("SaturationDown",                   "Saturation Down",                     None,    (58,True )),
    ("ContrastUp",                       "Contrast Up",                         None,    (59,True )),
    ("ContrastDown",                     "Contrast Down",                       None,    (60,True )),
    ("HueUp",                            "Hue Up",                              None,    (61,True )),
    ("HueDown",                          "Hue Down",                            None,    (62,True )),
    ("Equalizer",                        "Equalizer",                           None,   (116,True )),
    ("Playlist",                         "Playlist",                            None,    (64,True )),
    ("PlaylistFirst",                    "Playlist First",                      None,    (65,True )),
    ("PlaylistNext",                     "Playlist Next",                       None,    (66,True )),
    ("PlaylistPrevious",                 "Playlist Previous",                   None,    (67,True )),
    ("PlaylistLoop",                     "Playlist Loop",                       None,    (68,True )),
    ("PlaylistStop",                     "Playlist Stop",                       None,    (69,True )),
    ("PlaylistRandom",                   "Playlist Random",                     None,    (70,True )),
    ("HideAll",                          "Hide All",                            None,    (71,True )),
    ("AudioChannel",                     "Audio Channel",                       None,    (72,True )),
    ("BestWidth",                        "Best Width",                          None,    (89,True )),
    ("Play",                             "Play",                                None,    (92,True )),
    ("OpenFile",                         "Open File",                           None,    (94,True )),
    ("LastFile",                         "Last File",                           None,   (118,True )),
    ("StereoLeftRight",                  "Stereo/Left/Right",                   None,    (95,True )),
    ("JumpMinus10",                      "Jump Minus 10",                       None,   (102,True )),
    ("JumpPlus10",                       "Jump Plus 10",                        None,   (103,True )),
    ("ZoomUp",                           "Zoom Up",                             None,   (104,True )),
    ("ZoomDown",                         "Zoom Down",                           None,   (105,True )),
    ("StretchHUp",                       "StretchH Up",                         None,   (106,True )),
    ("StretchHDown",                     "StretchH Down",                       None,   (107,True )),
    ("StretchVUp",                       "StretchV Up",                         None,   (108,True )),
    ("StretchVDown",                     "StretchV Down",                       None,   (109,True )),
    ("StretchReset",                     "Stretch Reset",                       None,   (110,True )),
    ("Previous",                         "Previous",                            None,   (112,True )),
    ("Next",                             "Next",                                None,   (113,True )),
    ("Stop",                             "Stop",                                None,   (114,True )),
    ("RebuildGraph",                     "Rebuild Graph",                       None,    (53,True )),
    ("StopGraph",                        "Stop Graph",                          None, (16383,False)),
    ("StopRenderer",                     "Stop Renderer",                       None,  (8256,False)),
    ("ShowVideowindow",                  "Show Videowindow",                    None,   (821,True )),
    ("ToggleMosaicpreview",              "Toggle Mosaicpreview",                None,  (8211,True )),
    ("ShowHelp",                         "Show Help",                           None,  (8213,True )),
    ("HideVideowindow",                  "Hide Videowindow",                    None,  (8214,True )),
    ("ToggleBackground",                 "Toggle Background",                   None, (12297,True )),
    ("PlayAudioCD",                      "Play AudioCD",                        None,  (8257,True )),
    ("PlayDVD",                          "Play DVD",                            None,  (8250,True )),
    ("EjectCD",                          "Eject CD",                            None, (12299,True )),
    ("Forward",                          "Forward",                             None, (12304,True )),
    ("Rewind",                           "Rewind",                              None, (12305,True )),
    ("AddBookmark",                      "Add Bookmark",                        None, (12306,True )),
    ("SpeedUp",                          "Speed Up",                            None, (12382,True )),
    ("SpeedDown",                        "Speed Down",                          None, (12383,True )),
    ("ShowPlaylist",                     "Show Playlist",                       None, (12384,True )),
    ("ShowVersion",                      "Show Version",                        None, (16384,True )),
    ("ShowCurrentInfo",                  "Show Current Info",                   None,  (8264,True )),
    ("ShowRadioList",                    "Show Radio List",                     None,  (8265,True )),
    ("DisableAudio",                     "Disable Audio",                       None, (16385,True )),
    ("DisableAudioVideo",                "Disable AudioVideo",                  None, (16386,True )),
    ("DisableVideo",                     "Disable Video",                       None, (16387,True )),
    ("EnableAudioVideo",                 "Enable AudioVideo",                   None, (16388,True )),
    ("VideoOutputAB",                    "Video Output A/B",                    None,   (132,True )),
    ("AudioOutputAB",                    "Audio Output A/B",                    None,   (133,True )),
    ("WindowMinimize",                   "WindowMinimize",                      None, (16382,True )),
    ("WindowRestore",                    "WindowRestore",                       None, (16397,True )),
    ("Screenshot",                       "Screenshot",                          None,   (115,True )),
    ("ZoomlevelStandard",                "Zoomlevel Standard",                  None, (16389,True )),
    ("Zoomlevel0",                       "Zoomlevel 0",                         None, (16390,True )),
    ("Zoomlevel1",                       "Zoomlevel 1",                         None, (16391,True )),
    ("Zoomlevel2",                       "Zoomlevel 2",                         None, (16392,True )),
    ("Zoomlevel3",                       "Zoomlevel 3",                         None, (16393,True )),
    ("ZoomlevelToggle",                  "Zoomlevel Toggle",                    None, (16394,True )),
    ("TogglePreview",                    "Toggle Preview",                      None, (16395,True )),
    ("RestoreDefaultColors",             "Restore Default Colors",              None, (16396,True )),
    ("DVDMenu",                          "DVD Menu",                            None,  (8246,True )),
    ("ShutdownCard",                     "Shutdown Card",                       None, (12327,True )),
    ("ShutdownMonitor",                  "Shutdown Monitor",                    None, (12328,True )),
    ("Hibernate",                        "Hibernate",                           None, (12323,True )),
    ("Standby",                          "Standby",                             None, (12324,True )),
    ("Slumbermode",                      "Slumbermode",                         None, (12325,True )),
    ("Reboot",                           "Reboot",                              None, (12329,True )),
    ("Shutdown",                         "Shutdown",                            None, (12325,True )),
    ("Exit",                             "Exit",                                None, (12294,False)),
    ("ServiceStandby",                   "Service Standby",                     None,  (8272,True )),
    ("ServiceHibernate",                 "Service Hibernate",                   None,  (8274,True )),
    ("ServiceShutdown",                  "Service Shutdown",                    None,  (8273,True )),
    ("ServiceWakeOnLAN",                 "Service Wake on LAN",                 None,  (8275,True )),
    ("ServiceGetEPG",                    "Service get EPG",                     None,  (8276,True ))
)



windowDVBViewer = eg.WindowMatcher( u'dvbviewer.exe',
                                    winName=u'DVB Viewer{*}' )



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
from time import time, strptime, mktime, ctime, strftime, localtime, asctime
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
#from re import IGNORECASE as reIGNORECASE
from base64 import encodestring as encodestring64
from xml.etree import cElementTree as ElementTree
from tempfile import NamedTemporaryFile



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

    serviceDVBViewer      = " By DVBViewer"
    serviceDVBService     = " By DVBViewerService"
    serviceUpdate         = " Update from DVBViewerService"


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


    class GetSetupValue :
        name = "Gets a value from the setup.xml of the DVBViewer."
        section = "Section: "
        setupName = "Name: "
        default = "Default: "


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


    class ShowInfoinTVPic :
        name  = "Show the Infobar in the TVPicture."
        text  = "Displayed message: "
        time  = "Timeinterval [s]: "
        force = "Start DVBViewer if not executing"


    class DeleteInfoinTVPic :
        name  = "Delete the Infobar in the TVPicture."


    class UpdateEPG :
        name = "Update EPG"
        description =   (
                            "For updating, one channel change for each transponder/booklet"
                            "will be done. If a recording is active, the executing of the EPG"
                            "update will be delayed until the recording is finished."
                        )
        disableAV             = "Disable AV"
        time  = "Time between channel change: "
        event = "Fired event after update finished: "


    class AddRecording :
        name = "Add recording to the timer"
        description = (
                    'Add a recording to the timer list. This action should '
                    'be used by scripts or other plugins. The configuration '
                    'tool is only for demonstration.'
                    'This command will not supported in newer versions because'
                    'DVBViewer will not support functions which are necessary'
                    'for this macro in future.'
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


    class GetNumberOfClients :
        name =          "Get the number of connected clients connected to the service"
        serviceUpdate = " Update from DVBViewerService"


    class IsEPGUpdating :
        name =          "Get the DVBViewerService EPG update status"
        serviceUpdate = " Update from DVBViewerService"




class EventHandler:

    # The event gets fired whenever a new action is processed.
    # Parameter :
    #       ActionID        ID of the action ( see actions.ini in the DVBViewer folder)
    #

    def __init__( self ) :
        self.lastActiveChannelNr = -1



    def OnonAction(self, ActionID):
        plugin = self.plugin
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
    def OnonAddRecord(self, ID):
        plugin = self.plugin
        plugin.UpdateRecordingsByDVBViewerEvent()
        if plugin.oldInterface :
            self.TriggerEvent( "AddRecord:" + str(ID) )
        if plugin.newInterface :
            self.TriggerEvent( "AddRecord", ID )
        return True



    # The event gets fired whenever a recording starts.
    # Parameter :
    #       ID                          ID of the timer.
    #       numberOfActiveRecordings    Number of recordings which are now active
    #
    @eg.LogIt
    def OnonStartRecord(self, ID):
        self.plugin.UpdateRecordingsByDVBViewerEvent()
        return True



    # The event gets fired whenever a recording ends.
    # Parameter :
    #       numberOfActiveRecordings    Number of recordings which are still active
    #
    @eg.LogIt
    def OnonEndRecord(self):
        self.plugin.UpdateRecordingsByDVBViewerEvent()
        return True



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
        return True



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
        return True



    # The event gets fired whenever the selectedItem in an OSD list changes.
    #
    def OnonSelectedItemChange(self):
        self.TriggerEvent("SelectedItemChange")
        return True



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
        return True



    # The event gets fired whenever a new playlistitem starts playing.
    # Parameter :
    #       Filename        Filename of the starting playlistitem.
    #
    def OnonPlaylist(self, Filename):
        self.TriggerEvent("Playlist", str(Filename))
        return True



    # The event gets fired whenever a media playback starts.
    #
    def OnonPlaybackstart(self):
        thread = self.plugin.workerThread
        thread.Call( partial( thread.ProcessMediaplayback ) )
        return True



    # The event gets fired whenever a media playback ends.
    #
    def OnPlaybackEnd(self):
        thread = self.plugin.workerThread
        thread.Call( partial( thread.ProcessMediaplayback ) )
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
        return True



    # The event gets fired when the DVBViewer is shutting down.
    @eg.LogIt
    def OnonDVBVClose(self):

        self.plugin.lockedByTerminate = self.plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        plugin = self.plugin

        if not plugin.closeWaitActive :
            plugin.closeWaitActive = True
            plugin.closeWaitLock.acquire( timeout = TERMINATE_TIMEOUT )

        plugin.terminateThread = DVBViewerTerminateThread( self.plugin )
        plugin.terminateThread.start()
        return True




class DVBViewerTerminateThread( Thread ) :

    def __init__( self, plugin ) :

        Thread.__init__(self, name="DVBViewerTerminateThread")
        self.plugin = plugin



    @eg.LogItWithReturn
    def run(self) :
        plugin = self.plugin

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        workerThread = self.plugin.workerThread

        if workerThread is None :
            self.plugin.executionStatusChangeLock.release()
            eg.PrintDebugNotice( "DVBViewer is not disconnected by the close event processing" )
            return True

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        plugin.workerThread = None

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        CoInitialize()

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )
        
        queryA = "SELECT * FROM Win32_ProcessStopTrace WHERE ProcessName='dvbviewer.exe'"
        queryU = (
                   "SELECT * FROM __InstanceDeletionEvent  WITHIN 1 "
                   "WHERE TargetInstance ISA 'Win32_Process' "
                   "AND TargetInstance.Name='dvbviewer.exe'"
                 )

        WMI = GetObject('winmgmts:')

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )
        events = None

        try :
            events = WMI.ExecNotificationQuery( queryA )
        except :
            events = WMI.ExecNotificationQuery( queryU )

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        finished = True

        if len( WMI.ExecQuery('select * from Win32_Process where Name="dvbviewer.exe"') ) > 0 :

            try :
                events.NextEvent( TERMINATE_TIMEOUT * 1000 )

            except :

                eg.PrintDebugNotice("DVBViewer could not be terminated")
                plugin.TriggerEvent( "DVBViewerCouldNotBeTerminated" )
                finished = False

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        if finished :
            plugin.DVBViewerIsFinished()

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        if workerThread is not None :
            if workerThread.Stop( TERMINATE_TIMEOUT ) :
                eg.PrintError("Could not terminate DVBViewer thread")
                plugin.TriggerEvent( "DVBViewerCouldNotBeTerminated" )

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        del events

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        del WMI

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        CoUninitialize()

        plugin.lockedByTerminate |= plugin.executionStatusChangeLock.acquire( blocking = False, timeout = TERMINATE_TIMEOUT )

        plugin.terminateThread = None

        if plugin.lockedByTerminate :
            plugin.executionStatusChangeLock.release()
            plugin.lockedByTerminate = False
        return finished




class DVBViewerWorkerThread(eg.ThreadWorker):
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



    def GetCurrentChannelNr( self ) :
        return self.dvbviewer.CurrentChannelNr



    def GetSetupValue( self, section, name, default ) :
        return self.dvbviewer.GetSetupValue( section, name, default )



    def GetChannelList( self ) :
        channelManager = self.dvbviewer.ChannelManager
        return channelManager.GetChannelList( )



    @eg.LogItWithReturn
    def TuneChannelIfNotRecording( self, channelNr, text = "", time = 0.0) :
        dvbviewer = self.dvbviewer
        timerCollection = dvbviewer.TimerManager

        if not timerCollection.Recording :
            dvbviewer.CurrentChannelNr = channelNr
            self.ShowInfoinTVPic( text, time + 2 )
            return True
        else :
            return False



    def ShowInfoinTVPic( self, text = "", time = 10.0 ) :
        dvbviewer = self.dvbviewer
        if text != "" :
            dvbviewer.OSD.ShowInfoinTVPic( text, time * 1000 )
        return True



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
        return True



    def IfMustInList( self, now, record, active, recordingsIDsService ) :

        if record[ 4 ] not in recordingsIDsService :

            tStart = mktime( strptime( str(record[5])+str(record[6]),"%d.%m.%Y 00:00:0030.12.1899 %H:%M:%S" ) )

            if tStart <= now :

                tStop  = mktime( strptime( str(record[5])+str(record[7]),"%d.%m.%Y 00:00:0030.12.1899 %H:%M:%S" ) )

                if tStart > tStop :
                    tStop = tStop + 24*60*60

                if tStop <= now :
                    return False

            if active and not record[11] :
                return False
            return True
        return False



    def GetRecordings( self, active = True, update = False ) :

        plugin = self.plugin

        recordingsIDsService = {}
        if plugin.useService and self.GetSetupValue( 'Service', 'Timerlist', '0' ) != '0' :
            recordingsIDsService = plugin.service.GetPseudoIDs( update )

        all = self.dvbviewer.TimerManager.GetTimerList()[1]

        now = time()

        list = [ record for record in all if self.IfMustInList( now, record, active, recordingsIDsService ) ]

        #print "active = ", active, "  list = ", list

        return list



    def GetRecordingsIDs( self, active = True, update = False ) :
        plugin = self.plugin

        recordingsIDsService = {}
        if plugin.useService and self.GetSetupValue( 'Service', 'Timerlist', '0' ) != '0' :
            recordingsIDsService = plugin.service.GetPseudoIDs( update )

        all = self.dvbviewer.TimerManager.GetTimerList()[1]

        now = time()


        IDs = [ record[ 4 ] for record in all if self.IfMustInList( now, record, active, recordingsIDsService ) ]

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
        return True



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

        count = self.dvbviewer.TimerManager.Count

        try :
            timerItem = self.dvbviewer.TimerManager.AddItem( channelID, pDate, pStart, pEnd,
                                                             description, disableAV, enabled,
                                                             recAction, actionAfterRec, days )
        except :
            pass        #in case of "this is deprecated and will go away on"

        return True




class DVBViewerWatchDogThread( Thread ) :

    def __init__( self, plugin, watchDogTime ) :

        Thread.__init__(self, name="DVBViewerWatchDogThread")
        self.plugin = plugin
        self.abort = False
        self.watchDogTime = watchDogTime
        self.started = False



    @eg.LogItWithReturn
    def run(self) :
        if self.watchDogTime == 0 :
            return False
        plugin = self.plugin
        CoInitialize()

        queryTime = 5

        if self.watchDogTime < queryTime :
            queryTime = self.watchDogTime

        queryU = (
                "SELECT * FROM __InstanceOperationEvent  WITHIN " + str( queryTime) +
                " WHERE TargetInstance ISA 'Win32_Process' "
                "AND TargetInstance.Name='dvbviewer.exe'" )

        queryA = ( "SELECT * FROM Win32_ProcessTrace WHERE ProcessName='dvbviewer.exe'" )

        WMI = GetObject('winmgmts:')
        
        eventSource = None
        startType = 'Win32_ProcessStartTrace'
        stopType  = 'Win32_ProcessStopTrace'

        try :
            eventSource = WMI.ExecNotificationQuery( queryA )
            #print "Administrator rights"
        except :
            eventSource = WMI.ExecNotificationQuery( queryU )
            startType = '__InstanceCreationEvent'
            stopType  = '__InstanceDeletionEvent'
            #print "User rights"


        self.started = len( WMI.ExecQuery('select * from Win32_Process where Name="dvbviewer.exe"') ) > 0

        nextTimeViewer = time()

        timeout = True

        while not self.abort :
            try :
                eventType = eventSource.NextEvent( 500 ).Path_.Class
                if eventType == startType and not self.started :
                    #print "DVBViewer started"
                    eg.PrintDebugNotice("DVBViewer started")
                elif eventType == stopType and self.started:
                    #print "DVBViewer terminated"
                    eg.PrintDebugNotice("DVBViewer terminated")
                elif time() < nextTimeViewer :
                    continue
            except :
                #print "Timeout"
                if time() < nextTimeViewer :
                    continue
                timeout = True

            plugin.executionStatusChangeLock.acquire( timeout = TERMINATE_TIMEOUT )

            if plugin.useService and timeout :
                plugin.service.Update( UPDATE_ALL )

            if plugin.closeWaitActive :
                plugin.executionStatusChangeLock.release()
                continue

            started = len( WMI.ExecQuery('select * from Win32_Process where Name="dvbviewer.exe"') ) > 0
            if self.started == started and not timeout :
                plugin.executionStatusChangeLock.release()
                continue

            self.started = started
            timeout = False

            #print "started = ", self.started, "  workerThread = ", plugin.workerThread

            nextTimeViewer = time() + self.watchDogTime

            if not self.started and plugin.workerThread is not None :
                #print "WatchDog: Disconnect"
                eg.PrintDebugNotice( "Termination of DVBViewer detected by watch dog" )
                if plugin.workerThread.Stop( TERMINATE_TIMEOUT ) :
                    eg.PrintError("Could not terminate DVBViewer thread")
                plugin.workerThread = None
                plugin.DVBViewerIsFinished()

            elif self.started and plugin.workerThread is None :
                #print "WatchDog: Connect"
                eg.PrintDebugNotice( "DVBViewer will be connected by watch dog" )
                plugin.Connect( CONNECT )

            if plugin.workerThread is not None :
                #print "WatchDog: Update recordings"

                updatedRecordings = 0

                try :
                    plugin.checkEventHandlingLock.acquire( blocking = False, timeout = CALLWAIT_TIMEOUT )
                    if plugin.SendCommand( DUMMY_ACTION, lock = False, connectionMode = CHECK_CONNECT ) :
                        updatedRecordings = plugin.UpdateRecordings( lock = False, updateService = False )
                    else :
                        plugin.checkEventHandlingLock.acquire( blocking = False )
                        plugin.checkEventHandlingLock.release()
                except :
                    eg.PrintDebugNotice("DVBViewer could not accessed by the Watch Dog Thread")
                    plugin.TriggerEvent( "DVBViewerCouldNotBeConnected" )
                    plugin.checkEventHandlingLock.acquire( blocking = False )
                    plugin.checkEventHandlingLock.release()
                else :
                    if updatedRecordings > 0 :
                        eg.PrintDebugNotice(    "Number of recordings ("
                                              + str(updatedRecordings)
                                              + ") was updated  by watch dog" )
            plugin.executionStatusChangeLock.release()

        del eventSource
        del WMI
        CoUninitialize()
        return True



    @eg.LogIt
    def Finish( self ) :
        plugin = self.plugin
        plugin.checkEventHandlingLock.acquire( blocking = False )
        plugin.checkEventHandlingLock.release()
        self.abort = True
        self.started = False
        return True




class DVBViewer(eg.PluginClass):
    text = Text

    class LockWithTimeout :

        def Timeout( self ) :
            eg.PrintDebugNotice('DVBViewer plugin lock "' + self.name + '" timeout detected, lock released')
            eg.PrintError( "Error: Lock released to prevent a dead lock" )
            self.lock.release()
            return True


        def __init__( self, name, timeoutFunc = Timeout , *args, **kwargs ) :
            self.timeoutFunc = partial(timeoutFunc, self, *args, **kwargs)
            self.timer = None
            self.lock = Lock()
            self.name = name


        def __del__(self) :
            if self.timer is not None :
                self.timer.cancel()
                del self.timer
                self.timer = None
                eg.PrintDebugNotice('Warning: Lock object "' + self.name + ' deleted while lock')
            del self.lock


        def acquire( self, blocking=True, timeout = CALLWAIT_TIMEOUT-10 ) :
            #print "Acquire: blocking = ", blocking
            blocked = self.lock.acquire( blocking )
            if blocked :
                self.timer = Timer( timeout, self.timeoutFunc )
                self.timer.start()
            #print "Acquired: blocking = ", blocking, "  retrun = ", ret
            return blocked


        def release( self ) :
            ret = True
            if self.timer is not None :
                self.timer.cancel()
                del self.timer
                self.timer = None
                self.lock.release()
            else :
                eg.PrintDebugNotice('DVBViewer plugin unlocked lock "' + self.name + '" release detected')
                eg.PrintError( "Error: unlock lock released" )
                ret = False
            #print "Released"
            return ret



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
        self.AddAction(ShowInfoinTVPic)
        self.AddAction(DeleteInfoinTVPic)
        self.AddAction(GetSetupValue)
        self.AddAction(SendAction)
        self.AddAction(GetNumberOfClients)
        self.AddAction(IsEPGUpdating)
        self.AddAction(GetDVBViewerObject, hidden = True)
        self.AddAction(ExecuteDVBViewerCommandViaCOM, hidden = True)

        class ActionPrototype(eg.ActionClass):
            def __call__(self2):
                if self2.value[1] :
                    connectionMode = WAIT_CHECK_START_CONNECT
                else :
                    connectionMode = CHECK_CONNECT
                return self.SendCommand(self2.value[0], connectionMode = connectionMode )
        self.AddActionsFromList(ACTIONS, ActionPrototype)

        # create a new subclass of the EventHandler with the ability to use
        # the plugin's TriggerEvent method
        class SubEventHandler(EventHandler):
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

        self.completeRecordingsInfo = []

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

        self.updateRecordingsTimer = None

        self.updateRecordingsLock      = self.LockWithTimeout( "UpdateRecordings" )

        self.executionStatusChangeLock = self.LockWithTimeout( "ExecutionStatusChange" )
        self.lockedByTerminate = False

        def CheckEventHandlingFunc( self, plugin ) :
            plugin.checkEventHandlingLock.release()
            eg.PrintDebugNotice("DVBViewer event handling not alive")
            plugin.TriggerEvent( "DVBViewerEventHandlingNotAlive" )
            return False

        self.checkEventHandlingLock    = self.LockWithTimeout( "CheckEventHandling", CheckEventHandlingFunc, self )

        def WaitForTerminationTimeoutFunc( self, plugin ) :
            plugin.closeWaitLock.release()
            plugin.closeWaitActive = False
            plugin.timeout = True
            eg.PrintDebugNotice("DVBViewer could not be terminated")
            plugin.TriggerEvent( "DVBViewerCouldNotBeTerminated" )
            return False

        self.closeWaitLock             = self.LockWithTimeout( "CloseWait", WaitForTerminationTimeoutFunc, self )
        self.closeWaitActive  = False
        self.timeout = False

        self.infoInTVPicTimeout = 0.0

        self.DVBViewerService = None
        self.useService = False



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
        return True



    @eg.LogItWithReturn
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
                    useService = False,
                    watchDogTime = 60.0,
                    schedulerTaskNamePrefix = "StartRecording",
                    schedulerEventName      = "StartRecording",
                    schedulerLeadTime       = 3.0,
                    scheduleAllRecordings   = False,
                    schedulerEntryHidden    = False,
                    waitTimeBeforeConnect = 5.0,
                    serviceAddress = '127.0.0.1:80',
                    serviceEvent = 'DVBViewerService',
                    dummy = False
                    ) :
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

        version = self.service.GetVersion()

        if version is not None :
            eg.PrintDebugNotice( "DVBViewerServiceVersion : ", version )

        return True



    @eg.LogItWithReturn
    def __stop__(self):
        # If the DVBViewer was started by the COM interface, the DVBViewer must be terminated before
        # stopping the DVBViewer Thread. Otherwise the DVBViewer is going into an endless loop.
        if self.tuneEPGThread is not None :
            self.tuneEPGThread.Finish()

        if self.watchDogThread is not None :
            self.watchDogThread.Finish()
            self.watchDogThread.join()
            self.watchDogThread = None

        self.executionStatusChangeLock.acquire( timeout = TERMINATE_TIMEOUT )
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



    def DVBViewerIsFinished( self ) :
        self.UpdateRecordings( lock = False )
        self.TriggerEvent( "Close" )
        if self.closeWaitActive :
            self.closeWaitActive = False
            self.closeWaitLock.release()
        self.checkEventHandlingLock.acquire( blocking = False )
        self.checkEventHandlingLock.release()
        return True



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



    def UpdateRecordingsByDVBViewerEvent( self ) :

        @eg.LogItWithReturn
        def UpdateRecordings(self) :
            plugin = self
            lock = plugin.updateRecordingsLock
            lock.acquire()
            plugin.updateRecordingsTimer = None
            lock.release()
            plugin.UpdateRecordings()

        lock = self.updateRecordingsLock
        lock.acquire()

        if self.updateRecordingsTimer is not None :
            self.updateRecordingsTimer.cancel()

        self.updateRecordingsTimer = Timer( 1.1, self.UpdateRecordings )  #A thread is necessary in case of a DVBViewer dead lock
        self.updateRecordingsTimer.start()

        lock.release()

        return True



    def UpdateRecordings( self, lock = True, updateService = False ) :

        if lock :
            self.executionStatusChangeLock.acquire()

        recordingsIDs = []
        completeRecordingsInfo = []

        started = False


        if self.workerThread is not None :
            completeRecordingsInfo = self.workerThread.CallWait(
                        partial(self.workerThread.GetRecordings, False, updateService ),
                        CALLWAIT_TIMEOUT
            )
            recordingsIDs = [ record[ 4 ] for record in completeRecordingsInfo if record[ 11 ] ]
            started = True

        if lock :
            self.executionStatusChangeLock.release()

        numberOfActiveRecordings = len( recordingsIDs )

        newRecordingsIDs     = [ ID for ID in recordingsIDs if ID not in self.firedRecordingsIDs ]
        #print "newRecordingsIDs = ", newRecordingsIDs

        updatedRecordings = 0

        if self.numberOfActiveRecordings != numberOfActiveRecordings or len( newRecordingsIDs ) != 0 :

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
            updatedRecordings = newRecordings + removed

            if self.numberOfActiveRecordings == 0 :
                self.TriggerEvent( "AllActiveRecordingsFinished" )

        if started :
            if completeRecordingsInfo != self.completeRecordingsInfo :
                self.TriggerEvent( "TimerListUpdated" )
                self.completeRecordingsInfo = completeRecordingsInfo

        return updatedRecordings



    def SendCommandThroughSendMessage(self, value, lock = True, connectionMode = WAIT_CHECK_START_CONNECT):
        try:
            hwnd = gWindowMatcher()[0]
            return SendMessageTimeout(hwnd, 45762, 2069, 100 + value)
        except:
            raise self.Exceptions.ProgramNotRunning
        return True



    def SendCommandThroughCOM(self, value, lock = True, connectionMode = WAIT_CHECK_START_CONNECT ):
        if lock :
            self.executionStatusChangeLock.acquire()
        ececuted = False
        if self.Connect( connectionMode ) :
            self.workerThread.CallWait(
                partial(self.workerThread.dvbviewer.SendCommand, value),
                CALLWAIT_TIMEOUT
            )
            ececuted = True
        if lock :
            self.executionStatusChangeLock.release()
        return ececuted



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
        self.executionStatusChangeLock.acquire()
        try :
            if self.Connect( WAIT_CHECK_START_CONNECT ) :
                ret = self.workerThread.CallWait(
                        partial( self.workerThread.TuneChannelIfNotRecording, channelNr, text, time ),
                        CALLWAIT_TIMEOUT
                     )
        except :
            pass
        self.executionStatusChangeLock.release()
        return ret



    def WaitForTermination( self, sendCloseCommand = False, block = True ) :

        self.executionStatusChangeLock.acquire()

        if block :
            self.closeWaitActive = True

        if sendCloseCommand :
            self.SendCommand( DVBVIEWER_CLOSE[1], lock = False )

        if block :
            self.closeWaitLock.acquire( timeout = TERMINATE_TIMEOUT )

        self.timeout = False

        self.executionStatusChangeLock.release()

        if block :
            self.closeWaitLock.acquire()
            self.closeWaitLock.release()

        return not self.timeout



    def Connect( self, connectingMode = WAIT_CHECK_START_CONNECT, lock = False ) :
        #WAIT_CHECK_START_CONNECT  = 0   #wait for free, check if executing, start if not executing, connect
        #CONNECT                   = 1   #connect
        #CHECK_CONNECT             = 2   #connect only, if executing

        def WaitForDVBViewerWindow( timeout ) :
            end = time() + timeout
            while True:
                if len( windowDVBViewer() ) > 0 :
                    return True
                elif time() >= end :
                    return False
                eg.Wait(0.25)


        self.closeWaitLock.acquire()
        self.closeWaitLock.release()

        if lock :
            self.executionStatusChangeLock.acquire()

        started = False

        if self.workerThread is None :
            timeout = 20.0
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
                            return False
                        self.DVBViewerStartedByCOM = False
                        timeout = 60.0
                    else :
                        self.DVBViewerStartedByCOM = True
                    started = True
                del WMI
            else :
                self.DVBViewerStartedByCOM = False
                started = True
            if started :
                if not self.DVBViewerStartedByCOM :
                    found = WaitForDVBViewerWindow( timeout )
                    if not found:
                        eg.PrintError( "Warning: DVBViewer window not found. Hidden?" )
                        eg.PrintDebugNotice( "DVBViewer window not found. Hidden?" )
                    eg.Wait( self.waitTimeBeforeConnect )    #  necessary otherwise hang up
                self.workerThread = DVBViewerWorkerThread(self)
                try:
                    self.workerThread.Start( 60.0 )
                except:
                    self.TriggerEvent( "DVBViewerCouldNotBeConnected" )
                    eg.PrintDebugNotice( "DVBViewer couldn't be connected" )
                    self.workerThread = None
                    if lock :
                        self.executionStatusChangeLock.release()
                    return False

                if len( self.tvChannels ) == 0 and len( self.radioChannels ) == 0 :
                    self.GetChannelLists()
                    #print self.tvChannels
                    #print self.radioChannels

        if lock :
            self.executionStatusChangeLock.release()

        return self.workerThread



    def ServiceConfigure(  self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False, affirmed = True, panel = None ) :

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
                    useService = False,
                    watchDogTime = 60.0,
                    schedulerTaskNamePrefix = "StartRecording",
                    schedulerEventName      = "StartRecording",
                    schedulerLeadTime       = 3.0,
                    scheduleAllRecordings   = False,
                    schedulerEntryHidden    = False,
                    waitTimeBeforeConnect = 5.0,
                    serviceAddress = '127.0.0.1:80',
                    serviceEvent = 'DVBViewerService',
                    dummy = False
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


        def onPasswordChange( event, forceAccount = -1 ) :
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



    def HandlePasswordFile( self, write = False, accounts=[('','')] ) :

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



    def Crypt( self, string, key, gen = True ) :
        m = hashlib.md5()
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




class Start(eg.ActionClass):

    def __call__(self):
        self.plugin.Connect( WAIT_CHECK_START_CONNECT, lock = True )
        return True




class CloseDVBViewer( eg.ActionClass ) :

    def __call__( self, waitForTermination = False ) :
        plugin = self.plugin
        if plugin.workerThread is None :
            return False

        return plugin.WaitForTermination( sendCloseCommand = True, block = waitForTermination )


    def Configure(  self, waitForTermination = False ) :

        plugin = self.plugin

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

    def __call__( self ) :
        plugin = self.plugin
        plugin.executionStatusChangeLock.acquire()
        if plugin.Connect( CHECK_CONNECT ) :
            plugin.workerThread.CallWait(
                        partial(plugin.workerThread.StopAllActiveRecordings ),
                        CALLWAIT_TIMEOUT
            )
        plugin.executionStatusChangeLock.release()
        return True




class GetNumberOfActiveRecordings( eg.ActionClass ) :

    def __call__( self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :
        plugin = self.plugin

        count = 0
        if enableDVBService :
            count = plugin.service.GetNumberOfActiveRecordings( updateDVBService )

        plugin.executionStatusChangeLock.acquire()
        if enableDVBViewer :
            if plugin.Connect( CHECK_CONNECT ) :
                list =  plugin.workerThread.CallWait(
                                 partial(plugin.workerThread.GetRecordingsIDs,
                                         True, not enableDVBService and updateDVBService ),
                                 CALLWAIT_TIMEOUT
                             )
                count += len( list )

        plugin.executionStatusChangeLock.release()
        return count



    def Configure(  self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        self.plugin.ServiceConfigure( enableDVBViewer, enableDVBService, updateDVBService )




class GetRecordingsIDs( eg.ActionClass ) :

    def __call__( self, active = True, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :
        plugin = self.plugin

        list = []

        if enableDVBService :

            plugin.executionStatusChangeLock.acquire()
            recordingIDs = plugin.service.GetRecordingsIDs( updateDVBService )
            if recordingIDs is None :
                recordingIDs = {}
            plugin.executionStatusChangeLock.release()

            for k, v in recordingIDs.iteritems() :
                if v[0] or not active :
                    list.append( v[2] )

        if enableDVBViewer :

            connectionMode = WAIT_CHECK_START_CONNECT
            if active :
                connectionMode = CHECK_CONNECT

            plugin.executionStatusChangeLock.acquire()
            if plugin.Connect( connectionMode ) :
                list.extend( plugin.workerThread.CallWait(
                                 partial(plugin.workerThread.GetRecordingsIDs, active,
                                         not enableDVBService and updateDVBService ),
                                 CALLWAIT_TIMEOUT
                             ) )
            plugin.executionStatusChangeLock.release()
        return list



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

    def __call__( self ) :
        plugin = self.plugin
        plugin.executionStatusChangeLock.acquire()
        res = self.plugin.workerThread
        plugin.executionStatusChangeLock.release()
        return res




class IsRecording( eg.ActionClass ) :

    def __call__( self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :
        return eg.plugins.DVBViewer.GetNumberOfActiveRecordings(
                                                        enableDVBViewer,
                                                        enableDVBService,
                                                        updateDVBService ) != 0



    def Configure(  self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        self.plugin.ServiceConfigure( enableDVBViewer, enableDVBService, updateDVBService )




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
        return True




class ShowInfoinTVPic( eg.ActionClass ) :

    def __call__( self, text = "", timeout = 15.0, force = False ) :

        connectMode = CHECK_CONNECT
        if force :
            connectMode = WAIT_CHECK_START_CONNECT

        plugin = self.plugin

        if plugin.Connect( connectMode, lock = True ) :
            plugin.workerThread.CallWait(
                                        partial(
                                            plugin.workerThread.ShowInfoinTVPic,
                                            " "+ text + " ", timeout
                                         ),
                                         CALLWAIT_TIMEOUT
                         )

            plugin.infoInTVPicTimeout = time() + timeout

            return True

        return False



    def Configure( self, displayText = "", timeout = 15.0, force = False ) :

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

    def __call__( self ) :

        plugin = self.plugin
        if plugin.infoInTVPicTimeout > time() + 0.01 :

            plugin.infoInTVPicTimeout = 0.0

            if plugin.Connect( CHECK_CONNECT, lock = True ) :
                plugin.workerThread.CallWait(
                            partial( plugin.workerThread.ShowInfoinTVPic, " ", 0 ),
                            CALLWAIT_TIMEOUT
                         )
                return True
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

                    if plugin.numberOfActiveRecordings == 0 :

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



    def Configure(  self, timeBetweenChannelChange = 60.0, disableAVafterChannelChange = True, event = "EPGUpdateFinished" ) :

        plugin = self.plugin
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

        plugin.executionStatusChangeLock.acquire()
        if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
            plugin.workerThread.CallWait(
               partial( plugin.workerThread.AddRecording, channelID, date, startTime,
                                                          endTime, description, disableAV,
                                                          enabled, recAction, actionAfterRec,
                                                          days
                      ),
               CALLWAIT_TIMEOUT
            )

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

            id = plugin.IDbychannelIDList[ channelID ]
            self.tv = id[1]

            if ( self.tv ) :
                self.choices = plugin.tvChannels
            else :
                self.choices = plugin.radioChannels

            ix = id[0]
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

    def __call__( self, section = "", name = "", default = "" ) :

        plugin = self.plugin
        if plugin.Connect( WAIT_CHECK_START_CONNECT, lock = True ) :
            res = plugin.workerThread.CallWait(
                        partial( plugin.workerThread.GetSetupValue, section, name, default ),
                        CALLWAIT_TIMEOUT
                     )
            return res
        return default



    def Configure(  self, section = "", name = "", default = "" ) :

        plugin = self.plugin

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




class GetDateOfRecordings( eg.ActionClass ) :

    def __call__( self,
                  allRecordings = False,
                  enableDVBViewer = True,
                  enableDVBService = False,
                  updateDVBService = False
                ) :

        plugin = self.plugin

        plugin.executionStatusChangeLock.acquire()

        readOutSuccessfull = True

        recordingDates = []

        if enableDVBService :
            recordingDates = plugin.service.GetRecordingDates( False, update = updateDVBService )
            if recordingDates is None :
                recordingDates = []
                readOutSuccessfull = False

        plugin.executionStatusChangeLock.release()

        if enableDVBViewer :

            plugin.executionStatusChangeLock.acquire()
            if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
                recordingList = plugin.workerThread.CallWait( partial( plugin.workerThread.GetRecordings,
                                                                       False,
                                                                       updateDVBService and not enableDVBService ),
                                    CALLWAIT_TIMEOUT )
                plugin.executionStatusChangeLock.release()
                now = time()
                for record in recordingList :
                    if record[8] :                  # Recording enabled

                        if record[18] ==1 and record[0] == "EPG-Update by EventGhost" :
                            continue

                        nextDate = record[5]
                        nextTime = record[6]

                        #nextDate =  19.07.2008 00:00:00    nextTime =  30.12.1899 05:15:00
                        t = mktime( strptime( str(nextDate)+str(nextTime),"%d.%m.%Y 00:00:0030.12.1899 %H:%M:%S" ) )

                        if t < now :
                            continue
                        if not t in recordingDates :
                            recordingDates.append(t)
                        #print "date = ", ctime(t)
            else :
                plugin.executionStatusChangeLock.release()
                readOutSuccessfull = False

        recordingDates.sort()

        if allRecordings :
            return ( readOutSuccessfull, recordingDates )
        else :
            if len( recordingDates ) == 0 :
                return ( readOutSuccessfull, -1 )
            else :
                return ( readOutSuccessfull, recordingDates[ 0 ] )



    def Configure(  self, allRecordings = False, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        plugin = self.plugin

        panel = eg.ConfigPanel()

        checkBox = wx.CheckBox( panel, -1, self.text.all )
        checkBox.SetValue( allRecordings )

        panel.sizer.Add( checkBox )
        panel.sizer.Add(wx.Size(0,10))

        getFlags = plugin.ServiceConfigure(  enableDVBViewer, enableDVBService, updateDVBService, affirmed = False, panel = panel )

        while panel.Affirmed():
             allRecordings      = checkBox.GetValue()

             enableDVBViewer, enableDVBService, updateDVBService = getFlags()

             panel.SetResult( allRecordings, enableDVBViewer, enableDVBService, updateDVBService )




class TaskScheduler( eg.ActionClass ) :

    @eg.LogItWithReturn
    def __call__( self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        plugin = self.plugin

        leadTime = plugin.schedulerLeadTime * 60.0

        recordingDates = eg.plugins.DVBViewer.GetDateOfRecordings(
                                                    allRecordings = plugin.scheduleAllRecordings,
                                                    enableDVBViewer = enableDVBViewer,
                                                    enableDVBService = enableDVBService,
                                                    updateDVBService = updateDVBService )

        if not recordingDates[0] :
            eg.PrintError( "dates not valid" )
            return False

        dates = []

        if plugin.scheduleAllRecordings :
            dates = recordingDates[1]

        elif recordingDates[1] > 0 :
            dates = [ recordingDates[1] ]

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



    def Configure(  self, enableDVBViewer = True, enableDVBService = False, updateDVBService = False ) :

        self.plugin.ServiceConfigure( enableDVBViewer, enableDVBService, updateDVBService )





class GetDVBViewerObject( eg.ActionClass ) :

    def __call__( self ) :
        plugin = self.plugin
        result = None
        if plugin.Connect( WAIT_CHECK_START_CONNECT, lock = True ) :
            return plugin.workerThread.dvbviewer
        return None




class ExecuteDVBViewerCommandViaCOM( eg.ActionClass ) :

    def __call__( self, command, *args, **kwargs ) :
        plugin = self.plugin
        result = None
        plugin.executionStatusChangeLock.acquire()
        if plugin.Connect( WAIT_CHECK_START_CONNECT ) :
            result = plugin.workerThread.CallWait(
                        partial( command, *args, **kwargs ),
                        CALLWAIT_TIMEOUT
            )
        plugin.executionStatusChangeLock.release()
        return result




class GetNumberOfClients( eg.ActionClass ) :

    def __call__( self, update = False ) :
        plugin = self.plugin

        if not plugin.useService :
            return -1

        return self.plugin.service.GetNumberOfClients( update )

    def Configure( self, updateDVBService = False ) :

        panel = eg.ConfigPanel()

        text = self.text

        updateCheckBoxCtrl = wx.CheckBox(panel, -1, text.serviceUpdate)
        updateCheckBoxCtrl.SetValue( updateDVBService )

        panel.sizer.Add( updateCheckBoxCtrl )


        while panel.Affirmed():

            panel.SetResult(updateCheckBoxCtrl.GetValue() )



class IsEPGUpdating( eg.ActionClass ) :

    def __call__( self, update = False ) :
        plugin = self.plugin

        if not plugin.useService :
            return False

        return self.plugin.service.IsEPGUpdating( update )



    def Configure( self, updateDVBService = False ) :

        panel = eg.ConfigPanel()

        text = self.text

        updateCheckBoxCtrl = wx.CheckBox(panel, -1, text.serviceUpdate)
        updateCheckBoxCtrl.SetValue( updateDVBService )

        panel.sizer.Add( updateCheckBoxCtrl )


        while panel.Affirmed():

            panel.SetResult(updateCheckBoxCtrl.GetValue() )




class DVBViewerService() :

    def __init__( self, plugin, serviceAddress = '127.0.0.1:80',
                  account = ( 'admin', 'admin' ),
                  serviceEvent = 'DVBViewerService') :

        self.serviceAddress = serviceAddress
        self.account = account

        self.simulateDVBViewerInterface = True

        self.recordingIDs = {}       #Key: ID, Value: Recording
        self.pseudoIDs = {}
        self.numberOfRecordings = 0
        self.recordingDates       = []
        self.activeRecordingDates = []

        self.versionDVBViewerService = None

        self.serviceEvent = serviceEvent

        self.failing = False

        self.plugin = plugin

        self.numberOfClients = -1
        self.updateEPG = False




    def TriggerEvent( self, suffix, payload=None ):
            return eg.TriggerEvent( suffix, payload = payload, prefix=self.serviceEvent, source=self.plugin)



    def GetData( self, interface ) :

        def ErrorProcessing( e ) :
            if hasattr(e, 'code') and e.code == 401 :
                eg.PrintError( "Setup error: DVBViewer Service password not correct" )
                return None
            elif hasattr(e, 'errno') :
                if e.errno != 10054 :
                    eg.PrintError( "DVBViewer Service not alive or service address/port are not correct" )
                    self.TriggerEvent( "ServiceNotAlive" )
                    self.failing = True
                    return None
                else :
                    print e.code
                    self.failing = True
                    raise
            else :
                raise
            return

        interface = interface.lower()

        theurl = (   'http://' + self.serviceAddress
                   + '/API/' + interface + '.html')

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

        return pageHandle.read()



    def Update( self, type = UPDATE_RECORDINGS ) :

        def GetID( *args ) :

            m = hashlib.md5()
            for arg in args:
                m.update(arg.encode("utf-8"))
            id = 0
            for c in m.hexdigest() :
                id = id * 251 + ord(c)

            return id


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


        plugin = self.plugin

        if self.versionDVBViewerService is None :

            xmlData = self.GetData( 'version' )

            if xmlData is None :
                return False

            # EXAMPLE of xmldata:

            #<?xml version="1.0" encoding="utf-8" ?>
            #<version>DVBViewer Recording Service 1.5.0.2 (beta) (TOWER2008)</version>

            tree = ElementTree.fromstring( xmlData )

            matchObject = reSearch( r'(\d+\.\d+\.\d+\.\d+)', tree.text )

            self.versionDVBViewerService = matchObject.group(1)

        if type & UPDATE_RECORDINGS != 0 :

            xmlData = self.GetData( 'timerlist' )

            if xmlData is None :
                xmlData = '<?xml version="1.0" encoding="iso-8859-1"?><Timers/>'

            self.recordingDates = []
            self.activeRecordingDates = []

            #print xmlData

            """
             EXAMPLE of xmldata:

            <?xml version="1.0" encoding="iso-8859-1"?>
            <Timers>
               <Timer Type="1" Enabled="0" Priority="50" Date="05.07.2999" Start="23:39:00" End="00:09:00" Action="0">
                   <Descr>Bayerisches FS Süd (deu)</Descr>
                   <Options AdjustPAT="-1" AllAudio="-1" DVBSubs="-1" Teletext="-1"/>
                   <Format>2</Format>
                   <Folder>Auto</Folder>
                   <NameScheme>%event_%date_%time</NameScheme>
                   <Log Enabled="-1" Extended="0"/>
                   <Channel ID="550137291|Bayerisches FS Süd (deu)"/>
                   <Executeable>0</Executeable>
                   <Recording>0</Recording>
                   <ID>0</ID>
               </Timer>
               <Timer Type="1" Enabled="-1" Priority="50" Date="05.07.2009" Start="18:35:00" End="19:50:00" Action="0">
                   <Descr>Lindenstrasse</Descr>
                   <Options AdjustPAT="-1"/>
                   <Format>2</Format>
                   <Folder>Auto</Folder>
                   <NameScheme>%event_%date_%time</NameScheme>
                   <Log Enabled="-1" Extended="0"/>
                   <Channel ID="543583690|Das Erste (deu)"/>
                   <Executeable>-1</Executeable>
                   <Recording>-1</Recording>
                   <ID>1</ID>
               </Timer>
            </Timers>
            """

            tree = ElementTree.fromstring( xmlData )

            #tree = ElementTree.parse( "C:\\Dokumente und Einstellungen\\Stefan Gollmer\\Desktop\\timer.xml" )

            now = time()

            IDs = {}
            pseudoIDs = {}

            for timer in tree.findall("Timer"):

                enabled     = ( timer.get( "Enabled","-1" ) != '0')
                recording   = ( GetText( timer, "Recording" ) != '0' )
                action      = timer.get( "Action","0" )

                date        = timer.get( "Date","" )
                startTime   = timer.get( "Start","" )
                endTime     = timer.get( "End","" )
                channelID   = timer.find( "Channel" ).get( "ID","")
                description = GetText( timer, "Descr" )
                pseudoID    = int( GetText( timer, "ID" ) )

                t = mktime( strptime( date + startTime,"%d.%m.%Y%H:%M:%S" ) )

                id = GetID( date, startTime, endTime, action, channelID, str( pseudoID ) )

                pseudoIDs[ pseudoID ] = id

                if id not in self.recordingIDs :
                    if plugin.oldInterface :
                        self.TriggerEvent( "AddRecord:" + str(pseudoID) )
                    if plugin.newInterface :
                        self.TriggerEvent( "AddRecord", pseudoID )

                IDs[ id ] = ( recording, enabled, pseudoID )

                #print "ID = ", id, "  recording = ", recording, "  IDs[ id ] = ", IDs[ id ]

                if enabled : #and action == '0' :

                    if t < now :
                        continue
                    if not t in self.recordingDates:
                        self.recordingDates.append(t)
                        if recording :
                            self.activeRecordingDates.append(t)
                        #print "date = ", ctime(t)

            numberOfRecordings = self.numberOfRecordings

            #print self.recordingDates
            #print "isRecording = ", isRecording

            if self.recordingIDs != IDs :

                for k, v in self.recordingIDs.iteritems() :
                    g = IDs.get( k )
                    if v[0] and ( g is None or not g[0] ) :    # last query time recording but not now
                        numberOfRecordings -= 1
                        if plugin.oldInterface :
                            self.TriggerEvent( "EndRecord" )
                        if plugin.newInterface :
                            self.TriggerEvent( "EndRecord", ( v[2], numberOfRecordings ) )

                for k, v in IDs.iteritems() :
                    g = self.recordingIDs.get( k )

                    if v[0] and ( g is None or not g[0] ) :    # last query time not recording but now
                        numberOfRecordings += 1
                        if plugin.oldInterface :
                            self.TriggerEvent( "StartRecord" )
                        if plugin.newInterface :
                            self.TriggerEvent( "StartRecord", ( v[2], numberOfRecordings ) )

                self.TriggerEvent( "TimerListUpdated" )

                #print "numberOfRecordings = ", numberOfRecordings

                if numberOfRecordings == 0 and self.numberOfRecordings != 0 :

                    self.TriggerEvent( "AllActiveRecordingsFinished" )

                self.numberOfRecordings = numberOfRecordings

                self.recordingIDs = IDs
                self.pseudoIDs = pseudoIDs

        if type & UPDATE_STREAM != 0 and self.versionDVBViewerService != '1.5.0.2' :

            page = 'status'
            if self.versionDVBViewerService == '1.5.0.21' :
                page = 'clientcount'

            xmlData = self.GetData( page )

            #print xmlData

            # EXAMPLE of xmldata, Service version 1.5.0.21:

            #<?xml version="1.0" encoding="utf-8" ?>
            #<clientcount>0</clientcount>

            # EXAMPLE of xmldata, Service version >=1.5.0.25:

            #<?xml version="1.0" encoding="utf-8" ?>
            #<status>
            #   <recordcount>0</recordcount>
            #   <clientcount>0</clientcount>
            #   <epgudate>0</epgudate>
            #</status>

            if xmlData is None :
                xmlData = '<?xml version="1.0" encoding="utf-8" ?><clientcount>0</clientcount>'

            tree = ElementTree.fromstring( xmlData )

            element = tree
            if self.versionDVBViewerService != '1.5.0.21' :
                element = tree.find( 'clientcount' )

            numberOfClients = int( GetText( element, None, '0' ) ) - self.numberOfRecordings

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

        return True



    def GetNumberOfClients( self, update = True ) :
        if update or self.failing :
            self.Update( UPDATE_STREAM )

        return self.numberOfClients



    def GetNumberOfActiveRecordings( self, update = True ) :
        if update or self.failing :
            self.Update( UPDATE_RECORDINGS )

        return self.numberOfRecordings



    def IsRecording( self, update = True ) :
        return GetNumberOfActiveRecordings( update ) != 0



    def IsEPGUpdating( self, update = True ) :
        if update or self.failing :
            self.Update( UPDATE_STREAM )

        return self.updateEPG



    def GetRecordingDates( self, active = True, update = True ) :
        if update or self.failing :
            self.Update( UPDATE_RECORDINGS )

        if self.failing :
            return None

        if active :
            return self.activeRecordingDates
        else :
            return self.recordingDates



    def GetRecordingsIDs( self, update = True ) :
        if update or self.failing :
            self.Update( UPDATE_RECORDINGS )

        if self.failing :
            return None
        return self.recordingIDs



    def GetPseudoIDs( self, update = True ) :
        if update or self.failing :
            self.Update( UPDATE_RECORDINGS )

        if self.failing :
            return None
        return self.pseudoIDs



    def GetVersion( self ) :
        if self.versionDVBViewerService is None :
            self.Update( UPDATE_RECORDINGS )
        return self.versionDVBViewerService

