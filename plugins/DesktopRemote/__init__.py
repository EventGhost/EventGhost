# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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

u"""
    Name: Desktop Remote
    Author: Bitmonster
    Version: 1.0
    Description: Creates a remote-like desktop window.
    GUID: {5DFFBD61-7582-4D6F-8EA9-9CB36284C9CF}
    URL: http://www.eventghost.org/forum/viewtopic.php?t=513
"""

import eg

eg.RegisterPlugin(
    name = "Desktop Remote",
    author = "Bitmonster",
    version = "1.0.1158",
    guid = "{5DFFBD61-7582-4D6F-8EA9-9CB36284C9CF}",
    canMultiLoad = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=513",
    description = "Creates a remote-like desktop window.",
)


import wx
import wx.lib.buttons as buttons
import os
from base64 import b64decode, b64encode
from cStringIO import StringIO
from eg.WinApi import GetCursorPos



class Text:
    class CreateNew:
        pass

    class AddButton:
        label = "Label:"
        event = "Event:"


class ButtonType:
    pass

class LineType:
    pass



class ImageButton(wx.Button):

    def __init__(self, parent, value=None, label=""):
        self.value = value
        self.view = None
        wx.Button.__init__(self, parent, label=label)
        self.Bind(wx.EVT_BUTTON, self.OnButton)


    def OnButton(self, event):
        dialog = wx.FileDialog(
            self.GetParent(),
            #message=self.mesg,
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST,
            wildcard="All image files|*jpg;*.png;*.bmp;*.gif|All files|*.*"
        )
        if dialog.ShowModal() == wx.ID_OK:
            filePath = dialog.GetPath()
            imageFile = open(filePath, "rb")
            stream = imageFile.read()
            imageFile.close()
            self.SetValue(b64encode(stream))
            event.Skip()


    def SetValue(self, value):
        self.value = value
        if value and self.view:
            stream = StringIO(b64decode(value))
            image = wx.ImageFromStream(stream)
            stream.close()
            boxWidth, boxHeight = self.view.GetClientSizeTuple()
            width, height = image.GetSize()
            if width > boxWidth:
                height *= 1.0 * boxWidth / width
                width = boxWidth
            if height > boxHeight:
                width *= 1.0 * boxHeight / height
                height = boxHeight
            image.Rescale(width, height)
            bmp = wx.BitmapFromImage(image)
            self.view.SetBitmap(bmp)
            self.view.SetClientSize((boxWidth, boxHeight))


    def GetValue(self):
        return self.value



class DesktopRemote(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddEvents()

        self.AddAction(CreateNew)
        self.AddAction(AddButton)
        self.AddAction(StartNewLine)
        self.AddAction(Show)
        self.AddAction(Close)
        self.data = []
        self.lastEvent = None
        self.defaults = {
            "fontInfo": u'0;-13;0;0;0;700;0;0;0;0;3;2;1;34;Arial',
            "image": None,
            "foregroundColour": (255, 255, 255),
            "backgroundColour": (78, 78, 78),
            "width": 40,
            "height": 40,
        }
        self.frame = None


    def OnButtonUp(self, event):
        event.Skip()
        self.lastEvent.SetShouldEnd()


    def __stop__(self):
        if self.frame:
            wx.CallAfter(self.frame.Destroy)
            self.frame = None



class CreateNew(eg.ActionBase):
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
        fontInfo=u'0;-13;0;0;0;700;0;0;0;0;3;2;1;34;Arial',
        caption="Remote",
        windowStyle=0,
        showInTaskbar=True,
        moveOnDrag=True,
        iconizeOnDoubleClick=True,
        *args
    ):
        plugin = self.plugin
        plugin.data = []
        plugin.defaults["width"] = width
        plugin.defaults["height"] = height
        plugin.defaults["foregroundColour"] = foregroundColour
        plugin.defaults["backgroundColour"] = backgroundColour
        plugin.defaults["fontInfo"] = fontInfo
        plugin.rowGap = rowGap
        plugin.columnGap = columnGap
        plugin.borderSize = borderSize
        plugin.windowColour = windowColour
        plugin.caption = caption
        plugin.windowStyle = windowStyle
        plugin.showInTaskbar = showInTaskbar
        plugin.moveOnDrag = moveOnDrag
        plugin.iconizeOnDoubleClick = iconizeOnDoubleClick


    def GetLabel(self, *args):
        return self.name


    @eg.LogIt
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
        fontInfo=u'0;-13;0;0;0;700;0;0;0;0;3;2;1;34;Arial',
        caption="Remote",
        windowStyle=0,
        showInTaskbar=True,
        moveOnDrag=True,
        iconizeOnDoubleClick=True,
        *args
    ):
        panel = eg.ConfigPanel()
        panel.SetSizerProperty(vgap=2)
        captionCtrl = panel.TextCtrl(caption)
        showInTaskbarCtrl = panel.CheckBox(showInTaskbar, "Show in taskbar")
        moveOnDragCtrl = panel.CheckBox(
            moveOnDrag,
            "Move window on drag click in empty area"
        )
        iconizeOnDoubleClickCtrl = panel.CheckBox(
            iconizeOnDoubleClick,
            "Minimize window on double click in empty area"
        )
        choices = [
            "Normal window",
            "Simple border",
            "No border",
        ]
        windowStyleCtrl = panel.Choice(windowStyle, choices=choices)
        widthCtrl = panel.SpinIntCtrl(width)
        heightCtrl = panel.SpinIntCtrl(height)
        rowGapCtrl = panel.SpinIntCtrl(rowGap)
        columnGapCtrl = panel.SpinIntCtrl(columnGap)
        borderSizeCtrl = panel.SpinIntCtrl(borderSize)
        windowColourCtrl = panel.ColourSelectButton(windowColour)
        foregroundColourCtrl = panel.ColourSelectButton(foregroundColour)
        backgroundColourCtrl = panel.ColourSelectButton(backgroundColour)
        fontCtrl = panel.FontSelectButton(fontInfo)

        panel.AddLine("Caption:", captionCtrl)
        panel.AddLine(showInTaskbarCtrl)
        panel.AddLine(moveOnDragCtrl)
        panel.AddLine(iconizeOnDoubleClickCtrl)
        panel.AddLine("Window style:", windowStyleCtrl)
        panel.AddLine("Default button width:", widthCtrl)
        panel.AddLine("Default button height:", heightCtrl)
        panel.AddLine("Row gap:", rowGapCtrl)
        panel.AddLine("Column gap:", columnGapCtrl)
        panel.AddLine("Outside border size:", borderSizeCtrl)
        panel.AddLine("Window colour:", windowColourCtrl)
        panel.AddLine("Button foreground colour:", foregroundColourCtrl)
        panel.AddLine("Button background colour:", backgroundColourCtrl)
        panel.AddLine("Button font:", fontCtrl)

        while panel.Affirmed():
            panel.SetResult(
                widthCtrl.GetValue(),
                heightCtrl.GetValue(),
                rowGapCtrl.GetValue(),
                columnGapCtrl.GetValue(),
                borderSizeCtrl.GetValue(),
                windowColourCtrl.GetValue(),
                foregroundColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
                fontCtrl.GetValue(),
                captionCtrl.GetValue(),
                windowStyleCtrl.GetValue(),
                showInTaskbarCtrl.GetValue(),
                moveOnDragCtrl.GetValue(),
                iconizeOnDoubleClickCtrl.GetValue(),
            )



class AddButton(eg.ActionBase):
    name = "Add Button"

    def __call__(self, kwargs):
        self.plugin.data.append((ButtonType, kwargs))


    def GetLabel(self, kwargs):
        return self.name + ": " + kwargs.get("label", "")


    def Configure(self, kwargs={}):

        def MakeOption(name, checkBox, ctrl):
            value = kwargs.get(name, None)
            def OnCheckBox(event):
                ctrl.Enable(checkBox.GetValue())
                event.Skip()
            checkBox.Bind(wx.EVT_CHECKBOX, OnCheckBox)
            if value is None:
                checkBox.SetValue(False)
                ctrl.SetValue(self.plugin.defaults[name])
                ctrl.Enable(False)
            else:
                checkBox.SetValue(True)
                ctrl.SetValue(value)
            panel.AddLine(checkBox, ctrl)
            def SetResult():
                if checkBox.GetValue():
                    kwargs[name] = ctrl.GetValue()
            return SetResult

        panel = eg.ConfigPanel()
        panel.SetSizerProperty(vgap=2)
        text = self.text

        labelCtrl = panel.TextCtrl(kwargs.get("label", ""))
        panel.AddLine(text.label, labelCtrl)

        eventCtrl = panel.TextCtrl(kwargs.get("event", ""))
        panel.AddLine(text.event, eventCtrl)

        invisibleCtrl = panel.CheckBox(
            kwargs.get("invisible", False),
            "Invisible"
        )
        panel.AddLine(invisibleCtrl)

        imageButton = ImageButton(panel, label="Choose Image")
        imageBox = wx.StaticBitmap(
            panel,
            size=(40, 40),
            pos=(280, 70),
            style=wx.SUNKEN_BORDER
        )
        imageButton.view = imageBox

        imageOption = MakeOption(
            "image",
            panel.CheckBox(label="Use image as label:"),
            imageButton
        )

        foregroundColour = MakeOption(
            "foregroundColour",
            panel.CheckBox(label="Override foreground colour:"),
            panel.ColourSelectButton()
        )

        backgroundColour = MakeOption(
            "backgroundColour",
            panel.CheckBox(label="Override background colour:"),
            panel.ColourSelectButton()
        )

        fontInfo = MakeOption(
            "fontInfo",
            panel.CheckBox(label="Override button font:"),
            panel.FontSelectButton()
        )

        width = MakeOption(
            "width",
            panel.CheckBox(label="Override width:"),
            panel.SpinIntCtrl()
        )

        height = MakeOption(
            "height",
            panel.CheckBox(label="Override height:"),
            panel.SpinIntCtrl()
        )

        while panel.Affirmed():
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
            if invisibleCtrl.GetValue():
                kwargs["invisible"] = True
            panel.SetResult(kwargs)




class StartNewLine(eg.ActionBase):
    name = "Start New Line"

    def __call__(self, height=0):
        self.plugin.data.append((LineType, (height,)))


    def GetLabel(self, *args):
        return self.name


    def Configure(self, height=0):
        panel = eg.ConfigPanel()
        heightCtrl = panel.SpinIntCtrl(height)
        panel.AddLine("Height:", heightCtrl)
        while panel.Affirmed():
            panel.SetResult(heightCtrl.GetValue())



class Show(eg.ActionBase):

    def __call__(self, xPos=0, yPos=0, alwaysOnTop=False):
        wx.CallAfter(CreateRemote, self.plugin, xPos, yPos, alwaysOnTop)


    def GetLabel(self, xPos, yPos, *args):
        return "Show at %d,%d" % (xPos, yPos)


    def Configure(self, xPos=0, yPos=0, alwaysOnTop=False):
        panel = eg.ConfigPanel()
        xPosCtrl = panel.SpinIntCtrl(xPos, min=-32768, max=32767)
        yPosCtrl = panel.SpinIntCtrl(yPos, min=-32768, max=32767)
        alwaysOnTopCtrl = panel.CheckBox(
            alwaysOnTop,
            "Keep window always on top"
        )
        panel.AddLine("Screen horizontal position:", xPosCtrl)
        panel.AddLine("Screen vertical position:", yPosCtrl)
        panel.AddLine(alwaysOnTopCtrl)
        while panel.Affirmed():
            panel.SetResult(
                xPosCtrl.GetValue(),
                yPosCtrl.GetValue(),
                alwaysOnTopCtrl.GetValue(),
            )



class Close(eg.ActionBase):

    def __call__(self):
        if self.plugin.frame:
            self.plugin.frame.Destroy()
            self.plugin.frame = None



class GenButton(buttons.GenButton):

    def DrawFocusIndicator(self, *args):
        pass



class GenBitmapButton(buttons.GenBitmapButton):

    def DrawFocusIndicator(self, *args):
        pass



class RemotePanel(wx.Panel):

    def __init__(self, parent, plugin):
        self.parent = parent
        wx.Panel.__init__(self, parent)
        if plugin.moveOnDrag:
            self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        if plugin.iconizeOnDoubleClick:
            self.Bind(wx.EVT_LEFT_DCLICK, self.OnCmdIconize)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        self.menu = menu = wx.Menu()
        item = wx.MenuItem(menu, wx.NewId(), "Hide")
        menu.AppendItem(item)
        menu.Bind(wx.EVT_MENU, self.OnCmdIconize, item)
        item = wx.MenuItem(menu, wx.NewId(),"Close")
        menu.AppendItem(item)
        menu.Bind(wx.EVT_MENU, self.OnCmdClose, item)


    def OnCmdClose(self, event):
        self.parent.Close()


    def OnCmdIconize(self, event):
        self.parent.Iconize()


    def OnRightDown(self, event):
        self.PopupMenu(self.menu)


    def OnLeftDown(self, event):
        x1, y1 = GetCursorPos()
        x2, y2 = self.parent.GetScreenPosition()
        self.offset = (x1 - x2, y1 - y2)

        # from now on we want all mouse motion events
        self.Bind(wx.EVT_MOTION, self.OnDrag)
        # and the left up event
        self.Bind(wx.EVT_LEFT_UP, self.OnDragEnd)

        # and call Skip in for handling focus events etc.
        event.ResumePropagation(wx.EVENT_PROPAGATE_MAX)
        event.Skip()
        # start capturing the mouse exclusively
        self.CaptureMouse()


    def OnDrag(self, event):
        x1, y1 = GetCursorPos()
        x2, y2 = self.offset
        self.parent.SetPosition((x1 - x2, y1 - y2))


    def OnDragEnd(self, event):
        # unbind the unneeded events
        self.Unbind(wx.EVT_MOTION)
        self.Unbind(wx.EVT_LEFT_UP)

        # stop processing the mouse capture
        self.ReleaseMouse()



class RemoteFrame(wx.Frame):

    def __init__(self, plugin, pos, alwaysOnTop):
        style = wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLIP_CHILDREN|wx.CLOSE_BOX
        if not plugin.showInTaskbar:
            style |= wx.FRAME_NO_TASKBAR
        if plugin.windowStyle == 0:
            style |= wx.CAPTION
        elif plugin.windowStyle == 1:
            style |= wx.RAISED_BORDER
        elif plugin.windowStyle == 2:
            style |= wx.NO_BORDER|wx.FRAME_SHAPED
        if alwaysOnTop:
            style |= wx.STAY_ON_TOP
        wx.Frame.__init__(
            self,
            None,
            title=plugin.caption,
            pos=pos,
            style=style
        )
        self.SetBackgroundColour(plugin.windowColour)



def CreateRemote(plugin, xPos, yPos, alwaysOnTop):
    data = plugin.data
    borderSize = plugin.borderSize

    if plugin.frame:
        plugin.frame.Destroy()
    plugin.frame = frame = RemoteFrame(plugin, (xPos, yPos), alwaysOnTop)
    panel = RemotePanel(frame, plugin)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add((0, borderSize))
    lineSizer = wx.BoxSizer(wx.HORIZONTAL)
    x = 0
    y = 0

    def MakeButtonDownFunc(eventstring):
        if not eventstring:
            return
        def OnButtonDown(event):
            event.Skip()
            plugin.lastEvent = plugin.TriggerEnduringEvent(eventstring)
        return OnButtonDown


    for itemType, args in data:
        if itemType is ButtonType:
            kwargs = args
            def GetOption(name):
                return kwargs.get(name, plugin.defaults.get(name))
            label = kwargs.get("label")
            event = kwargs.get("event")
            image = kwargs.get("image", None)
            invisible = kwargs.get("invisible", False)
            size =(GetOption("width"), GetOption("height"))
            if invisible:
                # create a spacer
                button = size
            else:
                if image:
                    stream = StringIO(b64decode(image))
                    bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
                    stream.close()
                    button = GenBitmapButton(panel, -1, bmp, size=size)
                    button.SetLabel(label)
                else:
                    button = GenButton(panel, -1, label, size=size)
                button.SetFont(
                    wx.FontFromNativeInfoString(GetOption("fontInfo"))
                )

                button.SetBezelWidth(3)
                button.SetBackgroundColour(GetOption("backgroundColour"))
                button.SetForegroundColour(GetOption("foregroundColour"))

                OnButtonDown = MakeButtonDownFunc(event)
                if OnButtonDown:
                    button.Bind(wx.EVT_LEFT_DOWN, OnButtonDown)
                    button.Bind(wx.EVT_LEFT_DCLICK, OnButtonDown)
                    button.Bind(wx.EVT_LEFT_UP, plugin.OnButtonUp)
            if x == 0:
                lineSizer.Add(button)
            else:
                lineSizer.Add(button, 0, wx.LEFT, plugin.rowGap)
            x += 1
        elif itemType is LineType:
            height = args[0]
            mainSizer.Add(
                lineSizer,
                0,
                wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL,
                height + plugin.columnGap
            )
            lineSizer = wx.BoxSizer(wx.HORIZONTAL)
            y += 1
            x = 0

    mainSizer.Add(lineSizer, 0, wx.LEFT|wx.RIGHT, borderSize)
    mainSizer.Add((0, borderSize))
    panel.SetSizerAndFit(mainSizer)
    frame.SetClientSize(panel.GetSize())
    frame.Show(True)
    frame.Update()

