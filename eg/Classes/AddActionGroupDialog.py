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

# Local imports
import eg

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
