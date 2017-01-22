# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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


from eg.Classes.UndoHandler import UndoHandlerBase


class PersistentData(UndoHandlerBase):
    _UndoHandlers = []

    def __init__(self, config):
        UndoHandlerBase.__init__(self, None)
        self.__class__._UndoHandlers.append(self)
        self.config = config
        self.flag = False
        self.Redo = self.Undo
        if config:
            config.SetDelete(False)

    def Undo(self):
        if self.config:
            self.flag = not self.flag
            self.config.SetDelete(self.flag)

    def Delete(self, flag):
        self.flag = flag
        if self.config:
            self.config.SetDelete(flag)

    def Remove(self):
        if self.config:
            del(self.config)
        self.__class__._UndoHandlers.remove(self)

    @classmethod
    def UndoAll(cls):
        for handler in cls._UndoHandlers:
            handler.Undo()

