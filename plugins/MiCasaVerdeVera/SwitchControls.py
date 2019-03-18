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

import eg
import wx
from TextControls import *
from ConfigControls import *
from ChoiceControls import *



class Switch(eg.ActionBase):

    text = Text

    def __call__(self, device, switch):
        device = self.plugin.VDL.GetID(device=device)
        if device:
            try: switch = str(int(switch))
            except: switch = '1' if switch == 'On' else '0'

            self.plugin.SERVER.send(device=device, switch=switch)
        
    def Configure(self, device=" ", switch="Off"):
        
        text = self.text.Switch
        panel = eg.ConfigPanel()
        deviceCtrl = DeviceConfigPanel(self, panel)
        switchCtrl = Choice(panel, switch, text.Choice)
        switchBox = panel.BoxedGroup(text.SwitchBox, (text.SwitchText, switchCtrl))

        deviceCtrl.AddItems(self.text.Vera.DeviceBox, '3', device=device)
        panel.sizer.AddMany([(deviceCtrl, 0, wx.EXPAND), (switchBox, 0, wx.EXPAND)])

        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetStringSelection(), switchCtrl.GetStringSelection())

class Toggle(eg.ActionBase):

    text = Text

    def __call__(self, device):

        device = self.plugin.VDL.GetID(device=device)
        if device: self.plugin.SERVER.send(toggle=device)

    def Configure(self, device=" "):
        
        text = self.text.Toggle
        panel = eg.ConfigPanel()
        deviceCtrl = DeviceConfigPanel(self, panel)
    
        deviceCtrl.AddItems(self.text.Vera.DeviceBox, '3', device=device)
        panel.sizer.Add(deviceCtrl, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetStringSelection())