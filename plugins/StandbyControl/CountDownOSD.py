# -*- coding: utf-8 -*-

#
# plugins/Standby/CountDownOSD.py
#
# Copyright (C) 2008-2012 Stefan Gollmer & Daniel Brugger
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# This code is based on plugins/EventGhost/ShowOSD.py
# Unfortunately I couldn't just call the original implementation 
# since here we show an OSD out of a running Thread (and not out of a running eg.Action)


import eg
import wx
from threading import Thread, Event, Timer, Lock
from os.path import join, dirname, abspath
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import (
    CreateEvent,
    SetEvent,
    SetWindowPos,
    SWP_HIDEWINDOW,
    SWP_FRAMECHANGED,
    SWP_NOACTIVATE,
    SWP_NOOWNERZORDER,
    SWP_SHOWWINDOW
)

HWND_FLAGS = SWP_NOACTIVATE | SWP_NOOWNERZORDER | SWP_FRAMECHANGED
SKIN_DIR = abspath(join(
    dirname(__file__.decode('mbcs')),
    "..\\EventGhost\\OsdSkins"
))

DEFAULT_FONT_INFO = wx.Font(
    24,
    wx.SWISS,
    wx.NORMAL,
    wx.NORMAL
).GetNativeFontInfoDesc()


def AlignLeft(width, offset):
    return offset


def AlignCenter(width, offset):
    return (width / 2) + offset


def AlignRight(width, offset):
    return width - offset


ALIGNMENT_FUNCS = (
    (AlignLeft, AlignLeft), # Top Left
    (AlignRight, AlignLeft), # Top Right
    (AlignLeft, AlignRight), # Bottom Left
    (AlignRight, AlignRight), # Bottom Right
    (AlignCenter, AlignCenter), # Screen Center
    (AlignCenter, AlignRight), # Bottom Center
    (AlignCenter, AlignLeft), # Top Center
    (AlignLeft, AlignCenter), # Left Center
    (AlignRight, AlignCenter), # Right Center
)


def DrawTextLines(deviceContext, textLines, textHeights, xOffset=0, yOffset=0):
    for i, textLine in enumerate(textLines):
        deviceContext.DrawText(textLine, xOffset, yOffset)
        yOffset += textHeights[i]


# The GUI code of this frame is 99% the same as the one from EventGhost.OSDFrame.
# However, unfortunately I couldn't reuse that one because of crucial details: 
# 1) EventGhost.OSDFrame is called from an Action, while MyOSDFrame is called from a Thread.
#    Thread synchronization is therefore different; calling 'eg.actionThread.WaitOnEvent(event)' 
#    would be illegal if we are not in the actionThread.
# 2) EventGhost.OSDFrame is reused allover the runtime of EG while MyOSDFrame is destroyed on close.
class MyOSDFrame(wx.Frame):
    """ A shaped frame to display the OSD. """

    @eg.LogIt
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            "OSD Window",
            size=(0, 0),
            style=wx.FRAME_SHAPED
                |wx.NO_BORDER
                |wx.FRAME_NO_TASKBAR
                |wx.STAY_ON_TOP
        )
        self.hwnd = self.GetHandle()
        self.bitmap = wx.Bitmap(0, 0)
        # we need a timer to possibly cancel it
        self.timer = Timer(0.0, eg.DummyFunc)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CLOSE, self.OnClose)


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
            self.bitmap = wx.Bitmap(0, 0)
            SetWindowPos(self.hwnd, 0, 0, 0, 0, 0, HWND_FLAGS|SWP_HIDEWINDOW)
            event.set()
            return

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
        font = wx.Font(fontInfo)
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
                "Default"
            )
            width, height = bitmap.GetSize()
        elif outlineColour is None:
            width, height = textWidth, textHeight
            bitmap = wx.Bitmap(width, height)
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
            outlineBitmap = wx.Bitmap(width, height, 1)
            outlineDC = wx.MemoryDC()
            outlineDC.SetFont(font)
            outlineDC.SelectObject(outlineBitmap)
            outlineDC.Clear()
            outlineDC.SetBackgroundMode(wx.SOLID)
            DrawTextLines(outlineDC, textLines, textHeights)
            outlineDC.SelectObject(wx.NullBitmap)
            outlineBitmap.SetMask(wx.Mask(outlineBitmap))
            outlineDC.SelectObject(outlineBitmap)

            bitmap = wx.Bitmap(width, height)
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

        region = wx.Region(bitmap)
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
            self.hwnd, 0, x, y, width, height, HWND_FLAGS|SWP_SHOWWINDOW
        )

        if timeout > 0.0:
            self.timer = Timer(timeout, self.OnTimeout)
            self.timer.start()
        eg.app.Yield(True)
        event.set()

    def GetSkinnedBitmap(
        self,
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

        def Setup(minWidth, minHeight, xMargin, yMargin, transparentColour):
            width = textWidth + 2 * xMargin
            if width < minWidth:
                width = minWidth
            height = textHeight + 2 * yMargin
            if height < minHeight:
                height = minHeight
            option.xMargin = xMargin
            option.yMargin = yMargin
            option.transparentColour = transparentColour
            bitmap = wx.Bitmap(width, height)
            option.bitmap = bitmap
            memoryDC.SelectObject(bitmap)
            return width, height

        def Copy(x, y, width, height, toX, toY):
            bmp = wx.Bitmap(image.GetSubImage((x, y, width, height)))
            memoryDC.DrawBitmap(bmp, toX, toY)

        def Scale(x, y, width, height, toX, toY, toWidth, toHeight):
            subImage = image.GetSubImage((x, y, width, height))
            subImage.Rescale(toWidth, toHeight, wx.IMAGE_QUALITY_HIGH)
            bmp = wx.Bitmap(subImage)
            memoryDC.DrawBitmap(bmp, toX, toY)

        scriptGlobals = dict(Setup=Setup, Copy=Copy, Scale=Scale)
        #eg.ExecFile(join(SKIN_DIR, skinName + ".py"), scriptGlobals)
        execfile(join(SKIN_DIR, skinName + ".py"), scriptGlobals)
        
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


    @eg.LogIt
    def OnTimeout(self):
        wx.CallAfter(self.Close)


    @eg.LogIt
    def OnPaint(self, dummyEvent=None):
        wx.BufferedPaintDC(self, self.bitmap)


    @eg.LogIt
    def OnClose(self, dummyEvent=None):
        self.timer.cancel()
        self.Destroy()


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass


class DisplayOsdThread(Thread):
    def __init__(
        self,
        plugin,
        osdText,
        fontInfo,
        foregroundColour,
        backgroundColour,
        alignment,
        offset,
        displayNumber,
        skin,
        countDownTime,
        startValue,
        endValue,
        interval,
        countDownFinishEvent,
        useExternalOSD,
        alternativeOSD
    ):

        Thread.__init__(self, name="DisplayOsdThread")

        self.plugin = plugin

        self.osdText = osdText
        self.fontInfo = fontInfo
        self.foregroundColour = foregroundColour
        self.backgroundColour = backgroundColour
        self.alignment = alignment
        self.offset = offset
        self.displayNumber = displayNumber
        self.skin = skin

        self.countDownTime = countDownTime
        self.endTime = endValue
        self.interval = interval

        self.countDownFinishEvent = countDownFinishEvent
        self.useExternalOSD = useExternalOSD
        self.alternativeOSD = alternativeOSD

        # texts with the syntax: '${myexpr}' are evaluated and replaced by the content of 'myexpr'
        # for example: ${'eg.globals.OsdText.getText('OsdDemoText')'} will evaluate the expression 
        # assuming that the method 'getText()' exists and returning the language dependant text
        try:
            expr = osdText
            pos = expr.find(u'${')
            if pos >= 0:
                expr = expr[pos+2:]
                pos = expr.find(u'}')
                if pos > 0:
                    expr = expr[0:pos].strip()
                    self.osdText = unicode(eval(expr))
                else:
                    eg.PrintError("%s is not a valid expression, following the syntax '${my_expression}'. The closing bracket is missing", osdText)
        except Exception, exc:
            eg.PrintTraceback("CountDownOSD: Invalid expression: " + repr(osdText))
            eg.PrintError(unicode(exc))
            self.osdText = osdText

        length = 0
        pos = self.osdText.find(u'%c%')
        if pos >= 0:
            length = 3
            insert = u'%(counter)i'
        else:
            pos = self.osdText.find(u'%cf%')
            if pos >= 0:
                length = 4
                insert = u'%(counter)'
        if length > 0:
            self.osdText = self.osdText[:pos] + insert + self.osdText[pos+length:]
            self.formatedOSD = True
        else:
            self.formatedOSD = False

        self.nextTime = startValue
        self.lastTime = startValue
        self.close = False
        self.finishThread = False
        self.threadEvent = Event()
        self.guiEvent = Event()
        self.lock = plugin.osdLock
        
        wx.CallAfter(self.MakeOsd, self.guiEvent)
        self.guiEvent.wait(countDownTime)


    def MakeOsd(self, guiEvt):
        self.osdFrame = MyOSDFrame(None)
        guiEvt.set()


    @eg.LogItWithReturn
    def run(self):
        if not hasattr(self, 'osdFrame'):
            return False # sometimes during shutdown / startup
        
        osdFrame = self.osdFrame
        lock = self.lock
        lock.acquire()
        try:
            timeout = self.countDownTime * 2
            useExternalOSD = self.useExternalOSD
    
            while True:
                if self.close:
                    break
    
                if self.finishThread:
                    timeout = 0.1
                    self.nextTime = self.lastTime
                    text = "" # empty text causes MyOSDFrame to close
                else:
                    if self.formatedOSD:
                        text = self.osdText % {'counter': self.nextTime}
                    else:
                        text = self.osdText
    
                if useExternalOSD:
                    # Note: it's very likely that this 'useExternalOSD' code block does not properly run, I don't know, I never tested this
                    command = u'eg.plugins.' + self.alternativeOSD
                    pos = command.find(u'%s%')
                    if pos >= 0:
                        command = command[:pos] + "text" + command[pos + 3:]
                    pos = command.find(u'%t%')
                    if pos >= 0:
                        command = command[:pos] + str(timeout) + command[pos + 3:]
    
                    tries = 5
                    try:
                        exec command in eg.globals.__dict__, locals()
                    except:
                        eg.PrintError("CountDownOSD: Error on executing external function")
                        tries -= 1
    
                        if tries == 0:
                            eg.PrintError("CountDownOSD: Too many errors on external function, set to standard OSD")
                            useExternalOSD = False

                if not useExternalOSD:
                    osdText = eg.ParseString(text)
                    # Note: although tempting, we cannot simply call the Action 'eg.plugins.EventGhost.ShowOSD' since we are not in the action thread!
                    if osdFrame is not None and hasattr(osdFrame, 'ShowOSD'):
                        wx.CallAfter(
                            osdFrame.ShowOSD,
                            osdText,
                            self.fontInfo,
                            self.foregroundColour,
                            self.backgroundColour,
                            self.alignment,
                            self.offset,
                            self.displayNumber,
                            timeout,
                            self.guiEvent,
                            self.skin
                        )
                    self.guiEvent.wait(self.countDownTime)

                if self.finishThread:
                    # time.sleep(2*timeout) # necessary?
                    break

                self.lastTime = self.nextTime
                self.nextTime -= self.interval
    
                if self.nextTime < self.endTime:
                    self.nextTime = self.endTime
                    lock.release()
                    self.threadEvent.wait(self.countDownTime)
                    lock.acquire()
                    if not self.finishThread:
                        self.plugin.TriggerEvent(self.countDownFinishEvent)
                    self.finishThread = True
                else:
                    lock.release()
                    self.threadEvent.wait(self.countDownTime)
                    lock.acquire()
        except Exception, exc:
            eg.PrintTraceback("Error showing OSD")
            eg.PrintError(unicode(exc))
            raise
        finally:
            try:
                osdFrame.Close()
            except:
                pass
            lock.release()
        return True

    @eg.LogItWithReturn
    def Finish(self):
        lock = self.lock
        lock.acquire()
        result = False
        if self.isAlive():
            self.finishThread = True
            self.threadEvent.set()
            result = True
        lock.release()
        return result

    @eg.LogIt
    def OnClose(self):
        lock = self.lock
        lock.acquire()
        if self.isAlive():
            self.close = True
            self.threadEvent.set()
        lock.release()


class CountDownOSD(eg.ActionClass):
    
    @eg.LogIt
    def __call__(
        self,
        osdText="",
        fontInfo=None,
        foregroundColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        alignment=0,
        offset=(0, 0),
        displayNumber=0,
        skin=None,

        countDownTime=3.0,
        startValue = 120,
        endValue = 0,
        interval = 1,
        countDownFinishEvent = "OSDCountDownFinished",
        useExternalOSD = False,
        alternativeOSD = ""
    ):
        plugin = self.plugin

        if not plugin.started:
            self.PrintError(plugin.text.notStarted)
            return False
        
        if self.OSDCancel():
            eg.PrintDebugNotice("OSDCancel: running osd thread cancelled")
            
        plugin.countDownOSD = self
        plugin.osdThread = DisplayOsdThread(
            self.plugin,
            osdText,
            fontInfo,
            foregroundColour,
            backgroundColour,
            alignment,
            offset,
            displayNumber,
            skin,

            countDownTime,
            startValue,
            endValue,
            interval,
            countDownFinishEvent,
            useExternalOSD,
            alternativeOSD
        )
        plugin.osdThread.start()

    @eg.LogIt
    def OSDCancel(self):
        plugin = self.plugin
        if plugin.osdThread != None and plugin.osdThread.isAlive():
            plugin.osdThread.Finish()
            plugin.osdThread.join()
            plugin.osdThread = None
            plugin.countDownOSD = None
            return True
        return False

    @eg.LogIt
    def OnClose(self):
        plugin = self.plugin
        if plugin.osdThread != None and plugin.osdThread.isAlive():
            plugin.osdThread.OnClose()
            plugin.osdThread = None

    def Configure(
        self,
        osdText="Try me %c%",
        fontInfo=None,
        foregroundColour=(255, 255, 255),
        outlineColour=None,
        alignment=4,
        offset=(0, 0),
        displayNumber=0,
        skin="Default",

        countDownTime=1.0,
        startValue=60,
        endValue=1,
        interval=1,
        countDownFinishEvent = "OSDCountDownFinished",
        useExternalOSD = False,
        alternativeOSD = ""
    ):

        def OnCheckBox(event):
            outlineColourButton.Enable(outlineCheckBox.IsChecked())
            event.Skip()

        def OnCheckBoxExternalOSD(event):
            enable = useExternalOSDCheckBox.IsChecked()
            alignmentChoice.Enable(not enable)
            displayChoice.Enable(not enable)
            xOffsetCtrl.Enable(not enable)
            yOffsetCtrl.Enable(not enable)
            fontButton.Enable(not enable)
            textColourButton.Enable(not enable)
            outlineCheckBox.Enable(not enable)
            outlineColourButton.Enable(not enable)
            skinCtrl.Enable(not enable)
            externalOSDCtrl.Enable(enable)
            if enable:
                outlineColourButton.Enable(False)
            else:
                OnCheckBox(wx.CommandEvent())
            event.Skip()

        if fontInfo is None:
            fontInfo = DEFAULT_FONT_INFO
        panel = eg.ConfigPanel(self)
        text = self.text
        eventTextCtrl = panel.TextCtrl(countDownFinishEvent)

        useExternalOSDCheckBox = wx.CheckBox(panel, -1, text.useExternal)
        useExternalOSDCheckBox.SetValue(useExternalOSD)
        externalOSDCtrl = panel.TextCtrl(alternativeOSD)

        editTextCtrl = panel.TextCtrl("\n\n", style=wx.TE_MULTILINE)
        w, h = editTextCtrl.GetBestSize()
        editTextCtrl.ChangeValue(osdText)
        editTextCtrl.SetMinSize((-1, h))

        alignmentChoice = panel.Choice(alignment, choices=text.alignmentChoices)
        displayChoice = eg.DisplayChoice(panel, displayNumber)
        xOffsetCtrl = panel.SpinIntCtrl(offset[0], -32000, 32000)
        yOffsetCtrl = panel.SpinIntCtrl(offset[1], -32000, 32000)
        timeCtrl = panel.SpinNumCtrl(countDownTime)
        startCtrl = panel.SpinNumCtrl(startValue)
        endCtrl = panel.SpinNumCtrl(endValue)
        intervalCtrl = panel.SpinNumCtrl(interval)

        fontButton = panel.FontSelectButton(fontInfo)
        textColourButton = panel.ColourSelectButton(foregroundColour)

        if outlineColour is None:
            tmpColour = (0, 0, 0)
        else:
            tmpColour = outlineColour
        outlineCheckBox = panel.CheckBox(outlineColour is not None, text.outlineFont)

        outlineColourButton = panel.ColourSelectButton(tmpColour)
        skinCtrl = panel.CheckBox(bool(skin), text.skin)

        sizer = wx.GridBagSizer(5, 5)
        EXP = wx.EXPAND
        ACV = wx.ALIGN_CENTER_VERTICAL
        Add = sizer.Add

        rowCount = 0
        Add(wx.StaticText(panel, -1, text.eventText), (rowCount, 0), flag=ACV)
        Add(eventTextCtrl, (rowCount, 1), (1, 4), flag=EXP|ACV)

        rowCount += 1
        Add(useExternalOSDCheckBox, (rowCount, 1), (1, 4), flag=EXP|ACV)

        rowCount += 1
        Add(wx.StaticText(panel, -1, text.externalOSD), (rowCount, 0), flag=ACV)
        Add(externalOSDCtrl, (rowCount, 1), (1, 4), flag=EXP|ACV)

        rowCount += 1
        Add(wx.StaticText(panel, -1, text.headText), (rowCount, 1),(1,4), wx.ALIGN_BOTTOM |wx.ALIGN_CENTER)

        rowCount += 1
        Add(wx.StaticText(panel, -1, text.editText), (rowCount, 0), flag=ACV)
        Add(editTextCtrl, (rowCount, 1), (1, 4), flag=EXP)

        rowCount += 1
        sRowCount = rowCount
        Add(panel.StaticText(text.osdFont), (rowCount, 3), flag=ACV)
        Add(fontButton, (rowCount, 4))

        rowCount += 1
        Add(panel.StaticText(text.osdColour), (rowCount, 3), flag=ACV)
        Add(textColourButton, (rowCount, 4))

        rowCount += 1
        Add(outlineCheckBox, (rowCount, 3), flag=EXP)
        Add(outlineColourButton, (rowCount, 4))

        rowCount += 1
        Add(skinCtrl, (rowCount, 3))

        rowCount = sRowCount
        Add(panel.StaticText(text.alignment), (rowCount, 0), flag=ACV)
        Add(alignmentChoice, (rowCount, 1), flag=EXP)

        rowCount += 1
        Add(panel.StaticText(text.display), (rowCount, 0), flag=ACV)
        Add(displayChoice, (rowCount, 1), flag=EXP)

        rowCount += 1
        Add(panel.StaticText(text.xOffset), (rowCount, 0), flag=ACV)
        Add(xOffsetCtrl, (rowCount, 1), flag=EXP)

        rowCount += 1
        Add(panel.StaticText(text.yOffset), (rowCount, 0), flag=ACV)
        Add(yOffsetCtrl, (rowCount, 1), flag=EXP)

        rowCount += 1
        sRowCount = rowCount
        Add(panel.StaticText(text.start), (rowCount, 0), flag=ACV)
        Add(startCtrl, (rowCount, 1), flag=EXP)

        rowCount += 1
        Add(panel.StaticText(text.end), (rowCount, 0), flag=ACV)
        Add(endCtrl, (rowCount, 1), flag=EXP)

        rowCount = sRowCount
        Add(panel.StaticText(text.wait), (rowCount, 3), flag=ACV)
        Add(timeCtrl, (rowCount, 4), flag=EXP)

        rowCount += 1
        Add(panel.StaticText(text.interval), (rowCount, 3), flag=ACV)
        Add(intervalCtrl, (rowCount, 4), flag=EXP)

        sizer.AddGrowableCol(2)
        panel.sizer.Add(sizer, 1, wx.EXPAND)

        outlineCheckBox.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        useExternalOSDCheckBox.Bind(wx.EVT_CHECKBOX, OnCheckBoxExternalOSD)

        OnCheckBoxExternalOSD(wx.CommandEvent())

        while panel.Affirmed():
            if outlineCheckBox.IsChecked():
                outlineColour = outlineColourButton.GetValue()
            else:
                outlineColour = None
            panel.SetResult(
                editTextCtrl.GetValue(),
                fontButton.GetValue(),
                textColourButton.GetValue(),
                outlineColour,
                alignmentChoice.GetValue(),
                (xOffsetCtrl.GetValue(), yOffsetCtrl.GetValue()),
                displayChoice.GetValue(),
                skinCtrl.GetValue(),
                timeCtrl.GetValue(),
                startCtrl.GetValue(),
                endCtrl.GetValue(),
                intervalCtrl.GetValue(),
                eventTextCtrl.GetValue(),
                useExternalOSDCheckBox.GetValue(),
                externalOSDCtrl.GetValue()
            )

    def GetLabel(self, osdText, *dummyArgs):
        return self.text.label % osdText.replace("\n", r"\n")


class CancelOSDCountDown(eg.ActionClass):

    @eg.LogIt
    def __call__(self):
        self.plugin.OSDCancel()
