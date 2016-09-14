# -*- coding: utf-8 -*-

version="0.2.22"

# plugins/RadioSure/__init__.py
#
# Copyright (C)  2009 - 2013   Pako (lubos.ruckl@quick.cz)
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.2.22 by Pako 2013-01-26 12:17 UTC+1
#     - bugfix - scheduler size, when system font > 100%
# 0.2.21 by Pako 2012-12-02 13:06 UTC+1
#     - added "Stop processing event" feature (Menu frame)
# 0.2.20 by Pako 2011-08-24 09:12 UTC+1
#     - bugfix - wrong stored last position of manager and scheduler
# 0.2.19 by Pako 2011-06-27 13:54 UTC+1
#     - added action "Get last played favorite station" (retrieved from RS menu)
#     - action name "Start (Stop) observation of titlebar" changed to
#                   "Start (Stop) periodical observation"
#     - added option to observation of last played station (from file RadioSure.xml)
#     - bugfix - extended timeout for temporarily launched RS during plugin start
# 0.2.18 by Pako 2011-06-10 18:44 UTC+1
#     - bugfix - write to logfile when Schedule title is non-ascii
# 0.2.17 by Pako 2011-06-10 16:27 UTC+1
#     - Added action "Get favorites"
#     - Added period "minutes" for schedule type "Periodically"
# 0.2.16 by Pako 2011-06-08 18:21 UTC+1
#     - eg.scheduler used instead of the Threading
# 0.2.15 by Pako 2011-06-05 18:31 UTC+1
#     - Used eg.EVT_VALUE_CHANGED instead of EVT_BUTTON_AFTER
# 0.2.14 by Pako 2011-05-08 18:28 UTC+1
#     - Bug fix - action Minimize/Restore
# 0.2.13 by Pako 2011-04-06 11:07 UTC+1
#     - Bug fix - bad name of language file
# 0.2.12 by Pako 2011-04-05 17:38 UTC+1
#     - Added first version of Favorites manager
#     - Added "menu browser"
#     - Added many new actions
# 0.2.11 by Pako 2011-03-03 09:08 UTC+1
#     - The cursor is changed to indicate the existence of a context menu
#     - If exists file "contextCursor.cur", used as the cursor where there is a contextual menu
# 0.2.10 by Pako 2011-02-12 09:53 UTC+1
#     - FixedTimeCtrl replaced by eg.TimeCtrl
# 0.2.9 by Pako 2011-01-15 11:50 UTC+1
#     - different shape of the cursor on the table of schedules indicate that there is context menu available
# 0.2.8 by Pako 2011-01-11 14:25 UTC+1
#     - if you turn on logging then into the log file is written whole command line
# 0.2.7 by Pako 2011-01-07 18:39 UTC+1
#     - fixed bug - the Scheduler window opens although in Scheduler.xml there not the attribute "Position"
#       (this can happen when you upgrade from version 0.2.0 and lower)
# 0.2.6 by Pako 2011-01-07 11:39 UTC+1
#     - fixed bug - incorrect reading favorites, when applied a new structure of RadioSure.xml file
# 0.2.5 by Pako 2010-12-28 16:02 UTC+1
#     - added popup menu and features "Move schedule up/down"
# 0.2.4 by Pako 2010-12-24 12:08 UTC+1
#     - there is no need to reinstall this plugin, when changing the way the installation (especially the paths) of Radio?Sure!
# 0.2.3 by Pako 2010-12-24 08:30 UTC+1
#     - scheduler dialog opens, even though there is no node "Favorites" in RadioSure.xml
# 0.2.2 by Pako 2010-12-19 15:54 UTC+1
#     - changed the way of paths settings to the RadioSure.exe and RadioSure.xml
# 0.2.1 by Pako 2010-12-19 08:19 UTC+1
#     - scheduler dialog remembers its position even after closing EventGhost
#     - bugfix - "Add schedule" enable buttons, when schedule list is empty
# 0.2.0 by Pako 2010-12-14 11:13 UTC+1
#     - a comprehensive rework according to the plugin SchedulGhost:
#     - addded new types of schedule
#     - changed format of "Scheduler.xml" file
#     - added ability to affect certain types of schedules according to public holidays
#     - added option to select the first day of the week (Sunday or Monday)
#     - scheduler dialog remembers its position
#     - scheduler dialog is not modal and can be minimized
#     - added Apply button (scheduler dialog)
#     - added new actions - "Run schedule immediately"
# 0.1.9 by Pako 2010-12-09 13:52 UTC+1
#     - correction of previous versions (moreover redefine one pseudo-private method)
# 0.1.8 by Pako 2010-12-06 20:10 UTC+1
#     - wx.lib.masked.TimeCtrl workaround (see http://trac.wxwidgets.org/ticket/11171)
# 0.1.7 by Pako 2010-07-22 20:27 GMT+1
#     - bugfix
# 0.1.6 by Pako 2010-07-22 10:30 GMT+1
#     - added wx.ComboBox for Scheduler actions
# 0.1.5 by Pako 2010-07-10 08:21 GMT+1
#     - added Scheduler
#     - added guid attribute
# 0.1.4 by Pako 2010-03-23 11:20 GMT+1
#     - added action Random favorite
# 0.1.3 by Pako 2010-03-22 09:09 GMT+1
#     - added actions Start and Stop observation of titlebar
#===============================================================================

eg.RegisterPlugin(
    name = "RadioSure",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{84703620-87B4-4982-A9AB-DA1B3F8D22EA}",
    description = ur'''<rst>
Adds actions to control the `Radio?Sure!`_

.. _Radio?Sure!: http://www.radiosure.com/ ''',
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2359",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUA//+Gh4ju7/Ds"
        "7e7q6+zo6evm5+nk5efi4+Xg4ePd3+Db3N7Z2tzW2Nrr7e5+g4bo6erm5+js7e3a3N7Y"
        "2dt3fYDT1dfp6uzn6Orl5uhIS03V1tjS1NbQ0tTn6Onl5ufi5OXS09XP0dPNz9HR09XP"
        "0NPMztDKzM7h4+Tf4OLd3uCVmp1OUlQZGhoYGRlLTlCHjZDMzdDJy87Hycve4OHc3t+d"
        "oqQyNDU3OjtSVlgpKywqLC2IjpHHyMvExsnc3d/Z29xWWlyBh4p2fH9pbnFfZGYsLi9L"
        "T1HExsjCxMYbHB2XnJ5MUFJKTU9yeHtVWVvBw8a/wcTW19kcHR6UmZypra9RVVeGjI9l"
        "am0aGxu/wcO9v8JcYWNeY2W5vL6xtLamqqyboKK9vsG7vcA9QEG6vL+5u76LkJPIycyy"
        "tbddYmRYXV+jqKqDiYy3ubzFx8nDxcfBw8W4ur22uLsAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADQcfgAAAAAAAXQciD0AAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAABAAgAAAAAAAAAAAAAAAAAAAAAAAAAAABGa1gAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAEAAAAAAAAAAAAPAAAAAAEAAAEAAADQckT/C08AAAAAAAAAAAAAAAMAAADf"
        "BnAAAAAAAAAAAAAAAAAAAAQAAQEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACnZAh6AAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAKdJREFUeNpjYGBgRAVoAl9A"
        "ArwQCbDMayYgg5OTk5GBg4PhPzs7OwNIAESDARsbGwNICxtQKQeQLwSkb4EE1JEMPQfS"
        "wgMGjNwgANZix8h4UwOqYgdIxdmznGKcIPAMaBVIReARW6DcNW2QimUgAWlGe7DynTY8"
        "jPOYwNYzs/+//vqB3ANmZrAWVUeg9EsGCcafHIyTQQKGjDZAAUYOJt4/rH0M6N4HAFCJ"
        "GrcTFgV2AAAAAElFTkSuQmCC"
    ),
)
#===============================================================================

import wx.grid as gridlib
import subprocess
import wx.calendar as wxCal
from wx.lib.masked import EVT_TIMEUPDATE
from subprocess import Popen
from os import listdir, remove, rename
from os.path import abspath, join, dirname, split, isfile, exists
from calendar import day_name, month_name, monthrange
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from _winreg import OpenKey, HKEY_CURRENT_USER, EnumValue, QueryValueEx, CloseKey
from time import sleep, mktime, strptime, localtime
from datetime import datetime as dt
from datetime import timedelta as td
from copy import deepcopy as cpy
from xml.dom import minidom as miniDom
from threading import Timer
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import CreateEvent, SetEvent, PostMessage
from eg.WinApi.Dynamic import SendMessage, ShowWindow, RegisterWindowMessage
from eg.WinApi import SendMessageTimeout
from win32gui import GetWindowText, GetWindow, GetDlgCtrlID, GetMenuItemCount
from win32gui import GetWindowPlacement, GetDlgItem, GetClassName, GetSubMenu
from win32file import GetFileAttributes
from random import randrange
from codecs import lookup
from codecs import open as openFile
from winsound import PlaySound, SND_ASYNC
from locale import strxfrm
from ctypes import c_long, c_ulong, c_int, byref, sizeof, Structure, c_buffer
from ctypes.wintypes import WinDLL
_kernel32 = WinDLL("kernel32")
_user32 = WinDLL("user32")
from sys import getfilesystemencoding
FSE = getfilesystemencoding()

if eg.Version.base >= "0.4.0":
    from eg.Classes.MainFrame.TreeCtrl import DropTarget as EventDropTarget
    IMAGES_DIR = eg.imagesDir
else:
    from eg.Classes.MainFrame.TreeCtrl import EventDropTarget
    IMAGES_DIR = eg.IMAGES_DIR

ARIAL_INFO  = "0;-35;0;0;0;700;0;0;0;0;3;2;1;34;Arial"
TAHOMA_INFO = "0;-27;0;0;0;400;0;0;0;0;3;2;1;34;Tahoma"

PROCESS_TERMINATE     = 1
WM_CLOSE              = 16
WM_COMMAND            = 273
WM_SYSCOMMAND         = 274
TBM_GETPOS            = 1024
TBM_SETPOS            = 1029
SC_RESTORE            = 61728
#SW_HIDE               = 0
#SW_MINIMIZE           = 6
SW_RESTORE            = 9
GW_CHILD              = 5
GW_HWNDNEXT           = 2
FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_SYSTEM = 4
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
#===============================================================================

CUR_STRING = (
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAABnRSTlMA/wBmAADomHeP"
    "AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAMK0lEQVR42gEgDN/zAQAAAOns8xZ6DQAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAApKDTXa9EAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAA////AQEB1tLSKZQuAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAP///youLtds0gAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAD///8qLi7XbNIAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAACAAAAAAAA/wD+AAAA////Ki4u12zSAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAgAAAAAAAP7///8A/gAAAP///youLtds0wAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAIAAAAAAAAAAAD+////AP4AAAD//PwqLi3YbNQAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAA"
    "AAAAAAAAAAAA/gD/APwAAAMD9PjwKS4s2W3UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA"
    "AAABAAH6AQAAAPb69gkHC+ns9CgtLdlt1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAQAC+wLz"
    "+/P0+/QB+QHw8fEWEwvs6ecoLS/VcN8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAA/////vv+9/32AwMDAvsC"
    "AQkABQEHAAAAAAAAAAAAAQEJ/2b4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAIFAgsIDObm8gYKBwUBBwEB"
    "AQEBDQEBAQEBCAAA+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAADz9vsjIBicn6UAAAAAABTd2Nj/"
    "ZgD/Zvn/ZgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAABAAAA////8/X6DgwH/2YAAZoA////9fHwDBAR/2YAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAgAAAAAAAA4MB+Pk6wAAAAAAFMnFwgsPEAAEGLtQxAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAQAAAABAQHe3+YcghUAAADk59ocGRL////o4coYGx7/ZgAAAAAAAAAEoBoA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD8YOYAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAE/2YAAAAAAIcaAAAAAAAAG38SAAAQ8u7qFxodAAAAAAAAAAAAAAAAAAAAiodz+Pj4"
    "DAwMAQEBBQUF/Pz8+Pj47e3tCAgIg4aaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAA"
    "AAAAAAAAAAAAAAAAAAAAAPz/7wQBASEkOszP2ACXKAAAAAAAAAAAAFBQUCMjIwAAAAAA"
    "AAAAAAAAAAAAAHJycoeHh4OGmgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAA"
    "AAAAAAAAAAAAAAADZwH/ZgAAAMYAlygAAAAAAAAAAAAAAAAiIiLMzMwFBQULCwsAAAAB"
    "AQHn5+cXFxcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeHh46OjoAAAABQUF6enp+fn5CAgI"
    "BgYGISEhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM7OzqysrA8PD4WFhYKCgvz8/AgICIKCgouL"
    "iwMGGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH/ZgAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAEoBr9+uY2NjbKysogICDg4OAAAAAAAAAAAAAAAAADBhr8"
    "YOYAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAwcHBlZWVAAAA39/fZWVlAAAAysrKnZ2ds7OzAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAD4+PqysrAAAAAAAAJqamgAAAKmpqRMTE0xMTAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAtLS0AAADb29sEBAQAAAAxMTHt7e0AAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAB/2YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABKAa"
    "/PnlAAAADQ0NCQkJs7OzZmZm0dHRAAAAAAAABAcb/GDmAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMrKygEB"
    "AfT09Ovr65aWlmRkZAEBAURERAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2Njb/////////"
    "///u7u79/f3n5+e8vLwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/2YAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABKAaAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAA/GDmAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf9mAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADPbTswenz69gAAAABJRU5ErkJggg=="
)
#===============================================================================
class ConfigData(eg.PersistentData):
    pos = None
    plcmnt = None

class Text:
    label1 = "Radio?Sure! installation folder:"
    label2 = "RadioSure.xml and Scheduler.xml folder location:"
#    filemask = "RadioSure.exe|RadioSure.exe|All-Files (*.*)|*.*"
    text1 = "Couldn't find RadioSure window !"
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = 'Folder "%s" is incorrect'
    toolTipFile = "Press button and browse to select logfile ..."
    browseFile = 'Select the logfile'
    boxMessage1 = 'Missing file %s !'
    logLabel = "Log scheduler events to following logfile:"
#    nextRun = "Next run: %s"
    none = "None"
    execut = 'Schedule "%s" - execution. Next run: %s'
    cmdLine = 'Commandline: %s'
    cancAndDel = 'Schedule "%s" canceled and deleted'
    cancAndDis = 'Schedule "%s" canceled (disabled)'
    newSched = 'Schedule "%s" scheduled. Next run: %s'
    re_Sched = 'Schedule "%s" re-scheduled. New next run: %s'
    start = 'RadioSure plugin started. All valid schedules will be scheduled:'
    stop = 'RadioSure plugin stoped. All scheduled schedules will be canceled:'
    canc = 'Schedule "%s" canceled'
    launched = "Schedule.Launched"
    holidButton = "Public holidays ..."
    managerButton = "Show scheduler"
    fixBoxLabel = "Fixed public holidays:"
    varBoxLabel = "Variable public holidays:"
    ok = "OK"
    cancel = "Cancel"
    yes = "Yes"
    no = "No"
    add = "Add"
    delete = "Delete"
    first_day = "The first day of the week:"
    xmlComment = "Radio?Sure! scheduler configuration file. Updated at %s."
    messBoxTit0 = "EventGhost - Radio?Sure! plugin"
    messBoxTit1 = "Attention !"
    message2 = """You can not start another instance of Radio?Sure!,
because the maximum number of instances %i is exhausted!"""
    message3 = '''You can not start another instance of Radio?Sure!,
because the option "Allow only one instance" is chosen!'''
    autoClose = "Auto close after %i s"
    toolTip = "Drag-and-drop an event from the log into the box."
    popup = (
        "Delete item",
        "Delete all items",
    )
    clear  = "Clear all"
    opened = "Opened"
    closed = "Closed"
    root = "Main (root) menu"

    class OpenManager:
        dialogTitle = "Radio?Sure! Favorites manager %s  (plugin for EventGhost)"
        toolTipDelete = "Delete item(s)"
        toolTipUp = "Move item(s) up"
        toolTipDown = "Move item(s) down"
        moveTop = "Move item(s) top"
        moveBottom = "Move item(s) bottom"
        exportSel = "Export selected item(s) to XML file"
        exportAll = "Export all items to XML file"
        toolTipExport = "Export selected (if any) or all items to XML file"
        toolTipImport = "Import from XML file"
        toolTipImportSR = "Import from Screamer Radio"
        sort  = "Sort alphabetically"
        play = "Play selected favorite just now !"
        refresh = "Refresh favorites list from RadioSure.xml"
        export = "Export"
        imprt = "Import"
        importSR = "Import SR"
        lblSource = "Source:"
        lblGenre = "Genre:"
        lblLanguage = "Language:"
        lblCountry = "Country:"
        ok = "OK"
        cancel = "Cancel"
        apply = "Apply"
        lblList = "Favorites list:"
        xmlComment1 = "Radio?Sure! favorites backup file."
        xmlComment2 = 'Saved at %s by EventGhost.'
        choose = 'Choose a XML file to be import'
        save = 'Backup favorites as XML file ...'
        wildcard = "XML file (*.xml)|*.xml"
        removeDupl = "Remove duplications"
        messBoxTit2 = """Attention !
Radio?Sure! is running !"""
        messBoxTit3 = """Attention !
Recording is in progress !"""
        messBoxTit5 = "Congratulations!"
        messBoxTit6 = "Announcement"
        messBoxTit7 = "Warning"
        message1 = """Your version of Radio?Sure! allows you to save only the first %i favorite stations !
Other favorites will be ignored."""
        message2 = """If you want to save the modified list of favorite stations,
must be overwritten file RadioSure.xml.
You can not overwrite the file RadioSure.xml,
if the Radio?Sure! is currently running.
Otherwise, the favorites list is returned to its original condition.

Press button %s, if the program Radio?Sure! can be closed.
Press button %s, if the program Radio?Sure! can not be closed."""
        message3 = "Failed to save data to the file RadioSure.xml !"
        message4 = 'It is not possible to import because there is a problem.\n\
The file "%s" does not have the expected structure.'
        message5 = "Your list of favorite stations has been successfully updated!"
        message6 = "Failed to close Radio?Sure!"
        message7 = "Your list of favorite stations has not been updated!"
        message8 = """Your list of favorite stations contain (in sources) duplications!
They will be saved only unique items."""
        message9 = "Failed to open Radio?Sure!"

    class OpenScheduler:
        dialogTitle = "Radio?Sure! Scheduler %s  (plugin for EventGhost)"
        header = (
            "Enabled",
            "Schedule title",
            "Last run",
            "Next run",
        )
        sched_type = (
            "Only once (or yearly)",
            "Daily",
            "Weekly",
            "Monthly / weekday",
            "Monthly / day",
            "Periodically",
        )
        toolTipFile = """Press button and browse to select file ...
File type (as .mp3) need not be completed. Will be added automatically."""

        browseTitle = "Select a folder and enter file name (without file type):"
        serial_num = (
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "last"
        )
        the = "The"
        in_ = "in"
        buttons = (
            "Add new",
            "Duplicate",
            "Delete",
            "OK",
            "Cancel",
            "Apply"
        )
        type_label = "Schedule type:"
        source = "Source URL:"
        favorite = "Favorite station title:"
        filename = "Destination file name (optional):"
        chooseDay = "Choose day"
        theEvery = "The every"
        yearly = "Every year on the same day"
        chooseTime = "Choose start time and duration (00:00 = constantly)"
        choosePeriod = "Choose period"
        andThenEvery = "Repeat every"
        units = (
            "minutes",
            "hours",
            "days",
            "weeks",
            "months",
            "years",
        )
        start = "Start time (HH:MM:SS):"
        length = "Duration (HH:MM):"
        boxTitle = "Your setup is not properly configured !"
        boxTexts = (
            "Schedule title must not be an empty string !",
            "Schedule title must be unique !",
            'Determine the source URL, or set the mode "Do nothing" !',
            'Not allowed to set "Do nothing" while also "None" event !',
            'Must be chosen Schedule type !',
            "The span must be shorter than the period !",
        )
        workModeLabel = "Radio?Sure! working mode:"
        workModes = (
            "Playing (audibly)",
            "Recording (audibly)",
            "Recording (soundlessly)",
            "Do nothing"
        )
        windOpenLabel = "Window open:"
        windOpenChoices =(
            "Visible",
            "Hidden"
        )
        triggEvtLabel = "Trigger an event:"
        triggEvtChoices = (
            "None",
            "Schedule title",
            "All parameters"
        )
        testButton = "Test now"
        testRun = 'Schedule "%s" - TEST execution. Possible next run: %s'
        holidCheck_1 = "Do not trigger events for a chosen day if it happens to be a holiday"
        holidCheck_2 = "Do also trigger events for a non-chosen day if it happens to be a holiday"
        popup = (
            "Add schedule",
            "Duplicate schedule",
            "Delete schedule",
            "Enable all schedules",
            "Disable all schedules",
            "Move schedule up",
            "Move schedule down",
        )
#===============================================================================

def my_list2cmdline(seq):
    """ FIXING subprocess.list2cmdline
    Workaround, because subprocess.list2cmdline does not work with arguments like:
    filename="... ...". Ie, when we need quotes inside the string, and somewhere
    inside is a space character. When you properly prepare all items
    (including the quotes), it works!
    There is also done simultaneously filesystemencode encoding
    (otherwise there UnicodeDecodeError occurs...)"""
    return ' '.join([arg.encode(FSE) if isinstance(arg, unicode) else arg for arg in seq])
subprocess.list2cmdline = my_list2cmdline
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

class MyFileBrowseButton(eg.FileBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

class MySpinIntCtrl(eg.SpinIntCtrl):
    def SetNumCtrlId(self, id):
        self.numCtrl.SetId(id)
#===============================================================================

class MessageBoxDialog(wx.Dialog):

    def __init__(
        self,
        parent,
        message,
        caption = eg.APP_NAME,
        flags=wx.OK,
        time=0,
        plugin=None,
        pos=wx.DefaultPosition
    ):
        PlaySound('SystemExclamation', SND_ASYNC)
        if parent is None and eg.document.frame:
            parent = eg.document.frame
        dialogStyle = wx.DEFAULT_DIALOG_STYLE
        if flags & wx.STAY_ON_TOP:
            dialogStyle |= wx.STAY_ON_TOP
        wx.Dialog.__init__(self, parent, -1, caption, pos, style=dialogStyle)
        self.SetTitle(plugin.text.messBoxTit0)
        self.SetIcon(plugin.info.icon.GetWxIcon())
        bttns = []
        if flags:
            art = None
            if flags & wx.ICON_EXCLAMATION:
                art = wx.ART_WARNING
            elif flags & wx.ICON_ERROR:
                art = wx.ART_ERROR
            elif flags & wx.ICON_QUESTION:
                art = wx.ART_QUESTION
            elif flags & wx.ICON_INFORMATION:
                art = wx.ART_INFORMATION
            if art is not None:
                bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MESSAGE_BOX, (32,32))
                icon = wx.StaticBitmap(self, -1, bmp)
                icon2 = wx.StaticBitmap(self, -1, bmp)
            else:
                icon = (32,32)
                icon2 = (32,32)
            flag = True
            if flags & wx.YES:
                default = False
                if not flags & wx.NO_DEFAULT:
                    default = True
                    flag = False
                bttns.append((wx.ID_YES, plugin.text.yes, default))
            if flags & wx.NO:
                default = False
                if flags & wx.NO_DEFAULT:
                    default = True
                    flag = False
                bttns.append((wx.ID_NO, plugin.text.no, default))
            if flags & wx.OK:
                bttns.append((wx.ID_OK, plugin.text.ok, flag))
            if flags & wx.CANCEL:
                bttns.append((wx.ID_CANCEL, plugin.text.cancel, False))
            if not flags & (wx.OK | wx.CANCEL | wx.YES | wx.NO):
                bttns.append((wx.ID_OK, plugin.text.ok, True))
        else:
            bttns.append((wx.ID_OK, plugin.text.ok, True))
        if caption:
            caption = wx.StaticText(self, -1, caption)
            caption.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        message = wx.StaticText(self, -1, message)
        line = wx.StaticLine(self, -1, size=(1,-1), style = wx.LI_HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add((10, 1))

        if time:
            self.cnt = time
            txt = plugin.text.autoClose % self.cnt
            info = wx.StaticText(self, -1, txt)
            info.Enable(False)
            bottomSizer.Add(info, 0, wx.TOP, 3)

            def UpdateInfoLabel(evt):
                self.cnt -= 1
                txt = plugin.text.autoClose % self.cnt
                info.SetLabel(txt)
                if not self.cnt:
                    self.Close()

            self.Bind(wx.EVT_TIMER, UpdateInfoLabel)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
        else:
            self.timer = None

        bottomSizer.Add((5,1),1,wx.EXPAND)
        for bttn in bttns:
            b = wx.Button(self, bttn[0], bttn[1])
            if bttn[2]:
                #b.SetDefault()
                defBtn = b # SetDefault() workaround
            bottomSizer.Add(b, 0, wx.LEFT, 5)
        bottomSizer.Add((10, 1))
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(icon,0,wx.LEFT|wx.RIGHT,10)
        topSizer.Add((1,1),1,wx.EXPAND)
        topSizer.Add(caption,0,wx.TOP,5)
        topSizer.Add((1,1),1,wx.EXPAND)
        topSizer.Add(icon2,0,wx.LEFT|wx.RIGHT,10)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM,10)
        mainSizer.Add(message, 0, wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALL,5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND|wx.BOTTOM,5)
        # SetDefault() workaround:
        defBtn.SetFocus()

        def OnButton(evt):
            self.SetReturnCode(evt.GetId())
            self.Close()
            evt.Skip()
        wx.EVT_BUTTON(self, -1, OnButton)

        def onClose(evt):
            if self.GetReturnCode() not in (wx.ID_OK, wx.ID_CANCEL, wx.ID_YES, wx.ID_NO):
                self.SetReturnCode(wx.ID_CANCEL)
            if self.timer:
                self.timer.Stop()
                del self.timer
            self.MakeModal(False)
            self.GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

        self.SetSizer(mainSizer)
        self.Fit()

def MessageBox(parent, message, caption='', flags=0, time = 0, plugin = None):
    mssgbx = MessageBoxDialog(parent, message, caption, flags, time, plugin)
    val = mssgbx.ShowModal()
    return val
#===============================================================================

class MyTimer():
    def __init__(self, t, plugin):
        self.timer = Timer(t, self.Run)
        self.plugin = plugin
        self.timer.start()


    def Run(self):
        try:
            self.plugin.menuDlg.Close()
            self.plugin.menuDlg = None
        except:
            pass


    def Cancel(self):
        self.timer.cancel()
#===============================================================================

class HolidaysFrame(wx.Dialog):
    fixWin = None
    varWin = None
    fixHolidays = []
    varHolidays = []

    def __init__(self, parent, plugin):
        self.plugin = plugin
        wx.Dialog.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE,
            name = self.plugin.text.holidButton
        )
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.panel = parent
        self.fixHolidays, self.varHolidays = cpy(self.panel.holidays)
        self.Bind(wxCal.EVT_CALENDAR_DAY, self.OnChangeDay)


    def ShowHolidaysFrame(self):
        text = self.plugin.text
        self.SetTitle(self.plugin.text.holidButton)
        self.fixWin = CalendarPopup(self, False, self.plugin.first_day)
        self.varWin = CalendarPopup(self, True, self.plugin.first_day)
        calW, calH = self.fixWin.GetWinSize()
        fixLbl = wx.StaticText(self, -1, text.fixBoxLabel)
        variableLbl = wx.StaticText(self, -1, text.varBoxLabel)
        widthList = [self.GetTextExtent("30. %s 2000" % month)[0] +
            SYS_VSCROLL_X for month in list(month_name)]
        widthList.append(fixLbl.GetSize()[0])
        widthList.append(variableLbl.GetSize()[0])
        w = max(widthList) + 5
        self.SetMinSize((w + calW + 30, 2 * calH + 128))
        self.fixListBox = HolidaysBox(
            self,
            -1,
            size = wx.Size(w, 130),
            style = wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        self.fix_add_Btn = wx.Button(self, -1, text.add)
        self.fix_del_Btn = wx.Button(self, -1, text.delete)
        self.fix_del_Btn.Enable(False)
        self.varListBox = HolidaysBox(
            self,
            -1,
            size = wx.Size(w, 130),
            style = wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        self.var_add_Btn = wx.Button(self, -1, text.add)
        self.var_del_Btn = wx.Button(self, -1, text.delete)
        self.var_del_Btn.Enable(False)
        line = wx.StaticLine(self, -1, style = wx.LI_HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        fixSizer = wx.GridBagSizer(2, 8)
        fixSizer.SetMinSize((w + 8 + calW, -1))
        varSizer = wx.GridBagSizer(2, 8)
        varSizer.SetMinSize((w + 8 + calW, -1))
        fixSizer.Add(fixLbl, (0, 0))
        fixSizer.Add(self.fixListBox, (1, 0), (3, 1))
        fixSizer.Add(self.fix_add_Btn, (1, 1))
        fixSizer.Add((-1, 15), (2, 1))
        fixSizer.Add(self.fix_del_Btn, (3, 1))
        varSizer.Add(variableLbl, (0, 0))
        varSizer.Add(self.varListBox, (1, 0), (3,1))
        varSizer.Add(self.var_add_Btn, (1, 1))
        varSizer.Add((-1, 15), (2, 1))
        varSizer.Add(self.var_del_Btn, (3, 1))
        sizer.Add(fixSizer, 0, wx.EXPAND|wx.ALL, 8)
        sizer.Add((-1, 12))
        sizer.Add(varSizer, 0, wx.EXPAND|wx.ALL, 8)
        sizer.Add((1, 16))
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(line, 0, wx.EXPAND)
        sizer.Add((1,5))
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sz = self.GetMinSize()
        self.SetSize(sz)
        self.fixListBox.Reset(self.fixHolidays)
        self.varListBox.Reset(self.varHolidays)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        btn2.Bind(wx.EVT_BUTTON, self.onCancel)
        btn1.Bind(wx.EVT_BUTTON, self.onOK)
        self.fix_add_Btn.Bind(wx.EVT_BUTTON, self.onFixAddBtn)
        self.var_add_Btn.Bind(wx.EVT_BUTTON, self.onVarAddBtn)
        self.fix_del_Btn.Bind(wx.EVT_BUTTON, self.onFixDelBtn)
        self.var_del_Btn.Bind(wx.EVT_BUTTON, self.onVarDelBtn)
        self.Bind(wx.EVT_LISTBOX, self.onHolBoxSel)
        sizer.Layout()
        self.SetSizer(sizer)
        self.MakeModal(True)
        self.Show(True)


    def onClose(self, evt):
        self.MakeModal(False)
        self.GetParent().GetParent().Raise()
        self.Destroy()


    def onCancel(self, evt):
        self.Close()


    def onOK(self, evt):
        self.panel.holidays = (self.fixHolidays, self.varHolidays)
        self.Close()


    def onHolBoxSel(self, evt):
        if  evt.GetId() == self.fixListBox.GetId():
            self.fix_del_Btn.Enable(True)
        else:
            self.var_del_Btn.Enable(True)
        evt.Skip()


    def onFixAddBtn(self, evt):
        pos = self.ClientToScreen(self.fix_add_Btn.GetPosition())
        self.fixWin.PopUp(pos, self.fixHolidays)


    def onVarAddBtn(self, evt):
        pos = self.ClientToScreen(self.var_add_Btn.GetPosition())
        self.varWin.PopUp(pos, self.varHolidays)


    def onFixDelBtn(self, evt):
        self.fixHolidays.pop(self.fixListBox.GetSelection())
        if self.fixListBox.Reset(self.fixHolidays):
            self.fix_del_Btn.Enable(False)


    def onVarDelBtn(self, evt):
        self.varHolidays.pop(self.varListBox.GetSelection())
        if self.varListBox.Reset(self.varHolidays):
            self.var_del_Btn.Enable(False)


    def OnChangeDay(self, evt):
        if evt.GetId() == self.fixWin.GetCalId():
            self.fixListBox.Reset(self.fixHolidays)
        else:
            self.varListBox.Reset(self.varHolidays)
        evt.Skip()
#===============================================================================

class HolidaysBox(wx.ListBox):

    def __init__ (self, parent, id, size, style):
        wx.ListBox.__init__(
            self,
            parent = parent,
            id = id,
            size = size,
            style = style
        )
        self.sel = -1
        self.Bind(wx.EVT_LISTBOX, self.onHolBoxSel)


    def Reset(self, list):
        tmpList = []
        for item in list:
            day = item[-1]
            day = "  %i" % day if day < 10 else "%i" % day
            if len(item) == 2:
                tmpList.append("%s. %s" % (day, month_name[item[0]]))
            else:
                tmpList.append("%s. %s %i" % (day, month_name[item[1]], item[0]))
        self.Set(tmpList)
        if self.sel > -1 and self.sel < self.GetCount():
            self.SetSelection(self.sel)
            return False
        else:
            return True


    def  onHolBoxSel(self, evt):
        self.sel = evt.GetSelection()
        evt.Skip()
#===============================================================================

class CalendarPopup(wx.PopupWindow):
    yearChange = True

    def __init__(self, parent, yearChange, first_day):
        self.yearChange = yearChange
        wx.PopupWindow.__init__(self, parent)
        startDate = wx.DateTime()
        startDate.Set(1, 0)
        self.cal = wxCal.CalendarCtrl(
            self,
            -1,
            startDate,
            style = (wxCal.CAL_MONDAY_FIRST, wxCal.CAL_SUNDAY_FIRST)[first_day]
                | wxCal.CAL_SHOW_HOLIDAYS
                | wxCal.CAL_SEQUENTIAL_MONTH_SELECTION
                | wxCal.CAL_SHOW_SURROUNDING_WEEKS
        )
        self.cal.EnableYearChange(yearChange)
        sz = self.cal.GetBestSize()
        self.SetSize(sz)
        self.cal.Bind(wxCal.EVT_CALENDAR_DAY, self.OnChangeDay)
        self.cal.Bind(wxCal.EVT_CALENDAR_MONTH, self.OnChangeMonth)
        self.cal.Bind(wxCal.EVT_CALENDAR_YEAR, self.OnChangeMonth)
        self.cal.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)


    def OnLeaveWindow(self, evt):
        self.PopDown()
        evt.Skip()


    def GetCalId(self):
        return self.cal.GetId()


    def GetWinSize(self):
        return self.GetSize()


    def OnChangeDay(self, evt):
        date = evt.GetDate()
        day, month, year = date.GetDay(), 1 + date.GetMonth(), date.GetYear()
        newHoliday = (year, month, day) if self.yearChange else (month, day)
        if not newHoliday in self.holidays:
            self.holidays.append(newHoliday)
            self.holidays.sort()
        date = self.cal.GetDate()
        self.cal.SetHoliday(day)
        date.AddDS(wx.DateSpan.Day())
        self.cal.SetDate(date)
        self.Refresh()
        evt.Skip()


    def OnChangeMonth(self, evt = None):
        date = self.cal.GetDate()
        cur_month = date.GetMonth() + 1   # convert wx.DateTime 0-11 => 1-12
        if self.yearChange:
            cur_year = date.GetYear()
            for year, month, day in self.holidays:
                if year == cur_year and month == cur_month:
                    self.cal.SetHoliday(day)
        else:
            for month, day in self.holidays:
                if month == cur_month:
                    self.cal.SetHoliday(day)


    def PopUp(self, position, holidays):
        self.cal.EnableHolidayDisplay(False)
        self.cal.EnableHolidayDisplay(True)
        self.SetPosition(position)
        self.holidays = holidays
        self.OnChangeMonth()
        self.Show(True)


    def PopDown(self):
        self.Show(False)
        self.Close()
#===============================================================================

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):

    def __init__(self, parent, text, width):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            size = (width, 164),
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL
        )
        CheckListCtrlMixin.__init__(self)
        curFile = abspath(join(dirname(__file__), "contextCursor.cur"))
        img = None
        if exists(curFile):
            img = wx.EmptyImage(32, 32)
            img.LoadFile(curFile, wx.BITMAP_TYPE_CUR)
        if not img or not img.IsOk():
            from cStringIO import StringIO
            from base64 import b64decode
            stream = StringIO(b64decode(CUR_STRING))
            img = wx.ImageFromStream(stream)
            stream.close()
            img.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 0)
            img.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 0)
        self.SetCursor(wx.CursorFromImage(img))
        self.selRow = -1
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        for i, colLabel in enumerate(text.header):
            self.InsertColumn(i, colLabel)
        self.InsertStringItem(0, " ")
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetStringItem(0, 1, "Test Name")
        self.SetStringItem(0, 2, "8888-88-88 88:88:88")
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        col0 = self.GetColumnWidth(0)
        col23 = self.GetColumnWidth(2)
        self.SetColumnWidth(3, col23)
        self.SetColumnWidth(
            1,
            width - col0 - 2*col23 - SYS_VSCROLL_X-self.GetWindowBorderSize()[0]
        )
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)


    def OnItemSelected(self, evt):
        self.SelRow(evt.m_itemIndex)
        evt.Skip()


    # this is called by the base class when an item is checked/unchecked !!!!!!!
    def OnCheckItem(self, index, flag):
        evt = eg.ValueChangedEvent(self.GetId(), value = (index, flag))
        wx.PostEvent(self, evt)


    def SelRow(self, row):
        if row != self.selRow:
            if self.selRow in range(self.GetItemCount()):
                item = self.GetItem(self.selRow)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.selRow = row
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)


    def AppendRow(self):
        ix = self.GetItemCount()
        self.InsertStringItem(ix, "")
        self.CheckItem(ix)
        self.EnsureVisible(ix)
        self.SelRow(ix)
#===============================================================================

class ManagerDialog(wx.Dialog):

    def __init__(self, text, plugin):
        wx.Dialog.__init__(
            self,
            None,
            -1,
            text.dialogTitle % version,
            style = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.RESIZE_BORDER,
        )

        self.plugin = plugin
        statusRS = self.plugin.GetStatusRS()

        self.idUp      = wx.NewId()
        self.idDown    = wx.NewId()
        self.idTop     = wx.NewId()
        self.idBottom  = wx.NewId()
        self.idSort    = wx.NewId()
        self.idRefr    = wx.NewId()
        self.idPlay    = wx.NewId()
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.plugin.manager = self
        self.text = text
        self.Bind(wx.EVT_CLOSE, self.onClose)

        statPath = self.plugin.RadioSurePath+"\\Stations"
        rsd_files = [x for x in listdir(statPath) if x.endswith('.rsd') and x.startswith('stations-')]
        stations = statPath+"\\"+rsd_files[0]

        def unique(seq):
            res = set(seq)
            res = list(res)
            res.sort()
            return res

        f = openFile(stations, encoding='utf-8', mode='r')
        data = self.data = [item.split("\t") for item in f.readlines()]
        genres = [item[2] for item in data]
        genres = unique(genres)
        countrys = [item[3] for item in data]
        countrys = unique(countrys)
        languages = [item[4] for item in data]
        languages = unique(languages)
        titles = [item[0] for item in data]
        titles = unique(titles)
        f.close()

        curFile = abspath(join(dirname(__file__), "contextCursor.cur"))
        img = None
        if exists(curFile):
            img = wx.EmptyImage(32, 32)
            img.LoadFile(curFile, wx.BITMAP_TYPE_CUR)
        if not img or not img.IsOk():
            from cStringIO import StringIO
            from base64 import b64decode
            stream = StringIO(b64decode(CUR_STRING))
            img = wx.ImageFromStream(stream)
            stream.close()
            img.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 0)
            img.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 0)
        self.grid = wx.ListCtrl(self, style = wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_HRULES|wx.LC_VRULES)
        self.grid.SetCursor(wx.CursorFromImage(img))
        self.grid.InsertColumn(0,"")

        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(self, self.idUp, bmp)
        btnUP.SetToolTipString(self.text.toolTipUp)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(self, self.idDown, bmp)
        btnDOWN.SetToolTipString(self.text.toolTipDown)
        #Button DEL
        bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_OTHER, (16, 16))
        btnDEL = wx.BitmapButton(self, -1, bmp)
        btnDEL.SetToolTipString(self.text.toolTipDelete)

        btnExp = wx.Button(self, wx.ID_SAVEAS, self.text.export)
        btnExp.SetToolTipString(self.text.toolTipExport)

        btnImp = wx.Button(self, wx.ID_OPEN, self.text.imprt)
        btnImp.SetToolTipString(self.text.toolTipImport)

        btnImpSR = wx.Button(self, wx.ID_FILE, self.text.importSR)
        btnImpSR.SetToolTipString(self.text.toolTipImportSR)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_HELP_SETTINGS, wx.ART_OTHER, (16, 16))
        btnSort = wx.BitmapButton(self, self.idSort, bmp)
        btnSort.SetToolTipString(self.text.sort)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, (16, 16))
        btnRefr = wx.BitmapButton(self, self.idRefr, bmp)
        btnRefr.SetToolTipString(self.text.refresh)



        def EnableCtrls():
            first = self.grid.GetFirstSelected()
            cnt = self.grid.GetSelectedItemCount()
            subseq = True
            for ix in range(first, first + cnt):
                if not self.grid.IsSelected(ix):
                    subseq = False
                    break
            one = cnt==1
            self.menuFlagM = subseq

            itemCnt = self.grid.GetItemCount()
            upDown = cnt > 0 and cnt < itemCnt and subseq
            sourceLabel.Enable(one)
            genreLabel.Enable(one)
            langLabel.Enable(one)
            countryLabel.Enable(one)
            sourceCtrl.Enable(one)
            btnUP.Enable(upDown)
            btnDOWN.Enable(upDown)
            btnDEL.Enable(cnt > 0)
            btnExp.Enable(itemCnt > 0)
            btnSort.Enable(itemCnt > 1)


        def ListSelection(event=None):
            EnableCtrls()
            first = self.grid.GetFirstSelected()
            cnt = self.grid.GetSelectedItemCount()
            if cnt == 1:
                item = self.tmpFavs[first]
                src = item[0]
                sourceCtrl.Clear()
                srcs = ()
                i = -1
                for ix in range(5, 11):
                    srcIx = [itm[ix] for itm in data]
                    if src in srcIx:
                        i = srcIx.index(src)
                        break
                if i > -1:
                    srcs = data[i][5:]
                    sourceCtrl.AppendItems(srcs)
                if not src in srcs:
                    sourceCtrl.Append(src)
                sourceCtrl.SetStringSelection(src)
                if item[2] in genres:
                    genreCtrl.SetStringSelection(item[2])
                if item[3] in languages:
                    langCtrl.SetStringSelection(item[3])
                if item[4] in countrys:
                    countryCtrl.SetStringSelection(item[4])
            else:
                sourceCtrl.SetSelection(-1)
                genreCtrl.SetSelection(-1)
                langCtrl.SetSelection(-1)
                countryCtrl.SetSelection(-1)
            if event:
                event.Skip()
        self.grid.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        self.grid.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)


        def onRefresh(evt = None, seq = None):
            self.favs = seq if seq else self.plugin.RefreshVariables()
            self.tmpFavs = cpy(self.favs)
            self.grid.DeleteAllItems()
            for row in range(len(self.tmpFavs)):
                self.grid.InsertStringItem(row, self.tmpFavs[row][1])
            self.grid.SetColumnWidth(0, -1)
            self.grid.SetColumnWidth(0, self.grid.GetColumnWidth(0) + 6)
            ListSelection()
            self.Diff()
            EnableCtrls()
            #evt.Skip
        btnRefr.Bind(wx.EVT_BUTTON, onRefresh)


        def onSort(evt):
            self.tmpFavs = sorted(self.tmpFavs, key=lambda i: strxfrm(i[1].encode(eg.systemEncoding)))
            self.grid.DeleteAllItems()
            for row in range(len(self.tmpFavs)):
                self.grid.InsertStringItem(row, self.tmpFavs[row][1])
            ListSelection()
            self.Diff()
            self.Colour()
        btnSort.Bind(wx.EVT_BUTTON, onSort)

        sourceLabel = wx.StaticText(self, -1, self.text.lblSource)
        genreLabel = wx.StaticText(self, -1, self.text.lblGenre)
        langLabel = wx.StaticText(self, -1, self.text.lblLanguage)
        countryLabel = wx.StaticText(self, -1, self.text.lblCountry)
        sourceCtrl = wx.Choice(self, -1, choices=[])
        genreCtrl = wx.Choice(self, -1, choices=genres)
        langCtrl = wx.Choice(self, -1, choices=languages)
        countryCtrl = wx.Choice(self, -1, choices=countrys)
        genreCtrl.Enable(False)
        langCtrl.Enable(False)
        countryCtrl.Enable(False)
        line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK, self.text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL, self.text.cancel)
        btn3 = wx.Button(self, wx.ID_APPLY, self.text.apply)
        btn1.Bind(wx.EVT_BUTTON, self.onBtn)
        btn2.Bind(wx.EVT_BUTTON, self.onBtn)
        btn3.Bind(wx.EVT_BUTTON, self.onBtn)
        btnExp.Bind(wx.EVT_BUTTON, self.onBtnsInOut)
        btnImp.Bind(wx.EVT_BUTTON, self.onBtnsInOut)
        btnImpSR.Bind(wx.EVT_BUTTON, self.onBtnsInOut)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add(btnExp,0,wx.LEFT)
        btnsizer.Add((8,-1),0)
        btnsizer.Add(btnImp,0,wx.CENTER)
        btnsizer.Add((8,-1),0)
        btnsizer.Add(btnImpSR,0,wx.CENTER)
        btnsizer.Add((-1,-1),1)
        btnsizer.Add(btn1,0,wx.CENTER)
        btnsizer.Add((8,-1),0)
        btnsizer.Add(btn2,0,wx.CENTER)
        btnsizer.Add((8,-1),0)
        btnsizer.Add(btn3,0,wx.RIGHT)
        btnsizer.Layout()
        w = btn1.GetSize()[0]+btn2.GetSize()[0]+btn3.GetSize()[0]+btnExp.GetSize()[0]+btnImp.GetSize()[0]+btnImpSR.GetSize()[0]+5*8
        w1 = btnUP.GetSize()[0]+8

        onRefresh()

        self.grid.SetMinSize((w-w1,-1))
        szr = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(1,5)
        sizer.Add(wx.StaticText(self, -1, self.text.lblList),(0,0),(1,2))
        sizer.Add(self.grid, (1,0), (7, 2), wx.EXPAND, 5)
        sizer.Add(btnUP, (1,2), (1, 1),flag=wx.RIGHT)
        sizer.Add(btnDOWN, (2,2), (1, 1),flag=wx.RIGHT)
        sizer.Add(btnDEL, (3,2), (1, 1),flag=wx.RIGHT)
        sizer.Add((5,20), (4,2), (1, 1),flag=wx.RIGHT)
        sizer.Add(btnRefr, (5,2), (1, 1),flag=wx.RIGHT)
        sizer.Add(btnSort, (6,2), (1, 1),flag=wx.RIGHT)


        sizer.Add(sourceLabel, (8,0), (1, 1),wx.TOP, 10)
        sizer.Add(sourceCtrl, (8,1), (1, 2), wx.EXPAND|wx.TOP, 5)
        sizer.Add(genreLabel, (9,0), (1, 1),wx.TOP, 10)
        sizer.Add(genreCtrl, (9,1), (1, 2), wx.EXPAND|wx.TOP, 5)
        sizer.Add(langLabel, (10,0), (1, 1),wx.TOP, 10)
        sizer.Add(langCtrl, (10,1), (1, 2), wx.EXPAND|wx.TOP, 5)
        sizer.Add(countryLabel, (11,0), (1, 1),wx.TOP, 10)
        sizer.Add(countryCtrl, (11,1), (1, 2), wx.EXPAND|wx.TOP, 5)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(7)
        szr.Add(sizer, 1, wx.EXPAND|wx.ALL, 5)
        szr.Add(line, 0, wx.EXPAND|wx.TOP, 3)
        szr.Add(btnsizer, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(szr)
        self.Fit()

        #Learn New MINSIZE:
        #====================
        if ConfigData.plcmnt:
    #    if 0:
            self.SetPosition(ConfigData.plcmnt[0])
            sz = ConfigData.plcmnt[1]
            minsz = ConfigData.plcmnt[2]
        else:
            self.Center()
            sz = (w+w1, self.GetSize()[1] + btn1.GetSize()[1] + 10)
            minsz = sz
        self.SetMinSize(minsz)
        self.SetSize(sz)
        self.Show(True)


        def onSource(evt):
            if self.grid.GetSelectedItemCount() == 1:
                self.tmpFavs[self.grid.GetFirstSelected()][0] = evt.GetString()
                self.Diff()
        sourceCtrl.Bind(wx.EVT_CHOICE, onSource)


        def Move(evt):
            id = evt.GetId()
            first = self.grid.GetFirstSelected()
            cnt = self.grid.GetSelectedItemCount()
            if id == self.idUp:
                if first:
                    bit = self.tmpFavs.pop(first-1)
                    self.tmpFavs.insert(first-1+cnt, bit)
                else:
                    id = self.idBottom
            elif id == self.idDown:
                if first+cnt < len(self.tmpFavs):
                    bit = self.tmpFavs.pop(first+cnt)
                    self.tmpFavs.insert(first, bit)
                else:
                    id = self.idTop
            if id in (self.idBottom, self.idTop):
                p1=self.tmpFavs[:first]
                p2=self.tmpFavs[first:first+cnt]
                p3=self.tmpFavs[first+cnt:]
                if id == self.idTop:
                    p2.extend(p1)
                    p2.extend(p3)
                    self.tmpFavs = p2
                elif id == self.idBottom:
                    p1.extend(p3)
                    p1.extend(p2)
                    self.tmpFavs = p1
            self.grid.DeleteAllItems()
            for row in range(len(self.tmpFavs)):
                self.grid.InsertStringItem(row, self.tmpFavs[row][1])
            if id == self.idUp:
                if first:
                    b, e = (first-1, first-1+cnt)
            elif id == self.idDown:
                if first+cnt < len(self.tmpFavs):
                    b, e = (first+1,first+1+cnt)
            elif id == self.idBottom:
                ln = len(self.tmpFavs)
                b, e = (ln-cnt, ln)
            elif id == self.idTop:
                b, e = (0, cnt)
            for ix in range(b, e):
                    self.grid.Select(ix, True)
            self.grid.EnsureVisible(ix)
            self.Diff()
            self.Colour()
        btnUP.Bind(wx.EVT_BUTTON, Move)
        btnDOWN.Bind(wx.EVT_BUTTON, Move)


        def onRemDupl(evt):
            indexes=dict(map(None,[item[0] for item in self.tmpFavs],range(len(self.tmpFavs)))).values()
            indexes.sort()
            tmp = []
            for ix in indexes:
                tmp.append(self.tmpFavs[ix])
            onRefresh(None, tmp)
            self.Diff()
            self.Colour()


        def onDelete(evt):
            cnt = self.grid.GetItemCount()
            for ix in range(cnt-1, -1, -1):
                if self.grid.IsSelected(ix):
                    self.grid.DeleteItem(ix)
                    self.tmpFavs.pop(ix)
            EnableCtrls()
            self.Diff()
            self.Colour()
        btnDEL.Bind(wx.EVT_BUTTON, onDelete)


        def onPlayNow(evt):
            ix = self.grid.GetFirstSelected()
            self.plugin.RefreshVariables()
            sel = self.tmpFavs[ix][1]
            src = sourceCtrl.GetStringSelection()
            rsList = [item[1] for item in self.plugin.Favorites]
            hwnds = HandleRS()
            indx = None
            if sel in [item[1] for item in self.plugin.Favorites]:
                indx = rsList.index(sel)
                if src != self.plugin.Favorites[indx][0]:
                    indx = None
            if indx is not None: # start with favorite index
                if not hwnds:
                    hwnds = self.plugin.GetNewHwnd()
                    if hwnds:
                        SendMessage(hwnds[0], WM_COMMAND, 4102+indx, 0)
                    else:
                        self.FailedToOpen()
                else:
                    for hwnd in hwnds:
                        x, rec = self.plugin.GetStatusRS([hwnd])
                        if rec != 1:
                            SendMessage(hwnd, WM_COMMAND, 4102+indx, 0)
                            break
                    if rec or rec is None:
                        hwnds = self.plugin.GetNewHwnd(hwnds)
                        if hwnds:
                            SendMessage(hwnds[0], WM_COMMAND, 4102+indx, 0)
                        else:
                            self.FailedToOpen()
            else: #start with source="blablabla"
                if not hwnds:
                    hwnds = self.plugin.GetNewHwnd(hwnds, src=src)
                    if not hwnds:
                        self.FailedToOpen()
                else:
                    for hwnd in hwnds:
                        x, rec = self.plugin.GetStatusRS([hwnd])
                        if rec != 1:
                            PostMessage(hwnd, WM_COMMAND, 1, 0) #close
                            i = 0
                            while hwnd in hwnds and i < 100:
                                hwnds = HandleRS()
                                i += 1
                            if i == 100:
                                self.PrintError(self.text.message6)
                                rec = 1
                            else:
                                hwnds = self.plugin.GetNewHwnd(hwnds, src=src)
                                if not hwnds:
                                    self.FailedToOpen()
                                    rec = 1
                                else:
                                    break
                    if rec or rec is None:
                        hwnds = self.plugin.GetNewHwnd(hwnds, src=src)
                        if not hwnds:
                            self.FailedToOpen()
        self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, onPlayNow)


        def AreDuplications():
            srcList = [item[0] for item in self.tmpFavs]
            return len(srcList) > len(set(srcList))


        def OnRightClick(evt):
            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewId()
                self.popupID2 = wx.NewId()
                self.Bind(wx.EVT_MENU, onDelete, id = self.popupID1)
                self.Bind(wx.EVT_MENU, onRemDupl, id = self.popupID2)
                self.Bind(wx.EVT_MENU, Move, id = self.idUp)
                self.Bind(wx.EVT_MENU, Move, id = self.idDown)
                self.Bind(wx.EVT_MENU, Move, id = self.idTop)
                self.Bind(wx.EVT_MENU, Move, id = self.idBottom)
                self.Bind(wx.EVT_MENU, onPlayNow, id = self.idPlay)
                self.Bind(wx.EVT_MENU, onSort, id = self.idSort)
                self.Bind(wx.EVT_MENU, onRefresh, id = self.idRefr)
                self.Bind(wx.EVT_MENU, self.onBtnsInOut, id = wx.ID_SAVEAS)
                self.Bind(wx.EVT_MENU, self.onBtnsInOut, id = wx.ID_SAVE)
                self.Bind(wx.EVT_MENU, self.onBtnsInOut, id = wx.ID_OPEN)
                self.Bind(wx.EVT_MENU, self.onBtnsInOut, id = wx.ID_FILE)
            menu = wx.Menu()
            if self.grid.GetSelectedItemCount() == 1:
                menu.Append(self.idPlay, self.text.play)
                menu.AppendSeparator()
            menu.Append(self.popupID1, self.text.toolTipDelete)
            if AreDuplications():
                menu.Append(self.popupID2, self.text.removeDupl)
            if self.grid.GetItemCount() > 1:
                menu.Append(self.idSort, self.text.sort)
            if self.menuFlagM:
                menu.AppendSeparator()
                menu.Append(self.idUp, self.text.toolTipUp)
                menu.Append(self.idDown, self.text.toolTipDown)
                menu.Append(self.idTop, self.text.moveTop)
                menu.Append(self.idBottom, self.text.moveBottom)
            menu.AppendSeparator()
            menu.Append(self.idRefr, self.text.refresh)
            menu.Append(wx.ID_SAVEAS, self.text.exportSel)
            menu.Append(wx.ID_SAVE, self.text.exportAll)
            menu.Append(wx.ID_OPEN, self.text.toolTipImport)
            menu.Append(wx.ID_FILE, self.text.toolTipImportSR)
            self.PopupMenu(menu)
            menu.Destroy()
            evt.Skip()
        self.grid.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, OnRightClick)


    def FailedToOpen(self):
        return MessageBox(
            self,
            self.text.message9, #failed to open
            self.text.messBoxTit6,
            wx.ICON_EXCLAMATION,
            15,
            plugin = self.plugin,
            )


    def CreateFavorites(self, dom, node, itmList = None, save = False):
        max = self.plugin.maxFav
        mssgs = []
        if save:
            #Duplications check
            indexes = dict(map(None,[item[0] for item in self.tmpFavs],range(len(self.tmpFavs)))).values()
            indexes.sort()
            tmp = []
            for ix in indexes:
                tmp.append(self.tmpFavs[ix])
            itmList = range(len(tmp))
            if len(self.tmpFavs) > len(tmp):
                mssgs.append(self.text.message8)
        else:
            tmp = self.tmpFavs
        flag = save and len(itmList) > max
        if flag:
            mssgs.append(self.text.message1 % self.plugin.maxFav)
        if mssgs:
            MessageBox(
                self,
                "\n".join(mssgs),
                self.plugin.text.messBoxTit1,
                wx.ICON_EXCLAMATION,
                plugin = self.plugin,
                )
        elm = 0
        for i in itmList:
            elm += 1
            if flag and elm > max:
                break
            item = tmp[i]
            itemNode = dom.createElement(u'Item-%i' % elm)
            sourceNode = dom.createElement(u'Source')
            sourceText = dom.createTextNode(unicode(item[0]))
            sourceNode.appendChild(sourceText)
            itemNode.appendChild(sourceNode)
            titleNode = dom.createElement(u'Title')
            titleText = dom.createTextNode(unicode(item[1]))
            titleNode.appendChild(titleText)
            itemNode.appendChild(titleNode)
            genreNode = dom.createElement(u'Genre')
            genreText = dom.createTextNode(unicode(item[2]))
            genreNode.appendChild(genreText)
            itemNode.appendChild(genreNode)
            languageNode = dom.createElement(u'Language')
            languageText = dom.createTextNode(unicode(item[3]))
            languageNode.appendChild(languageText)
            itemNode.appendChild(languageNode)
            countryNode = dom.createElement(u'Country')
            countryText = dom.createTextNode(unicode(item[4]))
            countryNode.appendChild(countryText)
            itemNode.appendChild(countryNode)
            node.appendChild(itemNode)


    def UpdateRadioSureXml(self):
        # create a backup of original file
        new_file_name = u'%s\\RadioSure.xml' % self.plugin.xmlpath
        old_file_name = new_file_name + "~"
        if exists(old_file_name):
            remove(old_file_name)
        rename(new_file_name, old_file_name)
        try:
            # change Favorites node
            doc = miniDom.parse(old_file_name)
            node = doc.getElementsByTagName('XMLConfigSettings')[0]
            oldFavorites = node.getElementsByTagName('Favorites')[0]
            newFavorites = doc.createElement(u'Favorites')
            self.CreateFavorites(doc, newFavorites, save = True)
            node.replaceChild(newFavorites, oldFavorites)
            # persist changes to new file
            f = file(new_file_name, "wb")
            writer = lookup('utf-8')[3](f)
            doc.writexml(writer, encoding = 'utf-8')
            f.close()
            MessageBox(
                self,
                self.text.message5, #updated
                self.text.messBoxTit5,
                wx.ICON_INFORMATION,
                15,
                plugin = self.plugin,
                )
            return True
        except:
            raise
            MessageBox(
                self,
                self.text.message3,
                self.plugin.text.messBoxTit1,
                wx.ICON_EXCLAMATION,
                plugin = self.plugin,
                )
            if exists(new_file_name):
                remove(new_file_name)
            rename(old_file_name, new_file_name)
            return False

    def onBtn(self, evt):

        def UpdateXml():
            closeFlag = self.UpdateRadioSureXml()
            rs = u'%s\\RadioSure.exe' % self.plugin.RadioSurePath
            rs = rs.encode(FSE) if isinstance(rs, unicode) else rs
            args = [rs]
            if isfile(rs):
                Popen(args)
            return closeFlag

        closeFlag = False
        id = evt.GetId()
        if id == wx.ID_APPLY or (id == wx.ID_OK and self.favs != self.tmpFavs):
            hwnds = HandleRS()
            rec = 0
            for hwnd in hwnds:
                rec = self.plugin.GetStatusRS([hwnd])[1]
                if rec:
                    break
            title = self.text.messBoxTit3 if rec else self.text.messBoxTit2

            if hwnds:
                # RS is running !
                res = MessageBox(
                    self,
                    self.text.message2 % (self.plugin.text.yes, self.plugin.text.no),
                    title,
                    wx.ICON_EXCLAMATION|wx.YES_NO|wx.YES_DEFAULT,
                    plugin = self.plugin,
                    )
                if res == wx.ID_YES:
                    for hwnd in hwnds:
                        rec = self.plugin.GetStatusRS([hwnd])[1]
                        if rec:
                            PostMessage(hwnd, WM_COMMAND, 1051, 0) # Stop Rec
                            i=0
                            while rec and i < 100:
                                i+=1
                                rec = self.plugin.GetStatusRS([hwnd])[1]
                                sleep(0.1)
                            if not rec:
                                PostMessage(hwnd, WM_COMMAND, 1, 0) # Close
                        else:
                            PostMessage(hwnd, WM_COMMAND, 1, 0) # Close
                    i = 0
                    while hwnds and i < 100:
                        i += 1
                        hwnds = HandleRS()
                    if hwnds:
                        pid = eg.WinApi.Utils.PyGetWindowThreadProcessId(hwnd)[1]
                        handle = _kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
                        succ = _kernel32.TerminateProcess(handle, -1)
                        _kernel32.CloseHandle(handle)
                        if not succ:
                            MessageBox(
                                self,
                                self.text.message6, #failed to close
                                self.text.messBoxTit6,
                                wx.ICON_EXCLAMATION,
                                15,
                                plugin = self.plugin,
                                )
                        else:
                            closeFlag = UpdateXml()
                    else:
                        closeFlag = UpdateXml()
                else:
                    MessageBox(
                        self,
                        self.text.message7, #no update
                        self.text.messBoxTit7,
                        wx.ICON_EXCLAMATION,
                        15,
                        plugin = self.plugin,
                        )
            else:
                closeFlag = self.UpdateRadioSureXml()

        if id == wx.ID_APPLY and closeFlag:
            self.favs = cpy(self.tmpFavs)
            self.Diff()

        if id != wx.ID_APPLY:
            if id != wx.ID_OK or closeFlag or self.favs == self.tmpFavs:
                self.Close()
        #evt.Skip()


    def Import(self, data):
        # ToDo: Add check of duplications ???
        self.tmpFavs.extend(data)
        self.grid.DeleteAllItems()
        for row in range(len(self.tmpFavs)):
            self.grid.InsertStringItem(row, self.tmpFavs[row][1])
        self.grid.SetColumnWidth(0, -1)
        self.grid.SetColumnWidth(0, self.grid.GetColumnWidth(0) + 6)
        self.grid.EnsureVisible(len(self.tmpFavs)-1)
        self.grid.SetFocus()
        self.Colour()
        self.Diff()


    def Colour(self):
        maxF = self.plugin.maxFav
        cnt = self.grid.GetItemCount()
        fore = self.grid.GetTextColour()
        for row in range(min(maxF, cnt)):
            item = self.grid.GetItem(row)
            item.SetTextColour(fore)
            self.grid.SetItem(item)
        if maxF >= cnt:
            return
        for row in range(maxF, cnt):
            item = self.grid.GetItem(row)
            item.SetTextColour("red")
            self.grid.SetItem(item)


    def onBtnsInOut(self, evt):
        id = evt.GetId()
        if id == wx.ID_SAVEAS or id == wx.ID_SAVE:
            dlg = wx.FileDialog(
                self,
                message = self.text.save,
                defaultDir = self.plugin.xmlpath,
                defaultFile = "Favorites.xml",
                wildcard = self.text.wildcard,
                style=wx.SAVE
                )
            if dlg.ShowModal() == wx.ID_OK:
                self.Export(dlg.GetPath(), id)
            dlg.Destroy()
        elif id == wx.ID_OPEN: # Import
            dlg = wx.FileDialog(
                self,
                message = self.text.choose,
                defaultDir = self.plugin.xmlpath,
                defaultFile = "*.xml",
                wildcard = self.text.wildcard,
                style = wx.OPEN | wx.CHANGE_DIR
                )
            flg = True
            filePath = None
            if dlg.ShowModal() == wx.ID_OK:
                filePath = dlg.GetPath()
                dlg.Destroy()
                xmldoc = miniDom.parse(filePath)
                document = xmldoc.getElementsByTagName('Favorites')
                if len(document) > 0:
                    stations = getStations(document[0])
                    if stations:
                        flg = False
                        self.Import(stations)
            if flg and filePath:
                MessageBox(
                    self,
                    self.text.message4 % split(filePath)[1],
                    self.plugin.text.messBoxTit1,
                    wx.ICON_EXCLAMATION,
                    plugin = self.plugin,
                    )
        elif id == wx.ID_FILE: # Import SR
            dlg = wx.FileDialog(
                self,
                message = self.text.choose,
                defaultDir = eg.folderPath.ProgramFiles+'\\Screamer',
                defaultFile = "favorites.xml",
                wildcard = self.text.wildcard,
                style = wx.OPEN | wx.CHANGE_DIR
                )
            if dlg.ShowModal() == wx.ID_OK:
                filePath = dlg.GetPath()
                dlg.Destroy()
                stations = self.ImportSR(filePath)
                if not stations:
                    MessageBox(
                        self,
                        self.text.message4 % split(filePath)[1],
                        self.plugin.text.messBoxTit1,
                        wx.ICON_EXCLAMATION,
                        plugin = self.plugin,
                        )
                else:
                    self.Import(stations)
        evt.Skip()
        return


    def Diff(self):
        wx.FindWindowById(wx.ID_APPLY).Enable(self.favs != self.tmpFavs)


    def onClose(self, evt):
        hwnd = self.GetHandle()
        wp = GetWindowPlacement(hwnd)[4]
        cdr = wx.GetClientDisplayRect()
        #Note: GetPosition() return (-32000, -32000), if window is minimized !!!
        plcmnt = (
            (wp[0] + cdr[0], wp[1] + cdr[1]),                            # pos
            (wp[2] - wp[0], wp[3] - wp[1]),                              # size
            (self.GetMinSize().GetWidth(),self.GetMinSize().GetHeight()) # min size
        )
        if plcmnt != ConfigData.plcmnt:
            ConfigData.plcmnt = plcmnt
            #if not eg.document.IsDirty():
            #    wx.CallAfter(eg.Notify, "DocumentChange", True)
        self.plugin.manager = None
        wx.CallAfter(self.Show, False)
        wx.CallAfter(self.Destroy)
        evt.Skip()


    def ImportSR(self, filePath):
        xmldoc = miniDom.parse(filePath)
        document = xmldoc.getElementsByTagName('Screamer')
        if len(document) > 0:
            res = []
            stations = tuple(document[0].getElementsByTagName('Station'))
            for station in stations:
                if "title" in station.attributes.keys():
                    title = station.attributes["title"].value
                else:
                    return None
                src = station.getElementsByTagName('Source')
                if len(src)>0:
                    src = src[0].firstChild.data
                    i = -1
                    for ix in range(5, 11):
                        srcIx = [itm[ix] for itm in self.data]
                        if src in srcIx:
                            i = srcIx.index(src)
                            break
                    if i > -1:
                        station = self.data[i]
                        itm = (src, station[0], station[2], station[4], station[3])
                    else:
                        itm = (src, title, "-", "-", "-")
                    res.append(itm)
                else:
                    return None
            return res
        return None


    def Export(self, path, id):
        impl = miniDom.getDOMImplementation()
        dom = impl.createDocument(None, u'XMLConfigSettings', None)
        root = dom.documentElement
        commentNode = dom.createComment(self.text.xmlComment1)
        dom.insertBefore(commentNode, root)
        commentNode = dom.createComment(self.text.xmlComment2 % str(dt.now())[:19])
        dom.insertBefore(commentNode, root)
        favNode = dom.createElement(u'Favorites')
        root.appendChild(favNode)
        if id == wx.ID_SAVEAS and self.grid.GetSelectedItemCount():
            itmList = [itm for itm in range(len(self.tmpFavs)) if self.grid.IsSelected(itm)]
        else:
            itmList = range(len(self.tmpFavs))
        self.CreateFavorites(dom, favNode, itmList)
        f = file(path, 'wb')
        writer = lookup('utf-8')[3](f)
        dom.writexml(writer, encoding = 'utf-8')
        f.close()
#===============================================================================

class SchedulerDialog(wx.Dialog):
    lastRow = -1
    applyBttn = None

    def __init__(self, text, plugin):
        wx.Dialog.__init__(
            self,
            None,
            -1,
            text.dialogTitle % version,
            style = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX|wx.CLOSE_BOX,
        )

        #import locale as l
        #l.setlocale(l.LC_ALL, "us") # only for testing

        bttns = []
        self.ctrls=[]
        self.plugin = plugin
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.plugin.dialog = self
        self.tmpData = self.plugin.tmpData = cpy(self.plugin.data)
        self.text = text

        def fillDynamicSizer(type, data = None, old_type = 255):
            flag = old_type != type
            if flag:
                dynamicSizer.Clear(True)
                self.ctrls=[]
                self.ctrls.append(wx.NewId())
                self.ctrls.append(wx.NewId())
            if type == -1:
                return
            if type != 1 and flag:
                topSizer = wx.StaticBoxSizer(
                    wx.StaticBox(self, -1, self.text.chooseDay),
                    wx.HORIZONTAL
                )
            if type == 0:
                if flag:
                    self.ctrls.append(wx.NewId())
                    dp = wx.DatePickerCtrl(self, self.ctrls[2], size = (86, -1),
                            style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    topSizer.Add(dp,0,wx.EXPAND)
                    self.ctrls.append(wx.NewId())
                    yearlyCtrl = wx.CheckBox(self, self.ctrls[3], self.text.yearly)
                    topSizer.Add(yearlyCtrl, 0, wx.EXPAND|wx.LEFT, 30)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND|wx.TOP, 2)
                else:
                    dp = wx.FindWindowById(self.ctrls[2])
                    yearlyCtrl = wx.FindWindowById(self.ctrls[3])
                if data:
                    if not data[2]:
                        val = wx.DateTime_Now()
                        data[2] = str(dt.now())[:10]
                    wxDttm = wx.DateTime()
                    wxDttm.Set(
                        int(data[2][8:10]),
                        int(data[2][5:7]) - 1,
                        int(data[2][:4])
                    )
                    dp.SetValue(wxDttm)
                    yearlyCtrl.SetValue(data[3])
            elif type == 2:
                if flag:
                    if self.plugin.first_day:
                        choices = list(day_name)[:-1]
                        choices.insert(0, list(day_name)[-1])
                    else:
                        choices = list(day_name)
                    self.ctrls.append(wx.NewId())
                    weekdayCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = choices,
                        size=((-1,110)),
                    )
                    self.ctrls.append(wx.NewId())
                    holidCheck_2 = wx.CheckBox(
                        self,
                        self.ctrls[3],
                        self.text.holidCheck_2
                    )
                    self.ctrls.append(wx.NewId())
                    holidCheck_1 = wx.CheckBox(
                        self,
                        self.ctrls[4],
                        self.text.holidCheck_1
                    )
                    topSizer.Add((40,1), 0, wx.ALIGN_CENTER)
                    topSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.theEvery
                        ),
                        0,
                        wx.ALIGN_CENTER | wx.RIGHT, 10
                    )
                    topSizer.Add(weekdayCtrl, 0, wx.TOP)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP,2)
                    dynamicSizer.Add(holidCheck_1, 0, wx.TOP, 2)
                    dynamicSizer.Add(holidCheck_2, 0, wx.TOP, 2)
                else:
                    weekdayCtrl = wx.FindWindowById(self.ctrls[2])
                    holidCheck_2 = wx.FindWindowById(self.ctrls[3])
                    holidCheck_1 = wx.FindWindowById(self.ctrls[4])
                val = 127 if not data else data[2]
                if self.plugin.first_day:
                    exp = [6, 0, 1, 2, 3, 4, 5]
                else:
                    exp = [0, 1, 2, 3, 4, 5, 6]
                for i in range(7):
                    weekdayCtrl.Check(i, bool(val & (2 ** exp[i])))
                enable = val & 31 and not val & 96
                holidCheck_1.Enable(enable)
                check = 0 if (not data or not enable) else data[4]
                holidCheck_1.SetValue(check)
                enable = val & 96 and not val & 31
                holidCheck_2.Enable(enable)
                check = 0 if (not data or not enable) else data[3]
                holidCheck_2.SetValue(check)
            elif type == 3: # Monthly/weekday ...
                if flag:
                    dateSizer = wx.BoxSizer(wx.HORIZONTAL)
                    dateSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.the
                        ),
                        0,
                        wx.ALIGN_CENTER
                    )
                    topSizer.Add(dateSizer, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP,2)
                    self.ctrls.append(wx.NewId())
                    serialCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = self.text.serial_num,
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(serialCtrl, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    if self.plugin.first_day:
                        choices = list(day_name)[0:-1]
                        choices.insert(0, list(day_name)[-1])
                    else:
                        choices = list(day_name)
                    self.ctrls.append(wx.NewId())
                    weekdayCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[3],
                        choices = choices,
                        size = ((-1, 110)),
                    )
                    dateSizer.Add(weekdayCtrl, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    dateSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.in_
                        ),
                        0,
                        wx.ALIGN_CENTER | wx.LEFT, 10
                    )
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_1 = wx.CheckListBox(
                        self,
                        self.ctrls[4],
                        choices = list(month_name)[1:7],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_1, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_2 = wx.CheckListBox(
                        self,
                        self.ctrls[5],
                        choices = list(month_name)[7:],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_2, 0, wx.ALIGN_CENTER | wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    holidCheck_1 = wx.CheckBox(
                        self,
                        self.ctrls[6],
                        self.text.holidCheck_1
                    )
                    dynamicSizer.Add(holidCheck_1, 0, wx.TOP, 2)
                else:
                    serialCtrl = wx.FindWindowById(self.ctrls[2])
                    weekdayCtrl = wx.FindWindowById(self.ctrls[3])
                    monthsCtrl_1 = wx.FindWindowById(self.ctrls[4])
                    monthsCtrl_2 = wx.FindWindowById(self.ctrls[5])
                    holidCheck_1 = wx.FindWindowById(self.ctrls[6])
                val = 0 if not data else data[2]
                for i in range(6):
                    serialCtrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[3]
                if self.plugin.first_day:
                    exp = [6, 0, 1, 2, 3, 4, 5]
                else:
                    exp = [0, 1, 2, 3, 4, 5, 6]
                for i in range(7):
                    weekdayCtrl.Check(i, bool(val & (2 ** exp[i])))
                enable = val & 31 and not val & 96
                holidCheck_1.Enable(enable)
                val = 63 if not data else data[4]
                for i in range(6):
                    monthsCtrl_1.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[5]
                for i in range(6):
                    monthsCtrl_2.Check(i, bool(val & (2 ** i)))
                check = 0 if (not data or not enable) else data[6]
                holidCheck_1.SetValue(check)
            elif type == 4: # Monthly/day ...
                if flag:
                    dateSizer = wx.BoxSizer(wx.HORIZONTAL)
                    topSizer.Add(dateSizer, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP, 2)
                    self.ctrls.append(wx.NewId())
                    q_1_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = [str(i) + '.' for i in range(1, 9)],
                        size = ((40, 125)),
                    )
                    dateSizer.Add(q_1_Ctrl, 0, wx.LEFT, 5)
                    self.ctrls.append(wx.NewId())
                    q_2_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[3],
                        choices = [str(i) + '.' for i in range(9, 17)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_2_Ctrl, 0, wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    q_3_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[4],
                        choices = [str(i) + '.' for i in range(17, 25)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_3_Ctrl, 0, wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    q_4_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[5],
                        choices = [str(i) + '.' for i in range(25, 32)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_4_Ctrl, 0, wx.LEFT, -1)
                    dateSizer.Add((-1, 1), 1, wx.EXPAND)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_1 = wx.CheckListBox(
                        self,
                        self.ctrls[6],
                        choices = list(month_name)[1:7],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_1, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_2 = wx.CheckListBox(
                        self,
                        self.ctrls[7],
                        choices = list(month_name)[7:],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_2, 0, wx.ALIGN_CENTER | wx.LEFT, -1)
                    dateSizer.Add((5, 1), 0)
                else:
                    q_1_Ctrl = wx.FindWindowById(self.ctrls[2])
                    q_2_Ctrl = wx.FindWindowById(self.ctrls[3])
                    q_3_Ctrl = wx.FindWindowById(self.ctrls[4])
                    q_4_Ctrl = wx.FindWindowById(self.ctrls[5])
                    monthsCtrl_1 = wx.FindWindowById(self.ctrls[6])
                    monthsCtrl_2 = wx.FindWindowById(self.ctrls[7])
                val = 0 if not data else data[2]
                for i in range(8):
                    q_1_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[3]
                for i in range(8):
                    q_2_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[4]
                for i in range(8):
                    q_3_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[5]
                for i in range(7):
                    q_4_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[6]
                for i in range(6):
                    monthsCtrl_1.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[7]
                for i in range(6):
                    monthsCtrl_2.Check(i, bool(val & (2 ** i)))
            elif type == 5:
                if flag:
                    self.ctrls.append(wx.NewId())
                    dp = wx.DatePickerCtrl(self, self.ctrls[2], size = (86, -1),
                            style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    topSizer.Add(dp, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP, 2)
                else:
                    dp = wx.FindWindowById(self.ctrls[2])
                if data:
                    if not data[2]:
                        val = wx.DateTime_Now()
                        data[2] = str(dt.now())[:10]
                    wxDttm = wx.DateTime()
                    wxDttm.Set(
                        int(data[2][8:10]),
                        int(data[2][5:7])-1,
                        int(data[2][:4])
                    )
                    dp.SetValue(wxDttm)
            #elif type == 1: # daily
            #    pass
            if flag:
                timeSizer = wx.GridBagSizer(0, 0)
                bottomSizer = wx.StaticBoxSizer(
                    wx.StaticBox(self, -1, self.text.chooseTime6 if type == 6 else self.text.chooseTime),
                    wx.HORIZONTAL
                )
                dynamicSizer.Add(bottomSizer, 0, wx.EXPAND | wx.TOP, 16 if type != 2 else 5)
                bottomSizer.Add(timeSizer, 0, wx.EXPAND)
                stEvLbl = wx.StaticText(self, -1, self.text.start)
                timeSizer.Add(stEvLbl, (0, 0), (1, 2))
                durLabel = wx.StaticText(self, -1, self.text.length)
                timeSizer.Add(durLabel, (0, 3), (1, 2))
                spinBtn = wx.SpinButton(
                    self,
                    -1,
                    wx.DefaultPosition,
                    (-1, 22),
                    wx.SP_VERTICAL
                )
                initTime = wx.DateTime_Now()
                initTime.SetSecond(0)
                initTime.AddTS(wx.TimeSpan.Minute())
                val = data[0] if data and data[0] else initTime
                timeCtrl = eg.TimeCtrl(
                    self,
                    self.ctrls[0],
                    val,
                    fmt24hr = True,
                    spinButton = spinBtn
                )
                timeSizer.Add(timeCtrl, (1, 0), (1, 1))
                timeSizer.Add(spinBtn, (1, 1), (1, 1))
                timeSizer.Add((40, -1), (1, 2), (1, 1))
                spinBtn2 = wx.SpinButton(
                    self,
                    -1,
                    wx.DefaultPosition,
                    (-1, 22),
                    wx.SP_VERTICAL
                )
                val = data[1] if data and data[1] else "00:00"
                lenCtrl = eg.TimeCtrl_Duration(
                    self,
                    self.ctrls[1],
                    val,
                    fmt24hr = True,
                    spinButton = spinBtn2,
                    displaySeconds = False
                )
                timeSizer.Add(lenCtrl, (1, 3), (1, 1))
                timeSizer.Add(spinBtn2, (1, 4), (1, 1))
                bottomSizer.Add((-1,-1), 1, wx.EXPAND)
                testBttn = wx.Button(
                    self,
                    -1 if len(bttns) == 0 else bttns[-1],
                    self.text.testButton
                )
                bottomSizer.Add(testBttn, 0, wx.EXPAND | wx.RIGHT)
            else:
                timeCtrl = wx.FindWindowById(self.ctrls[0])
                val = data[0] if data and data[0] else wx.DateTime_Now()
                timeCtrl.SetValue(val)
                lenCtrl = wx.FindWindowById(self.ctrls[1])
                val = data[1] if data and data[1] else "00:00"
                lenCtrl.SetValue(val)
            if type == 5: #periodically
                if flag:
                    bottomSizer = wx.StaticBoxSizer(
                        wx.StaticBox(self, -1, self.text.choosePeriod),
                        wx.HORIZONTAL
                    )
                    self.ctrls.append(wx.NewId())
                    numCtrl = MySpinIntCtrl(self, -1, value = 1, min = 1)
                    numCtrl.SetNumCtrlId(self.ctrls[3])
                    bottomSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.andThenEvery
                        ),
                        0,
                        wx.ALIGN_CENTER
                    )
                    bottomSizer.Add(numCtrl, 0, wx.LEFT, 4)
                    self.ctrls.append(wx.NewId())
                    unitCtrl = wx.Choice(
                        self,
                        self.ctrls[4],
                        choices = self.text.units
                    )
                    bottomSizer.Add(unitCtrl, 0, wx.LEFT, 8)
                    dynamicSizer.Add(bottomSizer, 0, wx.EXPAND|wx.TOP, 16)
                    dynamicSizer.Layout()
                else:
                    numCtrl = wx.FindWindowById(self.ctrls[3])
                    unitCtrl = wx.FindWindowById(self.ctrls[4])
                if data:
                    numCtrl.SetValue(str(data[3]))
                    unitCtrl.SetSelection(data[4])
            elif flag:
                dynamicSizer.Layout()
            if type == 6:
                stEvLbl.Show(False)
                timeCtrl.Show(False)
                spinBtn.Show(False)
            return dynamicSizer.GetMinSize()


        def Diff():
            applyBttn = wx.FindWindowById(bttns[5])
            flg = self.tmpData != self.plugin.data
            applyBttn.Enable(flg)


        def onCheckListBox(evt):
            id = evt.GetId()
            sel = evt.GetSelection()
            box = self.FindWindowById(id)
            ix = self.ctrls.index(id)
            type = self.tmpData[self.lastRow][2]
            cond = (type == 2 and ix == 2) or (type == 3 and ix == 3)
            if cond and self.plugin.first_day:
                exp = (6, 0, 1, 2, 3, 4, 5)[sel]
            else:
                exp = sel
            if box.IsChecked(sel):
                self.tmpData[self.lastRow][3][ix] |= 2 ** exp
            else:
                self.tmpData[self.lastRow][3][ix] &= 255 - 2 ** exp
            if cond:
                holidCheck_1 = wx.FindWindowById(self.ctrls[-1])
                val = self.tmpData[self.lastRow][3][ix]
                flg = val & 31 and not val & 96
                holidCheck_1.Enable(flg)
                if not flg:
                    holidCheck_1.SetValue(0)
                    self.tmpData[self.lastRow][3][-1] = 0
                if type == 2:
                    holidCheck_2 = wx.FindWindowById(self.ctrls[3])
                    val = self.tmpData[self.lastRow][3][2]
                    flg = val & 96 and not val & 31
                    holidCheck_2.Enable(flg)
                    if not flg:
                        holidCheck_2.SetValue(0)
                        self.tmpData[self.lastRow][3][3] = 0
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def OnTimeChange(evt):
            ix = self.ctrls.index(evt.GetId())
            self.tmpData[self.lastRow][3][ix] = evt.GetValue()
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def onPeriodUnit(evt):
            if len(self.ctrls) == 5 and evt.GetId() == self.ctrls[4]:
                self.tmpData[self.lastRow][3][4] = evt.GetSelection()
                next = self.plugin.NextRun(
                    self.tmpData[self.lastRow][2],
                    self.tmpData[self.lastRow][3]
                )
                grid.SetStringItem(self.lastRow, 3, next)
            else:
                evt.Skip()
            Diff()


        def onDatePicker(evt):
            val = str(dt.fromtimestamp(evt.GetDate().GetTicks()))[:10]
            self.tmpData[self.lastRow][3][2] = val
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def onCheckBox(evt):
            val = evt.IsChecked()
            ix = self.ctrls.index(evt.GetId())
            if self.tmpData[self.lastRow][2] == 2 and ix == 3:
                self.tmpData[self.lastRow][3][3] = int(val)
            else:
                self.tmpData[self.lastRow][3][-1] = int(val)
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def OnUpdateDialog(evt):
            if self.lastRow == evt.GetId():
                OpenSchedule()


        def OnSelectCell(evt):
            self.lastRow = evt.m_itemIndex
            OpenSchedule()
            Diff()
            evt.Skip() # necessary !!!


        def enableBttns(value):
            for i in (1, 2):
                bttn = self.FindWindowById(bttns[i])
                bttn.Enable(value)
            Diff()


        def ShowMessageBox(mess):
            MessageBox(
                self,
                mess,
                self.text.boxTitle,
                wx.ICON_EXCLAMATION,
                plugin = self.plugin
                )


        def FindNewTitle(title):
            tmpLst = []
            for item in self.tmpData:
                if item[1].startswith(title + " ("):
                    tmpLst.append(item[1][2 + len(title):])
            if len(tmpLst) == 0:
                return "%s (1)" % title
            tmpLst2 = []
            for item in tmpLst:
                if item[-1] == ")":
                    try:
                        tmpLst2.append(int(item[:-1]))
                    except:
                        pass
            if len(tmpLst2) == 0:
                return "%s (1)" % title
            else:
                return "%s (%i)" % (title, 1 + max(tmpLst2))


        def testValidity(data, test = False):
            mssgs = []
            tempDict = dict([(item[1].strip(), item[2]) for item in data])
            if "" in tempDict.iterkeys():
                mssgs.append(self.text.boxTexts[0])
            if not test and len(tempDict) < len(data):
                mssgs.append(self.text.boxTexts[1])
            if -1 in tempDict.itervalues():
                mssgs.append(self.text.boxTexts[4])
            for item in data:
                val = item[7]
                if (val & 6) == 6: # = Do nothing
                    if not val & 24:
                        if not self.text.boxTexts[3] in mssgs:
                            mssgs.append(self.text.boxTexts[3])
                else: # Not "Do nothing"
                    if not item[5]:
                        if not self.text.boxTexts[2] in mssgs:
                            mssgs.append(self.text.boxTexts[2])
                if item[2] == 5 and item[3][4] < 2:
                    period = item[3][3] * (3600, 86400)[item[3][4]]
                    span = 60 * int(item[3][1][3:]) + 3600 * int(item[3][1][:2])
                    if period <= span:
                        if self.text.boxTexts[5] not in mssgs:
                            mssgs.append(self.text.boxTexts[5])
            flag = len(mssgs) > 0
            if flag:
                ShowMessageBox("\n".join(mssgs))
            return flag


        def addSchedule(evt = None):
            empty = [1, "", -1, [], " ", "", "", 5]
            self.lastRow = len(self.tmpData)
            self.tmpData.append(empty)
            Tidy()
            grid.AppendRow()
            grid.SelRow(self.lastRow)
            if not self.lastRow:
                enableBttns(True)
                EnableCtrls(True)
            Diff()


        def duplSchedule(evt = None):
            lngth = len(self.tmpData)
            item = cpy(self.tmpData[self.lastRow])
            nxt = grid.GetItem(self.lastRow, 3).GetText()
            item[4] = ""
            self.lastRow = lngth
            self.tmpData.append(item)
            newTitle = FindNewTitle(self.tmpData[lngth][1])
            self.tmpData[lngth][1] = newTitle
            grid.AppendRow()
            grid.SelRow(lngth)
            grid.SetStringItem(lngth, 1, newTitle)
            grid.SetStringItem(lngth, 3, nxt)
            OpenSchedule()
            Diff()


        def delSchedule(evt = None):
            self.tmpData.pop(self.lastRow)
            grid.DeleteItem(self.lastRow)
            if len(self.tmpData) > 0:
                if self.lastRow == len(self.tmpData):
                    self.lastRow -= 1
                OpenSchedule()
                grid.SelRow(self.lastRow)
            else:
                self.lastRow = -1
                Tidy()
                EnableCtrls(False)
                enableBttns(False)
            Diff()


        def Move(direction):
            lst = cpy(self.tmpData)
            index = self.lastRow
            max = len(lst)-1
            #Last to first position, other down
            if index == max and direction == 1:
                self.tmpData[1:] = lst[:-1]
                self.tmpData[0] = lst[max]
                index2 = 0
            #First to last position, other up
            elif index == 0 and direction == -1:
                self.tmpData[:-1] = lst[1:]
                self.tmpData[max] = lst[0]
                index2 = max
            else:
                index2 = index + direction
                self.tmpData[index] = lst[index2]
                self.tmpData[index2] = lst[index]
            del lst
            return index2


        def moveUp(evt = None):
            newSel = Move(-1)
            fillGrid(False)
            self.grid.SelRow(newSel)
            Diff()


        def moveDown(evt = None):
            newSel = Move(1)
            fillGrid(False)
            self.grid.SelRow(newSel)
            Diff()


        def onButton(evt):
            id = evt.GetId()
            if id == bttns[0]:   # Add new
                addSchedule()
            elif id == bttns[1]: # Duplicate
                duplSchedule()
            elif id == bttns[2]: # Delete
                delSchedule()
            elif id == bttns[3]: # OK
                if testValidity(self.tmpData):
                    evt.Skip()
                    return
                self.plugin.data = cpy(self.tmpData)
                self.tmpData = []
                self.plugin.dataToXml()
                self.plugin.UpdateEGscheduler()
                self.Close()
            elif id == bttns[4]: # Cancel
                self.tmpData = []
                self.Close()
            elif id == bttns[5]: # Apply
                applyBttn = wx.FindWindowById(bttns[5])
                applyBttn.Enable(False)
                if testValidity(self.tmpData):
                    evt.Skip()
                    return
                self.plugin.data = cpy(self.tmpData)
                self.plugin.dataToXml()
                self.plugin.UpdateEGscheduler()
            evt.Skip()


        def EnableCtrls(value):
            typeChoice.Enable(value)
            schedulerName.Enable(value)
            name_label.Enable(value)
            type_label.Enable(value)
            favorite_label.Enable(value)
            workModeLbl.Enable(value)
            triggEvtLbl.Enable(value)
            windOpenLbl.Enable(value)
            source_label.Enable(value)
            filename_label.Enable(value)
            favChoice.Enable(value)
            sourceCtrl.Enable(value)
            recordCtrl.Enable(value)
            workModeCtrl.Enable(value)
            triggEvtCtrl.Enable(value)
            windOpenCtrl.Enable(value)
            if not value:
                workModeCtrl.SetSelection(-1)
                triggEvtCtrl.SetSelection(-1)
                windOpenCtrl.SetSelection(-1)


        def OpenSchedule():
            schedulerName.ChangeValue(self.tmpData[self.lastRow][1])
            type = self.tmpData[self.lastRow][2]
            fillDynamicSizer(
                type,
                self.tmpData[self.lastRow][3],
                typeChoice.GetSelection()
            )
            typeChoice.SetSelection(type)
            modes = self.tmpData[self.lastRow][7]
            rsMode = (modes>>1)&3
            workModeCtrl.SetSelection(rsMode)
            recordCtrl.GetTextCtrl().ChangeValue(self.tmpData[self.lastRow][6])
            sourceCtrl.SetValue(self.tmpData[self.lastRow][5])
            if rsMode == 3:
                windOpenCtrl.SetSelection(-1)
                windOpenCtrl.Enable(False)
                windOpenLbl.Enable(False)
            else:
                windOpenCtrl.SetSelection(modes&1)
                windOpenCtrl.Enable(True)
                windOpenLbl.Enable(True)
            triggEvtCtrl.SetSelection((modes>>3)&3)


        def Tidy():
            favChoice.SetSelection(-1)
            typeChoice.SetSelection(-1)
            windOpenCtrl.SetSelection(1)
            workModeCtrl.SetSelection(2)
            triggEvtCtrl.SetSelection(0)
            sourceCtrl.ChangeValue("")
            recordCtrl.GetTextCtrl().ChangeValue("")
            schedulerName.ChangeValue("")
            fillDynamicSizer(-1)
            filename_label.Enable(True)
            recordCtrl.Enable(True)


        def onCheckListCtrl(evt):
            index, flag = evt.GetValue()
            if self.tmpData[index][0] != int(flag):
                self.tmpData[index][0] = int(flag)
                Diff()


        def onSchedulerTitle(evt):
            txt = evt.GetString()
            grid.SetStringItem(self.lastRow, 1, txt)
            self.tmpData[self.lastRow][1] = txt
            Diff()


        def onPeriodNumber(evt):
            if len(self.ctrls) == 5 and evt.GetId() == self.ctrls[3]:
                self.tmpData[self.lastRow][3][3] = int(evt.GetString())
                next = self.plugin.NextRun(
                    self.tmpData[self.lastRow][2],
                    self.tmpData[self.lastRow][3]
                )
                grid.SetStringItem(self.lastRow, 3, next)
                Diff()
            else:
                evt.Skip()


        def onTestButton(evt):
            data = self.tmpData[self.lastRow]
            if testValidity([data,], True):
                return
            ticks = mktime(localtime())
            next, cmdline = self.plugin.Execute(data, True)
            next = next[:19] if next else self.plugin.text.none
            self.plugin.updateLogFile(self.text.testRun % (data[1], next))
            if cmdline:
                self.plugin.updateLogFile(self.plugin.text.cmdLine % cmdline.decode(FSE))


        def OnRightClick(evt):
            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewId()
                self.popupID2 = wx.NewId()
                self.popupID3 = wx.NewId()
                self.popupID4 = wx.NewId()
                self.popupID5 = wx.NewId()
                self.popupID6 = wx.NewId()
                self.popupID7 = wx.NewId()
                self.Bind(wx.EVT_MENU, addSchedule, id=self.popupID1)
                self.Bind(wx.EVT_MENU, duplSchedule, id=self.popupID2)
                self.Bind(wx.EVT_MENU, delSchedule, id=self.popupID3)
                self.Bind(wx.EVT_MENU, self.EnableAll, id=self.popupID4)
                self.Bind(wx.EVT_MENU, self.DisableAll, id=self.popupID5)
                self.Bind(wx.EVT_MENU, moveUp, id=self.popupID6)
                self.Bind(wx.EVT_MENU, moveDown, id=self.popupID7)
            # make a menu
            menu = wx.Menu()
            menu.Append(self.popupID1, self.text.popup[0])
            menu.Append(self.popupID2, self.text.popup[1])
            menu.Append(self.popupID3, self.text.popup[2])
            menu.AppendSeparator()
            menu.Append(self.popupID4, self.text.popup[3])
            menu.Append(self.popupID5, self.text.popup[4])
            menu.AppendSeparator()
            menu.Append(self.popupID6, self.text.popup[5])
            menu.Append(self.popupID7, self.text.popup[6])
            self.PopupMenu(menu)
            menu.Destroy()
            evt.Skip()


        def fillGrid(flag):
            grid.DeleteAllItems()
            rows = len(self.tmpData)
            if rows > 0:
                for row in range(rows):
                    grid.InsertStringItem(row, "")
                    if self.tmpData[row][0]:
                        grid.CheckItem(row)
                    grid.SetStringItem(row, 1, self.tmpData[row][1])
                    grid.SetStringItem(row, 2, self.tmpData[row][4])
                    next = self.plugin.NextRun(self.tmpData[row][2], self.tmpData[row][3])
                    grid.SetStringItem(row, 3, next)
                if flag:
                    self.lastRow = 0
                    grid.SelRow(0)
                    OpenSchedule()
                    enableBttns(True)
            else:
                EnableCtrls(False)
                grid.DeleteItem(0)

        dynamicSizer = wx.BoxSizer(wx.VERTICAL)
        wDynamic = fillDynamicSizer(3)
        fillDynamicSizer(-1)
        grid = CheckListCtrl(self, text, wDynamic[0])
        self.grid = grid

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.ALL, 5)
        favorite_label = wx.StaticText(self, -1, self.text.favorite)
        workModeLbl = wx.StaticText(self, -1, self.text.workModeLabel)
        workModeCtrl = wx.Choice(self, -1, choices = self.text.workModes)
        triggEvtLbl = wx.StaticText(self, -1, self.text.triggEvtLabel)
        triggEvtCtrl = wx.Choice(self, -1, choices = self.text.triggEvtChoices)
        windOpenLbl = wx.StaticText(self, -1, self.text.windOpenLabel)
        windOpenCtrl = wx.Choice(self, -1, choices = self.text.windOpenChoices)
        source_label = wx.StaticText(self, -1, self.text.source)
        self.favorites = self.plugin.RefreshVariables()
        favChoice = wx.Choice(self, -1, choices = [item[1] for item in self.favorites])
        hgh =  48 + favChoice.GetSize()[1]
        sourceCtrl = wx.TextCtrl(self,-1,"")
        filename_label = wx.StaticText(self, -1, self.text.filename)
        schedulerName = wx.TextCtrl(self, -1, "")
        typeChoice = wx.Choice(self, -1, choices = self.text.sched_type)
        xmltoparse = u'%s\\RadioSure.xml' % self.plugin.xmlpath
        xmltoparse = xmltoparse.encode(FSE) if isinstance(xmltoparse, unicode) else xmltoparse
        xmldoc = miniDom.parse(xmltoparse)
        recordings = xmldoc.getElementsByTagName('Recordings')
        if not recordings:
            folder = u'%s\\RadioSure Recordings' % self.plugin.xmlpath
        else:
            folder = recordings[0].getElementsByTagName('Folder')[0].firstChild.data
        recordCtrl = MyFileBrowseButton(
            self,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse,
            startDirectory = folder
        )
        self.grid.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, OnRightClick)

        def onSource(evt):
            src = evt.GetString()
            srcs = [item[0] for item in self.favorites]
            if src in srcs:
                ix = srcs.index(src)
            else:
                ix = -1
            favChoice.SetSelection(ix)
            self.tmpData[self.lastRow][5] = src
            Diff()
            evt.Skip()
        sourceCtrl.Bind(wx.EVT_TEXT, onSource)


        def onFavChoice(evt):
            sel = evt.GetSelection()
            txt = self.favorites[sel][0]
            sourceCtrl.ChangeValue(txt)
            self.tmpData[self.lastRow][5] = txt
            Diff()
            evt.Skip()
        favChoice.Bind(wx.EVT_CHOICE, onFavChoice)


        def onRecordCtrl(evt):
            txt = evt.GetString()
            self.tmpData[self.lastRow][6] = txt
            Diff()
            evt.Skip()
        recordCtrl.GetTextCtrl().Bind(wx.EVT_TEXT, onRecordCtrl)


        def onTypeChoice(evt):
            type = evt.GetSelection()
            if self.tmpData[self.lastRow][2] != type:
                empty_data = [
                    ["", "", 0, 0],
                    ["", ""],
                    ["", "", 127, 0, 0],
                    ["", "", 0, 0, 63, 63, 0],
                    ["", "", 0, 0, 0, 0, 63, 63],
                    ["", "", 0, 1, 0],
                ]
                self.tmpData[self.lastRow][2] = type
                data = empty_data[self.tmpData[self.lastRow][2]]
                self.tmpData[self.lastRow][3] = data
                fillDynamicSizer(type, data)
            Diff()


        def onWorkMode(evt):
            sel = evt.GetSelection()
            if sel == 3:
                windOpenCtrl.SetSelection(-1)
                windOpenCtrl.Enable(False)
                windOpenLbl.Enable(False)
                if triggEvtCtrl.GetSelection() == 0:
                    ShowMessageBox(self.text.boxTexts[3])
            else:
                if windOpenCtrl.GetSelection() == -1:
                    windOpenCtrl.SetSelection(1)
                    windOpenCtrl.Enable(True)
                    windOpenLbl.Enable(True)
            val = self.tmpData[self.lastRow][7]
            val &= (255-6)
            val |= (sel<<1)
            self.tmpData[self.lastRow][7] = val
            Diff()
        workModeCtrl.Bind(wx.EVT_CHOICE, onWorkMode)


        def onWindOpen(evt):
            sel = evt.GetSelection()
            val = self.tmpData[self.lastRow][7]
            val &= (255-1)
            val |= sel
            self.tmpData[self.lastRow][7] = val
            Diff()
        windOpenCtrl.Bind(wx.EVT_CHOICE, onWindOpen)


        def onTriggEvtCtrl(evt):
            sel = evt.GetSelection()
            workMode = workModeCtrl.GetSelection()
            if sel == 0 and workMode == 3:
                ShowMessageBox(self.text.boxTexts[3])
            val = self.tmpData[self.lastRow][7]
            val &= (255-24)
            val |= (sel<<3)
            self.tmpData[self.lastRow][7] = val
            Diff()
        triggEvtCtrl.Bind(wx.EVT_CHOICE, onTriggEvtCtrl)

        bttnSizer = wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer.Add((5, -1))
        i = 0
        for bttn in self.text.buttons:
            id = wx.NewId()
            bttns.append(id)
            b = wx.Button(self, id, bttn)
            bttnSizer.Add(b,1)
            if i in (1, 2, 5):
                b.Enable(False)
            if i == 3:
                b.SetDefault()
            if i == 5:
                self.applyBttn = b
            b.Bind(wx.EVT_BUTTON, onButton, id = id)
            bttnSizer.Add((5, -1))
            i += 1
        sizer.Add(bttnSizer,0,wx.EXPAND)
        id = wx.NewId() #testBttn
        bttns.append(id)
        self.Bind(wx.EVT_BUTTON, onTestButton, id = id)
        wx.EVT_CHECKLISTBOX(self, -1, onCheckListBox)
        EVT_TIMEUPDATE(self, -1, OnTimeChange)
        wx.EVT_TEXT(self, -1, onPeriodNumber)
        wx.EVT_CHOICE(self, -1, onPeriodUnit)
        wx.EVT_DATE_CHANGED(self, -1, onDatePicker)
        wx.EVT_CHECKBOX(self, -1, onCheckBox)
        self.Bind(eg.EVT_VALUE_CHANGED, OnUpdateDialog)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, OnSelectCell)
        typeChoice.Bind(wx.EVT_CHOICE, onTypeChoice)
        schedulerName.Bind(wx.EVT_TEXT, onSchedulerTitle)
        self.grid.Bind(eg.EVT_VALUE_CHANGED, onCheckListCtrl)
        nameSizer = wx.FlexGridSizer(2, 0, 0, 20)
        nameSizer.AddGrowableCol(0,1)
        name_label = wx.StaticText(self, -1, self.text.header[1] + ":")
        nameSizer.Add(name_label)
        type_label = wx.StaticText(self, -1, self.text.type_label)
        nameSizer.Add(type_label)
        nameSizer.Add(schedulerName, 0, wx.EXPAND)
        nameSizer.Add(typeChoice)
        typeSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, -1, ""),
            wx.VERTICAL
        )
        #dynamicSizer.SetMinSize((-1, 226))
        dynamicSizer.SetMinSize((-1, wDynamic[1]))
        typeSizer.Add(nameSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        typeSizer.Add(dynamicSizer, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        sizer.Add(typeSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer.Add(source_label, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(sourceCtrl,0,wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        sizer.Add((1,4))
        sizer.Add(favorite_label, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(favChoice,0,wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        sizer.Add((1,4))
        choicesSizer = wx.FlexGridSizer(2,3,0,10)
        choicesSizer.Add(windOpenLbl,0)
        choicesSizer.Add(workModeLbl,0)
        choicesSizer.Add(triggEvtLbl,0)
        choicesSizer.Add(windOpenCtrl,0,wx.EXPAND)
        choicesSizer.Add(workModeCtrl,0,wx.EXPAND)
        choicesSizer.Add(triggEvtCtrl,0,wx.EXPAND)
        sizer.Add(choicesSizer,0,wx.ALL, 5)
        sizer.Add(filename_label, 0, wx.LEFT, 5)
        sizer.Add(recordCtrl,0,wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        fillGrid(True)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetSizer(sizer)
        sizer.Layout()
        hgh += grid.GetSize()[1]
        hgh += bttnSizer.GetSize()[1]
        hgh += typeSizer.GetSize()[1]
        hgh += source_label.GetSize()[1]
        hgh += sourceCtrl.GetSize()[1]
        hgh += favorite_label.GetSize()[1]
        hgh += choicesSizer.GetSize()[1]
        hgh += filename_label.GetSize()[1]
        hgh += recordCtrl.GetSize()[1]
        self.SetClientSize(wx.Size(wDynamic[0] + 10, hgh))
        if ConfigData.pos:
            self.SetPosition(ConfigData.pos)
        else:
            self.Center()
        self.Show(True)


    def EnableAll(self, flag):
        if isinstance(flag, wx.CommandEvent):
            schedule = self.tmpData[self.lastRow][1]
            flag = 1
        for ix in range(len(self.tmpData)):
            self.tmpData[ix][0] = flag
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                if flag:
                    self.grid.CheckItem(ix)
                elif self.grid.IsChecked(ix):
                    self.grid.ToggleItem(ix)
        self.applyBttn.Enable(self.tmpData != self.plugin.data)


    def DisableAll(self, evt):
        self.EnableAll(0)


    def EnableSchedule(self, schedule, flag):
        tmpList = [item[1] for item in self.tmpData]
        if schedule in tmpList:
            ix = tmpList.index(schedule)
            self.tmpData[ix][0] = flag
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                if flag:
                    self.grid.CheckItem(ix)
                elif self.grid.IsChecked(ix):
                    self.grid.ToggleItem(ix)


    def DeleteSchedule(self, schedule):
        tmpList = [item[1] for item in self.tmpData]
        if schedule in tmpList:
            ix = tmpList.index(schedule)
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                self.grid.DeleteItem(ix)
                self.grid.Refresh()
            self.tmpData.pop(ix)


    def AddSchedule(self, schedule):
        tmpList = [item[1] for item in self.tmpData]
        if schedule[1] in tmpList:
            ix = tmpList.index(schedule[1])
            self.tmpData[ix] = schedule
            if not self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                return
        else:
            ix = len(self.tmpData)
            self.tmpData.append(schedule)
            self.grid.InsertStringItem(ix, "")
        if schedule[0]:
            self.grid.CheckItem(ix)
        elif self.grid.IsChecked(ix):
            self.grid.ToggleItem(ix)
        self.grid.SetStringItem(ix, 1, schedule[1])
        next = self.plugin.NextRun(schedule[2], schedule[3])
        self.grid.SetStringItem(ix, 3, next)
        if self.lastRow == ix:
            evt = eg.ValueChangedEvent(ix)
            wx.PostEvent(self, evt)


    def RefreshGrid(self, ix, last, next):
        if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
            self.grid.SetStringItem(ix, 2, last)
            self.grid.SetStringItem(ix, 3, next)


    def onClose(self, evt):
        hwnd = self.GetHandle()
        wp = GetWindowPlacement(hwnd)[4]
        #Note: GetPosition() return (-32000, -32000), if window is minimized !!!
        cdr = wx.GetClientDisplayRect()
        pos = (wp[0] + cdr[0], wp[1] + cdr[1])
        if pos != ConfigData.pos:
            ConfigData.pos = pos
            #if not eg.document.IsDirty():
            #    wx.CallAfter(eg.Notify, "DocumentChange", True)
        self.plugin.dialog = None
        wx.CallAfter(self.Show, False)
        wx.CallAfter(self.Destroy)
        evt.Skip()
#===============================================================================

def HandleRS():

    FindRS = eg.WindowMatcher(
                u'RadioSure.exe',
                None,
                u'#32770',
                None,
                None,
                None,
                True,
                0.0,
                0
            )
    hwnds = FindRS()
    res = []
    for hwnd in hwnds:
        try: #maybe already closed !!!
            curhw = GetWindow(hwnd, GW_CHILD)
            while curhw > 0:
                if GetDlgCtrlID(curhw) == 1016 and GetClassName(curhw) == 'SysListView32':
                    res.append(hwnd)
                    break
                curhw = GetWindow(curhw, GW_HWNDNEXT)
        except:
            pass
    return res
#===============================================================================

class ObservationThread:

    def __init__(self, period, evtName, evtName2, plugin):
        self.alive = False
        self.period = period
        self.evtName = evtName
        self.evtName2 = evtName2
        self.task = None
        self.oldData = ""
        self.oldData2 = ""
        self.plugin = plugin


    def RS_ObservationThread(self):
        hwnd = HandleRS()
        if hwnd:
            if self.evtName:
                data = GetWindowText(hwnd[0]).decode(eg.systemEncoding)
                if data != self.oldData and data != "Radio? Sure!":
                    self.oldData = data
                    eg.TriggerEvent(self.evtName, payload = data, prefix = "RadioSure")
            if self.evtName2:
                data = self.plugin.GetLastPlayed()
                if data and data[0] != self.oldData2:
                    self.oldData2 = data[0]
                    eg.TriggerEvent(self.evtName2, payload = data, prefix = "RadioSure")
        if self.alive:
            self.task = eg.scheduler.AddTask(self.period, self.RS_ObservationThread)


    def start(self):
        self.alive = True
        self.RS_ObservationThread()


    def isAlive(self):
        return self.alive


    def AbortObservation(self):
        eg.scheduler.CancelTask(self.task)
        self.alive = False
        self.task = None

#===============================================================================

def GetCtrlByID(id):

    res = None
    hwnds = HandleRS()
    if hwnds:
        try:
            res = GetDlgItem(hwnds[0], id)
        except:
            pass
    return res
#===============================================================================

def getPathFromReg():

    try:
        rs_reg = OpenKey(
            HKEY_CURRENT_USER,
            "Software\\RadioSure"
        )
        res = unicode(EnumValue(rs_reg,0)[1])
        CloseKey(rs_reg)
    except:
        res = None
    return res
#===============================================================================

def FindMonthDay(year, month, weekday, index):
    """weekday = what day of the week looking for (numbered 0-6, 0 = monday)
    index = how many occurrence of looking for (numbered 0-4 and 5 for the last day)
    Returns the day of the month (date) or 0 (if no such date exists)"""
    first_wd, length = monthrange(year, month)
    day = 1 + weekday - first_wd
    if day < 1:
        day += 7
    if index == 5:
        index = 4 if day <= length % 7 else 3
    day += 7 * index
    if day > length:
        day = 0
    return day
#===============================================================================

def getStations(nodelist):
    tmp = []
    for item in nodelist.childNodes:
        if item.nodeName[:5] == "Item-":
            title = item.getElementsByTagName('Title')[0].firstChild
            if title:
                title = title.data
            source = item.getElementsByTagName('Source')[0].firstChild
            if source:
                source = source.data
            genre  = item.getElementsByTagName('Genre')[0].firstChild
            if genre:
                genre = genre.data
            language = item.getElementsByTagName('Language')[0].firstChild
            if language:
                language = language.data
            country = item.getElementsByTagName('Country')[0].firstChild
            if country:
                country = country.data
            tmp.append([source, title, genre, language, country])
    return tmp
#===============================================================================

class MenuGrid(gridlib.Grid):

    def __init__(self, parent, lngth):
        gridlib.Grid.__init__(self, parent)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetDefaultRowSize(16)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.EnableEditing(False)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.EnableGridLines(False)
        self.SetColMinimalAcceptableWidth(8)
        self.CreateGrid(lngth, 3)
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(1,attr)
        self.SetSelectionMode(gridlib.Grid.wxGridSelectRows)
        self.Bind(gridlib.EVT_GRID_CMD_SELECT_CELL, self.onGridSelectCell, self)


    def SetBackgroundColour(self, colour):
        self.SetDefaultCellBackgroundColour(colour)


    def SetForegroundColour(self, colour):
        self.SetDefaultCellTextColour(colour)


    def SetFont(self, font):
        self.SetDefaultCellFont(font)


    def GetSelection(self):
        return self.GetSelectedRows()[0]


    def Set(self, choices):
        oldLen = self.GetNumberRows()
        newLen = len(choices)
        h = self.GetDefaultRowSize()
        if oldLen > newLen:
            self.DeleteRows(0, oldLen-newLen, False)
        elif oldLen < newLen:
            self.AppendRows(newLen-oldLen, False)
        for i in range(len(choices)):
            chr = u"\u25a0" if choices[i][2] else ""
            self.SetCellValue(i,0,chr)
            self.SetCellValue(i,1," "+choices[i][0])
            chr = u"\u25ba" if choices[i][3] == -1 else ""
            self.SetCellValue(i,2, chr)
            self.SetRowSize(i,h)


    def onGridSelectCell(self, event):
        row = event.GetRow()
        self.SelectRow(row)
        if not self.IsVisible(row,1):
            self.MakeCellVisible(row,1)
        event.Skip()


    def MoveCursor(self, step):
        max = self.GetNumberRows()
        sel = self.GetSelectedRows()[0]
        new = sel + step
        if new < 0:
            new += max
        elif new > max-1:
            new -= max
        self.SetGridCursor(new, 1)
        self.SelectRow(new)
#===============================================================================

class MyTextDropTarget(EventDropTarget):

    def __init__(self, object):
        EventDropTarget.__init__(self, object)
        self.object = object


    def OnDragOver(self, x, y, dragResult):
        return wx.DragMove


    def OnData(self, dummyX, dummyY, dragResult):
        if self.GetData() and self.customData.GetDataSize() > 0:
            txt = self.customData.GetData()
            ix, evtList = self.object.GetEvtList()
            flag = True
            for lst in evtList:
                if txt in lst:
                    flag = False
                    break
            if flag:
                self.object.InsertImageStringItem(len(evtList[ix]), txt, 0)
                self.object.UpdateEvtList(ix, txt)
            else:
                PlaySound('SystemExclamation', SND_ASYNC)


    def OnLeave(self):
        pass
#===============================================================================

class EventListCtrl(wx.ListCtrl):

    def __init__(self, parent, id, evtList, ix, plugin):
        width = 205
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
            wx.LC_NO_HEADER | wx.LC_SINGLE_SEL, size = (width, -1))
        self.parent = parent
        self.id = id
        self.evtList = evtList
        self.ix = ix
        self.plugin = plugin
        self.sel = -1
        self.il = wx.ImageList(16, 16)
        self.il.Add(wx.BitmapFromImage(wx.Image(join(IMAGES_DIR, "event.png"), wx.BITMAP_TYPE_PNG)))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')
        self.SetColumnWidth(0, width - 5 - SYS_VSCROLL_X)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_SET_FOCUS, self.OnChange)
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self.OnChange)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnChange)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.SetToolTipString(self.plugin.text.toolTip)


    def OnSelect(self, event):
        self.sel = event.GetIndex()
        evt = eg.ValueChangedEvent(self.id, value = self)
        wx.PostEvent(self, evt)
        event.Skip()


    def OnChange(self, event):
        evt = eg.ValueChangedEvent(self.id, value = self)
        wx.PostEvent(self, evt)
        event.Skip()


    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnDeleteButton, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnDeleteAllButton, id=self.popupID2)
        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, self.plugin.text.popup[0])
        menu.Append(self.popupID2, self.plugin.text.popup[1])
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()


    def OnDeleteButton(self, event=None):
        self.DeleteItem(self.sel)
        self.evtList[self.ix].pop(self.sel)
        evt = eg.ValueChangedEvent(self.id, value = self)
        wx.PostEvent(self, evt)
        if event:
            event.Skip()


    def OnDeleteAllButton(self, event=None):
        self.DeleteAllItems()
        evt = eg.ValueChangedEvent(self.id, value = self)
        wx.PostEvent(self, evt)
        self.evtList[self.ix] = []
        if event:
            event.Skip()


    def GetEvtList(self):
        return self.ix, self.evtList


    def UpdateEvtList(self, ix, txt):
        self.evtList[ix].append(txt)


    def SetItems(self, evtList):
        for i in range(len(evtList)):
            self.InsertImageStringItem(i, evtList[i], 0)
#===============================================================================

class MenuEventsDialog(wx.MiniFrame):

    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="Menu events dialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.evtList = cpy(self.panel.evtList)
        self.SetBackgroundColour(wx.NullColour)
        self.ctrl = None
        self.sel = -1


    def ShowMenuEventsDialog(self, title, labels):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.SetMinSize((450, 308))
        topSizer=wx.GridBagSizer(2, 20)
        textLbl_0=wx.StaticText(self, -1, labels[0])
        id = wx.NewId()
        eventsCtrl_0 = EventListCtrl(self, id, self.evtList, 0, self.plugin)
        eventsCtrl_0.SetItems(self.evtList[0])
        dt0 = MyTextDropTarget(eventsCtrl_0)
        eventsCtrl_0.SetDropTarget(dt0)
        textLbl_1=wx.StaticText(self, -1, labels[1])
        id = wx.NewId()
        eventsCtrl_1 = EventListCtrl(self, id, self.evtList, 1, self.plugin)
        eventsCtrl_1.SetItems(self.evtList[1])
        dt1 = MyTextDropTarget(eventsCtrl_1)
        eventsCtrl_1.SetDropTarget(dt1)
        textLbl_2=wx.StaticText(self, -1, labels[2])
        id = wx.NewId()
        eventsCtrl_2 = EventListCtrl(self, id, self.evtList, 2, self.plugin)
        eventsCtrl_2.SetItems(self.evtList[2])
        dt2 = MyTextDropTarget(eventsCtrl_2)
        eventsCtrl_2.SetDropTarget(dt2)
        textLbl_3=wx.StaticText(self, -1, labels[3])
        id = wx.NewId()
        eventsCtrl_3 = EventListCtrl(self, id, self.evtList, 3, self.plugin)
        eventsCtrl_3.SetItems(self.evtList[3])
        dt3 = MyTextDropTarget(eventsCtrl_3)
        eventsCtrl_3.SetDropTarget(dt3)
        textLbl_4=wx.StaticText(self, -1, labels[4])
        id = wx.NewId()
        eventsCtrl_4 = EventListCtrl(self, id, self.evtList, 4, self.plugin)
        eventsCtrl_4.SetItems(self.evtList[4])
        dt4 = MyTextDropTarget(eventsCtrl_4)
        eventsCtrl_4.SetDropTarget(dt4)
        deleteSizer = wx.BoxSizer(wx.VERTICAL)
        delOneBtn = wx.Button(self, -1, self.plugin.text.popup[0])
        delBoxBtn = wx.Button(self, -1, self.plugin.text.popup[1])
        clearBtn  = wx.Button(self, -1, self.plugin.text.clear)
        deleteSizer.Add(delOneBtn, 1, wx.EXPAND)
        deleteSizer.Add(delBoxBtn, 1, wx.EXPAND|wx.TOP,5)
        deleteSizer.Add(clearBtn, 1, wx.EXPAND|wx.TOP,5)

        topSizer.Add(textLbl_0, (0,0))
        topSizer.Add(eventsCtrl_0, (1,0), flag = wx.EXPAND)
        topSizer.Add(textLbl_1, (0,1))
        topSizer.Add(eventsCtrl_1, (1,1), flag = wx.EXPAND)
        topSizer.Add(textLbl_2, (2,0),flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_2, (3,0), flag = wx.EXPAND)
        topSizer.Add(textLbl_3, (2,1), flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_3, (3,1), flag = wx.EXPAND)
        topSizer.Add(textLbl_4, (4,0), flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_4, (5,0), flag = wx.EXPAND)
        topSizer.Add(deleteSizer, (5,1), flag = wx.EXPAND)

        line = wx.StaticLine(self, -1, size=(20,-1),pos = (200,0), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(self.plugin.text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(self.plugin.text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(topSizer,0,wx.ALL,10)
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,6))
        self.SetSizer(sizer)
        sizer.Fit(self)


        def onFocus(evt):
            ctrl = evt.GetValue()
            if ctrl != self.ctrl:
                if self.ctrl:
                    self.ctrl.SetItemState(-1, wx.LIST_MASK_STATE, wx.LIST_STATE_SELECTED)
                self.ctrl = ctrl
            sel = self.ctrl.sel
            if sel != -1:
                self.sel = sel
            flag = self.ctrl.GetSelectedItemCount() > 0
            delOneBtn.Enable(flag)
            delBoxBtn.Enable(flag)
            evt.Skip()
        eventsCtrl_0.Bind(eg.EVT_VALUE_CHANGED, onFocus)
        eventsCtrl_1.Bind(eg.EVT_VALUE_CHANGED, onFocus)
        eventsCtrl_2.Bind(eg.EVT_VALUE_CHANGED, onFocus)
        eventsCtrl_3.Bind(eg.EVT_VALUE_CHANGED, onFocus)
        eventsCtrl_4.Bind(eg.EVT_VALUE_CHANGED, onFocus)


        def onDelOneBtn(evt):
            self.ctrl.OnDeleteButton()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            evt.Skip()
        delOneBtn.Bind(wx.EVT_BUTTON, onDelOneBtn)


        def onDelBoxBtn(evt):
            self.ctrl.OnDeleteAllButton()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            evt.Skip()
        delBoxBtn.Bind(wx.EVT_BUTTON, onDelBoxBtn)


        def onClearBtn(evt):
            eventsCtrl_0.DeleteAllItems()
            eventsCtrl_1.DeleteAllItems()
            eventsCtrl_2.DeleteAllItems()
            eventsCtrl_3.DeleteAllItems()
            eventsCtrl_4.DeleteAllItems()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            self.evtList = [[],[],[],[],[]]
            evt.Skip()
        clearBtn.Bind(wx.EVT_BUTTON, onClearBtn)


        def onClose(evt):
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
            self.panel.setFocus()
        self.Bind(wx.EVT_CLOSE, onClose)


        def onCancel(evt):
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)


        def onOK(evt):
            self.panel.evtList = self.evtList
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)

        sizer.Layout()
        self.Raise()
        self.Show()
#===============================================================================

class Menu(wx.Frame):

    def __init__(
        self,
        fore,
        back,
        foreSel,
        backSel,
        fontInfo,
        flag,
        plugin,
        event,
        monitor,
        hWnd,
        evtList,
        ix,
        ):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'MPC_menu',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )
        self.flag = False
        self.monitor = 0
        self.oldMenu = []

        self.fore     = fore
        self.back     = back
        self.foreSel  = foreSel
        self.backSel  = backSel
        self.fontInfo = fontInfo
        self.flag     = flag
        self.plugin   = plugin
        self.monitor  = monitor
        self.hWnd     = hWnd
        self.evtList  = evtList
        eg.TriggerEvent("OnScreenMenu.%s" % self.plugin.text.opened, prefix = "RadioSure")
        for evt in self.evtList[0]:
            eg.Bind(evt, self.onUp)
        for evt in self.evtList[1]:
            eg.Bind(evt, self.onDown)
        for evt in self.evtList[2]:
            eg.Bind(evt, self.onLeft)
        for evt in self.evtList[3]:
            eg.Bind(evt, self.onRight)
        for evt in self.evtList[4]:
            eg.Bind(evt, self.onEscape)
        self.menuHwnd, self.menu = self.plugin.GetRS_Menu(self.hWnd)
        self.items = self.plugin.GetItemList(self.menuHwnd, self.menu)
        self.choices = [item[0] for item in self.items]
        self.menuGridCtrl = MenuGrid(self, len(self.choices))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        mainSizer.Add(self.menuGridCtrl, 0, wx.EXPAND)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(gridlib.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.onDoubleClick, self.menuGridCtrl)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        font = wx.FontFromNativeInfoString(fontInfo)
        self.menuGridCtrl.SetFont(font)
        arial = wx.FontFromNativeInfoString(ARIAL_INFO)
        self.SetFont(font)
        hght = self.GetTextExtent('X')[1]
        for n in range(1,1000):
            arial.SetPointSize(n)
            self.SetFont(arial)
            h = self.GetTextExtent(u"\u25a0")[1]
            if h > hght:
                break
        arial.SetPointSize(2*n/3)
        self.SetFont(arial)
        self.w0 = 2 * self.GetTextExtent(u"\u25a0")[0]
        attr = gridlib.GridCellAttr()
        attr.SetFont(arial)
        attr.SetAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.menuGridCtrl.SetColAttr(0,attr)
        for n in range(1,1000):
            arial.SetPointSize(n)
            self.SetFont(arial)
            h = self.GetTextExtent(u"\u25ba")[1]
            if h > hght:
                break
        arial.SetPointSize(n/2)
        self.SetFont(arial)
        self.w2 = 2 * self.GetTextExtent(u"\u25ba")[0]
        attr = gridlib.GridCellAttr()
        attr.SetFont(arial)
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        self.menuGridCtrl.SetColAttr(2,attr)
        self.SetFont(font)
        self.SetBackgroundColour((0, 0, 0))
        self.menuGridCtrl.SetBackgroundColour(self.back)
        self.menuGridCtrl.SetForegroundColour(self.fore)
        self.menuGridCtrl.SetSelectionBackground(self.backSel)
        self.menuGridCtrl.SetSelectionForeground(self.foreSel)
        if self.flag:
            self.timer=MyTimer(t = 5.0, plugin = self.plugin)
        self.menuGridCtrl.Set(self.items)
        self.UpdateMenu(ix == 0, ix)
        self.plugin.menuDlg = self
        wx.Yield()
        SetEvent(event)


    def DrawMenu(self, ix):
        self.Show(False)
        self.menuGridCtrl.SetGridCursor(ix, 1)
        self.menuGridCtrl.SelectRow(ix)
        monDim = GetMonitorDimensions()
        try:
            x,y,ws,hs = monDim[self.monitor]
        except IndexError:
            x,y,ws,hs = monDim[0]
        # menu height calculation:
        h=self.GetCharHeight()+4
        for i in range(len(self.choices)):
            self.menuGridCtrl.SetRowSize(i,h)
            self.menuGridCtrl.SetCellValue(i,1," "+self.choices[i])
            if self.items[i][3] == -1:
                self.menuGridCtrl.SetCellValue(i,2, u"\u25ba")
        height0 = len(self.choices)*h
        height1 = h*((hs-20)/h)
        height = min(height0, height1)+6
        # menu width calculation:
        width_lst=[]
        for item in self.choices:
            width_lst.append(self.GetTextExtent(item+' ')[0])
        width = max(width_lst)+8
        self.menuGridCtrl.SetColSize(0,self.w0)
        self.menuGridCtrl.SetColSize(1,width)
        self.menuGridCtrl.SetColSize(2,self.w2)
        self.menuGridCtrl.ForceRefresh()
        width = width + self.w0 + self.w2
        if height1 < height0:
            width += SYS_VSCROLL_X
        if width > ws-50:
            if height + SYS_HSCROLL_Y < hs:
                height += SYS_HSCROLL_Y
            width = ws-50
        width += 6
        x_pos = x + (ws - width)/2
        y_pos = y + (hs - height)/2
        self.SetDimensions(x_pos,y_pos,width,height)
        self.menuGridCtrl.SetDimensions(2, 2, width-6, height-6, wx.SIZE_AUTO)
        self.Show(True)
        self.Raise()


    def UpdateMenu(self, root = False, ix = 0):
        if root:
            self.menuHwnd, self.menu = self.plugin.GetRS_Menu(self.hWnd)
        else:
            self.menuHwnd, self.menu = self.GetSubMenuExt(self.hWnd, ix)
            ix = 0
        self.items = self.plugin.GetItemList(self.menuHwnd, self.menu)
        if len(self.items)==0:
            PlaySound('SystemExclamation', SND_ASYNC)
            eg.PrintError("Please report: %i, %i, %i, %i" % (ix, int(root), self.menuHwnd, self.menu))
            #self.menu,ix = self.oldMenu.pop()
            #self.items = self.plugin.GetItemList(self.hWnd, self.menu)
        self.choices = [item[0] for item in self.items]
        self.menuGridCtrl.Set(self.items)
        self.DrawMenu(ix)


    def MoveCursor(self, step):
        max=len(self.choices)
        if max > 0:
            self.menuGridCtrl.MoveCursor(step)


    def onUp(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, -1)
        return True #stop processing this event !!!


    def onDown(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, 1)
        return True #stop processing this event !!!


    def onLeft(self, event):
        if len(self.oldMenu) > 0:
            ix = self.oldMenu.pop()
            wx.CallAfter(self.UpdateMenu, True, ix)
        else:
            wx.CallAfter(self.destroyMenu)
        return True #stop processing this event !!!


    def onRight(self, event):
        wx.CallAfter(self.DefaultAction)
        return True #stop processing this event !!!


    def onEscape(self, event):
        wx.CallAfter(self.destroyMenu)
        return True #stop processing this event !!!


    def GetSubMenuExt(self, hWnd, ix):
        menu, hMenu = self.plugin.GetRS_Menu(hWnd)
        if menu:
            hMenu = GetSubMenu(hMenu, ix)
            return (menu, hMenu)


    def DefaultAction(self):
        sel = self.menuGridCtrl.GetSelection()
        item = self.items[sel]
        id = item[3]
        if id != -1:
            self.destroyMenu()
            SendMessage(self.hWnd, WM_COMMAND, id, 0)
        else:
            self.oldMenu.append(sel)
            wx.CallAfter(self.UpdateMenu, False, item[1])


    def onFrameCharHook(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_F4:
            if event.AltDown():
                self.destroyMenu()
        elif keyCode == wx.WXK_RETURN or keyCode == wx.WXK_NUMPAD_ENTER:
            self.DefaultAction()
        elif keyCode == wx.WXK_RIGHT or keyCode == wx.WXK_NUMPAD_RIGHT:
            self.DefaultAction()
        elif keyCode == wx.WXK_ESCAPE:
            self.destroyMenu()
        elif keyCode == wx.WXK_UP or keyCode == wx.WXK_NUMPAD_UP:
            self.menuGridCtrl.MoveCursor(-1)
        elif keyCode == wx.WXK_DOWN or keyCode == wx.WXK_NUMPAD_DOWN:
            self.menuGridCtrl.MoveCursor(1)
        elif keyCode == wx.WXK_LEFT or keyCode == wx.WXK_NUMPAD_LEFT:
            if len(self.oldMenu) > 0:
                ix = self.oldMenu.pop()
                wx.CallAfter(self.UpdateMenu, True, ix)
            else:
                self.destroyMenu()
        else:
            event.Skip()


    def onDoubleClick(self, event):
        self.DefaultAction()
        event.Skip()


    def onClose(self, event):
        self.Show(False)
        self.Destroy()
        self.plugin.menuDlg = None


    def destroyMenu(self, event = None):
        for evt in self.evtList[0]:
            eg.Unbind(evt, self.onUp)
        for evt in self.evtList[1]:
            eg.Unbind(evt, self.onDown)
        for evt in self.evtList[2]:
            eg.Unbind(evt, self.onLeft)
        for evt in self.evtList[3]:
            eg.Unbind(evt, self.onRight)
        for evt in self.evtList[4]:
            eg.Unbind(evt, self.onEscape)
        if self.flag:
            self.timer.Cancel()
        eg.TriggerEvent("OnScreenMenu.%s" % self.plugin.text.closed, prefix = "RadioSure")
        self.Close()
#===============================================================================


class RadioSure(eg.PluginBase):

    text=Text
    menuDlg = None
    RadioSurePath = u''
    xmlPath = u''
    data = []
    tmpData = []
    dialog = None
    manager = None
    Favorites = []
    History = []
    Current = ['','']
    FavIx = -1
    HistIx = -1
    List = None
    maxFav = None
    submenus = None


    def GetRS_Menu(self, hwnd):

        WM_CONTEXTMENU   = 0x007B
        OBJID_CLIENT     = 0xFFFFFFFC

        class RECT(Structure):
            _fields_ = [
                ('left', c_long),
                ('top', c_long),
                ('right', c_long),
                ('bottom', c_long),
            ]

        class MENUBARINFO(Structure):
            _fields_ = [
                ('cbSize',  c_ulong),
                ('rcBar',  RECT),            # rect of bar, popup, item
                ('hMenu',  c_long),          # real menu handle of bar, popup
                ('hwndMenu',  c_long),       # hwnd of item submenu if one
                ('fBarFocused',  c_int, 1),  # bar, popup has the focus
                ('fFocused',  c_int, 1),     # item has the focus
            ]

        findMenu = eg.WindowMatcher(
                    u'RadioSure.exe',
                    None,
                    u'#32768',
                    None,
                    None,
                    None,
                    True,
                    0.0,
                    0
                )
        PostMessage(hwnd, WM_CONTEXTMENU, hwnd, 0x00010001)
        menu = []
        i = 0
        while len(menu) == 0:
            menu = findMenu()
            i+=1
            if i > 1000:
                break
        if menu:
            menu = menu[0]
            mbi = MENUBARINFO()
            mbi.cbSize = sizeof(mbi)
            if _user32.GetMenuBarInfo(
                menu,
                OBJID_CLIENT,
                0,
                byref(mbi)
            ):
                return (menu, mbi.hMenu)
        return (None, None)


    def GetItemList(self, hWnd, hMenu):
        WM_INITMENUPOPUP = 0x0117
        MF_BYPOSITION    = 1024
        MF_GRAYED        = 1
        MF_DISABLED      = 2
        MF_CHECKED       = 8
        MF_SEPARATOR     = 2048
        SendMessage(hWnd, WM_INITMENUPOPUP, hMenu, 0) #REFRESH MENU STATE !!!
        itemList = []
        itemName = c_buffer("\000" * 128)
        count = GetMenuItemCount(hMenu)
        for i in range(count):
            _user32.GetMenuStringA(c_int(hMenu),
                                         c_int(i),
                                         itemName,
                                         c_int(len(itemName)),
                                         MF_BYPOSITION)
            hMenuState = _user32.GetMenuState(c_int(hMenu),
                                                   c_int(i),
                                                   MF_BYPOSITION)
            id = _user32.GetMenuItemID(c_int(hMenu), c_int(i))
    #        if hMenuState & (MF_GRAYED|MF_DISABLED|MF_SEPARATOR):
            if hMenuState & (MF_GRAYED|MF_DISABLED):
                continue
            item = itemName.value.replace("&","").split("\t")[0]
            if item == "" and id == 0:
                continue
            checked = bool(hMenuState & MF_CHECKED)
            itemList.append((item, i, checked, id))
        PostMessage(hWnd, WM_CLOSE, 0, 0)
        return itemList


    def GetLanguageXml(self):
        xmltoparse = u'%s\\RadioSure.xml' % self.xmlpath
        xmltoparse = xmltoparse.encode(FSE) if isinstance(xmltoparse, unicode) else xmltoparse
        xmldoc = miniDom.parse(xmltoparse)
        general = xmldoc.getElementsByTagName('General')
        if general: #NOTE: don't use general[0].getElementsByTagName('Language') !!!!!!!!!!!!!!
            langNodes = [node for node in general[0].childNodes if node.localName =="Language"]
            if langNodes:
                langFile = abspath(join(self.RadioSurePath+"\\Lang", langNodes[0].firstChild.data))
                langFile = langFile.encode(FSE) if isinstance(langFile, unicode) else langFile
                languageXml = miniDom.parse(langFile)
                return languageXml


    def GetLastPlayed(self):
        xmltoparse = u'%s\\RadioSure.xml' % self.xmlpath
        xmltoparse = xmltoparse.encode(FSE) if isinstance(xmltoparse, unicode) else xmltoparse
        xmldoc = miniDom.parse(xmltoparse)
        lastPlayed = xmldoc.getElementsByTagName('LastPlayed')
        if lastPlayed:
            try:
                source = lastPlayed[0].getElementsByTagName('Source')[0].firstChild
                source = source.data if source else ""
                title = lastPlayed[0].getElementsByTagName('Title')[0].firstChild
                title = title.data  if title else ""
                genre = lastPlayed[0].getElementsByTagName('Genre')[0].firstChild
                genre = genre.data if genre else ""
                language = lastPlayed[0].getElementsByTagName('Language')[0].firstChild
                language = language.data if language else ""
                country = lastPlayed[0].getElementsByTagName('Country')[0].firstChild
                country = country.data if country else ""
                return (source, title, genre, language, country)
            except:
                pass
        return None


    def GetOneInstance(self):
        xmltoparse = u'%s\\RadioSure.xml' % self.xmlpath
        xmltoparse = xmltoparse.encode(FSE) if isinstance(xmltoparse, unicode) else xmltoparse
        xmldoc = miniDom.parse(xmltoparse)
        advanced = xmldoc.getElementsByTagName('Advanced')
        if advanced:
            oneInstance = advanced[0].getElementsByTagName('One_instance')[0].firstChild.data
            return oneInstance


    def GetStrings(self):
        language = self.GetLanguageXml()
        if language:
            res = {}
            mainWindow = language.getElementsByTagName('MainWindow')
            res['stop'] = mainWindow[0].getElementsByTagName('Stop')[0].firstChild.data
            res['unmute'] = mainWindow[0].getElementsByTagName('Unmute')[0].firstChild.data
            res['stopRec'] = mainWindow[0].getElementsByTagName('StopRecording')[0].firstChild.data
            return res


    def GetSubmenuStrings(self):
        choices = [self.text.root]
        language = self.GetLanguageXml()
        if language:
            mainWindow = language.getElementsByTagName('MainWindow')
            equaliser = language.getElementsByTagName('EQUALIZER')
            sleeptimer = language.getElementsByTagName('SleepTimer')
            favorites = language.getElementsByTagName('Favorites')
#            choices.append(favorites[0].getElementsByTagName('Title')[0].firstChild.data)
            for fav in favorites:
                title = fav.getElementsByTagName('Title')
                if title:
                    break
            choices.append(title[0].firstChild.data)
            choices.append(mainWindow[0].getElementsByTagName('Back')[0].firstChild.data)
            choices.append(equaliser[0].getElementsByTagName('Title')[0].firstChild.data)
            choices.append(mainWindow[0].getElementsByTagName('WindowMenu')[0].firstChild.data)
            choices.append(mainWindow[0].getElementsByTagName('ClipboardMenu')[0].firstChild.data)
            choices.append(sleeptimer[0].getElementsByTagName('Title')[0].firstChild.data)
            choices.append(mainWindow[0].getElementsByTagName('Language')[0].firstChild.data)
        return choices


    def GetRS_Status(self, hwnd):
        menu, hMenu = self.GetRS_Menu(hwnd)
        if menu:
            menuItems = self.GetItemList(menu, hMenu)
            strings = self.GetStrings()
            if menuItems and strings:
                res = [
                    strings['stop'] == menuItems[0][0],    # Playing
                    strings['unmute'] == menuItems[1][0],  # Muted
                    strings['stopRec'] == menuItems[2][0], # Recording
                    menuItems[3][2]        # Record only current track
                ]
                return res


    def GetMenuItem(self, hwnd, indx): # indx = 7 for Fav, 8 for Hist, 9 for Equalizer
        menu, hMenu = self.GetRS_Menu(hwnd)
        if menu:
            hMenu = GetSubMenu(hMenu, indx)
            menuItems = self.GetItemList(menu, hMenu)
            flags = [item[2] for item in menuItems]
            if True in flags:
                ix = flags.index(True)
                return (ix, unicode(menuItems[ix][0].decode(eg.systemEncoding)))
        return (-1, "")


    def RefreshVariables(self):
        xmltoparse = u'%s\\RadioSure.xml' % self.xmlpath
        xmltoparse = xmltoparse.encode(FSE) if isinstance(xmltoparse, unicode) else xmltoparse
        if not exists(xmltoparse):
            return
        xmldoc = miniDom.parse(xmltoparse)
        lastPlayed = xmldoc.getElementsByTagName('LastPlayed')
        if lastPlayed:
            lastPlayed=lastPlayed[0]
            src = lastPlayed.getElementsByTagName('Source')
            if src:
                src = src[0].firstChild.data
            else:
                src = ""

            ttl = lastPlayed.getElementsByTagName('Title')
            if ttl:
                ttl = ttl[0].firstChild.data
            else:
                ttl = ""
            self.Current = [src, ttl]
        else:
            self.Current = ["", ""]
        histNode = xmldoc.getElementsByTagName('History')
        if histNode:
            self.History = getStations(histNode[0])
        else:
            self.History = []
        favNode = xmldoc.getElementsByTagName('Favorites')
        if favNode:
            self.Favorites = getStations(favNode[0])
        else:
            self.Favorites = []
        tmp = [item[:2] for item in self.Favorites]
        if self.Current in tmp:
            self.FavIx = tmp.index(self.Current)
        else:
            self.FavIx = -1
        tmp = [item[:2] for item in self.History]
        if self.Current in tmp:
            self.HistIx = tmp.index(self.Current)
        else:
            self.HistIx = -1
        return self.Favorites


    def NextRun(self, type, data):

        def FindRunDateTime(runList, cond):
            runList.sort()
            runDateTime = ""
            if len(runList) > 0:
                if not cond:
                    return runList[0]
                found = False
                for item in runList:
                    if item.weekday() > 4:
                        found = True
                        break
                    else:
                        if (item.month, item.day) in self.holidays[0]:
                            pass
                        elif (item.year, item.month, item.day) in self.holidays[1]:
                            pass
                        else:
                            found = True
                            break
                if found:
                    runDateTime = item
            return runDateTime

        now = dt.now()
        now = now.replace(microsecond = 0) + td(seconds = 2)
        runTime = dt.strptime(data[0], "%H:%M:%S").time()
        if type == 0: # once or yearly
            runDate = dt.strptime(data[2], '%Y-%m-%d')
            runDateTime = dt.combine(runDate, runTime)
            if now < runDateTime:
                return str(runDateTime)
            elif not data[3]:
                return ""
            else:
                if runDateTime.replace(year = now.year) < now:
                    return str(runDateTime.replace(year = now.year + 1))
                else:
                    return str(runDateTime.replace(year = now.year))
        elif type == 1: # daily
            runDateTime = dt.combine(now.date(), runTime)
            if now.time() > runTime:
                runDateTime += td(days = 1)
            return str(runDateTime)
        elif type == 2: # weekly
            if not data[2]:
                return ""
            runDateTime = dt.combine(now.date(), runTime)
            weekdaysLower = []
            weekdaysLarger = []
            nowDay = now.weekday()
            for weekday in range(7):
                if 2**weekday & data[2]:
                    if weekday < nowDay or (weekday == nowDay and now.time() > runTime):
                        weekdaysLower.append(weekday)
                    else:
                        weekdaysLarger.append(weekday)
            if not data[4] and not data[3]: # without holiday check
                if len(weekdaysLarger) > 0:
                    delta = weekdaysLarger[0] - nowDay
                    return str(runDateTime + td(days = delta))
                delta = 7 + weekdaysLower[0] - nowDay
                return str(runDateTime + td(days = delta))
            elif data[4]: # holiday check
                found = False
                shift = 0
                while True:
                    for day in weekdaysLarger:
                        delta = day + shift - nowDay
                        tmpRunDT = runDateTime + td(days = delta)
                        if tmpRunDT.weekday() > 4: # weekend
                            found = True
                            break
                        else: # workday
                            if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                                pass
                            elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                                pass
                            else:
                                found = True
                                break
                    if found:
                        break
                    shift += 7
                    for day in weekdaysLower:
                        delta = day + shift - nowDay
                        tmpRunDT = runDateTime + td(days = delta)
                        if tmpRunDT.weekday() > 4: # weekend
                            found = True
                            break
                        else: # workday
                            if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                                pass
                            elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                                pass
                            else:
                                found = True
                                break
                    if found:
                        break
                return str(tmpRunDT)
            else: # holiday_2 check
                if len(weekdaysLarger) > 0:
                    Delta = weekdaysLarger[0] - nowDay
                else:
                    Delta = 7 + weekdaysLower[0] - nowDay
                start = 0 if now.time() < runTime else 1
                found = False
                for delta in range(start, Delta):
                    tmpRunDT = runDateTime + td(days = delta)
                    if tmpRunDT.weekday() < 5:
                        if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                            found = True
                            break
                        elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                            found = True
                            break
                return str(tmpRunDT if found else runDateTime + td(days = Delta))
        elif type == 3: # monthly/weekday
            if data[2] == 0 or data[3] == 0 or (data[4] + data[5]) == 0:
                return ""
            currMonth = now.month
            currYear = now.year
            monthsInt = data[4] + (data[5] << 6)
            months = []
            for month in range(1,13):
                if 2 ** (month - 1) & monthsInt:
                    months.append(month)
            if currMonth in months:
                runList = []
                for ix in range(6):
                    if 2 ** ix & data[2]:
                        for weekday in range(7):
                            if 2 ** weekday & data[3]:
                                day = FindMonthDay(currYear, currMonth, weekday, ix)
                                if day:
                                    runDateTime = dt.combine(dt(currYear, currMonth, day).date(), runTime)
                                    if now < runDateTime:
                                        runList.append(runDateTime)
                tmpRunDT = FindRunDateTime(runList, data[6])
                if tmpRunDT:
                    return str(tmpRunDT)
            lower = []
            larger = []
            for month in months:
                if month > currMonth:
                    larger.append(month)
                else: #month <= currMonth:
                    lower.append(month)
            year = currYear
            tmpRunDT = None
            while True:
                for month in larger:
                    runList = []
                    for ix in range(6):
                        if 2 ** ix & data[2]:
                            for weekday in range(7):
                                if 2 ** weekday & data[3]:
                                    day = FindMonthDay(year, month, weekday, ix)
                                    if day:
                                        runDateTime = dt.combine(dt(year, month, day).date(), runTime)
                                        runList.append(runDateTime)
                    tmpRunDT = FindRunDateTime(runList, data[6])
                    if tmpRunDT:
                        break
                if tmpRunDT:
                    break
                year += 1
                for month in lower:
                    runList = []
                    for ix in range(6):
                        if 2 ** ix & data[2]:
                            for weekday in range(7):
                                if 2 ** weekday & data[3]:
                                    day=FindMonthDay(year, month, weekday, ix)
                                    if day:
                                        runDateTime = dt.combine(dt(year, month, day).date(), runTime)
                                        runList.append(runDateTime)
                    tmpRunDT = FindRunDateTime(runList, data[6])
                    if tmpRunDT:
                        break
                if tmpRunDT:
                    break
            return str(tmpRunDT)
        elif type == 4: #monthly/day
            if (data[2] + data[3] + data[4] + data[5]) == 0 or (data[6] + data[7]) == 0:
                return ""
            runList = []
            currMonth = now.month
            currYear = now.year
            monthsInt = data[6] + (data[7] << 6)
            daysInt = data[2] + (data[3] << 8) + (data[4] << 16) + (data[5] << 24)
            days = []
            for day in range(1, 32):
                if 2 ** (day - 1) & daysInt:
                    days.append(day)
            months = []
            for month in range(1, 13):
                if 2 ** (month - 1) & monthsInt:
                    months.append(month)
            if currMonth in months:
                for day in days:
                    if day > monthrange(currYear, currMonth)[1]:
                        break
                    runDateTime = dt.combine(dt(currYear, currMonth, day).date(), runTime)
                    if now < runDateTime:
                        runList.append(runDateTime)
            if len(runList) == 0:
                lower = []
                larger = []
                nextMonth = None
                for month in months:
                    if month > currMonth:
                        larger.append(month)
                    else: #month<=currMonth:
                        lower.append(month)
                if len(larger) > 0:
                    nextYear = currYear
                    for month in larger:
                        for day in days:
                            if day > monthrange(nextYear, month)[1]:
                                break
                            runDateTime = dt.combine(dt(nextYear, month, day).date(), runTime)
                            runList.append(runDateTime)
                if len(runList) == 0 and len(lower) > 0:
                    nextYear = currYear + 1
                    for month in lower:
                        for day in days:
                            if day > monthrange(nextYear, month)[1]:
                                break
                            runDateTime = dt.combine(dt(nextYear, month, day).date(), runTime)
                            runList.append(runDateTime)
            if len(runList) > 0:
                return str(min(runList))
            else:
                return ""
        else: #type == 5: #periodically
            runDate = dt.strptime(data[2], '%Y-%m-%d')
            runDateTime = dt.combine(runDate, runTime)
            if now < runDateTime:
                return str(runDateTime)
            elif data[4] in (0, 1): #unit =  minute or hour
                period =  data[3] * 60 if not data[4] else data[3] * 3600
                if period < 86400 and not 86400 % period:
                    if now.time() > runTime:
                        date = now.date()
                    else:
                        date = now.date() - td(days = 1)
                    runDateTime = dt.combine(date, runTime)
                delta = now - runDateTime
                delta = delta.seconds + 86400 * delta.days
                share = delta / period
                share += 1
                delta = td(seconds = share * period)
                return str(runDateTime + delta)
            elif data[4] in (2, 3): #unit = day or week
                period = data[3] if data[4] == 2 else 7 * data[3]
                delta = (now - runDateTime).days
                share = delta / period
                if not delta % period:
                    if now.time() < runTime:
                        return str(dt.combine(now.date(), runTime))
                share += 1
                delta = td(days = share * period)
                return str(runDateTime + delta)
            elif data[4] == 4: #unit = month
                period = data[3]
                month = runDateTime.month
                year = runDateTime.year
                while now > runDateTime:
                    year += period / 12
                    m = month+period % 12
                    if m > 12:
                        year += 1
                        month = m % 12
                    else:
                        month = m
                    runDateTime = runDateTime.replace(year = year).replace(month = month)
                return str(runDateTime)
            else: # data[4] == 6: #unit = year
                period = data[3]
                year = runDateTime.year
                while now > runDateTime:
                    year += period
                    runDateTime = runDateTime.replace(year = year)
                return str(runDateTime)


    def updateLogFile(self, line, blank = False):
        if not self.logfile:
            return
        f = openFile(self.logfile, encoding='utf-8', mode='a')
        if blank:
            f.write("\r\n")
        f.write("%s  %s\r\n" % (str(dt.now())[:19], line))
        f.close()


    def Execute(self, params, immed = False):
        next = self.NextRun(params[2], params[3])
        modes = params[7]
        playRec = modes & 6
        args = []
        if playRec != 6:
            args.append(u'%s\\RadioSure.exe' % self.RadioSurePath)
            if playRec:
                args.append("/record")
            else:
                args.append("/play")
            if playRec == 4:
                args.append("/mute")
            if modes & 1:
                args.append("/hidden")
            args.append(u'/source="%s"' % params[5])
            duration = 60*int(params[3][1][:2])+int(params[3][1][-2:])
            if duration:
                args.append('/duration=%i' % duration)
            if params[6]:
                recfile = eg.ParseString(params[6])
                try:
                    recfile = eval(recfile)
                except:
                    pass
                args.append(u'/filename="%s"' % recfile)
            elif playRec:
                args.append(u'/filename="%s"' % params[1])
            Popen(args)
        if not immed and next: # new schedule, if valid next run time and not TEST/IMMEDIATELY run
            startTicks = mktime(strptime(next, "%Y-%m-%d %H:%M:%S"))
            eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, params[1])
        triggEvt = modes & 24
        if triggEvt == 8:
            eg.TriggerEvent(self.text.launched, prefix = "RadioSure", payload = params[1])
        elif triggEvt == 16:
            eg.TriggerEvent(self.text.launched, prefix = "RadioSure", payload = params)
        return (next, my_list2cmdline(args) if args else None)


    def RadioSureScheduleRun(self, schedule):
        data = self.data
        ix = [item[1] for item in data].index(schedule)
        next, cmdline = self.Execute(data[ix])
        last = str(dt.now())[:19]
        self.data[ix][4] = last
        if self.dialog:
            tmpList = [item[1] for item in self.tmpData]
            if schedule in tmpList:
                ixTmp = tmpList.index(schedule)
                self.tmpData[ixTmp][4] = last
            self.dialog.RefreshGrid(ixTmp, last, next)
        nxt = next[:19] if next else self.text.none
        self.updateLogFile(self.text.execut % (data[ix][1], nxt))
        if cmdline:
            self.updateLogFile(self.text.cmdLine % cmdline.decode(FSE))


    def UpdateEGscheduler(self):
        data = self.data
        tmpList = []
        sched_list = eg.scheduler.__dict__['heap']
        for sched in sched_list:
            if sched[1] == self.RadioSureScheduleRun:
                if sched[2][0] in [item[1] for item in data]:
                    tmpList.append(sched)
                else:
                    self.updateLogFile(self.text.cancAndDel % sched[2][0])
                    eg.scheduler.CancelTask(sched)
        sched_list = tmpList
        for schedule in data:
            startMoment = self.NextRun(schedule[2], schedule[3])
            if not startMoment:
                continue
            startTicks = mktime(strptime(startMoment,"%Y-%m-%d %H:%M:%S"))
            nameList = [item[2][0] for item in sched_list]
            if schedule[1] in nameList:
                sched = sched_list[nameList.index(schedule[1])]
                if not schedule[0]: # schedule is disabled !
                    eg.scheduler.CancelTask(sched)
                    self.updateLogFile(self.text.cancAndDis % schedule[1])
                elif sched[0] != startTicks: #Re-schedule
                    self.updateLogFile(self.text.re_Sched % (schedule[1], startMoment))
                    eg.scheduler.CancelTask(sched)
                    eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, schedule[1])
            elif schedule[0]: #New schedule
                    eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, schedule[1])
                    self.updateLogFile(self.text.newSched % (schedule[1], startMoment))


    def dataToXml(self):
        impl = miniDom.getDOMImplementation()
        dom = impl.createDocument(None, u'Document', None)
        root = dom.documentElement
        commentNode = dom.createComment(self.text.xmlComment % str(dt.now())[:19])
        dom.insertBefore(commentNode, root)
        for item in self.data:
            schedNode = dom.createElement(u'Schedule')
            schedNode.setAttribute(u'Name', unicode(item[1]))
            schedNode.setAttribute(u'Type', unicode(item[2]))
            enableNode = dom.createElement(u'Enable')
            enableText = dom.createTextNode(unicode(item[0]))
            enableNode.appendChild(enableText)
            schedNode.appendChild(enableNode)
            last_runNode = dom.createElement(u'Last_run')
            last_runText = dom.createTextNode(unicode(item[4]))
            last_runNode.appendChild(last_runText)
            schedNode.appendChild(last_runNode)
            sourceNode = dom.createElement(u'Source')
            sourceText = dom.createTextNode(unicode(item[5]))
            sourceNode.appendChild(sourceText)
            schedNode.appendChild(sourceNode)
            filenameNode = dom.createElement(u'Filename')
            filenameText = dom.createTextNode(unicode(item[6]))
            filenameNode.appendChild(filenameText)
            schedNode.appendChild(filenameNode)
            modesNode = dom.createElement(u'Modes')
            modesText = dom.createTextNode(unicode(item[7]))
            modesNode.appendChild(modesText)
            schedNode.appendChild(modesNode)
            dateTimeNode = dom.createElement(u'Datetime')
            start_timeNode = dom.createElement(u'Start_time')
            start_timeText = dom.createTextNode(unicode(item[3][0]))
            start_timeNode.appendChild(start_timeText)
            dateTimeNode.appendChild(start_timeNode)
            durationNode = dom.createElement(u'Duration')
            durationText = dom.createTextNode(unicode(item[3][1]))
            durationNode.appendChild(durationText)
            dateTimeNode.appendChild(durationNode)
            if item[2] == 0:
                dateNode = dom.createElement(u'Date')
                dateText = dom.createTextNode(unicode(item[3][2]))
                dateNode.appendChild(dateText)
                dateTimeNode.appendChild(dateNode)
                yearlyNode = dom.createElement(u'Yearly')
                yearlyText = dom.createTextNode(unicode(item[3][3]))
                yearlyNode.appendChild(yearlyText)
                dateTimeNode.appendChild(yearlyNode)
            if item[2] == 2:
                weekdayNode = dom.createElement(u'Weekday')
                weekdayText = dom.createTextNode(unicode(item[3][2]))
                weekdayNode.appendChild(weekdayText)
                dateTimeNode.appendChild(weekdayNode)
                holidayNode = dom.createElement(u'HolidayCheck')
                holidayText = dom.createTextNode(unicode(item[3][4]))
                holidayNode.appendChild(holidayText)
                dateTimeNode.appendChild(holidayNode)
                holiday2Node = dom.createElement(u'HolidayCheck_2')
                holiday2Text = dom.createTextNode(unicode(item[3][3]))
                holiday2Node.appendChild(holiday2Text)
                dateTimeNode.appendChild(holiday2Node)
            if item[2] == 3:
                orderNode = dom.createElement(u'Order')
                orderText = dom.createTextNode(unicode(item[3][2]))
                orderNode.appendChild(orderText)
                dateTimeNode.appendChild(orderNode)
                weekdayNode = dom.createElement(u'Weekday')
                weekdayText = dom.createTextNode(unicode(item[3][3]))
                weekdayNode.appendChild(weekdayText)
                dateTimeNode.appendChild(weekdayNode)
                first_halfNode = dom.createElement(u'First_half')
                first_halfText = dom.createTextNode(unicode(item[3][4]))
                first_halfNode.appendChild(first_halfText)
                dateTimeNode.appendChild(first_halfNode)
                second_halfNode = dom.createElement(u'Second_half')
                second_halfText = dom.createTextNode(unicode(item[3][5]))
                second_halfNode.appendChild(second_halfText)
                dateTimeNode.appendChild(second_halfNode)
                holidayNode = dom.createElement(u'HolidayCheck')
                holidayText = dom.createTextNode(unicode(item[3][6]))
                holidayNode.appendChild(holidayText)
                dateTimeNode.appendChild(holidayNode)
            if item[2] == 4:
                q_1_Node = dom.createElement(u'Q_1')
                q_1_Text = dom.createTextNode(unicode(item[3][2]))
                q_1_Node.appendChild(q_1_Text)
                dateTimeNode.appendChild(q_1_Node)
                q_2_Node = dom.createElement(u'Q_2')
                q_2_Text = dom.createTextNode(unicode(item[3][3]))
                q_2_Node.appendChild(q_2_Text)
                dateTimeNode.appendChild(q_2_Node)
                q_3_Node = dom.createElement(u'Q_3')
                q_3_Text = dom.createTextNode(unicode(item[3][4]))
                q_3_Node.appendChild(q_3_Text)
                dateTimeNode.appendChild(q_3_Node)
                q_4_Node = dom.createElement(u'Q_4')
                q_4_Text = dom.createTextNode(unicode(item[3][5]))
                q_4_Node.appendChild(q_4_Text)
                dateTimeNode.appendChild(q_4_Node)
                first_halfNode = dom.createElement(u'First_half')
                first_halfText = dom.createTextNode(unicode(item[3][6]))
                first_halfNode.appendChild(first_halfText)
                dateTimeNode.appendChild(first_halfNode)
                second_halfNode = dom.createElement(u'Second_half')
                second_halfText = dom.createTextNode(unicode(item[3][7]))
                second_halfNode.appendChild(second_halfText)
                dateTimeNode.appendChild(second_halfNode)
            if item[2] == 5:
                dateNode = dom.createElement(u'Date')
                dateText = dom.createTextNode(unicode(item[3][2]))
                dateNode.appendChild(dateText)
                dateTimeNode.appendChild(dateNode)
                numberNode = dom.createElement(u'Number')
                numberText = dom.createTextNode(unicode(item[3][3]))
                numberNode.appendChild(numberText)
                dateTimeNode.appendChild(numberNode)
                unitNode = dom.createElement(u'Unit')
                unitText = dom.createTextNode(unicode(item[3][4]))
                unitNode.appendChild(unitText)
                dateTimeNode.appendChild(unitNode)
            schedNode.appendChild(dateTimeNode)
            root.appendChild(schedNode)
        f = file(u'%s\\Scheduler.xml' % self.xmlpath, 'wb')
        writer = lookup('utf-8')[3](f)
        dom.writexml(writer, encoding = 'utf-8')
        f.close()
        return f.closed


    def xmlToData(self):
        data = []
        xmlfile = u'%s\\Scheduler.xml' % self.xmlpath
        if not exists(xmlfile):
            return data
        xmldoc = miniDom.parse(xmlfile)
        document = xmldoc.getElementsByTagName('Document')[0]
        schedules = tuple(document.getElementsByTagName('Schedule'))
        for schedule in schedules:
            dataItem = []
            enable = int(schedule.getElementsByTagName('Enable')[0].firstChild.data)
            dataItem.append(enable)
            name = schedule.attributes["Name"].value
            dataItem.append(name)
            schedType = int(schedule.attributes["Type"].value)
            dataItem.append(schedType)
            dateTime = schedule.getElementsByTagName('Datetime')[0]
            params = []
            start_time = dateTime.getElementsByTagName('Start_time')[0].firstChild.data
            params.append(start_time)
            duration = dateTime.getElementsByTagName('Duration')[0].firstChild.data
            params.append(duration)
            if schedType == 0:
                date = dateTime.getElementsByTagName('Date')[0].firstChild.data
                params.append(date)
                date = int(dateTime.getElementsByTagName('Yearly')[0].firstChild.data)
                params.append(date)
            if schedType == 2:
                weekday = int(dateTime.getElementsByTagName('Weekday')[0].firstChild.data)
                params.append(weekday)
                holiday2 = int(dateTime.getElementsByTagName('HolidayCheck_2')[0].firstChild.data)
                params.append(holiday2)
                holiday = int(dateTime.getElementsByTagName('HolidayCheck')[0].firstChild.data)
                params.append(holiday)
            if schedType == 3:
                order = int(dateTime.getElementsByTagName('Order')[0].firstChild.data)
                params.append(order)
                weekday = int(dateTime.getElementsByTagName('Weekday')[0].firstChild.data)
                params.append(weekday)
                first_half = int(dateTime.getElementsByTagName('First_half')[0].firstChild.data)
                params.append(first_half)
                second_half = int(dateTime.getElementsByTagName('Second_half')[0].firstChild.data)
                params.append(second_half)
                holiday = int(dateTime.getElementsByTagName('HolidayCheck')[0].firstChild.data)
                params.append(holiday)
            if schedType == 4:
                q_1 = int(dateTime.getElementsByTagName('Q_1')[0].firstChild.data)
                params.append(q_1)
                q_2 = int(dateTime.getElementsByTagName('Q_2')[0].firstChild.data)
                params.append(q_2)
                q_3 = int(dateTime.getElementsByTagName('Q_3')[0].firstChild.data)
                params.append(q_3)
                q_4 = int(dateTime.getElementsByTagName('Q_4')[0].firstChild.data)
                params.append(q_4)
                first_half = int(dateTime.getElementsByTagName('First_half')[0].firstChild.data)
                params.append(first_half)
                second_half = int(dateTime.getElementsByTagName('Second_half')[0].firstChild.data)
                params.append(second_half)
            if schedType == 5:
                date = dateTime.getElementsByTagName('Date')[0].firstChild.data
                params.append(date)
                number = int(dateTime.getElementsByTagName('Number')[0].firstChild.data)
                params.append(number)
                unit = int(dateTime.getElementsByTagName('Unit')[0].firstChild.data)
                params.append(unit)
            dataItem.append(params)
            last_run = schedule.getElementsByTagName('Last_run')[0].firstChild
            last_run = last_run.data if last_run else " "
            dataItem.append(last_run)
            source = schedule.getElementsByTagName('Source')[0].firstChild
            source = source.data if source else ""
            dataItem.append(source)
            filename = schedule.getElementsByTagName('Filename')[0].firstChild
            filename = filename.data if filename else ""
            dataItem.append(filename)
            modes = schedule.getElementsByTagName('Modes')[0].firstChild.data
            dataItem.append(int(modes))
            data.append(dataItem)
        return data


    def GetStatusRS(self, hwnds = None):
        hwnds = hwnds or HandleRS()
        maxFav = None
        recording = None
        if hwnds:
            for hwnd in hwnds:
                try:
                    maxFav = SendMessageTimeout(hwnd, self.favMesg, 0, 0)
                    recording = SendMessageTimeout(hwnd, self.recMesg, 0, 0)
                except:
                    #raise
                    pass
                if maxFav is not None and recording is not None:
                    #pass
                    break
        if maxFav is not None and recording is not None:
            return (maxFav, recording)
        else:
            return (None, None)


    def GetNewHwnd(self, oldHwnds = [], src = None, hid = False, mut = False):
        hwnds = HandleRS()
        if len(hwnds) > 0 and self.GetOneInstance():
            wx.CallAfter(
                MessageBox,
                None,
                self.text.message3,
                self.text.messBoxTit1,
                wx.ICON_EXCLAMATION,
                15,
                plugin = self,
                )
            return []
        maxInst = 2 if (not self.maxFav or self.maxFav == 30) else 10
        if len(oldHwnds) >= maxInst:
            wx.CallAfter(
                MessageBox,
                None,
                self.text.message2 % maxInst,
                self.text.messBoxTit1,
                wx.ICON_EXCLAMATION,
                15,
                plugin = self,
                )
            return []
        i = 0
        hwnds = oldHwnds if oldHwnds else []
        rs = u'%s\\RadioSure.exe' % self.RadioSurePath
        rs = rs.encode(FSE) if isinstance(rs, unicode) else rs
        args = [rs, "/play"]
        if mut:
            args.append("/mute")
        if hid:
            args.append("/hidden")
        if src:
            args.append(u'/source="%s"' % src)
        if isfile(rs):
            Popen(args)
            while i < 100 and hwnds == oldHwnds:
                i += 1
                hwnds = HandleRS()
                sleep(0.1)
            sleep(1.5)
        return list(set(hwnds)-set(oldHwnds))


    def SetMaxFavs(self):
        maxFav = 30
        hwnds = HandleRS()
        if hwnds:
            maxFav, rec = self.GetStatusRS(hwnds)
            if not maxFav: # ToDo: kill process ???
                hwnds = self.GetNewHwnd(hwnds, hid = True, mut = True)
                if hwnds:
                    maxFav, rec = self.GetStatusRS(hwnds)
                    PostMessage(hwnds[0], WM_COMMAND, 1, 0) # Close
        else:
            hwnds = self.GetNewHwnd(hid = True, mut = True)
            if hwnds:
                maxFav, rec = self.GetStatusRS(hwnds)
                PostMessage(hwnds[0], WM_COMMAND, 1, 0) # Close
        self.maxFav = maxFav

    def __init__(self):
        self.observThread = None
        text=Text
        self.AddActionsFromList(ACTIONS)

    def GetLabel(
        self,
        path = None,
        xmlpath = None,
        logfile = None,
        holidays = [[], []],
        first_day = 0,
    ):
        if not self.submenus:
            self.RadioSurePath = path
            self.xmlpath = xmlpath
            self.submenus = self.GetSubmenuStrings()
        return self.name


    def __start__(
        self,
        path = None,
        xmlpath = None,
        logfile = None,
        holidays = [[], []],
        first_day = 0,
        ):

        self.recMesg = RegisterWindowMessage("WM_RADIOSURE_GET_RECORDING_STATUS")
        self.favMesg = RegisterWindowMessage("WM_RADIOSURE_GET_MAX_FAVORITES")

        if not self.submenus:
            self.submenus = self.GetSubmenuStrings()
        self.RadioSurePath = path
        self.xmlpath = xmlpath
        wx.CallAfter(self.SetMaxFavs)
        self.logfile = logfile
        self.holidays = holidays
        self.first_day = first_day
        self.data = []
        self.tmpData = []
        if self.xmlpath:
            if exists(self.xmlpath):
                self.data = self.xmlToData()
            if logfile:
                 self.updateLogFile(self.text.start, True)
            self.UpdateEGscheduler()


    def __stop__(self):
        if self.dataToXml():
            self.updateLogFile("File Scheduler.xml saved")
        if self.observThread:
            ot = self.observThread
            if ot.isAlive():
                ot.AbortObservation()
            del self.observThread
        self.observThread = None
        sched_list = eg.scheduler.__dict__['heap']
        tmpLst = []
        for sched in sched_list:
            if sched[1] == self.RadioSureScheduleRun:
                tmpLst.append(sched)
        if len(tmpLst) > 0:
            self.updateLogFile(self.text.stop)
            for sched in tmpLst:
                eg.scheduler.CancelTask(sched)
                self.updateLogFile(self.text.canc % sched[2][0])
        if self.dialog:
            self.dialog.onClose(wx.CommandEvent())
        if self.manager:
            self.manager.onClose(wx.CommandEvent())


    def __close__(self):
        if self.observThread:
            ot = self.observThread
            if ot.isAlive():
                ot.AbortObservation()


    def Configure(
        self,
        path = "",
        xmlpath = "",
        logfile = None,
        holidays = [[], []],
        first_day = 0,
        ):
        panel = eg.ConfigPanel(self)
        panel.holidays = cpy(holidays)
        del holidays
        managerButton = wx.Button(panel, -1, self.text.managerButton)
        if not path: #First run after plugin insert
            managerButton.Enable(False)
        self.RadioSurePath = path
        self.xmlpath = xmlpath
        self.logfile = logfile
        self.first_day = first_day
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        rsPathCtrl = MyDirBrowseButton(
            panel,
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        rsPathCtrl.GetTextCtrl().SetEditable(False)
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        xmlPathCtrl = MyDirBrowseButton(
            panel,
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        xmlPathCtrl.GetTextCtrl().SetEditable(False)
        logFileCtrl = MyFileBrowseButton(
            panel,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseFile,
            buttonText = eg.text.General.browse
        )
        logFileCtrl.GetTextCtrl().SetEditable(False)
        logCheckBox = wx.CheckBox(panel, -1, self.text.logLabel)
        if not self.RadioSurePath or not exists(self.RadioSurePath):
            RSpath = getPathFromReg() #Try get path from registry
            if RSpath: #Regular installation
                if exists(RSpath):
                    self.RadioSurePath = RSpath
            else: #Portable installation
                self.RadioSurePath = u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
            xmlPath = u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
            if exists(xmlPath):
                self.xmlpath = xmlPath
        if exists(join(self.RadioSurePath, "RadioSure.exe")):
            rsPathCtrl.GetTextCtrl().ChangeValue(self.RadioSurePath)
            rsPathCtrl.Enable(False)
            label1Text.Enable(False)
        if exists(join(self.xmlpath, "RadioSure.xml")):
            xmlPathCtrl.GetTextCtrl().ChangeValue(self.xmlpath)
            xmlPathCtrl.Enable(False)
            label2Text.Enable(False)


        def NotHidden():
            try:
                nssh = OpenKey(
                    HKEY_CURRENT_USER,
                    "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced"
                )
                res = QueryValueEx(nssh, "Hidden")[0] != 2
                CloseKey(nssh)
            except:
                res = False
            return res


        def NotHiddenAttr(path):
            attr = GetFileAttributes(path)
            if attr & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                return False
            else:
                p = split(path)[0]
                if len(p) > 3:
                    return NotHiddenAttr(p)
                return True

        if self.logfile is None:
            logCheckBox.SetValue(True)
            if NotHiddenAttr(self.xmlpath) or NotHidden():
                self.logfile = u'%s\\RadioSureSchedulerLog.txt' % self.xmlpath
            else:
                self.logfile = u'%s\\RadioSureSchedulerLog.txt' % unicode(eg.folderPath.Documents)
        else:
            val = self.logfile != ""
            logCheckBox.SetValue(val)
            logFileCtrl.Enable(val)
        logFileCtrl.GetTextCtrl().ChangeValue(self.logfile)
        rsPathCtrl.startDirectory = self.RadioSurePath
        xmlPathCtrl.startDirectory = self.xmlpath
        logFileCtrl.startDirectory = self.logfile or u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
        sizerAdd = panel.sizer.Add
        sizerAdd(label1Text, 0)
        sizerAdd(rsPathCtrl,0,wx.TOP|wx.EXPAND,2)
        sizerAdd(label2Text, 0, wx.TOP,15)
        sizerAdd(xmlPathCtrl,0,wx.TOP|wx.EXPAND,2)
        sizerAdd(logCheckBox, 0, wx.TOP,15)
        sizerAdd(logFileCtrl, 0, wx.TOP|wx.EXPAND,2)
        firstDayLabel = wx.StaticText(panel, -1, self.text.first_day)
        firstDayCtrl = wx.Choice(
            panel,
            -1,
            choices = (
                day_name[0],
                day_name[6]
            ),
            size = (firstDayLabel.GetSize()[0], -1)
        )
        firstDayCtrl.SetSelection(first_day)
        panel.holidButton = wx.Button(panel, -1, self.text.holidButton)


        def OnApplyBtn(evt):
            managerButton.Enable(True)
            evt.Skip()
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyBtn)


        def onManagerButton(evt):
            if not self.dialog:
                wx.CallAfter(SchedulerDialog, self.text.OpenScheduler, self)
            else:
                if self.dialog.GetPosition() == (-32000, -32000):
                    ShowWindow(self.dialog.GetHandle(), SW_RESTORE)
                wx.CallAfter(self.dialog.Raise)
            evt.Skip()
        managerButton.Bind(wx.EVT_BUTTON, onManagerButton)


        def onHolidButton(evt):
            dlg = HolidaysFrame(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowHolidaysFrame)
            evt.Skip()
        panel.holidButton.Bind(wx.EVT_BUTTON, onHolidButton)
        bottomSizer = wx.GridBagSizer(1, 1)
        bottomSizer.Add(firstDayLabel, (0, 0), flag = wx.LEFT)
        bottomSizer.Add(firstDayCtrl, (1, 0), flag = wx.LEFT)
        bottomSizer.Add((1, -1), (1, 1), flag = wx.EXPAND)
        bottomSizer.Add((1, -1), (1, 3), flag = wx.EXPAND)
        bottomSizer.Add(panel.holidButton, (1, 2))
        bottomSizer.Add(managerButton, (1, 4), flag = wx.RIGHT)
        bottomSizer.AddGrowableCol(1,1)
        bottomSizer.AddGrowableCol(3,1)
        sizerAdd(bottomSizer, 1, wx.TOP | wx.EXPAND, 15)


        def Validation():
            flag1 = "%s\\RadioSure.exe" % exists(rsPathCtrl.GetValue())
            flag2 = "%s\\RadioSure.xml" % exists(xmlPathCtrl.GetValue())
            flag3 = logCheckBox.IsChecked() and logFileCtrl.GetValue() != "" or not logCheckBox.IsChecked()
            flag = flag1 and flag2 and flag3
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)


        def OnPathChange(event):
            path = rsPathCtrl.GetValue()
            if not exists("%s\\RadioSure.exe" % path):
                MessageBox(
                    panel,
                    self.text.boxMessage1 % 'RadioSure.exe',
                    self.text.boxTitle % path,
                    wx.ICON_EXCLAMATION,
                    plugin = self
                    )
            if path != "":
                rsPathCtrl.startDirectory = path
                self.RadioSurePath = path
            Validation()
            event.Skip()
        rsPathCtrl.Bind(wx.EVT_TEXT, OnPathChange)


        def OnPath2Change(event):
            path2 = xmlPathCtrl.GetValue()
            if not exists("%s\\RadioSure.xml" % path2):
                MessageBox(
                    panel,
                    self.text.boxMessage1 % 'RadioSure.xml',
                    self.text.boxTitle % path2,
                    wx.ICON_EXCLAMATION,
                    plugin = self
                    )
            if path2 != "":
                self.xmlpath = path2
                xmlPathCtrl.startDirectory = path2
            Validation()
            event.Skip()
        xmlPathCtrl.Bind(wx.EVT_TEXT, OnPath2Change)


        def logFileChange(event):
            self.logfile = logFileCtrl.GetValue()
            tmpVal = self.logfile
            if not tmpVal:
                tmpPath = u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
                tmpVal = tmpPath if exists(tmpPath) else self.RadioSurePath
            logFileCtrl.startDirectory = tmpVal
            Validation()
            event.Skip()
        logFileCtrl.Bind(wx.EVT_TEXT, logFileChange)


        def onLogCheckBox(evt):
            val = evt.IsChecked()
            logFileCtrl.Enable(val)
            if not val:
                logFileCtrl.SetValue("")
            else:
                Validation()
            evt.Skip()
        logCheckBox.Bind(wx.EVT_CHECKBOX, onLogCheckBox)
        while panel.Affirmed():
            panel.SetResult(
                rsPathCtrl.GetValue(),
                xmlPathCtrl.GetValue(),
                logFileCtrl.GetValue(),
                panel.holidays,
                firstDayCtrl.GetSelection(),
            )
#===============================================================================
#cls types for Actions list:
#===============================================================================

class Run(eg.ActionBase):

    class text:
        play = "Automatically play selected favorite after start"
        default = "Use start settings RadioSure"
        label = "Select favorite:"
        over = "Too large number (%s > %s) !"
        alr_run = "RadioSure is already running !"


    def __call__(self, play = False, fav = 1):

        def Play(hwnds):
                self.plugin.RefreshVariables()
                if fav <= len(self.plugin.Favorites):
                    if play:
                        SendMessage(hwnds[0], WM_COMMAND, 4101+fav, 0)
                    return str(fav)+": "+self.plugin.Favorites[self.plugin.FavIx][1]
                else:
                    return self.text.over % (str(fav),\
                        str(len(self.plugin.Favorites)))
        hwnds = HandleRS()
        if not hwnds:
            hwnds = self.plugin.GetNewHwnd()
            if hwnds:
                return Play(hwnds)
            else:
                self.PrintError(self.plugin.text.text1)
                return self.plugin.text.text1
        elif play:
            for hwnd in hwnds:
                x, rec = self.plugin.GetStatusRS([hwnd])
                if rec != 1:
                    SendMessage(hwnd, WM_COMMAND, 4101+fav, 0)
                    break
            if rec or rec is None:
                hwnds = self.plugin.GetNewHwnd(hwnds)
                if hwnds:
                    return Play(hwnds)
        else:
            self.PrintError(self.text.alr_run)
            return self.text.alr_run


    def GetLabel(self, play, fav):
        num = str(fav) if play else ''
        return "%s:  %s" % (self.name, num)


    def Configure(self, play = False, fav = 1):
        panel=eg.ConfigPanel(self)
        sizerAdd=panel.sizer.Add
        rb1 = panel.RadioButton(play, self.text.play, style=wx.RB_GROUP)
        rb2 = panel.RadioButton(not play, self.text.default)
        sizerAdd(rb1,0,wx.TOP,15)
        sizerAdd(rb2,0,wx.TOP,6)
        favLbl=wx.StaticText(panel, -1, self.text.label)
        sizerAdd(favLbl,0,wx.TOP,25)
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=30,
        )
        favCtrl.SetValue(fav)
        sizerAdd(favCtrl,0,wx.TOP,5)

        def onChangeMode(evt=None):
            enbl=rb1.GetValue()
            favLbl.Enable(enbl)
            favCtrl.Enable(enbl)
            if evt is not None:
                evt.Skip()
        rb1.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        rb2.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        onChangeMode()

        while panel.Affirmed():
            panel.SetResult(
                rb1.GetValue(),
                favCtrl.GetValue()
            )
#===============================================================================

class WindowControl(eg.ActionBase):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            SendMessage(hwnd[0], WM_SYSCOMMAND, self.value, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class SendMessageActions(eg.ActionBase):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            SendMessage(hwnd[0], WM_COMMAND, self.value, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class MinimRest(eg.ActionBase):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            winState = GetWindowPlacement(hwnd[0])[1]
            if winState == 1:
                SendMessage(hwnd[0], WM_COMMAND, 1075, 0)
            elif winState == 2:
                SendMessage(hwnd[0], WM_SYSCOMMAND, SC_RESTORE, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class CheckAndChange(eg.ActionBase):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            status = self.plugin.GetRS_Status(hwnd[0])
            if status[self.value[0]] == self.value[1]:
                SendMessage(hwnd[0], WM_COMMAND, self.value[2], 0)
#===============================================================================

class GetStatus(eg.ActionBase):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            status = self.plugin.GetRS_Status(hwnd[0])
            return status[self.value]
#===============================================================================

class GetMenuItem(eg.ActionBase):
    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            return self.plugin.GetMenuItem(hwnd[0], self.value)
#===============================================================================

class SetVolume(eg.ActionBase):

    class text:
        label=["Set volume (0 - 100%):",
            "Set step (1 - 25%):",
            "Set step (1 - 25%):"]


    def __call__(self, step = None):
        if step is None:
            if self.value == 0:
                step = 50
            else:
                step = 5
        hwnd = GetCtrlByID(1006) #1006 = ID of ctrl "msctls_trackbar32"
        if hwnd:
            vol = SendMessage(hwnd, TBM_GETPOS, 0, 0)
            key = None
            value = None
            if self.value == 0:
                volume = step
            elif self.value == 1:
                volume = vol+step if (vol+step)<100 else 100
            else:
                volume = vol-step if (vol-step)>0 else 0
            if vol>volume:
                key='{Left}'
                if vol>volume+1:
                    value = volume+1
            elif vol<volume:
                key='{Right}'
                if vol<volume-1:
                    value = volume-1
            if value:
                SendMessage(hwnd, TBM_SETPOS,1,value)
            if key:
                eg.SendKeys(hwnd, key, False)
            return SendMessage(hwnd, TBM_GETPOS, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1


    def Configure(self, step = None):
        if step is None:
            if self.value == 0:
                step = 50
            else:
                step = 5
        panel=eg.ConfigPanel(self)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.label[self.value]))
        if self.value == 0:
            Min = 0
            Max = 100
        else:
            Min = 1
            Max = 25
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            fractionWidth=0,
            increment=1,
            min=Min,
            max=Max,
        )
        volumeCtrl.SetValue(step)
        panel.sizer.Add(volumeCtrl,0,wx.TOP,10)

        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())
#===============================================================================

class GetVolume(eg.ActionBase):

    def __call__(self):
        hwnd = GetCtrlByID(1006)  #1006 = ID for ctrl "msctls_trackbar32"
        if hwnd:
            return SendMessage(hwnd, TBM_GETPOS, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class SelectFav(eg.ActionBase):

    class text:
        label = "Select preset number (1-30):"
        txtLabel = 'Preset number:'
        over = "Too large number (%s > %s) !"
        modeLabel = 'Preset number to get as:'
        modeChoices = [
            'Event payload',
            'Python expression',
            'Number'
        ]


    def __call__(self,fav = 1, mode = 0, number = '{eg.event.payload}'):
        hwnd = HandleRS()
        if hwnd:
            if mode == 2:
                indx = fav
            else:
                indx = int(eg.ParseString(number))
            self.plugin.RefreshVariables()
            if indx <= len(self.plugin.Favorites):
                SendMessage(hwnd[0], WM_COMMAND, 4101+indx, 0)
                return str(indx)+": "+self.plugin.Favorites[indx-1][1]
            else:
                self.PrintError(
                    self.text.over % (str(indx),str(len(self.plugin.Favorites))))
                return self.text.over % (str(indx),str(len(self.plugin.Favorites)))
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1


    def GetLabel(self, fav, mode, number):
        return "%s %s" % (self.text.txtLabel, str(fav) if mode == 2 else number)


    def Configure(self, fav = 1, mode = 0, number = '{eg.event.payload}'):
        self.number = number
        panel = eg.ConfigPanel(self)
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            self.text.modeLabel,
            choices = self.text.modeChoices,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(mode)
        txtBoxLabel = wx.StaticText(panel, -1, self.text.txtLabel)
        numberCtrl = wx.TextCtrl(panel,-1,self.number)
        spinLabel = wx.StaticText(panel, -1, self.text.label)
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=30,
        )
        favCtrl.SetValue(fav)
        panel.sizer.Add(radioBoxMode, 0, wx.TOP,0)
        panel.sizer.Add(txtBoxLabel,0,wx.TOP,10)
        panel.sizer.Add(numberCtrl,0,wx.TOP,5)
        panel.sizer.Add(spinLabel,0,wx.TOP,10)
        panel.sizer.Add(favCtrl,0,wx.TOP,5)

        def onRadioBox(event = None):
            sel = radioBoxMode.GetSelection()
            txtBoxLabel.Enable(False)
            numberCtrl.Enable(False)
            spinLabel.Enable(False)
            favCtrl.Enable(False)
            if sel == 0:
                self.number = '{eg.event.payload}'
            elif sel == 1:
                txtBoxLabel.Enable(True)
                numberCtrl.Enable(True)
            else:
                self.number = favCtrl.GetValue()
                spinLabel.Enable(True)
                favCtrl.Enable(True)
            numberCtrl.ChangeValue(str(self.number))
            if event:
                event.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, onRadioBox)
        onRadioBox()


        def onSpin(event):
            numberCtrl.ChangeValue(str(favCtrl.GetValue()))
            event.Skip()
        favCtrl.Bind(wx.EVT_TEXT, onSpin)

        while panel.Affirmed():
            panel.SetResult(
                favCtrl.GetValue(),
                radioBoxMode.GetSelection(),
                numberCtrl.GetValue())
#===============================================================================

class NextPrevFav(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            self.plugin.RefreshVariables()
            #ix = self.plugin.FavIx
            ix = self.plugin.GetMenuItem(hwnd[0], 7)[0]
            if self.value == 1 and ix == len(self.plugin.Favorites) - 1 :
                ix = -1
            elif self.value == -1 and ix == 0:
                ix = len(self.plugin.Favorites)
            SendMessage(hwnd[0], WM_COMMAND, 4102+ix+self.value, 0)
            return (str(ix+self.value+1)+": "+self.plugin.Favorites[ix+self.value][1])
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class RandomFav(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            self.plugin.RefreshVariables()
            ix = self.plugin.GetMenuItem(hwnd[0], 7)[0]
            lng = len(self.plugin.Favorites)
            if lng > 1:
                newIx = randrange(lng)
                while newIx == ix:
                    newIx = randrange(lng)
                SendMessage(hwnd[0], WM_COMMAND, 4102+newIx, 0)
                return (str(newIx+1)+": "+self.plugin.Favorites[newIx][1])
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class GetPlayingTitle(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            return GetWindowText(hwnd[0])
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class StartTitlebarObservation(eg.ActionBase):

    class text:
        intervalLabel = "Refresh interval (s):"
        label = "Tilebar event suffix (empty = no event):"
        label2 = "Station event suffix (empty = no event):"
        toolSuffix = """Here you specify the desired event suffix.
If the string is empty, the event is not triggered."""


    def __call__(
        self,
        period = 1.0,
        evtName ="titlebar",
        evtName2 ="station",
    ):
        if evtName or evtName2:
            if self.plugin.observThread:
                ot = self.plugin.observThread
                if ot.isAlive():
                    ot.AbortObservation()
                del self.plugin.observThread
            ot = ObservationThread(
                period,
                evtName,
                evtName2,
                self.plugin
            )
            ot.start()
            self.plugin.observThread = ot


    def GetLabel(
        self,
        period = 1.0,
        evtName ="",
        evtName2 ="",
    ):
        return "%s: %.1fs, %s, %s" % (self.name, period, evtName, evtName2)

    def Configure(
        self,
        period = 1.0,
        evtName = "titlebar",
        evtName2 ="station",
    ):
        panel = eg.ConfigPanel()
        periodNumCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            period,
            integerWidth = 5,
            fractionWidth = 1,
            allowNegative = False,
            min = 0.1,
            increment = 0.1,
        )
        intervalLbl = wx.StaticText(panel, -1, self.text.intervalLabel)
        textLabel = wx.StaticText(panel, -1, self.text.label)
        textControl = wx.TextCtrl(panel, -1, evtName, size = (200,-1))
        textControl.SetToolTipString(self.text.toolSuffix)
        textLabel2 = wx.StaticText(panel, -1, self.text.label2)
        textControl2 = wx.TextCtrl(panel, -1, evtName2, size = (200,-1))
        textControl2.SetToolTipString(self.text.toolSuffix)
        AddCtrl = panel.sizer.Add
        AddCtrl(intervalLbl, 0, wx.TOP, 20)
        AddCtrl(periodNumCtrl, 0, wx.TOP, 3)
        AddCtrl(textLabel, 0, wx.TOP, 20)
        AddCtrl(textControl, 0, wx.TOP, 3)
        AddCtrl(textLabel2, 0, wx.TOP, 20)
        AddCtrl(textControl2, 0, wx.TOP, 3)
        textLabel.SetFocus()

        while panel.Affirmed():
            panel.SetResult(
            periodNumCtrl.GetValue(),
            textControl.GetValue(),
            textControl2.GetValue(),
        )
#===============================================================================

class StopTitlebarObservation(eg.ActionBase):

    def __call__(self):
        if self.plugin.observThread:
            ot = self.plugin.observThread
            if ot.isAlive():
                ot.AbortObservation()
            del self.plugin.observThread
        self.plugin.observThread = None
#===============================================================================

class OpenManager(eg.ActionBase):

    def __call__(self):
        if not self.plugin.manager:
            wx.CallAfter(ManagerDialog, self.text, self.plugin)
        else:
            if self.plugin.manager.GetPosition() == (-32000, -32000):
                ShowWindow(self.plugin.manager.GetHandle(), SW_RESTORE)
            wx.CallAfter(self.plugin.manager.Raise)
#===============================================================================

class HideManager(eg.ActionBase):

    def __call__(self):
        if self.plugin.manager:
            wx.CallAfter(self.plugin.manager.Close)
#===============================================================================

class GetFavorites(eg.ActionBase):

    def __call__(self):
        self.plugin.RefreshVariables()
        return self.plugin.Favorites
#===============================================================================

class OpenScheduler(eg.ActionBase):

    def __call__(self):
        if not self.plugin.dialog:
            wx.CallAfter(SchedulerDialog, self.text, self.plugin)
        else:
            if self.plugin.dialog.GetPosition() == (-32000, -32000):
                ShowWindow(self.plugin.dialog.GetHandle(), SW_RESTORE)
            wx.CallAfter(self.plugin.dialog.Raise)
#===============================================================================

class HideScheduler(eg.ActionBase):

    def __call__(self):
        if self.plugin.dialog:
            wx.CallAfter(self.plugin.dialog.Close)
#===============================================================================

class EnableSchedule(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"
        notFound = 'Can not find schedule "%s" !'


    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not exists(xmlfile):
            return
        data = self.plugin.data
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            if self.value > -1:
                data[ix][0] = self.value
                self.plugin.dataToXml()
                self.plugin.UpdateEGscheduler()
                if self.plugin.dialog:
                    wx.CallAfter(self.plugin.dialog.EnableSchedule, schedule, self.value)
            return data[tmpLst.index(schedule)]
        else:
            return self.text.notFound % schedule


    def Configure(self, schedule=""):
        panel = eg.ConfigPanel()
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not exists(xmlfile):
            return
        data = self.plugin.xmlToData()
        choices = [item[1] for item in data]
        textControl = wx.ComboBox(panel, -1, schedule, size = (300,-1), choices = choices)
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.scheduleTitle), 0,wx.LEFT|wx.TOP, 10)
        panel.sizer.Add(textControl, 0, wx.LEFT, 10)

        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class EnableAll(eg.ActionBase):

    def __call__(self):
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not exists(xmlfile):
            return
        data = self.plugin.data
        for schedule in data:
            schedule[0] = self.value
        self.plugin.dataToXml()
        self.plugin.UpdateEGscheduler()
        if self.plugin.dialog:
            wx.CallAfter(self.plugin.dialog.EnableAll, self.value)
#===============================================================================

class DeleteSchedule(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"


    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not exists(xmlfile):
            return
        data = self.plugin.data
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            data.pop(ix)
            self.plugin.dataToXml()
            self.plugin.UpdateEGscheduler()
            if self.plugin.dialog:
                wx.CallAfter(self.plugin.dialog.DeleteSchedule, schedule)


    def Configure(self, schedule=""):
        panel = eg.ConfigPanel()
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not exists(xmlfile):
            return
        data = self.plugin.xmlToData()
        choices = [item[1] for item in data]
        textControl = wx.ComboBox(panel, -1, schedule, size = (300,-1), choices = choices)
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.scheduleTitle), 0,wx.LEFT|wx.TOP, 10)
        panel.sizer.Add(textControl, 0, wx.LEFT, 10)

        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class RunScheduleImmediately(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"
        notFound = 'Can not find schedule "%s" !'
        immedRun = 'Schedule "%s" - IMMEDIATELY execution. Possible next time: %s'

    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        data = self.plugin.data
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            sched = self.plugin.data[ix]
            if sched[0]:
                for sch in eg.scheduler.__dict__['heap']:
                    if sch[1] == self.plugin.RadioSureScheduleRun:
                        if sch[2][0] == sched[1]:
                            eg.scheduler.CancelTask(sch)
                            self.plugin.updateLogFile(self.plugin.text.canc % sch[2][0])
                            break
                next, cmdline = self.plugin.Execute(sched, True)
                next = next[:19] if next else self.plugin.text.none
                self.plugin.updateLogFile(self.text.immedRun % (sched[1], next))
                if cmdline:
                    self.plugin.updateLogFile(self.plugin.text.cmdLine % cmdline.decode(FSE))
        else:
            self.PrintError(self.text.notFound % schedule)
            return self.text.notFound % schedule


    def Configure(self, schedule = ""):
        panel = eg.ConfigPanel()
        data = self.plugin.data
        choices = [item[1] for item in data]
        textControl = wx.ComboBox(panel, -1, schedule, size = (300, -1), choices = choices)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.scheduleTitle), 0, wx.LEFT | wx.TOP, 10)
        panel.sizer.Add(textControl, 0, wx.LEFT, 10)

        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class AddSchedule(eg.ActionBase):

    class text:
        python_expr = "Python expression:"
        descr = u'''<rst>**Add schedule**.

In the edit box, enter a python expression with the parameters of the plan.
This may be for example *eg.result*, *eg.event.payload* or the entire list
(in the same format, what you get as a result of actions **"GetSchedule"**).

This action works in two ways (depending on the title of the schedule):

1. If a schedule with the same title already exists, its parameters are overwritten by new ones.
2. If the title does not exist yet, the schedule is added to the list as new.'''

    def __call__(self, expr = ""):
        schedule = eg.ParseString(expr)
        schedule = eval(schedule)
        if len(schedule) == 8 and isinstance(schedule[1], unicode):
            data = self.plugin.data
            tmpLst = [item[1] for item in data]
            if schedule[1] in tmpLst:
                data[tmpLst.index(schedule[1])] = cpy(schedule)
            else:
                data.append(schedule)
            self.plugin.UpdateEGscheduler()
            if self.plugin.dialog:
                wx.CallAfter(self.plugin.dialog.AddSchedule, schedule)


    def Configure(self, expr=""):
        panel = eg.ConfigPanel(resizable=True)
        textControl = wx.TextCtrl(panel, -1, expr, size = (300,-1), style = wx.TE_MULTILINE )
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.python_expr), 0,wx.LEFT|wx.TOP, 10)
        panel.sizer.Add(textControl, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class ShowMenu(eg.ActionClass):

    name = "Show Radio Sure menu"
    description = "Show Radio Sure menu."
    panel = None

    class text:
        OSELabel = 'Menu show on:'
        menuPreview = 'RS On Screen Menu preview:'
        menuFont = 'Font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        dialog = "Events ..."
        btnToolTip = """Press this button to assign events to control the menu !!!"""
        evtAssignTitle = "Menu control - events assignement"
        events = (
            "Cursor up:",
            "Cursor down:",
            "Back from the (sub)menu:",
            "Submenu, or select an item:",
            "Cancel (Escape):",
        )
        inverted = "Use inverted colours"
        submenuLbl = "Show main menu or submenu:"


    def __call__(
        self,
        fore,
        back,
        fontInfo = TAHOMA_INFO,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        evtList = [],
        inverted = True,
        submenu = 0
    ):
        hwnd = HandleRS()
        if hwnd:
            if not self.plugin.menuDlg:
                event = CreateEvent(None, 0, 0, None)
                wx.CallAfter(
                    Menu,
                    fore,
                    back,
                    foreSel,
                    backSel,
                    fontInfo,
                    False,
                    self.plugin,
                    event,
                    monitor,
                    hwnd[0],
                    evtList,
                    (0, 7, 8, 9, 10, 11, 12, 14)[submenu],
                )
                eg.actionThread.WaitOnEvent(event)


    def GetLabel(
        self,
        fore,
        back,
        fontInfo,
        monitor,
        foreSel,
        backSel,
        evtList,
        inverted,
        submenu = 0
    ):
        return "%s: %s" % (self.name, self.plugin.submenus[submenu])


    def Configure(
        self,
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = TAHOMA_INFO,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        evtList = [[],[],[],[],[]],
        inverted = True,
        submenu = 0
    ):
        self.fontInfo = fontInfo
        self.fore = fore
        self.back = back
        self.foreSel = foreSel
        self.backSel = backSel
        self.oldSel=0
        self.inverted = inverted
        global panel
        panel = eg.ConfigPanel(self)
        panel.evtList = cpy(evtList)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        listBoxCtrl = MenuGrid(panel, 3)
        items = (("Blabla_1",0,True,804),
                 ("Blabla_2",1,False,804),
                 ("Blabla_3",2,False,-1),)
        listBoxCtrl.Set(items)
        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        listBoxCtrl.SetSelectionBackground(self.backSel)
        listBoxCtrl.SetSelectionForeground(self.foreSel)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = eg.FontSelectButton(panel, value = fontInfo)
        font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            fontButton.SetFont(font)
            hght = fontButton.GetTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        arial = wx.FontFromNativeInfoString(ARIAL_INFO)
        fontButton.SetFont(font)
        for n in range(1,1000):
            arial.SetPointSize(n)
            fontButton.SetFont(arial)
            h = fontButton.GetTextExtent(u"\u25a0")[1]
            if h > hght:
                break
        arial.SetPointSize(2*n/3)
        fontButton.SetFont(arial)
        w0 = 2 * fontButton.GetTextExtent(u"\u25a0")[0]
        attr = gridlib.GridCellAttr()
        attr.SetFont(arial)
        attr.SetAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        listBoxCtrl.SetColAttr(0,attr)
        for n in range(1,1000):
            arial.SetPointSize(n)
            fontButton.SetFont(arial)
            h = fontButton.GetTextExtent(u"\u25ba")[1]
            if h > hght:
                break
        arial.SetPointSize(n/2)
        fontButton.SetFont(arial)
        w2 = 2 * fontButton.GetTextExtent(u"\u25ba")[0]
        attr = gridlib.GridCellAttr()
        attr.SetFont(arial)
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        listBoxCtrl.SetColAttr(2,attr)
        listBoxCtrl.SetDefaultRowSize(hght+4, True)
        displayChoice = eg.DisplayChoice(panel, monitor)
        w = displayChoice.GetSize()[0]
        OSElbl = wx.StaticText(panel, -1, self.text.OSELabel)
        useInvertedCtrl = wx.CheckBox(panel, -1, self.text.inverted)
        useInvertedCtrl.SetValue(inverted)
        subMenuLbl = wx.StaticText(panel, -1, self.text.submenuLbl)
        if self.plugin.submenus:
            choices = self.plugin.submenus
        else:
            choices = self.plugin.GetSubmenuStrings()
        subMenuCtrl = wx.Choice(panel, -1, choices = choices)
        subMenuCtrl.SetSelection(submenu)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = eg.ColourSelectButton(panel,fore,title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = eg.ColourSelectButton(panel,back,title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = eg.ColourSelectButton(panel,foreSel,title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = eg.ColourSelectButton(panel,backSel,title = self.text.backgroundSel)
        #Button Dialog "Menu control - assignement of events"
        dialogButton = wx.Button(panel,-1,self.text.dialog)
        dialogButton.SetToolTipString(self.text.btnToolTip)
        foreSelLbl.Enable(not inverted)
        foreSelColourButton.Enable(not inverted)
        backSelLbl.Enable(not inverted)
        backSelColourButton.Enable(not inverted)
        #Sizers
        mainSizer = panel.sizer
        topSizer=wx.GridBagSizer(2, 30)
        mainSizer.Add(topSizer)
        topSizer.Add(previewLbl,(0, 0),flag = wx.TOP,border = 0)
        topSizer.Add(listBoxCtrl,(1, 0),(4, 1))
        topSizer.Add(useInvertedCtrl,(6, 0),flag = wx.TOP, border = 8)
        topSizer.Add(subMenuLbl,(8, 0), flag = wx.TOP,border = 8)
        topSizer.Add(subMenuCtrl,(9, 0), flag = wx.TOP)
        topSizer.Add(fontLbl,(0, 1),flag = wx.TOP)
        topSizer.Add(fontButton,(1, 1),flag = wx.TOP)
        topSizer.Add(foreLbl,(2, 1),flag = wx.TOP,border = 8)
        topSizer.Add(foreColourButton,(3, 1),flag = wx.TOP)
        topSizer.Add(backLbl,(4, 1),flag = wx.TOP,border = 8)
        topSizer.Add(backColourButton,(5, 1),flag = wx.TOP)
        topSizer.Add(OSElbl,(0, 2), flag = wx.TOP)
        topSizer.Add(displayChoice,(1, 2),flag = wx.TOP)
        topSizer.Add(foreSelLbl,(6, 1), (1, 2), flag = wx.TOP,border = 8)
        topSizer.Add(foreSelColourButton, (7, 1), flag = wx.TOP)
        topSizer.Add(backSelLbl,(8, 1), (1, 2), flag = wx.TOP,border = 8)
        topSizer.Add(backSelColourButton, (9, 1), flag = wx.TOP)
        topSizer.Add(dialogButton, (3, 2), flag = wx.TOP|wx.EXPAND)
        panel.sizer.Layout()
        wdth = 160
        if (hght+4)*listBoxCtrl.GetNumberRows() > listBoxCtrl.GetSize()[1]: #after Layout() !!!
            wdth -=  SYS_VSCROLL_X
        listBoxCtrl.SetColSize(0, w0)
        listBoxCtrl.SetColSize(1, wdth - w0 - w2)
        listBoxCtrl.SetColSize(2, w2)
        listBoxCtrl.SetGridCursor(-1, 1)
        listBoxCtrl.SelectRow(0)


        def OnMonitor(evt):
            listBoxCtrl.SetFocus()
            evt.Skip
        displayChoice.Bind(wx.EVT_CHOICE, OnMonitor)


        def OnInverted(evt):
            flag = evt.IsChecked()
            foreSelLbl.Enable(not flag)
            foreSelColourButton.Enable(not flag)
            backSelLbl.Enable(not flag)
            backSelColourButton.Enable(not flag)
            self.inverted = flag
            if flag:
                self.foreSel = self.back
                self.backSel = self.fore
                backSelColourButton.SetValue(self.backSel)
                foreSelColourButton.SetValue(self.foreSel)
                listBoxCtrl.SetSelectionForeground(self.foreSel)
                listBoxCtrl.SetSelectionBackground(self.backSel)
            listBoxCtrl.SetFocus()
            evt.Skip
        useInvertedCtrl.Bind(wx.EVT_CHECKBOX, OnInverted)


        def OnDialogBtn(evt):
            dlg = MenuEventsDialog(
                parent = panel,
                plugin = self.plugin,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowMenuEventsDialog, self.text.evtAssignTitle, self.text.events)
            evt.Skip()
        dialogButton.Bind(wx.EVT_BUTTON, OnDialogBtn)


        def OnFontBtn(evt):
            value = evt.GetValue()
            self.fontInfo = value
            font = wx.FontFromNativeInfoString(value)
            for n in range(10,20):
                font.SetPointSize(n)
                fontButton.SetFont(font)
                hght = fontButton.GetTextExtent('X')[1]
                if hght > 20:
                    break
            listBoxCtrl.SetDefaultCellFont(font)
            listBoxCtrl.SetDefaultRowSize(hght+4, True)
            for i in range(listBoxCtrl.GetNumberRows()):
                listBoxCtrl.SetCellFont(i,1,font)
            listBoxCtrl.SetFocus()
            if evt:
                evt.Skip()
        fontButton.Bind(eg.EVT_VALUE_CHANGED, OnFontBtn)

        def OnColourBtn(evt):
            id = evt.GetId()
            value = evt.GetValue()
            if id == foreColourButton.GetId():
                listBoxCtrl.SetForegroundColour(value)
                if self.inverted:
                    self.backSel = self.fore
                    listBoxCtrl.SetSelectionBackground(value)
                    backSelColourButton.SetValue(value)
            elif id == backColourButton.GetId():
                listBoxCtrl.SetBackgroundColour(value)
                if self.inverted:
                    self.foreSel = self.back
                    listBoxCtrl.SetSelectionForeground(value)
                    foreSelColourButton.SetValue(value)
            elif id == foreSelColourButton.GetId():
                listBoxCtrl.SetSelectionForeground(value)
            elif id == backSelColourButton.GetId():
                listBoxCtrl.SetSelectionBackground(value)
            listBoxCtrl.Refresh()
            listBoxCtrl.SetFocus()
            evt.Skip()
        foreColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        foreSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)


        def setFocus():
            listBoxCtrl.SetFocus()
        panel.setFocus = setFocus

        # re-assign the test button
        def OnButton(event):
            hwnds = HandleRS()
            if hwnds:
                if not self.plugin.menuDlg:
                    wx.CallAfter(
                        Menu,
                        foreColourButton.GetValue(),
                        backColourButton.GetValue(),
                        foreSelColourButton.GetValue(),
                        backSelColourButton.GetValue(),
                        self.fontInfo,
                        True,
                        self.plugin,
                        CreateEvent(None, 0, 0, None),
                        displayChoice.GetSelection(),
                        hwnds[0],
                        panel.evtList,
                        (0, 7, 8, 9, 10, 11, 12, 14)[subMenuCtrl.GetSelection()]
                    )

        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            fontInfo = fontButton.GetValue()
            if not fontInfo:
                font = listBoxCtrl.GetFont()
                font.SetPointSize(36)
                fontInfo = font.GetNativeFontInfoDesc()
            panel.SetResult(
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontInfo,
            displayChoice.GetSelection(),
            foreSelColourButton.GetValue(),
            backSelColourButton.GetValue(),
            panel.evtList,
            useInvertedCtrl.GetValue(),
            subMenuCtrl.GetSelection()
        )
#===============================================================================

ACTIONS = (
    (Run,"Run","Run RadioSure","Run RadioSure with its default settings.",None),
    (SendMessageActions,"Close","Close window (exit RadioSure)","Close window (exit RadioSure).",1),
    (GetPlayingTitle,"GetPlayingTitle","Get currently playing station/title","Gets the name of currently playing station/title.", None),
    (StartTitlebarObservation,"StartTitlebarObservation","Start periodical observation","Starts periodical observation.", None),
    (StopTitlebarObservation,"StopTitlebarObservation","Stop periodical observation","Stops periodical observation.", None),
    (ShowMenu,"ShowMenu","ShowMenu","ShowMenu.",None),
    (eg.ActionGroup, 'Window', 'Window', 'Window',(
        (SendMessageActions,"Minimize","Minimize window","Minimize window.",2),
        (WindowControl,"Restore","Restore window","Restore window.",SC_RESTORE),
#        (SendMessageActions,"MinimRest","Minimize/Restore","Minimize/Restore window.",1075),
        (MinimRest,"MinimRest","Minimize/Restore","Minimize/Restore window.",None),
        (SendMessageActions,"Expand","Collapse/Expand window","Collapse/Expand window.",1076),
        (SendMessageActions,"OnTop","Stay on top On/Off","Stay on top On/Off.",1077),
    )),
    (eg.ActionGroup, 'MainControl', 'Main control', 'Main control',(
        (SendMessageActions,"PlayStop","Play/Stop","Play/Stop.",1000),
        (CheckAndChange,"Play","Play","Play.",(0, False, 1000)),
        (SendMessageActions,"Stop","Stop","Stop.",1008),
        (GetStatus,"GetPlaying","Get status of playing","Get status of playing.",0),
        (SendMessageActions,"MuteOnOff","Mute On/Off","Mute On/Off.",1027),
        (CheckAndChange,"MuteOn","Mute on","Mute on.",(1, False, 1027)),
        (CheckAndChange,"MuteOff","Mute off","Mute off.",(1, True, 1027)),
        (GetStatus,"GetMuted","Get muted","Get muted.",1),
        (SendMessageActions,"RecOnOff","Recording On/Off","Recording On/Off.",1051),
        (CheckAndChange,"RecOn","Recording on","Recording on.",(2, False, 1051)),
        (CheckAndChange,"RecOff","Recording off","Recording off.",(2, True, 1051)),
        (GetStatus,"GetRecording","Get recording","Get recording.",2),
        (SendMessageActions,"RecOnlyCurr",'Toggle "Record only current track"','Toggle "Record only current track".', 4036),
        (CheckAndChange,"RecOnlyOn",'Set "Record only current track"','Set "Record only current track".',(3, False, 4036)),
        (CheckAndChange,"RecOnlyOff",'Clear "Record only current track"','Clear "Record only current track".',(3, True, 4036)),
        (GetStatus,"GetRecOnlyCurr",'Get "Record only current track"','Get "Record only current track".',3),
    )),
    (eg.ActionGroup, 'Volume', 'Volume', 'Volume',(
        (GetVolume,"GetVolume","Get volume","Get volume.", None),
        (SetVolume,"SetVolume","Set volume","Set volume.", 0),
        (SetVolume,"VolumeUp","Volume up","Volume up.", 1),
        (SetVolume,"VolumeDown","Volume down","Volume down.", 2),
    )),
    (eg.ActionGroup, 'Clipboard', 'Clipboard', 'Clipboard',(
        (SendMessageActions,"CopyURLtoClipboard","Copy URL to Clipboard","Copy URL to Clipboard.", 4037),
        (SendMessageActions,"CopyTitleToClipboard","Copy Title to Clipboard","Copy Title to Clipboard.", 4038),
        (SendMessageActions,"PlayURLfromClipboard","Play URL from Clipboard","Play URL from Clipboard.", 4039),
    )),
    (eg.ActionGroup, 'Equalizer', 'Equalizer', 'Equalizer',(
        (SendMessageActions,"EqualizerOff","Equalizer Off","Equalizer Off.", 4040),
        (SendMessageActions,"EqualizerJazz","Equalizer Jazz","Equalizer Jazz.", 4041),
        (SendMessageActions,"EqualizerPop","Equalizer Pop","Equalizer Pop.", 4042),
        (SendMessageActions,"EqualizerRock","Equalizer Rock","Equalizer Rock.", 4043),
        (SendMessageActions,"EqualizerClassic","Equalizer Classic","Equalizer Classic.", 4044),
        (GetMenuItem, "GetEqualizerIndex", "Get Equalizer", "Get Equalizer.", 9),
    )),
    (eg.ActionGroup, 'SleepTimer', 'Sleep timer', 'Sleep timer',(
        (SendMessageActions,"SleepTimerOff","Sleep timer Off","Sleep timer Off.", 4034),
        (SendMessageActions,"SleepIn5Min","Sleep in 5 min","Sleep in 5 min.", 4026),
        (SendMessageActions,"SleepIn10Min","Sleep in 10 min","Sleep in 10 min.", 4027),
        (SendMessageActions,"SleepIn15Min","Sleep in 15 min","Sleep in 15 min.", 4028),
        (SendMessageActions,"SleepIn20Min","Sleep in 20 min","Sleep in 20 min.", 4029),
        (SendMessageActions,"SleepIn30Min","Sleep in 30 min","Sleep in 30 min.", 4030),
        (SendMessageActions,"SleepIn60Min","Sleep in 60 min","Sleep in 60 min.", 4031),
        (SendMessageActions,"SleepIn90Min","Sleep in 90 min","Sleep in 90 min.", 4032),
        (SendMessageActions,"SleepIn120Min","Sleep in 120 min","Sleep in 120 min.", 4033),
    )),
    (eg.ActionGroup, 'Fav_and_Hist', 'Favorites and History', 'Favorites and History',(
        (SendMessageActions,"AddFav","Add to favorites","Add current station to favorites.",1324),
        (SendMessageActions,"RemFav","Remove from favorites","Remove current station from favorites.",1325),
        (SelectFav,"SelectFav","Select favorite (preset number)","Select favorite by preset number (order).", None),
        (NextPrevFav,"NextFav","Next favorite","Next favorite.", 1),
        (NextPrevFav,"PreviousFav","Previous favorite","Previous favorite.", -1),
        (RandomFav,"RandomFav","Random favorite","Random favorite.", None),
        (SendMessageActions,"PreviousHist","Back in history","Back in history.",1038),
        (SendMessageActions,"ForwardHist","Forward in history","Forward in history.",1039),
        (OpenManager,"OpenManager","Open manager","Open manager.", None),
        (HideManager,"HideManager","Hide manager","Hide manager.", None),
        (GetFavorites,"GetFavorites","Get favorites","Get favorites.", None),
        (GetMenuItem, "GetFavoritesIndex", "Get last played favorite station", "Get last played favorite station.", 7),
    )),
    (eg.ActionGroup, 'Scheduler', 'Scheduler', 'Scheduler',(
        (OpenScheduler,"OpenScheduler","Open scheduler","Open scheduler.", None),
        (HideScheduler,"HideScheduler","Hide scheduler","Hide scheduler.", None),
        (EnableSchedule,"EnableSchedule","Enable schedule","Enable schedule.", 1),
        (EnableSchedule,"DisableSchedule","Disable schedule","Disable schedule.", 0),
        (EnableAll,"EnableAll","Enable all schedules","Enable all schedules.", 1),
        (EnableAll,"DisableAll","Disable all schedules","Disable all schedules.", 0),
        (EnableSchedule,"GetSchedule","Get schedule","Get schedule.", -1),
        (AddSchedule,"AddSchedule","Add schedule",AddSchedule.text.descr, None),
        (DeleteSchedule,"DeleteSchedule","Delete schedule","Delete schedule.", None),
        (RunScheduleImmediately, "RunScheduleImmediately", "Run schedule immediately", "Runs schedule immediately.", None),
    )),
)
#===============================================================================
