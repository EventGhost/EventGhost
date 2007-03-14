class TreePosition:
    """ 
    Object to find the position of an item inside the tree.
    
    This class is mainly used by the Undo/Redo handlers to find the
    right position of an item. Because previous Undo/Redo handlers
    might have deleted/restored an item or any of its parents, they can't 
    use any direct item reference, but must use an "index path" to find 
    the right object.
    """
    
    def __init__(self, item):
        self.root = item.root
        parent = item.parent
        if parent is None:
            self.GetItem = self.GetRootItem
            return
        self.path = parent.GetPath()
        pos = parent.childs.index(item)
        if pos + 1 >= len(parent.childs):
            pos = -1
        self.pos = pos
        
        
    def GetRootItem(self):
        return self.root
    
    
    def GetItem(self):
        """
        Returns the item this TreePosition is pointing to.
        """
        searchParent = self.root
        for parentPos in self.path:
            searchParent = searchParent.childs[parentPos]
        return searchParent.childs[self.pos]
        
        
    def GetPosition(self):
        """
        Return the parent item and the index inside the parents childs. 
        
        If the item is the last in the parents childs it will return -1 as 
        index.
        """
        searchParent = self.root
        for parentPos in self.path:
            searchParent = searchParent.childs[parentPos]
        return searchParent, self.pos
        
        
        
