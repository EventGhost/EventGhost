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
# This plugin is based on the Vera plugins by Rick Naething, well kinda sorta, gave me inspiration at the least.
# This plugin is currently being tested by the members of the EventGhost Forum, m19brandon, blaher, kgschlosser (the artist that is K)
# WinoOutWest, loveleejohn, kkl... I thank these people for being the first to tell me the errors which I am hoping are solved,
# but if not you know where to find me.


import eg

from TextControls import *
from MenuControls import *
from HVACControls import *
from SceneControls import *
from AlarmControls import *
from ChoiceControls import *
from ConfigControls import *
from DimmerControls import *
from SwitchControls import *
from ServerControls import *
from DeviceControls import *
from DoorLockControls import *
from PluginConfigControls import *


eg.RegisterPlugin(
    name = "MiCasaVerde Vera UI5 UI6 UI7",
    description = "Control of the MiCasaVerde Vera UI5 UI6 UI7",
    author = "K",
    version = "4.3b",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    kind = "external",
    guid = '{321D9F7C-6961-4C62-B6E0-86C950A25279}',
    icon= (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAQCAYAAAB3AH1ZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAA"
        "A7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAAJaSURBVEhL5ZNbiIxhGMe/8xwNw7BNs1NryipJ29"
        "RO0V6QNqE2yqF1yq5DO7usZbNklLiQGxkXbC4lbpQLFw6L4oKUKIcLN5Jib9QKUUrx+898o7nB52KkPPXrOb7v87zv937Gvy4uOFX"
        "z70nMsqwS3DdN6ybcNk3zDv52chqoseJ53iya9UEvjUehjL0WRkhPqVY1WGi2X7iu2+Y4znx/iHV+uqHi0mgXeoaxo7DF6G8frDDQ"
        "vpK7mUOul5yHXgOHoIif0kLsblQTuodbbEUP++y0bXuRSjKZjHRE9T8VTnsBLtH4qDFQ+FZha34zsedsdgB9A63mG7FHWfIGUvjj+"
        "NfhWCQSacbfA3vhILEnqs3lcpOptdXnV9IKX+xsotPoL7zj9I/ZZBuxcU7SyUbPKlW+4D8i34eeIL/YD0vMRCIxNZ1Op0Kh0ELyHx"
        "Wrpn4jFJ+BMZqXjJ62VdivaFKE9aQ/4T+sgf+e+DD2BO+lQ+vRBfyncA/uqg6+krKUDyLN8Nme5C1l8yHsF+BywuVs9DIWizXVQ84"
        "h/mMA7Mus2ydboj/rTwfQJsfhAeZbNttQjRpxeE38CH9IHubpwSlBrH6Ac3BNOZiNrRv9QCr4AMg0Fp2HU9j1D6eFWBmuwhjDXVEQ"
        "+ywDza1U8CjxT8ItuMjNdUGZeLA3EI1G8/F4fDqmGmtqLczV7HA4nE0mk1nfr6HaKLkFrNWvWYvPVE5/BjrYABR3cXWDDDLCqQ7zn"
        "buJreA1n4AlNOlQDbpEzSa0OE2uRTnWLlOMmiL2EHo17GbrYAP8R2IY3wGjEGZSjHVwLgAAAABJRU5ErkJggg=="
        )
    
)

import wx
import time
from copy import deepcopy as dc

class Vera(eg.PluginBase):

    text = Text
    
    def __init__(self):
        self.rampingdimmers = {}
        self.upspeed = 0.1
        self.VDL = VDL(self, STATIC)
        self.SERVER = SERVER(self, STATIC)
        self.UPDATEMENU = UPDATEMENU(self, STATIC)
        self.VERAMENU = VERAMENU(self, STATIC)

        self.AddAction(Switch)
        self.AddAction(Toggle)
        self.AddAction(Dimmer)
        self.AddAction(Scene)
        self.AddAction(HVAC)
        self.AddAction(Alarm)
        self.AddAction(DimmerStatus)
        self.AddAction(RampDimmer)
        self.AddAction(DoorLock)
        self.AddAction(DisplayMenu)

    def __start__(self, host, port, prefix, upSpeed, addons=[]):

        self.prefix = prefix
        self.upspeed = upSpeed
        self.info.eventPrefix = prefix
        self.URL = 'http://'+host+':'+str(port)+'/data_request?id='

        self.VDL.start()
        self.SERVER.start()
       
    def __close__(self):
        self.StopLightRamping()
        self.SERVER.EVENT.set()
        self.UPDATEMENU.EVENT.set()
        self.VERAMENU.EVENT.set()

    def __stop__(self):
        self.StopLightRamping()
        self.SERVER.EVENT.set()
        self.UPDATEMENU.EVENT.set()
        self.VERAMENU.EVENT.set()
        self.SERVER = SERVER(self, STATIC)
        self.SERVER.EVENT.clear()

    def StopLightRamping(self, device=None):
        def stopramp(key):
            t = self.rampingdimmers.pop(key)
            t.EVENT.set()

        for key in self.rampingdimmers.keys():
            if key == device: return stopramp(key)
            if device == None: stopramp(key)

    def AddLightRamping(self, device, t):

        self.StopLightRamping(device)
        self.rampingdimmers[device] = t
        t.start()

    def Configure(self, host="127.0.0.1", port=3480, prefix='MiCasaVerdeVera', upSpeed=0.10, addons=[]):

        text = self.text.Vera
        panel = eg.ConfigPanel()
        self.PluginConfig = PluginConfig(self, panel, host, port, prefix, upSpeed, addons)

        panel.sizer.Add(self.PluginConfig, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(*self.PluginConfig.GetValues())