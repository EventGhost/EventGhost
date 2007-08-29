# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2007-07-25 05:07:21 +0200 (Mi, 25 Jul 2007) $
# $LastChangedRevision: 187 $
# $LastChangedBy: bitmonster $

import eg

eg.RegisterPlugin(
    name = "Desktop Remote",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision: 187 $".split()[1],
    canMultiLoad = True,
    description = (
        "Creates a remote-like desktop window."
    ),
)


import wx
import wx.lib.buttons as buttons
import os
from base64 import b64decode, b64encode
from cStringIO import StringIO

DEFAULT_FONT_SIZE = 9
DEFAULT_SIZE = (40, 40)


class Options(object):
    def __init__(self, parent):
        self._parent = parent
        
    def __getattribute__(self, name):
        if name == "_parent":
            return self.__dict__._parent
        
            
        
class DesktopRemote(eg.PluginClass):
    
    def __init__(self):
        self.AddAction(CreateNew)
        self.AddAction(AddButton)
        self.AddAction(StartNewLine)
        self.AddAction(Show)
        self.data = []
        self.lastEvent = None
        self.defaults = {
            "fontInfo": None,
            "image": None,
        }
        self.frame = None


    def OnButtonUp(self, event):
        event.Skip()
        self.lastEvent.SetShouldEnd()
    
    


class CreateNew(eg.ActionClass):
    name = "Create New Remote"
    
    def __call__(
        self, 
        width=40, 
        height=40, 
        rowGap=3, 
        columnGap=3, 
        borderSize=4,
        windowColour=(108, 108, 108),
        foregroundColour=(255, 255, 255),
        backgroundColour=(78, 78, 78),
        fontInfo=None,
    ):
        self.plugin.data = []
        self.plugin.defaults["width"] = width
        self.plugin.defaults["height"] = height
        self.plugin.defaults["foregroundColour"] = foregroundColour
        self.plugin.defaults["backgroundColour"] = backgroundColour
        self.plugin.defaults["fontInfo"] = fontInfo
        self.plugin.rowGap = rowGap
        self.plugin.columnGap = columnGap
        self.plugin.borderSize = borderSize
        self.plugin.windowColour = windowColour

    
    def GetLabel(self, *args):
        return self.name
    
    
    def Configure(
        self, 
        width=40, 
        height=40, 
        rowGap=3, 
        columnGap=3, 
        borderSize=4,
        windowColour=(108, 108, 108),
        foregroundColour=(255, 255, 255),
        backgroundColour=(78, 78, 78),
        fontInfo=None,
    ):
        dialog = eg.ConfigurationDialog(self)
        widthCtrl = eg.SpinIntCtrl(dialog, value=width, min=0)
        heightCtrl = eg.SpinIntCtrl(dialog, value=height, min=0)
        rowGapCtrl = eg.SpinIntCtrl(dialog, value=rowGap, min=0)
        columnGapCtrl = eg.SpinIntCtrl(dialog, value=columnGap, min=0)
        borderSizeCtrl = eg.SpinIntCtrl(dialog, value=borderSize, min=0)
        windowColourCtrl = eg.ColourSelectButton(dialog, label="Choose Colour", colour=windowColour)
        foregroundColourCtrl = eg.ColourSelectButton(dialog, label="Choose Colour", colour=foregroundColour)
        backgroundColourCtrl = eg.ColourSelectButton(dialog, label="Choose Colour", colour=backgroundColour)

        fontCtrl = eg.FontButton(dialog, label="Choose Font")
        fontCtrl.SetValue(fontInfo)
        
        sizer = wx.GridBagSizer(2, 2)
        sizer.AddGrowableCol(1, 1)
        pos = [0, 0]
        def MakeLine(label, ctrl, flags=wx.ALIGN_CENTER_VERTICAL):
            st = wx.StaticText(dialog, -1, label)
            sizer.Add(st, pos, (1, 1), wx.ALIGN_CENTER_VERTICAL)
            pos[1] += 1
            sizer.Add(ctrl, pos, (1, 1), flags)
            pos[1] = 0
            pos[0] += 1
        MakeLine("Default button width:", widthCtrl)
        MakeLine("Default button height:", heightCtrl)
        MakeLine("Row gap:", rowGapCtrl)
        MakeLine("Column gap:", columnGapCtrl)
        MakeLine("Outside border size:", borderSizeCtrl)
        MakeLine("Window colour:", windowColourCtrl)
        MakeLine("Button foreground colour:", foregroundColourCtrl)
        MakeLine("Button background colour:", backgroundColourCtrl)
        MakeLine("Button font:", fontCtrl, wx.EXPAND)
        dialog.sizer.Add(sizer)

        if dialog.AffirmedShowModal():
            return (
                widthCtrl.GetValue(),
                heightCtrl.GetValue(),
                rowGapCtrl.GetValue(),
                columnGapCtrl.GetValue(),
                borderSizeCtrl.GetValue(),
                windowColourCtrl.GetValue(),
                foregroundColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
                fontCtrl.GetValue(),
            )



class AddButton(eg.ActionClass):
    name = "Add Button"
    
    def __call__(self, kwargs):
        self.plugin.data.append((BUTTON_TYPE, kwargs))

    
    def GetLabel(self, kwargs):
        return self.name + ": " + kwargs.get("label", "")
    
    
    def Configure(self, kwargs={}):
        label = kwargs.get("label", "")
        event = kwargs.get("event", "")
        #image = kwargs.get("image", None)
        invisible = kwargs.get("invisible", False)
        
        def MakeOption(name, checkBox, ctrl):
            value = kwargs.get(name, None)
            def OnCheckBox(event):
                ctrl.Enable(checkBox.GetValue())
            checkBox.Bind(wx.EVT_CHECKBOX, OnCheckBox)
            if value is None:
                checkBox.SetValue(False)
                ctrl.SetValue(self.plugin.defaults[name])
                ctrl.Enable(False)
            else:
                checkBox.SetValue(True)
                ctrl.SetValue(value)
            sizer.Add(checkBox, 0, wx.ALIGN_CENTER_VERTICAL)
            sizer.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL)
            def SetResult():
                if checkBox.GetValue():
                    kwargs[name] = ctrl.GetValue()
            return SetResult
        
        dialog = eg.ConfigurationDialog(self)
        sizer = wx.GridSizer(0, 2)
        labelCtrl = wx.TextCtrl(dialog, -1, label)
        sizer.Add(wx.StaticText(dialog, -1, "Label:"))
        sizer.Add(labelCtrl)
        eventCtrl = wx.TextCtrl(dialog, -1, event)
        sizer.Add(wx.StaticText(dialog, -1, "Event:"))
        sizer.Add(eventCtrl)
        
        imageOption = MakeOption(
            "image", 
            wx.CheckBox(dialog, -1, "Use image as label:"), 
            eg.ImagePicker(dialog, label = "Choose Image")
        )

        foregroundColour = MakeOption(
            "foregroundColour", 
            wx.CheckBox(dialog, -1, "Override foreground colour:"), 
            eg.ColourSelectButton(dialog, label="Choose Colour")
        )
        
        backgroundColour = MakeOption(
            "backgroundColour", 
            wx.CheckBox(dialog, -1, "Override background colour:"), 
            eg.ColourSelectButton(dialog, label="Choose Colour")
        )
        
        fontInfo = MakeOption(
            "fontInfo", 
            wx.CheckBox(dialog, -1, "Override button font:"), 
            eg.FontButton(dialog, label="Choose Font")
        )

        width = MakeOption(
            "width", 
            wx.CheckBox(dialog, -1, "Override width:"), 
            eg.SpinIntCtrl(dialog, min=0)
        )
        
        height = MakeOption(
            "height", 
            wx.CheckBox(dialog, -1, "Override height:"), 
            eg.SpinIntCtrl(dialog, min=0)
        )
        
        invisibleCtrl = wx.CheckBox(dialog, -1, "Invisible")
        invisibleCtrl.SetValue(invisible)
        sizer.Add(invisibleCtrl)
        dialog.sizer.Add(sizer)
        if dialog.AffirmedShowModal():
            image = kwargs.get("image", None)
            kwargs = {}
            kwargs["label"] = labelCtrl.GetValue()
            kwargs["event"] = eventCtrl.GetValue()
            fontInfo()
            foregroundColour()
            backgroundColour()
            width()
            height()
            imageOption()
            #image = imageCtrl.GetValue()
            #if image:
            #    kwargs["image"] = image
            if invisibleCtrl.GetValue():
                kwargs["invisible"] = True
            return kwargs,

        
        

class StartNewLine(eg.ActionClass):
    name = "Start New Line"
    
    def __call__(self, height=0):
        self.plugin.data.append((LINE_TYPE, (height,)))


    def GetLabel(self, *args):
        return self.name
    
    
    def Configure(self, height=0):
        dialog = eg.ConfigurationDialog(self)
        heightCtrl = eg.SpinIntCtrl(dialog, value=height)
        dialog.AddLabel("Height:")
        dialog.AddCtrl(heightCtrl)
        if dialog.AffirmedShowModal():
            return (
                heightCtrl.GetValue(),
            )



class Show(eg.ActionClass):
    
    def __call__(self, xPos=0, yPos=0):
        wx.CallAfter(CreateRemote, self.plugin, xPos, yPos)
        
        
    def GetLabel(self, xPos, yPos):
        return "Show at %d,%d" % (xPos, yPos)
    
    
    def Configure(self, xPos=0, yPos=0):
        dialog = eg.ConfigurationDialog(self)
        xPosCtrl = eg.SpinIntCtrl(dialog, value=xPos)
        yPosCtrl = eg.SpinIntCtrl(dialog, value=yPos)
        dialog.AddLabel("Window horizontal position:")
        dialog.AddCtrl(xPosCtrl)
        dialog.AddLabel("Window vertical position:")
        dialog.AddCtrl(yPosCtrl)
        if dialog.AffirmedShowModal():
            return (
                xPosCtrl.GetValue(),
                yPosCtrl.GetValue(),
            )
        
        
BUTTON_TYPE = 0
LINE_TYPE = 1
SPACER_TYPE = 2

class GenButton(buttons.GenButton):
    def DrawFocusIndicator(self, *args):
        pass
    

class GenBitmapButton(buttons.GenBitmapButton):
    def DrawFocusIndicator(self, *args):
        pass
    

def CreateRemote(plugin, xPos, yPos):
    data = plugin.data
    borderSize = plugin.borderSize
    
    if plugin.frame:
        plugin.frame.Destroy()
    plugin.frame = frame = wx.Frame(
        None, 
        wx.ID_ANY, 
        'Remote', 
        pos=(xPos, yPos),
        style=wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.CAPTION,
    )
    frame.SetBackgroundColour(plugin.windowColour)
    panel = wx.Panel(frame)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add((0, borderSize))
    lineSizer = wx.BoxSizer(wx.HORIZONTAL)
    x = 0
    y = 0
    
    fontSize = DEFAULT_FONT_SIZE
    for itemType, args in data:
        if itemType == BUTTON_TYPE:
            kwargs = args
            def GetOption(name):
                return kwargs.get(name, plugin.defaults.get(name))
            label = kwargs.get("label")
            event = kwargs.get("event")
            image = kwargs.get("image", None)
            invisible = kwargs.get("invisible", False)
            size=(GetOption("width"), GetOption("height"))
            if invisible:
                # create a spacer
                button = size
            else:
                if image:
                    stream = StringIO(b64decode(image))
                    bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
                    stream.close()
                    #bmp = wx.Bitmap(image)
                    button = GenBitmapButton(panel, -1, bmp, size=size)
                    button.SetLabel(label)
                else:
                    button = GenButton(panel, -1, label, size=size)
                button.SetFont(wx.FontFromNativeInfoString(GetOption("fontInfo")))
                
                button.SetBezelWidth(3)
                button.SetBackgroundColour(GetOption("backgroundColour"))
                button.SetForegroundColour(GetOption("foregroundColour"))
                def MakeButtonDownFunc(event):
                    def OnButtonDown(wxEvent):
                        wxEvent.Skip()
                        if plugin.lastEvent:
                            plugin.lastEvent.SetShouldEnd()
                        plugin.lastEvent = plugin.TriggerEnduringEvent(event)
                    return OnButtonDown
                button.Bind(wx.EVT_LEFT_DOWN, MakeButtonDownFunc(event))
                button.Bind(wx.EVT_LEFT_DCLICK, MakeButtonDownFunc(event))
                button.Bind(wx.EVT_LEFT_UP, plugin.OnButtonUp)
            if x == 0:
                lineSizer.Add(button)
            else:
                lineSizer.Add(button, 0, wx.LEFT, plugin.rowGap)
            x += 1
        elif itemType == LINE_TYPE:
            height = args[0]
            mainSizer.Add(lineSizer, 0, wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, height + plugin.columnGap)
            lineSizer = wx.BoxSizer(wx.HORIZONTAL)
            y += 1
            x = 0
        elif itemType == SPACER_TYPE:
            x += 1
            
            
    mainSizer.Add(lineSizer, 0, wx.LEFT|wx.RIGHT, borderSize)
    mainSizer.Add((0, borderSize))
    panel.SetSizerAndFit(mainSizer)
    frame.SetClientSize(panel.GetSize())
    frame.Show(True)
    frame.Update()
            
        
