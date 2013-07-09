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

def CreateStringAction(myParameterDescription, myDefaultParameter):
    class AnAction(eg.ActionWithStringParameter):
        parameterDescription = myParameterDescription
        defaultParameter = myDefaultParameter
        
        def __call__(self, value):
            print "action value:", self.value
            print "user value:", value
            
    return AnAction

ACTIONS = (
    (CreateStringAction("Please enter value A:", "default A"), "ActionA", "My A action", "This does something", "A"),
    (CreateStringAction("Please enter value B:", "default B"), "ActionB", "My B action", "This does something", "B"),
)

class Test(eg.PluginBase):
    
    def __init__(self):
        self.AddAction(TestAction)
        self.AddActionsFromList(ACTIONS)
        
    
#    def __start__(self, password):
#        print "__start__", password.Get()
#        
#    
#    def Configure(self, password=None):
#        password = eg.Password(password)
#        panel = eg.ConfigPanel()
#        passwordCtrl = panel.TextCtrl(password.Get(), style=wx.TE_PASSWORD)
#        panel.sizer.Add(passwordCtrl)
#        while panel.Affirmed():
#            password.Set(passwordCtrl.GetValue())
#            panel.SetResult(password)
            
            
            
class TestAction(eg.ActionBase):
    
    def __call__(self, password):
        print password.Get()
        
        
    def Configure(self, password=None):
        password = eg.Password(password)
        panel = eg.ConfigPanel()
        passwordCtrl = panel.TextCtrl(password.Get(), style=wx.TE_PASSWORD)
        panel.sizer.Add(passwordCtrl)
        while panel.Affirmed():
            password.Set(passwordCtrl.GetValue())
            panel.SetResult(password)
            