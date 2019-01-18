# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2019 EventGhost Project <http://www.eventghost.org/>
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

MODULE_GLOBALS = globals()

class UndoHandler:
    def __getattr__(self, name):
        try:
            mod = __import__(name, MODULE_GLOBALS)
            attr = getattr(mod, name)
            self.__dict__[name] = attr
            return attr
        except ImportError:
            return self._EmptyNode

    def _EmptyNode(*args, **kwargs):
        return []

UndoHandler = UndoHandler()


class UndoHandlerBase(object):
    def __init__(self, document):
        self.document = document

    def Do(self, *args):
        raise NotImplementedError

    def Redo(self):
        raise NotImplementedError

    def Undo(self):
        raise NotImplementedError
