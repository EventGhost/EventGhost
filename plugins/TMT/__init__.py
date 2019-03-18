# -*- coding: utf-8 -*-

version = "0.1"

import eg

eg.RegisterPlugin(
    name="TMT",
    guid='{F87C5C92-6EAE-4ED5-9D4D-49723BF19781}',
    author="Buyukbang",
    version=version,
    kind="program",
    description=(
        'Controls TotalMedia Theater 5'
    ),
    createMacrosOnAdd=True,
)

from win32gui import PostMessage

FindTMT = eg.WindowMatcher(u'uTotalMediaTheatre{*}.exe', None, None, None, None, 1, False, 0.0, 0)


class wmAction(eg.ActionClass):

    def __call__(self):
        hwnds = FindTMT()
        if len(hwnds) != 0:
            PostMessage(hwnds[0], 0x8D52, self.value, 0)
            print self.value
        else:
            self.PrintError("Error")
            return


class hotKeys(eg.ActionClass):

    def __call__(self):
        hwnds = FindTMT()
        if len(hwnds) != 0:
            eg.SendKeys(hwnds[0], self.value, False)
        else:
            self.PrintError("Error")
            return


ACTIONS = (
    (hotKeys, 'Esc', 'Normal Window', 'In full screen mode, it will resume playing in normal window mode.', u'{Esc}'),
    (hotKeys, 'Pause/Play', 'Pause/Play', 'Pause/Play', u'{Space}'),
    (hotKeys, 'Stop', 'Stop', 'Stop', u'{O}'),
    (hotKeys, 'Resume', 'Resume', 'Resume', u'{Ctrl+Enter}'),
    (hotKeys, 'Forward', 'Forward', 'Play forward', u'{F}'),
    (hotKeys, 'Rewind', 'Rewind', 'Play backward', u'{R}'),
    (hotKeys, 'Previous', 'Previous Chapter', 'Previous Chapter', u'{PgUp}'),
    (hotKeys, 'Next', 'Next Chapter', 'Next Chapter', u'{PgDown}'),
    (hotKeys, 'Exit', 'Exit', 'Exit', u'{Ctrl+X}'),
    (hotKeys, 'Open', 'Open', 'Open the Select Source menu', u'{Ctrl+O}'),
    (hotKeys, 'Eject', 'Eject/Insert Disc', 'Eject/Insert disc', u'{E}'),
    (hotKeys, 'Settings', 'Settings Dialog', 'Open Settings dialog', u'{Ctrl+S}'),
    (hotKeys, 'Mute', 'Mute', 'Mute On/Off', u'{Q}'),
    (hotKeys, 'VolumeUp', 'Volume Up', 'Increase volume', u'{Shift+Up}'),
    (hotKeys, 'VolumeDown', 'Volume Down', 'Decrease volume', u'{Shift+Down}'),
    (hotKeys, 'SubPanel', 'Hide/Show SubPanel', 'Show/Hide Sub Control Panel', u'{Ctrl+F}'),
    (hotKeys, 'FullScreen', 'Toggle Full Screen', 'Full screen/Normal window', u'{Z}'),
    (hotKeys, 'Help', 'Help', 'Help', u'{F1}'),
    (hotKeys, 'Information', 'Information', 'Information', u'{I}'),
    (hotKeys, 'Bookmark', 'Add Bookmark', 'Add bookmark', u'{K}'),
    (hotKeys, 'Capture', 'Capture Picture', 'Capture picture', u'{P}'),
    (hotKeys, 'ABRepeat', 'A-B Repeat', 'A-B repeat', u'{Ctrl + R}'),
    (hotKeys, 'TitleMenu', 'Title Menu', 'Title Menu', u'{Ctrl+T}'),
    (hotKeys, 'Popup', 'Popup Menu', 'Popup Menu', u'{Ctrl+U}'),
    (hotKeys, 'Angle', 'Change Angle', 'Change Angle', u'{G}'),
    (hotKeys, 'Audio', 'Change Audio', 'Change (Primary) Audio Stream', u'{L}'),
    (hotKeys, 'Subtitle', 'Change Subtitle', 'Change Subtitle', u'{S}'),
    (hotKeys, 'DiscMenu', 'Disc Menu', 'Disc Menu', u'{Ctrl+M}'),
    (hotKeys, 'Num0', 'Number 0', '0', u'{0}'),
    (hotKeys, 'Num1', 'Number 1', '1', u'{1}'),
    (hotKeys, 'Num2', 'Number 2', '2', u'{2}'),
    (hotKeys, 'Num3', 'Number 3', '3', u'{3}'),
    (hotKeys, 'Num4', 'Number 4', '4', u'{4}'),
    (hotKeys, 'Num5', 'Number 5', '5', u'{5}'),
    (hotKeys, 'Num6', 'Number 6', '6', u'{6}'),
    (hotKeys, 'Num7', 'Number 7', '7', u'{7}'),
    (hotKeys, 'Num8', 'Number 8', '8', u'{8}'),
    (hotKeys, 'Num9', 'Number 9', '9', u'{9}'),
    (hotKeys, 'Red', 'Red', 'Red key', u'{F9}'),
    (hotKeys, 'Green', 'Green', 'Green key', u'{F10}'),
    (hotKeys, 'Yellow', 'Yellow', 'Yellow key', u'{F11}'),
    (hotKeys, 'Blue', 'Blue', 'Blue key', u'{F12}'),
    (hotKeys, 'Select', 'Select', 'Select', u'{Enter}'),
    (hotKeys, 'RightMenu', 'Open Right-Click Menu', 'Right Click Menu', u'{Ctrl+D}'),
    (hotKeys, 'Up', 'Up', 'Up', u'{Up}'),
    (hotKeys, 'Down', 'Down', 'Down', u'{Down}'),
    (hotKeys, 'Left', 'Left', 'Left', u'{Left}'),
    (hotKeys, 'Right', 'Right', 'Right', u'{Right}'),
)


class TMT(eg.PluginClass):
    def __init__(self):
        self.AddActionsFromList(ACTIONS)
