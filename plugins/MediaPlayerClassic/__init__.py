#
# Plugins/MediaPlayerClassic/__init__.py
#
# Copyright (C) 2006 MonsterMagnet
#
# This file is a plugin for EventGhost.
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


eg.RegisterPlugin(
    name = "Media Player Classic",
    author = "MonsterMagnet",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control '
        '<a href="http://sourceforge.net/projects/guliverkli/">'
        'Media Player Classic</a>.'
    ),
    help = """
        Only for version <b>6.4.8.9</b> or above.
        The plugin will not work with older versions of MPC!
        
        <a href=http://www.eventghost.org/forum/viewtopic.php?t=17>
        Bugreports</a>
        
        <p><a href="http://sourceforge.net/projects/guliverkli/">
        Media Player Classic SourceForge Project</a>
    """,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAhElEQVR42rWRgQqAIAwF"
        "fV+++eWr1V6kiM6gQaTVHYehJEdV7bUG18hCInIDQMNhA+L7cQHBETQrBWERDXANjcxm"
        "Ee6CyFxd6ArkynZT5l7KK9gFbs3CrGgEPLzM1FonAn9kz59stqhnhdhEwK/j3m0Tgj8K"
        "OPmCr4eYpmMaASt3JS44ADcFoxFdcIMPAAAAAElFTkSuQmCC"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=694"
)
    
# changelog:
# 1.1 by bitmonster
#     - changed code to use new AddActionsFromList
# 1.0 by MonsterMagnet
#     - initial version


ACTIONS = (
(eg.ActionGroup, 'GroupMainControls', 'Main controls', None, (
    ('Exit', 'Quit Application', None, 816),
    ('PlayPause', 'Play/Pause', None, 889),
    ('Play', 'Play', None, 887),
    ('Pause', 'Pause', None, 888),
    ('Stop', 'Stop', None, 890),
    ('JumpForwardSmall', 'Jump Forward Small', None, 900),
    ('JumpBackwardSmall', 'Jump Backward Small', None, 899),
    ('JumpForwardMedium', 'Jump Forward Medium', None, 902),
    ('JumpBackwardMedium', 'Jump Backward Medium', None, 901),
    ('JumpForwardLarge', 'Jump Forward Large', None, 904),
    ('JumpBackwardLarge', 'Jump Backward Large', None, 903),
    ('JumpForwardKeyframe', 'Jump Forward Keyframe', None, 898),
    ('JumpBackwardKeyframe', 'Jump Backward Keyframe', None, 897),
    ('IncreaseRate', 'Increase Rate', None, 895),
    ('DecreaseRate', 'Decrease Rate', None, 894),
    ('ResetRate', 'Reset Rate', None, 896),
    ('VolumeUp', 'Volume Up', None, 907),
    ('VolumeDown', 'Volume Down', None, 908),
    ('VolumeMute', 'Volume Mute', None, 909),
    ('BossKey', 'Boss Key', None, 943),
    ('Next', 'Next', None, 921),
    ('Previous', 'Previous', None, 920),
    ('NextPlaylistItem', 'Next Playlist Item', None, 919),
    ('PreviousPlaylistItem', 'Previous Playlist Item', None, 918),
    ('OpenFile', 'Open File', None, 800),
    ('OpenDVD', 'Open DVD', None, 801),
    ('QuickOpen', 'Quick Open File', None, 968),
    ('FrameStep', 'Frame Step', None, 891),
    ('FrameStepBack', 'Frame Step Back', None, 892),
    ('GoTo', 'Go To', None, 893),
    ('AudioDelayAdd10ms', 'Audio Delay +10ms', None, 905),
    ('AudioDelaySub10ms', 'Audio Delay -10ms', None, 906),
)),
(eg.ActionGroup, 'GroupViewModes', 'View modes', None, (
    ('Fullscreen', 'Fullscreen', None, 830),
    ('FullscreenWOR', 'Fullscreen without resolution change', None, 831),
    ('PnSIncSize', 'Pan & Scan Increase Size', None, 862),
    ('PnSDecSize', 'Pan & Scan Decrease Size', None, 863),
    ('ViewMinimal', 'View Minimal', None, 827),
    ('ViewCompact', 'View Compact', None, 828),
    ('ViewNormal', 'View Normal', None, 829),
    ('AlwaysOnTop', 'Always On Top', None, 884),
    ('Zoom50', 'Zoom 50%', None, 832),
    ('Zoom100', 'Zoom 100%', None, 833),
    ('Zoom200', 'Zoom 200%', None, 834),
    ('VidFrmHalf', 'Video Frame Half', None, 835),
    ('VidFrmNormal', 'Video Frame Normal', None, 836),
    ('VidFrmDouble', 'Video Frame Double', None, 837),
    ('VidFrmStretch', 'Video Frame Stretch', None, 838),
    ('VidFrmInside', 'Video Frame Inside', None, 839),
    ('VidFrmOutside', 'Video Frame Outside', None, 840),
    ('PnSReset', 'Pan & Scan Reset', None, 861),
    ('PnSIncWidth', 'Pan & Scan Increase Width', None, 864),
    ('PnSIncHeight', 'Pan & Scan Increase Height', None, 866),
    ('PnSDecWidth', 'Pan & Scan Decrease Width', None, 865),
    ('PnSDecHeight', 'Pan & Scan Decrease Height', None, 867),
    ('PnSCenter', 'Pan & Scan Center', None, 876),
    ('PnSLeft', 'Pan & Scan Left', None, 868),
    ('PnSRight', 'Pan & Scan Right', None, 869),
    ('PnSUp', 'Pan & Scan Up', None, 870),
    ('PnSDown', 'Pan & Scan Down', None, 871),
    ('PnSUpLeft', 'Pan & Scan Up/Left', None, 872),
    ('PnSUpRight', 'Pan & Scan Up/Right', None, 873),
    ('PnSDownLeft', 'Pan & Scan Down/Left', None, 874),
    ('PnSDownRight', 'Pan & Scan Down/Right', None, 875),
    ('PnSRotateAddX', 'Pan & Scan Rotate X+', None, 877),
    ('PnSRotateSubX', 'Pan & Scan Rotate X-', None, 878),
    ('PnSRotateAddY', 'Pan & Scan Rotate Y+', None, 879),
    ('PnsRotateSubY', 'Pan & Scan Rotate Y-', None, 880),
    ('PnSRotateAddZ', 'Pan & Scan Rotate Z+', None, 881),
    ('PnSRotateSubZ', 'Pan & Scan Rotate Z-', None, 882),
)),
(eg.ActionGroup, 'GroupDvdControls', 'DVD controls', None, (
    ('DVDTitleMenu', 'DVD Title Menu', None, 922),
    ('DVDRootMenu', 'DVD Root Menu', None, 923),
    ('DVDSubtitleMenu', 'DVD Subtitle Menu', None, 924),
    ('DVDAudioMenu', 'DVD Audio Menu', None, 925),
    ('DVDAngleMenu', 'DVD Angle Menu', None, 926),
    ('DVDChapterMenu', 'DVD Chapter Menu', None, 927),
    ('DVDMenuLeft', 'DVD Menu Left', None, 928),
    ('DVDMenuRight', 'DVD Menu Right', None, 929),
    ('DVDMenuUp', 'DVD Menu Up', None, 930),
    ('DVDMenuDown', 'DVD Menu Down', None, 931),
    ('DVDMenuActivate', 'DVD Menu Activate', None, 932),
    ('DVDMenuBack', 'DVD Menu Back', None, 933),
    ('DVDMenuLeave', 'DVD Menu Leave', None, 934),
    ('DVDNextAngle', 'DVD Next Angle', None, 960),
    ('DVDPrevAngle', 'DVD Previous Angle', None, 961),
    ('DVDNextAudio', 'DVD Next Audio', None, 962),
    ('DVDPrevAudio', 'DVD Prev Audio', None, 963),
    ('DVDNextSubtitle', 'DVD Next Subtitle', None, 964),
    ('DVDPrevSubtitle', 'DVD Prev Subtitle', None, 965),
    ('DVDOnOffSubtitle', 'DVD On/Off Subtitle', None, 966),
)),
(eg.ActionGroup, 'GroupExtendedControls', 'Extended controls', None, (
    ('OpenDevice', 'Open Device', None, 802),
    ('SaveAs', 'Save As', None, 805),
    ('SaveImage', 'Save Image', None, 806),
    ('SaveImageAuto', 'Save Image Auto', None, 807),
    ('LoadSubTitle', 'Load Subtitle', None, 809),
    ('SaveSubtitle', 'Save Subtitle', None, 810),
    ('Close', 'Close File', None, 804),
    ('Properties', 'Properties', None, 814),
    ('PlayerMenuShort', 'Player Menu Short', None, 948),
    ('PlayerMenuLong', 'Player Menu Long', None, 949),
    ('FiltersMenu', 'Filters Menu', None, 950),
    ('Options', 'Options', None, 886),
    ('NextAudio', 'Next Audio', None, 951),
    ('PrevAudio', 'Previous Audio', None, 952),
    ('NextSubtitle', 'Next Subtitle', None, 953),
    ('PrevSubtitle', 'Prev Subtitle', None, 954),
    ('OnOffSubtitle', 'On/Off Subtitle', None, 955),
    ('ReloadSubtitles', 'Reload Subtitles', None, 2302),
    ('NextAudioOGM', 'Next Audio OGM', None, 956),
    ('PrevAudioOGM', 'Previous Audio OGM', None, 957),
    ('NextSubtitleOGM', 'Next Subtitle OGM', None, 958),
    ('PrevSubtitleOGM', 'Previous Subtitle OGM', None, 959),
)),
(eg.ActionGroup, 'GroupToggleControls', 'Toggle player controls', None, (
    ('ToggleCaptionMenu', 'Toggle Caption Menu', None, 817),
    ('ToggleSeeker', 'Toggle Seeker', None, 818),
    ('ToggleControls', 'Toggle Controls', None, 819),
    ('ToggleInformation', 'Toggle Information', None, 820),
    ('ToggleStatistics', 'Toggle Statistics', None, 821),
    ('ToggleStatus', 'Toggle Status', None, 822),
    ('ToggleSubresyncBar', 'Toggle Subresync Bar', None, 823),
    ('TogglePlaylistBar', 'Toggle Playlist Bar', None, 824),
    ('ToggleCaptureBar', 'Toggle Capture Bar', None, 825),
    ('ToggleShaderEditorBar', 'Toggle Shader Editor Bar', None, 826),
)),
)

from eg.WinApi import FindWindow, SendMessageTimeout, WM_COMMAND


class ActionPrototype(eg.ActionClass):
    
    def __call__(self):
        try:
            hWnd = FindWindow("MediaPlayerClassicW")
            return SendMessageTimeout(hWnd, WM_COMMAND, self.value, 0)
        except:
            raise self.Exceptions.ProgramNotRunning
    


class MediaPlayerClassic(eg.PluginClass):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)

