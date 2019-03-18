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
# This plugin is an HTTP client and Server that sends and receives MiCasaVerde UI5 and UI7 states.
# This plugin is based on the Vera plugins by Rick Naething, well kinda sorta, 

import wx

from ChoiceControls import *
from copy import deepcopy as dc

class GetConfig:

    def __init__(self):
        pass

    def __call__(self, plugin, category, **kwargs):
        VDL = plugin.VDL
        ID = VDL.GetID(**kwargs)
        try: ID = int(ID)
        except: pass

        data = dc(VDL.devices) if 'device' in kwargs else dc(VDL.scenes)
        res = {}
        NAME = None

        for i, itemdata in enumerate(data):
            if itemdata and itemdata['category'] == category:
                roomdata  = VDL.rooms[int(itemdata['room'])]
                try: sectdata  = VDL.sections[int(roomdata['section'])]
                except: sectdata  = VDL.sections[1]
                catename  = VDL.GetCategory(category)
                sectname  = sectdata['name']
                try: roomname  = roomdata['name']
                except: roomname = 'NO ROOM'
                itemname  = itemdata['name']
                event = [dc(itemdata['id']), '.'.join([sectname, roomname, itemname])]

                if ID == i: NAME = event[1]
                event[1] += '.'+catename

                try: res[sectname]
                except: res[sectname] = {}
                try:  res[sectname][roomname][itemname] = event
                except:  res[sectname][roomname] = {itemname: event}
        return NAME, dc(res)


class DeviceBox(wx.StaticBoxSizer):

    def __init__(self, parent, lbl):
        self.parent = parent
        deviceChoiceBox = wx.StaticBox(parent, -1, lbl)
        wx.StaticBoxSizer.__init__(self, deviceChoiceBox, wx.VERTICAL)

    def AddMany(self, items):
        self.name = None
        devicesizer = wx.BoxSizer(wx.HORIZONTAL)
        for item in items:
            if isinstance(item[0], str):
                box = wx.StaticBox(self.parent, -1, item[0])
                boxsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
                boxsizer.Add(*item[2])
                devicesizer.Add(boxsizer, *item[1])
            else:
                self.Add(*item)
        self.Add(devicesizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 5)


class DeviceConfigPanel(wx.Panel):

    name = None

    def __init__(self, plugin, parent):
        self.plugin = plugin.plugin
        self.parent = parent
        wx.Panel.__init__(self, parent)

    def AddItems(self, lbl, category, **kwargs):
        name, self.choices = GetConfig()(self.plugin, category, **kwargs)

        sect, room, device = [' ']*3 if name is None else name.split('.')
        sectkeys = sorted(self.choices.keys())
        roomkeys = sorted(self.choices[sect].keys()) if sect in sectkeys else []
        devicekeys = sorted(self.choices[sect][room].keys()) if roomkeys and room in roomkeys else []

        self.st1 = self.parent.StaticText('ID:\nEvent:')

        self.sections, self.rooms, self.devices = [Choice(self, *item) for item in [[sect, sectkeys], [room, roomkeys], [device, devicekeys]]]

        devicesizer = DeviceBox(self, lbl)
        self.SetSizer(devicesizer)
        devicesizer.AddMany([
                        (self.st1, 0, wx.ALIGN_LEFT|wx.LEFT, 25),
                        ("Sections (Hubs)", (0, wx.ALIGN_CENTER|wx.LEFT, 20), (self.sections, 0, wx.ALL, 5)),
                        ("Rooms", (0, wx.ALIGN_CENTER|wx.LEFT, 5), (self.rooms, 0, wx.ALL, 5)),
                        ("Devices", (0, wx.ALIGN_CENTER|wx.LEFT, 5), (self.devices, 0, wx.ALL, 5))
                        ])

        self.sections.Bind(wx.EVT_CHOICE, self.onSection)
        self.rooms.Bind(wx.EVT_CHOICE, self.onRoom)
        self.devices.Bind(wx.EVT_CHOICE, self.onDevice)

        if not self.devices.GetStringSelection(): wx.CallAfter(self.onSection)
        else: wx.CallAfter(self.updateDeviceDisplay)

    def updateDeviceDisplay(self, evt=None):
        d = self.devices.GetStringSelection()
        if d != '---NO DEVICES---':
            r = self.rooms.GetStringSelection()
            s = self.sections.GetStringSelection()
            item = self.choices[s][r][d]
            self.name = '.'.join(item[1].split('.')[:-1])
            self.st1.SetLabel('ID: '+str(item[0])+'\nEvent: '+item[1])
        else: self.st1.SetLabel('ID: '+'\nEvent: ')
        if evt: evt.Skip()

    def onDevice(self, evt):
        self.updateDeviceDisplay(evt)

    def onRoom(self, evt):
        s = self.sections.GetStringSelection()
        r = self.rooms.GetStringSelection()
        try: items = sorted(self.choices[s][r].keys())
        except: items = ['---NO DEVICES---']
        self.devices.Clear()
        self.devices.AppendItems(items=items)
        self.devices.SetSelection(0)
        self.onDevice(evt)

    def onSection(self, evt=None):
        s = self.sections.GetStringSelection()
        self.rooms.Clear()
        self.devices.Clear()
        try: items = sorted(self.choices[s].keys())
        except:
            self.sections.Clear()
            self.sections.AppendItems(items=['---NO SECTIONS---'])
            self.sections.SetSelection(0)
            items = ['---NO ROOMS---']
        self.rooms.AppendItems(items=items)
        self.rooms.SetSelection(0)
        self.onRoom(evt)

    def GetStringSelection(self):
        return self.name


class SceneConfigPanel:

    def __init__(self):
        pass
        
    def __call__(self, plugin, parent):
        return DeviceConfigPanel(plugin, parent)
