# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2008-06-01 17:49:55 +0200 (Sun, 01 Jun 2008) $
# $LastChangedRevision: 439 $
# $LastChangedBy: bitmonster $

eg.RegisterPlugin(
    name="ATI Remote Wonder II",
    description=(
        'Plugin for the ATI Remote Wonder II remote.'
        '\n\n<p>'
        '<center><img src="picture.jpg" /></a></center>'
    ),
    help = """
        <b>Notice:</b> The ATI Remote Wonder software must also run to
        receive events from this remote and the special "EventGhost.dll" 
        must be imported and enabled inside the ATI Remote Wonder 
        Software.<p>
        You will find this DLL inside:<br>
        <i>{Program&nbsp;Files}</i>\\EventGhost\\Plugins\\AtiRemoteWonder2\\
    """,
    url="http://www.eventghost.org/forum/viewtopic.php?t=915",
    author="Bitmonster",
    version="1.0." + "$LastChangedRevision: 363 $".split()[1],
    kind="remote",
)


KEY_MAP = (
    "Num0", "Num1", "Num2", "Num3", "Num4", 
    "Num5", "Num6", "Num7", "Num8", "Num9",
    "Hand",
    "LButtonDown", "RButtonDown", "LButtonDoubleClick", "RButtonDoubleClick",
    "Mouse090", "Mouse000", "Mouse270", "Mouse180", 
    "Mouse045", "Mouse135", "Mouse315", "Mouse225",
    "ChannelUp", "ChannelDown",
    "VolumeUp", "VolumeDown", "Mute",
    "Menu", "Setup",
    "Up", "Down", "Left", "Right", "Ok",
    "FastForward", "Rewind", "Play", "Pause", "Stop", "Record",
    "StopWatch",
    "A", "B", "C", "D", "E", "F",
    "Resize", "WebLaunch", "Help", "Info", "Power", "Book",
    "Ati", "TV", "TV2", "FM", "DVD", "Guide",
)

MSG_NUM = 0x8123

class AtiRemoteWonder2(eg.PluginClass):
    
    def __start__(self):
        self.info.eventPrefix = "ATI"
        self.auxNum = -1
        for i in range(5):
            eg.messageReceiver.AddHandler(MSG_NUM + i, self.HandleEvent)
        
        
    def __stop__(self):
        for i in range(5):
            eg.messageReceiver.RemoveHandler(MSG_NUM + i, self.HandleEvent)
        
        
    def HandleEvent(self, hWnd, mesg, keyCode, keyState):
        auxNum = mesg - MSG_NUM
        if auxNum != self.auxNum:
            if auxNum == 0:
                self.TriggerEvent("PC")
            else:
                self.TriggerEvent("AUX%i" % auxNum)
            self.auxNum = auxNum
        if keyState == 0:
            self.EndLastEvent()
            return
        try:
            keyStr = KEY_MAP[keyCode]
        except:
            keyStr = str(keyCode)
        self.TriggerEnduringEvent(keyStr)
