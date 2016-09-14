# -*- coding: utf-8 -*-

version="0.1"

# plugins/OnkyoISCP/__init__.py
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
    name = "MCE",
    author = "Brett Stottlemyer",
    version = version,
    kind = "program",
    guid = "{921D3571-92D9-43BE-B7F2-C1369F3ABACD}",
    description = (
        'Adds actions to control Windows Media Center.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1838",
    createMacrosOnAdd = False,
)

FindMCE = eg.WindowMatcher(u'ehshell.exe', u'Windows Media Center', None, None, None, 1, False, 0.0, 0)

class hotKeys(eg.ActionClass):

    def __call__(self):
        hwnds = FindMCE()
        if len(hwnds) != 0:
            eg.SendKeys(hwnds[0], self.value, False)
        else:
            self.PrintError("MCE is not running")
            return

ACTIONS = (
  (hotKeys, 'Num0', 'Num0', '0', u'{0}'),
  (hotKeys, 'Num1', 'Num1', '1', u'{1}'),
  (hotKeys, 'Num2', 'Num2', '2', u'{2}'),
  (hotKeys, 'Num3', 'Num3', '3', u'{3}'),
  (hotKeys, 'Num4', 'Num4', '4', u'{4}'),
  (hotKeys, 'Num5', 'Num5', '5', u'{5}'),
  (hotKeys, 'Num6', 'Num6', '6', u'{6}'),
  (hotKeys, 'Num7', 'Num7', '7', u'{7}'),
  (hotKeys, 'Num8', 'Num8', '8', u'{8}'),
  (hotKeys, 'Num9', 'Num9', '9', u'{9}'),
  (hotKeys, 'Escape', 'Escape', 'Escape', u'{Escape}'),
  (hotKeys, 'EnterKey', 'Enter', 'Enter', u'{Enter}'),
  (hotKeys, 'Start', 'Start', 'Start Media Center', u'{Win+Alt+Enter}'),
  (hotKeys, 'Mute', 'Mute', 'Volume mute', u'{F8}'),
  (hotKeys, 'VolumeUpKey', 'VolumeUp', 'Volume up', u'{F10}'),
  (hotKeys, 'VolumeDownKey', 'VolumeDown', 'Volume down', u'{F9}'),
  (hotKeys, 'ChannelUpKey', 'ChannelUp', 'Channel up', u'{PgUp}'),
  (hotKeys, 'ChannelDownKey', 'ChannelDown', 'Channel down', u'{PgDown}'),
  (hotKeys, 'ForwardKey', 'Forward', 'Fast Forward', u'{Ctrl+Shift+F}'),
  (hotKeys, 'RewindKey', 'Rewind', 'Rewind', u'{Ctrl+Shift+B}'),
  (hotKeys, 'Play', 'Play', 'Media play', u'{Ctrl+Shift+P}'),
  (hotKeys, 'Record', 'Record', 'Media record', u'{Ctrl+R}'),
  (hotKeys, 'Pause', 'Pause', 'Media pause', u'{Ctrl+P}'),
  (hotKeys, 'Stop', 'Stop', 'Media Stop', u'{Ctrl+Shift+S}'),
  (hotKeys, 'SkipKey', 'Skip', 'Media next track', u'{Ctrl+F}'),
  (hotKeys, 'ReplayKey', 'Replay', 'Media previous track', u'{Ctrl+B}'),
  (hotKeys, 'Pound', 'Pound', 'Pound', u'{Pound}'),
  (hotKeys, 'Star', 'Star', 'Star', u'{Star}'),
  (hotKeys, 'UpKey', 'Up', 'Up arrow', u'{Up}'),
  (hotKeys, 'DownKey', 'Down', 'Down arrow', u'{Down}'),
  (hotKeys, 'LeftKey', 'Left', 'Left arrow', u'{Left}'),
  (hotKeys, 'RightKey', 'Right', 'Right arrow', u'{Right}'),
  (hotKeys, 'Ok', 'Ok', 'Return', u'{Enter}'),
  (hotKeys, 'BackKey', 'Back', 'Back', u'{Backspace}'),
  (hotKeys, 'DVDMenu', 'DVDMenu', 'Go to DVD menu', u'{Ctrl+Shift+M}'),
  (hotKeys, 'LiveTV', 'LiveTV', 'Go to live TV', u'{Ctrl+T}'),
  (hotKeys, 'Guide', 'Guide', 'Go to the Guide', u'{Ctrl+G}'),
  (hotKeys, 'F24', 'F24', 'F24', u'{F24}'),
  (hotKeys, 'Music', 'Music', 'Go to Music', u'{Ctrl+M}'),
  (hotKeys, 'Recorded_TV', 'Recorded_TV', 'Go to recorded TV', u'{Ctrl+O}'),
  (hotKeys, 'Pictures', 'Pictures', 'Go to pictures', u'{Ctrl+I}'),
  (hotKeys, 'Videos', 'Videos', 'Go to videos', u'{Ctrl+E}'),
  (hotKeys, 'Zoom', 'Zoom', 'Zoom', u'{Ctrl+Shift+Z}'),
  (hotKeys, 'Radio', 'Radio', 'Go to Radio', u'{Ctrl+A}'),
  (hotKeys, 'Flip3D', 'Flip3D', 'Flip 3D', u'{Ctrl+Win+Tab}'),
  (hotKeys, 'Exit', 'Exit', 'Exit Application', u'{Alt+F4}'),
  (hotKeys, 'PlayPause', 'PlayPause', 'Media play/pause', u'{Ctrl+P}'),
  (hotKeys, 'Audio', 'Audio', 'Change DVD audio selection', u'{Ctrl+Shift+A}'),
  (hotKeys, 'Subtitle', 'Subtitle', 'Change DVD subtitle selection', u'{Ctrl+U}'),
  (hotKeys, 'Home', 'Home', 'First item', u'{Home}'),
  (hotKeys, 'End', 'End', 'Last item', u'{End}'),
  (hotKeys, 'ToggleWindowMode', 'ToggleWindowMode', 'Toggle window mode', u'{Alt+Enter}'),
  (hotKeys, 'ToggleClosedCap', 'ToggleClosedCap', 'Toggle closed captions', u'{Ctrl+Shift+C}'),
  (hotKeys, 'Menu', 'Menu', 'Display context menu', u'{Ctrl+D}'),
  (hotKeys, 'RipCD', 'RipCD', 'Rip a CD', u'{Ctrl+R}'),
)
predefinedCustomActions = {
  "Up":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.UpKey()))",
  "Down":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.DownKey()))",
  "Left":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.LeftKey()))",
  "Right":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.RightKey()))",
  "Back":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.EscKey()))",
  "Enter":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.EnterKey()))",
  "VolumeUp":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.VolumeUpKey()))",
  "VolumeDown":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.VolumeDownKey()))",
  "Forward":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.ForwardKey()))",
  "Rewind":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.RewindKey()))",
  "Skip":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.SkipKey()))",
  "Replay":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.ReplayKey()))",
  "ChannelUp":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.ChannelUpKey()))",
  "ChannelDown":"ContextSwitcher.AutoRepeat(.6,.3,.6,.01,action(MCE.ChannelDownKey()))",
  "Sleep":"System.Hibernate(True)",
  "PowerOff":"System.PowerDown(True)",
}

class MCE(eg.PluginClass):

    def __init__(self):
        self.windowMatch = FindMCE
        self.AddActionsFromList(ACTIONS)
        self.predefinedCustomActions = predefinedCustomActions
