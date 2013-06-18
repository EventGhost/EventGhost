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
        #self.myItems.append(tmp)   
        wx.Menu.AppendItem(self, tmp)
        tmp.Enable(enabled)
        if func is not None:
            wx.EVT_MENU(self.parent, tmp.id, func)
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
        #menuhotkey = getattr(self.myStrings, name + "HotKey", "")
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
    
    def __init__(self, parent, name, func, kind, hotkey=""):
        id = wx.NewId()
        if hotkey:
            name += " \t" + hotkey
        wx.MenuItem.__init__(self, parent, id, name, "", kind)
        self.id = id
        self.func = func
        self.parent = parent
        self.hotkey = hotkey


    def SetText(self, name):
        if self.hotkey:
            name += " \t" + self.hotkey
        wx.MenuItem.SetText(self, name)
        
        
    def Enable(self, enable = True):
        self.parent.Enable(self.id, enable)
        
        
        
