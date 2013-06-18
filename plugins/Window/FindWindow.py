import os, sys, time
import win32api, win32con
import types
import cStringIO

from win32process import EnumProcesses, GetModuleFileNameEx
from os.path import basename
from win32gui import (
    EnumWindows, 
    EnumChildWindows, 
    IsWindowVisible, 
    GetWindowText, 
    GetClassName
)
from win32process import GetWindowThreadProcessId


import wx


import eg
from eg.WinAPI.win32types import GetAncestor, GA_ROOT, GA_PARENT
from eg.WinAPI.Utils import GetHwndIcon, GetHwndChildren, HwndHasChildren
from eg.WinAPI.Utils import HighlightWindow
from eg.WinAPI.Utils import GetModulesPID, GetNameOfPID, GetHwndProcessName

from eg.Controls.WindowDragFinder import WindowDragFinder
from eg.IconTools import GetIcon
from compile_string import compile_string
        


ourProcessID = win32api.GetCurrentProcessId()



def FindWindowByChain(exeName=None, winChain=None, includeInvisible=False):
    pids = GetModulesPID(basename(exeName))
    hwnds = []
    pids_hwnds = []
    for i in pids:
        pids_hwnds.append([])
        
    def EnumProc(hwnd, data):
        _, pid = GetWindowThreadProcessId(hwnd)
        if pid in pids:
            if not includeInvisible and not IsWindowVisible(hwnd):
                return True
            pids_hwnds[pids.index(pid)].append(hwnd)
        return True
    
    EnumWindows(EnumProc, None)
        
    def MatchWindow(hwnds, level, result):
        titleName, className, count = winChain[level]
        i = 0
        for hwnd in hwnds:
            if titleName != GetWindowText(hwnd):
                continue
            if className != GetClassName(hwnd):
                continue
            i += 1
            if count != i:
                continue
            if len(winChain) > level + 1:
                hwnds = GetHwndChildren(hwnd, includeInvisible)
                MatchWindow(hwnds, level + 1, result)
                return True
            else:
                result.append(hwnd)
                return True
        return False
            
    result = []
    for pid in pids:
        MatchWindow(pids_hwnds[pids.index(pid)], 0, result)
    return result


def FindWindowWait(
    exeName=None, 
    winChain=None, 
    includeInvisible=False, 
    timeout=0
):
    endtime = time.clock() + timeout
    while 1:
        hwnds = FindWindowByChain(exeName, winChain, includeInvisible)
        if hwnds:
            return hwnds
        if time.clock() >= endtime:
            return []
        eg.Wait(0.1)
                


class WindowMatcher:
    
    def __init__(
        self, 
        program, 
        winName=None, 
        winClass=None, 
        childName=None,
        childClass=None, 
        matchNum=1, 
        includeInvisible=False, 
        timeout=0, 
        stop=2
    ):
        #eg.whoami()
        self.timeout = timeout
        self.matchNum = matchNum or 0
        self.stop = stop
        dummy = (lambda x: True)
        if not includeInvisible:
            self.invisibleMatch = IsWindowVisible
        else:
            self.invisibleMatch = dummy
            
        self.program = compile_string(program)
        self.winNameMatch = compile_string(winName) or dummy
        self.winClassMatch = compile_string(winClass) or dummy
        self.scanChilds = False
        if (childName is not None) or (childClass is not None):
            self.scanChilds = True
            self.childNameMatch = compile_string(childName) or dummy
            self.childClassMatch = compile_string(childClass) or dummy
    
    
    def EnumWindowsProc(self, hwnd, add):
        if not self.invisibleMatch(hwnd):
            return True
        if not self.winClassMatch(GetClassName(hwnd)):
            return True
        if not self.winNameMatch(GetWindowText(hwnd)):
            return True
        add(hwnd)
        return True
    
    
    def EnumChildsProc(self, hwnd, add):
        if not self.invisibleMatch(hwnd):
            return True
        if not self.childClassMatch(GetClassName(hwnd)):
            return True
        if not self.childNameMatch(GetWindowText(hwnd)):
            return True
        add(hwnd)
        return True
        
        
    def Enumerate(self):
        top_hwnds = []
        EnumWindows(self.EnumWindowsProc, top_hwnds.append)
        match = self.program
        if match is not None:
            top_hwnds = [
                hwnd for hwnd in top_hwnds if match(GetHwndProcessName(hwnd))
            ]
        if not self.scanChilds:
            return top_hwnds
        child_hwnds = []
        for hwnd in top_hwnds:
            try:
                EnumChildWindows(
                    hwnd, self.EnumChildsProc, child_hwnds.append
                )
            except:
                pass
        return child_hwnds


    def __call__(self):
        endtime = time.clock() + self.timeout
        matchNum = self.matchNum
        while 1:
            hwnds = self.Enumerate()
            if matchNum:
                if len(hwnds) >= matchNum:
                    hwnds = [hwnds[matchNum-1]]
                    break
            elif hwnds:
                break
            if time.clock() >= endtime:
                hwnds = []
                break
            eg.Wait(0.1)
        stop = self.stop
        if (stop == 0 and not hwnds) or (stop == 1 and hwnds):
            eg.SetProgramCounter(None)
        eg.lastFoundWindows[:] = hwnds
        return hwnds
        
            
    def Test(self):
        start = time.clock()
        res = self.Enumerate()
        execution_time = time.clock() - start
        print len(res), res, execution_time
        
        
    def __del__(self):
        eg.whoami()
                
                
                
def UseForegroundWindowOnly():
    """ Instruct EventGhost to use the active desktop window only, by 
        clearing eg.lastFoundWindows
    """
    del eg.lastFoundWindows[:]
    return []
    
                
                
class FindWindow(eg.ActionClass):
    name = "Find a window"
    iconFile = "FindWindow"
    class text:
        label = "Find Window: %s"
        label2 = "Find frontmost window"
        drag1 = "Drag me to\na window."
        drag2 = "Now move me\nto a window."
        refresh_btn = "&Refresh"
        onlyForground = "Only match frontmost window"
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
        class defaults:
            hideOnDrag = False
        self.config = eg.GetConfig("plugins.Window.FindWindow", defaults)
            
            
    def Compile(
        self, 
        program, 
        winName=None, 
        winClass=None, 
        childName=None,
        childClass=None, 
        matchNum=1, 
        includeInvisible=False, 
        timeout=0, 
        stop=2
    ):
        if type(winName) in (types.TupleType, types.ListType):
            class OldFindWindow:
                exe_path = program
                win_chain= winName
                include_invisible = winClass
                timeout = childName
                def __call__(self):
                    res = FindWindowWait(
                        self.exe_path, 
                        self.win_chain,
                        self.include_invisible, 
                        self.timeout
                    )
                    eg.lastFoundWindows[:] = res
                    return res
            return OldFindWindow()
        else:
            if stop is None:
                return UseForegroundWindowOnly

            return WindowMatcher(
                program, 
                winName, 
                winClass, 
                childName,
                childClass, 
                matchNum, 
                includeInvisible,
                timeout, 
                stop
            )
    
    
    def GetLabel(self, exe_path, *args):
        if args[7] is None:
            return self.text.label2
        else:
            return self.text.label % os.path.basename(exe_path or '')
    
    
    @eg.logit()
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
        stop=0
    ):
        dialog = eg.ConfigurationDialog(self, resizeable=True)
        text = self.text
        searchOnlyFrontmost = False
        if stop is None:
            program = ""
            matchNum = 1
            includeInvisible = False
            timeout = 0
            stop = 0
            searchOnlyFrontmost = True
        elif type(winName) in  (types.TupleType, types.ListType):
            program = basename(program)
            win_chain = winName
            includeInvisible = winClass
            timeout = childName
            winName = win_chain[0][0]
            winClass = win_chain[0][1]
            if len(win_chain) > 1:
                childName = win_chain[-1][0]
                childClass = win_chain[-1][1]
            else:
                childName = None
                childClass = None
        self.dialog = dialog
        self.lastHwnd = None
        self.lastPid = None
        self.hideOnDrag = True
        
        finderTool = WindowDragFinder(dialog, self.OnFinderToolLeftClick, self.OnFinderTool)
        #finderTool.Bind(wx.EVT_LEFT_DOWN, self.OnFinderToolLeftClick)
        #finderTool.Bind(wx.EVT_BUTTON, self.OnFinderTool)
        self.finderTool = finderTool
        
        # the "only search for the frontmost" checkbox
        force_front_cb = wx.CheckBox(dialog, -1, text.onlyForground)
        def OnSearchOnlyFrontmostCheckbox(event):
            flag = not force_front_cb.IsChecked()
            cbIncludeInvisible.Enable(flag)
            stopMacroCtrl.Enable(flag)
            waitCtrl.Enable(flag)
            for cb, tb in self.options[:-1]:
                cb.Enable(flag)
                tb.Enable(flag and cb.GetValue())
            self.options[-1][0].Enable(flag)
            self.options[-1][1].Enable(flag)
        force_front_cb.Bind(wx.EVT_CHECKBOX, OnSearchOnlyFrontmostCheckbox)
        
        # the IncludeInvisible checkbox
        cbIncludeInvisible = wx.CheckBox(dialog, -1, text.invisible_box)
        def OnCheckbox(event):
            tmp = self.lastHwnd
            tree.includeInvisible = cbIncludeInvisible.IsChecked()
            tree.Refresh()
            tree.SelectHwnd(tmp)
        cbIncludeInvisible.Bind(wx.EVT_CHECKBOX, OnCheckbox)
        
        # the HideOnDrag checkbox
        cbHideOnDrag = wx.CheckBox(dialog, -1, text.hide_box)
        cbHideOnDrag.SetValue(self.config.hideOnDrag)
        def OnCheckbox(event):
            self.config.hideOnDrag = cbHideOnDrag.IsChecked()     
        cbHideOnDrag.Bind(wx.EVT_CHECKBOX, OnCheckbox)

        # the tree to display processes and windows
        tree = self.tree = WindowTree(dialog, -1, includeInvisible)
        cbIncludeInvisible.SetValue(includeInvisible)
                
        # the wait parameter
        waitCtrl = eg.SpinNumCtrl(dialog)
        waitCtrl.SetValue(timeout)
        
        # the stop-macro choice
        stopMacroCtrl = wx.CheckBox(dialog, -1, text.stopMacro[0])
        if stop != 2:
            stopMacroCtrl.SetValue(True)
        
        
        # the refresh button
        refreshButton = wx.Button(dialog, -1, text.refresh_btn)
        def OnButton(event):
            tmp = self.lastHwnd
            tree.Refresh()
            tree.SelectHwnd(tmp)
        refreshButton.Bind(wx.EVT_BUTTON, OnButton)
        #dialog.buttonRow.Add(refreshButton)

        # the test button
        testButton = wx.Button(dialog, -1, text.testButton)
        def OnButton(event):
            WindowMatcher(*get_result()).Test()
        testButton.Bind(wx.EVT_BUTTON, OnButton)
        dialog.buttonRow.Add(testButton)
        
        #-----------------------------------------
        # construction of the layout with sizers
        #-----------------------------------------
        
        drag_sizer = wx.StaticBoxSizer(
            wx.StaticBox(dialog, -1, "Drag Finder"), 
            wx.VERTICAL
        )
        drag_sizer.Add(finderTool, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM, 4)
        drag_sizer.Add(cbHideOnDrag)

        top_sizer = wx.GridBagSizer(vgap=0, hgap=0)
        top_sizer.AddGrowableCol(2, 100)
        top_sizer.SetEmptyCellSize((0, 0))
        Add = top_sizer.Add
        Add(force_front_cb, (0, 0), (1, 2), wx.ALIGN_CENTER_VERTICAL)
        Add(cbIncludeInvisible, (1, 0), (1, 2), wx.ALIGN_CENTER_VERTICAL)
        Add(
            stopMacroCtrl, 
            (2, 0), 
            (1, 2), 
            wx.TOP|wx.ALIGN_BOTTOM|wx.EXPAND, 
            3
        )
        Add((10,1), (0, 2), (2, 1))
        Add(drag_sizer, (0, 3), (3, 1), wx.ALIGN_TOP)
        
        sizer1 = wx.GridBagSizer(vgap=4, hgap=4)
        sizer1.AddGrowableCol(2, 100)
        sizer1.AddGrowableRow(0, 100)
        sizer1.SetEmptyCellSize((0, 0))
        sizer1.Add(tree, (0, 0), (1, 5), wx.EXPAND)
        sizer1.Add(refreshButton, (1, 4), (2, 1), wx.ALIGN_TOP|wx.ALIGN_RIGHT)
        
        self.options = options = []
        
        def wrapper(tb, cb):
            def OnCheckBox(event):
                tb.Enable(cb.GetValue())
            return OnCheckBox
        
        def make_line(line, cb_text, value):
            cb = wx.CheckBox(dialog, -1, cb_text)
            sizer1.Add(cb, (line, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
            tb = wx.TextCtrl(dialog, -1, size=(20, -1))
            if value is not None:
                cb.SetValue(True)
                tb.SetValue(value)
            else:
                tb.Enable(False)
            sizer1.Add(tb, (line, 1), (1, 3), wx.EXPAND)
            cb.Bind(wx.EVT_CHECKBOX, wrapper(tb, cb))
            options.append((cb, tb))
            line += 1
            
        make_line(1, text.options[0], program)    
        make_line(2, text.options[1], winName)    
        make_line(3, text.options[2], winClass)    
        make_line(4, text.options[3], childName)    
        make_line(5, text.options[4], childClass)  
        line = 6
        numMatchCB = wx.CheckBox(dialog, -1, text.matchNum1)
        numMatchCB.SetValue(bool(matchNum))
        sizer1.Add(numMatchCB, (line, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        numMatchCtrl = eg.SpinIntCtrl(dialog, -1, matchNum or 1, 1)
        sizer1.Add(numMatchCtrl, (line, 1), (1, 1))
        sizer1.Add(
            wx.StaticText(dialog, -1, text.matchNum2), 
            (line, 2), 
            (1, 3), 
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT
        )
        numMatchCB.Bind(wx.EVT_CHECKBOX, wrapper(numMatchCtrl, numMatchCB))
        options.append((numMatchCB, numMatchCtrl))
        line += 1
        
        sizer1.Add(
            wx.StaticText(dialog, -1, text.wait1), 
            (line, 0), 
            (1, 1), 
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT
        )
        sizer1.Add(waitCtrl, (line, 1), (1, 1), wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(
            wx.StaticText(dialog, -1, text.wait2), 
            (line, 2), 
            (1, 3), 
            wx.ALIGN_CENTER_VERTICAL
        )
        line += 1
        sizer1.Add((1, 1), (line, 0))
        #sizer1.SetItemMinSize(options[0][1], 300, -1)
        
        # group the main lines together
        Add = dialog.sizer.Add
        Add(top_sizer, 0, wx.EXPAND)
        Add((5,5))
        Add(sizer1, 1, wx.EXPAND)

        def get_result():
            eg.whoami()
            res_list = []
            for cb, tb in options:
                if not cb.IsChecked():
                    res_list.append(None)
                else:
                    res_list.append(tb.GetValue())
            res_list.append(tree.includeInvisible)
            res_list.append(waitCtrl.GetValue())
            if stopMacroCtrl.IsChecked():
                res_list.append(0)
            else:
                res_list.append(2)
            #res_list.append(stopMacroCtrl.GetSelection())
            return res_list
        
        hwnds = WindowMatcher(
            program, 
            winName, 
            winClass, 
            childName,
            childClass, 
            matchNum, 
            includeInvisible,
            timeout, 
            stop
        ).Enumerate()
        if matchNum is not None and len(hwnds) >= matchNum:
            self.lastHwnd = hwnds[matchNum-1]
            tree.SelectHwnd(self.lastHwnd)
        if searchOnlyFrontmost:
            force_front_cb.SetValue(True)
            OnSearchOnlyFrontmostCheckbox(None)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        isOk = dialog.AffirmedShowModal()
        tree.Unbind(wx.EVT_TREE_SEL_CHANGED)
        if isOk:
            if force_front_cb.IsChecked():
                return None, None, None, None, None, None, None, None, None
            else:
                return get_result()
    

    def __del__(self):
        eg.whoami()
        
        
    def OnSelectionChanged(self, event):
        eg.whoami()
        event.Skip()
        tree = self.tree
        item = tree.GetSelection()
        if not item.IsOk():
            return
        hwnd = tree.GetPyData(item)
        eg.notice("HWND:", hwnd)
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
        
        def set_option(flag, option, value):                
            cb, tb = option
            cb.SetValue(flag)
            tb.SetValue(value)
            tb.Enable(flag)
        
        data = [0]
        def EnumChildProc(hwnd, data):
            if not tree.includeInvisible and not IsWindowVisible(hwnd):
                return True
            if GetClassName(hwnd) != search_class:
                return True
            if GetWindowText(hwnd) != search_name:
                return True
            data[0] += 1
            return hwnd != search_hwnd

        def EnumWindowsProc(hwnd, data):
            if not tree.includeInvisible and not IsWindowVisible(hwnd):
                return True
            if GetClassName(hwnd) != search_class:
                return True
            if GetWindowText(hwnd) != search_name:
                return True
            if GetWindowThreadProcessId(hwnd)[1] != pid:
                return True
            data[0] += 1
            return hwnd != root_hwnd

        root_hwnd = None
        options = self.options
        set_option(bool(exe), options[0], exe)
        if hwnd is not None:
            root_hwnd = GetAncestor(hwnd, GA_ROOT)
            search_name = GetWindowText(root_hwnd)
            search_class = GetClassName(root_hwnd)
            set_option(True, options[1], search_name)
            set_option(True, options[2], search_class)
        else:
            set_option(False, options[1], "")
            set_option(False, options[2], "")
        if root_hwnd is not None and root_hwnd != hwnd:
            search_name = GetWindowText(hwnd)
            search_class = GetClassName(hwnd)
            set_option(True, options[3], search_name)
            set_option(True, options[4], search_class)
            search_hwnd = hwnd
            try:
                EnumChildWindows(root_hwnd, EnumChildProc, data)
            except:
                pass
        else:
            set_option(False, options[3], "")
            set_option(False, options[4], "")
            if root_hwnd is not None:
                try:
                    EnumWindows(EnumWindowsProc, data)
                except:
                    pass
                    
        count = data[0]
        set_option(count > 0, options[5], count or 1)
        
            
    def OnFinderToolLeftClick(self, event=None):
        eg.whoami()
        self.oldFramePosition = eg.mainFrame.GetPosition()
        self.oldDialogPosition = self.dialog.GetPosition()
        if self.config.hideOnDrag:
            eg.mainFrame.SetPosition((-32000, -32000))
            self.dialog.SetPosition((-32000, -32000))
        #event.Skip()
        
        
    def OnFinderTool(self, event=None):
        eg.whoami()
        if self.config.hideOnDrag:
            eg.mainFrame.SetPosition(self.oldFramePosition)
            self.dialog.SetPosition(self.oldDialogPosition)
        lastTarget = self.finderTool.GetValue()
        if lastTarget is not None:
            self.tree.Unselect()
            self.tree.Refresh()
            self.tree.SelectHwnd(lastTarget)

        
    

class WindowTree(wx.TreeCtrl):
    STYLE = wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT
    
    def __init__(self, parent, id=-1, includeInvisible=False):
        self.includeInvisible = includeInvisible
        wx.TreeCtrl.__init__(
            self, 
            parent, 
            -1, 
            style=self.STYLE, 
            size=(-1, 150)
        )
        path = os.path.dirname(__file__)
        self.imageList = imageList = wx.ImageList(16, 16)
        imageList.Add(GetIcon(os.path.join(path, "cwindow.png")))
        imageList.Add(GetIcon(os.path.join(path, "cedit.png")))
        imageList.Add(GetIcon(os.path.join(path, "cstatic.png")))
        imageList.Add(GetIcon(os.path.join(path, "cbutton.png")))
        self.SetImageList(imageList)
        self.root = self.AddRoot("")
        
        # tree context menu
        menu = eg.Menu(self, "")
        
        def OnCmdHighlight(event):
            hwnd = self.GetPyData(self.GetSelection())
            for i in range(10):
                HighlightWindow(hwnd)
                time.sleep(0.1)
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
            icon_index = 0
            for hwnd in self.pids[pid]:
                icon = GetHwndIcon(hwnd)
                if icon:
                    icon_index = self.imageList.AddIcon(icon)
                    break
            exe = os.path.basename(GetNameOfPID(pid))
            item = self.AppendItem(self.root, exe)
            self.SetItemHasChildren(item, True)
            self.SetPyData(item, pid)
            self.SetItemImage(item, icon_index, which=wx.TreeItemIcon_Normal)
                 
                
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
                name = u'"' + name + '" '
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
            
            
    def AppendChildWindows(self, parent_hwnd, item):
        for hwnd in GetHwndChildren(parent_hwnd, self.includeInvisible):
            try:
                name = GetWindowText(hwnd)
                className = GetClassName(hwnd)
            except:
                continue
            if name != "":
                name = "\"" + name + "\" "
            index = self.AppendItem(item, name + className)
            self.SetPyData(index, hwnd)
            if className == "Edit" or className == "TEdit":
                self.SetItemImage(index, 1, which=wx.TreeItemIcon_Normal)
            elif className == "Static" or className == "TStaticText":
                self.SetItemImage(index, 2, which=wx.TreeItemIcon_Normal)
            elif className == "Button" or className == "TButton":
                self.SetItemImage(index, 3, which=wx.TreeItemIcon_Normal)
            elif GetClassName(parent_hwnd) == "MDIClient":
                icon = GetHwndIcon(hwnd)
                if icon:
                    icon_index = self.imageList.AddIcon(icon)
                    self.SetItemImage(
                        index, 
                        icon_index, 
                        which=wx.TreeItemIcon_Normal
                    )
                
            if HwndHasChildren(hwnd, self.includeInvisible):
                self.SetItemHasChildren(index, True)
                
                
    def Refresh(self):
        eg.whoami()
        self.Freeze()
        self.DeleteChildren(self.root)
        self.AppendPrograms()
        self.Thaw()
                          
                        
    def Destroy(self):
        eg.whoami()
        self.Unselect()
        self.imageList.Destroy()
        return wx.TreeCtrl.Destroy(self)
    
    
    def SelectHwnd(self, hwnd):
        eg.whoami()
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
        root_hwnd = GetAncestor(hwnd, GA_ROOT)
        tmp = hwnd
        while tmp != root_hwnd:
            tmp = GetAncestor(tmp, GA_PARENT)
            chain.append(tmp)
        
        last_item = item
        for child in chain[::-1]:
            self.Expand(item)
            item, cookie = self.GetFirstChild(last_item)
            while self.GetPyData(item) != child:
                item, cookie = self.GetNextChild(last_item, cookie)
                if not item.IsOk():
                    return
            last_item = item
        self.SelectItem(last_item)            
        
        
    def __del__(self):
        eg.whoami()
        
        
