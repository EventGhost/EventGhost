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


class Cut:
    name = eg.text.MainFrame.Menu.Cut.replace("&", "")

    def __init__(self, document, selection):
        if not selection.CanDelete() or not selection.AskDelete():
            return
        self.data = selection.GetFullXml()
        self.positionData = eg.TreePosition(selection)
        document.AppendUndoHandler(self)
        selection.OnCmdCopy()
        selection.Delete()


    def Undo(self, document):
        item = document.RestoreItem(self.positionData, self.data)
        item.Select()


    def Redo(self, document):
        self.positionData.GetItem().Delete()

