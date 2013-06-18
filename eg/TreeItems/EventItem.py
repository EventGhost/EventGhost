import eg
from TreeItem import TreeItem


        
class EventItem(TreeItem):
    xmlTag = "Event"
    iconIndex = eg.SetupIcons("event")
    
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        eg.RegisterEvent(self.name, self)
        
        
    def _Delete(self):
        eg.UnRegisterEvent(self.name, self)
        TreeItem._Delete(self)
        
        
    def RenameTo(self, newName):
        eg.UnRegisterEvent(self.name, self)
        TreeItem.RenameTo(self, newName)
        eg.RegisterEvent(newName, self)
        
        
    def DropTest(self, cls):
        if cls == EventItem:
            return 4 # 4 = item can be inserted before or after
        if cls == ActionItem:
            return 3 # 3 = item would move after
        return None # None = item cannot be dropped on it


