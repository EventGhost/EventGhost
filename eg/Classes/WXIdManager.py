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

import wx
import sys


class WXIdManager(object):
    """
    Convenience class for wxID's.

    This is an attribute only class. If the attribute name exists in wx as an
    id it will collect that id and set it into this class and return it. If it
    does not exist this class will generate a wxNewId and and set it then
    return it. Every time the same attribute name is used it will always
    return the same id.

    Example:
        widgetId = eg.WXIdManager.OK
            The above will grab the wx.ID_OK and return it.

        widgetId = eg.WXIdManager.SOME_ID
            The above will generate a new wxId and return it.
    """
    def __init__(self):
        self.__dict__ = sys.modules[__name__].__dict__
        self.__originalmodule__ = sys.modules[__name__]
        sys.modules[__name__] = self
        sys.modules[__name__ + '.' + __name__.split('.')[-1]] = self

    def __getitem__(self, item):
        return getattr(self, item.upper())

    def __getattr__(self, item):
        if item.startswith('_'):
            if item in self.__dict__:
                return self.__dict__[item]
            raise AttributeError(
                '%r does not have attribute %s' % (self, item)
            )

        item = item.upper()
        if hasattr(wx, 'ID_' + item):
            attr = getattr(wx, 'ID_' + item)
        else:
            attr = wx.NewId()
        setattr(self, item, attr)
        return attr

WXIdManager = WXIdManager()
