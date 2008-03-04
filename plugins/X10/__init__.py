# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$


eg.RegisterPlugin(
    name = "X10 Remote",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    canMultiLoad = True,
    description = 'Hardware plugin for X10 compatible RF remotes.',
    help = u"""
        This includes remotes like:
        <ul>
        <li><a href="http://www.ati.com/products/remotewonder/index.html">
        ATI Remote Wonder\u2122</a></li>
        <li><a href="http://www.ati.com/products/remotewonderplus/index.html">
        ATI Remote Wonder\u2122 PLUS</a></li>
        <li><a href="http://www.snapstream.com/">
        SnapStream Firefly</a></li>
        <li><a href="http://www.nvidia.com/object/feature_PC_remote.html">
        NVIDIA Personal Cinema Remote</a></li>
        <li><a href="http://www.marmitek.com/">
        Marmitek PC Control</a></li>
        <li><a href="http://www.pearl.de/product.jsp?pdid=PE4444&catid=1601">
        Pearl Q-Sonic Master Remote 6in1</a></li>
        <li><a href="http://www.niveusmedia.com/support/PCremote.htm">
        Niveus PC Remote Control</a></li>
        <li>Medion RF Remote Control</li>
        </ul>
    """,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
        "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
        "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
        "YII="
    ),
)


from win32com.client import DispatchWithEvents

class Text:
    allButton = "&All"
    noneButton = "&None"
    remoteBox = "Remote type:"
    idBox = "Active IDs:"
    usePrefix = "Event prefix:"
    errorMesg = "No X10 receiver found!"    


gRemotes = [
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


gRemotesOrder = [2,0,1,3]


class X10Events:
    
    def OnX10Command(
        self, 
        bszCommand, 
        eCommand, 
        lAddress, 
        EKeyState,
        lSequence, 
        eCommandType, 
        varTimestamp
    ):
        if EKeyState == 3:
            return
        plugin = self.plugin
        id = (lAddress >> 4) + 1
        if id not in plugin.ids:
            return
        event = str(bszCommand)
        if EKeyState == 1:
            plugin.TriggerEnduringEvent(plugin.mappingTable.get(event, event))
        elif EKeyState == 2:
            plugin.EndLastEvent()
        
    @eg.LogIt
    def __getattr__(self, name):
        "Create event handler methods on demand"
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def handler(*args):
            print args
            return 0

        return handler
        
        
class X10WorkerThread(eg.ThreadWorker):
    comInstance = None
    
    def Setup(self, plugin, eventHandler):
        self.plugin = plugin
        self.eventHandler = eventHandler
        self.comInstance = DispatchWithEvents('X10net.X10Control.1', eventHandler)

        
    def Finish(self):
        if self.comInstance:
            self.comInstance.Close()
            del self.comInstance
        
        
        
class X10(eg.PluginClass):
    text = Text
    
    def __start__(self, remoteType=None, ids=None, prefix=None):
        self.remoteType = remoteType
        self.ids = ids
        self.info.eventPrefix = prefix
        self.mappingTable = gRemotes[remoteType][1]
        
        class SubX10Events(X10Events):
            plugin = self
        self.workerThread = X10WorkerThread(self, SubX10Events)
        try:
            self.workerThread.Start()
        except:
            raise self.Exception(self.text.errorMesg)
        

    def SetArguments(self, remoteType=2, ids=None, prefix=None):
        eventList = [(name, None) for name in gRemotes[remoteType][1].values()]
        eventList.sort()
        self.RegisterEvents(eventList)
        
        
    def __stop__(self):
        self.workerThread.Stop()
            
            
    def GetLabel(self, remoteType=None, ids=None, prefix=None):
        return "X10: " + gRemotes[remoteType][0]
        
        
    def Configure(self, remoteType=2, ids=None, prefix="X10"):
        panel = eg.ConfigPanel(self)
        text = self.text
        fbtypes = []
        selection = 0
        for i, id in enumerate(gRemotesOrder):
            fbtypes.append(gRemotes[id][0])
            if id == remoteType:
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
            ((5,5), 1),
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
            ((0,0), 1, wx.EXPAND),
            (wx.StaticLine(panel, style=wx.LI_VERTICAL), 0, wx.EXPAND),
            ((0,0), 1, wx.EXPAND),
            (rightSizer),
            ((0,0), 1, wx.EXPAND),
        )
        panel.sizer.Add(mainSizer, 1, wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(
                gRemotesOrder[remoteTypeCtrl.GetValue()], 
                [i+1 for i, button in enumerate(idBtns) if button.GetValue()], 
                prefixCtrl.GetValue()
            )


