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

import inspect
import re
import types
import wx
import wx.aui
from collections import defaultdict
from os.path import join

# Local imports
import eg
from eg.Classes.MainFrame.LogCtrl import LogCtrl
from eg.Classes.MainFrame.StatusBar import StatusBar
from eg.Classes.MainFrame.TreeCtrl import TreeCtrl
from eg.Icons import CreateBitmapOnTopOfIcon, GetInternalBitmap
from eg.WinApi.Dynamic import GetDesktopWindow, HH_DISPLAY_TOPIC, HtmlHelp
from eg.WinApi.Utils import BringHwndToFront

ADD_ICON = eg.Icons.ADD_ICON
ADD_PLUGIN_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.PLUGIN_ICON)
ADD_FOLDER_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.FOLDER_ICON)
ADD_MACRO_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.MACRO_ICON)
ADD_EVENT_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.EVENT_ICON)
ADD_ACTION_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.ACTION_ICON)

ID_DISABLED = wx.NewId()
ID_EXECUTE = wx.NewId()
ID_PYTHON = wx.NewId()
ID_TOOLBAR_EXECUTE = wx.NewId()

ID = defaultdict(wx.NewId, {
    "Save": wx.ID_SAVE,
    "Undo": wx.ID_UNDO,
    "Redo": wx.ID_REDO,
    "Cut": wx.ID_CUT,
    "Copy": wx.ID_COPY,
    "Python": ID_PYTHON,
    "Paste": wx.ID_PASTE,
    "Delete": wx.ID_DELETE,
    "Disabled": ID_DISABLED,
    "Execute": ID_EXECUTE,
})

Text = eg.text.MainFrame

class Config(eg.PersistentData):
    position = (50, 50)
    size = (700, 450)
    showToolbar = True
    logTime = False
    indentLog = True
    expandOnEvents = False
    perspective = None
    perspective2 = None
    ratio = 2.0


class MainFrame(wx.Frame):
    """
    This is the MainFrame of EventGhost
    """
    style = (
        wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.CAPTION |
        wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL
    )

    @eg.AssertInMainThread
    def __init__(self, document):
        """
        Create the MainFrame
        """
        self.document = document
        self.findDialog = None
        self.openDialogs = []
        self.lastClickedTool = None
        self.egEvent = None
        self.lastFocus = None

        wx.Frame.__init__(
            self,
            None,
            -1,
            document.GetTitle(),
            pos=Config.position,
            size=(1, 1),
            style=self.style
        )
        self.SetMinSize((400, 200))
        document.frame = self
        auiManager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_DEFAULT)
        self.auiManager = auiManager

        self.logCtrl = self.CreateLogCtrl()
        self.corConst = self.logCtrl.GetWindowBorderSize()[0] + \
            wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
        self.treeCtrl = self.CreateTreeCtrl()
        self.toolBar = self.CreateToolBar()
        self.menuBar = self.CreateMenuBar()
        self.statusBar = StatusBar(self)
        self.SetStatusBar(self.statusBar)

        # tree popup menu
        self.popupMenu = self.CreateTreePopupMenu()

        iconBundle = wx.IconBundle()
        iconBundle.AddIcon(eg.taskBarIcon.stateIcons[0])
        icon = wx.EmptyIcon()
        icon.LoadFile(join(eg.imagesDir, "icon32x32.png"), wx.BITMAP_TYPE_PNG)
        iconBundle.AddIcon(icon)
        self.SetIcons(iconBundle)

        self.Bind(wx.EVT_ICONIZE, self.OnIconize)
        self.Bind(wx.EVT_MENU_OPEN, self.OnMenuOpen)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.mainSizeFlag = True
        self.ratioLock = False
        self.ratio = Config.ratio
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOVE, self.OnMove)
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(wx.aui.EVT_AUI_PANE_MAXIMIZE, self.OnPaneMaximize)
        self.Bind(wx.aui.EVT_AUI_PANE_RESTORE, self.OnPaneRestore)
        self.UpdateViewOptions()
        self.SetSize(Config.size)
        eg.Bind("DocumentFileChange", self.OnDocumentFileChange)
        eg.Bind("DocumentChange", self.OnDocumentChange)
        eg.Bind("DialogCreate", self.OnAddDialog)
        eg.Bind("DialogDestroy", self.OnRemoveDialog)
        eg.Bind("UndoChange", self.OnUndoChange)
        self.OnUndoChange(document.undoState)
        eg.Bind("SelectionChange", self.OnSelectionChange)
        if document.selection is not None:
            self.OnSelectionChange(document.selection)
        eg.Bind("FocusChange", self.OnFocusChange)
        self.OnFocusChange(self.treeCtrl)
        eg.Bind("ClipboardChange", self.OnClipboardChange)
        # tell FrameManager to manage this frame
        if (Config.perspective is not None):
            try:
                auiManager.LoadPerspective(Config.perspective, False)
            except:
                pass
        artProvider = auiManager.GetArtProvider()
        artProvider.SetMetric(wx.aui.AUI_DOCKART_PANE_BORDER_SIZE, 0)
        artProvider.SetMetric(
            wx.aui.AUI_DOCKART_GRADIENT_TYPE,
            wx.aui.AUI_GRADIENT_HORIZONTAL
        )
        artProvider.SetColour(
            wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR,
            eg.colour.inactiveCaption
        )
        artProvider.SetColour(
            wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR,
            eg.colour.inactiveCaptionGradient
        )
        artProvider.SetColour(
            wx.aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR,
            eg.colour.inactiveCaptionTextColour
        )
        auiManager.GetPane("tree").Caption(" " + Text.Tree.caption)
        self.toolBar.Show(Config.showToolbar)
        auiManager.Update()
        auiManager.GetPane("logger").MinSize((100, 100))\
            .Caption(" " + Text.Logger.caption)

        # create an accelerator for the "Log only assigned and activated
        # events" checkbox. An awful hack.
        @eg.LogIt
        def ToggleOnlyLogAssigned(dummyEvent):
            checkBox = self.statusBar.checkBox
            flag = not checkBox.GetValue()
            checkBox.SetValue(flag)
            eg.config.onlyLogAssigned = flag
            self.statusBar.SetCheckBoxColour(flag)

        toggleOnlyLogAssignedId = wx.NewId()
        wx.EVT_MENU(self, toggleOnlyLogAssignedId, ToggleOnlyLogAssigned)

        # find the accelerator key in the label of the checkbox
        labelText = eg.text.MainFrame.onlyLogAssigned
        result = re.search(r'&([a-z])', labelText, re.IGNORECASE)
        if result:
            hotKey = result.groups()[0].upper()
        else:
            hotKey = "L"

        # create an accelerator for the "Del" key. This way we can temporarily
        # disable it while editing a tree label.
        # (see TreeCtrl.py OnBeginLabelEdit and OnEndLabelEdit)

        def OnDelKey(dummyEvent):
            self.DispatchCommand('OnCmdDelete')
        delId = wx.NewId()
        wx.EVT_MENU(self, delId, OnDelKey)

        def OnEnterKey(dummyEvent):
            if self.lastFocus == self.treeCtrl.editControl:
                self.treeCtrl.EndEditLabel(self.treeCtrl.editLabelId, False)
        enterId = wx.NewId()
        wx.EVT_MENU(self, enterId, OnEnterKey)

        self.acceleratorTable = wx.AcceleratorTable(
            [
                (wx.ACCEL_NORMAL, wx.WXK_DELETE, delId),
                (wx.ACCEL_NORMAL, wx.WXK_RETURN, enterId),
                (wx.ACCEL_ALT, ord(hotKey), toggleOnlyLogAssignedId),
            ]
        )
        self.SetAcceleratorTable(self.acceleratorTable)
        self.logCtrl.Bind(wx.EVT_SIZE, self.OnLogCtrlSize)
        eg.EnsureVisible(self)

    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass

    def CreateLogCtrl(self):
        logCtrl = LogCtrl(self)
        logCtrl.Freeze()
        if not Config.logTime:
            logCtrl.SetTimeLogging(False)
        logCtrl.SetIndent(Config.indentLog)
        self.auiManager.AddPane(
            logCtrl,
            wx.aui.AuiPaneInfo().
            Name("logger").
            Left().
            MinSize((280, 300)).
            MaximizeButton(True).
            CloseButton(False).
            Caption(" " + Text.Logger.caption)
        )
        self.auiManager.Update()
        logCtrl.Thaw()
        return logCtrl

    def CreateMenuBar(self):
        """
        Creates the main menu bar and all its menus.
        """
        text = Text.Menu
        menuBar = wx.MenuBar()

        def Append(ident, hotkey="", kind=wx.ITEM_NORMAL, image=None):
            label = getattr(text, ident, ident)
            item = wx.MenuItem(menu, ID[ident], label + hotkey, "", kind)
            if image:
                item.SetBitmap(image)
            menu.AppendItem(item)
            func = getattr(self, "OnCmd" + ident)

            def FuncWrapper(dummyEvent):
                func()

            self.Bind(wx.EVT_MENU, FuncWrapper, item)
            return item

        # file menu
        menu = wx.Menu()
        menuBar.Append(menu, text.FileMenu)
        Append("New", "\tCtrl+N")
        Append("Open", "\tCtrl+O")
        Append("Save", "\tCtrl+S").Enable(False)
        Append("SaveAs", "\tShift+Ctrl+S")
        menu.AppendSeparator()
        Append("Options", "\tCtrl+P")
        menu.AppendSeparator()
        Append("Restart", "\tShift+Ctrl+~")
        Append("RestartAsAdmin")
        menu.AppendSeparator()
        Append("Exit")

        # edit menu
        menu = wx.Menu()
        menuBar.Append(menu, text.EditMenu)
        Append("Undo", "\tCtrl+Z")
        Append("Redo", "\tCtrl+Y")
        menu.AppendSeparator()
        Append("Cut", "\tCtrl+X")
        Append("Copy", "\tCtrl+C")
        Append("Python", "\tShift+Ctrl+C")
        Append("Paste", "\tCtrl+V")
        # notice that we add a ascii zero byte at the end of the hotkey.
        # this way we prevent the normal accelerator to happen. We will later
        # catch the key ourself.
        oldLogging = wx.Log.EnableLogging(False)  # suppress warning
        Append("Delete", "\tDel\x00")
        wx.Log.EnableLogging(oldLogging)
        menu.AppendSeparator()
        Append("Find", "\tCtrl+F")
        Append("FindNext", "\tF3")

        # view menu
        menu = wx.Menu()
        menuBar.Append(menu, text.ViewMenu)
        Append("HideShowToolbar", kind=wx.ITEM_CHECK).Check(Config.showToolbar)
        menu.AppendSeparator()
        Append("ExpandAll")
        Append("CollapseAll")
        menu.AppendSeparator()
        item = Append("ExpandOnEvents", kind=wx.ITEM_CHECK)
        item.Check(Config.expandOnEvents)
        menu.AppendSeparator()
        Append("LogMacros", kind=wx.ITEM_CHECK).Check(eg.config.logMacros)
        Append("LogActions", kind=wx.ITEM_CHECK).Check(eg.config.logActions)
        Append("LogDebug", kind=wx.ITEM_CHECK).Check(eg.config.logDebug)
        menu.AppendSeparator()
        Append("IndentLog", kind=wx.ITEM_CHECK).Check(Config.indentLog)
        Append("LogTime", kind=wx.ITEM_CHECK).Check(Config.logTime)
        menu.AppendSeparator()
        Append("ClearLog")

        # configuration menu
        menu = wx.Menu()
        menuBar.Append(menu, text.ConfigurationMenu)
        Append("AddPlugin", "\tShift+Ctrl+P", image=ADD_PLUGIN_ICON)
        Append("AddFolder", "\tShift+Ctrl+N", image=ADD_FOLDER_ICON)
        Append("AddMacro", "\tShift+Ctrl+M", image=ADD_MACRO_ICON)
        Append("AddEvent", "\tShift+Ctrl+E", image=ADD_EVENT_ICON)
        Append("AddAction", "\tShift+Ctrl+A", image=ADD_ACTION_ICON)
        menu.AppendSeparator()
        Append("Configure", "\tReturn")
        Append("Rename", "\tF2")
        Append("Execute", "\tF5")
        menu.AppendSeparator()
        Append("Disabled", "\tCtrl+D", kind=wx.ITEM_CHECK)

        # help menu
        menu = wx.Menu()
        menuBar.Append(menu, text.HelpMenu)
        Append("HelpContents", "\tF1")
        menu.AppendSeparator()
        Append("WebHomepage")
        Append("WebForum")
        Append("WebWiki")
        menu.AppendSeparator()
        Append("CheckUpdate")
        menu.AppendSeparator()
        Append("PythonShell", "\tShift+Ctrl+I")
        Append("WIT")
        menu.AppendSeparator()
        Append("About")

        self.SetMenuBar(menuBar)
        return menuBar

    def CreateToolBar(self):
        """
        Creates the toolbar of the frame.
        """
        toolBar = wx.ToolBar(self, style=wx.TB_FLAT)
        toolBar.SetToolBitmapSize((16, 16))
        text = Text.Menu

        def Append(ident, image):
            toolBar.AddSimpleTool(ID[ident], image, getattr(text, ident))

        Append("New", GetInternalBitmap("New"))
        Append("Open", GetInternalBitmap("Open"))
        Append("Save", GetInternalBitmap("Save"))
        toolBar.AddSeparator()
        Append("Cut", GetInternalBitmap("Cut"))
        Append("Copy", GetInternalBitmap("Copy"))
        Append("Python", GetInternalBitmap("Python"))
        Append("Paste", GetInternalBitmap("Paste"))
        toolBar.AddSeparator()
        Append("Undo", GetInternalBitmap("Undo"))
        Append("Redo", GetInternalBitmap("Redo"))
        toolBar.AddSeparator()
        Append("AddPlugin", ADD_PLUGIN_ICON)
        Append("AddFolder", ADD_FOLDER_ICON)
        Append("AddMacro", ADD_MACRO_ICON)
        Append("AddEvent", ADD_EVENT_ICON)
        Append("AddAction", ADD_ACTION_ICON)
        toolBar.AddSeparator()
        Append("Disabled", GetInternalBitmap("Disabled"))
        toolBar.AddSeparator()
        # the execute button must be added with unique id, because otherwise
        # the menu command OnCmdExecute will be used in conjunction to
        # our special mouse click handlers
        toolBar.AddSimpleTool(
            ID_TOOLBAR_EXECUTE,
            GetInternalBitmap("Execute"),
            getattr(text, "Execute")
        )

        toolBar.EnableTool(wx.ID_SAVE, self.document.isDirty)
        toolBar.Realize()
        self.SetToolBar(toolBar)

        toolBar.Bind(wx.EVT_LEFT_DOWN, self.OnToolBarLeftDown)
        toolBar.Bind(wx.EVT_LEFT_UP, self.OnToolBarLeftUp)
        return toolBar

    def CreateTreeCtrl(self):
        treeCtrl = TreeCtrl(self, document=self.document)
        self.auiManager.AddPane(
            treeCtrl,
            wx.aui.AuiPaneInfo().
            Name("tree").
            Center().
            MinSize((100, 100)).
            Floatable(True).
            Dockable(True).
            MaximizeButton(True).
            Caption(" " + Text.Tree.caption).
            CloseButton(False)
        )
        self.auiManager.Update()
        treeCtrl.SetFocus()
        return treeCtrl

    def CreateTreePopupMenu(self):
        """
        Creates the pop-up menu for the configuration tree.
        """
        menu = wx.Menu()
        text = Text.Menu

        def Append(ident, kind=wx.ITEM_NORMAL, image=wx.NullBitmap):
            item = wx.MenuItem(menu, ID[ident], getattr(text, ident), "", kind)
            item.SetBitmap(image)
            menu.AppendItem(item)
            return item

        Append("Undo")
        Append("Redo")
        menu.AppendSeparator()
        Append("Cut")
        Append("Copy")
        Append("Python")
        Append("Paste")
        Append("Delete")
        menu.AppendSeparator()
        Append("AddPlugin", image=ADD_PLUGIN_ICON)
        Append("AddFolder", image=ADD_FOLDER_ICON)
        Append("AddMacro", image=ADD_MACRO_ICON)
        Append("AddEvent", image=ADD_EVENT_ICON)
        Append("AddAction", image=ADD_ACTION_ICON)
        menu.AppendSeparator()
        Append("Configure")
        Append("Rename")
        Append("Execute")
        menu.AppendSeparator()
        Append("Disabled", kind=wx.ITEM_CHECK)
        return menu

    @eg.LogItWithReturn
    def Destroy(self):
        self.Hide()
        eg.log.SetCtrl(None)
        Config.perspective = self.auiManager.SavePerspective()
        eg.Unbind("DocumentFileChange", self.OnDocumentFileChange)
        eg.Unbind("DocumentChange", self.OnDocumentChange)
        eg.Unbind("FocusChange", self.OnFocusChange)
        eg.Unbind("ClipboardChange", self.OnClipboardChange)
        eg.Unbind("DialogCreate", self.OnAddDialog)
        eg.Unbind("DialogDestroy", self.OnRemoveDialog)
        eg.Unbind("SelectionChange", self.OnSelectionChange)
        eg.Unbind("UndoChange", self.OnUndoChange)
        self.logCtrl.Destroy()
        self.treeCtrl.Destroy()
        self.SetStatusBar(None)
        self.statusBar.Destroy()
        result = wx.Frame.Destroy(self)
        self.popupMenu.Destroy()
        return result

    @eg.LogIt
    def DispatchCommand(self, command):
        focus = self.FindFocus()
        if focus is self.treeCtrl:
            getattr(self.document, command[2:])()
        elif isinstance(focus, wx.TextCtrl):  # Added by Pako
            getattr(focus.GetParent().editControl, command)()
        else:
            getattr(focus, command)()

    def DisplayError(self, errorText):
        eg.MessageBox(
            errorText,
            style=wx.ICON_EXCLAMATION | wx.OK,
            parent=self
        )

    def GetEditCmdState(self):
        focus = self.lastFocus
        if focus == self.treeCtrl.editControl:
            return (
                focus.CanCut(),
                focus.CanCopy(),
                False,
                focus.CanPaste(),
                focus.CanDelete()
            )
        elif focus == self.logCtrl:
            return (False, True, False, False, False)
        elif focus == self.treeCtrl:
            return self.treeCtrl.GetEditCmdState()
        return (False, False, False, False, False)

    def GetPanelDirection(self, panel):
        info = self.auiManager.SavePaneInfo(panel)
        pos = info.find(";dir=") + 5
        return info[pos]

    def SetWindowStyleFlag(self, *args, **kwargs):
        """
        Changes the main frame style depending on the display of the tray icon.

        Sets the style flags for the minimize button. It will be grayed out if
        the tray icon is shown and there child dialogs open.
        If the tray icon is not shown the minimize button will function as
        usual.

        :param args: unused, kept for compatibility with
        wxFrame.SetWindowStyleFlag()
        :param kwargs: unused, kept for compatibility with
        wxFrame.SetWindowStyleFlag()
        :return: None
        """
        if eg.config.showTrayIcon:
            if len(self.openDialogs):
                style = ~(wx.MINIMIZE_BOX | wx.CLOSE_BOX) & self.style
            else:
                style = self.style
        else:
            style = self.style

        wx.Frame.SetWindowStyleFlag(self, style)

    @eg.LogIt
    def Iconize(self, flag=True):
        if flag and eg.config.showTrayIcon:
            self.document.HideFrame()
        else:
            wx.Frame.Iconize(self, flag)

            for dialog in self.openDialogs:
                dialog.Iconize(flag)

    def OnAddDialog(self, dialog):
        if dialog.GetParent() != self:
            return
        self.openDialogs.append(dialog)
        dialog.Bind(wx.EVT_WINDOW_DESTROY, self.OnDialogDestroy)
        self.SetWindowStyleFlag()

    @eg.LogIt
    def OnClipboardChange(self, dummyValue):
        if self.lastFocus == self.treeCtrl:
            canPaste = self.treeCtrl.GetSelectedNode().CanPaste()
            self.toolBar.EnableTool(wx.ID_PASTE, canPaste)

    @eg.LogIt
    def OnClose(self, dummyEvent):
        """
        Handle wx.EVT_CLOSE
        """
        if eg.config.hideOnClose:
            self.Iconize(True)
        elif len(self.openDialogs) == 0:
            eg.app.Exit()
        else:
            self.Iconize(False)
            self.RequestUserAttention()

    @eg.LogIt
    def OnDialogDestroy(self, event):
        dialog = event.GetWindow()
        try:
            self.openDialogs.remove(dialog)
        except ValueError:
            pass
        self.SetWindowStyleFlag()

    def OnDocumentChange(self, isDirty):
        wx.CallAfter(self.toolBar.EnableTool, wx.ID_SAVE, bool(isDirty))
        wx.CallAfter(self.menuBar.Enable, wx.ID_SAVE, bool(isDirty))

    def OnDocumentFileChange(self, filepath):
        self.SetTitle(self.document.GetTitle())

    def OnFocusChange(self, focus):
        if focus == self.lastFocus:
            return
        if focus == self.treeCtrl.editControl:
            # avoid programmatic change of the selected item while editing
            self.UpdateViewOptions()
            # temporarily disable the "Del" accelerator
            #self.SetAcceleratorTable(wx.AcceleratorTable([]))
        elif self.lastFocus == self.treeCtrl.editControl:
            # restore the "Del" accelerator
            #self.SetAcceleratorTable(self.acceleratorTable)
            self.UpdateViewOptions()

        self.lastFocus = focus
        toolBar = self.toolBar
        canCut, canCopy, canPython, canPaste = self.GetEditCmdState()[:4]
        toolBar.EnableTool(wx.ID_CUT, canCut)
        toolBar.EnableTool(wx.ID_COPY, canCopy)
        toolBar.EnableTool(ID_PYTHON, canPython)
        toolBar.EnableTool(wx.ID_PASTE, canPaste)

    @eg.LogIt
    def OnIconize(self, event):
        """
        Handle wx.EVT_ICONIZE
        """
        self.Iconize(event.Iconized())

    def OnLogCtrlSize(self, evt):
        if self.mainSizeFlag:
            wx.CallAfter(self.UpdateRatio)
        evt.Skip()

    def OnMenuOpen(self, dummyEvent):
        """
        Handle wx.EVT_MENU_OPEN
        """
        self.SetupEditMenu(self.menuBar)

    def OnMove(self, event):
        """
        Handle wx.EVT_MOVE
        """
        if not self.IsMaximized() and not self.IsIconized():
            Config.position = self.GetPositionTuple()
        event.Skip()

    def OnPaneClose(self, event):
        """
        React to a wx.aui.EVT_AUI_PANE_CLOSE event.

        Monitors if the toolbar gets closed and updates the check menu
        entry accordingly
        """
        paneName = event.GetPane().name
        if paneName == "toolBar":
            Config.showToolbar = False
            self.menuBar.Check(ID["HideShowToolbar"], False)

    def OnPaneMaximize(self, dummyEvent):
        """
        React to a wx.aui.EVT_AUI_PANE_MAXIMIZE event.
        """
        Config.perspective2 = self.auiManager.SavePerspective()

    def OnPaneRestore(self, dummyEvent):
        """
        React to a wx.aui.EVT_AUI_PANE_RESTORE event.
        """
        if Config.perspective2 is not None:
            self.auiManager.LoadPerspective(Config.perspective2)

    def OnRemoveDialog(self, dialog):
        try:
            self.openDialogs.remove(dialog)
        except ValueError:
            pass
        if len(self.openDialogs) == 0:
            self.SetWindowStyleFlag(self.style)

    def OnSelectionChange(self, dummySelection):
        canCut, canCopy, canPython, canPaste = self.GetEditCmdState()[:4]
        self.toolBar.EnableTool(wx.ID_CUT, canCut)
        self.toolBar.EnableTool(wx.ID_COPY, canCopy)
        self.toolBar.EnableTool(ID_PYTHON, canPython)
        self.toolBar.EnableTool(wx.ID_PASTE, canPaste)

    def OnSize(self, event):
        """
        Handle wx.EVT_SIZE
        """
        self.mainSizeFlag = False
        wx.CallAfter(self.UpdateSize)
        event.Skip()

    @eg.LogIt
    def OnToolBarLeftDown(self, event):
        """
        Handles the wx.EVT_LEFT_DOWN events for the toolbar.
        """
        x, y = event.GetPosition()
        item = self.toolBar.FindToolForPosition(x, y)
        if item and item.GetId() == ID_TOOLBAR_EXECUTE:
            node = self.treeCtrl.GetSelectedNode()
            if not node.isExecutable:
                self.DisplayError(Text.Messages.cantExecute)
            else:
                self.lastClickedTool = item
                self.egEvent = self.document.ExecuteNode(node)
        event.Skip()

    @eg.LogIt
    def OnToolBarLeftUp(self, event):
        """
        Handles the wx.EVT_LEFT_UP events for the toolbar.
        """
        if self.lastClickedTool:
            self.lastClickedTool = None
            self.egEvent.SetShouldEnd()
        event.Skip()

    def OnUndoChange(self, undoState):
        hasUndos, hasRedos, undoName, redoName = undoState
        undoName = Text.Menu.Undo + undoName
        redoName = Text.Menu.Redo + redoName

        self.menuBar.Enable(wx.ID_UNDO, hasUndos)
        self.menuBar.SetLabel(wx.ID_UNDO, undoName + "\tCtrl+Z")
        self.menuBar.Enable(wx.ID_REDO, hasRedos)
        self.menuBar.SetLabel(wx.ID_REDO, redoName + "\tCtrl+Y")

        self.popupMenu.Enable(wx.ID_UNDO, hasUndos)
        self.popupMenu.SetLabel(wx.ID_UNDO, undoName)
        self.popupMenu.Enable(wx.ID_REDO, hasRedos)
        self.popupMenu.SetLabel(wx.ID_REDO, redoName)

        self.toolBar.EnableTool(wx.ID_UNDO, hasUndos)
        self.toolBar.SetToolShortHelp(wx.ID_UNDO, undoName)
        self.toolBar.EnableTool(wx.ID_REDO, hasRedos)
        self.toolBar.SetToolShortHelp(wx.ID_REDO, redoName)

    def Raise(self):
        BringHwndToFront(self.GetHandle())
        wx.Frame.Raise(self)

    def SetupEditMenu(self, menu):
        canCut, canCopy, canPython, canPaste, canDelete = self.GetEditCmdState()
        menu.Enable(wx.ID_CUT, canCut)
        menu.Enable(wx.ID_COPY, canCopy)
        menu.Enable(ID_PYTHON, canPython)
        menu.Enable(wx.ID_PASTE, canPaste)
        menu.Enable(wx.ID_DELETE, canDelete)
        selection = self.treeCtrl.GetSelectedNode()
        menu.Check(ID_DISABLED, selection is not None and not selection.isEnabled)

    def UpdateRatio(self):
        self.logCtrl.SetColumnWidth(
            0,
            self.logCtrl.GetSizeTuple()[0] - self.corConst
        )
        if not eg.config.propResize:
            return
        panel = self.auiManager.GetPane("logger")
        if panel.IsDocked():
            if self.ratioLock:
                self.ratioLock = False
                self.UpdateSize()
                #self.UpdateSize(False)
            dir = self.GetPanelDirection(panel)
            coord = None
            if dir in ("2", "4"):
                coord = 0
            elif dir in ("1", "3"):
                coord = 1
            if coord is not None:
                l_val = self.logCtrl.GetSizeTuple()[coord]
                t_val = self.treeCtrl.GetSizeTuple()[coord]
                self.ratio = float(t_val) / float(l_val)
                Config.ratio = self.ratio
        else:
            self.ratioLock = True

    def UpdateSize(self):
        if eg.config.propResize:
            panel = self.auiManager.GetPane("logger")
            if panel.IsDocked():
                s = self.auiManager.SavePerspective()
                dir = self.GetPanelDirection(panel)
                coord = None
                if dir in ("2", "4"):
                    coord = 0
                elif dir in ("1", "3"):
                    coord = 1
                if coord is not None:
                    l_val = self.logCtrl.GetSizeTuple()[coord]
                    t_val = self.treeCtrl.GetSizeTuple()[coord]
                    c_val = self.GetClientSizeTuple()[coord]
                    k = c_val - l_val - t_val
                    l_val = int((c_val - k) / (1 + self.ratio))
                    #t_val = (c_val-k)-l_val
                    b1 = s.find("|dock_size(%s," % dir) + 1
                    b2 = s.find("=", b1) + 1
                    e = s.find("|", b1)
                    s = "%s%i%s" % (s[:b2], l_val, s[e:])
                    self.auiManager.LoadPerspective(s, True)
                    self.logCtrl.SetColumnWidth(
                        0,
                        self.logCtrl.GetSizeTuple()[0] - self.corConst
                    )
        self.mainSizeFlag = True
        if not self.IsMaximized() and not self.IsIconized():
            Config.size = self.GetSizeTuple()

    def UpdateViewOptions(self):
        expandOnEvents = (
            not self.IsIconized() and
            Config.expandOnEvents and
            (self.treeCtrl and self.treeCtrl.editLabelId is None)
        )
        self.document.ActionItem.shouldSelectOnExecute = expandOnEvents
        self.document.MacroItem.shouldSelectOnExecute = expandOnEvents

    #-------------------------------------------------------------------------
    #---- Menu Handlers ------------------------------------------------------
    #-------------------------------------------------------------------------

    #---- File ---------------------------------------------------------------
    def OnCmdNew(self):
        self.document.New()

    def OnCmdOpen(self):
        self.document.Open()

    def OnCmdSave(self):
        self.document.Save()

    def OnCmdSaveAs(self):
        self.document.SaveAs()

    @eg.AsTasklet
    def OnCmdOptions(self):
        eg.OptionsDialog.GetResult(self)

    def OnCmdRestart(self):
        eg.app.Restart()

    def OnCmdRestartAsAdmin(self):
        eg.app.RestartAsAdmin()

    def OnCmdExit(self):
        eg.app.Exit()

    #---- Edit ---------------------------------------------------------------
    def OnCmdUndo(self):
        self.document.Undo()

    def OnCmdRedo(self):
        self.document.Redo()

    def OnCmdCut(self):
        self.DispatchCommand("OnCmdCut")

    def OnCmdCopy(self):
        self.DispatchCommand("OnCmdCopy")

    def OnCmdPython(self):
        self.DispatchCommand("OnCmdPython")

    def OnCmdPaste(self):
        self.DispatchCommand("OnCmdPaste")

    def OnCmdDelete(self):
        self.DispatchCommand("OnCmdDelete")

    def OnCmdFind(self):
        if self.findDialog is None:
            self.findDialog = eg.FindDialog(self, self.document)
        self.findDialog.Show()

    def OnCmdFindNext(self):
        if (
            self.findDialog is None or
            not self.findDialog.searchButton.IsEnabled()
        ):
            self.OnCmdFind()
        else:
            self.findDialog.OnFindButton()

    #---- View ---------------------------------------------------------------
    def OnCmdHideShowToolbar(self):
        Config.showToolbar = not Config.showToolbar
        #self.auiManager.GetPane("toolBar").Show(Config.showToolbar)
        #self.auiManager.Update()
        self.toolBar.Show(Config.showToolbar)
        self.Layout()
        self.SendSizeEvent()

    def OnCmdExpandAll(self):
        self.treeCtrl.ExpandAll()

    def OnCmdCollapseAll(self):
        self.treeCtrl.CollapseAll()

    def OnCmdExpandOnEvents(self):
        Config.expandOnEvents = not Config.expandOnEvents
        self.menuBar.Check(ID["ExpandOnEvents"], Config.expandOnEvents)
        self.UpdateViewOptions()

    def OnCmdLogMacros(self):
        eg.config.logMacros = not eg.config.logMacros
        self.menuBar.Check(ID["LogMacros"], eg.config.logMacros)

    def OnCmdLogActions(self):
        eg.config.logActions = not eg.config.logActions
        self.menuBar.Check(ID["LogActions"], eg.config.logActions)

    def OnCmdLogDebug(self):
        eg.config.logDebug = not eg.config.logDebug
        self.menuBar.Check(ID["LogDebug"], eg.config.logDebug)
        eg.debugLevel = int(eg.config.logDebug)

    def OnCmdLogTime(self):
        flag = self.menuBar.IsChecked(ID["LogTime"])
        Config.logTime = flag
        self.logCtrl.SetTimeLogging(flag)

    def OnCmdIndentLog(self):
        shouldIndent = self.menuBar.IsChecked(ID["IndentLog"])
        Config.indentLog = shouldIndent
        self.logCtrl.SetIndent(shouldIndent)

    def OnCmdClearLog(self):
        self.logCtrl.OnCmdClearLog()

    #---- Configuration ------------------------------------------------------
    @eg.AsTasklet
    def OnCmdAddPlugin(self):
        self.document.CmdAddPlugin()

    def OnCmdAddFolder(self):
        self.document.CmdAddFolder()

    @eg.AsTasklet
    def OnCmdAddMacro(self):
        self.document.CmdAddMacro()

    @eg.AsTasklet
    def OnCmdAddEvent(self):
        self.document.CmdAddEvent()

    @eg.AsTasklet
    def OnCmdAddAction(self):
        self.document.CmdAddAction()

    @eg.AsTasklet
    def OnCmdConfigure(self):
        self.document.CmdConfigure()

    def OnCmdRename(self):
        self.document.CmdRename()

    def OnCmdExecute(self):
        self.document.CmdExecute()

    def OnCmdDisabled(self):
        self.document.CmdToggleEnable()

    #---- Help ---------------------------------------------------------------
    def OnCmdHelpContents(self):
        HtmlHelp(
            GetDesktopWindow(),
            join(eg.mainDir, "EventGhost.chm"),
            HH_DISPLAY_TOPIC,
            0
        )

    def OnCmdWebHomepage(self):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/", 2, 1)

    def OnCmdWebForum(self):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/forum/", 2, 1)

    def OnCmdWebWiki(self):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/mediawiki/", 2, 1)

    def OnCmdCheckUpdate(self):
        eg.CheckUpdate.CheckUpdateManually()

    def OnCmdWIT(self):
        if eg.wit:
            eg.wit.Show(refreshTree=True)
            return

        from wx.lib.inspection import InspectionTool
        eg.wit = InspectionTool()
        eg.wit.Show(refreshTree=True)

    def OnCmdPythonShell(self):
        if eg.pyCrustFrame:
            eg.pyCrustFrame.Raise()
            return

        import wx.py as py

        # The FillingTree of the pyCrustFrame has some bug, that will raise
        # a UnicodeError if some item has a non-ascii str-representation.
        # For example a module that resides in a non-ascii file-system path
        # will trigger that error.
        # Thus we monkey-path the responsible code here with a bug-fixed
        # version.
        from wx.py.filling import FillingTree

        def display(self):
            item = self.item
            if not item:
                return
            if self.IsExpanded(item):
                self.addChildren(item)
            self.setText('')
            obj = self.GetPyData(item)
            if wx.Platform == '__WXMSW__':
                if obj is None:  # Windows bug fix.
                    return
            self.SetItemHasChildren(item, self.objHasChildren(obj))
            otype = type(obj)
            text = u''
            text += self.getFullName(item)
            text += '\n\nType: ' + str(otype)
            try:
                # BUGFIX: Here is the problematic code. We replace str(obj)
                #         with unicode(obj) and everything seems to be fine.
                #value = str(obj)
                value = unicode(obj)
            except:
                value = ''
            if otype is types.StringType or otype is types.UnicodeType:  # NOQA
                value = repr(obj)
            text += '\n\nValue: ' + value
            if otype not in SIMPLETYPES:  # NOQA
                try:
                    text += '\n\nDocstring:\n\n"""' + \
                            inspect.getdoc(obj).strip() + '"""'
                except:
                    pass
            if otype is types.InstanceType:  # NOQA
                try:
                    text += '\n\nClass Definition:\n\n' + \
                            inspect.getsource(obj.__class__)
                except:
                    pass
            else:
                try:
                    text += '\n\nSource Code:\n\n' + \
                            inspect.getsource(obj)
                except:
                    pass
            self.setText(text)
        FillingTree.display.im_func.func_code = display.func_code

        fileName = join(eg.configDir, 'PyCrust')
        pyCrustConfig = wx.FileConfig(localFilename=fileName)
        pyCrustConfig.SetRecordDefaults(True)

        eg.pyCrustFrame = frame = py.crust.CrustFrame(
            rootObject=eg.globals.__dict__,
            #locals=eg.globals.__dict__,
            rootLabel="eg.globals",
            config=pyCrustConfig,
            dataDir=eg.configDir,
        )
        tree = frame.crust.filling.tree
        tree.Expand(tree.GetRootItem())

        @eg.LogIt
        def OnPyCrustClose(event):
            frame.OnClose(event)
            # I don't know if this is a bug of wxPython, but if we don't
            # delete the notebook explicitly, the program crashes on exit.
            frame.crust.notebook.Destroy()
            eg.pyCrustFrame = None
            #event.Skip()
        frame.Bind(wx.EVT_CLOSE, OnPyCrustClose)
        frame.Show()

    @eg.AsTasklet
    @eg.LogItWithReturn
    def OnCmdAbout(self):
        eg.AboutDialog.GetResult(self)
