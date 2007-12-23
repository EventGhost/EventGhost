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

import os
import sys
import gc
import re

import wx.aui

from eg import (
    EventItem, 
    ActionItem, 
    MacroItem, 
    FolderItem, 
    RootItem, 
)
import UndoableTasks

# local imports
from LogCtrl import LogCtrl
from TreeCtrl import TreeCtrl
from StatusBar import StatusBar

from eg.WinAPI.Utils import BringHwndToFront
ADD_ICON = eg.Icons.PathIcon('images/add.png')

PLUGIN_ICON = eg.Icons.PilToBitmap(
    eg.Icons.GetIconOnTop(ADD_ICON, eg.Icons.PLUGIN_ICON)
)
FOLDER_ICON = eg.Icons.PilToBitmap(
    eg.Icons.GetIconOnTop(ADD_ICON, eg.Icons.FOLDER_ICON)
)
MACRO_ICON = eg.Icons.PilToBitmap(
    eg.Icons.GetIconOnTop(ADD_ICON, eg.Icons.MACRO_ICON)
)
EVENT_ICON = eg.Icons.PilToBitmap(
    eg.Icons.GetIconOnTop(ADD_ICON, eg.Icons.EVENT_ICON)
)
ACTION_ICON = eg.Icons.PilToBitmap(
    eg.Icons.GetIconOnTop(ADD_ICON, eg.Icons.ACTION_ICON)
)
#FOLDER_ICON = eg.Icons.FOLDER_ICON.GetBitmap()
#MACRO_ICON = eg.Icons.MACRO_ICON.GetBitmap()
#EVENT_ICON = eg.Icons.EVENT_ICON.GetBitmap()
#ACTION_ICON = eg.Icons.ACTION_ICON.GetBitmap()
RESET_ICON = eg.Icons.PathIcon('images/error.png').GetBitmap()

Text = eg.text.MainFrame


        
class DefaultConfig:
    position = (50, 50)
    size = (700, 433)
    showToolbar = True
    hideOnClose = False
    logTime = False
    expandOnEvents = True
    expandTillMacro = False
    perspective = None
    perspective2 = None

config = eg.GetConfig("mainFrame", DefaultConfig)



class MainFrame(wx.Frame):
    """ This is the MainFrame of EventGhost """
        
    aboutDialog = None
    
    @eg.AssertNotMainThread
    def __init__(self, document):
        """ Create the MainFrame """
        text = eg.text
        self.document = document
        self.menuState = menuState = eg.Bunch()
        menuState.newEvent = False
        menuState.newAction = False
        menuState.edit = False
        menuState.execute = False
        menuState.rename = False
        menuState.disable = False

        wx.Frame.__init__(
            self, 
            None, 
            -1, 
            eg.APP_NAME, 
            pos=config.position, 
            size=(1, 1), 
            style=wx.MINIMIZE_BOX
                |wx.MAXIMIZE_BOX
                |wx.RESIZE_BORDER
                |wx.SYSTEM_MENU
                |wx.CAPTION
                |wx.CLOSE_BOX
                |wx.CLIP_CHILDREN
                |wx.TAB_TRAVERSAL
        )
        document.frame = self
        auiManager = wx.aui.AuiManager()
        auiManager.SetManagedWindow(self)
        self.auiManager = auiManager
        
        self.treeCtrl = None
        self.logCtrl = None
        self.CreateLogCtrl()
        self.CreateTreeCtrl()
        
        self.iconState = 0
        self.findDialog = None
        
        
        self.observer = []
        def DocumentBind(item, dataset):
            item.Enable(dataset.get())
            dataset.addCallback(item.Enable)
            self.observer.append((dataset, item.Enable))
        
        # toolBar
        toolBar = eg.ToolBar(self, style=wx.TB_FLAT)
        self.toolBar = toolBar
        toolBar.SetParams(self, Text.Menu)
        toolBar.SetToolBitmapSize((16, 16))
        AddItem = toolBar.AddButton
        AddItem("New")
        AddItem("Open")
        DocumentBind(AddItem("Save"), document.isDirty)
        AddItem()
        AddItem("Cut")
        AddItem("Copy")
        AddItem("Paste")
        AddItem()
        AddItem("Undo")
        AddItem("Redo")
        AddItem()
        AddItem("AddPlugin", image=PLUGIN_ICON)
        AddItem("NewFolder", image=FOLDER_ICON)
        AddItem("NewMacro", image=MACRO_ICON)
        AddItem("NewEvent", image=EVENT_ICON)
        AddItem("NewAction", image=ACTION_ICON)
        AddItem()
        AddItem("Disabled")
        AddItem()
        
        def OnLeftDown(event):
            self.egEvent = document.ExecuteSelected()
            event.Skip()
            
        def OnLeftUp(event):
            self.egEvent.SetShouldEnd()
            event.Skip()
        AddItem("Execute", downFunc=OnLeftDown, upFunc=OnLeftUp)
        
        if eg.debugLevel:
            AddItem("Reset", image=RESET_ICON)

        self.SetToolBar(toolBar)
        self.SetMinSize((400, 200))
        toolBar.Realize()
        
        
        # statusbar
        self.statusBar = StatusBar(self)
        self.SetStatusBar(self.statusBar)

        # menu creation
        menuBar = self.menuBar = eg.MenuBar(self, Text.Menu)
        menuItems = self.menuItems = eg.Bunch()

        # file menu
        menu = menuBar.AddMenu("File")
        menu.Item("New", hotkey="Ctrl+N")
        menu.Item("Open", hotkey="Ctrl+O")
        DocumentBind(menu.Item("Save", False, hotkey="Ctrl+S"), document.isDirty)
        menu.Item("SaveAs")
        menu.Separator()
        if eg.debugLevel:
            menu.Item("Export")
            menu.Item("Import")
            menu.Separator()
        menu.Item("Options")
        menu.Separator()
        menu.Item("Exit")

        # edit menu        
        menu = editMenu = menuBar.AddMenu("Edit")
        menuItems.undo = menu.Item("Undo", hotkey="Ctrl+Z")
        menuItems.redo = menu.Item("Redo", hotkey="Ctrl+Y")
        menu.Separator()
        menuItems.cut = menu.Item("Cut", hotkey="Ctrl+X")
        menuItems.copy = menu.Item("Copy", hotkey="Ctrl+C")
        menuItems.paste = menu.Item("Paste", hotkey="Ctrl+V")
        # notice that we add a ascii zero byte at the end of the hotkey.
        # this way we prevent the normal accelerator to happen. We will later
        # catch the key ourself.
        oldLogging = wx.Log.EnableLogging(False) # suppress warning
        menuItems.delete = menu.Item("Delete", hotkey="Del\x00")
        wx.Log.EnableLogging(oldLogging)
        menu.Separator()
        menu.Item("Find", hotkey="Ctrl+F")
        menu.Item("FindNext", hotkey="F3")

        # view menu        
        menu = menuBar.AddMenu("View")
        menu.CheckItem("HideShowToolbar", config.showToolbar)
        menu.Separator()
        menu.Item("ExpandAll")
        menu.Item("CollapseAll")
        menu.Separator()
        menu.CheckItem("ExpandOnEvents", config.expandOnEvents)
        menu.CheckItem("ExpandTillMacro", config.expandTillMacro, config.expandOnEvents)
        menu.Separator()
        menu.CheckItem("LogMacros", eg.config.logMacros)
        menu.CheckItem("LogActions", eg.config.logActions)
        menu.CheckItem("LogTime", config.logTime)
        menu.Separator()
        menu.Item("ClearLog")
                
        # 
        menu = menuBar.AddMenu("Configuration")
        menuItems.newPlugin = menu.Item("AddPlugin", image=PLUGIN_ICON)
        menuItems.newFolder = menu.Item("NewFolder", image=FOLDER_ICON)
        menuItems.newMacro = menu.Item("NewMacro", image=MACRO_ICON)
        menuItems.newEvent = menu.Item("NewEvent", image=EVENT_ICON)
        menuItems.newAction = menu.Item("NewAction", image=ACTION_ICON)
        menu.Separator()
        menuItems.editItem = menu.Item("Edit", hotkey="Return")
        menuItems.renameItem = menu.Item("Rename", hotkey="F2")
        menuItems.executeItem = menu.Item("Execute", hotkey="F5")
        menu.Separator()
        menuItems.disableItem = menu.CheckItem("Disabled", hotkey="Ctrl+D")
        
        # help menu
        menu = menuBar.AddMenu("Help")
        menu.Item("WebHomepage")
        menu.Item("WebForum")
        menu.Item("WebWiki")
        menu.Separator()
        menu.Item("CheckUpdate")
        menu.Separator()
        menu.Item("About")
        if eg.debugLevel:
            menu.Separator()
            menu.Item("Reload")
            menu.Item("Shell")
            menu.Item("GetInfo")
            menu.Item("CollectGarbage")
            menu.Item("Reset", hotkey="Pause")
            menu.Item("Test")
            
        menuBar.Realize()
        
        # tree popup menu
        popupMenu = self.popupMenu = eg.Menu(self, Text.Menu.EditMenu, Text.Menu)
        pmi = self.popupMenuItems = eg.Bunch()
        pmi.undo = popupMenu.Item("Undo")
        pmi.redo = popupMenu.Item("Redo")
        popupMenu.Separator()
        pmi.cut = popupMenu.Item("Cut")
        pmi.copy = popupMenu.Item("Copy")
        pmi.paste = popupMenu.Item("Paste")
        pmi.delete = popupMenu.Item("Delete")
        popupMenu.Separator()
        pmi.newPlugin = popupMenu.Item("AddPlugin", image=PLUGIN_ICON)
        pmi.newFolder = popupMenu.Item("NewFolder", image=FOLDER_ICON)
        pmi.newMacro = popupMenu.Item("NewMacro", image=MACRO_ICON)
        pmi.newEvent = popupMenu.Item("NewEvent", image=EVENT_ICON)
        pmi.newAction = popupMenu.Item("NewAction", image=ACTION_ICON)
        popupMenu.Separator()
        pmi.editItem = popupMenu.Item("Edit")
        pmi.renameItem = popupMenu.Item("Rename")
        pmi.executeItem = popupMenu.Item("Execute")
        popupMenu.Separator()
        pmi.disableItem = popupMenu.CheckItem("Disabled")
        
        iconBundle = wx.IconBundle()
        iconBundle.AddIcon(eg.taskBarIcon.stateIcons[0])
        icon = wx.EmptyIcon()
        icon.LoadFile("images/icon32x32.png", wx.BITMAP_TYPE_PNG)
        iconBundle.AddIcon(icon)
        self.SetIcons(iconBundle)
        
        self.editMenus = (toolBar.buttons, editMenu, popupMenu)
        self.lastFocus = "None"
                
        Bind = self.Bind
        Bind(wx.EVT_ICONIZE, self.OnIconize)
        Bind(wx.EVT_MENU_OPEN, self.OnMenuOpen)
        Bind(wx.EVT_CLOSE, self.OnClose)
        Bind(wx.EVT_SIZE, self.OnSize)
        Bind(wx.EVT_MOVE, self.OnMove)
        Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        Bind(wx.aui.EVT_AUI_PANE_MAXIMIZE, self.OnPaneMaximize)
        Bind(wx.aui.EVT_AUI_PANE_RESTORE, self.OnPaneRestore)
        self.UpdateViewOptions()
        self.SetSize(config.size)
        document.undoEvent.Bind(self.OnUndoEvent)
        args = document.undoEvent.Get()
        if len(args):
            self.OnUndoEvent(*args)
        document.selectionEvent.Bind(self.OnTreeSelectionEvent)
        args = document.selectionEvent.Get()
        if len(args):
            self.OnTreeSelectionEvent(*args)
        # tell FrameManager to manage this frame

        if (
            eg.config.buildNum == eg.buildNum 
            and config.perspective is not None
        ):
            #pass
            auiManager.LoadPerspective(config.perspective, False)
        auiManager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_PANE_BORDER_SIZE, 0)
        #auiManager.SetFlags(auiManager.GetFlags() ^ wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE)
        auiManager.GetPane("tree").Caption(" " + Text.Tree.caption)
        toolBar.Show(config.showToolbar)
        auiManager.Update()
        (
            auiManager.GetPane("logger").
                MinSize((100, 100)).
                Caption(" " + Text.Logger.caption)
        )
        eg.focusEvent.Bind(self.OnFocusChange)
        args = eg.focusEvent.Get()
        if len(args):
            self.OnFocusChange(*args)
        
        eg.app.clipboardEvent.Bind(self.OnClipboardChange)
        self.UpdateTitle(self.document.filePath)
        
        # create an accelerator for the "Log only assigned and activated 
        # events" checkbox. An awfull hack.
        @eg.LogIt
        def ToggleOnlyLogAssigned(event):
            cb = self.statusBar.cb
            flag = not cb.GetValue()
            cb.SetValue(flag)
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

        # create an accelerator for the "Del" key. This way we can temporarly
        # disable it while editing a tree label. 
        # (see TreeCtrl.py OnBeginLabelEdit and OnEndLabelEdit)
        delId = menuItems.delete.GetId()
        
        self.acceleratorTable = wx.AcceleratorTable(
            [
                (wx.ACCEL_NORMAL, wx.WXK_DELETE, delId),
                (wx.ACCEL_ALT, ord(hotKey), toggleOnlyLogAssignedId),
            ]
        )        
        self.SetAcceleratorTable(self.acceleratorTable)
        eg.EnsureVisible(self)
        
        
    @eg.LogIt
    def Destroy(self):
        self.document.SetTree(None)
        eg.log.SetCtrl(None)
        config.perspective = self.auiManager.SavePerspective()
        self.SetStatusBar(None)
        for dataset, func in self.observer:
            dataset.delCallback(func)
        eg.focusEvent.Unbind(self.OnFocusChange)
        eg.app.clipboardEvent.Unbind(self.OnClipboardChange)
        self.document.undoEvent.Unbind(self.OnUndoEvent)
        self.document.selectionEvent.Unbind(self.OnTreeSelectionEvent)
        self.logCtrl.Destroy()
        self.treeCtrl.Destroy()
        eg.Icons.ClearImageList()
        #gc.collect()
        return wx.Frame.Destroy(self)
    
    
    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
        
        
    def Raise(self):
        BringHwndToFront(self.GetHandle())
        wx.Frame.Raise(self)
    
    
    def UpdateTitle(self, filePath):
        if filePath is None:
            title = eg.text.General.unnamedFile
        else:
            title = os.path.basename(filePath)
        self.SetTitle("EventGhost %s - %s" % (eg.versionStr, title))

    
    def CreateTreeCtrl(self):
        treeCtrl = TreeCtrl(self, document=eg.document)
        self.document.SetTree(treeCtrl)
        self.treeCtrl = treeCtrl
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
        
    
    def CreateLogCtrl(self):
        logCtrl = LogCtrl(self)
        logCtrl.Freeze()
        self.logCtrl = logCtrl
        if not config.logTime:
            logCtrl.SetTimeLogging(False)
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
        
    
    def OnPaneClose(self, event):
        """ 
        React to a wx.aui.EVT_AUI_PANE_CLOSE event.
        
        Monitors if the toolbar gets closed and updates the check menu
        entry accordingly
        """
        paneName = event.GetPane().name
        if paneName == "toolBar":
            config.showToolbar = False
            self.menuBar.View.HideShowToolbar.Check(False)
            
        
    def OnPaneMaximize(self, event):
        """ 
        React to a wx.aui.EVT_AUI_PANE_MAXIMIZE event.
        """
        config.perspective2 = self.auiManager.SavePerspective()
        
        
    def OnPaneRestore(self, event):
        """ 
        React to a wx.aui.EVT_AUI_PANE_RESTORE event.
        """
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
    def OnClose(self, event):
        '''Handle wx.EVT_CLOSE'''
        event.Veto()
        if config.hideOnClose:
            self.document.HideFrame()
        else:
            eg.app.Exit()


    @eg.LogIt
    def OnIconize(self, event):
        '''Handle wx.EVT_ICONIZE'''
        # On iconizing, we actually destroy the frame completely
        self.document.HideFrame()


    @eg.LogIt
    def OnClipboardChange(self):
        if self.lastFocus == self.treeCtrl:
            canPaste = self.document.selection.CanPaste()
            self.toolBar.buttons.Paste.Enable(canPaste)
    
    
    #@eg.LogIt
    def OnFocusChange(self, focus):
        if focus == self.lastFocus:
            return
        if focus == "Edit":
            # avoid programmatic change of the selected item while editing
            self.UpdateViewOptions()
            # temporarily disable the "Del" accelerator
            self.SetAcceleratorTable(wx.AcceleratorTable([]))
        elif self.lastFocus == "Edit":
            # restore the "Del" accelerator
            self.SetAcceleratorTable(self.acceleratorTable)
            self.UpdateViewOptions()
            
        self.lastFocus = focus
        toolBarButtons = self.toolBar.buttons
        canCut, canCopy, canPaste, canDelete = self.GetEditCmdState(focus)
        toolBarButtons.Cut.Enable(canCut)
        toolBarButtons.Copy.Enable(canCopy)
        toolBarButtons.Paste.Enable(canPaste)
        
        
    #@eg.LogIt
    def GetEditCmdState(self, focus):
        if focus is None:
            return (False, False, False, False)
        elif focus == "Edit":
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
            #print selection
            return (
                selection.CanCut(), 
                selection.CanCopy(), 
                selection.CanPaste(), 
                selection.CanDelete(), 
            )
        else:
            return (False, False, False, False)
        
    
    def OnTreeSelectionEvent(self, selection):
        isFolder = selection.__class__ in (
            self.document.FolderItem, 
            self.document.RootItem
        )
        menuState = self.menuState
        menuState.newEvent = bool(selection.DropTest(EventItem))
        menuState.newAction = not isFolder
        menuState.edit = selection.isConfigurable
        menuState.execute = selection.isExecutable and selection.isEnabled
        menuState.rename = selection.isRenameable
        menuState.disable = selection.isDeactivatable
        
        tbb = self.toolBar.buttons
        canCut, canCopy, canPaste, canDelete =\
            self.GetEditCmdState(self.lastFocus)
        tbb.Cut.Enable(canCut)
        tbb.Copy.Enable(canCopy)
        tbb.Paste.Enable(canPaste)
        tbb.NewAction.Enable(menuState.newAction)
        tbb.NewEvent.Enable(menuState.newEvent)
        tbb.Disabled.Enable(menuState.disable)
        tbb.Execute.Enable(menuState.execute)
        
    
    def OnUndoEvent(self, hasUndos, hasRedos, undoName, redoName):
        undoName = Text.Menu.Undo + undoName
        redoName = Text.Menu.Redo + redoName
        for editMenu in self.editMenus:
            editMenu.Undo.Enable(hasUndos)
            editMenu.Undo.SetText(undoName)
            editMenu.Redo.Enable(hasRedos)
            editMenu.Redo.SetText(redoName)
        
        
    @eg.LogIt
    def SetupEditMenu(self, menuItems):
        canCut, canCopy, canPaste, canDelete =\
            self.GetEditCmdState(self.lastFocus)
        menuItems.cut.Enable(canCut)
        menuItems.copy.Enable(canCopy)
        menuItems.paste.Enable(canPaste)
        menuItems.delete.Enable(canDelete)
        menuState = self.menuState
        menuItems.newAction.Enable(menuState.newAction)
        menuItems.newEvent.Enable(menuState.newEvent)
        menuItems.editItem.Enable(menuState.edit)
        menuItems.executeItem.Enable(menuState.execute)
        menuItems.renameItem.Enable(menuState.rename)
        menuItems.disableItem.Enable(menuState.disable)
        menuItems.disableItem.Check(
            bool(self.document.selection and not self.document.selection.isEnabled)
        )
        
        
    @eg.LogIt
    def OnMenuOpen(self, event):
        self.SetupEditMenu(self.menuItems)            
            
            
    def UpdateViewOptions(self):
        expandOnEvents = (
            not self.IsIconized()
            and config.expandOnEvents 
            and (self.treeCtrl and not self.treeCtrl.isInEditLabel)
        )
        ActionItem.shouldSelectOnExecute = (
            expandOnEvents and not config.expandTillMacro
        )
        MacroItem.shouldSelectOnExecute = expandOnEvents
        
        
    @eg.LogIt
    def DispatchCommand(self, command, event):
        if self.lastFocus == "Edit" and command == "Clear":
            editCtrl = self.treeCtrl.GetEditControl()
            editCtrl.Remove(*editCtrl.GetSelection())
            return
        focus = self.FindFocus()
        method = getattr(focus, command, None)
        if method is not None:
            method()
        else:
            event.Skip()
        
        
    #-------------------------------------------------------------------------
    #---- Menu Handlers ------------------------------------------------------
    #-------------------------------------------------------------------------
    
    #------- file menu -------------------------------------------------------
    
    def OnCmdNew(self, event):
        """ Handle the menu command 'New'. """
        if self.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            return
        eg.eventThread.CallWait(eg.eventThread.StopSession)
        self.treeCtrl.DeleteAllItems()
        eg.eventThread.Call(eg.eventThread.StartSession, None)


    def OnCmdOpen(self, event):
        """ Handle the menu command 'Open'. """
        if self.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            return wx.ID_CANCEL
        fileDialog = wx.FileDialog(self, "", "", "", "*.xml", wx.OPEN)
        result = fileDialog.ShowModal()
        fileDialog.Destroy()
        if result == wx.ID_CANCEL:
            return wx.ID_CANCEL
        filePath = fileDialog.GetPath()
        eg.eventThread.CallWait(eg.eventThread.StopSession)
        self.treeCtrl.DeleteAllItems()
        eg.eventThread.Call(eg.eventThread.StartSession, filePath)
        
        
    def OnCmdSave(self, event=None):
        """ Handle the menu command 'Save'. """
        self.document.Save()


    def OnCmdSaveAs(self, event=None):
        """ Handle the menu command 'Save As'. """
        self.document.SaveAs()


    def OnCmdExport(self, event):
        """ Handle the menu command 'Export'. """
        result = eg.ExportDialog().DoModal()
        if result:
            for item in result:
                print item.GetLabel()


    def OnCmdImport(self, event):
        """ Handle the menu command 'Import'. """
        pass
    
    
    def OnCmdOptions(self, event):
        """ Handle the menu command 'Options...'. """
        eg.OptionsDialog.ShowModeless(self)
        
        
    def OnCmdExit(self, event):
        eg.app.Exit()
        
        
    #------- edit menu -------------------------------------------------------
    
    def OnCmdUndo(self, event):
        """ Handle the menu command 'Undo'. """
        self.document.Undo()
            
            
    def OnCmdRedo(self, event):
        """ Handle the menu command 'Redo'. """
        self.document.Redo()
        
    
    def OnCmdCut(self, event):
        """ Handle the menu command 'Cut'. """
        self.DispatchCommand("Cut", event)
        
        
    def OnCmdCopy(self, event):
        """ Handle the menu command 'Copy'. """
        self.DispatchCommand("Copy", event)
            
            
    def OnCmdPaste(self, event):
        """ Handle the menu command 'Paste'. """
        self.DispatchCommand("Paste", event)
    
    
    @eg.LogIt
    def OnCmdDelete(self, event):
        """ Handle the menu command 'Delete'. """
        #if self.focus == "Edit":
        #    self.tree.GetEditControl().EmulateKeyPress()
        #else:
        self.DispatchCommand("Clear", event)
                
                
    def OnCmdFind(self, event):
        """ Handle the menu command 'Find'. """
        if self.findDialog is None:
            self.findDialog = eg.FindDialog(self, self.document)
        self.findDialog.Show()
        
        
    def OnCmdFindNext(self, event):
        """ Handle the menu command 'Find Next'. """
        if (
            self.findDialog is None 
            or not self.findDialog.searchButton.IsEnabled()
        ):
            self.OnCmdFind(event)
        else:
            self.findDialog.OnFindButton()
        

    def OnCmdAddPlugin(self, event):
        """ 
        Menu: Edit -> Add Plugin
        """
        pluginInfo = eg.AddPluginDialog(self).DoModal()
        if pluginInfo is None:
            return
        eg.Greenlet(UndoableTasks.NewPlugin().Do).switch(self.document, pluginInfo)
            
            
    def OnCmdNewEvent(self, event):
        """ 
        Menu: Edit -> New Event
        """
        UndoableTasks.NewEvent().Do(self.document)
                
                
    def OnCmdNewFolder(self, event):
        """ 
        Menu: Edit -> New Folder
        """
        UndoableTasks.NewFolder().Do(self.document)
        
    
    def OnCmdNewMacro(self, event):
        """ 
        Menu: Edit -> New Macro
        """
        eg.Greenlet(UndoableTasks.NewMacro().Do).switch(self.document)
        
    
    def OnCmdNewAction(self, event):
        """ 
        Menu: Edit -> New Action
        """        
        # let the user choose an action
        action = eg.AddActionDialog(self).DoModal()
        # if user canceled the dialog, take a quick exit
        if action is None:
            return None
        eg.Greenlet(UndoableTasks.NewAction().Do).switch(self.document, action)
        
    
    def OnCmdRename(self, event):
        """ 
        Menu: Edit -> Rename
        """
        self.treeCtrl.SetFocus()
        self.treeCtrl.EditLabel(self.treeCtrl.GetSelection())


    def OnCmdEdit(self, event):
        """ 
        Menu: Edit -> Configure Element
        """
        UndoableTasks.CmdConfigure().Try(self.document)


    def OnCmdExecute(self, event):
        """ 
        Menu: Edit -> Execute Element
        """
        self.document.ExecuteSelected().SetShouldEnd()


    def OnCmdDisabled(self, event):
        UndoableTasks.CmdToggleEnable(self.document)


    #------- view menu -------------------------------------------------------
    
    def OnCmdHideShowToolbar(self, event):
        config.showToolbar = not config.showToolbar
        #self.auiManager.GetPane("toolBar").Show(config.showToolbar)
        #self.auiManager.Update()
        self.toolBar.Show(config.showToolbar)
        self.Layout()
        self.SendSizeEvent()


    def OnCmdLogMacros(self, event):
        eg.config.logMacros = not eg.config.logMacros
        self.menuBar.View.LogMacros.Check(eg.config.logMacros)
        
        
    def OnCmdLogActions(self, event):
        eg.config.logActions = not eg.config.logActions
        self.menuBar.View.LogActions.Check(eg.config.logActions)
        
        
    def OnCmdExpandOnEvents(self, event):
        config.expandOnEvents = not config.expandOnEvents
        self.menuBar.View.ExpandOnEvents.Check(config.expandOnEvents)
        self.menuBar.View.ExpandTillMacro.Enable(config.expandOnEvents)
        self.UpdateViewOptions()
        
        
    def OnCmdExpandTillMacro(self, event):
        config.expandTillMacro = not config.expandTillMacro
        self.menuBar.View.ExpandTillMacro.Check(config.expandTillMacro)
        self.UpdateViewOptions()
        
        
    def OnCmdLogTime(self, event):
        flag = event.IsChecked()
        config.logTime = flag
        self.logCtrl.SetTimeLogging(flag)
    
    
    def OnCmdExpandAll(self, event):
        self.treeCtrl.ExpandAll()
    
    
    def OnCmdCollapseAll(self, event):
        self.treeCtrl.CollapseAll()
    
    
    def OnCmdClearLog(self, event):
        self.logCtrl.OnCmdClearLog(event)
        
    
    #------- help menu -------------------------------------------------------
    
    def OnCmdWebHomepage(self, event):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/", True, True)
    
    
    def OnCmdWebForum(self, event):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/forum/", True, True)
    
    
    def OnCmdWebWiki(self, event):
        import webbrowser
        webbrowser.open("http://www.eventghost.org/wiki/", True, True)
    
    
    def OnCmdCheckUpdate(self, event):
        eg.CheckUpdate.CheckUpdateManually()
    
    
    def OnCmdAbout(self, event):
        #eg.AboutDialog(self).DoModal()
        eg.AboutDialog.ShowModeless(self)
    
        
    #----- debugging and experimental stuff that will be removed someday -----
    
    def OnCmdReload(self, event):
        if self.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            return wx.ID_CANCEL
        eg.eventThread.CallWait(eg.eventThread.StopSession)
        self.treeCtrl.DeleteAllItems()
        eg.eventThread.Call(eg.eventThread.StartSession, self.document.filePath)
    
    
    def OnCmdShell(self, event):
        import wx.py.crust
        intro = "Welcome to EventGhost"
        win = wx.py.crust.CrustFrame(
            None, 
            -1, 
            rootObject=eg.globals.__dict__, 
            #locals=eg.globals.__dict__, 
            locals={}, 
            rootIsNamespace=False
        )
        win.Show()
        self.crust = win
        
        
    def OnCmdGetInfo(self, event):
        self.document.selection.ShowInfo()

        
    def OnCmdCollectGarbage(self, event):
        import gc
        gc.set_debug(gc.DEBUG_SAVEALL)
    
        from pprint import pprint
        print "unreachable object count:", gc.collect()
        #print_cycles(gc.garbage, sys.stdout)
        l = gc.garbage[:]
        for i, o in enumerate(l):
            print "Object Num %d:" % i
            pprint(o)
            print "Referrers:"
            #print(gc.get_referrers(o))
            print "Referents:"
            #print(gc.get_referents(o))
        print "Done."
        #print "unreachable object count:", gc.collect()
        #from pprint import pprint
        #pprint(gc.garbage)
        
        
    def OnCmdReset(self, event):
        eg.stopExecutionFlag = True
        eg.programCounter = None
        del eg.programReturnStack[:]
        eg.eventThread.FlushAllEvents()
        eg.actionThread.FlushAllEvents()
        eg.PrintError("Execution stopped by user")
        
    
    def OnCmdTest(self, event):
        eg.AddEventDialog(self).ShowModal()
        #eg.NamespaceTree.Test()

        
import gc
from types import FrameType

def print_cycles(objects, outstream=sys.stdout, show_progress=False):
    """
    objects:       A list of objects to find cycles in.  It is often useful
                   to pass in gc.garbage to find the cycles that are
                   preventing some objects from being garbage collected.
    outstream:     The stream for output.
    show_progress: If True, print the number of objects reached as they are
                   found.
    """
    def print_path(path):
        for i, step in enumerate(path):
            # next "wraps around"
            next = path[(i + 1) % len(path)]

            outstream.write("   %s -- " % str(type(step)))
            if isinstance(step, dict):
                for key, val in step.items():
                    if val is next:
                        outstream.write("[%s]" % repr(key))
                        break
                    if key is next:
                        outstream.write("[key] = %s" % repr(val))
                        break
            elif isinstance(step, list):
                outstream.write("[%d]" % step.index(next))
            elif isinstance(step, tuple):
                outstream.write("[%d]" % list(step).index(next))
            else:
                outstream.write(repr(step))
            outstream.write(" ->\n")
        outstream.write("\n")
    
    def recurse(obj, start, all, current_path):
        if show_progress:
            outstream.write("%d\r" % len(all))

        all[id(obj)] = None

        referents = gc.get_referents(obj)
        for referent in referents:
            # If we've found our way back to the start, this is
            # a cycle, so print it out
            if referent is start:
                print_path(current_path)

            # Don't go back through the original list of objects, or
            # through temporary references to the object, since those
            # are just an artifact of the cycle detector itself.
            elif referent is objects or isinstance(referent, FrameType): 
                continue

            # We haven't seen this object before, so recurse
            elif id(referent) not in all:
                recurse(referent, start, all, current_path + [obj])

    for obj in objects:
        try:
            outstream.write("Examining: %s\n" % repr(obj))
        except:
            outstream.write("Examining: %s\n" % obj)
        recurse(obj, obj, { }, [])        
