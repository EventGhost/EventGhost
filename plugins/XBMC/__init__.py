
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
    version = "0.2." + "$LastChangedRevision$".split()[1],
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

# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs

ACTIONS = (   
    ("Up", "Up", "Moves up in the interface.", "Up"),        
    ("Down", "Down", "Moves down in the interface.", "Down"),        
    ("Left", "Left", "Moves left in the interface.", "Left"),        
    ("Right", "Right", "Moves right in the interface.", "Right"),        
    ("PageUp", "Page Up", "Moves up a page in the interface.", "PageUp"),
    ("PageDown", "Page Down", "Moves down a page in the interface.", "PageDown"),
    ("Select", "Select", "Selects the current element.", "Select"),
    ("PreviousMenu", "Previous Menu", "Previous menu.", "PreviousMenu"),
    ("ContextMenu", "Context Menu", "Context menu.", "ContextMenu"),
    ("Play", "Play", "Toggles play/pause of the current media.", "Play"),
    ("Pause", "Pause", "Pauses the current media.", "Pause"),
    ("Stop", "Stop", "Stops playback of the current media.", "Stop"),
    ("FastForward", "Fast Forward", "Fast-forwards the current media.", "FastForward"),
    ("Rewind", "Rewind", "Rewinds the current media.", "Rewind"),
    ("SkipNext", "Skip Next", "Skips to the next media item.", "SkipNext"),
    ("SkipPrevious", "Skip Previous", "Skips back to the previous media item.", "SkipPrevious"),
    ("Record", "Record", "Starts recording.", "Record"),
    ("BigSkipBackward", "Big Skip Backward", "Big skip backward.", "PlayerControl(BigSkipBackWard)"),
    ("BigSkipForward", "Big Skip Forward", "Big skip forward.", "PlayerControl(BigSkipForward)"),
    ("SmallSkipBackward", "Small Skip Backward", "Small skip backward.", "PlayerControl(SmallSkipBackward)"),
    ("SmallSkipForward", "Small Skip Forward", "Small skip forward.", "PlayerControl(SmallSkipForward)"),
    ("AspectRatio", "Aspect Ratio", "Display the aspect ratio of the current media.", "AspectRatio"),
    ("CodecInfo", "Codec Info", "Display the codec information of the current media.", "CodecInfo"),
    ("FullScreen", "Full Screen", "Display the current media in full screen mode.", "FullScreen"),
    ("Repeat", "Repeat", "Repeat.", "PlayerControl(Repeat)"),      
    ("ShowSubtitles", "Show Subtitles", "Toggle subtitles on or off.", "ShowSubtitles"),
    ("OSD", "Show OSD", "Shows the on-screen display.", "OSD"),
    ("ShowTime", "Show Time", "Show current play time.", "ShowTime"),
    ("VolumeUp", "Volume Up", "Raises the volume.", "VolumeUp"),       
    ("VolumeDown", "Volume Down", "Lowers the volume.", "VolumeDown"), 
    ("Mute", "Mute", "Simulate a press on the mute button.", "Mute"),
    ("ScrollUp", "Scroll Up", "Scroll up in list.", "ScrollUp"),
    ("ScrollDown", "Scroll Down", "Scroll down in list.", "ScrollDown"),
    ("Close", "Close", "Close and open dialog box.", "Close"),
    ("Number0", "Number 0", "Remote number 0.", "Number0"),
    ("Number1", "Number 1", "Remote number 1.", "Number1"),
    ("Number2", "Number 2", "Remote number 2.", "Number2"),
    ("Number3", "Number 3", "Remote number 3.", "Number3"),
    ("Number4", "Number 4", "Remote number 4.", "Number4"),
    ("Number5", "Number 5", "Remote number 5.", "Number5"),
    ("Number6", "Number 6", "Remote number 6.", "Number6"),
    ("Number7", "Number 7", "Remote number 7.", "Number7"),
    ("Number8", "Number 8", "Remote number 8.", "Number8"),
    ("Number9", "Number 9", "Remote number 9.", "Number9"),
    ("Playlist", "Playlist", "Shows the current playlist.", "Playlist"),
    ("Queue", "Queue", "Queue the current item.", "Queue"),
    ("MoveItemUp", "Move Item Up", "Move item up in playlist.", "MoveItemUp"),
    ("MoveItemDown", "Move Item Down", "Move item down in playlist.", "MoveItemDown"),
    ("Delete", "Delete", "Delete the current item.", "Delete"),
    ("Random", "Random", "Random.", "PlayerControl(Random)"),
    ("Repeat", "Repeat", "Repeat.", "PlayerControl(Repeat)"),
    ("PartyMode", "Party Mode", "Party mode.", "PlayerControl(PartyMode)"),
    ("ParentDir", "Parent Dir", "Parent directory.", "ParentDir"),
    ("Info", "Info", "Contextual information.", "Info"),
    ("TakeScreenShot", "Take Screen Shot", "Takes a screen shot.", "TakeScreenshot"),
    ("EjectTray", "Eject Tray", "Close or open the DVD tray.", "EjectTray"),
    ("PlayDVD", "Play DVD", "Plays the inserted CD or DVD media from the DVD-ROM Drive.", "PlayDVD"),
    ("Home", "Show Home Screen", "Show Home screen.", "ActivateWindow(Home)"),
    ("MyVideos", "Show Videos Screen", "Show Videos screen.", "ActivateWindow(MyVideos)"),
    ("MyMusic", "Show Music Screen", "Show Music screen.", "ActivateWindow(MyMusic)"),
    ("MyPictures", "Show Pictures Screen", "Show Pictures screen.", "ActivateWindow(MyPictures)"),
	("MyMovies", "Show Movies Screen", "Show Movies screen.", "ActivateWindow(MyVideoLibrary,movietitles,return)"),
	("MyTVShows", "Show TV Shows Screen", "Show TV Shows screen.", "ActivateWindow(MyVideoLibrary,tvshowtitles,return)"),   
    ("Weather", "Show Weather Screen", "Show Weather screen.", "ActivateWindow(Weather)"),
    ("Settings", "Show Settings Screen", "Show Settings screen.", "ActivateWindow(Settings)"),
    ("Favorites", "Show Favorites Screen", "Show Favorites screen.", "ActivateWindow(Favourites)"),
    ("SystemInfo", "Show System Info Screen", "Show System Info screen.", "ActivateWindow(SystemInfo)"),
    ("LastFMLove", "Last FM Love", "Add the current playing last.fm radio track to the last.fm loved tracks.", "LastFM.Love"),
    ("LastFMBan", "Last FM Ban", "Ban the current playing last.fm radio track.", "LastFM.Ban"),
    ("UpdateVideoLibrary", "Update Video Library", "Update the video library.", "UpdateLibrary(Video)"),
    ("UpdateMusicLibrary", "Update Music Library", "Update the music library.", "UpdateLibrary(Music)"),
    ("ShutdownMenu", "Show Shutdown Menu", "Show the shutdown Menu.", "ActivateWindow(ShutdownMenu)"),
    ("Quit", "Quit XBMC", "Quit XBMC.", "Quit"),
    ("Shutdown", "Shutdown Computer", "Trigger default shutdown behavior from settings.", "Shutdown"),
    ("Powerdown", "Powerdown Computer", "Powerdown the computer.", "Powerdown"),
    ("Suspend", "Suspend Computer", "Suspend the computer.", "Suspend"),
    ("Hibernate", "Hibernate Computer", "Hibernate the computer.", "Hibernate"),
    ("Reset", "Reset Computer", "Reset the computer.", "Reset"),
)    

class ActionPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.xbmc.send_action(self.value, ACTION_BUTTON)
        except:
            raise self.Exceptions.ProgramNotRunning

# And now we define the actual plugin:

class XBMC(eg.PluginClass):
    def __init__(self):
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