# Copyright (C) 2008 Chris Longo <cal@chrislongo.net> and Tobias Arrskog (topfs2)
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

from xbmcclient import *

# expose some information about the plugin through an eg.PluginInfo subclass

eg.RegisterPlugin(
    name = "XBMC",
    author = "Chris Longo",
    version = "0.2." + "$LastChangedRevision: 386 $".split()[1],
    kind = "program",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=1005",
    description = "Adds actions to control <a href='http://www.xbmc.org/'>XBMC</a>.",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsRAAALEQF/ZF+RAAAA"
        "BGdBTUEAALGeYUxB9wAAACBjSFJNAAB6fAAAfosAAPoBAACHPAAAbUoAAPFDAAA2IAAAHlNX4WK7"
        "AAACYElEQVR42tTTPW8ScQDH8d/9n44HESgFKQjFWku1rUYdTEAT0sGHSU10cHZz0piYjqYxbia6"
        "+hB3Y0w3kzq0scaojdZqYiMp1dQWAlLg4A7ugbvzRXTy8wK+21dyXRe7QbBLuw6wG3ceJnJnLuTL"
        "279DrutySBIhEnUopSbjtMsYVzkXLSFEU5Y9dY/XW5Nlr207DpRWE+zzp6VHxWLpstpWKaEA5RT9"
        "XgCcC/jDDihjOpWI6vF4WkLweigULgdD4R/p4ZH30X1Dr6XhbK4i/OH43qSKVikJLhhGz26AEo61"
        "+Qz0roWR8RDWixtIJKP4/mUVA5EgkvvjOHEy/1FKj+XnwpHMxdipIhJH29C2o0hMVmH1KJQyxWTw"
        "FuKhKYCbaDUVOI4LwzKxOD8PAvkrMazOW1uSUH43ilCqgUYphvJyBitzKUyfLiCVBe7PPkVzp4l7"
        "dx9g+lwB5T9bePPqJTIjB4v0uqmVi4cHbx67UkFteRjRAx30mgEcym9iZz2NpRcyfAM6Om0Nruui"
        "sr2F8SNZuIQjEhl6Lj0LAY8Hcwtq6nwhStuQJB8sWOh3fTClBgIDOhj1wDAtcEFRq/5FW+shPRRF"
        "diyTYJNe4Kr1bfaJHiv0qAtBKTgX4D6CAJXAbQIhaYhyG16iIxvpwEfW0BITM75YrsJm3Ah6SnfB"
        "kCtzWmLikmabYLYAIRxO34Zp6nAs9VdX6xSVRn2lb7QWe2b3w9RxplwLy2AL8AOMIa5s3vb6gzUm"
        "+5mh1XXL0Lq2pVRVQ2z66J6fpLdaMqu6KjwUXo8XnFH0+w6k/3+mfwMAzwT87LI0qNEAAAAASUVO"
        "RK5CYII="            
    ),
)

# the physical remote buttons mapped to what is defined in Keymap.xml

BUTTONS = (
    ("Up", "Up", "Simulate a press on the up button.", "up"),        
    ("Down", "Down", "Simulate a press on the down button.", "down"),        
    ("Left", "Left", "Simulate a press on the left button.", "left"),        
    ("Right", "Right", "Simulate a press on the right button.", "right"),        
    ("PageUp", "Page Up", "Simulate a press on the page up button.", "pageplus"),
    ("Page Down", "Page Down", "Simulate a press on the page down button.", "pageminus"),
    ("Select", "Select", "Simulate a press on the select button.", "select"),
    ("Back", "Back", "Simulate a press on the back button.", "back"),
    ("Play", "Play", "Simulate a press on the play button.", "play"),
    ("Pause", "Pause", "Simulate a press on the pause button.", "pause"),
    ("Stop", "Stop", "Simulate a press on the stop button.", "stop"),
    ("FastForward", "Fast Forward", "Simulate a press on the fast-forward button.", "forward"),
    ("Rewind", "Rewind", "Simulate a press on the rewind button.", "reverse"),
    ("SkipNext", "Skip Next", "Simulate a press on the skip-next button.", "skipplus"),
    ("SkipPrevious", "Skip Previous", "Simulate a press on the skip-previous button.", "skipminus"),
    ("Record", "Record", "Simulate a press on the record button.", "record"),
    ("VolumeUp", "Volume Up", "Simulate a press on the volume up button.", "volumeplus"),       
    ("VolumeDown", "Volume Down", "Simulate a press on the volume down button.", "volumeminus"), 
    ("Mute", "Mute", "Simulate a press on the mute button.", "mute"),
    ("Zero", "Zero", "Simulate a press on the 0 button.", "zero"),              
    ("One", "One", "Simulate a press on the 1 button.", "one"),              
    ("Two", "Two", "Simulate a press on the 2 button.", "two"),              
    ("Three", "Three", "Simulate a press on the 3 button.", "three"),              
    ("Four", "Four", "Simulate a press on the 4 button.", "four"),              
    ("Five", "Five", "Simulate a press on the 5 button.", "five"),              
    ("Six", "Six", "Simulate a press on the 6 button.", "six"),              
    ("Seven", "Seven", "Simulate a press on the 7 button.", "seven"),              
    ("Eight", "Eight", "Simulate a press on the 8 button.", "eight"),              
    ("Nine", "Nine", "Simulate a press on the 9 button.", "nine"),
    ("Star", "Star", "Simulate a press on the * button.", "star"),
    ("Hash", "Hash", "Simulate a press on the # button.", "hash"),
    ("Menu", "Menu", "Simulate a press on the menu button.", "menu"),
    ("Display", "Display", "Simulate a press on the display button.", "display"),
    ("Start", "Start", "Simulate a press on the start button.", "start"),
    ("Title", "Title", "Simulate a press on the title button.", "title"),
    ("Info", "Info", "Simulate a press on the info button.", "info"),
    ("Clear", "Clear", "Simulate a press on the clear button.", "clear"),
    ("MyVideo", "My Video", "Simulate a press on the My Video button.", "myvideo"),
    ("MyMusic", "My Music", "Simulate a press on the My Music button.", "mymusic"),
    ("MyPictures", "My Pictures", "Simulate a press on the My Pictures button.", "mypictures"),
    ("MyTV", "My TV", "Simulate a press on the My TV button.", "mytv"),
    ("Power", "Power", "Simulate a press on the power button.", "power"),
)

# actions above and beyond what the simple remote can do for people with Harmony Remotes, etc.

ACTIONS = (   
    ("BigSkipBackward", "Big Skip Backward", "Big skip backward.", "PlayerControl(BigSkipBackWard)"),
    ("BigSkipForward", "Big Skip Forward", "Big skip forward.", "PlayerControl(BigSkipForward)"),
    ("SmallSkipBackward", "Small Skip Backward", "Small skip backward.", "PlayerControl(SmallSkipBackward)"),
    ("SmallSkipForward", "Small Skip Forward", "Small skip forward.", "PlayerControl(SmallSkipForward)"),
    ("PartyMode", "Party Mode", "Party mode.", "PlayerControl(PartyMode)"),
    ("Random", "Random", "Random.", "PlayerControl(Random)"),
    ("Repeat", "Repeat", "Repeat.", "PlayerControl(Repeat)"),
    ("TakeScreenShot", "Take Screen Shot", "Takes a screen shot.", "TakeScreenshot"),
    ("LastFMLove", "Last FM Love", "Add the current playing last.fm radio track to the last.fm loved tracks.", "LastFM.Love"),
    ("LastFMBan", "Last FM Ban", "Ban the current playing last.fm radio track.", "LastFM.Ban"),
    ("EjectTray", "Eject Tray", "Close or open the DVD tray.", "EjectTray"),
    ("PlayDVD", "Play DVD", "Plays the inserted CD or DVD media from the DVD-ROM Drive.", "PlayDVD"),
    ("UpdateVideoLibrary", "Update Video Library", "Update the video library.", "UpdateLibrary(Video)"),
    ("UpdateMusicLibrary", "Update Music Library", "Update the music library.", "UpdateLibrary(Music)"),
    ("Reset", "Reset Computer", "Reset the computer.", "Reset"),
)    

# prototype for remote button presses

class ButtonPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.xbmc.send_remote_button(self.value, 0, 1)
        except:
            raise self.Exceptions.ProgramNotRunning        

# prototype for actions

class ActionPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.xbmc.send_action(self.value)
        except:
            raise self.Exceptions.ProgramNotRunning

# And now we define the actual plugin:

class XBMC(eg.PluginClass):
    def __init__(self):
        self.AddActionsFromList(BUTTONS, ButtonPrototype)
        self.AddActionsFromList(ACTIONS, ActionPrototype)
        self.xbmc = XBMCClient("EventGhost")
    
    def __start__(self):
        try:
            self.xbmc.connect()
        except:
            raise self.Exceptions.ProgramNotRunning
    
    def __stop__(self):
        try:
            self.xbmc.close()
        except:
            pass
    
    def __close__(self):
        pass