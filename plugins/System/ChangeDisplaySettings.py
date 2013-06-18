import wx

import eg
from eg.WinAPI.Display import GetDisplays

gDisplays = GetDisplays()
            
            
class DisplayChoice(wx.Choice):
    
    def __init__(self, parent, id=-1, display=0):
        wx.Choice.__init__(self, parent, id)
        for i, display in enumerate(gDisplays):
            self.Append("%d: %s" % (i+1, display.DeviceString))
            self.SetClientData(i, display.DeviceName)
        self.SetSelection(0)
        
        
    def GetValue(self):
        pos = wx.Choice.GetSelection(self)
        return gDisplays[pos]
        


class ChangeDisplaySettings(eg.ActionClass):
    name = "Change Display Settings"
    iconFile = "Display"
    
    def __call__(
        self, 
        displayNum=None, 
        size=None, 
        frequency=None, 
        depth=None, 
        includeAll=False, 
        updateRegistry=False
    ):
        # CDS_UPDATEREGISTRY = 1
        flags = int(updateRegistry)
        gDisplays[displayNum - 1].SetDisplayMode(
            size, frequency, depth, flags)
    
    
    def GetLabel(
        self, 
        displayNum, 
        size, 
        frequency, 
        depth, 
        includeAll, 
        updateRegistry=False
    ):
        return "Set Display%d to mode %dx%d@%d Hz" % (
            displayNum, size[0], size[1], frequency)
        
        
    def Configure(
        self, 
        displayNum=None, 
        size=None,
        frequency=None, 
        depth=None, 
        includeAll=False, 
        updateRegistry=False
    ):
        dialog = eg.ConfigurationDialog(self)                            
        if displayNum is None:
            displayNum = 1
            size, frequency, depth = gDisplays[0].GetCurrentMode()
            
        displayChoice = DisplayChoice(dialog)
        if displayNum is not None and displayNum <= displayChoice.GetCount():
            displayChoice.SetSelection(displayNum - 1)
            
        resolutionChoice = wx.Choice(dialog)
        frequencyChoice = wx.Choice(dialog)
        depthChoice = wx.Choice(dialog)
        includeAllCheckBox = wx.CheckBox(dialog, -1, 
            "Include modes this monitor might not support.")
        includeAllCheckBox.SetValue(includeAll)
        updateRegistryCheckBox = wx.CheckBox(dialog, -1, 
            "Store mode in the registry.")
        updateRegistryCheckBox.SetValue(updateRegistry)
        
        st1 = wx.StaticText(dialog, -1, "Display:")
        st2 = wx.StaticText(dialog, -1, "Resolution:")
        st3 = wx.StaticText(dialog, -1, "Frequency:")
        st4 = wx.StaticText(dialog, -1, "Colour Depth:")
        
        sizer = wx.GridBagSizer(5, 5)
        Add = sizer.Add
        Add(st1, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        Add(displayChoice, (0, 1), (1, 1))
        Add(st2, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        Add(resolutionChoice, (1, 1), (1, 1))
        Add(st3, (2, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        Add(frequencyChoice, (2, 1), (1, 1))
        Add(st4, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        Add(depthChoice, (3, 1), (1, 1))
        dialog.sizer.Add(sizer)
        dialog.sizer.Add(includeAllCheckBox, 0, wx.TOP, 10)
        dialog.sizer.Add(updateRegistryCheckBox, 0, wx.TOP, 10)
        
        settings = eg.Bunch()
        
        def GetClientData(ctrl):
            return ctrl.GetClientData(ctrl.GetSelection())
        
        def UpdateResolutions(event=None):
            eg.whoami()
            display = displayChoice.GetValue()
            modes = display.GetDisplayModes(includeAllCheckBox.GetValue())
            settings.modes = modes
            resolutions = modes.keys()
            resolutions.sort()
            resolutionChoice.Clear()
            sel = 0
            for pos, res in enumerate(resolutions):
                resolutionChoice.Append("%d x %d" % res)
                resolutionChoice.SetClientData(pos, res)
                if res == size:
                    sel = pos
            resolutionChoice.Select(sel)
            UpdateDeepth(None)
                
        def UpdateDeepth(event=None):
            eg.whoami()
            resolution = GetClientData(resolutionChoice)
            settings.depthDict = depthDict = settings.modes[resolution]
            depthList = depthDict.keys()
            depthList.sort()
            depthChoice.Clear()
            sel = len(depthList) - 1
            for pos, bits in enumerate(depthList):
                depthChoice.Append("%d Bits" % bits)
                depthChoice.SetClientData(pos, bits)
                if bits == depth:
                    sel = pos
            depthChoice.Select(sel)
            UpdateFrequencies()
        
        def UpdateFrequencies(event=None):
            eg.whoami()
            depth = GetClientData(depthChoice)
            frequencyList = settings.depthDict[depth]
            frequencyChoice.Clear()
            sel = 0
            for pos, f in enumerate(frequencyList):
                frequencyChoice.Append("%d Hz" % f)
                frequencyChoice.SetClientData(pos, f)
                if f == frequency:
                    sel = pos
            frequencyChoice.Select(sel)

        displayChoice.Bind(wx.EVT_CHOICE, UpdateResolutions)
        resolutionChoice.Bind(wx.EVT_CHOICE, UpdateDeepth)
        depthChoice.Bind(wx.EVT_CHOICE, UpdateFrequencies)
        includeAllCheckBox.Bind(wx.EVT_CHECKBOX, UpdateResolutions)
        
        UpdateResolutions()
        
        if dialog.AffirmedShowModal():
            return (
                displayChoice.GetSelection() + 1,
                GetClientData(resolutionChoice),
                GetClientData(frequencyChoice),
                GetClientData(depthChoice),
                includeAllCheckBox.GetValue(),
                updateRegistryCheckBox.GetValue()
            )
