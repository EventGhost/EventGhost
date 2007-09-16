# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2007-08-02 19:02:53 +0200 (Thu, 02 Aug 2007) $
# $LastChangedRevision: 198 $
# $LastChangedBy: bitmonster $

import wx
import eg

class Text:
    caption = "Add Actions?"
    message = (
        "EventGhost can add a folder with all actions of this plugin to your "
        "configuration tree. If you want to do so, select the location where "
        "it should be added and press OK.\n\n"
        "Otherwise press the cancel button."
    )

text = eg.GetTranslation(Text)


class AddActionGroupDialog(eg.TreeItemBrowseDialog):
    
    def __init__(self, parent=None):
        eg.TreeItemBrowseDialog.__init__(
            self, 
            text.caption,
            text.message,
            None,
            (eg.FolderItem, eg.RootItem),
            filterClasses=(eg.FolderItem, ),
            parent=parent,
        )
        
