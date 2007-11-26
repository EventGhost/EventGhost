#
# Plugins/DVBDream/__init__.py
#
# Copyright (C) 2007 townkat
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

import eg

eg.RegisterPlugin(
    name = "DVB Dream",
    author = "townkat",
    version = "2" ,
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control '
        '<a href="http://www.dvbdream.org">'
        'DVB Dream</a>.'
        '\n\n<p>'
        'Tested with DVB Dream 1.4d'
        '\n\n<p>'
        'In DVB Dream Select:'
        '\n'
        'Options->Remote->RemoteControlType->Native'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=612",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAAXNSR0IArs4c6QAAAARn"
        "QU1BAACxjwv8YQUAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdw"
        "nLpRPAAAAklJREFUOE+Vkt1PUnEYx+m6f6B1059Qrbtu20RraytnLa3GlktqeqGzVlHZ"
        "IjIXp5klGqaB8bqABOTFFhDIm0dEOJzDISXAAwUY76/iHKdDMKZNL3qunn2f3+f3e37f"
        "fQ/hOE76rypXdiQa8MMcSJD1WljCtGafRIc2ld0NKVvYYnHkBqP16uAUTw0BXNPikqeQ"
        "iQ+8kOwPEOrkJ7CTQj1ybrqzl+lygkIBHwv9oI8rDgSIQQvlZeuVfqKBYY/X690uZY63"
        "M1lyPyCCARHySowwPkKhaL724fo11x8IUcRlMOhjsZgHcvuDYTTwC/Fj3mBkLRj+HtgI"
        "hyN3AGU6X6kBClPAsrLmQxEMwxAESUVDHXQzoIlNmtMCV6mbHz1Jg1oeO6UqcyZbIlVx"
        "/K3Q8ncZeNXpmJdLgz7H5ScWsS0hsKa+eLL9vBCZDp25a+OKtZn8FimTLyt0rkwytqBW"
        "3BtiHm0do7P1XTTjqCzwRrmhXfn9TOTveu44TdHOiDWEpbWV+obnbt1/Tb45sYxupou4"
        "VG3teGo/3K47RrWdH0FujKMXGaunegxTfGUDaNoXiBZG+dboz7BqOf5eHxfZkyIwxTHF"
        "WdrI7FeMxZX/C/Qw5nG8mkomsqnNddS9jkKwC0Tc4MS7GfY098SF4WKl2rC1/sgjQOiw"
        "L1rMRtM33c52OZlM5HK5YDBQKhbaBrX1M3uAgTEj+fbs2T5+Wy9vhK2EIAiBIRiGOGJV"
        "91AjKXuA3VmwejYv0ZRUuuzaw88sGdQcHQjsGyRC/AMHw0nBpbiPVAAAAABJRU5ErkJg"
        "gg=="
    ),
)
    
    
MyActionList = (
    ('Power', 'Power', None, 1),
    ('Mute', 'Mute', None, 2),
    ('Zero', 'Zero', None, 3),
    ('One', 'One', None, 4),
    ('Two', 'Two', None, 5),
    ('Three', 'Three', None, 6),
    ('Four', 'Four', None, 7),
    ('Five', 'Five', None, 8),
    ('Six', 'Six', None, 9),
    ('Seven', 'Seven', None, 10),
    ('Eight', 'Eight', None, 11),
    ('Nine', 'Nine', None, 12),
    ('ChUp', 'ChUp', None, 13),
    ('ChDn', 'ChDn', None, 14),
    ('VolumeDn', 'VolumeDn', None, 15),
    ('VolumeUp', 'VolumeUp', None, 16),
    ('Ok', 'Ok', None, 17),
    ('Record', 'Record', None, 18),
    ('Recall', 'Recall', None, 19),
    ('Fullscreen', 'Fullscreen', None, 20),
    ('Teletext', 'Teletext', None, 21),
    ('EPG', 'EPG', None, 22),
    ('Tab', 'Tab', None, 23),
    ('Info', 'Info', None, 24),
    ('Optional1', 'Optional1', None, 25),
    ('Optional2', 'Optional2', None, 26),
    ('Optional3', 'Optional3', None, 27),
    ('Optional4', 'Optional4', None, 28),
    ('Optional5', 'Optional5', None, 29),
    ('Optional6', 'Optional6', None, 30),
    ('Optional7', 'Optional7', None, 31),
    ('Optional8', 'Optional8', None, 32),
    ('Optional9', 'Optional9', None, 33),
    ('Play', 'Play', None, 34),
    ('Stop', 'Stop', None, 35),
    ('Forward', 'Forward', None, 36),
    ('Rewind', 'Rewind', None, 37),
    ('Pause', 'Pause', None, 38),
    ('Scheduler', 'Scheduler', None, 39),
    ('Menu', 'Menu', None, 40),
    ('Red', 'Red', None, 41),
    ('Green', 'Green', None, 42),
    ('Yellow', 'Yellow', None, 43),
    ('Blue', 'Blue', None, 44),
    ('Radio', 'Radio', None, 45),
    ('RecordList', 'RecordList', None, 46),
    ('Exit', 'Exit', None, 47),
)


from win32gui import FindWindow, SendMessageTimeout 
from win32con import SMTO_ABORTIFHUNG, SMTO_NORMAL
from pluginImport.Window.FindWindow import WindowMatcher

MyWindowMatcher = WindowMatcher("dvbdream.exe").Enumerate



class MyActionTemplate(eg.ActionClass):
    
    def __call__(self):
        try:
            hwnd = MyWindowMatcher()[0]
            return SendMessageTimeout(
                hwnd, 
                1347, 
                0, 
                self.value, 
                SMTO_ABORTIFHUNG|SMTO_NORMAL, 
                1000
            )[1]
        except:
            self.PrintError("DVB Dream not running")
    


def ScanListRecursive(theList, group):
    for parts in theList:
        if len(parts) == 3:
            # this is a new sub-group
            groupName, groupDescription, groupList = parts
            newGroup = group.AddGroup(groupName, groupDescription)
            ScanListRecursive(groupList, newGroup)
        elif len(parts) == 4:
            # this is a new action
            tmpClassName, tmpName, tmpDescription, tmpValue = parts
               
            class tmpAction(MyActionTemplate):
                name = tmpName
                description = tmpDescription
                value = tmpValue
                       
            tmpAction.__name__ = tmpClassName
            group.AddAction(tmpAction)
        else:
            raise Exception("Wrong number of fields in the list")



class DVBDream(eg.PluginClass):

    def __init__(self):
        ScanListRecursive(MyActionList, self)

