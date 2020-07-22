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
import os
from time import clock
from wx import aui
from wx.lib import scrolledpanel

import pyIRDecoder
from pyIRDecoder import ir_code
from pyIRDecoder import protocol_base

# Local imports
import eg
from eg.WinApi.Dynamic import SendMessageTimeout


def v_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer


def h_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)

    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer


class Config(eg.PersistentData):
    IrDecoderPane = None
    CodeInfoPane = None
    OriginalCodePane = None
    NormalizedCodePane = None
    OriginalOscilloscopePane = None
    MCEOscilloscopePane = None


class CodePanelBase(scrolledpanel.ScrolledPanel):

    def __init__(self, parent):
        scrolledpanel.ScrolledPanel.__init__(
            self,
            parent,
            -1,
            style=wx.BORDER_NONE
        )
        self.rlc_ctrl = RLCPanel(self)
        self.pronto_ctrl = ProntoPanel(self)
        self.mce_rlc_ctrl = RLCPanel(self)
        self.mce_pronto_ctrl = ProntoPanel(self)

        rlc_sizer = eg.BoxedGroup(
            self,
            'Run-Length Code',
        )
        rlc_sizer.Add(self.rlc_ctrl, 0, wx.EXPAND)

        mce_rlc_sizer = eg.BoxedGroup(
            self,
            'Run-Length Code',
        )
        mce_rlc_sizer.Add(self.mce_rlc_ctrl, 0, wx.EXPAND)

        mce_sizer = eg.BoxedGroup(
            self,
            'Media Center Edition (MCE) Code'
        )

        mce_sizer.Add(mce_rlc_sizer, 0, wx.EXPAND)
        mce_sizer.Add(self.mce_pronto_ctrl, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(rlc_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.pronto_ctrl, 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(mce_sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)

        self.SetupScrolling(scroll_x=False, scroll_y=True)

    def SetValue(self, value):
        raise NotImplementedError


class OriginalCodePanel(CodePanelBase):

    def SetValue(self, value):
        if value is None:
            self.rlc_ctrl.SetValue([])
            self.pronto_ctrl.SetValue('')

            self.mce_rlc_ctrl.SetValue([])
            self.mce_pronto_ctrl.SetValue('')
        else:
            self.rlc_ctrl.SetValue(value.original_rlc)
            self.pronto_ctrl.SetValue(value.original_rlc_pronto)

            self.mce_rlc_ctrl.SetValue(value.original_mce_rlc)
            self.mce_pronto_ctrl.SetValue(value.original_mce_pronto)


class NormalizedCodePanel(CodePanelBase):

    def SetValue(self, value):
        if value is None:
            self.rlc_ctrl.SetValue([])
            self.pronto_ctrl.SetValue('')

            self.mce_rlc_ctrl.SetValue([])
            self.mce_pronto_ctrl.SetValue('')
        else:
            self.rlc_ctrl.SetValue(value.normalized_rlc)
            self.pronto_ctrl.SetValue(value.normalized_rlc_pronto)

            self.mce_rlc_ctrl.SetValue(value.normalized_mce_rlc)
            self.mce_pronto_ctrl.SetValue(value.normalized_mce_pronto)


class ProntoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)

        pronto_label = wx.StaticText(self, -1, 'Pronto')
        self.pronto_ctrl = wx.TextCtrl(
            self,
            -1,
            '',
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP
        )
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pronto_label, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.pronto_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)

    def SetValue(self, value):
        self.pronto_ctrl.SetValue(value)


class RLCPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)

        frame0_label = wx.StaticText(self, -1, 'Frame 0')
        self.frame0_ctrl = wx.TextCtrl(
            self,
            -1,
            '',
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP
        )
        frame0_sizer = v_sizer(frame0_label, self.frame0_ctrl)

        frame1_label = wx.StaticText(self, -1, 'Frame 1')
        self.frame1_ctrl = wx.TextCtrl(
            self,
            -1,
            '',
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP
        )
        frame1_sizer = v_sizer(frame1_label, self.frame1_ctrl)

        frame2_label = wx.StaticText(self, -1, 'Frame 2')
        self.frame2_ctrl = wx.TextCtrl(
            self,
            -1,
            '',
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP
        )
        frame2_sizer = v_sizer(frame2_label, self.frame2_ctrl)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(frame0_sizer, 0, wx.EXPAND)
        sizer.Add(frame1_sizer, 0, wx.EXPAND)
        sizer.Add(frame2_sizer, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def SetValue(self, value):
        while len(value) < 3:
            value += [[]]

        def _do(itm):
            if itm > 0:
                return '+' + str(itm)
            return str(itm)

        code = list(', '.join(_do(item) for item in items) for items in value)

        self.frame0_ctrl.SetValue(code[0])

        if len(code) > 1:
            self.frame1_ctrl.SetValue(code[1])
        else:
            self.frame1_ctrl.SetValue('')

        if len(code) > 2:
            self.frame2_ctrl.SetValue(code[2])
        else:
            self.frame2_ctrl.SetValue('')


class InfoPanel(scrolledpanel.ScrolledPanel):
    def __init__(self, parent, icon):
        scrolledpanel.ScrolledPanel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        self.icon = icon
        name_label = wx.StaticText(self, -1, 'Name:')
        self.name_ctrl = wx.TextCtrl(self, -1, ' ' * 15)
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_sizer.Add(name_label, 0, wx.EXPAND | wx.ALL, 5)
        name_sizer.Add(self.name_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        protocol_label = wx.StaticText(self, -1, 'Protocol:')
        self.protocol_ctrl = wx.TextCtrl(self, -1, ' ' * 32, style=wx.TE_READONLY)
        protocol_sizer = h_sizer(protocol_label, self.protocol_ctrl)

        frequency_label = wx.StaticText(self, -1, 'Frequency:')
        frequency_suffix = wx.StaticText(self, -1, 'hz')
        self.frequency_ctrl = wx.TextCtrl(self, -1, '00000', style=wx.TE_READONLY)
        frequency_sizer = h_sizer(frequency_label, self.frequency_ctrl, frequency_suffix)

        bit_label = wx.StaticText(self, -1, 'Bit Count:')
        self.bit_ctrl = wx.TextCtrl(self, -1, '  0', style=wx.TE_READONLY)
        bit_sizer = h_sizer(bit_label, self.bit_ctrl)

        hex_label = wx.StaticText(self, -1, 'Code as Hexadecimal:')
        self.hex_ctrl = wx.TextCtrl(self, -1, ' ' * 32, style=wx.TE_READONLY)
        hex_sizer = h_sizer(hex_label, self.hex_ctrl)

        integer_label = wx.StaticText(self, -1, 'Code as Integer:')
        self.integer_ctrl = wx.TextCtrl(self, -1, ' ' * 32, style=wx.TE_READONLY)
        integer_sizer = h_sizer(integer_label, self.integer_ctrl)

        parameter_label = wx.StaticText(self, -1, 'Parameters:')
        self.parameter_ctrl = wx.TextCtrl(
            self,
            -1,
            '\n' * 3,
            style=wx.TE_MULTILINE | wx.TE_READONLY
        )
        parameter_sizer = h_sizer(parameter_label, self.parameter_ctrl)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(name_sizer, 0, wx.EXPAND)
        right_sizer.Add(protocol_sizer, 0, wx.EXPAND)
        right_sizer.Add(frequency_sizer, 0, wx.EXPAND)
        right_sizer.Add(bit_sizer, 0, wx.EXPAND)
        right_sizer.Add(hex_sizer, 0, wx.EXPAND)
        right_sizer.Add(integer_sizer, 0, wx.EXPAND)
        right_sizer.Add(parameter_sizer, 1, wx.EXPAND)

        self.code = None
        self.original_oscope_pane = None
        self.mce_oscope_pane = None
        self.original_code_pane = None
        self.normalized_code_pane = None
        self.mce_code_pane = None

        original_code_button = wx.Button(self, -1, 'Original Code', size=(150, 25))
        original_code_button.Bind(wx.EVT_BUTTON, self.on_original_code)

        normalized_code_button = wx.Button(self, -1, 'Normalized Code', size=(150, 25))
        normalized_code_button.Bind(wx.EVT_BUTTON, self.on_normalized_code)

        original_oscope_button = wx.Button(self, -1, 'Original Oscilloscope', size=(150, 25))
        original_oscope_button.Bind(wx.EVT_BUTTON, self.on_original_oscope)

        mce_oscope_button = wx.Button(self, -1, 'MCE Oscilloscope', size=(150, 25))
        mce_oscope_button.Bind(wx.EVT_BUTTON, self.on_mce_oscope)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(original_code_button, 0, wx.EXPAND | wx.BOTTOM, 5)
        left_sizer.Add(normalized_code_button, 0, wx.EXPAND | wx.BOTTOM, 5)
        left_sizer.Add(original_oscope_button, 0, wx.EXPAND | wx.BOTTOM, 5)
        left_sizer.Add(mce_oscope_button, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(left_sizer, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 10)
        sizer.Add(right_sizer, 1, wx.EXPAND)

        self.manager = aui.AuiManager.GetManager(eg.mainFrame)

        eg.EqualizeWidths((
            name_label,
            protocol_label,
            frequency_label,
            bit_label,
            hex_label,
            integer_label,
            parameter_label
        ))

        self.SetSizer(sizer)
        self.SetupScrolling(scroll_x=False, scroll_y=True)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)

    def on_original_oscope(self, _):
        if self.original_oscope_pane is None:
            self.original_oscope_pane = OriginalOscilloscopePane(self.icon)
            self.original_oscope_pane.SetValue(self.code)
            self.manager.AddPane(self.original_oscope_pane.ctrl, self.original_oscope_pane)

            def _on_close(evt):
                pane = evt.GetPane()
                if pane == self.original_oscope_pane:
                    eg.mainFrame.Unbind(aui.EVT_AUI_PANE_CLOSE, handler=_on_close)

                    pane_info = self.manager.SavePaneInfo(pane)
                    setattr(Config, pane.__name__, pane_info)
                    pane.ctrl.Hide()
                    pane.Hide()
                    self.manager.DetachPane(pane.ctrl)
                    pane.ctrl.Destroy()

                    self.original_oscope_pane = None
                    self.manager.Update()

            eg.mainFrame.Bind(aui.EVT_AUI_PANE_CLOSE, _on_close)

        else:
            self.original_oscope_pane.Show()

        self.manager.Update()

    def on_mce_oscope(self, _):
        if self.mce_oscope_pane is None:
            self.mce_oscope_pane = MCEOscilloscopePane(self.icon)
            self.mce_oscope_pane.SetValue(self.code)
            self.manager.AddPane(self.mce_oscope_pane.ctrl, self.mce_oscope_pane)

            def _on_close(evt):
                pane = evt.GetPane()
                if pane == self.mce_oscope_pane:
                    eg.mainFrame.Unbind(aui.EVT_AUI_PANE_CLOSE, handler=_on_close)

                    pane_info = self.manager.SavePaneInfo(pane)
                    setattr(Config, pane.__name__, pane_info)
                    pane.ctrl.Hide()
                    pane.Hide()
                    self.manager.DetachPane(pane.ctrl)
                    pane.ctrl.Destroy()

                    self.mce_oscope_pane = None
                    self.manager.Update()

            eg.mainFrame.Bind(aui.EVT_AUI_PANE_CLOSE, _on_close)

        else:
            self.mce_oscope_pane.Show()

        self.manager.Update()

    def on_original_code(self, _):
        if self.original_oscope_pane is None:
            self.original_code_pane = OriginalCodePane(self.icon)
            self.original_code_pane.SetValue(self.code)
            self.manager.AddPane(self.original_code_pane.ctrl, self.original_code_pane)

            def _on_close(evt):
                pane = evt.GetPane()
                if pane == self.original_code_pane:
                    eg.mainFrame.Unbind(aui.EVT_AUI_PANE_CLOSE, handler=_on_close)

                    pane_info = self.manager.SavePaneInfo(pane)
                    setattr(Config, pane.__name__, pane_info)
                    pane.ctrl.Hide()
                    pane.Hide()
                    self.manager.DetachPane(pane.ctrl)
                    pane.ctrl.Destroy()

                    self.original_code_pane = None
                    self.manager.Update()

            eg.mainFrame.Bind(aui.EVT_AUI_PANE_CLOSE, _on_close)

        else:
            self.original_code_pane.Show()

        self.manager.Update()

    def on_normalized_code(self, _):
        if self.normalized_code_pane is None:
            self.normalized_code_pane = NormalizedCodePane(self.icon)
            self.normalized_code_pane.SetValue(self.code)
            self.manager.AddPane(self.normalized_code_pane.ctrl, self.normalized_code_pane)

            def _on_close(evt):
                pane = evt.GetPane()
                if pane == self.normalized_code_pane:
                    eg.mainFrame.Unbind(aui.EVT_AUI_PANE_CLOSE, handler=_on_close)

                    pane_info = self.manager.SavePaneInfo(pane)
                    setattr(Config, pane.__name__, pane_info)
                    pane.ctrl.Hide()
                    pane.Hide()
                    self.manager.DetachPane(pane.ctrl)
                    pane.ctrl.Destroy()

                    self.normalized_code_pane = None
                    self.manager.Update()

            eg.mainFrame.Bind(aui.EVT_AUI_PANE_CLOSE, _on_close)

        else:
            self.normalized_code_pane.Show()

        self.manager.Update()

    def on_destroy(self, evt):
        def _detach(pane):
            if pane is None:
                return

            pane_info = self.manager.SavePaneInfo(pane)
            setattr(Config, pane.__name__, pane_info)
            pane.ctrl.Hide()
            pane.Hide()
            self.manager.DetachPane(pane.ctrl)
            pane.ctrl.Destroy()

        _detach(self.original_oscope_pane)
        _detach(self.mce_oscope_pane)
        _detach(self.original_code_pane)
        _detach(self.normalized_code_pane)

        evt.Skip()

    def SetValue(self, value):
        name = value.name
        integer = int(value)
        hexadecimal = value.hexadecimal
        params = repr(value).split('(', 1)[-1].rsplit(')', 1)[0].replace(',', '\n')
        frequency = value.frequency
        protocol = value.decoder.name
        bit_count = value.decoder.bit_count

        self.name_ctrl.SetValue(name)
        self.protocol_ctrl.SetValue(protocol)
        self.frequency_ctrl.SetValue(str(frequency))
        self.parameter_ctrl.SetValue(params)
        self.bit_ctrl.SetValue(str(bit_count))
        self.hex_ctrl.SetValue(hexadecimal)
        self.integer_ctrl.SetValue(str(integer))

        self.code = value

        if self.original_oscope_pane is not None:
            self.original_oscope_pane.SetValue(value)

        if self.mce_oscope_pane is not None:
            self.mce_oscope_pane.SetValue(value)

        if self.original_code_pane is not None:
            self.original_code_pane.SetValue(value)

        if self.normalized_code_pane is not None:
            self.normalized_code_pane.SetValue(value)


HITTEST_FLAG = (
    wx.TREE_HITTEST_ONITEMLABEL |
    wx.TREE_HITTEST_ONITEMICON |
    wx.TREE_HITTEST_ONITEMRIGHT
)

ID_DISABLED = wx.NewId()
ID_CONFIGURE = wx.NewId()
ID_RENAME = wx.NewId()


class DropSource(wx.DropSource):

    def __init__(self, win, text):
        wx.DropSource.__init__(self, win)
        customData = wx.CustomDataObject("DragItem")
        customData.SetData(text)
        textData = wx.TextDataObject(text.decode("UTF-8"))

        data = wx.DataObjectComposite()
        data.Add(textData)
        data.Add(customData)

        self.data = data
        self.SetData(data)


class DropTarget(wx.PyDropTarget):

    def __init__(self, treeCtrl):
        wx.PyDropTarget.__init__(self)
        self.treeCtrl = treeCtrl
        self.srcNode = None
        self.srcItemId = 0

        textData = wx.TextDataObject()
        self.customData = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        self.customData.SetData("")
        compositeData = wx.DataObjectComposite()
        compositeData.Add(textData)
        compositeData.Add(self.customData)
        self.SetDataObject(compositeData)
        self.lastHighlighted = None
        self.whereToDrop = None
        self.lastDropTime = clock()
        self.lastTargetItemId = None
        timerId = wx.NewId()
        self.autoScrollTimer = wx.Timer(self.treeCtrl, timerId)
        self.treeCtrl.Bind(wx.EVT_TIMER, self.OnDragTimerEvent, id=timerId)

    def OnData(self, _, __, dragResult):
        self.OnLeave()
        tree = self.treeCtrl

        if self.lastHighlighted is not None:
            tree.SetItemDropHighlight(self.lastHighlighted, False)

        if self.whereToDrop is not None:
            if not self.GetData():
                return wx.DragNone

            if self.customData.GetDataSize() == 0:
                return wx.DragNone

            xml = self.customData.GetData()
            decoder = tree.GetPyData(self.whereToDrop)
            code = ir_code.IRCode.load_from_xml(xml, decoder)

            child = tree.AppendItem(self.whereToDrop, str(code))
            tree.SetPyData(child, code)

            self.customData.SetData("")

            tree.Delete(self.srcItemId)

        return dragResult

    def OnDragOver(self, x, y, _):
        tree = self.treeCtrl
        self.whereToDrop = None

        if self.lastHighlighted is not None:
            tree.SetItemDropHighlight(self.lastHighlighted, False)
            self.lastHighlighted = None

        dstItemId, flags = tree.HitTest((x, y))

        if not (flags & HITTEST_FLAG):
            return wx.DragNone

        dstNode = tree.GetPyData(dstItemId)
        srcNode = self.srcNode

        if isinstance(dstNode, pyIRDecoder.IRDecoder):
            child, cookie = tree.GetFirstChild(dstItemId)
            while child.IsOk():
                node = tree.GetPyData(dstItemId)
                if node.name == srcNode.decoder.name:
                    if node == srcNode.decoder:
                        break

                    if dstItemId == self.lastTargetItemId:
                        if (
                            self.lastDropTime + 0.6 < clock() and
                            not tree.IsExpanded(dstItemId)
                        ):
                            tree.Expand(dstItemId)
                    else:
                        self.lastDropTime = clock()
                        self.lastTargetItemId = dstItemId

                    tree.SetItemDropHighlight(child, True)
                    self.lastHighlighted = child
                    self.whereToDrop = child
                    tree.SetInsertMark(child, 1)

                    return wx.DragMove

                child, cookie = self.GetNextChild(child, cookie)

            tree.ClearInsertMark()
            return wx.DragNone

        if isinstance(dstNode, ir_code.IRCode):
            if dstNode.decoder.name == srcNode.decoder.name:
                if dstNode.decoder == srcNode.decoder:
                    tree.ClearInsertMark()
                    return wx.DragNone

                dstNode = dstNode.decoder
                dstItemId = tree.GetItemParent(dstItemId)
            else:
                tree.ClearInsertMark()
                return wx.DragNone

        if isinstance(dstNode, protocol_base.IrProtocolBase):
            if dstNode.name == srcNode.decoder.name:
                if dstItemId == self.lastTargetItemId:
                    if (
                        self.lastDropTime + 0.6 < clock() and
                        not tree.IsExpanded(dstItemId)
                    ):
                        tree.Expand(dstItemId)

                else:
                    self.lastDropTime = clock()
                    self.lastTargetItemId = dstItemId

                tree.SetItemDropHighlight(dstItemId, True)
                self.lastHighlighted = dstItemId
                self.whereToDrop = dstItemId
                tree.SetInsertMark(dstItemId, 1)
            else:
                tree.ClearInsertMark()
                return wx.DragNone

    def OnDragTimerEvent(self, _):
        """
        Handles wx.EVT_TIMER, while a drag operation is in progress. It is
        responsible for the automatic scrolling if the mouse gets on the
        upper or lower bounds of the control.
        """
        tree = self.treeCtrl
        x, y = wx.GetMousePosition()
        treeRect = tree.GetScreenRect()
        if treeRect.x <= x <= treeRect.GetRight():
            if y < treeRect.y + 20:
                tree.ScrollLines(-1)
            elif y > treeRect.GetBottom() - 20:
                tree.ScrollLines(1)

    def OnEnter(self, _, __, dragResult):
        self.autoScrollTimer.Start(50)
        return dragResult

    def OnLeave(self):
        self.treeCtrl.ClearInsertMark()
        self.autoScrollTimer.Stop()


class EditControlProxy(object):
    def __init__(self, parent):
        self.parent = parent
        self.realControl = None

    def CanCut(self):
        return self.realControl.CanCut()

    def CanCopy(self):
        return self.realControl.CanCopy()

    def CanPaste(self):
        return self.realControl.CanPaste()

    def CanDelete(self):
        start, end = self.realControl.GetSelection()
        return start != end

    def ClearControl(self):
        self.realControl = None

    def OnCmdCut(self):
        self.realControl.Cut()

    def OnCmdCopy(self):
        self.realControl.Copy()

    def OnCmdPaste(self):
        self.realControl.Paste()

    def OnCmdDelete(self):
        start, end = self.realControl.GetSelection()
        if end - start == 0:
            end += 1
        self.realControl.Remove(start, end)
        return

    def SetControl(self):
        self.realControl = self.parent.GetEditControl()
        self.parent.lastFocus = self


class CodesPanel(wx.TreeCtrl):

    def __init__(self, parent, size=wx.DefaultSize):
        self.root = None
        self.editLabelId = None
        self.insertionMark = None
        self.editControl = EditControlProxy(self)

        style = (
            wx.TR_HAS_BUTTONS |
            wx.TR_EDIT_LABELS |
            wx.TR_ROW_LINES |
            wx.CLIP_CHILDREN |
            wx.TR_HIDE_ROOT |
            wx.TR_LINES_AT_ROOT |
            wx.TR_SINGLE
        )
        wx.TreeCtrl.__init__(self, parent, size=size, style=style)

        self.hwnd = self.GetHandle()

        self.Bind(wx.EVT_SET_FOCUS, self.OnGetFocusEvent)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocusEvent)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginLabelEditEvent)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEditEvent)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClickEvent)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnItemMenuEvent)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDragEvent)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.lastFocus = None

        self.dropTarget = DropTarget(self)
        self.SetDropTarget(self.dropTarget)
        self._cut_item = None

        self.root = self.AddRoot('root')
        for plugin_name, decoder in self.load_decoders():
            for d in decoder:
                print d.name
                for c in d:
                    print '   ', c.name

            itemId = self.AppendItem(
                self.root,
                plugin_name
            )

            self.SetPyData(itemId, decoder)

            for protocol in decoder:
                self.CreateTreeItem(protocol, itemId)

    def OnGetFocusEvent(self, event):
        """
        Handles wx.EVT_SET_FOCUS
        """
        self.lastFocus = self
        event.Skip()

    def OnKillFocusEvent(self, event):
        """
        Handles wx.EVT_KILL_FOCUS
        """
        if self.editLabelId is None:
            self.lastFocus = None

        event.Skip()

    def CreatePopupMenu(self, obj):
        """
        Creates the pop-up menu for the configuration tree.
        """
        menu = wx.Menu()

        if isinstance(obj, ir_code.IRCode):
            cut = menu.AppendItem(wx.MenuItem(menu, wx.ID_CUT, "Cut", "", wx.ITEM_NORMAL))
            self.Bind(wx.EVT_MENU, self.OnCut, cut)

            copy = menu.AppendItem(wx.MenuItem(menu, wx.ID_COPY, "Copy", "", wx.ITEM_NORMAL))
            self.Bind(wx.EVT_MENU, self.OnCopy, copy)

            paste = menu.AppendItem(wx.MenuItem(menu, wx.ID_PASTE, "Paste", "", wx.ITEM_NORMAL))
            self.Bind(wx.EVT_MENU, self.OnPaste, paste)

            delete = menu.AppendItem(wx.MenuItem(menu, wx.ID_DELETE, "Delete", "", wx.ITEM_NORMAL))
            self.Bind(wx.EVT_MENU, self.OnDelete, delete)

            menu.AppendSeparator()

            rename = menu.AppendItem(wx.MenuItem(menu, ID_RENAME, "Rename", "", wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.OnRename, rename)

        elif isinstance(obj, protocol_base.IrProtocolBase):
            add_code = menu.AppendItem(wx.MenuItem(menu, wx.ID_ADD, "Add Code", "", wx.ITEM_NORMAL))
            self.Bind(wx.EVT_MENU, self.OnAddParamCode, add_code)

            menu.AppendSeparator()

            paste = menu.AppendItem(wx.MenuItem(menu, wx.ID_PASTE, "Paste", "", wx.ITEM_NORMAL))
            self.Bind(wx.EVT_MENU, self.OnPaste, paste)

            menu.AppendSeparator()

            disabled = menu.AppendItem(wx.MenuItem(menu, ID_DISABLED, "Disabled", "", wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.OnDisabled, disabled)
            menu.Check(ID_DISABLED, obj.enabled)

            configure = menu.AppendItem(wx.MenuItem(menu, ID_CONFIGURE, "Configure", "", wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.OnConfigure, configure)

        else:
            add_menu = wx.Menu()
            menu.AppendSubMenu(add_menu, "Add Code", "")
            menu.AppendSeparator()

            add_pronto = add_menu.AppendItem(
                wx.MenuItem(add_menu, wx.ID_ADD, "Add Pronto/RLC Code", "", wx.ITEM_NORMAL)
            )
            self.Bind(wx.EVT_MENU, self.OnAddTextCode, add_pronto)

            add_database = add_menu.AppendItem(
                wx.MenuItem(add_menu, wx.ID_ADD, "Add Database Code", "", wx.ITEM_NORMAL)
            )
            self.Bind(wx.EVT_MENU, self.OnAddDatabaseCode, add_database)

            paste = menu.AppendItem(wx.MenuItem(menu, wx.ID_PASTE, "Paste", "", wx.ITEM_NORMAL))
            self.Bind(wx.EVT_MENU, self.OnPaste, paste)

        return menu

    def _set_new_code(self, selection, code):
        child, cookie = self.GetFirstChild(selection)
        while child.IsOk():
            if code == self.GetPyData(child):
                self.SelectItem(child)
                self.EnsureVisible(child)
                event = wx.TreeEvent(wx.wxEVT_TREE_ITEM_ACTIVATED, self, item=child)
                self.GetEventHandler().ProcessEvent(event)

                return

            child, cookie = self.GetNextChild(child, cookie)

        itemId = self.CreateTreeItem(code, selection)
        self.SelectItem(itemId)
        self.EnsureVisible(itemId)
        event = wx.TreeEvent(wx.wxEVT_TREE_ITEM_ACTIVATED, self, item=itemId)
        self.GetEventHandler().ProcessEvent(event)

    def OnAddTextCode(self, _):
        selection = self.GetSelection()

        if not selection.IsOk():
            return

        obj = self.GetPyData(selection)
        code = eg.IrCodeTextDialog.GetResult(obj)

        if code is None:
            return

        child, cookie = self.GetFirstChild(selection)
        while child.IsOk():
            decoder = self.GetPyData(child)
            if decoder.name == code.decoder.name:
                selection = child
                break

            selection = None
            child, cookie = self.GetNextChild(child, cookie)

        if selection is None:
            raise RuntimeError('This should not happen')

        self._set_new_code(selection, code)

    def OnAddDatabaseCode(self, _):
        selection = self.GetSelection()

        if not selection.IsOk():
            return

        obj = self.GetPyData(selection)

        code = eg.IrCodeTextDialog.GetResult(obj)

        if code is None:
            return

        child, cookie = self.GetFirstChild(selection)
        while child.IsOk():
            decoder = self.GetPyData(child)
            if decoder.name == code.decoder.name:
                selection = child
                break

            selection = None
            child, cookie = self.GetNextChild(child, cookie)

        if selection is None:
            raise RuntimeError('This should not happen')

        self._set_new_code(selection, code)

    def OnAddParamCode(self, _):
        selection = self.GetSelection()

        if not selection.IsOk():
            return

        obj = self.GetPyData(selection)

        code = eg.IrCodeParamDialog.GetResult(obj)

        if code is None:
            return

        self._set_new_code(selection, code)

    def OnCopy(self, _):
        selection = self.Selection()

        if not selection.IsOk():
            return

        obj = self.GetPyData(selection)
        data = str(obj.xml)

        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(data))
            wx.TheClipboard.Close()
            self._cut_item = None

    def OnLeave(self, evt):
        self._cut_item = None
        evt.Skip()

    def OnChar(self, evt):
        keycode = evt.GetKeyCode()

        if evt.ControlDown():
            # 88 = x cut
            if keycode == 67:
                self.OnCopy(None)
            elif keycode == 86:
                self.OnPaste(None)
            elif keycode == 88:
                self.OnCut(None)
            else:
                evt.Skip()
        else:
            if keycode == 127:
                self.OnDelete(None)
            elif keycode == 13:
                self.OnEnter(None)
            elif keycode == 341:
                self.OnRename(None)
            else:
                evt.Skip()

    def OnCut(self, _):
        selection = self.Selection()
        if not selection.IsOk():
            return

        obj = self.GetPyData(selection)
        if not isinstance(obj, ir_code.IRCode):
            return

        self._cut_item = (selection, obj)

    def OnPaste(self, _):
        selection = self.Selection()
        if not selection.IsOk():
            return

        obj = self.GetPyData(selection)

        if self._cut_item is not None:
            src_id, src_obj = self._cut_item

            if isinstance(obj, ir_code.IRCode):
                selection = self.GetItemParent(selection)
                obj = self.GetPyData(selection)

            if isinstance(obj, protocol_base.IrProtocolBase):
                if src_obj.decoder.name != obj.name:
                    return

                code = ir_code.IRCode.load_from_xml(src_obj.xml, obj)
                code.save()
                itemId = self.CreateTreeItem(code, selection)

                self.Delete(src_id)
                src_obj.delete()

                self.SelectItem(itemId)
                self.EnsureVisible(itemId)
                event = wx.TreeEvent(wx.wxEVT_TREE_ITEM_ACTIVATED, self, item=itemId)
                self.GetEventHandler().ProcessEvent(event)
                self._cut_item = None

                return

            if isinstance(obj, pyIRDecoder.IRDecoder):
                for decoder in obj:
                    if decoder.name == src_obj.decoder.name:
                        break
                else:
                    return

                child, cookie = self.GetFirstChild(selection)
                while child.IsOk():
                    if decoder == self.GetPyData(child):
                        code = ir_code.IRCode.load_from_xml(src_obj.xml, decoder)
                        code.save()
                        itemId = self.CreateTreeItem(code, child)

                        self.Delete(src_id)
                        src_obj.delete()

                        self.SelectItem(itemId)
                        self.EnsureVisible(itemId)
                        event = wx.TreeEvent(wx.wxEVT_TREE_ITEM_ACTIVATED, self, item=itemId)
                        self.GetEventHandler().ProcessEvent(event)
                        self._cut_item = None

                        return
                    child, cookie = self.GetNextChild(child, cookie)

            return

        if not wx.TheClipboard.Open():
            eg.PrintError("Can't open clipboard.")
            return
        try:
            dataObj = wx.TextDataObject()

            if not wx.TheClipboard.GetData(dataObj):
                return

            data = dataObj.GetText().encode("utf-8")

            try:
                from pyIRDecoder.xml_handler import XMLElement
                xml = XMLElement.from_string(data)

                if isinstance(obj, ir_code.IRCode):
                    selection = self.GetItemParent(selection)
                    obj = self.GetPyData(selection)

                if isinstance(obj, pyIRDecoder.IRDecoder):
                    for decoder in obj:
                        if decoder.name == xml.decoder:
                            break
                    else:
                        return

                    child, cookie = self.GetFirstChild(selection)
                    while child.IsOk():
                        if decoder == self.GetPyData(child):
                            code = ir_code.IRCode.load_from_xml(xml, decoder)
                            code.save()
                            itemId = self.CreateTreeItem(code, child)
                            self.SelectItem(itemId)
                            self.EnsureVisible(itemId)
                            event = wx.TreeEvent(wx.wxEVT_TREE_ITEM_ACTIVATED, self, item=itemId)
                            self.GetEventHandler().ProcessEvent(event)

                            return
                        child, cookie = self.GetNextChild(child, cookie)

                    return

                if xml.decoder != obj.name:
                    return

                code = ir_code.IRCode.load_from_xml(xml, obj)
                code.save()

                itemId = self.CreateTreeItem(code, selection)

                self.SelectItem(itemId)
                self.EnsureVisible(itemId)
                event = wx.TreeEvent(wx.wxEVT_TREE_ITEM_ACTIVATED, self, item=itemId)
                self.GetEventHandler().ProcessEvent(event)
                return

            except:
                if not isinstance(obj, pyIRDecoder.IRDecoder):
                    return

                from eg.Classes.IrCodeTextDialog import _parse_code_text

                frequency, data = _parse_code_text(data)
                if data is None:
                    return

                code = None

                for rlc in data:
                    c = obj.decode(rlc, frequency=frequency)
                    if c is None:
                        continue
                    code = c

                if code is None:
                    return

                for decoder in obj:
                    if decoder.name == code.decoder.name:
                        break
                else:
                    return

                child, cookie = self.GetFirstChild(selection)
                while child.IsOk():
                    if decoder == self.GetPyData(child):
                        code.save()
                        itemId = self.CreateTreeItem(code, child)
                        self.SelectItem(itemId)
                        self.EnsureVisible(itemId)
                        event = wx.TreeEvent(wx.wxEVT_TREE_ITEM_ACTIVATED, self, item=itemId)
                        self.GetEventHandler().ProcessEvent(event)

                        return
                    child, cookie = self.GetNextChild(child, cookie)
        finally:
            wx.TheClipboard.Close()

    def OnDelete(self, _):
        selection = self.GetSelection()
        if not selection.IsOk():
            return
        obj = self.GetPyData(selection)

        obj.delete()
        self.Delete(selection)

    def OnDisabled(self, evt):
        menu = evt.GetMenu()
        menu_item = evt.GetMenuId()

        selection = self.GetSelection()
        if not selection.IsOk():
            return

        obj = self.GetPyData(selection)
        obj.enabled = menu.IsChecked(menu_item)

    def OnConfigure(self, _):
        selection = self.Selection()
        if not selection.IsOk():
            return

        obj = self.GetPyData(selection)
        eg.IrProtocolConfigDialog.GetResult(obj)

    def OnRename(self, _):
        selection = self.GetSelection()
        if not selection.IsOk():
            return

        self.SetFocus()
        self.EditLabel(selection)

    def OnEnter(self, _):
        if self.lastFocus == self.editControl:
            self.EndEditLabel(self.editLabelId, False)

    def load_decoders(self):
        config_path = os.path.join(eg.configDir, 'ir_decoders')

        for config_file in os.listdir(config_path):
            if not config_file.endswith('xml'):
                continue

            plugin_name = os.path.splitext(config_file)[0]
            config_file = os.path.join(config_path, config_file)

            config = pyIRDecoder.Config(config_file)
            decoder = pyIRDecoder.IRDecoder(config)
            yield plugin_name, decoder

    def ClearInsertMark(self):
        SendMessageTimeout(self.hwnd, 4378, 0, long(0), 1, 100, None)
        self.insertionMark = None

    def CreateTreeItem(self, obj, parentId):
        itemId = self.AppendItem(
            parentId,
            obj.name
        )

        self.SetPyData(itemId, obj)

        if isinstance(obj, ir_code.IRCode):
            return itemId

        for child in obj:
            self.CreateTreeItem(child, itemId)

        return itemId

    def SetInsertMark(self, treeItem, after):
        if treeItem:
            lParam = long(treeItem.m_pItem)
            if self.insertionMark == (lParam, after):
                return

            # TVM_SETINSERTMARK = 4378
            SendMessageTimeout(self.hwnd, 4378, after, lParam, 1, 100, None)
            self.insertionMark = (lParam, after)
        else:
            self.ClearInsertMark()

    # -------------------------------------------------------------------------
    # wx.Event Handlers
    # -------------------------------------------------------------------------

    def OnBeginDragEvent(self, event):
        """
        Handles wx.EVT_TREE_BEGIN_DRAG
        """
        srcItemId = event.GetItem()
        srcNode = self.GetPyData(srcItemId)
        if not isinstance(srcNode, ir_code.IRCode):
            return

        self.SelectItem(srcItemId)
        dropTarget = self.dropTarget
        dropTarget.srcNode = srcNode

        DropSource(self, str(srcNode.xml)).DoDragDrop(wx.Drag_AllowMove)

        dropTarget.srcNode = None

        self.ClearInsertMark()
        if dropTarget.lastHighlighted is not None:
            self.SetItemDropHighlight(dropTarget.lastHighlighted, False)

    def OnBeginLabelEditEvent(self, event):
        """
        Handles wx.EVT_TREE_BEGIN_LABEL_EDIT
        """
        obj = self.GetPyData(event.GetItem())
        if not isinstance(obj, ir_code.IRCode):
            event.Veto()
            return

        self.editLabelId = event.GetItem()
        wx.CallAfter(self.editControl.SetControl)
        event.Skip()

    def OnEndLabelEditEvent(self, event):
        """
        Handles wx.EVT_TREE_END_LABEL_EDIT
        """
        self.editLabelId = None

        itemId = event.GetItem()
        obj = self.GetPyData(itemId)
        newLabel = event.GetLabel()

        if not event.IsEditCancelled() and obj.name != newLabel:
            obj.name = newLabel

        event.Skip()

    def OnItemMenuEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_MENU
        """
        itemId = event.GetItem()
        if not itemId.IsOk():
            return

        obj = self.GetPyData(itemId)

        self.SetFocus()
        menu = self.CreatePopupMenu(obj)
        self.PopupMenu(menu, event.GetPoint())
        event.Skip()

    def OnRightClickEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_RIGHT_CLICK
        """
        itemId = event.GetItem()
        if not itemId.IsOk():
            return

        self.SelectItem(itemId)


TIME_FORMAT = '''\
{0}μs
{1}ms
{2}sec
'''


def remap(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (((value - old_min) * new_range) / old_range) + new_min


class Oscilloscope(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.original_o_scope = Scope(self)
        original_o_scope_label = wx.StaticText(self, -1, 'Original Code')
        self.cleaned_o_scope = Scope(self)
        cleaned_o_scope_label = wx.StaticText(self, -1, 'Normalized Code')
        sync = wx.CheckBox(self, -1, 'Match Oscilloscope Movements')
        sync.SetValue(True)

        def on_sync(_):
            if sync.GetValue():
                position = self.original_o_scope.position
                self.cleaned_o_scope.position = position

                def _do():
                    self.cleaned_o_scope.Refresh()
                    self.cleaned_o_scope.Update()

                wx.CallAfter(_do)

        sync.Bind(wx.EVT_CHECKBOX, on_sync)

        def on_original_position(evt):
            if not sync.GetValue():
                return

            position = evt.GetPosition()
            self.cleaned_o_scope.position = position

            def _do():
                self.cleaned_o_scope.Refresh()
                self.cleaned_o_scope.Update()

            wx.CallAfter(_do)

        self.original_o_scope.Bind(wx.EVT_SCROLL_CHANGED, on_original_position)

        def on_cleaned_position(evt):
            if not sync.GetValue():
                return

            position = evt.GetPosition()
            self.original_o_scope.position = position

            def _do():
                self.original_o_scope.Refresh()
                self.original_o_scope.Update()

            wx.CallAfter(_do)

        self.cleaned_o_scope.Bind(wx.EVT_SCROLL_CHANGED, on_cleaned_position)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(v_sizer(original_o_scope_label, self.original_o_scope), 1, wx.EXPAND)
        sizer.Add(v_sizer(cleaned_o_scope_label, self.cleaned_o_scope), 1, wx.EXPAND)
        sizer.Add(sync, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        self.SetMinSize((-1, 50))

    def SetValue(self, o_code, n_code):
        self.original_o_scope.SetValue(o_code)
        self.cleaned_o_scope.SetValue(n_code)


class Scope(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_SUNKEN)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMoveMouse)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.data = []
        self.rects = []
        self.gauge = wx.Rect(0, 0, 1, 1)
        self.slider_rect = wx.Rect(0, 0, 1, 1)
        self._position = 0
        self.mouse_x = 0
        self.slide = False
        self.total_time = 0
        self.total_times = []

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        width = self.GetClientSize()[0]

        if value > (self.total_time // 50) - width:
            value = (self.total_time // 50) - width

        elif value < 0:
            value = 0

        self._position = value

    def _create_event(self, value):
        event = wx.ScrollEvent(
            wx.wxEVT_SCROLL_CHANGED,
            self.GetId()
        )
        event.SetId(self.GetId())
        event.SetEventObject(self)
        event.SetPosition(value)
        self.GetEventHandler().ProcessEvent(event)

    def OnLeave(self, evt):
        if self.HasCapture():
            self.slide = False
            self.ReleaseMouse()
            self.Refresh()
            self.Update()

        evt.Skip()

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.slide = False
            self.ReleaseMouse()
            self.Refresh()
            self.Update()
        evt.Skip()

    def OnLeftDown(self, evt):
        x, y = evt.GetPosition()
        if self.slider_rect.Contains(wx.Point(x, y)):
            self.slide = True
        else:
            self.slide = False

        self.mouse_x = x
        self.CaptureMouse()
        self.Refresh()
        self.Update()

        evt.Skip()

    def OnMoveMouse(self, evt):
        x, y = evt.GetPosition()

        if self.HasCapture():
            width = self.GetClientSize()[0]

            if self.slide:
                new_percent = float(x) / float(width)
                old_percent = float(self.mouse_x) / float(width)
                percent_change = old_percent - new_percent
                amount_change = int(round((self.total_time // 50) * percent_change))
                self.mouse_x = x

                if x < self.mouse_x:
                    self.position += amount_change
                else:
                    self.position -= amount_change
            else:
                change = x - self.mouse_x
                self.position -= change
                self.mouse_x = x

            self._create_event(self.position)
            self.Refresh()
            self.Update()

        temp_x = x + self.position
        for i, rect in enumerate(self.rects):
            if rect.Contains(wx.Point(temp_x, y)):
                len_count = 0

                for j, rlc in enumerate(self.data):
                    if i < len_count + len(rlc):
                        timing = rlc[i - len_count]
                        frame = j
                        break

                    len_count += len(rlc)
                else:
                    raise RuntimeError('not supposed to happen')

                if timing < 0:
                    timing = -timing
                    text = 'Idle\n'
                else:
                    text = 'Pulse\n'

                text = (
                    'Frame ' +
                    str(frame) +
                    '\n' +
                    text +
                    TIME_FORMAT.format(
                        timing,
                        timing / 1000.0,
                        (timing / 1000.0) / 1000.0
                    )
                )
                self.SetToolTipString(text)
                break
        else:
            if self.gauge.Contains(wx.Point(x, y)):
                width = self.GetClientSize()[0]
                timing = remap(x + int(x * 0.012), 0, width, 0, self.total_time)
                total_time = 0
                for i, tt in enumerate(self.total_times):
                    if timing > tt:
                        timing -= tt
                        total_time += tt
                    else:
                        total_time += timing
                        text = (
                            'Frame ' +
                            str(i) +
                            '\n' +
                            TIME_FORMAT.format(
                                timing,
                                timing / 1000.0,
                                (timing / 1000.0) / 1000.0
                            )
                        )

                        text += (
                            '\nTotal\n' +
                            TIME_FORMAT.format(
                                total_time,
                                total_time / 1000.0,
                                (total_time / 1000.0) / 1000.0
                            )
                        )
                        self.SetToolTipString(text)
                        break
                else:
                    self.SetToolTipString('')

            else:
                self.SetToolTipString('')

        evt.Skip()

    def SetValue(self, value):
        self.data = value
        self.rects = []
        self.total_times = []
        self.gauge = wx.Rect(0, 0, 1, 1)
        self.slider_rect = wx.Rect(0, 0, 1, 1)
        self.position = 0
        self.mouse_x = 0
        self.slide = False

        total_time = 0

        for rlc in self.data:
            tt = sum(abs(item) for item in rlc)
            self.total_times += [tt]
            total_time += tt

        self.total_time = total_time

        self.SetMaxClientSize(wx.Size((self.total_time // 50) + 5, -1))
        self.Refresh()
        self.Update()

    def DoGetBestClientSize(self):
        height = self.GetSize()[1]
        if self.total_time:
            width = (self.total_time // 50) + 5
        else:
            width = -1
        return wx.Size(width, height)

    def DoGetBestSize(self):
        height = self.GetSize()[1]
        if self.total_time:
            width = (self.total_time // 50) + 5
        else:
            width = -1
        return wx.Size(width, height)

    def GetBestSize(self):
        height = self.GetSize()[1]
        if self.total_time:
            width = (self.total_time // 50) + 5
        else:
            width = -1
        return wx.Size(width, height)

    def OnSize(self, evt):
        w, h = evt.GetSize()

        if self.total_time:
            width = (self.total_time // 50) + 5
            if w > width:
                self.SetSize(w, h)

        def _do():
            self.Refresh()
            self.Update()

        wx.CallAfter(_do)
        evt.Skip()

    def OnPaint(self, _):
        client_width, height = self.GetClientSize()
        if self.total_time:
            width = self.total_time // 50
            bmp = wx.EmptyBitmap(width + 5, height)
        else:
            width = client_width
            bmp = wx.EmptyBitmap(width, height)

        dc = wx.MemoryDC()
        dc.SelectObject(bmp)

        amount_visible = remap(client_width, 0, width + 5, 0, client_width)
        current_position = remap(self.position, 0, width + 5, 0, client_width)

        position_start = current_position + self.position
        position_end = position_start + amount_visible

        while position_end + 3 > width:
            self.position -= 1
            current_position = remap(self.position, 0, width + 5, 0, client_width)
            position_start = current_position + self.position
            position_end = position_start + amount_visible

            if self.position == 0:
                break

        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 255)))
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 255), 1))
        dc.DrawRectangle(0, 0, width + 5, height)
        #
        # dc.SetBrush(wx.Brush(wx.Colour(190, 190, 190, 255)))
        # dc.SetPen(wx.Pen(wx.Colour(190, 190, 190, 255), 1))
        # dc.DrawRectangle(3, height - 13, client_width - 6, 12)

        dc.SetBrush(wx.Brush(wx.Colour(75, 75, 75, 255)))
        dc.SetPen(wx.Pen(wx.Colour(75, 75, 75, 255), 1))
        dc.DrawRectangle(position_start, height - 20, amount_visible, 17)

        pulse_on_small = height - 18
        pulse_off_small = height - 3
        last_point_small = (5 + self.position, pulse_off_small)
        pens_small = []
        lines_small = []

        pulse_on_large = 10
        pulse_off_large = height - 25
        last_point_large = (5, pulse_off_large)
        pens_large = []
        lines_large = []

        total_time = 0

        in_pens = [
            wx.Pen(wx.Colour(219, 172, 79, 255), 1),
            wx.Pen(wx.Colour(134, 186, 81, 255), 1),
            wx.Pen(wx.Colour(186, 61, 154, 255), 1)
        ]

        out_pen = wx.Pen(wx.Colour(75, 110, 177, 255), 1)

        x_large = 5
        del self.rects[:]

        for i, rlc in enumerate(self.data):
            in_pen = in_pens[i]

            if self.position:
                current_pen = out_pen
            else:
                current_pen = in_pen

            for item in rlc:
                if item > 0:
                    y_large = pulse_on_large
                    y_small = pulse_on_small
                else:
                    y_large = pulse_off_large
                    y_small = pulse_off_small
                    item = -item

                total_time += item // 50

                x_large += item // 50
                x_small = remap(total_time, 0, self.total_time // 50, 0, client_width) + 5 + self.position

                start_1 = last_point_large
                end_1 = (last_point_large[0], y_large)
                start_2 = end_1
                end_2 = (x_large, y_large)

                self.rects += [wx.Rect(last_point_large[0], pulse_on_large, item // 50, pulse_off_large - 10)]
                lines_large += [start_1 + end_1, start_2 + end_2]
                pens_large += [in_pen, in_pen]
                last_point_large = end_2

                if x_small > position_start:
                    if x_small > position_end:
                        diff = x_small - position_end
                        current_pen = out_pen
                    else:
                        diff = x_small - position_start
                        current_pen = in_pen

                    if last_point_small[0] < position_start:
                        pens_small += [out_pen, out_pen]
                        start_1 = last_point_small
                        end_1 = (last_point_small[0], y_small)
                        start_2 = end_1
                        end_2 = (position_start, y_small)
                        start_3 = end_2

                        lines_small += [start_1 + end_1, start_2 + end_2]

                        if x_small < position_end:
                            end_3 = (x_small, y_small)
                            pens_small += [in_pen]
                            lines_small += [start_3 + end_3]
                            current_pen = in_pen
                            last_point_small = end_3
                        else:
                            end_3 = (position_end, y_small)
                            start_4 = end_3
                            end_4 = (x_small, y_small)
                            pens_small += [in_pen, out_pen]
                            lines_small += [start_3 + end_3, start_4 + end_4]
                            current_pen = out_pen
                            last_point_small = end_4
                        continue

                    if x_small > position_end > last_point_small[0] or last_point_small[0] < position_start:
                        if total_time > self.position + amount_visible:
                            pens_small += [in_pen, in_pen, out_pen]
                        else:
                            pens_small += [out_pen, out_pen, in_pen]

                        x1 = x_small - diff
                        x2 = x_small

                        start_1 = last_point_small
                        end_1 = (last_point_small[0], y_small)
                        start_2 = end_1
                        end_2 = (x1, y_small)
                        start_3 = end_2
                        end_3 = (x2, y_small)
                        lines_small += [start_1 + end_1, start_2 + end_2, start_3 + end_3]
                        last_point_small = end_3

                        continue

                pens_small += [current_pen, current_pen]
                start_1 = last_point_small
                end_1 = (last_point_small[0], y_small)
                start_2 = end_1
                end_2 = (x_small, y_small)

                lines_small += [start_1 + end_1, start_2 + end_2]
                last_point_small = end_2

        dc.DrawLineList(lines_small + lines_large, pens_small + pens_large)

        self.slider_rect = wx.Rect(current_position, height - 20, amount_visible, 17)
        self.gauge = wx.Rect(3, height - 20, client_width - 6, 17)

        dc.SelectObject(wx.NullBitmap)

        dc.Destroy()
        del dc

        pdc = wx.PaintDC(self)
        pdc.DrawBitmap(bmp, -self.position + -1, 0)


def PaneBase(icon):
    pane = aui.AuiPaneInfo()
    pane.CloseButton(False)
    pane.DestroyOnClose(False)
    pane.Floatable()
    pane.Dockable()
    pane.Icon(icon)
    pane.Movable()
    pane.PaneBorder()
    pane.PinButton()
    pane.Resizable()
    pane.MaximizeButton()
    pane.MinimizeButton()
    pane.CaptionVisible()
    pane.Gripper()
    pane.ctrl = None

    def SetValue(value):
        pane.ctrl.SetValue(value)

    pane.SetValue = SetValue
    return pane


def CodeInfoPane(icon):
    pane = PaneBase(icon)
    pane.__name__ = 'CodeInfoPane'
    pane.Caption('IR Code: Code Information')
    pane.Name('ir_code_information')
    pane.Row(0)
    pane.Bottom()
    pane.ctrl = InfoPanel(eg.mainFrame, icon)
    pane.MinSize((100, 100))
    pane.Show()

    return pane


def OriginalCodePane(icon):
    pane = PaneBase(icon)
    pane.__name__ = 'OriginalCodePane'
    pane.Caption('IR Code: Original Code')
    pane.Name('ir_code_original')
    pane.ctrl = OriginalCodePanel(eg.mainFrame)
    pane.MinSize((200, 200))
    pane.FloatingSize((400, 400))
    pane.Float()
    pane.CloseButton(True)
    pane.DestroyOnClose(False)
    pane.Show()

    return pane


def NormalizedCodePane(icon):
    pane = PaneBase(icon)
    pane.__name__ = 'NormalizedCodePane'
    pane.Caption('IR Code: Normalized Code')
    pane.Name('ir_code_normalized')
    pane.ctrl = NormalizedCodePanel(eg.mainFrame)
    pane.MinSize((200, 200))
    pane.FloatingSize((400, 400))
    pane.Float()
    pane.CloseButton(True)
    pane.DestroyOnClose(False)
    pane.Show()

    return pane


def OriginalOscilloscopePane(icon):
    pane = PaneBase(icon)
    pane.__name__ = 'OriginalOscilloscopePane'
    pane.Caption('IR Code: Original Oscilloscope')
    pane.Name('ir_code_original_oscilloscope')
    pane.ctrl = OriginalOscilloscopePanel(eg.mainFrame)
    pane.MinSize((400, 200))
    pane.FloatingSize((600, 300))
    pane.Float()
    pane.CloseButton(True)
    pane.DestroyOnClose(False)
    pane.Show()

    return pane


def MCEOscilloscopePane(icon):
    pane = PaneBase(icon)
    pane.__name__ = 'MCEOscilloscopePane'
    pane.Caption('IR Code: MCE Oscilloscope')
    pane.Name('ir_code_mce_oscilloscope')
    pane.ctrl = MCEOscilloscopePanel(eg.mainFrame)
    pane.MinSize((400, 200))
    pane.FloatingSize((600, 300))
    pane.Float()
    pane.CloseButton(True)
    pane.DestroyOnClose(False)
    pane.Show()

    return pane


class OscilloscopePanelBase(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        self.ctrl = Oscilloscope(self)
        self.ctrl.SetMinSize((300, 300))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ctrl, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)

    def SetValue(self, value):
        raise NotImplementedError


class OriginalOscilloscopePanel(OscilloscopePanelBase):

    def SetValue(self, value):
        if value is None:
            self.ctrl.SetValue([], [])
        else:
            self.ctrl.SetValue(
                value.original_rlc,
                value.normalized_rlc
            )


class MCEOscilloscopePanel(OscilloscopePanelBase):

    def SetValue(self, value):
        if value is None:
            self.ctrl.SetValue([], [])
        else:
            self.ctrl.SetValue(
                value.original_mce_rlc,
                value.normalized_mce_rlc
            )


class IrDecoderPane(object):

    def __init__(self):
        bmp = eg.Icons.GetInternalBitmap("remote")
        img = bmp.ConvertToImage().Rescale(16, 16, wx.IMAGE_QUALITY_HIGH)
        icon = img.ConvertToBitmap()

        self.manager = eg.mainFrame.auiManager

        self.pane = PaneBase(icon)
        self.pane.Caption('IR Code: Codes')
        self.pane.Name('ir_code_codes')
        self.pane.Bottom()
        self.pane.Row(0)
        self.ctrl = CodesPanel(eg.mainFrame)
        self.pane.CloseButton()
        self.pane.Show()

        self.manager.AddPane(self.ctrl, self.pane)
        if Config.IrDecoderPane is not None:
            self.manager.LoadPaneInfo(Config.IrDecoderPane, self.pane)

        def _attach_pane(pane):
            pane_info = getattr(Config, pane.__name__)
            self.manager.AddPane(pane.ctrl, pane)
            if pane_info is not None:
                self.manager.LoadPaneInfo(pane_info, pane)

        self.info_pane = CodeInfoPane(icon)

        _attach_pane(self.info_pane)

        self.manager.Update()

        eg.mainFrame.Bind(aui.EVT_AUI_PANE_CLOSE, self.on_pane_close)
        self.ctrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_item_activate)
        self.ctrl.Bind(wx.EVT_LEFT_DCLICK, self.on_left_double_click)

    def _set_code(self, code):
        self.info_pane.SetValue(code)

    def on_item_activate(self, event):
        """
        Handles wx.EVT_TREE_ITEM_ACTIVATED
        """
        itemId = event.GetItem()
        if itemId.IsOk():
            obj = self.ctrl.GetPyData(itemId)
            if isinstance(obj, ir_code.IRCode):
                self._set_code(obj)
            else:
                self._set_code(None)

        event.Skip()

    def on_left_double_click(self, event):
        """
        Handles wx.EVT_LEFT_DCLICK
        """

        itemId = self.ctrl.HitTest(event.GetPosition())[0]
        if itemId.IsOk():
            obj = self.ctrl.GetPyData(itemId)
            if isinstance(obj, ir_code.IRCode):
                self._set_code(obj)
            else:
                self._set_code(None)

        event.Skip()

    def on_pane_close(self, evt):
        print evt.GetPane().name
        if evt.GetPane() == self.pane:
            eg.mainFrame.Unbind(aui.EVT_AUI_PANE_CLOSE, handler=self.on_pane_close)

            def _detach(pane):
                pane_info = self.manager.SavePaneInfo(pane)
                setattr(Config, pane.__name__, pane_info)
                pane.ctrl.Hide()
                pane.Hide()
                self.manager.DetachPane(pane.ctrl)
                pane.ctrl.Destroy()

            _detach(self.info_pane)

            Config.IrDecoderPane = self.manager.SavePaneInfo(self.pane)
            self.ctrl.Hide()
            self.pane.Hide()
            self.manager.DetachPane(self.ctrl)
            self.ctrl.Destroy()

            eg.mainFrame.decoder_pane = None
