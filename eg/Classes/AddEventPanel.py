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
import wx.lib.agw.supertooltip as STT
from wx._core import PyDeadObjectError

import eg


Text = eg.text.EventDialog


class Config(eg.PersistentData):
    lastSelected = None


class AddEventPanel(eg.Panel):
    def __init__(self, parent, editName=""):
        super(AddEventPanel, self).__init__(parent=parent)

        self.parent = parent

        self.splitterWindow = splitterWindow = wx.SplitterWindow(
            self,
            -1,
            style=(
                wx.SP_LIVE_UPDATE |
                wx.CLIP_CHILDREN |
                wx.NO_FULL_REPAINT_ON_RESIZE
            )
        )

        leftPanel = eg.Panel(splitterWindow)
        self.tree = tree = wx.TreeCtrl(
            leftPanel, -1,
            style=wx.TR_DEFAULT_STYLE |
            wx.TR_HIDE_ROOT |
            wx.TR_FULL_ROW_HIGHLIGHT
        )
        tree.SetMinSize((100, 100))
        tree.SetImageList(eg.Icons.gImageList)

        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnStartDrag)
        tree.Bind(wx.EVT_SET_FOCUS, self.OnFocusTree)

        userEventLabel = wx.StaticText(
            leftPanel,
            label="{0}:".format(Text.userEventLabel)
        )
        userEventLabel.SetToolTip(wx.ToolTip(Text.userEventTooltip))

        self.eventName = eventName =wx.TextCtrl(
            leftPanel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER
        )
        eventName.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
        eventName.Bind(wx.EVT_SET_FOCUS, self.OnFocusUserEvent)
        eventName.Bind(wx.EVT_TEXT, self.OnText)
        eventName.SetToolTip(wx.ToolTip(Text.userEventTooltip))

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(tree, 1, wx.EXPAND)
        leftSizer.Add(userEventLabel, 0, wx.TOP, 5)
        leftSizer.Add(eventName, 0, wx.EXPAND)
        leftPanel.SetSizer(leftSizer)
        leftPanel.SetToolTip(wx.ToolTip(Text.userEventTooltip))

        rightPanel = self.rightPanel = eg.Panel(splitterWindow)
        rightSizer = self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightPanel.SetSizer(rightSizer)
        rightPanel.SetAutoLayout(True)

        self.nameText = nameText = wx.StaticText(rightPanel)
        nameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))

        rightSizer.Add(nameText, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)

        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label=Text.descriptionLabel),
            wx.VERTICAL
        )
        self.docText = eg.HtmlWindow(rightPanel)
        self.docText.SetBorders(2)

        staticBoxSizer.Add(self.docText, 1, wx.EXPAND)
        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND, 5)

        splitterWindow.SplitVertically(leftPanel, rightPanel)
        splitterWindow.SetMinimumPaneSize(120)
        splitterWindow.UpdateSize()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitterWindow, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(mainSizer)
        self.SetSizer(mainSizer)
        splitterWindow.SetSashPosition(220)

        self.resultData = ""
        self.GenerateEventlist()
        self.FillTree(self._allEventsData)

        if editName:
            eventName.ChangeValue(editName)
            item = self.FindEventItem(editName)
            if item.IsOk():
                tree.EnsureVisible(item)
                tree.SelectItem(item)
        else:
            self.ReselectLastSelected()
        eventName.SetInsertionPointEnd()
        wx.CallAfter(eventName.SetFocus)

    def GenerateEventlist(self):
        self._allEventsDict = eventDict = {Text.unknown: []}
        for e in eg.eventTable.keys():
            if "." not in e:
                eventDict[Text.unknown].append(e)
                continue
            parts = e.split(".", 1)
            if parts[0] in eventDict:
                eventDict[parts[0]].append(parts[1])
            else:
                eventDict[parts[0]] = ["*", parts[1]]

        self._allEventsData = allevents = {}
        for plugin in eg.pluginList:
            eventList = plugin.info.eventList
            prefix = plugin.info.eventPrefix
            if not eventList and prefix not in eventDict:
                continue

            allevents.update(
                {plugin.name: (
                    plugin.info.icon.folderIndex,
                    plugin.info,
                    {}  # events
                )}
            )

            for eventName, description in eventList:
                data = eg.EventInfo(eventName, description, plugin.info)
                allevents[plugin.name][2].update(
                    {eventName: (data.icon.index, data)}
                )
                try:
                    eventDict[prefix].remove(eventName)
                    if not eventDict[prefix]:
                        eventDict.pop(prefix)
                except ValueError:
                    pass

            if prefix in eventDict:
                for eventName in eventDict[prefix]:
                    data = eg.EventInfo(
                        eventName, Text.noDescription, plugin.info
                    )
                    allevents[plugin.name][2].update(
                        {eventName: (data.icon.index, data)}
                    )

        if not eventDict:
            return

        dummy_info = eg.PluginInstanceInfo()
        dummy_info.name = ""
        dummy_info.evalName = ""
        dummy_info.eventPrefix = ""
        dummy_info.description = Text.unknownDesc

        allevents.update(
            {Text.unknown: (
                eg.Icons.FOLDER_ICON._GetIndex(),
                dummy_info,
                {}  # events
            )}
        )

        for eventName in eventDict[Text.unknown]:
            allevents[Text.unknown][2].update(
                {eventName: (
                    eg.Icons.EVENT_ICON._GetIndex(),
                    eg.EventInfo(eventName, "", dummy_info)
                )}
            )

    def FillTree(self, eventlist):
        tree = self.tree
        tree.DeleteAllItems()
        self.root = tree.AddRoot("Functions")
        for plugin in sorted(eventlist):
            image, data, events = eventlist[plugin]
            item = tree.AppendItem(
                parent=self.root,
                text=plugin,
                image=image,
            )
            tree.SetPyData(item, data)

            for event in sorted(events):
                image, data = events[event]
                subitem = tree.AppendItem(
                    parent=item,
                    text=event,
                    image=image,
                )
                tree.SetPyData(subitem, data)

    def OnActivated(self, event):
        item = self.tree.GetSelection()
        if item.IsOk():
            data = self.tree.GetPyData(item)
            if isinstance(data, eg.EventInfo):
                Config.lastSelected = data.info.eventPrefix + "." + data.name
                self.resultData = Config.lastSelected
                self.parent.OnOK(event)

    def OnFocusTree(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk():
            return
        self.DoSelectionChanged(item)

    def OnFocusUserEvent(self, event):
        value = self.resultData
        self.eventName.ChangeValue(value)
        self.resultData = value
        event.Skip()

    def OnStartDrag(self, event):
        item = self.tree.GetPyData(event.GetItem())
        if item.info.pluginCls:
            text = item.info.eventPrefix + "." + item.name
        else:
            text = item.name
        # create our own data format and use it in a
        # custom data object
        customData = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        customData.SetData(text.encode("utf-8"))

        # And finally, create the drop source and begin the drag
        # and drop opperation
        dropSource = wx.DropSource(self)
        dropSource.SetData(customData)
        result = dropSource.DoDragDrop(wx.Drag_DefaultMove)
        if result == wx.DragMove:
            self.Refresh()

    def OnSelectionChanged(self, event):
        item = event.GetItem()
        self.DoSelectionChanged(item)
        event.Skip()

    def DoSelectionChanged(self, item):
        if not item.IsOk():
            return
        data = self.tree.GetPyData(item)
        if isinstance(data, eg.EventInfo):
            if data.info.eventPrefix:
                evt = data.info.eventPrefix + "." + data.name
            else:
                evt = data.name
            self.resultData = evt
            Config.lastSelected = evt
            path = data.info.path
            label = data.name
            desc = data.description
        elif isinstance(data, eg.PluginInstanceInfo):
            path = data.path
            label = data.name
            desc = data.description
            self.resultData = label
        else:
            path = ""
            label = ""
            desc = None
        self.eventName.ChangeValue(self.resultData)
        self.eventName.SetInsertionPointEnd()
        wx.CallAfter(self.SetFocusToTextCtrl)
        self.nameText.SetLabel(label)
        self.docText.SetBasePath(path)
        self.docText.SetPage(desc if desc else Text.noDescription)

    def SetFocusToTextCtrl(self):
        try:
            # It could happen that an event arrives after the dialog
            # has been closed. To avoid an error we use try/except here.
            self.eventName.SetFocus()
        except PyDeadObjectError:
            pass

    def OnText(self, evt):
        if not evt.GetEventObject().HasFocus():
            return
        self.resultData = value = evt.GetString()
        if not value:
            wx.CallAfter(self.FillTree, self._allEventsData)
            return

        values = [value.lower()]
        if "." in value:
            for v in value.split(".", 1):
                if v:
                    values.append(v.lower())

        allevts = self._allEventsData
        filtered = {}
        match = False
        label = Text.userEventLabel
        path = ""
        desc = Text.userEventTooltip

        for plugin in allevts:
            if len(values) < 3:
                if any(v in allevts[plugin][1].evalName.lower() for v in values):
                    filtered.update({plugin: allevts[plugin]})
                    continue

            events = allevts[plugin][2]
            for event in events:
                if any(v in event.lower() for v in values):
                    if any(v == event.lower() for v in values):
                        match = True
                        data = events[event][1]
                        if data.info.eventPrefix:
                            evt = data.info.eventPrefix + "." + data.name
                        else:
                            evt = data.name
                        self.resultData = evt
                        Config.lastSelected = evt
                        path = data.info.path
                        label = data.name
                        desc = data.description

                    if plugin not in filtered:
                        filtered.update(
                            {plugin: (
                                allevts[plugin][0],
                                allevts[plugin][1],
                                {event: (
                                    allevts[plugin][2][event][0],
                                    allevts[plugin][2][event][1]
                                )}
                            )}
                        )
                    else:
                        filtered[plugin][2].update(
                            {event: (
                                allevts[plugin][2][event][0],
                                allevts[plugin][2][event][1]
                            )}
                        )

        if not filtered:
            dummy_info = eg.PluginInstanceInfo()
            dummy_info.name = ""
            dummy_info.eventPrefix = ""
            dummy_info.description = Text.noMatch

            filtered = {Text.noMatch: (
                -1,
                dummy_info,
                {}  # events
            )}

        self.nameText.SetLabel(label if match else Text.userEventLabel)
        self.docText.SetBasePath(path if match else "")
        self.docText.SetPage(desc if match else Text.userEventTooltip)
        self.FillTree(filtered)
        self.tree.ExpandAllChildren(self.root)

    def OnTextEnter(self, event):
        value = event.GetString()
        if value:
            self.resultData = value
            Config.lastSelected = value
            #event.Skip()
            self.parent.OnOK(event)
        else:
            self.resultData = ""

    def ReselectLastSelected(self):
        if Config.lastSelected:
            item = self.FindEventItem(Config.lastSelected)
            if item.IsOk():
                self.tree.EnsureVisible(item)
                self.tree.SelectItem(item)

    def FindEventItem(self, searchText):
        if not searchText or "." not in searchText:
            return wx.TreeItemId()

        tree = self.tree
        parts = searchText.split(".", 1)
        plugin, event = parts[0], parts[1].lower()

        pluginItem = self.FindPluginItem(plugin)
        if not pluginItem.IsOk() or pluginItem is tree.GetRootItem():
            return wx.TreeItemId()

        item, cookie = tree.GetFirstChild(pluginItem)
        while item.IsOk():
            if tree.GetItemText(item).lower() == event:
                return item
            item, cookie = tree.GetNextChild(pluginItem, cookie)

        return wx.TreeItemId()

    def FindPluginItem(self, pluginName):
        plgName = pluginName.lower()
        tree = self.tree
        root = tree.GetRootItem()
        pluginItem, cookie = tree.GetFirstChild(root)
        while pluginItem.IsOk():
            data = tree.GetItemPyData(pluginItem)
            if data.evalName:
                if data.evalName.lower() == plgName:
                    break
            pluginItem, cookie = tree.GetNextChild(root, cookie)

        if pluginItem is tree.GetRootItem():
            return wx.TreeItemId()
        return pluginItem

