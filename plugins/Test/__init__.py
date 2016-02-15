# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#
# $LastChangedDate: 2010-01-04 18:53:33 +0100 (po, 04 1 2010) $
# $LastChangedRevision: 1338 $
# $LastChangedBy: Bitmonster $

import eg

eg.RegisterPlugin(
    name="Test",
    guid="{5533428D-57AB-4DAE-BA11-BB039DE0C4AA}",
    description=(
        "This plugin does nothing useful for end-users. It's purpose is to"
        "show developers some tricks in EventGhost"
    ),
)

import wx



class Test(eg.PluginBase):
    
    def __init__(self):
        self.AddAction(TestAction)
        
    
    def __start__(self, password=""):
        print "__start__", password
        
    
    def Configure(self, password=""):
        panel = eg.ConfigPanel()
        passwordCtrl = panel.PasswordCtrl(password)
        panel.sizer.Add(passwordCtrl)
        while panel.Affirmed():
            panel.SetResult(passwordCtrl.GetValue())
            
            
            
class TestAction(eg.ActionBase):
    
    def __call__(self, password):
        print repr(unicode(password))
        
        
    def Configure(self, password=""):
        panel = eg.ConfigPanel()
        passwordCtrl = panel.PasswordCtrl(password)
        panel.sizer.Add(passwordCtrl)
        while panel.Affirmed():
            panel.SetResult(passwordCtrl.GetValue())
            