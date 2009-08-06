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

