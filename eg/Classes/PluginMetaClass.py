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

import sys

class PluginMetaClass(type):
    """
    The metaclass of PluginBase that allows us to monitor the definition of a
    new plugin.
    """
    lastCreatedCls = None
    
    def __new__(mcs, name, bases, dct):
        newClass = type.__new__(mcs, name, bases, dct)
        # store the plugin class as __pluginCls__ in the plugins module
        sys.modules[newClass.__module__].__pluginCls__ = newClass
        PluginMetaClass.lastCreatedCls = newClass
        return newClass

