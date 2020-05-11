# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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
    version="3.0",
    createMacrosOnAdd=True,
)


import ctypes


class SendAction(eg.ActionBase):

    def __call__(self):
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

        hwnds = []

        # Main window
        hwndMainWindow = ctypes.windll.user32.FindWindowA(None, "PowerDVD")
        if hwndMainWindow:
            hwnds.append(hwndMainWindow)

        # Player window
        if hwndMainWindow:
            hwndPlayerWindow = ctypes.windll.user32.FindWindowExA(
                hwndMainWindow, 0, 0, 0)
            if hwndPlayerWindow:
                hwnds.append(hwndPlayerWindow)

        if hwnds:
            eg.SendKeys(hwnds[-1], self.value)
        else:
            raise self.Exceptions.ProgramNotRunning


ACTION_LIST = (
    (eg.ActionGroup, 'AudioActions', 'Audio Actions', 'Audio Actions', (
        (SendAction, "fnVolumeUp", "Volume Up", "Increase audio volume.", "+"),
        (SendAction, "fnVolumeDown", "Volume Down", "Decrease audio volume.", "-"),
        (SendAction, "fnToggleMute", "Toggle Mute", "Mute on/off.", "q"),
        (SendAction, "fnSwitchAudioChannels", "Switch Audio Channels",
         "Switch among available audio channels.", "h"),
        (SendAction, "fnToggleSecondaryAudio", "Toggle Secondary Audio",
         "Enable/disable secondary audio for Blu-ray Disc movies.", "{Ctrl+d}"),
    )),
    (eg.ActionGroup, 'VideoPlayActions', 'Video Play Actions', 'Video Play Actions', (
        (SendAction, "fnTogglePlayPause", "Toggle Play/Pause",
         "Play/pause media playback.", "{Space}"),
        (SendAction, "fnStop", "Stop", "Stop playback.", "s"),
        (SendAction, "fnFastForward", "Fast Forward",
         "Fast forward through media content. Press repeatedly to increase the fast forward speed.", "f"),
        (SendAction, "fnSlowForward", "Slow Forward",
         "Slow forward through media content. Press repeatedly to increase the slow forward speed.", "}"),
        (SendAction, "fnStepForward", "Step Forward",
         "Pause playback and go to the next frame of video. Press repeatedly to step forward through media one frame at a time.", "t"),
        (SendAction, "fnRewind", "Rewind",
         "Reverse through media content. Press repeatedly to increase the reverse speed.", "b"),
        (SendAction, "fnStepBackward", "Step Backward",
         "Pause playback and step backward. Press repeatedly to step backward through video content. Note: this feature is not available for some video file formats.", "e"),
        (SendAction, "fnNextChapter", "Next Chapter",
         "Go to the next chapter or media file in a playlist/folder. Also go to next song on a music disc.", "n"),
        (SendAction, "fnPreviousChapter", "Previous Chapter",
         "Return to previous chapter or media file in a playlist/folder. Also return to previous song on a music disc.", "p"),
        (SendAction, "fnJumpBack8Seconds", "Jump back 8 seconds",
         "Jump back 8 seconds.", "{Ctrl+Left}"),
        (SendAction, "fnJumpForward30Seconds", "Jump forward 30 seconds",
         "Jump forward 30 seconds.", "{Ctrl+Right}"),
        (SendAction, "fnNextViewingAngle", "Next Viewing Angle",
         "Go to next available angle.", "a"),
        (SendAction, "fnToggleSecondaryVideo", "Toggle Secondary Video",
         "Enable/disable secondary video.", "{Ctrl+v}"),
    )),
    (eg.ActionGroup, 'VideoSubtitleActions', 'Video Subtitle Actions', 'Video Subtitle Actions', (
        (SendAction, "fnTogglePrimarySubtitles", "Toggle Primary Subtitles And Language",
         "Enable/disable primary subtitles, toggle through languages.", "{Ctrl+g}"),
        (SendAction, "fnToggleSecondarySubtitles", "Toggle Secondary Subtitles And Language",
         "Enable/disable secondary subtitles, toggle through languages.", "{Ctrl+u}"),
        (SendAction, "fnToggleEnhancedSubtitles", "Toggle Enhanced Subtitles And Language",
         "Enable/disable enhanced subtitles, toggle through languages.", "{Ctrl+u}"),
        (SendAction, "fnChangeSecondarySubtitlesPosition", "Change Secondary Subtitles Position",
         "Change secondary subtitles position (Read-it-Clearly).", "{Ctrl+y}"),
    )),
    (eg.ActionGroup, 'VideoMenuActions', 'Video Menu Actions', 'Video Menu Actions', (
        (SendAction, "fnDVDRootMenu", "DVD Root Menu",
         "Go to the DVD root menu.", "j"),
        (SendAction, "fnAllDiscMenus", "All Disc Menus",
         "Access a menu that lets you quickly jump to one of the available disc menus.", "l"),
        (SendAction, "fnPlaybackMenu", "Playback Menu",
         "Displays the playback menu.", "{Ctrl+p}"),
        (SendAction, "fnResumePlaybackFromInteractiveMenu", "Resume Playback From Interactive Menu",
         "When the video playback is paused, but the interactive menu is active, this will resume the video.", "{Ctrl+w}"),
        (SendAction, "fnGoToBookmark", "Go To Bookmark", "Go to bookmark.", "g"),
        (SendAction, "fnDVDMenu", "DVD Menu",
         "Provides access to DVD menu controls during DVD playback. During Blu-ray Disc playback pressing this button will display the pop-up menu.", "m"),
        (SendAction, "fnMenuUp", "Menu Up", "Navigate up in menus.", "r"),
    )),
    (eg.ActionGroup, 'PictureActions', 'Picture Actions', 'Picture Actions', (
        (SendAction, "fnRotateCounterclockwise", "Rotate Counterclockwise",
         "Rotate photo 90 degrees in the counterclockwise direction.", "{Ctrl+,"),
        (SendAction, "fnRotateClockwise", "Rotate Clockwise",
         "Rotate photo/video 90 degrees in the clockwise direction.", "{Ctrl+.}"),
        (SendAction, "fnSnapshot", "Snapshot",
         "Take a photo snapshot.", "{Ctrl+c}"),
    )),
    (eg.ActionGroup, 'MusicActions', 'Music Actions', 'Music Actions', (
        (SendAction, "fnRepeat", "Repeat",
         "Repeat one or all of the media files in a folder/playlist.", "{Ctrl+r}"),
        (SendAction, "fnShuffle", "Shuffle", "Turn music shuffle on/off.", "v"),
        (SendAction, "fnSwitchKaraokeModes", "Switch Karaoke Modes",
         "Switches among karaoke modes.", "k"),
        (SendAction, "fnMiniPlayer", "Mini Player",
         "Switch to Mini Player mode during music playback.", "{Ctrl+m}"),
        (SendAction, "fnA-BRepeatDialogWindow", "A-B Repeat Dialog Window",
         "Open A-B Repeat dialog window.", "x"),
    )),
    (eg.ActionGroup, 'NavigationActions', 'Navigation Actions', 'Navigation Actions', (
        (SendAction, "fnLeft", "Left", "Navigate left in menus.", "{Left}"),
        (SendAction, "fnRight", "Right",
         "Navigate right in menus.", "{Right}"),
        (SendAction, "fnUp", "Up", "Navigate up in menus.", "{Up}"),
        (SendAction, "fnDown", "Down", "Navigate down in menus.", "{Down}"),
        (SendAction, "fnEnter", "Enter",
         "Accepts the selected option when using the arrow keys to navigate menus.", "{Enter}"),
        (SendAction, "fnCloseActiveDialogOrExitFullscreen", "Close Active Dialog Or Exit Fullscreen",
         "Close active dialog or exit full screen mode.", "{Esc}"),
        (SendAction, "fnGreenButton", "Green Button",
         "Green button on a remote control.", "{F10}"),
        (SendAction, "fnYellowButton", "Yellow Button",
         "Yellow button on a remote control.", "{F11}"),
        (SendAction, "fnBlueButton", "Blue Button",
         "Blue button on a remote control.", "{F12}"),
        (SendAction, "fnRedButton", "Red Button",
         "Red button on a remote control.", "{F9}"),
    )),
    (eg.ActionGroup, 'ProgramManagementActions', 'Program Management Actions', 'Program Management Actions', (
        (SendAction, "fnMaximize", "Maximize",
         "Maximize the CyberLink PowerDVD program.", "{F5}"),
        (SendAction, "fnMinimize", "Minimize",
         "Minimize the CyberLink PowerDVD program.", "{Ctrl+n}"),
        (SendAction, "fnToggleFullscreen", "Toggle Fullscreen",
         "Toggle playback to/from full screen mode.", "z"),
        (SendAction, "fnIncreaseScreenBrightness", "Increase Screen Brightness",
         "Increase screen brightness on supported displays.", "{Ctrl+Up}"),
        (SendAction, "fnDecreaseScreenBrightness", "Decrease Screen Brightness",
         "Decrease screen brightness on supported displays.", "{Ctrl+Down}"),
        (SendAction, "fnEjectDisc", "Eject Disc",
         "Eject the disc in the selected disc drive.", "{Ctrl+e}"),
        (SendAction, "fnSettings", "Settings",
         "Open the PowerDVD settings window.", "{Ctrl+Shift+c}"),
        (SendAction, "fnHelp", "Help", "Open PowerDVD help.", "{F1}"),
        (SendAction, "fnAbout", "About",
         "Open the About PowerDVD window.", "{Ctrl+Shift+a}"),
        (SendAction, "fnAccessUpgradeInfo", "Access Upgrade Info",
         "Access PowerDVD upgrade information dialog.", "i"),
        (SendAction, "fnClose", "Close PowerDVD",
         "Close PowerDVD.", "{Alt+F4}"),
    ))
)


class PowerDVD(eg.PluginBase):

    def __init__(self):
        self.AddActionsFromList(ACTION_LIST)
