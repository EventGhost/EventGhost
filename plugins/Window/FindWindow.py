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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from time import sleep
from win32api import GetCurrentProcessId
from win32process import EnumProcesses
from os.path import basename, join, dirname
from win32gui import (
    EnumWindows, 
    EnumChildWindows, 
    IsWindowVisible, 
    GetWindowText, 
    GetClassName
)
from win32process import GetWindowThreadProcessId

from ctypes.dynamic import GetAncestor, GA_ROOT, GA_PARENT
from eg.WinAPI.Utils import (
    GetHwndIcon, 
    GetHwndChildren, 
    HwndHasChildren,
    HighlightWindow,
    GetNameOfPID, 
)
        

ourProcessID = GetCurrentProcessId()

STOP_IF_NOT_FOUND = 0
STOP_IF_FOUND = 1
STOP_NEVER = 2


class TestDialog(eg.Dialog):  
    
    def __init__(self, parent, hwnds):
        eg.Dialog.__init__(self, parent, title="Found Windows", size=(500, 200))
        list = eg.WindowList(self, hwnds)
        okButton = wx.Button(self, wx.ID_OK)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(list, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(okButton, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.SetSizer(sizer)
        

                
def UseForegroundWindowOnly():
    """ Instruct EventGhost to use the active desktop window only, by 
        clearing eg.lastFoundWindows
    """
    del eg.lastFoundWindows[:]
    return []
    
                
                
class FindWindow(eg.ActionClass):
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

    def __init__(self):
        class Defaults:
            hideOnDrag = False
        self.config = eg.GetConfig("plugins.Window.FindWindow", Defaults)
            
            
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
        panel = eg.ConfigPanel(self, resizeable=True)
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
            stopMacroCtrl.Enable(flag)
            waitCtrl.Enable(flag)
            for cb, tb in self.options[:-1]:
                cb.Enable(flag)
                tb.Enable(flag and cb.GetValue())
            self.options[-1][0].Enable(flag)
            self.options[-1][1].Enable(flag)
            event.Skip()
        cbOnlyFrontmost.Bind(wx.EVT_CHECKBOX, OnSearchOnlyFrontmostCheckbox)
        
        # the IncludeInvisible checkbox
        cbIncludeInvisible = wx.CheckBox(panel, -1, text.invisible_box)
        def OnCheckbox(event):
            tmp = self.lastHwnd
            tree.includeInvisible = cbIncludeInvisible.IsChecked()
            tree.Refresh()
            tree.SelectHwnd(tmp)
            event.Skip()
        cbIncludeInvisible.Bind(wx.EVT_CHECKBOX, OnCheckbox)
        
        # the stop-macro choice
        stopMacroCtrl = wx.CheckBox(panel, -1, text.stopMacro[0])
        if stop != 2:
            stopMacroCtrl.SetValue(True)
        
        finderTool = eg.WindowDragFinder(
            panel, 
            self.OnFinderToolLeftClick, 
            self.OnFinderTool
        )
        self.finderTool = finderTool
        
        # the HideOnDrag checkbox
        cbHideOnDrag = wx.CheckBox(panel, -1, text.hide_box)
        cbHideOnDrag.SetValue(self.config.hideOnDrag)
        def OnCheckbox(event):
            self.config.hideOnDrag = cbHideOnDrag.IsChecked()     
        cbHideOnDrag.Bind(wx.EVT_CHECKBOX, OnCheckbox)

        # the tree to display processes and windows
        tree = self.tree = WindowTree(panel, -1, includeInvisible)
        cbIncludeInvisible.SetValue(includeInvisible)
                        
        # the refresh button
        refreshButton = wx.Button(panel, -1, text.refresh_btn)
        def OnButton(event):
            tmp = self.lastHwnd
            tree.Refresh()
            tree.SelectHwnd(tmp)
        refreshButton.Bind(wx.EVT_BUTTON, OnButton)

        # construction of the layout with sizers
        dragSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, "Drag Finder"), 
            wx.VERTICAL
        )
        dragSizer.Add(finderTool, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM, 4)
        dragSizer.Add(cbHideOnDrag)

        topSizer = wx.GridBagSizer(vgap=0, hgap=0)
        topSizer.AddGrowableCol(2, 100)
        topSizer.SetEmptyCellSize((0, 0))
        Add = topSizer.Add
        Add(cbOnlyFrontmost, (0, 0), (1, 2), wx.ALIGN_CENTER_VERTICAL)
        Add(cbIncludeInvisible, (1, 0), (1, 2), wx.ALIGN_CENTER_VERTICAL)
        Add(
            stopMacroCtrl, 
            (2, 0), 
            (1, 2), 
            wx.TOP|wx.ALIGN_BOTTOM|wx.EXPAND, 
            3
        )
        Add((10,1), (0, 2), (2, 1))
        Add(dragSizer, (0, 3), (3, 1), wx.ALIGN_TOP)
        
        sizer1 = wx.GridBagSizer(vgap=4, hgap=4)
        sizer1.AddGrowableCol(2, 100)
        sizer1.AddGrowableRow(0, 100)
        sizer1.SetEmptyCellSize((0, 0))
        sizer1.Add(tree, (0, 0), (1, 5), wx.EXPAND)
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
        #sizer1.SetItemMinSize(options[0][1], 300, -1)
        
        # group the main lines together
        Add = panel.sizer.Add
        Add(topSizer, 0, wx.EXPAND)
        Add((5,5))
        Add(sizer1, 1, wx.EXPAND)

        # re-assign the test button
        def OnButton(event):
            args = GetResult()[:-2] # we don't need timeout and stopMacro parameter
            hwnds = eg.WindowMatcher(*args)()
            TestDialog(panel.dialog, hwnds).ShowModal()
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)
        
        @eg.LogIt
        def GetResult():
            resultList = []
            for cb, tb in options:
                if not cb.IsChecked():
                    resultList.append(None)
                else:
                    resultList.append(tb.GetValue())
            resultList.append(tree.includeInvisible)
            resultList.append(waitCtrl.GetValue())
            if stopMacroCtrl.IsChecked():
                resultList.append(STOP_IF_NOT_FOUND)
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
        if matchNum is not None and len(hwnds) >= matchNum:
            self.lastHwnd = hwnds[matchNum-1]
            tree.SelectHwnd(self.lastHwnd)
        if searchOnlyFrontmost:
            cbOnlyFrontmost.SetValue(True)
            OnSearchOnlyFrontmostCheckbox(wx.CommandEvent())
        while True:
            tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
            ok = panel.Affirmed()
            tree.Unbind(wx.EVT_TREE_SEL_CHANGED)
            if ok:
                if cbOnlyFrontmost.IsChecked():
                    panel.SetResult(None, None, None, None, None, None, None, None, None)
                else:
                    panel.SetResult(*GetResult())
            else:
                break
    

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
        exe = basename(GetNameOfPID(pid))
        
        def SetOption(flag, option, value):                
            checkBox, textCtrl = option
            checkBox.SetValue(flag)
            textCtrl.SetValue(value)
            textCtrl.Enable(flag)
        
        data = [0]
        def EnumChildProc(hwnd, data):
            if not tree.includeInvisible and not IsWindowVisible(hwnd):
                return True
            if GetClassName(hwnd) != targetWinClass:
                return True
            if GetWindowText(hwnd) != targetWinName:
                return True
            data[0] += 1
            return hwnd != search_hwnd

        def EnumWindowsProc(hwnd, data):
            if not tree.includeInvisible and not IsWindowVisible(hwnd):
                return True
            if GetClassName(hwnd) != targetWinClass:
                return True
            if GetWindowText(hwnd) != targetWinName:
                return True
            if GetWindowThreadProcessId(hwnd)[1] != pid:
                return True
            data[0] += 1
            return hwnd != rootHwnd

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
            search_hwnd = hwnd
            try:
                EnumChildWindows(rootHwnd, EnumChildProc, data)
            except:
                pass
        else:
            SetOption(False, options[3], "")
            SetOption(False, options[4], "")
            if rootHwnd is not None:
                try:
                    EnumWindows(EnumWindowsProc, data)
                except:
                    pass
                    
        count = data[0]
        SetOption(count > 0, options[5], count or 1)
        
            
    @eg.LogIt
    def OnFinderToolLeftClick(self, event=None):
        self.oldFramePosition = eg.document.frame.GetPosition()
        self.oldDialogPosition = self.dialog.GetPosition()
        if self.config.hideOnDrag:
            eg.document.frame.SetPosition((-32000, -32000))
            self.dialog.SetPosition((-32000, -32000))
        #event.Skip()
        
        
    @eg.LogIt
    def OnFinderTool(self, event=None):
        if self.config.hideOnDrag:
            eg.document.frame.SetPosition(self.oldFramePosition)
            self.dialog.SetPosition(self.oldDialogPosition)
        lastTarget = self.finderTool.GetValue()
        if lastTarget is not None:
            self.tree.Unselect()
            self.tree.Refresh()
            self.tree.SelectHwnd(lastTarget)

        
    

class WindowTree(wx.TreeCtrl):
    
    def __init__(self, parent, id=-1, includeInvisible=False):
        self.includeInvisible = includeInvisible
        wx.TreeCtrl.__init__(
            self, 
            parent, 
            -1, 
            style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT, 
            size=(-1, 150)
        )
        path = join(dirname(__file__), "icons")
        self.imageList = imageList = wx.ImageList(16, 16)
        imageList.Add(wx.Bitmap(join(path, "cwindow.png")))
        imageList.Add(wx.Bitmap(join(path, "cedit.png")))
        imageList.Add(wx.Bitmap(join(path, "cstatic.png")))
        imageList.Add(wx.Bitmap(join(path, "cbutton.png")))
        self.SetImageList(imageList)
        self.root = self.AddRoot("")
        
        # tree context menu
        menu = eg.Menu(self, "")
        
        def OnCmdHighlight(event):
            hwnd = self.GetPyData(self.GetSelection())
            for i in range(10):
                HighlightWindow(hwnd)
                sleep(0.1)
        menu.Append("Highlight", OnCmdHighlight)
        
        def OnPopupMenu(event):
            self.PopupMenu(menu)        
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, OnPopupMenu)
        
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.AppendPrograms()
        
        
    def OnItemExpanding(self, event):
        item = event.GetItem()
        if self.IsExpanded(item):  
            # This event can happen twice in the self.Expand call
            return
            
        res = self.GetItemParent(item)
        if res == self.root:
            pid = self.GetPyData(item)
            self.AppendToplevelWindows(pid, item)
        else:
            hwnd = self.GetPyData(item)
            self.AppendChildWindows(hwnd, item)


    def OnItemCollapsed(self, event):
        # We need to remove all children here, otherwise we'll see all
        # that old rubbish again after the next expansion.
        self.DeleteChildren(event.GetItem())
        
        
    def AppendPrograms(self):
        self.pids = {}
        processes = EnumProcesses()    # get PID list
        for pid in processes:
            self.pids[pid] = []
            
        hwnds = []
        def EnumProc(hwnd, data):
            data.append(hwnd)
            return True
        EnumWindows(EnumProc, hwnds)
        
        for hwnd in hwnds:
            threadID, pid = GetWindowThreadProcessId(hwnd)
            if pid == ourProcessID:
                continue
            if not self.includeInvisible and not IsWindowVisible(hwnd):
                continue
            self.pids[pid].append(hwnd)

        for pid in processes:
            if len(self.pids[pid]) == 0:
                continue
            iconIndex = 0
            for hwnd in self.pids[pid]:
                icon = GetHwndIcon(hwnd)
                if icon:
                    iconIndex = self.imageList.AddIcon(icon)
                    break
            exe = basename(GetNameOfPID(pid))
            item = self.AppendItem(self.root, exe)
            self.SetItemHasChildren(item, True)
            self.SetPyData(item, pid)
            self.SetItemImage(item, iconIndex, which=wx.TreeItemIcon_Normal)
                 
                
    def AppendToplevelWindows(self, pid, item):
        hwnds = self.pids[pid]
        for hwnd in hwnds:
            try:
                name = GetWindowText(hwnd)
                className = GetClassName(hwnd)
                icon = GetHwndIcon(hwnd)
            except:
                continue
            if name != '':
                name = '"%s"' % name
            icon_index = 0
            if icon:
                icon_index = self.imageList.AddIcon(icon)
            new_item = self.AppendItem(item, name)
            self.SetPyData(new_item, hwnd)
            self.SetItemText(new_item, name + className)
            self.SetItemImage(
                new_item, 
                icon_index, 
                which=wx.TreeItemIcon_Normal
            )
            if HwndHasChildren(hwnd, self.includeInvisible):
                self.SetItemHasChildren(new_item, True)
            
            
    def AppendChildWindows(self, parentHwnd, item):
        for hwnd in GetHwndChildren(parentHwnd, self.includeInvisible):
            try:
                name = GetWindowText(hwnd)
                className = GetClassName(hwnd)
            except:
                continue
            if name != "":
                name = "\"" + name + "\" "
            index = self.AppendItem(item, name + className, 0)
            self.SetPyData(index, hwnd)
            if className == "Edit" or className == "TEdit":
                self.SetItemImage(index, 1, which=wx.TreeItemIcon_Normal)
            elif className == "Static" or className == "TStaticText":
                self.SetItemImage(index, 2, which=wx.TreeItemIcon_Normal)
            elif className == "Button" or className == "TButton":
                self.SetItemImage(index, 3, which=wx.TreeItemIcon_Normal)
            elif GetClassName(parentHwnd) == "MDIClient":
                icon = GetHwndIcon(hwnd)
                if icon:
                    iconIndex = self.imageList.AddIcon(icon)
                    self.SetItemImage(
                        index, 
                        iconIndex, 
                        which=wx.TreeItemIcon_Normal
                    )
                
            if HwndHasChildren(hwnd, self.includeInvisible):
                self.SetItemHasChildren(index, True)
                
                
    @eg.LogIt
    def Refresh(self):
        self.Freeze()
        self.DeleteChildren(self.root)
        self.AppendPrograms()
        self.Thaw()
                          
                        
    @eg.LogIt
    def Destroy(self):
        self.Unselect()
        self.imageList.Destroy()
        return wx.TreeCtrl.Destroy(self)
    
    
    @eg.LogIt
    def SelectHwnd(self, hwnd):
        if hwnd is None:
            self.Unselect()
            return
        pid = GetWindowThreadProcessId(hwnd)[1]
        item, cookie = self.GetFirstChild(self.root)
        while self.GetPyData(item) != pid:
            item, cookie = self.GetNextChild(self.root, cookie)
            if not item.IsOk():
                return

        chain = [hwnd]
        rootHwnd = GetAncestor(hwnd, GA_ROOT)
        tmp = hwnd
        while tmp != rootHwnd:
            tmp = GetAncestor(tmp, GA_PARENT)
            chain.append(tmp)
        
        lastItem = item
        for child in chain[::-1]:
            self.Expand(item)
            item, cookie = self.GetFirstChild(lastItem)
            while self.GetPyData(item) != child:
                item, cookie = self.GetNextChild(lastItem, cookie)
                if not item.IsOk():
                    return
            lastItem = item
        self.SelectItem(lastItem)            
        
        
    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
        
        
