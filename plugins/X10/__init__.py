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
Hardware plugin for X10 compatible RF remotes.

This includes remotes like:

* `ATI Remote Wonder
  <http://www.ati.com/products/remotewonder/index.html>`_
* `ATI Remote Wonder PLUS
  <http://www.ati.com/products/remotewonderplus/index.html>`_
* `SnapStream Firefly
  <http://www.snapstream.com/products/firefly/>`_
* `NVIDIA Personal Cinema Remote
  <http://www.nvidia.com/object/feature_PC_remote.html>`_
* `Marmitek PC Control
  <http://www.marmitek.com/>`_
* `Pearl Q-Sonic Master Remote 6in1
  <http://www.pearl.de/product.jsp?pdid=PE4444&catid=1601&vid=916&curr=DEM>`_
* `Niveus PC Remote Control
  <http://www.niveusmedia.com/>`_
* Medion RF Remote Control
* Packard Bell RF MCE Remote Control OR32E
"""

import eg

eg.RegisterPlugin(
    name = "X10 Remote",
    author = "Bitmonster",
    version = "1.0",
    kind = "remote",
    hardwareId = "USB\\VID_0BC7&PID_0006",
    guid = "{C3E96757-E507-4CC3-A2E6-465D48B87D09}",
    canMultiLoad = True,
    description = __doc__,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=1589",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
        "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
        "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
        "YII="
    ),
)

import wx
from win32com.client import DispatchWithEvents

class Text:
    allButton = "&All"
    noneButton = "&None"
    remoteBox = "Remote type:"
    idBox = "Active IDs:"
    usePrefix = "Event prefix:"
    errorMesg = "No X10 receiver found!"


REMOTES = [
    [
        "ATI Remote Wonder",
        {
            'One': 'Num1',
            'Two': 'Num2',
            'Three': 'Num3',
            'Four': 'Num4',
            'Five': 'Num5',
            'Six': 'Num6',
            'Seven': 'Num7',
            'Eight': 'Num8',
            'Nine': 'Num9',
            'Zero': 'Num0',
            'MouseUp': 'Mouse000',
            'MouseRightUp': 'Mouse045',
            'MouseRight': 'Mouse090',
            'MouseRightDown': 'Mouse135',
            'MouseDown': 'Mouse180',
            'MouseLeftDown': 'Mouse225',
            'MouseLeft': 'Mouse270',
            'MouseLeftUp': 'Mouse315',
            'MTAddDelete': 'Menu',
            'MTAB': 'Check',
        }
    ],
    [
        "Medion",
        {
            'MTTV': 'TV',
            'MTVCR': 'VCR',
            'Book': 'Music',
            'MTRadio': 'Radio',
            'Web': 'Photo',
            'MTPC': 'TVPreview',
            'MTChannelList': 'ChannelList',
            'D': 'Setup',
            'MTAlbum': 'VideoDesktop',
            'VolumeUp': 'VolumeDown',
            'VolumeDown': 'VolumeUp',
            'A': 'Mute',
            'MTArtist': 'Red',
            'MTGenre': 'Green',
            'MTTrack': 'Yellow',
            'MTUp': 'Blue',
            'MTAddDelete': 'TXT',
            'One': 'Num1',
            'Two': 'Num2',
            'Three': 'Num3',
            'Four': 'Num4',
            'Five': 'Num5',
            'Six': 'Num6',
            'Seven': 'Num7',
            'Eight': 'Num8',
            'Nine': 'Num9',
            'Zero': 'Num0',
            'Bookmark': 'ChannelSearch',
            'Resize': 'Delete',
            'MTLeft': 'Rename',
            'MTAB': 'Snapshot',
            'MTDown': 'AcquireImage',
            'MTRight': 'EditImage',
            'E': 'PreviousTrack',
            'F': 'NextTrack',
            'C': 'DVDMenu',
            'MTPlaylist': 'DVDAudio',
            'MTEnter': 'Fullscreen',
        }
    ],
    [
        "Generic X10",
        {
            'One': 'Num1',
            'Two': 'Num2',
            'Three': 'Num3',
            'Four': 'Num4',
            'Five': 'Num5',
            'Six': 'Num6',
            'Seven': 'Num7',
            'Eight': 'Num8',
            'Nine': 'Num9',
            'Zero': 'Num0',
        }
    ],
    [
        "SnapStream FireFly",
        {
            'One': 'Num1',
            'Two': 'Num2',
            'Three': 'Num3',
            'Four': 'Num4',
            'Five': 'Num5',
            'Six': 'Num6',
            'Seven': 'Num7',
            'Eight': 'Num8',
            'Nine': 'Num9',
            'Zero': 'Num0',
            'MTTV': 'Maximize',
            'Power': 'Close',
            'MTAddDelete': 'Back',
            'MTAB': 'Enter',
            'VolumeDown': 'VolumeUp',
            'VolumeUp': 'VolumeDown',
            'A': 'FireFly',
            'MTRadio': 'Info',
            'MTPC': 'Option',
            'Bookmark': 'Menu',
            'Resize': 'Exit',
            'Input': 'PreviousTrack',
            'Zoom': 'NextTrack',
            'Book': 'Music',
            'Web': 'Photo',
            'Hand': 'Video',
            'B': 'Help',
            'MTVCR': 'Mouse',
            'C': 'A',
            'D': 'B',
            'E': 'C',
            'F': 'D',
        }
    ],
]


REMOTES_SORT_ORDER = [2, 0, 1, 3]

REMOTE_IDS = {
    192: 1,
    208: 2,
    224: 3,
    240: 4,
    32: 5,
    48: 6,
    0: 7,
    16: 8,
    64: 9,
    80: 10,
    96: 11,
    112: 12,
    160: 13,
    176: 14,
    128: 15,
    144: 16,
}


class X10Events:
    plugin = None

    #@eg.LogIt
    def OnX10Command(
        self,
        bszCommand,
        eCommand,
        lAddress,
        eKeyState,
        lSequence,
        eCommandType,
        varTimestamp
    ):
        if eKeyState == 3:
            return
        plugin = self.plugin
        remoteId = REMOTE_IDS[lAddress & 0xF0]
        if remoteId not in plugin.ids:
            return
        event = str(bszCommand)
        if eKeyState == 1:
            plugin.TriggerEnduringEvent(plugin.mappingTable.get(event, event))
        elif eKeyState == 2:
            plugin.EndLastEvent()



class X10ThreadWorker(eg.ThreadWorker):
    comInstance = None
    plugin = None
    eventHandler = None

    def Setup(self, plugin, eventHandler):
        self.plugin = plugin
        self.eventHandler = eventHandler
        self.comInstance = DispatchWithEvents(
            'X10net.X10Control.1',
            eventHandler
        )


    def Finish(self):
        if self.comInstance:
            self.comInstance.Close()
            del self.comInstance



class X10(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddEvents()


    def __start__(self, remoteType=None, ids=None, prefix=None):
        self.remoteType = remoteType
        self.ids = ids
        self.info.eventPrefix = prefix
        self.mappingTable = REMOTES[remoteType][1]

        class SubX10Events(X10Events):
            plugin = self
        self.workerThread = X10ThreadWorker(self, SubX10Events)
        try:
            self.workerThread.Start(20)
        except:
            raise self.Exception(self.text.errorMesg)


    def __stop__(self):
        self.workerThread.Stop(10)


    def GetLabel(self, remoteType, *dummyArgs):
        return "X10: " + REMOTES[remoteType][0]


    def Configure(self, remoteType=2, ids=None, prefix="X10"):
        panel = eg.ConfigPanel()
        text = self.text
        fbtypes = []
        selection = 0
        for i, remoteId in enumerate(REMOTES_SORT_ORDER):
            fbtypes.append(REMOTES[remoteId][0])
            if remoteId == remoteType:
                selection = i
        remoteTypeCtrl = panel.Choice(selection, fbtypes)
        prefixCtrl = panel.TextCtrl(prefix)

        btnsizer = wx.FlexGridSizer(4, 4)
        idBtns = []
        for i in xrange(16):
            btn = wx.ToggleButton(panel, -1, size=(35, 35), label=str(i + 1))
            if (ids is None) or ((i+1) in ids):
                btn.SetValue(True)
            btnsizer.Add(btn)
            idBtns.append(btn)

        selectAllButton = panel.Button(text.allButton, style=wx.BU_EXACTFIT)
        def OnSelectAll(event):
            for item in idBtns:
                item.SetValue(True)
            event.Skip()
        selectAllButton.Bind(wx.EVT_BUTTON, OnSelectAll)

        selectNoneButton = panel.Button(text.noneButton, style=wx.BU_EXACTFIT)
        def OnSelectNone(event):
            for item in idBtns:
                item.SetValue(False)
            event.Skip()
        selectNoneButton.Bind(wx.EVT_BUTTON, OnSelectNone)

        rightBtnSizer = eg.VBoxSizer(
            (selectAllButton, 0, wx.EXPAND),
            ((5, 5), 1),
            (selectNoneButton, 0, wx.EXPAND),
        )
        idSizer = eg.HBoxSizer(
            (btnsizer),
            ((10, 10), 0),
            (rightBtnSizer, 0, wx.EXPAND),
        )
        leftSizer = eg.VBoxSizer(
            (panel.StaticText(text.remoteBox), 0, wx.BOTTOM, 2),
            (remoteTypeCtrl, 0, wx.BOTTOM, 10),
            (panel.StaticText(text.usePrefix), 0, wx.BOTTOM, 2),
            (prefixCtrl),
        )
        rightSizer = eg.VBoxSizer(
            (panel.StaticText(text.idBox), 0, wx.BOTTOM, 2),
            (idSizer),
        )
        mainSizer = eg.HBoxSizer(
            (leftSizer),
            ((0, 0), 1, wx.EXPAND),
            (wx.StaticLine(panel, style=wx.LI_VERTICAL), 0, wx.EXPAND),
            ((0, 0), 1, wx.EXPAND),
            (rightSizer),
            ((0, 0), 1, wx.EXPAND),
        )
        panel.sizer.Add(mainSizer, 1, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                REMOTES_SORT_ORDER[remoteTypeCtrl.GetValue()],
                [i+1 for i, button in enumerate(idBtns) if button.GetValue()],
                prefixCtrl.GetValue()
            )

