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

# Local imports
import eg

KIND_TAGS = ["other", "remote", "program", "external"]

class Config(eg.PersistentData):
    position = None
    size = (640, 450)
    splitPosition = 240
    lastSelection = None
    collapsed = set()


class Text(eg.TranslatableStrings):
    title = "Add Plugin..."
    noInfo = "No information available."
    noMultiloadTitle = "No multiload possible"
    noMultiload = (
        "This plugin doesn't support multiload and you already have one "
        "instance of this plugin in your configuration."
    )
    otherPlugins = "General Plugins"
    remotePlugins = "Input Devices"
    programPlugins = "Software Control"
    externalPlugins = "Hardware Control"
    author = "Author:"
    version = "Version:"
    descriptionBox = "Description"


class AddPluginDialog(eg.TaskletDialog):
    instance = None

    def CheckMultiload(self):
        if not self.checkMultiLoad:
            return True
        info = self.resultData
        if not info:
            return True
        if info.canMultiLoad:
            return True
        if any((plugin.info.path == info.path) for plugin in eg.pluginList):
            eg.MessageBox(
                Text.noMultiload,
                Text.noMultiloadTitle,
                style=wx.ICON_EXCLAMATION
            )
            return False
        else:
            return True

    @eg.LogItWithReturn
    def Configure(self, parent, checkMultiLoad=True, title=None):
        if title is None:
            title = Text.title
        self.checkMultiLoad = checkMultiLoad
        if self.__class__.instance:
            self.__class__.instance.Raise()
            return
        self.__class__.instance = self

        self.resultData = None

        eg.TaskletDialog.__init__(
            self,
            parent,
            -1,
            title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )

        splitterWindow = wx.SplitterWindow(
            self,
            style=(
                wx.SP_LIVE_UPDATE |
                wx.CLIP_CHILDREN |
                wx.NO_FULL_REPAINT_ON_RESIZE
            )
        )

        self.treeCtrl = treeCtrl = wx.TreeCtrl(
            splitterWindow,
            style=(
                wx.TR_SINGLE |
                wx.TR_HAS_BUTTONS |
                wx.TR_HIDE_ROOT |
                wx.TR_LINES_AT_ROOT
            )
        )

        treeCtrl.SetMinSize((170, 200))

        imageList = wx.ImageList(16, 16)
        imageList.Add(eg.Icons.PLUGIN_ICON.GetBitmap())
        imageList.Add(eg.Icons.FOLDER_ICON.GetBitmap())
        treeCtrl.SetImageList(imageList)

        root = treeCtrl.AddRoot("")
        typeIds = {
            KIND_TAGS[0]: treeCtrl.AppendItem(
                root, getattr(Text, KIND_TAGS[0] + "Plugins"), 1
            ),
            KIND_TAGS[1]: treeCtrl.AppendItem(
                root, getattr(Text, KIND_TAGS[1] + "Plugins"), 1
            ),
            KIND_TAGS[2]: treeCtrl.AppendItem(
                root, getattr(Text, KIND_TAGS[2] + "Plugins"), 1
            ),
            KIND_TAGS[3]: treeCtrl.AppendItem(
                root, getattr(Text, KIND_TAGS[3] + "Plugins"), 1
            ),
        }
        self.typeIds = typeIds
        itemToSelect = typeIds[KIND_TAGS[0]]

        for info in eg.pluginManager.GetPluginInfoList():
            if info.kind in ("hidden", "core"):
                continue
            if info.icon and info.icon != eg.Icons.PLUGIN_ICON:
                idx = imageList.Add(
                    eg.Icons.PluginSubIcon(info.icon).GetBitmap()
                )
            else:
                idx = 0

            treeId = treeCtrl.AppendItem(typeIds[info.kind], info.name, idx)
            if not info.valid:
                treeCtrl.SetItemTextColour(treeId, eg.colour.pluginError)
            treeCtrl.SetPyData(treeId, info)
            if info.path == Config.lastSelection:
                itemToSelect = treeId

        for kind, treeId in typeIds.iteritems():
            if kind in Config.collapsed:
                treeCtrl.Collapse(treeId)
            else:
                treeCtrl.Expand(treeId)

        treeCtrl.ScrollTo(itemToSelect)

        def OnCmdExport(dummyEvent=None):
            info = self.treeCtrl.GetPyData(self.treeCtrl.GetSelection())
            if info:
                eg.PluginInstall.Export(info)
        menu = wx.Menu()
        menuId = wx.NewId()
        menu.Append(menuId, eg.text.MainFrame.Menu.Export)
        self.Bind(wx.EVT_MENU, OnCmdExport, id=menuId)
        self.contextMenu = menu
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemRightClick)

        rightPanel = wx.Panel(splitterWindow)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightPanel.SetSizer(rightSizer)

        self.nameText = nameText = wx.StaticText(rightPanel)
        nameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        rightSizer.Add(nameText, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)

        subSizer = wx.FlexGridSizer(2, 2)
        self.authorLabel = wx.StaticText(rightPanel, label=Text.author)
        subSizer.Add(self.authorLabel)
        self.authorText = wx.StaticText(rightPanel)
        subSizer.Add(self.authorText, 0, wx.EXPAND | wx.LEFT, 5)
        self.versionLabel = wx.StaticText(rightPanel, label=Text.version)
        subSizer.Add(self.versionLabel)
        self.versionText = wx.StaticText(rightPanel)
        subSizer.Add(self.versionText, 0, wx.EXPAND | wx.LEFT, 5)
        rightSizer.Add(subSizer, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)

        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label=Text.descriptionBox)
        )

        self.descrBox = eg.HtmlWindow(rightPanel)
        staticBoxSizer.Add(self.descrBox, 1, wx.EXPAND)

        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND | wx.LEFT, 5)

        splitterWindow.SplitVertically(self.treeCtrl, rightPanel)
        splitterWindow.SetMinimumPaneSize(60)
        splitterWindow.SetSashGravity(0.0)
        splitterWindow.UpdateSize()

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL), True)
        self.okButton = self.buttonRow.okButton
        self.okButton.Enable(False)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitterWindow, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(mainSizer)
        #minSize = mainSizer.GetMinSize()
        #self.SetMinSize(minSize)
        self.SetSize(Config.size)
        splitterWindow.SetSashPosition(Config.splitPosition)
        if Config.position:
            self.SetPosition(Config.position)
        treeCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        treeCtrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        treeCtrl.SelectItem(itemToSelect)


# -------- This code is for setting the use GUID instead of XmlIdLink ---------
        self.click_count = 0

        def on_left_down(evt):
            x, y = evt.GetPosition()
            width, height = self.GetClientSize()

            start_x = width - 20
            stary_y = 0

            stop_x = start_x + 20
            stop_y = stary_y + 20

            if stop_x > x > start_x and stop_y > y > stary_y:
                if not self.click_count:
                    self.CaptureMouse()

            start_x = 0
            stary_y = height - 20

            stop_x = start_x + 20
            stop_y = stary_y + 20

            if stop_x > x > start_x and stop_y > y > stary_y:
                if self.click_count:
                    self.CaptureMouse()

            evt.Skip()

        def on_left_up(evt):
            if self.HasCapture():

                self.ReleaseMouse()
                self.click_count += 1

                if self.click_count == 2:
                    self.click_count = 0
                    dialog = eg.MessageDialog(
                        parent=None,
                        message=(
                            'Warning: This process cannot be undone so make\n'
                            '                  a backup copy of your save file now.\n\n'
                            'This process will modify and save all EventGhost Data!!\n'
                            'Enable using GUID\'s?\n\n'
                        ),
                        style=wx.YES_NO | wx.STAY_ON_TOP
                    )
                    if dialog.ShowModal() == wx.ID_YES:
                        eg.useTreeItemGUID = True
                        eg.document.SetIsDirty(True)
                        eg.document.Save()
                        eg.config.Save()

                    dialog.Destroy()

            evt.Skip()

        if eg.useTreeItemGUID is False:
            self.Bind(wx.EVT_LEFT_DOWN, on_left_down)
            self.Bind(wx.EVT_LEFT_UP, on_left_up)

# -----------------------------------------------------------------------------

        while self.Affirmed():
            if self.CheckMultiload():
                self.SetResult(self.resultData)
        Config.size = self.GetSizeTuple()
        Config.position = self.GetPositionTuple()
        Config.splitPosition = splitterWindow.GetSashPosition()
        Config.collapsed = set(
            kind for kind, treeId in typeIds.iteritems()
            if not treeCtrl.IsExpanded(treeId)
        )
        self.__class__.instance = None

    def OnItemActivated(self, event):
        item = self.treeCtrl.GetSelection()
        info = self.treeCtrl.GetPyData(item)
        if info is not None:
            #self.SetResult("huhu")
            self.OnOK(wx.CommandEvent())
            return
        event.Skip()

    def OnItemRightClick(self, event):
        """
        Handles wx.EVT_TREE_ITEM_RIGHT_CLICK events.
        """
        item = event.GetItem()
        self.treeCtrl.SelectItem(item)
        info = self.treeCtrl.GetPyData(item)
        if info:
            self.PopupMenu(self.contextMenu)

    def OnSelectionChanged(self, event):
        """
        Handle the wx.EVT_TREE_SEL_CHANGED events.
        """
        item = event.GetItem()
        self.resultData = info = self.treeCtrl.GetPyData(item)
        if info is None:
            name = self.treeCtrl.GetItemText(item)
            description = Text.noInfo
            self.authorLabel.SetLabel("")
            self.authorText.SetLabel("")
            self.versionLabel.SetLabel("")
            self.versionText.SetLabel("")
            self.okButton.Enable(False)
            event.Skip()
        else:
            name = info.name
            description = info.description
            self.descrBox.SetBasePath(info.path)
            self.authorLabel.SetLabel(Text.author)
            self.authorText.SetLabel(info.author.replace("&", "&&"))
            self.versionLabel.SetLabel(Text.version)
            self.versionText.SetLabel(info.version)
            self.okButton.Enable(True)
        self.nameText.SetLabel(name)
        url = info.url if info else None
        self.descrBox.SetPage(eg.Utils.AppUrl(description, url))
