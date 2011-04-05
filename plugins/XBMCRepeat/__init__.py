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
import urllib
import json
import ast
import xml.dom.minidom
from xml.dom.minidom import Node

# expose some information about the plugin through an eg.PluginInfo subclass

eg.RegisterPlugin(
    name = "XBMC2",
    author = "Joni Boren",
    version = "0.6.0",
    kind = "program",
    guid = "{2DD98E35-F060-4444-9F11-168CD8131A6B}",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=10&t=1562",
    description = "Adds actions buttons to control <a href='http://www.xbmc.org/'>XBMC</a>.",
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

# from threading import Event, Thread

# Windows availible in XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Window_IDs
"""
"""

WINDOWS = (
(eg.ActionGroup, "Windows", "Windows", None, (
    ("MyMovies", "Show Movies Screen", "Show Movies screen.", "ActivateWindow(MyVideoLibrary,movietitles,return)"),
    ("MyTVShows", "Show TV Shows Screen", "Show TV Shows screen.", "ActivateWindow(MyVideoLibrary,tvshowtitles,return)"),
    ("ShutdownMenu", "Show Shutdown Menu", "Show the shutdown Menu.", "ActivateWindow(ShutdownMenu)"),
    ("Home", "Home", "Home", "Activatewindow(Home)"),
    ("Programs", "Programs", "Programs", "Activatewindow(Programs)"),
    ("Pictures", "Pictures", "Pictures", "Activatewindow(Pictures)"),
    ("Files", "Files", "Files", "Activatewindow(Files)"),
    ("Settings", "Settings", "Settings", "Activatewindow(Settings)"),
    ("Music", "Music", "Music", "Activatewindow(Music)"),
    ("Musicfiles", "Musicfiles", "Musicfiles", "Activatewindow(Musicfiles)"),
    ("Musiclibrary", "Musiclibrary", "Musiclibrary", "Activatewindow(Musiclibrary)"),
    ("Musicplaylist", "Musicplaylist", "Musicplaylist", "Activatewindow(Musicplaylist)"),
    ("Musicplaylisteditor", "Musicplaylisteditor", "Musicplaylisteditor", "Activatewindow(Musicplaylisteditor)"),
    ("Musicinformation", "Musicinformation", "Musicinformation", "Activatewindow(Musicinformation)"),
    ("Video", "Video", "Video", "Activatewindow(Video)"),
    ("Videofiles", "Videofiles", "Videofiles", "Activatewindow(Videofiles)"),
    ("Videolibrary", "Videolibrary", "Videolibrary", "Activatewindow(Videolibrary)"),
    ("Videoplaylist", "Videoplaylist", "Videoplaylist", "Activatewindow(Videoplaylist)"),
    ("Systeminfo", "Systeminfo", "Systeminfo", "Activatewindow(Systeminfo)"),
    ("Guicalibration", "Guicalibration", "Guicalibration", "Activatewindow(Guicalibration)"),
    ("Screencalibration", "Screencalibration", "Screencalibration", "Activatewindow(Screencalibration)"),
    ("Picturessettings", "Picturessettings", "Picturessettings", "Activatewindow(Picturessettings)"),
    ("Programssettings", "Programssettings", "Programssettings", "Activatewindow(Programssettings)"),
    ("Weathersettings", "Weathersettings", "Weathersettings", "Activatewindow(Weathersettings)"),
    ("Musicsettings", "Musicsettings", "Musicsettings", "Activatewindow(Musicsettings)"),
    ("Systemsettings", "Systemsettings", "Systemsettings", "Activatewindow(Systemsettings)"),
    ("Videossettings", "Videossettings", "Videossettings", "Activatewindow(Videossettings)"),
    ("Networksettings", "Networksettings", "Networksettings", "Activatewindow(Networksettings)"),
    ("Appearancesettings", "Appearancesettings", "Appearancesettings", "Activatewindow(Appearancesettings)"),
    ("Scripts", "Scripts", "Scripts", "Activatewindow(Scripts)"),
    ("Gamesaves", "Gamesaves", "Gamesaves", "Activatewindow(Gamesaves)"),
    ("Profiles", "Profiles", "Profiles", "Activatewindow(Profiles)"),
    ("Virtualkeyboard", "Virtualkeyboard", "Virtualkeyboard", "Activatewindow(Virtualkeyboard)"),
    ("Volumebar", "Volumebar", "Volumebar", "Activatewindow(Volumebar)"),
    ("Favourites", "Favourites", "Favourites", "Activatewindow(Favourites)"),
    ("Musicosd", "Musicosd", "Musicosd", "Activatewindow(Musicosd)"),
    ("Visualisationsettings", "Visualisationsettings", "Visualisationsettings", "Activatewindow(Visualisationsettings)"),
    ("Visualisationpresetlist", "Visualisationpresetlist", "Visualisationpresetlist", "Activatewindow(Visualisationpresetlist)"),
    ("Osdvideosettings", "Osdvideosettings", "Osdvideosettings", "Activatewindow(Osdvideosettings)"),
    ("Osdaudiosettings", "Osdaudiosettings", "Osdaudiosettings", "Activatewindow(Osdaudiosettings)"),
    ("Videobookmarks", "Videobookmarks", "Videobookmarks", "Activatewindow(Videobookmarks)"),
    ("Profilesettings", "Profilesettings", "Profilesettings", "Activatewindow(Profilesettings)"),
    ("Locksettings", "Locksettings", "Locksettings", "Activatewindow(Locksettings)"),
    ("Contentsettings", "Contentsettings", "Contentsettings", "Activatewindow(Contentsettings)"),
    ("Networksetup", "Networksetup", "Networksetup", "Activatewindow(Networksetup)"),
    ("Smartplaylisteditor", "Smartplaylisteditor", "Smartplaylisteditor", "Activatewindow(Smartplaylisteditor)"),
    ("Smartplaylistrule", "Smartplaylistrule", "Smartplaylistrule", "Activatewindow(Smartplaylistrule)"),
    ("Movieinformation", "Movieinformation", "Movieinformation", "Activatewindow(Movieinformation)"),
    ("Scriptsdebuginfo", "Scriptsdebuginfo", "Scriptsdebuginfo", "Activatewindow(Scriptsdebuginfo)"),
    ("Fullscreenvideo", "Fullscreenvideo", "Fullscreenvideo", "Activatewindow(Fullscreenvideo)"),
    ("Visualisation", "Visualisation", "Visualisation", "Activatewindow(Visualisation)"),
    ("Slideshow", "Slideshow", "Slideshow", "Activatewindow(Slideshow)"),
    ("Filestackingdialog", "Filestackingdialog", "Filestackingdialog", "Activatewindow(Filestackingdialog)"),
    ("Weather", "Weather", "Weather", "Activatewindow(Weather)"),
    ("Screensaver", "Screensaver", "Screensaver", "Activatewindow(Screensaver)"),
    ("Videoosd", "Videoosd", "Videoosd", "Activatewindow(Videoosd)"),
    ("Videomenu", "Videomenu", "Videomenu", "Activatewindow(Videomenu)"),
    ("Filebrowser", "Filebrowser", "Filebrowser", "Activatewindow(Filebrowser)"),
    ("Startup", "Startup", "Startup", "Activatewindow(Startup)"),
    ("Startwindow", "Startwindow", "Startwindow", "Activatewindow(Startwindow)"),
    ("Loginscreen", "Loginscreen", "Loginscreen", "Activatewindow(Loginscreen)"),
    ("Musicoverlay", "Musicoverlay", "Musicoverlay", "Activatewindow(Musicoverlay)"),
    ("Videooverlay", "Videooverlay", "Videooverlay", "Activatewindow(Videooverlay)"),
    ("Pictureinfo", "Pictureinfo", "Pictureinfo", "Activatewindow(Pictureinfo)"),
    ("Pluginsettings", "Pluginsettings", "Pluginsettings", "Activatewindow(Pluginsettings)"),
    ("Fullscreeninfo", "Fullscreeninfo", "Fullscreeninfo", "Activatewindow(Fullscreeninfo)"),
    ("PlayerControls", "Player Controls", "Player Controls", "ActivateWindow(PlayerControls)"),
)),
)
# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_throughout_most_of_XBMC

GENERAL_ACTIONS = (
(eg.ActionGroup, "General", "General", None, (
    ("Left", "Left", "Move left off a control.", "Left"),
    ("Right", "Right", "Move right off a control.", "Right"),
    ("Up", "Up", "Move up off a control.", "Up"),
    ("Down", "Down", "Move down off a control.", "Down"),
    ("PageUp", "Page Up", "Scroll up on page in a list, thumb, or text view.", "PageUp"),
    ("PageDown", "Page Down", "Scroll down on page in a list, thumb, or text view.", "PageDown"),
    ("Select", "Select", "Select a button, or an item from a list of thumb view.", "Select"),
    ("Highlight", "Highlight", "Highlight an item in a list or thumb view.", "highlight"),
    ("ParentDir", "ParentDir", "Go up a folder to the parent folder.", "parentdir"),
    ("PreviousMenu", "PreviousMenu", "Go back to the previous menu screen.", "previousmenu"),
    ("Info", "Info", "Show the information about the currently highlighted item, or currently playing item.", "info"),
    ("Screenshot", "Screenshot", "Take a screenshot of the current screen..", "Screenshot"),
    ("PowerOff", "PowerOff", "Shutdown and power off.", "PowerOff"),
    ("VolumeUp", "VolumeUp", "Increase the volume of playback..", "VolumeUp"),
    ("VolumeDown", "VolumeDown", "Decrease the volume of playback..", "VolumeDown"),
    ("Mute", "Mute", "Mute the volume..", "Mute"),
    ("ContextMenu", "ContextMenu", "Pops up a contextual menu.", "ContextMenu"),
    ("ScrollUp", "ScrollUp", "Variable speed scroll up for analog keys (stick or triggers).", "ScrollUp"),
    ("ScrollDown", "ScrollDown", "Variable speed scroll down for analog keys (stick or triggers).", "ScrollDown"),
    ("Close", "Close", "Used to close a dialog.", "Close"),
    ("Number0", "Number0", "Used to input the number 0.", "Number0"),
    ("Number1", "Number1", "Used to input the number 1.", "Number1"),
    ("Number2", "Number2", "Used to input the number 2.", "Number2"),
    ("Number3", "Number3", "Used to input the number 3.", "Number3"),
    ("Number4", "Number4", "Used to input the number 4.", "Number4"),
    ("Number5", "Number5", "Used to input the number 5.", "Number5"),
    ("Number6", "Number6", "Used to input the number 6.", "Number6"),
    ("Number7", "Number7", "Used to input the number 7.", "Number7"),
    ("Number8", "Number8", "Used to input the number 8.", "Number8"),
    ("Number9", "Number9", "Used to input the number 9.", "Number9"),
)),
)

# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_while_video_or_music_are_playing

MEDIA_PLAYING_ACTIONS = (
(eg.ActionGroup, "MediaPlaying", "Media playing", None, (
    ("Play", "Play", "Play the selected item (or folder of items), or unpause a paused item..", "Play"),
    ("Pause", "Pause", " Pause the currently playing item. .", "Pause"),
    ("Stop", "Stop", " Stop the currently playing item. .", "Stop"),
    ("FastForward", "FastForward", "Toggle the fastforward speed between normal play, 2x, 4x, 8x, 16x, and 32x..", "FastForward"),
    ("Rewind", "Rewind", "Toggle the rewind speed between normal play, 2x, 4x, 8x, 16x, and 32x..", "Rewind"),
    ("SkipNext", "SkipNext", "Skip to the next item in a playlist..", "SkipNext"),
    ("SkipPrevious", "SkipPrevious", "Skip to the previous item in a playlist..", "SkipPrevious"),
    ("FullScreen", "FullScreen", "Toggles fullscreen modes (either visualisation or video playback).", "FullScreen"),
    ("CodecInfo", "CodecInfo", "Show codec information about the currently playing item (during video or visualisation playback).", "CodecInfo"),
    ("AnalogSeekForward", "AnalogSeekForward", "Variable speed seeking for analog keys (stick or triggers).", "AnalogSeekForward"),
    ("AnalogSeekBack", "AnalogSeekBack", "Variable speed seeking for analog keys (stick or triggers).", "AnalogSeekBack"),
    ("AnalogFastForward", "AnalogFastForward", "Variable speed fast forward for analog keys (stick or triggers).", "AnalogFastForward"),
    ("AnalogRewind", "AnalogRewind", "Variable speed rewind for analog keys (stick or triggers).", "AnalogRewind"),
    ("PartyMode", "Party Mode", "Party mode.", "PlayerControl(PartyMode)"),
    ("Random", "Random", "Random.", "PlayerControl(Random)"),
    ("Repeat", "Repeat", "Repeat.", "PlayerControl(Repeat)"),
    ("UpdateVideoLibrary", "Update Video Library", "Update the video library.", "UpdateLibrary(Video)"),
    ("UpdateMusicLibrary", "Update Music Library", "Update the music library.", "UpdateLibrary(Music)"),
    ("IncreaseRating", "IncreaseRating", "Unused.", "IncreaseRating"),
    ("DecreaseRating", "DecreaseRating", "Unused .", "DecreaseRating"),
    ("EjectTray", "Eject Tray", "Close or open the DVD tray.", "EjectTray"),
    ("Record", "Record", "Starts recording.", "Record"),
    ("PlayDVD", "Play DVD", "Plays the inserted CD or DVD media from the DVD-ROM Drive.", "PlayDVD"),
    ("LastFMLove", "Last FM Love", "Add the current playing last.fm radio track to the last.fm loved tracks.", "LastFM.Love"),
    ("LastFMBan", "Last FM Ban", "Ban the current playing last.fm radio track.", "LastFM.Ban"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_only_in_Music_and_Videos_windows_only

PLAYLIST_ACTIONS = (
(eg.ActionGroup, "Playlist", "Playlist", None, (
    ("Playlist", "Playlist", "Toggle to playlist view from My Music or My Videos.", "Playlist"),
    ("Queue", "Queue", "Queue the item to the current playlist.", "Queue"),
    ("MoveItemUp", "MoveItemUp", "Used to rearrange playlists.", "MoveItemUp"),
    ("MoveItemDown", "MoveItemDown", "Used to rearrange playlists.", "MoveItemDown"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_only_in_Full_Screen_Video

FULLSCREEN_VIDEO_ACTIONS = (
(eg.ActionGroup, "FullscreenVideo", "FullScreen Video", None, (
    ("StepForward", "StepForward", "Step forward 1% in the movie..", "StepForward"),
    ("StepBack", "StepBack", "Step back 1% in the movie..", "StepBack"),
    ("BigStepForward", "BigStepForward", "Step forward 10% in the movie..", "BigStepForward"),
    ("BigStepBack", "BigStepBack", "Step back 10% in the movie..", "BigStepBack"),
    ("SmallStepBack", "SmallStepBack", "Step back 7 seconds in the current video..", "SmallStepBack"),
    ("OSD", "OSD", "Toggles the OSD while playing an item..", "OSD"),
    ("AspectRatio", "AspectRatio", "Toggle through the various aspect ratio modes (Normal is the preferred option)..", "AspectRatio"),
    ("ShowSubtitles", "ShowSubtitles", "Toggles whether subtitles are shown or not..", "ShowSubtitles"),
    ("NextSubtitle", "NextSubtitle", "Change to the next subtitle language, if there is more than one..", "NextSubtitle"),
    ("SubtitleDelayMinus", "SubtitleDelayMinus", "Decrease the delay amount of subtitles (use if subtitles are displaying too late).", "SubtitleDelayMinus"),
    ("SubtitleDelayPlus", "SubtitleDelayPlus", "Increase the delay amount of subtitles (use if subtitles are displaying too early).", "SubtitleDelayPlus"),
    ("AudioDelayMinus", "AudioDelayMinus", "Decrease the delay amount of audio (use if audio is being heard too early).", "AudioDelayMinus"),
    ("AudioDelayPlus", "AudioDelayPlus", "Increase the delay amount of audio (use if audio is being heard too late).", "AudioDelayPlus"),
    ("AudioNextLanguage", "AudioNextLanguage", "Change to the next audio track in a video with multiple audio tracks..", "AudioNextLanguage"),
    ("mplayerosd", "mplayerosd", "Show Mplayer's OSD.", "mplayerosd"),
    ("ShowTime", "ShowTime", "Used to show the current play time in music + video playback.", "ShowTime"),
    ("ShowVideoMenu", "ShowVideoMenu", "Go to the DVD Video menu when playing a DVD..", "ShowVideoMenu"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_during_a_picture_slideshow

SLIDESHOW_ACTIONS = (
(eg.ActionGroup, "PictureSlideshow", "Picture slideshow", None, (
    ("NextPicture", "NextPicture", "Move to the next picture in a slideshow..", "NextPicture"),
    ("PreviousPicture", "PreviousPicture", "Move to the previous picture in a slideshow..", "PreviousPicture"),
    ("ZoomOut", "ZoomOut", "Used in picture or slideshow to zoom out of the current image..", "ZoomOut"),
    ("ZoomIn", "ZoomIn", "Used in picture or slideshow to zoom in to the current image..", "ZoomIn"),
    ("ZoomNormal", "ZoomNormal", "Normal (fullscreen) viewing in My Pictures.", "ZoomNormal"),
    ("ZoomLevel1", "ZoomLevel1", "Zoom to 120% in My Pictures.", "ZoomLevel1"),
    ("ZoomLevel2", "ZoomLevel2", "Zoom to 150% in My Pictures.", "ZoomLevel2"),
    ("ZoomLevel3", "ZoomLevel3", "Zoom to 200% in My Pictures.", "ZoomLevel3"),
    ("ZoomLevel4", "ZoomLevel4", "Zoom to 280% in My Pictures.", "ZoomLevel4"),
    ("ZoomLevel5", "ZoomLevel5", "Zoom to 400% in My Pictures.", "ZoomLevel5"),
    ("ZoomLevel6", "ZoomLevel6", "Zoom to 600% in My Pictures.", "ZoomLevel6"),
    ("ZoomLevel7", "ZoomLevel7", "Zoom to 900% in My Pictures.", "ZoomLevel7"),
    ("ZoomLevel8", "ZoomLevel8", "Zoom to 1350% in My Pictures.", "ZoomLevel8"),
    ("ZoomLevel9", "ZoomLevel9", "Zoom to 2000% in My Pictures.", "ZoomLevel9"),
    ("AnalogMove", "AnalogMove", "Move in the calibration screens, and while zoomed in My Pictures..", "AnalogMove"),
    ("Rotate", "Rotate", "Rotate a picture in My Pictures.", "Rotate"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_screen_calibration

CALIBRATION_ACTIONS = (
(eg.ActionGroup, "ScreenCalibration", "Screen calibration", None, (
    ("NextCalibration", "NextCalibration", "Used in Video + GUI calibration.", "NextCalibration"),
    ("ResetCalibration", "ResetCalibration", "Used in Video + GUI calibration.", "ResetCalibration"),
    ("AnalogMove", "AnalogMove", "Move in the calibration screens, and while zoomed in My Pictures..", "AnalogMove"),
    ("NextResolution", "NextResolution", "Used in Video calibration.", "NextResolution"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_the_File_Manager

FILEMANAGER_ACTIONS = (
(eg.ActionGroup, "FileManager", "File Manager", None, (
    ("Delete", "Delete", "Used in My Files to delete a file..", "Delete"),
    ("Copy", "Copy", "Used in My Files to copy a file..", "Copy"),
    ("Move", "Move", "Used in My Files to move a file..", "Move"),
    ("Rename", "Rename", "Used in My Files to rename a file..", "Rename"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_the_on-screen_keyboard

ON_SCREEN_KEYBOARD_ACTIONS = (
(eg.ActionGroup, "On-screenKeyboard", "On-screen keyboard", None, (
    ("BackSpace", "BackSpace", "Used in the virtual keyboards to delete one letter..", "BackSpace"),
    ("Shift", "Shift", "Used in Virtual Keyboard to switch to upper or lower case letters.", "Shift"),
    ("Symbols", "Symbols", "Used in Virtual Keyboard to switch to or from symbols mode.", "Symbols"),
    ("CursorLeft", "CursorLeft", "Used in Virtual Keyboard to move the current cursor point to the left.", "CursorLeft"),
    ("CursorRight", "CursorRight", "Used in Virtual Keyboard to move the current cursor point to the right.", "CursorRight"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_during_a_music_visualisation

VISUALISATION_ACTIONS = (
(eg.ActionGroup, "MusicVisualisation", "Music visualisation", None, (
    ("OSD", "OSD", "Toggles the OSD while playing an item..", "OSD"),
    ("ShowPreset", "ShowPreset", "Shows the current visualisation preset (milkdrop/spectrum).", "ShowPreset"),
    ("PresetList", "PresetList", "Pops up the visualisation preset list (milkdrop/spectrum).", "PresetList"),
    ("NextPreset", "NextPreset", "Next visualisation preset.", "NextPreset"),
    ("PreviousPreset", "PreviousPreset", "Previous visualisation preset.", "PreviousPreset"),
    ("LockPreset", "LockPreset", "Lock the current visualisation preset.", "LockPreset"),
    ("RandomPreset", "RandomPreset", "Switch to a new random preset.", "RandomPreset"),
    ("increasevisrating", "increasevisrating", "increasevisrating.", "increasevisrating"),
    ("decreasevisrating", "decreasevisrating", "decreasevisrating.", "decreasevisrating"),
)),
)

SHUTDOWN_ACTIONS = (
(eg.ActionGroup, "ShutdownRelated", "Shutdown related", None, (
    ("Quit", "Quit XBMC", "Quit XBMC.", "Quit"),
    ("RestartApp", "Restart XBMC", "Restarts XBMC.", "RestartApp"),
    ("Reset", "Reset Computer", "Reset the computer.", "Reset"),
    ("Shutdown", "Shutdown Computer", "Trigger default Shutdown action defined in System Settings, Default Quit on Windows.", "Shutdown"),
    ("Powerdown", "Powerdown Computer", "Powerdown system.", "Powerdown"),
    ("Suspend", "Suspend Computer", "Suspends (S3 / S1 depending on bios setting) the System.", "Suspend"),
    ("Hibernate", "Hibernate Computer", "Hibernate (S5) the System.", "Hibernate"),
    ("Reboot", "Reboot Computer", "Cold reboots the system (power cycle).", "Reboot"),
    ("Restart", "Restart Computer", "Cold reboots the system (power cycle).", "Restart"),
)),
)

UNCATEGORIZED_ACTIONS = (
(eg.ActionGroup, "UncategorizedActions", "Uncategorized actions", None, (
    ("JumpSMS2", "JumpSMS2", "JumpSMS2.", "JumpSMS2"),
    ("JumpSMS3", "JumpSMS3", "JumpSMS3.", "JumpSMS3"),
    ("JumpSMS4", "JumpSMS4", "JumpSMS4.", "JumpSMS4"),
    ("JumpSMS5", "JumpSMS5", "JumpSMS5.", "JumpSMS5"),
    ("JumpSMS6", "JumpSMS6", "JumpSMS6.", "JumpSMS6"),
    ("JumpSMS7", "JumpSMS7", "JumpSMS7.", "JumpSMS7"),
    ("JumpSMS8", "JumpSMS8", "JumpSMS8.", "JumpSMS8"),
    ("JumpSMS9", "JumpSMS9", "JumpSMS9.", "JumpSMS9"),
    ("FilterClear", "FilterClear", "FilterClear.", "FilterClear"),
    ("FilterSMS2", "FilterSMS2", "FilterSMS2.", "FilterSMS2"),
    ("FilterSMS3", "FilterSMS3", "FilterSMS3.", "FilterSMS3"),
    ("FilterSMS4", "FilterSMS4", "FilterSMS4.", "FilterSMS4"),
    ("FilterSMS5", "FilterSMS5", "FilterSMS5.", "FilterSMS5"),
    ("FilterSMS6", "FilterSMS6", "FilterSMS6.", "FilterSMS6"),
    ("FilterSMS7", "FilterSMS7", "FilterSMS7.", "FilterSMS7"),
    ("FilterSMS8", "FilterSMS8", "FilterSMS8.", "FilterSMS8"),
    ("FilterSMS9", "FilterSMS9", "FilterSMS9.", "FilterSMS9"),
    ("FirstPage", "FirstPage", "FirstPage.", "FirstPage"),
    ("LastPage", "LastPage", "LastPage.", "LastPage"),

    ("HideSubMenu", "HideSubMenu", "<Depreciated>.", "HideSubMenu"),

    ("ToggleSource", "ToggleSource", "ToggleSource.", "ToggleSource"),
    ("Remove", "Remove", "Remove.", "Remove"),

    ("AudioToggleDigital", "AudioToggleDigital", "AudioToggleDigital.", "AudioToggleDigital"),

    ("OSDLeft", "OSDLeft", "OSDLeft.", "OSDLeft"),
    ("OSDRight", "OSDRight", "OSDRight.", "OSDRight"),
    ("OSDUp", "OSDUp", "OSDUp.", "OSDUp"),
    ("OSDDown", "OSDDown", "OSDDown.", "OSDDown"),
    ("OSDSelect", "OSDSelect", "OSDSelect.", "OSDSelect"),
    ("OSDValuePlus", "OSDValuePlus", "OSDValuePlus.", "OSDValuePlus"),
    ("OSDValueMinus", "OSDValueMinus", "OSDValueMinus.", "OSDValueMinus"),

    ("ToggleWatched", "ToggleWatched", "ToggleWatched.", "ToggleWatched"),
    ("ScanItem", "ScanItem", "ScanItem.", "ScanItem"),

    ("Enter", "Enter", "Enter.", "Enter"),
    ("IncreaseRating", "IncreaseRating", "IncreaseRating.", "IncreaseRating"),
    ("DecreaseRating", "DecreaseRating", "DecreaseRating.", "DecreaseRating"),
    ("ToggleFullScreen", "ToggleFullScreen", "ToggleFullScreen.", "ToggleFullScreen"),
    ("NextScene", "NextScene", "NextScene.", "NextScene"),
    ("PreviousScene", "PreviousScene", "PreviousScene.", "PreviousScene"),
    ("NextLetter", "NextLetter", "NextLetter.", "NextLetter"),
    ("PrevLetter", "PrevLetter", "PrevLetter.", "PrevLetter"),
)),
)

# Remote buttons handled by XBMC.  For a list of all buttons see: http://xbmc.org/wiki/?title=Keymap.xml#Remote_Buttons

REMOTE_BUTTONS = (
(eg.ActionGroup, "Remote", "Remote", None, (
    ("RemoteLeft", "Left", "Move left off a control.", "left"),
    ("RemoteRight", "Right", "Move right off a control.", "right"),
    ("RemoteUp", "Up", "Move up off a control.", "up"),
    ("RemoteDown", "Down", "Move down off a control.", "down"),
    ("RemoteSelect", "Select", "Select a button, or an item from a list of thumb view.", "select"),
    ("RemoteBack", "Back", "", "back"),
    ("RemoteMenu", "Menu", "", "menu"),
    ("RemoteInfo", "Info", "", "info"),
    ("RemoteDisplay", "Display", "", "display"),
    ("RemoteTitle", "Title", "", "title"),
    ("RemotePlay", "Play", "", "play"),
    ("RemotePause", "Pause", "", "pause"),
    ("RemoteReverse", "Reverse", "", "reverse"),
    ("RemoteForward", "Forward", "", "forward"),
    ("RemoteSkipPlus", "Skip +", "", "skipplus"),
    ("RemoteSkipMinus", "Skip -", "", "skipminus"),
    ("RemoteStop", "Stop", "", "stop"),
    ("Remote0", "0", "", "zero"),
    ("Remote1", "1", "", "one"),
    ("Remote2", "2", "", "two"),
    ("Remote3", "3", "", "three"),
    ("Remote4", "4", "", "four"),
    ("Remote5", "5", "", "five"),
    ("Remote6", "6", "", "six"),
    ("Remote7", "7", "", "seven"),
    ("Remote8", "8", "", "eight"),
    ("Remote9", "9", "", "nine"),
    ("RemotePower", "Power", "", "power"),
    ("RemoteMyTV", "My TV", "", "myTV"),
    ("RemoteMyMusic", "My Music", "", "mymusic"),
    ("RemoteMyPictures", "My Pictures", "", "mypictures"),
    ("RemoteMyVideo", "My Video", "", "myvideo"),
    ("RemoteRecord", "Record", "", "record"),
    ("RemoteStart", "Start", "", "start"),
    ("RemoteVolPlus", "Vol +", "", "volumeplus"),
    ("RemoteVolMinus", "Vol -", "", "volumeminus"),
    ("Remotechannelplus", "channelplus", "", "channelplus"),
    ("Remotechannelminus", "channelminus", "", "channelminus"),
    ("Remotepageplus", "pageplus", "", "pageplus"),
    ("Remotepageminus", "pageminus", "", "pageminus"),
    ("RemoteMute", "Mute", "", "mute"),
    ("RemoteRecordedTV", "Recorded TV", "", "recordedtv"),
    ("RemoteLiveTV", "Live TV", "", "livetv"),
    ("RemoteStar", "*", "", "star"),
    ("Remote#", "#", "", "hash"),
    ("RemoteClear", "Clear", "", "clear"),
    ("Remoteguide", "guide", "", "guide"),
    ("Remoteenter", "enter", "", "enter"),
    ("Remotexbox", "xbox", "", "xbox"),
    ("Remoteteletext", "teletext", "", "teletext"),
    ("Remotered", "red", "", "red"),
    ("Remotegreen", "green", "", "green"),
    ("Remoteyellow", "yellow", "", "yellow"),
    ("Remoteblue", "blue", "", "blue"),
    ("Remotesubtitle", "subtitle", "", "subtitle"),
    ("Remotelanguage", "language", "", "language"),
)),
)
# Remote buttons handled by XBMC.  For a list of all buttons see: http://xbmc.org/wiki/?title=Keymap.xml#Gamepad_Buttons

GAMEPAD_BUTTONS = (
(eg.ActionGroup, "Gamepad", "Gamepad", None, (
    ("GamepadA", "a", "a.", "a"),
    ("GamepadB", "b", "b.", "b"),
    ("GamepadX", "x", "x.", "x"),
    ("GamepadY", "y", "y.", "y"),
    ("GamepadWhite", "white", "white.", "white"),
    ("GamepadBlack", "black", "black.", "black"),
    ("GamepadStart", "start", "start.", "start"),
    ("GamepadBack", "back", "back.", "back"),
    ("GamepadLeftThumbButton", "leftthumbbutton", "leftthumbbutton.", "leftthumbbutton"),
    ("GamepadRightThumbButton", "rightthumbbutton", "rightthumbbutton.", "rightthumbbutton"),
    ("GamepadLeftThumbStick", "leftthumbstick", "leftthumbstick.", "leftthumbstick"),
    ("GamepadLeftThumbStickUp", "leftthumbstickup", "leftthumbstickup.", "leftthumbstickup"),
    ("GamepadLeftThumbStickDown", "leftthumbstickdown", "leftthumbstickdown.", "leftthumbstickdown"),
    ("GamepadLeftThumbStickLeft", "leftthumbstickleft", "leftthumbstickleft.", "leftthumbstickleft"),
    ("GamepadLeftThumbStickRight", "leftthumbstickright", "leftthumbstickright.", "leftthumbstickright"),
    ("GamepadRightThumbStick", "rightthumbstick", "rightthumbstick.", "rightthumbstick"),
    ("GamepadRightThumbStickUp", "rightthumbstickup", "rightthumbstickup.", "rightthumbstickup"),
    ("GamepadRightThumbStickDown", "rightthumbstickdown", "rightthumbstickdown.", "rightthumbstickdown"),
    ("GamepadRightThumbStickLeft", "rightthumbstickleft", "rightthumbstickleft.", "rightthumbstickleft"),
    ("GamepadRightThumbStickRight", "rightthumbstickright", "rightthumbstickright.", "rightthumbstickright"),
    ("GamepadLeftTrigger", "lefttrigger", "lefttrigger.", "lefttrigger"),
    ("GamepadRightTrigger", "righttrigger", "righttrigger.", "righttrigger"),
    ("GamepadLeftAnalogTrigger", "leftanalogtrigger", "leftanalogtrigger.", "leftanalogtrigger"),
    ("GamepadRightAnalogTrigger", "rightanalogtrigger", "rightanalogtrigger.", "rightanalogtrigger"),
    ("GamepadDpadLeft", "dpadleft", "dpadleft.", "dpadleft"),
    ("GamepadDpadRight", "dpadright", "dpadright.", "dpadright"),
    ("GamepadDpadUp", "dpadup", "dpadup.", "dpadup"),
    ("GamepadDpadDown", "dpaddown", "dpaddown.", "dpaddown"),
)),
)

# Support functions
def ParseString2(text, filterFunc=None):
	start = 0
	chunks = []
	last = len(text) - 1
	while 1:
		pos = text.find('{{', start)
		if pos < 0:
			break
		if pos == last:
			break
		chunks.append(text[start:pos])
		start = pos + 2
		end = text.find('}}', start)
		if end == -1:
			raise SyntaxError("unmatched bracket")
		word = text[start:end]
		res = None
		if filterFunc:
			res = filterFunc(word)
		if res is None:
			res = eval(word, {}, eg.globals.__dict__)
		chunks.append(unicode(res))
		start = end + 2
	chunks.append(text[start:])
	return "".join(chunks)


class ActionPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.xbmc.send_action(self.value, ACTION_BUTTON)
        except:
            raise self.Exceptions.ProgramNotRunning

# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_throughout_most_of_XBMC
"""
CONFIGURABLE_ACTIONS = (
(eg.ActionGroup, "General", "General", None, (
    ("UpdateLibrary", "UpdateLibrary", "UpdateLibrary", "UpdateLibrary(Video)"),
)),
)
"""
class UpdateLibrary(eg.ActionBase):
    def __call__(self, libraryType="Video", updatePath=""):
        try:
            self.plugin.xbmc.send_action("UpdateLibrary("+libraryType+","+updatePath+")", ACTION_BUTTON)
        except:
            raise self.Exceptions.ProgramNotRunning

    def Configure(self, libraryType="Video", updatePath="" ):
        panel = eg.ConfigPanel()
        textControl1 = wx.TextCtrl(panel, -1, libraryType)
        textControl2 = wx.TextCtrl(panel, -1, updatePath)
        panel.sizer.Add(textControl1, 1, wx.EXPAND)
        panel.sizer.Add(textControl2, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl1.GetValue())
            panel.SetResult(textControl2.GetValue())

class ButtonPrototype(eg.ActionClass):
    def __call__(self):
        try:
            packet = PacketBUTTON(map_name=str("R1"), button_name=str(self.value), repeat=0)
            packet.send(self.plugin.xbmc.sock, self.plugin.xbmc.addr, self.plugin.xbmc.uid)
        except:
            raise self.Exceptions.ProgramNotRunning

class GamepadPrototype(eg.ActionClass):
    def __call__(self):
        try:
            packet = PacketBUTTON(map_name=str("XG"), button_name=str(self.value), repeat=0)
            packet.send(self.plugin.xbmc.sock, self.plugin.xbmc.addr, self.plugin.xbmc.uid)
        except:
            raise self.Exceptions.ProgramNotRunning

class XBMC_HTTP_API:

	def __init__(self):
		self.ip = "127.0.0.1"
		self.port = "80"
		return

	def connect(self, ip=None, port=None):
		if ip: self.ip = ip
		if port: self.port = port
		print 'HTTP API connected'

	def send(self, method, params = ""):
		try:
			responce = urllib.urlopen('http://'+self.ip+':'+self.port+'/xbmcCmds/xbmcHttp?command='+method+'('+urllib.quote(eg.ParseString(params), ':\\')+')').readlines()
		except IOError:
#			print 'HTTP API connection error:'+' http://'+self.ip+':'+self.port+'\n'+method+'('+urllib.quote(eg.ParseString(params), ':\\')+')'
			eg.PrintError('HTTP API connection error:'+' http://'+self.ip+':'+self.port+'\n'+method+'('+urllib.quote(eg.ParseString(params), ':\\')+')')
		else:
			if (''.join(responce).find('<html>') != -1):
				responce2 = {}
				for lines in responce:
					if (lines.find('<html>') != -1): lines = lines[lines.find('<html>')+6:]
					if (lines.find('</html>') != -1): lines = lines[:lines.find('</html>')]
					if (lines.find('<li>') != -1):
						if (lines.find('OK') != -1):
							responce2 = 'OK'
						elif (lines.find('ERROR') != -1):
							responce2 = lines[4:].rstrip('\n').split(':', 1)
						elif (lines.find(':') != -1):
							lines = lines[4:].rstrip('\n').split(':', 1)
							responce2[lines[0]] = lines[1]
						else:
							responce2 = lines[4:].rstrip('\n')
					else:
						if (lines.rstrip('\n') != ''):
							responce2 = lines.rstrip('\n')
				return responce2

	def close(self):
		print 'HTTP API connection closed'

class XBMC_JSON_RPC:

	def __init__(self):
		self.jsoninit = {'jsonrpc':'2.0', 'id':1}
		self.ip = "127.0.0.1"
		self.port = "80"
		return

	def connect(self, ip=None, port=None):
		if ip: self.ip = ip
		if port: self.port = port
		print 'JSON-RPC connected'

	def send(self, method, params = None):
		self.jsoninit['method'] = method
		if params: self.jsoninit['params'] = params
		try:
			responce = urllib.urlopen('http://'+self.ip+':'+self.port+'/jsonrpc', json.dumps(self.jsoninit)).read()
		except IOError:
#			print 'JSON-RPC connection error:'+' http://'+self.ip+':'+self.port+'\n'+json.dumps(self.jsoninit)
			eg.PrintError('JSON-RPC connection error:'+' http://'+self.ip+':'+self.port+'\n'+json.dumps(self.jsoninit))
		else:
#			print responce
			return json.loads(responce)

	def close(self):
		print 'JSON-RPC connection closed'

class GetCurrentlyPlayingFilename(eg.ActionClass):
  description = "Get filename of currently playing file"

  def __call__(self):
		responce = self.plugin.JSON_RPC.send('Player.GetActivePlayers')
		if (responce != None):
			Method = None
			if (responce['result']['picture']): Method = 'Picture'
			elif (responce['result']['video']): Method = 'Video'
			elif (responce['result']['audio']): Method = 'Audio'
			if Method:
				print 'Method: ', Method
				if (Method != 'Picture'):
					responce = self.plugin.JSON_RPC.send(Method+'Playlist.GetItems')
#					print 'eg.result: ', responce['items'][responce['current']]['file']
					return responce['result']['items'][responce['result']['current']]['file']
				else:
					responce = self.plugin.HTTP_API.send('getcurrentlyplaying')
					if responce:
						if (responce['result']['Filename'] == ''):
							print 'No file playing'
						return responce['result']['Filename']
					else:
						raise self.Exceptions.ProgramNotRunning
			else:
				print 'No file playing'
		else:
			responce = self.plugin.HTTP_API.send('getcurrentlyplaying')
			if responce:
				if (responce['Filename'] == ''):
					print 'No file playing'
				return responce['Filename']
			else:
				raise self.Exceptions.ProgramNotRunning

class SendNotification(eg.ActionClass):
	description = "Send a notification to the connected XBMC"

	def __call__(self, title, message):
		try:
			self.plugin.xbmc.send_notification(str(eg.ParseString(title)), str(eg.ParseString(message)))
		except UnicodeEncodeError:
#			print "Error: ascii charecters only."
			eg.PrintError("Error: ascii charecters only.")
		except:
			raise self.Exceptions.ProgramNotRunning
	def Configure(self, title='Hello', message='world'):
		panel = eg.ConfigPanel()
		Title = wx.TextCtrl(panel, -1, value=title)
		Message = wx.TextCtrl(panel, -1, value=message)
		panel.sizer.Add(wx.StaticText(panel, -1, "Title"))
		panel.sizer.Add(Title)
		panel.sizer.Add(wx.StaticText(panel, -1, "Message"))
		panel.sizer.Add(Message)
		while panel.Affirmed():
			panel.SetResult(Title.GetValue(), Message.GetValue())

class HTTPAPI(eg.ActionClass):
	description = "Run any <a href='http://wiki.xbmc.org/index.php?title=Web_Server_HTTP_API'>XBMC HTTP API</a> command."

	def __call__(self, command, param, category, log):
		if param:
			responce = self.plugin.HTTP_API.send(command, param)
		else:
			responce = self.plugin.HTTP_API.send(command)
		if responce != None:
#			print 'Result:\n', responce
			if log:
				import pprint
				print 'Result:'
				pprint.PrettyPrinter(indent=2).pprint(responce)
			return responce
		else:
			raise self.Exceptions.ProgramNotRunning

	def Configure(self, command="GetCurrentPlaylist", param="", category=0, log=True):
		class record:
			pass
		httpapi = record()
		httpapi.Headers = []
		httpapi.Commands = []
		OldCategory = category

		def OnUpdate(event):
			UpdateCommands()
			try:
				with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'httpapi.dat'), 'rb') as f:
					import pickle
					httpapi.Headers, httpapi.Commands = pickle.load(f)
			except IOError:
#				print 'Failed to open: httpapi.dat'
				eg.PrintError('Failed to open: httpapi.dat')
			else:
				category = OldCategory
				HBoxControl.Clear()
				for i in httpapi.Headers:
					HBoxControl.Append(i)
				HBoxControl.SetValue(httpapi.Headers[category])
				UpdateCommandCtrl(HBoxControl.GetSelection())
		def OnCommandChange(event):
			if event.GetEventObject() == comboBoxControl:
				syntax.SetLabel(httpapi.Commands[HBoxControl.GetSelection()][1][event.GetSelection()])
				description.SetLabel(httpapi.Commands[HBoxControl.GetSelection()][2][event.GetSelection()])
				description.Wrap(480)
			else:
				UpdateCommandCtrl(event.GetSelection())
		def UpdateCommandCtrl(Selection):
			value = comboBoxControl.GetValue()
			comboBoxControl.Clear()
			for i in httpapi.Commands[Selection][0]:
				comboBoxControl.Append(i)
			comboBoxControl.SetValue(value)

		def GetText(nodes):
			Text = ''
			for node in nodes.childNodes:
				if node.nodeType == Node.TEXT_NODE: Text += node.data
				else: Text += GetText(node)
			return Text
		def UpdateCommands():
			httpapi.Headers = [];httpapi.Commands = []
			doc = xml.dom.minidom.parse(urllib.urlopen('http://wiki.xbmc.org/index.php?title=Web_Server_HTTP_API'))
			for h3 in doc.getElementsByTagName("h3")[11:-1]:
				for span in h3.getElementsByTagName("span"):
					httpapi.Headers.append(span.childNodes[0].data)
			Header = 0
			for node in doc.getElementsByTagName("table")[3:8]:
				for node2 in node.getElementsByTagName("tr")[1:]:
					httpapi.Commands.append([[],[],[]])
					node3 = node2.getElementsByTagName("td")[0]
					for node4 in node3.childNodes:
						if node4.nodeType == Node.TEXT_NODE:
							Text = node4.data.strip()
							httpapi.Commands[Header][1].append(Text)
							Pos = Text.find('(')
							if (Pos != -1):
								httpapi.Commands[Header][0].append(Text[:Pos])
							else:
								httpapi.Commands[Header][0].append(Text)
						else:
							print '<'+node4.tagName+'>'
					httpapi.Commands[Header][2].append(GetText(node2.getElementsByTagName("td")[1]).strip())
				Header += 1
#			import os
			if not os.path.exists(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2')):
				os.makedirs(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2'))

			with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'httpapi.dat'), 'wb') as f:
				import pickle
				pickle.dump((httpapi.Headers, httpapi.Commands), f, 1)

		import os
		try:
			with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'httpapi.dat'), 'rb') as f:
				import pickle
				httpapi.Headers, httpapi.Commands = pickle.load(f)
		except IOError:
			category = 0
			httpapi.Headers = ['No categorys']
			httpapi.Commands = [[['No commands'],[''],['']]]
		panel = eg.ConfigPanel()
		HBoxControl = wx.ComboBox(panel, -1, value=httpapi.Headers[category], choices=httpapi.Headers, style=wx.CB_READONLY)
		comboBoxControl = wx.ComboBox(panel, -1, value=command, choices=httpapi.Commands[category][0])
		comboBoxControl.SetStringSelection(command)
		textControl1 = wx.TextCtrl(panel, -1, param, size=(500, -1))
		Category = wx.BoxSizer(wx.HORIZONTAL)
		Category.Add(wx.StaticText(panel, -1, "Category"))
		Category.Add(HBoxControl)
		Category.Add(wx.StaticText(panel, -1, "Command"))
		Category.Add(comboBoxControl)
		panel.sizer.Add(wx.StaticText(panel, -1, "Choose or type in a HTTP API command and add parameter(s)"))
		panel.sizer.Add(Category)
		panel.sizer.Add(textControl1)
		panel.sizer.Add(wx.StaticText(panel, -1, "Command syntax:"))
		if (comboBoxControl.GetSelection() != -1):
			syntax = wx.TextCtrl(panel, -1, httpapi.Commands[category][1][comboBoxControl.GetSelection()], (1, 70), size=(500,-1), style=wx.TE_READONLY)
		else:
			syntax = wx.TextCtrl(panel, -1, '', (1, 70), size=(500,-1), style=wx.TE_READONLY)
		panel.sizer.Add(syntax)
		panel.sizer.Add(wx.StaticBox(panel, -1, 'Command description:', size=(500, 150)))
		if (comboBoxControl.GetSelection() != -1):
			description = wx.StaticText(panel, -1, httpapi.Commands[category][2][comboBoxControl.GetSelection()], (5, 105), style=wx.ALIGN_LEFT)
		else:
			description = wx.StaticText(panel, -1, '', (5, 105), style=wx.ALIGN_LEFT)
		description.Wrap(480)
		CheckBox = wx.CheckBox(panel, -1, 'Show result in the log')
		CheckBox.SetValue(log)
		UpdateButton = wx.Button(panel, -1, 'Update')
		UpdateButton.Bind(wx.EVT_BUTTON, OnUpdate)
		Bottom = wx.BoxSizer(wx.HORIZONTAL)
		Bottom.Add(CheckBox)
		Bottom.Add(UpdateButton,0,wx.LEFT,280)
		panel.sizer.Add(Bottom)
		panel.Bind(wx.EVT_COMBOBOX, OnCommandChange)
		while panel.Affirmed():
			panel.SetResult(comboBoxControl.GetValue(), textControl1.GetValue(), HBoxControl.GetSelection(), CheckBox.GetValue())

class JSONRPC(eg.ActionClass):
	description = "Run any <a href='http://wiki.xbmc.org/index.php?title=JSON_RPC'>XBMC JSON-RPC</a> method"

	def __call__(self, method="JSONRPC.Introspect", param="", log=True):
		if param:
			responce = self.plugin.JSON_RPC.send(method, ast.literal_eval(ParseString2(param)))
		else:
			responce = self.plugin.JSON_RPC.send(method)
		if responce != None:
			if responce.has_key('result'):
				if log:
					print 'Result:\n', json.dumps(responce['result'], sort_keys=True, indent=2)
				return responce['result']
			elif responce.has_key('error'):
#				print 'Error:\n', json.dumps(responce['error'], sort_keys=True, indent=2)
				eg.PrintError('Error:\n', json.dumps(responce['error'], sort_keys=True, indent=2))
			else:
#				print 'Got bad JSON-RPC responce', responce
				eg.PrintError('Got bad JSON-RPC responce', responce)
		else:
			raise self.Exceptions.ProgramNotRunning

	def Configure(self, method="JSONRPC.Introspect", param="", log=True):
		import os
		import pickle
		class record:
			Namespaces = ['No namespaces']
			Methods = {'No namespaces':['No methods']}
			Descriptions = {'No namespaces':['']}
		jsonrpc = record()
		def OnUpdate(event):
			UpdateMethods()
			try:
				with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'jsonrpc.dat'), 'rb') as f:
					jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions = pickle.load(f)
			except IOError:
#				print 'Error opening: jsonrpc.dat'
				eg.PrintError('Error opening: jsonrpc.dat')
			else:
				HBoxControl.Clear()
				for i in jsonrpc.Namespaces:
					HBoxControl.Append(i)
				HBoxControl.SetValue(method[:method.find('.')])
				UpdateMethodCtrl(HBoxControl.GetSelection())
		def UpdateMethods():
			jsonrpc.Namespaces = []
			jsonrpc.Methods = {}
			jsonrpc.Descriptions = {}
			OldNamespace = ''
			responce = self.plugin.JSON_RPC.send('JSONRPC.Introspect', json.loads('{"getdescriptions": true, "getpermissions": false}'))
			if responce != None:
				if responce.has_key('result'):
					for method in responce['result']['commands']:
						namespace = method['command'][:method['command'].find('.')]
						if OldNamespace != namespace:
							jsonrpc.Namespaces.append(namespace)
							jsonrpc.Methods[namespace] = []
							jsonrpc.Descriptions[namespace] = []
						OldNamespace = namespace
						jsonrpc.Methods[namespace].append(method['command'][method['command'].find('.')+1:])
						jsonrpc.Descriptions[namespace].append(method['description'])
					if not os.path.exists(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2')):
						os.makedirs(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2'))
					with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'jsonrpc.dat'), 'wb') as f:
						pickle.dump((jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions), f, 1)
					return False
				elif responce.has_key('error'):
#					print 'Error', responce['error']
					eg.PrintError('Error', responce['error'])
					return responce['error']
				else:
#					print 'Got bad JSON-RPC responce', responce
					eg.PrintError('Got bad JSON-RPC responce', responce)
					return False
			else:
				return False
		def UpdateMethodCtrl(Selection):
			comboBoxControl.Clear()
			for i in jsonrpc.Methods[jsonrpc.Namespaces[Selection]]:
				comboBoxControl.Append(i)
			comboBoxControl.SetValue(method[method.find('.')+1:])
		def OnMethodChange(event):
			if event.GetEventObject() == comboBoxControl:
				description.SetLabel(jsonrpc.Descriptions[jsonrpc.Namespaces[HBoxControl.GetSelection()]][event.GetSelection()])
				description.Wrap(480)
			else:
				UpdateMethodCtrl(event.GetSelection())
#				comboBoxControl.Clear()
#				for i in jsonrpc.Methods[jsonrpc.Namespaces[event.GetSelection()]]:
#					comboBoxControl.Append(i)

		panel = eg.ConfigPanel()
		try:
			with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'jsonrpc.dat'), 'rb') as f:
				jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions = pickle.load(f)
		except IOError:
#			print 'Error opening: jsonrpc.dat'
			eg.PrintError('Error opening: jsonrpc.dat')
		HBoxControl = wx.ComboBox(panel, -1, value=method[:method.find('.')], choices=jsonrpc.Namespaces, style=wx.CB_READONLY)
		comboBoxControl = wx.ComboBox(panel, -1, value=method[method.find('.')+1:], choices=jsonrpc.Methods[jsonrpc.Namespaces[HBoxControl.GetSelection()]] , style=wx.CB_READONLY)
		textControl2 = wx.TextCtrl(panel, -1, param, size=(500, -1))
		Category = wx.BoxSizer(wx.HORIZONTAL)
		Category.Add(wx.StaticText(panel, -1, "Namespace"))
		Category.Add(HBoxControl)
		Category.Add(wx.StaticText(panel, -1, "Method"))
		Category.Add(comboBoxControl)
		panel.sizer.Add(wx.StaticText(panel, -1, "Choose a JSON-RPC Method and add any parameter(s)"))
		panel.sizer.Add(Category)
		panel.sizer.Add(textControl2)
		panel.sizer.Add(wx.StaticBox(panel, -1, 'Method description:', size=(500, 150)))
		if (comboBoxControl.GetSelection() != -1):
			description = wx.StaticText(panel, -1, jsonrpc.Descriptions[jsonrpc.Namespaces[HBoxControl.GetSelection()]][comboBoxControl.GetSelection()], (5, 70), style=wx.ALIGN_LEFT)
		else:
			description = wx.StaticText(panel, -1, '', (5, 70), style=wx.ALIGN_LEFT)
		description.Wrap(480)
		Bottom = wx.BoxSizer(wx.HORIZONTAL)
		CheckBox = wx.CheckBox(panel, -1, 'Show result in the log')
		CheckBox.SetValue(log)
		Bottom.Add(CheckBox)
		UpdateButton = wx.Button(panel, -1, 'Update')
		UpdateButton.Bind(wx.EVT_BUTTON, OnUpdate)
		Bottom.Add(UpdateButton,0,wx.LEFT,280)
		panel.sizer.Add(Bottom)
		panel.Bind(wx.EVT_COMBOBOX, OnMethodChange)
		while panel.Affirmed():
			panel.SetResult(HBoxControl.GetValue()+'.'+comboBoxControl.GetValue(), textControl2.GetValue(), CheckBox.GetValue())

#class StopRepeating(eg.ActionClass):
#    name = "Stop Repeating"
#    description = "Stops a button repeating."

#    def __call__(self):
#        try:
#            self.plugin.xbmc.release_button()
#        except:
#            raise self.Exceptions.ProgramNotRunning


# And now we define the actual plugin:

class XBMC2(eg.PluginClass):
    def __init__(self):
#        self.ip = "127.0.0.1"
#        self.port = port
        ButtonsGroup = self.AddGroup("Buttons", "Button actions to send to XBMC")
        ButtonsGroup.AddActionsFromList(REMOTE_BUTTONS, ButtonPrototype)
        ButtonsGroup.AddActionsFromList(GAMEPAD_BUTTONS, GamepadPrototype)
        ActionsGroup = self.AddGroup("Actions", "Actions to send to XBMC")
        ActionsGroup.AddActionsFromList(GENERAL_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(MEDIA_PLAYING_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(PLAYLIST_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(FULLSCREEN_VIDEO_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(SLIDESHOW_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(CALIBRATION_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(FILEMANAGER_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(ON_SCREEN_KEYBOARD_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(VISUALISATION_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(SHUTDOWN_ACTIONS, ActionPrototype)
        ActionsGroup.AddActionsFromList(UNCATEGORIZED_ACTIONS, ActionPrototype)
#        ConfigurableGroup = ActionsGroup.AddGroup("Configurable", "Actions that have configurable settings")
#        ConfigurableGroup.AddAction(UpdateLibrary)
        self.AddActionsFromList(WINDOWS, ActionPrototype)

        TestGroup = self.AddGroup("Experimental", "Experimental")
        TestGroup.AddAction(JSONRPC)
        TestGroup.AddAction(HTTPAPI)
        TestGroup.AddAction(GetCurrentlyPlayingFilename)
        TestGroup.AddAction(SendNotification)

#        self.AddAction(StopRepeating)
        self.xbmc = XBMCClient("EventGhost")
        self.JSON_RPC = XBMC_JSON_RPC()
        self.HTTP_API = XBMC_HTTP_API()

    def Configure(self, ip="127.0.0.1", port="80"):
#    def Configure(self, ip="127.0.0.1", IPs = ['127.0.0.1', '192.168.0.100']):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, ip)
        textControl2 = wx.TextCtrl(panel, -1, port)
#        textControl = panel.ComboBox(
#            ip,
#            IPs,
#            style=wx.CB_DROPDOWN,
#            validator=eg.DigitOnlyValidator()
#        )
        panel.sizer.Add(wx.StaticText(panel, -1, "IP address of XBMC ( 127.0.0.1 is this computer )"))
#        panel.sizer.Add(textControl, 1, wx.EXPAND)
        panel.sizer.Add(textControl)
        panel.sizer.Add(textControl2)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue(), textControl2.GetValue())

    def __start__(self, ip='127.0.0.1', port='80'):
        self.ip = ip
        self.port = port
        try:
            self.xbmc.connect(ip=ip)
#            self.xbmc.connect()
#            self.xbmc.connect(ip="192.168.0.100")
#            self.stopThreadEvent = Event()
#            thread = Thread(target=self.ThreadWorker, args=(self.stopThreadEvent,))
#            thread.start()
        except:
            raise self.Exceptions.ProgramNotRunning
        self.JSON_RPC.connect(ip=ip, port=port)
        self.HTTP_API.connect(ip=ip, port=port)

    def __stop__(self):
        try:
#            self.stopThreadEvent.set()
            self.xbmc.close()
        except:
            pass

    def __close__(self):
        pass

#    def ThreadWorker(self, stopThreadEvent):
#        while not stopThreadEvent.isSet():
#            self.TriggerEvent("MyTimerEvent")
#            stopThreadEvent.wait(10.0)
