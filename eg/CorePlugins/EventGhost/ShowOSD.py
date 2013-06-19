import threading
import win32gui
import win32con
import win32event
import wx

import eg
from eg.WinAPI.Utils import GetMonitorDimensions

    

class OSDFrame(wx.Frame):
    """ A shaped frame to display the OSD. """
    
    def __init__(self, parent):
        eg.whoami()
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
#        hwnd = self.GetHandle()
#        lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
#        win32gui.SetWindowLong(
#            hwnd, 
#            win32con.GWL_EXSTYLE, 
#            lExStyle | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
#        )
#        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
        self.bitmap = wx.EmptyBitmap(0,0)
        self.timer = threading.Timer(
            0.0,
            self.SetPosition, 
            ((-10000, -10000),)
        )
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetPosition((-10000, -10000))
        
        
    def ShowOSD(
        self, 
        osdText="", 
        fontInfo=None,
        foregroundColour=(255,255,255), 
        backgroundColour=(0,0,0),
        alignment=0, 
        offset=(0,0), 
        displayNumber=0, 
        timeout=3.0, 
        event=None
    ):        
        eg.whoami()
        self.osdText = osdText
        if osdText.strip() == "":
            w = 0
            h = 0
            bitmap = wx.EmptyBitmap(0,0)
        else:
            # make sure the mask colour is not used by foreground or 
            # background colour
            maskColour = (255,0,255)
            if (
                maskColour == foregroundColour 
                or maskColour == backgroundColour
            ):
                maskColour = (0,0,2)
                if (
                    maskColour == foregroundColour 
                    or maskColour == backgroundColour
                ):
                    maskColour = (0,0,3)
            brush = wx.Brush(maskColour, wx.SOLID)
            memoryDC = wx.MemoryDC()
            font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
            if fontInfo:
                nativeFontInfo = wx.NativeFontInfo()
                nativeFontInfo.FromString(fontInfo)
                font.SetNativeFontInfo(nativeFontInfo)
            memoryDC.SetFont(font)
            
            if backgroundColour is None:
                w, h = memoryDC.GetTextExtent(self.osdText + "M")
                bitmap = wx.EmptyBitmap(w, h)
                memoryDC.SetTextForeground(foregroundColour)
                memoryDC.SetBackground(brush)
                memoryDC.SelectObject(bitmap)
                memoryDC.Clear()
                memoryDC.DrawText(self.osdText, 0, 0) 
                memoryDC.SelectObject(wx.NullBitmap)
                bitmap.SetMask(wx.Mask(bitmap, maskColour))
                memoryDC.SetBackground(wx.Brush(foregroundColour, wx.SOLID))
                memoryDC.SelectObject(bitmap)
                memoryDC.Clear()
            else:
                w, h = memoryDC.GetTextExtent(self.osdText)
                w += 5 + memoryDC.GetTextExtent("M")[0]
                h += 5
                outlineBitmap = wx.EmptyBitmap(w, h, 1)
                memoryDC.SelectObject(outlineBitmap)
                memoryDC.Clear()
                memoryDC.SetBackgroundMode(wx.SOLID)
                memoryDC.DrawText(self.osdText, 0, 0) 
                memoryDC.SelectObject(wx.NullBitmap)
                outlineBitmap.SetMask(wx.Mask(outlineBitmap))
                memoryDC.SelectObject(outlineBitmap)
                
                bitmap = wx.EmptyBitmap(w, h)
                memoryDC2 = wx.MemoryDC()
                memoryDC2.SetFont(font)
                memoryDC2.SetBackground(brush)
                memoryDC2.SetTextForeground(backgroundColour)
                memoryDC2.SetTextBackground(maskColour)
                memoryDC2.SelectObject(bitmap)
                memoryDC2.Clear()
                Blit = memoryDC2.Blit
                WX_COPY = wx.COPY
                for x in xrange(5):
                    for y in xrange(5):
                        Blit(x, y, w, h, memoryDC, 0, 0, WX_COPY, True)
                memoryDC2.SetTextForeground(foregroundColour)
                memoryDC2.SetTextBackground(backgroundColour)
                memoryDC2.DrawText(self.osdText, 2, 2) 
                memoryDC2.SelectObject(wx.NullBitmap)
                memoryDC.SelectObject(wx.NullBitmap)
                bitmap.SetMask(wx.Mask(bitmap, maskColour))
        
        self.SetPosition((-10000, -10000))
        self.SetClientSize((w, h))
        
        r = wx.RegionFromBitmap(bitmap)
        _,_,w,_ = r.GetBox()
        self.hasShape = self.SetShape(r)
        self.bitmap = bitmap
        d = GetMonitorDimensions()[displayNumber]
        xOffset, yOffset = offset
        if alignment == 0: 
            # Top Left
            x = d.x + xOffset
            y = yOffset
        elif alignment == 1: 
            # Top Right
            x = d.x + d.width - xOffset - w
            y = yOffset
        elif alignment == 2: 
            # Bottom Left
            x = d.x + xOffset
            y = d.y + d.height - yOffset - h
        elif alignment == 3: 
            # Bottom Right
            x = d.x + d.width - xOffset - w
            y = d.y + d.height - yOffset - h
        elif alignment == 4: 
            # Screen Center
            x = d.x + ((d.width - w) / 2) + xOffset
            y = d.y + ((d.height - h) / 2) + yOffset
        self.Show()
        win32gui.BringWindowToTop(self.GetHandle())
        self.Refresh()
        self.SetPosition((x, y))
        #self.Raise()
        if timeout > 0.0:
            self.timer = threading.Timer(timeout, self.OnTimeout)
            self.timer.start()
        win32event.SetEvent(event)
        

    def OnTimeout(self):
        self.SetPosition((-10000, -10000))
        self.Hide()
        
        
    def OnPaint(self, evt=None):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0, False)


    def __del__(self):
        eg.whoami()
        
     
    
class ShowOSD(eg.ActionClass):
    name = "Show OSD"
    description = "Shows a simple On Screen Display."
    iconFile = "ShowOSD"
    class text:
        label = "Show OSD: %s"
        editText = "Text to display:"
        osdFont = "OSD Font:"
        osdFontButton = "Font Face"
        osdColour = "OSD Colour:"
        osdColourButton = "Font Colour"
        outlineColour = "Outline Colour"
        outlineFont = "Outline OSD"
        alignment = "Alignment:"
        alignmentChoices = [
            "Top Left", 
            "Top Right", 
            "Bottom Left",
            "Bottom Right", 
            "Center"
        ]
        display = "Show on display:"
        xOffset = "Horizontal offset X:"
        yOffset = "Vertical offset Y:"
        wait1 = "Autohide OSD after"
        wait2 = "seconds (0 = never)"

    
    def __init__(self):
        def makeOSD():
            self.osdFrame = OSDFrame(None)
            def closeOSD():
                self.osdFrame.timer.cancel()
                self.osdFrame.Close()
            eg.app.onExitFuncs.append(closeOSD)
        wx.CallAfter(makeOSD)
        

    def OnClose(self):
        eg.whoami()
        #self.osdFrame.timer.cancel()
        #wx.CallAfter(self.osdFrame.Close)
        self.osdFrame = None
        
        
    def __call__(
        self, 
        osdText="", 
        fontInfo=None,
        foregroundColour=(255,255,255), 
        backgroundColour=(0,0,0),
        alignment=0, 
        offset=(0,0), 
        displayNumber=0, 
        timeout=3.0
    ):
                
        self.osdFrame.timer.cancel()
        osdText = eg.ParseString(osdText)
        event = win32event.CreateEvent(None, 0, 0, None)
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
            event
        )
        eg.actionThread.WaitOnEvent(event)


    def GetLabel(self, osdText, *args):
        return self.text.label % osdText
    
    
    def Configure(
        self, 
        osdText="", 
        fontInfo=None,
        foregroundColour=(255,255,255), 
        backgroundColour=(0,0,0),
        alignment=0, 
        offset=(0,0), 
        displayNumber=0, 
        timeout=3.0
    ):                   
        eg.whoami()
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        editTextCtrl = wx.TextCtrl(dialog, value=osdText)
        alignmentChoice = wx.Choice(dialog, -1, choices=text.alignmentChoices)
        alignmentChoice.SetSelection(alignment)
        displayChoice = eg.DisplayChoice(dialog, -1, displayNumber)
        xOffsetCtrl = eg.SpinIntCtrl(dialog, -1, offset[0], -32000, 32000)
        yOffsetCtrl = eg.SpinIntCtrl(dialog, -1, offset[1], -32000, 32000)
        timeCtrl = eg.SpinNumCtrl(dialog, -1, value=timeout)
        

        fontButton = eg.FontButton(
            dialog, -1, text.osdFontButton, fontInfo=fontInfo
        )
        foregroundColourButton = eg.ColourSelectButton(
            dialog, -1, text.osdColourButton, foregroundColour
        )
        
        if backgroundColour is None:
            tmpColour = (0,0,0)
        else:
            tmpColour = backgroundColour
        outlineCheckBox = wx.CheckBox(dialog, -1, text.outlineFont)
        outlineCheckBox.SetValue(backgroundColour is not None)
        
        backgroundColourButton = eg.ColourSelectButton(
            dialog, -1, text.outlineColour, tmpColour
        )
        
        backgroundColourButton2 = wx.Button(dialog, -1, text.outlineColour)
        backgroundColourButton2.Disable()
        
        sizer = wx.GridBagSizer(5, 5)
        EXP = wx.EXPAND
        ACV = wx.ALIGN_CENTER_VERTICAL
        Add = sizer.Add
        Add(wx.StaticText(dialog, -1, text.editText), (0, 0), flag=ACV)
        Add(editTextCtrl, (0, 1), (1, 4), flag=EXP)
        
        Add(wx.StaticText(dialog, -1, text.osdFont), (1, 3), flag=ACV)
        Add(fontButton, (1, 4), flag=EXP)
        
        Add(wx.StaticText(dialog, -1, text.osdColour), (2, 3), flag=ACV)
        Add(foregroundColourButton, (2, 4), flag=EXP)

        Add(outlineCheckBox, (3, 3), flag=EXP)
        
        if backgroundColour is None:
            Add(backgroundColourButton2, (3, 4), flag=EXP)
            backgroundColourButton.Hide()
        else:
            Add(backgroundColourButton, (3, 4), flag=EXP)
            backgroundColourButton2.Hide()
        
        Add(wx.StaticText(dialog, -1, text.alignment), (1, 0), flag=ACV)
        Add(alignmentChoice, (1, 1), flag=EXP)
        Add(wx.StaticText(dialog, -1, text.display), (2, 0), flag=ACV)
        Add(displayChoice, (2, 1), flag=EXP)
        
        Add(wx.StaticText(dialog, -1, text.xOffset), (3, 0), flag=ACV)
        Add(xOffsetCtrl, (3, 1), flag=EXP)
        
        Add(wx.StaticText(dialog, -1, text.yOffset), (4, 0), flag=ACV)
        Add(yOffsetCtrl, (4, 1), flag=EXP)
        
        Add(wx.StaticText(dialog, -1, text.wait1), (5, 0), flag=ACV)
        Add(timeCtrl, (5, 1), flag=EXP)
        Add(wx.StaticText(dialog, -1, text.wait2), (5, 2), (1, 3), flag=ACV)
            
        sizer.AddGrowableCol(2)
        dialog.sizer.Add(sizer, 1, wx.EXPAND)
        backgroundColourButton.SetMinSize(
            backgroundColourButton2.GetBestSize())
        
        def on_outline(event):
            if outlineCheckBox.IsChecked():
                sizer.Detach(backgroundColourButton2)
                backgroundColourButton2.Hide()
                sizer.Add(backgroundColourButton, (3, 4), flag=wx.EXPAND)
                backgroundColourButton.Show()
            else:
                sizer.Detach(backgroundColourButton)
                backgroundColourButton.Hide()
                sizer.Add(backgroundColourButton2, (3, 4), flag=wx.EXPAND)
                backgroundColourButton2.Show()
            sizer.Layout()
            
        outlineCheckBox.Bind(wx.EVT_CHECKBOX, on_outline)
        
        if dialog.AffirmedShowModal():
            if outlineCheckBox.IsChecked():
                outlineColour = backgroundColourButton.GetColour()
            else:
                outlineColour = None
            return (
                editTextCtrl.GetValue(),
                fontButton.GetValue(), 
                foregroundColourButton.GetColour(), 
                outlineColour,
                alignmentChoice.GetSelection(),
                (xOffsetCtrl.GetValue(), yOffsetCtrl.GetValue()),
                displayChoice.GetSelection(),
                timeCtrl.GetValue()
            )
        
        
