import eg
import wx
import types

class ConfigPanel(wx.PyPanel):
    
    def __init__(self, executable):
        dialog = eg.ConfigurationDialog(executable)
        self.dialog = dialog
        #notebook = wx.Notebook(dialog)
        wx.PyPanel.__init__(self, dialog, -1)
        #notebook.AddPage(self, "Options")
        self.lines = []
        dialog.sizer.Add(self, 1, wx.EXPAND)
        self.sizerProps = (6, 5)
        self.rowFlags = {}
        self.colFlags = {}
        
        
    def SetSizerProperty(self, vgap=6, hgap=5):
        self.sizerProps = (vgap, hgap)
    
    
    def SetRowFlags(self, rowNum, flags):
        self.rowFlags[rowNum] = flags
        
    
    def SetColumnFlags(self, colNum, flags):
        self.colFlags[colNum] = flags
        
    
    def Affirmed(self):
        if self.lines:
            self.AddGrid(self.lines, *self.sizerProps)
        return self.dialog.AffirmedShowModal()
    
    
    def AddLine(self, *items, **kwargs):
        growable = kwargs.get("growable", False)
        self.lines.append((items, growable))


    def AddGrid(self, grid, vgap=6, hgap=5):
        columns = len(max(grid))
        sizer = wx.GridBagSizer(vgap, hgap)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        RowFlagsGet = self.rowFlags.get
        ColFlagsGet = self.colFlags.get
        for rowNum, (row, growable) in enumerate(grid):
            if growable:
                sizer.AddGrowableRow(rowNum)
            for colNum, ctrl in enumerate(row):
                if ctrl is None:
                    ctrl = (1, 1)
                elif type(ctrl) in types.StringTypes:
                    ctrl = wx.StaticText(self, -1, ctrl)
                
                flags = RowFlagsGet(rowNum, 0) | ColFlagsGet(colNum, 0)
                flags |= (wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                sizer.Add(ctrl, (rowNum, colNum), (1, 1), flags)
                
            if colNum < columns - 1:
                sizer.SetItemSpan(ctrl, (1, columns - colNum + 1))
        self.SetSizer(sizer)
        
        
        
    def SpinIntCtrl(self, value=0, *args, **kwargs):
        return eg.SpinIntCtrl(self, -1, value, *args, **kwargs)
    
    
    def SpinNumCtrl(self, value=0, *args, **kwargs):
        return eg.SpinNumCtrl(self, -1, value, *args, **kwargs)
    
    
    def TextCtrl(self, value="", *args, **kwargs):
        return wx.TextCtrl(self, -1, value, *args, **kwargs)
    
    
    def Choice(self, value=0, *args, **kwargs):
        return eg.Choice(self, value, *args, **kwargs)
    
    
    def DisplayChoice(self, value=0, *args, **kwargs):
        return eg.DisplayChoice(self, value, *args, **kwargs)
    
    
    def ColourSelectButton(self, value=(255, 255, 255), *args, **kwargs):
        return eg.ColourSelectButton(self, value, *args, **kwargs)
    
    
    def FontSelectButton(self, value=None, *args, **kwargs):
        fontCtrl = eg.FontSelectButton(self)
        fontCtrl.SetValue(value)
        return fontCtrl
    
    
    def CheckBox(self, value=0, label="", *args, **kwargs):
        checkBox = wx.CheckBox(self, -1, label, *args, **kwargs)
        checkBox.SetValue(value)
        return checkBox
    
    
    def RadioBox(self, value=0, label="", *args, **kwargs):
        radioBox = eg.RadioBox(self, -1, label, *args, **kwargs)
        radioBox.SetValue(value)
        return radioBox
    
    
    def Button(self, label="", *args, **kwargs):
        return wx.Button(self, -1, label, *args, **kwargs)
    
    
    def DirBrowseButton(self, value, *args, **kwargs):
        dirpathCtrl = eg.DirBrowseButton(
            self,
            size=(320,-1),
            startDirectory=value, 
            labelText="",
            buttonText=eg.text.General.browse
        )
        dirpathCtrl.SetValue(value)
        return dirpathCtrl
    
    
    def SerialPortChoice(self, value=0, *args, **kwargs):
        kwargs['value'] = value
        return eg.SerialPortChoice(self, *args, **kwargs)
    
    
    def MacroSelectButton(self, *args, **kwargs):
        return eg.MacroSelectButton(self, *args, **kwargs)
    

        