import os
import sys
import gc

import wx
import wx.aui

import eg
from Document import Document
from eg import (
    EventItem, 
    ActionItem, 
    MacroItem,
    FolderItem, 
    RootItem, 
)
from eg.IconTools import GetIcon
from eg.WinAPI.Utils import BringHwndToFront

PLUGIN_ICON = GetIcon('images/plugin.png')
FOLDER_ICON = GetIcon('images/folder.png')
MACRO_ICON = GetIcon('images/macro.png')
EVENT_ICON = GetIcon('images/event.png')
ACTION_ICON = GetIcon('images/action.png')
RESET_ICON = GetIcon('images/error.png')

Text = eg.text.MainFrame


    
def ExecuteSelectedTreeItem():
    item = eg.treeCtrl.document.selection
    event = eg.EventGhostEvent("OnCmdExecute")
    eg.actionThread.Call(eg.actionThread.ExecuteTreeItem, item, event)
    return event

    
class ExecuteButton(wx.Button):
    
    def __init__(self, parent):
        id = wx.NewId()
        wx.Button.__init__(
            self, 
            parent, 
            id, 
            Text.Menu.Execute, 
            style=wx.NO_BORDER
        )
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.egEvent = None
        
        
    def OnLeftDown(self, event):
        self.egEvent = ExecuteSelectedTreeItem()
        event.Skip()
        
        
    def OnLeftUp(self, event):
        self.egEvent.SetShouldEnd()
        event.Skip()
        
        
        
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
        
    def __init__(self, parent=None):
        """ Create the MainFrame """
        text = eg.text
        self.document = document = Document()
        self.menuState = eg.Bunch()
        wx.Frame.__init__(
            self, 
            parent, 
            -1,
            eg.APP_NAME,
            pos=config.position,
            size=(1,1),
            style=wx.MINIMIZE_BOX
                |wx.MAXIMIZE_BOX
                |wx.RESIZE_BORDER
                |wx.SYSTEM_MENU
                |wx.CAPTION
                |wx.CLOSE_BOX
                |wx.CLIP_CHILDREN
                |wx.TAB_TRAVERSAL
        )
        from MainLogger import LoggerCtrl
        logCtrl = LoggerCtrl(self)
        
        from MainTree import TreeCtrl
        treeCtrl = TreeCtrl(self, document=self.document)
        self.document.SetTree(treeCtrl)
        
        def UpdateTitle(filePath):
            if filePath is None:
                title = eg.text.General.unnamedFile
            else:
                title = os.path.basename(filePath)
            self.SetTitle("EventGhost %s - %s" % (eg.versionStr, title))
        document.filePath.addCallback(UpdateTitle)
        #UpdateTitle(document.filePath.get())
        
        self.treeCtrl = treeCtrl
        self.logCtrl = logCtrl
        
        self.inProcessing = False
        self.iconState = 0
        self.findDialog = None
        
        
        def DocumentBind(item, dataset):
            item.Enable(dataset.get())
            dataset.addCallback(item.Enable)
        
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
        AddItem("Disabled", func=treeCtrl.ToggleEnable)
        AddItem()
        
        def OnLeftDown(event):
            self.egEvent = ExecuteSelectedTreeItem()
            event.Skip()
            
        def OnLeftUp(event):
            self.egEvent.SetShouldEnd()
            event.Skip()
        AddItem("Execute", downFunc=OnLeftDown, upFunc=OnLeftUp)
        #button = ExecuteButton(toolBar)
        #toolBar.AddControl(button)
        #setattr(toolBar.buttons, "Execute", button)
       
        #spacer = wx.Control(toolBar, size=(10,1))
        #toolBar.AddControl(spacer)
        
        if eg._debug:
            self.toolBarSpacer = wx.Control(toolBar, size=(50,1))
            toolBar.AddControl(self.toolBarSpacer)
        
            AddItem("Reset", image=RESET_ICON)
            #AddItem("Test", image=RESET_ICON)

        toolBar.Realize()
        self.SetToolBar(toolBar)
        self.SetMinSize((400, 200))
        
        # statusbar
        self.statusBar = eg.StatusBar(self)
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
        if eg._debug:
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
#        AddItem()
#        AddItem("AddPlugin", image=PLUGIN_ICON)
#        AddItem("NewFolder", image=FOLDER_ICON)
#        AddItem("NewMacro", image=MACRO_ICON)
#        AddItem("NewEvent", image=EVENT_ICON)
#        AddItem("NewAction", image=ACTION_ICON)
#        AddItem()
#        AddItem("Edit", hotkey="Return")
#        AddItem("Rename", hotkey="F2")
#        AddItem("Execute", hotkey="F5")
#        AddItem()
#        AddItem(
#            "Disabled", 
#            kind=wx.ITEM_CHECK, 
#            hotkey="Ctrl+D", 
#            func=treeCtrl.ToggleEnable
#        )

        # view menu        
        viewMenu = menuBar.AddMenu("View")
        AddItem = viewMenu.AddItem
        AddItem(
            "HideShowToolbar", 
            kind=wx.ITEM_CHECK
        ).Check(config.showToolbar)
        AddItem()
        AddItem("ExpandAll", func=treeCtrl.ExpandAll)
        AddItem("CollapseAll", func=treeCtrl.CollapseAll)
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
            func=treeCtrl.ToggleEnable
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
        if eg._debug:
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
        popupMenuItems.disableItem = AddItem("Disabled", 
            kind=wx.ITEM_CHECK, 
            func=treeCtrl.ToggleEnable
        )

        self.SetIcon(eg.app.taskBarIcon.stateIcons[0])
        
        if not config.logTime:
            logCtrl.SetTimeLogging(False)
            
        self.editMenus = (toolBar.buttons, editMenu, popupMenu)
        self.lastFocus = "None"
        self.focusEvent = eg.EventHook()
        
        Bind = logCtrl.Bind
        def OnLogSetFocus(event):
            eg.whoami()
            self.focusEvent.Fire("Log")
            event.Skip()
        Bind(wx.EVT_SET_FOCUS, OnLogSetFocus)
        def OnLogKillFocus(event):
            eg.whoami()
            self.focusEvent.Fire("None")
            event.Skip()
        Bind(wx.EVT_KILL_FOCUS, OnLogKillFocus)
        
        
        Bind = treeCtrl.Bind
        def OnTreeSetFocus(event):
            eg.whoami()
            self.focusEvent.Fire("Tree")
            event.Skip()
        Bind(wx.EVT_SET_FOCUS, OnTreeSetFocus)
        def OnTreeKillFocus(event):
            eg.whoami()
            if not self.treeCtrl.isInEditLabel:
                self.focusEvent.Fire("None")
            event.Skip()
        Bind(wx.EVT_KILL_FOCUS, OnTreeKillFocus)

        Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        
        Bind = self.Bind
        Bind(wx.EVT_ICONIZE, self.OnIconize)
        Bind(wx.EVT_MENU_OPEN, self.OnMenuOpen)
        Bind(wx.EVT_CLOSE, self.OnCloseEvent)
        Bind(wx.EVT_SIZE, self.OnSize)
        Bind(wx.EVT_MOVE, self.OnMove)
        Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        Bind(wx.aui.EVT_AUI_PANE_MAXIMIZE, self.OnPaneMaximize)
        Bind(wx.aui.EVT_AUI_PANE_RESTORE, self.OnPaneRestore)
        self.UpdateViewOptions()
        self.SetSize(config.size)
        document.undoEvent.Bind(self.OnUndoEvent)
        document.selectionEvent.Bind(self.OnTreeSelectionEvent)
        
        # tell FrameManager to manage this frame
        auiManager = wx.aui.AuiManager()
        auiManager.SetManagedWindow(self)
        self.auiManager = auiManager

#        self.toolBarPane = (wx.aui.AuiPaneInfo().
#                Name("toolBar").
#                Caption("Toolbar").
#                ToolbarPane().
#                Top().
#                RightDockable(False).
#                LeftDockable(False)
#        )
#        auiManager.AddPane(toolBar, self.toolBarPane)
#        
        auiManager.AddPane(
            logCtrl, 
            wx.aui.AuiPaneInfo().
                Name("logger").
                Left().
                MinSize((280,300)).
                MaximizeButton(True).
                CloseButton(False)
        )
        
        auiManager.AddPane(
            treeCtrl, 
            wx.aui.AuiPaneInfo().
                Name("tree").
                #CaptionVisible().
                #CenterPane().
                Center().
                MinSize((100,100)).
                Floatable(True).
                Dockable(True).
                MaximizeButton(True).
                CloseButton(False)
        )
        
        if (
            eg.config.buildNum == eg.buildNum 
            and config.perspective is not None
        ):
            auiManager.LoadPerspective(config.perspective, False)
        auiManager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_PANE_BORDER_SIZE, 0)

        auiManager.GetPane("logger").Caption(" " + Text.Logger.caption)
        auiManager.GetPane("tree").Caption(" " + Text.Tree.caption)
        toolBar.Show(config.showToolbar)
        auiManager.Update()
        auiManager.GetPane("logger").MinSize((100,100))
        self.focusEvent.Bind(self.OnFocusChange)
        treeCtrl.SetFocus()
        eg.app.clipboardEvent.Bind(self.OnClipboardChange)
        

    def OnPaneClose(self, event):
        """ 
        React to a wx.aui.EVT_AUI_PANE_CLOSE event.
        
        Monitors if the toolbar gets closed and updates the check menu
        entry accordingly
        """
        if event.GetPane().name == "toolBar":
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
        
        
    def OnAutoLoad(self, filename):
        tree = self.treeCtrl
        tree.Freeze()
        try:
            root = self.document.Load(filename)
            selectItem = root
            firstItem = root
            treeStateData = config.treeStateData
            if (
                treeStateData 
                and treeStateData.guid == root.guid
                and treeStateData.time == root.time
            ):
                tree.SetExpandState(treeStateData.state)
                try:
                    for pos in treeStateData.selected:
                        selectItem = selectItem.childs[pos]
                except:
                    selectItem = root
                    
                if hasattr(treeStateData, "first"):
                    try:
                        for pos in treeStateData.first:
                            firstItem = firstItem.childs[pos]
                    except:
                        firstItem = root
            root.CreateTreeItem(tree, None)
            tree.Expand(root.id)
            selectItem.Select()
            if firstItem.id is not None:
                tree.ScrollTo(firstItem.id)
        finally:
            tree.Thaw()
        
        
    def OnSize(self, event):
        """ Handle wx.EVT_SIZE """
        if not self.IsMaximized() and self.IsShown():
            config.size = self.GetSizeTuple()
        event.Skip()


    def OnMove(self, event):
        """ Handle wx.EVT_MOVE """
        if not (self.IsMaximized() or self.IsIconized()) and self.IsShown():
            config.position = self.GetPositionTuple()
        event.Skip()
        
        
    def OnCloseEvent(self, event):
        '''Handle wx.EVT_CLOSE'''
        eg.whoami()
        if config.hideOnClose and event.CanVeto() and self.IsShown():
            eg.notice("calling Veto")
            event.Veto()
            self.Show(False)
            wx.GetApp().ProcessIdle()
        else:
            if self.OnClose(event) != wx.ID_CANCEL:
                eg.app.Exit()


    def OnClose(self, event=None):
        eg.whoami()
        res = self.CheckFileNeedsSave()
        if res == wx.ID_CANCEL:
            eg.notice("Skipping event in OnClose")
            if event:
                event.Skip(False)
            return wx.ID_CANCEL
        #eg.notice("Binding close dummy")
        #self.Bind(wx.EVT_CLOSE, self.CloseDummy)
        eg.config.hideOnStartup = self.IsIconized()
        eg.config.autoloadFilePath = self.document.filePath.get()
        config.perspective = self.auiManager.SavePerspective()
        if res in (wx.ID_OK, wx.ID_YES):
            tree = self.treeCtrl
            item = self.document.selection
            firstItem = tree.GetPyData(tree.GetFirstVisibleItem())
            class data:
                guid = tree.root.guid
                time = tree.root.time
                state = tree.GetExpandState()
                selected = item.GetPath() if item else None
                first = firstItem.GetPath()
            config.treeStateData = data
        return None
        

    def OnIconize(self, event):
        if event.Iconized:
            self.Show(False)
            event.Skip(True)
        else:
            self.Iconize(False)
            self.Show(True)
            self.Raise()
            self.GetFocus()
        self.UpdateViewOptions()
        wx.GetApp().ProcessIdle()


    def BringToFront(self):
        self.Iconize(False)
        self.Show(True)
        self.Raise()
        BringHwndToFront(self.GetHandle())
        
        
    def OnRightClick(self, event):
        self.treeCtrl.EndEditLabel(self.treeCtrl.GetSelection(), False)
        # seems like newer wxPython doesn't select the item on right-click
        # so we have to do it ourself
        pos = event.GetPosition()
        id, flags = self.treeCtrl.HitTest(pos)
        self.treeCtrl.SelectItem(id)
        

    def OnRightUp(self, event):
        self.treeCtrl.SetFocus()
        self.SetupEditMenu(self.popupMenuItems)
        self.treeCtrl.PopupMenu(self.popupMenu)


    def CheckFileNeedsSave(self):
        """
        Checks if the file was changed and if necessary asks the user if he 
        wants to save it. If the user affirms, calls Save/SaveAs also.
        
        returns: wx.ID_OK     if no save was needed
                 wx.ID_YES    if file was saved
                 wx.ID_NO     if file was not saved
                 wx.ID_CANCEL if user canceled posssible save
        """
        if not self.document.isDirty.get():
            return wx.ID_OK
        dialog = wx.MessageDialog(
            self,
            Text.SaveChanges.mesg, 
            eg.APP_NAME + ": " + Text.SaveChanges.title, 
            style = wx.YES_DEFAULT
                |wx.YES_NO
                |wx.CANCEL
                |wx.STAY_ON_TOP
                |wx.ICON_EXCLAMATION
        )
        res = dialog.ShowModal()
        dialog.Destroy()
        if res == wx.ID_CANCEL:
            return wx.ID_CANCEL
        if res == wx.ID_YES:
            return self.OnCmdSave()
        return wx.ID_NO
            
             
    def OnClipboardChange(self):
        eg.whoami()
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
        
        
    def GetEditCmdState(self, focus):
        if focus == "Edit":
            return (True, True, True, True)
        elif focus == "Log":
            return (False, True, False, False)
        elif focus == "Tree" and self.document.selection:
            selection = self.document.selection
            return (
                selection.CanCut(), 
                selection.CanCopy(), 
                selection.CanPaste(), 
                selection.CanDelete()
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
        
        tbb = self.toolBar.buttons
        tbb.NewAction.Enable(menuState.newAction)
        tbb.NewEvent.Enable(menuState.newEvent)
        tbb.Execute.Enable(menuState.execute)
        canCut, canCopy, canPaste, canDelete =\
            self.GetEditCmdState(self.lastFocus)
        tbb.Cut.Enable(canCut)
        tbb.Copy.Enable(canCopy)
        tbb.Paste.Enable(canPaste)
        
    
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
        menuItems.disableItem.Check(not self.document.selection.isEnabled)
        
        
    def OnMenuOpen(self, event):
        self.SetupEditMenu(self.menuItems)            
            
            
    def UpdateViewOptions(self):
        expandOnEvents = (
            not self.IsIconized()
            and config.expandOnEvents 
            and not self.treeCtrl.isInEditLabel
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
        if self.CheckFileNeedsSave() == wx.ID_CANCEL:
            return
        eg.eventThread.CallWait(eg.eventThread.StopSession)
        self.treeCtrl.DeleteAllItems()
        eg.eventThread.Call(eg.eventThread.StartSession, None)


    def OnCmdOpen(self, event):
        """ Handle the menu command 'Open'. """
        if self.CheckFileNeedsSave() == wx.ID_CANCEL:
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
        if self.document.filePath.get() is None:
            return self.OnCmdSaveAs()
        self.document.Save()
        return wx.ID_YES


    def OnCmdSaveAs(self, event=None):
        """ Handle the menu command 'Save As'. """
        dlg = wx.FileDialog(
            self, 
            message="", 
            wildcard="*.xml", 
            style=wx.SAVE|wx.OVERWRITE_PROMPT
        )
        res = dlg.ShowModal()
        if res == wx.ID_CANCEL:
            return res
        filePath = dlg.GetPath()
        dlg.Destroy()
        self.document.Save(filePath)
        return wx.ID_YES


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
        if self.OnClose(event) != wx.ID_CANCEL:
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
        import gc
        gc.collect()
                
                
    def OnCmdFind(self, event):
        """ Handle the menu command 'Find'. """
        if self.findDialog is None:
            from Dialogs.FindDialog import FindDialog
            self.findDialog = FindDialog(self)
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
        ExecuteSelectedTreeItem().SetShouldEnd()


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
        flag = self.menuBar.View.LogTime.IsChecked()
        config.logTime = flag
        self.logCtrl.SetTimeLogging(flag)
    
    
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
        #gc.set_debug(gc.DEBUG_LEAK)
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
        from eg.Dialogs import LinkListDialog
        reload(LinkListDialog)
        dialog = LinkListDialog.LinkListDialog(self)
        dialog.ShowModal()
        dialog.Destroy()