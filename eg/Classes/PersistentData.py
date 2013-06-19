# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2009-01-06 19:53:06 +0100 (Di, 06 Jan 2009) $
# $LastChangedRevision: 700 $
# $LastChangedBy: bitmonster $

import eg


class PersistentDataMeta(type):

    def __new__(mcs, name, bases, dct):
        cls = type.__new__(mcs, name, bases, dct)
        if len(bases):
            searchPath = dct["__module__"]
            config = eg.config
            parts = searchPath.split(".")
            for part in parts[:-1]:
                config = config.SetDefault(part, eg.Bunch)
            return config.SetDefault(parts[-1], cls)
        return cls



class PersistentData:
    __metaclass__ = PersistentDataMeta
    
    