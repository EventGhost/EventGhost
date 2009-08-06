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
from ContainerItem import ContainerItem
from TreeItem import HINT_MOVE_EVERYWHERE, HINT_NO_DROP

class FolderItem(ContainerItem):
    xmlTag = "Folder"
    icon = eg.Icons.FOLDER_ICON

    def DropTest(self, cls):
        if cls == eg.MacroItem:
            return HINT_MOVE_EVERYWHERE
        if cls == eg.FolderItem:
            return HINT_MOVE_EVERYWHERE
        return HINT_NO_DROP

