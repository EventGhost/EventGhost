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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

__all__ = [
    "TreeItem", 
    "ContainerItem", 
    "EventItem", 
    "RootItem", 
    "MacroItem",
    "FolderItem", 
    "ActionItem", 
    "AutostartItem", 
    "PluginItem",
    "TreeLink",
]

from TreeItem import TreeItem
from ContainerItem import ContainerItem
from EventItem import EventItem
from ActionItem import ActionItem
from PluginItem import PluginItem
from RootItem import RootItem
from FolderItem import FolderItem
from MacroItem import MacroItem
from AutostartItem import AutostartItem
from TreeLink import TreeLink

__tmp = {
    "TreeItem": TreeItem,
    "ContainerItem": ContainerItem,
    "EventItem": EventItem,
    "ActionItem": ActionItem,
    "PluginItem": PluginItem,
    "RootItem": RootItem,
    "FolderItem": FolderItem,
    "MacroItem": MacroItem,
    "AutostartItem": AutostartItem,
    }

# insert all TreeItem classes into the modules as globals
import TreeItem as tmp
tmp.__dict__.update(__tmp)
import ContainerItem as tmp
tmp.__dict__.update(__tmp)
import EventItem as tmp
tmp.__dict__.update(__tmp)
import ActionItem as tmp
tmp.__dict__.update(__tmp)
import PluginItem as tmp
tmp.__dict__.update(__tmp)
import RootItem as tmp
tmp.__dict__.update(__tmp)
import FolderItem as tmp
tmp.__dict__.update(__tmp)
import MacroItem as tmp
tmp.__dict__.update(__tmp)
import AutostartItem as tmp
tmp.__dict__.update(__tmp)



