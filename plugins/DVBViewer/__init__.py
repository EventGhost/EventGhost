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


eg.RegisterPlugin(
    name = "DVBViewer",
    author = "Bitmonster & Nativityplay",
    version = "1.2." + "$LastChangedRevision$".split()[1],
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds support functions to control <a href="http://www.dvbviewer.com/">'
        'DVBViewer Pro/GE</a> and returns events.'
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
    

ACTIONS = (
    ("OSDMenu", "OSD-Menu", None, 111),
    ("OSDLeft", "OSD-Left", None, 2000),
    ("OSDRight", "OSD-Right", None, 2100),
    ("OSDUp", "OSD-Up", None, 78),
    ("OSDDown", "OSD-Down", None, 79),
    ("OSDOK", "OSD-OK", None, 73),
    ("OSDRed", "OSD-Red", None, 74),
    ("OSDGreen", "OSD-Green", None, 75),
    ("OSDYellow", "OSD-Yellow", None, 76),
    ("OSDBlue", "OSD-Blue", None, 77),
    ("OSDFirst", "OSD-First", None, 80),
    ("OSDLast", "OSD-Last", None, 81),
    ("OSDPrevious", "OSD-Previous", None, 82),
    ("OSDNext", "OSD-Next", None, 83),
    ("OSDClose", "OSD-Close", None, 84),
    ("OSDPositioning", "OSD-Positioning", None, 85),
    ("OSDClock", "OSD-Clock", None, 2010),
    ("OSDUndefined2", "OSD-Undefined2", None, 2110),
    ("OSDShowHTPC", "OSD-Show HTPC", None, 2110),
    ("OSDBackgroundToggle", "OSD-Background Toggle", None, 8194),
    ("OSDTeletext", "OSD-Teletext", None, 101),
    ("OSDShowTimer", "OSD-Show Timer", None, 8195),
    ("OSDShowRecordings", "OSD-Show Recordings", None, 8196),
    ("OSDShowNow", "OSD-Show Now", None, 8197),
    ("OSDShowEPG", "OSD-Show EPG", None, 8198),
    ("OSDShowChannels", "OSD-Show Channels", None, 8199),
    ("OSDShowFavourites", "OSD-Show Favourites", None, 8200),
    ("OSDShowTimeline", "OSD-Show Timeline", None, 8201),
    ("OSDShowPicture", "OSD-Show Picture", None, 8202),
    ("OSDShowMusic", "OSD-Show Music", None, 8203),
    ("OSDShowVideo", "OSD-Show Video", None, 8204),
    ("OSDShowNews", "OSD-Show News", None, 8205),
    ("OSDShowWeather", "OSD-Show Weather", None, 8206),
    ("OSDShowMiniepg", "OSD-Show Miniepg", None, 8207),
    ("OSDShowMusicPlaylist", "OSD-Show Music playlist", None, 8208),
    ("OSDShowVideoPlaylist", "OSD-Show Video playlist", None, 8209),
    ("OSDShowComputer", "OSD-Show Computer", None, 8210),
    ("OSDShowAlarms", "OSD-Show Alarms", None, 8212),
    ("Pause", "Pause", None, 0),
    ("OnTop", "On Top", None, 1),
    ("HideMenu", "Hide Menu", None, 2),
    ("ShowStatusbar", "Show Statusbar", None, 3),
    ("Toolbar", "Toolbar", None, 4),
    ("Fullscreen", "Fullscreen", None, 5),
    ("Exit", "Exit", None, 6),
    ("Channellist", "Channellist", None, 7),
    ("ChannelMinus", "Channel -", None, 8),
    ("ChannelPlus", "Channel +", None, 9),
    ("ChannelSave", "Channel Save", None, 10),
    ("Favourite1", "Favourite 1", None, 11),
    ("Favourite2", "Favourite 2", None, 12),
    ("Favourite3", "Favourite 3", None, 13),
    ("Favourite4", "Favourite 4", None, 14),
    ("Favourite5", "Favourite 5", None, 15),
    ("Favourite6", "Favourite 6", None, 16),
    ("Favourite7", "Favourite 7", None, 17),
    ("Favourite8", "Favourite 8", None, 18),
    ("Favourite9", "Favourite 9", None, 19),
    ("Favourite0", "Favourite 0", None, 38),
    ("FavouritePlus", "Favourite +", None, 20),
    ("FavouriteMinus", "Favourite -", None, 21),
    ("Aspect", "Aspect", None, 22),
    ("Zoom", "Zoom", None, 23),
    ("Options", "Options", None, 24),
    ("Mute", "Mute", None, 25),
    ("VolumeUp", "Volume Up", None, 26),
    ("VolumeDown", "Volume Down", None, 27),
    ("Display", "Display", None, 28),
    ("Zoom50", "Zoom 50%", None, 29),
    ("Zoom100", "Zoom 100%", None, 30),
    ("Zoom200", "Zoom 200%", None, 31),
    ("Desktop", "Desktop", None, 32),
    ("RecordSettings", "Record Settings", None, 33),
    ("Record", "Record", None, 34),
    ("Teletext", "Teletext", None, 35),
    ("EPG", "EPG", None, 37),
    ("Channel1", "Channel 1", None, 41),
    ("Channel2", "Channel 2", None, 42),
    ("Channel3", "Channel 3", None, 43),
    ("Channel4", "Channel 4", None, 44),
    ("Channel5", "Channel 5", None, 45),
    ("Channel6", "Channel 6", None, 46),
    ("Channel7", "Channel 7", None, 47),
    ("Channel8", "Channel 8", None, 48),
    ("Channel9", "Channel 9", None, 49),
    ("Channel0", "Channel 0", None, 40),
    ("TimeShift", "TimeShift", None, 50),
    ("TimeShiftWindow", "TimeShift Window", None, 51),
    ("TimeshiftStop", "Timeshift Stop", None, 52),
    ("RebuildGraph", "Rebuild Graph", None, 53),
    ("TitlebarHide", "Titlebar Hide", None, 54),
    ("BrightnessUp", "Brightness Up", None, 55),
    ("BrightnessDown", "Brightness Down", None, 56),
    ("SaturationUp", "Saturation Up", None, 57),
    ("SaturationDown", "Saturation Down", None, 58),
    ("ContrastUp", "Contrast Up", None, 59),
    ("ContrastDown", "Contrast Down", None, 60),
    ("HueUp", "Hue Up", None, 61),
    ("HueDown", "Hue Down", None, 62),
    ("LastChannel", "Last Channel", None, 63),
    ("Playlist", "Playlist", None, 64),
    ("PlaylistFirst", "Playlist First", None, 65),
    ("PlaylistNext", "Playlist Next", None, 66),
    ("PlaylistPrevious", "Playlist Previous", None, 67),
    ("PlaylistLast", "Playlist Last", None, 68),
    ("PlaylistStop", "Playlist Stop", None, 69),
    ("PlaylistRandom", "Playlist Random", None, 70),
    ("HideAll", "Hide All", None, 71),
    ("AudioChannel", "Audio Channel", None, 72),
    ("BestWidth", "Best Width", None, 89),
    ("Play", "Play", None, 92),
    ("OpenFile", "Open File", None, 94),
    ("StereoLeftRight", "Stereo/Left/Right", None, 95),
    ("JumpMinus10", "Jump Minus 10", None, 102),
    ("JumpPlus10", "Jump Plus 10", None, 103),
    ("ZoomUp", "Zoom Up", None, 104),
    ("ZoomDown", "Zoom Down", None, 105),
    ("StretchHUp", "StretchH Up", None, 106),
    ("StretchHDown", "StretchH Down", None, 107),
    ("StretchVUp", "StretchV Up", None, 108),
    ("StretchVDown", "StretchV Down", None, 109),
    ("StretchReset", "Stretch Reset", None, 110),
    ("Previous", "Previous", None, 112),
    ("Next", "Next", None, 113),
    ("Stop", "Stop", None, 114),
    ("ShowVideowindow", "Show Videowindow", None, 821),
    ("ToggleMosaicpreview", "Toggle Mosaicpreview", None, 8211),
    ("ShowHelp", "Show Help", None, 8213),
    ("HideVideowindow", "Hide Videowindow", None, 8214),
    ("Reboot", "Reboot", None, 12295),
    ("Shutdown", "Shutdown", None, 12296),
    ("ToggleBackground", "Toggle Background", None, 12297),
    ("EjectCD", "Eject CD", None, 12299),
    ("Forward", "Forward", None, 12304),
    ("Rewind", "Rewind", None, 12305),
    ("AddBookmark", "Add Bookmark", None, 12306),
    ("Hibernate", "Hibernate", None, 12323),
    ("Standby", "Standby", None, 12324),
    ("Slumbermode", "Slumbermode", None, 12325),
    ("CloseDVBViewer", "Close DVBViewer", None, 12326),
    ("SpeedUp", "Speed Up", None, 12382),
    ("SpeedDown", "Speed Down", None, 12383),
    ("ShowPlaylist", "Show Playlist", None, 12384),
    ("ShowVersion", "Show Version", None, 16384),
    ("DisableAudio", "Disable Audio", None, 16385),
    ("DisableAudioVideo", "Disable AudioVideo", None, 16386),
    ("DisableVideo", "Disable Video", None, 16387),
    ("EnableAudioVideo", "Enable AudioVideo", None, 16388),
    ("ZoomlevelStandard", "Zoomlevel Standard", None, 16389),
    ("Zoomlevel0", "Zoomlevel 0", None, 16390),
    ("Zoomlevel1", "Zoomlevel 1", None, 16391),
    ("Zoomlevel2", "Zoomlevel 2", None, 16392),
    ("Zoomlevel3", "Zoomlevel 3", None, 16393),
    ("ZoomlevelToggle", "Zoomlevel Toggle", None, 16394),
    ("TogglePreview", "Toggle Preview", None, 16395),
    ("RestoreDefaultColors", "Restore Default Colors", None, 16396),
    ("DVDMenu", "DVD Menu", None, 8246),
    ("ShutdownCard", "Shutdown Card", None, 12327),
    ("ShutdownMonitor", "Shutdown Monitor", None, 12328),
    ("StopGraph", "Stop Graph", None, 16383),
    ("Exit", "Exit", None, 12294),
)

        
from functools import partial
from win32com.client import Dispatch, DispatchWithEvents
from win32com.client.gencache import EnsureDispatch
from eg.WinApi import SendMessageTimeout


class Text:
    interfaceBox = "Interface API"
    useComApi = "COM-API (for DVBViewer Pro)"
    useSendMessage = "SendMessage-API (for DVBViewer GE)"


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
    def Setup(self, plugin):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin
        self.dvbviewer = EnsureDispatch("DVBViewerServer.DVBViewer")
        # try if we can get an attribute from the COM instance
        self.dvbviewer.CurrentChannelNr
        comEvents = self.dvbviewer.Events
        self.comObj = DispatchWithEvents(comEvents, self.plugin.EventHandler)
            
            
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        del self.dvbviewer
        self.plugin.workerThread = None


gWindowMatcher = eg.WindowMatcher(
    'DVBViewer.exe', None, 'TfrmMain', None, None, 1, True, 0.0, 0
)


class DVBViewer(eg.PluginClass):
    text = Text
    
    def __init__(self):
        self.AddAction(Start)
        
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
            
            
    def __start__(self, useSendMessage=False):
        if useSendMessage:
            self.SendCommand = self.SendCommandThroughSendMessage
        else:
            self.SendCommand = self.SendCommandThroughCOM
        
            
    def __stop__(self):
        if self.workerThread:
            self.workerThread.Stop()
        
        
    def SendCommandThroughSendMessage(self, value):
        try:
            hwnd = gWindowMatcher()[0]
            return SendMessageTimeout(hwnd, 45762, 2069, 100 + value)
        except:
            raise self.Exceptions.ProgramNotRunning
        
        
    def SendCommandThroughCOM(self, value):
        if not self.workerThread:
            self.workerThread = DvbViewerWorkerThread(self)
            self.workerThread.Start(20.0)
        self.workerThread.CallWait(
            partial(self.workerThread.dvbviewer.SendCommand, value)
        )
           
            
    def Configure(self, useSendMessage=False):
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
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection() == 1)
        
        
    
class Start(eg.ActionClass):
    name = "Start DVBViewer"
    description = "Start DVBViewer through COM-API. For DVBViewer Pro only."
   
    def __call__(self):
        if self.plugin.workerThread:
            return
            #self.plugin.workerThread.Stop(timeout=5.0)
        self.plugin.workerThread = DvbViewerWorkerThread(self.plugin)
        self.plugin.workerThread.Start(20.0)
            

        