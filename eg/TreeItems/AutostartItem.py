import eg
from MacroItem import MacroItem

class AutostartItem(MacroItem):
    xmlTag = "Autostart"
    iconIndex = eg.SetupIcons("Execute")

    def __init__(self, parent, node):
        MacroItem.__init__(self, parent, node)
        self.name = eg.text.General.autostartItem
        self.document.autostartMacro = self
        
        
    def IsEditable(self):
        return False


    def CanCut(self):
        return False
    
    
    def CanCopy(self):
        return False
    
    
    def CanDelete(self):
        return False
    
    
    def UnloadPlugins(self):
        eg.whoami()
        for child in self.childs:
            if child.__class__ == self.document.PluginItem:
                if child.executable:
                    child.StopPlugin()
                    eg.ClosePlugin(child.executable)
    
    
    def DropTest(self, cls):
        if cls == FolderItem:
            return 3 # 3 = item would move after
        if cls == MacroItem:
            return 3 # 3 = item would move after
        if cls == ActionItem:
            return 1 # 1 = item would be dropped inside
        #if cls == PluginItem:
        #    return 1 # 1 = item would be dropped inside
        return None # None = item cannot be dropped on it

