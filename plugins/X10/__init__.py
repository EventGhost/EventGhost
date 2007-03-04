#
# plugins/X10/__init__.py
#
# Copyright (C) 2005 Lars-Peter Voss
#
# This file is part of EventGhost.
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

import eg

class PluginInfo(eg.PluginInfo):
    name = "X10 Remote"
    author = "Bitmonster"
    version = "1.0.0"
    kind = "remote"
    description = (
        'Hardware plugin for X10 compatible RF remotes.'
        '}n\nThis includes remotes like:<br>'
        '<ul>'
        '<li><a href="http://www.ati.com/products/remotewonder/index.html">'
        'ATI Remote Wonder</a></li>'
        '<li><a href="http://www.snapstream.com/">'
        'SnapStream Firefly</a></li>'
        '<li><a href="http://www.nvidia.com/object/feature_PC_remote.html">'
        'NVIDIA Personal Cinema Remote</a></li>'
        '<li><a href="http://www.marmitek.com/">'
        'Marmitek PC Control</a></li>'
        '<li><a href="http://www.pearl.de/product.jsp?pdid=PE4444&catid=1601">'
        'Pearl Q-Sonic Master Remote 6in1</a></li>'
        '<li><a href="http://www.niveusmedia.com/support/PCremote.htm">'
        'Niveus PC Remote Control</a></li>'
        '<li>Medion RF Remote Control</li>'
        '</ul>'
    )
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
        "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
        "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
        "YII="
    )

import threading
import win32event

import wx

from X10com import X10Control


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
        }            ],
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
        #eg.whoami()
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
        
        
        
class X10(eg.PluginClass):
    text = Text
    canMultiLoad = True
    
    def __start__(self, remoteType=None, ids=None, prefix=None):
        self.remoteType = remoteType
        self.ids = ids
        self.info.eventPrefix = prefix
        self.mappingTable = gRemotes[remoteType][1]
        self.errorState = 0
        startupEvent = threading.Event()
        self.stopEvent = win32event.CreateEvent(None, 0, 0, None)
        self.thread = threading.Thread(
            target=self.WorkerThread, 
            args=(startupEvent, self.stopEvent)
        )
        self.thread.start()
        startupEvent.wait(10.0)
        if self.errorState:
            raise eg.Exception(self.text.errorMesg)
        

    def __stop__(self):
        win32event.SetEvent(self.stopEvent)
        self.thread.join(10.0)
            
            
    def WorkerThread(self, startupEvent, stopEvent):
        from win32event import MsgWaitForMultipleObjects, QS_ALLINPUT, WAIT_OBJECT_0
        from win32com.client import DispatchWithEvents
        from pythoncom import CoInitialize, CoUninitialize, PumpWaitingMessages        
        
        CoInitialize()
        try:
            comInstance = DispatchWithEvents(X10Control(), X10Events)
        except:
            self.errorState = 1
            CoUninitialize()
            return
        finally:
            startupEvent.set()
        comInstance.plugin = self
        pHandles = [self.stopEvent]
        while 1:
            # We can't simply give a timeout of 30 seconds, as
            # we may continouusly be recieving other input messages,
            # and therefore never expire.
            rc = MsgWaitForMultipleObjects(
                    pHandles, # list of objects
                    0, # wait all
                    500,  # timeout
                    QS_ALLINPUT, # type of input
                    #win32event.QS_ALLEVENTS, # type of input
                    )
            if rc == WAIT_OBJECT_0:
                # Event signaled.
                break
            elif rc == WAIT_OBJECT_0+1:
                # Message waiting.
                PumpWaitingMessages()
            
        comInstance.Close()
        CoUninitialize()
        del comInstance
    
    
    def Configure(self, remoteType=2, ids=None, prefix="X10"):
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        fbtypes = []
        selection = 0
        for i, id in enumerate(gRemotesOrder):
            fbtypes.append(gRemotes[id][0])
            if id == remoteType:
                selection = i
        choice = wx.Choice(dialog, -1, choices=fbtypes)
        choice.SetSelection(selection)
        
        editCtrl = wx.TextCtrl(dialog, -1, prefix)
        
        btnsizer = wx.FlexGridSizer(4, 4)
        idBtns = []
        for i in xrange(16):
            btn = wx.ToggleButton(dialog, -1, size=(35, 35), label=str(i + 1))
            if (ids is None) or ((i+1) in ids):
                btn.SetValue(True)
            btnsizer.Add(btn)
            idBtns.append(btn)
            
        def OnSelectAll(event):
            for item in idBtns:
                item.SetValue(True)
    
        selectAllBtn = wx.Button(
            dialog, -1, text.allButton, style=wx.BU_EXACTFIT
        )
        selectAllBtn.Bind(wx.EVT_BUTTON, OnSelectAll)
        
        def OnSelectNone(event):
            for item in idBtns:
                item.SetValue(False)
            
        selectNoneBtn = wx.Button(
            dialog, -1, text.noneButton, style=wx.BU_EXACTFIT
        )
        selectNoneBtn.Bind(wx.EVT_BUTTON, OnSelectNone)

        rightBtnSizer = wx.BoxSizer(wx.VERTICAL)
        rightBtnSizer.Add(selectAllBtn, 0, wx.EXPAND)
        rightBtnSizer.Add((5,5), 1)
        rightBtnSizer.Add(selectNoneBtn, 0, wx.EXPAND)
            
        idSizer = wx.BoxSizer(wx.HORIZONTAL)
        idSizer.Add(btnsizer)
        idSizer.Add((10, 10), 0)
        idSizer.Add(rightBtnSizer, 0, wx.EXPAND)
        
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(wx.StaticText(dialog, -1, text.remoteBox), 0, wx.BOTTOM, 2)
        leftSizer.Add(choice, 0, wx.BOTTOM, 10)
        leftSizer.Add(wx.StaticText(dialog, -1, text.usePrefix), 0, wx.BOTTOM, 2)
        leftSizer.Add(editCtrl)
        
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(wx.StaticText(dialog, -1, text.idBox), 0, wx.BOTTOM, 2)
        rightSizer.Add(idSizer)
        
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer)
        mainSizer.Add((0,0), 1, wx.EXPAND)
        mainSizer.Add(wx.StaticLine(dialog, style=wx.LI_VERTICAL), 0, wx.EXPAND)
        mainSizer.Add((0,0), 1, wx.EXPAND)
        mainSizer.Add(rightSizer)
        mainSizer.Add((0,0), 1, wx.EXPAND)
        
        dialog.sizer.Add(mainSizer, 1, wx.EXPAND)
        
        if dialog.AffirmedShowModal():
            return (
                gRemotesOrder[choice.GetSelection()], 
                [i+1 for i, button in enumerate(idBtns) if button.GetValue()], 
                editCtrl.GetValue()
            )

