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
import re

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

Text = eg.text.MainFrame

        
class DefaultConfig:
    position = (50, 50)
    size = (700, 433)
    showToolbar = True
    hideOnClose = False
    logTime = False
    expandOnEvents = False
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
        self.aboutDialog = None
        self.optionsDialog = None
        self.iconState = 0
        self.findDialog = None
        self.openDialogs = []
        self.menuState = eg.Bunch(
            addEvent = False,
            ddAction = False,
            configure = False,
            execute = False,
            rename = False,
            disable = False,
        )
        self.style=(
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

        self.observer = []
        for item in (self.toolBar.buttons.save, self.menuBar.File.save):
            item.Enable(document.isDirty.get())
            document.isDirty.addCallback(item.Enable)
            self.observer.append((document.isDirty, item.Enable))
        
        iconBundle = wx.IconBundle()
        iconBundle.AddIcon(eg.taskBarIcon.stateIcons[0])
        icon = wx.EmptyIcon()
        icon.LoadFile("images/icon32x32.png", wx.BITMAP_TYPE_PNG)
        iconBundle.AddIcon(icon)
        self.SetIcons(iconBundle)
        
        self.editMenus = (
            self.toolBar.buttons, 
            self.MenuBar.Edit, 
            self.popupMenu
        )
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
        self.toolBar.Show(config.showToolbar)
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
        
        delId = wx.NewId()
        def OnDelKey(event):
            self.DispatchCommand('Clear', event)
        wx.EVT_MENU(self, delId, OnDelKey)
        
        self.acceleratorTable = wx.AcceleratorTable(
            [
                (wx.ACCEL_NORMAL, wx.WXK_DELETE, delId),
                (wx.ACCEL_ALT, ord(hotKey), toggleOnlyLogAssignedId),
            ]
        )        
        self.SetAcceleratorTable(self.acceleratorTable)
        eg.EnsureVisible(self)
    
    
    def CreateToolBar(self):
        """
        Creates the toolbar of the frame.
        """
        def OnLeftDown(event):
            self.egEvent = self.document.ExecuteSelected()
            event.Skip()
            
        def OnLeftUp(event):
            self.egEvent.SetShouldEnd()
            event.Skip()
            
        toolBar = eg.ToolBar(self, style=wx.TB_FLAT)
        toolBar.SetParams(self, Text.Menu)
        toolBar.SetToolBitmapSize((16, 16))
        Add = toolBar.AddButton
        Add("New")
        Add("Open")
        Add("Save")
        Add()
        Add("Cut")
        Add("Copy")
        Add("Paste")
        Add()
        Add("Undo")
        Add("Redo")
        Add()
        Add("AddPlugin", image=ADD_PLUGIN_ICON)
        Add("AddFolder", image=ADD_FOLDER_ICON)
        Add("AddMacro", image=ADD_MACRO_ICON)
        Add("AddEvent", image=ADD_EVENT_ICON)
        Add("AddAction", image=ADD_ACTION_ICON)
        Add()
        Add("Disabled")
        Add()
        Add("Execute", downFunc=OnLeftDown, upFunc=OnLeftUp)
        if eg.debugLevel:
            Add("Reset", image=RESET_ICON)

        self.SetToolBar(toolBar)
        toolBar.Realize()
        return toolBar
        
        
    def CreateMenuBar(self):
        """
        Creates the main menu bar and all its menus.
        """
        menuBar = eg.MenuBar(self, Text.Menu)
        menuItems = self.menuItems = eg.Bunch()

        # file menu
        Add = menuBar.AddMenu("File").AddItem
        Add("New", hotkey="Ctrl+N")
        Add("Open", hotkey="Ctrl+O")
        Add("Save", hotkey="Ctrl+S").Enable(False)
        Add("SaveAs")
        Add()
        if eg.debugLevel:
            Add("Export")
            Add("Import")
            Add()
        Add("Options")
        Add()
        Add("Exit")

        # edit menu        
        Add = menuBar.AddMenu("Edit").AddItem
        menuItems.undo = Add("Undo", hotkey="Ctrl+Z")
        menuItems.redo = Add("Redo", hotkey="Ctrl+Y")
        Add()
        menuItems.cut = Add("Cut", hotkey="Ctrl+X")
        menuItems.copy = Add("Copy", hotkey="Ctrl+C")
        menuItems.paste = Add("Paste", hotkey="Ctrl+V")
        menuItems.delete = Add("Delete", hotkey="Del")
        Add()
        Add("Find", hotkey="Ctrl+F")
        Add("FindNext", hotkey="F3")

        # view menu        
        Add = menuBar.AddMenu("View").AddItem
        Add("HideShowToolbar", kind=wx.ITEM_CHECK).Check(config.showToolbar)
        Add()
        Add("ExpandAll")
        Add("CollapseAll")
        Add()
        Add("ExpandOnEvents", kind=wx.ITEM_CHECK).Check(config.expandOnEvents)
        Add("ExpandTillMacro", kind=wx.ITEM_CHECK)\
            .Check(config.expandTillMacro)\
            .Enable(config.expandOnEvents)
        Add()
        Add("LogMacros", kind=wx.ITEM_CHECK).Check(eg.config.logMacros)
        Add("LogActions", kind=wx.ITEM_CHECK).Check(eg.config.logActions)
        Add("LogTime", kind=wx.ITEM_CHECK).Check(config.logTime)
        Add()
        Add("ClearLog")
                
        # configuration menu
        Add = menuBar.AddMenu("Configuration").AddItem
        menuItems.addPlugin = Add("AddPlugin", image=ADD_PLUGIN_ICON)
        menuItems.addFolder = Add("AddFolder", image=ADD_FOLDER_ICON)
        menuItems.addMacro = Add("AddMacro", image=ADD_MACRO_ICON)
        menuItems.addEvent = Add("AddEvent", image=ADD_EVENT_ICON)
        menuItems.addAction = Add("AddAction", image=ADD_ACTION_ICON)
        Add()
        menuItems.configure = Add("Configure", hotkey="Return")
        menuItems.rename = Add("Rename", hotkey="F2")
        menuItems.execute = Add("Execute", hotkey="F5")
        Add()
        menuItems.disabled = Add("Disabled", hotkey="Ctrl+D", kind=wx.ITEM_CHECK)
        
        # help menu
        Add = menuBar.AddMenu("Help").AddItem
        Add("WebHomepage")
        Add("WebForum")
        Add("WebWiki")
        Add()
        Add("CheckUpdate")
        Add()
        Add("About")
        if eg.debugLevel:
            Add()
            Add("Reload")
            Add("Shell")
            Add("GetInfo")
            Add("CollectGarbage")
            Add("Reset", hotkey="Pause")
            Add("AddEventDialog")
            
        menuBar.Realize()
        return menuBar
        
        
    def CreateTreePopupMenu(self):
        """
        Creates the pop-up menu for the configuration tree.
        
        Since our custom menu code automatically assign events to the window
        that creates the menu, we create it here and not in the tree control,
        because most menu commands are handled by the frame.
        """
        popupMenu = eg.Menu(self, Text.Menu.EditMenu, Text.Menu)
        Add = popupMenu.AddItem
        Add("Undo")
        Add("Redo")
        Add()
        Add("Cut")
        Add("Copy")
        Add("Paste")
        Add("Delete")
        Add()
        Add("AddPlugin", image=ADD_PLUGIN_ICON)
        Add("AddFolder", image=ADD_FOLDER_ICON)
        Add("AddMacro", image=ADD_MACRO_ICON)
        Add("AddEvent", image=ADD_EVENT_ICON)
        Add("AddAction", image=ADD_ACTION_ICON)
        Add()
        Add("Configure")
        Add("Rename")
        Add("Execute")
        Add()
        Add("Disabled", kind=wx.ITEM_CHECK)
        return popupMenu
    
        
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
        
    
    @eg.LogItWithReturn
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
        result = wx.Frame.Destroy(self)
        eg.Icons.ClearImageList()
        return result
    
    
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

    
    def OnPaneClose(self, event):
        """ 
        React to a wx.aui.EVT_AUI_PANE_CLOSE event.
        
        Monitors if the toolbar gets closed and updates the check menu
        entry accordingly
        """
        paneName = event.GetPane().name
        if paneName == "toolBar":
            config.showToolbar = False
            self.menuBar.View.hideShowToolbar.Check(False)
            
        
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
        if len(self.openDialogs) == 0:
            if config.hideOnClose:
                self.document.HideFrame()
            else:
                eg.app.Exit()
        else:
            self.RequestUserAttention()


    @eg.LogIt
    def OnIconize(self, event):
        '''Handle wx.EVT_ICONIZE'''
        # On iconizing, we actually destroy the frame completely
        self.document.HideFrame()


    @eg.LogIt
    def OnClipboardChange(self):
        if self.lastFocus == self.treeCtrl:
            canPaste = self.document.selection.CanPaste()
            self.toolBar.buttons.paste.Enable(canPaste)
    
    
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
        toolBarButtons = self.toolBar.buttons
        canCut, canCopy, canPaste, canDelete = self.GetEditCmdState(focus)
        toolBarButtons.cut.Enable(canCut)
        toolBarButtons.copy.Enable(canCopy)
        toolBarButtons.paste.Enable(canPaste)
        
        
    def AddDialog(self, dialog):
        self.openDialogs.append(dialog)
        dialog.Bind(wx.EVT_WINDOW_DESTROY, self.OnDialogDestroy)
        self.SetWindowStyleFlag(~(wx.MINIMIZE_BOX|wx.CLOSE_BOX) & self.style)
        
        
    @eg.LogIt
    def OnDialogDestroy(self, event):
        dialog = event.GetWindow()
        try:
            self.openDialogs.remove(dialog)
        except:
            pass
        if len(self.openDialogs) == 0:
            self.SetWindowStyleFlag(self.style)
    

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
        menuState.addEvent = bool(selection.DropTest(EventItem))
        menuState.addAction = not isFolder
        menuState.configure = selection.isConfigurable
        menuState.execute = selection.isExecutable and selection.isEnabled
        menuState.rename = selection.isRenameable
        menuState.disabled = selection.isDeactivatable
        
        toolBarButton = self.toolBar.buttons
        canCut, canCopy, canPaste, canDelete =\
            self.GetEditCmdState(self.lastFocus)
        toolBarButton.cut.Enable(canCut)
        toolBarButton.copy.Enable(canCopy)
        toolBarButton.paste.Enable(canPaste)
        toolBarButton.addAction.Enable(menuState.addAction)
        toolBarButton.addEvent.Enable(menuState.addEvent)
        toolBarButton.disabled.Enable(menuState.disabled)
        toolBarButton.execute.Enable(menuState.execute)
        
    
    def OnUndoEvent(self, hasUndos, hasRedos, undoName, redoName):
        undoName = Text.Menu.Undo + undoName
        redoName = Text.Menu.Redo + redoName
        for editMenu in self.editMenus:
            editMenu.undo.Enable(hasUndos)
            editMenu.undo.SetText(undoName)
            editMenu.redo.Enable(hasRedos)
            editMenu.redo.SetText(redoName)
        
        
    @eg.LogIt
    def SetupEditMenu(self, menuItems):
        canCut, canCopy, canPaste, canDelete =\
            self.GetEditCmdState(self.lastFocus)
        menuItems.cut.Enable(canCut)
        menuItems.copy.Enable(canCopy)
        menuItems.paste.Enable(canPaste)
        menuItems.delete.Enable(canDelete)
        menuState = self.menuState
        menuItems.addAction.Enable(menuState.addAction)
        menuItems.addEvent.Enable(menuState.addEvent)
        menuItems.configure.Enable(menuState.configure)
        menuItems.execute.Enable(menuState.execute)
        menuItems.rename.Enable(menuState.rename)
        menuItems.disabled.Enable(menuState.disabled)
        menuItems.disabled.Check(
            self.document.selection and not self.document.selection.isEnabled
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
            start, end = editCtrl.GetSelection()
            if end - start == 0:
                end += 1
            editCtrl.Remove(start, end)
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
    
    def OnCmdNew(self, event):
        self.document.New()


    def OnCmdOpen(self, event):
        self.document.Open()
        
        
    def OnCmdSave(self, event):
        self.document.Save()


    def OnCmdSaveAs(self, event):
        self.document.SaveAs()


    def OnCmdExport(self, event):
        result = eg.ExportDialog.GetModalResult()
        if result is not None:
            for item in result[0][0]:
                print item.GetLabel()


    def OnCmdImport(self, event):
        pass
    
    
    @eg.AsGreenlet
    def OnCmdOptions(self, event):
        if not self.optionsDialog:
            self.optionsDialog = eg.OptionsDialog.Create(self)
            while self.optionsDialog.GetResult() is not None:
                pass
        else:
            self.optionsDialog.Raise()
            
        
    def OnCmdExit(self, event):
        eg.app.Exit()
        
        
    def OnCmdUndo(self, event):
        self.document.Undo()
            
            
    def OnCmdRedo(self, event):
        self.document.Redo()
        
    
    def OnCmdCut(self, event):
        self.DispatchCommand("Cut", event)
        
        
    def OnCmdCopy(self, event):
        self.DispatchCommand("Copy", event)
            
            
    def OnCmdPaste(self, event):
        self.DispatchCommand("Paste", event)
    
    
    def OnCmdDelete(self, event):
        self.DispatchCommand("Clear", event)
                
                
    def OnCmdFind(self, event):
        if self.findDialog is None:
            self.findDialog = eg.FindDialog(self, self.document)
        self.findDialog.Show()
        
        
    def OnCmdFindNext(self, event):
        if (
            self.findDialog is None 
            or not self.findDialog.searchButton.IsEnabled()
        ):
            self.OnCmdFind(event)
        else:
            self.findDialog.OnFindButton()
        

    def OnCmdAddPlugin(self, event):
        result = eg.AddPluginDialog.GetModalResult(self)
        if result is None:
            return
        pluginInfo = result[0][0]
        if pluginInfo is None:
            return
        eg.Greenlet(eg.UndoHandler.NewPlugin().Do).switch(self.document, pluginInfo)
            
            
    def OnCmdAddEvent(self, event):
        eg.UndoHandler.NewEvent().Do(self.document)
                
                
    def OnCmdAddFolder(self, event):
        eg.UndoHandler.NewFolder().Do(self.document)
        
    
    def OnCmdAddMacro(self, event):
        eg.UndoHandler.NewMacro().Do(self.document)
        
    
    def OnCmdAddAction(self, event):
        # let the user choose an action
        result = eg.AddActionDialog.GetModalResult(self)
        # if user canceled the dialog, take a quick exit
        if result is None:
            return None
        action = result[0][0]
        eg.Greenlet(eg.UndoHandler.NewAction().Do).switch(self.document, action)
        
    
    def OnCmdRename(self, event):
        self.treeCtrl.SetFocus()
        self.treeCtrl.EditLabel(self.treeCtrl.GetSelection())


    def OnCmdConfigure(self, event):
        eg.UndoHandler.Configure().Try(self.document)


    def OnCmdExecute(self, event):
        self.document.ExecuteSelected().SetShouldEnd()


    def OnCmdDisabled(self, event):
        eg.UndoHandler.ToggleEnable(self.document)


    def OnCmdHideShowToolbar(self, event):
        config.showToolbar = not config.showToolbar
        #self.auiManager.GetPane("toolBar").Show(config.showToolbar)
        #self.auiManager.Update()
        self.toolBar.Show(config.showToolbar)
        self.Layout()
        self.SendSizeEvent()


    def OnCmdLogMacros(self, event):
        eg.config.logMacros = not eg.config.logMacros
        self.menuBar.View.logMacros.Check(eg.config.logMacros)
        
        
    def OnCmdLogActions(self, event):
        eg.config.logActions = not eg.config.logActions
        self.menuBar.View.logActions.Check(eg.config.logActions)
        
        
    def OnCmdExpandOnEvents(self, event):
        config.expandOnEvents = not config.expandOnEvents
        self.menuBar.View.expandOnEvents.Check(config.expandOnEvents)
        self.menuBar.View.expandTillMacro.Enable(config.expandOnEvents)
        self.UpdateViewOptions()
        
        
    def OnCmdExpandTillMacro(self, event):
        config.expandTillMacro = not config.expandTillMacro
        self.menuBar.View.expandTillMacro.Check(config.expandTillMacro)
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
    
    
    @eg.AsGreenlet
    def OnCmdAbout(self, event):
        if self.aboutDialog is None:
            self.aboutDialog = eg.AboutDialog.Create(self)
            self.aboutDialog.GetResult()
            self.aboutDialog = None
        else:
            self.aboutDialog.Raise()

    
        
    #----- debugging and experimental stuff that will be removed someday -----
    
    def OnCmdReload(self, event):
        if self.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            return wx.ID_CANCEL
        self.document.StartSession(self.document.filePath)
    
    
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
        eg.eventThread.ClearPendingEvents()
        eg.actionThread.ClearPendingEvents()
        eg.PrintError("Execution stopped by user")
        
    
    #@eg.AsGreenlet
    def OnCmdAddEventDialog(self, event):
        frame = eg.TestFrame()
        return
        dialog = eg.AddEventDialog.Create(self)
        while True:
            result = dialog.GetResult()
            if result is None:
                break
            label = result[0][0]
            eg.UndoHandler.NewEvent().Do(self.document, label)
        #eg.AddEventDialog.GetModalResult(self)
        #eg.NamespaceTree.Test()

        
