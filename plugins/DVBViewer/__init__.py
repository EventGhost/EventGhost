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
    name = "DVBViewer",
    author = "Bitmonster & Nativityplay",
    version = "1.2." + "$LastChangedRevision$".split()[1],
    kind = "program",
    description = (
        'Adds support functions to control DVBViewer Pro/GE and returns events.'
        '\n\n<p><a href="http://www.dvbviewer.com/">DVBViewer Homepage</a>'
    ),
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
    

CMDS = (
    ("OSDMenu", "OSD-Menu", 111),
    ("OSDLeft", "OSD-Left", 2000),
    ("OSDRight", "OSD-Right", 2100),
    ("OSDUp", "OSD-Up", 78),
    ("OSDDown", "OSD-Down", 79),
    ("OSDOK", "OSD-OK", 73),
    ("OSDRed", "OSD-Red", 74),
    ("OSDGreen", "OSD-Green", 75),
    ("OSDYellow", "OSD-Yellow", 76),
    ("OSDBlue", "OSD-Blue", 77),
    ("OSDFirst", "OSD-First", 80),
    ("OSDLast", "OSD-Last", 81),
    ("OSDPrevious", "OSD-Previous", 82),
    ("OSDNext", "OSD-Next", 83),
    ("OSDClose", "OSD-Close", 84),
    ("OSDPositioning", "OSD-Positioning", 85),
    ("OSDClock", "OSD-Clock", 2010),
    ("OSDUndefined2", "OSD-Undefined2", 2110),
    ("OSDShowHTPC", "OSD-Show HTPC", 2110),
    ("OSDBackgroundToggle", "OSD-Background Toggle", 8194),
    ("OSDTeletext", "OSD-Teletext", 101),
    ("OSDShowTimer", "OSD-Show Timer", 8195),
    ("OSDShowRecordings", "OSD-Show Recordings", 8196),
    ("OSDShowNow", "OSD-Show Now", 8197),
    ("OSDShowEPG", "OSD-Show EPG", 8198),
    ("OSDShowChannels", "OSD-Show Channels", 8199),
    ("OSDShowFavourites", "OSD-Show Favourites", 8200),
    ("OSDShowTimeline", "OSD-Show Timeline", 8201),
    ("OSDShowPicture", "OSD-Show Picture", 8202),
    ("OSDShowMusic", "OSD-Show Music", 8203),
    ("OSDShowVideo", "OSD-Show Video", 8204),
    ("OSDShowNews", "OSD-Show News", 8205),
    ("OSDShowWeather", "OSD-Show Weather", 8206),
    ("OSDShowMiniepg", "OSD-Show Miniepg", 8207),
    ("OSDShowMusicPlaylist", "OSD-Show Music playlist", 8208),
    ("OSDShowVideoPlaylist", "OSD-Show Video playlist", 8209),
    ("OSDShowComputer", "OSD-Show Computer", 8210),
    ("OSDShowAlarms", "OSD-Show Alarms", 8212),
    ("Pause", "Pause", 0),
    ("OnTop", "On Top", 1),
    ("HideMenu", "Hide Menu", 2),
    ("ShowStatusbar", "Show Statusbar", 3),
    ("Toolbar", "Toolbar", 4),
    ("Fullscreen", "Fullscreen", 5),
    ("Exit", "Exit", 6),
    ("Channellist", "Channellist", 7),
    ("ChannelMinus", "Channel -", 8),
    ("ChannelPlus", "Channel +", 9),
    ("ChannelSave", "Channel Save", 10),
    ("Favourite1", "Favourite 1", 11),
    ("Favourite2", "Favourite 2", 12),
    ("Favourite3", "Favourite 3", 13),
    ("Favourite4", "Favourite 4", 14),
    ("Favourite5", "Favourite 5", 15),
    ("Favourite6", "Favourite 6", 16),
    ("Favourite7", "Favourite 7", 17),
    ("Favourite8", "Favourite 8", 18),
    ("Favourite9", "Favourite 9", 19),
    ("Favourite0", "Favourite 0", 38),
    ("FavouritePlus", "Favourite +", 20),
    ("FavouriteMinus", "Favourite -", 21),
    ("Aspect", "Aspect", 22),
    ("Zoom", "Zoom", 23),
    ("Options", "Options", 24),
    ("Mute", "Mute", 25),
    ("VolumeUp", "Volume Up", 26),
    ("VolumeDown", "Volume Down", 27),
    ("Display", "Display", 28),
    ("Zoom50", "Zoom 50%", 29),
    ("Zoom100", "Zoom 100%", 30),
    ("Zoom200", "Zoom 200%", 31),
    ("Desktop", "Desktop", 32),
    ("RecordSettings", "Record Settings", 33),
    ("Record", "Record", 34),
    ("Teletext", "Teletext", 35),
    ("EPG", "EPG", 37),
    ("Channel1", "Channel 1", 41),
    ("Channel2", "Channel 2", 42),
    ("Channel3", "Channel 3", 43),
    ("Channel4", "Channel 4", 44),
    ("Channel5", "Channel 5", 45),
    ("Channel6", "Channel 6", 46),
    ("Channel7", "Channel 7", 47),
    ("Channel8", "Channel 8", 48),
    ("Channel9", "Channel 9", 49),
    ("Channel0", "Channel 0", 40),
    ("TimeShift", "TimeShift", 50),
    ("TimeShiftWindow", "TimeShift Window", 51),
    ("TimeshiftStop", "Timeshift Stop", 52),
    ("RebuildGraph", "Rebuild Graph", 53),
    ("TitlebarHide", "Titlebar Hide", 54),
    ("BrightnessUp", "Brightness Up", 55),
    ("BrightnessDown", "Brightness Down", 56),
    ("SaturationUp", "Saturation Up", 57),
    ("SaturationDown", "Saturation Down", 58),
    ("ContrastUp", "Contrast Up", 59),
    ("ContrastDown", "Contrast Down", 60),
    ("HueUp", "Hue Up", 61),
    ("HueDown", "Hue Down", 62),
    ("LastChannel", "Last Channel", 63),
    ("Playlist", "Playlist", 64),
    ("PlaylistFirst", "Playlist First", 65),
    ("PlaylistNext", "Playlist Next", 66),
    ("PlaylistPrevious", "Playlist Previous", 67),
    ("PlaylistLast", "Playlist Last", 68),
    ("PlaylistStop", "Playlist Stop", 69),
    ("PlaylistRandom", "Playlist Random", 70),
    ("HideAll", "Hide All", 71),
    ("AudioChannel", "Audio Channel", 72),
    ("BestWidth", "Best Width", 89),
    ("Play", "Play", 92),
    ("OpenFile", "Open File", 94),
    ("StereoLeftRight", "Stereo/Left/Right", 95),
    ("JumpMinus10", "Jump Minus 10", 102),
    ("JumpPlus10", "Jump Plus 10", 103),
    ("ZoomUp", "Zoom Up", 104),
    ("ZoomDown", "Zoom Down", 105),
    ("StretchHUp", "StretchH Up", 106),
    ("StretchHDown", "StretchH Down", 107),
    ("StretchVUp", "StretchV Up", 108),
    ("StretchVDown", "StretchV Down", 109),
    ("StretchReset", "Stretch Reset", 110),
    ("Previous", "Previous", 112),
    ("Next", "Next", 113),
    ("Stop", "Stop", 114),
    ("ShowVideowindow", "Show Videowindow", 821),
    ("ToggleMosaicpreview", "Toggle Mosaicpreview", 8211),
    ("ShowHelp", "Show Help", 8213),
    ("HideVideowindow", "Hide Videowindow", 8214),
    ("Reboot", "Reboot", 12295),
    ("Shutdown", "Shutdown", 12296),
    ("ToggleBackground", "Toggle Background", 12297),
    ("EjectCD", "Eject CD", 12299),
    ("Forward", "Forward", 12304),
    ("Rewind", "Rewind", 12305),
    ("AddBookmark", "Add Bookmark", 12306),
    ("Hibernate", "Hibernate", 12323),
    ("Standby", "Standby", 12324),
    ("Slumbermode", "Slumbermode", 12325),
    ("CloseDVBViewer", "Close DVBViewer", 12326),
    ("SpeedUp", "Speed Up", 12382),
    ("SpeedDown", "Speed Down", 12383),
    ("ShowPlaylist", "Show Playlist", 12384),
    ("ShowVersion", "Show Version", 16384),
    ("DisableAudio", "Disable Audio", 16385),
    ("DisableAudioVideo", "Disable AudioVideo", 16386),
    ("DisableVideo", "Disable Video", 16387),
    ("EnableAudioVideo", "Enable AudioVideo", 16388),
    ("ZoomlevelStandard", "Zoomlevel Standard", 16389),
    ("Zoomlevel0", "Zoomlevel 0", 16390),
    ("Zoomlevel1", "Zoomlevel 1", 16391),
    ("Zoomlevel2", "Zoomlevel 2", 16392),
    ("Zoomlevel3", "Zoomlevel 3", 16393),
    ("ZoomlevelToggle", "Zoomlevel Toggle", 16394),
    ("TogglePreview", "Toggle Preview", 16395),
    ("RestoreDefaultColors", "Restore Default Colors", 16396),
    ("DVDMenu", "DVD Menu", 8246),
    ("ShutdownCard", "Shutdown Card", 12327),
    ("ShutdownMonitor", "Shutdown Monitor", 12328),
    ("StopGraph", "Stop Graph", 16383),
    ("Exit", "Exit", 12294),
)

        
import wx
from win32com.client import Dispatch, DispatchWithEvents
from win32gui import SendMessageTimeout
from win32con import SMTO_BLOCK, SMTO_ABORTIFHUNG


class Text:
    interfaceBox = "Interface API"
    useComApi = "COM-API (for DVBViewer Pro)"
    useSendMessage = "SendMessage-API (for DVBViewer GE)"
    errorNoWindow = "Couldn't find DVBViewer window"


class EventHandler:

    def OnonEndRecord(self):
        self.TriggerEvent("EndRecord")               
       
    def OnonOSDWindow(self, WindowID):
        self.TriggerEvent("Window:" + str(WindowID))

    def OnonSelectedItemChange(self):
        self.TriggerEvent("SelectedItemChange")

    def OnChannelChange(self, ChannelNr):
        self.TriggerEvent("Channel", ChannelNr)

    def OnonRDS(self, RDS):
        self.TriggerEvent("RDS:" + str(RDS))

    def OnonPlaylist(self, Filename):
        self.TriggerEvent("Playlist", str(Filename))

    def OnonControlChange(self, WindowID, ControlID):
        self.TriggerEvent("ControlChange:WindID" + str(WindowID) + "ContrID"+ str(ControlID))

    def OnonAction(self, ActionID):
        self.TriggerEvent("Action:" + str(ActionID))

    def OnPlaybackEnd(self):
        self.TriggerEvent("PlaybackEnd")

    def OnonStartRecord(self, ID):
        self.TriggerEvent("StartRecord", str(ID))
       
    def OnonAddRecord(self, ID):
        self.TriggerEvent("AddRecord:" + str(ID))

    def OnPlaystatechange(self, RendererType, State):
        self.TriggerEvent("Playstatechange:RenderTy" + str(RendererType) + "State"+ str(State))

    def OnonPlaybackstart(self):
        self.TriggerEvent("Playbackstart")
        
    def OnonDVBVClose(self):
        if self.plugin.workerThread:
            self.plugin.workerThread.Stop()
        self.TriggerEvent("Close")

    
    
    
class DvbViewerWorkerThread(eg.ThreadWorker):
    """
    Handles the COM interface in a thread of its own.
    """
    def __init__(self, plugin):
        self.plugin = plugin
        eg.ThreadWorker.__init__(self)
    
    
    def Setup(self):
        """
        This will be called inside the thread at the beginning.
        """
        self.dvbviewer = Dispatch("DVBViewerServer.DVBViewer")
        comEvents = self.dvbviewer.Events
        self.comObj = DispatchWithEvents(comEvents, self.plugin.EventHandler)
            
            
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        del self.dvbviewer
        self.plugin.workerThread = None

    
    
class DVBViewer(eg.PluginClass):
    text = Text
    
    def __init__(self):
        self.AddAction(Start)
        for tmpName, tmpDescription, tmpValue in CMDS:
            class tmpAction(eg.ActionClass):
                name = tmpDescription
                value = tmpValue
                def __call__(self2):
                    self.SendCommand(self2.value)
            tmpAction.__name__ = tmpName
            self.AddAction(tmpAction)
            
        # create a new subclass of the EventHandler with the ability to use 
        # the plugin's TriggerEvent method
        class SubEventHandler(EventHandler):
            plugin = self
            TriggerEvent = self.TriggerEvent
        self.EventHandler = SubEventHandler
        self.workerThread = None
            
            
    def __start__(self, useSendMessage=False):
        if useSendMessage:
            self.SearchWindowProc = eg.plugins.Window.FindWindow.Compile(
                'DVBViewer.exe', None, 'TfrmMain', None, None, 1, True, 0.0, 0)
            self.SendCommand = self.SendCommandThroughSendMessage
        else:
            self.SendCommand = self.SendCommandThroughCOM
        
            
    def __stop__(self):
        if self.workerThread:
            self.workerThread.Stop()
        
        
    def SendCommandThroughSendMessage(self, value):
        hwnds = self.SearchWindowProc()
        if len(hwnds) == 0:
            self.PrintError(self.text.errorNoWindow)
            return
        _, result = SendMessageTimeout(
            hwnds[0],
            45762, 
            2069, 
            100 + value, 
            SMTO_BLOCK|SMTO_ABORTIFHUNG,
            2000 # wait at most 2 seconds
        )

        
    def SendCommandThroughCOM(self, value):
        if not self.workerThread:
            self.workerThread = DvbViewerWorkerThread(self)
            self.workerThread.Start(20.0)
        self.workerThread.CallWait(
            self.workerThread.dvbviewer.SendCommand, 
            value
        )
           
            
    def Configure(self, useSendMessage=False):
        text = self.text
        dialog = eg.ConfigurationDialog(self)
        radioBox = wx.RadioBox(
            dialog, 
            -1, 
            text.interfaceBox, 
            choices=[text.useComApi, text.useSendMessage], 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(int(useSendMessage))
        dialog.sizer.Add(radioBox, 0, wx.EXPAND)
        if dialog.AffirmedShowModal():
            return (radioBox.GetSelection() == 1, )
        
        
    
class Start(eg.ActionClass):
    name = "Start DVBViewer"
    description = "Start DVBViewer through COM-API. For DVBViewer Pro only."
   
    def __call__(self):
        if self.plugin.workerThread:
            return
            self.plugin.workerThread.Stop(timeout=5.0)
        self.plugin.workerThread = DvbViewerWorkerThread(self.plugin)
        self.plugin.workerThread.Start(20.0)
            

        