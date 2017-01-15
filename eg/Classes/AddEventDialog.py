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

import eg


class Config(eg.PersistentData):
    position = None
    size = (550, 400)
    splitPosition = 210
    lastSelected = None


class Text(eg.TranslatableStrings):
    title = "Add Event..."
    descriptionLabel = "Description"
    noDescription = "<i>No description available</i>"
    userEventLabel = "Search or manually enter event"
    userEvent = (
        "If an event is not in the list of available events,"
        " it can be manually entered here.<br><br> While you enter some "
        "text, the list is filtered for matching entries."
        '<br>If you for example type <span style="color: blue;">'
        '<i>X10.Red</i></span>, the list will be '
        'filtered for any matching <span style="color: blue;"><i>X10.Red</i>'
        '</span>, <span style="color: blue;"><i>X10</i></span> or '
        '<span style="color: blue;"><i>Red</i></span>. '
        "(The search string will only be splitted at the first '<b>.</b>' if "
        "there are more than one.)"
    )

    info = "Note: You can drag and drop events from the list to a macro."
    noMatch = "<no matching event>"
    unknown = "<unknown>"
    unknownDesc = (
        "Here you find events that are used in your configuration, but "
        "couldn't be associated with a plugin."
    )


class AddEventDialog(eg.TaskletDialog):
    @eg.LogItWithReturn
    def Configure(self, parent):
        self._allEventsData = {}
        self._allEventsDict = {}
        self._searchstring = ""
        self.resultData = ""
        super(AddEventDialog, self).__init__(
            parent=parent, id=wx.ID_ANY, title=Text.title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        panel = eg.AddEventPanel(self)
        self.tree = panel.tree
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL), True)
        info = eg.HeaderBox(
            parent=self,
            name=Text.info,
            icon=eg.Icons.INFO_ICON,
            url=None
        )

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(info, 0, wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALIGN_CENTER, 0),
        mainSizer.Add(panel, 1, wx.EXPAND)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(mainSizer)
        minSize = mainSizer.GetMinSize()
        self.SetMinSize(minSize)
        self.SetSize(Config.size)
        if Config.position is not None:
            self.SetPosition(Config.position)

        while self.Affirmed():
            self.SetResult(panel.resultData)

        Config.size = self.GetSizeTuple()
        Config.position = self.GetPositionTuple()

    def OnActivated(self, event):
        event.Skip()
        self.OnOK(event)

    def OnSelectionChanged(self, event):
        item = event.GetItem()
        if not item.IsOk():
            return
        data = self.tree.GetPyData(item)
        if isinstance(data, eg.EventInfo):
            self.buttonRow.okButton.Enable(True)
        elif isinstance(data, eg.PluginInstanceInfo):
            self.buttonRow.okButton.Enable(False)
        event.Skip()

