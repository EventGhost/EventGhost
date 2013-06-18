import wx
import eg
from eg.IconTools import GetIcon


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
        self.Bind(wx.EVT_TOOL_ENTER, self.OnEvent)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.curTool = -1
        self.lastClickedTool = None
        
        
    def OnSize(self, event):
        eg.whoami()
        event.Skip()
        
        
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
                func_wrapper = getattr(self.parent, "OnCmd" + name)
            else:
                def func_wrapper(event):
                    func()
            self.Bind(wx.EVT_TOOL, func_wrapper, id=id)
        setattr(self.buttons, name, obj)
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
        
        
    def OnEvent(self, event):
        self.curTool = event.GetSelection()
        event.Skip()
                
                
    def AddCheckButton(self, name):
        id = wx.NewId()
        image = GetIcon("images/" + name + ".png")
        func = getattr(self.parent, "OnCmd" + name)
        menuname = getattr(self.myStrings, name)
        self.AddCheckLabelTool(id, "", image, shortHelp=menuname)
        self.Bind(wx.EVT_TOOL, func, id=id)
        setattr(self.buttons, name, ToolBarButton(self, id))
        
        
    def OnLeftClick(self, event):
        eg.whoami()
        x, y = event.GetPosition()
        item = self.FindToolForPosition(x, y)
        if item:
            data = item.GetClientData()
            if hasattr(data, "downFunc"):
                data.downFunc(event)
        self.lastClickedTool = item
        event.Skip()
        
        
    def OnLeftUp(self, event):
        if self.lastClickedTool:
            obj = self.lastClickedTool.GetClientData()
            if hasattr(obj, "upFunc"):
                obj.upFunc(event)
        event.Skip()
                
                
