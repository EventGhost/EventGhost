# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://www.eventghost.net/>
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

import eg

eg.RegisterPlugin(
    name="CyberLink PowerDVD",
    description="Adds actions to control CyberLink PowerDVD.",
    kind="program",
    author="Bitmonster, GruberMarkus",
    guid="{4DBDFFA7-9E47-4782-B843-B196C74DE3EF}",
    version="2.0",
    createMacrosOnAdd=True,
)


AudioActions = [
    ("VolumeUp", "Volume Up", "Increase audio volume.", "+"),
    ("VolumeDown", "Volume Down", "Decrease audio volume.", "-"),
    ("ToggleMute", "Toggle Mute", "Mute on/off.", "q"),
    ("SwitchAudioChannels", "Switch Audio Channels", "Switch among available audio channels.", "h"),
    ("ToggleSecondaryAudio", "Toggle Secondary Audio", "Enable/disable secondary audio for Blu-ray Disc movies.", "{Ctrl+d}"),
]

VideoPlayActions = [
    ("TogglePlayPause", "Toggle Play/Pause", "Play/pause media playback.", "{Space}"),
    ("Stop", "Stop", "Stop playback.", "s"),
    ("FastForward", "Fast Forward", "Fast forward through media content. Press repeatedly to increase the fast forward speed.", "f"),
    ("SlowForward", "Slow Forward", "Slow forward through media content. Press repeatedly to increase the slow forward speed.", "}"),
    ("StepForward", "Step Forward", "Pause playback and go to the next frame of video. Press repeatedly to step forward through media one frame at a time.", "t"),
    ("Rewind", "Rewind", "Reverse through media content. Press repeatedly to increase the reverse speed.", "b"),
    ("StepBackward", "Step Backward", "Pause playback and step backward. Press repeatedly to step backward through video content. Note: this feature is not available for some video file formats.", "e"),
    ("NextChapter", "Next Chapter", "Go to the next chapter or media file in a playlist/folder. Also go to next song on a music disc.", "n"),
    ("PreviousChapter", "Previous Chapter", "Return to previous chapter or media file in a playlist/folder. Also return to previous song on a music disc.", "p"),
    ("JumpBack8Seconds", "Jump back 8 seconds", "Jump back 8 seconds.", "{Ctrl+Left}"),
    ("JumpForward30Seconds", "Jump forward 30 seconds", "Jump forward 30 seconds.", "{Ctrl+Right}"),
    ("NextViewingAngle", "Next Viewing Angle", "Go to next available angle.", "a"),
    ("ToggleSecondaryVideo", "Toggle Secondary Video", "Enable/disable secondary video.", "{Ctrl+v}"),
]

VideoSubtitleActions = [
    ("TogglePrimarySubtitles", "Toggle Primary Subtitles And Language", "Enable/disable primary subtitles, toggle through languages.", "{Ctrl+g}"),
    ("ToggleSecondarySubtitles", "Toggle Secondary Subtitles And Language", "Enable/disable secondary subtitles, toggle through languages.", "{Ctrl+u}"),
    ("ToggleEnhancedSubtitles", "Toggle Enhanced Subtitles And Language", "Enable/disable enhanced subtitles, toggle through languages.", "{Ctrl+u}"),
    ("ChangeSecondarySubtitlesPosition", "Change Secondary Subtitles Position", "Change secondary subtitles position (Read-it-Clearly).", "{Ctrl+y}"),
]

VideoMenuActions = [
    ("DVDRootMenu", "DVD Root Menu", "Go to the DVD root menu.", "j"),
    ("AllDiscMenus", "All Disc Menus", "Access a menu that lets you quickly jump to one of the available disc menus.", "l"),
    ("PlaybackMenu", "Playback Menu", "Displays the playback menu.", "{Ctrl+p}"),
    ("ResumePlaybackFromInteractiveMenu", "Resume Playback From Interactive Menu", "When the video playback is paused, but the interactive menu is active, this will resume the video.", "{Ctrl+w}"),
    ("GoToBookmark", "Go To Bookmark", "Go to bookmark.", "g"),
    ("DVDMenu", "DVD Menu", "Provides access to DVD menu controls during DVD playback. During Blu-ray Disc playback pressing this button will display the pop-up menu.", "m"),
    ("MenuUp", "Menu Up", "Navigate up in menus.", "r"),
]

PictureActions = [
    ("RotateCounterclockwise", "Rotate Counterclockwise", "Rotate photo 90 degrees in the counterclockwise direction.", "{Ctrl+,"),
    ("RotateClockwise", "Rotate Clockwise", "Rotate photo/video 90 degrees in the clockwise direction.", "{Ctrl+.}"),
    ("Snapshot", "Snapshot", "Take a photo snapshot.", "{Ctrl+c}"),
]

MusicActions = [
    ("Repeat", "Repeat", "Repeat one or all of the media files in a folder/playlist.", "{Ctrl+r}"),
    ("Shuffle", "Shuffle", "Turn music shuffle on/off.", "v"),
    ("SwitchKaraokeModes", "Switch Karaoke Modes", "Switches among karaoke modes.", "k"),
    ("MiniPlayer", "Mini Player", "Switch to Mini Player mode during music playback.", "{Ctrl+m}"),
    ("A-BRepeatDialogWindow", "A-B Repeat Dialog Window", "Open A-B Repeat dialog window.", "x"),
]

NavigationActions = [
    ("Left", "Left", "Navigate left in menus.", "{Left}"),
    ("Right", "Right", "Navigate right in menus.", "{Right}"),
    ("Up", "Up", "Navigate up in menus.", "{Up}"),
    ("Down", "Down", "Navigate down in menus.", "{Down}"),
    ("Enter", "Enter", "Accepts the selected option when using the arrow keys to navigate menus.", "{Enter}"),
    ("CloseActiveDialogOrExitFullscreen", "Close Active Dialog Or Exit Fullscreen", "Close active dialog or exit full screen mode.", "{Esc}"),
    ("GreenButton", "Green Button", "Green button on a remote control.", "{F10}"),
    ("YellowButton", "Yellow Button", "Yellow button on a remote control.", "{F11}"),
    ("BlueButton", "Blue Button", "Blue button on a remote control.", "{F12}"),
    ("RedButton", "Red Button", "Red button on a remote control.", "{F9}"),
]

ProgramManagementActions = [
    ("Maximize", "Maximize", "Maximize the CyberLink PowerDVD program.", "{F5}"),
    ("Minimize", "Minimize", "Minimize the CyberLink PowerDVD program.", "{Ctrl+n}"),
    ("ToggleFullscreen", "Toggle Fullscreen", "Toggle playback to/from full screen mode.", "z"),
    ("IncreaseScreenBrightness", "Increase Screen Brightness", "Increase screen brightness on supported displays.", "{Ctrl+Up}"),
    ("DecreaseScreenBrightness", "Decrease Screen Brightness", "Decrease screen brightness on supported displays.", "{Ctrl+Down}"),
    ("EjectDisc", "Eject Disc", "Eject the disc in the selected disc drive.", "{Ctrl+e}"),
    ("Settings", "Settings", "Open the PowerDVD settings window.", "{Ctrl+Shift+c}"),
    ("Help", "Help", "Open PowerDVD help.", "{F1}"),
    ("About", "About", "Open the About PowerDVD window.", "{Ctrl+Shift+a}"),
    ("AccessUpgradeInfo", "Access Upgrade Info", "Access PowerDVD upgrade information dialog.", "i"),
    ("ClosePowerDVD", "Close PowerDVD", "Close PowerDVD.", "{Alt+F4}"),
]



class ActionPrototype(eg.ActionBase):

    def __call__(self):
        #
        # Get the window handle (HWND) of the PowerDVD main window and the HWND of the PowerDVD player window.
        #     When PowerDVD is running, the main window is not hidden and always has an HWND.
        #     The player window is hidden and only exists when playback has begun.
        # Combine the two lists, the main window being the first entry.
        # If the list is empty, raise an error.
        # Else, send the key stroke to the last element in the list
        # (i.e., to the player window when playback has begun, else to the main window).
        #
        # This also works when PowerDVD is running in the background.
        #
        #
        # AutoHotKey searches HWNDs differently, requiring only two lines of code to find the window
        # and sending a key to it (also works when PowerDVD is in the background).
        # AHK code for toggling play/pause:
        #     ControlGet, OutputVar, Hwnd,,, PowerDVD
        #     ControlSend, , {space}, ahk_id %OutputVar%
        #

	gWindowMatcherMainWindow = eg.WindowMatcher('PowerDVD{*}.exe', 'PowerDVD', None, None, None, 1, "false", 0, None)
	gWindowMatcherPlayerWindow = eg.WindowMatcher('PowerDVD{*}.exe', 'PowerDVD', '{*}', '{*}', '{*}', 1, "true", 0, None)

        hwnds = gWindowMatcherMainWindow() + gWindowMatcherPlayerWindow()

        if hwnds:
            eg.SendKeys(hwnds[-1], self.value)
        else:
            raise self.Exceptions.ProgramNotRunning


class PowerDVD(eg.PluginBase):

    def __init__(self):
        group = self.AddGroup("Audio", "")
        group.AddActionsFromList(AudioActions, ActionPrototype)

        group = self.AddGroup("Video Playback", "")
        group.AddActionsFromList(VideoPlayActions, ActionPrototype)

        group = self.AddGroup("Video Subtitles", "")
        group.AddActionsFromList(VideoSubtitleActions, ActionPrototype)

        group = self.AddGroup("Video Menus", "")
        group.AddActionsFromList(VideoMenuActions, ActionPrototype)

        group = self.AddGroup("Pictures", "")
        group.AddActionsFromList(PictureActions, ActionPrototype)

        group = self.AddGroup("Music", "")
        group.AddActionsFromList(MusicActions, ActionPrototype)

        group = self.AddGroup("General Navigation", "")
        group.AddActionsFromList(NavigationActions, ActionPrototype)

        group = self.AddGroup("General Program Management", "")
        group.AddActionsFromList(ProgramManagementActions, ActionPrototype)
