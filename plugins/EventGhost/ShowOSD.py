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

import threading
from os import listdir
from os.path import abspath, dirname, join

import wx

import eg
from eg.WinApi.Dynamic import (
    CreateEvent,
    SetEvent,
    SetWindowPos,
    SWP_FRAMECHANGED,
    SWP_HIDEWINDOW,
    SWP_NOACTIVATE,
    SWP_NOOWNERZORDER,
    SWP_SHOWWINDOW,
)
from eg.WinApi.Utils import GetMonitorDimensions

HWND_FLAGS = SWP_NOACTIVATE | SWP_NOOWNERZORDER | SWP_FRAMECHANGED

SKIN_DIR = join(
    abspath(dirname(__file__.decode('mbcs'))),
    "OsdSkins"
)
SKINS = [name[:-3] for name in listdir(SKIN_DIR) if name.endswith(".py")]
SKINS.sort()

DEFAULT_FONT_INFO = wx.Font(
    18,
    wx.SWISS,
    wx.NORMAL,
    wx.BOLD
).GetNativeFontInfoDesc()


class ShowOSD(eg.ActionBase):
    name = "Show OSD"
    description = "Shows a simple On Screen Display."
    iconFile = "icons/ShowOSD"

    class text:
        label = "Show OSD: %s"
        editText = "Text to display:"
        osdFont = "Text Font:"
        osdColour = "Text Colour:"
        outlineFont = "Outline OSD"
        alignment = "Alignment:"
        alignmentChoices = [
            "Top Left",
            "Top Right",
            "Bottom Left",
            "Bottom Right",
            "Screen Center",
            "Bottom Center",
            "Top Center",
            "Left Center",
            "Right Center",
        ]
        display = "Show on display:"
        xOffset = "Horizontal offset X:"
        yOffset = "Vertical offset Y:"
        wait1 = "Autohide OSD after"
        wait2 = "seconds (0 = never)"
        skin = "Use skin"

    def __call__(
            self,
            osdText="",
            fontInfo=None,
            foregroundColour=(255, 255, 255),
            backgroundColour=(0, 0, 0),
            alignment=0,
            offset=(0, 0),
            displayNumber=0,
            timeout=3.0,
            skin=None
    ):
        if isinstance(skin, bool):
            skin = SKINS[0] if skin else None
        self.osdFrame.timer.cancel()
        osdText = eg.ParseString(osdText)
        event = CreateEvent(None, 0, 0, None)
        wx.CallAfter(
            self.osdFrame.ShowOSD,
            osdText,
            fontInfo,
            foregroundColour,
            backgroundColour,
            alignment,
            offset,
            displayNumber,
            timeout,
            event,
            skin
        )
        eg.actionThread.WaitOnEvent(event)

    def Configure(
            self,
            osdText="",
            fontInfo=None,
            foregroundColour=(255, 255, 255),
            backgroundColour=(0, 0, 0),
            alignment=0,
            offset=(0, 0),
            displayNumber=0,
            timeout=3.0,
            skin=None,
    ):
        if isinstance(skin, bool):
            skin = SKINS[0] if skin else None
        if fontInfo is None:
            fontInfo = DEFAULT_FONT_INFO
        panel = eg.ConfigPanel()
        text = self.text
        editTextCtrl = panel.TextCtrl("\n\n", style=wx.TE_MULTILINE)
        height = editTextCtrl.GetBestSize()[1]
        editTextCtrl.ChangeValue(osdText)
        editTextCtrl.SetMinSize((-1, height))
        alignmentChoice = panel.Choice(
            alignment, choices=text.alignmentChoices
        )
        displayChoice = eg.DisplayChoice(panel, displayNumber)
        xOffsetCtrl = panel.SpinIntCtrl(offset[0], -32000, 32000)
        yOffsetCtrl = panel.SpinIntCtrl(offset[1], -32000, 32000)
        timeCtrl = panel.SpinNumCtrl(timeout)

        fontButton = panel.FontSelectButton(fontInfo)
        foregroundColourButton = panel.ColourSelectButton(foregroundColour)

        if backgroundColour is None:
            tmpColour = (0, 0, 0)
        else:
            tmpColour = backgroundColour
        outlineCheckBox = panel.CheckBox(
            backgroundColour is not None, text.outlineFont
        )

        backgroundColourButton = panel.ColourSelectButton(tmpColour)
        backgroundColourButton.Enable(backgroundColour is not None)

        useSkin = skin is not None
        skinCtrl = panel.CheckBox(useSkin, text.skin)
        skinCtrl.SetValue(useSkin)
        skinChc = panel.Choice(SKINS.index(skin) if skin else 0, SKINS)
        skinChc.Enable(useSkin)

        sizer = wx.GridBagSizer(5, 5)
        expand = wx.EXPAND
        align = wx.ALIGN_CENTER_VERTICAL
        sizer.AddMany([
            (panel.StaticText(text.editText), (0, 0), (1, 1), align),
            (editTextCtrl, (0, 1), (1, 4), expand),
            (panel.StaticText(text.osdFont), (1, 3), (1, 1), align),
            (fontButton, (1, 4)),
            (panel.StaticText(text.osdColour), (2, 3), (1, 1), align),
            (foregroundColourButton, (2, 4)),
            (outlineCheckBox, (3, 3), (1, 1), expand),
            (backgroundColourButton, (3, 4)),
            (skinCtrl, (4, 3)),
            (skinChc, (4, 4), (1, 1), expand),
            (panel.StaticText(text.alignment), (1, 0), (1, 1), align),
            (alignmentChoice, (1, 1), (1, 1), expand),
            (panel.StaticText(text.display), (2, 0), (1, 1), align),
            (displayChoice, (2, 1), (1, 1), expand),
            (panel.StaticText(text.xOffset), (3, 0), (1, 1), align),
            (xOffsetCtrl, (3, 1), (1, 1), expand),
            (panel.StaticText(text.yOffset), (4, 0), (1, 1), align),
            (yOffsetCtrl, (4, 1), (1, 1), expand),
            (panel.StaticText(text.wait1), (5, 0), (1, 1), align),
            (timeCtrl, (5, 1), (1, 1), expand),
            (panel.StaticText(text.wait2), (5, 2), (1, 3), align),
        ])

        sizer.AddGrowableCol(2)
        panel.sizer.Add(sizer, 1, wx.EXPAND)

        def OnCheckBoxBGColour(event):
            backgroundColourButton.Enable(outlineCheckBox.IsChecked())
            event.Skip()
        outlineCheckBox.Bind(wx.EVT_CHECKBOX, OnCheckBoxBGColour)

        def OnCheckBoxSkin(event):
            skinChc.Enable(skinCtrl.IsChecked())
            event.Skip()
        skinCtrl.Bind(wx.EVT_CHECKBOX, OnCheckBoxSkin)

        while panel.Affirmed():
            if outlineCheckBox.IsChecked():
                outlineColour = backgroundColourButton.GetValue()
            else:
                outlineColour = None
            if skinCtrl.IsChecked():
                skin = skinChc.GetStringSelection()
            else:
                skin = None

            panel.SetResult(
                editTextCtrl.GetValue(),
                fontButton.GetValue(),
                foregroundColourButton.GetValue(),
                outlineColour,
                alignmentChoice.GetValue(),
                (xOffsetCtrl.GetValue(), yOffsetCtrl.GetValue()),
                displayChoice.GetValue(),
                timeCtrl.GetValue(),
                skin
            )

    def GetLabel(self, osdText, *dummyArgs):
        return self.text.label % osdText.replace("\n", r"\n")

    @classmethod
    def OnAddAction(cls):
        def MakeOSD():
            cls.osdFrame = OSDFrame(None)

            def CloseOSD():
                cls.osdFrame.timer.cancel()
                cls.osdFrame.Close()

            eg.app.onExitFuncs.append(CloseOSD)

        wx.CallAfter(MakeOSD)

    @eg.LogIt
    def OnClose(self):
        # self.osdFrame.timer.cancel()
        # wx.CallAfter(self.osdFrame.Close)
        self.osdFrame = None


class OSDFrame(wx.Frame):
    """
    A shaped frame to display the OSD.
    """

    @eg.LogIt
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            "OSD Window",
            size=(0, 0),
            style=(
                wx.FRAME_SHAPED |
                wx.NO_BORDER |
                wx.FRAME_NO_TASKBAR |
                wx.STAY_ON_TOP
            )
        )
        self.hwnd = self.GetHandle()
        self.bitmap = wx.EmptyBitmap(0, 0)
        # we need a timer to possibly cancel it
        self.timer = threading.Timer(0.0, eg.DummyFunc)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass

    @staticmethod
    def GetSkinnedBitmap(
            textLines,
            textWidths,
            textHeights,
            textWidth,
            textHeight,
            memoryDC,
            textColour,
            skinName
    ):
        image = wx.Image(join(SKIN_DIR, skinName + ".png"))
        option = eg.Bunch()

        def Setup(minWidth, minHeight, xMargin, yMargin,
                  transparentColour=None):
            width = textWidth + 2 * xMargin
            if width < minWidth:
                width = minWidth
            height = textHeight + 2 * yMargin
            if height < minHeight:
                height = minHeight
            option.xMargin = xMargin
            option.yMargin = yMargin
            option.transparentColour = transparentColour
            bitmap = wx.EmptyBitmap(width, height)
            option.bitmap = bitmap
            memoryDC.SelectObject(bitmap)
            return width, height

        def Copy(x, y, width, height, toX, toY):
            bmp = wx.BitmapFromImage(image.GetSubImage((x, y, width, height)))
            memoryDC.DrawBitmap(bmp, toX, toY)

        def Scale(x, y, width, height, toX, toY, toWidth, toHeight):
            subImage = image.GetSubImage((x, y, width, height))
            subImage.Rescale(toWidth, toHeight, wx.IMAGE_QUALITY_HIGH)
            bmp = wx.BitmapFromImage(subImage)
            memoryDC.DrawBitmap(bmp, toX, toY)

        scriptGlobals = dict(Setup=Setup, Copy=Copy, Scale=Scale)
        eg.ExecFile(join(SKIN_DIR, skinName + ".py"), scriptGlobals)

        bitmap = option.bitmap
        memoryDC.SelectObject(wx.NullBitmap)
        bitmap.SetMask(wx.Mask(bitmap, option.transparentColour))
        memoryDC.SelectObject(bitmap)
        memoryDC.SetTextForeground(textColour)
        memoryDC.SetTextBackground(textColour)
        DrawTextLines(
            memoryDC, textLines, textHeights, option.xMargin, option.yMargin
        )
        memoryDC.SelectObject(wx.NullBitmap)
        return bitmap

    def OnClose(self, dummyEvent=None):
        # BUGFIX: Just hooking this event makes sure that nothing happens
        # when this OSD window is closed
        pass

    @eg.LogIt
    def OnPaint(self, dummyEvent=None):
        wx.BufferedPaintDC(self, self.bitmap)

    @eg.LogIt
    def OnTimeout(self):
        wx.CallAfter(
            SetWindowPos, self.hwnd, 0, 0, 0, 0, 0, HWND_FLAGS | SWP_HIDEWINDOW
        )

    @eg.LogIt
    def ShowOSD(
            self,
            osdText="",
            fontInfo=None,
            textColour=(255, 255, 255),
            outlineColour=(0, 0, 0),
            alignment=0,
            offset=(0, 0),
            displayNumber=0,
            timeout=3.0,
            event=None,
            skin=None,
    ):
        self.timer.cancel()
        if osdText.strip() == "":
            self.bitmap = wx.EmptyBitmap(0, 0)
            SetWindowPos(self.hwnd, 0, 0, 0, 0, 0, HWND_FLAGS | SWP_HIDEWINDOW)
            SetEvent(event)
            return

        # self.Freeze()
        memoryDC = wx.MemoryDC()

        # make sure the mask colour is not used by foreground or
        # background colour
        forbiddenColours = (textColour, outlineColour)
        maskColour = (255, 0, 255)
        if maskColour in forbiddenColours:
            maskColour = (0, 0, 2)
            if maskColour in forbiddenColours:
                maskColour = (0, 0, 3)
        maskBrush = wx.Brush(maskColour, wx.SOLID)
        memoryDC.SetBackground(maskBrush)

        if fontInfo is None:
            fontInfo = DEFAULT_FONT_INFO
        font = wx.FontFromNativeInfoString(fontInfo)
        memoryDC.SetFont(font)

        textLines = osdText.splitlines()
        sizes = [memoryDC.GetTextExtent(line or " ") for line in textLines]
        textWidths, textHeights = zip(*sizes)
        textWidth = max(textWidths)
        textHeight = sum(textHeights)

        if skin:
            bitmap = self.GetSkinnedBitmap(
                textLines,
                textWidths,
                textHeights,
                textWidth,
                textHeight,
                memoryDC,
                textColour,
                skin
            )
            width, height = bitmap.GetSize()
        elif outlineColour is None:
            width, height = textWidth, textHeight
            bitmap = wx.EmptyBitmap(width, height)
            memoryDC.SelectObject(bitmap)

            # fill the DC background with the maskColour
            memoryDC.Clear()

            # draw the text with the foreground colour
            memoryDC.SetTextForeground(textColour)
            DrawTextLines(memoryDC, textLines, textHeights)

            # mask the bitmap, so we can use it to get the needed
            # region of the window
            memoryDC.SelectObject(wx.NullBitmap)
            bitmap.SetMask(wx.Mask(bitmap, maskColour))

            # fill the anti-aliased pixels of the text with the foreground
            # colour, because the region of the window will add these
            # half filled pixels also. Otherwise we would get an ugly
            # border with mask-coloured pixels.
            memoryDC.SetBackground(wx.Brush(textColour, wx.SOLID))
            memoryDC.SelectObject(bitmap)
            memoryDC.Clear()
            memoryDC.SelectObject(wx.NullBitmap)
        else:
            width, height = textWidth + 5, textHeight + 5
            outlineBitmap = wx.EmptyBitmap(width, height, 1)
            outlineDC = wx.MemoryDC()
            outlineDC.SetFont(font)
            outlineDC.SelectObject(outlineBitmap)
            outlineDC.Clear()
            outlineDC.SetBackgroundMode(wx.SOLID)
            DrawTextLines(outlineDC, textLines, textHeights)
            outlineDC.SelectObject(wx.NullBitmap)
            outlineBitmap.SetMask(wx.Mask(outlineBitmap))
            outlineDC.SelectObject(outlineBitmap)

            bitmap = wx.EmptyBitmap(width, height)
            memoryDC.SetTextForeground(outlineColour)
            memoryDC.SelectObject(bitmap)
            memoryDC.Clear()

            Blit = memoryDC.Blit
            logicalFunc = wx.COPY
            for x in xrange(5):
                for y in xrange(5):
                    Blit(
                        x, y, width, height, outlineDC, 0, 0, logicalFunc, True
                    )
            outlineDC.SelectObject(wx.NullBitmap)
            memoryDC.SetTextForeground(textColour)
            DrawTextLines(memoryDC, textLines, textHeights, 2, 2)
            memoryDC.SelectObject(wx.NullBitmap)
            bitmap.SetMask(wx.Mask(bitmap, maskColour))

        region = wx.RegionFromBitmap(bitmap)
        self.SetShape(region)
        self.bitmap = bitmap
        monitorDimensions = GetMonitorDimensions()
        try:
            displayRect = monitorDimensions[displayNumber]
        except IndexError:
            displayRect = monitorDimensions[0]
        xOffset, yOffset = offset
        xFunc, yFunc = ALIGNMENT_FUNCS[alignment]
        x = displayRect.x + xFunc((displayRect.width - width), xOffset)
        y = displayRect.y + yFunc((displayRect.height - height), yOffset)
        deviceContext = wx.ClientDC(self)
        deviceContext.DrawBitmap(self.bitmap, 0, 0, False)
        SetWindowPos(
            self.hwnd, 0, x, y, width, height, HWND_FLAGS | SWP_SHOWWINDOW
        )

        if timeout > 0.0:
            self.timer = threading.Timer(timeout, self.OnTimeout)
            self.timer.start()
        eg.app.Yield(True)
        SetEvent(event)


def AlignLeft(width, offset):
    return offset


def AlignCenter(width, offset):
    return (width / 2) + offset


def AlignRight(width, offset):
    return width - offset


ALIGNMENT_FUNCS = (
    (AlignLeft, AlignLeft),  # Top Left
    (AlignRight, AlignLeft),  # Top Right
    (AlignLeft, AlignRight),  # Bottom Left
    (AlignRight, AlignRight),  # Bottom Right
    (AlignCenter, AlignCenter),  # Screen Center
    (AlignCenter, AlignRight),  # Bottom Center
    (AlignCenter, AlignLeft),  # Top Center
    (AlignLeft, AlignCenter),  # Left Center
    (AlignRight, AlignCenter),  # Right Center
)


def DrawTextLines(deviceContext, textLines, textHeights, xOffset=0, yOffset=0):
    for i, textLine in enumerate(textLines):
        deviceContext.DrawText(textLine, xOffset, yOffset)
        yOffset += textHeights[i]
