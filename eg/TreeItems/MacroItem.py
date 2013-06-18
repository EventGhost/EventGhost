import wx
import eg
from ContainerItem import ContainerItem


class MacroItem(ContainerItem):
    xmlTag = "Macro"
    iconIndex = eg.SetupIcons("macro")
    canExecute = True    
    

    def GetNextChild(self, index):
        index += 1
        if len(self.childs) > index:
            return self.childs[index], index
        else:
            return None
        
        
    def Execute(self):
        if self.isEnabled:
            del eg.lastFoundWindows[:]
            if self.shouldSelectOnExecute:
                wx.CallAfter(self.Select)
                
            if self.childs:
                eg.SetProgramCounter((self.childs[0], 0))
            else:
                eg.SetProgramCounter(None)


    def DropTest(self, cls):
        if cls == EventItem:
            return 1 # 1 = item would be dropped inside
        if cls == MacroItem:
            return 4 # 4 = item can be inserted before or after
        if cls == FolderItem:
            return 4 # 4 = item can be inserted before or after
        if cls == ActionItem:
            return 1 # 1 = item would be dropped inside
        return None  # None = item cannot be dropped on it
