# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Ralph Eisenbach
#
# This plugin is based on the plugin for ZoomPlayer
# by Lars-Peter Voss <bitmonster@eventghost.org>
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
    name = "TheaterTek",
    author = "SurFan",
    version = "0.0.1",
    kind = "program",
    guid = "{EF830DA5-EF08-4050-BAE0-D5FC0057D149}",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control <a href="http://www.theatertek.com/">TheaterTek</a>.'
        '\n\n<p><b>Notice:</b><br>'
        'To make it work, you have to enable TCP control in TheaterTek. '
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=559",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACGElEQVR42m1RPWhaURQ+"
        "gg6lCjooxnZIH9iARAi9QqwQTcBmioNQcWskwxV5i+AgDqHERZdsEfreUE3BDFJI4XUq"
        "EeqeizjUnw6CKO1SUJ4lWKR5PXotjaZ3eefv+873nafT6/XT6dRkMp1+PgUA0Svy9Ozs"
        "zfY2cbvdmLpcri/VOsyfDgiAxGP8SpgyxmSQFyUGQAjE2a0yWQJQoBL5i+MNWbeIcCAO"
        "qwCNaLMkPhsilFyTa9zjiXtmXQeAcg9AGEoB5mBwAChHk7TBYBAIBNLpNJYvUhfq1x/L"
        "Hti/7Yebh6VSCekbbxvomM+dn5df7b9cNY3ckWGkUqkgq9fgxUI2m81kMni0VqtVr9cP"
        "PPt3NjCghEpUUhTl5ONJ0BLsdrsIlmVZFEWn09lsNtHYHEABvoO0JlFKY7FYuVxGbi4m"
        "l8uFw+F8Pu/z+bCL4DkgBHRtxo0TuH0ymdjt9uMPxxs/N7BSLBbREpeMyxcA7bUGyw9t"
        "7Jp2G41Gv9/vdDpcVTKZ5JIIxcMCE64ESzCIw8OrYdfSxTLqsVqttVotkUiYzeZQKKQz"
        "Go3j8dhgMBwVjrZ+b/V6PVSMqd/vr1arGHAzKAan2+227vbb5K6Sd5/er68/xlMiIJVK"
        "CYJgs9kikQiy4ImeOTZXARyzs/McR1VVLRQKaGBv7wWy+J/O/sx/APjGD39dXio3NyrG"
        "o9EoGo0+efCIt/4ArUT50E11E2MAAAAASUVORK5CYII="
    ),
)

# ===================================================================
# TheaterTek TCP/IP Interface
# ===================================================================

"""\
IP COMMANDS
-----------

TT->AP		Sent from TT to client application
AP->TT		Sent from client application to TT
TT<-->AP	Sent from TT and can be polled by client.

Commands are sent ASCII in the form:
4 byte command, space, {parameter} CRLF

A successful command returns:
Command, space, 0
OR
Command, space, response

An unsuccessful command returns:
Command, space, -1

Example:
0000			// Client app
0000 TheaterTek DVD	// Returned value



Enum values
-----------
IP_MEDIASTATE	0=Stopped/NoMedia, 1=Playing, 2=paused, 3=FF, 4=RW
IP_FULLSCREEN	0=Minimized, 1=Windowed, 2=Fullscreen
IP_GETPRIVATE	Allows client to set/get a private string up to 1024 bytes on TT. This data persists as long as TT is running.


#define	IP_APPLICATION		0 	// TT<-->AP	Application name
#define	IP_VERSION		1 	// TT<-->AP	Application version
#define IP_FLASH		500 	// TT<-->AP	OSD Flash message
#define IP_FULLSCREEN		510 	// TT<-->AP	Fullscreen/windowed status

#define IP_MEDIASTATE		1000 	// TT<-->AP	State enum
#define IP_MEDIATIME		1010 	// TT<-->AP	Media time (hh:mm:ss / hh:mm:ss)
#define IP_MEDIAPOS		1020 	// AP->TT	Set media time (hh:mm:ss)
#define IP_ENDOFMEDIA		1030 	// TT->AP	Signals end of media
#define IP_FORMAT		1040	// TT->AP	(0=NTSC, 1=PAL)

#define IP_GETAR		1300 	// TT<-->AP	Return Current AR (name)
#define IP_ARCOUNT		1310 	// AP->TT	AR Count
#define IP_ARNAMES		1320 	// AP->TT	AR Names (name|name)
#define IP_SETAR		1330 	// AP->TT	Set Current AR (number)

#define IP_CURFILE		1400 	// TT<-->AP	Current file
#define	IP_DISKINSERTION	1410 	// TT->AP	Disk inserted
#define IP_DISKEJECTION		1420 	// TT->AP	Disk ejected

#define IP_DVDUNIQUEID		1500 	// AP->TT	DVD unique ID
#define IP_DVDTITLE		1510 	// TT<-->AP	Current Title
#define IP_DVDTITLECOUNT	1520 	// AP->TT	Title count
#define IP_DVDPLAYTITLE		1530 	// AP->TT	Play Title

#define IP_DVDCHAPTER		1600 	// TT<-->AP	Current Chapter
#define IP_DVDCHAPTERCOUNT	1610 	// AP->TT	Chapter count
#define IP_DVDPLAYCHAPTER	1620 	// AP->TT	Play chapter
#define IP_DVDPLAYTITCHAP	1630 	// AP->TT	Play Chapter in Title (Chapter Title)

#define IP_DVDAUDIO		1700 	// TT<-->AP	Current audio stream
#define IP_DVDSETAUDIO		1710 	// AP->TT	Set audio stream
#define IP_DVDAUDIOCOUNT	1720 	// AP->TT	Audio stream count
#define IP_DVDAUDIONAMES	1730 	// AP->TT	Audio stream names (name|name)

#define IP_DVDSUBTITLE		1800 	// TT<-->AP	Current subtitle stream
#define IP_DVDSETSUBTITLE	1810 	//	AP->TT	Set subtitle stream, -1 to disable
#define IP_DVDSUBTITLECOUNT 	1820 	// AP->TT	Subtitle stream count
#define IP_DVDSUBTITLENAMES	1830 	// AP->TT	Subtitle names (name|name)

#define IP_DVDANGLE		1900 	// TT<-->AP	Current angle
#define IP_DVDSETANGLE		1910 	// AP->TT	Set angle
#define IP_DVDANGLECOUNT	1920 	// AP->TT	Angle count

#define IP_DVDMENUMODE		2000 	// TT<-->AP	Menu mode
#define IP_DOMAIN		2010 	// TT->AP	DVD Domain

#define IP_GETVOLUME		2100 	// TT<-->AP	Get Current volume
#define IP_SETVOLUME		2110 	// AP->TT	Set Current volume
#define IP_GETAUDIOOUTPUT	2120 	// AP->TT	Get Current audio output
#define IP_SETAUDIOOUTPUT	2130 	// AP->TT	Set audio output

#define IP_ADDBOOKMARK		2200 	// AP->TT	Add a bookmark
#define IP_NEXTBOOKMARK		2210 	// AP->TT	Next bookmark
#define IP_PREVBOOKMARK		2220 	// AP->TT	Previous bookmark

#define IP_PLAYFILE		3000 	// AP->TT	Play file
#define IP_ADDFILE		3010 	// AP->TT	Add file to playlist
#define IP_CLEARLIST		3020 	// AP->TT	Clear playlist
#define IP_GETINDEX		3030 	// AP->TT	Current item index
#define IP_PLAYATINDEX		3040 	// AP->TT	Play item at index
#define IP_GETLISTCOUNT		3050 	// AP->TT	Current list count
#define IP_GETLIST		3060 	// AP->TT	Get playlist (name|name)
#define IP_DELATINDEX		3070 	// AP->TT	Delete file at index

#define IP_SETPRIVATE		4000 	// AP->TT	Private app string
#define IP_GETPRIVATE		4010 	// AP->TT	Private app string

#define IP_WM_COMMAND		5000 	// AP->TT	Internal command
#define IP_KEYPRESS		5010	// AP->TT	Key code
#define IP_SENDMSG		5020 	// AP->TT	Send message
#define IP_POSTMSG		5030 	// AP->TT	Post message


Auto Killer Commands
--------------------
#define IP_LAUNCH		8000 	// AP->AK
#define IP_QUIT			8010 	// AP->AK
#define IP_MOUNTDISK		8020 	// AP->AK	Changer#, Slot#
#define IP_UNMOUNTDISK		8030 	// AP->AK	Changer#  ->Slot#
#define IP_EJECTDISK		8040 	// AP->AK	Changer#, Slot#
#define IP_GETSLOTDATA		8050 	// AP->AK	Changer#, Slot#
#define IP_GETDRIVEDATA		8060 	// AP->AK	Changer#  ->DriveData
#define IP_CHECKCHANGED		8070 	// AP->AK
#define IP_REBUILDDATA		8080 	// AP->AK
#define IP_DATACHANGED		8100 	// AK->AP	Notification of data change
#define IP_COUNTCHANGERS	8110 	// AP->AK



WM_COMMANDS
-----------
#define ID_PLAY                         32771
#define ID_STOP                         32772
#define ID_PAUSE                        32773
#define ID_NEXT                         32774
#define ID_PREVIOUS                     32775
#define ID_EXIT                         32776
#define ID_FF                           32777
#define ID_RW                           32778
#define ID_MENU_LIST                    32779
#define ID_TITLE_MENU                   32780
#define ID_FF_1X                        32782
#define ID_FF_2X                        32784
#define ID_FF_5X                        32785
#define ID_FF_10X                       32786
#define ID_FF_20X                       32787
#define ID_FF_SLOW                      32788
#define ID_RW_1X                        32790
#define ID_RW_2X                        32791
#define ID_RW_5X                        32792
#define ID_RW_10X                       32793
#define ID_RW_20X                       32794
#define ID_ROOT_MENU                    32796
#define ID_AUDIO_MENU                   32797
#define ID_SUBTITLE_MENU                32798
#define ID_CHAPTER_MENU                 32799
#define ID_CC_ON                        32804
#define ID_CC_OFF                       32805
#define ID_ABOUT                        32807
#define ID_SUB_OFF                      32808
#define ID_ASPECT_DEFINE                32810
#define ID_ASPECT_ANAM                  32811
#define ID_ASPECT_NONANAM               32812
#define ID_ASPECT_LETTERBOX             32813
#define ID_BOOK_ADD                     32814
#define ID_BUTTON32819                  32819
#define ID_BUTTON32820                  32820
#define ID_ONSCREEN                     32821
#define ID_VID_BRIGHTNESS               32824
#define ID_VID_CONTRAST                 32825
#define ID_VID_HUE                      32826
#define ID_VID_SATURATION               32827
#define ID_OVERSCAN                     32828
#define ID_VID_GAMMA                    32829
#define ID_MENU_CHAPTER                 32830
#define ID_MENU_AUDIO                   32831
#define ID_MENU_ANGLE                   32832
#define ID_MENU_FF                      32833
#define ID_MENU_SUBTITLES               32834
#define ID_CLOSED_CAPTIONS              32835
#define ID_BOOK_DELETE                  32836
#define ID_ANGLE_MENU                   32837
#define ID_RESUME                       32838
#define ID_MENU_TITLE                   32839
#define ID_SETUP                        32841
#define ID_ADJUSTVIDEO                  32842
#define ID_ASPECT_LOCK                  32843
#define ID_SETSTARTPOINT                32846
#define ID_K_RETURN                     32849
#define ID_K_UP                         32850
#define ID_K_DOWN                       32851
#define ID_K_LEFT                       32852
#define ID_K_RIGHT                      32853
#define ID_K_FF                         32854
#define ID_K_RW                         32855
#define ID_K_ESCAPE                     32856
#define ID_NEXTAR                       32857
#define ID_INFO                         32858
#define ID_ARFIRST                      32859
#define ID_AR2                          32860
#define ID_AR3                          32861
#define ID_AR4                          32862
#define ID_AR5                          32863
#define ID_AR6                          32864
#define ID_AR7                          32865
#define ID_AR8                          32866
#define ID_AR9                          32867
#define ID_ARLAST                       32868
#define ID_EJECT                        32870
#define ID_CONTEXT                      32872
#define ID_ALTEXIT                      32873
#define ID_MINIMIZE                     32874
#define ID_NEXTSUB                      32875
#define ID_NEXTAUDIO                    32876
#define ID_REPLAY                       32877
#define ID_JUMP                         32878
#define ID_FRAMESTEP                    32879
#define ID_ABREPEAT                     32880
#define ID_CHAPTITREP                   32881
#define ID_NEXT_ANGLE                   32883
#define ID_OPEN                         32884
#define ID_NEXT_TIT                     32885
#define ID_STATS                        32886
#define ID_CAPTURE                      32887
#define ID_BK_RESUME                    32888
#define ID_DEINTERLACE                  32889
#define ID_VOLUP                        32891
#define ID_VOLDOWN                      32892
#define ID_NEXTDISK                     32893
#define ID_SHOWTIME                     32894
#define ID_CC_NUDGE_UP                  32895
#define ID_CC_NUDGE_DOWN                32896
#define ID_UPGRADE                      32897
#define ID_NEXT_FILE                    32898
#define ID_PREVIOUS_FILE                32899
#define ID_TSPROG                       32901
#define ID_PREV_TIT                     32902
#define ID_SLOW                         32904
#define ID_CCTOGGLE                     32905
#define ID_AR11                         32906
#define ID_AR12                         32907
#define ID_AR13                         32908
#define ID_AR14                         32909
#define ID_AR15                         32910
#define ID_AR16                         32911
#define ID_AR17                         32912
#define ID_AR18                         32913
#define ID_AR19                         32914
#define ID_AR20                         32915
#define ID_VMRSTATS                     32916
#define ID_LIPDOWN                      32917
#define ID_LIPUP                        32918
#define ID_MUTE                         32919
#define ID_BLANKING                     32920
#define ID_TOGGLE                       32922
#define ID_MOVELEFT                     32924
#define ID_MOVERIGHT                    32925
#define ID_MOVEUP                       32926
#define ID_MOVEDOWN                     32927
#define ID_H_EXPAND                     32928
#define ID_H_CONTRACT                   32929
#define ID_V_EXPAND                     32930
#define ID_V_CONTRACT                   32931
#define ID_ZOOM_IN                      32932
#define ID_ZOOM_OUT                     32933
#define ID_BL_LEFT                      32934
#define ID_BL_RIGHT                     32935
#define ID_BT_UP                        32936
#define ID_BT_DOWN                      32937
#define ID_BR_LEFT                      32938
#define ID_BR_RIGHT                     32939
#define ID_BB_UP                        32940
#define ID_BB_DOWN                      32941
#define ID_STREAM                       32943

"""

import asynchat
import socket
import asyncore
import threading
import new

ttRequests = (
('IP_APPLICATION', '0000', 'Request Application name'),
('IP_VERSION', '0001', 'Request Application version'),
('IP_FULLSCREEN', '0510', 'Request Fullscreen/windowed status'),
('IP_MEDIASTATE', '1000', 'Request MediaState'),
('IP_MEDIATIME', '1010', 'Request Media time'),
('IP_ENDOFMEDIA', '1030', 'End of media'),
('IP_FORMAT', '1040', 'Request Video Format'),
('IP_GETAR', '1300', 'Request Current Aspect Ratio'),
('IP_ARCOUNT', '1310', 'Request Aspect Ratio Count'),
('IP_ARNAMES', '1320', 'ARequest Aspect Ratio Names'),
('IP_CURFILE', '1400', 'Request Current file'),
('IP_DISKINSERTION', '1410', 'Disk inserted'),
('IP_DISKEJECTION', '1420', 'Disk ejected'),
('IP_DVDUNIQUEID', '1500', 'DVD unique ID'),
('IP_DVDTITLE', '1510', 'Request Current Title'),
('IP_DVDTITLECOUNT', '1520', 'Request Title count'),
('IP_DVDCHAPTER', '1600', 'Request Current Chapter'),
('IP_DVDCHAPTERCOUNT', '1610', 'Request Chapter count'),
('IP_DVDAUDIO', '1700', 'Request Current audio stream'),
('IP_DVDAUDIOCOUNT', '1720', 'Request Audio stream count'),
('IP_DVDAUDIONAMES', '1730', 'Request Audio stream names'),
('IP_DVDSUBTITLE', '1800', 'Request Current subtitle stream'),
('IP_DVDSUBTITLECOUNT', '1820', 'Request Subtitle stream count'),
('IP_DVDSUBTITLENAMES', '1830', 'Request Subtitle names (name|name)'),
('IP_DVDANGLE', '1900', 'Request Current angle'),
('IP_DVDANGLECOUNT', '1920', 'Request Angle count'),
('IP_DVDMENUMODE', '2000', 'Request Menu mode'),
('IP_DOMAIN', '2010', 'Request DVD Domain'),
('IP_GETVOLUME', '2100', 'Request Current volume'),
('IP_GETAUDIOOUTPUT', '2120', 'Request Current audio output'),
('IP_GETLISTCOUNT', '3050', 'Request Current list count'),
('IP_GETLIST', '3060', 'Request  playlist'),
('IP_GETPRIVATE', '4010', 'Request Private app string'),
('IP_COUNTCHANGERS', '8110', 'CountChangers'),
)

ttCommands = (
('IP_FLASH', '0500', 'OSD Flash message','Message'),
('IP_MEDIAPOS', '1020', 'Set media time', 'Time(hh:mm:ss)'),
('IP_SETAR', '1330', 'Set Current AR', 'AR number'),
('IP_DVDPLAYTITLE', '1530', 'Play Title', 'Title Number'),
('IP_DVDPLAYCHAPTER', '1620', 'Play chapter', 'Chapter number'),
('IP_DVDPLAYTITCHAP', '1630', 'Play Chapter in Title', 'Title/Chapter (space delimited)'),
('IP_DVDSETAUDIO', '1710', 'Set audio stream','Stream number'),
('IP_DVDSETSUBTITLE', '1810', 'Set subtitle stream', 'Stream number (-1 to disable)'),
('IP_DVDSETANGLE', '1910', 'Set angle', 'Angle'),
('IP_SETVOLUME', '2110', 'Set Current volume', 'Volume'),
('IP_SETAUDIOOUTPUT', '2130', 'Set audio output', 'Audio Output'),
('IP_ADDBOOKMARK', '2200', 'Add a bookmark', ''),
('IP_NEXTBOOKMARK', '2210', 'Next bookmark', ''),
('IP_PREVBOOKMARK', '2220', 'Previous bookmark', ''),
('IP_PLAYFILE', '3000', 'Play file', 'Filename'),
('IP_ADDFILE', '3010', 'Add file to playlist', 'Filename'),
('IP_CLEARLIST', '3020', 'Clear playlist', ''),
('IP_PLAYATINDEX', '3040', 'Play item at index', 'Index'),
('IP_GETINDEX', '3030', 'Current item index', 'Index'),
('IP_DELATINDEX', '3070', 'Delete file at index', 'Index'),
('IP_SETPRIVATE', '4000', 'Private app string', 'String'),
('IP_KEYPRESS', '5010', 'Key code', 'Key-Code'),
('ID_PLAY', '32771', 'Play', ''),
('ID_STOP', '32772', 'Stop', ''),
('ID_PAUSE', '32773', 'Pause', ''),
('ID_NEXT', '32774', 'Next', ''),
('ID_PREVIOUS', '32775', 'Previous', ''),
('ID_EXIT', '32776', 'Exit', ''),
('ID_FF', '32777', 'FastForward', ''),
('ID_RW', '32778', 'Fast Rewind', ''),
('ID_MENU_LIST', '32779', 'Menu List', ''),
('ID_TITLE_MENU', '32780', 'Title Menu', ''),
('ID_FF_1X', '32782', 'Normal Play', ''),
('ID_FF_2X', '32784', 'Fast Forward 2x', ''),
('ID_FF_5X', '32785', 'Fast Forward 5x', ''),
('ID_FF_10X', '32786', 'Fast Forward 10x', ''),
('ID_FF_20X', '32787', 'Fast Forward 20x', ''),
('ID_FF_SLOW', '32788', 'Fast Forward Slow', ''),
('ID_RW_1X', '32790', 'Reverse Play', ''),
('ID_RW_2X', '32791', 'Fast Reverse 2X', ''),
('ID_RW_5X', '32792', 'Faste Reverse 5X', ''),
('ID_RW_10X', '32793', 'Fast Reverse 10X', ''),
('ID_RW_20X', '32794', 'Fast Reverse 20X', ''),
('ID_ROOT_MENU', '32796', 'Root Menu', ''),
('ID_AUDIO_MENU', '32797', 'Audio Menu', ''),
('ID_SUBTITLE_MENU', '32798', 'Subtitle Menu', ''),
('ID_CHAPTER_MENU', '32799', 'Chapter Menu', ''),
('ID_CC_ON', '32804', 'Closed Captions On', ''),
('ID_CC_OFF', '32805', 'Closed Captions Off', ''),
('ID_ABOUT', '32807', 'About', ''),
('ID_SUB_OFF', '32808', 'Subtitles Off', ''),
('ID_ASPECT_DEFINE', '32810', 'Define Aspect Ratio', ''),
('ID_ASPECT_ANAM', '32811', 'AR anamorph', ''),
('ID_ASPECT_NONANAM', '32812', 'AR non anamorph', ''),
('ID_ASPECT_LETTERBOX', '32813', 'AR Letterbox', ''),
('ID_BOOK_ADD', '32814', 'Add Bookmark', ''),
('ID_BUTTON32819', '32819', 'BUTTON32819', ''),
('ID_BUTTON32820', '32820', 'BUTTON32820', ''),
('ID_ONSCREEN', '32821', 'On Screen', ''),
('ID_VID_BRIGHTNESS', '32824', 'Brightness', ''),
('ID_VID_CONTRAST', '32825', 'Contrast', ''),
('ID_VID_HUE', '32826', 'Hue', ''),
('ID_VID_SATURATION', '32827', 'Saturation', ''),
('ID_OVERSCAN', '32828', 'Overscan', ''),
('ID_VID_GAMMA', '32829', 'Gamma', ''),
('ID_MENU_CHAPTER', '32830', 'Menu Chapter', ''),
('ID_MENU_AUDIO', '32831', 'Menu Audio', ''),
('ID_MENU_ANGLE', '32832', 'Menu Angle', ''),
('ID_MENU_FF', '32833', 'Menu FF', ''),
('ID_MENU_SUBTITLES', '32834', 'Menu Subtitles', ''),
('ID_CLOSED_CAPTIONS', '32835', 'Closed Captions', ''),
('ID_BOOK_DELETE', '32836', 'Delete Bookmark', ''),
('ID_ANGLE_MENU', '32837', 'Angle Menu', ''),
('ID_RESUME', '32838', 'Resume', ''),
('ID_MENU_TITLE', '32839', 'Menu Title', ''),
('ID_SETUP', '32841', 'Setup', ''),
('ID_ADJUSTVIDEO', '32842', 'Adjust Video', ''),
('ID_ASPECT_LOCK', '32843', 'Lock Aspect ratio', ''),
('ID_SETSTARTPOINT', '32846', 'Set Startpoint', ''),
('ID_K_RETURN', '32849', 'Key Return', ''),
('ID_K_UP', '32850', 'Key Up', ''),
('ID_K_DOWN', '32851', 'Key Down', ''),
('ID_K_LEFT', '32852', 'Key Left', ''),
('ID_K_RIGHT', '32853', 'Key Right', ''),
('ID_K_FF', '32854', 'Key FastForward', ''),
('ID_K_RW', '32855', 'Key Rewind', ''),
('ID_K_ESCAPE', '32856', 'Key Escape', ''),
('ID_NEXTAR', '32857', 'Next Aspect ratio', ''),
('ID_INFO', '32858', 'Info', ''),
('ID_ARFIRST', '32859', 'First Aspect Ratio', ''),
('ID_AR2', '32860', 'Aspect ratio 2', ''),
('ID_AR3', '32861', 'Aspect ratio 3', ''),
('ID_AR4', '32862', 'Aspect ratio 4', ''),
('ID_AR5', '32863', 'Aspect ratio 5', ''),
('ID_AR6', '32864', 'Aspect ratio 6', ''),
('ID_AR7', '32865', 'Aspect ratio 7', ''),
('ID_AR8', '32866', 'Aspect ratio 8', ''),
('ID_AR9', '32867', 'Aspect ratio 9', ''),
('ID_ARLAST', '32868', 'Last Aspect ratio', ''),
('ID_EJECT', '32870', 'Eject', ''),
('ID_CONTEXT', '32872', 'Context', ''),
('ID_ALTEXIT', '32873', 'ALT Exit', ''),
('ID_MINIMIZE', '32874', 'Minimize', ''),
('ID_NEXTSUB', '32875', 'Next Subtitle', ''),
('ID_NEXTAUDIO', '32876', 'Next Audio', ''),
('ID_REPLAY', '32877', 'Replay', ''),
('ID_JUMP', '32878', 'Jump', ''),
('ID_FRAMESTEP', '32879', 'Framestep', ''),
('ID_ABREPEAT', '32880', 'A/B-Repeat', ''),
('ID_CHAPTITREP', '32881', 'Chapter Title Repeat', ''),
('ID_NEXT_ANGLE', '32883', 'Next Angle', ''),
('ID_OPEN', '32884', 'Open', ''),
('ID_NEXT_TIT', '32885', 'Next Title', ''),
('ID_STATS', '32886', 'Statistics', ''),
('ID_CAPTURE', '32887', 'Capture', ''),
('ID_BK_RESUME', '32888', 'BK Resume', ''),
('ID_DEINTERLACE', '32889', 'Deinterlace', ''),
('ID_VOLUP', '32891', 'Volume Up', ''),
('ID_VOLDOWN', '32892', 'Volume Down', ''),
('ID_NEXTDISK', '32893', 'Next Disk', ''),
('ID_SHOWTIME', '32894', 'Show Time', ''),
('ID_CC_NUDGE_UP', '32895', 'CC Nudge Up', ''),
('ID_CC_NUDGE_DOWN', '32896', 'CC Nudge Down', ''),
('ID_UPGRADE', '32897', 'Upgrade', ''),
('ID_NEXT_FILE', '32898', 'Next File', ''),
('ID_PREVIOUS_FILE', '32899', 'Previous File', ''),
('ID_TSPROG', '32901', 'TSPROG', ''),
('ID_PREV_TIT', '32902', 'Previous Title', ''),
('ID_SLOW', '32904', 'Slow', ''),
('ID_CCTOGGLE', '32905', 'Closed Captions Toggle', ''),
('ID_AR11', '32906', 'Aspect ratio 11', ''),
('ID_AR12', '32907', 'Aspect ratio 12', ''),
('ID_AR13', '32908', 'Aspect ratio 13', ''),
('ID_AR14', '32909', 'Aspect ratio 14', ''),
('ID_AR15', '32910', 'Aspect ratio 15', ''),
('ID_AR16', '32911', 'Aspect ratio 16', ''),
('ID_AR17', '32912', 'Aspect ratio 17', ''),
('ID_AR18', '32913', 'Aspect ratio 18', ''),
('ID_AR19', '32914', 'Aspect ratio 19', ''),
('ID_AR20', '32915', 'Aspect ratio 20', ''),
('ID_VMRSTATS', '32916', 'VMR Statistics', ''),
('ID_LIPDOWN', '32917', 'Lipsync down', ''),
('ID_LIPUP', '32918', 'Lipsync Up', ''),
('ID_MUTE', '32919', 'Mute', ''),
('ID_BLANKING', '32920', 'Blanking', ''),
('ID_TOGGLE', '32922', 'Toggle', ''),
('ID_MOVELEFT', '32924', 'Move Left', ''),
('ID_MOVERIGHT', '32925', 'Move Right', ''),
('ID_MOVEUP', '32926', 'Move Up', ''),
('ID_MOVEDOWN', '32927', 'Move Down', ''),
('ID_H_EXPAND', '32928', 'Horizontal Expand', ''),
('ID_H_CONTRACT', '32929', 'Horizontal Contract', ''),
('ID_V_EXPAND', '32930', 'Vertical Expand', ''),
('ID_V_CONTRACT', '32931', 'Vertical Contract', ''),
('ID_ZOOM_IN', '32932', 'Zoom In', ''),
('ID_ZOOM_OUT', '32933', 'Zoom Out', ''),
('ID_BL_LEFT', '32934', 'BL_LEFT', ''),
('ID_BL_RIGHT', '32935', 'BL_RIGHT', ''),
('ID_BT_UP', '32936', 'BT_UP', ''),
('ID_BT_DOWN', '32937', 'BT_DOWN', ''),
('ID_BR_LEFT', '32938', 'BR_LEFT', ''),
('ID_BR_RIGHT', '32939', 'BR_RIGHT', ''),
('ID_BB_UP', '32940', 'BB_UP', ''),
('ID_BB_DOWN', '32941', 'BB_DOWN', ''),
('ID_STREAM', 32943, 'STREAM', ''),
)

ttAutoKillerAndChangerCommands = (
('IP_LAUNCH', '8000', 'Launch AutoKiller'),
('IP_QUIT', '8010', 'Quit Autokiller'),
('IP_MOUNTDISK', '8020', 'Mount Disk', 'Changer/Slot (comma delimited)'),
('IP_UNMOUNTDISK', '8030', 'Unmount Disk', 'Changer/Slot (comma delimited)'),
('IP_EJECTDISK', '8040', 'Eject Disk', 'Changer/Slot (comma delimited)'),
('IP_GETSLOTDATA', '8050', 'GETSLOTDATA', 'Changer, Slot'),
('IP_GETDRIVEDATA', '8060', 'GETDRIVEDATA', 'Changer  ->DriveData'),
('IP_CHECKCHANGED', '8070', 'CHECKCHANGED'),
('IP_REBUILDDATA',  '8080',  'REBUILDDATA'),
('IP_DATACHANGED', '8100', 'Notification of data change'),
)

class TheaterTekSession(asynchat.async_chat):
    """
    Handles a Theatertek TCP/IP session.
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
        self.plugin.ValueUpdate(self.buffer)

        # reset the buffer
        self.buffer = ''

class stdAction(eg.ActionClass):

    def __call__(self):
        self.plugin.DoCommand(self.value)

class stdActionWithStringParameter(eg.ActionWithStringParameter):

    def __call__(self, Param):
        self.plugin.DoCommand(self.value + " " + Param)

class wmAction(eg.ActionClass):

    def __call__(self):
        self.plugin.DoCommand("5000 " + self.value)

class TheaterTek(eg.PluginClass):

    def __init__(self):
        self.host = "localhost"
        self.port = 2663
        self.isSessionRunning = False
        self.timeline = ""
        self.waitStr = None
        self.waitFlag = threading.Event()
        self.PlayState = -1
        self.lastMessage = {}
        self.lastSubtitleNum = 0
        self.lastSubtitlesEnabled = False
        self.lastAudioTrackNum = 0

        group = self.AddGroup('Requests')
        for className, scancode, descr in ttRequests:
            clsAttributes = dict(name=descr, value=scancode)
            cls = new.classobj(className, (stdAction,), clsAttributes)
            group.AddAction(cls)

        group = self.AddGroup('Commands')
        for className, scancode, descr, ParamDescr in ttCommands:
            clsAttributes = dict(name=descr, value=scancode)
            if ParamDescr == "":
                 if className[0:3] == "IP_":
                    cls = new.classobj(className, (stdAction,), clsAttributes)
                 else:
                    cls = new.classobj(className, (wmAction,), clsAttributes)
            else:
                cls = new.classobj(className, (stdActionWithStringParameter,), clsAttributes)
                cls.parameterDescription = ParamDescr
            group.AddAction(cls)

    def __start__(
        self,
        host="localhost",
        port=2663,
        dummy1=None,
        dummy2=None,
        useNewEvents=False
    ):
        self.host = host
        self.port = port
        self.events = self.ttEvents

    ttEvents = {
        "0000": "ApplicationName",
        "0001": "Version",
        "0500": "OSD",
        "0510": (
            "WindowState",
            {
                "0": "Minimized",
                "1": "Windowed",
                "2": "Fullscreen"
            },
        ),
        "1000": (
            "MediaState",
            {
                "0": "Stopped",
                "1": "Playing",
                "2": "Paused",
                "3": "FF",
                "4": "RW"
            },
        ),
        "1010": "MediaTime",
        "1030": "EndOfMedia",
        "1040": (
            "Format",
            {
                "0": "NTSC",
                "1": "PAL",
            },
        ),
        "1300": "AspectRatio",
        "1310": "AspectRatioCount",
        "1320": "AspectRatioNames",
        "1400": "Currentfile",
        "1410": "DiskInserted",
        "1420": "DiskEjected",
        "1500": "DVDUniqueID",
        "1510": "CurrentTitle",
        "1520": "TitleCount",
        "1600": "CurrentChapter",
        "1610": "ChapterCount",
        "1700": "CurrentAudioStream",
        "1720": "AudioStreamCount",
        "1730": "AudioStreamNames",
        "1800": "CurrentSubtitleStream",
        "1820": "SubtitleStreamCount",
        "1830": "SubtitleNames",
        "1900": "CurrentAngle",
        "1920": "AngleCount",
        "2000": (
            "MenuMode",
            {
                "0": "Off",
                "1": "On",
            },
        ),
        "2010": "DVDDomain",
        "2100": "CurrentVolume",
        "2120": "CurrentAudioOutput",
        "3050": "CurrentListCount",
        "3060": "Playlist",
        "4010": "PrivateAppString",
        "8110": "CountChangers",
    }

    def ValueUpdate(self, text):
        if text == self.waitStr:
            self.waitStr = None
            self.waitFlag.set()
            return
        header = text[0:4]
        state = text[5:].decode('utf-8')
        self.lastMessage[header] = state
        ttEvent = self.ttEvents.get(header, None)
        if ttEvent is not None:
            if type(ttEvent) == type({}):
                eventString = ttEvent.get(state, None)
                if eventString is not None:
                    self.TriggerEvent(eventString)
                else:
                    self.TriggerEvent(header, [state])
            elif type(ttEvent) == type(()):
                suffix2 = ttEvent[1].get(state, None)
                if suffix2 is not None:
                    self.TriggerEvent(ttEvent[0] + "." + suffix2)
                else:
                    self.TriggerEvent(ttEvent[0] + "." + str(state))
            else:
                if state == "":
                    self.TriggerEvent(ttEvent)
                else:
                    self.TriggerEvent(ttEvent, [state])
            return
        else:
            self.TriggerEvent(header, [state])

    @eg.LogIt
    def DoCommand(self, cmdstr):
        self.waitFlag.clear()
        self.waitStr = cmdstr
        if not self.isSessionRunning:
            self.session = TheaterTekSession(self, (self.host, self.port))
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
        port=2663,
        dummy1=None,
        dummy2=None
    ):
        panel = eg.ConfigPanel(self)
        hostEdit = panel.TextCtrl(host)
        portEdit = panel.SpinIntCtrl(port, max=65535)
        panel.AddLine("TCP/IP host:", hostEdit)
        panel.AddLine("TCP/IP port:", portEdit)
        while panel.Affirmed():
            panel.SetResult(
                hostEdit.GetValue(),
                portEdit.GetValue(),
                None,
                None
            )

    class MyCommand(eg.ActionWithStringParameter):
        name = "Raw Command"

        def __call__(self, cmd):
            self.plugin.DoCommand(cmd)
