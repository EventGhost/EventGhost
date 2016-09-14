# -*- coding: utf-8 -*-
#
# Plugins/GOMlayer/__init__.py
#
# Copyright (C) 2008 CHeitkamp
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


eg.RegisterPlugin(
    name = "GOM Player",
    author = "CHeitkamp",
    version = "1.0.1093",
    kind = "program",
    guid = "{A4CF41AC-8813-4920-98E9-576D08711022}",
    createMacrosOnAdd = True,
    description = (
        "Adds support functions to control GOM Player.\n\n"
        "<p>Only tested with version <b>2.1.x.x</b>.</p>"
        "<p>The plugin may not work with other versions of GOM Player!</p>"
        "<p><a href=\"http://www.gomplayer.com/\">GOM Player Homepage</a></p>"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=854",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACQUlEQVR4nKWTTUhVQRSA"
        "v7n/plj+BYKFKAlGi8pwEVZgLkqiRS0DSXla4MLaWFRuBFvloo1kGVSuo8gQoqhFWYtK"
        "AvvRfggrQnwVr3yivjf3TnOv9Z60KjswnDkz53wzZ+YcoUK52chyROwZRgRDu1VoVMfu"
        "/lPwq4H6SBvLCV4aY/xeMPTsxuUD1FbY1K3PZexJLy31hZEuzLcjXVrkYFkWhsiCMoCO"
        "lrVU1bVyrqsSIQ2eDvYxuwD9Pb00713No0tnKM6zuNOznUD9AQip1SUWyXudTI5JxqZS"
        "zBaVcursSQ53ttO0fzO1DXlcPFbC4NCLyD8cGYBt23QPxOnue8v9T18YGW5nZ+w2dlkb"
        "VvkRrDWHEP46rCJJ264CevaV4zh2FuB6Lklp8jIhOdi8FbPiNN9ujTAqHGZGn2OWNSBc"
        "nRr61FzJjspcbNddAtCGo8e1jjjmpgv4Ror3jduYCze9UpjXOpjRH2/qfw8XBZ7nRYAo"
        "EU/fQOlFmcjBHD+BU9XPRiWJHlsK0s9aUfIdan4BP7EKX4WHOlmA63oo7e37G5CPz6OS"
        "4/raTTooIJgcxucrKvUBfzofOWchrSCKyQBsTRNCEKRNgkQN6dcTyM8xnXe+3izWIJtg"
        "aiV+PIeUCnjwMcDx3CzAcZwor66HiuNbDNzpcszvZYgVabQ/atbBT5nMa2PiR8D1CYdf"
        "n7DYC00DyUxh5FiKozULFNghcrHkfP1Cc7p6rr7RFRm3Mr5XYnnZZloK+RsJg6Mb/G87"
        "/wRX99eUmF4hlQAAAABJRU5ErkJggg=="
    ),
)


# changelog:
# 1.0 by CHeitkamp
#     - initial version
# 1.1 by bitmonster
#     - added None to all action tuples in the ACTIONS list, that didn't have
#       an item for the 'description' attribute, because the use of
#       AddActionFromList without an argument for the description is now
#       deprecated.

ACTIONS = (
    ( eg.ActionGroup, 'GroupMainControls', 'Main controls', None, (
        ( 'Exit', 'Quit Application', None, 0x8048 ),
        ( 'PlayPause', 'Play/Pause', None, 0x800C ),
        ( 'Stop', 'Stop', None, 0x8006 ),
        ( 'Restart', 'Restart from the beginning', None, 0x8010 ),
        ( 'JumpForwardSmall', 'Jump Forward Small', 'Jump Forward 10sec, if not configured otherwise', 0x8009 ),
        ( 'JumpBackwardSmall', 'Jump Backward Small', 'Jump Backward 10sec, if not configured otherwise', 0x8008 ),
        ( 'JumpForwardMedium', 'Jump Forward Medium', 'Jump Forward 60sec, if not configured otherwise', 0x800B ),
        ( 'JumpBackwardMedium', 'Jump Backward Medium', 'Jump Backward 60sec, if not configured otherwise', 0x800A ),
        ( 'JumpForwardLarge', 'Jump Forward Large', 'Jump Forward 300sec, if not configured otherwise', 0x8012 ),
        ( 'JumpBackwardLarge', 'Jump Backward Large', 'Jump Backward 300sec, if not configured otherwise', 0x8011 ),
        ( 'IncreaseRate', 'Increase Rate', None, 0x8060 ),
        ( 'DecreaseRate', 'Decrease Rate', None, 0x8061 ),
        ( 'ResetRate', 'Reset Rate', None, 0x8062 ),
        ( 'VolumeUp', 'Volume Up', None, 0x8014 ),
        ( 'VolumeDown', 'Volume Down', None, 0x8013 ),
        ( 'VolumeMute', 'Volume Mute', None, 0x8016 ),
        ( 'BossKey', 'Boss Key', None, 0x8022 ),
        ( 'Next', 'Next', None, 0x809A ),
        ( 'Previous', 'Previous', None, 0x8099 ),
        ( 'OpenFile', 'Open File', None, 0x8003 ),
        ( 'OpenDVD', 'Open DVD', None, 0x8045 ),
        ( 'AudioDelayAdd100ms', 'Audio Delay +100ms', None, 0x827F ),
        ( 'AudioDelaySub100ms', 'Audio Delay -100ms', None, 0x827E ),
        ( 'AudioDelayReset', 'Audio Delay Reset', None, 0x8280 ),
    ) ),
    ( eg.ActionGroup, 'GroupViewModes', 'View modes', None, (
        ( 'Fullscreen', 'Fullscreen', None, 0x8154 ),
        ( 'FullscreenStretched', 'Fullscreen Stretched', None, 0x801C ),
        ( 'AlwaysOnTop', 'Always On Top', None, 0x8044 ),
        ( 'OnTopWhilePlaying', 'On Top while playing', None, 0x8085 ),
        ( 'Zoom50', 'Zoom 50%', None, 0x801D ),
        ( 'Zoom100', 'Zoom 100%', None, 0x801E ),
        ( 'Zoom150', 'Zoom 150%', None, 0x801F ),
        ( 'Zoom200', 'Zoom 200%', None, 0x8020 ),
        ( 'ZoomFit', 'Zoom Fit to Desktop Resolution', None, 0x8021 ),
    ) ),
    ( eg.ActionGroup, 'GroupDvdControls', 'DVD controls', None, (
        ( 'DVDTitleMenu', 'DVD Title Menu', None, 0x8149 ),
        ( 'DVDRootMenu', 'DVD Root Menu', None, 0x814A ),
        ( 'DVDSubtitleMenu', 'DVD Subtitle Menu', None, 0x814B ),
        ( 'DVDAudioMenu', 'DVD Audio Menu', None, 0x814D ),
        ( 'DVDAngleMenu', 'DVD Angle Menu', None, 0x814D ),
        ( 'DVDChapterMenu', 'DVD Chapter Menu', None, 0x814C ),
    ) ),
    ( eg.ActionGroup, 'GroupExtendedControls', 'Extended controls', None, (
        ( 'Close', 'Close File', None, 0x8045 ),
        ( 'Options', 'Options', None, 0x8059 ),
        ( 'OnOffSubtitle', 'On/Off Subtitle', None, 0x8029 ),
    ) ),
)


from eg.WinApi import FindWindow, SendMessageTimeout, WM_COMMAND


class ActionPrototype(eg.ActionClass):

    def __call__(self):
        try:
            hWnd = FindWindow( "GomPlayer1.x" )
            return SendMessageTimeout(hWnd, WM_COMMAND, self.value, 0)
        except:
            raise self.Exceptions.ProgramNotRunning


class GOMPlayer(eg.PluginClass):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)
