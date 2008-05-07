import types

class BoxedGroup(wx.StaticBoxSizer):
    
    def __init__(self, parent, label="", *items):
        staticBox = wx.StaticBox(parent, -1, label)
        sizer = wx.StaticBoxSizer.__init__(self, staticBox, wx.VERTICAL)
        self.items = []
        for item in items:
            lineSizer = wx.BoxSizer(wx.HORIZONTAL)
            if isinstance(item, types.StringTypes):
                labelCtrl = wx.StaticText(parent, -1, item)
                lineSizer.Add(labelCtrl, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
                self.items.append([labelCtrl])
            elif isinstance(item, (types.ListType, types.TupleType)):
                lineItems = []
                for subitem in item:
                    if isinstance(subitem, types.StringTypes):
                        subitem = wx.StaticText(parent, -1, subitem)
                        lineSizer.Add(subitem, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
                    else:
                        lineSizer.Add(subitem, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
                    lineItems.append(subitem)
                self.items.append(lineItems)
            else:
                lineSizer.Add(item, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
                self.items.append([item])
            self.Add(lineSizer, 0, wx.EXPAND)
                      
                        
    def GetColumnItems(self, colNum):
        return [row[colNum] for row in self.items if len(row) > colNum]
    
    
    def AppendItem(self):
        pass