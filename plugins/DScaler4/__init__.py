# -*- coding: utf-8 -*-
#
# Plugins/DScaler/__init__.py
# DScaler Plugin for EventGhost.
# Version 1.0a
# Written by Lee Woolf
# All the GPL info below applies to this plug-in too please leave this
# info intact when making modification
#
# Written in Python a language solely dependent on a character
# you cant see in a basic text editor :)
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

eg.RegisterPlugin(
    name = "DScaler 4",
    author = "Lee Woolf",
    version = "1.1.1093",
    kind = "program",
    guid = "{8F55042E-ABBC-40DE-8ACF-A1017C99F333}",
    description = (
        'Adds support functions for '
        '<a href="http://deinterlace.sourceforge.net/">'
        'DScaler 4</a>.'
    ),
    url="http://www.eventghost.org/forum/viewtopic.php?t=807",
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAlUlEQVR4nO2TUQoDMQhE"
        "nbL3ikfzaJOTTT+KIdnI7pb+VhCCmueQKCQZANkDk4Rz7JiSt4BsNINeTzrPTUguio9z"
        "Ue/d3H2JkRzn1tpONTORFEnpE5AkS8+8pK2mVFBIBwClkrnmqzeo7A8oAPOfpwFQRFwD"
        "8mIOEQClR8SIkzR3H+O8zEFCqm6Vsg1wZwmelwm/rvMbuW11hNUu88kAAAAASUVORK5C"
        "YII="
    ),
)

# Change Log:
# 1.1 by bitmonster
#     - made code compatible with EventGhost 0.3.6
#     - stuffed some actions into groups
# 1.0 by Lee Woolf
#     - initial version



# ######### Channel Stuff ##############################
IDM_CHANNELPLUS =           266     # Channel Up/Page Up
IDM_CHANNELMINUS =          267     # Channel Down/Page Down
IDM_CHANNEL_PREVIOUS =      813     # Channel Recall
IDM_CHANNEL_LIST =          242     # Calls up the channel list window
IDM_CHANNEL_PREVIEW =       32958   # Channel Preview
IDM_PREVIEW_PAGE_PREV =     32965   # Preview previous page
IDM_PREVIEW_PAGE_NEXT =     32964   # Preview  next page


# ######### Audio Stuff ##############################
IDM_VOLUMEPLUS =            374     # Its a gimee
IDM_VOLUMEMINUS =           375     #
IDM_MUTE =                  402     # Mute
IDM_AUDIOSETTINGS =         264     # Audio Adj Window
IDM_AUDIO_MIXER =           400     # Mixer Window
IDM_AUDIO_0 =               1110    # Tuner for my card
IDM_AUDIO_1 =               1111    # Radio
IDM_AUDIO_2 =               1112    # External
IDM_AUDIO_3 =               1113    # Internal
IDM_AUDIO_4 =               1114    # Disabled
IDM_AUDIO_5 =               1115    # Strereo

# ######### Guide Stuff  ############################
IDM_DISPLAY_EPG =           32981   # EPG Info Same as G key
IDM_HIDE_EPG =              32990   # Hide Guide
IDM_DISPLAY_EPG_NOW =       32982   # Show EPG Now
IDM_DISPLAY_EPG_NEXT =      32985   # Next page
IDM_DISPLAY_EPG_NEXT_IN_PAGE = 32987 # Next item in page
IDM_DISPLAY_EPG_LATER =     32984   # Later time
IDM_DISPLAY_EPG_EARLIER =   32983   # Earlier time

# #### On Screen Stuff  ########################
IDM_HIDE_OSD =              592     # Hide On Screen Display
IDM_SHOW_OSD =              593     # Sho On Screen Display

# ######### Video Stuff ##############################
IDM_OVERLAY_STOP =          590     # Overlay Stop on Actions Menu
IDM_OVERLAY_START =         591     # Overlay Start on Action Menu
IDM_TAKESTILL =             485     # Screen Shot same as L key
IDM_TAKESTREAMSNAP =        1899    # Take Stream Snapshot
IDM_TAKECYCLICSTILL =       32790   # Take Peridoic Still
IDM_TAKECONSECUTIVESTILL =  32840   # Take Consecutive Stills
IDM_CAPTURE_PAUSE =         232     # Video Pause same as P key

IDM_ASPECT_LETTERBOX =      702     # Aspect 16:9 Letterboxed
IDM_ASPECT_FULLSCREEN =     701     # Aspect 4:3 Fullscreen
IDM_ASPECT_ANAMORPHIC =     703     # Aspect 16:9 Anamorphic

IDM_COLOR_PLUS =            615     # More Saturation
IDM_COLOR_MINUS	=           616     # Less Saturation
IDM_COLOR_CURRENT =         617     # Show Current Saturation
IDM_BRIGHTNESS_PLUS =       600     # Brightness up
IDM_BRIGHTNESS_MINUS =      601     # Brightness down
IDM_BRIGHTNESS_CURRENT =    602     # Current Brightness

IDM_SOURCE_INPUT1 =         1089    # Tuner for my card,   Ctrl+Alt+F1
IDM_SOURCE_INPUT2 =         1090    # Composite   Ctrl+Alt+F2
IDM_SOURCE_INPUT3 =         1091    # S-Video  Ctrl+Alt+F3
IDM_SOURCE_INPUT4 =         1092    # Composite over S-Video  Ctrl+Alt+F4
IDM_SOURCE_INPUT5 =         1093    # Input 5  Ctrl+Alt+F5
IDM_SOURCE_INPUT6 =         1094    # Input 6  Ctrl+Alt+F6
IDM_SOURCE_INPUT7 =         1095    # Input 7  Ctrl+Alt+F7
IDM_SOURCE_FIRST =          2086    # First video source
IDM_SOURCE_INITIAL =        32772   # Initial video source

IDM_SOURCE_INPUT8 =         1096    # Not setup. See notes
IDM_SOURCE_INPUT9 =         1097    # at the end of this file
IDM_SOURCE_INPUT10 =        1098    #
IDM_SOURCE_INPUT11 =        1099    #
IDM_SOURCE_INPUT12 =        1100    #
IDM_SOURCE_INPUT13 =        1101    #

IDM_SETTINGS_PIXELWIDTH_768 =   760 # Self-explanatory
IDM_SETTINGS_PIXELWIDTH_754 =   2012#
IDM_SETTINGS_PIXELWIDTH_720 =   761 #
IDM_SETTINGS_PIXELWIDTH_640 =   762 #
IDM_SETTINGS_PIXELWIDTH_480 =   2243#
IDM_SETTINGS_PIXELWIDTH_384 =   764 #
IDM_SETTINGS_PIXELWIDTH_320 =   763 #
IDM_ZOOM_PLUS =                 2008#
IDM_ZOOM_MINUS =                2007#
IDM_ON_TOP =                    309 # Bring Window to Front


# # For recording I don't use them as Dscaler is not stable for
#recording yet on my system
# Other then the three labeled below you will need to test
#them to be sure what they control.

IDM_TSRECORD =              2031    # Start Recording
IDM_TSSTOP =                2032    # Stop Recording
IDM_TSRWND =                2036
IDM_TSFFWD =                2035
IDM_TSPLAY =                2033
IDM_TSPREV =                2037
IDM_TSNEXT =                2038
IDM_TSPAUSE =               2034
IDM_TSOPTIONS =             2030    # Brings up the Time-shift options window
# ###########################################

# ##### Closed Caption Stuff  #######
IDM_CCOFF =                 795
IDM_CC1 =                   796
IDM_CC2=                    797
IDM_CC3 =                   798
IDM_CC4 =                   799


from win32gui import FindWindow, SendMessageTimeout, GetWindowText
from win32con import WM_COMMAND, WM_USER, SMTO_BLOCK, SMTO_ABORTIFHUNG


def SendCommand(mesg, wParam, lParam=0):
    """
    Find DScaler's message window
    """
    try:
        hDScaler = FindWindow('DScaler', None)
        _, result = SendMessageTimeout(hDScaler, mesg, wParam, lParam,
                                       SMTO_BLOCK|SMTO_ABORTIFHUNG, 2000)
        return result
    except:
        raise self.Exception.ProgramNotRunning



class Dscaler(eg.PluginClass):

    def __init__(self):
        self.AddAction(ChannelPlus)
        self.AddAction(ChannelMinus)
        self.AddAction(ChannelPrevious)
        self.AddAction(ChannelList)
        self.AddAction(ChannelPreview)
        self.AddAction(Preview_page_prev)
        self.AddAction(Preview_page_next)

        self.AddAction(VolUp)
        self.AddAction(VolDown)
        self.AddAction(Mute)
        self.AddAction(AudioSettings)
        self.AddAction(AudioMixer)

        self.AddAction(EpgDisplay)
        self.AddAction(HideEPG)
        self.AddAction(ShowCurrentEPG)
        self.AddAction(NextEPG)
        self.AddAction(NextItem_in_Page)
        self.AddAction(EPG_Later_Time)
        self.AddAction(EPG_Earlier_Time)

        self.AddAction(HideOSD)
        self.AddAction(ShowOSD)

        self.AddAction(OverLayStop)
        self.AddAction(OverLayStart)
        self.AddAction(StillShot)
        self.AddAction(StreamShot)
        self.AddAction(CyclicStill)
        self.AddAction(ConsecutiveStills)
        self.AddAction(CapturePause)
        self.AddAction(AspectLetterboxed)
        self.AddAction(AspectFullscreen)
        self.AddAction(AspectAnamorphic)
        self.AddAction(SaturationUp)
        self.AddAction(SaturationDown)
        self.AddAction(CurrentSaturation)
        self.AddAction(BrightnessUp)
        self.AddAction(BrightnessDown)
        self.AddAction(CurrentBrightness)
        self.AddAction(ZoomIn)
        self.AddAction(ZoomOut)
        self.AddAction(WindowOnTop)

        self.AddAction(TS_Record)
        self.AddAction(TS_StopRecording)
        self.AddAction(TS_Rewind)
        self.AddAction(TS_FastForward)
        self.AddAction(TS_Play)
        self.AddAction(TS_Previous)
        self.AddAction(TS_Next)
        self.AddAction(TS_Pause)
        self.AddAction(TS_Options)

        group = self.AddGroup("Video Input Sources")
        group.AddAction(SourceIn1)
        group.AddAction(SourceIn2)
        group.AddAction(SourceIn3)
        group.AddAction(SourceIn4)
        group.AddAction(SourceIn5)
        group.AddAction(SourceIn6)
        group.AddAction(SourceIn7)
        group.AddAction(FirstSource)
        group.AddAction(InitialSource)

        group = self.AddGroup("Audio Input Sources")
        group.AddAction(AudioSource0)
        group.AddAction(AudioSource1)
        group.AddAction(AudioSource2)
        group.AddAction(AudioSource3)
        group.AddAction(AudioSource4)
        group.AddAction(AudioSource5)

        group = self.AddGroup("Vertical Pixel Width")
        group.AddAction(PixelWidth_768)
        group.AddAction(PixelWidth_754)
        group.AddAction(PixelWidth_720)
        group.AddAction(PixelWidth_640)
        group.AddAction(PixelWidth_480)
        group.AddAction(PixelWidth_384)
        group.AddAction(PixelWidth_320)

        group = self.AddGroup("Closed Caption")
        group.AddAction(CC_Off)
        group.AddAction(CC1)
        group.AddAction(CC2)
        group.AddAction(CC3)
        group.AddAction(CC4)


# #########  Channel Stuff  ######################
class ChannelPlus(eg.ActionClass):
    name = "Channel Up"
    description = "Channel Up"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CHANNELPLUS)

class ChannelMinus(eg.ActionClass):
    name = "Channel Down"
    description = "Channel Down"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CHANNELMINUS)

class ChannelPrevious(eg.ActionClass):
    name = "Channel Recall"
    description = "Channel Recall"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CHANNEL_PREVIOUS)

class ChannelList(eg.ActionClass):
    name = "Channel Window"
    description = "Brings up the Channel Window"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CHANNEL_LIST)

class ChannelPreview(eg.ActionClass):
    name = "Channel Preview"
    description = "Channel Preview"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CHANNEL_PREVIEW)

class Preview_page_prev(eg.ActionClass):
    name = "Preview Previous Page"
    description = "Preview previous Page"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_PREVIEW_PAGE_PREV)

class Preview_page_next(eg.ActionClass):
    name = "Preview next page "
    description = "Preview next page "
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_PREVIEW_PAGE_NEXT)


# #########  Audio Stuff  ########################
class VolUp(eg.ActionClass):
    name = "Volume Up"
    description = "Volume Up"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_VOLUMEPLUS)

class VolDown(eg.ActionClass):
    name = "Volume Down"
    description = "Volume Down"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_VOLUMEMINUS)

class Mute(eg.ActionClass):
    name = "Mute"
    description = "Mute"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_MUTE)

class AudioSettings(eg.ActionClass):
    name = "Audio Settings"
    description = "Audio Adj Window"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_AUDIOSETTINGS)

class AudioMixer(eg.ActionClass):
    name = "Audio Mixer"
    description = "Mixer Window"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_AUDIO_MIXER)

class AudioSource0(eg.ActionClass):
    name = "Audio Source 1"
    description = "Tuner audio input for most cards or keys Ctrl+Shift+F1"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_AUDIO_0)

class AudioSource1(eg.ActionClass):
    name = "Audio Source 2"
    description = "Audio input 2, radio or keys Ctrl+Shift+F2"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_AUDIO_1)

class AudioSource2(eg.ActionClass):
    name = "Audio Source 3"
    description = "Audio input 3, external or keys Ctrl+Shift+F3"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_AUDIO_2)

class AudioSource3(eg.ActionClass):
    name = "Audio Source 4"
    description = "Audio input 4, internal or keys Ctrl+Shift+F4"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_AUDIO_3)

class AudioSource4(eg.ActionClass):
    name = "Audio Source 5"
    description = "Audio input 5, Disable or keys Ctrl+Shift+F5"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_AUDIO_4)

class AudioSource5(eg.ActionClass):
    name = "Audio Source 6"
    description = "Audio input 6, Stereo or keys Ctrl+Shift+F6"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_AUDIO_5)


# ######### Guide Stuff  ############################

class EpgDisplay(eg.ActionClass):
    name = "EPG Display"
    description = "EPG Info Same as the G key"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_DISPLAY_EPG)

class HideEPG(eg.ActionClass):
    name = "Hide EPG"
    description = "Hide the Program Guide "
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_HIDE_EPG)

class ShowCurrentEPG(eg.ActionClass):
    name = "EPG Now"
    description = "Show the current EPG"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_DISPLAY_EPG_NOW)

class NextEPG(eg.ActionClass):
    name = "Next page "
    description = "Next guide page"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_DISPLAY_EPG_NEXT)

class NextItem_in_Page (eg.ActionClass):
    name = "Next item"
    description = "Next item in EPG page"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_DISPLAY_EPG_NEXT_IN_PAGE)

class EPG_Later_Time(eg.ActionClass):
    name = "Later EPG Time"
    description = "Advance the Program Guide to a later time"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_DISPLAY_EPG_LATER)

class EPG_Earlier_Time(eg.ActionClass):
    name = "Earlier EPG Time"
    description = "Move the Program Guide to a earlier time"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_DISPLAY_EPG_EARLIER)


# ######### OSD Stuff  ############################

class HideOSD(eg.ActionClass):
    name = "Hide OSD"
    description = "Hide the On Screen Display"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_HIDE_OSD)

class ShowOSD(eg.ActionClass):
    name = "Show OSD"
    description = "Show the On Screen Display"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SHOW_OSD)


# ######### Video Stuff  ############################

class OverLayStop(eg.ActionClass):
    name = "Overlay Stop"
    description = "Stop overlay video. Same as Stop Video on the Actions Menu"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_OVERLAY_STOP)

class OverLayStart(eg.ActionClass):
    name = "Overlay Start"
    description = "Start overlay video Same as StartVideo on the Actions Menu"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_OVERLAY_START)

class StillShot(eg.ActionClass):
    name = "Screen Shot"
    description = "Take Screen Shot, same as the L key"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TAKESTILL)

class StreamShot(eg.ActionClass):
    name = "Stream Snapshot"
    description = "Take a Stream Snapshot, same as Shift+L"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TAKESTREAMSNAP)

class CyclicStill(eg.ActionClass):
    name = "Periodic Stills"
    description = "Take Periodic Still Pictures. Same as Ctrl+L"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TAKECYCLICSTILL)

class ConsecutiveStills(eg.ActionClass):
    name = "Consecutive Stills"
    description = "Take Consecutive Stills Pictures. Same as Alt+L"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TAKECONSECUTIVESTILL)

class CapturePause(eg.ActionClass):
    name = "Capture Pause"
    description = "Video Pause same as P key"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CAPTURE_PAUSE)

class AspectLetterboxed(eg.ActionClass):
    name = "Aspect Letterbox"
    description = "Change the aspect to 16:9 letterboxed"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_ASPECT_LETTERBOX)

class AspectFullscreen (eg.ActionClass):
    name = "Aspect Fullscreen"
    description = "Change the aspect to 4:3 full screen"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_ASPECT_FULLSCREEN)

class AspectAnamorphic (eg.ActionClass):
    name = "Aspect Anamorphic"
    description = "Change the aspect to 16:9 Anamorphic"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_ASPECT_ANAMORPHIC)

class SaturationUp(eg.ActionClass):
    name = "Saturation Up"
    description = "Change the saturation, more color"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_COLOR_PLUS)
class SaturationDown(eg.ActionClass):
    name = "Saturation Down"
    description = "Change the saturation, less color"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_COLOR_MINUS)

class CurrentSaturation (eg.ActionClass):
    name = "Current Saturation"
    description = ""
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_COLOR_CURRENT)

class BrightnessUp(eg.ActionClass):
    name = "Brightness Up"
    description = "Brightness control Up"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_BRIGHTNESS_PLUS)

class BrightnessDown(eg.ActionClass):
    name = "Brightness Down"
    description = "Brightness control Down"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_BRIGHTNESS_MINUS)

class CurrentBrightness (eg.ActionClass):
    name = "Current Brightness"
    description = "The current brightness setting"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_BRIGHTNESS_CURRENT)

class SourceIn1(eg.ActionClass):
    name = "Video Input Source 1"
    description = "Tuner input for TVcards. DScaler shortcut keys Ctrl+Alt+F1"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_INPUT1)

class SourceIn2(eg.ActionClass):
    name = "Video Input Source 2"
    description = "Composite input. DScaler shortcut keys Ctrl+Alt+F2"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_INPUT2)

class SourceIn3(eg.ActionClass):
    name = "Video Input Source 3"
    description = "S-Video input. DScaler shortcut keys Ctrl+Alt+F3"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_INPUT3)

class SourceIn4(eg.ActionClass):
    name = "Video Input Source 4"
    description = "Composite over S-Video. DScaler shortcut keys Ctrl+Alt+F4"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_INPUT4)

class SourceIn5(eg.ActionClass):
    name = "Video Input Source 5"
    description = "DScaler shortcut keys Ctrl+Alt+F5"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_INPUT5)

class SourceIn6(eg.ActionClass):
    name = "Video Input Source 6"
    description = "DScaler shortcut keys Ctrl+Alt+F6"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_INPUT6)

class SourceIn7(eg.ActionClass):
    name = "Video Input Source 7"
    description = "DScaler shortcut keys Ctrl+Alt+F7"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_INPUT7)

class FirstSource(eg.ActionClass):
    name = "First Video Input"
    description = "Change to first input source."
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_FIRST)

class InitialSource(eg.ActionClass):
    name = "Initial Video Input Source"
    description = "Change to initial input source. See DScaler Documentation"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SOURCE_INITIAL)


class PixelWidth_768(eg.ActionClass):
    name = "Pixel Width 768"
    description = "Pixel Width 768 "
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SETTINGS_PIXELWIDTH_768)

class PixelWidth_754(eg.ActionClass):
    name = "Pixel Width 754"
    description = "Pixel Width 754"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SETTINGS_PIXELWIDTH_754)

class PixelWidth_720(eg.ActionClass):
    name = "Pixel Width 720"
    description = "Pixel Width 720"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SETTINGS_PIXELWIDTH_720)

class PixelWidth_640(eg.ActionClass):
    name = "Pixel Width 640"
    description = "Pixel Width 640"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SETTINGS_PIXELWIDTH_640)

class PixelWidth_480(eg.ActionClass):
    name = "Pixel Width 480"
    description = "Pixel Width 480"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SETTINGS_PIXELWIDTH_480)

class PixelWidth_384(eg.ActionClass):
    name = "Pixel Width 384"
    description = "Pixel Width 384"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SETTINGS_PIXELWIDTH_384)

class PixelWidth_320(eg.ActionClass):
    name = "Pixel Width 320"
    description = "Pixel Width 320"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_SETTINGS_PIXELWIDTH_320)

class ZoomIn(eg.ActionClass):
    name = "Zoom In"
    description = "Video zoom in. Same as Shift+Z key."
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_ZOOM_PLUS)

class ZoomOut(eg.ActionClass):
    name = "Zoom Out"
    description = "Video zoom out. Same as Z key."
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_ZOOM_MINUS)

class WindowOnTop(eg.ActionClass):
    name = "Window On Top"
    description = "Bring window to the top Same as Always On Top Window option"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_ON_TOP)

# ######### Recording Stuff  ############################

class TS_Record(eg.ActionClass):
    name = "Start Recording"
    description = "Start Recording. Same as Shift+R"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TSRECORD)

class TS_StopRecording(eg.ActionClass):
    name = "Stop Recording"
    description = "Stop Recording. Same as Shift+S"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TSSTOP)

class TS_Rewind(eg.ActionClass):
    name = "Fast Backward"
    description = "Rewind or 'Fast Backward'. Same as the { key"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TSRWND)

class TS_FastForward(eg.ActionClass):
    name = "Fast Forward"
    description = "Fast Forward. Same as the } key"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TSFFWD)

class TS_Play(eg.ActionClass):
    name = "Play"
    description = "Play. Same as Shift+P"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TSPLAY)

class TS_Previous(eg.ActionClass):
    name = "Previous"
    description = "Previous, Same as the < key"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TSPREV)

class TS_Next(eg.ActionClass):
    name = "Next"
    description = "Next, Same as the > key"
    def __call__(self):
        return SendCommand(WM_COMMAND,IDM_TSNEXT)

class TS_Pause(eg.ActionClass):
    name = "Pause"
    description = "Pause, Same as the | key"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TSPAUSE)

class TS_Options(eg.ActionClass):
    name = "Options"
    description = "Brings up the Time-shift options window"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_TSOPTIONS)

# ############ Closed Caption Stuff ######################
class CC_Off(eg.ActionClass):
    name = "Closed Caption Off"
    description = "Turn off closed caption."
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CCOFF)

class CC1 (eg.ActionClass):
    name = "Closed Caption 1"
    description = " Closed Caption 1"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CC1)

class CC2(eg.ActionClass):
    name = "Closed Caption 2"
    description = "Closed Caption 2"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CC2)

class CC3(eg.ActionClass):
    name = "Closed Caption 3"
    description = "Closed Caption 3"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CC3)

class CC4(eg.ActionClass):
    name = "Closed Caption 4"
    description = "Closed Caption 4"
    def __call__(self):
        return SendCommand(WM_COMMAND, IDM_CC4)


"""
You can add your own Calls using the included txt
file with other Dscaler Calls in it.

class Your Class(eg.ActionClass):
    name = "Name Here"
    description = "Description Here"
    def __call__(self):
        return SendCommand(WM_COMMAND, The API Call)

"""
#

