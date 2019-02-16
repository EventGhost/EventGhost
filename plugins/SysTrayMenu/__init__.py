# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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

import eg

eg.RegisterPlugin(
    name=u'System Tray Menu',
    description=u'Allows you to add custom menu entries '
                u'to the tray menu of EventGhost.',
    author=u'Bitmonster',
    version=u'1.1',
    guid=u'{842BFFE8-DCB9-4C72-9877-AB2EF49794C5}',
)

import wx
import wx.dataview


KIND_SEPARATOR = u'separator'
KIND_ITEM = u'item'


# noinspection PyClassHasNoInit
class Text:
    labelHeader = u'Label'
    eventHeader = u'Event'
    editLabel = u'Label:'
    editEvent = u'Event:'
    addBox = u'Append:'
    addItemButton = u'Menu Item'
    add_separator_button = u'Separator'
    deleteButton = u'Delete'
    invalid_menu = u'INVALID menu entry'
    unnamed_label = u'New Menu Item'
    unnamed_event = u'MenuItem_'


class MenuTreeListCtrl(wx.dataview.TreeListCtrl):

    def __init__(self, parent, text, menu_data, selected_item=None):
        wx.dataview.TreeListCtrl.__init__(
            self,
            parent,
            style=wx.dataview.TL_SINGLE
        )
        self.SetMinSize((10, 150))
        self.AppendColumn(text.labelHeader)
        self.AppendColumn(text.eventHeader)
        root = self.GetRootItem()
        for data in menu_data:
            name, kind, event_string, menu_id = data
            event_string = data[2]
            item = self.AppendItem(root, name)
            self.SetItemText(item, col=1, text=event_string)
            self.SetItemData(item, data)
            if menu_id == selected_item:
                self.Select(item)

        self.SetColumnWidth(0, 200)
        self.Expand(root)

    def ensure_visible(self):
        dv = self.GetDataView()
        item = dv.GetSelection()
        if item.IsOk():
            dv.EnsureVisible(item)

    def move_item_down(self, item):
        if not item.IsOk():
            return item
        next_item = self.GetNextItem(item)
        if not next_item.IsOk():
            return item
        data = self.GetItemData(item)
        cols_texts = []
        cnt = self.GetColumnCount()
        for col in range(cnt):
            cols_texts.append(self.GetItemText(item, col))
        self.Freeze()
        self.DeleteItem(item)
        item = self.InsertItem(
            parent=self.GetRootItem(),
            previous=next_item,
            text=cols_texts[0],
            data=data
        )
        for col in range(1, cnt):
            self.SetItemText(item, col, cols_texts[col])
        self.Select(item)
        self.Thaw()

    def move_item_up(self, item):
        if not item.IsOk():
            return item
        prev_item = self.get_previous_item(item)
        if not prev_item.IsOk():
            return item
        data = self.GetItemData(item)
        cols_texts = []
        cnt = self.GetColumnCount()
        for col in range(cnt):
            cols_texts.append(self.GetItemText(item, col))
        self.Freeze()
        self.DeleteItem(item)
        prev_item = self.get_previous_item(prev_item)
        if prev_item.IsOk():
            item = self.InsertItem(
                parent=self.GetRootItem(),
                previous=prev_item,
                text=cols_texts[0],
                data=data
            )
        else:
            item = self.PrependItem(
                parent=self.GetRootItem(),
                text=cols_texts[0],
                data=data
            )
        for col in range(1, cnt):
            self.SetItemText(item, col, cols_texts[col])
        self.Select(item)
        self.Thaw()

    def get_item_count(self):
        cnt = 0
        item = self.GetFirstChild(self.GetRootItem())
        while item.IsOk():
            cnt += 1
            item = self.GetNextItem(item)
        return cnt

    def get_previous_item(self, item):
        prev_child = self.GetFirstItem()
        if item == prev_child:
            return wx.dataview.TreeListItem()
        next_child = self.GetNextItem(prev_child)
        while next_child.IsOk():
            if item == next_child:
                return prev_child
            prev_child = next_child
            next_child = self.GetNextItem(prev_child)
        return wx.dataview.TreeListItem()

    def get_selected_id(self):
        item = self.GetSelection()
        if item.IsOk():
            data = self.GetItemData(item)
            if data:
                return data[3]
        return None


class SysTrayMenu(eg.PluginBase):
    text = Text

    def __init__(self):
        super(SysTrayMenu, self).__init__()
        self.AddAction(Enable)
        self.AddAction(Disable)
        self.menu_data = None
        self.tree = None

    def convert_data(self, menu_data=None):
        """ convert data from older format versions to actual format """
        if not menu_data:
            return None

        new_data = []
        for data in menu_data:
            if isinstance(data, tuple):
                data = list(data)
            if len(data) < 4 or not isinstance(data[3], str):
                # noinspection PyCallByClass,PyArgumentList
                data.append(str(eg.GUID.NewId(self)))
            new_data.append(data)
        return new_data

    @eg.LogIt
    def __start__(self, menu_data=None):
        self.menu_items = {}

        self.menu_data = menu_data = self.convert_data(menu_data)
        if not menu_data:
            return
        menu = eg.taskBarIcon.menu
        self.menu_items.update(
            {wx.NewIdRef(): [menu.PrependSeparator(), None]}
        )
        for data in reversed(menu_data):
            name, kind, event_string, menu_id = data
            if kind == KIND_ITEM:
                wx_id = wx.NewIdRef()
                self.menu_items.update(
                    {wx_id: [menu.Prepend(wx_id, name), data]}
                )
                menu.Bind(wx.EVT_MENU, self.on_menu_item, id=wx_id)
            elif kind == KIND_SEPARATOR:
                self.menu_items.update(
                    {wx.NewIdRef(): [menu.PrependSeparator(), None]}
                )

    def __stop__(self):
        for item in self.menu_items.itervalues():
            eg.taskBarIcon.menu.Unbind(wx.EVT_MENU, item[0])
            eg.taskBarIcon.menu.Remove(item[0])
            del item
        del self.menu_items

    @eg.LogIt
    def on_menu_item(self, event):
        self.TriggerEvent(self.menu_items[event.GetId()][1][2])

    def enable_menu(self, menu_id):
        for key, value in self.menu_items.iteritems():
            menu_item, data = value
            if not data:
                continue
            if menu_id == data[3]:
                menu_item.Enable()

    def disable_menu(self, menu_id):
        for key, value in self.menu_items.iteritems():
            menu_item, data = value
            if not data:
                continue
            if menu_id == data[3]:
                menu_item.Enable(False)

    # noinspection PyAttributeOutsideInit
    def Configure(self, menu_data=None):
        if menu_data is None:
            menu_data = []
        self.menu_data = menu_data = self.convert_data(menu_data)
        self.panel = panel = eg.ConfigPanel(resizable=True)
        text = self.text

        self.tree = tree = MenuTreeListCtrl(panel, text, menu_data)
        self.label_box = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.label_box.Disable()
        self.event_box = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.event_box.Disable()
        add_item_button = wx.Button(panel, wx.ID_ANY, text.addItemButton)
        add_separator_button = wx.Button(panel, wx.ID_ANY, text.add_separator_button)
        self.delete_button = wx.Button(panel, wx.ID_ANY, text.deleteButton)
        self.delete_button.Disable()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        self.down_button = wx.BitmapButton(panel, wx.ID_ANY, bmp)
        self.down_button.Enable(False)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        self.up_button = wx.BitmapButton(panel, wx.ID_ANY, bmp)
        self.up_button.Disable()

        tree.Bind(wx.dataview.EVT_TREELIST_SELECTION_CHANGED, self.on_selection_changed)
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete)
        self.up_button.Bind(wx.EVT_BUTTON, self.on_up)
        self.down_button.Bind(wx.EVT_BUTTON, self.on_down)
        add_item_button.Bind(wx.EVT_BUTTON, self.on_add_item)
        add_separator_button.Bind(wx.EVT_BUTTON, self.on_add_separator)
        self.label_box.Bind(wx.EVT_TEXT, self.on_label_text_change)
        self.event_box.Bind(wx.EVT_TEXT, self.on_event_text_change)

        static_box = wx.StaticBox(panel, wx.ID_ANY, text.addBox)
        add_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        add_sizer.Add(add_item_button, 0, wx.EXPAND)
        add_sizer.Add((5, 5))
        add_sizer.Add(add_separator_button, 0, wx.EXPAND)

        edit_sizer = wx.FlexGridSizer(2, 2, 5, 5)
        edit_sizer.AddMany((
            (panel.StaticText(text.editLabel), 0, wx.ALIGN_CENTER_VERTICAL),
            (self.label_box, 0, wx.EXPAND),
            (panel.StaticText(text.editEvent), 0, wx.ALIGN_CENTER_VERTICAL),
            (self.event_box, 0, wx.EXPAND),
        ))
        edit_sizer.AddGrowableCol(1)

        main_sizer = eg.HBoxSizer(
            (
                eg.VBoxSizer(
                    (tree, 1, wx.EXPAND),
                    (edit_sizer, 0, wx.EXPAND | wx.TOP, 5),
                ), 1, wx.EXPAND
            ),
            (wx.Size((5, 5))),
            (
                eg.VBoxSizer(
                    (self.delete_button, 0, wx.EXPAND),
                    ((5, 5), 1, wx.EXPAND),
                    (self.up_button, 0),
                    (self.down_button, 0, wx.TOP, 5),
                    ((5, 5), 1, wx.EXPAND),
                    (add_sizer, 0, wx.EXPAND),
                ), 0, wx.EXPAND
            ),
        )
        panel.sizer.Add(main_sizer, 1, wx.EXPAND)

        self.on_selection_changed()
        while panel.Affirmed():
            data = self.get_menu_data()
            panel.SetResult(data)

    def get_menu_data(self):
        tree = self.tree
        result_list = []
        item = tree.GetFirstChild(tree.GetRootItem())
        while item.IsOk():
            _, kind, _, menu_id = tree.GetItemData(item)
            name = tree.GetItemText(item, 0)
            event_string = tree.GetItemText(item, 1)
            result_list.append([name, kind, event_string, menu_id])
            item = tree.GetNextItem(item)
        self.menu_data = result_list
        return result_list

    # noinspection PyUnusedLocal
    @eg.LogIt
    def on_add_item(self, evt):
        tree = self.tree
        num_str = str(self.get_unnamed_count() + 1)
        # noinspection PyCallByClass,PyArgumentList
        data = (
            self.text.unnamed_label + num_str,
            KIND_ITEM,
            self.text.unnamed_event + num_str,
            str(eg.GUID.NewId(self))
        )
        item = tree.AppendItem(tree.GetRootItem(), data[0])
        tree.SetItemText(item, col=1, text=data[2])
        tree.SetItemData(item, data)
        tree.Select(item)
        tree.ensure_visible()
        self.panel.SetIsDirty()
        self.on_selection_changed()

    # noinspection PyUnusedLocal
    def on_add_separator(self, evt):
        tree = self.tree
        item = tree.AppendItem(tree.GetRootItem(), '---------')
        # noinspection PyCallByClass,PyArgumentList
        tree.SetItemData(
            item,
            ['', KIND_SEPARATOR, '', str(eg.GUID.NewId(self))]
        )
        tree.Select(item)
        tree.ensure_visible()
        self.panel.SetIsDirty()
        self.on_selection_changed()

    def get_unnamed_count(self):
        tree = self.tree
        child = tree.GetFirstChild(tree.GetRootItem())
        cnt = 0
        while child.IsOk():
            if tree.GetItemText(child).startswith(self.text.unnamed_label):
                cnt += 1
            child = tree.GetNextItem(child)
        return cnt

    def get_label_for_id(self, menu_id):
        for data in self.menu_data:
            if menu_id == data[3]:
                return data[0]
        return self.text.invalid_menu

    # noinspection PyUnusedLocal
    def on_down(self, evt):
        tree = self.tree
        item = tree.GetSelection()
        tree.move_item_down(item)
        tree.ensure_visible()

    # noinspection PyUnusedLocal
    def on_up(self, evt):
        tree = self.tree
        item = tree.GetSelection()
        tree.move_item_up(item)
        tree.ensure_visible()

    # noinspection PyUnusedLocal
    def on_delete(self, evt):
        tree = self.tree
        item = tree.GetSelection()
        if not item.IsOk():
            return
        next_item = tree.GetNextItem(item)
        if not next_item.IsOk():
            next_item = tree.get_previous_item(item)
        if item.IsOk():
            tree.Select(next_item)
        tree.DeleteItem(item)
        tree.ensure_visible()
        self.on_selection_changed()

    # noinspection PyUnusedLocal
    @eg.LogIt
    def on_selection_changed(self, evt=None):
        tree = self.tree
        item = tree.GetSelection()
        flag = item.IsOk()
        self.up_button.Enable(flag)
        self.down_button.Enable(flag)
        self.delete_button.Enable(flag)
        self.panel.EnableButtons(bool(tree.get_item_count()))
        if not flag or tree.GetItemData(item)[1] == KIND_SEPARATOR:
            # separator
            self.label_box.ChangeValue('')
            self.event_box.ChangeValue('')
            self.label_box.Disable()
            self.event_box.Disable()
        elif flag:
            # menu item
            self.label_box.ChangeValue(tree.GetItemText(item, 0))
            self.event_box.ChangeValue(tree.GetItemText(item, 1))
            self.label_box.Enable()
            self.event_box.Enable()

    def on_label_text_change(self, evt):
        item = self.tree.GetSelection()
        if item.IsOk():
            self.tree.SetItemText(item, col=0, text=evt.GetString())
        evt.Skip()

    def on_event_text_change(self, evt):
        item = self.tree.GetSelection()
        if item.IsOk():
            self.tree.SetItemText(item, col=1, text=evt.GetString())
        evt.Skip()


class Enable(eg.ActionBase):
    # noinspection PyClassHasNoInit,PyPep8Naming
    class text:
        name = u'Enable Item'
        description = u'Enables a menu item.'

    def __call__(self, menu_id):
        self.plugin.enable_menu(menu_id)

    def GetLabel(self, menu_id):
        return self.name + u': ' + self.plugin.get_label_for_id(menu_id)

    def Configure(self, menu_id=None):
        plugin = self.plugin
        # noinspection PyAttributeOutsideInit
        self.panel = panel = eg.ConfigPanel()
        tree = MenuTreeListCtrl(panel, plugin.text, plugin.menu_data, menu_id)
        tree.Bind(wx.dataview.EVT_TREELIST_SELECTION_CHANGED, self.on_selection_changed)
        panel.sizer.Add(tree, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(tree.get_selected_id())

    # noinspection PyUnusedLocal
    def on_selection_changed(self, evt):
        self.panel.SetIsDirty()


class Disable(eg.ActionBase):
    # noinspection PyClassHasNoInit,PyPep8Naming
    class text:
        name = u'Disable Item'
        description = u'Disables a menu item.'

    def __call__(self, menu_id):
        self.plugin.disable_menu(menu_id)

    def GetLabel(self, menu_id):
        return self.name + u': ' + self.plugin.get_label_for_id(menu_id)

    def Configure(self, menu_id=None):
        plugin = self.plugin
        # noinspection PyAttributeOutsideInit
        self.panel = panel = eg.ConfigPanel()
        tree = MenuTreeListCtrl(panel, plugin.text, plugin.menu_data, menu_id)
        tree.Bind(wx.dataview.EVT_TREELIST_SELECTION_CHANGED, self.on_selection_changed)
        panel.sizer.Add(tree, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(tree.get_selected_id())

    # noinspection PyUnusedLocal
    def on_selection_changed(self, evt):
        self.panel.SetIsDirty()
