# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
from NewItem import NewItem


class NewPlugin(NewItem):
    """
    Create a new PluginItem if the user has choosen to do so from the menu
    or toolbar.
    """
    name = eg.text.MainFrame.Menu.AddPlugin.replace("&", "")

    @eg.AssertInMainThread
    @eg.LogItWithReturn
    def Do(self, pluginInfo):
        document = self.document
        pluginItem = eg.actionThread.Func(document.PluginItem.Create)(
            document.autostartMacro,
            -1,
            file=pluginInfo.pluginName
        )
        pluginItem.Select()
        if pluginItem.executable:
            if pluginItem.NeedsStartupConfiguration():
                if not eg.UndoHandler.Configure(document).Do(pluginItem, True):
                    eg.actionThread.Call(pluginItem.Delete)
                    return None
            eg.actionThread.Call(pluginItem.Execute)
        self.StoreItem(pluginItem)
        if pluginInfo.createMacrosOnAdd:
            eg.UndoHandler.AddActionGroup(document).Do(pluginItem)
        return pluginItem

