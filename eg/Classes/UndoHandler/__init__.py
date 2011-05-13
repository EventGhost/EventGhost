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

MODULE_GLOBALS = globals()

class UndoHandler:

    def __getattr__(self, name):
        mod = __import__(name, MODULE_GLOBALS)
        attr = getattr(mod, name)
        self.__dict__[name] = attr
        return attr

UndoHandler = UndoHandler()


class UndoHandlerBase(object):

    def __init__(self, document):
        self.document = document

    def Do(self, *args):
        raise NotImplementedError

    def Undo(self):
        raise NotImplementedError

    def Redo(self):
        raise NotImplementedError

