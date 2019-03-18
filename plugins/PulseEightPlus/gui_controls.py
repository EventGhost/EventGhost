# -*- coding: utf-8 -*-
# This file is part of the libCEC(R) library.
#
# libCEC(R) is Copyright (C) 2011-2015 Pulse-Eight Limited.
# All rights reserved.
# libCEC(R) is an original work, containing original code.
#
# libCEC(R) is a trademark of Pulse-Eight Limited.
#
# This program is dual-licensed; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA
#
#
# Alternatively, you can license this library under a commercial license,
# please contact Pulse-Eight Licensing for more information.
#
# For more information contact:
# Pulse-Eight Licensing       <license@pulse-eight.com>
#     http://www.pulse-eight.com/
#     http://www.pulse-eight.net/
#
#
# The code contained within this file also falls under the GNU license of
# EventGhost
#
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

import eg
import threading
import wx
import cStringIO
import wx.lib.agw.foldpanelbar as fpb
import wx.lib.scrolledpanel as scrolled
from .text import Text
from __cec_core import KEY_CODES, cec


def collapsed_icon_data():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x8eIDAT8\x8d\xa5\x93-n\xe4@\x10\x85?g\x03\n6lh)\xc4\xd2\x12\xc3\x81\
\xd6\xa2I\x90\x154\xb9\x81\x8f1G\xc8\x11\x16\x86\xcd\xa0\x99F\xb3A\x91\xa1\
\xc9J&\x96L"5lX\xcc\x0bl\xf7v\xb2\x7fZ\xa5\x98\xebU\xbdz\xf5\\\x9deW\x9f\xf8\
H\\\xbfO|{y\x9dT\x15P\x04\x01\x01UPUD\x84\xdb/7YZ\x9f\xa5\n\xce\x97aRU\x8a\
\xdc`\xacA\x00\x04P\xf0!0\xf6\x81\xa0\xf0p\xff9\xfb\x85\xe0|\x19&T)K\x8b\x18\
\xf9\xa3\xe4\xbe\xf3\x8c^#\xc9\xd5\n\xa8*\xc5?\x9a\x01\x8a\xd2b\r\x1cN\xc3\
\x14\t\xce\x97a\xb2F0Ks\xd58\xaa\xc6\xc5\xa6\xf7\xdfya\xe7\xbdR\x13M2\xf9\
\xf9qKQ\x1fi\xf6-\x00~T\xfac\x1dq#\x82,\xe5q\x05\x91D\xba@\xefj\xba1\xf0\xdc\
zzW\xcff&\xb8,\x89\xa8@Q\xd6\xaaf\xdfRm,\xee\xb1BDxr#\xae\xf5|\xddo\xd6\xe2H\
\x18\x15\x84\xa0q@]\xe54\x8d\xa3\xedf\x05M\xe3\xd8Uy\xc4\x15\x8d\xf5\xd7\x8b\
~\x82\x0fh\x0e"\xb0\xad,\xee\xb8c\xbb\x18\xe7\x8e;6\xa5\x89\x04\xde\xff\x1c\
\x16\xef\xe0p\xfa>\x19\x11\xca\x8d\x8d\xe0\x93\x1b\x01\xd8m\xf3(;x\xa5\xef=\
\xb7w\xf3\x1d$\x7f\xc1\xe0\xbd\xa7\xeb\xa0(,"Kc\x12\xc1+\xfd\xe8\tI\xee\xed)\
\xbf\xbcN\xc1{D\x04k\x05#\x12\xfd\xf2a\xde[\x81\x87\xbb\xdf\x9cr\x1a\x87\xd3\
0)\xba>\x83\xd5\xb97o\xe0\xaf\x04\xff\x13?\x00\xd2\xfb\xa9`z\xac\x80w\x00\
\x00\x00\x00IEND\xaeB`\x82'


def expanded_icon_data():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x9fIDAT8\x8d\x95\x93\xa1\x8e\xdc0\x14EO\xb2\xc4\xd0\xd2\x12\xb7(mI\
\xa4%V\xd1lQT4[4-\x9a\xfe\xc1\xc2|\xc6\xc2~BY\x83:A3E\xd3\xa0*\xa4\xd2\x90H!\
\x95\x0c\r\r\x1fK\x81g\xb2\x99\x84\xb4\x0fY\xd6\xbb\xc7\xf7>=\'Iz\xc3\xbcv\
\xfbn\xb8\x9c\x15 \xe7\xf3\xc7\x0fw\xc9\xbc7\x99\x03\x0e\xfbn0\x99F+\x85R\
\x80RH\x10\x82\x08\xde\x05\x1ef\x90+\xc0\xe1\xd8\ryn\xd0Z-\\A\xb4\xd2\xf7\
\x9e\xfbwoF\xc8\x088\x1c\xbbae\xb3\xe8y&\x9a\xdf\xf5\xbd\xe7\xfem\x84\xa4\
\x97\xccYf\x16\x8d\xdb\xb2a]\xfeX\x18\xc9s\xc3\xe1\x18\xe7\x94\x12cb\xcc\xb5\
\xfa\xb1l8\xf5\x01\xe7\x84\xc7\xb2Y@\xb2\xcc0\x02\xb4\x9a\x88%\xbe\xdc\xb4\
\x9e\xb6Zs\xaa74\xadg[6\x88<\xb7]\xc6\x14\x1dL\x86\xe6\x83\xa0\x81\xba\xda\
\x10\x02x/\xd4\xd5\x06\r\x840!\x9c\x1fM\x92\xf4\x86\x9f\xbf\xfe\x0c\xd6\x9ae\
\xd6u\x8d \xf4\xf5\x165\x9b\x8f\x04\xe1\xc5\xcb\xdb$\x05\x90\xa97@\x04lQas\
\xcd*7\x14\xdb\x9aY\xcb\xb8\\\xe9E\x10|\xbc\xf2^\xb0E\x85\xc95_\x9f\n\xaa/\
\x05\x10\x81\xce\xc9\xa8\xf6><G\xd8\xed\xbbA)X\xd9\x0c\x01\x9a\xc6Q\x14\xd9h\
[\x04\xda\xd6c\xadFkE\xf0\xc2\xab\xd7\xb7\xc9\x08\x00\xf8\xf6\xbd\x1b\x8cQ\
\xd8|\xb9\x0f\xd3\x9a\x8a\xc7\x08\x00\x9f?\xdd%\xde\x07\xda\x93\xc3{\x19C\
\x8a\x9c\x03\x0b8\x17\xe8\x9d\xbf\x02.>\x13\xc0n\xff{PJ\xc5\xfdP\x11""<\xbc\
\xff\x87\xdf\xf8\xbf\xf5\x17FF\xaf\x8f\x8b\xd3\xe6K\x00\x00\x00\x00IEND\xaeB\
`\x82'


def convert_icon(icon_data):
    stream = cStringIO.StringIO(icon_data)
    image = wx.Image(stream)
    stream.close()
    return wx.Bitmap(image)

try:
    COLLAPSED_ICON = convert_icon(collapsed_icon_data())
    EXPANDED_ICON = convert_icon(expanded_icon_data())

    IMAGE_LIST = wx.ImageList(16, 16)
    IMAGE_LIST.Add(COLLAPSED_ICON)
    IMAGE_LIST.Add(EXPANDED_ICON)
except:
    pass


_fold_panel_item = fpb.FoldPanelItem


class CaptionBar(wx.Window):
    def __init__(
        self,
        parent,
        id,
        pos,
        size,
        caption="",
        foldIcons=None,
        cbstyle=None,
        rightIndent=fpb.FPB_BMP_RIGHTSPACE,
        iconWidth=16,
        iconHeight=16,
        collapsed=False
    ):

        wx.Window.__init__(
            self,
            parent,
            wx.ID_ANY,
            pos=pos,
            size=(20, 20),
            style=wx.NO_BORDER
        )

        self._controlCreated = False
        self._collapsed = collapsed
        self.ApplyCaptionStyle(cbstyle, True)

        if foldIcons is None:
            foldIcons = wx.ImageList(16, 16)

            bmp = fpb.ExpandedIcon.GetBitmap()
            foldIcons.Add(bmp)
            bmp = fpb.CollapsedIcon.GetBitmap()
            foldIcons.Add(bmp)

        # set initial size
        if foldIcons:
            assert foldIcons.GetImageCount() > 1
            iconWidth, iconHeight = foldIcons.GetSize(0)

        self._caption = caption
        self._foldIcons = foldIcons
        self._style = cbstyle
        self._rightIndent = rightIndent
        self._iconWidth = iconWidth
        self._iconHeight = iconHeight
        self._oldSize = wx.Size(20, 20)

        self._controlCreated = True

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def ApplyCaptionStyle(self, cbstyle=None, applyDefault=True):
        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        newstyle = cbstyle

        if applyDefault:
            if not newstyle.FirstColourUsed():
                newstyle.SetFirstColour(wx.WHITE)

            if not newstyle.SecondColourUsed():
                colour = self.GetParent().GetBackgroundColour()
                r, g, b = (
                    int(colour.Red()),
                    int(colour.Green()),
                    int(colour.Blue())
                )
                colour = ((r >> 1) + 20, (g >> 1) + 20, (b >> 1) + 20)
                newstyle.SetSecondColour(
                    wx.Colour(
                        colour[0],
                        colour[1],
                        colour[2])
                )

            if not newstyle.CaptionColourUsed():
                newstyle.SetCaptionColour(wx.BLACK)

            if not newstyle.CaptionFontUsed():
                newstyle.SetCaptionFont(self.GetParent().GetFont())

            if not newstyle.CaptionStyleUsed():
                newstyle.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_V)

        self._style = newstyle

    def SetCaptionStyle(self, cbstyle=None, applyDefault=True):
        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        self.ApplyCaptionStyle(cbstyle, applyDefault)
        self.Refresh()

    def GetCaptionStyle(self):
        return self._style

    def IsCollapsed(self):
        return self._collapsed

    def SetRightIndent(self, pixels):
        assert pixels >= 0
        self._rightIndent = pixels
        if self._foldIcons:
            self.Refresh()

    def Collapse(self):
        self._collapsed = True
        self.RedrawIconBitmap()

    def Expand(self):
        self._collapsed = False
        self.RedrawIconBitmap()

    def SetBoldFont(self):
        self.GetFont().SetWeight(wx.BOLD)

    def SetNormalFont(self):
        self.GetFont().SetWeight(wx.NORMAL)

    def IsVertical(self):
        fld = self.GetParent()
        if isinstance(fld, FoldPanelItem):
            return fld.IsVertical()
        else:
            raise Exception("ERROR: Wrong Parent " + repr(fld))

    def OnPaint(self, event):
        if not self._controlCreated:
            event.Skip()
            return

        dc = wx.PaintDC(self)
        wndRect = self.GetRect()
        vertical = self.IsVertical()

        self.FillCaptionBackground(dc)
        dc.SetFont(self._style.GetCaptionFont())
        dc.SetTextForeground(self._style.GetCaptionColour())

        if vertical:
            dc.DrawText(self._caption, 4, fpb.FPB_EXTRA_Y / 2)
        else:
            dc.DrawRotatedText(
                self._caption,
                fpb.FPB_EXTRA_Y / 2,
                wndRect.GetBottom() - 4,
                90
            )

        if self._foldIcons:

            index = self._collapsed

            if vertical:
                drw = wndRect.GetRight() - self._iconWidth - self._rightIndent
                self._foldIcons.Draw(
                    index,
                    dc,
                    drw,
                    (wndRect.GetHeight() - self._iconHeight) / 2,
                    wx.IMAGELIST_DRAW_TRANSPARENT
                )
            else:
                self._foldIcons.Draw(
                    index,
                    dc,
                    (wndRect.GetWidth() - self._iconWidth) / 2,
                    self._rightIndent,
                    wx.IMAGELIST_DRAW_TRANSPARENT
                )

    def FillCaptionBackground(self, dc):
        style = self._style.GetCaptionStyle()

        if style == fpb.CAPTIONBAR_GRADIENT_V:
            if self.IsVertical():
                self.DrawVerticalGradient(dc, self.GetRect())
            else:
                self.DrawHorizontalGradient(dc, self.GetRect())

        elif style == fpb.CAPTIONBAR_GRADIENT_H:
            if self.IsVertical():
                self.DrawHorizontalGradient(dc, self.GetRect())
            else:
                self.DrawVerticalGradient(dc, self.GetRect())

        elif style == fpb.CAPTIONBAR_SINGLE:
            self.DrawSingleColour(dc, self.GetRect())
        elif (
            style == fpb.CAPTIONBAR_RECTANGLE or
            style == fpb.CAPTIONBAR_FILLED_RECTANGLE
        ):
            self.DrawSingleRectangle(dc, self.GetRect())
        else:
            raise Exception(
                "STYLE Error: Undefined Style Selected: " + repr(style))

    def OnMouseEvent(self, event):
        send_event = False
        vertical = self.IsVertical()

        if event.LeftDown() and self._foldIcons:

            pt = event.GetPosition()
            rect = self.GetRect()

            drw = (rect.GetWidth() - self._iconWidth - self._rightIndent)
            if (
                vertical and
                pt.x > drw or
                not vertical and
                pt.y < (self._iconHeight + self._rightIndent)
            ):
                send_event = True

        elif event.LeftDClick():
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            send_event = True

        elif event.Entering() and self._foldIcons:
            pt = event.GetPosition()
            rect = self.GetRect()

            drw = (rect.GetWidth() - self._iconWidth - self._rightIndent)
            if (
                vertical and
                pt.x > drw or
                not vertical and
                pt.y < (self._iconHeight + self._rightIndent)
            ):
                self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        elif event.Leaving():
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        elif event.Moving():
            pt = event.GetPosition()
            rect = self.GetRect()

            drw = (rect.GetWidth() - self._iconWidth - self._rightIndent)
            if (
                vertical and
                pt.x > drw or
                not vertical and
                pt.y < (self._iconHeight + self._rightIndent)
            ):
                self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        if send_event:
            event = fpb.CaptionBarEvent(fpb.wxEVT_CAPTIONBAR)
            event.SetId(self.GetId())
            event.SetEventObject(self)
            event.SetBar(self)
            self.GetEventHandler().ProcessEvent(event)

    def OnChar(self, event):
        event.Skip()

    def DoGetBestSize(self):
        if self.IsVertical():
            x, y = self.GetTextExtent(self._caption)
        else:
            y, x = self.GetTextExtent(self._caption)

        if x < self._iconWidth:
            x = self._iconWidth

        if y < self._iconHeight:
            y = self._iconHeight

        return wx.Size(x + fpb.FPB_EXTRA_X, y + fpb.FPB_EXTRA_Y)

    def DrawVerticalGradient(self, dc, rect):
        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)
        col2 = self._style.GetSecondColour()
        col1 = self._style.GetFirstColour()

        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        flrect = float(rect.height)

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0

        for y in range(rect.y, rect.y + rect.height):
            currCol = (r1 + rf, g1 + gf, b1 + bf)

            dc.SetBrush(wx.Brush(currCol, wx.SOLID))
            dc.DrawRectangle(
                rect.x,
                rect.y + (y - rect.y),
                rect.width,
                rect.height
            )
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

    def DrawHorizontalGradient(self, dc, rect):
        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)

        col2 = self._style.GetSecondColour()
        col1 = self._style.GetFirstColour()

        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        flrect = float(rect.width)

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0

        for x in range(rect.x, rect.x + rect.width):
            currCol = (r1 + rf, g1 + gf, b1 + bf)

            dc.SetBrush(wx.Brush(currCol, wx.SOLID))
            dc.DrawRectangle(rect.x + (x - rect.x), rect.y, 1, rect.height)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

    def DrawSingleColour(self, dc, rect):
        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self._style.GetFirstColour(), wx.SOLID))
        dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

    def DrawSingleRectangle(self, dc, rect):
        if rect.height < 2 or rect.width < 1:
            return

        if self._style.GetCaptionStyle() == fpb.CAPTIONBAR_RECTANGLE:
            colour = self.GetParent().GetBackgroundColour()
            br = wx.Brush(colour, wx.SOLID)
        else:
            colour = self._style.GetFirstColour()
            br = wx.Brush(colour, wx.SOLID)

        pen = wx.Pen(self._style.GetSecondColour())
        dc.SetPen(pen)
        dc.SetBrush(br)
        dc.DrawRectangle(
            rect.x,
            rect.y,
            rect.width,
            rect.height - 1
        )

        bgpen = wx.Pen(self.GetParent().GetBackgroundColour())
        dc.SetPen(bgpen)
        dc.DrawLine(
            rect.x, rect.y + rect.height - 1,
            rect.x + rect.width,
            rect.y + rect.height - 1
        )

    def OnSize(self, event):
        if not self._controlCreated:
            event.Skip()
            return

        size = event.GetSize()

        if self._foldIcons:
            rect = wx.Rect(
                size.GetWidth() - self._iconWidth - self._rightIndent,
                0,
                self._iconWidth + self._rightIndent,
                self._iconWidth + self._rightIndent
            )
            diffX = size.GetWidth() - self._oldSize.GetWidth()

            if diffX > 1:
                rect.SetWidth(rect.GetWidth() + diffX + 10)
                rect.SetX(rect.GetX() - diffX - 10)

            self.RefreshRect(rect)

        else:

            rect = self.GetRect()
            self.RefreshRect(rect)

        self._oldSize = size

    def RedrawIconBitmap(self):
        if self._foldIcons:
            rect = self.GetRect()

            rect.SetX(rect.GetWidth() - self._iconWidth - self._rightIndent)
            rect.SetWidth(self._iconWidth + self._rightIndent)
            self.RefreshRect(rect)


def iter_child(parent):
    try:
        for child in parent.GetChildren():
            child.Show()
            iter_child(child)
    except:
        pass


class CheckListBox(wx.Panel):

    def __init__(self, parent, choices, style):
        wx.Panel.__init__(self, parent, -1, style=style)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        l_sizer = wx.BoxSizer(wx.VERTICAL)
        r_sizer = wx.BoxSizer(wx.VERTICAL)

        self.texts = []
        self.ctrls = []

        def add(c, s):
            st = wx.StaticText(self, -1, c)
            ctrl = wx.CheckBox(self, -1, '')
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h_sizer.Add(
                st,
                0,
                wx.EXPAND | wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL,
                5
            )
            h_sizer.AddStretchSpacer(1)
            h_sizer.Add(ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
            self.texts.append(st)
            self.ctrls.append(ctrl)
            s.Add(h_sizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)

        for i, choice in enumerate(choices):
            if i % 2:
                add(choice, r_sizer)

            else:
                add(choice, l_sizer)

        eg.EqualizeWidths(tuple(self.texts))

        sizer.Add(l_sizer, 0, wx.EXPAND | wx.RIGHT, 5)
        sizer.AddStretchSpacer(1)
        sizer.Add(r_sizer, 0, wx.EXPAND)
        sizer.AddStretchSpacer(1)

        self.SetSizer(sizer)

    def SetChecked(self, checks):
        for i in range(len(self.ctrls)):
            if i in checks:
                self.ctrls[i].SetValue(True)
            else:
                self.ctrls[i].SetValue(False)

    def GetChecked(self):
        res = []

        for i, ctrl in enumerate(self.ctrls):
            if ctrl.GetValue():
                res += [i]

        return res

    def SetToolTip(self, index, tooltip):

        if index is None:
            wx.Panel.SetToolTip(self, tooltip)
        else:
            self.texts[index].SetToolTip(tooltip)
            self.ctrls[index].SetToolTip(tooltip)


class FoldPanelItem(wx.Panel):

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        caption="",
        foldIcons=None,
        collapsed=False,
        cbstyle=None
    ):
        wx.Panel.__init__(
            self,
            parent,
            id,
            wx.Point(0, 0),
            style=wx.CLIP_CHILDREN
        )

        self._controlCreated = False
        self._UserSize = 0
        self._PanelSize = 0
        self._LastInsertPos = 0
        self._itemPos = 0
        self._userSized = False

        if foldIcons is None:
            foldIcons = wx.ImageList(16, 16)

            bmp = fpb.ExpandedIcon.GetBitmap()
            foldIcons.Add(bmp)
            bmp = fpb.CollapsedIcon.GetBitmap()
            foldIcons.Add(bmp)

        self._foldIcons = foldIcons
        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        self._captionBar = CaptionBar(
            self,
            wx.ID_ANY,
            wx.Point(0, 0),
            size=wx.DefaultSize,
            caption=caption,
            foldIcons=foldIcons,
            cbstyle=cbstyle
        )

        if collapsed:
            self._captionBar.Collapse()
        self._controlCreated = True

        size = self._captionBar.GetSize()

        if self.IsVertical():
            self.__panel = scrolled.ScrolledPanel(self, -1, style=wx.VSCROLL)
            self.__panel.SetupScrolling(scroll_x=False)
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
            self._PanelSize = size.GetHeight()
        else:
            self.__panel = scrolled.ScrolledPanel(self, -1, style=wx.HSCROLL)
            self.__panel.SetupScrolling(scroll_y=False)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self._PanelSize = size.GetWidth()

        sizer.Add(self._captionBar, 0, wx.EXPAND)
        sizer.Add(self.__panel, 1, wx.EXPAND)
        wx.Panel.SetSizer(self, sizer)
        self.__panel.SetSizer(self.__main_sizer)

        self._LastInsertPos = self._PanelSize
        self._items = []

        self.Bind(fpb.EVT_CAPTIONBAR, self.OnPressCaption)

        if collapsed:
            self.Collapse()
        else:
            self.Expand()

        self.Bind(wx.EVT_SIZE, self.OnSize)

    def SetSizer(self, sizer):
        self.__panel.SetSizer(sizer)

    def SetSizerAndFit(self, sizer):
        self.__panel.SetSizerAndFit(sizer)

    def OnSize(self, event):
        size = event.GetSize()
        caption_size = self._captionBar.GetSize()
        vsize = self.__panel.GetVirtualSize()

        if self._captionBar.IsCollapsed():
            size = caption_size

        else:
            size = (
                size[0] - caption_size[0] - 40,
                size[1] - caption_size[1] - 40
            )

        if self.IsVertical():
            self.__panel.SetVirtualSize((size[0], vsize[1]))
        else:
            self.__panel.SetVirtualSize((vsize[0], size[1]))

        event.Skip()

    def AddWindow(
        self,
        window,
        flags=fpb.FPB_ALIGN_WIDTH,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTSPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTSPACING
    ):
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        if flags | fpb.FPB_ALIGN_WIDTH == flags:
            sizer1.AddStretchSpacer(1)

        sizer2.Add(window, 1, wx.EXPAND | wx.LEFT, leftSpacing)
        sizer1.Add(sizer2, 1, wx.EXPAND | wx.ALL, spacing)

        sizer1.AddStretchSpacer(1)
        self.__main_sizer.Add(sizer1, wx.EXPAND | wx.RIGHT, rightSpacing)

    def AddSeparator(
        self,
        colour=wx.BLACK,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTSPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTSPACING
    ):
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        if self.IsVertical():
            line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        else:
            line = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)

        sizer2.Add(line, 1, wx.EXPAND | wx.LEFT, leftSpacing)
        sizer1.Add(sizer2, 1, wx.EXPAND | wx.ALL, spacing)

        self.__main_sizer.Add(sizer1, wx.EXPAND | wx.RIGHT, rightSpacing)

    def Reposition(self, pos):
        return self.GetPanelLength()

    def OnPressCaption(self, event):
        event.SetTag(self)
        event.Skip()

    def ResizePanel(self):
        self.Layout()
        self.Refresh()
        self.Update()

    def IsVertical(self):
        if isinstance(self.GetParent(), FoldPanelBar):
            return self.GetParent().IsVertical()
        else:
            raise Exception(
                "ERROR: Wrong Parent " + repr(
                    self.GetParent())
            )

    def IsExpanded(self):
        return not self._captionBar.IsCollapsed()

    def Collapse(self):
        for child in self.GetChildren():
            if child not in (self.__panel, self._captionBar):
                child.Reparent(self.__panel)
                child.Show()
                iter_child(child)

        self._captionBar.Collapse()
        self.__panel.Hide()

    def Expand(self):
        self.__panel.Show()
        for child in self.GetChildren():
            if child not in (self.__panel, self._captionBar):
                child.Reparent(self.__panel)
                child.Show()
                iter_child(child)

        self._captionBar.Expand()

    def GetPanelLength(self):
        if self._captionBar.IsCollapsed():
            return self.GetCaptionLength()

        if self.IsVertical():
            return self.GetSize()[1]

        return self.GetSize()[0]

    def GetCaptionLength(self):
        size = self._captionBar.GetSize()
        return (
            self.IsVertical() and [size.GetHeight()] or [size.GetWidth()]
        )[0]

    def ApplyCaptionStyle(self, cbstyle):
        self._captionBar.SetCaptionStyle(cbstyle)

    def GetCaptionStyle(self):
        return self._captionBar.GetCaptionStyle()

    def SetCaptionLabel(self, label):
        self._captionBar._caption = label
        self._captionBar.Refresh()
        self._captionBar.Update()

    def GetCaptionLabel(self):
        return self._captionBar._caption


_fold_panel_window = fpb.FoldWindowItem


class FoldWindowItem(_fold_panel_window):

    def ResizeItem(self, size, vertical=True):
        pass

    def GetWindowLength(self, vertical=True):
        return self._spacing


fpb.FoldWindowItem = FoldWindowItem


class FoldPanelBar(wx.Panel):

    def __init__(
        self,
        parent,
        id=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TAB_TRAVERSAL | wx.NO_BORDER,
        agwStyle=0
    ):

        self._controlCreated = False

        if not agwStyle & (fpb.FPB_HORIZONTAL | fpb.FPB_VERTICAL):
            agwStyle = agwStyle | fpb.FPB_VERTICAL

        if agwStyle & fpb.FPB_HORIZONTAL:
            self._isVertical = False
            sizer = wx.BoxSizer(wx.HORIZONTAL)
        else:
            self._isVertical = True
            sizer = wx.BoxSizer(wx.VERTICAL)

        self._agwStyle = agwStyle

        wx.Panel.__init__(self, parent, id, pos, size, style)
        self.SetSizer(sizer)

        self._controlCreated = True
        self._panels = []

        self.Bind(fpb.EVT_CAPTIONBAR, self.OnPressCaption)

    def AddFoldPanel(
        self,
        caption="",
        collapsed=False,
        foldIcons=None,
        cbstyle=None
    ):

        self.Freeze()

        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        if foldIcons is None:
            foldIcons = wx.ImageList(16, 16)

            bmp = fpb.ExpandedIcon.GetBitmap()
            foldIcons.Add(bmp)
            bmp = fpb.CollapsedIcon.GetBitmap()
            foldIcons.Add(bmp)

        item = FoldPanelItem(self, -1, caption=caption,
            foldIcons=foldIcons,
            collapsed=collapsed, cbstyle=cbstyle)

        sizer = self.GetSizer()
        sizer.Add(item, 1, wx.EXPAND)

        if not collapsed:
            if (
                self._agwStyle & fpb.FPB_SINGLE_FOLD or
                self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD
            ):
                for panel in self._panels:
                    panel.Collapse()

            if self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD:
                self._panels.append(item)
                self.SetSizer(sizer)
                self.RepositionCollapsedToBottom()

        if collapsed and self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD:
            self._panels.append(item)
            self.SetSizer(sizer)
            self.RepositionCollapsedToBottom()

        if item not in self._panels:
            self._panels.append(item)
            self.SetSizer(sizer)

        self.Layout()
        self.Refresh()
        self.Update()

        self.Thaw()

        return item

    def AddFoldPanelWindow(
        self,
        panel,
        window,
        flags=fpb.FPB_ALIGN_WIDTH,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTLINESPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTLINESPACING
    ):
        try:
            item = self._panels.index(panel)
        except:
            raise Exception(
                "ERROR: Invalid Panel Passed "
                "To AddFoldPanelWindow: " + repr(panel)
            )

        panel.AddWindow(window, flags, spacing, leftSpacing, rightSpacing)
        return 0

    def AddFoldPanelSeparator(
        self,
        panel,
        colour=wx.BLACK,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTLINESPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTLINESPACING
    ):
        try:
            item = self._panels.index(panel)
        except:
            raise Exception(
                "ERROR: Invalid Panel Passed To "
                "AddFoldPanelSeparator: " + repr(Panel)
            )

        panel.AddSeparator(colour, spacing, leftSpacing, rightSpacing)
        return 0


    def OnPressCaption(self, event):
        if event.GetFoldStatus():
            self.Collapse(event.GetTag())
        else:
            self.Expand(event.GetTag())

    def RefreshPanelsFrom(self, item):
        try:
            index = self._panels.index(item)
        except:
            raise Exception(
                "ERROR: Invalid Panel Passed To "
                "RefreshPanelsFrom: " + repr(item)
            )

        self.Freeze()
        for i in range(index, len(self._panels)):
            self._panels[i].Refresh()
            self._panels[i].Update()

        self.Thaw()

    def RedisplayFoldPanelItems(self):
        self.Layout()
        self.Refresh()
        self.Update()

    def RepositionCollapsedToBottom(self):
        self.Freeze()
        sizer = self.GetSizer()

        for panel in self._panels:
            sizer.Detach(panel)

        if self.IsVertical():
            sizer = wx.BoxSizer(wx.VERTICAL)
        else:
            sizer = wx.BoxSizer(wx.HORIZONTAL)

        for panel in self._panels:
            if panel.IsExpanded():
                sizer.Add(panel, 1, wx.EXPAND)
                break
        else:
            sizer.AddStretchSpacer(1)

        for panel in self._panels:
            if not panel.IsExpanded():
                sizer.Add(panel, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Thaw()

    def GetPanelsLength(self, collapsed, expanded):
        value = 0
        for j in range(0, len(self._panels)):
            offset = self._panels[j].GetPanelLength()
            value = value + offset
            if self._panels[j].IsExpanded():
                expanded = expanded + offset
            else:
                collapsed = collapsed + offset

        return collapsed, expanded, value

    def Collapse(self, foldpanel):
        try:
            item = self._panels.index(foldpanel)
        except:
            raise Exception(
                "ERROR: Invalid Panel Passed To Collapse: " + repr(foldpanel))

        self.Freeze()

        foldpanel.Collapse()
        if self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD:
            self.RepositionCollapsedToBottom()

        self.Layout()
        self.Refresh()
        self.Update()

        self.Thaw()

    def Expand(self, foldpanel):

        self.Freeze()
        if (
            self._agwStyle & fpb.FPB_SINGLE_FOLD or
            self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD
        ):
            for panel in self._panels:
                panel.Collapse()

        foldpanel.Expand()

        if self._agwStyle & fpb.FPB_EXCLUSIVE_FOLD:
            self.RepositionCollapsedToBottom()
        self.Layout()
        self.Refresh()
        self.Update()

        self.Thaw()

    def ApplyCaptionStyle(self, foldpanel, cbstyle):
        foldpanel.ApplyCaptionStyle(cbstyle)

    def ApplyCaptionStyleAll(self, cbstyle):
        for panels in self._panels:
            self.ApplyCaptionStyle(panels, cbstyle)

    def GetCaptionStyle(self, foldpanel):
        return foldpanel.GetCaptionStyle()

    def IsVertical(self):
        return self._isVertical

    def GetFoldPanel(self, item):
        try:
            ind = self._panels[item]
            return self._panels[item]
        except:
            raise Exception(
                "ERROR: List Index Out Of Range Or Bad Item Passed: " +
                repr(item) +
                ". Item Should Be An Integer Between " +
                repr(0) +
                " And " +
                repr(len(self._panels))
            )

    def GetCount(self):
        try:
            return len(self._panels)
        except:
            raise Exception("ERROR: No Panels Have Been Added To FoldPanelBar")


class AdapterListCtrl(FoldPanelBar):

    def __init__(self, parent):
        self.__adapter_data = []
        FoldPanelBar.__init__(
            self,
            parent,
            -1,
            size=(450, 500),
            agwStyle=(
                fpb.FPB_VERTICAL | fpb.FPB_EXCLUSIVE_FOLD
            )
        )

        self.__parent = parent
        #
        # def on_size(evt):
        #     self.RedisplayFoldPanelItems()
        #     evt.Skip()
        #
        # parent.Bind(wx.EVT_SIZE, on_size)

    def __iter__(self):
        for adapter_data in self.__adapter_data:
            yield adapter_data

    def get_value(self):
        res = ()

        for item in self.__adapter_data:
            value = item.value
            if value is not None:
                res += (value,)
        return res

    def add_adapter(self, adapter):
        fold_panel = self.AddFoldPanel(
            adapter.name,
            collapsed=True,
            foldIcons=IMAGE_LIST
        )

        adapter.parent = fold_panel
        panel = fold_panel

        style = fpb.CaptionBarStyle()

        first_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        second_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNSHADOW)

        style.SetFirstColour(first_colour)
        style.SetSecondColour(second_colour)

        fold_panel.ApplyCaptionStyle(style)

        def h_sizer(ctrl1, ctrl2, tooltip=None, prop=1):
            tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)

            if not isinstance(ctrl1, wx.Sizer):
                prop = 0
                ctrl1 = wx.StaticText(panel, -1, ctrl1 + ':')
                # ctrl1.Show(False)
                if tooltip is not None:
                    ctrl1.SetToolTip(tooltip)

            tmp_sizer.Add(ctrl1, 0, wx.EXPAND | wx.ALL, 5)

            tmp_sizer.Add(ctrl2, 0, wx.EXPAND | wx.ALL, 5)
            return ctrl1, ctrl2, tmp_sizer

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        adapter_box = wx.StaticBox(panel, -1, "Adapter Settings")
        adapter_sizer = wx.StaticBoxSizer(adapter_box, wx.VERTICAL)

        name_st, name_ctrl, name_sizer = h_sizer(
            Text.adapter_name_header,
            adapter[0],
            Text.adapter_name_tooltip
        )

        port_st, port_ctrl, port_sizer = h_sizer(
                Text.adapter_port_header,
                adapter[1],
                Text.adapter_port_tooltip
            )

        type_st, type_ctrl, type_sizer = h_sizer(
                Text.adapter_type_header,
                adapter[2],
                Text.adapter_type_tooltip
            )

        hdmi_st, hdmi_ctrl, hdmi_sizer = h_sizer(
                Text.hdmi_header,
                adapter[7],
                Text.hdmi_tooltip,
            )

        hdmi_sizer2 = wx.BoxSizer(wx.VERTICAL)
        hdmi_sizer2.Add(hdmi_sizer)
        hdmi_sizer2.AddStretchSpacer(1)

        eg.EqualizeWidths((name_st, type_st))
        eg.EqualizeWidths((name_ctrl, type_ctrl))

        eg.EqualizeWidths((port_st, hdmi_st))
        eg.EqualizeWidths((port_ctrl, hdmi_ctrl))

        adapter_line_1 = name_sizer
        adapter_line_2 = h_sizer(port_sizer, hdmi_sizer2)[2]
        adapter_line_3 = type_sizer

        adapter_sizer.Add(adapter_line_1, 0, wx.EXPAND)
        adapter_sizer.Add(adapter_line_2, 0, wx.EXPAND)
        adapter_sizer.Add(adapter_line_3, 0, wx.EXPAND)

        audio_box = wx.StaticBox(panel, -1, "Audio Settings")
        audio_sizer = wx.StaticBoxSizer(audio_box, wx.VERTICAL)

        avr_st, avr_ctrl, avr_sizer = h_sizer(
            Text.avr_audio_header,
            adapter[5],
            Text.avr_audio_tooltip
        )

        wake_st, wake_ctrl, wake_sizer = h_sizer(
            Text.wake_avr_header,
            adapter[6],
            Text.wake_avr_tooltip
        )

        audio_line_1 = h_sizer(avr_sizer, wake_sizer)[2]
        audio_sizer.Add(audio_line_1, 0, wx.EXPAND)

        power_box = wx.StaticBox(panel, -1, "PC Power Settings")
        power_sizer = wx.StaticBoxSizer(power_box, wx.VERTICAL)

        off_st, off_ctrl, off_sizer = h_sizer(
            Text.power_off_header,
            adapter[3],
            Text.power_off_tooltip
        )

        standby_st, standby_ctrl, standby_sizer = h_sizer(
            Text.power_standby_header,
            adapter[4],
            Text.power_standby_tooltip
        )

        power_line_1 = h_sizer(off_sizer, standby_sizer)[2]
        power_sizer.Add(power_line_1, 0, wx.EXPAND)

        eg.EqualizeWidths((avr_st, off_st))
        eg.EqualizeWidths((wake_st, standby_st))

        remote_box = wx.StaticBox(panel, -1, "Remote Keypress Settings")
        remote_sizer = wx.StaticBoxSizer(remote_box, wx.VERTICAL)

        timeout_st, timeout_ctrl, timeout_sizer = h_sizer(
            Text.keypress_combo_timeout_header,
            adapter[9],
            Text.keypress_combo_timeout_tooltip
        )

        repeat_st, repeat_ctrl, repeat_sizer = h_sizer(
            Text.keypress_repeat_header,
            adapter[10],
            Text.keypress_repeat_tooltip
        )

        double_st, double_ctrl, double_sizer = h_sizer(
            Text.keypress_double_tap_header,
            adapter[12],
            Text.keypress_double_tap_tooltip
        )

        release_st, release_ctrl, release_sizer = h_sizer(
            Text.keypress_release_header,
            adapter[11],
            Text.keypress_release_delay_tooltip
        )

        eg.EqualizeWidths((timeout_st, double_st))
        eg.EqualizeWidths((timeout_ctrl, double_ctrl))

        eg.EqualizeWidths((repeat_st, release_st))
        eg.EqualizeWidths((repeat_ctrl, release_ctrl))

        remote_line_1 = h_sizer(
            Text.keypress_combo_header,
            adapter[8],
            Text.keypress_combo_tooltip
        )[2]

        remote_line_2 = h_sizer(timeout_sizer, repeat_sizer)[2]
        remote_line_3 = h_sizer(double_sizer, release_sizer)[2]

        remote_sizer.Add(remote_line_1, 0, wx.EXPAND)
        remote_sizer.Add(remote_line_2, 0, wx.EXPAND)
        remote_sizer.Add(remote_line_3, 0, wx.EXPAND)

        log_box = wx.StaticBox(panel, -1, "Log Settings")
        log_sizer = wx.StaticBoxSizer(log_box, wx.VERTICAL)
        log_sizer.Add(adapter[13], 0, wx.EXPAND)

        dummy_item = wx.StaticText(panel, -1, '')
        main_sizer.Add(dummy_item)
        main_sizer.Add(adapter_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(audio_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(power_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(remote_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(log_sizer, 0, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(main_sizer)

        self.__adapter_data += [adapter]

        def on_name(evt):
            fold_panel.SetCaptionLabel(evt.GetString())
            evt.Skip()

        adapter[0].Bind(wx.EVT_TEXT, on_name)
        self.Expand(fold_panel)


class AdapterConfig(object):

    def __init__(
        self,
        name
    ):
        self.__connected = None
        self.name = name
        self.__name_ctrl = None
        self.__port_ctrl = None
        self.__type_ctrl = None
        self.__power_off_ctrl = None
        self.__power_standby_ctrl = None
        self.__avr_audio_ctrl = None
        self.__wake_avr_ctrl = None
        self.__hdmi_ctrl = None
        self.__combo_ctrl = None
        self.__combo_timeout_ctrl = None
        self.__keypress_repeat_ctrl = None
        self.__keypress_release_ctrl = None
        self.__keypress_double_ctrl = None
        self.__logging_ctrl = None
        self.__parent = None

        self.__connected_thread = None
        self.__connected_event = threading.Event()

    def parent(self, fold_panel):
        parent = wx.Panel(fold_panel, -1)
        self.__parent = fold_panel

        cec_lib = cec.ICECAdapter.Create(cec.libcec_configuration())

        type_choices = list(
            cec_lib.DeviceTypeToString(i).title()
            for i in range(1, 5)
        )
        cec_lib.Close()

        self.__name_ctrl = wx.TextCtrl(parent, -1, 'Enter Name')
        self.__port_ctrl = wx.StaticText(parent, -1, '')
        self.__power_off_ctrl = wx.CheckBox(parent, -1, '')
        self.__power_standby_ctrl = wx.CheckBox(parent, -1, '')
        self.__avr_audio_ctrl = wx.CheckBox(parent, -1, '')
        self.__wake_avr_ctrl = wx.CheckBox(parent, -1, '')
        self.__hdmi_ctrl = eg.SpinIntCtrl(parent, value=0, max=15)
        self.__combo_timeout_ctrl = eg.SpinIntCtrl(parent, value=500)
        self.__keypress_repeat_ctrl = eg.SpinIntCtrl(parent, value=65)
        self.__keypress_release_ctrl = eg.SpinIntCtrl(parent, value=200)
        self.__keypress_double_ctrl = eg.SpinIntCtrl(parent, value=100)

        self.__logging_ctrl = CheckListBox(
            parent,
            [
                Text.info_header,
                Text.notice_header,
                Text.warning_header,
                Text.error_header,
                Text.debug_header,
                Text.log_file_header
            ],
            style=wx.BORDER_NONE
        )
        self.__type_ctrl = CheckListBox(
            parent,
            type_choices,
            style=wx.SUNKEN_BORDER
        )

        self.__combo_ctrl = wx.Choice(
            parent,
            -1,
            choices=sorted(KEY_CODES.keys())
        )

        self.__combo_ctrl.SetStringSelection(KEY_CODES[0x71])
        self.__type_ctrl.SetChecked([0])

        self.__name_ctrl.SetToolTip(Text.adapter_name_tooltip)
        self.__port_ctrl.SetToolTip(Text.adapter_port_tooltip)
        self.__type_ctrl.SetToolTip(None, Text.adapter_type_tooltip)
        self.__wake_avr_ctrl.SetToolTip(Text.wake_avr_tooltip)
        self.__hdmi_ctrl.numCtrl.SetToolTip(Text.hdmi_tooltip)
        self.__avr_audio_ctrl.SetToolTip(Text.avr_audio_tooltip)
        self.__power_off_ctrl.SetToolTip(Text.power_off_tooltip)
        self.__combo_ctrl.SetToolTip(Text.keypress_combo_tooltip)
        self.__power_standby_ctrl.SetToolTip(Text.power_standby_tooltip)
        self.__combo_timeout_ctrl.numCtrl.SetToolTip(
            Text.keypress_combo_timeout_tooltip
        )
        self.__keypress_repeat_ctrl.numCtrl.SetToolTip(
            Text.keypress_repeat_tooltip
        )
        self.__keypress_release_ctrl.numCtrl.SetToolTip(
            Text.keypress_release_delay_tooltip
        )
        self.__keypress_double_ctrl.numCtrl.SetToolTip(
            Text.keypress_double_tap_tooltip
        )

        self.__logging_ctrl.SetToolTip(0, Text.info_tooltip)
        self.__logging_ctrl.SetToolTip(1, Text.notice_tooltip)
        self.__logging_ctrl.SetToolTip(2, Text.warning_tooltip)
        self.__logging_ctrl.SetToolTip(3, Text.error_tooltip)
        self.__logging_ctrl.SetToolTip(4, Text.debug_tooltip)
        self.__logging_ctrl.SetToolTip(5, Text.log_file_tooltip)

        def on_power_off(evt):
            if evt.IsChecked():
                self.__power_standby_ctrl.SetValue(False)
            evt.Skip()

        self.__power_off_ctrl.Bind(wx.EVT_CHECKBOX, on_power_off)

        def on_power_standby(evt):
            if evt.IsChecked():
                self.__power_off_ctrl.SetValue(False)
            evt.Skip()

        self.__power_standby_ctrl.Bind(wx.EVT_CHECKBOX, on_power_standby)

        for child in parent.GetChildren():
            child.Show(False)
            child.Reparent(fold_panel)
        parent.Destroy()

    parent = property(fset=parent)

    def __getitem__(self, item):
        items = (
            self.__name_ctrl,
            self.__port_ctrl,
            self.__type_ctrl,
            self.__power_off_ctrl,
            self.__power_standby_ctrl,
            self.__avr_audio_ctrl,
            self.__wake_avr_ctrl,
            self.__hdmi_ctrl,
            self.__combo_ctrl,
            self.__combo_timeout_ctrl,
            self.__keypress_repeat_ctrl,
            self.__keypress_release_ctrl,
            self.__keypress_double_ctrl,
            self.__logging_ctrl
        )
        return items[item]

    @property
    def value(self):
        name = self.adapter_name
        if name and name != 'Enter Name':
            return (
                self.adapter_name,
                self.adapter_port,
                self.adapter_types,
                self.hdmi_port,
                self.power_off,
                self.power_standby,
                self.avr_audio,
                self.wake_avr,
                self.keypress_combo,
                self.keypress_combo_timeout,
                self.keypress_repeat,
                self.keypress_release_delay,
                self.keypress_double_tap,
                self.log_info,
                self.log_notice,
                self.log_warning,
                self.log_error,
                self.log_debug,
                self.log_file
            )

    @property
    def connected(self):
        return self.__connected

    @connected.setter
    def connected(self, value):
        if value:
            if self.__connected_thread is not None:
                self.__connected_event.set()
                self.__connected_thread.join()

            self.__connected = True
        else:
            while self.__connected_event.isSet():
                pass

            def do():
                style = self.__parent.GetCaptionStyle()
                colour = style.GetSecondColour().Get(False)

                current_red = float(colour[0])
                current_green = float(colour[1])
                current_blue = float(colour[2])

                red_steps = (255 - current_red) / 3
                red_increment = 3
                green_increment = -(current_green / red_steps)
                blue_increment = -(current_blue / red_steps)

                while not self.__connected_event.isSet():
                    try:
                        current_red += red_increment

                        if colour[0] > current_red or current_red > 255:
                            red_increment = -red_increment
                            green_increment = -green_increment
                            blue_increment = -blue_increment
                            current_red += red_increment

                        current_green += green_increment
                        current_blue += blue_increment

                        if current_green < 0.0:
                            current_green = 0.0

                        if current_blue < 0.0:
                            current_blue = 0.0

                        if current_green > 255.0:
                            current_green = 255.0

                        if current_blue > 255.0:
                            current_blue = 255.0

                        new_colour = wx.Colour(
                            int(current_red),
                            int(current_green),
                            int(current_blue)
                        )

                        style.SetSecondColour(new_colour)
                        self.__parent._captionBar.Refresh()
                        self.__parent._captionBar.Update()
                    except:
                        self.__connected_event.set()
                    self.__connected_event.wait(0.05)

                try:
                    style.SetSecondColour(wx.Colour(*colour))
                    self.__parent._captionBar.Refresh()
                    self.__parent._captionBar.Update()
                except:
                    pass

                self.__connected_thread = None
                self.__connected_event.clear()

            self.__connected_thread = threading.Thread(target=do)
            self.__connected_thread.daemon = True
            self.__connected_thread.start()

    @property
    def log_file(self):
        return 5 in self.__logging_ctrl.GetChecked()

    @log_file.setter
    def log_file(self, value):
        if value:
            self.__logging_ctrl.SetChecked([5])

    @property
    def log_info(self):
        return 0 in self.__logging_ctrl.GetChecked()

    @log_info.setter
    def log_info(self, value):
        if value:
            self.__logging_ctrl.SetChecked([0])

    @property
    def log_notice(self):
        return 1 in self.__logging_ctrl.GetChecked()

    @log_notice.setter
    def log_notice(self, value):
        if value:
            self.__logging_ctrl.SetChecked([1])

    @property
    def log_warning(self):
        return 2 in self.__logging_ctrl.GetChecked()

    @log_warning.setter
    def log_warning(self, value):
        if value:
            self.__logging_ctrl.SetChecked([2])

    @property
    def log_error(self):
        return 3 in self.__logging_ctrl.GetChecked()

    @log_error.setter
    def log_error(self, value):
        if value:
            self.__logging_ctrl.SetChecked([3])

    @property
    def log_debug(self):
        return 4 in self.__logging_ctrl.GetChecked()

    @log_debug.setter
    def log_debug(self, value):
        if value:
            self.__logging_ctrl.SetChecked([4])

    @property
    def adapter_name(self):
        return self.__name_ctrl.GetValue()

    @adapter_name.setter
    def adapter_name(self, value):
        self.__name_ctrl.SetValue(value)

    @property
    def adapter_port(self):
        return self.__port_ctrl.GetLabel()

    @adapter_port.setter
    def adapter_port(self, value):
        self.__port_ctrl.SetLabel(value)

    @property
    def adapter_types(self):
        return list(value + 1 for value in self.__type_ctrl.GetChecked())

    @adapter_types.setter
    def adapter_types(self, values):
        if not isinstance(values, (list, tuple)):
            values = [values]

        values = list(value - 1 for value in values)

        self.__type_ctrl.SetChecked(values)

    @property
    def hdmi_port(self):
        value = self.__hdmi_ctrl.GetValue()
        if value:
            return value

    @hdmi_port.setter
    def hdmi_port(self, value):
        self.__hdmi_ctrl.SetValue(value if value is not None else 0)

    @property
    def power_off(self):
        return self.__power_off_ctrl.GetValue()

    @power_off.setter
    def power_off(self, value):
        self.__power_off_ctrl.SetValue(value)
        if value:
            self.__power_standby_ctrl.SetValue(False)

    @property
    def power_standby(self):
        return self.__power_standby_ctrl.GetValue()

    @power_standby.setter
    def power_standby(self, value):
        self.__power_standby_ctrl.SetValue(value)
        if value:
            self.__power_off_ctrl.SetValue(False)

    @property
    def avr_audio(self):
        return self.__avr_audio_ctrl.GetValue() and self.avr_audio_enable

    @avr_audio.setter
    def avr_audio(self, value):
        self.__avr_audio_ctrl.SetValue(value)

    @property
    def avr_audio_enable(self):
        return self.__avr_audio_ctrl.IsEnabled()

    @avr_audio_enable.setter
    def avr_audio_enable(self, value):
        self.__avr_audio_ctrl.Enable(value)
        self.wake_avr = False
        self.__wake_avr_ctrl.Enable(value)

    @property
    def wake_avr(self):
        return self.__wake_avr_ctrl.GetValue() and self.avr_audio_enable

    @wake_avr.setter
    def wake_avr(self, value):
        self.__wake_avr_ctrl.SetValue(value)

    @property
    def keypress_combo(self):
        return KEY_CODES[self.__combo_ctrl.GetStringSelection()]

    @keypress_combo.setter
    def keypress_combo(self, value):
        self.__combo_ctrl.SetStringSelection(KEY_CODES[value])

    @property
    def keypress_combo_timeout(self):
        return self.__combo_timeout_ctrl.GetValue()

    @keypress_combo_timeout.setter
    def keypress_combo_timeout(self, value):
        self.__combo_timeout_ctrl.SetValue(value)

    @property
    def keypress_repeat(self):
        return self.__keypress_repeat_ctrl.GetValue()

    @keypress_repeat.setter
    def keypress_repeat(self, value):
        self.__keypress_repeat_ctrl.SetValue(value)

    @property
    def keypress_release_delay(self):
        return self.__keypress_release_ctrl.GetValue()

    @keypress_release_delay.setter
    def keypress_release_delay(self, value):
        self.__keypress_release_ctrl.SetValue(value)

    @property
    def keypress_double_tap(self):
        return self.__keypress_double_ctrl.GetValue()

    @keypress_double_tap.setter
    def keypress_double_tap(self, value):
        self.__keypress_double_ctrl.SetValue(value)


class AdapterCtrl(wx.Panel):

    def __init__(self, parent, com_port, adapter_name, adapters):
        wx.Panel.__init__(self, parent, -1)

        choices = list(
            '{0} : {1} : {2}'.format(
                adapter.lib_cec_device.osd_name,
                adapter.port,
                adapter.lib_cec_device.name
            )
            for adapter in adapters
        )

        if adapter_name is None and len(adapters) > 1:
            choices.insert(0, '')
            adapter_name = ''

        adapters_st = wx.StaticText(self, -1, Text.adapter_lbl)
        adapters_ctrl = eg.Choice(self, 0, choices=sorted(choices))

        if adapter_name:
            for choice in choices:
                if adapter_name in choice and com_port in choice:
                    adapters_ctrl.SetStringSelection(choice)
                    break
                if adapter_name in choice:
                    adapters_ctrl.SetStringSelection(choice)
                    break
                if com_port in choice:
                    adapters_ctrl.SetStringSelection(choice)
                    break
            else:
                adapters_ctrl.SetSelection(0)
        else:
            adapters_ctrl.SetSelection(0)

            if '' in choices:

                def on_choice(evt):
                    choices.remove('')
                    value = adapters_ctrl.GetStringSelection()
                    adapters_ctrl.Clear()
                    adapters_ctrl.AppendItems(choices)
                    adapters_ctrl.SetStringSelection(value)
                    adapters_ctrl.Unbind(wx.EVT_CHOICE, handler=on_choice)
                    evt.Skip()

                adapters_ctrl.Bind(wx.EVT_CHOICE, on_choice)

        def get_value():
            value = adapters_ctrl.GetStringSelection()
            if value:
                a_name, c_port, d_name = value.split(' : ')
                return c_port, a_name

            return None, None

        adapters_sizer = wx.BoxSizer(wx.HORIZONTAL)
        adapters_sizer.Add(adapters_st, 0, wx.EXPAND | wx.ALL, 5)
        adapters_sizer.Add(adapters_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        self.GetValue = get_value
        self.SetSizer(adapters_sizer)


class DeviceCtrl(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        device_st = wx.StaticText(self, -1, Text.device_lbl)
        device_ctrl = eg.Choice(self, 0, choices=[])
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(device_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        def update_devices(adapter, dev_name=None):
            if adapter is not None:
                if dev_name is None:
                    if device_ctrl.GetItems():
                        dev_name = device_ctrl.GetStringSelection()
                    else:
                        dev_name = ''

                choices = list(d.osd_name for d in adapter)
                device_ctrl.SetItems(choices)

                if dev_name in choices:
                    device_ctrl.SetStringSelection(dev_name)
                else:
                    device_ctrl.SetSelection(0)

        def get_value():
            return device_ctrl.GetStringSelection()

        self.GetValue = get_value
        self.UpdateDevices = update_devices
        self.SetSizer(sizer)
