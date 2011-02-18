#
# plugins/DVBDream/__init__.py
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

eg.RegisterPlugin(
    name = "DVB Dream",
    author = "townkat",
    version = "4.1" + "$LastChangedRevision$".split()[1],
    kind = "program",
    url = "http://www.eventghost.net/forum/viewtopic.php?t=612",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control '
        '<a href="http://www.dvbdream.org">DVB Dream</a>.'
        '\n\n<p>'
        'Tested with DVB Dream 1.4d<p>'
        'In DVB Dream Select:<br>'
        'Options->Remote->RemoteControlType->Native'
    ),
)

# changelog
# 4.1 by bitmonster 
#     - changed code to use PluginClass.AddActionsFromList

    
ACTIONS = (
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
    ('ChUp', 'Channel Up', None, 13),
    ('ChDn', 'Channel Down', None, 14),
    ('VolumeUp', 'Volume Up', None, 16),
    ('VolumeDn', 'Volume Down', None, 15),
    ('Ok', 'Ok', None, 17),
    ('Record', 'Record', None, 18),
    ('Recall', 'Recall', None, 19),
    ('Fullscreen', 'Fullscreen', None, 20),
    ('Teletext', 'Teletext', None, 21),
    ('EPG', 'EPG', None, 22),
    ('Tab', 'Tab', None, 23),
    ('Info', 'Info', None, 24),
    ('Optional1', 'Optional 1', None, 25),
    ('Optional2', 'Optional 2', None, 26),
    ('Optional3', 'Optional 3', None, 27),
    ('Optional4', 'Optional 4', None, 28),
    ('Optional5', 'Optional 5', None, 29),
    ('Optional6', 'Optional 6', None, 30),
    ('Optional7', 'Optional 7', None, 31),
    ('Optional8', 'Optional 8', None, 32),
    ('Optional9', 'Optional 9', None, 33),
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
    ('RecordList', 'Record List', None, 46),
    ('Exit', 'Exit', None, 47),
)


from eg.WinApi import SendMessageTimeout

MyWindowMatcher = eg.WindowMatcher(
    u'dvbdream.exe', None, u'Tfmain', None, None, None, True, 0.0, 0
) 

class MyActionTemplate(eg.ActionClass):
    
    def __call__(self):
        hwnds = MyWindowMatcher()
        if len(hwnds) == 0:
            raise self.Exceptions.ProgramNotRunning
        try:
    	    for hwnd in hwnds:           
            	SendMessageTimeout(hwnd, 1347, 0, self.value)	
        except:
            raise self.Exceptions.ProgramNotRunning
    


class DVBDream(eg.PluginClass):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, MyActionTemplate)

