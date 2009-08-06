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


class ToggleEnable:
    name = eg.text.MainFrame.Menu.Disabled.replace("&", "")

    def __init__(self, document, node):
        self.positionData = eg.TreePosition(node)
        self.state = not node.isEnabled
        node.SetEnable(self.state)
        eg.Notify("NodeChanged", node)
        document.AppendUndoHandler(self)


    def Undo(self, document):
        node = self.positionData.GetItem()
        node.SetEnable(not self.state)
        eg.Notify("NodeChanged", node)
        node.Select()


    def Redo(self, document):
        node = self.positionData.GetItem()
        node.SetEnable(self.state)
        eg.Notify("NodeChanged", node)
        node.Select()

