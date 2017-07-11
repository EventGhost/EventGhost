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
import urllib2
import json
import ast
import xml.dom.minidom
from xml.dom.minidom import Node
import socket
import base64
from urlparse import urlparse
import os
import pickle

from threading import Event, Thread

# expose some information about the plugin through an eg.PluginInfo subclass

eg.RegisterPlugin(
    name = "XBMC2",
    author = "Joni Boren",
    version = "0.6.35",
    kind = "program",
    guid = "{8C8B850C-773F-4583-AAD9-A568262B7933}",
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

"""
'http://www.xbmc.org/'
'http://wiki.xbmc.org/index.php?title=Web_Server_HTTP_API'
http://xbmc.org/wiki/?title=Window_IDs
http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_throughout_most_of_XBMC
'http://wiki.xbmc.org/?title=Action_IDs'
'https://raw.githubusercontent.com/xbmc/xbmc/master/xbmc/input/ButtonTranslator.cpp'
"""
# from threading import Event, Thread

# Windows availible in XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Window_IDs http://kodi.wiki/view/Window_IDs
"""
"""

WINDOWS = (
(eg.ActionGroup, "Windows", "Windows", None, (
    ("MyMovies", "Show Movies Screen", "Show Movies screen.", "Activatewindow(MyVideoLibrary,movietitles,return)"),
    ("MyTVShows", "Show TV Shows Screen", "Show TV Shows screen.", "Activatewindow(MyVideoLibrary,tvshowtitles,return)"),
    ("ShutdownMenu", "Show Shutdown Menu", "Show the shutdown Menu.", "Activatewindow(ShutdownMenu)"),
    ("Home", "Home", "WINDOW_HOME", "Activatewindow(Home)"),
    ("Programs", "Programs", "WINDOW_PROGRAMS", "Activatewindow(Programs)"),
    ("Pictures", "Pictures", "WINDOW_PICTURES", "Activatewindow(Pictures)"),
    ("Files", "Files", "WINDOW_FILES\nbackward compat", "Activatewindow(Files)"),
    ("Settings", "Settings", "WINDOW_SETTINGS_MENU", "Activatewindow(Settings)"),
    ("Music", "Music", "WINDOW_MUSIC", "Activatewindow(Music)"),
    ("Musicfiles", "Musicfiles", "WINDOW_MUSIC_FILES", "Activatewindow(Musicfiles)"),
    ("Musiclibrary", "Musiclibrary", "WINDOW_MUSIC_NAV", "Activatewindow(Musiclibrary)"),
    ("Musicplaylist", "Musicplaylist", "WINDOW_MUSIC_PLAYLIST", "Activatewindow(Musicplaylist)"),
    ("Musicplaylisteditor", "Musicplaylisteditor", "WINDOW_MUSIC_PLAYLIST_EDITOR", "Activatewindow(Musicplaylisteditor)"),
    ("Musicinformation", "Musicinformation", "WINDOW_DIALOG_MUSIC_INFO", "Activatewindow(Musicinformation)"),
    ("Video", "Video", "WINDOW_VIDEOS", "Activatewindow(Video)"),
    ("Videofiles", "Videofiles", "WINDOW_VIDEO_FILES", "Activatewindow(Videofiles)"),
    ("Videolibrary", "Videolibrary", "WINDOW_VIDEO_NAV", "Activatewindow(Videolibrary)"),
    ("Videoplaylist", "Videoplaylist", "WINDOW_VIDEO_PLAYLIST", "Activatewindow(Videoplaylist)"),
    ("Systeminfo", "Systeminfo", "WINDOW_SYSTEM_INFORMATION", "Activatewindow(Systeminfo)"),
    ("Guicalibration", "Guicalibration", "WINDOW_SCREEN_CALIBRATION\nbackward compat", "Activatewindow(Guicalibration)"),
    ("Screencalibration", "Screencalibration", "WINDOW_SCREEN_CALIBRATION", "Activatewindow(Screencalibration)"),
    ("Picturessettings", "Picturessettings", "WINDOW_SETTINGS_MYPICTURES", "Activatewindow(Picturessettings)"),
    ("Programssettings", "Programssettings", "WINDOW_SETTINGS_MYPROGRAMS", "Activatewindow(Programssettings)"),
    ("Weathersettings", "Weathersettings", "WINDOW_SETTINGS_MYWEATHER", "Activatewindow(Weathersettings)"),
    ("Musicsettings", "Musicsettings", "WINDOW_SETTINGS_MYMUSIC", "Activatewindow(Musicsettings)"),
    ("Systemsettings", "Systemsettings", "WINDOW_SETTINGS_SYSTEM", "Activatewindow(Systemsettings)"),
    ("Videossettings", "Videossettings", "WINDOW_SETTINGS_MYVIDEOS", "Activatewindow(Videossettings)"),
    ("Networksettings", "Networksettings", "WINDOW_SETTINGS_NETWORK", "Activatewindow(Networksettings)"),
    ("Appearancesettings", "Appearancesettings", "WINDOW_SETTINGS_APPEARANCE", "Activatewindow(Appearancesettings)"),
    ("Scripts", "Scripts", "WINDOW_PROGRAMS\nbackward compat", "Activatewindow(Scripts)"),
    ("Gamesaves", "Gamesaves", "Gamesaves", "Activatewindow(Gamesaves)"),
    ("Profiles", "Profiles", "WINDOW_SETTINGS_PROFILES", "Activatewindow(Profiles)"),
    ("Virtualkeyboard", "Virtualkeyboard", "WINDOW_DIALOG_KEYBOARD", "Activatewindow(Virtualkeyboard)"),
    ("Volumebar", "Volumebar", "WINDOW_DIALOG_VOLUME_BAR", "Activatewindow(Volumebar)"),
    ("Favourites", "Favourites", "WINDOW_DIALOG_FAVOURITES", "Activatewindow(Favourites)"),
    ("Musicosd", "Musicosd", "WINDOW_DIALOG_MUSIC_OSD", "Activatewindow(Musicosd)"),
    ("Visualisationsettings", "Visualisationsettings", "WINDOW_DIALOG_ADDON_SETTINGS\nbackward compat", "Activatewindow(Visualisationsettings)"),
    ("Visualisationpresetlist", "Visualisationpresetlist", "WINDOW_DIALOG_VIS_PRESET_LIST", "Activatewindow(Visualisationpresetlist)"),
    ("Osdvideosettings", "Osdvideosettings", "WINDOW_DIALOG_VIDEO_OSD_SETTINGS", "Activatewindow(Osdvideosettings)"),
    ("Osdaudiosettings", "Osdaudiosettings", "WINDOW_DIALOG_AUDIO_OSD_SETTINGS", "Activatewindow(Osdaudiosettings)"),
    ("Videobookmarks", "Videobookmarks", "WINDOW_DIALOG_VIDEO_BOOKMARKS", "Activatewindow(Videobookmarks)"),
    ("Profilesettings", "Profilesettings", "WINDOW_DIALOG_PROFILE_SETTINGS", "Activatewindow(Profilesettings)"),
    ("Locksettings", "Locksettings", "WINDOW_DIALOG_LOCK_SETTINGS", "Activatewindow(Locksettings)"),
    ("Contentsettings", "Contentsettings", "WINDOW_DIALOG_CONTENT_SETTINGS", "Activatewindow(Contentsettings)"),
    ("Networksetup", "Networksetup", "WINDOW_DIALOG_NETWORK_SETUP", "Activatewindow(Networksetup)"),
    ("Smartplaylisteditor", "Smartplaylisteditor", "WINDOW_DIALOG_SMART_PLAYLIST_EDITOR", "Activatewindow(Smartplaylisteditor)"),
    ("Smartplaylistrule", "Smartplaylistrule", "WINDOW_DIALOG_SMART_PLAYLIST_RULE", "Activatewindow(Smartplaylistrule)"),
    ("Movieinformation", "Movieinformation", "WINDOW_DIALOG_VIDEO_INFO", "Activatewindow(Movieinformation)"),
    ("Scriptsdebuginfo", "Scriptsdebuginfo", "Scriptsdebuginfo", "Activatewindow(Scriptsdebuginfo)"),
    ("Fullscreenvideo", "Fullscreenvideo", "WINDOW_FULLSCREEN_VIDEO", "Activatewindow(Fullscreenvideo)"),
    ("Visualisation", "Visualisation", "WINDOW_VISUALISATION", "Activatewindow(Visualisation)"),
    ("Slideshow", "Slideshow", "WINDOW_SLIDESHOW", "Activatewindow(Slideshow)"),
    ("Filestackingdialog", "Filestackingdialog", "WINDOW_DIALOG_FILESTACKING", "Activatewindow(Filestackingdialog)"),
    ("Weather", "Weather", "WINDOW_WEATHER", "Activatewindow(Weather)"),
    ("Screensaver", "Screensaver", "WINDOW_SCREENSAVER", "Activatewindow(Screensaver)"),
    ("Videoosd", "Videoosd", "WINDOW_DIALOG_VIDEO_OSD", "Activatewindow(Videoosd)"),
    ("Videomenu", "Videomenu", "WINDOW_VIDEO_MENU", "Activatewindow(Videomenu)"),
    ("Filebrowser", "Filebrowser", "WINDOW_DIALOG_FILE_BROWSER", "Activatewindow(Filebrowser)"),
    ("Startup", "Startup", "WINDOW_STARTUP_ANIM", "Activatewindow(Startup)"),
    ("Startwindow", "Startwindow", "WINDOW_START", "Activatewindow(Startwindow)"),
    ("Loginscreen", "Loginscreen", "WINDOW_LOGIN_SCREEN", "Activatewindow(Loginscreen)"),
    ("Musicoverlay", "Musicoverlay", "WINDOW_DIALOG_MUSIC_OVERLAY", "Activatewindow(Musicoverlay)"),
    ("Videooverlay", "Videooverlay", "WINDOW_DIALOG_VIDEO_OVERLAY", "Activatewindow(Videooverlay)"),
    ("Pictureinfo", "Pictureinfo", "WINDOW_DIALOG_PICTURE_INFO", "Activatewindow(Pictureinfo)"),
    ("Pluginsettings", "Pluginsettings", "Pluginsettings", "Activatewindow(Pluginsettings)"),
    ("Fullscreeninfo", "Fullscreeninfo", "WINDOW_DIALOG_FULLSCREEN_INFO", "Activatewindow(Fullscreeninfo)"),
    ("PlayerControls", "Player Controls", "WINDOW_DIALOG_PLAYER_CONTROLS", "Activatewindow(Playercontrols)"),
)),
)
# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_throughout_most_of_XBMC http://kodi.wiki/view/Action_IDs#General_actions_available_throughout_most_of_XBMC

GENERAL_ACTIONS = (
(eg.ActionGroup, "General", "General", None, (
    ("Left", "Left", "Move left off a control.", "left"),
    ("Right", "Right", "Move right off a control.", "right"),
    ("Up", "Up", "Move up off a control.", "up"),
    ("Down", "Down", "Move down off a control.", "down"),
    ("PageUp", "PageUp", "Scroll up on page in a list, thumb, or text view.", "pageup"),
    ("PageDown", "PageDown", "Scroll down on page in a list, thumb, or text view.", "pagedown"),
    ("Select", "Select", "Select a button, or an item from a list of thumb view.", "select"),
    ("Highlight", "Highlight", "Highlight an item in a list or thumb view.", "highlight"),
    ('Parentfolder', 'Parentfolder', 'Go up a folder to the parent folder.', 'parentfolder'),
    ('Back', 'Back', '', 'back'),
    ("ParentDir", "ParentDir", "Go up a folder to the parent folder.\n// backward compatibility", "parentdir"),
    ("PreviousMenu", "PreviousMenu", "Go back to the previous menu screen.", "previousmenu"),
    ("Info", "Info", "Show the information about the currently highlighted item, or currently playing item.", "info"),
    ("Screenshot", "Screenshot", "Take a screenshot of the current screen.", "screenshot"),
    ("PowerOff", "PowerOff", "Shutdown and power off.", "poweroff"),
    ("VolumeUp", "VolumeUp", "Increase the volume of playback.", "volumeup"),
    ("VolumeDown", "VolumeDown", "Decrease the volume of playback.", "volumedown"),
    ("Mute", "Mute", "Mute the volume.", "mute"),
    ("ContextMenu", "ContextMenu", "Pops up a contextual menu", "contextmenu"),
    ("ScrollUp", "ScrollUp", "Variable speed scroll up for analog keys (stick or triggers)", "scrollup"),
    ("ScrollDown", "ScrollDown", "Variable speed scroll down for analog keys (stick or triggers)", "scrolldown"),
    ("Close", "Close", "Used to close a dialog", "close"),
    ("Number0", "Number0", "Used to input the number 0", "number0"),
    ("Number1", "Number1", "Used to input the number 1", "number1"),
    ("Number2", "Number2", "Used to input the number 2", "number2"),
    ("Number3", "Number3", "Used to input the number 3", "number3"),
    ("Number4", "Number4", "Used to input the number 4", "number4"),
    ("Number5", "Number5", "Used to input the number 5", "number5"),
    ("Number6", "Number6", "Used to input the number 6", "number6"),
    ("Number7", "Number7", "Used to input the number 7", "number7"),
    ("Number8", "Number8", "Used to input the number 8", "number8"),
    ("Number9", "Number9", "Used to input the number 9", "number9"),
)),
)

# actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#General_actions_available_while_video_or_music_are_playing http://kodi.wiki/view/Action_IDs#General_actions_available_while_video_or_music_are_playing

MEDIA_PLAYING_ACTIONS = (
(eg.ActionGroup, "MediaPlaying", "Media playing", None, (
    ("Play", "Play", "Play the selected item (or folder of items), or unpause a paused item.", "play"),
    ("Pause", "Pause", "Pause the currently playing item.", "pause"),
    ("Stop", "Stop", "Stop the currently playing item.", "stop"),
    ("FastForward", "FastForward", "Toggle the fastforward speed between normal play, 2x, 4x, 8x, 16x, and 32x.", "fastforward"),
    ("Rewind", "Rewind", "Toggle the rewind speed between normal play, 2x, 4x, 8x, 16x, and 32x.", "rewind"),
    ("SkipNext", "SkipNext", "Skip to the next item in a playlist or scene in a video.", "skipnext"),
    ("SkipPrevious", "SkipPrevious", "Skip to the previous item in a playlist or scene in a video.", "skipprevious"),
    ("FullScreen", "FullScreen", "Toggles fullscreen modes (either visualisation or video playback)", "fullscreen"),
    ("CodecInfo", "CodecInfo", "Show codec information about the currently playing item (during video or visualisation playback)", "codecinfo"),
    ("AnalogSeekForward", "AnalogSeekForward", "Variable speed seeking for analog keys (stick or triggers)", "analogseekforward"),
    ("AnalogSeekBack", "AnalogSeekBack", "Variable speed seeking for analog keys (stick or triggers)", "analogseekback"),
    ("AnalogFastForward", "AnalogFastForward", "Variable speed fast forward for analog keys (stick or triggers)", "analogfastforward"),
    ("AnalogRewind", "AnalogRewind", "Variable speed rewind for analog keys (stick or triggers)", "analogrewind"),
    ("PartyMode", "Party Mode", "Party mode.", "playercontrol(partymode)"),
    ("Random", "Random", "Toggles random playback", "playercontrol(Random,Notify)"),
    ("Repeat", "Repeat", "Cycles through the repeat modes", "playercontrol(Repeat,Notify)"),
    ("UpdateVideoLibrary", "Update Video Library", "Update the video library.", "updatelibrary(video)"),
    ("UpdateMusicLibrary", "Update Music Library", "Update the music library.", "updatelibrary(music)"),
    ("IncreaseRating", "IncreaseRating", "Unused.", "increaserating"),
    ("DecreaseRating", "DecreaseRating", "Unused .", "decreaserating"),
    ("EjectTray", "EjectTray", "Close or open the DVD tray", "EjectTray"),
    ("Record", "Record", "Starts recording.", "record"),
    ("PlayDVD", "PlayDVD", "Plays the inserted CD or DVD media from the DVD-ROM Drive!", "PlayDVD"),
    ("LastFMLove", "LastFM.Love", "Add the current playing last.fm radio track to the last.fm loved tracks", "LastFM.Love"),
    ("LastFMBan", "LastFM.Ban", "Ban the current playing last.fm radio track", "LastFM.Ban"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_only_in_Music_and_Videos_windows_only http://kodi.wiki/view/Action_IDs#Actions_available_only_in_Music_and_Videos_windows_only

PLAYLIST_ACTIONS = (
(eg.ActionGroup, "Playlist", "Playlist", None, (
    ("Playlist", "Playlist", "Toggle to playlist view from My Music or My Videos", "playlist"),
    ("Queue", "Queue", "Queue the item to the current playlist", "queue"),
    ("MoveItemUp", "MoveItemUp", "Used to rearrange playlists", "moveitemup"),
    ("MoveItemDown", "MoveItemDown", "Used to rearrange playlists", "moveitemdown"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_only_in_Full_Screen_Video http://kodi.wiki/view/Action_IDs#Actions_available_only_in_Full_Screen_Video

FULLSCREEN_VIDEO_ACTIONS = (
(eg.ActionGroup, "FullscreenVideo", "FullScreen Video", None, (
    ("StepForward", "StepForward", "Step forward 1% in the movie.", "stepforward"),
    ("StepBack", "StepBack", "Step back 1% in the movie.", "stepback"),
    ("BigStepForward", "BigStepForward", "Step forward 10% in the movie.", "bigstepforward"),
    ("BigStepBack", "BigStepBack", "Step back 10% in the movie.", "bigstepback"),
    ("SmallStepBack", "SmallStepBack", "Step back 7 seconds in the current video.", "smallstepback"),
    ("OSD", "OSD", "Toggles the OSD while playing an item.", "osd"),
    ("AspectRatio", "AspectRatio", "Toggle through the various aspect ratio modes (Normal is the preferred option).", "aspectratio"),
    ("ShowSubtitles", "ShowSubtitles", "Toggles whether subtitles are shown or not.", "showsubtitles"),
    ("NextSubtitle", "NextSubtitle", "Change to the next subtitle language, if there is more than one.", "nextsubtitle"),
    ('Subtitledelay', 'SubtitleDelay', 'Show subtitle delay slider', 'subtitledelay'),
    ("SubtitleDelayMinus", "SubtitleDelayMinus", "Decrease the delay amount of subtitles (use if subtitles are displaying too late)", "subtitledelayminus"),
    ("SubtitleDelayPlus", "SubtitleDelayPlus", "Increase the delay amount of subtitles (use if subtitles are displaying too early)", "subtitledelayplus"),
    ('Audiodelay', 'AudioDelay', 'Show audio delay slider', 'audiodelay'),
    ("AudioDelayMinus", "AudioDelayMinus", "Decrease the delay amount of audio (use if audio is being heard too early)", "audiodelayminus"),
    ("AudioDelayPlus", "AudioDelayPlus", "Increase the delay amount of audio (use if audio is being heard too late)", "audiodelayplus"),
    ("AudioNextLanguage", "AudioNextLanguage", "Change to the next audio track in a video with multiple audio tracks.", "audionextlanguage"),
    ("mplayerosd", "MplayerOSD", "Show Mplayer's OSD", "mplayerosd"),
    ("ShowTime", "ShowTime", "Used to show the current play time in music + video playback", "showtime"),
    ("ShowVideoMenu", "ShowVideoMenu", "Go to the DVD Video menu when playing a DVD.", "showvideomenu"),
    ('Increasepar', 'IncreasePAR', 'Used in video fullscreen to increase the pixel aspect ratio (stretch).', 'increasepar'),
    ('Decreasepar', 'DecreasePAR', 'Used in video fullscreen to decrease the pixel aspect ratio (stretch).', 'decreasepar'),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_during_a_picture_slideshow http://kodi.wiki/view/Action_IDs#Actions_available_during_a_picture_slideshow

SLIDESHOW_ACTIONS = (
(eg.ActionGroup, "PictureSlideshow", "Picture slideshow", None, (
    ("NextPicture", "NextPicture", "Move to the next picture in a slideshow.", "nextpicture"),
    ("PreviousPicture", "PreviousPicture", "Move to the previous picture in a slideshow.", "previouspicture"),
    ("ZoomOut", "ZoomOut", "Used in picture, slideshow or video fullscreen to zoom out of the current image/video.", "zoomout"),
    ("ZoomIn", "ZoomIn", "Used in picture, slideshow or video fullscreen to zoom in to the current image/video.", "zoomin"),
    ("ZoomNormal", "ZoomNormal", "Normal (fullscreen) viewing in My Pictures", "zoomnormal"),
    ("ZoomLevel1", "ZoomLevel1", "Zoom to 120% in My Pictures", "zoomlevel1"),
    ("ZoomLevel2", "ZoomLevel2", "Zoom to 150% in My Pictures", "zoomlevel2"),
    ("ZoomLevel3", "ZoomLevel3", "Zoom to 200% in My Pictures", "zoomlevel3"),
    ("ZoomLevel4", "ZoomLevel4", "Zoom to 280% in My Pictures", "zoomlevel4"),
    ("ZoomLevel5", "ZoomLevel5", "Zoom to 400% in My Pictures", "zoomlevel5"),
    ("ZoomLevel6", "ZoomLevel6", "Zoom to 600% in My Pictures", "zoomlevel6"),
    ("ZoomLevel7", "ZoomLevel7", "Zoom to 900% in My Pictures", "zoomlevel7"),
    ("ZoomLevel8", "ZoomLevel8", "Zoom to 1350% in My Pictures", "zoomlevel8"),
    ("ZoomLevel9", "ZoomLevel9", "Zoom to 2000% in My Pictures", "zoomlevel9"),
    ("AnalogMove", "AnalogMove", "Move in the calibration screens, and while zoomed in My Pictures.", "analogmove"),
    ("Rotate", "Rotate", "Rotate a picture in My Pictures", "rotate"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_screen_calibration http://kodi.wiki/view/Action_IDs#Actions_available_in_screen_calibration

CALIBRATION_ACTIONS = (
(eg.ActionGroup, "ScreenCalibration", "Screen calibration", None, (
    ("NextCalibration", "NextCalibration", "Used in Video + GUI calibration", "nextcalibration"),
    ("ResetCalibration", "ResetCalibration", "Used in Video + GUI calibration", "resetcalibration"),
    ("AnalogMove", "AnalogMove", "Move in the calibration screens, and while zoomed in My Pictures.", "analogmove"),
    ("NextResolution", "NextResolution", "Used in Video calibration", "nextresolution"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_the_File_Manager http://kodi.wiki/view/Action_IDs#Actions_available_in_the_File_Manager

FILEMANAGER_ACTIONS = (
(eg.ActionGroup, "FileManager", "File Manager", None, (
    ("Delete", "Delete", "Used in My Files to delete a file.", "delete"),
    ("Copy", "Copy", "Used in My Files to copy a file.", "copy"),
    ("Move", "Move", "Used in My Files to move a file.", "move"),
    ("Rename", "Rename", "Used in My Files to rename a file.", "rename"),
)),
)
# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_in_the_on-screen_keyboard http://kodi.wiki/view/Action_IDs#Actions_available_in_the_on-screen_keyboard

ON_SCREEN_KEYBOARD_ACTIONS = (
(eg.ActionGroup, "On-screenKeyboard", "On-screen keyboard", None, (
    ("BackSpace", "BackSpace", "Used in the virtual keyboards to delete one letter.", "backspace"),
    ("Shift", "Shift", "Used in Virtual Keyboard to switch to upper or lower case letters", "shift"),
    ("Symbols", "Symbols", "Used in Virtual Keyboard to switch to or from symbols mode", "symbols"),
    ("CursorLeft", "CursorLeft", "Used in Virtual Keyboard to move the current cursor point to the left", "cursorleft"),
    ("CursorRight", "CursorRight", "Used in Virtual Keyboard to move the current cursor point to the right", "cursorright"),
)),
)

# Actions handled by XBMC.  For a list of all actions see: http://xbmc.org/wiki/?title=Action_IDs#Actions_available_during_a_music_visualisation http://kodi.wiki/view/Action_IDs#Actions_available_during_a_music_visualisation

VISUALISATION_ACTIONS = (
(eg.ActionGroup, "MusicVisualisation", "Music visualisation", None, (
    ("OSD", "OSD", "Toggles the OSD while playing an item.", "osd"),
    ("ShowPreset", "ShowPreset", "Shows the current visualisation preset (milkdrop/spectrum)", "showpreset"),
    ("PresetList", "PresetList", "Pops up the visualisation preset list (milkdrop/spectrum)", "presetlist"),
    ("NextPreset", "NextPreset", "Next visualisation preset", "nextpreset"),
    ("PreviousPreset", "PreviousPreset", "Previous visualisation preset", "previouspreset"),
    ("LockPreset", "LockPreset", "Lock the current visualisation preset", "lockpreset"),
    ("RandomPreset", "RandomPreset", "Switch to a new random preset", "randompreset"),
    ("increasevisrating", "IncreaseVisRating", "", "increasevisrating"),
    ("decreasevisrating", "DecreaseVisRating", "", "decreasevisrating"),
)),
)

SHUTDOWN_ACTIONS = (
(eg.ActionGroup, "ShutdownRelated", "Shutdown related", None, (
    ("Quit", "Quit", "Quit XBMC", "Quit"),
    ("RestartApp", "RestartApp", "Restart XBMC", "RestartApp"),
    ("Reset", "Reset Computer", "Reset the computer.", "reset"),
    ("Shutdown", "Shutdown Computer", "Trigger default Shutdown action defined in System Settings, Default Quit on Windows.", "shutdown"),
    ("Powerdown", "Powerdown", "Powerdown system", "Powerdown"),
    ("Suspend", "Suspend", "Suspends the system", "Suspend"),
    ("Hibernate", "Hibernate", "Hibernates the system", "Hibernate"),
    ("Reboot", "Reboot Computer", "Cold reboots the system (power cycle).", "reboot"),
    ("Restart", "Restart Computer", "Cold reboots the system (power cycle).", "restart"),
)),
)

UNCATEGORIZED_ACTIONS = (
(eg.ActionGroup, "UncategorizedActions", "Uncategorized actions", None, (
    ("JumpSMS2", "JumpSMS2", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms2"),
    ("JumpSMS3", "JumpSMS3", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms3"),
    ("JumpSMS4", "JumpSMS4", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms4"),
    ("JumpSMS5", "JumpSMS5", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms5"),
    ("JumpSMS6", "JumpSMS6", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms6"),
    ("JumpSMS7", "JumpSMS7", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms7"),
    ("JumpSMS8", "JumpSMS8", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms8"),
    ("JumpSMS9", "JumpSMS9", "Jump through a list using SMS-style input (eg press 2 twice to jump to the B's.)", "jumpsms9"),
    ("FilterClear", "FilterClear", "", "filterclear"),
    ("FilterSMS2", "FilterSMS2", "Filter a list in music or videos using SMS-style input.", "filtersms2"),
    ("FilterSMS3", "FilterSMS3", "Filter a list in music or videos using SMS-style input.", "filtersms3"),
    ("FilterSMS4", "FilterSMS4", "Filter a list in music or videos using SMS-style input.", "filtersms4"),
    ("FilterSMS5", "FilterSMS5", "Filter a list in music or videos using SMS-style input.", "filtersms5"),
    ("FilterSMS6", "FilterSMS6", "Filter a list in music or videos using SMS-style input.", "filtersms6"),
    ("FilterSMS7", "FilterSMS7", "Filter a list in music or videos using SMS-style input.", "filtersms7"),
    ("FilterSMS8", "FilterSMS8", "Filter a list in music or videos using SMS-style input.", "filtersms8"),
    ("FilterSMS9", "FilterSMS9", "Filter a list in music or videos using SMS-style input.", "filtersms9"),
    ("FirstPage", "FirstPage", "", "firstpage"),
    ("LastPage", "LastPage", "", "lastpage"),

    ("HideSubMenu", "HideSubMenu", "<depreciated>", "hidesubmenu"),

    ("ToggleSource", "ToggleSource", "", "togglesource"),
    ("Remove", "Remove", "", "remove"),

    ("AudioToggleDigital", "AudioToggleDigital", "", "audiotoggledigital"),

    ("OSDLeft", "OSDLeft", "", "osdleft"),
    ("OSDRight", "OSDRight", "", "osdright"),
    ("OSDUp", "OSDUp", "", "osdup"),
    ("OSDDown", "OSDDown", "", "osddown"),
    ("OSDSelect", "OSDSelect", "", "osdselect"),
    ("OSDValuePlus", "OSDValuePlus", "", "osdvalueplus"),
    ("OSDValueMinus", "OSDValueMinus", "", "osdvalueminus"),

    ("ToggleWatched", "ToggleWatched", "Toggles watched/unwatched status for Videos", "togglewatched"),
    ("ScanItem", "ScanItem", "", "scanitem"),

    ("Enter", "Enter", "", "enter"),
    ("IncreaseRating", "IncreaseRating", "Unused", "increaserating"),
    ("DecreaseRating", "DecreaseRating", "Unused", "decreaserating"),
    ("ToggleFullScreen", "ToggleFullScreen", "", "togglefullscreen"),
    ("NextScene", "NextScene", "", "nextscene"),
    ("PreviousScene", "PreviousScene", "", "previousscene"),
    ("NextLetter", "NextLetter", "Move to the next letter in a list or thumb panel.  Note that SHIFT-B on the keyboard will take you to the B's.", "nextletter"),
    ("PrevLetter", "PrevLetter", "Move to the previous letter in a list or thumb panel.  Note that SHIFT-Z on the keyboard will take you to the Z's.", "prevletter"),

    ('Verticalshiftup', 'VerticalShiftUp', '', 'verticalshiftup'),
    ('Verticalshiftdown', 'VerticalShiftDown', '', 'verticalshiftdown'),
    ('Playpause', 'PlayPause', '', 'playpause'),
    ('Reloadkeymaps', 'ReloadKeymaps', '', 'reloadkeymaps'),
    ('Guiprofile', 'GuiProfile', '', 'guiprofile'),
    ('Red', 'Red', '', 'red'),
    ('Green', 'Green', '', 'green'),
    ('Yellow', 'Yellow', '', 'yellow'),
    ('Blue', 'Blue', '', 'blue'),

    ('Subtitleshiftup', 'Subtitleshiftup', '', 'subtitleshiftup'),
    ('Subtitleshiftdown', 'Subtitleshiftdown', '', 'subtitleshiftdown'),
    ('Subtitlealign', 'Subtitlealign', '', 'subtitlealign'),
    ('Help', 'Help', 'This help message', 'Help'),
    ('Minimize', 'Minimize', 'Minimize XBMC', 'Minimize'),
    ('Mastermode', 'Mastermode', 'Control master mode', 'Mastermode'),
    ('TakeScreenshot', 'TakeScreenshot', 'Takes a Screenshot', 'TakeScreenshot'),
    ('ReloadSkin', 'ReloadSkin', "Reload XBMC's skin", 'ReloadSkin'),
    ('UnloadSkin', 'UnloadSkin', "Unload XBMC's skin", 'UnloadSkin'),
    ('RefreshRSS', 'RefreshRSS', 'Reload RSS feeds from RSSFeeds.xml', 'RefreshRSS'),
    ('Playlist.Clear', 'Playlist.Clear', 'Clear the current playlist', 'Playlist.Clear'),
    ('RipCD', 'RipCD', 'Rip the currently inserted audio CD', 'RipCD'),
    ('Skin.ResetSettings', 'Skin.ResetSettings', 'Resets all skin settings', 'Skin.ResetSettings'),
    ('System.LogOff', 'System.LogOff', 'Log off current user', 'System.LogOff'),
    ('Container.Refresh', 'Container.Refresh', 'Refresh current listing', 'Container.Refresh'),
    ('Container.Update', 'Container.Update', 'Update current listing. Send Container.Update(path,replace) to reset the path history', 'Container.Update'),
    ('Container.NextViewMode', 'Container.NextViewMode', 'Move to the next view type (and refresh the listing)', 'Container.NextViewMode'),
    ('Container.PreviousViewMode', 'Container.PreviousViewMode', 'Move to the previous view type (and refresh the listing)', 'Container.PreviousViewMode'),
    ('Container.NextSortMethod', 'Container.NextSortMethod', 'Change to the next sort method', 'Container.NextSortMethod'),
    ('Container.PreviousSortMethod', 'Container.PreviousSortMethod', 'Change to the previous sort method', 'Container.PreviousSortMethod'),
    ('Container.SortDirection', 'Container.SortDirection', 'Toggle the sort direction', 'Container.SortDirection'),
    ('UpdateAddonRepos', 'UpdateAddonRepos', 'Check add-on repositories for updates', 'UpdateAddonRepos'),
    ('UpdateLocalAddons', 'UpdateLocalAddons', 'Check for local add-on changes', 'UpdateLocalAddons'),
    ('ToggleDPMS', 'ToggleDPMS', 'Toggle DPMS mode manually', 'ToggleDPMS'),
    ('Weather.Refresh', 'Weather.Refresh', 'Force weather data refresh', 'Weather.Refresh'),
    ('Weather.LocationNext', 'Weather.LocationNext', 'Switch to next weather location', 'Weather.LocationNext'),
    ('Weather.LocationPrevious', 'Weather.LocationPrevious', 'Switch to previous weather location', 'Weather.LocationPrevious'),
    ('LIRC.Stop', 'LIRC.Stop', 'Removes XBMC as LIRC client', 'LIRC.Stop'),
    ('LIRC.Start', 'LIRC.Start', 'Adds XBMC as LIRC client', 'LIRC.Start'),
    ('LCD.Suspend', 'LCD.Suspend', 'Suspends LCDproc', 'LCD.Suspend'),
    ('LCD.Resume', 'LCD.Resume', 'Resumes LCDproc', 'LCD.Resume'),
)),
)

# Remote buttons handled by XBMC.  For a list of all buttons see: http://wiki.xbmc.org/?title=Keymap.xml#Remote_Section http://kodi.wiki/view/Keymap.xml#Remotes

REMOTE_BUTTONS = (
(eg.ActionGroup, "Remote", "Remote", None, (
    ("RemoteLeft", "Left", "", "left"),
    ("RemoteRight", "Right", "", "right"),
    ("RemoteUp", "Up", "", "up"),
    ("RemoteDown", "Down", "", "down"),
    ("RemoteSelect", "Select", "", "select"),
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
    ("RemoteMyTV", "My TV", "", "mytv"),
    ("RemoteMyMusic", "My Music", "", "mymusic"),
    ("RemoteMyPictures", "My Pictures", "", "mypictures"),
    ("RemoteMyVideo", "My Video", "", "myvideo"),
    ("RemoteRecord", "Record", "", "record"),
    ("RemoteStart", "Start", "", "start"),
    ("RemoteVolPlus", "Vol +", "", "volumeplus"),
    ("RemoteVolMinus", "Vol -", "", "volumeminus"),
    ("Remotechannelplus", "CH +", "", "channelplus"),
    ("Remotechannelminus", "CH -", "", "channelminus"),
    ("Remotepageplus", "PG +", "", "pageplus"),
    ("Remotepageminus", "PG -", "", "pageminus"),
    ("RemoteMute", "Mute", "", "mute"),
    ("RemoteRecordedTV", "Recorded TV", "", "recordedtv"),
    ("RemoteLiveTV", "Live TV", "", "livetv"),
    ("RemoteStar", "*", "", "star"),
    ("Remote#", "#", "", "hash"),
    ("RemoteClear", "Clear", "", "clear"),
    ("Remoteguide", "Guide", "", "guide"),
    ("Remoteenter", "Enter", "", "enter"),
    ("Remotexbox", "Xbox", "", "xbox"),
    ("Remoteteletext", "Teletext", "", "teletext"),
    ("Remotered", "Red", "", "red"),
    ("Remotegreen", "Green", "", "green"),
    ("Remoteyellow", "Yellow", "", "yellow"),
    ("Remoteblue", "Blue", "", "blue"),
    ("Remotesubtitle", "Subtitle", "", "subtitle"),
    ("Remotelanguage", "Language", "", "language"),
)),
)
# Remote buttons handled by XBMC.  For a list of all buttons see: http://wiki.xbmc.org/?title=Keymap.xml#Gamepad_Section http://kodi.wiki/view/Keymap.xml#Gamepads

GAMEPAD_BUTTONS = (
(eg.ActionGroup, "Gamepad", "Gamepad", None, (
    ("GamepadA", "A", "", "a"),
    ("GamepadB", "B", "", "b"),
    ("GamepadX", "X", "", "x"),
    ("GamepadY", "Y", "", "y"),
    ("GamepadWhite", "White", "", "white"),
    ("GamepadBlack", "Black", "", "black"),
    ("GamepadStart", "Start", "", "start"),
    ("GamepadBack", "Back", "", "back"),
    ("GamepadLeftThumbButton", "LeftThumbButton", "", "leftthumbbutton"),
    ("GamepadRightThumbButton", "RightThumbButton", "", "rightthumbbutton"),
    ("GamepadLeftThumbStick", "LeftThumbStick", "", "leftthumbstick"),
    ("GamepadLeftThumbStickUp", "LeftThumbStickUp", "", "leftthumbstickup"),
    ("GamepadLeftThumbStickDown", "LeftThumbStickDown", "", "leftthumbstickdown"),
    ("GamepadLeftThumbStickLeft", "LeftThumbStickLeft", "", "leftthumbstickleft"),
    ("GamepadLeftThumbStickRight", "LeftThumbStickRight", "", "leftthumbstickright"),
    ("GamepadRightThumbStick", "RightThumbStick", "", "rightthumbstick"),
    ("GamepadRightThumbStickUp", "RightThumbStickUp", "", "rightthumbstickup"),
    ("GamepadRightThumbStickDown", "RightThumbStickDown", "", "rightthumbstickdown"),
    ("GamepadRightThumbStickLeft", "RightThumbStickLeft", "", "rightthumbstickleft"),
    ("GamepadRightThumbStickRight", "RightThumbStickRight", "", "rightthumbstickright"),
    ("GamepadLeftTrigger", "LeftTrigger", "", "lefttrigger"),
    ("GamepadRightTrigger", "RightTrigger", "", "righttrigger"),
    ("GamepadLeftAnalogTrigger", "LeftAnalogTrigger", "", "leftanalogtrigger"),
    ("GamepadRightAnalogTrigger", "RightAnalogTrigger", "", "rightanalogtrigger"),
    ("GamepadDpadLeft", "DpadLeft", "", "dpadleft"),
    ("GamepadDpadRight", "DpadRight", "", "dpadright"),
    ("GamepadDpadUp", "DpadUp", "", "dpadup"),
    ("GamepadDpadDown", "DpadDown", "", "dpaddown"),
)),
)

# Remote buttons handled by XBMC.  For a list of all buttons see: http://wiki.xbmc.org/?title=Keymap.xml#Custom_Joystick_Configuration http://kodi.wiki/view/Keymap.xml#Custom_Joystick_Configuration

APPLEREMOTE_BUTTONS = (
(eg.ActionGroup, "AppleRemote", "AppleRemote", None, (
	("AppleRemote1", "plus", "AppleRemote", 1),
	("AppleRemote2", "minus", "AppleRemote", 2),
	("AppleRemote3", "left", "AppleRemote", 3),
	("AppleRemote4", "right", "AppleRemote", 4),
	("AppleRemote5", "center", "AppleRemote", 5),
	("AppleRemote6", "menu", "AppleRemote", 6),
	("AppleRemote7", "hold center", "AppleRemote", 7),
	("AppleRemote8", "hold menu", "AppleRemote", 8),

	#<!-- old buttons for ATV1 <2.2, used on OSX  -->
	("AppleRemote9", "hold left", "AppleRemote:\nold buttons for ATV1 <2.2, used on OSX", 9),
	("AppleRemote10", "hold right", "AppleRemote:\nold buttons for ATV1 <2.2, used on OSX", 10),

	#<!-- new aluminium remote buttons  -->
	("AppleRemote12", "play/pause", "AppleRemote:\nnew aluminium remote buttons", 12),

	#<!-- Additional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen-->
	("AppleRemote13", "pageup", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 13),
	("AppleRemote14", "pagedown", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 14),
	("AppleRemote15", "pause", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 15),
	("AppleRemote16", "play2", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 16),
	("AppleRemote17", "stop", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 17),
	("AppleRemote18", "fast fwd", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 18),
	("AppleRemote19", "rewind", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 19),
	("AppleRemote20", "skip fwd", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 20),
	("AppleRemote21", "skip back", "AppleRemote:\nAdditional buttons via Harmony Apple TV remote profile - these are also the learned buttons on Apple TV 2gen", 21),

	#<!-- Learned remote buttons (ATV1 >2.3) -->
	("AppleRemote70", "Play", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 70),
	("AppleRemote71", "Pause", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 71),
	("AppleRemote72", "Stop", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 72),
	("AppleRemote73", "Previous", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 73),
	("AppleRemote74", "Next", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 74),
	("AppleRemote75", "Rewind", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 75),
	("AppleRemote76", "Forward", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 76),
	("AppleRemote77", "Return", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 77),
	("AppleRemote78", "Enter", "AppleRemote:\nLearned remote buttons (ATV1 >2.3)", 78),

	#<!-- few gestures from Apple's iPhone Remote (ATV1 > 2.3 ?) -->
	("AppleRemote80", "SwipeLeft", "AppleRemote:\nfew gestures from Apple's iPhone Remote (ATV1 > 2.3 ?)", 80),
	("AppleRemote81", "SwipeRight", "AppleRemote:\nfew gestures from Apple's iPhone Remote (ATV1 > 2.3 ?)", 81),
	("AppleRemote82", "SwipeUp", "AppleRemote:\nfew gestures from Apple's iPhone Remote (ATV1 > 2.3 ?)", 82),
	("AppleRemote83", "SwipeDown", "AppleRemote:\nfew gestures from Apple's iPhone Remote (ATV1 > 2.3 ?)", 83),

	("AppleRemote85", "FlickLeft", "AppleRemote:\nfew gestures from Apple's iPhone Remote (ATV1 > 2.3 ?)", 85),
	("AppleRemote86", "FlickRight", "AppleRemote:\nfew gestures from Apple's iPhone Remote (ATV1 > 2.3 ?)", 86),
	("AppleRemote87", "FlickUp", "AppleRemote:\nfew gestures from Apple's iPhone Remote (ATV1 > 2.3 ?)", 87),
	("AppleRemote88", "FlickDown", "AppleRemote:\nfew gestures from Apple's iPhone Remote (ATV1 > 2.3 ?)", 88),
)),
)

# Keyboard keys handled by XBMC.  For a list of all keys see: http://wiki.xbmc.org/index.php?title=List_of_XBMC_keynames http://kodi.wiki/view/List_of_XBMC_keynames

KEYBOARD_KEYS = (
(eg.ActionGroup, "Keyboard", "Keyboard", None, (
    ("KeyboardBackspace", "Backspace", "", "backspace"),
    ("KeyboardEnter", "Enter", "", "enter"),
    ("KeyboardTab", "Tab", "", "tab"),
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
        parameterString = libraryType
        if not updatePath == "":
					parameterString += "," + updatePath
        print repr(parameterString)
        try:
            #self.plugin.xbmc.send_action("UpdateLibrary("+libraryType+","+updatePath+")", ACTION_BUTTON)
            #self.plugin.xbmc.send_action("UpdateLibrary(video,\\\\MYTHTV\\Media\\Multimedia\\Movies\\Anime TV\\Mikagura Gakuen Kumikyoku)", ACTION_BUTTON)
            self.plugin.xbmc.send_action("UpdateLibrary(" + str(parameterString) + ")")
        except:
            raise self.Exceptions.ProgramNotRunning

    def Configure(self, libraryType="Video", updatePath="" ):
        panel = eg.ConfigPanel()
        textControl1 = wx.TextCtrl(panel, -1, libraryType)
        textControl2 = wx.TextCtrl(panel, -1, updatePath)
        panel.sizer.Add(textControl1, 1, wx.EXPAND)
        panel.sizer.Add(textControl2, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl1.GetValue(), textControl2.GetValue())

class BuiltInFunctions(eg.ActionBase):
	def __call__(self, Function="Help", Parameters=""):
		try:
			self.plugin.xbmc.send_action(Function + "(" + str(eg.ParseString(Parameters)) + ")")
		except:
			raise self.Exceptions.ProgramNotRunning

	def Configure(self, Function="Help", Parameters=""):
		import os, contextlib, pickle
		BuiltInFunctionList = {}
		def UpdateFunctions():
			def GetFunctions():
				try:
					with contextlib.closing(urllib2.urlopen(urllib2.Request('https://raw.githubusercontent.com/xbmc/xbmc/Isengard/xbmc/interfaces/Builtins.cpp'))) as Builtinscpp:
						Builtinslines = Builtinscpp.read().splitlines(False)
				except (urllib2.HTTPError, urllib2.URLError):
					eg.PrintError('XBMC2: Error: Can\'t connect to "https://raw.githubusercontent.com/xbmc/xbmc/Isengard/xbmc/interfaces/Builtins.cpp" to update "BuiltInFunctions".')
					raise
				else:
					Builtinslist = Builtinslines[Builtinslines.index("const BUILT_IN commands[] = {") + 1:Builtinslines.index("};")]

					FunctionList = []
					for Function in Builtinslist:
						try:
							FunctionList.append((Function.strip(' {},').split(',')[0].strip('" '), True if Function.strip(' {},').split(',')[1].strip('" ') == 'true' else False, Function.strip(' {},').split(',')[2].strip('" ')))
						except IndexError:
							pass
					return FunctionList
			def GetSyntax():
				def XMLText(Node):
					text = ''
					#print "Info:", Node.nodeValue, Node.nodeName
					try:
						for n in Node.childNodes:
							text += n.nodeValue if n.nodeName == '#text' else XMLText(n)
						#print "Text:", text
					except:
						print "Try:", Node.nodeValue, Node.nodeName

					return text

				URL = 'http://kodi.wiki/view/List_of_built-in_functions'
				UserAgent = 'XBMC2 EventGhost plugin'
				hdr = {'User-Agent': UserAgent}

				request = urllib2.Request(URL, headers=hdr)
				try:
					w = urllib2.urlopen(request)
				except (urllib2.HTTPError, urllib2.URLError):
					eg.PrintError('XBMC2: Error: Can\'t connect to "http://kodi.wiki/view/List_of_built-in_functions" to update "BuiltInFunctions".')
					raise
				else:
					Page2 = w.read()

					ActionDict = {}
					for table in xml.dom.minidom.parseString(Page2).getElementsByTagName("table")[1:2]:
						for tr in table.getElementsByTagName("tr"):
							for code in tr.getElementsByTagName("code")[0:1]:
								ActionDict[XMLText(code).strip().split('(')[0]] = (XMLText(code).strip(), XMLText(code.parentNode.nextSibling.nextSibling).strip())
								#print XMLText(code).strip().split('(')[0]
					return ActionDict

			try:
				FunctionsList = GetFunctions()
			except (urllib2.HTTPError, urllib2.URLError):
				BuiltInFunctionList['Help'] = {'Syntax': 'Help', 'Description': "", 'Parameters': False}
			else:
				try:
					SyntaxList = GetSyntax()
				except (urllib2.HTTPError, urllib2.URLError):
					SyntaxList = {}
				for Function, Parameters, Description in sorted(FunctionsList):
					try:
						SyntaxList[Function]
						Syntax = SyntaxList[Function][0]
						Description = SyntaxList[Function][1]
					except KeyError:
						Syntax = Function
					BuiltInFunctionList[Function] = {'Syntax': Syntax, 'Description': Description, 'Parameters': Parameters}

				"""
				if not os.path.exists(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2')):
					os.makedirs(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2'))
				with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'BuiltInFunctions.dat'), 'wb') as f:
					pickle.dump(BuiltInFunctionList, f, 1)
					print 'XBMC2: Builtin functions updated.'
				"""
				try:
					writeData('BuiltInFunctions.dat', BuiltInFunctionList)
				except IOError:
					pass
				else:
					print 'XBMC2: Builtin functions updated.'

		"""
		def loadfile():
			try:
				with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'BuiltInFunctions.dat'), 'rb') as f:
					return pickle.load(f)
			except IOError:
				print 'XBMC2: Warning: Failed to open: BuiltInFunctions.dat'
				raise
		"""
		def OnUpdate(event):
			UpdateFunctions()

		def OnFunctionChange(event):
			if event.GetEventObject() == panel.combo_box_function:
				if not BuiltInFunctionList[panel.combo_box_function.GetValue()]['Parameters']:
					panel.text_ctrl_parameters.Disable()
				else:
					panel.text_ctrl_parameters.Enable()
				panel.text_ctrl_syntax.SetValue(BuiltInFunctionList[panel.combo_box_function.GetValue()]['Syntax'])
				panel.label_description.SetLabel(BuiltInFunctionList[panel.combo_box_function.GetValue()]['Description'])

		def initPanel(self):
			self.combo_box_function = wx.ComboBox(self, wx.ID_ANY, value=Function, choices=sorted(BuiltInFunctionList.keys()), style=wx.CB_READONLY)
			self.sizer_function_staticbox = wx.StaticBox(self, wx.ID_ANY, "Function")
			self.label_left = wx.StaticText(self, wx.ID_ANY, "(")
			self.text_ctrl_parameters = wx.TextCtrl(self, wx.ID_ANY, Parameters)
			self.label_right = wx.StaticText(self, wx.ID_ANY, ")")
			self.sizer_parameter_staticbox = wx.StaticBox(self, wx.ID_ANY, "Parameter(s)")
			self.text_ctrl_syntax = wx.TextCtrl(self, wx.ID_ANY, BuiltInFunctionList[Function]['Syntax'], style=wx.TE_READONLY | wx.BORDER_NONE)
			self.sizer_syntax_staticbox = wx.StaticBox(self, wx.ID_ANY, "Syntax")
			self.label_description = wx.TextCtrl(self, wx.ID_ANY, BuiltInFunctionList[Function]['Description'], style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE | wx.TE_RICH)
			self.sizer_description_staticbox = wx.StaticBox(self, wx.ID_ANY, "Description")
			self.button_update = wx.Button(self, wx.ID_ANY, "Update")
			if not BuiltInFunctionList[Function]['Parameters']:
				self.text_ctrl_parameters.Disable()

			setPanelProperties(self)
			doPanelLayout(self)

			self.Bind(wx.EVT_COMBOBOX, OnFunctionChange, self.combo_box_function)
			self.button_update.Bind(wx.EVT_BUTTON, OnUpdate)

		def setPanelProperties(self):
			self.label_left.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
			self.label_right.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
			self.button_update.SetToolTipString("Update \"BuiltInFunctions\" form Kodis website.")

		def doPanelLayout(self):
			sizer_main = wx.BoxSizer(wx.VERTICAL)
			self.sizer_description_staticbox.Lower()
			sizer_description = wx.StaticBoxSizer(self.sizer_description_staticbox, wx.HORIZONTAL)
			self.sizer_syntax_staticbox.Lower()
			sizer_syntax = wx.StaticBoxSizer(self.sizer_syntax_staticbox, wx.HORIZONTAL)
			sizer_functionparameter = wx.BoxSizer(wx.HORIZONTAL)
			self.sizer_parameter_staticbox.Lower()
			sizer_parameter = wx.StaticBoxSizer(self.sizer_parameter_staticbox, wx.HORIZONTAL)
			self.sizer_function_staticbox.Lower()
			sizer_function = wx.StaticBoxSizer(self.sizer_function_staticbox, wx.HORIZONTAL)
			sizer_function.Add(self.combo_box_function, 0, 0, 0)
			sizer_functionparameter.Add(sizer_function, 0, 0, 0)
			sizer_parameter.Add(self.label_left, 0, 0, 0)
			sizer_parameter.Add(self.text_ctrl_parameters, 1, wx.EXPAND, 0)
			sizer_parameter.Add(self.label_right, 0, 0, 0)
			sizer_functionparameter.Add(sizer_parameter, 1, 0, 0)
			sizer_main.Add(sizer_functionparameter, 0, wx.EXPAND, 0)
			sizer_syntax.Add(self.text_ctrl_syntax, 1, 0, 0)
			sizer_main.Add(sizer_syntax, 0, wx.EXPAND, 0)
			sizer_description.Add(self.label_description, 1, wx.EXPAND, 0)
			sizer_main.Add(sizer_description, 1, wx.EXPAND, 0)
			sizer_main.Add(self.button_update, 0, wx.ALIGN_RIGHT, 0)
			self.sizer.Add(sizer_main, 1, wx.EXPAND, 0)

		panel = eg.ConfigPanel()
		try:
			#BuiltInFunctionList = loadfile()
			BuiltInFunctionList = readData('BuiltInFunctions.dat')
		except IOError:
			UpdateFunctions()

		initPanel(panel)

		while panel.Affirmed():
			panel.SetResult(str(panel.combo_box_function.GetValue()), str(panel.text_ctrl_parameters.GetValue()))

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

class AppleRemotePrototype(eg.ActionClass):
    def __call__(self):
        try:
            packet = PacketBUTTON(map_name=str("JS0:AppleRemote"), code=self.value, repeat=0)
            packet.send(self.plugin.xbmc.sock, self.plugin.xbmc.addr, self.plugin.xbmc.uid)
        except:
            raise self.Exceptions.ProgramNotRunning

class KeyboardPrototype(eg.ActionClass):
    def __call__(self):
        try:
            packet = PacketBUTTON(map_name=str("KB"), button_name=str(self.value), repeat=0)
            packet.send(self.plugin.xbmc.sock, self.plugin.xbmc.addr, self.plugin.xbmc.uid)
        except:
            raise self.Exceptions.ProgramNotRunning

class XBMC_HTTP_API:

	def __init__(self):
		pass

	def connect(self, ip="127.0.0.1", port="80", username='', password=''):
		self.ip = ip
		self.port = port
		self.base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
		print 'HTTP API connected'

	def send(self, method, params = ""):
		request = urllib2.Request('http://'+self.ip+':'+self.port+'/xbmcCmds/xbmcHttp?command='+method+'('+urllib2.quote(eg.ParseString(params), ':\\')+')')
		request.add_header("Authorization", "Basic %s" % self.base64string)
		try:
			responce = urllib2.urlopen(request).readlines()
		except IOError:
			#eg.PrintError('HTTP API connection error:'+' http://'+self.ip+':'+self.port+'\n'+method+'('+urllib2.quote(eg.ParseString(params), ':\\')+')')
			raise
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

	def connect(self, ip="127.0.0.1", port=80, username='', password=''):
		self.ip = ip
		self.port = str(port)
		self.base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
		print 'JSON-RPC connected'

	def send(self, method, params = None, wait=True):
		self.jsoninit['method'] = method
		if params:
			self.jsoninit['params'] = params
		else:
			if self.jsoninit.has_key('params'):
				del self.jsoninit['params']
		request = urllib2.Request('http://'+self.ip+':'+self.port+'/jsonrpc',json.dumps(self.jsoninit))
		request.add_header("Authorization", "Basic %s" % self.base64string)
		request.add_header('Content-Type', 'application/json')
		try:
			#responce = urllib2.urlopen(request, timeout=5).read()
			responce = urllib2.urlopen(request, timeout=(60 if wait else 1)).read()
		except urllib2.HTTPError as e:
			#print 'HTTPError', e.args
			#if hasattr(e, 'reason'): # <--
			#		print 'We failed to reach a server.'
			#		print 'Reason: ', e.reason
			#if hasattr(e, 'code'): # <--
			#		print 'The server couldn\'t fulfill the request.'
			#		import BaseHTTPServer
			#		print 'Error code: ', e.code, BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code]
			raise
		except urllib2.URLError as e:
			#print 'URLError', e.reason, e.args
			if type(e.reason) == socket.timeout:
				return {'noresult': None}
			else:
				#print 'URLError', e.reason, e.args
				raise
      #URLError: <urlopen error timed out>
      #URLError timed out (timeout('timed out',),)
      #URLError <class 'socket.timeout'> (timeout('timed out',),)
		except:
			#eg.PrintError('JSON-RPC connect error: ')
			#import sys, traceback
			#traceback.print_exc()
			raise
		#except IOError:
		#eg.PrintError('JSON-RPC connection error:'+' http://'+self.ip+':'+self.port+'\n'+json.dumps(self.jsoninit))
		else:
			try:
				#print responce
				return json.loads(responce)
			except ValueError as e:
				#eg.PrintError("Server responded but didn't provide valid JSON data: ")
				#import sys, traceback
				#traceback.print_exc()
				#eg.PrintError("Error data: " + str(e)+': "'+str(responce)+'"')
				raise

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
			"""
			try:
				with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'httpapi.dat'), 'rb') as f:
					import pickle
					httpapi.Headers, httpapi.Commands = pickle.load(f)
			except IOError:
#				print 'Failed to open: httpapi.dat'
				eg.PrintError('Failed to open: httpapi.dat')
			"""
			try:
				httpapi.Headers, httpapi.Commands = readData('httpapi.dat')
			except IOError:
				pass
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

			try:
				doc = xml.dom.minidom.parseString(urllib2.urlopen(urllib2.Request('http://kodi.wiki/view/Web_Server_HTTP_API')).read())
			except (urllib2.HTTPError, urllib2.URLError):
				print "Connect error"
			else:
				for h3 in doc.getElementsByTagName("h3")[10:-1]:
					for span in h3.getElementsByTagName("span"):
						httpapi.Headers.append(span.childNodes[0].data)
				Header = 0
				for node in doc.getElementsByTagName("table")[3:9]:
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
				try:
					writeData('httpapi.dat', (httpapi.Headers, httpapi.Commands))
				except IOError:
					pass

		import os
		try:
			httpapi.Headers, httpapi.Commands = readData('httpapi.dat')
		except IOError:
			UpdateCommands()
			#category = 0
			#httpapi.Headers = ['No categorys']
			#httpapi.Commands = [[['No commands'],[''],['']]]
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

def readData(filename):
	try:
		with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', filename), 'rb') as f:
			print "Reading:", filename
			return pickle.load(f)
	except IOError:
		#eg.PrintError('XBMC2: Error opening: ' + filename)
		raise

def writeData(filename, data):
	if not os.path.exists(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2')):
		os.makedirs(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2'))
	try:
		with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', filename), 'wb') as f:
			print "Writing:", filename
			pickle.dump(data, f, 1)
	except IOError:
		eg.PrintError('XBMC2: Error writing to:', filename)
		raise

class JSONRPC(eg.ActionClass):
	description = "Run any <a href='http://wiki.xbmc.org/index.php?title=JSON_RPC'>XBMC JSON-RPC</a> method"

	def __call__(self, method="JSONRPC.Introspect", param="", log=True, wait=True):
		if param:
			responce = self.plugin.JSON_RPC.send(method, ast.literal_eval(ParseString2(param)), wait=wait)
		else:
			responce = self.plugin.JSON_RPC.send(method, wait=wait)
		if responce != None:
			if responce.has_key('noresult'):
				return
			elif responce.has_key('result'):
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

	def Configure(self, method="JSONRPC.Introspect", param="", log=True, wait=True):
		class record:
			Namespaces = ['No namespaces']
			Methods = {'No namespaces':['No methods']}
			Descriptions = {'No namespaces':['']}
		jsonrpc = record()
		def OnUpdate(event):
			UpdateMethods()
			try:
				jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions = readData('jsonrpc.dat')
			except IOError:
				pass
			else:
				HBoxControl.Clear()
				for i in jsonrpc.Namespaces:
					HBoxControl.Append(i)
				HBoxControl.SetValue(method[:method.find('.')])
				UpdateMethodCtrl(HBoxControl.GetSelection())

		def UpdateMethods():
			responce = self.plugin.JSON_RPC.send('JSONRPC.Version')
			if responce:
				jsonrpc.Namespaces = []
				jsonrpc.Methods = {}
				jsonrpc.Descriptions = {}
				if responce['result']['version'] > 2:
					responce = self.plugin.JSON_RPC.send('JSONRPC.Introspect', json.loads('{"filterbytransport": false}'))
					if responce != None:
						if responce.has_key('result'):
							for method in responce['result']['methods']:
								namespace = method[:method.find('.')]
								if namespace not in jsonrpc.Namespaces:
									jsonrpc.Namespaces.append(namespace)
									jsonrpc.Methods[namespace] = []
									jsonrpc.Descriptions[namespace] = []
								jsonrpc.Methods[namespace].append(method[method.find('.')+1:])
								if responce['result']['methods'][method].has_key('description'):
									jsonrpc.Descriptions[namespace].append(responce['result']['methods'][method]['description'])
								else:
									jsonrpc.Descriptions[namespace].append('')
							try:
								writeData('jsonrpc.dat', (jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions))
							except IOError:
								pass
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
				else:
					responce = self.plugin.JSON_RPC.send('JSONRPC.Introspect', json.loads('{"getdescriptions": true, "getpermissions": false}'))
					if responce != None:
						if responce.has_key('result'):
							for method in responce['result']['commands']:
								namespace = method['command'][:method['command'].find('.')]
								if namespace not in jsonrpc.Namespaces:
									jsonrpc.Namespaces.append(namespace)
									jsonrpc.Methods[namespace] = []
									jsonrpc.Descriptions[namespace] = []
								jsonrpc.Methods[namespace].append(method['command'][method['command'].find('.')+1:])
								jsonrpc.Descriptions[namespace].append(method['description'])
							try:
								writeData('jsonrpc.dat', (jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions))
							except IOError:
								pass
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
			jsonrpc.Namespaces, jsonrpc.Methods, jsonrpc.Descriptions = readData('jsonrpc.dat')
		except IOError:
			UpdateMethods()
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
		CheckBox2 = wx.CheckBox(panel, -1, "Wait for result.(Timeout 60s)")
		CheckBox.SetValue(log)
		CheckBox2.SetValue(wait)
		Bottom.Add(CheckBox2)
		Bottom.Add(CheckBox)
		UpdateButton = wx.Button(panel, -1, 'Update')
		UpdateButton.Bind(wx.EVT_BUTTON, OnUpdate)
		Bottom.Add((0, 0), 1, wx.EXPAND)
		#Bottom.Add(UpdateButton,0,wx.LEFT,280)
		Bottom.Add(UpdateButton, flag= wx.ALIGN_RIGHT)
		panel.sizer.Add(Bottom, 1, flag=wx.EXPAND)
		panel.Bind(wx.EVT_COMBOBOX, OnMethodChange)
		while panel.Affirmed():
			try:
				jsonTemp = json.loads(textControl2.GetValue())
			except:
				pass
			else:
				if 'jsonrpc' in jsonTemp:
					namespaceTemp, methodTemp = jsonTemp['method'].split('.')
					HBoxControl.SetValue(namespaceTemp)
					comboBoxControl.Clear()
					for i in jsonrpc.Methods[jsonrpc.Namespaces[HBoxControl.GetSelection()]]:
						comboBoxControl.Append(i)
					comboBoxControl.SetValue(methodTemp)
					try:
						textControl2.SetValue(json.dumps(jsonTemp['params']))
					except:
						textControl2.SetValue('')

			panel.SetResult(HBoxControl.GetValue()+'.'+comboBoxControl.GetValue(), textControl2.GetValue(), CheckBox.GetValue(), CheckBox2.GetValue())

#class StopRepeating(eg.ActionClass):
#    name = "Stop Repeating"
#    description = "Stops a button repeating."

#    def __call__(self):
#        try:
#            self.plugin.xbmc.release_button()
#        except:
#            raise self.Exceptions.ProgramNotRunning

def ssdpSearch():
	import socket
	from urlparse import urlparse
	import os
	def Headers(data):
		headers = {}
		for line in data.splitlines():
			if not line.split(':', 1)[0]:
				continue
			try:
				headers[line.split(':', 1)[0].upper()] = line.split(':', 1)[1]
			except:
				headers['Start-line'] = line.split(':', 1)[0]
		return headers

	MCAST_GRP = '239.255.255.250'
	MCAST_PORT = 1900
	LIB_ID = 'upnp'
	DISCOVERY_MSG = ('M-SEARCH * HTTP/1.1\r\n' +
									'ST: %(library)s:%(service)s\r\n' +
									'MX: 3\r\n' +
									'MAN: "ssdp:discover"\r\n' +
									'HOST: 239.255.255.250:1900\r\n\r\n')

	def interface_addresses(family=socket.AF_INET):
			for fam, _, _, _, sockaddr in socket.getaddrinfo('', None):
					if family == fam:
							yield sockaddr[0]

	msg = DISCOVERY_MSG % dict(service='rootdevice', library=LIB_ID)
	#socket.setdefaulttimeout(3)
	USNCache = []
	ssdpResultList = []
	XBMCResultList = {}
	for addr in interface_addresses():
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		sock.settimeout(3)
		sock.bind((addr, 0))

		for _ in xrange(2):
			sock.sendto(msg, (MCAST_GRP, MCAST_PORT))

		while True:
			try:
				#data = sock.recv(1024).splitlines()
				data = sock.recv(1024)
			except socket.timeout:
					print 'XBMC2: Search finished, results in address dropbox.'
					break
			else:
				headers = Headers(data)
				if "HTTP/1.1 200 OK" == headers['Start-line']:
					if headers['USN'] not in USNCache:
						USNCache.append(headers['USN'])
						ssdpResultList.append(headers['LOCATION'])
						#with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'ssdp.log'), 'a') as f:
						#	f.write(data)

	for result in ssdpResultList:
		#with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'ssdp.log'), 'a') as f:
		#	f.write(urllib2.urlopen(result).read())
		doc = xml.dom.minidom.parse(urllib2.urlopen(result))
		for modelName in doc.getElementsByTagName("modelName"):
			if modelName.firstChild.data in ('XBMC Media Center', 'Kodi'):
				XBMCResultList[urlparse(doc.getElementsByTagName("presentationURL")[0].firstChild.data).netloc] = doc.getElementsByTagName("friendlyName")[0].firstChild.data
	return XBMCResultList

def CheckDefault(Dict1, Dict2):
	for i in Dict1.iterkeys():
		if type(Dict1[i]) is dict:
			try:
				CheckDefault(Dict1[i], Dict2[i])
			except KeyError:
				Dict2[i] = Dict1[i].copy()
		else:
			if not Dict2.has_key(i):
				Dict2[i] = Dict1[i]

# And now we define the actual plugin:

class XBMC2(eg.PluginClass):
    pluginConfigDefault = {
    	'XBMC': {
    		'ip': '127.0.0.1',
    		'port': 80,
    		'username': '',
    		'password': '',
    	},
    	'EventServer': {
    		'enable': True,
    		'port': 9777,
    	},
    	'JSONRPC': {
    		'enable': False,
    		'port': 9090,
    		#'retrys': 5,
    		#'retryTime': 5,
    	},
    	'Broadcast':{
				'enable': False,
				'port': 8278,
				#'workaround': False,
    	},
    	'logRawEvents': False,
    	'logDebug': False,
    }

    def __init__(self):
        ButtonsGroup = self.AddGroup("Buttons", "Button actions to send to XBMC")
        ButtonsGroup.AddActionsFromList(REMOTE_BUTTONS, ButtonPrototype)
        ButtonsGroup.AddActionsFromList(GAMEPAD_BUTTONS, GamepadPrototype)
        ButtonsGroup.AddActionsFromList(APPLEREMOTE_BUTTONS, AppleRemotePrototype)
        ButtonsGroup.AddActionsFromList(KEYBOARD_KEYS, KeyboardPrototype)
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
        try:
					MANUALLYUPDATED_ACTIONS = [[eg.ActionGroup, "ManuallyUpdated", "Manually Updated", None, readData('actions.dat')]]
        except IOError:
          #eg.PrintError('Failed to open: httpapi.dat')
          pass
        else:
          ActionsGroup.AddActionsFromList(MANUALLYUPDATED_ACTIONS, ActionPrototype)

        ConfigurableGroup = ActionsGroup.AddGroup("Configurable", "Actions that have configurable settings")
        ConfigurableGroup.AddAction(UpdateLibrary)
        self.AddActionsFromList(WINDOWS, ActionPrototype)

        TestGroup = self.AddGroup("Experimental", "Experimental")
        TestGroup.AddAction(JSONRPC)
        TestGroup.AddAction(HTTPAPI)
        TestGroup.AddAction(BuiltInFunctions)
        TestGroup.AddAction(GetCurrentlyPlayingFilename)
        TestGroup.AddAction(SendNotification)

#        self.AddAction(StopRepeating)
        self.xbmc = XBMCClient("EventGhost")
        self.JSON_RPC = XBMC_JSON_RPC()
        self.HTTP_API = XBMC_HTTP_API()
        self.stopJSONRPCNotifications = Event()
        self.stopBroadcastEvents = Event()

    def Configure(self, pluginConfig={}, *args):
				def UpdateActions(event):
					def GetActions():
						URL = 'https://raw.githubusercontent.com/xbmc/xbmc/Krypton/xbmc/input/ButtonTranslator.cpp'
						request = urllib2.Request(URL)
						#try:
						w = urllib2.urlopen(request)
						#except urllib2.HTTPError:
						#	#Page = Cache[URL]['Page']
						#	pass
						#else:
						Page1 = w.read().splitlines(False)
						#print repr(Page1)

						#print Page1.index("static const ActionMapping actions[] =")
						#print Page1[Page1.index("static const ActionMapping actions[] ="):].index("};")
						Page1a = Page1[Page1.index("static const ActionMapping actions[] =") + 2:Page1.index("};")]
						#print Page1a[0]
						#print len(Page1a)

						ActionList = []
						for i in Page1a:
							try:
								#print repr(i.split('"')[1])
								ActionList.append(i.split('"')[1])
							except IndexError:
								pass
						return ActionList

					def GetActionDescriptions():
						def XMLText(Node):
							text = ''
							#print "Info:", Node.nodeValue, Node.nodeName
							try:
								for n in Node.childNodes:
									text += n.nodeValue if n.nodeName == '#text' else XMLText(n)
								#print "Text:", text
							except:
								print "Try:", Node.nodeValue, Node.nodeName

							return text

						UserAgent = 'XBMC2 EventGhost plugin'
						URL = 'http://kodi.wiki/view/Action_IDs'
						hdr = {'User-Agent': UserAgent}

						request = urllib2.Request(URL, headers=hdr)
						w = urllib2.urlopen(request)

						Page2 = w.read()

						ActionDict = {}
						for tr in xml.dom.minidom.parseString(Page2).getElementsByTagName("tr"):
							#for code in xml.dom.minidom.parseString(Page2).getElementsByTagName("code"):
							for code in tr.getElementsByTagName("code")[0:1]:
								#code = tr.getElementsByTagName("code")[0]
								#print "code:", code.nodeValue, code.nodeName
								#print repr(code.childNodes.item(0).nodeValue)
								if '2-9' in XMLText(code).strip():
									for i in range(2, 10):
										#print i
										#print repr((XMLText(code).strip()[:-5] + str(i)).lower()),
										#print repr(XMLText(code.parentNode.nextSibling.nextSibling).strip())
										ActionDict[(XMLText(code).strip()[:-5] + str(i)).lower()] = ((XMLText(code).strip()[:-5] + str(i)), XMLText(code.parentNode.nextSibling.nextSibling).strip())
								elif '0-9' in XMLText(code).strip():
									for i in range(10):
										#print i
										#print repr((XMLText(code).strip()[:-5] + str(i)).lower()),
										#print repr(XMLText(code.parentNode.nextSibling.nextSibling).strip())
										ActionDict[(XMLText(code).strip()[:-5] + str(i)).lower()] = ((XMLText(code).strip()[:-5] + str(i)), XMLText(code.parentNode.nextSibling.nextSibling).strip())
								else:
									if XMLText(code).strip().lower() not in ActionDict:
										#print repr(XMLText(code).strip().lower()),
										#print repr(XMLText(code.parentNode.nextSibling.nextSibling).strip())
										ActionDict[XMLText(code).strip().lower()] = (XMLText(code).strip(), XMLText(code.parentNode.nextSibling.nextSibling).strip())
										#print "End"
						return ActionDict

					ActionList = GetActions()
					ActionDict = GetActionDescriptions()

					for a in GENERAL_ACTIONS[0][4] + MEDIA_PLAYING_ACTIONS[0][4] + PLAYLIST_ACTIONS[0][4] + FULLSCREEN_VIDEO_ACTIONS[0][4] + SLIDESHOW_ACTIONS[0][4] + CALIBRATION_ACTIONS[0][4] + FILEMANAGER_ACTIONS[0][4] + ON_SCREEN_KEYBOARD_ACTIONS[0][4] + VISUALISATION_ACTIONS[0][4] + SHUTDOWN_ACTIONS[0][4] + UNCATEGORIZED_ACTIONS[0][4]:
						#print a
						if a[3].lower() in ActionList:
							ActionList.remove(a[3])
						#else:
						#	print repr(a)

					EGActionList = []
					for action in sorted(ActionList):
						try:
							ActionDict[action]
							#print repr((action, ActionDict[action][0], ActionDict[action][1], action))
							EGActionList.append((action, ActionDict[action][0], ActionDict[action][1], action))
						except KeyError:
							#print "Description missing:", action
							pass
					#print repr(EGActionList)

					writeData('actions.dat', EGActionList)
					print 'XBMC2: "Manually added" actions updated, restart EventGhost to use.'
				def ConnectionTest(event):
					print "XBMC2: Starting connection test, trying to connect to XBMC using", panel.combo_box_IP.GetValue()

					self.JSON_RPC.connect(ip=panel.combo_box_IP.GetValue().split(':')[0], port=panel.combo_box_IP.GetValue().split(':')[1], username=panel.text_ctrl_Username.GetValue(), password=panel.text_ctrl_Password.GetValue())
					try:
						result = self.JSON_RPC.send('GUI.ShowNotification', ast.literal_eval("['XBMC2 for EventGhost','Connection test, JSON-RPC works.']"))
					except urllib2.HTTPError as e:
						eg.PrintError('XBMC2:', str(e))
						print 'XBMC2: Please check that your username and password are correct.'
					except urllib2.URLError as e:
						eg.PrintError('XBMC2:', str(e.reason))
						print 'XBMC2: Please check that XBMC is running, that your IP address and port are correct.\nXBMC2: Also in XBMCs settings\\Services\\Webserver, "Allow control of XBMC via HTTP" needs to be set.'
					except ValueError as e:
						eg.PrintError("XBMC2: Server responded but didn't provide valid JSON data. Check that your IP and port are correct.")
					except:
						eg.PrintError('XBMC2: Unknown error: ')
						import sys, traceback
						traceback.print_exc()
					finally:
						self.JSON_RPC.close()

					try:
						if result['result'] == 'OK':
							print 'XBMC2: JSON-RPC works.'
					#except KeyError:
					#	eg.PrintError('XBMC2: JSON-RPC error: ', str(result['error']['message']))
					except:
						self.HTTP_API.connect(ip=panel.combo_box_IP.GetValue().split(':')[0], port=panel.combo_box_IP.GetValue().split(':')[1], username=panel.text_ctrl_Username.GetValue(), password=panel.text_ctrl_Password.GetValue())
						try:
							result = self.HTTP_API.send('ExecBuiltIn', 'Notification(XBMC2 for EventGhost, Connection test. HTTPAPI works.)')
						except urllib2.HTTPError as e:
							if e.code == 401:
								eg.PrintError('XBMC2:', str(e))
								print 'XBMC2: Please check that your username and password are correct.'
							else:
								eg.PrintError('XBMC2:', str(e))
								print 'XBMC2: Please check that XBMC is running, that your IP address and port are correct.\nXBMC2: Also in XBMCs settings\\Network\\Services\\ "Allow control of XBMC via HTTP" needs to be set.'
						except urllib2.URLError as e:
							eg.PrintError('XBMC2:', str(e.reason))
							print 'XBMC2: Please check that XBMC is running, that your IP address and port are correct.\nXBMC2: Also in XBMCs settings\\Network\\Services\\ "Allow control of XBMC via HTTP" needs to be set.'
						except:
							eg.PrintError('XBMC2: Unknown error: ')
							import sys, traceback
							traceback.print_exc()
						else:
								if result == 'OK':
									print 'XBMC2: HTTPAPI works.', result
								else:
									eg.PrintError('XBMC2: HTTPAPI error: ', result)
									self.xbmc.connect(ip=panel.combo_box_IP.GetValue().split(':')[0])
									self.xbmc.send_notification('XBMC2 for EventGhost', 'Connection test, if you see this your IP address is correct.')
									self.xbmc.close()
						finally:
							self.HTTP_API.close()

				def SearchForXBMC(event):
					for i in ssdpSearch().keys():
						panel.combo_box_IP.Append(i)

				def initPanel(self):
					self.combo_box_IP = wx.ComboBox(self, wx.ID_ANY, value=pluginConfig['XBMC']['ip']+':'+str(pluginConfig['XBMC']['port']), choices=["127.0.0.1:80"], style=wx.CB_DROPDOWN)
					self.button_IPTest = wx.Button(self, wx.ID_ANY, "Test")

					self.button_UpdateActions = wx.Button(self, wx.ID_ANY, "Update Actions")

					self.button_Search = wx.Button(self, wx.ID_ANY, "Search")
					self.label_Username = wx.StaticText(self, wx.ID_ANY, "Username")
					self.text_ctrl_Username = wx.TextCtrl(self, wx.ID_ANY, pluginConfig['XBMC']['username'])
					self.label_Password = wx.StaticText(self, wx.ID_ANY, "Password")
					self.text_ctrl_Password = wx.TextCtrl(self, wx.ID_ANY, pluginConfig['XBMC']['password'], style=wx.TE_PASSWORD)
					self.sizer_Global_staticbox = wx.StaticBox(self, wx.ID_ANY, "IP address and port of XBMC (127.0.01 is this computer)")
					self.checkbox_EventServerEnable = wx.CheckBox(self, wx.ID_ANY, "Enable")
					self.label_EventServerPort = wx.StaticText(self, wx.ID_ANY, "Port")
					self.spin_ctrl_EventServerPort = wx.SpinCtrl(self, wx.ID_ANY, str(pluginConfig['EventServer']['port']), min=0, max=65535)
					self.sizer_EventServer_staticbox = wx.StaticBox(self, wx.ID_ANY, "EventServer")
					self.checkbox_JSONRPCEnable = wx.CheckBox(self, wx.ID_ANY, "Enable")
					self.label_Port = wx.StaticText(self, wx.ID_ANY, "Port")
					self.spin_ctrl_JSONRPCPort = wx.SpinCtrl(self, wx.ID_ANY, str(pluginConfig['JSONRPC']['port']), min=0, max=65535)
					self.label_Retrys = wx.StaticText(self, wx.ID_ANY, "Retrys")
					self.spin_ctrl_Retrys = wx.SpinCtrl(self, wx.ID_ANY, "5", min=0, max=100)
					self.label_Time = wx.StaticText(self, wx.ID_ANY, "Time between retrys")
					self.spin_ctrl_Time = wx.SpinCtrl(self, wx.ID_ANY, "5", min=0, max=100)
					self.label_Seconds = wx.StaticText(self, wx.ID_ANY, "Seconds")
					self.sizer_JSONRPC_staticbox = wx.StaticBox(self, wx.ID_ANY, "JSON-RPC notifications")
					self.checkbox_BroadcastEnable = wx.CheckBox(self, wx.ID_ANY, "Enable")
					self.label_BroadcastPort = wx.StaticText(self, wx.ID_ANY, "Port")
					self.spin_ctrl_BroadcastPort = wx.SpinCtrl(self, wx.ID_ANY, str(pluginConfig['Broadcast']['port']), min=0, max=65535)
					self.checkbox_BroadcastWorkaround = wx.CheckBox(self, wx.ID_ANY, "Repeating events workaround")
					self.sizer_Broadcast_staticbox = wx.StaticBox(self, wx.ID_ANY, "Broadcast events")
					self.checkbox_logRawEvents = wx.CheckBox(self, wx.ID_ANY, "Log raw events")

					self.checkbox_logDebug = wx.CheckBox(self, wx.ID_ANY, "Debug")

					self.sizer_Events_staticbox = wx.StaticBox(self, wx.ID_ANY, "Event settings")
					self.button_IPTest.Bind(wx.EVT_BUTTON, ConnectionTest)

					self.button_UpdateActions.Bind(wx.EVT_BUTTON, UpdateActions)

					self.button_Search.Bind(wx.EVT_BUTTON, SearchForXBMC)
					setPanelProperties(self)
					doPanelLayout(self)
				def setPanelProperties(self):
					self.combo_box_IP.SetMinSize((147, 21))
					self.combo_box_IP.SetToolTipString("IP address of the XBMC you want to control.")
					self.button_IPTest.SetToolTipString("Test to connect to XBMC")

					self.button_UpdateActions.SetToolTipString('Add any new XBMC actions to a category "Manually Updated". You need to restart EventGhost for the new actions to be visible')

					self.button_Search.SetToolTipString("Search for any XBMCs that are running and reachable over the LAN.")
					self.text_ctrl_Username.SetToolTipString("Username that are specified in XBMC")
					self.text_ctrl_Password.SetToolTipString("Password that are specified in XBMC")
					self.checkbox_EventServerEnable.Enable(False)
					self.checkbox_EventServerEnable.SetValue(1)
					self.spin_ctrl_EventServerPort.SetMinSize((60, -1))
					self.spin_ctrl_EventServerPort.SetToolTipString("Port used by XBMC to recieve notifications")
					self.checkbox_JSONRPCEnable.SetToolTipString("Enable JSON-RPC notifications")
					self.checkbox_JSONRPCEnable.SetValue(pluginConfig['JSONRPC']['enable'])
					self.checkbox_BroadcastEnable.SetValue(pluginConfig['Broadcast']['enable'])
					self.checkbox_logRawEvents.SetValue(pluginConfig['logRawEvents'])

					self.checkbox_logDebug.SetValue(pluginConfig['logDebug'])

					self.spin_ctrl_JSONRPCPort.SetMinSize((60, -1))
					self.spin_ctrl_JSONRPCPort.SetToolTipString("Port used by XBMC to recieve notifications")
					self.spin_ctrl_Retrys.SetMinSize((50, -1))
					self.spin_ctrl_Time.SetMinSize((50, -1))
					self.checkbox_logRawEvents.SetToolTipString("Show any events from XBMC in the log, exactly as XBMC sends them.")

					self.checkbox_logDebug.SetToolTipString("Activate debugging messages in the log(Will spam the log so use only when needed).")
				def doPanelLayout(self):
					self.sizer = wx.BoxSizer(wx.VERTICAL)
					self.sizer_Events_staticbox.Lower()
					sizer_Events = wx.StaticBoxSizer(self.sizer_Events_staticbox, wx.VERTICAL)
					self.sizer_Broadcast_staticbox.Lower()
					sizer_Broadcast = wx.StaticBoxSizer(self.sizer_Broadcast_staticbox, wx.HORIZONTAL)
					sizer_BroadcastEnable = wx.BoxSizer(wx.VERTICAL)
					sizer_BroadcastPort = wx.BoxSizer(wx.HORIZONTAL)
					self.sizer_JSONRPC_staticbox.Lower()
					sizer_JSONRPC = wx.StaticBoxSizer(self.sizer_JSONRPC_staticbox, wx.VERTICAL)
					sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
					sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
					self.sizer_EventServer_staticbox.Lower()
					sizer_EventServer = wx.StaticBoxSizer(self.sizer_EventServer_staticbox, wx.VERTICAL)
					sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
					self.sizer_Global_staticbox.Lower()
					sizer_Global = wx.StaticBoxSizer(self.sizer_Global_staticbox, wx.VERTICAL)
					sizer_Password = wx.BoxSizer(wx.HORIZONTAL)
					sizer_IPPort = wx.BoxSizer(wx.HORIZONTAL)
					sizer_IPPort.Add(self.combo_box_IP, 0, 0, 0)
					sizer_IPPort.Add(self.button_IPTest, 0, 0, 0)
					sizer_IPPort.Add(self.button_Search, 0, 0, 0)
					sizer_Global.Add(sizer_IPPort, 1, wx.EXPAND, 0)
					sizer_Password.Add(self.label_Username, 0, 0, 0)
					sizer_Password.Add(self.text_ctrl_Username, 0, 0, 0)
					sizer_Password.Add(self.label_Password, 0, 0, 0)
					sizer_Password.Add(self.text_ctrl_Password, 0, 0, 0)
					sizer_Global.Add(sizer_Password, 1, wx.EXPAND, 0)
					sizer_2.Add(sizer_Global, 0, 0, 0)
					sizer_EventServer.Add(self.checkbox_EventServerEnable, 0, 0, 0)
					sizer_1.Add(self.label_EventServerPort, 0, 0, 0)
					sizer_1.Add(self.spin_ctrl_EventServerPort, 0, 0, 0)
					sizer_EventServer.Add(sizer_1, 1, wx.SHAPED, 0)
					sizer_2.Add(sizer_EventServer, 0, wx.SHAPED, 0)
					self.sizer.Add(sizer_2, 0, wx.EXPAND, 0)
					sizer_JSONRPC.Add(self.checkbox_JSONRPCEnable, 0, 0, 0)
					sizer_14.Add(self.label_Port, 0, 0, 0)
					sizer_14.Add(self.spin_ctrl_JSONRPCPort, 0, 0, 0)
					sizer_14.Add(self.label_Retrys, 0, 0, 0)
					sizer_14.Add(self.spin_ctrl_Retrys, 0, 0, 0)
					sizer_14.Add(self.label_Time, 0, 0, 0)
					sizer_14.Add(self.spin_ctrl_Time, 0, 0, 0)
					sizer_14.Add(self.label_Seconds, 0, 0, 0)
					sizer_JSONRPC.Add(sizer_14, 1, wx.EXPAND, 0)
					sizer_Events.Add(sizer_JSONRPC, 1, wx.EXPAND, 0)
					sizer_BroadcastEnable.Add(self.checkbox_BroadcastEnable, 0, 0, 0)
					sizer_BroadcastPort.Add(self.label_BroadcastPort, 0, 0, 0)
					sizer_BroadcastPort.Add(self.spin_ctrl_BroadcastPort, 0, 0, 0)
					sizer_BroadcastPort.Add(self.checkbox_BroadcastWorkaround, 0, 0, 0)
					sizer_BroadcastEnable.Add(sizer_BroadcastPort, 1, wx.EXPAND, 0)
					sizer_Broadcast.Add(sizer_BroadcastEnable, 1, wx.EXPAND, 0)
					sizer_Events.Add(sizer_Broadcast, 1, wx.EXPAND, 0)
					sizer_Events.Add(self.checkbox_logRawEvents, 0, 0, 0)

					sizer_Events.Add(self.checkbox_logDebug, 0, 0, 0)

					sizer_Events.Add(self.button_UpdateActions, 0, 0, 0)

					self.sizer.Add(sizer_Events, 1, wx.EXPAND, 0)
					self.sizer.Fit(self)

				if type(pluginConfig) is not dict:
					pluginConfig = {}
				CheckDefault(self.pluginConfigDefault, pluginConfig)

				panel = eg.ConfigPanel()
				initPanel(panel)
#        textControl = panel.ComboBox(
#            ip,
#            IPs,
#            style=wx.CB_DROPDOWN,
#            validator=eg.DigitOnlyValidator()
#        )
				while panel.Affirmed():
					changed = False
					if pluginConfig['XBMC']['ip'] != panel.combo_box_IP.GetValue().split(':')[0]:
						pluginConfig['XBMC']['ip'] = panel.combo_box_IP.GetValue().split(':')[0]
						changed = True
					if pluginConfig['XBMC']['port'] != int(panel.combo_box_IP.GetValue().split(':')[1]):
						pluginConfig['XBMC']['port'] = int(panel.combo_box_IP.GetValue().split(':')[1])
						changed = True
					if pluginConfig['XBMC']['username'] != panel.text_ctrl_Username.GetValue():
						pluginConfig['XBMC']['username'] = panel.text_ctrl_Username.GetValue()
						changed = True
					if pluginConfig['XBMC']['password'] != panel.text_ctrl_Password.GetValue():
						pluginConfig['XBMC']['password'] = panel.text_ctrl_Password.GetValue()
						changed = True
					if pluginConfig['EventServer']['port'] != int(panel.spin_ctrl_EventServerPort.GetValue()):
						pluginConfig['EventServer']['port'] = int(panel.spin_ctrl_EventServerPort.GetValue())
						changed = True
					if pluginConfig['JSONRPC']['enable'] != panel.checkbox_JSONRPCEnable.GetValue():
						pluginConfig['JSONRPC']['enable'] = panel.checkbox_JSONRPCEnable.GetValue()
						changed = True
					if pluginConfig['JSONRPC']['port'] != int(panel.spin_ctrl_JSONRPCPort.GetValue()):
						pluginConfig['JSONRPC']['port'] = int(panel.spin_ctrl_JSONRPCPort.GetValue())
						changed = True
					if pluginConfig['Broadcast']['enable'] != panel.checkbox_BroadcastEnable.GetValue():
						pluginConfig['Broadcast']['enable'] = panel.checkbox_BroadcastEnable.GetValue()
						changed = True
					if pluginConfig['Broadcast']['port'] != int(panel.spin_ctrl_BroadcastPort.GetValue()):
						pluginConfig['Broadcast']['port'] = int(panel.spin_ctrl_BroadcastPort.GetValue())
						changed = True
					if pluginConfig['logRawEvents'] != panel.checkbox_logRawEvents.GetValue():
						pluginConfig['logRawEvents'] = panel.checkbox_logRawEvents.GetValue()
						changed = True
					if pluginConfig['logDebug'] != panel.checkbox_logDebug.GetValue():
						pluginConfig['logDebug'] = panel.checkbox_logDebug.GetValue()
						changed = True
					#pluginConfig['JSONRPC']['retrys'] = int(JSONRPCNotificationRetrys.GetValue())
					#pluginConfig['JSONRPC']['retryTime'] = int(JSONRPCNotificationRetryTime.GetValue())
					try:
						panel.SetResult(pluginConfig, (args[0], not(args[0]))[changed])
					except:
						panel.SetResult(pluginConfig, changed)

    def __start__(self, pluginConfig={}, *args):
				if type(pluginConfig) is not dict:
					pluginConfig = {}
				CheckDefault(self.pluginConfigDefault, pluginConfig)

				self.pluginConfig = pluginConfig
				try:
						self.xbmc.connect(ip=pluginConfig['XBMC']['ip'], port=pluginConfig['EventServer']['port'])
				except:
						raise self.Exceptions.ProgramNotRunning
				self.JSON_RPC.connect(ip=pluginConfig['XBMC']['ip'], port=pluginConfig['XBMC']['port'], username=pluginConfig['XBMC']['username'], password=pluginConfig['XBMC']['password'])
				self.HTTP_API.connect(ip=pluginConfig['XBMC']['ip'], port=pluginConfig['XBMC']['port'], username=pluginConfig['XBMC']['username'], password=pluginConfig['XBMC']['password'])
				if self.pluginConfig['JSONRPC']['enable']:
					try:
						self.JSONRPCNotificationsThread.join(10)
					except:
						self.stopJSONRPCNotifications.clear()
						self.JSONRPCNotificationsThread = Thread(target=self.JSONRPCNotifications, args=(self.stopJSONRPCNotifications,))
						self.JSONRPCNotificationsThread.start()
					else:
						if not self.JSONRPCNotificationsThread.isAlive():
							self.stopJSONRPCNotifications.clear()
							self.JSONRPCNotificationsThread = Thread(target=self.JSONRPCNotifications, args=(self.stopJSONRPCNotifications,))
							self.JSONRPCNotificationsThread.start()
						else:
							print "XBMC2: Can't stop old JSON-RPC notification thread, will not start a new one."

				if self.pluginConfig['Broadcast']['enable']:
					self.stopBroadcastEvents.clear()
					BroadcastEventsThread = Thread(target=self.BroadcastEvents, args=(self.stopBroadcastEvents,))
					BroadcastEventsThread.start()

    def __stop__(self):
				#if self.pluginConfig['JSONRPC']['enable']:
				self.stopJSONRPCNotifications.set()
				#if self.pluginConfig['Broadcast']['enable']:
				self.stopBroadcastEvents.set()
				try:
						self.xbmc.close()
				except:
						pass

    def __close__(self):
        pass

#    def ThreadWorker(self, stopThreadEvent):
#        while not stopThreadEvent.isSet():
#            self.TriggerEvent("MyTimerEvent")
#            stopThreadEvent.wait(10.0)

    def JSONRPCNotifications(self, stopJSONRPCNotifications):
			import os
			import struct
			from collections import deque
			import select
			debug = self.pluginConfig['logDebug']
			def SSDPInit(SSDP_IP, SSDP_PORT):
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				sock.settimeout(10)
				sock.bind(('', SSDP_PORT))
				mreq = struct.pack("4sl", socket.inet_aton(SSDP_IP), socket.INADDR_ANY)
				sock.setsockopt(socket.IPPROTO_IP, socket.SO_DEBUG, True)
				try:
					sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
				except:
					if debug:
						eg.PrintError('JSON-RPC connect error: ')
						import sys, traceback
						traceback.print_exc()
					try:
						INTERFACE_ADDR = socket.gethostbyname(socket.gethostname())
						mreq = socket.inet_aton(SSDP_IP) + socket.inet_aton(INTERFACE_ADDR)
						sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
					except:
						eg.PrintError('JSON-RPC connect error: ')
						import sys, traceback
						traceback.print_exc()
						raise
				#sock.settimeout(10)
				#sock.bind(('', SSDP_PORT))
				return sock
			def Headers(data):
				headers = {}
				for line in data.splitlines():
					if not line.split(':', 1)[0]:
						continue
					try:
						headers[line.split(':', 1)[0].upper()] = line.split(':', 1)[1]
					except:
						headers['Start-line'] = line.split(':', 1)[0]
				return headers
			def interface_addresses(family=socket.AF_INET):
				for fam, _, _, _, sockaddr in socket.getaddrinfo('', None):
					if family == fam:
						yield sockaddr[0]

			def JSONSplit(data):
				parts = []
				rest = data
				while rest:
					part = ''
					while True:
						try:
							part += rest[:rest.index('}')+1]
						except ValueError:
							rest = ''
							break
						else:
							rest = rest[rest.find('}')+1:]
							try:
								parts.append(json.loads(part))
								break
							except:
								continue
				return parts
			def BufferedRead(Socket):
				_PacketSize = 4096
				Buffer = deque()
				rlist = [Socket, ]
				while not stopJSONRPCNotifications.isSet():
					if Buffer:
						ready, _, _ = select.select(rlist, [], [], 0)
						if ready:
							data = Socket.recv(_PacketSize)
						else:
							#print('{0}: Buffer: {1}\n'.format(MyName, len(Buffer)), end='')
							#Q.put((MyName, Buffer.popleft(), len(Buffer)), True)
							yield Buffer.popleft()
							continue
					else:
						try:
							data = Socket.recv(_PacketSize)
						except socket.timeout:
							#logging.debug('SSDPListener: Wait for event: Timeout.')
							if debug:
								print 'XBMC2: SSDP: Wait for event: Timeout.'
							continue
					Buffer.append(data)
				if debug:
					print 'XBMC2: SSDP: Wait for event: Stop recieving messages.'

			def WaitForXBMC(Socket):
				USNCache = []
				XBMCDetected = False
				BRead = BufferedRead(Socket)

				if debug:
					print 'XBMC2: SSDP is on'
				while not (stopJSONRPCNotifications.isSet() or XBMCDetected):
					if debug:
						print 'XBMC2: SSDP: Wait for event.'
					try:
						#data = sock.recv(4096)
						data = BRead.next()
						headers = Headers(data)
						#headers = Headers(sock.recv(4096))
					except socket.timeout:
						if debug:
							print 'XBMC2: SSDP: Wait for event: Timeout.'
						pass
					except StopIteration:
						continue
					else:
						try:
							if debug:
								with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'ssdp.log'), 'a+') as f:
									f.write("Got ssdp message.")
							if "NOTIFY * HTTP/1.1" == headers['Start-line']:
								try:
									if headers['USN'].split(':', 2)[1] not in USNCache:
										try:
											doc = xml.dom.minidom.parse(urllib2.urlopen(headers['LOCATION']))
										except:
											continue
										else:
											for modelName in doc.getElementsByTagName("modelName"):
												if modelName.firstChild.data in ('Kodi', 'XBMC Media Center', 'XBMC'):
													if debug:
														with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'ssdp.log'), 'a+') as f:
															f.write(data)
															f.write(urllib2.urlopen(headers['LOCATION']).read())
														print 'XBMC2: SSDP modelName:', modelName.firstChild.data
													#from urlparse import urlparse
													if self.pluginConfig['XBMC']['ip'] == '127.0.0.1':
														for ip in interface_addresses():
															#if urlparse(doc.getElementsByTagName("presentationURL")[0].firstChild.data).netloc == ip+':'+str(self.pluginConfig['XBMC']['port']):
															if urlparse(doc.getElementsByTagName("presentationURL")[0].firstChild.data).netloc.split(":")[0] == ip:
																try:
																	if urlparse(doc.getElementsByTagName("presentationURL")[0].firstChild.data).netloc.split(":")[1] == str(self.pluginConfig['XBMC']['port']):
																		XBMCDetected = True
																		break
																	else:
																		continue
																except:
																	pass
																XBMCDetected = True
																break
													else:
														if debug:
															print 'XBMC2: SSDP address:', urlparse(doc.getElementsByTagName("presentationURL")[0].firstChild.data).netloc
														if urlparse(doc.getElementsByTagName("presentationURL")[0].firstChild.data).netloc == self.pluginConfig['XBMC']['ip']+':'+str(self.pluginConfig['XBMC']['port']):
															XBMCDetected = True
												else:
													if debug:
														with open(os.path.join(eg.folderPath.RoamingAppData, 'EventGhost', 'plugins', 'XBMC2', 'ssdp.log'), 'a+') as f:
															f.write(data)
															f.write(urllib2.urlopen(headers['LOCATION']).read())
														print 'XBMC2: SSDP unknown modelName:', modelName.firstChild.data
											USNCache.append(headers['USN'].split(':', 2)[1])
								except IndexError:
									if debug:
										print 'XBMC2: SSDP: No USN in headers:', headers
									continue
							elif "M-SEARCH * HTTP/1.1" == headers['Start-line']:
								if 'Kodi' in headers['USER-AGENT']:
									if debug:
										print 'XBMC2: SSDP: Found search message from Kodi:', headers['USER-AGENT']
									XBMCDetected = True
									break
						except KeyError:
							if debug:
								print 'XBMC2: SSDP: "Start-line" test failed: Content of headers:', headers
								eg.PrintError('JSON-RPC connect error: ')
								import sys, traceback
								traceback.print_exc()
						except:
							if debug:
								print 'XBMC2: SSDP: Error in headers:', headers
								eg.PrintError('JSON-RPC connect error: ')
								import sys, traceback
								traceback.print_exc()

				#sock.close()
				if debug:
					print 'XBMC2: SSDP is off'

			SSDP_IP = '239.255.255.250'
			SSDP_PORT = 1900
			Socket = SSDPInit(SSDP_IP, SSDP_PORT)
			print "XBMC2: Activating JSON-RPC notifications"
			while not stopJSONRPCNotifications.isSet():
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(10)
				try:
					if debug:
						print "XBMC2: Connecting to XBMC, to be able to recive JSON-RPC notifications."
					s.connect((self.pluginConfig['XBMC']['ip'], self.pluginConfig['JSONRPC']['port']))
				except socket.error:
					if debug:
						eg.PrintError('XBMC2: connection error: ')
						import sys, traceback
						traceback.print_exc()
						print "XBMC2: Not able to connect to XBMC, will use SSDP to detect when XBMC is available."
					WaitForXBMC(Socket)
				else:
					print "XBMC2: Connected to XBMC (", self.pluginConfig['XBMC']['ip'], ":", self.pluginConfig['JSONRPC']['port'], "), ready to recive JSON-RPC notifications."
					self.TriggerEvent('System.OnStart')
					message = ''
					if debug:
						print 'XBMC2: JSON-RPC sent: "GetConfiguration".'
						s.send(json.dumps({'jsonrpc':'2.0', 'method': 'JSONRPC.GetConfiguration', 'id':1}))
					while not stopJSONRPCNotifications.isSet():
						try:
							if debug:
								print "XBMC2: JSON-RPC notifications: Wait for event."
							message += s.recv(4096)
							#print len(message)
							if not message:
								break
						except socket.timeout:
							if debug:
								print "XBMC2: JSON-RPC notifications: Wait for event: Timeout."
							s.send(json.dumps({'jsonrpc':'2.0', 'method': 'JSONRPC.Ping', 'id':1}))
							if debug:
								print 'XBMC2: JSON-RPC sent: "ping".'
							continue
						except socket.error:
							eg.PrintError('XBMC2: JSON socket.error: ')
							import sys, traceback
							traceback.print_exc()
							break
						except:
							eg.PrintError('XBMC2: Error: JSON-RPC event ')
							import sys, traceback
							traceback.print_exc()
							break
						else:
							if self.pluginConfig['logRawEvents']:
								print "XBMC2: Raw event: %s" % repr(message)
							try:
								messages = [json.loads(message)]
							except:
								#eg.PrintError('XBMC2: Error: JSON-RPC event ')
								#import sys, traceback
								#traceback.print_exc()
								#eg.PrintError('XBMC2: Error decoding: JSON-RPC event \n' + "Raw event: %s" % repr(message))
								#continue
								messages = JSONSplit(message)
							#else:Raw event: {u'jsonrpc': u'2.0', u'id': 1, u'result': u'pong'}
							for message in messages:
								if self.pluginConfig['logRawEvents']:
									print "Raw event: %s" % repr(message)
								try:
									event = message['method']
								except:
									try:
										message['id']
									except:
										eg.PrintError('XBMC2: Error: JSON-RPC event, "method" missing ' + repr(message))
										self.PrintError('JSON unrecogniced event type: \n' + "Raw event: %s" % repr(message))
									else:
										try:
											if 'notifications' in message['result']:
												if debug:
													print 'XBMC2: JSON-RPC responce: "notifications":', message['result']['notifications']
												continue
										except KeyError:
											if debug:
												eg.PrintError('XBMC2: Error: JSON-RPC responce, "result" missing ' + repr(message))
										else:
											if message['result'] == 'pong':
												if debug:
													print 'XBMC2: JSON-RPC responce: "pong".'
												continue
											else:
												eg.PrintError('XBMC2: Error: JSON-RPC responce, "pong" missing ' + repr(message))
												self.PrintError('JSON unrecogniced responce type: \n' + "Raw responce: %s" % repr(message))
								else:
									try:
										payload = message['params']['data']
									except KeyError:
										pass
									else:
										if not payload==None:
											try:
												event += '.' + payload['item']['type']
												del payload['item']['type']
												if not payload['item']:
													del payload['item']
											except KeyError:
												try:
													event += '.' + payload['type']
													del payload['type']
												except KeyError:
													#self.PrintError('JSON unrecogniced event type: \n' + "Raw event: %s" % repr(message))
													pass
											except TypeError:
												#self.PrintError('XBMC2: JSON unrecogniced event type: \n' + "Raw event: %s" % repr(message))
												pass
											except:
												self.PrintError('XBMC2: JSON unrecogniced event type: \n' + "Raw event: %s" % repr(message))

									if not stopJSONRPCNotifications.isSet():
										self.TriggerEvent(event, payload)
						message = ''
					s.close()
					print "XBMC2: Disconnected from XBMC, not receiving JSON-RPC notifications."
			print "XBMC2: Deactivating JSON-RPC notifications"

    def BroadcastEvents(self, stopBroadcastEvents):
			ActionList = {
# actions that we have defined...
'0':'ACTION_NONE',
'1':'ACTION_MOVE_LEFT',
'2':'ACTION_MOVE_RIGHT',
'3':'ACTION_MOVE_UP',
'4':'ACTION_MOVE_DOWN',
'5':'ACTION_PAGE_UP',
'6':'ACTION_PAGE_DOWN',
'7':'ACTION_SELECT_ITEM',
'8':'ACTION_HIGHLIGHT_ITEM',
'9':'ACTION_PARENT_DIR',
'10':'ACTION_PREVIOUS_MENU',
'11':'ACTION_SHOW_INFO',

'12':'ACTION_PAUSE',
'13':'ACTION_STOP',
'14':'ACTION_NEXT_ITEM',
'15':'ACTION_PREV_ITEM',
'16':'ACTION_FORWARD', # Can be used to specify specific action in a window, Playback control is handled in ACTION_PLAYER_*
'17':'ACTION_REWIND', # Can be used to specify specific action in a window, Playback control is handled in ACTION_PLAYER_*

'18':'ACTION_SHOW_GUI', # toggle between GUI and movie or GUI and visualisation.
'19':'ACTION_ASPECT_RATIO', # toggle quick-access zoom modes. Can b used in videoFullScreen.zml window id=2005
'20':'ACTION_STEP_FORWARD', # seek +1% in the movie. Can b used in videoFullScreen.xml window id=2005
'21':'ACTION_STEP_BACK', # seek -1% in the movie. Can b used in videoFullScreen.xml window id=2005
'22':'ACTION_BIG_STEP_FORWARD', # seek +10% in the movie. Can b used in videoFullScreen.xml window id=2005
'23':'ACTION_BIG_STEP_BACK', # seek -10% in the movie. Can b used in videoFullScreen.xml window id=2005
'24':'ACTION_SHOW_OSD', # show/hide OSD. Can b used in videoFullScreen.xml window id=2005
'25':'ACTION_SHOW_SUBTITLES', # turn subtitles on/off. Can b used in videoFullScreen.xml window id=2005
'26':'ACTION_NEXT_SUBTITLE', # switch to next subtitle of movie. Can b used in videoFullScreen.xml window id=2005
'27':'ACTION_SHOW_CODEC', # show information about file. Can b used in videoFullScreen.xml window id=2005 and in slideshow.xml window id=2007
'28':'ACTION_NEXT_PICTURE', # show next picture of slideshow. Can b used in slideshow.xml window id=2007
'29':'ACTION_PREV_PICTURE', # show previous picture of slideshow. Can b used in slideshow.xml window id=2007
'30':'ACTION_ZOOM_OUT', # zoom in picture during slideshow. Can b used in slideshow.xml window id=2007
'31':'ACTION_ZOOM_IN', # zoom out picture during slideshow. Can b used in slideshow.xml window id=2007
'32':'ACTION_TOGGLE_SOURCE_DEST', # used to toggle between source view and destination view. Can be used in myfiles.xml window id=3
'33':'ACTION_SHOW_PLAYLIST', # used to toggle between current view and playlist view. Can b used in all mymusic xml files
'34':'ACTION_QUEUE_ITEM', # used to queue a item to the playlist. Can b used in all mymusic xml files
'35':'ACTION_REMOVE_ITEM', # not used anymore
'36':'ACTION_SHOW_FULLSCREEN', # not used anymore
'37':'ACTION_ZOOM_LEVEL_NORMAL', # zoom 1x picture during slideshow. Can b used in slideshow.xml window id=2007
'38':'ACTION_ZOOM_LEVEL_1', # zoom 2x picture during slideshow. Can b used in slideshow.xml window id=2007
'39':'ACTION_ZOOM_LEVEL_2', # zoom 3x picture during slideshow. Can b used in slideshow.xml window id=2007
'40':'ACTION_ZOOM_LEVEL_3', # zoom 4x picture during slideshow. Can b used in slideshow.xml window id=2007
'41':'ACTION_ZOOM_LEVEL_4', # zoom 5x picture during slideshow. Can b used in slideshow.xml window id=2007
'42':'ACTION_ZOOM_LEVEL_5', # zoom 6x picture during slideshow. Can b used in slideshow.xml window id=2007
'43':'ACTION_ZOOM_LEVEL_6', # zoom 7x picture during slideshow. Can b used in slideshow.xml window id=2007
'44':'ACTION_ZOOM_LEVEL_7', # zoom 8x picture during slideshow. Can b used in slideshow.xml window id=2007
'45':'ACTION_ZOOM_LEVEL_8', # zoom 9x picture during slideshow. Can b used in slideshow.xml window id=2007
'46':'ACTION_ZOOM_LEVEL_9', # zoom 10x picture during slideshow. Can b used in slideshow.xml window id=2007

'47':'ACTION_CALIBRATE_SWAP_ARROWS', # select next arrow. Can b used in: settingsScreenCalibration.xml windowid=11
'48':'ACTION_CALIBRATE_RESET', # reset calibration to defaults. Can b used in: settingsScreenCalibration.xml windowid=11/settingsUICalibration.xml windowid=10
'49':'ACTION_ANALOG_MOVE', # analog thumbstick move. Can b used in: slideshow.xml window id=2007/settingsScreenCalibration.xml windowid=11/settingsUICalibration.xml windowid=10
'50':'ACTION_ROTATE_PICTURE', # rotate current picture during slideshow. Can b used in slideshow.xml window id=2007

'52':'ACTION_SUBTITLE_DELAY_MIN', # Decrease subtitle/movie Delay. Can b used in videoFullScreen.xml window id=2005
'53':'ACTION_SUBTITLE_DELAY_PLUS', # Increase subtitle/movie Delay. Can b used in videoFullScreen.xml window id=2005
'54':'ACTION_AUDIO_DELAY_MIN', # Increase avsync delay. Can b used in videoFullScreen.xml window id=2005
'55':'ACTION_AUDIO_DELAY_PLUS', # Decrease avsync delay. Can b used in videoFullScreen.xml window id=2005
'56':'ACTION_AUDIO_NEXT_LANGUAGE', # Select next language in movie. Can b used in videoFullScreen.xml window id=2005
'57':'ACTION_CHANGE_RESOLUTION', # switch 2 next resolution. Can b used during screen calibration settingsScreenCalibration.xml windowid=11

'58':'REMOTE_0', # remote keys 0-9. are used by multiple windows
'59':'REMOTE_1', # for example in videoFullScreen.xml window id=2005 you can
'60':'REMOTE_2', # enter time (mmss) to jump to particular point in the movie
'61':'REMOTE_3',
'62':'REMOTE_4', # with spincontrols you can enter 3digit number to quickly set
'63':'REMOTE_5', # spincontrol to desired value
'64':'REMOTE_6',
'65':'REMOTE_7',
'66':'REMOTE_8',
'67':'REMOTE_9',

'68':'ACTION_PLAY', # Unused at the moment
'69':'ACTION_OSD_SHOW_LEFT', # Move left in OSD. Can b used in videoFullScreen.xml window id=2005
'70':'ACTION_OSD_SHOW_RIGHT', # Move right in OSD. Can b used in videoFullScreen.xml window id=2005
'71':'ACTION_OSD_SHOW_UP', # Move up in OSD. Can b used in videoFullScreen.xml window id=2005
'72':'ACTION_OSD_SHOW_DOWN', # Move down in OSD. Can b used in videoFullScreen.xml window id=2005
'73':'ACTION_OSD_SHOW_SELECT', # toggle/select option in OSD. Can b used in videoFullScreen.xml window id=2005
'74':'ACTION_OSD_SHOW_VALUE_PLUS', # increase value of current option in OSD. Can b used in videoFullScreen.xml window id=2005
'75':'ACTION_OSD_SHOW_VALUE_MIN', # decrease value of current option in OSD. Can b used in videoFullScreen.xml window id=2005
'76':'ACTION_SMALL_STEP_BACK', # jumps a few seconds back during playback of movie. Can b used in videoFullScreen.xml window id=2005

'77':'ACTION_PLAYER_FORWARD', # FF in current file played. global action, can be used anywhere
'78':'ACTION_PLAYER_REWIND', # RW in current file played. global action, can be used anywhere
'79':'ACTION_PLAYER_PLAY', # Play current song. Unpauses song and sets playspeed to 1x. global action, can be used anywhere

'80':'ACTION_DELETE_ITEM', # delete current selected item. Can be used in myfiles.xml window id=3 and in myvideoTitle.xml window id=25
'81':'ACTION_COPY_ITEM', # copy current selected item. Can be used in myfiles.xml window id=3
'82':'ACTION_MOVE_ITEM', # move current selected item. Can be used in myfiles.xml window id=3
'83':'ACTION_SHOW_MPLAYER_OSD', # toggles mplayers OSD. Can be used in videofullscreen.xml window id=2005
'84':'ACTION_OSD_HIDESUBMENU', # removes an OSD sub menu. Can be used in videoOSD.xml window id=2901
'85':'ACTION_TAKE_SCREENSHOT', # take a screenshot
'87':'ACTION_RENAME_ITEM', # rename item

'88':'ACTION_VOLUME_UP',
'89':'ACTION_VOLUME_DOWN',
'91':'ACTION_MUTE',
'92':'ACTION_NAV_BACK',

'100':'ACTION_MOUSE_START',
'100':'ACTION_MOUSE_LEFT_CLICK',
'101':'ACTION_MOUSE_RIGHT_CLICK',
'102':'ACTION_MOUSE_MIDDLE_CLICK',
'103':'ACTION_MOUSE_DOUBLE_CLICK',
'104':'ACTION_MOUSE_WHEEL_UP',
'105':'ACTION_MOUSE_WHEEL_DOWN',
'106':'ACTION_MOUSE_DRAG',
'107':'ACTION_MOUSE_MOVE',
'109':'ACTION_MOUSE_END',

'110':'ACTION_BACKSPACE',
'111':'ACTION_SCROLL_UP',
'112':'ACTION_SCROLL_DOWN',
'113':'ACTION_ANALOG_FORWARD',
'114':'ACTION_ANALOG_REWIND',

'115':'ACTION_MOVE_ITEM_UP', # move item up in playlist
'116':'ACTION_MOVE_ITEM_DOWN', # move item down in playlist
'117':'ACTION_CONTEXT_MENU', # pops up the context menu


# stuff for virtual keyboard shortcuts
'118':'ACTION_SHIFT',
'119':'ACTION_SYMBOLS',
'120':'ACTION_CURSOR_LEFT',
'121':'ACTION_CURSOR_RIGHT',

'122':'ACTION_BUILT_IN_FUNCTION',

'123':'ACTION_SHOW_OSD_TIME', # displays current time, can be used in videoFullScreen.xml window id=2005
'124':'ACTION_ANALOG_SEEK_FORWARD', # seeks forward, and displays the seek bar.
'125':'ACTION_ANALOG_SEEK_BACK', # seeks backward, and displays the seek bar.

'126':'ACTION_VIS_PRESET_SHOW',
'127':'ACTION_VIS_PRESET_LIST',
'128':'ACTION_VIS_PRESET_NEXT',
'129':'ACTION_VIS_PRESET_PREV',
'130':'ACTION_VIS_PRESET_LOCK',
'131':'ACTION_VIS_PRESET_RANDOM',
'132':'ACTION_VIS_RATE_PRESET_PLUS',
'133':'ACTION_VIS_RATE_PRESET_MINUS',

'134':'ACTION_SHOW_VIDEOMENU',
'135':'ACTION_ENTER',

'136':'ACTION_INCREASE_RATING',
'137':'ACTION_DECREASE_RATING',

'138':'ACTION_NEXT_SCENE', # switch to next scene/cutpoint in movie
'139':'ACTION_PREV_SCENE', # switch to previous scene/cutpoint in movie

'140':'ACTION_NEXT_LETTER', # jump through a list or container by letter
'141':'ACTION_PREV_LETTER',

'142':'ACTION_JUMP_SMS2', # jump direct to a particular letter using SMS-style input
'143':'ACTION_JUMP_SMS3',
'144':'ACTION_JUMP_SMS4',
'145':'ACTION_JUMP_SMS5',
'146':'ACTION_JUMP_SMS6',
'147':'ACTION_JUMP_SMS7',
'148':'ACTION_JUMP_SMS8',
'149':'ACTION_JUMP_SMS9',

'150':'ACTION_FILTER_CLEAR',
'151':'ACTION_FILTER_SMS2',
'152':'ACTION_FILTER_SMS3',
'153':'ACTION_FILTER_SMS4',
'154':'ACTION_FILTER_SMS5',
'155':'ACTION_FILTER_SMS6',
'156':'ACTION_FILTER_SMS7',
'157':'ACTION_FILTER_SMS8',
'158':'ACTION_FILTER_SMS9',

'159':'ACTION_FIRST_PAGE',
'160':'ACTION_LAST_PAGE',

'161':'ACTION_AUDIO_DELAY',
'162':'ACTION_SUBTITLE_DELAY',

'180':'ACTION_PASTE',
'181':'ACTION_NEXT_CONTROL',
'182':'ACTION_PREV_CONTROL',
'183':'ACTION_CHANNEL_SWITCH',

'199':'ACTION_TOGGLE_FULLSCREEN', # switch 2 desktop resolution
'200':'ACTION_TOGGLE_WATCHED', # Toggle watched status (videos)
'201':'ACTION_SCAN_ITEM', # scan item
'202':'ACTION_TOGGLE_DIGITAL_ANALOG', # switch digital <-> analog
'203':'ACTION_RELOAD_KEYMAPS', # reloads CButtonTranslator's keymaps
'204':'ACTION_GUIPROFILE_BEGIN', # start the GUIControlProfiler running

'215':'ACTION_TELETEXT_RED', # Teletext Color buttons to control TopText
'216':'ACTION_TELETEXT_GREEN', # " " " " " "
'217':'ACTION_TELETEXT_YELLOW', # " " " " " "
'218':'ACTION_TELETEXT_BLUE', # " " " " " "

'219':'ACTION_INCREASE_PAR',
'220':'ACTION_DECREASE_PAR',

'221':'ACTION_GESTURE_NOTIFY',
'222':'ACTION_GESTURE_BEGIN',
'223':'ACTION_GESTURE_ZOOM', #sendaction with point and currentPinchScale (fingers together < 1.0 -> fingers apart > 1.0)
'224':'ACTION_GESTURE_ROTATE',
'225':'ACTION_GESTURE_PAN',
'226':'ACTION_GESTURE_END',
'227':'ACTION_VSHIFT_UP', # shift up video image in DVDPlayer
'228':'ACTION_VSHIFT_DOWN', # shift down video image in DVDPlayer

'229':'ACTION_PLAYER_PLAYPAUSE', # Play/pause. If playing it pauses, if paused it plays.

# The NOOP action can be specified to disable an input event. This is
# useful in user keyboard.xml etc to disable actions specified in the
# system mappings.
'999':'ACTION_NOOP',

'230':'ACTION_SUBTITLE_VSHIFT_UP', # shift up subtitles in DVDPlayer
'231':'ACTION_SUBTITLE_VSHIFT_DOWN', # shift down subtitles in DVDPlayer
'232':'ACTION_SUBTITLE_ALIGN', # toggle vertical alignment of subtitles

# Window ID defines to make the code a bit more readable
'9999':'WINDOW_INVALID',
'10000':'WINDOW_HOME',
'10001':'WINDOW_PROGRAMS',
'10002':'WINDOW_PICTURES',
'10003':'WINDOW_FILES',
'10004':'WINDOW_SETTINGS_MENU',
'10005':'WINDOW_MUSIC', # virtual window to return the music start window.
'10006':'WINDOW_VIDEOS',
'10007':'WINDOW_SYSTEM_INFORMATION',
'10008':'WINDOW_TEST_PATTERN',
'10011':'WINDOW_SCREEN_CALIBRATION',

'10012':'WINDOW_SETTINGS_MYPICTURES',
'10013':'WINDOW_SETTINGS_MYPROGRAMS',
'10014':'WINDOW_SETTINGS_MYWEATHER',
'10015':'WINDOW_SETTINGS_MYMUSIC',
'10016':'WINDOW_SETTINGS_SYSTEM',
'10017':'WINDOW_SETTINGS_MYVIDEOS',
'10018':'WINDOW_SETTINGS_NETWORK',
'10019':'WINDOW_SETTINGS_APPEARANCE',

'10020':'WINDOW_SCRIPTS', # virtual window for backward compatibility

'10024':'WINDOW_VIDEO_FILES',
'10025':'WINDOW_VIDEO_NAV',
'10028':'WINDOW_VIDEO_PLAYLIST',

'10029':'WINDOW_LOGIN_SCREEN',
'10034':'WINDOW_SETTINGS_PROFILES',

'10040':'WINDOW_ADDON_BROWSER',

'10099':'WINDOW_DIALOG_POINTER',
'10100':'WINDOW_DIALOG_YES_NO',
'10101':'WINDOW_DIALOG_PROGRESS',
'10103':'WINDOW_DIALOG_KEYBOARD',
'10104':'WINDOW_DIALOG_VOLUME_BAR',
'10105':'WINDOW_DIALOG_SUB_MENU',
'10106':'WINDOW_DIALOG_CONTEXT_MENU',
'10107':'WINDOW_DIALOG_KAI_TOAST',
'10109':'WINDOW_DIALOG_NUMERIC',
'10110':'WINDOW_DIALOG_GAMEPAD',
'10111':'WINDOW_DIALOG_BUTTON_MENU',
'10112':'WINDOW_DIALOG_MUSIC_SCAN',
'10113':'WINDOW_DIALOG_MUTE_BUG',
'10114':'WINDOW_DIALOG_PLAYER_CONTROLS',
'10115':'WINDOW_DIALOG_SEEK_BAR',
'10120':'WINDOW_DIALOG_MUSIC_OSD',
'10121':'WINDOW_DIALOG_VIS_SETTINGS',
'10122':'WINDOW_DIALOG_VIS_PRESET_LIST',
'10123':'WINDOW_DIALOG_VIDEO_OSD_SETTINGS',
'10124':'WINDOW_DIALOG_AUDIO_OSD_SETTINGS',
'10125':'WINDOW_DIALOG_VIDEO_BOOKMARKS',
'10126':'WINDOW_DIALOG_FILE_BROWSER',
'10128':'WINDOW_DIALOG_NETWORK_SETUP',
'10129':'WINDOW_DIALOG_MEDIA_SOURCE',
'10130':'WINDOW_DIALOG_PROFILE_SETTINGS',
'10131':'WINDOW_DIALOG_LOCK_SETTINGS',
'10132':'WINDOW_DIALOG_CONTENT_SETTINGS',
'10133':'WINDOW_DIALOG_VIDEO_SCAN',
'10134':'WINDOW_DIALOG_FAVOURITES',
'10135':'WINDOW_DIALOG_SONG_INFO',
'10136':'WINDOW_DIALOG_SMART_PLAYLIST_EDITOR',
'10137':'WINDOW_DIALOG_SMART_PLAYLIST_RULE',
'10138':'WINDOW_DIALOG_BUSY',
'10139':'WINDOW_DIALOG_PICTURE_INFO',
'10140':'WINDOW_DIALOG_ADDON_SETTINGS',
'10141':'WINDOW_DIALOG_ACCESS_POINTS',
'10142':'WINDOW_DIALOG_FULLSCREEN_INFO',
'10143':'WINDOW_DIALOG_KARAOKE_SONGSELECT',
'10144':'WINDOW_DIALOG_KARAOKE_SELECTOR',
'10145':'WINDOW_DIALOG_SLIDER',
'10146':'WINDOW_DIALOG_ADDON_INFO',
'10147':'WINDOW_DIALOG_TEXT_VIEWER',
'10148':'WINDOW_DIALOG_PLAY_EJECT',
'10149':'WINDOW_DIALOG_PERIPHERAL_MANAGER',
'10150':'WINDOW_DIALOG_PERIPHERAL_SETTINGS',

'10500':'WINDOW_MUSIC_PLAYLIST',
'10501':'WINDOW_MUSIC_FILES',
'10502':'WINDOW_MUSIC_NAV',
'10503':'WINDOW_MUSIC_PLAYLIST_EDITOR',

'10600':'WINDOW_DIALOG_OSD_TELETEXT',

#'11000':'WINDOW_VIRTUAL_KEYBOARD',
'12000':'WINDOW_DIALOG_SELECT',
'12001':'WINDOW_DIALOG_MUSIC_INFO',
'12002':'WINDOW_DIALOG_OK',
'12003':'WINDOW_DIALOG_VIDEO_INFO',
'12005':'WINDOW_FULLSCREEN_VIDEO',
'12006':'WINDOW_VISUALISATION',
'12007':'WINDOW_SLIDESHOW',
'12008':'WINDOW_DIALOG_FILESTACKING',
'12009':'WINDOW_KARAOKELYRICS',
'12600':'WINDOW_WEATHER',
'12900':'WINDOW_SCREENSAVER',
'12901':'WINDOW_DIALOG_VIDEO_OSD',

'12902':'WINDOW_VIDEO_MENU',
'12903':'WINDOW_DIALOG_MUSIC_OVERLAY',
'12904':'WINDOW_DIALOG_VIDEO_OVERLAY',
'12905':'WINDOW_VIDEO_TIME_SEEK', # virtual window for time seeking during fullscreen video

'12998':'WINDOW_START', # first window to load
'12999':'WINDOW_STARTUP_ANIM', # for startup animations

# WINDOW_ID's from 13000 to 13099 reserved for Python

'13000':'WINDOW_PYTHON_START',
'13099':'WINDOW_PYTHON_END',
}
			import socket
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			s.settimeout(3)
			s.bind(('', self.pluginConfig['Broadcast']['port']))
			print 'XBMC2: Listening for XBMC broadcast events'
			while not stopBroadcastEvents.isSet():
				#s.settimeout(None)
				message = ''
				addr = ''
				try:
					message, addr = s.recvfrom(4096)
				except socket.timeout:
					#print "XBMC2: Broadcast timeout"
					continue
				except socket.error:
					eg.PrintError('XBMC2: socket.error: ')
					import sys, traceback
					traceback.print_exc()
					continue
				except:
					eg.PrintError('XBMC2: Error: get1: ')
					import sys, traceback
					traceback.print_exc()
					continue
				if self.pluginConfig['logRawEvents']:
					print "XBMC2: Raw event: %s %s" % (repr(message), repr(addr))
				if self.pluginConfig['XBMC']['ip'] != addr[0]:
					if self.pluginConfig['XBMC']['ip'] == '127.0.0.1':
						if not addr[0] in socket.gethostbyname_ex('')[2]: continue
					else:
						continue
				"""
				if self.pluginConfig['Broadcast']['workaround']:
					s.settimeout(0)
					try:
						message2 = ''
						addr2 = ''
						if self.pluginConfig['logRawEvents']:
							message2, addr2 = s.recvfrom(4096)
							print "XBMC2: Raw event2: %s %s" % (repr(message2), repr(addr2))
						else:
							s.recvfrom(4096)
					except:
						eg.PrintError('XBMC2: Error: get2')
					try:
						message2 = ''
						addr2 = ''
						if self.pluginConfig['logRawEvents']:
							message2, addr2 = s.recvfrom(4096)
							print "XBMC2: Raw event3: %s %s" % (repr(message2), repr(addr2))
						else:
							s.recvfrom(4096)
					except:
						eg.PrintError('XBMC2: Error: get3')
				"""
				import re
				parts = re.sub('<[^<]+?>', '', message).split(';', 1)
				try:
					event, payload = parts[0].split(':', 1)
					if event != 'OnAction':
						event += '.' + payload.split(':', 1)[0]
					else:
						try:
							event += '.' + ActionList[payload.split(':', 1)[0]]
						except:
							event += '.' + payload.split(':', 1)[0]
					try:
						payload = unicode(payload.split(':', 1)[1], 'UTF8')
					except:
						payload = None
				except:
					event = parts[0].split(':', 1)[0]
					payload = None
				if not stopBroadcastEvents.isSet():
					self.TriggerEvent('Broadcast.' + event, payload)

			s.close()
			print 'XBMC2: Not listening for XBMC broadcast events'
