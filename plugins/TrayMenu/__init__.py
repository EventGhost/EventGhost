import eg

class PluginInfo(eg.PluginInfo):
    name = "Tray Menu"
    
import wx
import wx.gizmos

MENU_DATA = [
    ("Test1", "item", "TestEvent1"),
    ("Test2", "item", "TestEvent2"),
    ("Test3", "item", "TestEvent3"),
    ("Test4", "item", "TestEvent4"),
]

class TrayMenu(eg.PluginClass):
    
    def __init__(self):
        self.menuItems = {}
        self.menuIds = {}
    
    
    def __start__(self, menuData=None):
        menuData = MENU_DATA
        menu =  eg.app.trayMenu
        self.menuItems[menu.PrependSeparator()] = None
        for name, kind, data in reversed(menuData):
            if kind == "item":
                id = wx.NewId()
                item = menu.Prepend(id, name)
                wx.EVT_MENU(menu, id, self.OnMenuItem)
                self.menuIds[id] = data
        
        
    def __stop__(self):
        for menuItem in self.menuItems:
            eg.app.trayMenu.RemoveItem(menuItem)
        self.menuItems.clear()
        self.menuIds.clear()
        
        
    @eg.LogIt
    def OnMenuItem(self, event):
        data = self.menuIds[event.GetId()]
        self.TriggerEvent(data)
        
    
    def Configure(self, menuData=MENU_DATA):
        dialog = eg.ConfigurationDialog(self)
        tree = wx.gizmos.TreeListCtrl(
            dialog, 
            -1,
            style = 
                  wx.TR_FULL_ROW_HIGHLIGHT
                | wx.TR_DEFAULT_STYLE
                #| wx.TR_COLUMN_LINES
                | wx.TR_NO_LINES 
                #| wx.TR_ROW_LINES
                | wx.TR_HIDE_ROOT
                
        )
        tree.AddColumn("Label")
        tree.AddColumn("Event")
        id = tree.AddRoot("Tray Menu")
        for name, kind, data in menuData:
            if kind == "item":
                item = tree.AppendItem(id, name)
                tree.SetItemText(item, str(data), 1)
        dialog.sizer.Add(tree, 1, wx.EXPAND)
        if dialog.AffirmedShowModal():
            return (None,)
    
    
        