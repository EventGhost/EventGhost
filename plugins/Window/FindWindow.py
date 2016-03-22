# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# by Pako 2011-04-28 15:22 UTC+1
#     - Added option "Stop macro if target found"

import eg
import wx
from os.path import basename

from eg.WinApi.Dynamic import (
    GetAncestor,
    GA_ROOT,
)
from eg.WinApi import (
    GetProcessName,
    GetWindowText,
    GetClassName,
    GetWindowThreadProcessId,
    GetTopLevelWindowList,
    GetWindowChildsList,
)

STOP_IF_NOT_FOUND = 0
STOP_IF_FOUND = 1
STOP_NEVER = 2

class Config(eg.PersistentData):
    hideOnDrag = True



class TestDialog(eg.Dialog):

    def __init__(self, parent, hwnds):
        eg.Dialog.__init__(
            self,
            parent,
            title="Found Windows",
            size=(500, 350),
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER,
        )
        windowList = eg.WindowList(self, hwnds)
        okButton = wx.Button(self, wx.ID_OK)
        btnSizer = eg.HBoxSizer(
            ((0, 0), 1, wx.EXPAND),
            (okButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALL, 5),
            ((0, 0), 1, wx.EXPAND),
            (eg.SizeGrip(self), 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT),
        )
        mainSizer = eg.VBoxSizer(
            (windowList, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5),
            (btnSizer, 0, wx.EXPAND),
        )
        self.SetSizer(mainSizer)



def UseForegroundWindowOnly():
    """ Instruct EventGhost to use the active desktop window only, by
        clearing eg.lastFoundWindows
    """
    del eg.lastFoundWindows[:]
    return []



class FindWindow(eg.ActionBase):
    name = "Find a window"
    description = (
        'Searches for a window, which is afterwards used as a target for '
        'further window actions in the macro.\n\n<p>'
        'If a macro has no "Find a window" actions, all window actions will '
        'target the frontmost window.<p>'
        'In the edit boxes you can use the curly brace wildcards {*} to match '
        'any string sequence and {?} to match a single letter.'
    )
    iconFile = "icons/FindWindow"
    class text:
        label = "Find Window: %s"
        label2 = "Find frontmost window"
        drag1 = "Drag me to\na window."
        drag2 = "Now move me\nto a window."
        refresh_btn = "&Refresh"
        onlyFrontmost = "Only match frontmost window"
        invisible_box = "Search invisible items also"
        hide_box = "Hide EventGhost while dragging"
        stopMacro = [
            "Stop macro if target is not found",
            "Stop macro if target is found",
            "Never stop macro"
        ]
        matchNum1 = "Only return"
        matchNum2 = "'th match"
        wait1 = "Wait up to"
        wait2 = "seconds for the window to appear."
        testButton = "Test"
        options = (
            "Program:",
            "Window Name:",
            "Window Class:",
            "Child Name:",
            "Child Class:"
        )


    def Compile(
        self,
        program=None,
        winName=None,
        winClass=None,
        childName=None,
        childClass=None,
        matchNum=1,
        includeInvisible=False,
        timeout=0,
        stopMacro=STOP_IF_NOT_FOUND
    ):
        if stopMacro is None:
            return UseForegroundWindowOnly

        matcher = eg.WindowMatcher(
            program,
            winName,
            winClass,
            childName,
            childClass,
            matchNum,
            includeInvisible,
            timeout,
        )
        def Do():
            hwnds = matcher()
            if (
                (stopMacro == STOP_IF_NOT_FOUND and not hwnds)
                or (stopMacro == STOP_IF_FOUND and hwnds)
            ):
                eg.programCounter = None
            eg.lastFoundWindows[:] = hwnds
            return hwnds
        return Do



    def GetLabel(self, program, *args):
        if args[7] is None:
            return self.text.label2
        else:
            return self.text.label % basename(program or '')


    def Configure(
        self,
        program="",
        winName=None,
        winClass=None,
        childName=None,
        childClass=None,
        matchNum=1,
        includeInvisible=False,
        timeout=0,
        stop=STOP_IF_NOT_FOUND
    ):
        panel = eg.ConfigPanel(resizable=True)
        text = self.text
        searchOnlyFrontmost = False
        if stop is None:
            program = ""
            matchNum = 1
            includeInvisible = False
            timeout = 0
            stop = 0
            searchOnlyFrontmost = True
        self.dialog = panel.dialog
        self.lastHwnd = None
        self.lastPid = None
        self.hideOnDrag = True

        # the "only search for the frontmost" checkbox
        cbOnlyFrontmost = wx.CheckBox(panel, -1, text.onlyFrontmost)
        def OnSearchOnlyFrontmostCheckbox(event):
            flag = not cbOnlyFrontmost.IsChecked()
            cbIncludeInvisible.Enable(flag)
            if not flag:
                stopMacroCtrl_1.SetValue(False)
                stopMacroCtrl_2.SetValue(False)
            stopMacroCtrl_1.Enable(flag)
            stopMacroCtrl_2.Enable(flag)
            waitCtrl.Enable(flag)
            for checkBox, textCtrl in self.options[:-1]:
                checkBox.Enable(flag)
                textCtrl.Enable(flag and checkBox.GetValue())
            self.options[-1][0].Enable(flag)
            self.options[-1][1].Enable(flag)
            event.Skip()
        cbOnlyFrontmost.Bind(wx.EVT_CHECKBOX, OnSearchOnlyFrontmostCheckbox)

        # the IncludeInvisible checkbox
        cbIncludeInvisible = wx.CheckBox(panel, -1, text.invisible_box)
        def OnIncludeInvisibleCheckbox(event):
            hwnd = self.lastHwnd
            self.tree.includeInvisible = cbIncludeInvisible.IsChecked()
            self.tree.Refresh()
            self.tree.SelectHwnd(hwnd)
            event.Skip()
        cbIncludeInvisible.Bind(wx.EVT_CHECKBOX, OnIncludeInvisibleCheckbox)

        # the stop-macro choice
        id_1 = wx.NewId()
        stopMacroCtrl_1 = wx.CheckBox(panel, id_1, text.stopMacro[0])
        id_2 = wx.NewId()
        stopMacroCtrl_2 = wx.CheckBox(panel, id_2, text.stopMacro[1])

        if stop == STOP_IF_NOT_FOUND:
            stopMacroCtrl_1.SetValue(True)
            stopMacroCtrl_2.Enable(False)
        elif stop == STOP_IF_FOUND:
            stopMacroCtrl_2.SetValue(True)
            stopMacroCtrl_1.Enable(False)

        def OnStopMacroCtrl(event):
           # if cbOnlyFrontmost.IsChecked():
            id = event.GetId()
            flag = event.IsChecked()
            if id == id_1:
                stopMacroCtrl_2.Enable(not flag)
                if flag:
                    stopMacroCtrl_2.SetValue(False)
            else:
                stopMacroCtrl_1.Enable(not flag)
                if flag:
                    stopMacroCtrl_1.SetValue(False)
            event.Skip()
        stopMacroCtrl_1.Bind(wx.EVT_CHECKBOX, OnStopMacroCtrl)
        stopMacroCtrl_2.Bind(wx.EVT_CHECKBOX, OnStopMacroCtrl)



        finderTool = eg.WindowDragFinder(
            panel,
            self.OnFinderToolLeftClick,
            self.OnFinderTool
        )
        self.finderTool = finderTool

        # the HideOnDrag checkbox
        cbHideOnDrag = wx.CheckBox(panel, -1, text.hide_box)
        cbHideOnDrag.SetValue(Config.hideOnDrag)
        def OnHideOnDragCheckbox(dummyEvent):
            Config.hideOnDrag = cbHideOnDrag.IsChecked()
        cbHideOnDrag.Bind(wx.EVT_CHECKBOX, OnHideOnDragCheckbox)

        # the tree to display processes and windows
        self.tree = eg.WindowTree(panel, includeInvisible=includeInvisible)
        cbIncludeInvisible.SetValue(includeInvisible)

        # the refresh button
        refreshButton = wx.Button(panel, -1, text.refresh_btn)
        def OnButton(dummyEvent):
            hwnd = self.lastHwnd
            self.tree.Refresh()
            self.tree.SelectHwnd(hwnd)
        refreshButton.Bind(wx.EVT_BUTTON, OnButton)

        # construction of the layout with sizers
        dragSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, "Drag Finder"),
            wx.VERTICAL
        )
        dragSizer.Add(finderTool, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM, 4)
        dragSizer.Add(cbHideOnDrag)

        leftTopSizer = wx.BoxSizer(wx.VERTICAL)
        leftTopSizer.Add(cbOnlyFrontmost, 0, wx.BOTTOM, 5)
        leftTopSizer.Add(cbIncludeInvisible, 0, wx.BOTTOM, 5)
        leftTopSizer.Add(stopMacroCtrl_1, 0, wx.BOTTOM, 5)
        leftTopSizer.Add(stopMacroCtrl_2, 0, wx.BOTTOM, 5)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(leftTopSizer, 1, wx.EXPAND)
        topSizer.Add(dragSizer)

        sizer1 = wx.GridBagSizer(vgap=4, hgap=4)
        sizer1.SetEmptyCellSize((0, 0))
        sizer1.Add(self.tree, (0, 0), (1, 5), wx.EXPAND)
        sizer1.Add(refreshButton, (1, 4), (2, 1), wx.ALIGN_TOP|wx.ALIGN_RIGHT)

        self.options = options = []

        def Wrapper(textCtrl, checkBox):
            def OnCheckBox(event):
                textCtrl.Enable(checkBox.GetValue())
                event.Skip()
            return OnCheckBox

        def MakeLine(line, checkBoxText, value):
            checkBox = wx.CheckBox(panel, -1, checkBoxText)
            sizer1.Add(checkBox, (line, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
            textCtrl = wx.TextCtrl(panel, -1, size=(20, -1))
            if value is not None:
                checkBox.SetValue(True)
                textCtrl.SetValue(value)
            else:
                textCtrl.Enable(False)
            sizer1.Add(textCtrl, (line, 1), (1, 3), wx.EXPAND)
            checkBox.Bind(wx.EVT_CHECKBOX, Wrapper(textCtrl, checkBox))
            options.append((checkBox, textCtrl))
            line += 1

        MakeLine(1, text.options[0], program)
        MakeLine(2, text.options[1], winName)
        MakeLine(3, text.options[2], winClass)
        MakeLine(4, text.options[3], childName)
        MakeLine(5, text.options[4], childClass)
        line = 6
        numMatchCB = wx.CheckBox(panel, -1, text.matchNum1)
        numMatchCB.SetValue(bool(matchNum))
        sizer1.Add(numMatchCB, (line, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        numMatchCtrl = eg.SpinIntCtrl(panel, -1, matchNum or 1, 1)
        sizer1.Add(numMatchCtrl, (line, 1), (1, 1), wx.EXPAND)
        sizer1.Add(
            wx.StaticText(panel, -1, text.matchNum2),
            (line, 2),
            (1, 3),
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT
        )
        numMatchCB.Bind(wx.EVT_CHECKBOX, Wrapper(numMatchCtrl, numMatchCB))
        options.append((numMatchCB, numMatchCtrl))
        line += 1

        # the wait parameter
        waitCtrl = eg.SpinNumCtrl(panel)
        waitCtrl.SetValue(timeout)

        sizer1.Add(
            panel.StaticText(text.wait1),
            (line, 0),
            (1, 1),
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT
        )
        sizer1.Add(
            waitCtrl,
            (line, 1),
            (1, 1),
            wx.ALIGN_CENTER_VERTICAL|wx.EXPAND
        )
        sizer1.Add(
            panel.StaticText(text.wait2),
            (line, 2),
            (1, 3),
            wx.ALIGN_CENTER_VERTICAL
        )
        line += 1
        sizer1.Add((1, 1), (line, 0))
        sizer1.AddGrowableCol(2, 100)
        sizer1.AddGrowableRow(0, 100)
        #sizer1.SetItemMinSize(options[0][1], 300, -1)

        # group the main lines together
        panel.sizer.AddMany([
            (topSizer, 0, wx.EXPAND),
            ((5, 5), ),
            (sizer1, 1, wx.EXPAND),
        ])
        # re-assign the test button
        def OnTestButton(dummyEvent):
            args = GetResult()[:-2] # we don't need timeout and stopMacro
                                    # parameter
            hwnds = eg.WindowMatcher(*args)()
            dialog = TestDialog(panel.dialog, hwnds)
            dialog.ShowModal()
            dialog.Destroy()
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnTestButton)

        @eg.LogIt
        def GetResult():
            resultList = []
            for checkBox, textCtrl in options:
                if not checkBox.IsChecked():
                    resultList.append(None)
                else:
                    resultList.append(textCtrl.GetValue())
            resultList.append(self.tree.includeInvisible)
            resultList.append(waitCtrl.GetValue())
            if stopMacroCtrl_1.IsChecked():
                resultList.append(STOP_IF_NOT_FOUND)
            elif stopMacroCtrl_2.IsChecked():
                resultList.append(STOP_IF_FOUND)
            else:
                resultList.append(STOP_NEVER)
            return resultList

        hwnds = eg.WindowMatcher(
            program,
            winName,
            winClass,
            childName,
            childClass,
            matchNum,
            includeInvisible,
        )()
        if matchNum is not None and len(hwnds):
            self.lastHwnd = hwnds[0]
            self.tree.SelectHwnd(self.lastHwnd)
        if searchOnlyFrontmost:
            cbOnlyFrontmost.SetValue(True)
            OnSearchOnlyFrontmostCheckbox(wx.CommandEvent())
        while True:
            self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
            affirmed = panel.Affirmed()
            self.tree.Unbind(wx.EVT_TREE_SEL_CHANGED)
            if not affirmed:
                break
            if cbOnlyFrontmost.IsChecked():
                panel.SetResult(
                    None, None, None, None, None, None, None, None, None
                )
            else:
                panel.SetResult(*GetResult())


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass


    @eg.LogIt
    def OnSelectionChanged(self, event):
        event.Skip()
        tree = self.tree
        item = tree.GetSelection()
        if not item.IsOk():
            return
        hwnd = tree.GetPyData(item)
        eg.PrintDebugNotice("HWND:", hwnd)
        if tree.GetItemParent(item) == tree.root:
            # only selected a program
            pid = hwnd
            hwnd = None
        else:
            pid = GetWindowThreadProcessId(hwnd)[1]

        if pid == self.lastPid and hwnd == self.lastHwnd:
            return
        self.lastPid = pid
        self.lastHwnd = hwnd
        exe = GetProcessName(pid)

        def SetOption(flag, option, value):
            checkBox, textCtrl = option
            checkBox.SetValue(flag)
            textCtrl.SetValue(value)
            textCtrl.Enable(flag)

        rootHwnd = None
        options = self.options
        SetOption(bool(exe), options[0], exe)
        if hwnd is not None:
            rootHwnd = GetAncestor(hwnd, GA_ROOT)
            targetWinName = GetWindowText(rootHwnd)
            targetWinClass = GetClassName(rootHwnd)
            SetOption(True, options[1], targetWinName)
            SetOption(True, options[2], targetWinClass)
        else:
            SetOption(False, options[1], "")
            SetOption(False, options[2], "")
        if rootHwnd is not None and rootHwnd != hwnd:
            targetWinName = GetWindowText(hwnd)
            targetWinClass = GetClassName(hwnd)
            SetOption(True, options[3], targetWinName)
            SetOption(True, options[4], targetWinClass)
            searchHwnd = hwnd
            data = [
                child
                for child in GetWindowChildsList(
                    rootHwnd,
                    tree.includeInvisible
                )
                    if (
                        GetClassName(child) == targetWinClass and
                        GetWindowText(child) == targetWinName
                    )
            ]
            try:
                count = data.index(searchHwnd) + 1
            except:
                count = 0
        else:
            SetOption(False, options[3], "")
            SetOption(False, options[4], "")
            if rootHwnd is not None:
                data = [
                    hwnd
                    for hwnd in GetTopLevelWindowList(tree.includeInvisible)
                        if (
                            GetClassName(hwnd) == targetWinClass and
                            GetWindowText(hwnd) != targetWinName and
                            GetWindowThreadProcessId(hwnd)[1] == pid
                        )
                ]
                count = len(data)
            else:
                count = 0
        SetOption(count > 0, options[5], count or 1)


    @eg.LogIt
    def OnFinderToolLeftClick(self, dummyEvent=None):
        self.oldFramePosition = eg.document.frame.GetPosition()
        self.oldDialogPosition = self.dialog.GetPosition()
        if Config.hideOnDrag:
            eg.document.frame.SetPosition((-32000, -32000))
            self.dialog.SetPosition((-32000, -32000))
        #event.Skip()


    @eg.LogIt
    def OnFinderTool(self, dummyEvent=None):
        if Config.hideOnDrag:
            eg.document.frame.SetPosition(self.oldFramePosition)
            self.dialog.SetPosition(self.oldDialogPosition)
        lastTarget = self.finderTool.GetValue()
        if lastTarget is not None:
            self.tree.Unselect()
            self.tree.Refresh()
            self.tree.SelectHwnd(lastTarget)

