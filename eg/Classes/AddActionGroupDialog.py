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
import wx


class Text(eg.TranslatableStrings):
    caption = "Add Actions?"
    message = (
        "EventGhost can add a folder with all actions of this plugin to your "
        "configuration tree. If you want to do so, select the location where "
        "it should be added and press OK.\n\n"
        "Otherwise press the cancel button."
    )



class AddActionGroupDialog(eg.TreeItemBrowseDialog):

    def Configure(self, parent=None):
        eg.TreeItemBrowseDialog.Configure(
            self,
            Text.caption,
            Text.message,
            searchItem=None,
            resultClasses=(eg.FolderItem, eg.RootItem),
            filterClasses=(eg.FolderItem, ),
            parent=parent,
        )

