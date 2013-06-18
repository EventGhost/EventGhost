import eg
from ContainerItem import ContainerItem


class FolderItem(ContainerItem):
    xmlTag = "Folder"
    iconIndex = eg.SetupIcons("folder")

    def DropTest(self, cls):
        if cls == MacroItem:
            return 5 # item can be inserted before or after or dropped inside
        if cls == FolderItem:
            return 5 # item can be inserted before or after or dropped inside
        return None # item cannot be dropped on it

    
