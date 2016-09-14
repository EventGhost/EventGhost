# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import wx

# Local imports
import eg
from eg.WinApi.Display import GetDisplay, GetDisplays

class ChangeDisplaySettings(eg.ActionBase):
    name = "Change Display Settings"
    description = "Changes display settings."
    iconFile = "icons/Display"

    class text:
        label = "Set Display%d to mode %dx%d@%d Hz"
        display = "Display:"
        resolution = "Resolution:"
        frequency = "Frequency:"
        colourDepth = "Colour Depth:"
        includeAll = "Include modes this monitor might not support."
        storeInRegistry = "Store mode in the registry."

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
        GetDisplay(displayNum - 1).SetDisplayMode(
            size, frequency, depth, flags
        )

    def Configure(
        self,
        displayNum=None,
        size=None,
        frequency=None,
        depth=None,
        includeAll=False,
        updateRegistry=False
    ):
        text = self.text
        panel = eg.ConfigPanel()
        if displayNum is None:
            displayNum = 1
            size, frequency, depth = GetDisplay(0).GetCurrentMode()

        displayChoice = DisplayChoice(panel)
        if displayNum is not None and displayNum <= displayChoice.GetCount():
            displayChoice.SetSelection(displayNum - 1)

        resolutionChoice = wx.Choice(panel)
        frequencyChoice = wx.Choice(panel)
        depthChoice = wx.Choice(panel)
        includeAllCheckBox = panel.CheckBox(includeAll, text.includeAll)
        updateRegistryCheckBox = panel.CheckBox(
            updateRegistry, text.storeInRegistry
        )

        sizer = wx.GridBagSizer(6, 5)
        flag = wx.ALIGN_CENTER_VERTICAL
        sizer.Add(panel.StaticText(text.display), (0, 0), flag=flag)
        sizer.Add(panel.StaticText(text.resolution), (1, 0), flag=flag)
        sizer.Add(panel.StaticText(text.frequency), (2, 0), flag=flag)
        sizer.Add(panel.StaticText(text.colourDepth), (3, 0), flag=flag)
        sizer.Add(displayChoice, (0, 1), flag=flag)
        sizer.Add(resolutionChoice, (1, 1), flag=flag)
        sizer.Add(frequencyChoice, (2, 1), flag=flag)
        sizer.Add(depthChoice, (3, 1), flag=flag)

        panel.sizer.Add(sizer, 0, wx.EXPAND)
        flag = wx.ALIGN_CENTER_VERTICAL | wx.TOP
        panel.sizer.Add(includeAllCheckBox, 0, flag, 10)
        panel.sizer.Add(updateRegistryCheckBox, 0, flag, 10)

        settings = eg.Bunch()

        def GetClientData(ctrl):
            return ctrl.GetClientData(ctrl.GetSelection())

        def UpdateDeepth(event=None):
            resolution = GetClientData(resolutionChoice)
            settings.depthDict = depthDict = settings.modes[resolution]
            depthList = depthDict.keys()
            depthList.sort()
            depthChoice.Clear()
            sel = len(depthList) - 1
            for pos, bits in enumerate(depthList):
                depthChoice.Append("%d Bit" % bits)
                depthChoice.SetClientData(pos, bits)
                if bits == depth:
                    sel = pos
            depthChoice.Select(sel)
            UpdateFrequencies()
            if event:
                event.Skip()

        def UpdateFrequencies(event=None):
            depth = GetClientData(depthChoice)
            frequencyList = settings.depthDict[depth]
            frequencyChoice.Clear()
            sel = 0
            for pos, frequency in enumerate(frequencyList):
                frequencyChoice.Append("%d Hz" % frequency)
                frequencyChoice.SetClientData(pos, frequency)
                if frequency == frequency:
                    sel = pos
            frequencyChoice.Select(sel)
            if event:
                event.Skip()

        def UpdateResolutions(event=None):
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
            if event:
                event.Skip()

        displayChoice.Bind(wx.EVT_CHOICE, UpdateResolutions)
        resolutionChoice.Bind(wx.EVT_CHOICE, UpdateDeepth)
        depthChoice.Bind(wx.EVT_CHOICE, UpdateFrequencies)
        includeAllCheckBox.Bind(wx.EVT_CHECKBOX, UpdateResolutions)

        UpdateResolutions()

        while panel.Affirmed():
            panel.SetResult(
                displayChoice.GetSelection() + 1,
                GetClientData(resolutionChoice),
                GetClientData(frequencyChoice),
                GetClientData(depthChoice),
                includeAllCheckBox.GetValue(),
                updateRegistryCheckBox.GetValue()
            )

    def GetLabel(
        self,
        displayNum,
        size,
        frequency,
        depth,
        includeAll,
        updateRegistry=False
    ):
        return self.text.label % (displayNum, size[0], size[1], frequency)


class DisplayChoice(wx.Choice):
    def __init__(self, parent, id=-1, display=0):
        self.displays = GetDisplays()
        wx.Choice.__init__(self, parent, id)
        for i, display in enumerate(self.displays):
            self.Append("%d: %s" % (i + 1, display.deviceString))
            self.SetClientData(i, display.deviceName)
        self.SetSelection(0)

    def GetValue(self):
        pos = wx.Choice.GetSelection(self)
        return self.displays[pos]
