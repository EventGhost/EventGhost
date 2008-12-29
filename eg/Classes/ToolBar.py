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
import wx


GetIcon = eg.Icons.GetIcon
#GetIcon = wx.Bitmap

class ToolBarButton:
    
    def __init__(self, toolbar, id):
        self.toolbar = toolbar
        self.id = id        
        
        
    def Enable(self, flag=True):
        self.toolbar.EnableTool(self.id, flag)
        
        
    def Toggle(self, flag=True):
        self.toolbar.ToggleTool(self.id, flag)
        
        
    def Check(self, flag=True):
        self.toolbar.ToggleTool(self.id, flag)
        
        
    def SetText(self, text):
        self.toolbar.SetToolShortHelp(self.id, text)
        
        

class ToolBar(wx.ToolBar):
    
    def __init__(self, *args, **kwargs):
        wx.ToolBar.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.lastClickedTool = None
        

    def SetParams(self, parent, stringMappingObj):
        self.parent = parent
        self.myStrings = stringMappingObj
        self.buttons = eg.Bunch()
        
        
    def AddButton(self, name=None, image=None, func=None, downFunc=None, upFunc=None):
        if name is None:
            return self.AddSeparator()
        id = wx.NewId()
        obj = ToolBarButton(self, id)
        if image is None:
            image = GetIcon("images/" + name + ".png")
        menuname = getattr(self.myStrings, name)
        toolBarBase = self.AddSimpleTool(id, image, menuname)
        toolBarBase.SetClientData(obj)
        if upFunc:
            obj.upFunc = upFunc
            obj.downFunc = downFunc
        else:
            if func is None:
                func = getattr(self.parent, "OnCmd" + name)
            
            def FuncWrapper(event):
                func()
            self.Bind(wx.EVT_TOOL, FuncWrapper, id=id)
        ident = name[0].lower() + name[1:]
        setattr(self.buttons, ident, obj)
        return obj
        
        
    def AddTextButton(self, name=None):
        id = wx.NewId()
        func = getattr(self.parent, "OnCmd" + name)
        menuname = getattr(self.myStrings, name)
        button = wx.Button(self, id, menuname, style=wx.NO_BORDER)
        self.AddControl(button)
        button.Bind(wx.EVT_BUTTON, func)
        obj = ToolBarButton(self, id)
        setattr(self.buttons, name, obj)
        return obj
        
        
    def AddCheckButton(self, name):
        id = wx.NewId()
        image = GetIcon("images/" + name + ".png")
        func = getattr(self.parent, "OnCmd" + name)
        menuname = getattr(self.myStrings, name)
        self.AddCheckLabelTool(id, None, image, shortHelp=menuname)
        self.Bind(wx.EVT_TOOL, func, id=id)
        setattr(self.buttons, name, ToolBarButton(self, id))
        
        
    @eg.LogIt
    def OnLeftDown(self, event):
        """
        Handles the wx.EVT_LEFT_DOWN events.
        """
        x, y = event.GetPosition()
        item = self.FindToolForPosition(x, y)
        if item:
            data = item.GetClientData()
            if hasattr(data, "downFunc"):
                data.downFunc(event)
        self.lastClickedTool = item
        event.Skip()
        
        
    def OnLeftUp(self, event):
        """
        Handles the wx.EVT_LEFT_UP events.
        """
        if self.lastClickedTool:
            obj = self.lastClickedTool.GetClientData()
            if hasattr(obj, "upFunc"):
                obj.upFunc(event)
        event.Skip()
                
                
    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
        
        
                
