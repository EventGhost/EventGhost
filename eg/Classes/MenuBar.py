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
# $LastChangedDate: 2007-03-18 13:14:34 +0100 (So, 18 Mrz 2007) $
# $LastChangedRevision: 81 $
# $LastChangedBy: bitmonster $

import wx
import eg


class MenuBar(wx.MenuBar):
    
    def __init__(self, parent, stringMappingObj=None):
        wx.MenuBar.__init__(self)
        self.parent = parent
        parent.SetMenuBar(self)
        self.menus = []
        self.stringMappingObj = stringMappingObj
        
        
    def AddMenu(self, name=None):
        fullname = getattr(self.stringMappingObj, name + "Menu", name)
        menu = eg.Menu(self.parent, fullname, self.stringMappingObj)
        self.menus.append(menu)
        setattr(self, name, menu)
        return menu
    
    
    def Realize(self):
        for menu in self.menus:
            wx.MenuBar.Append(self, menu, menu.mytitle)


