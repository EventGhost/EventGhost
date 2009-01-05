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

import eg
import wx
import os
import re
from collections import defaultdict

import wx.aui

from eg import (
    EventItem, 
    ActionItem, 
    MacroItem, 
    FolderItem, 
    RootItem, 
)
from eg.WinApi.Utils import BringHwndToFront
from eg.Icons import CreateBitmapOnTopOfIcon

# local imports
from LogCtrl import LogCtrl
from TreeCtrl import TreeCtrl
from StatusBar import StatusBar


ADD_ICON = eg.Icons.PathIcon('images/add.png')
ADD_PLUGIN_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.PLUGIN_ICON)
ADD_FOLDER_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.FOLDER_ICON)
ADD_MACRO_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.MACRO_ICON)
ADD_EVENT_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.EVENT_ICON)
ADD_ACTION_ICON = CreateBitmapOnTopOfIcon(ADD_ICON, eg.Icons.ACTION_ICON)
RESET_ICON = eg.Icons.PathIcon('images/error.png').GetBitmap()

ID_DISABLED = wx.NewId()
ID_EXECUTE = wx.NewId()
ID_TOOLBAR_EXECUTE = wx.NewId()

ID = defaultdict(wx.NewId, {
    "Save": wx.ID_SAVE,
    "Undo": wx.ID_UNDO,
    "Redo": wx.ID_REDO,
    "Cut": wx.ID_CUT,
    "Copy": wx.ID_COPY,
    "Paste": wx.ID_PASTE,
    "Delete": wx.ID_DELETE,
    "Disabled": ID_DISABLED,
    "Execute": ID_EXECUTE,
})

Text = eg.text.MainFrame

        
class DefaultConfig:
    position = (50, 50)
    size = (700, 433)
    showToolbar = True
    hideOnClose = False
    logTime = False
    indentLog = True
    expandOnEvents = False
    expandTillMacro = False
    perspective = None
    perspective2 = None

config = eg.GetConfig("mainFrame", DefaultConfig)


def GetIcon(name):
    return eg.Icons.GetIcon("images\\" + name + ".png")


class MainFrame(wx.Frame):
    """ This is the MainFrame of EventGhost """
        
    aboutDialog = None
    
    @eg.AssertNotMainThread
    def __init__(self, document):
        """ Create the MainFrame """
        self.document = document
        self.aboutDialog = None
        self.optionsDialog = None
        self.iconState = 0
        self.findDialog = None
        self.openDialogs = []
        self.lastClickedTool = None
        self.egEvent = None
        self.style = (
            wx.MINIMIZE_BOX
            |wx.MAXIMIZE_BOX
            |wx.RESIZE_BORDER
            |wx.SYSTEM_MENU
            |wx.CAPTION
            |wx.CLOSE_BOX
            |wx.CLIP_CHILDREN
            |wx.TAB_TRAVERSAL
        )
        wx.Frame.__init__(
            self, 
            None, 
            -1, 
            eg.APP_NAME, 
            pos=config.position, 
            size=(1, 1), 
            style=self.style
        )
        self.SetMinSize((400, 200))
        document.frame = self
        auiManager = wx.aui.AuiManager()
        auiManager.SetManagedWindow(self)
        self.auiManager = auiManager
        
        self.logCtrl = self.CreateLogCtrl()
        self.treeCtrl = self.CreateTreeCtrl()
        self.toolBar = self.CreateToolBar()
        self.menuBar = self.CreateMenuBar()
        self.statusBar = StatusBar(self)
        self.SetStatusBar(self.statusBar)

        # tree popup menu
        self.popupMenu = self.CreateTreePopupMenu()

        value = document.isDirty.Subscribe(self.OnDocumentDirty)
        self.toolBar.EnableTool(wx.ID_SAVE, value)
        #self.menuBar.File.save.Enable(value)
        
        iconBundle = wx.IconBundle()
        iconBundle.AddIcon(eg.taskBarIcon.stateIcons[0])
        icon = wx.EmptyIcon()
        icon.LoadFile("images/icon32x32.png", wx.BITMAP_TYPE_PNG)
        iconBundle.AddIcon(icon)
        self.SetIcons(iconBundle)
        
        self.lastFocus = "None"
                
        self.Bind(wx.EVT_ICONIZE, self.OnIconize)
        self.Bind(wx.EVT_MENU_OPEN, self.OnMenuOpen)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOVE, self.OnMove)
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(wx.aui.EVT_AUI_PANE_MAXIMIZE, self.OnPaneMaximize)
        self.Bind(wx.aui.EVT_AUI_PANE_RESTORE, self.OnPaneRestore)
        self.UpdateViewOptions()
        self.SetSize(config.size)
        undoState = document.undoEvent.Subscribe(self.OnUndoEvent)
        self.OnUndoEvent(undoState)
        selection = document.selectionEvent.Subscribe(
            self.OnTreeSelectionEvent
        )
        if selection is not None:
            self.OnTreeSelectionEvent(selection)
        # tell FrameManager to manage this frame

        if (
            eg.config.buildNum == eg.buildNum 
            and config.perspective is not None
        ):
            auiManager.LoadPerspective(config.perspective, False)
        auiManager.GetArtProvider().SetMetric(
            wx.aui.AUI_DOCKART_PANE_BORDER_SIZE, 0
        )
        auiManager.GetPane("tree").Caption(" " + Text.Tree.caption)
        self.toolBar.Show(config.showToolbar)
        auiManager.Update()
        auiManager.GetPane("logger").MinSize((100, 100))\
            .Caption(" " + Text.Logger.caption)
        value = eg.focusChangeEvent.Subscribe(self.OnFocusChange)
        self.OnFocusChange(value)
        
        eg.clipboardEvent.Subscribe(self.OnClipboardChange)
        self.UpdateTitle(self.document.filePath)
        
        # create an accelerator for the "Log only assigned and activated 
        # events" checkbox. An awfull hack.
        @eg.LogIt
        def ToggleOnlyLogAssigned(dummyEvent):
            checkBox = self.statusBar.checkBox
            flag = not checkBox.GetValue()
            checkBox.SetValue(flag)
            eg.config.onlyLogAssigned = flag

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
            self.DispatchCommand('Clear')
        delId = wx.NewId()
        wx.EVT_MENU(self, delId, OnDelKey)
        
        def OnEnterKey(dummyEvent):
            if self.lastFocus == "Edit":
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
        eg.EnsureVisible(self)
        
    
    @eg.LogItWithReturn
    def Destroy(self):
        self.document.SetTree(None)
        eg.log.SetCtrl(None)
        config.perspective = self.auiManager.SavePerspective()
        self.SetStatusBar(None)
        self.document.isDirty.UnSubscribe(self.OnDocumentDirty)
        eg.focusChangeEvent.UnSubscribe(self.OnFocusChange)
        eg.clipboardEvent.UnSubscribe(self.OnClipboardChange)
        self.document.undoEvent.UnSubscribe(self.OnUndoEvent)
        self.document.selectionEvent.UnSubscribe(self.OnTreeSelectionEvent)
        self.logCtrl.Destroy()
        self.treeCtrl.Destroy()
        result = wx.Frame.Destroy(self)
        eg.Icons.ClearImageList()
        return result
    
    
    def CreateToolBar(self):
        """
        Creates the toolbar of the frame.
        """
        toolBar = wx.ToolBar(self, style=wx.TB_FLAT)
        toolBar.SetToolBitmapSize((16, 16))
        text = Text.Menu
        
        def Append(ident, image):
            toolBar.AddSimpleTool(ID[ident], image, getattr(text, ident))
            
        Append("New", GetIcon("New"))
        Append("Open", GetIcon("Open"))
        Append("Save", GetIcon("Save"))
        toolBar.AddSeparator()
        Append("Cut", GetIcon("Cut"))
        Append("Copy", GetIcon("Copy"))
        Append("Paste", GetIcon("Paste"))
        toolBar.AddSeparator()
        Append("Undo", GetIcon("Undo"))
        Append("Redo", GetIcon("Redo"))
        toolBar.AddSeparator()
        Append("AddPlugin", ADD_PLUGIN_ICON)
        Append("AddFolder", ADD_FOLDER_ICON)
        Append("AddMacro", ADD_MACRO_ICON)
        Append("AddEvent", ADD_EVENT_ICON)
        Append("AddAction", ADD_ACTION_ICON)
        toolBar.AddSeparator()
        Append("Disabled", GetIcon("Disabled"))
        toolBar.AddSeparator()
        # the execute button must be added with unique id, because otherwise
        # the menu command OnCmdExecute will be used in conjunction to 
        # our special mouse click handlers
        toolBar.AddSimpleTool(
            ID_TOOLBAR_EXECUTE, 
            GetIcon("Execute"), 
            getattr(text, "Execute")
        )
        if eg.debugLevel:
            Append("Reset", GetIcon("error"))
        
        toolBar.Realize()
        self.SetToolBar(toolBar)

        toolBar.Bind(wx.EVT_LEFT_DOWN, self.OnToolBarLeftDown)
        toolBar.Bind(wx.EVT_LEFT_UP, self.OnToolBarLeftUp)
        return toolBar
    
                    
    @eg.LogIt
    def OnToolBarLeftDown(self, event):
        """
        Handles the wx.EVT_LEFT_DOWN events for the toolbar.
        """
        x, y = event.GetPosition()
        item = self.toolBar.FindToolForPosition(x, y)
        if item and item.GetId() == ID_TOOLBAR_EXECUTE:
            self.lastClickedTool = item
            self.egEvent = self.document.ExecuteSelected()
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
        Append("SaveAs")
        menu.AppendSeparator()
        Append("Options")
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
        Append("Paste", "\tCtrl+V")
        # notice that we add a ascii zero byte at the end of the hotkey.
        # this way we prevent the normal accelerator to happen. We will later
        # catch the key ourself.
        oldLogging = wx.Log.EnableLogging(False) # suppress warning
        Append("Delete", "\tDel\x00")
        wx.Log.EnableLogging(oldLogging)
        menu.AppendSeparator()
        Append("Find", "\tCtrl+F")
        Append("FindNext", "\tF3")

        # view menu        
        menu = wx.Menu()
        menuBar.Append(menu, text.ViewMenu)
        Append("HideShowToolbar", kind=wx.ITEM_CHECK).Check(config.showToolbar)
        menu.AppendSeparator()
        Append("ExpandAll")
        Append("CollapseAll")
        menu.AppendSeparator()
        item = Append("ExpandOnEvents", kind=wx.ITEM_CHECK)
        item.Check(config.expandOnEvents)
        item = Append("ExpandTillMacro", kind=wx.ITEM_CHECK)
        item.Check(config.expandTillMacro)
        item.Enable(config.expandOnEvents)
        menu.AppendSeparator()
        Append("LogMacros", kind=wx.ITEM_CHECK).Check(eg.config.logMacros)
        Append("LogActions", kind=wx.ITEM_CHECK).Check(eg.config.logActions)
        Append("LogTime", kind=wx.ITEM_CHECK).Check(config.logTime)
        Append("IndentLog", kind=wx.ITEM_CHECK).Check(config.indentLog)
        menu.AppendSeparator()
        Append("ClearLog")
                
        # configuration menu
        menu = wx.Menu()
        menuBar.Append(menu, text.ConfigurationMenu)
        Append("AddPlugin", image=ADD_PLUGIN_ICON)
        Append("AddFolder", image=ADD_FOLDER_ICON)
        Append("AddMacro", image=ADD_MACRO_ICON)
        Append("AddEvent", image=ADD_EVENT_ICON)
        Append("AddAction", image=ADD_ACTION_ICON)
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
        Append("PythonShell")
        menu.AppendSeparator()
        Append("About")
        if eg.debugLevel:
            menu = wx.Menu()
            menuBar.Append(menu, "Debug")
            Append("Export")
            Append("Import")
            menu.AppendSeparator()
            Append("Reload")
            Append("GetInfo")
            Append("CollectGarbage")
            Append("Reset", "\tPause")
            Append("AddEventDialog")
            
        self.SetMenuBar(menuBar)
        return menuBar
        
        
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
    
        
    def CreateTreeCtrl(self):
        treeCtrl = TreeCtrl(self, document=self.document)
        self.document.SetTree(treeCtrl)
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
        
    
    def CreateLogCtrl(self):
        logCtrl = LogCtrl(self)
        logCtrl.Freeze()
        if not config.logTime:
            logCtrl.SetTimeLogging(False)
        logCtrl.SetIndent(config.indentLog)
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
        
    
    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
        
        
    def Raise(self):
        BringHwndToFront(self.GetHandle())
        wx.Frame.Raise(self)
    
    
    def UpdateTitle(self, filePath):
        if filePath is None:
            filename = eg.text.General.unnamedFile
        else:
            filename = os.path.basename(filePath)
        self.SetTitle("EventGhost %s - %s" % (eg.Version.string, filename))

    
    def OnDocumentDirty(self, isDirty):
        self.toolBar.EnableTool(wx.ID_SAVE, bool(isDirty))
        self.menuBar.Enable(wx.ID_SAVE, bool(isDirty))
        
        
    def OnPaneClose(self, event):
        """ 
        React to a wx.aui.EVT_AUI_PANE_CLOSE event.
        
        Monitors if the toolbar gets closed and updates the check menu
        entry accordingly
        """
        paneName = event.GetPane().name
        if paneName == "toolBar":
            config.showToolbar = False
            self.menuBar.Check(ID["HideShowToolbar"], False)
            
        
    def OnPaneMaximize(self, dummyEvent):
        """ React to a wx.aui.EVT_AUI_PANE_MAXIMIZE event. """
        config.perspective2 = self.auiManager.SavePerspective()
        
        
    def OnPaneRestore(self, dummyEvent):
        """ React to a wx.aui.EVT_AUI_PANE_RESTORE event. """
        if config.perspective2 is not None:
            self.auiManager.LoadPerspective(config.perspective2)
        
        
    def OnSize(self, event):
        """ Handle wx.EVT_SIZE """
        if not self.IsMaximized() and not self.IsIconized():
            config.size = self.GetSizeTuple()
        event.Skip()


    def OnMove(self, event):
        """ Handle wx.EVT_MOVE """
        if not self.IsMaximized() and not self.IsIconized():
            config.position = self.GetPositionTuple()
        event.Skip()
        
        
    @eg.LogIt
    def OnClose(self, dummyEvent):
        """ Handle wx.EVT_CLOSE """
        if len(self.openDialogs) == 0:
            if config.hideOnClose:
                self.document.HideFrame()
            else:
                eg.app.Exit()
        else:
            self.RequestUserAttention()


    @eg.LogIt
    def OnIconize(self, dummyEvent):
        """ Handle wx.EVT_ICONIZE """
        # On iconizing, we actually destroy the frame completely
        self.document.HideFrame()


    def OnMenuOpen(self, dummyEvent):
        """ Handle wx.EVT_MENU_OPEN """
        self.SetupEditMenu(self.menuBar)            
            
            
    @eg.LogIt
    def OnClipboardChange(self, dummyValue):
        if self.lastFocus == self.treeCtrl:
            canPaste = self.document.selection.CanPaste()
            self.toolBar.EnableTool(wx.ID_PASTE, canPaste)
    
    
    def OnFocusChange(self, focus):
        if focus == self.lastFocus:
            return
        if focus == "Edit":
            # avoid programmatic change of the selected item while editing
            self.UpdateViewOptions()
            # temporarily disable the "Del" accelerator
            #self.SetAcceleratorTable(wx.AcceleratorTable([]))
        elif self.lastFocus == "Edit":
            # restore the "Del" accelerator
            #self.SetAcceleratorTable(self.acceleratorTable)
            self.UpdateViewOptions()
            
        self.lastFocus = focus
        toolBar = self.toolBar
        canCut, canCopy, canPaste = self.GetEditCmdState()[:3]
        toolBar.EnableTool(wx.ID_CUT, canCut)
        toolBar.EnableTool(wx.ID_COPY, canCopy)
        toolBar.EnableTool(wx.ID_PASTE, canPaste)
        
        
    def AddDialog(self, dialog):
        self.openDialogs.append(dialog)
        dialog.Bind(wx.EVT_WINDOW_DESTROY, self.OnDialogDestroy)
        self.SetWindowStyleFlag(~(wx.MINIMIZE_BOX|wx.CLOSE_BOX) & self.style)
        
        
    @eg.LogIt
    def OnDialogDestroy(self, event):
        dialog = event.GetWindow()
        try:
            self.openDialogs.remove(dialog)
        except ValueError:
            pass
        if len(self.openDialogs) == 0:
            self.SetWindowStyleFlag(self.style)
    

    def DisplayError(self, message, caption="EventGhost Error"):
        eg.MessageBox(message, caption, wx.ICON_EXCLAMATION|wx.OK, self)


    def GetEditCmdState(self):
        focus = self.lastFocus
        if focus == "Edit":
            editCtrl = self.treeCtrl.GetEditControl()
            start, end = editCtrl.GetSelection()
            return (
                editCtrl.CanCut(), 
                editCtrl.CanCopy(), 
                editCtrl.CanPaste(), 
                (start != end)
            )
        elif focus == self.logCtrl:
            return (False, True, False, False)
        elif focus == self.treeCtrl and self.document.selection:
            selection = self.document.selection
            return (
                selection.CanCut(), 
                selection.CanCopy(), 
                selection.CanPaste(), 
                selection.CanDelete(), 
            )
        else:
            return (False, False, False, False)
        
    
    def OnTreeSelectionEvent(self, dummySelection):
        canCut, canCopy, canPaste = self.GetEditCmdState()[:3]
        self.toolBar.EnableTool(wx.ID_CUT, canCut)
        self.toolBar.EnableTool(wx.ID_COPY, canCopy)
        self.toolBar.EnableTool(wx.ID_PASTE, canPaste)
        
    
    def OnUndoEvent(self, undoState):
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
        
        
    def SetupEditMenu(self, menu):
        canCut, canCopy, canPaste, canDelete = self.GetEditCmdState()
        menu.Enable(wx.ID_CUT, canCut)
        menu.Enable(wx.ID_COPY, canCopy)
        menu.Enable(wx.ID_PASTE, canPaste)
        menu.Enable(wx.ID_DELETE, canDelete)
        selection = self.document.selection
        menu.Check(ID_DISABLED, selection and not selection.isEnabled)
        
        
    def UpdateViewOptions(self):
        expandOnEvents = (
            not self.IsIconized()
            and config.expandOnEvents 
            and (self.treeCtrl and self.treeCtrl.editLabelId is None)
        )
        ActionItem.shouldSelectOnExecute = (
            expandOnEvents and not config.expandTillMacro
        )
        MacroItem.shouldSelectOnExecute = expandOnEvents
        
        
    @eg.LogIt
    def DispatchCommand(self, command):
        if self.lastFocus == "Edit" and command == "Clear":
            editCtrl = self.treeCtrl.GetEditControl()
            start, end = editCtrl.GetSelection()
            if end - start == 0:
                end += 1
            editCtrl.Remove(start, end)
            return
        focus = self.FindFocus()
        getattr(focus, command)()
        
    #-------------------------------------------------------------------------
    #---- Menu Handlers ------------------------------------------------------
    #-------------------------------------------------------------------------
    
    def OnCmdNew(self):
        self.document.New()


    def OnCmdOpen(self):
        self.document.Open()
        
        
    def OnCmdSave(self):
        self.document.Save()


    def OnCmdSaveAs(self):
        self.document.SaveAs()


    @eg.AsGreenlet
    def OnCmdOptions(self):
        if not self.optionsDialog:
            self.optionsDialog = eg.OptionsDialog.Create(self)
            while self.optionsDialog.GetResult() is not None:
                pass
        else:
            self.optionsDialog.Raise()
            
        
    def OnCmdExit(self):
        eg.app.Exit()
        
        
    def OnCmdUndo(self):
        self.document.Undo()
            
            
    def OnCmdRedo(self):
        self.document.Redo()
        
    
    def OnCmdCut(self):
        self.DispatchCommand("Cut")
        
        
    def OnCmdCopy(self):
        self.DispatchCommand("Copy")
            
            
    def OnCmdPaste(self):
        self.DispatchCommand("Paste")
    
    
    def OnCmdDelete(self):
        self.DispatchCommand("Clear")
                
                
    def OnCmdFind(self):
        if self.findDialog is None:
            self.findDialog = eg.FindDialog(self, self.document)
        self.findDialog.Show()
        
        
    def OnCmdFindNext(self):
        if (
            self.findDialog is None 
            or not self.findDialog.searchButton.IsEnabled()
        ):
            self.OnCmdFind()
        else:
            self.findDialog.OnFindButton()
        

    def OnCmdAddPlugin(self):
        result = eg.AddPluginDialog.GetModalResult(self)
        if result is None:
            return
        pluginInfo = result[0][0]
        if pluginInfo is None:
            return
        eg.Greenlet(
            eg.UndoHandler.NewPlugin().Do
        ).switch(self.document, pluginInfo)
            
            
    def OnCmdAddEvent(self):
        if self.document.selection.DropTest(EventItem):
            eg.UndoHandler.NewEvent().Do(self.document)
        else:
            text = Text.ErrorMessages.CantAddEvent
            self.DisplayError(text.mesg, text.caption)
                
                
    def OnCmdAddFolder(self):
        eg.UndoHandler.NewFolder().Do(self.document)
        
    
    def OnCmdAddMacro(self):
        eg.UndoHandler.NewMacro().Do(self.document)
        
    
    def OnCmdAddAction(self):
        if not self.document.selection.DropTest(ActionItem):
            text = Text.ErrorMessages.CantAddAction
            self.DisplayError(
                text.mesg,
                text.caption,
            )
            return
        # let the user choose an action
        result = eg.AddActionDialog.GetModalResult(self)
        # if user canceled the dialog, take a quick exit
        if result is None:
            return None
        action = result[0][0]
        eg.Greenlet(
            eg.UndoHandler.NewAction().Do
        ).switch(self.document, action)
        
    
    @eg.LogIt
    def OnCmdRename(self):
        self.treeCtrl.SetFocus()
        self.treeCtrl.EditLabel(self.treeCtrl.GetSelection())


    def OnCmdConfigure(self):
        eg.UndoHandler.Configure().Try(self.document)


    def OnCmdExecute(self):
        self.document.ExecuteSelected().SetShouldEnd()


    def OnCmdDisabled(self):
        eg.UndoHandler.ToggleEnable(self.document)


    def OnCmdHideShowToolbar(self):
        config.showToolbar = not config.showToolbar
        #self.auiManager.GetPane("toolBar").Show(config.showToolbar)
        #self.auiManager.Update()
        self.toolBar.Show(config.showToolbar)
        self.Layout()
        self.SendSizeEvent()


    def OnCmdLogMacros(self):
        eg.config.logMacros = not eg.config.logMacros
        self.menuBar.Check(ID["LogMacros"], eg.config.logMacros)
        
        
    def OnCmdLogActions(self):
        eg.config.logActions = not eg.config.logActions
        self.menuBar.Check(ID["LogActions"], eg.config.logActions)
        
        
    def OnCmdExpandOnEvents(self):
        config.expandOnEvents = not config.expandOnEvents
        self.menuBar.Check(ID["ExpandOnEvents"], config.expandOnEvents)
        self.menuBar.Enable(ID["ExpandTillMacro"], config.expandOnEvents)
        self.UpdateViewOptions()
        
        
    def OnCmdExpandTillMacro(self):
        config.expandTillMacro = not config.expandTillMacro
        self.menuBar.Check(ID["ExpandTillMacro"], config.expandTillMacro)
        self.UpdateViewOptions()
        
        
    def OnCmdLogTime(self):
        flag = self.menuBar.IsChecked(ID["LogTime"])
        config.logTime = flag
        self.logCtrl.SetTimeLogging(flag)
    
    
    def OnCmdIndentLog(self):
        shouldIndent = self.menuBar.IsChecked(ID["IndentLog"])
        config.indentLog = shouldIndent
        self.logCtrl.SetIndent(shouldIndent)
        
        
    def OnCmdExpandAll(self):
        self.treeCtrl.OnCmdExpandAll()
    
    
    def OnCmdCollapseAll(self):
        self.treeCtrl.OnCmdCollapseAll()
    
    
    def OnCmdClearLog(self):
        self.logCtrl.OnCmdClearLog()
        
    
    def OnCmdHelpContents(self):
        from eg.WinApi.Dynamic import (
            HtmlHelp, 
            HH_DISPLAY_TOPIC, 
            GetDesktopWindow
        )
        HtmlHelp(GetDesktopWindow(), "EventGhost.chm", HH_DISPLAY_TOPIC, 0)
        
        
    def OnCmdWebHomepage(self):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/", 2, 1)
    
    
    def OnCmdWebForum(self):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/forum/", 2, 1)
    
    
    def OnCmdWebWiki(self):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/wiki/", 2, 1)
    
    
    def OnCmdCheckUpdate(self):
        eg.CheckUpdate.CheckUpdateManually()
    
    
    def OnCmdPythonShell(self):
        if eg.pyCrustFrame:
            eg.pyCrustFrame.Raise()
            return
        
        import wx.py as py

        fileName = os.path.join(eg.configDir, 'PyCrust')
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
        
        
    @eg.AsGreenlet
    def OnCmdAbout(self):
        if self.aboutDialog is None:
            self.aboutDialog = eg.AboutDialog.Create(self)
            self.aboutDialog.GetResult()
            self.aboutDialog = None
        else:
            self.aboutDialog.Raise()

    
        
    #----- debugging and experimental stuff that will be removed someday -----
    
    def OnCmdExport(self):
        result = eg.ExportDialog.GetModalResult()
        if result is not None:
            for item in result[0][0]:
                print item.GetLabel()


    def OnCmdImport(self):
        pass
    
    
    def OnCmdReload(self):
        if self.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            return wx.ID_CANCEL
        self.document.StartSession(self.document.filePath)
    
    
    def OnCmdGetInfo(self):
        self.document.selection.ShowInfo()

        
    def OnCmdCollectGarbage(self):
        import gc
        gc.set_debug(gc.DEBUG_SAVEALL)
    
        from pprint import pprint
        print "unreachable object count:", gc.collect()
        garbageList = gc.garbage[:]
        for i, obj in enumerate(garbageList):
            print "Object Num %d:" % i
            pprint(obj)
            print "Referrers:"
            #print(gc.get_referrers(o))
            print "Referents:"
            #print(gc.get_referents(o))
        print "Done."
        #print "unreachable object count:", gc.collect()
        #from pprint import pprint
        #pprint(gc.garbage)
        
        
    def OnCmdReset(self):
        eg.stopExecutionFlag = True
        eg.programCounter = None
        del eg.programReturnStack[:]
        eg.eventThread.ClearPendingEvents()
        eg.actionThread.ClearPendingEvents()
        eg.PrintError("Execution stopped by user")
        
    
    #@eg.AsGreenlet
    def OnCmdAddEventDialog(self):
        result = eg.AddEventDialog.GetModalResult(self)
        if result is None:
            return
        label = result[0][0]
        eg.UndoHandler.NewEvent().Do(self.document, label)

