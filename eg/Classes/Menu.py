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


class Menu(wx.Menu):
    
    def __init__(self, parent, mytitle = "", myStrings=None):
        wx.Menu.__init__(self)
        self.mytitle = mytitle
        self.myStrings = myStrings
        self.parent = parent
        
        
    def Append(
        self, 
        name, 
        func = None, 
        hotkey = "", 
        kind = wx.ITEM_NORMAL, 
        image = None
    ):
        tmp = MenuItem(self, name, func, kind, hotkey)
        if image is not None:
            tmp.SetBitmap(image)
        wx.Menu.AppendItem(self, tmp)
        return tmp


    def AddItem(
        self, 
        name = None, 
        kind = wx.ITEM_NORMAL, 
        image = None,
        hotkey = "",
        func = None
    ):
        if name is None:
            return self.AppendSeparator()
        if func is None:
            FuncWrapper = getattr(self.parent, "OnCmd" + name)
        else:
            def FuncWrapper(event):
                func()

        menuname = getattr(self.myStrings, name, name)
        menuitem = self.Append(
            menuname, 
            FuncWrapper, 
            hotkey, 
            kind, 
            image
        )
        ident = name[0].lower() + name[1:]
        setattr(self, ident, menuitem)
        return menuitem
    
    

class MenuItem(wx.MenuItem):
    
    def __init__(self, parentMenu, name, func, kind, hotkey=None):
        id = wx.NewId()
        if hotkey:
            name += " \t" + hotkey
        wx.MenuItem.__init__(self, parentMenu, id, name, "", kind)
        self.func = func
        self.hotkey = hotkey
        if func is not None:
            wx.EVT_MENU(parentMenu.parent, id, func)


    def SetText(self, name):
        if self.hotkey:
            name += " \t" + self.hotkey
        wx.MenuItem.SetText(self, name)
        return self
        
    
    def Check(self, check=True):
        wx.MenuItem.Check(self, check)
        return self
        
    
    def Enable(self, enable=True):
        wx.MenuItem.Enable(self, enable)
        return self
        
        
        
