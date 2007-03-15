# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
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

import wx
import wx.aui

import eg
from eg import (
    EventItem, 
    ActionItem, 
    MacroItem, 
    FolderItem, 
    RootItem, 
)
from eg.IconTools import GetIcon
#from eg.WinAPI.Utils import BringHwndToFront

PLUGIN_ICON = GetIcon('images/plugin.png')
FOLDER_ICON = GetIcon('images/folder.png')
MACRO_ICON = GetIcon('images/macro.png')
EVENT_ICON = GetIcon('images/event.png')
ACTION_ICON = GetIcon('images/action.png')
RESET_ICON = GetIcon('images/error.png')

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
    treeStateData = None

config = eg.GetConfig("mainFrame", DefaultConfig)



class MainFrame(wx.Frame):
    """ This is the MainFrame of EventGhost """
        
    def __init__(self, document):
        """ Create the MainFrame """
        eg.AssertThread()
        
        text = eg.text
        self.document = document
        self.menuState = eg.Bunch()
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
        toolBar = eg.ToolBar(self, style=wx.TB_FLAT)#|wx.TB_NODIVIDER)
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
            self.toolBarSpacer = wx.Control(toolBar, size=(50, 1))
            toolBar.AddControl(self.toolBarSpacer)
        
            AddItem("Reset", image=RESET_ICON)
            #AddItem("Test", image=RESET_ICON)

        toolBar.Realize()
        self.SetToolBar(toolBar)
        self.SetMinSize((400, 200))
        
        # statusbar
        from StatusBar import StatusBar
        self.statusBar = StatusBar(self)
        self.SetStatusBar(self.statusBar)

        # menu creation
        menuBar = self.menuBar = eg.MenuBar(self, Text.Menu)
        menuItems = self.menuItems = eg.Bunch()

        # file menu
        fileMenu = menuBar.AddMenu("File")
        AddItem = fileMenu.AddItem
        AddItem("New", hotkey="Ctrl+N")
        AddItem("Open", hotkey="Ctrl+O")
        DocumentBind(AddItem("Save", False, hotkey="Ctrl+S"), document.isDirty)
        AddItem("SaveAs")
        AddItem()
        if eg.debugLevel:
            AddItem("Export")
            AddItem("Import")
            AddItem()
        AddItem("Options")
        AddItem()
        AddItem("Exit", hotkey="Alt+F4")

        # edit menu        
        editMenu = menuBar.AddMenu("Edit")
        AddItem = editMenu.AddItem
        
        menuItems.undo = AddItem("Undo", hotkey="Ctrl+Z")
        menuItems.redo = AddItem("Redo", hotkey="Ctrl+Y")
        AddItem()
        menuItems.cut = AddItem("Cut", hotkey="Ctrl+X")
        menuItems.copy = AddItem("Copy", hotkey="Ctrl+C")
        menuItems.paste = AddItem("Paste", hotkey="Ctrl+V")
        menuItems.delete = AddItem("Delete", hotkey="Del")
        AddItem()
        AddItem("Find", hotkey="Ctrl+F")
        AddItem("FindNext", hotkey="F3")

        # view menu        
        viewMenu = menuBar.AddMenu("View")
        AddItem = viewMenu.AddItem
        AddItem(
            "HideShowToolbar", 
            kind=wx.ITEM_CHECK
        ).Check(config.showToolbar)
        AddItem()
        AddItem("ExpandAll")
        AddItem("CollapseAll")
        AddItem()
        AddItem(
            "ExpandOnEvents", 
            kind=wx.ITEM_CHECK
        ).Check(config.expandOnEvents)
        AddItem(
            "ExpandTillMacro", 
            config.expandOnEvents, 
            kind=wx.ITEM_CHECK
        ).Check(config.expandTillMacro)
        AddItem()
        AddItem("LogActions", kind=wx.ITEM_CHECK).Check(eg.config.logActions)
        AddItem("LogTime", kind=wx.ITEM_CHECK).Check(config.logTime)
                
        # 
        configurationMenu = menuBar.AddMenu("Configuration")
        AddItem = configurationMenu.AddItem
        menuItems.newPlugin = AddItem("AddPlugin", image=PLUGIN_ICON)
        menuItems.newFolder = AddItem("NewFolder", image=FOLDER_ICON)
        menuItems.newMacro = AddItem("NewMacro", image=MACRO_ICON)
        menuItems.newEvent = AddItem("NewEvent", image=EVENT_ICON)
        menuItems.newAction = AddItem("NewAction", image=ACTION_ICON)
        AddItem()
        menuItems.editItem = AddItem("Edit", hotkey="Return")
        menuItems.renameItem = AddItem("Rename", hotkey="F2")
        menuItems.executeItem = AddItem("Execute", hotkey="F5")
        AddItem()
        menuItems.disableItem = AddItem(
            "Disabled", 
            kind=wx.ITEM_CHECK, 
            hotkey="Ctrl+D", 
        )
        
        # help menu
        helpMenu = menuBar.AddMenu("Help")
        AddItem = helpMenu.AddItem
        AddItem("WebHomepage")
        AddItem("WebForum")
        AddItem("WebWiki")
        AddItem()
        AddItem("CheckUpdate")
        AddItem()
        AddItem("About")
        if eg.debugLevel:
            AddItem()
            AddItem("Reload")
            AddItem("Shell")
            AddItem("GetInfo")
            AddItem("CollectGarbage")
            AddItem("Reset", hotkey = "Pause")
            AddItem("Test")
            
        menuBar.Realize()
        
        # tree popup menu
        popupMenu = self.popupMenu = eg.Menu(
            self, 
            Text.Menu.EditMenu, 
            Text.Menu
        )
        popupMenuItems = self.popupMenuItems = eg.Bunch()
        AddItem = popupMenu.AddItem
        popupMenuItems.undo = AddItem("Undo")
        popupMenuItems.redo = AddItem("Redo")
        AddItem()
        popupMenuItems.cut = AddItem("Cut")
        popupMenuItems.copy = AddItem("Copy")
        popupMenuItems.paste = AddItem("Paste")
        popupMenuItems.delete = AddItem("Delete")
        AddItem()
        popupMenuItems.newPlugin = AddItem("AddPlugin", image=PLUGIN_ICON)
        popupMenuItems.newFolder = AddItem("NewFolder", image=FOLDER_ICON)
        popupMenuItems.newMacro = AddItem("NewMacro", image=MACRO_ICON)
        popupMenuItems.newEvent = AddItem("NewEvent", image=EVENT_ICON)
        popupMenuItems.newAction = AddItem("NewAction", image=ACTION_ICON)
        AddItem()
        popupMenuItems.editItem = AddItem("Edit")
        popupMenuItems.renameItem = AddItem("Rename")
        popupMenuItems.executeItem = AddItem("Execute")
        AddItem()
        popupMenuItems.disableItem = AddItem("Disabled", kind=wx.ITEM_CHECK)
        
        self.SetIcon(eg.app.taskBarIcon.stateIcons[0])
        
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
            pass
            #auiManager.LoadPerspective(config.perspective, False)
        auiManager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_PANE_BORDER_SIZE, 0)

        #auiManager.GetPane("tree").Caption(" " + Text.Tree.caption)
        toolBar.Show(config.showToolbar)
        auiManager.Update()
        auiManager.GetPane("logger").MinSize((100, 100))
        eg.app.focusEvent.Bind(self.OnFocusChange)
        args = eg.app.focusEvent.Get()
        if len(args):
            self.OnFocusChange(*args)
        
        eg.app.clipboardEvent.Bind(self.OnClipboardChange)
        self.UpdateTitle(self.document.filePath)
        
        
    @eg.LogIt
    def Destroy(self):
        self.document.frame = None
        config.perspective = self.auiManager.SavePerspective()
        self.SetStatusBar(None)
        for dataset, func in self.observer:
            dataset.delCallback(func)
        eg.app.focusEvent.Unbind(self.OnFocusChange)
        eg.app.clipboardEvent.Unbind(self.OnClipboardChange)
        self.document.undoEvent.Unbind(self.OnUndoEvent)
        self.document.selectionEvent.Unbind(self.OnTreeSelectionEvent)
        if self.logCtrl:
            self.logCtrl.Destroy()
        if self.treeCtrl:
            self.treeCtrl.Destroy()
        eg.app.mainFrame = None
        gc.collect()
        return wx.Frame.Destroy(self)
    
    
    @eg.LogIt
    def __del__(self):
        pass
        
        
    def UpdateTitle(self, filePath):
        if filePath is None:
            title = eg.text.General.unnamedFile
        else:
            title = os.path.basename(filePath)
        self.SetTitle("EventGhost %s - %s" % (eg.versionStr, title))

    
    def CreateTreeCtrl(self):
        from TreeCtrl import TreeCtrl
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
        from LogCtrl import LogCtrl
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
            self.Destroy()
        else:
            eg.app.Exit()


    @eg.LogIt
    def OnIconize(self, event):
        '''Handle wx.EVT_ICONIZE'''
        # On iconizing, we actually destroy the frame completely
        self.Destroy()


#    def OnClose(self, event=None):
#        res = self.document.CheckFileNeedsSave()
#        if res == wx.ID_CANCEL:
#            eg.Notice("Skipping event in OnClose")
#            if event:
#                event.Skip(False)
#            return wx.ID_CANCEL
#        #eg.Notice("Binding close dummy")
#        #self.Bind(wx.EVT_CLOSE, self.CloseDummy)
#        eg.config.hideOnStartup = self.IsIconized()
#        eg.config.autoloadFilePath = self.document.filePath.get()
#        #config.perspective = self.auiManager.SavePerspective()
#        if res in (wx.ID_OK, wx.ID_YES):
#            if self.logCtrl:
#                self.CloseLog()
#            if self.treeCtrl:
#                self.CloseTree()
#            self.CloseSelf()
#        return None
        


#    def BringToFront(self):
#        self.Iconize(False)
#        self.Show(True)
#        self.Raise()
#        BringHwndToFront(self.GetHandle())
#        
#        

    @eg.LogIt
    def OnClipboardChange(self):
        if self.lastFocus == "Tree":
            canPaste = self.document.selection.CanPaste()
            self.toolBar.buttons.Paste.Enable(canPaste)
    
    
    def OnFocusChange(self, focus):
        if focus == self.lastFocus:
            return
        self.lastFocus = focus
        tbb = self.toolBar.buttons
        canCut, canCopy, canPaste, canDelete = self.GetEditCmdState(focus)
        tbb.Cut.Enable(canCut)
        tbb.Copy.Enable(canCopy)
        tbb.Paste.Enable(canPaste)
        
        
    @eg.LogIt
    def GetEditCmdState(self, focus):
        if focus is None:
            return (False, False, False, False)
        elif focus == "Edit":
            return (True, True, True, True)
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
        
    
    def OnTreeSelectionEvent(self, selection):
        isFolder = selection.__class__ in (
            self.document.FolderItem, 
            self.document.RootItem
        )
        menuState = self.menuState
        menuState.newEvent = bool(selection.DropTest(EventItem))
        menuState.newAction = not isFolder
        menuState.edit = selection.IsConfigurable()
        menuState.execute = selection.canExecute and selection.isEnabled
        menuState.rename = selection.IsEditable()
        menuState.disable = selection.CanDisable()
        
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
        menuItems.disableItem.Check(self.document.selection and not self.document.selection.isEnabled)
        
        
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
        
        
    def DispatchCommand(self, command):
        focus = self.FindFocus()
        method = getattr(focus, command, None)
        if method is not None:
            method()
        
        
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
        dlg = wx.FileDialog(self, "", "", "", "*.xml", wx.OPEN)
        res = dlg.ShowModal()
        dlg.Destroy()
        if res == wx.ID_CANCEL:
            return wx.ID_CANCEL
        filePath = dlg.GetPath()
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
        from eg.Dialogs.ExportDialog import ExportDialog
        result = ExportDialog().DoModal()
        if result:
            for item in result:
                print item.GetLabel()


    def OnCmdImport(self, event):
        """ Handle the menu command 'Import'. """
        pass
    
    
    def OnCmdOptions(self, event):
        """ Handle the menu command 'Options...'. """
        from eg.Dialogs.OptionsDialog import OptionsDialog
        OptionsDialog().DoModal()
        
        
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
        self.DispatchCommand("Cut")
        
        
    def OnCmdCopy(self, event):
        """ Handle the menu command 'Copy'. """
        self.DispatchCommand("Copy")
            
            
    def OnCmdPaste(self, event):
        """ Handle the menu command 'Paste'. """
        self.DispatchCommand("Paste")
    
    
    def OnCmdDelete(self, event):
        """ Handle the menu command 'Delete'. """
        self.DispatchCommand("Clear")
                
                
    def OnCmdFind(self, event):
        """ Handle the menu command 'Find'. """
        if self.findDialog is None:
            from Dialogs.FindDialog import FindDialog
            self.findDialog = FindDialog(self, self.document)
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
        from UndoableCommands import CmdNewPlugin
        eg.actionThread.Call(CmdNewPlugin().Do, self.document)
            
            
    def OnCmdNewEvent(self, event):
        """ 
        Menu: Edit -> New Event
        """
        from UndoableCommands import CmdNewEvent
        eg.actionThread.Call(CmdNewEvent().Do, self.document)
                
                
    def OnCmdNewFolder(self, event):
        """ 
        Menu: Edit -> New Folder
        """
        from UndoableCommands import CmdNewFolder
        eg.actionThread.Call(CmdNewFolder().Do, self.document)
        
    
    def OnCmdNewMacro(self, event):
        """ 
        Menu: Edit -> New Macro
        """
        from UndoableCommands import CmdNewMacro
        eg.actionThread.Call(CmdNewMacro().Do, self.document)
        
    
    def OnCmdNewAction(self, event):
        """ 
        Menu: Edit -> New Action
        """        
        from UndoableCommands import CmdNewAction
        eg.actionThread.Call(CmdNewAction().Do, self.document)
        
    
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
        item = self.document.selection
        if isinstance(item, ActionItem):
            item.Configure()


    def OnCmdExecute(self, event):
        """ 
        Menu: Edit -> Execute Element
        """
        self.document.ExecuteSelected().SetShouldEnd()


    def OnCmdDisabled(self, event):
        from UndoableCommands import CmdToggleEnable
        CmdToggleEnable(self.document)


    #------- view menu -------------------------------------------------------
    
    def OnCmdHideShowToolbar(self, event):
        config.showToolbar = not config.showToolbar
        #self.auiManager.GetPane("toolBar").Show(config.showToolbar)
        #self.auiManager.Update()
        self.toolBar.Show(config.showToolbar)
        self.Layout()
        self.SendSizeEvent()


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
    
    
    def OnCmdLogTime(self, event):
        flag = event.IsChecked()
        config.logTime = flag
        self.logCtrl.SetTimeLogging(flag)
    
    
    def OnCmdExpandAll(self, event):
        self.treeCtrl.ExpandAll()
    
    
    def OnCmdCollapseAll(self, event):
        self.treeCtrl.CollapseAll()
    
    
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
        import CheckUpdate
        CheckUpdate.CheckUpdateManually()
    
    
    def OnCmdAbout(self, event):
        from eg.Dialogs.AboutDialog import AboutDialog
        AboutDialog().DoModal()
    
        
    #----- debugging and experimental stuff that will be removed someday -----
    
    def OnCmdReload(self, event):
        if self.CheckFileNeedsSave() == wx.ID_CANCEL:
            return wx.ID_CANCEL
        eg.eventThread.CallWait(eg.eventThread.StopSession)
        self.treeCtrl.DeleteAllItems()
        eg.eventThread.Call(eg.eventThread.StartSession, self.document.filePath)
    
    
    def OnCmdShell(self, event):
        import wx.py.crust
        intro = "Welcome to EventGhost"
        win = wx.py.crust.CrustFrame(
            self, 
            -1, 
            rootObject=eg.globals, 
            locals=eg.globals.__dict__, 
            rootIsNamespace=False
        )
        win.Show()
        self.crust = win
        
        
    def OnCmdGetInfo(self, event):
        self.document.selection.ShowInfo()
        
        
    def OnCmdCollectGarbage(self, event):
        print gc.collect()
        print gc.garbage
        
        
    def OnCmdReset(self, event):
        eg.__dict__["stopExecutionFlag"] = True
        eg.SetProgramCounter(None)
        del eg.programReturnStack[:]
        eg.eventThread.FlushAllEvents()
        eg.actionThread.FlushAllEvents()
        eg.PrintError("Execution stopped by user")
        
    
    def OnCmdTest(self, event):
        self.Close()
        return
    
        self.CreateLogCtrl()
        return
        
        from eg.Dialogs import LinkListDialog
        reload(LinkListDialog)
        dialog = LinkListDialog.LinkListDialog(self)
        dialog.ShowModal()
        dialog.Destroy()
        
        
