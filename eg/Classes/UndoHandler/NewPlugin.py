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

import threading
import wx
# Local imports
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

        def do(p_info, p_item):
            p_info.load_language_file(eg.config.language)

            if p_item.executable:
                if p_item.NeedsStartupConfiguration():
                    event = threading.Event()
                    res = []

                    def configure():
                        if not eg.UndoHandler.Configure(document).Do(p_item, True):
                            eg.actionThread.Call(p_item.Delete)
                            res.append(None)
                        event.set()

                    wx.CallAfter(configure)
                    event.wait()

                    if len(res):
                        return None

                eg.actionThread.Call(p_item.Execute)
            self.StoreItem(p_item)
            if pluginInfo.createMacrosOnAdd:
                eg.UndoHandler.AddActionGroup(document).Do(p_item)
            return pluginItem

        t = threading.Thread(target=do, args=(pluginInfo, pluginItem))
        t.daemon = True
        t.start()

