import eg
    
class PluginInfo(eg.PluginInfo):
    name = "Zoom Player"
    author = "Bitmonster"
    version = "1.0.0"
    kind = "program"
    description = """
Adds support functions to control the famous Zoom Player.

<p>
<b>Notice:</b><br>
To make it work, you have to enable TCP control in Zoom Player. Either enable it
in the options of Zoom Player under:
<p>
<i>Option/Setup => Values & Tools => Interface => Enable External TCP Control</i>
<P>
or call the executable with the option <i>/TCP:[port]</i>
<p>
<b>Hint:</b><br>
Disable scroll acceleration in Zoom Player. Otherweise scrolling in navigators 
might be jumpy if you use autorepeat in EventGhost (which has a more 
sophisticated scroll acceleration). You find the setting in Zoom Player under:<br>
<i>Option/Setup => OSD => Navigators => Settings => Disable Scroll Acceleration</i>
"""

# ===================================================================
# ZoomPlayer TCP/IP Interface
# ===================================================================

"""\
 When the SendMessage interface is used, the message number is returned
on the "WParam" value and the message content is returned on the "LParam"
value.  If the LParam contain a string, it is stored as an ATOM String.

When the TCP interface is used, the message number is always returned/sent
as a 4-digit code. The message content is seperated by a space character
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
1100 - TimeLine update               | String containing timeline data
1110 - Current Duration              | Current Duration in milliseconds
1120 - Current Position              | Current Position in milliseconds
1200 - OSD Message                   | String containing the OSD message
1201 - OSD Message Off               | No value, message just tells that the OSD
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
1600 - DVD Audio Change              | Current Audio Track
1601 - DVD Audio Count               | Number of Audio Tracks
1602 - DVD Audio Name                | Contains the name of the Audio track and a
                                       padded number for example "001 5.1 AC3"
1700 - DVD Sub Change                | Current Subtitle Track
1701 - DVD Sub Count                 | Number of Subtitle Tracks
1702 - DVD Audio Name                | Contains the name of the Subtitle track and a
                                       padded number for example "001 5.1 AC3"
1750 - DVD Angle Change              | Current Angle
1751 - DVD Angle Count               | Number of Angles in the DVD Title
1800 - Currently Loaded File         | String containing file name
1810 - Current Play List             | String containing the Zoom Player Play List
                                       structure.  Each entry is separated by the
                                       ">" character.  Each entry is sub-divided
                                       into additional information:
                                       |N .. |n - Name
                                       |E .. |e - Extension
                                       |D .. |d - Date
                                       |S .. |s - Size
                                       |P .. |p - Path
                                       |R .. |r - Duration
                                       |F .. |f - Forced Duration
                                       It is possible addtional tags will be used
                                       in future version, so code safely.
1855 - End of File                   | End of file has been reached
1900 - File PlayList Pos             | String containing file
                                       position in play list
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
                                        8 - Play List Navigator
                                        9 - Resize Navigator
                                       10 - Station Navigator
                                       11 - Web URL Navigator
3110 - Nav Dialog Closed             | A Navigator Dialog has closed
                                       (Values are the same as #3100)
3200 - Screen Saver Mode             | The ZP Screen Saver has:
                                       0 - Started
                                       1 - Ended
5100 - ZP Function Called            | Value contains name of function
5110 - ZP ExFunction Called          | Value contains name of function
5120 - ZP ScanCode Called            | Value contains ScanCode.


External Messages (Program -> ZP, TCP/IP only)
Messages that contain parameters should be space seperated,
for example: "5100 fnPlay"
and a comma used to seperate multiple parameters,
for example: "5110 exSetAR,1".

0000 - Get Application Name          | Returns 0000 message
0001 - Get Version                   | Returns 0001 message
1000 - Get Play State                | Returns 1000 message
1010 - Get Fullscreen State          | Returns 1010 message
1110 - Get Current Duration          | Returns 1110 message
1120 - Get Current Position          | Returns 1120 message
1200 - Show a PopUp OSD Text         | Parameter is a UTF8 encoded text to be
                                       shown as a PopUp OSD
1201 - Temp Disable PopUp OSD        | Temporarily Disables the PopUp OSD
1202 - Re-Enable PopUp OSD           | Re-Enables the PopUp OSD
1210 - Set OSD Visible Duration      | Value in Seconds
1300 - Get Play Mode                 | Returns 1300 message
1400 - Request DVD Title             | Returns 1400 message
1401 - Request DVD Title Count       | Returns 1401 message
1420 - Request DVD Menu Mode         | Returns 1420 message
1500 - Request DVD Chapter           | Returns 1500 message
1501 - Request DVD Chapter Count     | Returns 1501 message
1600 - Request DVD Audio             | Returns 1600 message
1601 - Request DVD Audio Count       | Returns 1601 message
1602 - Request DVD Audio Names       | Returns 1602 message
1603 - Set DVD Audio Track           | Set the DVD's Audio Track
                                       Valid values 0-7 or 15 for default track
1700 - Request DVD Subtitle          | Returns 1700 message
1701 - Request DVD Subtitle Count    | Returns 1701 message
1702 - Request DVD Subtitle Names    | Returns 1702 message
1703 - Set DVD Subtitle Track        | Set the DVD's Subtitle Track
                                       Valid values 0-31, also enables subtitle
1704 - Hide DVD Subtitle             | Disable DVD Subtitles from showing
1750 - Request DVD Angle             | Returns 1750 message
1751 - Request DVD Angle Count       | Returns 1751 message
1753 - Set DVD Angle                 | Set the DVD's Angle
                                       Valid Values 1-9
1800 - Request File Name             | Returns 1800 message
1810 - Request Play List             | Returns 1810 message
1850 - Play File                     | Play a Media File, Value is a UTF8 encoded
                                       string containing the file name.
1900 - Get Play List Index           | Returns 1900 message
1910 - Set Play List Index           | Value from 0 to Number items in
                                       the play list-1 (plays the file in index).
1920 - Clear Play List               | Clears the Current Play List
                                       (will close any playing file)
1930 - Add Play List File            | Add a file to the Play List
1940 - Select Play List Item         | Select an Item in the Play List
1941 - DeSelect Play List Item       | Remove selection of a Play List item
2200 - Request AR Mode               | Request the current ZP AR Mode
2210 - Request DVD AR Mode           | Request the DVD AR Mode (see outgoing #2210)
2300 - Request Audio Volume          | Request the Audio Volume Level
3000 - Dismiss ZP Error              | Close the ZP Error message (if visible).
5000 - Set Current Position          | Sets the Current Play Position (in seconds)
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
"""


import asynchat
import socket
import asyncore
import time
import threading
import new
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin


class MyCheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
                

displayList = (
('timeline', 'timeline', 'events with the current position as payload (produced every second)'),
('osd', 'OSD', 'triggered everytime the ZP OnScreenMenu pops up or disappears'),
('subtitles', 'subtitles', 'basic subtitle information'),
('subtitles2', 'subtitles complete', 'all remaining subtitle information'),
('audio', 'audio', 'basic information about the current audio track'),
('audio2', 'audio complete', 'all remaining audio track information'),
('states', 'states', 'events about the current Play State (closed, stopped, paused or playing)'),
('mode', 'play mode', 'event with the current mode (audio, DVD, media)'),
('dvdar', 'DVD aspect ratio', 'events about the current aspect ratio of the DVD'),
('navs', 'navigators', 'triggerd everytime a navigator is opened or closed'),
('remaining', 'remaining', 'all the remaing events. Event names are just numbers.')
) 

fnList = (
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
('fnSkipForward', '<b>All:</b> Skip forward a specified number of seconds.'),
('fnSkipBackward', '<b>All:</b> Skip backward a specified number of seconds.'),
('fnJumpForward', '<b>All:</b> Jump forward a specified number of seconds.'),
('fnJumpBackward', '<b>All:</b> Jump backward a specified number of seconds.'),
('fnSeekForward', '<b>All:</b> Seek forward a specified number of seconds.'),
('fnSeekBackward', '<b>All:</b> Seek backward a specified number of seconds.'),
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
)

exList = (
('exSetAR', 'Set Aspect Ratio\n<br>value = 0-6'),
('exApplyPR', 'Apply Zoom Preset\n<br>value = 0-9'),
('exSavePR', 'Save Zoom Preset\n<br>value = 0-9'),
('exChapterTrack', 'Chapter/Track Selector\n<br>value = 0-9 (Opens chapter/track dialog with 5 seconds timeout for a second key)'),
('exBlanking', 'Set Blanking Preset\n<br>value = 0-9 (Automatically enables blanking)'),
('exSetMode', 'Set Playback Mode\n<br>value = 0-Media Mode, 1-DVD Mode'),
('exInterface', 'Toggle Interfaces\n<br>value = 00-Show Control Bar<br>        01-Hide Control Bar<br>        02-Show Play List Editor<br>        03-Hide Play List Editor<br>        04-Show Chapter/Bookmark Editor<br>        05-Hide Chapter/Bookmark Editor<br>        06-Set Windowed Mode<br>        07-Set Zoom Mode<br>        08-Set Fullscreen Mode<br>        09-Show Equalizer<br>        10-Hide Equalizer'),
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
)

nvList = (
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
)

   
class ZoomPlayer_Session(asynchat.async_chat):
   
    def __init__ (self, handler, address):
        # Call constructor of the parent class
        asynchat.async_chat.__init__(self)

        # Set up input line terminator
        self.set_terminator('\r\n')

        # Initialize input data buffer
        self.buffer = ''
        self.handler = handler
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.settimeout(1.0)
        try:
            self.connect(address)
        except:
            pass


    def handle_connect(self):
        # connection succeeded
        self.handler.TriggerEvent("Connected")
         
       
    def handle_expt(self):
        # connection failed
        self.handler.dispatcher_running = False
        self.handler.TriggerEvent("NoConnection")
        self.close()


    def handle_close(self):
        # connection closed
        self.handler.dispatcher_running = False
        self.handler.TriggerEvent("ConnectionLost")
        self.close()


    def collect_incoming_data(self, data):
        # received a chunk of incoming data
        self.buffer = self.buffer + data


    def found_terminator(self):
        self.handler.ValueUpdate(self.buffer)
        self.buffer = ''
         
       

class ZoomPlayer(eg.PluginClass):
    canMultiLoad = True
   
    def __init__(self):
        self.host = "localhost"
        self.port = 4769
        self.dispatcher_running = False
        self.timeline = ""
        self.waitStr = None
        self.waitFlag = threading.Event()
        self.PlayState = -1
        self.lastMessage = {}
        self.lastSubtitleNo = 0
        self.lastSubtitlesEnabled = False
        self.lastAudioTrackNo = 0
       
        subGroup = self.AddGroup('Navigational Commands')
       
        def returnHandler(value):
            def handler(self):
                self.plugin.DoCommand(value)
            return handler
       
        for className, text, scancode in nvList:
            class Handler(eg.ActionClass):
                name = text
                description = text
                __call__ = returnHandler("5120 " + str(scancode))
            Handler.__name__ = className
            subGroup.AddAction(Handler)

        subGroup = self.AddGroup('Regular Functions')
        for action_name, text in fnList:
            class Handler(eg.ActionClass):
                name = action_name[2:]
                description = text
                __call__ = returnHandler("5100 " + action_name)
            Handler.__name__ = action_name
            action = subGroup.AddAction(Handler)
            setattr(self, action_name[2:], action)

        def returnExecute(value):
            def __call__(self, value2):
                self.plugin.DoCommand(value + value2)
            return __call__
       
        def returnGetLabel(value):
            def GetLabel(self, value2=None):
                return value + (value2 or '')
            return GetLabel
       
        subGroup = self.AddGroup('Extended Functions')
        for action_name, text in exList:
            shortDoc = text.splitlines()[0].strip()
            class Handler(eg.ActionWithStringParameter):
                name = shortDoc
                description = text
                __call__ = returnExecute("5110 " + action_name + ",")
                GetLabel = returnGetLabel(shortDoc + ": ")   
            Handler.__name__ = action_name
            action = subGroup.AddAction(Handler)
            setattr(self, action_name[2:], action)
        self.AddAction(self.MyCommand)


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
        if useNewEvents:
            self.zpEvents = self.zpEvents2
        else:
            self.zpEvents = self.zpEvents1
        
    
    def __stop__(self):
        pass


    def __close__(self):
        pass
   

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
        "2210": (
            "DvdAr",
            {
                "0": "Unknown",
                "1": "FullFrame",
                "2": "Letterbox",
                "3": "Anamorphic",
            },
        ),
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
            },
        ),
    }
                
    def ValueUpdate(self, text):
        if text == self.waitStr:
            self.waitStr = None
            self.waitFlag.set()
            return
        header = text[0:4]
        state = text[5:].decode('utf-8')
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
                self.TriggerEvent(zpEvent)
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
            self.lastAudioTrackNo = int(state)
            self.TriggerEvent("CurrentAudioTrack", int(state))
        elif header == "1601":
            self.TriggerEvent("AudioTrackCount", int(state))
        elif header == "1602":
            no = int(state[0:3])
            text = state[4:]
            self.TriggerEvent("AudioTrackName", (no, text))
            if no == self.lastAudioTrackNo:
                self.TriggerEvent("CurrentAudioTrackName", text)
        elif header == "1700":
            self.lastSubtitleNo = int(state)
            self.TriggerEvent("CurrentSubtitle", int(state))
        elif header == "1701":
            self.TriggerEvent("SubtitleCount", int(state))
        elif header == "1702":
            no = int(state[0:3])
            text = state[4:]
            self.TriggerEvent("SubtitleName", (no, text))
            if (
                self.lastSubtitlesEnabled 
                and no == self.lastSubtitleNo 
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


    def push(self, data):
        if not self.dispatcher_running:
            self.dispatcher = ZoomPlayer_Session(self, (self.host, self.port))
            self.dispatcher_running = True
        try:
            self.dispatcher.sendall(data)
        except:
            self.dispatcher_running = False
            self.TriggerEvent('close')
            self.dispatcher.close()


    def DoCommand(self, cmdstr):
        self.waitFlag.clear()
        self.waitStr = cmdstr
        self.push(cmdstr + "\r\n")
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
        useNewEvents=False
    ):
        dialog = eg.ConfigurationDialog(self)

        hostEdit = wx.TextCtrl(dialog, -1, host)       
        portEdit = eg.SpinIntCtrl(dialog, -1, port, max=65535)
        newEventCtrl = wx.CheckBox(dialog, -1, "Use new events")
        newEventCtrl.SetValue(useNewEvents)
        dialog.AddLabel("TCP/IP control host:")
        dialog.AddCtrl(hostEdit)
        dialog.AddLabel("TCP/IP control port:")
        dialog.AddCtrl(portEdit)
        dialog.AddLabel("")
        dialog.AddCtrl(newEventCtrl)
       
        if dialog.AffirmedShowModal():
            return (
                hostEdit.GetValue(), 
                portEdit.GetValue(), 
                None,
                None,
                newEventCtrl.GetValue(),
            )
    
    
    
    class MyCommand(eg.ActionWithStringParameter):
        def __call__(self, cmd):
            self.plugin.DoCommand(cmd)