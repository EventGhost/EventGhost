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

import sys

class PluginMetaClass(type):
    """
    The metaclass of PluginBase that allows us to monitor the definition of a
    new plugin.
    """

    def __new__(mcs, name, bases, dct):
        newClass = type.__new__(mcs, name, bases, dct)
        # store the plugin class as __pluginCls__ in the plugins module
        sys.modules[newClass.__module__].__pluginCls__ = newClass
        return newClass

