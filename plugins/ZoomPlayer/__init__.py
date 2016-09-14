# -*- coding: utf-8 -*-
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

"""<rst>
Adds actions to control the famous `Zoom Player <http://www.inmatrix.com/>`_.

|

**Notice:**
To make it work, you have to enable TCP control in Zoom Player. Either enable
it in the options of Zoom Player under:

*Option/Setup => Values & Tools => Interface => Enable External TCP Control*

or call the executable with the option */TCP:[port]*

**Hint:**
Disable scroll acceleration in Zoom Player. Otherwise scrolling in
navigators might be jumpy if you use autorepeat in EventGhost (which
has a more sophisticated scroll acceleration). You find the setting
in Zoom Player under:

*Option/Setup => OSD => Navigators => Settings => Disable Scroll Acceleration*
"""

import eg

eg.RegisterPlugin(
    name = "Zoom Player",
    description = __doc__,
    author = "Bitmonster",
    version = "1.0",
    kind = "program",
    guid = "{C5E2609E-C1C4-4432-A532-EDA79A7EE41D}",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=3498",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7DAAAOwwHH"
        "b6hkAAAC5ElEQVR4nIWTz08cZRjH5z/YmTnqoZvGm2cPiKEYzSZErTXFNrHUJt68tNmW"
        "BYpL2aQeZxqbGgikRhOqDRLLQYM/Q7pZ6bBIKLhWt8tu93UDCOv8WmbdsnRmPh5AWtDE"
        "T/K9PHm+3yfvm+eRpAPk4pHY4rmIfvdsxLh7NuLuylg8F9Fz8UjsYP8e97vlaC4e0X6J"
        "y15ptIW1qbepi6/YMhdprGSwFz5GjBxv5OIR7X63HN1nLnTL0Xvn5bHSaAsb33VSyxzn"
        "Ya4ff/1rAitL4BUIHm4QbNm4S59S0l6YLDwZkr8ga+L689jpk1THWyhfeQZzshN/eQQ2"
        "pgjtLGF9mXCrSug3qP38GfkLsiZJkiQVE3JsOSF79vQJtu4co6wfpmmVsDIfIoZaMafe"
        "xa9MgDMH9SJh0yRsuqx+1NkoJuSYVEzI+uonrTSMNwlmOyhcfpp/aFplrB+HEMMvYX7f"
        "i//HbfirTLht4+VuUEzIulTqkQ3ry1fYnj1GaMQoXH6KgzQtgTUzghh9FWfmA8JGhe2N"
        "nyj1yIYkemV3M32CIHsUZl/+z4C9IPt3xOhR2LyHv1lC9MquVOlT3HpmN2Cu438CBGKk"
        "g9A28J0lKn2KK61cVAzvm9cI5t6Ahbf2/cHjJzzAylxDDLXiTPcRVr+l+eALVi4qhrTW"
        "r+juzTaC+ZPw63kK7x96bDRLWGkNceUw5udt+Ln3YPUmYXmY+u1u1voVXVpPKrHqgOI9"
        "yp6CfBJx7bmdiWkdoR/CvPEsfroN5jshn4R8kkfZU1QHFG89qeysdnVA0erjRwgXTuNM"
        "9yCGX8ScfB1/rguW3oHfeqFyHdbGCRdOUx8/QnVA0fY20R5UotYlZawx0Q7zXfDnD+AY"
        "YN/ZkWPs1Oa7aEy0Y11SxuxBZf89uCk16gyqWi2les1b7QQzZwiLVwmLVwlmztC81U4t"
        "pXrOoKq5KXW/+UlqKTXmplS9llKNWkp1d2Xs1v51zn8D3aqe3eiSdiUAAAAASUVORK5C"
        "YII="
    ),
)


#pylint: disable-msg=C0301
"""
===================================================================
    ZoomPlayer TCP/IP Interface
===================================================================

 When the SendMessage interface is used, the message number is returned
 on the "WParam" value and the message content is returned on the "LParam"
 value.  If the LParam contain a string, it is stored as an ATOM String.

 When the TCP interface is used, the message number is always returned/sent
 as a 4-digit code. The message content is separated by a space character
 following the message number.  All content is string based and UTF-8
 encoded to preserve country specific text codes.

 When sending Zoom Player TCP commands, make sure to terminate each
 command with CRLF (Ascii #13#10)..

 The default TCP/IP port is 4769, but a user can change it under
 Advanced Options / Values / Interface.

 External Messages (ZP -> Program, TCP/IP or SendMessage):

 [WParam]                             | [LParam]
 -------------------------------------+----------------------------------------------
 0000 - Application Name              | String describing the Application
 0001 - Application Version           | String with the version text
 0100 - Ping                          | Result of a call to message 0100,
                                        indicating the player is responsive
 1000 - State Change                  | 0  - Closed
                                        1  - Stopped (doesn't apply to DVD,
                                                      DVD Stop = Closed)
                                        2  - Paused
                                        3  - Playing
 1010 - Current Fullscreen State      | 0  - Windowed
                                        1  - Fullscreen
 1020 - Current FastForward State     | 0  - Disabled
                                        1  - Enabled
 1021 - Current Rewind State          | 0  - Disabled
                                        1  - Enabled
 1100 - Position update               | String containing media [Position / Duration],
                                        For example:
                                        00:00:12 / 01:02:35
 1110 - Current Duration              | Current Duration in milliseconds
 1120 - Current Position              | Current Position in milliseconds
 1130 - Current Frame Rate (realtime) | Current Realtime Frame Rate in Frames per second (FPS)
                                        Only works with DirectShow based content playback
 1140 - Estimated Frame Rate          | Estimated Frame Rate in Frames Per Second (FPS)
                                        Note, some formats don't have a frame rate so the returned
                                        value is an estimate.
 1200 - OSD Message                   | String containing the OSD message
 1201 - OSD Message Off               | No value, message just tells that the OSD window
                                        has disappeared
 1300 - Current Play Mode             | 0  - DVD Mode
                                        1  - Media Mode
                                        2  - Audio Mode
 1310 - TV/PC Mode                    | 0  - PC Mode
                                        1  - TV Mode (unused)
 1400 - DVD Title Change              | Current Title
 1401 - DVD Title Count               | Number of Titles
 1410 - DVD Domain Change             | See EC_DVD_DOMAIN_CHANGE in DirectX SDK
 1420 - DVD Menu Mode                 | 0  - Not in a Menu
                                      | 1  - In a Menu
 1450 - DVD Unique String             | Returns a unique DVD indentifer
 1500 - DVD Chapter Change            | Current Chapter
 1501 - DVD Chapter Count             | Number of Chapters
 1600 - DVD/Media Active Audio Track  | Current Audio Track Index
 1601 - DVD/Media Audio Track Count   | Number of Audio Tracks
 1602 - DVD Audio Name                | Contains the name of the Audio track and a
                                        padded number for example "001 5.1 AC3"
 1700 - DVD/Media Active Sub          | Current Subtitle Track
 1701 - DVD/Media Sub Count           | Number of Subtitle Tracks
 1702 - DVD Sub Name                  | Contains the name of the Subtitle track and a
                                        padded number for example "001 5.1 AC3"
 1704 - DVD Sub Disabled              | 0 - Sub Visible
                                      | 1 - Sub Hidden
 1750 - DVD Angle Change              | Current Angle
 1751 - DVD Angle Count               | Number of Angles in the DVD Title
 1800 - Currently Loaded File         | String containing file name
 1810 - Current Playlist              | String containing the Zoom Player Playlist
                                        structure.  Each entry is separated by the ">"
                                        character and is further sub-divided
                                        into additional sections in this structure:
                                        |T .. |t - Title
                                        |N .. |n - Name
                                        |E .. |e - Extension
                                        |D .. |d - Date
                                        |S .. |s - Size
                                        |P .. |p - Path
                                        |R .. |r - Duration
                                        |F .. |f - Forced Duration
                                        It is possible addtional tags will be used
                                        in future version, so code safely.
 1811 - Playlist Count/Change         | Triggered when the playlist is modified and returns the
                                        Number of items in updated Playlist.
 1855 - End of File                   | End of file has been reached
 1900 - File PlayList Pos             | String containing file position in playlist
 1920 - Playlist Cleared Ack.         | A notification that the playlist has been cleared
 1950 - A Play List file was removed  | String containing the file name
 2000 - Video Resolution              | String containing the
                                        video resolution (if there is one)
 2100 - Video Frame Rate              | String containing the
                                        video frame rate (if there is one)
 2200 - AR Change                     | String containing the AR String
                                        (same as OSD message)
 2210 - DVD AR Mode Change            | 0  - Unknown
                                        1  - Full-Frame
                                        2  - Letterbox
                                        3  - Anamorphic
 2300 - Current Audio Volume          | The current Audio Volume
 2400 - Media Content Tags            | Returns Media Content Strings
                                        (ID3/APE/WMA/Etc... Tags)
 2500 - A CD/DVD Was Inserted         | Returns path to drive the disc was inserted to
 2611 - Video Display Area X-Ofs      | Integer Value
 2621 - Video Display Area Y-Ofs      | Integer Value
 2631 - Video Display Area Width      | Integer Value
 2641 - Video Display Area Height     | Integer Value
 2700 - Play Rate Changed             | In Media Mode the Fast Play/Slow Motion Rate.
                                        In DVD Mode the Fast Forward/Slow Motion/Rewind Rate.
                                        Value is play rate multiplied by 1000.  For example:
                                        A value of "1500" means a play rate of "1.5".
                                        If you call a function and get this message with the
                                        play rate value unchanged, it means the function failed
                                        to change the play rate.
 2710 - Random Play State             | 0 - Disabled
                                        1 - Enabled
 3000 - ZP Error Message              | String of error messsage
                                        Note that there can be multiple errors
                                        appearing in sequence, only the last
                                        error may be visible by the user.
 3100 - Nav Dialog Opened             | A Navigator Dialog has opened
                                         0 - Blanking Navigator
                                         1 - Chapter Navigator
                                         2 - Context Navigator
                                         3 - File Navigator
                                         4 - GoTo Navigator
                                         5 - Media Library Navigator
                                         6 - MouseWheel Navigator
                                         7 - Color Control Navigator
                                         8 - Playlist Navigator
                                         9 - Resize Navigator
                                        10 - Station Navigator
                                        11 - Web URL Navigator
                                        12 - Main Navigator
                                        13 - Media Library Selection Navigator
                                        14 - Virtual Keyboard Input Navigator
                                        15 - Equalizer Navigator
                                        16 - Station Navigator
                                        17 - Confirmation Navigator
                                        18 - Play History Navigator
                                        19 - Navigation Style Navigator
                                        20 - Download Navigator
                                        21 - Information Navigator
 3110 - Nav Dialog Closed             | A Navigator Dialog has closed
                                        (Values are the same as #3100)
 3200 - Screen Saver Mode             | The ZP Screen Saver has:
                                        0 - Started
                                        1 - Ended
 4000 - Virtual Keyboard Input Result | This message contains 3 parameters separated by the
                                        "|" character.
                                        The first parameter contains a value of "0" (fail) or
                                        "1" (success).
                                        The second parameter contains the unique text identifier
                                        used in the initial 4000 call.  In the cases where the
                                        call was originated from within Zoom Player, the unique
                                        identifier is always prefixed by "vk", for example "vkRename".
                                        The third parameter contains the user entered UTF8 encoded
                                        text string.
 5100 - ZP Function Called            | Value contains name of function
 5110 - ZP ExFunction Called          | Value contains name of function
 5120 - ZP ScanCode Called            | Value contains ScanCode.

 6000 - Shared Items List             | Value contains a list of files and folder returned
                                        by the previous 6000 call.  The returned format is
                                        the same as message 1810.
 6010 - Add Shared files ack.         | This messages acknowledges that a call to message 6010
                                        has finished processing.
 9000 - Flash Mouse Click             | Used to indicate a screen position was clicked if
                                        when interactive flash mode is enabled.










 External Messages (Program -> ZP, TCP/IP only)
 Messages that contain parameters should be space separated,
 for example: "5100 fnPlay"
 and a comma used to separate multiple parameters,
 for example: "5110 exSetAR,1".

 0000 - Get Application Name          | Returns 0000 message
 0001 - Get Version                   | Returns 0001 message
 0100 - Ping                          | Returns 0100 message
 1000 - Get Play State                | Returns 1000 message
 1010 - Get Fullscreen State          | Returns 1010 message
 1100 - Set Timeline Updates (on/off) | 0 - Stop   Media Position Update messages
                                        1 - Start  Media Position Update messages
                                        2 - Resend Media Position Update messages
 1110 - Get Current Duration          | Returns 1110 message
 1120 - Get Current Position          | Returns 1120 message
 1130 - Get Current Frame Rate (FPS)  | Returns 1130 message
 1140 - Get Estimated Frame Rate (FPS)| Returns 1140 message
 1200 - Show a PopUp OSD Text         | Parameter is a UTF8 encoded text to be
                                        shown as a PopUp OSD
 1201 - Temp Disable PopUp OSD        | Temporarily Disables the PopUp OSD
 1202 - Re-Enable PopUp OSD           | Re-Enables the PopUp OSD
 1210 - Set OSD "Visible" Duration    | Value in Seconds
 1300 - Get Play Mode                 | Returns 1300 message
 1400 - Request DVD Title             | Returns 1400 message
 1401 - Request DVD Title Count       | Returns 1401 message
 1420 - Request DVD Menu Mode         | Returns 1420 message
 1450 - Request DVD Unique String     | Returns 1450 message
 1500 - Request DVD Chapter           | Returns 1500 message
 1501 - Request DVD Chapter Count     | Returns 1501 message
 1600 - Request Audio Track           | Returns 1600 message
 1601 - Request Audio Track Count     | Returns 1601 message
 1602 - Request DVD Audio Names       | Returns 1602 message
 1603 - Set Audio Track               | Set the active Audio Track
                                        Valid DVD values are 0-7 or 15 for default track
 1700 - Request Subtitle Index        | Returns 1700 message
 1701 - Request Subtitle Count        | Returns 1701 message
 1702 - Request DVD Subtitle Names    | Returns 1702 message
 1703 - Set Subtitle Track            | Set the DVD's Subtitle Track
                                        Valid values 0-31, also enables subtitle
 1704 - Hide Subtitles                | Disable Subtitles from showing
 1750 - Request DVD Angle             | Returns 1750 message
 1751 - Request DVD Angle Count       | Returns 1751 message
 1753 - Set DVD Angle                 | Set the DVD's Angle
                                        Valid Values 1-9
 1800 - Request Playing File Name     | Returns 1800 message
 1810 - Request Playlist              | Returns 1810 message
 1811 - Request Playlist Count        | Returns 1811 message
 1850 - Play File                     | Play a Media File, Value is a UTF8 encoded
                                        string containing the file name.
 1852 - Close Media File              | Closes the playing media file or stops a DVD in DVD Mode.
 1860 - Browse Web                    | Browse a web page, Value is the web address (URL)
 1900 - Get Playlist Index            | Returns 1900 message
 1910 - Set Playlist Index            | Value from 0 to Number items in
                                        the playlist-1 (plays the file in index).
 1920 - Clear Playlist                | Clears the Current Playlist
                                        (will close any playing file)
 1930 - Add Playlist File             | Add a file to the Playlist
 1940 - Select Playlist Item          | Select an Item in the Playlist
                                        Value from 0 to Number items in
                                        the playlist-1.
 1941 - DeSelect Playlist Item        | Remove selection of a Playlist item
                                        Value from 0 to Number items in
                                        the playlist-1.
 1950 - Remove Playlist Item          | Remove a Playlist item from the list
                                        Value from 0 to Number items in
                                        the playlist-1.
                                        Returns both an 1950 and 1900 message.
 2200 - Request AR Mode               | Request the current ZP AR Mode
 2210 - Request DVD AR Mode           | Request the DVD AR Mode (see outgoing #2210)
 2300 - Request Audio Volume          | Request the Audio Volume Level
 2600 - Set Derived Mode Aspect Ratio | Sets the aspect ratio used for Derived Aspect Ratio
                                        mode for the currentply playing video.  The aspect
                                        ratio is specified as:
                                        "Width Ratio"+"Height Ratio" left shifted 16 bits.
                                        For Example, 16:9 would be "16+9*65536" or "16+9<<16"
                                        or "16+(9 shl 16)" (the examples do the same thing
                                        in a different syntax).
 2610 - Set Video Display Area X-Ofs  | Integer Value.
 2611 - Get Video Display Area X-Ofs  | Integer Value (Returns 2611 message).
 2620 - Set Video Display Area Y-Ofs  | Integer Value.
 2621 - Get Video Display Area Y-Ofs  | Integer Value (Returns 2621 message).
 2630 - Set Video Display Area Width  | Integer Value.
 2631 - Get Video Display Area Width  | Integer Value (Returns 2631 message).
 2640 - Set Video Display Area Height | Integer Value.
 2641 - Get Video Display Area Height | Integer Value (Returns 2641 message).
 2650 - Set Player Window dimensions  | Integer Values representing the Left,Top,Width,Height position
                                        of the player window.  For example: 50,50,800,600
 2660 - Set Player on-top value       | 0 = Standard window mode
                                        1 = Player window is on-top of other windows
 2670 - Set Fullscreen Monitor        | 0 = Monitor where the player window is displayed
                                        1 = Monitor #1
                                        2 = Monitor #2
                                        3 = Monitor #3...
 2700 - Get Play Rate                 | Returns 2700 message.
 2701 - Set Play Rate                 | Set the Media Mode Fast Play/Slow Motion rate or
                                        the DVD Mode Fast Forward/Slow Motion/ Rewind rate.
                                        Value is an integer representing the play rate multiplied
                                        by 1000.  For example a value of "500" means a play rate of "0.5".
                                        Do not use negative values in media mode, it will not work.
                                        Fast Play in media mode has a speed restriction a bit over "2.0"
                                        unless Reclock is used as the audio renderer (this is a microsoft
                                        limitation due to sound driver architecture).
 2710 - Get Random Play Mode          | Returns a 2710 message.
 3000 - Dismiss ZP Error              | Close the ZP Error message (if visible).
 4000 - Virtual Keyboard Input Query  | Pop up the Virtual Keyboard interface to ask the user to input
                                        a text string.
                                        This message requires three UTF8 encoded text string parameters.
                                        The first parameter indicates a unique identifier which is returned
                                        to you in the callback message, which will help you identify which
                                        message prompted the user for input.
                                        The second parameter populates the text entry field with the specified
                                        text (you can leave this empty if you want an empty text input value.
                                        The third parameter is used to query the user for the type of input
                                        required.
                                        For example:
                                        "4000 eMail||Enter your eMail address"
                                        or to include an existing text:
                                        "4000 eMail|no@one.org|Enter your eMail address"
                                        The result is returned in a 4000 message indicating failure/success,
                                        the unique identfier and the text entered.  The entered text is returned
                                        even in the case where the user selected to cancel the operation.
 5000 - Set Current Position          | Sets the Current Play Position (in seconds.ms)
                                      | For example "122.500" will seek to 2min:2sec.500ms
 5010 - Play DVD Title                | Plays a DVD Title (depends on DVD Navigation
                                        accepting the title).
 5020 - Play DVD Title,Chapter        | Same as 5010, Plays a DVD Title at a specific
                                        chapter, value of "1,5" plays Title #1, Chapter #5
                                        (without the "" of course).
 5030 - Play DVD Chapter              | Same as 5010, Plays a DVD Chapter in the
                                        current Title.
 5100 - Call ZP Function              | Calls a Zoom Player function
                                        by name (see skinning tutorial for list)
 5110 - Call ZP ExFunction            | Calls a Zoom Player extended function
                                        by name (see skinning tutorial for list)
                                        Format "exFunctionName,Value"
 5120 - Call ZP ScanCode              | Pass a keyboard scancode number to the
                                        Zoom Player Interperter (such as VK_DOWN),
                                        this can be used to access the Navigator
                                        interfaces, pass the scancode as a parameter.
 5130 - Call ZP nvFunction            | Calls a Zoom Player navigation function
                                        by name (see skinning tutorial for list)
 6000 - List Shared Folder            | Lists the content of the shared folder specified by the "/SharePath:[Path]"
                                        Command Line Parameter.  If no value is specified, the root path is returned,
                                        if a path is specified, the content of the path (under the shared folder)
                                        is returned.  Please note that for security reasons, paths can't begin with
                                        the ".", "/" or "\" character and may not include any invalid character in
                                        the path's body (such as "|").
                                        For Example:
                                        "6000 TV\Wednesday\"
                                        If the "/SharePath" parameter is not specified, an empty message is returned.
 6010 - Add Shared files to Playlist  | Accept a list of file names separated by the "|" characters as the new playlist.
                                        The file names are appended to the end of the playlist and a 6010 message is fired
                                        off to ackknowledge that processing has ended.
                                        The 'SharePath' value is automatically added to the path of each file.
                                        For example:
                                        "6010 MyVideo.avi|MP3\MyAudio.mp3"
                                        With this example and 'SharePath' specified as "/SharePath:X:\Content\",
                                        Zoom Player will add the files to the playlist as:
                                        X:\Content\MyVideo.avi
                                        X:\Content\MP3\MyAudio.mp3
"""


FN_ACTIONS = (
('fnPlay', '<b>All:</b> Starts playback and toggles between Play & Pause states.'),
('fnPause', '<b>All:</b> Pauses video and frame advances when already paused.'),
('fnStop', '<b>Media:</b> Stops playback and goes to the beginning of the video.<br><b>DVD:</b> Stops playback and closes DVD.'),
('fnStopToFirst', '<b>Media:</b> Stop to First Item in a Play List.'),
('fnNextChapter', '<b>Media:</b> Go to Next Chapter (Internal or OGM), if no chapters are specified, advance to the next item in the Play List.<br><b>DVD:</b> Open the Next Bookmark.'),
('fnPrevChapter', '<b>Media:</b> Go to Previous Chapter (Internal or OGM), if no chapters are specified, go back to the previous item in the Play List.<br><b>DVD:</b> Open the Previous Bookmark.'),
('fnNextTrack', '<b>Media:</b> Go to the Next item on the Play List<br><b>DVD:</b> Go to the Next Chapter.'),
('fnPrevTrack', '<b>Media:</b> Go to the Previous item on the Play List.<br><b>DVD:</b> Go to the Next Chapter.'),
('fnNextFrame', '<b>All:</b> Frame Step Forward.'),
('fnPrevFrame', '<b>All:</b> Frame Step Backward.'),
('fnNextVid', '<b>Media:</b> Play the Next Video in the current directory.'),
('fnPrevVid', '<b>Media:</b> Play the Previous Video in the current directory.'),
('fnSkipForward', '<b>All:</b> Short seek forward a specified number of seconds.'),
('fnSkipBackward', '<b>All:</b> Short seek backward a specified number of seconds.'),
('fnJumpForward', '<b>All:</b> Medium seek forward a specified number of seconds.'),
('fnJumpBackward', '<b>All:</b> Medium seek backward a specified number of seconds.'),
('fnSeekForward', '<b>All:</b> Long seek forward a specified number of seconds.'),
('fnSeekBackward', '<b>All:</b> Long seek backward a specified number of seconds.'),
('fnFastForward', '<b>All:</b> Play in Fast Forward.'),
('fnRewind', '<b>All:</b> Rewind Playback.'),
('fnSlowMotion', '<b>All:</b> Play in Slow Motion.'),
('fnHalfFF', '<b>All:</b> Half Fast forward speed.'),
('fnHalfSM', '<b>All:</b> Half Slow Motion speed.'),
('fnVolUp', '<b>All:</b> Increase Volume.'),
('fnVolDown', '<b>All:</b> Decrease Volume.'),
('fnMute', '<b>All:</b> Mute Volume (ON/OFF).'),
('fnABRepeat', '<b>All:</b> Start, Stop and Cancel AB-Repeat.'),
('fnPlayEndCycle', '<b>All:</b> Cycle through the "On Play Complete" values.'),
('fnZoomAxis', '<b>All:</b> Toggles the Zoom Axis (used with Zoom-In / Zoom-Out).'),
('fnZoomIn', '<b>All:</b> Zoom into video (enlarge video area).'),
('fnZoomOut', '<b>All:</b> Zoom out of video (shrink video area).'),
('fnZoomInWidth', '<b>All:</b> Stretch the video width.'),
('fnZoomOutWidth', '<b>All:</b> Shrink the video width.'),
('fnZoomInHeight', '<b>All:</b> Stretch the video height.'),
('fnZoomOutHeight', '<b>All:</b> Shrink the video height.'),
('fnZoom', '<b>All:</b> Go into Zoom Mode.'),
('fnFullScreen', '<b>All:</b> Go Into Fullscreen Mode.'),
('fnFitSource', '<b>All:</b> Resize video area to the original video source size..'),
('fnMax', '<b>All:</b> Maximize user interface to cover work area or if in fullscreen maximize video area to cover screen.'),
('fnMinimize', '<b>All:</b> Minimize the user interface.'),
('fnARCycle', '<b>All:</b> Cycle through Aspect Ratio modes.'),
('fnRevARCycle', '<b>All:</b> Reverse Cycle through Aspect Ratio modes.'),
('fnBar', '<b>All:</b> Show / Hide the Control Bar.'),
('fnOSD', '<b>All:</b> Turn the On Screen Display ON / OFF.'),
('fnOpen', '<b>All:</b> Open File(s) for playback.'),
('fnOpenDir', '<b>All:</b> Open a Directory for playback.'),
('fnInfo', '<b>All:</b> Playback Information Dialog (some information on the playing media).'),
('fnOptions', '<b>All:</b> Open the Options Dialog.'),
('fnPresets', '<b>All:</b> Open the Video Position Preset Dialog.'),
('fnPlayList', '<b>All:</b> Show / Hide the Play List Editor.'),
('fnChapter', '<b>Media:</b> Show / Hide the Chapter Editor.<br><b>DVD:</b> Show / Hide the Bookmark Editor.'),
('fnSkin', '<b>All:</b> Show / Hide the Skin Selection dialog.'),
('fnKeyHelp', '<b>All:</b> Opens the Keyboard Hotkey Dialog (key list).'),
('fnExit', '<b>All:</b> Exit application.'),
('fnAddChapter', '<b>Media:</b> Add Current Position to the Chapter Editor.<br><b>DVD:</b> Save Current Position as a Bookmark.'),
('fnSaveChapter', '<b>Media:</b> Save Chapter List.'),
('fnDVDMode', '<b>All:</b> Switch between the Media and DVD Modes.'),
('fnDVDRootMenu', "<b>DVD:</b> Go to the DVD's Root Menu."),
('fnDVDTitleMenu', "<b>DVD:</b> Go to the DVD's Title Menu."),
('fnDVDSubMenu', "<b>DVD:</b> Go to the DVD's Subtitle Menu."),
('fnDVDAudioMenu', "<b>DVD:</b> Go to the DVD's Audio Menu."),
('fnDVDAngleMenu', "<b>DVD:</b> Go to the DVD's Angle Menu."),
('fnDVDChapterMenu', "<b>DVD:</b> Go to the DVD's Chapter Menu."),
('fnDVDMenuLeft', '<b>DVD:</b> Move left on a DVD Menu.'),
('fnDVDMenuRight', '<b>DVD:</b> Move right on a DVD Menu.'),
('fnDVDMenuUp', '<b>DVD:</b> Move up on a DVD Menu.'),
('fnDVDMenuDown', '<b>DVD:</b> Move down on a DVD Menu.'),
('fnDVDMenuSelect', '<b>DVD:</b> Activate selected Menu item.'),
('fnDVDCC', '<b>DVD:</b> Closed Captions ON / OFF.'),
('fnDVDAngle', '<b>Media:</b> Cycle through OGM Video Tracks.<br><b>DVD:</b> Cycle through DVD Angles.'),
('fnDVDSub', '<b>Media:</b> Cycle through VobSub/OGM Subtitle Tracks.<br><b>DVD:</b> Cycle through DVD Subtitle Tracks.'),
('fnAudioTrack', '<b>Media:</b> Cycle through Media Audio Tracks.<br><b>DVD:</b> Cycle through DVD Audio Tracks.'),
('fnStayOnTop', '<b>All:</b> Stay On Top ON / OFF.'),
('fnMPEG4', '<b>All:</b> MPEG4/DivX/Video Decoder Dialog (if filter is in use).'),
('fnSub', '<b>All:</b> Opens the VobSub dialog (if filter is in use).'),
('fnAudioFilter', '<b>All:</b> TFM/DeDynamic Audio Filter Dialog (if filter is in use).'),
('fnIncRate', '<b>All:</b> Increase Play rate.'),
('fnDecRate', '<b>All:</b> Decrease Play rate.'),
('fnPrevFilterFile', 'None: Previous Manual Filter File ** disabled **'),
('fnNextFilterFile', 'None: Next Manual Filter File ** disabled **'),
('fnSaveDF', '<b>All:</b> Save Definition File for the currently open media.'),
('fnFrameCapture', '<b>All:</b> Screenshot / Frame Capture.'),
('fnPattern', '<b>All:</b> Cycle Pattern Modes.'),
('fnEject', '<b>All:</b> Eject the specified CD drive.'),
('fnOverlayControl', '<b>All:</b> Show / Hide the Overlay Color Control Interface.'),
('fnOverlayApply', '<b>All:</b> Apply the Overlay Color Controls (same as button in options).'),
('fnOverlayReset', '<b>All:</b> Reset the Overlay Color Controls back to their default settings.'),
('fnIncBrightness', '<b>All:</b> Increase Overlay Brightness.'),
('fnDecBrightness', '<b>All:</b> Decrease Overlay Brightness.'),
('fnIncContrast', '<b>All:</b> Increase Overlay Contrast.'),
('fnDecContrast', '<b>All:</b> Decrease Overlay Contrast.'),
('fnIncGamma', '<b>All:</b> Increase Overlay Gamma.'),
('fnDecGamma', '<b>All:</b> Decrease Overlay Gamma.'),
('fnIncHue', '<b>All:</b> Increase Overlay Hue.'),
('fnDecHue', '<b>All:</b> Decrease Overlay Hue.'),
('fnIncSaturation', '<b>All:</b> Increase Overlay Saturation.'),
('fnDecSaturation', '<b>All:</b> Decrease Overlay Saturation.'),
('fnUnpause', '<b>All:</b> Unpause the video (Discrete Play).'),
('fnAddALBookmark', '<b>DVD:</b> Add DVD Auto-Load Bookmark.'),
('fnSeekToStart', '<b>All:</b> Seek to start of Video.'),
('fnAudioDecoder', '<b>All:</b> Pop the property dialog of filters with "Audio Decoder" in their titles.'),
('fnDVDMenuPrev', '<b>DVD:</b> Return from DVD Sub-Menu. If on Top Menu then Resume playback.'),
('fnChapterNav', '<b>Media:</b> Show / Hide the Chapter Navigator dialog.<br><b>DVD:</b> Show / Hide the Bookmark Navigator dialog.'),
('fnPlayListNav', '<b>All:</b> Show / Hide the Play List Navigator dialog.'),
('fnFileNav', '<b>All:</b> Show / Hide the File Navigator dialog.'),
('fnBlankingNav', '<b>All:</b> Show / Hide the Blanking Navigator dialog.'),
('fnBlankingPreset', '<b>All:</b> Show / Hide the Blanking Presets dialog.'),
('fnBlanking', '<b>All:</b> Show / Hide Video Blanking.'),
('fnRandomPlay', '<b>Media:</b> Turns Random (shuffle) Play ON / OFF.'),
('fnResizeNav', '<b>All:</b> Show / Hide the Resize Navigator dialog.'),
('fnDisableDVDSub', '<b>Media:</b> Disable VobSub / OGG Subtitles.<br><b>DVD:</b> Disable DVD Subtitle.'),
('fnPresetCycle', '<b>All:</b> Cycle through Video Position Presets.'),
('fnRevPresetCycle', '<b>All:</b> Reverse Cycle through Video Position Presets.'),
('fnBlankCycle', '<b>All:</b> Cycle through Blanking Position Presets.'),
('fnRevBlankCycle', '<b>All:</b> Reverse Cycle through Blanking Position Presets.'),
('fnDVDPlayStart', '<b>DVD:</b> Play DVD bypassing Auto-Bookmark loading features.'),
('fnNextArrowFunc', '<b>All:</b> Next Active Arrow Control function.'),
('fnPrevArrowFunc', '<b>All:</b> Previous Active Arrow Control function.'),
('fnAutoARToggle', '<b>DVD:</b> Enable / Disable Automatic DVD Aspect Ratio.'),
('fnFrameZeroALBM', '<b>DVD:</b> Attempt setting a DVD Auto-Load bookmark at frame zero.'),
('fnPauseAtEOF', '<b>Media:</b> Pause Playback at end of currently playing file.'),
('fnSceneCut', '<b>All:</b> Show / Hide the Scene Cut Editor.'),
('fnGoTo', '<b>All:</b> Show / Hide the GoTo Timeline dialog.'),
('fnGoToNav', '<b>All:</b> Show / Hide the GoTo Timeline Navigator interface.'),
('fnMWFuncNav', '<b>All:</b> Show / Hide the Mouse Wheel Function Navigator interface.'),
('fnLoop', '<b>Media:</b> Switch between Do Nothing and Auto Reply on Play Complete.'),
('fnBalanceLeft', '<b>All:</b> Move Audio Balance to the Left.'),
('fnBalanceRight', '<b>All:</b> Move Audio Balance to the Right.'),
('fnOpenDrive', '<b>All:</b> Open an entire drive.'),
('fnMediaNav', '<b>All:</b> Show / Hide the Media Library Navigator.'),
('fnMediaPathEdit', '<b>All:</b> Show / Hide the Media Library Path and Category Editor.'),
('fnSrcRelStretch', '<b>All:</b> Enable / Disable Source Relative User Interface Stretch.'),
('fnZoom50', '<b>All:</b> Set video to default to 50%.'),
('fnZoom100', '<b>All:</b> Set video to default to 100%.'),
('fnZoom200', '<b>All:</b> Set video to default to 200%.'),
('fnZoom400', '<b>All:</b> Set video to default to 400%.'),
('fnZoom800', '<b>All:</b> Set video to default to 800%.'),
('fnWebNav', '<b>All:</b> Show / Hide the Web URL Navigator.'),
('fnBringToFront', '<b>All:</b> Bring Player Window to Front.'),
('fnLoopPlay', '<b>Media:</b> Enable / Disable looping of currently playing track.'),
('fnPLAddFiles', '<b>All:</b> Add Files to Play List.'),
('fnPLAddDir', '<b>All:</b> Add Directory to Play List.'),
('fnPLRemove', '<b>All:</b> Remove Selected Items from Play List.'),
('fnPLClear', '<b>All:</b> Clear the entire Play List.'),
('fnPLLoadList', '<b>All:</b> Load a Play List.'),
('fnPLSaveList', '<b>All:</b> Save the Play List.'),
('fnPLSort', '<b>All:</b> Sort the Play List Items.'),
('fnPLItemUp', '<b>All:</b> Move Selected Play List Items Up.'),
('fnPLItemDown', '<b>All:</b> Move Selected Play List Items Down.'),
('fnPLMax', '<b>All:</b> Maximize the Play List Window.'),
('fnLoadDF', '<b>All:</b> Load Definition File for the currently open media.'),
('fnRadioManager', '<b>Media:</b> Show/Hide the Radio Station Manager Dialog.'),
('fnContextNav', '<b>All:</b> Show/Hide the Context Navigator.'),
('fnPlayHistory', '<b>Media:</b> Show/Hide the Play History Interface.'),
('fnPLGetDuration', '<b>Media:</b> Get Duration of Media Files in the current Play list.'),
('fnEqualizer', '<b>All:</b> Show/Hide the Internal Equalizer Window.'),
('fnEQEditor', '<b>All:</b> Show/Hide the Equalizer Profile Selector/Editor.'),
('fnEQReset', '<b>All:</b> Reset the current Equalizer Values.'),
('fnEQToggle', '<b>All:</b> Enable/Disable the Equalizer.'),
('fnResyncAhead', '<b>All:</b> Resynchronize Audio Ahead.'),
('fnResyncBack', '<b>All:</b> Resynchronize Audio Back.'),
('fnFastPlay', '<b>Media:</b> Fast Playback with Audio.'),
('fnVobSubSelect', '<b>All:</b> DirectVobSub Subtitle File Selection.'),
('fnOpenURL', '<b>All:</b> Open URL.'),
('fnAudioMode', '<b>Media:</b> Switch to Audio only mode (no video area) skin.'),
('fnSSaverToggle', '<b>All:</b> Internal Screen Saver Toggle.'),
('fnTVMode', 'None: Not implemented.'),
('fnSpace', '<b>All:</b> Call the user-selected Space function.'),
('fnIncHeight', '<b>All:</b> Increase Height 1 Pixel.'),
('fnDecHeight', '<b>All:</b> Decrease Height 1 Pixel.'),
('fnIncWidth', '<b>All:</b> Increase Width 1 Pixel.'),
('fnDecWidth', '<b>All:</b> Decrease Width 1 Pixel.'),
('fnDummy', '<b>All:</b> Does nothing, useful for skinning.'),
('fnSceneCutToggle', '<b>All:</b> Enable/Disable the Scene Cut feature.'),
('fnStationNav', '<b>All:</b> Show/Hide the Station Navigator.'),
('fnVidLeft', '<b>All:</b> Move Video Position to the Left.'),
('fnVidRight', '<b>All:</b> Move Video Position to the Right.'),
('fnVidUp', '<b>All:</b> Move Video Position Upwards.'),
('fnVidDown', '<b>All:</b> Move Video Position Downwards.'),
('fnPLItemDir', '<b>All:</b> Open the directory of the currently highlighted item in the play list.'),
('fnDateTime', '<b>All:</b> OSD-Popup of the current Date & Time.'),
('fnSubSyncAhead', '<b>Media:</b> (Only with DirectVobSub) Resynch Subtitles Ahead 10ms.'),
('fnSubSyncBack', '<b>Media:</b> (Only with DirectVobSub) Resynch Subtitles Back 10ms.'),
('fnSubUp', '<b>Media:</b> (Only with DirectVobSub) Move Subtitles Up 1 percent.'),
('fnSubDown', '<b>Media:</b> (Only with DirectVobSub) Move Subtitles Down 1 percent.'),
('fnPLControl', '<b>All:</b> Open/Close the Play List Control interface.'),
('fnPLMagToggle', "<b>All:</b> Toggle the Play List Editor's Magnetic Docking."),
('fnEQMagToggle', "<b>All:</b> Toggle the Equalizer's Magnetic Docking."),
('fnIncPreAmp', "<b>All:</b> Increase PreAmp Volume."),
('fnDecPreAmp', "<b>All:</b> Decrease PreAmp Volume."),
('fnMainNav', "<b>All:</b> Show/Hide the Main Navigator."),
('fnLibCategoryNav', "<b>All:</b> Show/Hide the Media Library Category Navigator."),
('fnPrevDirFileExt', "<b>Media:</b> Play Previous file in the directory with the same File Extension."),
('fnNextDirFileExt', "<b>Media:</b> Play Next file in the directory with the same File Extension."),
('fnCBarButToggle', "<b>All:</b> Show/Hide the Control Bar Buttons."),
('fnDeleteCurrent', "<b>Media:</b> Delete the Currently Playing file."),
('fnPLtoTop', "<b>All:</b> Move selected Play List items to top of list."),
('fnPLtoBottom', "<b>All:</b> Move selected Play List items to bottom of list."),
('fnEQNav', "<b>All:</b> Show/Hide the Equalizer Navigator."),
('fnPlayHistoryNav', "<b>All:</b> Show/Hide the Play History Navigator."),
('fnCloseNavs', "<b>All:</b> Close All Navigators."),
('fnLastNav', "<b>All:</b> Open/Close the last open navigator."),
('fnPrevDVDTitle', "<b>DVD:</b> Go to Previous DVD Title."),
('fnNextDVDTitle', "<b>DVD:</b> Go to Next DVD Title."),
('fnContactSheet', "<b>Media:</b> Open the Contact Sheet dialog."),
('fnReloadCurrent', "<b>Media:</b> Reload the currently open media file."),
('fnBlankMonitors', "<b>All:</b> Blank (cover with a black window) non-Active monitors."),
('fnFSActMonitor', "<b>All:</b> Fullscreen on active monitor."),
('fnDownloadNav', "<b>All:</b> Download Manager Navigator (show/hide)."),
('fnPosToClipboard', "<b>All</b> Copy the current position to the Windows Clipboard"),
('fnInfoNav', "<b>All</b> Information Navigator (show/hide)"),
('fnSaveFileAs', "<b>All</b> Save currently playing file"),
('fnDoSearch', "<b>All</b> Unused at this time"),
('fnSearchList', "<b>All</b> Unused at this time"),
('fnDeInterlace', "<b>All</b> DeInterlace Video (enabled/disabled)"),
('fnSharpen', "<b>All</b> Sharpen Video (enabled/disabled)"),
('fnOpenWebPage', "<b>All</b> Open Web Page Dialog"),
('fnRingTone', "<b>All</b> Create a RingTone from a playing media section"),
('fnZoomTo43Wide', "<b>All</b> Zoom on badly encoded 16:9 content (encoded with black bars)"),
('fnVolumeWindow', "<b>All</b> Pop-up the Volume-Slider Window"),
('fnWhiteWash', "<b>All</b> WhiteWash Screen-Burn repair"),
('fnResetWindows', "<b>All</b> Reset user interface windows to their default location"),
('fnIncRateEx', "<b>All</b> Increase Play Rate by a user specified value"),
('fnDecRateEx', "<b>All</b> Decrease Play Rate by a user specified value"),
('fnZoomInLevel', "<b>All</b> Cycle Zoom-in Levels (16.6%, 33.3%, 50%, 100%)"),
('fnSkinSelectNav', "<b>All</b> Fullscreen navigation skin selection navigator (show/hide)"),
('fnResetBright', "<b>All</b> Reset Brightness to default value."),
('fnResetContrast', "<b>All</b> Reset Contrast to default value."),
('fnResetGamma', "<b>All</b> Reset Gamma to default value."),
('fnResetHue', "<b>All</b> Reset Hue to default value."),
('fnResetSatur', "<b>All</b> Reset Saturation to default value."),
('fnRandDirNedia', "<b>All</b> Random play a media file from the playing directory."),
('fnRandDirFileExt', "<b>All</b> Random play a file with the same extension from the playing directory."),
('fnSeekLongForward', "<b>All</b> Long seek forward a specified number of seconds (default 600 seconds = 10 minutes)."),
('fnSeekLongBackward', "<b>All</b> Long seek backward a specified number of seconds (default 600 seconds = 10 minutes)."),
)

EX_ACTIONS = (
('exSetAR', 'Set Aspect Ratio\n<br>value = 0-6'),
('exApplyPR', 'Apply Zoom Preset\n<br>value = 0-9'),
('exSavePR', 'Save Zoom Preset\n<br>value = 0-9'),
('exChapterTrack', 'Chapter/Track Selector\n<br>value = 0-9 (Opens chapter/track dialog with 5 seconds timeout for a second key)'),
('exBlanking', 'Set Blanking Preset\n<br>value = 0-9 (Automatically enables blanking)'),
('exSetMode', 'Set Playback Mode\n<br>value = 0-Media Mode, 1-DVD Mode'),
('exInterface', 'Toggle Interfaces\n<br>value = 00-Show Control Bar<br>        01-Hide Control Bar<br>        02-Show Play List Editor<br>        03-Hide Play List Editor<br>        04-Show Chapter/Bookmark Editor<br>        05-Hide Chapter/Bookmark Editor<br>        06-Set Windowed Mode<br>        07-Set Zoom Mode<br>        08-Set Fullscreen Mode<br>        09-Show Equalizer<br>        10-Hide Equalizer<br>        11-Enable Pop-up OSD messages<br>        12-Disable Pop-up OSD messages'),
('exSetPlayRate', 'Set Media Play Rate\n<br>value = 1-22670 (where 10000 = Standard Play)'),
('exSetCustomAR', 'Set Custom Aspect Ratio\n<br>value = 0-9 (Automatically switches AR to Custom mode)'),
('exOverlayColor', 'Set Color Control Preset\n<br>value = 0-9'),
('exPlayComplete', 'Set Play Complete Mode\n<br>value = 0-6 (may expand in a future version)'),
('exDVDNumPad', 'Select DVD Number Pad\n<br>value = 0-9'),
('exOpenDrive', 'Open an entire drive\n<br>value = 0-25 (0 = A:, 2 = C: ... 25 = Z:)'),
('exSeekAhead', 'Seek Ahead [n] Seconds\n<br>value = 1-999999999'),
('exSeekBack', 'Seek Back [n] Seconds\n<br>value = 1-999999999'),
('exSeekTo', 'Seek to Position [n] Sec\n<br>value = 1-999999999'),
('exGroupToggle', 'Toggle Skin Groups\n<br>value = 0-1^32 (Bitmask indicating which groups to toggle)'),
('exGroupEnable', 'Enable Skin Groups\n<br>value = 0-1^32 (Bitmask indicating which groups to enable)'),
('exGroupDisable', 'Disable Skin Groups\n<br>value = 0-1^32 (Bitmask indicating which groups to disable)'),
('exGroupSet', 'Set the Skin Groups Mask\n<br>value = 0-1^32 (Bitmask indicating the group mask)'),
('exSetVolume', 'Set the Audio Volume\n<br>value = 0-100 (Percentage of volume level)'),
('exEjectDrive', 'Eject/Insert a drive\n<br>value = 0-25 (drives A-Z where 0=A and 25=Z)'),
('exEnableTCP', 'Enable TCP/IP interface\n<br>value = TCP Port number'),
('exZoomTo', 'Zoom Video Size (percent)\n<br>value = 1-1000 Zoom Video Size (percent)'),
('exTransWin', 'Set player Window Transparency\n<br>value = 1-255, where 255 = disable transparency'),
('exRandomPlay', 'Set Random Play ON/OFF\n<br>value = 0=Off, 1=On'),
('exSkinTint', 'Set the User Interface color Tint\n<br>value = RGB Integer Value (Example: "$FF0000" = Red)'),
('exSkinMode', 'Enable Skin-Specific Mode\n<br>value = 1-6, by default assigned to F4-F9 keys'),
)

NV_ACTIONS = (
('Up', 'Navigational Control Up', '38'),
('Down', 'Navigational Control Down', '40'),
('Left', 'Navigational Control Left', '37'),
('Right', 'Navigational Control Right', '39'),
('Enter', 'Navigational Control Enter', '13'),
('KeyPgUp', 'Navigational Control Page Up', '33'),
('KeyPgDown', 'Navigational Control Page Down', '34'),
('KeyHome', 'Navigational Control Home', '36'),
('KeyEnd', 'Navigational Control End', '36'),
('KeyInsert', 'Navigational Control Insert', '45'),
('KeyDelete', 'Navigational Control Delete', '46'),
('KeyBackspace', 'Navigational Control Backspace', '8'),
('KeyEscape', 'Navigational Control Escape', '27'),
('KeyShift', 'Navigational Control Shift', '16'),
('KeyCapsLock',  'Navigational Control CAPSLOCK', '20'),
)
#pylint: enable-msg=C0301

import wx
import asynchat
import socket
import asyncore
import threading
from types import ClassType


class Text:
    tcpBox = "TCP/IP Settings"
    hostLabel = "Host:"
    portLabel = "Port:"
    eventBox = "Event generation"
    useNewEvents = "Use new events"



class ZoomPlayerSession(asynchat.async_chat):
    """
    Handles a Zoom Player TCP/IP session.
    """

    def __init__ (self, plugin, address):
        self.plugin = plugin

        # Call constructor of the parent class
        asynchat.async_chat.__init__(self)

        # Set up input line terminator
        self.set_terminator('\r\n')

        # Initialize input data buffer
        self.buffer = ''

        # create and connect a socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.RestartAsyncore()
        self.settimeout(1.0)
        try:
            self.connect(address)
        except:
            pass


    def handle_connect(self):
        """
        Called when the active opener's socket actually makes a connection.
        """
        self.plugin.TriggerEvent("Connected")


    def handle_expt(self):
        # connection failed
        self.plugin.isSessionRunning = False
        self.plugin.TriggerEvent("NoConnection")
        self.close()


    def handle_close(self):
        """
        Called when the channel is closed.
        """
        self.plugin.isSessionRunning = False
        self.plugin.TriggerEvent("ConnectionLost")
        self.close()


    def collect_incoming_data(self, data):
        """
        Called with data holding an arbitrary amount of received data.
        """
        self.buffer = self.buffer + data


    def found_terminator(self):
        """
        Called when the incoming data stream matches the termination
        condition set by set_terminator.
        """
        # call the plugins handler method
        self.plugin.ValueUpdate(self.buffer.decode('utf-8'))

        # reset the buffer
        self.buffer = ''



class NvAction(eg.ActionBase):

    def __call__(self):
        self.plugin.DoCommand("5120 " + self.value)



class FnAction(eg.ActionBase):

    def __call__(self):
        self.plugin.DoCommand("5100 " + self.value)



class ExAction(eg.ActionWithStringParameter):

    def __call__(self, param="0"):
        self.plugin.DoCommand("5110 " + self.value + "," + param)




class ZoomPlayer(eg.PluginBase):
    text = Text

    def __init__(self):
        self.host = "localhost"
        self.port = 4769
        self.isSessionRunning = False
        self.timeline = ""
        self.waitStr = None
        self.waitFlag = threading.Event()
        self.PlayState = -1
        self.lastMessage = {}
        self.lastSubtitleNum = 0
        self.lastSubtitlesEnabled = False
        self.lastAudioTrackNum = 0
        self.session = None

        group = self.AddGroup('Navigational Commands')
        for className, descr, scancode in NV_ACTIONS:
            clsAttributes = dict(name=descr, value=scancode)
            cls = ClassType(className, (NvAction,), clsAttributes)
            group.AddAction(cls)

        group = self.AddGroup('Regular Functions')
        for className, descr in FN_ACTIONS:
            clsAttributes = dict(
                name=className[2:],
                description=descr,
                value=className
            )
            cls = ClassType(className, (FnAction,), clsAttributes)
            group.AddAction(cls)

        group = self.AddGroup('Extended Functions')
        for className, descr in EX_ACTIONS:
            clsAttributes = dict(
                name=descr.splitlines()[0].strip(),
                description=descr,
                value=className
            )
            cls = ClassType(className, (ExAction,), clsAttributes)
            group.AddAction(cls)

        self.AddAction(self.MyCommand)
        self.AddEvents()


    def __start__(
        self,
        host="localhost",
        port=4769,
        dummy1=None,
        dummy2=None,
        useNewEvents=False
    ):
        self.host = host
        self.port = port
        self.lastHeader = "9999"
        if useNewEvents:
            self.zpEvents = self.zpEvents2
        else:
            self.zpEvents = self.zpEvents1


    def __stop__(self):
        if self.isSessionRunning:
            self.session.close()


    zpEvents1 = {
        "1201": "OSDClosed",
        "1300": {
            "0": "ModeDVD",
            "1": "ModeMedia",
            "2": "ModeAudio",
        },
        "1420": {
            "0": "DvdMenuOff",
            "1": "DvdMenuOn"
        },
        "2210": {
            "0": "DvdArUnknown",
            "1": "DvdArFullFrame",
            "2": "DvdArLetterbox",
            "3": "DvdArAnamorphic",
        },
        "3100": {
            "0": "BlankingNav",
            "1": "ChapterNav",
            "2": "ContextNav",
            "3": "FileNav",
            "4": "GoToNav",
            "5": "MediaNav",
            "6": "MWFuncNav",
            "7": "ColorNav",
            "8": "PlayListNav",
            "9": "ResizeNav",
            "10": "StationNav",
            "11": "WebNav",
            "12": "MainNav",
            "13": "LibCategoryNav",
            "14": "KeyNav",
            "15": "EQNav",
            "16": "StationNav",
            "17": "ConfirmNav",
            "18": "PlayHistoryNav",
            "19": "SkinSelectNav",
            "20": "DownloadNav",
            "21": "InfoNav",
        },
       "3110": "NavigatorClosed",
    }

    zpEvents2 = {
        "1000": (
            "State",
            {
                "0": "Closed",
                "1": "Stopped",
                "2": "Paused",
                "3": "Playing",
            },
        ),
        "1201": "OSDClosed",
        "1300": (
            "Mode",
            {
                "0": "DVD",
                "1": "Media",
                "2": "Audio",
            },
        ),
        "1420": (
            "DvdMenu",
            {
                "0": "Off",
                "1": "On"
            },
        ),
        "1811": "PlaylistCount",
        "2210": (
            "DvdAr",
            {
                "0": "Unknown",
                "1": "FullFrame",
                "2": "Letterbox",
                "3": "Anamorphic",
            },
        ),
        "2710": (
            "RandomPlayState",
            {
                "0": "Disabled",
                "1": "Enabled",
            }
        ),
        "3000": "ErrorMessage",
        "3100": (
            "NavigatorOpen",
            {
                "0": "Blanking",
                "1": "Chapter",
                "2": "Context",
                "3": "File",
                "4": "GoTo",
                "5": "MediaLibrary",
                "6": "MouseWheel",
                "7": "Color",
                "8": "PlayList",
                "9": "Resize",
                "10": "Station",
                "11": "WebUrl",
                "12": "Main",
                "13": "MLSelection",
                "14": "VirtualKeyboard",
                "15": "Equalizer",
                "16": "Station",
                "17": "Confirm",
                "18": "PlayHistory",
                "19": "NavigationStyle",
                "20": "Download",
                "21": "Information",
            },
        ),
        "3110": (
            "NavigatorClose",
            {
                "0": "Blanking",
                "1": "Chapter",
                "2": "Context",
                "3": "File",
                "4": "GoTo",
                "5": "MediaLibrary",
                "6": "MouseWheel",
                "7": "Color",
                "8": "PlayList",
                "9": "Resize",
                "10": "Station",
                "11": "WebUrl",
                "12": "Main",
                "13": "MLSelection",
                "14": "VirtualKeyboard",
                "15": "Equalizer",
                "16": "Station",
                "17": "Confirm",
                "18": "PlayHistory",
                "19": "NavigationStyle",
                "20": "Download",
                "21": "Information",
            },
        ),
        "3200": (
            "ScreenSaver",
            {
                "0": "Started",
                "1": "Ended",
            }
        )
    }

    def ValueUpdate(self, text):
        if text == self.waitStr:
            self.waitStr = None
            self.waitFlag.set()
            return
        header = text[0:4]
        if not header.isdigit():
            header = self.lastHeader
            state = text
        else:
            self.lastHeader = header
            state = text[5:]
        self.lastMessage[header] = state
        zpEvent = self.zpEvents.get(header, None)
        if zpEvent is not None:
            if type(zpEvent) == type({}):
                eventString = zpEvent.get(state, None)
                if eventString is not None:
                    self.TriggerEvent(eventString)
                else:
                    self.TriggerEvent(header, [state])
            elif type(zpEvent) == type(()):
                suffix2 = zpEvent[1].get(state, None)
                if suffix2 is not None:
                    self.TriggerEvent(zpEvent[0] + "." + suffix2)
                else:
                    self.TriggerEvent(zpEvent[0] + "." + str(state))
            else:
                if not state:
                    state = None
                self.TriggerEvent(zpEvent, state)
            return
        if header == "1100":
            self.TriggerEvent("Timeline", [state])
        elif header == "1200":
            self.TriggerEvent("OSD", [state])
        elif header == "1000":
            state = int(state)
            self.PlayState = state
            if state == 0:
                self.TriggerEvent("StateClosed")
            elif state == 1:
                self.TriggerEvent("StateStopped")
            elif state == 2:
                self.TriggerEvent("StatePaused")
            elif state == 3:
                self.TriggerEvent("StatePlaying")
            else:
                self.PrintError("unknown State Change")
        elif header == "1600":
            self.lastAudioTrackNum = int(state)
            self.TriggerEvent("CurrentAudioTrack", int(state))
        elif header == "1601":
            self.TriggerEvent("AudioTrackCount", int(state))
        elif header == "1602":
            num = int(state[0:3])
            text = state[4:]
            self.TriggerEvent("AudioTrackName", (num, text))
            if num == self.lastAudioTrackNum:
                self.TriggerEvent("CurrentAudioTrackName", text)
        elif header == "1700":
            self.lastSubtitleNum = int(state)
            self.TriggerEvent("CurrentSubtitle", int(state))
        elif header == "1701":
            self.TriggerEvent("SubtitleCount", int(state))
        elif header == "1702":
            num = int(state[0:3])
            text = state[4:]
            self.TriggerEvent("SubtitleName", (num, text))
            if (
                self.lastSubtitlesEnabled
                and num == self.lastSubtitleNum
            ):
                self.TriggerEvent("CurrentSubtitleName", text)
        elif header == "1704":
            self.lastSubtitlesEnabled = not bool(int(state))
            if self.lastSubtitlesEnabled:
                self.TriggerEvent("SubtitlesEnabled")
            else:
                self.TriggerEvent("SubtitlesDisabled")
                self.TriggerEvent("CurrentSubtitleName")
        else:
            self.TriggerEvent(header, [state])


    @eg.LogIt
    def DoCommand(self, cmdstr):
        self.waitFlag.clear()
        self.waitStr = cmdstr
        if not self.isSessionRunning:
            self.session = ZoomPlayerSession(self, (self.host, self.port))
            self.isSessionRunning = True
        try:
            self.session.sendall(cmdstr + "\r\n")
        except:
            self.isSessionRunning = False
            self.TriggerEvent('close')
            self.session.close()
        self.waitFlag.wait(1.0)
        self.waitStr = None
        self.waitFlag.set()


    def SetOSD(self, text):
        self.DoCommand("1200 " + text)


    def Configure(
        self,
        host="localhost",
        port=4769,
        dummy1=None,
        dummy2=None,
        useNewEvents=True
    ):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        newEventCtrl = panel.CheckBox(useNewEvents, text.useNewEvents)

        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.hostLabel, hostCtrl),
            (text.portLabel, portCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        eventBox = panel.BoxedGroup(
            text.eventBox,
            newEventCtrl,
        )
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(eventBox, 0, wx.TOP|wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                None,
                None,
                newEventCtrl.GetValue(),
            )



    class MyCommand(eg.ActionWithStringParameter):
        name = "Raw Command"

        def __call__(self, cmd):
            self.plugin.DoCommand(cmd)

