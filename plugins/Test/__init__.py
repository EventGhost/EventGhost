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
# $LastChangedDate: 2008-12-03 22:59:02 +0100 (Mi, 03 Dez 2008) $
# $LastChangedRevision: 614 $
# $LastChangedBy: bitmonster $

import eg

eg.RegisterPlugin(
    name="Test",
    description=(
        "This plugin does nothing useful for end-users. It's purpose is to"
        "show developers some tricks in EventGhost"
    ),
)

import wx


class Test(eg.PluginClass):
    
    def __init__(self):
        pass
        
    
    def Configure(self, password=eg.Bunch(data="")):
        panel = eg.ConfigPanel()
        passwordCtrl = panel.TextCtrl(password.data, style=wx.TE_PASSWORD)
        panel.sizer.Add(passwordCtrl)
        while panel.Affirmed():
            value = eg.Bunch(data=passwordCtrl.GetValue())
            panel.SetResult(value)
            
            