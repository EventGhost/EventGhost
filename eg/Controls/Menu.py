# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import wx


class MenuBar(wx.MenuBar):
    
    def __init__(self, parent, stringMappingObj=None):
        wx.MenuBar.__init__(self)
        self.parent = parent
        parent.SetMenuBar(self)
        self.menus = []
        self.stringMappingObj = stringMappingObj
        
        
    def AddMenu(self, name=None):
        fullname = getattr(self.stringMappingObj, name + "Menu", name)
        menu = Menu(self.parent, fullname, self.stringMappingObj)
        self.menus.append(menu)
        setattr(self, name, menu)
        return menu
    
    
    def Realize(self):
        for menu in self.menus:
            wx.MenuBar.Append(self, menu, menu.mytitle)



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
        enabled = True, 
        kind = wx.ITEM_NORMAL, 
        image = None
    ):
        tmp = MenuItem(self, name, func, kind, hotkey)
        if image is not None:
            tmp.SetBitmap(image)
        wx.Menu.AppendItem(self, tmp)
        tmp.Enable(enabled)
        return tmp


    def AddItem(
        self, 
        name=None, 
        enabled=True, 
        kind=wx.ITEM_NORMAL, 
        image=None,
        hotkey = "",
        func = None
    ):
        if name is None:
            return wx.Menu.AppendSeparator(self)
        if func is None:
            func_wrapper = getattr(self.parent, "OnCmd" + name)
        else:
            def func_wrapper(event):
                func()

        menuname = getattr(self.myStrings, name, name)
        menuitem = self.Append(
            menuname, 
            func_wrapper, 
            hotkey, 
            enabled, 
            kind, 
            image
        )
        setattr(self, name, menuitem)
        return menuitem
    
    
    def AddCheckItem(self, name, enabled=True, checked=False, image=None):
        item = self.AddItem(name, enabled, wx.ITEM_CHECK, image)
        item.Check(checked)
        return item
    
    
    def AddSeparator(self):
        wx.Menu.AppendSeparator(self)



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
        
        
        
        
        
